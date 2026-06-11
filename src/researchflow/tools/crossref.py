"""Crossref REST API search tool."""

from __future__ import annotations

import html
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from researchflow.env import load_local_env
from researchflow.models import PaperRecord


CROSSREF_WORKS_URL = "https://api.crossref.org/works"
USER_AGENT = "ResearchFlow/0.1 (cs599-course-project)"


class CrossrefSearchError(RuntimeError):
    """Raised when Crossref search fails."""


def _first_text(value: Any) -> str:
    if isinstance(value, list) and value:
        return str(value[0]).strip()
    return str(value or "").strip()


def _clean_abstract(value: Any) -> str:
    text = html.unescape(str(value or "")).strip()
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _authors(raw_authors: Any) -> list[str]:
    if not isinstance(raw_authors, list):
        return ["Unknown"]
    names: list[str] = []
    for author in raw_authors:
        if not isinstance(author, dict):
            continue
        given = str(author.get("given", "")).strip()
        family = str(author.get("family", "")).strip()
        name = " ".join(part for part in [given, family] if part)
        if name:
            names.append(name)
    return names or ["Unknown"]


def _published_year(item: dict[str, Any]) -> int:
    for key in ["published-print", "published-online", "published", "issued", "created"]:
        value = item.get(key)
        if not isinstance(value, dict):
            continue
        date_parts = value.get("date-parts")
        if (
            isinstance(date_parts, list)
            and date_parts
            and isinstance(date_parts[0], list)
            and date_parts[0]
        ):
            try:
                return int(date_parts[0][0])
            except (TypeError, ValueError):
                continue
    return 0


def parse_crossref_response(json_text: str, limit: int | None = None) -> list[PaperRecord]:
    """Parse Crossref works JSON into PaperRecord objects."""

    try:
        payload = json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise CrossrefSearchError(f"Invalid Crossref JSON: {exc}") from exc

    message = payload.get("message", {})
    if not isinstance(message, dict):
        raise CrossrefSearchError("Crossref JSON missing message object.")
    raw_items = message.get("items", [])
    if not isinstance(raw_items, list):
        raise CrossrefSearchError("Crossref JSON missing message.items list.")

    papers: list[PaperRecord] = []
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        doi = str(item.get("DOI", "")).strip()
        title = _first_text(item.get("title"))
        if not doi or not title:
            continue

        abstract = _clean_abstract(item.get("abstract"))
        if not abstract:
            container = _first_text(item.get("container-title"))
            work_type = str(item.get("type", "work")).replace("-", " ")
            abstract = (
                f"Crossref metadata record for {work_type}"
                + (f" published in {container}" if container else "")
                + ". Abstract is not available in this metadata response."
            )
        url = str(item.get("URL") or f"https://doi.org/{doi}").strip()

        papers.append(
            PaperRecord(
                paper_id=f"crossref:{doi.lower()}",
                title=title,
                authors=_authors(item.get("author")),
                year=_published_year(item),
                abstract=abstract,
                url=url,
                doi=doi,
                source="crossref",
                citation_count=int(item.get("is-referenced-by-count") or 0),
            )
        )
        if limit is not None and len(papers) >= limit:
            break

    return papers


def build_crossref_query_url(
    query: str,
    limit: int = 20,
    from_year: int | None = None,
) -> str:
    clean_query = " ".join(query.strip().split())
    if not clean_query:
        raise ValueError("Crossref query cannot be empty.")

    params = {
        "query.bibliographic": clean_query,
        "rows": str(max(1, min(limit, 100))),
        "sort": "relevance",
        "order": "desc",
    }
    if from_year and from_year > 0:
        params["filter"] = f"from-pub-date:{from_year}-01-01"
    mailto = os.environ.get("CROSSREF_MAILTO", "").strip()
    if mailto:
        params["mailto"] = mailto
    return f"{CROSSREF_WORKS_URL}?{urllib.parse.urlencode(params)}"


def search_crossref(
    query: str,
    limit: int = 20,
    timeout: float = 20.0,
    from_year: int | None = None,
) -> list[PaperRecord]:
    """Search Crossref and return parsed work metadata."""

    load_local_env()
    url = build_crossref_query_url(query, limit=limit, from_year=from_year)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            json_text = response.read().decode("utf-8", errors="replace")
    except (OSError, urllib.error.URLError) as exc:
        raise CrossrefSearchError(f"Crossref request failed: {exc}") from exc

    return parse_crossref_response(json_text, limit=limit)
