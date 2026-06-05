from pathlib import Path

from researchflow.pipeline import run_research


def test_run_research_offline_generates_report(tmp_path: Path) -> None:
    output = tmp_path / "report.md"

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
    assert result.metrics["evidence_count"] == 6
