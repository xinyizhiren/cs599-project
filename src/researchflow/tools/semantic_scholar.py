"""Semantic Scholar Academic Graph search tool."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from researchflow.env import load_local_env
from researchflow.models import PaperRecord


SEMANTIC_SCHOLAR_SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
SEMANTIC_SCHOLAR_FIELDS = ",".join(
    [
        "paperId",
        "title",
        "authors",
        "year",
        "abstract",
        "url",
        "externalIds",
        "citationCount",
        "venue",
        "publicationDate",
    ]
)
USER_AGENT = "ResearchFlow/0.1 (cs599-course-project)"


class SemanticScholarSearchError(RuntimeError):
    """Raised when Semantic Scholar search fails."""


def _as_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _authors(raw_authors: Any) -> list[str]:
    if not isinstance(raw_authors, list):
        return ["Unknown"]
    names = [
        str(author.get("name", "")).strip()
        for author in raw_authors
        if isinstance(author, dict)
    ]
    return [name for name in names if name] or ["Unknown"]


def parse_semantic_scholar_response(json_text: str, limit: int | None = None) -> list[PaperRecord]:
    """Parse Semantic Scholar search JSON into PaperRecord objects."""

    try:
        payload = json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise SemanticScholarSearchError(f"Invalid Semantic Scholar JSON: {exc}") from exc

    raw_items = payload.get("data", [])
    if not isinstance(raw_items, list):
        raise SemanticScholarSearchError("Semantic Scholar JSON missing data list.")

    papers: list[PaperRecord] = []
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        paper_id = str(item.get("paperId", "")).strip()
        title = str(item.get("title", "")).strip()
        if not paper_id or not title:
            continue

        external_ids = item.get("externalIds") or {}
        if not isinstance(external_ids, dict):
            external_ids = {}
        doi = external_ids.get("DOI")
        arxiv_id = external_ids.get("ArXiv")
        url = str(item.get("url") or f"https://www.semanticscholar.org/paper/{paper_id}")
        abstract = str(
            item.get("abstract")
            or "No abstract is available in the Semantic Scholar metadata for this paper."
        ).strip()

        papers.append(
            PaperRecord(
                paper_id=f"s2:{paper_id}",
                title=title,
                authors=_authors(item.get("authors")),
                year=_as_int(item.get("year")),
                abstract=abstract,
                url=url,
                doi=str(doi).strip() if doi else None,
                arxiv_id=str(arxiv_id).strip() if arxiv_id else None,
                source="semantic_scholar",
                citation_count=_as_int(item.get("citationCount")),
            )
        )
        if limit is not None and len(papers) >= limit:
            break

    return papers


def build_semantic_scholar_query_url(query: str, limit: int = 20) -> str:
    clean_query = " ".join(query.strip().split())
    if not clean_query:
        raise ValueError("Semantic Scholar query cannot be empty.")

    params = {
        "query": clean_query,
        "limit": str(max(1, min(limit, 100))),
        "fields": SEMANTIC_SCHOLAR_FIELDS,
    }
    return f"{SEMANTIC_SCHOLAR_SEARCH_URL}?{urllib.parse.urlencode(params)}"


def search_semantic_scholar(
    query: str,
    limit: int = 20,
    timeout: float = 20.0,
) -> list[PaperRecord]:
    """Search Semantic Scholar and return parsed paper metadata."""

    load_local_env()
    request = urllib.request.Request(
        build_semantic_scholar_query_url(query, limit=limit),
        headers={"User-Agent": USER_AGENT},
    )
    api_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    if api_key:
        request.add_header("x-api-key", api_key)

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            json_text = response.read().decode("utf-8", errors="replace")
    except (OSError, urllib.error.URLError) as exc:
        raise SemanticScholarSearchError(f"Semantic Scholar request failed: {exc}") from exc

    return parse_semantic_scholar_response(json_text, limit=limit)
