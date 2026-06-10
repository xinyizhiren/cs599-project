from pathlib import Path

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
