"""Lightweight Web UI for the ResearchFlow agent.

The server intentionally uses the Python standard library so the course demo
can run on a small VM without a separate frontend build step.
"""

from __future__ import annotations

import argparse
import copy
import json
import mimetypes
import threading
import traceback
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources
from pathlib import Path
from time import perf_counter
from typing import Any
from urllib.parse import unquote, urlparse

from .models import ResearchResult
from .pipeline import (
    DEFAULT_CANDIDATE_MULTIPLIER,
    DEFAULT_FROM_YEAR,
    RESEARCH_NODES,
    _serialize,
    candidate_limit_for,
    make_task_id,
    normalize_from_year,
    render_process_markdown,
    render_summary_report,
    slugify,
    write_json,
)
from .planner import topic_terms
from .state import ResearchState


StepStatus = str
ALLOWED_SOURCES = {"offline", "arxiv", "semantic_scholar", "crossref"}
DOWNLOAD_KINDS = {
    "report": ("report_markdown", "report.md"),
    "summary": ("summary_markdown", "summary.md"),
    "process": ("process_markdown", "process.md"),
}

STEP_DEFINITIONS: list[dict[str, str]] = [
    {
        "id": "understand_topic",
        "name": "Understand Topic",
        "label": "理解主题",
        "description": "Normalize the topic, source, time window, and search budget.",
    },
    {
        "id": "plan_queries",
        "name": "Plan Queries",
        "label": "规划检索",
        "description": "Split the research task into auditable search queries.",
    },
    {
        "id": "search_papers",
        "name": "Search Papers",
        "label": "检索论文",
        "description": "Collect candidate papers from the selected source.",
    },
    {
        "id": "rank_papers",
        "name": "Rank Evidence",
        "label": "排序筛选",
        "description": "Score, deduplicate, and choose the core papers.",
    },
    {
        "id": "extract_evidence",
        "name": "Extract Evidence",
        "label": "抽取证据",
        "description": "Turn abstracts and metadata into structured evidence items.",
    },
    {
        "id": "synthesize_claims",
        "name": "Synthesize Claims",
        "label": "综合观点",
        "description": "Create claim records that point back to evidence.",
    },
    {
        "id": "check_citations",
        "name": "Verify Citations",
        "label": "引用校验",
        "description": "Check that selected citations and claim links are usable.",
    },
    {
        "id": "write_report",
        "name": "Write Report",
        "label": "生成报告",
        "description": "Render a Markdown literature review report.",
    },
    {
        "id": "evaluate_result",
        "name": "Evaluate Result",
        "label": "质量评估",
        "description": "Score completeness, traceability, and citation quality.",
    },
]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_step(definition: dict[str, str]) -> dict[str, Any]:
    return {
        **definition,
        "status": "idle",
        "elapsed_ms": None,
        "summary": "",
        "output_keys": [],
        "stats": {},
        "updated_at": None,
    }


def _safe_int(value: Any, default: int, minimum: int, maximum: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(minimum, min(maximum, parsed))


def normalize_run_request(payload: dict[str, Any]) -> dict[str, Any]:
    topic = str(payload.get("topic", "")).strip()
    if not topic:
        raise ValueError("Research topic cannot be empty.")

    raw_sources = payload.get("sources")
    if isinstance(raw_sources, list):
        sources = [
            str(source).strip().replace("-", "_")
            for source in raw_sources
            if str(source).strip().replace("-", "_") in ALLOWED_SOURCES
        ]
    else:
        source = str(payload.get("source", "offline")).strip().replace("-", "_")
        sources = ["arxiv", "semantic_scholar", "crossref"] if source == "hybrid" else [source]

    sources = list(dict.fromkeys(source for source in sources if source in ALLOWED_SOURCES))
    if not sources:
        sources = ["offline"]

    llm = str(payload.get("llm", "deepseek")).strip()
    if llm not in {"off", "deepseek"}:
        llm = "deepseek"

    from_year = _safe_int(payload.get("from_year"), DEFAULT_FROM_YEAR, 0, 2100)
    return {
        "topic": topic,
        "top_k": _safe_int(payload.get("top_k"), 5, 1, 200),
        "source": "+".join(sources),
        "sources": sources,
        "from_year": from_year,
        "candidate_multiplier": _safe_int(
            payload.get("candidate_multiplier"),
            DEFAULT_CANDIDATE_MULTIPLIER,
            1,
            20,
        ),
        "max_candidates": None,
        "llm": llm,
        "refine_topic": bool(payload.get("refine_topic", False)),
        "require_live": bool(payload.get("require_live", False)),
    }


def _build_initial_state(request: dict[str, Any], task_id: str, run_dir: Path) -> ResearchState:
    requested_source = request["source"]
    selected_sources = list(request.get("sources", [requested_source]))
    top_k = int(request["top_k"])
    candidate_multiplier = int(request["candidate_multiplier"])
    candidate_limit = candidate_limit_for(top_k, candidate_multiplier, request.get("max_candidates"))
    normalized_from_year = normalize_from_year(request.get("from_year"))
    slug = slugify(request["topic"])

    return {
        "task_id": task_id,
        "topic": request["topic"],
        "effective_topic": request["topic"],
        "refine_topic": bool(request.get("refine_topic", False)),
        "top_k": top_k,
        "candidate_multiplier": candidate_multiplier,
        "candidate_limit": candidate_limit,
        "from_year": normalized_from_year,
        "requested_source": requested_source,
        "selected_sources": selected_sources,
        "output_path": str(run_dir / f"{slug}.md"),
        "summary_output_path": str(run_dir / "summary.md"),
        "process_output_path": str(run_dir / "process.md"),
        "write_trace": True,
        "llm_provider": request["llm"],
        "llm_used": False,
        "llm_fallback_reason": "",
        "errors": [],
        "node_trace": [],
    }


def _count_statuses(checks: list[Any]) -> dict[str, int]:
    counts = {"passed": 0, "warning": 0, "failed": 0}
    for check in checks:
        status = getattr(check, "status", "")
        if status in counts:
            counts[status] += 1
    return counts


def _summarize_node(node_name: str, state: ResearchState, update: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    if node_name == "plan_queries":
        queries = state.get("query_plan", [])
        first = getattr(queries[0], "query_text", "") if queries else ""
        return (
            f"Planned {len(queries)} search queries.",
            {
                "first_query": first,
                "effective_topic": state.get("effective_topic", state.get("topic", "")),
                "topic_refinement_used": bool(state.get("topic_refinement_used", False)),
            },
        )

    if node_name == "search_papers":
        papers = state.get("searched_papers", [])
        actual_source = state.get("actual_source", "")
        fallback = state.get("fallback_reason", "")
        summary = f"Collected {len(papers)} candidate papers from {actual_source}."
        if fallback:
            summary += " Fallback was recorded."
        return summary, {"actual_source": actual_source, "fallback_reason": fallback}

    if node_name == "rank_papers":
        selected = state.get("selected_papers", [])
        ranked = state.get("ranked_candidates", [])
        top_title = getattr(selected[0], "title", "") if selected else ""
        return (
            f"Selected {len(selected)} core papers from {len(ranked)} ranked candidates.",
            {"top_paper": top_title},
        )

    if node_name == "extract_evidence":
        evidence = state.get("evidence_items", [])
        return (
            f"Extracted {len(evidence)} evidence items.",
            {
                "llm_used": bool(state.get("llm_used", False)),
                "llm_fallback_reason": state.get("llm_fallback_reason", ""),
            },
        )

    if node_name == "synthesize_claims":
        claims = state.get("claims", [])
        return f"Synthesized {len(claims)} auditable claims.", {"claim_count": len(claims)}

    if node_name == "check_citations":
        checks = state.get("citation_checks", [])
        counts = _count_statuses(checks)
        return (
            f"Checked {len(checks)} citation and evidence links.",
            counts,
        )

    if node_name == "write_report":
        markdown = state.get("report_markdown", "")
        return (
            f"Rendered {len(markdown)} Markdown characters.",
            {"report_path": state.get("report_path", "")},
        )

    if node_name == "evaluate_result":
        metrics = state.get("metrics", {})
        return (
            f"Overall score: {metrics.get('overall_score', 'n/a')}.",
            {
                "overall_score": metrics.get("overall_score"),
                "trace_complete": metrics.get("trace_complete"),
            },
        )

    return f"Produced {len(update)} output fields.", {}


def _snapshot_state(state: ResearchState) -> dict[str, Any]:
    return {
        "topic": state.get("topic", ""),
        "effective_topic": state.get("effective_topic", state.get("topic", "")),
        "refine_topic": bool(state.get("refine_topic", False)),
        "topic_refinement": _serialize(state.get("topic_refinement", {})),
        "topic_refinement_used": bool(state.get("topic_refinement_used", False)),
        "topic_refinement_fallback_reason": state.get("topic_refinement_fallback_reason", ""),
        "query_plan": _serialize(state.get("query_plan", [])),
        "searched_papers": _serialize(state.get("searched_papers", []))[:12],
        "selected_papers": _serialize(state.get("selected_papers", [])),
        "ranked_candidates": _serialize(state.get("ranked_candidates", []))[:20],
        "temporal_profile": _serialize(state.get("temporal_profile", {})),
        "corpus_profile": _serialize(state.get("corpus_profile", {})),
        "research_lens": _serialize(state.get("research_lens", {})),
        "evidence_items": _serialize(state.get("evidence_items", [])),
        "claims": _serialize(state.get("claims", [])),
        "citation_checks": _serialize(state.get("citation_checks", [])),
        "metrics": _serialize(state.get("metrics", {})),
        "node_trace": _serialize(state.get("node_trace", [])),
        "report_markdown": state.get("report_markdown", ""),
        "summary_markdown": state.get("summary_markdown", ""),
        "process_markdown": state.get("process_markdown", ""),
        "actual_source": state.get("actual_source", ""),
        "fallback_reason": state.get("fallback_reason", ""),
    }


class JobStore:
    def __init__(self) -> None:
        self._jobs: dict[str, dict[str, Any]] = {}
        self._lock = threading.Lock()

    def create(self, request: dict[str, Any]) -> dict[str, Any]:
        task_id = make_task_id(request["topic"])
        steps = [_new_step(step) for step in STEP_DEFINITIONS]
        job = {
            "id": task_id,
            "status": "queued",
            "request": request,
            "steps": steps,
            "current_step": None,
            "snapshots": {},
            "result": None,
            "error": None,
            "created_at": _now_iso(),
            "updated_at": _now_iso(),
        }
        with self._lock:
            self._jobs[task_id] = job
        return copy.deepcopy(job)

    def list_recent(self) -> list[dict[str, Any]]:
        with self._lock:
            jobs = list(self._jobs.values())
        jobs.sort(key=lambda item: item["created_at"], reverse=True)
        return copy.deepcopy(jobs[:20])

    def get(self, job_id: str) -> dict[str, Any] | None:
        with self._lock:
            job = self._jobs.get(job_id)
            return copy.deepcopy(job) if job else None

    def mutate(self, job_id: str, mutator: Any) -> dict[str, Any] | None:
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return None
            mutator(job)
            job["updated_at"] = _now_iso()
            return copy.deepcopy(job)


STORE = JobStore()


def _mutate_step(job: dict[str, Any], step_id: str, status: StepStatus, **fields: Any) -> None:
    for step in job["steps"]:
        if step["id"] == step_id:
            step["status"] = status
            step["updated_at"] = _now_iso()
            step.update(fields)
            break
    job["current_step"] = step_id if status == "running" else job.get("current_step")


def _mark_job(job_id: str, **fields: Any) -> None:
    STORE.mutate(job_id, lambda job: job.update(fields))


def _record_understanding(job_id: str, state: ResearchState) -> None:
    terms = topic_terms(state["topic"])[:8]
    summary = f"Topic normalized with {len(terms)} search terms and source {state['requested_source']}."
    stats = {
        "terms": terms,
        "sources": state.get("selected_sources", [state["requested_source"]]),
        "candidate_limit": state.get("candidate_limit"),
        "from_year": state.get("from_year"),
        "llm_provider": state.get("llm_provider", "off"),
        "refine_topic": bool(state.get("refine_topic", False)),
    }

    def mutate(job: dict[str, Any]) -> None:
        job["status"] = "running"
        _mutate_step(
            job,
            "understand_topic",
            "success",
            elapsed_ms=0,
            summary=summary,
            output_keys=[
                "topic",
                "requested_source",
                "selected_sources",
                "candidate_limit",
                "from_year",
                "llm_provider",
                "refine_topic",
            ],
            stats=stats,
        )
        job["snapshots"] = _snapshot_state(state)

    STORE.mutate(job_id, mutate)


def _run_web_job(job_id: str) -> None:
    job = STORE.get(job_id)
    if not job:
        return

    request = job["request"]
    run_dir = Path("data/web_runs") / job_id
    run_dir.mkdir(parents=True, exist_ok=True)
    state = _build_initial_state(request, job_id, run_dir)
    _record_understanding(job_id, state)

    trace: list[dict[str, Any]] = []
    try:
        for node_name, node_fn in RESEARCH_NODES:
            def start_mutation(job: dict[str, Any]) -> None:
                job["status"] = "running"
                _mutate_step(job, node_name, "running", summary="Running...", output_keys=[], stats={})

            STORE.mutate(job_id, start_mutation)
            start = perf_counter()
            update = node_fn(state)
            elapsed_ms = round((perf_counter() - start) * 1000, 3)
            trace.append(
                {
                    "node": node_name,
                    "status": "success",
                    "elapsed_ms": elapsed_ms,
                    "output_keys": sorted(update.keys()),
                }
            )
            state.update(update)
            state["node_trace"] = list(trace)
            summary, stats = _summarize_node(node_name, state, update)

            def success_mutation(job: dict[str, Any]) -> None:
                _mutate_step(
                    job,
                    node_name,
                    "success",
                    elapsed_ms=elapsed_ms,
                    summary=summary,
                    output_keys=sorted(update.keys()),
                    stats=stats,
                )
                job["snapshots"] = _snapshot_state(state)

            STORE.mutate(job_id, success_mutation)

        state["graph_runtime"] = "sequential_web"
        metrics = dict(state.get("metrics", {}))
        metrics["graph_runtime"] = "sequential_web"
        live_requirement_met = not (
            request.get("require_live")
            and state.get("requested_source") != "offline"
            and state.get("actual_source") == "offline"
        )
        metrics["live_requirement_met"] = live_requirement_met
        if not live_requirement_met:
            metrics["live_requirement_error"] = (
                "A live source was required, but the run fell back to offline fixtures."
            )
        state["metrics"] = metrics

        process_path = Path(str(state["process_output_path"]))
        process_markdown = render_process_markdown(state)
        process_path.parent.mkdir(parents=True, exist_ok=True)
        process_path.write_text(process_markdown, encoding="utf-8")
        state["process_path"] = str(process_path)
        state["process_markdown"] = process_markdown

        summary_path = Path(str(state["summary_output_path"]))
        summary_markdown = render_summary_report(state)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(summary_markdown, encoding="utf-8")
        state["summary_path"] = str(summary_path)
        state["summary_markdown"] = summary_markdown

        trace_path = Path("data/runtime") / job_id / "trace.json"
        write_json(
            trace_path,
            {
                "task_id": job_id,
                "topic": state["topic"],
                "graph_runtime": state.get("graph_runtime", ""),
                "query_plan": _serialize(state.get("query_plan", [])),
                "searched_papers": _serialize(state.get("searched_papers", [])),
                "ranked_candidates": _serialize(state.get("ranked_candidates", [])),
                "selected_papers": _serialize(state.get("selected_papers", [])),
                "research_lens": _serialize(state.get("research_lens", {})),
                "corpus_profile": _serialize(state.get("corpus_profile", {})),
                "temporal_profile": _serialize(state.get("temporal_profile", {})),
                "evidence_items": _serialize(state.get("evidence_items", [])),
                "claims": _serialize(state.get("claims", [])),
                "citation_checks": _serialize(state.get("citation_checks", [])),
                "node_trace": _serialize(state.get("node_trace", [])),
                "errors": _serialize(state.get("errors", [])),
                "process_path": str(process_path),
                "summary_path": str(summary_path),
                "metrics": metrics,
            },
        )

        status = "success" if live_requirement_met else "failed"
        result = ResearchResult(
            task_id=job_id,
            status=status,
            selected_papers=state.get("selected_papers", []),
            report_path=str(state["report_path"]),
            trace_path=str(trace_path),
            process_path=str(process_path),
            summary_path=str(summary_path),
            metrics=metrics,
        )

        def complete_mutation(job: dict[str, Any]) -> None:
            job["status"] = status
            job["current_step"] = None
            job["result"] = result.to_dict()
            job["snapshots"] = _snapshot_state(state)

        STORE.mutate(job_id, complete_mutation)
    except Exception as exc:  # pragma: no cover - defensive UI boundary.
        error_text = "".join(traceback.format_exception_only(type(exc), exc)).strip()
        trace.append(
            {
                "node": "web_runner",
                "status": "failed",
                "elapsed_ms": 0,
                "error": error_text,
            }
        )

        def failed_mutation(job: dict[str, Any]) -> None:
            job["status"] = "error"
            job["error"] = error_text
            job["current_step"] = None
            job["snapshots"] = _snapshot_state(state)
            job["snapshots"]["node_trace"] = trace

        STORE.mutate(job_id, failed_mutation)


def start_background_run(payload: dict[str, Any]) -> dict[str, Any]:
    request = normalize_run_request(payload)
    job = STORE.create(request)
    thread = threading.Thread(target=_run_web_job, args=(job["id"],), daemon=True)
    thread.start()
    return job


class ResearchFlowHandler(BaseHTTPRequestHandler):
    server_version = "ResearchFlowWeb/0.1"

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003 - stdlib signature
        return

    def _send_json(self, status: int, payload: Any, send_body: bool = True) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if send_body:
            self.wfile.write(body)

    def _send_bytes(
        self,
        status: int,
        body: bytes,
        content_type: str,
        send_body: bool = True,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if send_body:
            self.wfile.write(body)

    def _send_error_json(self, status: int, message: str) -> None:
        self._send_json(status, {"error": message})

    def _send_markdown_download(self, job: dict[str, Any], kind: str) -> None:
        key, filename = DOWNLOAD_KINDS[kind]
        markdown = str(job.get("snapshots", {}).get(key, "") or "")
        if not markdown:
            self._send_error_json(HTTPStatus.NOT_FOUND, "Markdown content is not ready.")
            return
        body = markdown.encode("utf-8")
        safe_id = slugify(str(job.get("id", "researchflow")), max_length=36)
        download_name = f"{safe_id}-{filename}"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/markdown; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Disposition", f'attachment; filename="{download_name}"')
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        if length > 256_000:
            raise ValueError("Request body is too large.")
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def _static_bytes(self, filename: str) -> tuple[bytes, str]:
        safe_name = filename.strip("/").replace("\\", "/")
        if ".." in safe_name or not safe_name:
            raise FileNotFoundError(filename)
        path = resources.files("researchflow").joinpath("web_static", safe_name)
        body = path.read_bytes()
        content_type = mimetypes.guess_type(safe_name)[0] or "application/octet-stream"
        if safe_name.endswith(".js"):
            content_type = "text/javascript; charset=utf-8"
        if safe_name.endswith(".css"):
            content_type = "text/css; charset=utf-8"
        if safe_name.endswith(".html"):
            content_type = "text/html; charset=utf-8"
        return body, content_type

    def _handle_get(self, send_body: bool) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        if path in {"/", "/index.html"}:
            body, content_type = self._static_bytes("index.html")
            self._send_bytes(HTTPStatus.OK, body, content_type, send_body=send_body)
            return

        if path.startswith("/static/"):
            try:
                body, content_type = self._static_bytes(path.removeprefix("/static/"))
            except FileNotFoundError:
                self._send_error_json(HTTPStatus.NOT_FOUND, "Static file not found.")
                return
            self._send_bytes(HTTPStatus.OK, body, content_type, send_body=send_body)
            return

        if path == "/api/health":
            self._send_json(
                HTTPStatus.OK,
                {"status": "ok", "service": "researchflow-web"},
                send_body=send_body,
            )
            return

        if path == "/api/runs":
            self._send_json(HTTPStatus.OK, {"runs": STORE.list_recent()}, send_body=send_body)
            return

        if path.startswith("/api/runs/"):
            parts = path.removeprefix("/api/runs/").strip("/").split("/")
            job_id = parts[0]
            job = STORE.get(job_id)
            if not job:
                self._send_error_json(HTTPStatus.NOT_FOUND, "Run not found.")
                return
            if len(parts) == 3 and parts[1] == "download" and parts[2] in DOWNLOAD_KINDS:
                if send_body:
                    self._send_markdown_download(job, parts[2])
                else:
                    self._send_json(HTTPStatus.OK, {"status": "ready"}, send_body=False)
                return
            self._send_json(HTTPStatus.OK, job, send_body=send_body)
            return

        self._send_error_json(HTTPStatus.NOT_FOUND, "Route not found.")

    def do_GET(self) -> None:  # noqa: N802 - stdlib hook
        self._handle_get(send_body=True)

    def do_HEAD(self) -> None:  # noqa: N802 - stdlib hook
        self._handle_get(send_body=False)

    def do_POST(self) -> None:  # noqa: N802 - stdlib hook
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path != "/api/runs":
            self._send_error_json(HTTPStatus.NOT_FOUND, "Route not found.")
            return
        try:
            payload = self._read_json_body()
            job = start_background_run(payload)
        except (ValueError, json.JSONDecodeError) as exc:
            self._send_error_json(HTTPStatus.BAD_REQUEST, str(exc))
            return
        self._send_json(HTTPStatus.ACCEPTED, job)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="researchflow-web")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8001)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    server = ThreadingHTTPServer((args.host, args.port), ResearchFlowHandler)
    print(f"ResearchFlow Web running at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
