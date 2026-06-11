"""External tool adapters for ResearchFlow."""

from .arxiv import ArxivSearchError, parse_arxiv_feed, search_arxiv
from .crossref import CrossrefSearchError, parse_crossref_response, search_crossref
from .semantic_scholar import (
    SemanticScholarSearchError,
    parse_semantic_scholar_response,
    search_semantic_scholar,
)

__all__ = [
    "ArxivSearchError",
    "CrossrefSearchError",
    "SemanticScholarSearchError",
    "parse_arxiv_feed",
    "parse_crossref_response",
    "parse_semantic_scholar_response",
    "search_arxiv",
    "search_crossref",
    "search_semantic_scholar",
]
