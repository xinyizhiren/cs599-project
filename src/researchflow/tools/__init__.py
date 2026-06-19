"""External tool adapters for ResearchFlow."""

from .arxiv import ArxivSearchError, parse_arxiv_feed, search_arxiv
from .crossref import CrossrefSearchError, parse_crossref_response, search_crossref
from .openalex import OpenAlexSearchError, parse_openalex_response, search_openalex
from .semantic_scholar import (
    SemanticScholarSearchError,
    parse_semantic_scholar_response,
    search_semantic_scholar,
)
from .tavily import TavilySearchError, parse_tavily_response, search_tavily

__all__ = [
    "ArxivSearchError",
    "CrossrefSearchError",
    "OpenAlexSearchError",
    "SemanticScholarSearchError",
    "TavilySearchError",
    "parse_arxiv_feed",
    "parse_crossref_response",
    "parse_openalex_response",
    "parse_semantic_scholar_response",
    "parse_tavily_response",
    "search_arxiv",
    "search_crossref",
    "search_openalex",
    "search_semantic_scholar",
    "search_tavily",
]
