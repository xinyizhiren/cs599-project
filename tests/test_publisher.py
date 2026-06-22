from researchflow.models import CitationCheck, EvidenceItem
from researchflow.offline_data import OFFLINE_PAPERS
from researchflow.publisher import publish_full_report_with_llm


def test_llm_publisher_filters_untrusted_references(monkeypatch) -> None:
    papers = OFFLINE_PAPERS[:2]
    evidence = [
        EvidenceItem(
            evidence_id="ev-1",
            paper_id=papers[0].paper_id,
            category="method",
            claim="The paper studies evidence-grounded literature review workflows.",
            support_text="The abstract discusses evidence-grounded research workflows.",
            confidence=0.82,
        ),
        EvidenceItem(
            evidence_id="ev-2",
            paper_id=papers[1].paper_id,
            category="limitation",
            claim="The paper highlights the need for citation checking.",
            support_text="The abstract discusses citation checking and auditability.",
            confidence=0.78,
        ),
    ]

    class FakeClient:
        def generate_json(self, system_prompt, user_payload):
            return {
                "title": "RAG 调研报告",
                "abstract": "这是一个基于证据的中文综合报告。",
                "scope_and_strategy": [
                    {
                        "description": "系统从多源检索和证据矩阵组织调研。",
                        "paper_refs": ["P1"],
                        "evidence_ids": ["ev-1"],
                    }
                ],
                "field_map": [
                    {
                        "name": "证据约束生成",
                        "description": "报告围绕证据组织，而不是堆叠论文。",
                        "paper_refs": ["P1", "P999"],
                        "evidence_ids": ["ev-1", "missing-evidence"],
                    }
                ],
                "key_findings": [
                    {
                        "finding": "证据链是可靠调研的核心。",
                        "why_it_matters": "它降低了幻觉引用风险。",
                        "paper_refs": ["P2", "P404"],
                        "evidence_ids": ["ev-2", "fake"],
                    }
                ],
                "method_comparison": [],
                "benchmarks_and_metrics": [],
                "controversies_and_limits": [],
                "future_directions": [],
                "reading_roadmap": [{"step": "先读核心论文", "papers": ["P1", "P999"], "reason": "建立地图"}],
            }

    monkeypatch.setattr("researchflow.publisher.build_llm_client", lambda provider: FakeClient())
    report = publish_full_report_with_llm(
        {
            "topic": "retrieval augmented generation",
            "effective_topic": "retrieval augmented generation",
            "actual_source": "offline",
            "selected_papers": papers,
            "ranked_candidates": papers,
            "searched_papers": papers,
            "evidence_items": evidence,
            "citation_checks": [
                CitationCheck("check-1", papers[0].paper_id, "passed", "ok"),
                CitationCheck("check-2", papers[1].paper_id, "passed", "ok"),
            ],
            "query_tree": {
                "branches": [
                    {
                        "question": "How should RAG literature be organized?",
                        "subtopics": [],
                    }
                ]
            },
            "query_plan": [],
            "research_lens": {},
            "corpus_profile": {},
            "source_results": {},
            "reading_notes": [],
            "full_text_chunks": [],
            "snowball_records": [],
        },
        provider="deepseek",
    )

    assert "RAG 调研报告" in report
    assert "系统从多源检索和证据矩阵组织调研。" in report
    assert "[{" not in report
    assert "`P1`" in report
    assert "`P2`" in report
    assert "`ev-1`" in report
    assert "`ev-2`" in report
    assert "P999" not in report
    assert "P404" not in report
    assert "missing-evidence" not in report
    assert "fake" not in report
