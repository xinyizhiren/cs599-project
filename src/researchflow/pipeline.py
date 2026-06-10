"""Offline-first ResearchFlow pipeline.

The MVP uses deterministic local fixtures so the course demo remains stable.
Real API-backed tools can replace the search function without changing the
state and report contracts.
"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .evaluation import evaluate_state, render_evaluation_markdown
from .graph import NodeSpec, run_research_graph
from .llm import LLMError, build_llm_client
from .models import CitationCheck, ClaimRecord, EvidenceItem, PaperRecord, ResearchResult
from .offline_data import OFFLINE_PAPERS
from .planner import plan_queries, topic_terms
from .report import render_report
from .state import ResearchState
from .tools import ArxivSearchError, search_arxiv


def slugify(value: str, max_length: int = 48) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return (slug[:max_length].strip("-") or "research-task")


def make_task_id(topic: str) -> str:
    stamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    return f"{stamp}-{slugify(topic, 32)}"


def score_paper(paper: PaperRecord, terms: list[str]) -> float:
    haystack = f"{paper.title} {paper.abstract}".lower()
    term_score = sum(1 for term in terms if term.lower() in haystack)
    recency_score = max(0, paper.year - 2020) * 0.1
    citation_score = min(paper.citation_count, 100) / 100
    return term_score * 2.0 + recency_score + citation_score


def search_offline(topic: str, limit: int = 20) -> list[PaperRecord]:
    terms = topic_terms(topic)
    scored = []
    for paper in OFFLINE_PAPERS:
        score = score_paper(paper, terms)
        clone = PaperRecord(**{**paper.to_dict(), "score": score})
        scored.append(clone)
    scored.sort(key=lambda item: (item.score, item.year, item.citation_count), reverse=True)
    return scored[:limit]


def dedupe_papers(papers: list[PaperRecord]) -> list[PaperRecord]:
    seen: set[str] = set()
    unique: list[PaperRecord] = []
    for paper in papers:
        key = paper.paper_id or paper.url or paper.title.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(paper)
    return unique


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
        collected: list[PaperRecord] = []
        errors: list[str] = []
        for query in query_plan[:3]:
            try:
                collected.extend(search_arxiv(query.query_text, limit=limit))
            except ArxivSearchError as exc:
                errors.append(str(exc))
        unique = dedupe_papers(collected)
        if unique:
            return unique[:limit], "arxiv", None
        fallback_reason = "; ".join(errors) or "arXiv returned no papers."
        return search_offline(topic, limit=limit), "offline", fallback_reason

    fallback_reason = f"Source '{source}' is not implemented; offline fallback used."
    return search_offline(topic, limit=limit), "offline", fallback_reason


def rank_papers(papers: list[PaperRecord], topic: str, top_k: int) -> list[PaperRecord]:
    terms = topic_terms(topic)
    seen: set[str] = set()
    ranked: list[PaperRecord] = []
    for paper in sorted(
        papers,
        key=lambda item: (score_paper(item, terms), item.year, item.citation_count),
        reverse=True,
    ):
        if paper.paper_id in seen:
            continue
        seen.add(paper.paper_id)
        paper.score = score_paper(paper, terms)
        ranked.append(paper)
        if len(ranked) >= top_k:
            break
    return ranked


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


def extract_evidence_with_llm(papers: list[PaperRecord], provider: str) -> list[EvidenceItem]:
    client = build_llm_client(provider)
    paper_payload = [
        {
            "paper_id": paper.paper_id,
            "title": paper.title,
            "authors": paper.authors,
            "year": paper.year,
            "abstract": paper.abstract,
        }
        for paper in papers
    ]
    system_prompt = (
        "You extract evidence for a literature review agent. Return only a JSON object "
        "with key evidence_items. Each item must use a paper_id from the input and include "
        "category, claim, support_text, and confidence. Use categories contribution, method, "
        "experiment, limitation, or future_work. Do not invent papers or references."
    )
    payload = client.generate_json(system_prompt, {"papers": paper_payload})
    raw_items = payload.get("evidence_items")
    if not isinstance(raw_items, list):
        raise LLMError("LLM JSON missing evidence_items list.")

    allowed_papers = {paper.paper_id for paper in papers}
    evidence_items: list[EvidenceItem] = []
    counters: dict[str, int] = {}
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

    if not evidence_items:
        raise LLMError("LLM did not produce usable evidence items.")
    return evidence_items


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
        item.evidence_id for item in evidence_items if item.category == "contribution"
    ][:3]
    limitation_ids = [
        item.evidence_id for item in evidence_items if item.category == "limitation"
    ][:3]
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
    return {"query_plan": plan_queries(state["topic"], source=requested_source)}


def node_search_papers(state: ResearchState) -> dict[str, Any]:
    searched_papers, actual_source, fallback_reason = search_source(
        topic=state["topic"],
        query_plan=state["query_plan"],
        source=state["requested_source"],
        limit=max(int(state["top_k"]) * 4, 10),
    )
    return {
        "searched_papers": searched_papers,
        "actual_source": actual_source,
        "fallback_reason": fallback_reason or "",
    }


def node_rank_papers(state: ResearchState) -> dict[str, Any]:
    return {
        "selected_papers": rank_papers(
            state["searched_papers"],
            state["topic"],
            top_k=int(state["top_k"]),
        )
    }


def node_extract_evidence(state: ResearchState) -> dict[str, Any]:
    provider = state.get("llm_provider", "off")
    if provider == "deepseek":
        try:
            return {
                "evidence_items": extract_evidence_with_llm(
                    state["selected_papers"],
                    provider=provider,
                ),
                "llm_used": True,
                "llm_fallback_reason": "",
            }
        except LLMError as exc:
            return {
                "evidence_items": extract_evidence(state["selected_papers"]),
                "llm_used": False,
                "llm_fallback_reason": str(exc),
            }
    return {
        "evidence_items": extract_evidence(state["selected_papers"]),
        "llm_used": False,
        "llm_fallback_reason": "LLM provider is disabled.",
    }


def node_synthesize_claims(state: ResearchState) -> dict[str, Any]:
    return {"claims": synthesize_claims(state["topic"], state["evidence_items"])}


def node_check_citations(state: ResearchState) -> dict[str, Any]:
    return {"citation_checks": check_citations(state["selected_papers"], state["claims"])}


def node_write_report(state: ResearchState) -> dict[str, Any]:
    report_markdown = render_report(
        topic=state["topic"],
        selected_papers=state["selected_papers"],
        evidence_items=state["evidence_items"],
        claims=state["claims"],
        citation_checks=state["citation_checks"],
    )
    llm_used = bool(state.get("llm_used", False))
    llm_fallback_reason = state.get("llm_fallback_reason", "")
    if state.get("llm_provider") == "deepseek":
        try:
            report_markdown = polish_background_with_llm(
                state["topic"],
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
    offline: bool = False,
    write_trace: bool = True,
    llm: str = "off",
) -> ResearchResult:
    if not topic.strip():
        raise ValueError("Research topic cannot be empty.")
    if top_k <= 0:
        raise ValueError("top_k must be greater than 0.")

    task_id = make_task_id(topic)
    requested_source = "offline" if offline else source
    initial_state: ResearchState = {
        "task_id": task_id,
        "topic": topic.strip(),
        "top_k": top_k,
        "requested_source": requested_source,
        "output_path": output,
        "write_trace": write_trace,
        "llm_provider": llm,
        "llm_used": False,
        "llm_fallback_reason": "",
        "errors": [],
        "node_trace": [],
    }
    final_state = run_research_graph(initial_state, RESEARCH_NODES)
    metrics = dict(final_state["metrics"])
    metrics["graph_runtime"] = final_state.get("graph_runtime", metrics.get("graph_runtime", ""))

    trace_path: Path | None = None
    if write_trace:
        trace_path = Path("data/runtime") / task_id / "trace.json"
        write_json(
            trace_path,
            {
                "task_id": task_id,
                "topic": topic.strip(),
                "graph_runtime": final_state.get("graph_runtime", ""),
                "query_plan": _serialize(final_state.get("query_plan", [])),
                "searched_papers": _serialize(final_state.get("searched_papers", [])),
                "selected_papers": _serialize(final_state.get("selected_papers", [])),
                "evidence_items": _serialize(final_state.get("evidence_items", [])),
                "claims": _serialize(final_state.get("claims", [])),
                "citation_checks": _serialize(final_state.get("citation_checks", [])),
                "node_trace": _serialize(final_state.get("node_trace", [])),
                "errors": _serialize(final_state.get("errors", [])),
                "metrics": metrics,
            },
        )

    return ResearchResult(
        task_id=task_id,
        status="success",
        selected_papers=final_state.get("selected_papers", []),
        report_path=final_state["report_path"],
        trace_path=str(trace_path) if trace_path else None,
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
