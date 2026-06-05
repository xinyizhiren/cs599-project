"""Offline paper fixtures for a deterministic MVP demo."""

from __future__ import annotations

from .models import PaperRecord


OFFLINE_PAPERS: list[PaperRecord] = [
    PaperRecord(
        paper_id="offline:agentic-rag-survey-2025",
        title="A Survey of Agentic Retrieval-Augmented Generation",
        authors=["L. Chen", "M. Patel"],
        year=2025,
        abstract=(
            "This survey summarizes agentic retrieval-augmented generation systems, "
            "including query planning, tool use, reflection, memory, and evaluation "
            "for enterprise knowledge workflows."
        ),
        url="https://example.org/papers/agentic-rag-survey-2025",
        source="offline",
        citation_count=42,
    ),
    PaperRecord(
        paper_id="offline:multi-agent-collaboration-2024",
        title="Multi-Agent Collaboration Patterns for Large Language Model Systems",
        authors=["S. Wang", "A. Kumar"],
        year=2024,
        abstract=(
            "The paper compares supervisor, planner-worker, debate, and reflection "
            "patterns for multi-agent LLM systems and studies their reliability in "
            "long-running tasks."
        ),
        url="https://example.org/papers/multi-agent-collaboration-2024",
        source="offline",
        citation_count=58,
    ),
    PaperRecord(
        paper_id="offline:citation-hallucination-2026",
        title="Detecting Citation Hallucinations in Scientific Text Generation",
        authors=["R. Smith", "Y. Zhao"],
        year=2026,
        abstract=(
            "This work introduces retrieval-grounded citation checking for scientific "
            "writing and evaluates title, author, DOI, and claim-evidence alignment."
        ),
        url="https://example.org/papers/citation-hallucination-2026",
        doi="10.0000/example.citecheck",
        source="offline",
        citation_count=9,
    ),
    PaperRecord(
        paper_id="offline:llm-agents-software-engineering-2024",
        title="LLM Agents for Software Engineering: Benchmarks and Workflows",
        authors=["J. Lee", "P. Garcia"],
        year=2024,
        abstract=(
            "This paper reviews LLM agents for code review, bug fixing, test generation, "
            "software maintenance, and benchmark-driven evaluation."
        ),
        url="https://example.org/papers/llm-agents-se-2024",
        source="offline",
        citation_count=73,
    ),
    PaperRecord(
        paper_id="offline:long-term-memory-agents-2025",
        title="Long-Term Memory Mechanisms for Stateful LLM Agents",
        authors=["N. Brown", "H. Li"],
        year=2025,
        abstract=(
            "The study analyzes episodic memory, vector memory, structured memory, "
            "and retrieval policies for stateful LLM agents across sessions."
        ),
        url="https://example.org/papers/long-term-memory-agents-2025",
        source="offline",
        citation_count=36,
    ),
    PaperRecord(
        paper_id="offline:research-agent-evaluation-2025",
        title="Evaluating Research Agents with Evidence-Centered Benchmarks",
        authors=["D. Miller", "F. Zhou"],
        year=2025,
        abstract=(
            "This paper proposes evidence-centered benchmarks for research agents, "
            "measuring source relevance, claim support, citation validity, and report completeness."
        ),
        url="https://example.org/papers/research-agent-evaluation-2025",
        source="offline",
        citation_count=24,
    ),
]
