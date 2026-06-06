from researchflow.tools.arxiv import build_arxiv_query_url, parse_arxiv_feed


SAMPLE_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2401.01234v1</id>
    <updated>2024-01-03T00:00:00Z</updated>
    <published>2024-01-02T00:00:00Z</published>
    <title>Agentic Retrieval Augmented Generation for Research Workflows</title>
    <summary>
      This paper studies query planning, tool use, evidence extraction,
      and citation checking for research agents.
    </summary>
    <author>
      <name>Alice Researcher</name>
    </author>
    <author>
      <name>Bob Engineer</name>
    </author>
    <arxiv:doi>10.0000/example.arxiv</arxiv:doi>
  </entry>
</feed>
"""


def test_parse_arxiv_feed_extracts_metadata() -> None:
    papers = parse_arxiv_feed(SAMPLE_FEED)

    assert len(papers) == 1
    paper = papers[0]
    assert paper.paper_id == "arxiv:2401.01234v1"
    assert paper.arxiv_id == "2401.01234v1"
    assert paper.year == 2024
    assert paper.authors == ["Alice Researcher", "Bob Engineer"]
    assert paper.doi == "10.0000/example.arxiv"
    assert "citation checking" in paper.abstract


def test_build_arxiv_query_url_encodes_query() -> None:
    url = build_arxiv_query_url("agentic RAG evaluation", limit=5)

    assert "export.arxiv.org/api/query" in url
    assert "max_results=5" in url
    assert "agentic" in url
