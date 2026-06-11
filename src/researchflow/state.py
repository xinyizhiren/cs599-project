"""State contract for the ResearchFlow agent workflow."""

from __future__ import annotations

from typing import Any, TypedDict

from .models import CitationCheck, ClaimRecord, EvidenceItem, PaperRecord, QueryItem


class ResearchState(TypedDict, total=False):
    task_id: str
    topic: str
    effective_topic: str
    refine_topic: bool
    refined_topic: str
    topic_refinement: dict[str, Any]
    topic_refinement_used: bool
    topic_refinement_fallback_reason: str
    top_k: int
    candidate_multiplier: int
    candidate_limit: int
    from_year: int | None
    requested_source: str
    selected_sources: list[str]
    actual_source: str
    fallback_reason: str
    output_path: str | None
    summary_output_path: str | None
    process_output_path: str | None
    process_path: str
    summary_path: str
    write_trace: bool
    llm_provider: str
    llm_used: bool
    llm_fallback_reason: str
    query_plan: list[QueryItem]
    searched_papers: list[PaperRecord]
    ranked_candidates: list[PaperRecord]
    selected_papers: list[PaperRecord]
    temporal_profile: dict[str, Any]
    research_lens: dict[str, Any]
    corpus_profile: dict[str, Any]
    evidence_items: list[EvidenceItem]
    llm_chunk_count: int
    claims: list[ClaimRecord]
    citation_checks: list[CitationCheck]
    report_markdown: str
    report_path: str
    summary_markdown: str
    metrics: dict[str, Any]
    errors: list[dict[str, Any]]
    node_trace: list[dict[str, Any]]
    graph_runtime: str
