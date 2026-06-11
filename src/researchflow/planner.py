"""Query planning for ResearchFlow."""

from __future__ import annotations

import re

from .models import QueryItem


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "for",
    "in",
    "of",
    "on",
    "the",
    "to",
    "with",
}


def normalize_topic(topic: str) -> str:
    return " ".join(topic.strip().split())


def topic_terms(topic: str) -> list[str]:
    terms = re.findall(r"[A-Za-z][A-Za-z0-9_-]+", topic.lower())
    return [term for term in terms if term not in STOPWORDS and len(term) > 2]


def _clean_text_items(items: list[str] | None, max_items: int) -> list[str]:
    cleaned: list[str] = []
    seen: set[str] = set()
    for item in items or []:
        text = normalize_topic(str(item))
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(text)
        if len(cleaned) >= max_items:
            break
    return cleaned


def plan_queries(
    topic: str,
    source: str = "offline",
    *,
    adjacent_topics: list[str] | None = None,
    query_hints: list[str] | None = None,
    from_year: int = 2020,
    max_queries: int = 10,
) -> list[QueryItem]:
    """Create direct and adjacent search intents from a research topic."""

    clean_topic = normalize_topic(topic)
    if not clean_topic:
        raise ValueError("Research topic cannot be empty.")

    terms = topic_terms(clean_topic)
    core = " ".join(terms[:6]) or clean_topic
    query_specs: list[tuple[str, str, str]] = [
        (clean_topic, "core", "direct"),
        (f"{core} survey taxonomy", "survey_taxonomy", "direct"),
        (f"{core} methods systems architecture", "methods_systems", "direct"),
        (f"{core} evaluation benchmark dataset", "evaluation_benchmark", "direct"),
        (f"{core} challenges limitations open problems", "limitations_challenges", "direct"),
        (f"{core} applications case studies", "applications_domains", "adjacent"),
        (f"{core} security robustness hallucination", "security_robustness", "adjacent"),
    ]

    for hint in _clean_text_items(query_hints, max_items=3):
        query_specs.append((hint, "llm_hint", "adjacent"))

    for adjacent in _clean_text_items(adjacent_topics, max_items=3):
        query_specs.append((adjacent, "adjacent_topic", "adjacent"))

    unique_queries: list[tuple[str, str, str]] = []
    seen = set()
    for text, angle, distance in query_specs:
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        unique_queries.append((text, angle, distance))
        if len(unique_queries) >= max(1, max_queries):
            break

    return [
        QueryItem(
            query_id=f"q{index}",
            query_text=query_text,
            source=source,
            filters={
                "from_year": from_year,
                "angle": angle,
                "distance": distance,
            },
        )
        for index, (query_text, angle, distance) in enumerate(unique_queries, start=1)
    ]
