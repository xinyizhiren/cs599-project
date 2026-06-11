from researchflow.tools.crossref import build_crossref_query_url, parse_crossref_response


SAMPLE_RESPONSE = """
{
  "status": "ok",
  "message": {
    "items": [
      {
        "DOI": "10.1234/example.rag",
        "title": ["Retrieval-Augmented Generation: A Review"],
        "author": [
          {"given": "Alice", "family": "Researcher"},
          {"given": "Bob", "family": "Builder"}
        ],
        "published-online": {"date-parts": [[2025, 3, 1]]},
        "abstract": "<jats:p>This paper reviews retrieval augmented generation.</jats:p>",
        "URL": "https://doi.org/10.1234/example.rag",
        "is-referenced-by-count": 17,
        "container-title": ["Example Journal"],
        "type": "journal-article"
      }
    ]
  }
}
"""


def test_parse_crossref_response_extracts_metadata() -> None:
    papers = parse_crossref_response(SAMPLE_RESPONSE)

    assert len(papers) == 1
    paper = papers[0]
    assert paper.paper_id == "crossref:10.1234/example.rag"
    assert paper.source == "crossref"
    assert paper.authors == ["Alice Researcher", "Bob Builder"]
    assert paper.year == 2025
    assert paper.doi == "10.1234/example.rag"
    assert paper.citation_count == 17
    assert "reviews retrieval augmented generation" in paper.abstract


def test_build_crossref_query_url_encodes_query_and_year() -> None:
    url = build_crossref_query_url("retrieval augmented generation", limit=5, from_year=2020)

    assert "api.crossref.org/works" in url
    assert "query.bibliographic=retrieval+augmented+generation" in url
    assert "rows=5" in url
    assert "from-pub-date%3A2020-01-01" in url
