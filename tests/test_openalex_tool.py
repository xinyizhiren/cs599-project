from researchflow.tools.openalex import parse_openalex_response


def test_parse_openalex_response_reconstructs_inverted_abstract() -> None:
    payload = {
        "results": [
            {
                "id": "https://openalex.org/W123",
                "display_name": "Retrieval-Augmented Generation Survey",
                "publication_year": 2025,
                "doi": "https://doi.org/10.1234/rag-survey",
                "ids": {"arxiv": "https://arxiv.org/abs/2501.00001"},
                "cited_by_count": 42,
                "abstract_inverted_index": {
                    "Retrieval": [0],
                    "augmented": [1],
                    "generation": [2],
                    "is": [3],
                    "surveyed": [4],
                },
                "authorships": [
                    {"author": {"display_name": "A. Researcher"}},
                    {"author": {"display_name": "B. Scholar"}},
                ],
                "primary_location": {
                    "landing_page_url": "https://doi.org/10.1234/rag-survey",
                    "pdf_url": "https://example.org/rag-survey.pdf",
                },
                "open_access": {"oa_url": "https://example.org/rag-survey.pdf"},
            }
        ]
    }

    papers = parse_openalex_response(payload)

    assert len(papers) == 1
    assert papers[0].paper_id == "openalex:W123"
    assert papers[0].source == "openalex"
    assert papers[0].doi == "10.1234/rag-survey"
    assert papers[0].arxiv_id == "2501.00001"
    assert papers[0].abstract == "Retrieval augmented generation is surveyed"
    assert papers[0].citation_count == 42
    assert papers[0].pdf_url == "https://example.org/rag-survey.pdf"
    assert papers[0].open_access_url == "https://example.org/rag-survey.pdf"
    assert papers[0].metadata_confidence > 0.8
