"""Offline-first ResearchFlow pipeline.

The MVP uses deterministic local fixtures so the course demo remains stable.
Real API-backed tools can replace the search function without changing the
state and report contracts.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .evaluation import evaluate_state, render_evaluation_markdown
from .graph import NodeSpec, run_research_graph
from .llm import LLMError, build_llm_client
from .models import CitationCheck, ClaimRecord, EvidenceItem, PaperRecord, ResearchResult
from .offline_data import OFFLINE_PAPERS
from .planner import normalize_topic, plan_queries, topic_terms
from .report import render_process_markdown, render_report, render_summary_report
from .session import save_session
from .state import ResearchState
from .tools import (
    ArxivSearchError,
    CrossrefSearchError,
    SemanticScholarSearchError,
    search_arxiv,
    search_crossref,
    search_semantic_scholar,
)


RAG_TOPIC_PATTERNS = (
    "retrieval augmented generation",
    "retrieval-augmented generation",
    "rag",
)
RAG_TITLE_SIGNALS = (
    "survey",
    "review",
    "benchmark",
    "evaluation",
    "security",
    "secure",
    "threat",
    "defense",
    "taxonomy",
    "graphrag",
    "causalrag",
    "trustworthy",
    "robust",
)
RAG_SYSTEM_SIGNALS = (
    "retriever",
    "retrieval",
    "embedding",
    "vector",
    "knowledge base",
    "grounding",
    "hallucination",
    "context",
    "chunk",
    "rerank",
    "index",
)
RAG_DOMAIN_APP_SIGNALS = (
    "food",
    "nutrition",
    "milky way",
    "globular",
    "novice math",
    "bachelor project",
    "immunogenicity",
    "protein drugs",
    "metaverse",
    "turkish language",
    "urban studies",
    "traditional chinese",
    "corporate",
)
RAG_CORE_METHOD_SIGNALS = (
    "survey",
    "review",
    "benchmark",
    "evaluation",
    "taxonomy",
    "method",
    "architecture",
    "framework",
    "system",
    "agentic",
    "graph",
    "faithful",
    "adaptive",
    "robust",
    "security",
    "retriever",
    "rerank",
)
RAG_LENS_DIMENSIONS: dict[str, tuple[str, ...]] = {
    "Survey & Taxonomy": ("survey", "review", "taxonomy", "sok", "systematic"),
    "Retrieval & Indexing": (
        "retrieval",
        "retriever",
        "embedding",
        "vector",
        "index",
        "search",
        "knowledge base",
        "corpus",
    ),
    "Generation & Grounding": (
        "generation",
        "grounded",
        "grounding",
        "context",
        "hallucination",
        "faithfulness",
        "answer",
    ),
    "Evaluation & Benchmarks": ("evaluation", "benchmark", "metric", "dataset", "test"),
    "Security & Robustness": (
        "security",
        "secure",
        "attack",
        "threat",
        "poisoning",
        "adversarial",
        "privacy",
        "defense",
        "robust",
    ),
    "Graph & Structured RAG": (
        "graph",
        "graphrag",
        "causalrag",
        "knowledge graph",
        "hypergraph",
        "structured",
    ),
    "Domain Applications": (
        "recommendation",
        "assistant",
        "education",
        "health",
        "nutrition",
        "science",
        "domain",
        "application",
    ),
}
DEFAULT_CANDIDATE_MULTIPLIER = 8
DEFAULT_FROM_YEAR = 2020
DEFAULT_LLM_BATCH_CHARS = 9000
LIVE_QUERY_PLAN_LIMIT = 6


def slugify(value: str, max_length: int = 48) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return (slug[:max_length].strip("-") or "research-task")


def make_task_id(topic: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{stamp}-{slugify(topic, 32)}"


def is_rag_topic(topic: str) -> bool:
    normalized = topic.lower()
    return any(pattern in normalized for pattern in RAG_TOPIC_PATTERNS)


def score_paper(paper: PaperRecord, terms: list[str], topic: str = "") -> float:
    title = paper.title.lower()
    abstract = paper.abstract.lower()
    term_score = 0.0
    for term in terms:
        clean_term = term.lower()
        if clean_term in title:
            term_score += 3.0
        if clean_term in abstract:
            term_score += 1.0
    recency_score = max(0, paper.year - 2020) * 0.08
    citation_score = min(paper.citation_count, 100) / 100
    score = term_score + recency_score + citation_score

    if is_rag_topic(topic):
        combined = f"{title} {abstract}"
        if "retrieval-augmented generation" in title or "retrieval augmented generation" in title:
            score += 8.0
        elif "retrieval-augmented generation" in abstract or "retrieval augmented generation" in abstract:
            score += 3.0
        if re.search(r"\brag\b", title):
            score += 6.0
        elif re.search(r"\brag\b", abstract):
            score += 2.0
        score += sum(2.0 for signal in RAG_TITLE_SIGNALS if signal in title)
        score += min(4.0, sum(0.5 for signal in RAG_SYSTEM_SIGNALS if signal in combined))
        has_core_method_signal = any(signal in title for signal in RAG_CORE_METHOD_SIGNALS)
        has_domain_drift = any(signal in title for signal in RAG_DOMAIN_APP_SIGNALS)
        if has_domain_drift and not has_core_method_signal:
            score -= 7.0
        if re.search(r"\bfor\b", title) and not has_core_method_signal:
            score -= 4.0
        if paper.source == "crossref" and has_domain_drift and not has_core_method_signal:
            score -= 2.0
    return max(0.0, score)


def search_offline(topic: str, limit: int = 20) -> list[PaperRecord]:
    terms = topic_terms(topic)
    scored = []
    for paper in OFFLINE_PAPERS:
        score = score_paper(paper, terms, topic=topic)
        clone = PaperRecord(**{**paper.to_dict(), "score": score})
        scored.append(clone)
    scored.sort(key=lambda item: (item.score, item.year, item.citation_count), reverse=True)
    return scored[:limit]


def normalize_from_year(from_year: int | None) -> int | None:
    if from_year is None or from_year <= 0:
        return None
    return from_year


def candidate_limit_for(top_k: int, candidate_multiplier: int, max_candidates: int | None) -> int:
    if max_candidates is not None and max_candidates > 0:
        return max(top_k, max_candidates)
    multiplier = max(1, candidate_multiplier)
    return max(top_k, min(200, top_k * multiplier))


def filter_papers_by_year(papers: list[PaperRecord], from_year: int | None) -> list[PaperRecord]:
    normalized_year = normalize_from_year(from_year)
    if normalized_year is None:
        return papers
    return [
        paper
        for paper in papers
        if not paper.year or paper.year >= normalized_year
    ]


def dedupe_papers(papers: list[PaperRecord]) -> list[PaperRecord]:
    seen: set[str] = set()
    unique: list[PaperRecord] = []
    for paper in papers:
        key, title_key = paper_dedupe_keys(paper)
        if title_key and title_key in seen:
            continue
        if key in seen:
            continue
        seen.add(key)
        if title_key:
            seen.add(title_key)
        unique.append(paper)
    return unique


def paper_dedupe_keys(paper: PaperRecord) -> tuple[str, str]:
    title_key = re.sub(r"\W+", "", paper.title.lower())
    key = paper.doi or paper.arxiv_id or paper.paper_id or paper.url or title_key
    return key, title_key


def balanced_merge_papers(source_groups: list[list[PaperRecord]], limit: int) -> list[PaperRecord]:
    """Round-robin sources so hybrid search is not dominated by the first source."""

    seen: set[str] = set()
    merged: list[PaperRecord] = []
    max_len = max((len(group) for group in source_groups), default=0)
    for index in range(max_len):
        for group in source_groups:
            if index >= len(group):
                continue
            paper = group[index]
            key, title_key = paper_dedupe_keys(paper)
            if key in seen or (title_key and title_key in seen):
                continue
            seen.add(key)
            if title_key:
                seen.add(title_key)
            merged.append(paper)
            if len(merged) >= limit:
                return merged
    return merged


def _search_arxiv_queries(query_plan: list[Any], limit: int) -> tuple[list[PaperRecord], list[str]]:
    collected: list[PaperRecord] = []
    errors: list[str] = []
    for query in query_plan[:LIVE_QUERY_PLAN_LIMIT]:
        try:
            collected.extend(search_arxiv(query.query_text, limit=limit))
        except ArxivSearchError as exc:
            errors.append(str(exc))
    return collected, errors


def _search_semantic_scholar_queries(
    query_plan: list[Any],
    limit: int,
) -> tuple[list[PaperRecord], list[str]]:
    collected: list[PaperRecord] = []
    errors: list[str] = []
    for query in query_plan[:LIVE_QUERY_PLAN_LIMIT]:
        try:
            collected.extend(search_semantic_scholar(query.query_text, limit=limit))
        except SemanticScholarSearchError as exc:
            errors.append(str(exc))
    return collected, errors


def _search_crossref_queries(
    query_plan: list[Any],
    limit: int,
    from_year: int | None = None,
) -> tuple[list[PaperRecord], list[str]]:
    collected: list[PaperRecord] = []
    errors: list[str] = []
    for query in query_plan[:LIVE_QUERY_PLAN_LIMIT]:
        try:
            collected.extend(search_crossref(query.query_text, limit=limit, from_year=from_year))
        except CrossrefSearchError as exc:
            errors.append(str(exc))
    return collected, errors


def search_source(
    topic: str,
    query_plan: list[Any],
    source: str,
    limit: int,
) -> tuple[list[PaperRecord], str, str | None]:
    """Search papers from the requested source with offline fallback."""

    if source == "offline":
        return search_offline(topic, limit=limit), "offline", None

    if source == "arxiv":
        collected, errors = _search_arxiv_queries(query_plan, limit)
        unique = dedupe_papers(collected)
        if unique:
            return unique[:limit], "arxiv", None
        fallback_reason = "; ".join(errors) or "arXiv returned no papers."
        return search_offline(topic, limit=limit), "offline", fallback_reason

    if source == "semantic_scholar":
        collected, errors = _search_semantic_scholar_queries(query_plan, limit)
        unique = dedupe_papers(collected)
        if unique:
            return unique[:limit], "semantic_scholar", None
        fallback_reason = "; ".join(errors) or "Semantic Scholar returned no papers."
        return search_offline(topic, limit=limit), "offline", fallback_reason

    if source == "crossref":
        from_year = None
        if query_plan:
            filters = getattr(query_plan[0], "filters", {})
            if isinstance(filters, dict):
                from_year = filters.get("from_year")
        collected, errors = _search_crossref_queries(query_plan, limit, from_year=from_year)
        unique = dedupe_papers(collected)
        if unique:
            return unique[:limit], "crossref", None
        fallback_reason = "; ".join(errors) or "Crossref returned no papers."
        return search_offline(topic, limit=limit), "offline", fallback_reason

    if source == "hybrid":
        arxiv_papers, arxiv_errors = _search_arxiv_queries(query_plan, limit)
        semantic_papers, semantic_errors = _search_semantic_scholar_queries(query_plan, limit)
        from_year = None
        if query_plan:
            filters = getattr(query_plan[0], "filters", {})
            if isinstance(filters, dict):
                from_year = filters.get("from_year")
        crossref_papers, crossref_errors = _search_crossref_queries(
            query_plan,
            limit,
            from_year=from_year,
        )
        unique = balanced_merge_papers(
            [
                dedupe_papers(arxiv_papers),
                dedupe_papers(semantic_papers),
                dedupe_papers(crossref_papers),
            ],
            limit=limit,
        )
        if unique:
            return unique[:limit], "hybrid", None
        errors = arxiv_errors + semantic_errors + crossref_errors
        fallback_reason = "; ".join(errors) or "Hybrid search returned no papers."
        return search_offline(topic, limit=limit), "offline", fallback_reason

    fallback_reason = f"Source '{source}' is not implemented; offline fallback used."
    return search_offline(topic, limit=limit), "offline", fallback_reason


def search_selected_sources(
    topic: str,
    query_plan: list[Any],
    sources: list[str],
    limit: int,
) -> tuple[list[PaperRecord], str, str | None]:
    """Search a user-selected source set and merge results fairly."""

    normalized_sources: list[str] = []
    for source in sources:
        normalized = source.replace("-", "_")
        if normalized == "hybrid":
            normalized_sources.extend(["arxiv", "semantic_scholar", "crossref"])
        elif normalized in {"offline", "arxiv", "semantic_scholar", "crossref"}:
            normalized_sources.append(normalized)

    if not normalized_sources:
        normalized_sources = ["offline"]

    normalized_sources = list(dict.fromkeys(normalized_sources))
    if len(normalized_sources) == 1:
        return search_source(topic, query_plan, normalized_sources[0], limit)

    source_groups: list[list[PaperRecord]] = []
    actual_sources: list[str] = []
    errors: list[str] = []

    if "offline" in normalized_sources:
        source_groups.append(search_offline(topic, limit=limit))
        actual_sources.append("offline")

    if "arxiv" in normalized_sources:
        papers, source_errors = _search_arxiv_queries(query_plan, limit)
        unique = dedupe_papers(papers)
        if unique:
            source_groups.append(unique)
            actual_sources.append("arxiv")
        else:
            errors.extend(source_errors or ["arXiv returned no papers."])

    if "semantic_scholar" in normalized_sources:
        papers, source_errors = _search_semantic_scholar_queries(query_plan, limit)
        unique = dedupe_papers(papers)
        if unique:
            source_groups.append(unique)
            actual_sources.append("semantic_scholar")
        else:
            errors.extend(source_errors or ["Semantic Scholar returned no papers."])

    if "crossref" in normalized_sources:
        from_year = None
        if query_plan:
            filters = getattr(query_plan[0], "filters", {})
            if isinstance(filters, dict):
                from_year = filters.get("from_year")
        papers, source_errors = _search_crossref_queries(query_plan, limit, from_year=from_year)
        unique = dedupe_papers(papers)
        if unique:
            source_groups.append(unique)
            actual_sources.append("crossref")
        else:
            errors.extend(source_errors or ["Crossref returned no papers."])

    if source_groups:
        merged = balanced_merge_papers(source_groups, limit=limit)
        live_sources = {"arxiv", "semantic_scholar", "crossref"}
        actual_label = "+".join(actual_sources)
        if set(normalized_sources) == live_sources and set(actual_sources) == live_sources:
            actual_label = "hybrid"
        return merged, actual_label, "; ".join(errors) or None

    fallback_reason = "; ".join(errors) or "Selected live sources returned no papers."
    return search_offline(topic, limit=limit), "offline", fallback_reason


def rank_papers(papers: list[PaperRecord], topic: str, top_k: int) -> list[PaperRecord]:
    return rank_all_papers(papers, topic)[:top_k]


def rank_all_papers(papers: list[PaperRecord], topic: str) -> list[PaperRecord]:
    terms = topic_terms(topic)
    seen: set[str] = set()
    ranked: list[PaperRecord] = []
    for paper in sorted(
        papers,
        key=lambda item: (score_paper(item, terms, topic=topic), item.year, item.citation_count),
        reverse=True,
    ):
        if paper.paper_id in seen:
            continue
        seen.add(paper.paper_id)
        paper.score = score_paper(paper, terms, topic=topic)
        ranked.append(paper)
    return ranked


def build_temporal_profile(papers: list[PaperRecord]) -> dict[str, Any]:
    years = [paper.year for paper in papers if paper.year > 0]
    if not years:
        return {
            "year_counts": {},
            "earliest_year": None,
            "latest_year": None,
            "last_3_year_count": 0,
            "last_5_year_count": 0,
            "last_3_year_ratio": 0.0,
            "last_5_year_ratio": 0.0,
        }

    current_year = datetime.now(timezone.utc).year
    year_counts: dict[int, int] = {}
    for year in years:
        year_counts[year] = year_counts.get(year, 0) + 1
    last_3_year_count = sum(1 for year in years if year >= current_year - 2)
    last_5_year_count = sum(1 for year in years if year >= current_year - 4)
    return {
        "year_counts": dict(sorted(year_counts.items())),
        "earliest_year": min(years),
        "latest_year": max(years),
        "last_3_year_count": last_3_year_count,
        "last_5_year_count": last_5_year_count,
        "last_3_year_ratio": round(last_3_year_count / len(years), 3),
        "last_5_year_ratio": round(last_5_year_count / len(years), 3),
    }


def classify_lens_dimensions(paper: PaperRecord) -> list[str]:
    haystack = f"{paper.title} {paper.abstract}".lower()
    dimensions = [
        dimension
        for dimension, keywords in RAG_LENS_DIMENSIONS.items()
        if any(keyword in haystack for keyword in keywords)
    ]
    return dimensions or ["Unclassified"]


def build_research_lens(topic: str, papers: list[PaperRecord]) -> dict[str, Any]:
    if not is_rag_topic(topic):
        return {}

    paper_profiles = [
        {
            "paper_id": paper.paper_id,
            "title": paper.title,
            "dimensions": classify_lens_dimensions(paper),
        }
        for paper in papers
    ]
    dimension_counts: dict[str, int] = {}
    for profile in paper_profiles:
        for dimension in profile["dimensions"]:
            if dimension == "Unclassified":
                continue
            dimension_counts[dimension] = dimension_counts.get(dimension, 0) + 1

    expected_dimensions = list(RAG_LENS_DIMENSIONS)
    missing_dimensions = [
        dimension for dimension in expected_dimensions if dimension not in dimension_counts
    ]
    coverage = len(dimension_counts) / max(len(expected_dimensions), 1)
    return {
        "lens_name": "RAG Research Lens",
        "description": (
            "A domain-aware lens that checks whether selected RAG papers cover survey, "
            "retrieval, grounding, evaluation, security, structured RAG, and applications."
        ),
        "dimension_counts": dimension_counts,
        "coverage": round(coverage, 3),
        "missing_dimensions": missing_dimensions,
        "paper_profiles": paper_profiles,
    }


def build_corpus_profile(
    topic: str,
    candidate_papers: list[PaperRecord],
    selected_papers: list[PaperRecord],
    from_year: int | None,
) -> dict[str, Any]:
    return {
        "candidate_count": len(candidate_papers),
        "selected_count": len(selected_papers),
        "from_year": normalize_from_year(from_year),
        "temporal_profile": build_temporal_profile(candidate_papers),
        "candidate_lens": build_research_lens(topic, candidate_papers),
        "selected_lens": build_research_lens(topic, selected_papers),
        "compression_strategy": [
            "Retrieve a broad candidate pool before ranking.",
            "Use temporal profiling to expose whether the review is recent enough.",
            "Map the candidate pool to domain dimensions before writing conclusions.",
            "Extract evidence from selected papers in LLM-sized batches.",
            "Keep claim-evidence-citation links as the auditable final surface.",
        ],
    }


def extract_evidence(papers: list[PaperRecord]) -> list[EvidenceItem]:
    evidence_items: list[EvidenceItem] = []
    for paper_index, paper in enumerate(papers, start=1):
        prefix = f"e{paper_index}"
        evidence_items.extend(
            [
                EvidenceItem(
                    evidence_id=f"{prefix}-contribution",
                    paper_id=paper.paper_id,
                    category="contribution",
                    claim=f"{paper.title} contributes evidence about {paper.abstract.split('.')[0].lower()}.",
                    support_text=paper.abstract,
                    confidence=0.78,
                ),
                EvidenceItem(
                    evidence_id=f"{prefix}-limitation",
                    paper_id=paper.paper_id,
                    category="limitation",
                    claim=(
                        "The current MVP only sees metadata and abstracts, so full-text validation "
                        f"is still needed for {paper.title}."
                    ),
                    support_text=paper.abstract,
                    confidence=0.62,
                ),
            ]
        )
    return evidence_items


def _clamp_confidence(value: Any) -> float:
    try:
        confidence = float(value)
    except (TypeError, ValueError):
        return 0.65
    return max(0.0, min(1.0, confidence))


def _paper_payload(paper: PaperRecord) -> dict[str, Any]:
    return {
            "paper_id": paper.paper_id,
            "title": paper.title,
            "authors": paper.authors,
            "year": paper.year,
            "abstract": paper.abstract,
    }


def _clean_llm_text(value: Any, max_length: int = 180) -> str:
    text = normalize_topic(str(value or ""))
    if len(text) > max_length:
        return text[:max_length].rstrip()
    return text


def _clean_llm_list(value: Any, max_items: int, max_length: int = 140) -> list[str]:
    if not isinstance(value, list):
        return []
    cleaned: list[str] = []
    seen: set[str] = set()
    for item in value:
        text = _clean_llm_text(item, max_length=max_length)
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(text)
        if len(cleaned) >= max_items:
            break
    return cleaned


def refine_topic_with_llm(topic: str, provider: str) -> dict[str, Any]:
    """Use an optional LLM to turn a fuzzy topic into a searchable review scope."""

    client = build_llm_client(provider)
    system_prompt = (
        "You help a literature-review agent clarify vague research topics before search. "
        "Return only a JSON object with keys refined_topic, research_questions, "
        "adjacent_topics, query_hints, and scope_notes. refined_topic must be a concise "
        "English academic search topic. research_questions should be 3-5 questions. "
        "adjacent_topics should contain 2-3 related but not identical angles worth checking. "
        "query_hints should contain 3-5 search queries. Do not include citations, URLs, "
        "paper titles, or hidden reasoning."
    )
    payload = client.generate_json(
        system_prompt,
        {
            "raw_topic": topic,
            "task": "Refine the topic for broad, authoritative literature search.",
        },
    )
    refined_topic = _clean_llm_text(payload.get("refined_topic"), max_length=160)
    if len(refined_topic) < 4:
        raise LLMError("LLM topic refinement did not return a usable refined_topic.")

    return {
        "original_topic": normalize_topic(topic),
        "refined_topic": refined_topic,
        "research_questions": _clean_llm_list(payload.get("research_questions"), max_items=5),
        "adjacent_topics": _clean_llm_list(payload.get("adjacent_topics"), max_items=3),
        "query_hints": _clean_llm_list(payload.get("query_hints"), max_items=5),
        "scope_notes": _clean_llm_text(payload.get("scope_notes"), max_length=260),
    }


def chunk_papers_for_llm(
    papers: list[PaperRecord],
    max_batch_chars: int = DEFAULT_LLM_BATCH_CHARS,
) -> list[list[PaperRecord]]:
    """Split papers into prompt-sized batches to avoid context window pressure."""

    if not papers:
        return []
    batches: list[list[PaperRecord]] = []
    current: list[PaperRecord] = []
    current_chars = 0
    budget = max(1200, max_batch_chars)

    for paper in papers:
        estimated_chars = len(paper.title) + len(paper.abstract) + 160
        if current and current_chars + estimated_chars > budget:
            batches.append(current)
            current = []
            current_chars = 0
        current.append(paper)
        current_chars += estimated_chars

    if current:
        batches.append(current)
    return batches


def _parse_llm_evidence_items(
    raw_items: Any,
    papers: list[PaperRecord],
    counters: dict[str, int],
) -> list[EvidenceItem]:
    if not isinstance(raw_items, list):
        raise LLMError("LLM JSON missing evidence_items list.")

    allowed_papers = {paper.paper_id for paper in papers}
    evidence_items: list[EvidenceItem] = []
    for raw in raw_items:
        if not isinstance(raw, dict):
            continue
        paper_id = str(raw.get("paper_id", ""))
        if paper_id not in allowed_papers:
            continue
        category = str(raw.get("category", "contribution")).strip() or "contribution"
        claim = str(raw.get("claim", "")).strip()
        support_text = str(raw.get("support_text", "")).strip()
        if not claim or not support_text:
            continue
        counters[paper_id] = counters.get(paper_id, 0) + 1
        evidence_items.append(
            EvidenceItem(
                evidence_id=f"llm-{slugify(paper_id, 18)}-{counters[paper_id]}",
                paper_id=paper_id,
                category=category,
                claim=claim,
                support_text=support_text,
                confidence=_clamp_confidence(raw.get("confidence", 0.72)),
            )
        )
    return evidence_items


def extract_evidence_with_llm(
    papers: list[PaperRecord],
    provider: str,
    max_batch_chars: int = DEFAULT_LLM_BATCH_CHARS,
) -> tuple[list[EvidenceItem], int]:
    client = build_llm_client(provider)
    system_prompt = (
        "You extract evidence for a literature review agent. Return only a JSON object "
        "with key evidence_items. Each item must use a paper_id from the input and include "
        "category, claim, support_text, and confidence. Use categories contribution, method, "
        "experiment, limitation, or future_work. Do not invent papers or references."
    )
    evidence_items: list[EvidenceItem] = []
    counters: dict[str, int] = {}
    batches = chunk_papers_for_llm(papers, max_batch_chars=max_batch_chars)
    for batch_index, batch in enumerate(batches, start=1):
        payload = client.generate_json(
            system_prompt,
            {
                "batch_index": batch_index,
                "batch_count": len(batches),
                "papers": [_paper_payload(paper) for paper in batch],
            },
        )
        evidence_items.extend(
            _parse_llm_evidence_items(payload.get("evidence_items"), batch, counters)
        )

    if not evidence_items:
        raise LLMError("LLM did not produce usable evidence items.")
    return evidence_items, len(batches)


def polish_background_with_llm(
    topic: str,
    report_markdown: str,
    selected_papers: list[PaperRecord],
    provider: str,
) -> str:
    client = build_llm_client(provider)
    system_prompt = (
        "You polish only the Research Background paragraph for a literature review report. "
        "Return a JSON object with key research_background. Do not add citations, URLs, "
        "paper IDs, evidence IDs, or references. Keep it concise and factual."
    )
    payload = client.generate_json(
        system_prompt,
        {
            "topic": topic,
            "selected_papers": [
                {"title": paper.title, "year": paper.year, "abstract": paper.abstract}
                for paper in selected_papers
            ],
        },
    )
    paragraph = str(payload.get("research_background", "")).strip()
    if not paragraph:
        raise LLMError("LLM did not return research_background.")
    if "http" in paragraph or "[P" in paragraph or "evidence_id" in paragraph:
        raise LLMError("LLM background attempted to add citations or evidence IDs.")

    start_marker = "## 1. Research Background\n\n"
    end_marker = "\n\n## 2. Core Papers"
    start = report_markdown.find(start_marker)
    end = report_markdown.find(end_marker)
    if start == -1 or end == -1 or end <= start:
        raise LLMError("Report structure does not support background polish.")
    prefix = report_markdown[: start + len(start_marker)]
    suffix = report_markdown[end:]
    return f"{prefix}{paragraph}{suffix}"


def synthesize_claims(topic: str, evidence_items: list[EvidenceItem]) -> list[ClaimRecord]:
    contribution_ids = [
        item.evidence_id
        for item in evidence_items
        if item.category in {"contribution", "method", "experiment"}
    ][:4]
    if not contribution_ids:
        contribution_ids = [item.evidence_id for item in evidence_items[:4]]
    limitation_ids = [
        item.evidence_id
        for item in evidence_items
        if item.category in {"limitation", "future_work"}
    ][:3]
    if not limitation_ids:
        limitation_ids = [item.evidence_id for item in evidence_items[-3:]]
    claims = [
        ClaimRecord(
            claim_id="c1",
            claim_text=(
                f"Research on {topic} is moving from single-step generation toward "
                "tool-using, evidence-grounded workflows."
            ),
            claim_type="Synthesis",
            evidence_ids=contribution_ids,
        ),
        ClaimRecord(
            claim_id="c2",
            claim_text=(
                "A promising research gap is to make the literature review process "
                "auditable through claim-evidence alignment and citation checking."
            ),
            claim_type="Hypothesis",
            evidence_ids=limitation_ids,
        ),
    ]
    return claims


def check_citations(papers: list[PaperRecord], claims: list[ClaimRecord]) -> list[CitationCheck]:
    checks: list[CitationCheck] = []
    paper_ids = {paper.paper_id for paper in papers}
    evidence_ids = {
        evidence_id
        for claim in claims
        for evidence_id in claim.evidence_ids
        if evidence_id
    }
    for index, paper in enumerate(papers, start=1):
        if not paper.title or not paper.url:
            status = "failed"
            message = "Missing title or URL."
        elif paper.paper_id not in paper_ids:
            status = "failed"
            message = "Paper not found in selected set."
        elif not (paper.doi or paper.arxiv_id or paper.url):
            status = "warning"
            message = "No DOI or arXiv ID; URL is used as fallback."
        else:
            status = "passed"
            message = "Citation metadata is available."
        checks.append(
            CitationCheck(
                check_id=f"check-{index}",
                paper_id=paper.paper_id,
                status=status,  # type: ignore[arg-type]
                message=message,
            )
        )

    unsupported_claims = [claim.claim_id for claim in claims if not claim.evidence_ids]
    if unsupported_claims:
        checks.append(
            CitationCheck(
                check_id="check-claims",
                paper_id="claims",
                status="failed",
                message=f"Unsupported claims: {', '.join(unsupported_claims)}",
            )
        )
    missing_evidence = [
        claim.claim_id
        for claim in claims
        if any(not evidence_id for evidence_id in claim.evidence_ids)
    ]
    if missing_evidence:
        checks.append(
            CitationCheck(
                check_id="check-evidence-links",
                paper_id="claims",
                status="failed",
                message=f"Claims contain empty evidence IDs: {', '.join(missing_evidence)}",
            )
        )
    if claims and not evidence_ids:
        checks.append(
            CitationCheck(
                check_id="check-evidence-ledger",
                paper_id="claims",
                status="failed",
                message="No claim-evidence links were produced.",
            )
        )
    return checks


def _serialize(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return value.to_dict()
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: _serialize(item) for key, item in value.items()}
    return value


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def node_plan_queries(state: ResearchState) -> dict[str, Any]:
    requested_source = state["requested_source"]
    effective_topic = state["topic"]
    refinement: dict[str, Any] = {
        "original_topic": state["topic"],
        "refined_topic": "",
        "research_questions": [],
        "adjacent_topics": [],
        "query_hints": [],
        "scope_notes": "",
    }
    refinement_used = False
    refinement_fallback_reason = ""

    if state.get("refine_topic"):
        provider = state.get("llm_provider", "off")
        if provider != "deepseek":
            refinement_fallback_reason = "Topic refinement requires --llm deepseek."
        else:
            try:
                refinement = refine_topic_with_llm(state["topic"], provider=provider)
                effective_topic = refinement["refined_topic"]
                refinement_used = True
            except LLMError as exc:
                refinement_fallback_reason = str(exc)

    query_plan = plan_queries(
        effective_topic,
        source=requested_source,
        adjacent_topics=refinement.get("adjacent_topics", []),
        query_hints=refinement.get("query_hints", []),
        from_year=int(state.get("from_year") or DEFAULT_FROM_YEAR),
    )
    return {
        "effective_topic": effective_topic,
        "refined_topic": refinement.get("refined_topic", "") if refinement_used else "",
        "topic_refinement": refinement,
        "topic_refinement_used": refinement_used,
        "topic_refinement_fallback_reason": refinement_fallback_reason,
        "query_plan": query_plan,
    }


def node_search_papers(state: ResearchState) -> dict[str, Any]:
    raw_papers, actual_source, fallback_reason = search_selected_sources(
        topic=state.get("effective_topic", state["topic"]),
        query_plan=state["query_plan"],
        sources=state.get("selected_sources", [state["requested_source"]]),
        limit=int(state.get("candidate_limit", max(int(state["top_k"]) * 4, 10))),
    )
    searched_papers = filter_papers_by_year(raw_papers, state.get("from_year"))
    if raw_papers and not searched_papers:
        searched_papers = raw_papers
        year_note = (
            f"Year filter from_year={state.get('from_year')} removed all candidates; "
            "unfiltered candidates were kept."
        )
        fallback_reason = f"{fallback_reason}; {year_note}" if fallback_reason else year_note
    return {
        "searched_papers": searched_papers,
        "actual_source": actual_source,
        "fallback_reason": fallback_reason or "",
        "temporal_profile": build_temporal_profile(searched_papers),
    }


def node_rank_papers(state: ResearchState) -> dict[str, Any]:
    effective_topic = state.get("effective_topic", state["topic"])
    ranked_candidates = rank_all_papers(state["searched_papers"], effective_topic)
    selected_papers = ranked_candidates[: int(state["top_k"])]
    return {
        "ranked_candidates": ranked_candidates,
        "selected_papers": selected_papers,
        "research_lens": build_research_lens(effective_topic, selected_papers),
        "corpus_profile": build_corpus_profile(
            effective_topic,
            ranked_candidates,
            selected_papers,
            state.get("from_year"),
        ),
    }


def node_extract_evidence(state: ResearchState) -> dict[str, Any]:
    provider = state.get("llm_provider", "off")
    if provider == "deepseek":
        try:
            evidence_items, chunk_count = extract_evidence_with_llm(
                state["selected_papers"],
                provider=provider,
            )
            return {
                "evidence_items": evidence_items,
                "llm_chunk_count": chunk_count,
                "llm_used": True,
                "llm_fallback_reason": "",
            }
        except LLMError as exc:
            return {
                "evidence_items": extract_evidence(state["selected_papers"]),
                "llm_chunk_count": 0,
                "llm_used": False,
                "llm_fallback_reason": str(exc),
            }
    return {
        "evidence_items": extract_evidence(state["selected_papers"]),
        "llm_chunk_count": 0,
        "llm_used": False,
        "llm_fallback_reason": "LLM provider is disabled.",
    }


def node_synthesize_claims(state: ResearchState) -> dict[str, Any]:
    return {
        "claims": synthesize_claims(
            state.get("effective_topic", state["topic"]),
            state["evidence_items"],
        )
    }


def node_check_citations(state: ResearchState) -> dict[str, Any]:
    return {"citation_checks": check_citations(state["selected_papers"], state["claims"])}


def node_write_report(state: ResearchState) -> dict[str, Any]:
    report_topic = state.get("effective_topic", state["topic"])
    report_markdown = render_report(
        topic=report_topic,
        selected_papers=state["selected_papers"],
        evidence_items=state["evidence_items"],
        claims=state["claims"],
        citation_checks=state["citation_checks"],
        query_plan=state.get("query_plan", []),
        actual_source=state.get("actual_source", ""),
        fallback_reason=state.get("fallback_reason", ""),
        llm_provider=state.get("llm_provider", "off"),
        llm_used=bool(state.get("llm_used", False)),
        research_lens=state.get("research_lens", {}),
    )
    llm_used = bool(state.get("llm_used", False))
    llm_fallback_reason = state.get("llm_fallback_reason", "")
    if state.get("llm_provider") == "deepseek":
        try:
            report_markdown = polish_background_with_llm(
                report_topic,
                report_markdown,
                state["selected_papers"],
                provider="deepseek",
            )
            llm_used = True
        except LLMError as exc:
            reason = f"Report polish fallback: {exc}"
            llm_fallback_reason = (
                f"{llm_fallback_reason}; {reason}" if llm_fallback_reason else reason
            )
    output_path = state.get("output_path")
    report_path = Path(output_path) if output_path else Path("examples/reports") / f"{slugify(state['topic'])}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_markdown, encoding="utf-8")
    return {
        "report_markdown": report_markdown,
        "report_path": str(report_path),
        "llm_used": llm_used,
        "llm_fallback_reason": llm_fallback_reason,
    }


def node_evaluate_result(state: ResearchState) -> dict[str, Any]:
    return {"metrics": evaluate_state(state)}


RESEARCH_NODES: list[NodeSpec] = [
    ("plan_queries", node_plan_queries),
    ("search_papers", node_search_papers),
    ("rank_papers", node_rank_papers),
    ("extract_evidence", node_extract_evidence),
    ("synthesize_claims", node_synthesize_claims),
    ("check_citations", node_check_citations),
    ("write_report", node_write_report),
    ("evaluate_result", node_evaluate_result),
]


def run_research(
    topic: str,
    top_k: int = 5,
    source: str = "offline",
    output: str | None = None,
    summary_output: str | None = None,
    process_output: str | None = None,
    offline: bool = False,
    write_trace: bool = True,
    llm: str = "off",
    require_live: bool = False,
    candidate_multiplier: int = DEFAULT_CANDIDATE_MULTIPLIER,
    max_candidates: int | None = None,
    from_year: int | None = DEFAULT_FROM_YEAR,
    refine_topic: bool = False,
) -> ResearchResult:
    if not topic.strip():
        raise ValueError("Research topic cannot be empty.")
    if top_k <= 0:
        raise ValueError("top_k must be greater than 0.")

    task_id = make_task_id(topic)
    created_at = datetime.now(timezone.utc).isoformat()
    requested_source = "offline" if offline else source.replace("-", "_")
    selected_sources = (
        ["arxiv", "semantic_scholar", "crossref"]
        if requested_source == "hybrid"
        else [requested_source]
    )
    candidate_limit = candidate_limit_for(top_k, candidate_multiplier, max_candidates)
    normalized_from_year = normalize_from_year(from_year)
    initial_state: ResearchState = {
        "task_id": task_id,
        "session_id": task_id,
        "topic": topic.strip(),
        "effective_topic": topic.strip(),
        "refine_topic": refine_topic,
        "top_k": top_k,
        "candidate_multiplier": max(1, candidate_multiplier),
        "candidate_limit": candidate_limit,
        "from_year": normalized_from_year,
        "requested_source": requested_source,
        "selected_sources": selected_sources,
        "output_path": output,
        "summary_output_path": summary_output,
        "process_output_path": process_output,
        "write_trace": write_trace,
        "llm_provider": llm,
        "llm_used": False,
        "llm_fallback_reason": "",
        "errors": [],
        "node_trace": [],
        "conversation_messages": [],
        "revision_history": [],
        "user_constraints": {},
        "excluded_paper_ids": [],
        "included_query_angles": [],
        "last_conversation_action": "",
        "created_at": created_at,
        "updated_at": created_at,
    }
    final_state = run_research_graph(initial_state, RESEARCH_NODES)
    metrics = dict(final_state["metrics"])
    metrics["graph_runtime"] = final_state.get("graph_runtime", metrics.get("graph_runtime", ""))
    live_requirement_met = not (
        require_live
        and requested_source != "offline"
        and final_state.get("actual_source") == "offline"
    )
    metrics["live_requirement_met"] = live_requirement_met
    if not live_requirement_met:
        metrics["live_requirement_error"] = (
            "A live source was required, but the run fell back to offline fixtures."
        )
    final_state["metrics"] = metrics
    status = "success" if live_requirement_met else "failed"

    process_path: Path | None = None
    if process_output:
        process_path = Path(process_output)
        final_state["process_path"] = str(process_path)

    summary_path: Path | None = None
    if summary_output:
        summary_path = Path(summary_output)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        final_state["summary_path"] = str(summary_path)
        summary_markdown = render_summary_report(final_state)
        final_state["summary_markdown"] = summary_markdown
        summary_path.write_text(summary_markdown, encoding="utf-8")
    elif "summary_markdown" not in final_state:
        final_state["summary_markdown"] = render_summary_report(final_state)

    if process_path:
        process_path.parent.mkdir(parents=True, exist_ok=True)
        process_markdown = render_process_markdown(final_state)
        final_state["process_markdown"] = process_markdown
        process_path.write_text(process_markdown, encoding="utf-8")
    elif "process_markdown" not in final_state:
        final_state["process_markdown"] = render_process_markdown(final_state)

    final_state["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_session(
        final_state,
        messages=final_state.get("conversation_messages", []),
        artifacts={
            "report.md": str(final_state.get("report_markdown", "")),
            "summary.md": str(final_state.get("summary_markdown", "")),
            "process.md": str(final_state.get("process_markdown", "")),
        },
    )

    trace_path: Path | None = None
    if write_trace:
        trace_path = Path("data/runtime") / task_id / "trace.json"
        write_json(
            trace_path,
            {
                "task_id": task_id,
                "topic": topic.strip(),
                "effective_topic": final_state.get("effective_topic", topic.strip()),
                "topic_refinement": _serialize(final_state.get("topic_refinement", {})),
                "topic_refinement_used": bool(final_state.get("topic_refinement_used", False)),
                "topic_refinement_fallback_reason": final_state.get(
                    "topic_refinement_fallback_reason",
                    "",
                ),
                "graph_runtime": final_state.get("graph_runtime", ""),
                "query_plan": _serialize(final_state.get("query_plan", [])),
                "searched_papers": _serialize(final_state.get("searched_papers", [])),
                "ranked_candidates": _serialize(final_state.get("ranked_candidates", [])),
                "selected_papers": _serialize(final_state.get("selected_papers", [])),
                "research_lens": _serialize(final_state.get("research_lens", {})),
                "corpus_profile": _serialize(final_state.get("corpus_profile", {})),
                "temporal_profile": _serialize(final_state.get("temporal_profile", {})),
                "evidence_items": _serialize(final_state.get("evidence_items", [])),
                "claims": _serialize(final_state.get("claims", [])),
                "citation_checks": _serialize(final_state.get("citation_checks", [])),
                "node_trace": _serialize(final_state.get("node_trace", [])),
                "errors": _serialize(final_state.get("errors", [])),
                "process_path": str(process_path) if process_path else None,
                "summary_path": str(summary_path) if summary_path else None,
                "metrics": metrics,
            },
        )

    return ResearchResult(
        task_id=task_id,
        status=status,
        selected_papers=final_state.get("selected_papers", []),
        report_path=final_state["report_path"],
        trace_path=str(trace_path) if trace_path else None,
        process_path=str(process_path) if process_path else None,
        summary_path=str(summary_path) if summary_path else None,
        metrics=metrics,
    )


def evaluate_benchmark(
    benchmark_path: Path,
    output_path: Path | None = None,
) -> dict[str, Any]:
    tasks = []
    for line in benchmark_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            tasks.append(json.loads(line))

    results = []
    for task in tasks:
        result = run_research(
            topic=task["topic"],
            top_k=int(task.get("top_k", 5)),
            source=task.get("source", "offline"),
            offline=bool(task.get("offline", task.get("source", "offline") == "offline")),
            llm=task.get("llm", "off"),
            candidate_multiplier=int(
                task.get("candidate_multiplier", DEFAULT_CANDIDATE_MULTIPLIER)
            ),
            max_candidates=task.get("max_candidates"),
            from_year=task.get("from_year", DEFAULT_FROM_YEAR),
            refine_topic=bool(task.get("refine_topic", False)),
            write_trace=False,
        )
        result_payload = result.to_dict()
        result_payload["topic"] = task["topic"]
        results.append(result_payload)

    scores = [float(item["metrics"].get("overall_score", 0.0)) for item in results]

    summary = {
        "benchmark": str(benchmark_path),
        "task_count": len(tasks),
        "success_count": sum(1 for item in results if item["status"] == "success"),
        "average_score": round(sum(scores) / max(len(scores), 1), 3),
        "results": results,
    }
    if output_path:
        write_json(output_path, summary)
        markdown_path = output_path.with_suffix(".md")
        markdown_path.write_text(render_evaluation_markdown(summary), encoding="utf-8")
    return summary
