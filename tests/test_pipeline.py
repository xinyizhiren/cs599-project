from pathlib import Path

from researchflow.models import PaperRecord
from researchflow.pipeline import run_research


def test_run_research_offline_generates_report() -> None:
    output = Path("tmp/test_outputs/pipeline-report.md")
    process_output = Path("tmp/test_outputs/pipeline-process.md")

    result = run_research(
        "Agentic RAG for enterprise knowledge management",
        top_k=3,
        output=str(output),
        process_output=str(process_output),
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
    assert result.process_path == str(process_output)
    process = process_output.read_text(encoding="utf-8")
    assert "Research Process" in process
    assert "Query Plan" in process
    assert "Evidence Extraction" in process
    assert "DEEPSEEK_API_KEY" not in process
    assert "sk-" not in process


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


def test_require_live_fails_when_live_source_falls_back(monkeypatch) -> None:
    output = Path("tmp/test_outputs/live-required-report.md")
    process_output = Path("tmp/test_outputs/live-required-process.md")

    monkeypatch.setattr("researchflow.pipeline.search_arxiv", lambda query, limit=20: [])

    result = run_research(
        "rare live source topic",
        top_k=2,
        source="arxiv",
        output=str(output),
        process_output=str(process_output),
        write_trace=False,
        require_live=True,
    )

    assert result.status == "failed"
    assert result.metrics["actual_source"] == "offline"
    assert result.metrics["live_requirement_met"] is False
    assert output.exists()
    assert process_output.exists()
    assert "live_requirement_error" in process_output.read_text(encoding="utf-8")
