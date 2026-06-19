from pathlib import Path

from researchflow.conversation import classify_conversation_intent, handle_conversation_turn
from researchflow.models import PaperRecord
from researchflow.pipeline import run_research
from researchflow.session import load_session
from researchflow.web import continue_conversation


def _offline_state(topic: str = "Agentic RAG for enterprise knowledge management"):
    result = run_research(
        topic,
        top_k=3,
        output="tmp/test_outputs/conversation-report.md",
        summary_output="tmp/test_outputs/conversation-summary.md",
        process_output="tmp/test_outputs/conversation-process.md",
        offline=True,
        write_trace=False,
        llm="off",
    )
    return load_session(result.task_id)["state"]


def test_conversation_intent_uses_fake_llm(monkeypatch) -> None:
    class FakeClient:
        def generate_json(self, system_prompt, user_payload):
            return {
                "action": "expand_search",
                "parameters": {"angle": "security_robustness"},
                "rationale": "User wants more security papers.",
            }

    monkeypatch.setattr("researchflow.conversation.build_llm_client", lambda provider: FakeClient())
    state = {"llm_provider": "deepseek", "selected_papers": [], "metrics": {}}

    intent = classify_conversation_intent(state, "多补充安全方向")

    assert intent["action"] == "expand_search"
    assert intent["parameters"]["angle"] == "security_robustness"
    assert intent["classifier"] == "deepseek"


def test_session_save_load_roundtrip_from_run_research() -> None:
    state = _offline_state()

    assert state["session_id"] == state["task_id"]
    assert state["selected_papers"]
    assert state["report_markdown"]
    assert isinstance(state["selected_papers"][0].title, str)


def test_rewrite_report_updates_summary_without_new_citations() -> None:
    state = _offline_state()

    result = handle_conversation_turn(state, "把总结写得更短")

    assert result["action"] == "rewrite_report"
    assert result["updated"] is True
    assert "对话调整后总结" in state["summary_markdown"]
    assert "Conversation Revisions" in state["process_markdown"]
    assert "http://fake" not in state["report_markdown"]


def test_expand_search_adds_query_and_rebuilds(monkeypatch) -> None:
    state = _offline_state("retrieval augmented generation")

    def fake_search(topic, query_plan, sources, limit, **kwargs):
        return (
            [
                PaperRecord(
                    paper_id="arxiv:security-rag",
                    title="Security and Robustness Benchmarks for Retrieval-Augmented Generation",
                    authors=["A. Author"],
                    year=2026,
                    abstract="This paper evaluates security, robustness, hallucination, and attacks in RAG.",
                    url="https://arxiv.org/abs/security-rag",
                    source="arxiv",
                    citation_count=7,
                )
            ],
            "arxiv",
            None,
        )

    monkeypatch.setattr("researchflow.conversation.search_selected_sources", fake_search)

    result = handle_conversation_turn(state, "多补充 security robustness 方向")

    assert result["action"] == "expand_search"
    assert any(query.filters.get("conversation") for query in state["query_plan"])
    assert any(paper.paper_id == "arxiv:security-rag" for paper in state["searched_papers"])


def test_filter_papers_removes_domain_applications() -> None:
    state = _offline_state("retrieval augmented generation")
    application = PaperRecord(
        paper_id="app:education",
        title="RAG Chatbot Application for Education",
        authors=["A. Teacher"],
        year=2025,
        abstract="This application case study deploys a RAG chatbot in education.",
        url="https://example.org/app",
        source="crossref",
        citation_count=1,
        score=99.0,
    )
    state["searched_papers"] = [application] + state["searched_papers"]
    state["ranked_candidates"] = [application] + state["ranked_candidates"]
    state["selected_papers"] = [application] + state["selected_papers"][:2]

    result = handle_conversation_turn(state, "去掉应用案例论文")

    assert result["action"] == "filter_papers"
    assert "app:education" in state["excluded_paper_ids"]
    assert all(paper.paper_id != "app:education" for paper in state["selected_papers"])
    assert all(item.paper_id != "app:education" for item in state["evidence_items"])


def test_continue_conversation_loads_persisted_session() -> None:
    result = run_research(
        "Long-term memory mechanisms for LLM agents",
        top_k=2,
        output="tmp/test_outputs/web-conversation-report.md",
        summary_output="tmp/test_outputs/web-conversation-summary.md",
        process_output="tmp/test_outputs/web-conversation-process.md",
        offline=True,
        write_trace=False,
        llm="off",
    )

    response = continue_conversation(result.task_id, {"message": "把总结写得更短"})

    assert response["action"] == "rewrite_report"
    assert response["run"]["messages"]
    assert response["snapshots"]["documents"]["summary"]["ready"] is True
    assert Path("tmp/test_outputs/web-conversation-summary.md").exists()
