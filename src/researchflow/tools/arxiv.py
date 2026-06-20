"""arXiv search tool.

The arXiv API returns Atom XML. This module keeps the parsing logic small and
dependency-free so the MVP can run in restricted environments.
"""

from __future__ import annotations

import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

from researchflow.models import PaperRecord


ARXIV_API_URL = "https://export.arxiv.org/api/query"
ARXIV_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}
USER_AGENT = "ResearchFlow/0.1 (cs599-course-project)"


class ArxivSearchError(RuntimeError):
    """Raised when arXiv search fails."""


def _text(parent: ET.Element, path: str) -> str:
    element = parent.find(path, ARXIV_NS)
    return normalize_whitespace(element.text if element is not None else "")


def normalize_whitespace(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def extract_arxiv_id(entry_id: str) -> str | None:
    if not entry_id:
        return None
    if "/abs/" in entry_id:
        return entry_id.rsplit("/abs/", 1)[-1]
    return entry_id.rsplit("/", 1)[-1] or None


def parse_year(published: str) -> int:
    if not published:
        return 0
    try:
        return datetime.fromisoformat(published.replace("Z", "+00:00")).year
    except ValueError:
        match = re.search(r"\d{4}", published)
        return int(match.group(0)) if match else 0


def parse_arxiv_feed(xml_text: str, limit: int | None = None) -> list[PaperRecord]:
    """Parse arXiv Atom XML into PaperRecord objects."""

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise ArxivSearchError(f"Invalid arXiv XML: {exc}") from exc

    papers: list[PaperRecord] = []
    for entry in root.findall("atom:entry", ARXIV_NS):
        entry_id = _text(entry, "atom:id")
        arxiv_id = extract_arxiv_id(entry_id)
        title = _text(entry, "atom:title")
        abstract = _text(entry, "atom:summary")
        published = _text(entry, "atom:published")
        authors = [
            _text(author, "atom:name")
            for author in entry.findall("atom:author", ARXIV_NS)
        ]
        authors = [author for author in authors if author]
        doi = _text(entry, "arxiv:doi") or None

        if not title or not arxiv_id:
            continue

        papers.append(
            PaperRecord(
                paper_id=f"arxiv:{arxiv_id}",
                title=title,
                authors=authors or ["Unknown"],
                year=parse_year(published),
                abstract=abstract,
                url=entry_id or f"https://arxiv.org/abs/{arxiv_id}",
                doi=doi,
                arxiv_id=arxiv_id,
                source="arxiv",
                pdf_url=f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                open_access_url=f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                merged_sources=["arxiv"],
                metadata_confidence=0.9,
            )
        )
        if limit is not None and len(papers) >= limit:
            break

    return papers


def build_arxiv_query_url(query: str, limit: int = 20) -> str:
    clean_query = normalize_whitespace(query).replace('"', "")
    if not clean_query:
        raise ValueError("arXiv query cannot be empty.")

    terms = re.findall(r"[A-Za-z0-9][A-Za-z0-9_-]+", clean_query)
    search_terms = [term for term in terms if len(term) > 2][:8]
    normalized = clean_query.lower()
    if "retrieval augmented generation" in normalized or "retrieval-augmented generation" in normalized:
        search_query = 'all:"retrieval augmented generation" OR all:"retrieval-augmented generation" OR all:RAG'
    else:
        # arXiv can be slow or return no results for long all:term AND chains.
        # Prefer broad recall here and let the local ranker perform precision filtering.
        search_query = " OR ".join(f"all:{term}" for term in search_terms[:6]) or f'all:"{clean_query}"'
    params = {
        "search_query": search_query,
        "start": "0",
        "max_results": str(max(1, min(limit, 50))),
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    return f"{ARXIV_API_URL}?{urllib.parse.urlencode(params)}"


def search_arxiv(query: str, limit: int = 20, timeout: float = 20.0) -> list[PaperRecord]:
    """Search arXiv and return parsed paper metadata."""

    url = build_arxiv_query_url(query, limit=limit)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            xml_text = response.read().decode("utf-8", errors="replace")
    except OSError as exc:
        raise ArxivSearchError(f"arXiv request failed: {exc}") from exc

    return parse_arxiv_feed(xml_text, limit=limit)
