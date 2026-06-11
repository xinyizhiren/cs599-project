import pytest

from researchflow.llm import DeepSeekClient, LLMError, parse_json_object
from researchflow.models import PaperRecord
from researchflow.offline_data import OFFLINE_PAPERS
from researchflow.pipeline import (
    chunk_papers_for_llm,
    extract_evidence_with_llm,
    node_extract_evidence,
    run_research,
)


def test_parse_json_object_accepts_fenced_json() -> None:
    parsed = parse_json_object('```json\n{"ok": true}\n```')

    assert parsed == {"ok": True}


def test_deepseek_without_key_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("researchflow.llm.load_local_env", lambda: None)
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    client = DeepSeekClient(api_key="")

    with pytest.raises(LLMError):
        client.generate_json("Return JSON.", {"topic": "test"})


def test_llm_evidence_extraction_accepts_valid_json(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeClient:
        def generate_json(self, system_prompt, user_payload):
            paper = user_payload["papers"][0]
            return {
                "evidence_items": [
                    {
                        "paper_id": paper["paper_id"],
                        "category": "method",
                        "claim": "The paper uses an agentic retrieval workflow.",
                        "support_text": paper["abstract"],
                        "confidence": 0.91,
                    }
                ]
            }

    monkeypatch.setattr("researchflow.pipeline.build_llm_client", lambda provider: FakeClient())

    evidence, chunk_count = extract_evidence_with_llm([OFFLINE_PAPERS[0]], provider="deepseek")

    assert len(evidence) == 1
    assert chunk_count == 1
    assert evidence[0].category == "method"
    assert evidence[0].confidence == 0.91


def test_llm_evidence_extraction_batches_large_inputs(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []

    class FakeClient:
        def generate_json(self, system_prompt, user_payload):
            calls.append(user_payload["batch_index"])
            paper = user_payload["papers"][0]
            return {
                "evidence_items": [
                    {
                        "paper_id": paper["paper_id"],
                        "category": "contribution",
                        "claim": f"{paper['title']} has usable evidence.",
                        "support_text": paper["abstract"],
                        "confidence": 0.8,
                    }
                ]
            }

    monkeypatch.setattr("researchflow.pipeline.build_llm_client", lambda provider: FakeClient())

    papers = [
        PaperRecord(
            paper_id=f"paper-{index}",
            title=f"Long Abstract Paper {index}",
            authors=["A. Author"],
            year=2025,
            abstract="Long abstract. " * 90,
            url=f"https://example.org/{index}",
        )
        for index in range(3)
    ]
    batches = chunk_papers_for_llm(papers, max_batch_chars=400)
    evidence, chunk_count = extract_evidence_with_llm(
        papers,
        provider="deepseek",
        max_batch_chars=400,
    )

    assert chunk_count == len(batches)
    assert chunk_count > 1
    assert calls == list(range(1, chunk_count + 1))
    assert len(evidence) == chunk_count


def test_node_extract_evidence_falls_back_when_llm_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    class FailingClient:
        def generate_json(self, system_prompt, user_payload):
            raise LLMError("boom")

    monkeypatch.setattr("researchflow.pipeline.build_llm_client", lambda provider: FailingClient())

    update = node_extract_evidence(
        {
            "selected_papers": [OFFLINE_PAPERS[0]],
            "llm_provider": "deepseek",
        }
    )

    assert update["llm_used"] is False
    assert "boom" in update["llm_fallback_reason"]
    assert update["llm_chunk_count"] == 0
    assert len(update["evidence_items"]) == 2


def test_run_research_deepseek_without_key_uses_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("researchflow.llm.load_local_env", lambda: None)
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    result = run_research(
        "Agentic RAG for enterprise knowledge management",
        top_k=2,
        output="tmp/test_outputs/deepseek-fallback.md",
        offline=True,
        write_trace=False,
        llm="deepseek",
    )

    assert result.status == "success"
    assert result.metrics["llm_provider"] == "deepseek"
    assert result.metrics["llm_used"] is False
    assert "DEEPSEEK_API_KEY" in result.metrics["llm_fallback_reason"]
