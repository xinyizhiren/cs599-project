"""Offline-first ResearchFlow pipeline.

The MVP uses deterministic local fixtures so the course demo remains stable.
Real API-backed tools can replace the search function without changing the
state and report contracts.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import CitationCheck, ClaimRecord, EvidenceItem, PaperRecord, ResearchResult
from .offline_data import OFFLINE_PAPERS
from .planner import plan_queries, topic_terms
from .report import render_report


def slugify(value: str, max_length: int = 48) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return (slug[:max_length].strip("-") or "research-task")


def make_task_id(topic: str) -> str:
    stamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
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
    return checks


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def run_research(
    topic: str,
    top_k: int = 5,
    source: str = "offline",
    output: str | None = None,
    offline: bool = False,
    write_trace: bool = True,
) -> ResearchResult:
    if not topic.strip():
        raise ValueError("Research topic cannot be empty.")
    if top_k <= 0:
        raise ValueError("top_k must be greater than 0.")

    task_id = make_task_id(topic)
    query_plan = plan_queries(topic, source="offline" if offline else source)

    if not offline and source != "offline":
        raise NotImplementedError(
            "MVP currently supports offline mode. API-backed tools are planned next."
        )

    searched_papers = search_offline(topic)
    selected_papers = rank_papers(searched_papers, topic, top_k=top_k)
    evidence_items = extract_evidence(selected_papers)
    claims = synthesize_claims(topic, evidence_items)
    citation_checks = check_citations(selected_papers, claims)

    report_markdown = render_report(
        topic=topic,
        selected_papers=selected_papers,
        evidence_items=evidence_items,
        claims=claims,
        citation_checks=citation_checks,
    )

    report_path = Path(output) if output else Path("examples/reports") / f"{slugify(topic)}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_markdown, encoding="utf-8")

    passed_checks = sum(1 for check in citation_checks if check.status == "passed")
    metrics: dict[str, int | float | str] = {
        "query_count": len(query_plan),
        "searched_paper_count": len(searched_papers),
        "selected_paper_count": len(selected_papers),
        "evidence_count": len(evidence_items),
        "citation_check_pass_rate": round(passed_checks / max(len(citation_checks), 1), 3),
        "mode": "offline",
    }

    trace_path: Path | None = None
    if write_trace:
        trace_path = Path("data/runtime") / task_id / "trace.json"
        write_json(
            trace_path,
            {
                "task_id": task_id,
                "topic": topic,
                "query_plan": [item.to_dict() for item in query_plan],
                "selected_papers": [paper.to_dict() for paper in selected_papers],
                "evidence_items": [item.to_dict() for item in evidence_items],
                "claims": [claim.to_dict() for claim in claims],
                "citation_checks": [check.to_dict() for check in citation_checks],
                "metrics": metrics,
            },
        )

    return ResearchResult(
        task_id=task_id,
        status="success",
        selected_papers=selected_papers,
        report_path=str(report_path),
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
            offline=True,
            write_trace=False,
        )
        results.append(result.to_dict())

    summary = {
        "benchmark": str(benchmark_path),
        "task_count": len(tasks),
        "success_count": sum(1 for item in results if item["status"] == "success"),
        "results": results,
    }
    if output_path:
        write_json(output_path, summary)
    return summary
