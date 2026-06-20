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
from .models import CitationCheck, ClaimRecord, EvidenceItem, PaperRecord, QueryItem, ResearchResult, SnowballRecord
from .offline_data import OFFLINE_PAPERS
from .planner import build_query_tree, normalize_topic, plan_queries, topic_terms
from .reading import (
    build_global_synthesis,
    build_question_synthesis,
    build_reading_notes,
    build_research_memory,
    evidence_from_reading_notes,
    read_selected_full_texts,
)
from .report import render_full_report, render_process_markdown, render_report, render_summary_report
from .session import save_session
from .state import ResearchState
from .tools import (
    ArxivSearchError,
    CrossrefSearchError,
    OpenAlexSearchError,
    SemanticScholarSearchError,
    TavilySearchError,
    search_arxiv,
    search_crossref,
    search_openalex,
    search_openalex_snowball,
    search_semantic_scholar,
    search_tavily,
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
    "framework",
    "agentic",
    "multi-hop",
    "multi-agent",
    "autonomous",
    "faithful",
    "security",
    "secure",
    "threat",
    "defense",
    "taxonomy",
    "graphrag",
    "causalrag",
    "trustworthy",
    "robust",
    "federated",
    "dynamic",
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
    "quranic",
    "religious",
    "legal",
    "law",
    "medical",
    "healthcare",
    "finance",
    "financial",
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
    "autonomous",
    "multi-hop",
    "multi-agent",
    "iterative",
    "temporal",
    "federated",
    "dynamic",
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
DEFAULT_READING_BUDGET_CHARS = 80000
DEFAULT_MAX_FULLTEXT_PAPERS = 6
LIVE_QUERY_PLAN_LIMIT = 6
ACADEMIC_SOURCES = {"arxiv", "semantic_scholar", "crossref", "openalex"}
LIVE_SOURCES = ACADEMIC_SOURCES | {"web"}
VALID_SOURCES = {"offline"} | LIVE_SOURCES | {"hybrid", "mixed"}
PAPER_TYPE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "survey": ("survey", "review", "taxonomy", "systematic literature", "sok"),
    "benchmark": ("benchmark", "dataset", "evaluation", "metric", "leaderboard"),
    "method": ("method", "algorithm", "approach", "framework", "model", "technique"),
    "system": ("system", "architecture", "pipeline", "stack", "agentic", "multi-agent"),
    "dataset": ("dataset", "corpus", "benchmarking", "testbed"),
    "application": ("application", "case study", "domain", "medical", "legal", "finance", "education"),
    "position": ("position", "perspective", "vision", "roadmap", "challenge", "open problem"),
    "web_background": ("web search", "blog", "documentation", "report"),
}


def slugify(value: str, max_length: int = 48) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return (slug[:max_length].strip("-") or "research-task")


def make_task_id(topic: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{stamp}-{slugify(topic, 32)}"


def is_rag_topic(topic: str) -> bool:
    normalized = topic.lower()
    return any(pattern in normalized for pattern in RAG_TOPIC_PATTERNS)


def classify_paper_type(paper: PaperRecord) -> str:
    if paper.source == "web":
        return "web_background"
    haystack = f"{paper.title} {paper.abstract}".lower()
    for paper_type, keywords in PAPER_TYPE_KEYWORDS.items():
        if paper_type == "web_background":
            continue
        if any(keyword in haystack for keyword in keywords):
            return paper_type
    return "unknown"


def source_quality_bonus(source: str) -> float:
    return {
        "semantic_scholar": 1.2,
        "openalex": 1.1,
        "arxiv": 1.0,
        "crossref": 0.9,
        "offline": 0.4,
        "web": -1.5,
    }.get(source, 0.0)


def paper_type_bonus(paper_type: str, topic: str) -> float:
    bonuses = {
        "survey": 3.0,
        "benchmark": 2.8,
        "method": 2.4,
        "system": 2.0,
        "dataset": 1.6,
        "position": 1.2,
        "application": -0.7,
        "web_background": -3.0,
        "unknown": 0.0,
    }
    bonus = bonuses.get(paper_type, 0.0)
    if "application" in topic.lower() and paper_type == "application":
        bonus = 1.5
    return bonus


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
    inferred_type = paper.paper_type if paper.paper_type != "unknown" else classify_paper_type(paper)
    score = (
        term_score
        + recency_score
        + citation_score
        + source_quality_bonus(paper.source)
        + paper_type_bonus(inferred_type, topic)
        + min(1.0, paper.metadata_confidence or metadata_confidence(paper))
    )
    if paper.pdf_url or paper.open_access_url:
        score += 0.8
    if any(str(source).startswith("snowball:") for source in paper.merged_sources):
        score += 0.9

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
        score += min(5.0, sum(1.0 for signal in RAG_CORE_METHOD_SIGNALS if signal in title))
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
    seen: dict[str, PaperRecord] = {}
    unique: list[PaperRecord] = []
    for paper in papers:
        key, title_key = paper_dedupe_keys(paper)
        existing = seen.get(key) or (seen.get(title_key) if title_key else None)
        if existing:
            merge_paper_metadata(existing, paper)
            continue
        seen[key] = paper
        if title_key:
            seen[title_key] = paper
        if not paper.merged_sources:
            paper.merged_sources = [paper.source]
        if not paper.metadata_confidence:
            paper.metadata_confidence = metadata_confidence(paper)
        unique.append(paper)
    return unique


def merge_paper_metadata(target: PaperRecord, source: PaperRecord) -> PaperRecord:
    if not target.doi and source.doi:
        target.doi = source.doi
    if not target.arxiv_id and source.arxiv_id:
        target.arxiv_id = source.arxiv_id
    if not target.pdf_url and source.pdf_url:
        target.pdf_url = source.pdf_url
    if not target.open_access_url and source.open_access_url:
        target.open_access_url = source.open_access_url
    if source.citation_count > target.citation_count:
        target.citation_count = source.citation_count
    if len(source.abstract or "") > len(target.abstract or ""):
        target.abstract = source.abstract
    if source.authors and target.authors == ["Unknown"]:
        target.authors = source.authors
    merged_sources = [*target.merged_sources, target.source, source.source, *source.merged_sources]
    target.merged_sources = list(dict.fromkeys(item for item in merged_sources if item))
    target.metadata_confidence = max(
        target.metadata_confidence,
        source.metadata_confidence,
        metadata_confidence(target),
        metadata_confidence(source),
    )
    return target


def metadata_confidence(paper: PaperRecord) -> float:
    score = 0.35
    if paper.title:
        score += 0.1
    if paper.abstract and "not available" not in paper.abstract.lower():
        score += 0.15
    if paper.doi:
        score += 0.12
    if paper.arxiv_id:
        score += 0.12
    if paper.pdf_url or paper.open_access_url:
        score += 0.1
    if paper.citation_count:
        score += 0.06
    return round(min(score, 1.0), 3)


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


def _query_from_year(query_plan: list[Any]) -> int | None:
    if not query_plan:
        return None
    filters = getattr(query_plan[0], "filters", {})
    if isinstance(filters, dict):
        return filters.get("from_year")
    return None


def _search_openalex_queries(
    query_plan: list[Any],
    limit: int,
    from_year: int | None = None,
) -> tuple[list[PaperRecord], list[str]]:
    collected: list[PaperRecord] = []
    errors: list[str] = []
    for query in query_plan[:LIVE_QUERY_PLAN_LIMIT]:
        try:
            collected.extend(search_openalex(query.query_text, limit=limit, from_year=from_year))
        except OpenAlexSearchError as exc:
            errors.append(str(exc))
    return collected, errors


def _search_tavily_queries(query_plan: list[Any], limit: int) -> tuple[list[PaperRecord], list[str]]:
    collected: list[PaperRecord] = []
    errors: list[str] = []
    for query in query_plan[:LIVE_QUERY_PLAN_LIMIT]:
        try:
            collected.extend(search_tavily(query.query_text, limit=max(1, min(limit, 10))))
        except TavilySearchError as exc:
            errors.append(str(exc))
    return collected, errors


def normalize_sources(sources: list[str], web_provider: str = "tavily") -> list[str]:
    normalized_sources: list[str] = []
    for source in sources:
        normalized = source.replace("-", "_")
        if normalized == "hybrid":
            normalized_sources.extend(["arxiv", "semantic_scholar", "crossref", "openalex"])
        elif normalized == "mixed":
            normalized_sources.extend(["arxiv", "semantic_scholar", "crossref", "openalex"])
            if web_provider != "off":
                normalized_sources.append("web")
        elif normalized in VALID_SOURCES:
            if normalized != "web" or web_provider != "off":
                normalized_sources.append(normalized)

    if not normalized_sources:
        normalized_sources = ["offline"]
    return list(dict.fromkeys(normalized_sources))


def search_live_source(
    source: str,
    query_plan: list[Any],
    limit: int,
) -> tuple[list[PaperRecord], list[str]]:
    from_year = _query_from_year(query_plan)
    if source == "arxiv":
        return _search_arxiv_queries(query_plan, limit)
    if source == "semantic_scholar":
        return _search_semantic_scholar_queries(query_plan, limit)
    if source == "crossref":
        return _search_crossref_queries(query_plan, limit, from_year=from_year)
    if source == "openalex":
        return _search_openalex_queries(query_plan, limit, from_year=from_year)
    if source == "web":
        return _search_tavily_queries(query_plan, limit)
    return [], [f"Source '{source}' is not implemented."]


def actual_source_label(requested_sources: list[str], actual_sources: list[str]) -> str:
    if not actual_sources:
        return ""
    actual_set = set(actual_sources)
    academic_set = {"arxiv", "semantic_scholar", "crossref", "openalex"}
    if actual_set == academic_set:
        return "hybrid"
    if "web" in actual_set and actual_set - {"web"}:
        return "mixed"
    return "+".join(actual_sources)


def expand_source_label(label: str) -> list[str]:
    if label == "hybrid":
        return ["arxiv", "semantic_scholar", "crossref", "openalex"]
    if label == "mixed":
        return ["arxiv", "semantic_scholar", "crossref", "openalex", "web"]
    return [
        item
        for item in label.split("+")
        if item and item not in {"hybrid", "mixed", "offline"}
    ]


def build_source_results(
    papers: list[PaperRecord],
    actual_source: str,
    fallback_reason: str | None = None,
) -> dict[str, Any]:
    counts: dict[str, int] = {}
    paper_types: dict[str, int] = {}
    for paper in papers:
        counts[paper.source] = counts.get(paper.source, 0) + 1
        paper_type = paper.paper_type if paper.paper_type != "unknown" else classify_paper_type(paper)
        paper_types[paper_type] = paper_types.get(paper_type, 0) + 1
    return {
        "actual_source": actual_source,
        "source_counts": dict(sorted(counts.items())),
        "paper_type_counts": dict(sorted(paper_types.items())),
        "fallback_reason": fallback_reason or "",
    }


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

    if source == "openalex":
        collected, errors = _search_openalex_queries(query_plan, limit, from_year=_query_from_year(query_plan))
        unique = dedupe_papers(collected)
        if unique:
            return unique[:limit], "openalex", None
        fallback_reason = "; ".join(errors) or "OpenAlex returned no papers."
        return search_offline(topic, limit=limit), "offline", fallback_reason

    if source == "web":
        collected, errors = _search_tavily_queries(query_plan, limit)
        unique = dedupe_papers(collected)
        if unique:
            return unique[:limit], "web", None
        fallback_reason = "; ".join(errors) or "Web search returned no sources."
        return search_offline(topic, limit=limit), "offline", fallback_reason

    if source == "hybrid":
        arxiv_papers, arxiv_errors = _search_arxiv_queries(query_plan, limit)
        semantic_papers, semantic_errors = _search_semantic_scholar_queries(query_plan, limit)
        crossref_papers, crossref_errors = _search_crossref_queries(
            query_plan,
            limit,
            from_year=_query_from_year(query_plan),
        )
        openalex_papers, openalex_errors = _search_openalex_queries(
            query_plan,
            limit,
            from_year=_query_from_year(query_plan),
        )
        unique = balanced_merge_papers(
            [
                dedupe_papers(arxiv_papers),
                dedupe_papers(semantic_papers),
                dedupe_papers(crossref_papers),
                dedupe_papers(openalex_papers),
            ],
            limit=limit,
        )
        if unique:
            return unique[:limit], "hybrid", None
        errors = arxiv_errors + semantic_errors + crossref_errors + openalex_errors
        fallback_reason = "; ".join(errors) or "Hybrid search returned no papers."
        return search_offline(topic, limit=limit), "offline", fallback_reason

    fallback_reason = f"Source '{source}' is not implemented; offline fallback used."
    return search_offline(topic, limit=limit), "offline", fallback_reason


def search_selected_sources(
    topic: str,
    query_plan: list[Any],
    sources: list[str],
    limit: int,
    web_provider: str = "tavily",
) -> tuple[list[PaperRecord], str, str | None]:
    """Search a user-selected source set and merge results fairly."""

    normalized_sources = normalize_sources(sources, web_provider=web_provider)
    if len(normalized_sources) == 1:
        return search_source(topic, query_plan, normalized_sources[0], limit)

    source_groups: list[list[PaperRecord]] = []
    actual_sources: list[str] = []
    errors: list[str] = []

    if "offline" in normalized_sources:
        source_groups.append(search_offline(topic, limit=limit))
        actual_sources.append("offline")

    for source in [item for item in normalized_sources if item in LIVE_SOURCES]:
        papers, source_errors = search_live_source(source, query_plan, limit)
        unique = dedupe_papers(papers)
        if unique:
            source_groups.append(unique)
            actual_sources.append(source)
        else:
            errors.extend(source_errors or [f"{source} returned no papers."])

    if source_groups:
        merged = balanced_merge_papers(source_groups, limit=limit)
        actual_label = actual_source_label(normalized_sources, actual_sources)
        return merged, actual_label, "; ".join(errors) or None

    fallback_reason = "; ".join(errors) or "Selected live sources returned no papers."
    return search_offline(topic, limit=limit), "offline", fallback_reason


def rank_papers(papers: list[PaperRecord], topic: str, top_k: int) -> list[PaperRecord]:
    return select_diverse_papers(rank_all_papers(papers, topic), top_k, topic)


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
        paper.paper_type = classify_paper_type(paper)
        paper.score = score_paper(paper, terms, topic=topic)
        ranked.append(paper)
    return ranked


def select_diverse_papers(
    ranked_candidates: list[PaperRecord],
    top_k: int,
    topic: str,
) -> list[PaperRecord]:
    """Select a high-scoring Top-K while preserving report-useful paper types."""

    if top_k <= 0:
        return []
    topic_lower = topic.lower()
    selected: list[PaperRecord] = []
    selected_ids: set[str] = set()
    required_types = ["survey", "method", "benchmark", "position"]
    if "application" in topic_lower:
        required_types.append("application")

    for paper_type in required_types:
        for paper in ranked_candidates:
            if paper.paper_id in selected_ids:
                continue
            if paper.paper_type == paper_type:
                selected.append(paper)
                selected_ids.add(paper.paper_id)
                break
        if len(selected) >= top_k:
            return selected[:top_k]

    application_limit = top_k if "application" in topic_lower else max(1, top_k // 4)
    for paper in ranked_candidates:
        if paper.paper_id in selected_ids:
            continue
        if paper.paper_type == "web_background":
            continue
        if paper.paper_type == "application":
            current_app_count = sum(1 for item in selected if item.paper_type == "application")
            if current_app_count >= application_limit:
                continue
        selected.append(paper)
        selected_ids.add(paper.paper_id)
        if len(selected) >= top_k:
            break

    if len(selected) < top_k:
        for paper in ranked_candidates:
            if paper.paper_id not in selected_ids:
                selected.append(paper)
                selected_ids.add(paper.paper_id)
            if len(selected) >= top_k:
                break
    return selected[:top_k]


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


def build_paper_type_counts(papers: list[PaperRecord]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for paper in papers:
        paper_type = paper.paper_type if paper.paper_type != "unknown" else classify_paper_type(paper)
        counts[paper_type] = counts.get(paper_type, 0) + 1
    return dict(sorted(counts.items()))


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
        "source_counts": build_source_results(candidate_papers, "", "").get("source_counts", {}),
        "paper_type_counts": build_paper_type_counts(candidate_papers),
        "selected_paper_type_counts": build_paper_type_counts(selected_papers),
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


def detect_coverage_gaps(
    topic: str,
    selected_papers: list[PaperRecord],
    research_lens: dict[str, Any],
    temporal_profile: dict[str, Any],
) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    for dimension in research_lens.get("missing_dimensions", [])[:4]:
        gaps.append(
            {
                "gap_id": f"lens:{dimension}",
                "gap_type": "lens_dimension",
                "label": dimension,
                "reason": f"Selected papers do not cover {dimension}.",
                "suggested_angle": _angle_for_gap(dimension),
            }
        )

    type_counts = build_paper_type_counts(selected_papers)
    for paper_type in ("survey", "method", "benchmark"):
        if type_counts.get(paper_type, 0) == 0:
            gaps.append(
                {
                    "gap_id": f"paper_type:{paper_type}",
                    "gap_type": "paper_type",
                    "label": paper_type,
                    "reason": f"No selected {paper_type} paper is available.",
                    "suggested_angle": paper_type,
                }
            )

    if is_rag_topic(topic) and type_counts.get("application", 0) > max(1, len(selected_papers) // 3):
        gaps.append(
            {
                "gap_id": "balance:too_many_applications",
                "gap_type": "balance",
                "label": "application_overweight",
                "reason": "Application papers dominate the core set.",
                "suggested_angle": "method",
            }
        )

    if selected_papers and float(temporal_profile.get("last_5_year_ratio", 0.0)) < 0.35:
        gaps.append(
            {
                "gap_id": "temporal:recent",
                "gap_type": "temporal",
                "label": "recent",
                "reason": "Recent papers are under-represented in the candidate pool.",
                "suggested_angle": "recent",
            }
        )
    return gaps


def _angle_for_gap(label: str) -> str:
    mapping = {
        "Survey & Taxonomy": "survey",
        "Retrieval & Indexing": "method",
        "Generation & Grounding": "method",
        "Evaluation & Benchmarks": "benchmark",
        "Security & Robustness": "security",
        "Graph & Structured RAG": "method",
        "Domain Applications": "application",
    }
    return mapping.get(label, "method")


def make_expansion_queries(
    topic: str,
    coverage_gaps: list[dict[str, Any]],
    from_year: int | None,
    max_queries: int = 3,
) -> list[QueryItem]:
    queries: list[QueryItem] = []
    seen: set[str] = set()
    gap_terms = {
        "survey": "survey taxonomy review",
        "method": "methods architecture framework",
        "benchmark": "benchmark evaluation dataset metrics",
        "security": "security robustness attack defense",
        "application": "applications case study domain",
        "recent": "2024 2025 2026 recent advances",
    }
    for index, gap in enumerate(coverage_gaps, start=1):
        angle = str(gap.get("suggested_angle", "method"))
        if angle in seen:
            continue
        seen.add(angle)
        query_text = f"{topic} {gap_terms.get(angle, angle)}"
        queries.append(
            QueryItem(
                query_id=f"expansion-{index}",
                query_text=query_text,
                source="expansion",
                filters={
                    "angle": angle,
                    "distance": "gap_recovery",
                    "from_year": from_year,
                    "gap_id": gap.get("gap_id", ""),
                },
            )
        )
        if len(queries) >= max_queries:
            break
    return queries


def question_tokens(question: str) -> set[str]:
    stopwords = {
        "the",
        "and",
        "for",
        "with",
        "how",
        "what",
        "why",
        "does",
        "can",
        "of",
        "in",
        "to",
        "a",
        "an",
        "研究",
        "问题",
        "如何",
        "什么",
    }
    return {
        token
        for token in re.findall(r"[A-Za-z0-9\u4e00-\u9fff]+", question.lower())
        if token not in stopwords and len(token) > 1
    }


def build_evidence_matrix(
    research_questions: list[str],
    selected_papers: list[PaperRecord],
    evidence_items: list[EvidenceItem],
) -> list[dict[str, Any]]:
    if not research_questions:
        research_questions = ["What are the main methods, evidence, limitations, and future directions?"]
    evidence_by_paper: dict[str, list[EvidenceItem]] = {}
    for item in evidence_items:
        evidence_by_paper.setdefault(item.paper_id, []).append(item)

    rows: list[dict[str, Any]] = []
    for question_index, question in enumerate(research_questions, start=1):
        tokens = question_tokens(question)
        for paper in selected_papers:
            haystack = f"{paper.title} {paper.abstract}".lower()
            overlap = sum(1 for token in tokens if token in haystack)
            paper_evidence = evidence_by_paper.get(paper.paper_id, [])
            if overlap == 0 and question_index > 1:
                continue
            rows.append(
                {
                    "question_id": f"rq{question_index}",
                    "question": question,
                    "paper_id": paper.paper_id,
                    "paper_title": paper.title,
                    "paper_type": paper.paper_type,
                    "evidence_ids": [item.evidence_id for item in paper_evidence[:3]],
                    "evidence_types": sorted({item.category for item in paper_evidence[:3]}),
                    "relevance_hint": overlap,
                }
            )
    return rows


def build_claim_graph(
    claims: list[ClaimRecord],
    evidence_items: list[EvidenceItem],
    selected_papers: list[PaperRecord],
) -> list[dict[str, Any]]:
    evidence_by_id = {item.evidence_id: item for item in evidence_items}
    paper_by_id = {paper.paper_id: paper for paper in selected_papers}
    graph: list[dict[str, Any]] = []
    for claim in claims:
        supporting = []
        limitations = []
        for evidence_id in claim.evidence_ids:
            evidence = evidence_by_id.get(evidence_id)
            if not evidence:
                continue
            paper = paper_by_id.get(evidence.paper_id)
            node = {
                "evidence_id": evidence.evidence_id,
                "paper_id": evidence.paper_id,
                "paper_title": paper.title if paper else "",
                "category": evidence.category,
                "confidence": evidence.confidence,
            }
            if evidence.category in {"limitation", "future_work"}:
                limitations.append(node)
            else:
                supporting.append(node)
        graph.append(
            {
                "claim_id": claim.claim_id,
                "claim_type": claim.claim_type,
                "claim_text": claim.claim_text,
                "supporting_evidence": supporting,
                "limitations": limitations,
                "confidence": round(
                    sum(item["confidence"] for item in supporting + limitations)
                    / max(len(supporting) + len(limitations), 1),
                    3,
                ),
            }
        )
    return graph


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
        "English academic search topic for search recall. research_questions should be "
        "3-5 Chinese questions for the final report. adjacent_topics should contain 2-3 "
        "Chinese related but not identical angles worth checking. scope_notes must be "
        "Chinese. query_hints should contain 3-5 English search queries. Do not include "
        "citations, URLs, paper titles, or hidden reasoning."
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
        "You polish only the Chinese research background paragraph for a literature review report. "
        "Return a JSON object with key research_background. Write in Chinese. Do not add citations, "
        "URLs, paper IDs, evidence IDs, or references. Keep it concise and factual."
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

    start_marker = "## 1. 研究背景\n\n"
    end_marker = "\n\n## 2. 核心文献"
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
        max_queries=max(6, int(state.get("depth", 2)) * int(state.get("breadth", 4)) + 2),
    )
    query_tree = build_query_tree(
        effective_topic,
        source=requested_source,
        research_questions=refinement.get("research_questions", []),
        adjacent_topics=refinement.get("adjacent_topics", []),
        query_hints=refinement.get("query_hints", []),
        from_year=int(state.get("from_year") or DEFAULT_FROM_YEAR),
        depth=int(state.get("depth", 2)),
        breadth=int(state.get("breadth", 4)),
    )
    return {
        "effective_topic": effective_topic,
        "refined_topic": refinement.get("refined_topic", "") if refinement_used else "",
        "topic_refinement": refinement,
        "topic_refinement_used": refinement_used,
        "topic_refinement_fallback_reason": refinement_fallback_reason,
        "query_plan": query_plan,
        "query_tree": query_tree,
        "subtopics": [
            subtopic
            for branch in query_tree.get("branches", [])
            for subtopic in branch.get("subtopics", [])
        ],
    }


def node_search_papers(state: ResearchState) -> dict[str, Any]:
    raw_papers, actual_source, fallback_reason = search_selected_sources(
        topic=state.get("effective_topic", state["topic"]),
        query_plan=state["query_plan"],
        sources=state.get("selected_sources", [state["requested_source"]]),
        limit=int(state.get("candidate_limit", max(int(state["top_k"]) * 4, 10))),
        web_provider=state.get("web_provider", "tavily"),
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
        "source_results": build_source_results(searched_papers, actual_source, fallback_reason),
    }


def node_rank_papers(state: ResearchState) -> dict[str, Any]:
    effective_topic = state.get("effective_topic", state["topic"])
    ranked_candidates = rank_all_papers(state["searched_papers"], effective_topic)
    selected_papers = select_diverse_papers(ranked_candidates, int(state["top_k"]), effective_topic)
    research_lens = build_research_lens(effective_topic, selected_papers)
    corpus_profile = build_corpus_profile(
        effective_topic,
        ranked_candidates,
        selected_papers,
        state.get("from_year"),
    )
    coverage_gaps = detect_coverage_gaps(
        effective_topic,
        selected_papers,
        research_lens,
        corpus_profile.get("temporal_profile", {}),
    )
    return {
        "ranked_candidates": ranked_candidates,
        "selected_papers": selected_papers,
        "research_lens": research_lens,
        "corpus_profile": corpus_profile,
        "coverage_gaps": coverage_gaps,
    }


def node_expand_search(state: ResearchState) -> dict[str, Any]:
    if (
        state.get("requested_source") == "offline"
        or not state.get("coverage_gaps")
        or int(state.get("max_expansion_rounds", 1)) <= 0
    ):
        return {"expansion_rounds": []}

    effective_topic = state.get("effective_topic", state["topic"])
    expansion_queries = make_expansion_queries(
        effective_topic,
        state.get("coverage_gaps", []),
        state.get("from_year"),
    )
    if not expansion_queries:
        return {"expansion_rounds": []}

    expansion_limit = max(20, min(int(state.get("candidate_limit", 80)), 60))
    expanded_papers, actual_source, fallback_reason = search_selected_sources(
        topic=effective_topic,
        query_plan=expansion_queries,
        sources=state.get("selected_sources", [state["requested_source"]]),
        limit=expansion_limit,
        web_provider=state.get("web_provider", "tavily"),
    )
    if actual_source == "offline" and not expanded_papers:
        return {
            "expansion_rounds": [
                {
                    "round": 1,
                    "queries": [query.to_dict() for query in expansion_queries],
                    "actual_source": actual_source,
                    "fallback_reason": fallback_reason or "No expansion results.",
                    "added_candidates": 0,
                }
            ]
        }

    searched_papers = filter_papers_by_year(
        dedupe_papers(list(state.get("searched_papers", [])) + expanded_papers),
        state.get("from_year"),
    )
    ranked_candidates = rank_all_papers(searched_papers, effective_topic)
    selected_papers = select_diverse_papers(ranked_candidates, int(state["top_k"]), effective_topic)
    research_lens = build_research_lens(effective_topic, selected_papers)
    corpus_profile = build_corpus_profile(
        effective_topic,
        ranked_candidates,
        selected_papers,
        state.get("from_year"),
    )
    coverage_gaps = detect_coverage_gaps(
        effective_topic,
        selected_papers,
        research_lens,
        corpus_profile.get("temporal_profile", {}),
    )
    actual_sources = expand_source_label(str(state.get("actual_source", "")))
    actual_sources.extend(expand_source_label(actual_source))
    actual_label = actual_source_label(state.get("selected_sources", []), list(dict.fromkeys(actual_sources)))
    return {
        "query_plan": list(state.get("query_plan", [])) + expansion_queries,
        "searched_papers": searched_papers,
        "ranked_candidates": ranked_candidates,
        "selected_papers": selected_papers,
        "research_lens": research_lens,
        "corpus_profile": corpus_profile,
        "coverage_gaps": coverage_gaps,
        "temporal_profile": build_temporal_profile(searched_papers),
        "actual_source": actual_label or state.get("actual_source", actual_source),
        "fallback_reason": "; ".join(
            item for item in [state.get("fallback_reason", ""), fallback_reason or ""] if item
        ),
        "source_results": build_source_results(searched_papers, actual_label, fallback_reason),
        "expansion_rounds": [
            {
                "round": 1,
                "queries": [query.to_dict() for query in expansion_queries],
                "actual_source": actual_source,
                "fallback_reason": fallback_reason or "",
                "added_candidates": len(expanded_papers),
                "remaining_gaps": coverage_gaps,
            }
        ],
    }


def _openalex_seed_ids(papers: list[PaperRecord], limit: int = 4) -> list[str]:
    ids: list[str] = []
    for paper in papers:
        if paper.paper_id.startswith("openalex:"):
            ids.append(paper.paper_id.removeprefix("openalex:"))
        elif "openalex.org/" in paper.url:
            ids.append(paper.url.rstrip("/").rsplit("/", 1)[-1])
        if len(ids) >= limit:
            break
    return ids


def node_snowball_search(state: ResearchState) -> dict[str, Any]:
    direction = str(state.get("snowball", "none"))
    if direction == "none" or state.get("requested_source") == "offline":
        return {
            "snowball_records": [],
            "metadata_enrichment": {
                "enabled": direction != "none",
                "added_candidates": 0,
                "reason": "Snowball search is disabled or offline mode is active.",
            },
        }

    seeds = _openalex_seed_ids(state.get("selected_papers", []))
    if not seeds:
        return {
            "snowball_records": [
                SnowballRecord(
                    seed_paper_id="none",
                    direction=direction,
                    added_paper_ids=[],
                    fallback_reason="No OpenAlex seed paper is available for snowball search.",
                )
            ],
            "metadata_enrichment": {
                "enabled": True,
                "added_candidates": 0,
                "reason": "No OpenAlex seed paper is available.",
            },
        }

    limit = max(10, min(int(state.get("candidate_limit", 80)) // 2, 60))
    snowball_papers, raw_records = search_openalex_snowball(
        seeds,
        direction=direction,
        limit=limit,
        from_year=state.get("from_year"),
    )
    searched_papers = filter_papers_by_year(
        dedupe_papers(list(state.get("searched_papers", [])) + snowball_papers),
        state.get("from_year"),
    )
    effective_topic = state.get("effective_topic", state["topic"])
    ranked_candidates = rank_all_papers(searched_papers, effective_topic)
    selected_papers = select_diverse_papers(ranked_candidates, int(state["top_k"]), effective_topic)
    research_lens = build_research_lens(effective_topic, selected_papers)
    corpus_profile = build_corpus_profile(
        effective_topic,
        ranked_candidates,
        selected_papers,
        state.get("from_year"),
    )
    coverage_gaps = detect_coverage_gaps(
        effective_topic,
        selected_papers,
        research_lens,
        corpus_profile.get("temporal_profile", {}),
    )
    records = [
        SnowballRecord(
            seed_paper_id=str(record.get("seed_paper_id", "")),
            direction=str(record.get("direction", direction)),
            added_paper_ids=[str(item) for item in record.get("added_paper_ids", [])],
            query_url=str(record.get("query_url", "")),
            fallback_reason=str(record.get("fallback_reason", "")),
        )
        for record in raw_records
    ]
    added_ids = {paper.paper_id for paper in snowball_papers}
    actual_sources = expand_source_label(str(state.get("actual_source", "")))
    if snowball_papers:
        actual_sources.append("openalex")
    actual_label = actual_source_label(state.get("selected_sources", []), list(dict.fromkeys(actual_sources)))
    return {
        "searched_papers": searched_papers,
        "ranked_candidates": ranked_candidates,
        "selected_papers": selected_papers,
        "research_lens": research_lens,
        "corpus_profile": corpus_profile,
        "coverage_gaps": coverage_gaps,
        "temporal_profile": build_temporal_profile(searched_papers),
        "actual_source": actual_label or state.get("actual_source", ""),
        "source_results": build_source_results(searched_papers, actual_label or state.get("actual_source", ""), state.get("fallback_reason", "")),
        "snowball_records": records,
        "metadata_enrichment": {
            "enabled": True,
            "direction": direction,
            "seed_count": len(seeds),
            "added_candidates": len(added_ids),
            "record_count": len(records),
            "metadata_confidence_avg": round(
                sum(metadata_confidence(paper) for paper in searched_papers) / max(len(searched_papers), 1),
                3,
            ),
        },
    }


def node_read_full_text(state: ResearchState) -> dict[str, Any]:
    read_depth = str(state.get("read_depth", "abstract"))
    chunks, reading_budget = read_selected_full_texts(
        state.get("selected_papers", []),
        read_depth=read_depth,
        max_fulltext_papers=int(state.get("max_fulltext_papers", DEFAULT_MAX_FULLTEXT_PAPERS)),
        reading_budget_chars=int(state.get("reading_budget_chars", DEFAULT_READING_BUDGET_CHARS)),
    )
    notes, note_llm_used, note_fallback_reason = build_reading_notes(
        state.get("selected_papers", []),
        chunks,
        provider=state.get("llm_provider", "off"),
    )
    research_questions = [
        branch.get("question", "")
        for branch in state.get("query_tree", {}).get("branches", [])
        if branch.get("question")
    ]
    llm_fallback_reason = state.get("llm_fallback_reason", "")
    if note_fallback_reason:
        reason = f"Reading-note fallback: {note_fallback_reason}"
        llm_fallback_reason = f"{llm_fallback_reason}; {reason}" if llm_fallback_reason else reason
    return {
        "full_text_chunks": chunks,
        "reading_notes": notes,
        "reading_budget": reading_budget,
        "question_synthesis": build_question_synthesis(research_questions, notes),
        "global_synthesis": build_global_synthesis(notes),
        "llm_used": bool(state.get("llm_used", False) or note_llm_used),
        "llm_fallback_reason": llm_fallback_reason,
    }


def node_extract_evidence(state: ResearchState) -> dict[str, Any]:
    if state.get("reading_notes"):
        return {
            "evidence_items": evidence_from_reading_notes(state["reading_notes"]),
            "llm_chunk_count": state.get("llm_chunk_count", 0),
            "llm_used": bool(state.get("llm_used", False)),
            "llm_fallback_reason": state.get("llm_fallback_reason", ""),
        }

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
    claims = synthesize_claims(
        state.get("effective_topic", state["topic"]),
        state["evidence_items"],
    )
    research_questions = [
        branch.get("question", "")
        for branch in state.get("query_tree", {}).get("branches", [])
        if branch.get("question")
    ]
    return {
        "claims": claims,
        "evidence_matrix": build_evidence_matrix(
            research_questions,
            state["selected_papers"],
            state["evidence_items"],
        ),
        "claim_graph": build_claim_graph(claims, state["evidence_items"], state["selected_papers"]),
        "research_memory": build_research_memory(state.get("reading_notes", []), state["evidence_items"]),
    }


def node_check_citations(state: ResearchState) -> dict[str, Any]:
    return {"citation_checks": check_citations(state["selected_papers"], state["claims"])}


def node_write_report(state: ResearchState) -> dict[str, Any]:
    report_topic = state.get("effective_topic", state["topic"])
    if state.get("report_style", "full") == "full":
        report_markdown = render_full_report(state)
    else:
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
    if state.get("llm_provider") == "deepseek" and state.get("report_style", "full") != "full":
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
    ("expand_search", node_expand_search),
    ("snowball_search", node_snowball_search),
    ("read_full_text", node_read_full_text),
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
    depth: int = 2,
    breadth: int = 4,
    report_style: str = "full",
    web_provider: str = "tavily",
    read_depth: str = "abstract",
    max_fulltext_papers: int = DEFAULT_MAX_FULLTEXT_PAPERS,
    reading_budget_chars: int = DEFAULT_READING_BUDGET_CHARS,
    snowball: str = "none",
    expansion_rounds: int = 1,
    summary_style: str = "comprehensive",
) -> ResearchResult:
    if not topic.strip():
        raise ValueError("Research topic cannot be empty.")
    if top_k <= 0:
        raise ValueError("top_k must be greater than 0.")

    task_id = make_task_id(topic)
    created_at = datetime.now(timezone.utc).isoformat()
    requested_source = "offline" if offline else source.replace("-", "_")
    selected_sources = normalize_sources([requested_source], web_provider=web_provider)
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
        "depth": max(1, depth),
        "breadth": max(1, breadth),
        "from_year": normalized_from_year,
        "requested_source": requested_source,
        "selected_sources": selected_sources,
        "web_provider": web_provider,
        "read_depth": read_depth if read_depth in {"abstract", "auto", "fulltext"} else "abstract",
        "max_fulltext_papers": max(0, max_fulltext_papers),
        "reading_budget_chars": max(1000, reading_budget_chars),
        "reading_budget": {},
        "snowball": snowball if snowball in {"none", "backward", "forward", "both"} else "none",
        "snowball_records": [],
        "metadata_enrichment": {},
        "full_text_chunks": [],
        "reading_notes": [],
        "question_synthesis": [],
        "global_synthesis": {},
        "research_memory": [],
        "summary_style": summary_style if summary_style in {"brief", "comprehensive"} else "comprehensive",
        "max_expansion_rounds": max(0, expansion_rounds),
        "report_style": report_style,
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
                "query_tree": _serialize(final_state.get("query_tree", {})),
                "subtopics": _serialize(final_state.get("subtopics", [])),
                "source_results": _serialize(final_state.get("source_results", {})),
                "searched_papers": _serialize(final_state.get("searched_papers", [])),
                "ranked_candidates": _serialize(final_state.get("ranked_candidates", [])),
                "selected_papers": _serialize(final_state.get("selected_papers", [])),
                "research_lens": _serialize(final_state.get("research_lens", {})),
                "corpus_profile": _serialize(final_state.get("corpus_profile", {})),
                "coverage_gaps": _serialize(final_state.get("coverage_gaps", [])),
                "expansion_rounds": _serialize(final_state.get("expansion_rounds", [])),
                "snowball_records": _serialize(final_state.get("snowball_records", [])),
                "metadata_enrichment": _serialize(final_state.get("metadata_enrichment", {})),
                "reading_budget": _serialize(final_state.get("reading_budget", {})),
                "full_text_chunks": _serialize(final_state.get("full_text_chunks", [])),
                "reading_notes": _serialize(final_state.get("reading_notes", [])),
                "question_synthesis": _serialize(final_state.get("question_synthesis", [])),
                "global_synthesis": _serialize(final_state.get("global_synthesis", {})),
                "research_memory": _serialize(final_state.get("research_memory", [])),
                "temporal_profile": _serialize(final_state.get("temporal_profile", {})),
                "evidence_items": _serialize(final_state.get("evidence_items", [])),
                "evidence_matrix": _serialize(final_state.get("evidence_matrix", [])),
                "claims": _serialize(final_state.get("claims", [])),
                "claim_graph": _serialize(final_state.get("claim_graph", [])),
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
