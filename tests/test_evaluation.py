from pathlib import Path

from researchflow.evaluation import render_evaluation_markdown
from researchflow.pipeline import evaluate_benchmark, run_research


def test_run_research_writes_trace_with_node_steps() -> None:
    output = Path("tmp/test_outputs/evaluation-report.md")

    result = run_research(
        "Citation hallucination detection in scientific writing",
        top_k=2,
        output=str(output),
        offline=True,
        write_trace=True,
    )

    assert result.trace_path is not None
    assert Path(result.trace_path).exists()
    assert "summary_path" in result.to_dict()
    assert result.metrics["graph_runtime"] in {
        "sequential",
        "sequential_fallback",
        "langgraph",
    }
    assert result.metrics["node_trace_count"] >= 7


def test_evaluate_benchmark_outputs_scores() -> None:
    output_dir = Path("tmp/test_outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    benchmark = output_dir / "benchmark.jsonl"
    benchmark.write_text(
        '{"topic": "Agentic RAG for enterprise knowledge management", "top_k": 3}\n',
        encoding="utf-8",
    )
    output = output_dir / "results.json"

    summary = evaluate_benchmark(benchmark, output)

    assert summary["task_count"] == 1
    assert summary["success_count"] == 1
    assert summary["average_score"] > 80
    assert output.exists()
    assert output.with_suffix(".md").exists()
    assert "ResearchFlow Evaluation Report" in render_evaluation_markdown(summary)
