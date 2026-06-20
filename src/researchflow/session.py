"""Persistent local sessions for conversational research runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import (
    CitationCheck,
    ClaimRecord,
    EvidenceItem,
    FullTextChunk,
    PaperReadingNote,
    PaperRecord,
    QueryItem,
    ResearchMemoryItem,
    SnowballRecord,
)
from .state import ResearchState


SESSION_ROOT = Path("data/sessions")


def _serialize(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return value.to_dict()
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: _serialize(item) for key, item in value.items()}
    return value


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def session_dir(session_id: str) -> Path:
    safe_id = "".join(char if char.isalnum() or char in "-_" else "-" for char in session_id)
    return SESSION_ROOT / safe_id


def _restore_query_items(items: Any) -> list[QueryItem]:
    return [QueryItem(**item) for item in items or [] if isinstance(item, dict)]


def _restore_papers(items: Any) -> list[PaperRecord]:
    return [PaperRecord(**item) for item in items or [] if isinstance(item, dict)]


def _restore_evidence(items: Any) -> list[EvidenceItem]:
    return [EvidenceItem(**item) for item in items or [] if isinstance(item, dict)]


def _restore_full_text_chunks(items: Any) -> list[FullTextChunk]:
    return [FullTextChunk(**item) for item in items or [] if isinstance(item, dict)]


def _restore_reading_notes(items: Any) -> list[PaperReadingNote]:
    return [PaperReadingNote(**item) for item in items or [] if isinstance(item, dict)]


def _restore_snowball_records(items: Any) -> list[SnowballRecord]:
    return [SnowballRecord(**item) for item in items or [] if isinstance(item, dict)]


def _restore_research_memory(items: Any) -> list[ResearchMemoryItem]:
    return [ResearchMemoryItem(**item) for item in items or [] if isinstance(item, dict)]


def _restore_claims(items: Any) -> list[ClaimRecord]:
    return [ClaimRecord(**item) for item in items or [] if isinstance(item, dict)]


def _restore_checks(items: Any) -> list[CitationCheck]:
    return [CitationCheck(**item) for item in items or [] if isinstance(item, dict)]


def restore_state(payload: dict[str, Any]) -> ResearchState:
    state: ResearchState = dict(payload)
    if "query_plan" in state:
        state["query_plan"] = _restore_query_items(state.get("query_plan"))
    for key in ("searched_papers", "ranked_candidates", "selected_papers"):
        if key in state:
            state[key] = _restore_papers(state.get(key))
    if "evidence_items" in state:
        state["evidence_items"] = _restore_evidence(state.get("evidence_items"))
    if "full_text_chunks" in state:
        state["full_text_chunks"] = _restore_full_text_chunks(state.get("full_text_chunks"))
    if "reading_notes" in state:
        state["reading_notes"] = _restore_reading_notes(state.get("reading_notes"))
    if "snowball_records" in state:
        state["snowball_records"] = _restore_snowball_records(state.get("snowball_records"))
    if "research_memory" in state:
        state["research_memory"] = _restore_research_memory(state.get("research_memory"))
    if "claims" in state:
        state["claims"] = _restore_claims(state.get("claims"))
    if "citation_checks" in state:
        state["citation_checks"] = _restore_checks(state.get("citation_checks"))
    return state


def save_session(
    state: ResearchState,
    messages: list[dict[str, Any]] | None = None,
    artifacts: dict[str, str] | None = None,
) -> Path:
    session_id = str(state.get("session_id") or state.get("task_id") or "researchflow-session")
    state["session_id"] = session_id
    path = session_dir(session_id)
    path.mkdir(parents=True, exist_ok=True)

    messages = messages if messages is not None else list(state.get("conversation_messages", []))
    revision_history = list(state.get("revision_history", []))
    artifacts = artifacts or {
        "report.md": str(state.get("report_markdown", "")),
        "summary.md": str(state.get("summary_markdown", "")),
        "process.md": str(state.get("process_markdown", "")),
    }

    (path / "state.json").write_text(
        json.dumps(_serialize(state), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (path / "messages.jsonl").write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in messages),
        encoding="utf-8",
    )
    (path / "revision_history.jsonl").write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in revision_history),
        encoding="utf-8",
    )
    for filename, content in artifacts.items():
        (path / filename).write_text(content, encoding="utf-8")
    return path


def load_session(session_id: str) -> dict[str, Any]:
    path = session_dir(session_id)
    state_payload = _load_json(path / "state.json", {})
    if not state_payload:
        raise FileNotFoundError(f"Session not found: {session_id}")

    messages = [
        json.loads(line)
        for line in (path / "messages.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ] if (path / "messages.jsonl").exists() else []
    revision_history = [
        json.loads(line)
        for line in (path / "revision_history.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ] if (path / "revision_history.jsonl").exists() else []
    artifacts = {
        "report.md": (path / "report.md").read_text(encoding="utf-8") if (path / "report.md").exists() else "",
        "summary.md": (path / "summary.md").read_text(encoding="utf-8") if (path / "summary.md").exists() else "",
        "process.md": (path / "process.md").read_text(encoding="utf-8") if (path / "process.md").exists() else "",
    }
    state = restore_state(state_payload)
    state["conversation_messages"] = messages
    state["revision_history"] = revision_history
    return {
        "state": state,
        "messages": messages,
        "revision_history": revision_history,
        "artifacts": artifacts,
        "path": str(path),
    }


def list_sessions() -> list[dict[str, Any]]:
    if not SESSION_ROOT.exists():
        return []
    sessions: list[dict[str, Any]] = []
    for path in SESSION_ROOT.iterdir():
        if not path.is_dir() or not (path / "state.json").exists():
            continue
        try:
            session = load_session(path.name)
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            continue
        state: ResearchState = session["state"]
        sessions.append(
            {
                "session_id": state.get("session_id", path.name),
                "state": state,
                "messages": session["messages"],
                "artifacts": session["artifacts"],
                "updated_at": state.get("updated_at", state.get("created_at", "")),
            }
        )
    sessions.sort(key=lambda item: str(item.get("updated_at", "")), reverse=True)
    return sessions
