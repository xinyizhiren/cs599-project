"""Simple query planning for the offline MVP."""

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


def plan_queries(topic: str, source: str = "offline") -> list[QueryItem]:
    """Create several search intents from a user research topic."""

    clean_topic = normalize_topic(topic)
    if not clean_topic:
        raise ValueError("Research topic cannot be empty.")

    terms = topic_terms(clean_topic)
    core = " ".join(terms[:6]) or clean_topic
    query_texts = [
        clean_topic,
        f"{core} survey",
        f"{core} methods",
        f"{core} evaluation benchmark",
        f"{core} challenges limitations",
    ]

    unique_queries = []
    seen = set()
    for text in query_texts:
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        unique_queries.append(text)

    return [
        QueryItem(
            query_id=f"q{index}",
            query_text=query_text,
            source=source,
            filters={"from_year": 2020},
        )
        for index, query_text in enumerate(unique_queries, start=1)
    ]
