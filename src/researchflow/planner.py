"""Query planning for ResearchFlow."""

from __future__ import annotations

import re
from typing import Any

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


def default_research_questions(topic: str, breadth: int = 4) -> list[str]:
    clean_topic = normalize_topic(topic)
    templates = [
        f"{clean_topic} 的核心研究问题和技术边界是什么？",
        f"{clean_topic} 目前有哪些主流方法、系统架构和代表性路线？",
        f"{clean_topic} 通常如何评测，关键数据集和指标是什么？",
        f"{clean_topic} 的主要局限、风险和未来研究方向是什么？",
    ]
    return templates[: max(1, min(breadth, len(templates)))]


def build_query_tree(
    topic: str,
    *,
    source: str = "offline",
    research_questions: list[str] | None = None,
    adjacent_topics: list[str] | None = None,
    query_hints: list[str] | None = None,
    from_year: int = 2020,
    depth: int = 2,
    breadth: int = 4,
) -> dict[str, Any]:
    """Build a lightweight Deep Research-style query tree."""

    clean_topic = normalize_topic(topic)
    if not clean_topic:
        raise ValueError("Research topic cannot be empty.")

    question_items = _clean_text_items(research_questions, max_items=breadth)
    if not question_items:
        question_items = default_research_questions(clean_topic, breadth=breadth)

    direct_queries = plan_queries(
        clean_topic,
        source=source,
        adjacent_topics=adjacent_topics,
        query_hints=query_hints,
        from_year=from_year,
        max_queries=max(7, breadth * max(1, depth)),
    )
    angle_lookup = {
        "survey_taxonomy": "survey",
        "methods_systems": "method",
        "evaluation_benchmark": "benchmark",
        "applications_domains": "application",
        "security_robustness": "security",
        "limitations_challenges": "limitation",
        "llm_hint": "recent",
        "adjacent_topic": "web_background",
        "core": "core",
    }

    branches: list[dict[str, Any]] = []
    cursor = 0
    for q_index, question in enumerate(question_items, start=1):
        subqueries: list[dict[str, Any]] = []
        branch_budget = max(1, min(breadth, len(direct_queries)))
        for _ in range(branch_budget):
            query = direct_queries[cursor % len(direct_queries)]
            cursor += 1
            angle = query.filters.get("angle", "core")
            subqueries.append(
                {
                    "query_id": query.query_id,
                    "query_text": query.query_text,
                    "angle": angle_lookup.get(str(angle), str(angle)),
                    "distance": query.filters.get("distance", "direct"),
                    "source": source,
                    "from_year": from_year,
                }
            )
        if depth > 1 and not any(item["distance"] == "adjacent" for item in subqueries):
            adjacent_query = next(
                (
                    query
                    for query in direct_queries
                    if query.filters.get("distance") == "adjacent"
                ),
                None,
            )
            if adjacent_query is not None:
                angle = adjacent_query.filters.get("angle", "adjacent_topic")
                adjacent_payload = {
                    "query_id": adjacent_query.query_id,
                    "query_text": adjacent_query.query_text,
                    "angle": angle_lookup.get(str(angle), str(angle)),
                    "distance": adjacent_query.filters.get("distance", "adjacent"),
                    "source": source,
                    "from_year": from_year,
                }
                if len(subqueries) >= branch_budget:
                    subqueries[-1] = adjacent_payload
                else:
                    subqueries.append(adjacent_payload)
        branches.append(
            {
                "question_id": f"rq{q_index}",
                "question": question,
                "subtopics": subqueries,
            }
        )

    return {
        "topic": clean_topic,
        "depth": max(1, depth),
        "breadth": max(1, breadth),
        "research_questions": question_items,
        "branches": branches,
    }


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
