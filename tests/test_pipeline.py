from pathlib import Path

from researchflow.models import PaperRecord
from researchflow.pipeline import run_research


def test_run_research_offline_generates_report() -> None:
    output = Path("tmp/test_outputs/pipeline-report.md")

    result = run_research(
        "Agentic RAG for enterprise knowledge management",
        top_k=3,
        output=str(output),
        offline=True,
        write_trace=False,
    )

    assert result.status == "success"
    assert len(result.selected_papers) == 3
    assert output.exists()
    report = output.read_text(encoding="utf-8")
    assert "Literature Review" in report
    assert "References" in report
    assert "Key Claims and Evidence" in report
    assert result.metrics["evidence_count"] == 6
    assert result.metrics["overall_score"] > 80
    assert result.metrics["claim_evidence_coverage"] == 1.0


def test_run_research_hybrid_uses_live_source_adapters(monkeypatch) -> None:
    output = Path("tmp/test_outputs/hybrid-report.md")

    def fake_arxiv(query: str, limit: int = 20) -> list[PaperRecord]:
        return [
            PaperRecord(
                paper_id="arxiv:2501.00001",
                title="Agentic Literature Review with arXiv",
                authors=["A. Researcher"],
                year=2025,
                abstract="This paper studies agentic literature review workflows with tools.",
                url="https://arxiv.org/abs/2501.00001",
                arxiv_id="2501.00001",
                source="arxiv",
                citation_count=3,
            )
        ]

    def fake_semantic_scholar(query: str, limit: int = 20) -> list[PaperRecord]:
        return [
            PaperRecord(
                paper_id="s2:abc123",
                title="Citation-Grounded Research Agents",
                authors=["B. Scientist"],
                year=2024,
                abstract="This paper studies citation-grounded research agents and evaluation.",
                url="https://www.semanticscholar.org/paper/abc123",
                doi="10.1234/example",
                source="semantic_scholar",
                citation_count=42,
            )
        ]

    monkeypatch.setattr("researchflow.pipeline.search_arxiv", fake_arxiv)
    monkeypatch.setattr("researchflow.pipeline.search_semantic_scholar", fake_semantic_scholar)

    result = run_research(
        "agentic literature review agents",
        top_k=2,
        source="hybrid",
        output=str(output),
        write_trace=False,
    )

    assert result.status == "success"
    assert len(result.selected_papers) == 2
    assert result.metrics["actual_source"] == "hybrid"
    report = output.read_text(encoding="utf-8")
    assert "Executive Summary" in report
    assert "Evidence Ledger" in report
