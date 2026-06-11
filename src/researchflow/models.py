"""Core data models used by the ResearchFlow MVP."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


ClaimType = Literal["Fact", "Synthesis", "Hypothesis"]
CheckStatus = Literal["passed", "warning", "failed"]


@dataclass(slots=True)
class QueryItem:
    query_id: str
    query_text: str
    source: str = "offline"
    filters: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class PaperRecord:
    paper_id: str
    title: str
    authors: list[str]
    year: int
    abstract: str
    url: str
    doi: str | None = None
    arxiv_id: str | None = None
    source: str = "offline"
    citation_count: int = 0
    score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class EvidenceItem:
    evidence_id: str
    paper_id: str
    category: str
    claim: str
    support_text: str
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ClaimRecord:
    claim_id: str
    claim_text: str
    claim_type: ClaimType
    evidence_ids: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class CitationCheck:
    check_id: str
    paper_id: str
    status: CheckStatus
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ResearchResult:
    task_id: str
    status: str
    selected_papers: list[PaperRecord]
    report_path: str
    metrics: dict[str, Any]
    trace_path: str | None = None
    process_path: str | None = None
    summary_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "status": self.status,
            "selected_papers": [paper.to_dict() for paper in self.selected_papers],
            "report_path": self.report_path,
            "metrics": self.metrics,
            "trace_path": self.trace_path,
            "process_path": self.process_path,
            "summary_path": self.summary_path,
        }
