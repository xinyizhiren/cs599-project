"""OpenAlex Works API search tool."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from researchflow.env import load_local_env
from researchflow.models import PaperRecord


OPENALEX_WORKS_URL = "https://api.openalex.org/works"
USER_AGENT = "ResearchFlow/0.1 (cs599-course-project)"


class OpenAlexSearchError(RuntimeError):
    """Raised when OpenAlex search fails."""


def _as_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _clean_doi(value: Any) -> str | None:
    doi = str(value or "").strip()
    if not doi:
        return None
    if doi.startswith("https://doi.org/"):
        doi = doi.removeprefix("https://doi.org/")
    return doi or None


def _authors(authorships: Any) -> list[str]:
    if not isinstance(authorships, list):
        return ["Unknown"]
    names: list[str] = []
    for item in authorships:
        if not isinstance(item, dict):
            continue
        author = item.get("author")
        if not isinstance(author, dict):
            continue
        name = str(author.get("display_name", "")).strip()
        if name:
            names.append(name)
    return names or ["Unknown"]


def _abstract_from_inverted_index(index: Any) -> str:
    if not isinstance(index, dict):
        return ""
    positions: list[tuple[int, str]] = []
    for token, raw_positions in index.items():
        if not isinstance(raw_positions, list):
            continue
        for position in raw_positions:
            try:
                positions.append((int(position), str(token)))
            except (TypeError, ValueError):
                continue
    if not positions:
        return ""
    return " ".join(token for _, token in sorted(positions))


def _primary_url(item: dict[str, Any], doi: str | None) -> str:
    primary_location = item.get("primary_location")
    if isinstance(primary_location, dict):
        source_url = str(primary_location.get("landing_page_url") or "").strip()
        if source_url:
            return source_url
    openalex_id = str(item.get("id") or "").strip()
    if openalex_id:
        return openalex_id
    return f"https://doi.org/{doi}" if doi else ""


def _location_url(location: Any, key: str) -> str:
    if not isinstance(location, dict):
        return ""
    return str(location.get(key) or "").strip()


def _open_access_urls(item: dict[str, Any]) -> tuple[str | None, str | None]:
    primary_location = item.get("primary_location")
    pdf_url = _location_url(primary_location, "pdf_url")
    landing_url = _location_url(primary_location, "landing_page_url")

    for location in item.get("locations") or []:
        if not pdf_url:
            pdf_url = _location_url(location, "pdf_url")
        if not landing_url:
            landing_url = _location_url(location, "landing_page_url")
        if pdf_url and landing_url:
            break

    open_access = item.get("open_access")
    if isinstance(open_access, dict):
        oa_url = str(open_access.get("oa_url") or "").strip()
        if oa_url and not pdf_url and oa_url.lower().endswith(".pdf"):
            pdf_url = oa_url
        if oa_url and not landing_url:
            landing_url = oa_url

    return pdf_url or None, (pdf_url or landing_url or None)


def _concept_summary(item: dict[str, Any]) -> str:
    concepts = item.get("concepts")
    if not isinstance(concepts, list):
        return ""
    names = [
        str(concept.get("display_name", "")).strip()
        for concept in concepts[:5]
        if isinstance(concept, dict) and concept.get("display_name")
    ]
    return ", ".join(names)


def parse_openalex_response(json_text: str | dict[str, Any], limit: int | None = None) -> list[PaperRecord]:
    """Parse OpenAlex works JSON into PaperRecord objects."""

    if isinstance(json_text, dict):
        payload = json_text
    else:
        try:
            payload = json.loads(json_text)
        except json.JSONDecodeError as exc:
            raise OpenAlexSearchError(f"Invalid OpenAlex JSON: {exc}") from exc

    raw_items = payload.get("results", [])
    if not isinstance(raw_items, list):
        raise OpenAlexSearchError("OpenAlex JSON missing results list.")

    papers: list[PaperRecord] = []
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        openalex_id = str(item.get("id", "")).strip()
        title = str(item.get("title") or item.get("display_name") or "").strip()
        if not openalex_id or not title:
            continue

        doi = _clean_doi(item.get("doi"))
        abstract = _abstract_from_inverted_index(item.get("abstract_inverted_index"))
        if not abstract:
            concepts = _concept_summary(item)
            abstract = (
                "OpenAlex metadata record"
                + (f" with concepts: {concepts}" if concepts else "")
                + ". Abstract is not available in this metadata response."
            )

        arxiv_id = None
        ids = item.get("ids")
        if isinstance(ids, dict):
            arxiv_url = str(ids.get("arxiv") or "").strip()
            if arxiv_url:
                arxiv_id = arxiv_url.rstrip("/").rsplit("/", 1)[-1]

        paper_id = f"openalex:{openalex_id.rstrip('/').rsplit('/', 1)[-1]}"
        pdf_url, open_access_url = _open_access_urls(item)
        papers.append(
            PaperRecord(
                paper_id=paper_id,
                title=re.sub(r"\s+", " ", title),
                authors=_authors(item.get("authorships")),
                year=_as_int(item.get("publication_year")),
                abstract=re.sub(r"\s+", " ", abstract).strip(),
                url=_primary_url(item, doi),
                doi=doi,
                arxiv_id=arxiv_id,
                source="openalex",
                citation_count=_as_int(item.get("cited_by_count")),
                pdf_url=pdf_url or (f"https://arxiv.org/pdf/{arxiv_id}.pdf" if arxiv_id else None),
                open_access_url=open_access_url or (f"https://arxiv.org/pdf/{arxiv_id}.pdf" if arxiv_id else None),
                merged_sources=["openalex"],
                metadata_confidence=0.88 if doi or arxiv_id or pdf_url else 0.72,
            )
        )
        if limit is not None and len(papers) >= limit:
            break

    return papers


def build_openalex_query_url(
    query: str,
    limit: int = 20,
    from_year: int | None = None,
) -> str:
    clean_query = " ".join(query.strip().split())
    if not clean_query:
        raise ValueError("OpenAlex query cannot be empty.")

    params = {
        "search": clean_query,
        "per-page": str(max(1, min(limit, 100))),
        "sort": "relevance_score:desc",
    }
    filters: list[str] = []
    if from_year and from_year > 0:
        filters.append(f"from_publication_date:{from_year}-01-01")
    if filters:
        params["filter"] = ",".join(filters)
    mailto = os.environ.get("OPENALEX_MAILTO", "").strip()
    if mailto:
        params["mailto"] = mailto
    return f"{OPENALEX_WORKS_URL}?{urllib.parse.urlencode(params)}"


def _work_id(value: str) -> str:
    clean = str(value or "").strip()
    if not clean:
        return ""
    if clean.startswith("openalex:"):
        return clean.split(":", 1)[1]
    if "openalex.org/" in clean:
        return clean.rstrip("/").rsplit("/", 1)[-1]
    return clean


def build_openalex_filter_url(
    filter_value: str,
    limit: int = 20,
    from_year: int | None = None,
) -> str:
    params = {
        "filter": filter_value,
        "per-page": str(max(1, min(limit, 100))),
        "sort": "cited_by_count:desc",
    }
    filters: list[str] = [filter_value]
    if from_year and from_year > 0:
        filters.append(f"from_publication_date:{from_year}-01-01")
    params["filter"] = ",".join(filters)
    mailto = os.environ.get("OPENALEX_MAILTO", "").strip()
    if mailto:
        params["mailto"] = mailto
    return f"{OPENALEX_WORKS_URL}?{urllib.parse.urlencode(params)}"


def fetch_openalex_work(
    work_id: str,
    timeout: float = 20.0,
) -> dict[str, Any]:
    clean_id = _work_id(work_id)
    if not clean_id:
        raise OpenAlexSearchError("OpenAlex work id cannot be empty.")
    url = f"{OPENALEX_WORKS_URL}/{urllib.parse.quote(clean_id, safe='')}"
    mailto = os.environ.get("OPENALEX_MAILTO", "").strip()
    if mailto:
        url = f"{url}?{urllib.parse.urlencode({'mailto': mailto})}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8", errors="replace"))
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        raise OpenAlexSearchError(f"OpenAlex work fetch failed: {exc}") from exc


def search_openalex_filter(
    filter_value: str,
    limit: int = 20,
    timeout: float = 20.0,
    from_year: int | None = None,
) -> list[PaperRecord]:
    load_local_env()
    request = urllib.request.Request(
        build_openalex_filter_url(filter_value, limit=limit, from_year=from_year),
        headers={"User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            json_text = response.read().decode("utf-8", errors="replace")
    except (OSError, urllib.error.URLError) as exc:
        raise OpenAlexSearchError(f"OpenAlex filtered request failed: {exc}") from exc
    return parse_openalex_response(json_text, limit=limit)


def search_openalex_cited_by(
    work_id: str,
    limit: int = 20,
    timeout: float = 20.0,
    from_year: int | None = None,
) -> list[PaperRecord]:
    clean_id = _work_id(work_id)
    if not clean_id:
        return []
    return search_openalex_filter(
        f"cites:{clean_id}",
        limit=limit,
        timeout=timeout,
        from_year=from_year,
    )


def search_openalex_references(
    work_id: str,
    limit: int = 20,
    timeout: float = 20.0,
    from_year: int | None = None,
) -> list[PaperRecord]:
    work = fetch_openalex_work(work_id, timeout=timeout)
    referenced = work.get("referenced_works") or []
    if not isinstance(referenced, list) or not referenced:
        return []
    ids = [_work_id(str(item)) for item in referenced if str(item).strip()]
    if not ids:
        return []
    batches = ids[: max(1, min(limit, 25))]
    return search_openalex_filter(
        "openalex:" + "|".join(batches),
        limit=limit,
        timeout=timeout,
        from_year=from_year,
    )


def search_openalex_snowball(
    seed_work_ids: list[str],
    direction: str = "both",
    limit: int = 20,
    timeout: float = 20.0,
    from_year: int | None = None,
) -> tuple[list[PaperRecord], list[dict[str, Any]]]:
    """Expand OpenAlex seed works through references and citing papers."""

    collected: list[PaperRecord] = []
    records: list[dict[str, Any]] = []
    if direction not in {"none", "backward", "forward", "both"}:
        direction = "none"
    if direction == "none":
        return [], []

    per_seed_limit = max(1, min(limit, 20))
    for seed in seed_work_ids:
        clean_id = _work_id(seed)
        if not clean_id:
            continue
        for branch in ("backward", "forward"):
            if direction not in {branch, "both"}:
                continue
            try:
                papers = (
                    search_openalex_references(
                        clean_id,
                        limit=per_seed_limit,
                        timeout=timeout,
                        from_year=from_year,
                    )
                    if branch == "backward"
                    else search_openalex_cited_by(
                        clean_id,
                        limit=per_seed_limit,
                        timeout=timeout,
                        from_year=from_year,
                    )
                )
                for paper in papers:
                    sources = list(dict.fromkeys([*paper.merged_sources, f"snowball:{branch}"]))
                    paper.merged_sources = sources
                    paper.source = "openalex"
                collected.extend(papers)
                records.append(
                    {
                        "seed_paper_id": f"openalex:{clean_id}",
                        "direction": branch,
                        "added_paper_ids": [paper.paper_id for paper in papers],
                        "fallback_reason": "",
                    }
                )
            except OpenAlexSearchError as exc:
                records.append(
                    {
                        "seed_paper_id": f"openalex:{clean_id}",
                        "direction": branch,
                        "added_paper_ids": [],
                        "fallback_reason": str(exc),
                    }
                )
    return collected[:limit], records


def search_openalex(
    query: str,
    limit: int = 20,
    timeout: float = 20.0,
    from_year: int | None = None,
) -> list[PaperRecord]:
    """Search OpenAlex and return parsed work metadata."""

    load_local_env()
    request = urllib.request.Request(
        build_openalex_query_url(query, limit=limit, from_year=from_year),
        headers={"User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            json_text = response.read().decode("utf-8", errors="replace")
    except (OSError, urllib.error.URLError) as exc:
        raise OpenAlexSearchError(f"OpenAlex request failed: {exc}") from exc

    return parse_openalex_response(json_text, limit=limit)
