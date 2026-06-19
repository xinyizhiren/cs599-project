"""Markdown report generation."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
import re
from typing import Any

from .models import CitationCheck, ClaimRecord, EvidenceItem, PaperRecord


def _clip_table_text(value: str, max_length: int = 160) -> str:
    text = " ".join(_sanitize_secret_text(value).replace("|", "\\|").split())
    if len(text) <= max_length:
        return text
    return text[: max_length - 3].rstrip() + "..."


def _sanitize_secret_text(value: Any) -> str:
    text = str(value)
    text = re.sub(r"sk-[A-Za-z0-9]+", "[REDACTED_API_KEY]", text)
    text = text.replace("DEEPSEEK_API_KEY", "[REDACTED_ENV_VAR]")
    return text


def _category_label(category: str) -> str:
    labels = {
        "contribution": "贡献",
        "method": "方法",
        "experiment": "实验与评测",
        "limitation": "局限",
        "future_work": "未来工作",
    }
    return labels.get(category, category.replace("_", " ").title())


def render_report(
    topic: str,
    selected_papers: list[PaperRecord],
    evidence_items: list[EvidenceItem],
    claims: list[ClaimRecord],
    citation_checks: list[CitationCheck],
    query_plan: list[Any] | None = None,
    actual_source: str = "",
    fallback_reason: str = "",
    llm_provider: str = "off",
    llm_used: bool = False,
    research_lens: dict[str, Any] | None = None,
) -> str:
    evidence_by_paper: dict[str, list[EvidenceItem]] = defaultdict(list)
    for item in evidence_items:
        evidence_by_paper[item.paper_id].append(item)

    check_by_paper = {check.paper_id: check for check in citation_checks}
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    query_plan = query_plan or []
    source_label = actual_source or "unknown"
    top_sources = ", ".join(sorted({paper.source for paper in selected_papers})) or source_label
    total_evidence = len(evidence_items)

    lines: list[str] = [
        f"# 文献调研报告：{topic}",
        "",
        "## 执行摘要",
        "",
        (
            f"ResearchFlow 于 {generated_at} 生成本次文献调研报告。Agent 检索 `{source_label}` "
            f"来源，筛选出 {len(selected_papers)} 篇核心文献，抽取 {total_evidence} 条证据，"
            f"并将 {len(claims)} 条综合结论绑定回可追溯来源。"
        ),
        "",
        (
            f"核心文献来源覆盖：{top_sources}。"
            f"LLM 模式：{llm_provider}；是否实际使用 LLM：{str(llm_used).lower()}。"
        ),
    ]
    if fallback_reason:
        lines.extend(["", f"降级说明：{fallback_reason}"])
    lines.extend(
        [
            "",
            "## 检索方法与范围",
            "",
            (
                "Agent 采用可追踪工作流：查询规划、联网文献检索、排序筛选、证据抽取、"
                "结论综合、引用校验和报告生成。报告中的关键判断尽量绑定到 Evidence ID，"
                "参考文献仅来自检索和筛选后的论文集合。"
            ),
            "",
        ]
    )
    if query_plan:
        lines.append("| Query ID | 检索式 | 来源意图 | 查询角度 | 距离 |")
        lines.append("| --- | --- | --- | --- | --- |")
        for query in query_plan:
            query_id = getattr(query, "query_id", "")
            query_text = getattr(query, "query_text", "")
            source = getattr(query, "source", "")
            filters = getattr(query, "filters", {})
            angle = filters.get("angle", "") if isinstance(filters, dict) else ""
            distance = filters.get("distance", "") if isinstance(filters, dict) else ""
            lines.append(f"| `{query_id}` | {query_text} | {source} | {angle} | {distance} |")
        lines.append("")
    lines.extend(
        [
            "## 1. 研究背景",
            "",
            (
                "这份报告由 ResearchFlow 自动生成，用作某一研究主题的一轮可复核文献调研。"
                "系统不会直接让大模型凭主题自由写作，而是先检索论文、筛选候选池、抽取 Evidence Ledger，"
                "再基于证据生成结论。这样做的重点是降低阅读海量论文的成本，同时保留来源、证据和引用校验入口。"
            ),
            "",
            "## 2. 核心文献",
            "",
        ]
    )

    for index, paper in enumerate(selected_papers, start=1):
        check = check_by_paper.get(paper.paper_id)
        status = check.status if check else "warning"
        lines.extend(
            [
                f"### P{index}. {paper.title}",
                "",
                f"- 作者：{', '.join(paper.authors)}",
                f"- 年份：{paper.year}",
                f"- 来源：{paper.source}",
                f"- URL: {paper.url}",
                f"- 引用数：{paper.citation_count}",
                f"- 引用校验：{status}",
                f"- 摘要：{paper.abstract}",
                "",
            ]
        )

    lines.extend(["## 3. 关键结论与证据", ""])
    if claims:
        lines.append("| Claim ID | 类型 | 结论 | Evidence IDs |")
        lines.append("| --- | --- | --- | --- |")
        for claim in claims:
            evidence_refs = ", ".join(f"`{item}`" for item in claim.evidence_ids) or "None"
            lines.append(
                f"| `{claim.claim_id}` | {claim.claim_type} | {claim.claim_text} | {evidence_refs} |"
            )
        lines.append("")
    else:
        lines.extend(["未生成关键结论。", ""])

    research_lens = research_lens or {}
    if research_lens:
        lines.extend(["## RAG 研究透镜", ""])
        lines.append(research_lens.get("description", "面向领域的研究覆盖度分析。"))
        lines.append("")
        lines.append(f"- 覆盖度：{float(research_lens.get('coverage', 0.0)):.3f}")
        missing_dimensions = research_lens.get("missing_dimensions", [])
        lines.append(
            "- 缺失方向："
            + ("、".join(_dimension_label(item) for item in missing_dimensions) if missing_dimensions else "无")
        )
        lines.append("")
        lines.append("| 方向 | 论文数 |")
        lines.append("| --- | ---: |")
        for dimension, count in sorted(research_lens.get("dimension_counts", {}).items()):
            lines.append(f"| {_dimension_label(dimension)} | {count} |")
        lines.append("")
        lines.append("| Paper ID | 研究方向 |")
        lines.append("| --- | --- |")
        for profile in research_lens.get("paper_profiles", []):
            dimensions = "、".join(_dimension_label(item) for item in profile.get("dimensions", []))
            lines.append(f"| `{profile.get('paper_id', '')}` | {dimensions} |")
        lines.append("")

    lines.extend(["## 4. 方法与主题分类", ""])
    grouped: dict[str, list[EvidenceItem]] = defaultdict(list)
    for item in evidence_items:
        grouped[item.category].append(item)
    for category, items in grouped.items():
        lines.append(f"### {_category_label(category)}")
        lines.append("")
        for item in items[:5]:
            lines.append(f"- {item.claim} (`{item.evidence_id}`)")
        lines.append("")

    lines.extend(["## 证据台账", ""])
    lines.append("| Evidence ID | Paper ID | 类型 | 置信度 | 支撑文本 |")
    lines.append("| --- | --- | --- | ---: | --- |")
    for item in evidence_items:
        support = item.support_text.replace("|", "\\|")
        if len(support) > 280:
            support = support[:277].rstrip() + "..."
        lines.append(
            f"| `{item.evidence_id}` | `{item.paper_id}` | {_category_label(item.category)} | "
            f"{item.confidence:.2f} | {support} |"
        )
    lines.append("")

    lines.extend(["## 5. 对比分析", ""])
    lines.append("| 论文 | 主要证据 | 置信度 |")
    lines.append("| --- | --- | --- |")
    for paper in selected_papers:
        items = evidence_by_paper.get(paper.paper_id, [])
        if not items:
            continue
        evidence = items[0]
        lines.append(f"| {paper.title} | {evidence.claim} | {evidence.confidence:.2f} |")
    lines.append("")

    lines.extend(["## 6. 研究空白", ""])
    gap_claims = [claim for claim in claims if claim.claim_type == "Hypothesis"]
    if gap_claims:
        for claim in gap_claims:
            evidence_refs = ", ".join(f"`{item}`" for item in claim.evidence_ids)
            lines.append(f"- {claim.claim_text} 证据：{evidence_refs}")
    else:
        lines.append("- 目前仍需要更多全文级证据，才能形成更强的研究空白判断。")
    lines.append("")

    lines.extend(["## 7. 自动化调研局限", ""])
    lines.extend(
        [
            "- 当前版本主要依赖论文元数据和摘要，尚未全面解析 PDF 正文。",
            "- 离线 fixture 模式用于稳定演示，不代表真实联网调研覆盖度。",
            "- 引用校验主要验证元数据可追溯性，不等同于同行评审质量判断。",
            "",
        ]
    )

    lines.extend(["## 引用校验", ""])
    lines.append("| Check ID | Paper ID | 状态 | 信息 |")
    lines.append("| --- | --- | --- | --- |")
    for check in citation_checks:
        lines.append(f"| `{check.check_id}` | `{check.paper_id}` | {check.status} | {check.message} |")
    lines.append("")

    lines.extend(["## 参考文献", ""])
    for index, paper in enumerate(selected_papers, start=1):
        authors = ", ".join(paper.authors)
        lines.append(f"[P{index}] {authors}. ({paper.year}). {paper.title}. {paper.url}")

    return "\n".join(lines) + "\n"


def _safe_join(items: list[str], fallback: str = "无") -> str:
    cleaned = [str(item) for item in items if str(item).strip()]
    return "、".join(cleaned) if cleaned else fallback


def _paper_citation(paper: PaperRecord, index: int) -> str:
    authors = ", ".join(paper.authors[:6]) if paper.authors else "Unknown authors"
    suffix = " et al." if len(paper.authors) > 6 else ""
    return f"[P{index}] {authors}{suffix}. ({paper.year}). {paper.title}. {paper.url}"


def render_full_report(state: dict[str, Any]) -> str:
    """Render a complete Chinese literature review organized by questions and evidence."""

    topic = str(state.get("effective_topic") or state.get("topic", ""))
    original_topic = str(state.get("topic", topic))
    selected_papers: list[PaperRecord] = state.get("selected_papers", [])
    ranked_candidates: list[PaperRecord] = state.get("ranked_candidates", [])
    searched_papers: list[PaperRecord] = state.get("searched_papers", [])
    evidence_items: list[EvidenceItem] = state.get("evidence_items", [])
    claims: list[ClaimRecord] = state.get("claims", [])
    citation_checks: list[CitationCheck] = state.get("citation_checks", [])
    query_plan = state.get("query_plan", [])
    query_tree = state.get("query_tree", {})
    evidence_matrix = state.get("evidence_matrix", [])
    claim_graph = state.get("claim_graph", [])
    research_lens = state.get("research_lens", {})
    corpus_profile = state.get("corpus_profile", {})
    source_results = state.get("source_results", {})
    coverage_gaps = state.get("coverage_gaps", [])
    expansion_rounds = state.get("expansion_rounds", [])
    metrics = state.get("metrics", {})
    temporal_profile = corpus_profile.get("temporal_profile") or state.get("temporal_profile", {})
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    evidence_by_paper: dict[str, list[EvidenceItem]] = defaultdict(list)
    for item in evidence_items:
        evidence_by_paper[item.paper_id].append(item)
    check_by_paper = {check.paper_id: check for check in citation_checks}
    refs = {paper.paper_id: f"P{index}" for index, paper in enumerate(selected_papers, start=1)}
    academic_papers = [paper for paper in selected_papers if paper.source != "web"]
    web_sources = [paper for paper in selected_papers if paper.source == "web"]

    source_counts = source_results.get("source_counts", {})
    paper_type_counts = corpus_profile.get("selected_paper_type_counts", {})
    candidate_count = len(ranked_candidates) or len(searched_papers)
    lens_coverage = float(research_lens.get("coverage", 0.0)) if research_lens else 0.0
    citation_rate = float(metrics.get("citation_check_pass_rate", _citation_pass_rate(citation_checks)))
    evidence_coverage = float(metrics.get("claim_evidence_coverage", 0.0))

    questions = [
        str(branch.get("question", ""))
        for branch in query_tree.get("branches", [])
        if branch.get("question")
    ]
    if not questions:
        questions = [
            f"{topic} 的核心问题、主流方法、评测方式和研究空白是什么？",
            f"{topic} 近几年有哪些值得优先阅读的代表性论文？",
        ]

    lines: list[str] = [
        f"# {original_topic}：中文文献调研报告",
        "",
        f"- 生成时间：{generated_at}",
        f"- 有效检索主题：`{topic}`",
        f"- 检索来源：`{state.get('actual_source', 'unknown')}`",
        f"- 候选文献数：{candidate_count}",
        f"- 核心文献数：{len(selected_papers)}",
        f"- Evidence 条目数：{len(evidence_items)}",
        f"- Citation validity：{citation_rate:.3f}",
        f"- Claim-Evidence coverage：{evidence_coverage:.3f}",
        "",
        "## 1. 摘要",
        "",
        (
            f"本报告围绕“{original_topic}”开展自动化学术调研。ResearchFlow 先将模糊主题规范化为可检索的问题树，"
            f"再从 {source_counts or {'source': state.get('actual_source', 'unknown')}} 等来源召回候选材料，经过去重、年份过滤、"
            "覆盖感知排序、论文类型平衡和覆盖缺口补搜后，抽取 Evidence Ledger，并把关键结论绑定到可追溯证据。"
        ),
        "",
        (
            "调研的重点不是把所有论文逐篇堆叠，而是回答三个问题：这个领域正在解决什么问题、已有方法如何形成谱系、"
            "哪些结论有证据支持以及哪些方向仍然存在研究空白。由于当前版本主要读取标题、摘要和开放元数据，报告适合作为"
            "快速建立领域地图和确定精读清单的初稿；涉及实验数值、方法细节和强因果判断时仍需要人工复核全文。"
        ),
        "",
        "## 2. 调研问题与检索策略",
        "",
        "本次调研采用 Deep Research 风格的分层查询：先生成研究问题，再为每个问题展开直接查询和相邻角度查询。相邻角度会覆盖综述、方法、评测、数据集、应用、安全、局限和近期进展，避免只检索与主题字面完全一致的论文。",
        "",
        "| 研究问题 | 子查询数量 | 查询角度 |",
        "| --- | ---: | --- |",
    ]
    for branch in query_tree.get("branches", []):
        subtopics = branch.get("subtopics", [])
        angles = sorted({str(item.get("angle", "")) for item in subtopics if item.get("angle")})
        lines.append(
            f"| {_clip_table_text(str(branch.get('question', '')), 120)} | {len(subtopics)} | {_safe_join(angles)} |"
        )
    if not query_tree.get("branches"):
        angles = sorted(
            {
                str(getattr(query, "filters", {}).get("angle", ""))
                for query in query_plan
                if getattr(query, "filters", {}).get("angle")
            }
        )
        lines.append(f"| {questions[0]} | {len(query_plan)} | {_safe_join(angles)} |")

    lines.extend(
        [
            "",
            "检索过程保留了可审计记录：每条查询包含 query id、查询文本、来源意图、年份过滤和查询角度；若覆盖检测发现缺少综述、方法、评测或安全等方向，会自动追加一次补搜。",
            "",
            "## 3. 文献覆盖与时间分布",
            "",
            f"候选池共包含 {candidate_count} 条去重后记录，核心集合包含 {len(selected_papers)} 篇。年份范围为 {_format_year_range(temporal_profile)}，近三年占比为 {float(temporal_profile.get('last_3_year_ratio', 0.0)):.3f}，近五年占比为 {float(temporal_profile.get('last_5_year_ratio', 0.0)):.3f}。",
            "",
            "| 来源 | 候选数量 |",
            "| --- | ---: |",
        ]
    )
    for source, count in sorted(source_counts.items()):
        lines.append(f"| {source} | {count} |")
    if not source_counts:
        lines.append(f"| {state.get('actual_source', 'unknown')} | {len(searched_papers)} |")

    lines.extend(["", "| 核心论文类型 | 数量 |", "| --- | ---: |"])
    for paper_type, count in sorted(paper_type_counts.items()):
        lines.append(f"| {paper_type} | {count} |")
    if not paper_type_counts:
        lines.append("| unknown | 0 |")

    lines.extend(["", "| 年份 | 候选数量 |", "| ---: | ---: |"])
    for year, count in temporal_profile.get("year_counts", {}).items():
        lines.append(f"| {year} | {count} |")

    lines.extend(
        [
            "",
            "## 4. 研究脉络与方法分类",
            "",
            "本报告用 Research Lens 将核心论文映射到研究方向，而不是按检索结果顺序阅读。这样可以快速判断调研是否覆盖了领域地图中的关键板块。",
            "",
        ]
    )
    if research_lens:
        lines.extend(
            [
                f"- Lens 覆盖度：{lens_coverage:.3f}",
                "- 尚未充分覆盖的方向："
                + (
                    _safe_join([str(item) for item in research_lens.get("missing_dimensions", [])])
                    if research_lens.get("missing_dimensions")
                    else "无明显缺口"
                ),
                "",
                "| 方向 | 覆盖论文数 | 代表论文 |",
                "| --- | ---: | --- |",
            ]
        )
        for dimension, count in sorted(research_lens.get("dimension_counts", {}).items()):
            title = _representative_title(dimension, research_lens)
            lines.append(f"| {_dimension_label(dimension)} | {count} | {_clip_table_text(title, 90)} |")
    else:
        lines.append("当前主题未启用专门领域 Lens，系统主要依据论文类型、年份、来源和关键词相关性组织内容。")

    lines.extend(["", "## 5. 核心论文精读", ""])
    for index, paper in enumerate(selected_papers, start=1):
        paper_evidence = evidence_by_paper.get(paper.paper_id, [])
        check = check_by_paper.get(paper.paper_id)
        lines.extend(
            [
                f"### P{index}. {paper.title}",
                "",
                f"- 年份：{paper.year}",
                f"- 来源：{paper.source}",
                f"- 类型：{paper.paper_type}",
                f"- 作者：{', '.join(paper.authors[:8]) if paper.authors else 'Unknown'}",
                f"- URL：{paper.url}",
                f"- 引用校验：{check.status if check else 'warning'}",
                f"- 摘要压缩：{_first_sentence(paper.abstract, 260)}",
            ]
        )
        if paper_evidence:
            lines.append("- 证据摘要：")
            for item in paper_evidence[:3]:
                lines.append(f"  - `{item.evidence_id}` {item.category}: {_clip_table_text(item.claim, 220)}")
        lines.append("")

    lines.extend(
        [
            "## 6. 方法对比表",
            "",
            "| 论文 | 类型 | 主要贡献/方法 | 局限或需复核点 |",
            "| --- | --- | --- | --- |",
        ]
    )
    for paper in selected_papers:
        items = evidence_by_paper.get(paper.paper_id, [])
        contribution = next((item.claim for item in items if item.category != "limitation"), "")
        limitation = next((item.claim for item in items if item.category == "limitation"), "")
        lines.append(
            "| "
            + " | ".join(
                [
                    f"{refs.get(paper.paper_id, '')}. {_clip_table_text(paper.title, 70)}",
                    paper.paper_type,
                    _clip_table_text(contribution or paper.abstract, 150),
                    _clip_table_text(limitation or "需要进一步阅读全文确认实验设置与适用边界。", 130),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## 7. 数据集与评测指标",
            "",
            "当前版本不会凭空生成论文没有提供的数据集或数值指标，而是从标题、摘要和证据条目中抽取与 benchmark、dataset、evaluation、metric 相关的信息。若核心集合中缺少评测论文，系统会把它标记为覆盖缺口并触发补搜。",
            "",
            "| 证据 | 论文 | 评测相关线索 |",
            "| --- | --- | --- |",
        ]
    )
    benchmark_items = [
        item
        for item in evidence_items
        if item.category == "experiment"
        or any(token in f"{item.claim} {item.support_text}".lower() for token in ["benchmark", "dataset", "evaluation", "metric"])
    ]
    for item in benchmark_items[:10]:
        paper_ref = refs.get(item.paper_id, item.paper_id)
        lines.append(f"| `{item.evidence_id}` | {paper_ref} | {_clip_table_text(item.claim, 180)} |")
    if not benchmark_items:
        lines.append("| - | - | 未从摘要级证据中稳定抽取到评测数据集或指标，需要全文级解析补充。 |")

    lines.extend(
        [
            "",
            "## 8. 主要结论与证据",
            "",
            "| Claim ID | 结论 | 支持证据 | 置信提示 |",
            "| --- | --- | --- | ---: |",
        ]
    )
    if claim_graph:
        for node in claim_graph:
            evidence_ids = [
                item["evidence_id"]
                for item in node.get("supporting_evidence", []) + node.get("limitations", [])
            ]
            lines.append(
                f"| `{node.get('claim_id', '')}` | {_clip_table_text(node.get('claim_text', ''), 220)} | "
                f"{', '.join(f'`{item}`' for item in evidence_ids) or 'None'} | {float(node.get('confidence', 0.0)):.3f} |"
            )
    else:
        for claim in claims:
            evidence_ids = ", ".join(f"`{item}`" for item in claim.evidence_ids) or "None"
            lines.append(f"| `{claim.claim_id}` | {_clip_table_text(claim.claim_text, 220)} | {evidence_ids} | - |")

    lines.extend(
        [
            "",
            "## 9. 争议、局限与研究空白",
            "",
        ]
    )
    if coverage_gaps:
        lines.append("自动覆盖检测发现以下缺口，这些缺口不等同于最终学术结论，而是下一轮调研的优先入口：")
        lines.append("")
        for gap in coverage_gaps:
            lines.append(f"- {gap.get('label', '')}: {gap.get('reason', '')}")
    else:
        lines.append("本轮核心文献在预设 Lens 上没有明显结构性缺口，但这只说明摘要级覆盖较均衡，不代表全文证据已经充分。")
    lines.extend(
        [
            "",
            "此外，当前系统仍受三类限制影响：第一，主要依赖开放元数据和摘要，缺少全文段落级证据；第二，不同数据库的引用数、出版状态和 DOI 完整度并不一致；第三，LLM 只参与主题修正、证据抽取或润色，最终报告仍需要 Citation Check 与人工复核共同约束。",
            "",
            "## 10. 未来方向",
            "",
            "1. 引入 PDF/HTML 全文解析，把 Evidence Ledger 从摘要级升级为段落级，并记录页码、章节和原文定位。",
            "2. 增加学术数据库交叉验证，把 arXiv、OpenAlex、Semantic Scholar、Crossref 与可选网页检索形成互证。",
            "3. 将 Evidence Matrix 扩展为可交互视图，允许用户按研究问题、年份、论文类型和证据类别过滤。",
            "4. 对每个重要 claim 进行反证搜索，区分“已有共识”“存在争议”和“证据不足”。",
            "5. 在对话式 Session 中支持局部重跑：只补搜 benchmark、安全或近三年论文，而不重做整个流程。",
            "",
            "## 11. 参考文献",
            "",
        ]
    )
    for index, paper in enumerate(academic_papers, start=1):
        lines.append(_paper_citation(paper, index))
    if web_sources:
        lines.extend(["", "### 网页背景来源", ""])
        for index, paper in enumerate(web_sources, start=1):
            lines.append(f"[W{index}] {paper.title}. {paper.url}")

    lines.extend(
        [
            "",
            "## 12. 附录：Evidence Matrix 与调研过程",
            "",
            "### Evidence Matrix",
            "",
            "| 研究问题 | 论文 | 类型 | Evidence IDs |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in evidence_matrix[:40]:
        lines.append(
            "| "
            + " | ".join(
                [
                    _clip_table_text(str(row.get("question", "")), 90),
                    _clip_table_text(str(row.get("paper_title", "")), 80),
                    str(row.get("paper_type", "")),
                    ", ".join(f"`{item}`" for item in row.get("evidence_ids", [])) or "None",
                ]
            )
            + " |"
        )
    if not evidence_matrix:
        lines.append("| - | - | - | 未生成 Evidence Matrix。 |")

    lines.extend(["", "### 补搜记录", ""])
    if expansion_rounds:
        for round_info in expansion_rounds:
            lines.append(
                f"- 第 {round_info.get('round', 1)} 轮补搜：新增候选 {round_info.get('added_candidates', 0)} 条；"
                f"来源 `{round_info.get('actual_source', '')}`；原因：覆盖缺口补偿。"
            )
    else:
        lines.append("- 本轮未触发补搜，或请求为离线模式。")

    lines.extend(
        [
            "",
            "### Citation Check",
            "",
            "| Check ID | Paper ID | 状态 | 信息 |",
            "| --- | --- | --- | --- |",
        ]
    )
    for check in citation_checks:
        lines.append(f"| `{check.check_id}` | `{check.paper_id}` | {check.status} | {_clip_table_text(check.message, 160)} |")

    lines.extend(
        [
            "",
            "### 可追溯产物",
            "",
            f"- 完整报告：`{state.get('report_path', '')}`",
            f"- 快速总结：`{state.get('summary_path', '') or '未指定输出路径'}`",
            f"- 调研过程记录：`{state.get('process_path', '') or '未指定输出路径'}`",
            f"- LLM：`{state.get('llm_provider', 'off')}`；实际使用：`{str(state.get('llm_used', False)).lower()}`",
        ]
    )
    fallback_reason = state.get("fallback_reason", "")
    if fallback_reason:
        lines.append(f"- 降级或部分失败说明：{_sanitize_secret_text(fallback_reason)}")
    llm_fallback_reason = state.get("llm_fallback_reason", "")
    if llm_fallback_reason:
        lines.append(f"- LLM fallback：{_sanitize_secret_text(llm_fallback_reason)}")

    return "\n".join(lines) + "\n"


def _citation_pass_rate(citation_checks: list[CitationCheck]) -> float:
    if not citation_checks:
        return 0.0
    return sum(1 for check in citation_checks if check.status == "passed") / len(citation_checks)


def _first_sentence(text: str, max_length: int = 170) -> str:
    sentence = re.split(r"(?<=[.!?])\s+", " ".join(text.split()), maxsplit=1)[0]
    return _clip_table_text(sentence, max_length)


def _dimension_label(dimension: str) -> str:
    labels = {
        "Survey & Taxonomy": "综述与分类",
        "Retrieval & Indexing": "检索与索引",
        "Generation & Grounding": "生成与事实约束",
        "Evaluation & Benchmarks": "评测与基准",
        "Security & Robustness": "安全与鲁棒性",
        "Graph & Structured RAG": "图结构与结构化 RAG",
        "Domain Applications": "领域应用",
        "Unclassified": "未分类",
    }
    return labels.get(dimension, dimension)


def _representative_title(dimension: str, research_lens: dict[str, Any]) -> str:
    for profile in research_lens.get("paper_profiles", []):
        if dimension in profile.get("dimensions", []):
            return _clip_table_text(profile.get("title", ""), 90)
    return "-"


def _dominant_dimensions(research_lens: dict[str, Any]) -> list[tuple[str, int]]:
    counts = research_lens.get("dimension_counts", {})
    if not isinstance(counts, dict):
        return []
    return sorted(
        ((str(dimension), int(count)) for dimension, count in counts.items()),
        key=lambda item: (-item[1], item[0]),
    )


def _format_year_range(temporal_profile: dict[str, Any]) -> str:
    earliest = temporal_profile.get("earliest_year")
    latest = temporal_profile.get("latest_year")
    if earliest is None or latest is None:
        return "unknown"
    return f"{earliest}-{latest}"


def render_summary_report(state: dict[str, Any]) -> str:
    """Render a synthesis-first report that reduces reading cost."""

    topic = str(state.get("topic", ""))
    selected_papers: list[PaperRecord] = state.get("selected_papers", [])
    evidence_items: list[EvidenceItem] = state.get("evidence_items", [])
    claims: list[ClaimRecord] = state.get("claims", [])
    citation_checks: list[CitationCheck] = state.get("citation_checks", [])
    metrics = state.get("metrics", {})
    research_lens = state.get("research_lens", {})
    corpus_profile = state.get("corpus_profile", {})
    topic_refinement = state.get("topic_refinement", {})
    effective_topic = str(state.get("effective_topic", topic))
    query_plan = state.get("query_plan", [])
    research_questions = [str(item) for item in topic_refinement.get("research_questions", [])]
    adjacent_topics = [str(item) for item in topic_refinement.get("adjacent_topics", [])]
    temporal_profile = corpus_profile.get("temporal_profile") or state.get("temporal_profile", {})
    candidate_count = int(corpus_profile.get("candidate_count", len(state.get("searched_papers", []))))
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    dominant_dimensions = _dominant_dimensions(research_lens)
    dimension_names = "、".join(_dimension_label(name) for name, _ in dominant_dimensions[:4])
    missing_dimensions = research_lens.get("missing_dimensions", []) if research_lens else []
    missing_text = "无明显缺口" if not missing_dimensions else "、".join(
        _dimension_label(item) for item in missing_dimensions
    )
    citation_rate = float(metrics.get("citation_check_pass_rate", _citation_pass_rate(citation_checks)))
    evidence_coverage = float(metrics.get("claim_evidence_coverage", 0.0))

    lines: list[str] = [
        f"# 领域调研总结：{topic}",
        "",
        f"- 生成时间：{generated_at}",
        f"- 联网来源：`{state.get('actual_source', 'unknown')}`",
        f"- 候选文献池：{candidate_count}",
        f"- 核心文献数：{len(selected_papers)}",
        f"- 查询计划数：{len(query_plan)}",
        f"- 时间范围：{_format_year_range(temporal_profile)}",
        f"- 引用校验通过率：{citation_rate:.3f}",
        f"- Claim-Evidence 覆盖率：{evidence_coverage:.3f}",
        "",
        "## 调研范围与问题",
        "",
        f"- 原始主题：`{topic}`",
        f"- 有效检索主题：`{effective_topic}`",
        "- 核心研究问题："
        + ("；".join(research_questions) if research_questions else "系统根据主题、论文标题和摘要自动归纳。"),
        "- 相邻扩展方向："
        + ("；".join(adjacent_topics) if adjacent_topics else "暂无显式相邻扩展方向。"),
        "- 本次目标：不是替代完整人工综述，而是快速建立领域地图、识别优先阅读材料、抽取可追溯证据，并给出下一步调研入口。",
        "",
        "## 一句话结论",
        "",
        (
            f"围绕 `{topic}`，当前更值得优先理解的不是单篇论文细节，而是 RAG "
            "从“检索增强生成技巧”演进为一套可评测、可审计、需安全治理的系统工程方法；"
            f"本次样本文献主要覆盖{dimension_names or '若干核心方向'}，"
            f"待补充方向为：{missing_text}。"
        ),
        "",
        "## 关键发现",
        "",
        (
            f"- Agent 从真实开放学术源中检索并筛选了 {len(selected_papers)} 篇核心文献，"
            "最终总结只保留结论、脉络和证据入口，降低逐篇阅读成本。"
        ),
        "- RAG 的主线已经从“把文档塞进上下文”转向检索、重排、生成、事实约束、评测和安全的端到端设计。",
        "- 综述、评测和安全相关论文应优先阅读，因为它们决定领域地图、可靠性边界和落地风险。",
        "- Citation 与 evidence 绑定是本项目的关键约束：总结中的判断不直接脱离检索文献生成。",
        f"- 从时间窗口看，本次候选池覆盖 {_format_year_range(temporal_profile)}，"
        f"近三年论文占比为 {float(temporal_profile.get('last_3_year_ratio', 0.0)):.3f}，"
        "因此总结会优先提醒近期方向是否足够覆盖。",
        "- 仅基于标题和摘要仍不足以做最终学术结论；需要在后续版本接入全文解析和人工复核。",
        "",
        "## 分层结论",
        "",
        "- 技术层：RAG 的核心能力不只是“检索 + 生成”，而是围绕查询改写、召回、重排、上下文组织、生成约束和引用输出形成流水线。",
        "- 评测层：需要同时评估检索相关性、证据覆盖、回答忠实度、引用真实性和任务完成度，单一自然语言打分不够可靠。",
        "- 可信层：报告可信度来自 Evidence Ledger、Citation Check 和来源白名单，而不是来自大模型语言流畅度。",
        "- 工程层：真正可用的调研 Agent 需要会话状态、增量检索、局部重写和过程记录，否则容易退化成一次性自动写作脚本。",
    ]

    if research_lens:
        lines.extend(
            [
                "",
                "## 技术脉络",
                "",
                "| 方向 | 覆盖论文数 | 代表性文献 | 读者应关注的问题 |",
                "| --- | ---: | --- | --- |",
            ]
        )
        focus_questions = {
            "Survey & Taxonomy": "先建立术语、分类和领域边界。",
            "Retrieval & Indexing": "检索器、索引、chunk 与重排如何影响最终答案。",
            "Generation & Grounding": "生成结果如何被上下文证据约束并减少幻觉。",
            "Evaluation & Benchmarks": "如何用可复现基准评估 RAG 的有效性。",
            "Security & Robustness": "如何处理投毒、隐私泄露和对抗样本风险。",
            "Graph & Structured RAG": "何时需要图结构、知识图谱或因果结构增强。",
            "Domain Applications": "哪些场景已经接近工程应用，哪些只是案例验证。",
        }
        for dimension, count in dominant_dimensions:
            lines.append(
                "| "
                + " | ".join(
                    [
                        _dimension_label(dimension),
                        str(count),
                        _representative_title(dimension, research_lens),
                        focus_questions.get(dimension, "结合证据判断其研究价值。"),
                    ]
                )
                + " |"
            )
        lines.extend(
            [
                "",
                f"Lens coverage: {float(research_lens.get('coverage', 0.0)):.3f}；"
                f"缺失方向：{missing_text}。",
            ]
        )

    if selected_papers:
        lines.extend(
            [
                "",
                "## 代表性阅读路线",
                "",
                "建议不要按检索顺序逐篇阅读，而是先建立地图，再看评测，再看方法细节，最后处理应用与风险：",
                "",
            ]
        )
        for index, paper in enumerate(selected_papers[:6], start=1):
            evidence = next(
                (item.claim for item in evidence_items if item.paper_id == paper.paper_id),
                _first_sentence(paper.abstract),
            )
            lines.append(
                f"{index}. {paper.title}（{paper.year}，{paper.source}）："
                f"{_clip_table_text(evidence, 140)}"
            )

    lines.extend(
        [
            "",
            "## 信息规模与时间窗口",
            "",
            (
                f"本次调研先从候选池中收集 {candidate_count} 篇文献，再筛选 "
                f"{len(selected_papers)} 篇进入细读证据层。候选池年份范围为 "
                f"{_format_year_range(temporal_profile)}；近三年占比 "
                f"{float(temporal_profile.get('last_3_year_ratio', 0.0)):.3f}，"
                f"近五年占比 {float(temporal_profile.get('last_5_year_ratio', 0.0)):.3f}。"
            ),
            "",
            "| 年份 | 候选论文数 |",
            "| ---: | ---: |",
        ]
    )
    for year, count in temporal_profile.get("year_counts", {}).items():
        lines.append(f"| {year} | {count} |")

    strategies = corpus_profile.get("compression_strategy", [])
    if strategies:
        lines.extend(["", "## 上下文压缩策略", ""])
        lines.extend(
            [
                "- 先用较大的候选池建立领域覆盖图，而不是直接让模型读取全部论文。",
                "- 用年份分布判断材料是否足够新，避免只总结过时资料或只看最新短期噪声。",
                "- 用 Research Lens 将候选文献映射到综述、检索、生成、评测、安全、结构化和应用等方向。",
                "- 只把筛选后的核心文献送入 Evidence Ledger，LLM 按批次抽取证据，避免上下文窗口溢出。",
                "- 最终总结只引用可追溯 evidence_id 和真实论文 URL，降低幻觉引用风险。",
            ]
        )

    lines.extend(
        [
            "",
            "## 当前共识",
            "",
            "- RAG 的价值在于把外部知识、可追溯证据和生成模型连接起来，从而缓解静态参数知识和上下文窗口限制。",
            "- 检索质量会直接决定生成质量；坏检索会放大幻觉、遗漏和错误归因。",
            "- 评测不能只看最终回答是否流畅，还要看来源是否有效、证据是否覆盖 claim、引用是否真实。",
            "- 安全和隐私不再是附加项，RAG 系统中的检索库、查询日志、上下文注入和文档投毒都可能成为风险入口。",
            "",
            "## 主要难点",
            "",
            "- 相关论文筛选难：RAG 已经成为热门关键词，纯应用案例容易挤占真正的综述、评测和方法论文。",
            "- 证据粒度不足：摘要级证据适合初筛，但不足以支撑细粒度方法比较和实验结论。",
            "- 评价标准分散：faithfulness、context precision、answer relevancy、citation validity 等指标需要组合使用。",
            "- 工程落地复杂：检索、重排、生成、缓存、权限、监控和安全策略需要协同设计。",
            "",
            "## 后续研究机会",
            "",
            "- 全文级 Evidence Ledger：从摘要级证据升级到段落级证据，并保留页码、章节和原文片段位置。",
            "- Claim-Citation 自动审计：把每个关键结论映射到可验证 citation，统计 unsupported claim rate。",
            "- 面向 RAG 的领域覆盖度评价：继续扩展 Research Lens，让系统能指出当前调研还缺哪些方向。",
            "- 多源交叉验证：结合 arXiv、Semantic Scholar、Crossref、OpenAlex 和出版元数据降低单源偏差。",
            "",
            "## 工程落地建议",
            "",
            "1. 先读综述和 taxonomy，建立领域地图；再读 benchmark 和 security，确定评价与风险边界。",
            "2. 对每个候选方案建立 Evidence Ledger，只把有 evidence_id 的结论写入正式报告。",
            "3. 把调研产物分成三层：本总结用于快速决策，完整文献报告用于展开阅读，过程记录用于复核与复现。",
            "4. 对重要结论安排人工复核，尤其是实验指标、对比结论和安全风险判断。",
            "",
            "## 风险与可信度判断",
            "",
            f"- 引用可信度：当前引用校验通过率为 {citation_rate:.3f}，低于阈值时应优先复查参考文献元数据。",
            f"- 证据覆盖度：当前 Claim-Evidence 覆盖率为 {evidence_coverage:.3f}，无证据 claim 不应进入最终强结论。",
            "- 来源偏差：开放学术源覆盖速度快，但可能缺少正式出版版本、系统综述和工业报告，需要后续多源交叉验证。",
            "- 上下文风险：大模型无法一次性可靠阅读海量论文，因此系统采用候选池筛选、Research Lens 分桶、Evidence Ledger 压缩和局部重写。",
            "- 人工复核点：实验指标、对比优劣、安全风险和研究空白判断最需要人工二次检查。",
            "",
            "## 可继续追问的问题",
            "",
            "- “只保留近三年的论文，并重新生成总结。”",
            "- “多补充安全与鲁棒性方向的文献。”",
            "- “去掉纯应用案例，只看方法、评测和综述论文。”",
            "- “把总结改成课程报告里的学术写法。”",
            "- “解释某一篇论文为什么被选入核心文献。”",
            "",
            "## 证据来源",
            "",
            "| 序号 | 论文 | 年份 | 来源 | 关键证据摘要 | URL |",
            "| ---: | --- | ---: | --- | --- | --- |",
        ]
    )
    evidence_by_paper: dict[str, list[EvidenceItem]] = defaultdict(list)
    for item in evidence_items:
        evidence_by_paper[item.paper_id].append(item)
    for index, paper in enumerate(selected_papers, start=1):
        first_evidence = evidence_by_paper.get(paper.paper_id, [])
        evidence_text = (
            first_evidence[0].claim if first_evidence else _first_sentence(paper.abstract)
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    _clip_table_text(paper.title, 90),
                    str(paper.year),
                    paper.source,
                    _clip_table_text(evidence_text, 130),
                    paper.url,
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## 可追溯性",
            "",
            f"- 完整文献调研报告：`{state.get('report_path', '')}`",
            f"- 调研过程记录：`{state.get('process_path', '') or '未生成'}`",
            f"- Trace：`{state.get('trace_path', '') or '见 data/runtime 目录'}`",
            f"- LLM provider：`{state.get('llm_provider', 'off')}`；LLM used：`{str(state.get('llm_used', False)).lower()}`",
        ]
    )
    llm_fallback_reason = state.get("llm_fallback_reason", "")
    if llm_fallback_reason:
        lines.append(f"- LLM fallback：{_sanitize_secret_text(llm_fallback_reason)}")
    if claims:
        lines.extend(["", "## Claim-Evidence 索引", "", "| Claim | Evidence IDs |", "| --- | --- |"])
        for claim in claims:
            evidence_ids = ", ".join(f"`{item}`" for item in claim.evidence_ids) or "None"
            lines.append(f"| {_clip_table_text(claim.claim_text, 150)} | {evidence_ids} |")

    return "\n".join(lines) + "\n"


def render_process_markdown(state: dict[str, Any]) -> str:
    """Render an auditable process log without exposing hidden model reasoning."""

    metrics = state.get("metrics", {})
    query_plan = state.get("query_plan", [])
    query_tree = state.get("query_tree", {})
    searched_papers = state.get("searched_papers", [])
    selected_papers = state.get("selected_papers", [])
    evidence_items = state.get("evidence_items", [])
    evidence_matrix = state.get("evidence_matrix", [])
    claims = state.get("claims", [])
    citation_checks = state.get("citation_checks", [])
    node_trace = state.get("node_trace", [])
    research_lens = state.get("research_lens", {})
    temporal_profile = state.get("temporal_profile", {})
    corpus_profile = state.get("corpus_profile", {})
    source_results = state.get("source_results", {})
    coverage_gaps = state.get("coverage_gaps", [])
    expansion_rounds = state.get("expansion_rounds", [])
    topic_refinement = state.get("topic_refinement", {})
    revision_history = state.get("revision_history", [])

    source_counts: dict[str, int] = defaultdict(int)
    for paper in searched_papers:
        source_counts[getattr(paper, "source", "unknown")] += 1

    lines: list[str] = [
        f"# Research Process: {state.get('topic', '')}",
        "",
        "This file records observable Agent actions and artifacts. It is not a hidden chain-of-thought transcript.",
        "",
        "## Run Summary",
        "",
        f"- Task ID: `{state.get('task_id', '')}`",
        f"- Original topic: `{state.get('topic', '')}`",
        f"- Effective search topic: `{state.get('effective_topic', state.get('topic', ''))}`",
        f"- Topic refinement enabled: `{str(state.get('refine_topic', False)).lower()}`",
        f"- Topic refinement used: `{str(state.get('topic_refinement_used', False)).lower()}`",
        f"- Topic refinement fallback: {_sanitize_secret_text(state.get('topic_refinement_fallback_reason', '') or 'None')}",
        f"- Requested source: `{state.get('requested_source', '')}`",
        f"- Actual source: `{state.get('actual_source', '')}`",
        f"- Candidate limit: `{state.get('candidate_limit', '')}`",
        f"- Candidate multiplier: `{state.get('candidate_multiplier', '')}`",
        f"- From year: `{state.get('from_year', '') or 'None'}`",
        f"- Fallback reason: {_sanitize_secret_text(state.get('fallback_reason', '') or 'None')}",
        f"- Report path: `{state.get('report_path', '')}`",
        f"- Summary path: `{state.get('summary_path', '') or 'None'}`",
        f"- Graph runtime: `{state.get('graph_runtime', '')}`",
        f"- LLM provider: `{state.get('llm_provider', 'off')}`",
        f"- LLM used: `{str(state.get('llm_used', False)).lower()}`",
        f"- LLM chunk count: `{state.get('llm_chunk_count', 0)}`",
        f"- LLM fallback reason: {_sanitize_secret_text(state.get('llm_fallback_reason', '') or 'None')}",
        "",
        "## Topic Understanding",
        "",
        f"- Refined topic: `{topic_refinement.get('refined_topic', '') or state.get('effective_topic', '')}`",
        f"- Scope notes: {_sanitize_secret_text(topic_refinement.get('scope_notes', '') or 'None')}",
        "- Research questions: "
        + (
            "; ".join(_sanitize_secret_text(item) for item in topic_refinement.get("research_questions", []))
            if topic_refinement.get("research_questions")
            else "None"
        ),
        "- Adjacent topics: "
        + (
            "; ".join(_sanitize_secret_text(item) for item in topic_refinement.get("adjacent_topics", []))
            if topic_refinement.get("adjacent_topics")
            else "None"
        ),
        "",
        "## Query Plan",
        "",
        "| Query ID | Search Query | Source Intent | Filters |",
        "| --- | --- | --- | --- |",
    ]
    for query in query_plan:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{getattr(query, 'query_id', '')}`",
                    _clip_table_text(getattr(query, "query_text", "")),
                    getattr(query, "source", ""),
                    f"`{getattr(query, 'filters', {})}`",
                ]
            )
            + " |"
        )

    if query_tree.get("branches"):
        lines.extend(
            [
                "",
                "## Query Tree",
                "",
                "| Research Question | Subquery Count | Angles |",
                "| --- | ---: | --- |",
            ]
        )
        for branch in query_tree.get("branches", []):
            subtopics = branch.get("subtopics", [])
            angles = sorted({str(item.get("angle", "")) for item in subtopics if item.get("angle")})
            lines.append(
                "| "
                + " | ".join(
                    [
                        _clip_table_text(str(branch.get("question", "")), 140),
                        str(len(subtopics)),
                        ", ".join(angles) or "None",
                    ]
                )
                + " |"
            )

    lines.extend(["", "## Search Results", ""])
    lines.append(f"- Retrieved candidates before ranking: {len(searched_papers)}")
    if source_counts:
        lines.append(
            "- Candidate source counts: "
            + ", ".join(f"{source}={count}" for source, count in sorted(source_counts.items()))
        )
    if source_results:
        lines.append(f"- Source results: `{_sanitize_secret_text(json_like(source_results))}`")
    if temporal_profile:
        lines.extend(
            [
                f"- Candidate year range: {_format_year_range(temporal_profile)}",
                f"- Last 3 year ratio: {float(temporal_profile.get('last_3_year_ratio', 0.0)):.3f}",
                f"- Last 5 year ratio: {float(temporal_profile.get('last_5_year_ratio', 0.0)):.3f}",
                "",
                "| Year | Candidate Count |",
                "| ---: | ---: |",
            ]
        )
        for year, count in temporal_profile.get("year_counts", {}).items():
            lines.append(f"| {year} | {count} |")
    if corpus_profile.get("compression_strategy"):
        lines.extend(["", "## Information Compression Strategy", ""])
        for strategy in corpus_profile["compression_strategy"]:
            lines.append(f"- {strategy}")
    lines.extend(
        [
            "",
            "## Top-K Selection",
            "",
            (
                "Ranking uses title-weighted topic matching, RAG phrase/acronym signals, "
                "survey/benchmark/security bonuses, recency, citation count when available, "
                "and duplicate removal."
            ),
            "",
            "| Rank | Paper ID | Title | Year | Source | Score | URL |",
            "| ---: | --- | --- | ---: | --- | ---: | --- |",
        ]
    )
    for index, paper in enumerate(selected_papers, start=1):
        lines.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    f"`{paper.paper_id}`",
                    _clip_table_text(paper.title, 120),
                    str(paper.year),
                    paper.source,
                    f"{paper.score:.3f}",
                    paper.url,
                ]
            )
            + " |"
        )

    if research_lens:
        lines.extend(
            [
                "",
                "## Research Lens",
                "",
                research_lens.get("description", "Domain-aware research lens."),
                "",
                f"- Lens name: {research_lens.get('lens_name', '')}",
                f"- Coverage: {float(research_lens.get('coverage', 0.0)):.3f}",
                "- Missing dimensions: "
                + (
                    ", ".join(research_lens.get("missing_dimensions", []))
                    if research_lens.get("missing_dimensions")
                    else "None"
                ),
                "",
                "| Dimension | Paper Count |",
                "| --- | ---: |",
            ]
        )
        for dimension, count in sorted(research_lens.get("dimension_counts", {}).items()):
            lines.append(f"| {dimension} | {count} |")
        lines.extend(["", "| Paper ID | Lens Dimensions |", "| --- | --- |"])
        for profile in research_lens.get("paper_profiles", []):
            dimensions = ", ".join(profile.get("dimensions", []))
            lines.append(f"| `{profile.get('paper_id', '')}` | {dimensions} |")

    lines.extend(["", "## Coverage Gaps and Expansion", ""])
    if coverage_gaps:
        lines.append("| Gap | Type | Suggested Angle | Reason |")
        lines.append("| --- | --- | --- | --- |")
        for gap in coverage_gaps:
            lines.append(
                "| "
                + " | ".join(
                    [
                        _clip_table_text(str(gap.get("label", "")), 80),
                        str(gap.get("gap_type", "")),
                        str(gap.get("suggested_angle", "")),
                        _clip_table_text(str(gap.get("reason", "")), 160),
                    ]
                )
                + " |"
            )
    else:
        lines.append("- No remaining structural coverage gaps detected.")
    if expansion_rounds:
        lines.extend(["", "| Round | Added Candidates | Source | Query Count |", "| ---: | ---: | --- | ---: |"])
        for round_info in expansion_rounds:
            lines.append(
                f"| {round_info.get('round', 1)} | {round_info.get('added_candidates', 0)} | "
                f"{round_info.get('actual_source', '')} | {len(round_info.get('queries', []))} |"
            )
    else:
        lines.append("- No expansion round was needed or executed.")

    lines.extend(
        [
            "",
            "## Evidence Extraction",
            "",
            "| Evidence ID | Paper ID | Category | Confidence | Claim |",
            "| --- | --- | --- | ---: | --- |",
        ]
    )
    for item in evidence_items:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item.evidence_id}`",
                    f"`{item.paper_id}`",
                    item.category,
                    f"{item.confidence:.2f}",
                    _clip_table_text(item.claim, 180),
                ]
            )
            + " |"
        )

    if evidence_matrix:
        lines.extend(
            [
                "",
                "## Evidence Matrix",
                "",
                "| Research Question | Paper ID | Evidence IDs |",
                "| --- | --- | --- |",
            ]
        )
        for row in evidence_matrix[:40]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        _clip_table_text(str(row.get("question", "")), 130),
                        f"`{row.get('paper_id', '')}`",
                        ", ".join(f"`{item}`" for item in row.get("evidence_ids", [])) or "None",
                    ]
                )
                + " |"
            )

    lines.extend(
        [
            "",
            "## Claim-Evidence Alignment",
            "",
            "| Claim ID | Type | Claim | Evidence IDs |",
            "| --- | --- | --- | --- |",
        ]
    )
    for claim in claims:
        evidence_refs = ", ".join(f"`{item}`" for item in claim.evidence_ids) or "None"
        lines.append(
            f"| `{claim.claim_id}` | {claim.claim_type} | "
            f"{_clip_table_text(claim.claim_text, 180)} | {evidence_refs} |"
        )

    lines.extend(
        [
            "",
            "## Citation Checks",
            "",
            "| Check ID | Paper ID | Status | Message |",
            "| --- | --- | --- | --- |",
        ]
    )
    for check in citation_checks:
        lines.append(
            f"| `{check.check_id}` | `{check.paper_id}` | {check.status} | "
            f"{_clip_table_text(check.message)} |"
        )

    if revision_history:
        lines.extend(
            [
                "",
                "## Conversation Revisions",
                "",
                "| Time | Action | Updated | Message | Output Keys |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for revision in revision_history:
            output_keys = ", ".join(str(item) for item in revision.get("output_keys", []))
            lines.append(
                "| "
                + " | ".join(
                    [
                        _clip_table_text(str(revision.get("timestamp", "")), 48),
                        f"`{_clip_table_text(str(revision.get('action', '')), 48)}`",
                        str(revision.get("updated", False)).lower(),
                        _clip_table_text(str(revision.get("message", "")), 120),
                        f"`{_clip_table_text(output_keys, 120)}`",
                    ]
                )
                + " |"
            )

    lines.extend(["", "## Agent Trace", "", "| Step | Node | Status | Output Keys |", "| ---: | --- | --- | --- |"])
    for index, step in enumerate(node_trace, start=1):
        node = step.get("node", "")
        status = step.get("status", "")
        output_keys = ", ".join(step.get("output_keys", []))
        lines.append(f"| {index} | `{node}` | {status} | `{output_keys}` |")

    lines.extend(["", "## Metrics", "", "| Metric | Value |", "| --- | --- |"])
    for key, value in metrics.items():
        if key == "dimension_scores" and isinstance(value, dict):
            lines.append(f"| `{key}` | `{_sanitize_secret_text(json_like(value))}` |")
        else:
            lines.append(f"| `{key}` | `{_sanitize_secret_text(value)}` |")

    return "\n".join(lines) + "\n"


def json_like(value: dict[str, Any]) -> str:
    return ", ".join(f"{key}: {item}" for key, item in value.items())
