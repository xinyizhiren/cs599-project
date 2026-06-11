"""Command line entrypoint for ResearchFlow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import __version__
from .pipeline import evaluate_benchmark, run_research


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="researchflow")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a literature review task.")
    run_parser.add_argument("topic", help="Research topic to investigate.")
    run_parser.add_argument("--top-k", type=int, default=5, help="Number of papers to select.")
    run_parser.add_argument(
        "--candidate-multiplier",
        type=int,
        default=8,
        help="Candidate pool size multiplier before ranking. Defaults to 8.",
    )
    run_parser.add_argument(
        "--max-candidates",
        type=int,
        default=None,
        help="Explicit maximum candidate pool size before ranking.",
    )
    run_parser.add_argument(
        "--from-year",
        type=int,
        default=2020,
        help="Keep candidates from this year onward. Use 0 to disable.",
    )
    run_parser.add_argument(
        "--source",
        default="offline",
        choices=["offline", "arxiv", "semantic_scholar", "semantic-scholar", "hybrid"],
        help="Paper data source. Use hybrid for live arXiv + Semantic Scholar search.",
    )
    run_parser.add_argument("--output", default=None, help="Markdown report output path.")
    run_parser.add_argument(
        "--process-output",
        default=None,
        help="Markdown process log output path.",
    )
    run_parser.add_argument(
        "--summary-output",
        default=None,
        help="Markdown final synthesis summary output path.",
    )
    run_parser.add_argument("--offline", action="store_true", help="Force offline fixture mode.")
    run_parser.add_argument(
        "--require-live",
        action="store_true",
        help="Fail if a live source request falls back to offline fixtures.",
    )
    run_parser.add_argument("--trace", action="store_true", default=True, help="Write trace JSON.")
    run_parser.add_argument(
        "--llm",
        default="off",
        choices=["off", "deepseek"],
        help="Optional LLM provider for evidence extraction. Defaults to off.",
    )

    eval_parser = subparsers.add_parser("evaluate", help="Run benchmark tasks.")
    eval_parser.add_argument("--benchmark", required=True, help="JSONL benchmark file.")
    eval_parser.add_argument(
        "--output",
        default="examples/evaluation/results.json",
        help="Evaluation JSON output path. A Markdown report is written next to it.",
    )

    subparsers.add_parser("version", help="Print version.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "version":
        print(__version__)
        return 0

    if args.command == "run":
        result = run_research(
            topic=args.topic,
            top_k=args.top_k,
            source=args.source,
            output=args.output,
            summary_output=args.summary_output,
            process_output=args.process_output,
            offline=args.offline or args.source == "offline",
            write_trace=args.trace,
            llm=args.llm,
            require_live=args.require_live,
            candidate_multiplier=args.candidate_multiplier,
            max_candidates=args.max_candidates,
            from_year=args.from_year,
        )
        print(f"Task ID: {result.task_id}")
        print(f"Status: {result.status}")
        print(f"Selected Papers: {len(result.selected_papers)}")
        print(f"Report: {result.report_path}")
        if result.summary_path:
            print(f"Summary: {result.summary_path}")
        if result.process_path:
            print(f"Process: {result.process_path}")
        if result.trace_path:
            print(f"Trace: {result.trace_path}")
        return 0 if result.status == "success" else 1

    if args.command == "evaluate":
        summary = evaluate_benchmark(
            benchmark_path=Path(args.benchmark),
            output_path=Path(args.output),
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        print(f"Evaluation JSON: {args.output}")
        print(f"Evaluation Markdown: {Path(args.output).with_suffix('.md')}")
        return 0

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
