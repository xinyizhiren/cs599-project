"""Local evaluator for ResearchFlow outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import CitationCheck, ClaimRecord, PaperRecord
from .state import ResearchState


EXPECTED_REPORT_SECTIONS = [
    "## 1. Research Background",
    "## 2. Core Papers",
    "## 3. Key Claims and Evidence",
    "## 4. Method Taxonomy",
    "## 5. Comparative Analysis",
    "## 6. Research Gaps",
    "## 7. Limitations of This Automated Review",
    "## References",
]


def _safe_divide(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def _round(value: float) -> float:
    return round(value, 3)


def citation_validity(checks: list[CitationCheck]) -> float:
    return _safe_divide(sum(1 for check in checks if check.status == "passed"), len(checks))


def claim_evidence_coverage(claims: list[ClaimRecord]) -> float:
    return _safe_divide(sum(1 for claim in claims if claim.evidence_ids), len(claims))


def hallucinated_reference_count(selected_papers: list[PaperRecord], report_markdown: str) -> int:
    # The report writer emits references only from selected_papers. This guard
    # still catches accidental future references that include non-selected IDs.
    known_urls = {paper.url for paper in selected_papers}
    reference_lines = [
        line for line in report_markdown.splitlines() if line.startswith("[P") and "http" in line
    ]
    return sum(1 for line in reference_lines if not any(url in line for url in known_urls))


def section_completeness(report_markdown: str) -> float:
    present = sum(1 for heading in EXPECTED_REPORT_SECTIONS if heading in report_markdown)
    return _safe_divide(present, len(EXPECTED_REPORT_SECTIONS))


def duplicate_rate(papers: list[PaperRecord]) -> float:
    if not papers:
        return 0.0
    unique = {paper.paper_id or paper.url or paper.title for paper in papers}
    return 1.0 - _safe_divide(len(unique), len(papers))


def evaluate_state(state: ResearchState) -> dict[str, Any]:
    query_plan = state.get("query_plan", [])
    searched = state.get("searched_papers", [])
    selected = state.get("selected_papers", [])
    evidence = state.get("evidence_items", [])
    claims = state.get("claims", [])
    checks = state.get("citation_checks", [])
    report = state.get("report_markdown", "")
    trace = state.get("node_trace", [])
    errors = state.get("errors", [])
    research_lens = state.get("research_lens", {})
    temporal_profile = state.get("temporal_profile", {})

    report_generated = bool(state.get("report_path")) and Path(state["report_path"]).exists()
    run_success_rate = 1.0 if report_generated and selected else 0.0
    node_failure_recovery = 1.0 if not errors else 0.75 if report_generated else 0.0
    task_completion_score = 20 * ((run_success_rate * 0.7) + (node_failure_recovery * 0.3))

    top_k = max(int(state.get("top_k", 1)), 1)
    top_k_relevance = _safe_divide(sum(1 for paper in selected if paper.score > 0), len(selected))
    source_success = 1.0 if searched else 0.0
    retrieval_score = 20 * (
        (top_k_relevance * 0.5)
        + ((1.0 - duplicate_rate(searched)) * 0.2)
        + (min(len(selected), top_k) / top_k * 0.2)
        + (source_success * 0.1)
    )

    citation_rate = citation_validity(checks)
    evidence_coverage = claim_evidence_coverage(claims)
    unsupported_claim_rate = 1.0 - evidence_coverage
    hallucinated_refs = hallucinated_reference_count(selected, report)
    evidence_score = 25 * (
        (citation_rate * 0.35)
        + (evidence_coverage * 0.4)
        + ((1.0 - unsupported_claim_rate) * 0.15)
        + ((1.0 if hallucinated_refs == 0 else 0.0) * 0.1)
    )

    completeness = section_completeness(report)
    method_taxonomy_quality = 1.0 if "### Contribution" in report and "### Limitation" in report else 0.5
    research_gap_usefulness = 1.0 if "Research Gaps" in report and "Evidence:" in report else 0.5
    readability = 1.0 if len(report.split()) >= 120 else 0.6
    report_score = 20 * (
        (completeness * 0.4)
        + (method_taxonomy_quality * 0.25)
        + (research_gap_usefulness * 0.2)
        + (readability * 0.15)
    )

    expected_nodes = 7
    tool_call_correctness = (
        1.0
        if state.get("actual_source") in {"offline", "arxiv", "semantic_scholar", "hybrid"}
        and searched
        else 0.0
    )
    plan_adherence = 1.0 if query_plan and selected and evidence and checks else 0.0
    step_efficiency = max(0.0, 1.0 - max(0, len(trace) - expected_nodes) / expected_nodes)
    trace_completeness = min(1.0, _safe_divide(len(trace), expected_nodes))
    agent_score = 15 * (
        (tool_call_correctness * 0.35)
        + (plan_adherence * 0.3)
        + (step_efficiency * 0.15)
        + (trace_completeness * 0.2)
    )

    overall_score = task_completion_score + retrieval_score + evidence_score + report_score + agent_score
    return {
        "query_count": len(query_plan),
        "searched_paper_count": len(searched),
        "selected_paper_count": len(selected),
        "candidate_limit": state.get("candidate_limit", len(searched)),
        "candidate_multiplier": state.get("candidate_multiplier", 0),
        "from_year": state.get("from_year"),
        "evidence_count": len(evidence),
        "claim_count": len(claims),
        "citation_check_count": len(checks),
        "citation_check_pass_rate": _round(citation_rate),
        "claim_evidence_coverage": _round(evidence_coverage),
        "unsupported_claim_rate": _round(unsupported_claim_rate),
        "hallucinated_reference_count": hallucinated_refs,
        "report_section_completeness": _round(completeness),
        "node_trace_count": len(trace),
        "requested_source": state.get("requested_source", ""),
        "actual_source": state.get("actual_source", ""),
        "fallback_reason": state.get("fallback_reason", ""),
        "llm_provider": state.get("llm_provider", "off"),
        "llm_used": bool(state.get("llm_used", False)),
        "llm_fallback_reason": state.get("llm_fallback_reason", ""),
        "llm_chunk_count": state.get("llm_chunk_count", 0),
        "earliest_candidate_year": temporal_profile.get("earliest_year"),
        "latest_candidate_year": temporal_profile.get("latest_year"),
        "recent_3_year_ratio": temporal_profile.get("last_3_year_ratio", 0.0),
        "recent_5_year_ratio": temporal_profile.get("last_5_year_ratio", 0.0),
        "research_lens_coverage": _round(float(research_lens.get("coverage", 0.0))),
        "graph_runtime": state.get("graph_runtime", ""),
        "dimension_scores": {
            "task_completion": _round(task_completion_score),
            "retrieval_quality": _round(retrieval_score),
            "evidence_trust": _round(evidence_score),
            "report_quality": _round(report_score),
            "agent_behavior": _round(agent_score),
        },
        "overall_score": _round(overall_score),
    }


def render_evaluation_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# ResearchFlow Evaluation Report",
        "",
        f"- Benchmark: {summary['benchmark']}",
        f"- Tasks: {summary['task_count']}",
        f"- Success: {summary['success_count']}",
        f"- Average Score: {summary['average_score']:.3f}",
        "",
        "## Task Results",
        "",
        "| Topic | Status | Score | Citation Validity | Evidence Coverage | Sections | Source |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for item in summary["results"]:
        metrics = item["metrics"]
        topic = item.get("topic", item["task_id"])
        lines.append(
            "| "
            + " | ".join(
                [
                    topic,
                    item["status"],
                    f"{metrics.get('overall_score', 0):.3f}",
                    f"{metrics.get('citation_check_pass_rate', 0):.3f}",
                    f"{metrics.get('claim_evidence_coverage', 0):.3f}",
                    f"{metrics.get('report_section_completeness', 0):.3f}",
                    str(metrics.get("actual_source", "")),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Scoring Rubric",
            "",
            "- Task completion: 20",
            "- Retrieval quality: 20",
            "- Evidence trust: 25",
            "- Report quality: 20",
            "- Agent behavior: 15",
        ]
    )
    return "\n".join(lines) + "\n"
