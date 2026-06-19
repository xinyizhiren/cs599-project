"""Optional Tavily web search adapter."""

from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from typing import Any

from researchflow.env import load_local_env
from researchflow.models import PaperRecord


TAVILY_SEARCH_URL = "https://api.tavily.com/search"
USER_AGENT = "ResearchFlow/0.1 (cs599-course-project)"


class TavilySearchError(RuntimeError):
    """Raised when Tavily search fails."""


def _stable_web_id(url: str, title: str) -> str:
    digest = hashlib.sha1(f"{url}|{title}".encode("utf-8")).hexdigest()[:16]
    return f"web:{digest}"


def parse_tavily_response(json_text: str | dict[str, Any], limit: int | None = None) -> list[PaperRecord]:
    """Parse Tavily JSON into web-source PaperRecord objects."""

    if isinstance(json_text, dict):
        payload = json_text
    else:
        try:
            payload = json.loads(json_text)
        except json.JSONDecodeError as exc:
            raise TavilySearchError(f"Invalid Tavily JSON: {exc}") from exc

    raw_items = payload.get("results", [])
    if not isinstance(raw_items, list):
        raise TavilySearchError("Tavily JSON missing results list.")

    papers: list[PaperRecord] = []
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title", "")).strip()
        url = str(item.get("url", "")).strip()
        content = str(item.get("content") or item.get("raw_content") or "").strip()
        if not title or not url:
            continue
        papers.append(
            PaperRecord(
                paper_id=_stable_web_id(url, title),
                title=re.sub(r"\s+", " ", title),
                authors=["Web Source"],
                year=0,
                abstract=re.sub(r"\s+", " ", content)
                or "Web search result without extracted content.",
                url=url,
                source="web",
                citation_count=0,
                score=float(item.get("score", 0.0) or 0.0),
                paper_type="web_background",
            )
        )
        if limit is not None and len(papers) >= limit:
            break
    return papers


def search_tavily(
    query: str,
    limit: int = 10,
    timeout: float = 20.0,
) -> list[PaperRecord]:
    """Search Tavily when TAVILY_API_KEY exists; otherwise skip gracefully."""

    load_local_env()
    api_key = os.environ.get("TAVILY_API_KEY", "").strip()
    if not api_key:
        return []

    clean_query = " ".join(query.strip().split())
    if not clean_query:
        raise ValueError("Tavily query cannot be empty.")

    payload = json.dumps(
        {
            "api_key": api_key,
            "query": clean_query,
            "max_results": max(1, min(limit, 20)),
            "search_depth": "advanced",
            "include_answer": False,
            "include_raw_content": False,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        TAVILY_SEARCH_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            json_text = response.read().decode("utf-8", errors="replace")
    except (OSError, urllib.error.URLError) as exc:
        raise TavilySearchError(f"Tavily request failed: {exc}") from exc

    return parse_tavily_response(json_text, limit=limit)
