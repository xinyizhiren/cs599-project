from researchflow.tools.tavily import parse_tavily_response, search_tavily


def test_parse_tavily_response_outputs_web_records() -> None:
    payload = {
        "results": [
            {
                "title": "RAG Benchmark Report",
                "url": "https://example.com/rag-benchmark",
                "content": "A web report discussing RAG benchmark trends and evaluation.",
                "score": 0.88,
            }
        ]
    }

    records = parse_tavily_response(payload)

    assert len(records) == 1
    assert records[0].source == "web"
    assert records[0].paper_type == "web_background"
    assert records[0].title == "RAG Benchmark Report"
    assert records[0].score == 0.88


def test_search_tavily_without_key_skips_gracefully(monkeypatch) -> None:
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)

    assert search_tavily("retrieval augmented generation", limit=3) == []
