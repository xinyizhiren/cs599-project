from researchflow.tools.semantic_scholar import (
    build_semantic_scholar_query_url,
    parse_semantic_scholar_response,
)


SAMPLE_RESPONSE = """
{
  "total": 1,
  "data": [
    {
      "paperId": "abc123",
      "title": "Tool-Augmented Literature Review Agents",
      "authors": [{"name": "Alice Researcher"}, {"name": "Bob Builder"}],
      "year": 2025,
      "abstract": "This paper studies query planning and citation checking.",
      "url": "https://www.semanticscholar.org/paper/abc123",
      "externalIds": {"DOI": "10.1234/example", "ArXiv": "2501.01234"},
      "citationCount": 42
    }
  ]
}
"""


def test_parse_semantic_scholar_response_extracts_metadata() -> None:
    papers = parse_semantic_scholar_response(SAMPLE_RESPONSE)

    assert len(papers) == 1
    paper = papers[0]
    assert paper.paper_id == "s2:abc123"
    assert paper.source == "semantic_scholar"
    assert paper.authors == ["Alice Researcher", "Bob Builder"]
    assert paper.year == 2025
    assert paper.doi == "10.1234/example"
    assert paper.arxiv_id == "2501.01234"
    assert paper.citation_count == 42


def test_build_semantic_scholar_query_url_encodes_query() -> None:
    url = build_semantic_scholar_query_url("agentic literature review", limit=5)

    assert "api.semanticscholar.org/graph/v1/paper/search" in url
    assert "agentic+literature+review" in url
    assert "limit=5" in url
