"""Evidence-constrained LLM publisher for full Chinese research reports."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any

from .llm import LLMError, build_llm_client
from .models import CitationCheck, EvidenceItem, PaperRecord


MAX_PUBLISHER_PAPERS = 30
MAX_PUBLISHER_EVIDENCE = 140


def _clip(value: Any, limit: int = 600) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)].rstrip() + "..."


def _text(value: Any, keys: tuple[str, ...] = ("description", "analysis", "summary", "content", "text", "rationale", "reason")) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return " ".join(value.split())
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, dict):
        for key in keys:
            if key in value:
                extracted = _text(value.get(key), keys=keys)
                if extracted:
                    return extracted
        pieces = [_text(item, keys=keys) for item in value.values()]
        return "；".join(item for item in pieces if item)
    if isinstance(value, (list, tuple, set)):
        pieces = [_text(item, keys=keys) for item in value]
        return "；".join(item for item in pieces if item)
    return " ".join(str(value).split())


def _obj_value(value: Any, key: str, default: Any = "") -> Any:
    if isinstance(value, dict):
        return value.get(key, default)
    return getattr(value, key, default)


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, (tuple, set)):
        return list(value)
    return [value]


def _dict_items(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        return [value]
    return [item for item in _as_list(value) if isinstance(item, dict)]


def _safe_refs(values: Any, allowed_refs: set[str], limit: int = 6) -> list[str]:
    refs: list[str] = []
    for item in _as_list(values):
        text = str(item).strip()
        if text in allowed_refs and text not in refs:
            refs.append(text)
        if len(refs) >= limit:
            break
    return refs


def _safe_evidence(values: Any, allowed_ids: set[str], limit: int = 8) -> list[str]:
    evidence_ids: list[str] = []
    for item in _as_list(values):
        text = str(item).strip()
        if text in allowed_ids and text not in evidence_ids:
            evidence_ids.append(text)
        if len(evidence_ids) >= limit:
            break
    return evidence_ids


def _format_refs(refs: list[str]) -> str:
    return ", ".join(f"`{item}`" for item in refs) if refs else "证据不足"


def _format_evidence(evidence_ids: list[str]) -> str:
    return ", ".join(f"`{item}`" for item in evidence_ids) if evidence_ids else "证据不足"


def _paper_ref_map(papers: list[PaperRecord]) -> dict[str, str]:
    return {paper.paper_id: f"P{index}" for index, paper in enumerate(papers, start=1)}


def _citation_rate(checks: list[CitationCheck]) -> float:
    if not checks:
        return 0.0
    passed = sum(1 for check in checks if check.status == "passed")
    return round(passed / len(checks), 3)


def _question_list(state: dict[str, Any]) -> list[str]:
    branches = state.get("query_tree", {}).get("branches", [])
    questions = [str(branch.get("question", "")).strip() for branch in branches if branch.get("question")]
    if questions:
        return questions
    topic = str(state.get("effective_topic") or state.get("topic", ""))
    return [
        f"{topic} 的核心问题、主流方法和评测方式是什么？",
        f"{topic} 的代表论文、争议局限和未来研究方向是什么？",
    ]


def _compact_papers(state: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    selected: list[PaperRecord] = list(state.get("selected_papers", []))[:MAX_PUBLISHER_PAPERS]
    refs = _paper_ref_map(selected)
    notes_by_paper = {
        str(_obj_value(note, "paper_id", "")): note
        for note in state.get("reading_notes", [])
    }
    paper_items: list[dict[str, Any]] = []
    for paper in selected:
        note = notes_by_paper.get(paper.paper_id)
        paper_items.append(
            {
                "ref": refs[paper.paper_id],
                "paper_id": paper.paper_id,
                "title": paper.title,
                "year": paper.year,
                "source": paper.source,
                "paper_type": paper.paper_type,
                "authors": paper.authors[:6],
                "url": paper.url,
                "doi": paper.doi,
                "arxiv_id": paper.arxiv_id,
                "citation_count": paper.citation_count,
                "abstract": _clip(paper.abstract, 750),
                "reading_note": {
                    "status": _obj_value(note, "status", ""),
                    "summary": _clip(_obj_value(note, "summary", ""), 520),
                    "methods": [_clip(item, 180) for item in _as_list(_obj_value(note, "methods", []))[:4]],
                    "experiments": [
                        _clip(item, 180) for item in _as_list(_obj_value(note, "experiments", []))[:4]
                    ],
                    "limitations": [
                        _clip(item, 180) for item in _as_list(_obj_value(note, "limitations", []))[:4]
                    ],
                }
                if note
                else {},
            }
        )
    return paper_items, refs


def _compact_evidence(state: dict[str, Any], paper_refs: dict[str, str]) -> list[dict[str, Any]]:
    evidence_items: list[EvidenceItem] = list(state.get("evidence_items", []))[:MAX_PUBLISHER_EVIDENCE]
    evidence: list[dict[str, Any]] = []
    for item in evidence_items:
        evidence.append(
            {
                "evidence_id": item.evidence_id,
                "paper_ref": paper_refs.get(item.paper_id, item.paper_id),
                "paper_id": item.paper_id,
                "category": item.category,
                "claim": _clip(item.claim, 320),
                "support_text": _clip(item.support_text, 420),
                "confidence": item.confidence,
            }
        )
    return evidence


def _compact_lens(state: dict[str, Any], paper_refs: dict[str, str]) -> dict[str, Any]:
    lens = dict(state.get("research_lens", {}) or {})
    representative: dict[str, list[str]] = {}
    raw_dimensions = lens.get("paper_dimensions", {})
    if isinstance(raw_dimensions, dict):
        for paper_id, dimensions in raw_dimensions.items():
            ref = paper_refs.get(str(paper_id))
            if not ref:
                continue
            for dimension in _as_list(dimensions):
                representative.setdefault(str(dimension), []).append(ref)
    return {
        "coverage": lens.get("coverage", 0.0),
        "dimension_counts": lens.get("dimension_counts", {}),
        "missing_dimensions": lens.get("missing_dimensions", []),
        "representative_refs": {key: value[:8] for key, value in representative.items()},
    }


def _publisher_payload(state: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str], set[str]]:
    papers, paper_refs = _compact_papers(state)
    evidence = _compact_evidence(state, paper_refs)
    allowed_evidence = {item["evidence_id"] for item in evidence}
    source_counts = (state.get("source_results", {}) or {}).get("source_counts", {})
    selected_types = Counter(paper["paper_type"] for paper in papers)
    selected_years = Counter(str(paper["year"]) for paper in papers if paper.get("year"))

    payload = {
        "language": "zh-CN",
        "task": "请基于给定证据生成完整、丰富、结构化的中文学术调研报告素材。",
        "topic": state.get("effective_topic") or state.get("topic", ""),
        "original_topic": state.get("topic", ""),
        "actual_source": state.get("actual_source", ""),
        "fallback_reason": state.get("fallback_reason", ""),
        "research_questions": _question_list(state),
        "query_plan": [
            {
                "query_id": _obj_value(query, "query_id", ""),
                "query_text": _obj_value(query, "query_text", ""),
                "source": _obj_value(query, "source", ""),
                "angle": (_obj_value(query, "filters", {}) or {}).get("angle", ""),
            }
            for query in state.get("query_plan", [])[:24]
        ],
        "corpus_profile": {
            "candidate_count": len(state.get("ranked_candidates", [])) or len(state.get("searched_papers", [])),
            "selected_count": len(papers),
            "source_counts": source_counts,
            "selected_paper_type_counts": dict(selected_types),
            "selected_year_counts": dict(selected_years),
            "temporal_profile": (state.get("corpus_profile", {}) or {}).get(
                "temporal_profile", state.get("temporal_profile", {})
            ),
        },
        "research_lens": _compact_lens(state, paper_refs),
        "coverage_gaps": state.get("coverage_gaps", [])[:12],
        "reading_budget": state.get("reading_budget", {}),
        "full_text_chunk_count": len(state.get("full_text_chunks", [])),
        "reading_note_count": len(state.get("reading_notes", [])),
        "snowball": state.get("snowball", "none"),
        "snowball_records": [
            {
                "seed_paper_id": _obj_value(record, "seed_paper_id", ""),
                "direction": _obj_value(record, "direction", ""),
                "added_count": len(_as_list(_obj_value(record, "added_paper_ids", []))),
                "fallback_reason": _obj_value(record, "fallback_reason", ""),
            }
            for record in state.get("snowball_records", [])[:10]
        ],
        "papers": papers,
        "evidence_items": evidence,
        "claim_graph": state.get("claim_graph", [])[:20],
        "question_synthesis": state.get("question_synthesis", [])[:12],
        "global_synthesis": state.get("global_synthesis", {}),
        "allowed_paper_refs": sorted(set(paper_refs.values())),
        "allowed_evidence_ids": sorted(allowed_evidence),
    }
    return payload, paper_refs, allowed_evidence


def _system_prompt() -> str:
    return (
        "You are ResearchFlow's academic publisher agent. Write in Chinese. "
        "Use only the provided papers and evidence. Never invent paper refs, evidence IDs, URLs, "
        "authors, datasets, metrics, or citations. If evidence is weak, explicitly say evidence is insufficient. "
        "Return only one JSON object with keys: title, abstract, scope_and_strategy, field_map, key_findings, "
        "method_comparison, benchmarks_and_metrics, controversies_and_limits, future_directions, reading_roadmap. "
        "field_map/key_findings/method_comparison/benchmarks_and_metrics/controversies_and_limits/"
        "future_directions/reading_roadmap must be arrays. Every analytical item should include paper_refs "
        "and evidence_ids chosen from the provided allowlists when possible. Make the report synthesis-oriented, "
        "not a paper-by-paper list."
    )


def _fallback_refs_for_dimension(
    dimension: str,
    payload: dict[str, Any],
    allowed_refs: set[str],
    limit: int = 5,
) -> list[str]:
    representative = payload.get("research_lens", {}).get("representative_refs", {})
    refs = _safe_refs(representative.get(dimension, []), allowed_refs, limit=limit)
    if refs:
        return refs
    return payload.get("allowed_paper_refs", [])[: min(limit, len(payload.get("allowed_paper_refs", [])))]


def _compose_markdown(
    payload: dict[str, Any],
    response: dict[str, Any],
    paper_refs: dict[str, str],
    allowed_evidence: set[str],
) -> str:
    allowed_refs = set(paper_refs.values())
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    topic = str(payload.get("topic") or payload.get("original_topic") or "Research Topic")
    title = _clip(_text(response.get("title")) or f"{topic}：中文深度文献调研报告", 120)
    abstract = _clip(_text(response.get("abstract")), 1800)
    if not abstract:
        abstract = (
            "本报告基于多源检索、证据抽取、引用校验和分层综合生成。报告只使用候选论文、"
            "Evidence Matrix 与阅读笔记中已经出现的信息，并将关键判断绑定到可追溯证据。"
        )
    lines: list[str] = [
        f"# {title}",
        "",
        f"- 生成时间：{generated_at}",
        f"- 原始主题：`{payload.get('original_topic', '')}`",
        f"- 有效主题：`{topic}`",
        f"- 数据来源：`{payload.get('actual_source', 'unknown')}`",
        f"- 候选文献数：{payload.get('corpus_profile', {}).get('candidate_count', 0)}",
        f"- 核心文献数：{payload.get('corpus_profile', {}).get('selected_count', 0)}",
        f"- 全文 chunk 数：{payload.get('full_text_chunk_count', 0)}",
        f"- 阅读笔记数：{payload.get('reading_note_count', 0)}",
        f"- 引用雪球：`{payload.get('snowball', 'none')}`",
        f"- Citation validity：{payload.get('citation_validity', '见过程记录')}",
        "",
        "## 1. 摘要",
        "",
        abstract,
        "",
        "## 2. 调研问题与检索策略",
        "",
        _clip(_text(response.get("scope_and_strategy")), 1600)
        or "系统先将主题拆分为研究问题和多角度查询，再通过多源检索、覆盖缺口补搜、引用雪球扩展、去重排序和证据抽取形成核心文献集合。",
        "",
        "| 研究问题 | 查询角度示例 |",
        "| --- | --- |",
    ]
    query_by_question = defaultdict(list)
    for query in payload.get("query_plan", []):
        angle = str(query.get("angle") or query.get("source") or "general")
        query_by_question[angle].append(str(query.get("query_text", "")))
    for question in payload.get("research_questions", []):
        lines.append(f"| {_clip(question, 140)} | {_clip('；'.join(list(query_by_question)[:6]), 160)} |")

    corpus = payload.get("corpus_profile", {})
    lines.extend(
        [
            "",
            "## 3. 文献覆盖与时间分布",
            "",
            "本轮调研优先保留综述、方法、系统、评测、数据集和挑战类论文，应用类论文只在能帮助解释场景边界时进入核心集合。",
            "",
            "| 统计项 | 结果 |",
            "| --- | --- |",
            f"| 来源分布 | `{corpus.get('source_counts', {})}` |",
            f"| 核心论文类型 | `{corpus.get('selected_paper_type_counts', {})}` |",
            f"| 核心论文年份 | `{corpus.get('selected_year_counts', {})}` |",
            f"| 时间画像 | `{corpus.get('temporal_profile', {})}` |",
        ]
    )

    lines.extend(["", "## 4. 方法谱系与主题地图", ""])
    field_map = _dict_items(response.get("field_map"))
    if field_map:
        for index, item in enumerate(field_map, start=1):
            refs = _safe_refs(item.get("paper_refs"), allowed_refs)
            evidence_ids = _safe_evidence(item.get("evidence_ids"), allowed_evidence)
            lines.extend(
                [
                    f"### 4.{index} {_clip(_text(item.get('name') or item.get('theme') or item.get('title')), 80) or f'方向 {index}'}",
                    "",
                    _clip(_text(item.get("description") or item.get("analysis") or item), 1200)
                    or "该方向需要结合核心论文进一步确认。",
                    "",
                    f"- 代表论文：{_format_refs(refs)}",
                    f"- 支持证据：{_format_evidence(evidence_ids)}",
                    "",
                ]
            )
    else:
        dimension_counts = payload.get("research_lens", {}).get("dimension_counts", {})
        for index, (dimension, count) in enumerate(dimension_counts.items(), start=1):
            refs = _fallback_refs_for_dimension(str(dimension), payload, allowed_refs)
            lines.extend(
                [
                    f"### 4.{index} {dimension}",
                    "",
                    f"该方向在核心文献中出现 {count} 次，是本领域方法谱系中的一个重要板块。",
                    "",
                    f"- 代表论文：{_format_refs(refs)}",
                    "",
                ]
            )

    lines.extend(["", "## 5. 核心发现与证据链", ""])
    findings = _dict_items(response.get("key_findings"))
    if not findings:
        findings = [
            {
                "finding": "当前证据显示，该领域正在从单点方法比较转向检索、生成、评测和可信性协同优化。",
                "why_it_matters": "这意味着调研报告需要组织方法谱系和证据链，而不是只列出论文摘要。",
                "paper_refs": payload.get("allowed_paper_refs", [])[:5],
                "evidence_ids": payload.get("allowed_evidence_ids", [])[:6],
            }
        ]
    for index, item in enumerate(findings, start=1):
        refs = _safe_refs(item.get("paper_refs"), allowed_refs)
        evidence_ids = _safe_evidence(item.get("evidence_ids"), allowed_evidence)
        lines.extend(
            [
                f"### 5.{index} {_clip(_text(item.get('finding') or item.get('claim') or item.get('title')), 120)}",
                "",
                _clip(_text(item.get("why_it_matters") or item.get("analysis") or item.get("description")), 1400)
                or "该发现的可信度取决于所绑定证据的覆盖范围。",
                "",
                f"- 关联论文：{_format_refs(refs)}",
                f"- 证据链：{_format_evidence(evidence_ids)}",
                "",
            ]
        )

    lines.extend(["", "## 6. 方法对比表", "", "| 方法/路线 | 代表论文 | 优势 | 局限 | 证据 |", "| --- | --- | --- | --- | --- |"])
    method_rows = _dict_items(response.get("method_comparison"))
    for item in method_rows:
        refs = _safe_refs(item.get("paper_refs") or item.get("representative_papers"), allowed_refs)
        evidence_ids = _safe_evidence(item.get("evidence_ids"), allowed_evidence)
        strengths = "；".join(_clip(_text(value), 100) for value in _as_list(item.get("strengths"))[:3])
        limits = "；".join(_clip(_text(value), 100) for value in _as_list(item.get("limitations"))[:3])
        lines.append(
            f"| {_clip(_text(item.get('method') or item.get('name') or item.get('theme')), 80)} | {_format_refs(refs)} | "
            f"{strengths or '需要结合全文验证'} | {limits or '证据不足'} | {_format_evidence(evidence_ids)} |"
        )
    if not method_rows:
        for paper in payload.get("papers", [])[:8]:
            lines.append(
                f"| {_clip(paper.get('paper_type'), 60)} | `{paper.get('ref')}` | "
                f"{_clip(paper.get('reading_note', {}).get('summary') or paper.get('abstract'), 120)} | "
                "需要进一步全文复核 | 证据见对应 Evidence Ledger |"
            )

    lines.extend(["", "## 7. 数据集、评测指标与实验线索", ""])
    benchmark_items = _dict_items(response.get("benchmarks_and_metrics"))
    if benchmark_items:
        for index, item in enumerate(benchmark_items, start=1):
            refs = _safe_refs(item.get("paper_refs"), allowed_refs)
            evidence_ids = _safe_evidence(item.get("evidence_ids"), allowed_evidence)
            lines.extend(
                [
                    f"### 7.{index} {_clip(_text(item.get('theme') or item.get('name') or item.get('title')), 100) or '评测线索'}",
                    "",
                    _clip(_text(item.get("description") or item.get("analysis") or item), 1000)
                    or "当前摘要级证据不足以稳定抽取具体数据集或指标。",
                    "",
                    f"- 相关论文：{_format_refs(refs)}",
                    f"- 支持证据：{_format_evidence(evidence_ids)}",
                    "",
                ]
            )
    else:
        lines.append("当前模型没有从证据白名单中稳定抽取出足够的评测细节，建议下一步优先精读 benchmark/dataset 类论文。")

    lines.extend(["", "## 8. 争议、局限与可信度风险", ""])
    limits = _dict_items(response.get("controversies_and_limits"))
    if not limits:
        limits = [
            {
                "issue": "摘要级证据与全文证据之间可能存在信息损失。",
                "analysis": "标题和摘要适合建立领域地图，但不足以确认实验设置、消融细节和负面结果。系统已通过全文读取状态、Citation Check 和 Evidence Matrix 标记该风险。",
                "paper_refs": payload.get("allowed_paper_refs", [])[:4],
                "evidence_ids": payload.get("allowed_evidence_ids", [])[:4],
            }
        ]
    for index, item in enumerate(limits, start=1):
        refs = _safe_refs(item.get("paper_refs"), allowed_refs)
        evidence_ids = _safe_evidence(item.get("evidence_ids"), allowed_evidence)
        lines.extend(
            [
                f"### 8.{index} {_clip(_text(item.get('issue') or item.get('title') or item.get('name')), 110)}",
                "",
                _clip(_text(item.get("analysis") or item.get("description") or item), 1200)
                or "该问题需要在后续调研中继续补充证据。",
                "",
                f"- 相关论文：{_format_refs(refs)}",
                f"- 支持证据：{_format_evidence(evidence_ids)}",
                "",
            ]
        )

    lines.extend(["", "## 9. 未来方向", ""])
    directions = _dict_items(response.get("future_directions"))
    if not directions:
        directions = [
            {
                "direction": "围绕证据可靠性、评测一致性和真实场景部署继续扩展调研。",
                "rationale": "这些方向直接决定该领域方法能否从原型走向可审计、可复现和可维护的系统。",
                "paper_refs": payload.get("allowed_paper_refs", [])[:5],
                "evidence_ids": payload.get("allowed_evidence_ids", [])[:5],
            }
        ]
    for index, item in enumerate(directions, start=1):
        refs = _safe_refs(item.get("paper_refs"), allowed_refs)
        evidence_ids = _safe_evidence(item.get("evidence_ids"), allowed_evidence)
        lines.extend(
            [
                f"### 9.{index} {_clip(_text(item.get('direction') or item.get('title') or item.get('name')), 120)}",
                "",
                _clip(_text(item.get("rationale") or item.get("reason") or item.get("description") or item), 1200)
                or "该方向来自覆盖缺口与核心证据的综合判断。",
                "",
                f"- 依据论文：{_format_refs(refs)}",
                f"- 依据证据：{_format_evidence(evidence_ids)}",
                "",
            ]
        )

    lines.extend(["", "## 10. 推荐阅读路线", ""])
    roadmap = _dict_items(response.get("reading_roadmap"))
    if roadmap:
        for index, item in enumerate(roadmap, start=1):
            refs = _safe_refs(item.get("paper_refs") or item.get("papers"), allowed_refs)
            lines.append(
                f"{index}. {_clip(_text(item.get('step')) or f'阶段 {index}', 100)}："
                f"{_clip(_text(item.get('reason') or item.get('rationale') or item.get('description')), 420)} 论文：{_format_refs(refs)}"
            )
    else:
        lines.append("1. 先读综述/分类论文建立地图，再读方法和系统论文，最后补 benchmark、可信性和应用边界论文。")

    ref_to_paper = {ref: paper for paper in payload.get("papers", []) for ref in [paper.get("ref")]}
    lines.extend(["", "## 11. 参考文献", ""])
    for ref in sorted(ref_to_paper, key=lambda item: int(str(item).lstrip("P") or "0")):
        paper = ref_to_paper[ref]
        authors = ", ".join(paper.get("authors", [])[:6]) or "Unknown authors"
        lines.append(
            f"[{ref}] {authors}. ({paper.get('year')}). {paper.get('title')}. {paper.get('url')}"
        )

    lines.extend(["", "## 12. 附录：Evidence Matrix 与调研过程", ""])
    lines.append("### 12.1 Evidence Ledger 摘要")
    lines.append("")
    lines.append("| Evidence ID | 论文 | 类别 | 证据内容 |")
    lines.append("| --- | --- | --- | --- |")
    for item in payload.get("evidence_items", [])[:40]:
        lines.append(
            f"| `{item.get('evidence_id')}` | {item.get('paper_ref')} | {item.get('category')} | "
            f"{_clip(item.get('claim'), 180)} |"
        )
    lines.extend(
        [
            "",
            "### 12.2 审计说明",
            "",
            "- 本报告由 LLM publisher 在 Evidence Matrix、PaperReadingNote 和核心论文白名单约束下生成。",
            "- 报告生成器会过滤不在白名单中的 paper ref 与 evidence_id，因此模型不能新增不存在的参考文献。",
            "- 若某一结论缺少可追溯证据，报告会标记为“证据不足”，而不是把模型推断当作论文事实。",
        ]
    )
    fallback_reason = str(payload.get("fallback_reason") or "").strip()
    if fallback_reason:
        lines.extend(["", "### 12.3 数据源降级记录", "", fallback_reason])
    return "\n".join(lines).rstrip() + "\n"


def publish_full_report_with_llm(state: dict[str, Any], provider: str = "deepseek") -> str:
    """Generate a rich full report with an LLM while enforcing citation allowlists."""

    payload, paper_refs, allowed_evidence = _publisher_payload(state)
    payload["citation_validity"] = _citation_rate(state.get("citation_checks", []))
    if not payload["papers"] or not payload["evidence_items"]:
        raise LLMError("LLM publisher requires selected papers and evidence items.")
    client = build_llm_client(provider)
    response = client.generate_json(_system_prompt(), payload)
    return _compose_markdown(payload, response, paper_refs, allowed_evidence)
