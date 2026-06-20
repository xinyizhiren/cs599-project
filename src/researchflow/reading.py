"""Open full-text reading and hierarchical synthesis helpers."""

from __future__ import annotations

import hashlib
import html
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from .llm import LLMError, build_llm_client
from .models import EvidenceItem, FullTextChunk, PaperReadingNote, PaperRecord, ResearchMemoryItem


CACHE_ROOT = Path("data/cache/full_text")
USER_AGENT = "ResearchFlow/0.1 (cs599-course-project)"
DEFAULT_CHUNK_CHARS = 2600


class FullTextReadError(RuntimeError):
    """Raised when an open full-text source cannot be read."""


def _slug(value: str, max_length: int = 56) -> str:
    clean = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return (clean[:max_length].strip("-") or "paper")


def derive_open_text_url(paper: PaperRecord) -> str | None:
    """Return a public PDF/HTML URL when metadata provides one."""

    for value in [paper.pdf_url, paper.open_access_url]:
        if value:
            return value
    if paper.arxiv_id:
        return f"https://arxiv.org/pdf/{paper.arxiv_id}.pdf"
    if paper.url and paper.url.lower().endswith(".pdf"):
        return paper.url
    return None


def cache_path_for(paper: PaperRecord, source_url: str) -> Path:
    digest = hashlib.sha1(source_url.encode("utf-8")).hexdigest()[:12]
    suffix = ".pdf" if source_url.lower().split("?", 1)[0].endswith(".pdf") else ".txt"
    return CACHE_ROOT / f"{_slug(paper.paper_id)}-{digest}{suffix}"


def fetch_open_text(paper: PaperRecord, timeout: float = 25.0) -> tuple[str, str, str]:
    """Fetch and cache an open full-text candidate.

    Returns `(text, source_url, status)`. The status is `pdf`, `html`, or `cache`.
    """

    source_url = derive_open_text_url(paper)
    if not source_url:
        raise FullTextReadError("No public PDF or open-access URL is available.")

    path = cache_path_for(paper, source_url)
    if path.exists() and path.stat().st_size > 0:
        raw = path.read_bytes()
        return extract_text_from_bytes(raw, path.suffix, source_url), source_url, "cache"

    path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(source_url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            content_type = str(response.headers.get("Content-Type", "")).lower()
    except (OSError, urllib.error.URLError) as exc:
        raise FullTextReadError(f"Open full-text download failed: {exc}") from exc

    suffix = ".pdf" if "pdf" in content_type or source_url.lower().endswith(".pdf") else ".txt"
    if path.suffix != suffix:
        path = path.with_suffix(suffix)
    path.write_bytes(raw)
    return extract_text_from_bytes(raw, suffix, source_url), source_url, "pdf" if suffix == ".pdf" else "html"


def extract_text_from_bytes(raw: bytes, suffix: str, source_url: str = "") -> str:
    if suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader  # type: ignore[import-not-found]
        except ImportError as exc:
            raise FullTextReadError("Optional dependency pypdf is not installed.") from exc

        from io import BytesIO

        try:
            reader = PdfReader(BytesIO(raw))
            pages = [page.extract_text() or "" for page in reader.pages[:40]]
        except Exception as exc:  # pragma: no cover - parser boundary.
            raise FullTextReadError(f"PDF parsing failed: {exc}") from exc
        text = "\n\n".join(page.strip() for page in pages if page.strip())
    else:
        decoded = raw.decode("utf-8", errors="replace")
        decoded = re.sub(r"(?is)<(script|style).*?</\1>", " ", decoded)
        decoded = re.sub(r"(?s)<[^>]+>", " ", decoded)
        text = html.unescape(decoded)

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(text) < 500:
        raise FullTextReadError(f"Open full-text source is too short after parsing: {source_url}")
    return text


def guess_section(text: str) -> str:
    head = text[:220].lower()
    for name in ["abstract", "introduction", "method", "experiment", "evaluation", "discussion", "conclusion"]:
        if name in head:
            return name
    return "body"


def chunk_full_text(
    paper: PaperRecord,
    text: str,
    source_url: str,
    budget_chars: int,
    chunk_chars: int = DEFAULT_CHUNK_CHARS,
) -> list[FullTextChunk]:
    chunks: list[FullTextChunk] = []
    cleaned = re.sub(r"\s+", " ", text).strip()
    max_chars = max(1000, budget_chars)
    cursor = 0
    while cursor < len(cleaned) and cursor < max_chars:
        end = min(len(cleaned), cursor + chunk_chars, max_chars)
        chunk_text = cleaned[cursor:end].strip()
        if chunk_text:
            chunks.append(
                FullTextChunk(
                    chunk_id=f"ft-{_slug(paper.paper_id, 24)}-{len(chunks) + 1}",
                    paper_id=paper.paper_id,
                    text=chunk_text,
                    source_url=source_url,
                    section_hint=guess_section(chunk_text),
                    token_estimate=max(1, len(chunk_text) // 4),
                    char_start=cursor,
                    char_end=end,
                )
            )
        cursor = end
    return chunks


def _sentences(text: str, limit: int = 3) -> list[str]:
    compact = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[.!?])\s+", compact)
    return [part.strip() for part in parts if part.strip()][:limit]


def build_rule_reading_note(
    paper: PaperRecord,
    chunks: list[FullTextChunk],
    status: str,
    fallback_reason: str = "",
) -> PaperReadingNote:
    corpus = " ".join(chunk.text for chunk in chunks[:4]) if chunks else paper.abstract
    sentences = _sentences(corpus, limit=20)
    summary = sentences[0] if sentences else paper.abstract[:260]
    methods = [item for item in sentences if re.search(r"\b(method|approach|framework|model|retrieval|rerank|index)\b", item, re.I)]
    experiments = [item for item in sentences if re.search(r"\b(experiment|evaluation|benchmark|dataset|metric|result)\b", item, re.I)]
    limitations = [
        item
        for item in sentences
        if re.search(r"\b(limitations?|challenges?|future|risks?|fail(?:ure|s)?|however)\b", item, re.I)
    ]
    return PaperReadingNote(
        note_id=f"note-{_slug(paper.paper_id, 32)}",
        paper_id=paper.paper_id,
        status=status,
        summary=summary,
        methods=methods[:3] or [paper.abstract[:240]],
        experiments=experiments[:3],
        limitations=limitations[:3],
        future_work=[],
        evidence_chunk_ids=[chunk.chunk_id for chunk in chunks[:4]],
        source="full_text" if chunks else "abstract",
        fallback_reason=fallback_reason,
    )


def _paper_chunks(chunks: list[FullTextChunk], paper_id: str) -> list[FullTextChunk]:
    return [chunk for chunk in chunks if chunk.paper_id == paper_id]


def _parse_llm_note(raw: dict[str, Any], paper: PaperRecord, chunks: list[FullTextChunk]) -> PaperReadingNote:
    return PaperReadingNote(
        note_id=f"note-{_slug(paper.paper_id, 32)}",
        paper_id=paper.paper_id,
        status="llm_full_text" if chunks else "llm_abstract",
        summary=str(raw.get("summary", "")).strip() or paper.abstract[:260],
        methods=[str(item).strip() for item in raw.get("methods", []) if str(item).strip()][:4],
        experiments=[str(item).strip() for item in raw.get("experiments", []) if str(item).strip()][:4],
        limitations=[str(item).strip() for item in raw.get("limitations", []) if str(item).strip()][:4],
        future_work=[str(item).strip() for item in raw.get("future_work", []) if str(item).strip()][:4],
        evidence_chunk_ids=[
            str(item).strip()
            for item in raw.get("evidence_chunk_ids", [])
            if str(item).strip() in {chunk.chunk_id for chunk in chunks}
        ][:6],
        source="llm",
        fallback_reason="",
    )


def build_reading_notes(
    papers: list[PaperRecord],
    chunks: list[FullTextChunk],
    provider: str = "off",
) -> tuple[list[PaperReadingNote], bool, str]:
    if provider != "deepseek":
        return [
            build_rule_reading_note(
                paper,
                _paper_chunks(chunks, paper.paper_id),
                status="full_text" if _paper_chunks(chunks, paper.paper_id) else "abstract_fallback",
            )
            for paper in papers
        ], False, "LLM provider is disabled for reading notes."

    client = build_llm_client(provider)
    notes: list[PaperReadingNote] = []
    try:
        for paper in papers:
            paper_chunks = _paper_chunks(chunks, paper.paper_id)
            payload = client.generate_json(
                (
                    "You create concise paper reading notes for a literature review agent. "
                    "Return JSON with summary, methods, experiments, limitations, future_work, "
                    "and evidence_chunk_ids. Use only the given paper and chunk IDs."
                ),
                {
                    "paper": {
                        "paper_id": paper.paper_id,
                        "title": paper.title,
                        "abstract": paper.abstract,
                    },
                    "chunks": [
                        {
                            "chunk_id": chunk.chunk_id,
                            "section_hint": chunk.section_hint,
                            "text": chunk.text[:1800],
                        }
                        for chunk in paper_chunks[:6]
                    ],
                },
            )
            notes.append(_parse_llm_note(payload, paper, paper_chunks))
    except LLMError as exc:
        return [
            build_rule_reading_note(
                paper,
                _paper_chunks(chunks, paper.paper_id),
                status="full_text" if _paper_chunks(chunks, paper.paper_id) else "abstract_fallback",
                fallback_reason=f"Reading-note LLM fallback: {exc}",
            )
            for paper in papers
        ], False, str(exc)
    return notes, True, ""


def read_selected_full_texts(
    papers: list[PaperRecord],
    read_depth: str,
    max_fulltext_papers: int,
    reading_budget_chars: int,
) -> tuple[list[FullTextChunk], dict[str, Any]]:
    if read_depth == "abstract":
        return [], {
            "read_depth": read_depth,
            "attempted_papers": 0,
            "successful_papers": 0,
            "failed_papers": 0,
            "failures": [],
            "used_chars": 0,
        }

    chunks: list[FullTextChunk] = []
    failures: list[dict[str, str]] = []
    used_chars = 0
    candidates = papers[: max(0, max_fulltext_papers)]
    per_paper_budget = max(1200, reading_budget_chars // max(len(candidates), 1))
    for paper in candidates:
        if used_chars >= reading_budget_chars:
            failures.append({"paper_id": paper.paper_id, "reason": "Reading budget exhausted."})
            continue
        try:
            text, source_url, status = fetch_open_text(paper)
            paper_budget = min(per_paper_budget, reading_budget_chars - used_chars)
            paper_chunks = chunk_full_text(paper, text, source_url, budget_chars=paper_budget)
            chunks.extend(paper_chunks)
            used_chars += sum(len(chunk.text) for chunk in paper_chunks)
            if status == "cache":
                continue
        except FullTextReadError as exc:
            failures.append({"paper_id": paper.paper_id, "reason": str(exc)})
            if read_depth == "fulltext":
                continue

    return chunks, {
        "read_depth": read_depth,
        "attempted_papers": len(candidates),
        "successful_papers": len({chunk.paper_id for chunk in chunks}),
        "failed_papers": len(failures),
        "failures": failures,
        "used_chars": used_chars,
        "budget_chars": reading_budget_chars,
    }


def evidence_from_reading_notes(notes: list[PaperReadingNote]) -> list[EvidenceItem]:
    evidence: list[EvidenceItem] = []
    for index, note in enumerate(notes, start=1):
        prefix = f"rn{index}"
        evidence.append(
            EvidenceItem(
                evidence_id=f"{prefix}-summary",
                paper_id=note.paper_id,
                category="contribution",
                claim=note.summary,
                support_text=note.summary,
                confidence=0.82 if note.source in {"full_text", "llm"} else 0.68,
            )
        )
        for category, values in [
            ("method", note.methods),
            ("experiment", note.experiments),
            ("limitation", note.limitations),
            ("future_work", note.future_work),
        ]:
            for item in values[:2]:
                evidence.append(
                    EvidenceItem(
                        evidence_id=f"{prefix}-{category}-{len(evidence) + 1}",
                        paper_id=note.paper_id,
                        category=category,
                        claim=item,
                        support_text=item,
                        confidence=0.78 if note.evidence_chunk_ids else 0.64,
                    )
                )
    return evidence


def build_question_synthesis(
    research_questions: list[str],
    notes: list[PaperReadingNote],
) -> list[dict[str, Any]]:
    if not research_questions:
        research_questions = ["What are the main methods, evidence, limitations, and future directions?"]
    rows: list[dict[str, Any]] = []
    note_text = {
        note.paper_id: " ".join([note.summary, *note.methods, *note.experiments, *note.limitations]).lower()
        for note in notes
    }
    for index, question in enumerate(research_questions, start=1):
        tokens = {token for token in re.findall(r"[A-Za-z0-9\u4e00-\u9fff]+", question.lower()) if len(token) > 2}
        matched = [
            note
            for note in notes
            if not tokens or any(token in note_text.get(note.paper_id, "") for token in tokens)
        ]
        if not matched:
            matched = notes[:3]
        rows.append(
            {
                "question_id": f"rq{index}",
                "question": question,
                "paper_ids": [note.paper_id for note in matched[:6]],
                "synthesis": "；".join(note.summary for note in matched[:3]),
                "evidence_chunk_ids": [
                    chunk_id
                    for note in matched[:4]
                    for chunk_id in note.evidence_chunk_ids[:2]
                ],
            }
        )
    return rows


def build_global_synthesis(notes: list[PaperReadingNote]) -> dict[str, Any]:
    method_count = sum(len(note.methods) for note in notes)
    experiment_count = sum(len(note.experiments) for note in notes)
    limitation_count = sum(len(note.limitations) for note in notes)
    full_text_count = sum(1 for note in notes if note.evidence_chunk_ids)
    return {
        "summary": (
            "The review uses a hierarchical compression path from papers to chunks, "
            "paper reading notes, research-question synthesis, and global synthesis."
        ),
        "paper_count": len(notes),
        "full_text_note_count": full_text_count,
        "method_signal_count": method_count,
        "experiment_signal_count": experiment_count,
        "limitation_signal_count": limitation_count,
    }


def build_research_memory(notes: list[PaperReadingNote], evidence: list[EvidenceItem]) -> list[ResearchMemoryItem]:
    evidence_by_paper: dict[str, list[str]] = {}
    for item in evidence:
        evidence_by_paper.setdefault(item.paper_id, []).append(item.evidence_id)
    return [
        ResearchMemoryItem(
            memory_id=f"mem-{index}",
            scope="paper_reading_note",
            content=note.summary,
            evidence_ids=evidence_by_paper.get(note.paper_id, [])[:4],
            paper_ids=[note.paper_id],
            confidence=0.82 if note.evidence_chunk_ids else 0.66,
        )
        for index, note in enumerate(notes, start=1)
    ]
