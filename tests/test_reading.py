from researchflow.models import FullTextChunk, PaperRecord
from researchflow.reading import (
    build_reading_notes,
    build_rule_reading_note,
    chunk_full_text,
    derive_open_text_url,
    evidence_from_reading_notes,
    read_selected_full_texts,
)


def _paper(**kwargs):
    return PaperRecord(
        paper_id=kwargs.get("paper_id", "arxiv:2501.00001"),
        title=kwargs.get("title", "Retrieval-Augmented Generation Survey"),
        authors=["A. Author"],
        year=2025,
        abstract=kwargs.get(
            "abstract",
            "This survey introduces a retrieval framework. The method evaluates benchmarks. "
            "However, full deployment risks remain.",
        ),
        url=kwargs.get("url", "https://arxiv.org/abs/2501.00001"),
        arxiv_id=kwargs.get("arxiv_id", "2501.00001"),
        pdf_url=kwargs.get("pdf_url"),
        open_access_url=kwargs.get("open_access_url"),
        source="arxiv",
    )


def test_derive_open_text_url_prefers_pdf_and_arxiv_fallback() -> None:
    assert derive_open_text_url(_paper(pdf_url="https://example.org/paper.pdf")) == "https://example.org/paper.pdf"
    assert derive_open_text_url(_paper(pdf_url=None)) == "https://arxiv.org/pdf/2501.00001.pdf"


def test_chunk_full_text_and_rule_reading_note() -> None:
    paper = _paper()
    text = (
        "Introduction. This paper proposes a retrieval framework for grounded generation. "
        "Method. The method uses reranking and indexing. "
        "Evaluation. The experiment reports benchmark results. "
        "However, limitations include context length and noisy retrieval. "
    ) * 12

    chunks = chunk_full_text(paper, text, "https://example.org/paper.pdf", budget_chars=5000, chunk_chars=800)
    note = build_rule_reading_note(paper, chunks, status="full_text")

    assert chunks
    assert chunks[0].paper_id == paper.paper_id
    assert note.evidence_chunk_ids
    assert note.methods
    assert note.limitations


def test_read_selected_full_texts_abstract_mode_skips_network() -> None:
    chunks, budget = read_selected_full_texts([_paper()], "abstract", 3, 10000)

    assert chunks == []
    assert budget["attempted_papers"] == 0
    assert budget["successful_papers"] == 0


def test_build_reading_notes_uses_fake_llm(monkeypatch) -> None:
    class FakeClient:
        def generate_json(self, system_prompt, user_payload):
            return {
                "summary": "The paper studies grounded retrieval generation.",
                "methods": ["Reranking and indexing pipeline."],
                "experiments": ["Benchmark evaluation."],
                "limitations": ["Needs stronger full-text validation."],
                "future_work": ["Study robustness."],
                "evidence_chunk_ids": [user_payload["chunks"][0]["chunk_id"]],
            }

    paper = _paper()
    chunks = [
        FullTextChunk(
            chunk_id="ft-1",
            paper_id=paper.paper_id,
            text="Method and benchmark evidence.",
            source_url="https://example.org/paper.pdf",
        )
    ]
    monkeypatch.setattr("researchflow.reading.build_llm_client", lambda provider: FakeClient())

    notes, used, reason = build_reading_notes([paper], chunks, provider="deepseek")

    assert used is True
    assert reason == ""
    assert notes[0].source == "llm"
    assert notes[0].evidence_chunk_ids == ["ft-1"]


def test_evidence_from_reading_notes_produces_bound_evidence() -> None:
    paper = _paper()
    notes, _, _ = build_reading_notes([paper], [], provider="off")
    evidence = evidence_from_reading_notes(notes)

    assert evidence
    assert all(item.paper_id == paper.paper_id for item in evidence)
    assert {item.category for item in evidence} >= {"contribution", "method", "limitation"}


def test_fallback_reason_is_not_promoted_to_evidence() -> None:
    paper = _paper(abstract="This paper proposes a retrieval framework for grounded generation.")
    note = build_rule_reading_note(
        paper,
        [],
        status="abstract_fallback",
        fallback_reason="DeepSeek request failed: network blocked",
    )
    evidence = evidence_from_reading_notes([note])

    assert note.fallback_reason
    assert all("DeepSeek request failed" not in item.claim for item in evidence)
