from researchflow.pipeline import node_plan_queries
from researchflow.planner import build_query_tree, plan_queries


def test_plan_queries_includes_multi_angle_and_adjacent_intents() -> None:
    queries = plan_queries(
        "retrieval augmented generation",
        source="arxiv",
        adjacent_topics=["context compression for LLMs", "citation hallucination"],
        query_hints=["RAG evaluation benchmark"],
        from_year=2024,
    )

    angles = {query.filters["angle"] for query in queries}
    distances = {query.filters["distance"] for query in queries}

    assert "core" in angles
    assert "evaluation_benchmark" in angles
    assert "security_robustness" in angles
    assert "adjacent_topic" in angles
    assert "adjacent" in distances
    assert all(query.filters["from_year"] == 2024 for query in queries)


def test_build_query_tree_contains_questions_and_adjacent_queries() -> None:
    tree = build_query_tree(
        "retrieval augmented generation",
        source="mixed",
        research_questions=["How should RAG systems be evaluated?"],
        adjacent_topics=["citation hallucination"],
        from_year=2024,
        depth=2,
        breadth=3,
    )

    assert tree["depth"] == 2
    assert len(tree["branches"]) >= 1
    assert tree["branches"][0]["question"]
    subtopics = [item for branch in tree["branches"] for item in branch["subtopics"]]
    assert subtopics
    assert any(item["distance"] == "adjacent" for item in subtopics)
    assert any(item["angle"] in {"benchmark", "method", "web_background", "core"} for item in subtopics)


def test_node_plan_queries_refines_fuzzy_topic_with_llm(monkeypatch) -> None:
    class FakeClient:
        def generate_json(self, system_prompt, user_payload):
            return {
                "refined_topic": "retrieval augmented generation for large language models",
                "research_questions": [
                    "How should RAG systems be evaluated?",
                    "How do retrieval and reranking affect grounding?",
                ],
                "adjacent_topics": [
                    "citation hallucination in language models",
                    "long context compression for retrieval systems",
                ],
                "query_hints": [
                    "retrieval augmented generation survey taxonomy",
                    "RAG evaluation benchmark dataset",
                ],
                "scope_notes": "Focus on recent system, evaluation, and reliability papers.",
            }

    monkeypatch.setattr("researchflow.pipeline.build_llm_client", lambda provider: FakeClient())

    update = node_plan_queries(
        {
            "topic": "RAG 怎么样",
            "requested_source": "arxiv",
            "from_year": 2024,
            "refine_topic": True,
            "llm_provider": "deepseek",
        }
    )

    assert update["topic_refinement_used"] is True
    assert update["effective_topic"] == "retrieval augmented generation for large language models"
    assert update["query_plan"][0].query_text == update["effective_topic"]
    assert any(query.filters["angle"] == "adjacent_topic" for query in update["query_plan"])


def test_node_plan_queries_falls_back_without_llm_provider() -> None:
    update = node_plan_queries(
        {
            "topic": "RAG 怎么样",
            "requested_source": "arxiv",
            "from_year": 2024,
            "refine_topic": True,
            "llm_provider": "off",
        }
    )

    assert update["topic_refinement_used"] is False
    assert update["effective_topic"] == "RAG 怎么样"
    assert "requires --llm deepseek" in update["topic_refinement_fallback_reason"]
