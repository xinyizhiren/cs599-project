"""Conversation controller for iterative ResearchFlow sessions."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any

from .evaluation import evaluate_state
from .llm import LLMError, build_llm_client
from .models import QueryItem
from .pipeline import (
    DEFAULT_FROM_YEAR,
    build_corpus_profile,
    build_research_lens,
    check_citations,
    dedupe_papers,
    filter_papers_by_year,
    node_extract_evidence,
    node_write_report,
    rank_all_papers,
    search_selected_sources,
    synthesize_claims,
)
from .planner import normalize_topic, topic_terms
from .report import render_process_markdown, render_summary_report
from .state import ResearchState


VALID_ACTIONS = {
    "answer_question",
    "rewrite_report",
    "adjust_scope",
    "expand_search",
    "filter_papers",
    "regenerate_section",
}
DOMAIN_APPLICATION_TERMS = {
    "application",
    "case stud",
    "education",
    "medical",
    "health",
    "finance",
    "fintech",
    "metaverse",
    "urban",
    "corporate",
    "drug",
    "mission",
    "chatbot",
    "domain",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _state_digest(state: ResearchState) -> dict[str, Any]:
    return {
        "topic": state.get("topic", ""),
        "effective_topic": state.get("effective_topic", state.get("topic", "")),
        "selected_papers": [
            {
                "paper_id": paper.paper_id,
                "title": paper.title,
                "year": paper.year,
                "source": paper.source,
            }
            for paper in state.get("selected_papers", [])[:12]
        ],
        "metrics": state.get("metrics", {}),
        "excluded_paper_ids": state.get("excluded_paper_ids", []),
    }


def classify_conversation_intent(state: ResearchState, user_message: str) -> dict[str, Any]:
    """Classify a follow-up request into an auditable action."""

    provider = state.get("llm_provider", "off")
    if provider == "deepseek":
        try:
            client = build_llm_client(provider)
            payload = client.generate_json(
                (
                    "Classify a follow-up message for a literature review agent. Return only JSON "
                    "with action, parameters, and rationale. action must be one of "
                    "answer_question, rewrite_report, adjust_scope, expand_search, filter_papers, "
                    "or regenerate_section. Keep rationale concise and do not include hidden reasoning."
                ),
                {
                    "message": user_message,
                    "state_digest": _state_digest(state),
                },
            )
            action = str(payload.get("action", "")).strip()
            if action in VALID_ACTIONS:
                parameters = payload.get("parameters", {})
                return {
                    "action": action,
                    "parameters": parameters if isinstance(parameters, dict) else {},
                    "rationale": str(payload.get("rationale", "")).strip(),
                    "classifier": "deepseek",
                }
        except LLMError:
            pass

    return classify_conversation_intent_fallback(user_message)


def classify_conversation_intent_fallback(user_message: str) -> dict[str, Any]:
    text = user_message.lower()
    parameters: dict[str, Any] = {}

    year_match = re.search(r"(20[0-9]{2})", text)
    if year_match:
        parameters["from_year"] = int(year_match.group(1))
    if "近三年" in user_message or "last 3" in text:
        parameters["from_year"] = datetime.now(timezone.utc).year - 2

    if any(keyword in user_message for keyword in ("删掉", "去掉", "排除", "不要")) or "remove" in text:
        if "应用" in user_message or "application" in text or "case" in text:
            parameters["filter"] = "domain_applications"
        paper_ids = re.findall(r"\b(?:P|p)([0-9]+)\b", user_message)
        if paper_ids:
            parameters["paper_indexes"] = [int(item) for item in paper_ids]
        return {
            "action": "filter_papers",
            "parameters": parameters,
            "rationale": "The message asks to remove or exclude papers.",
            "classifier": "rules",
        }

    if parameters.get("from_year") and any(
        keyword in user_message for keyword in ("近", "以后", "之后", "年份", "时间")
    ):
        return {
            "action": "adjust_scope",
            "parameters": parameters,
            "rationale": "The message changes the time scope.",
            "classifier": "rules",
        }

    if any(keyword in user_message for keyword in ("补充", "增加", "多关注", "扩展")) or "expand" in text:
        parameters["angle"] = _infer_angle(user_message)
        return {
            "action": "expand_search",
            "parameters": parameters,
            "rationale": "The message asks to add a research angle.",
            "classifier": "rules",
        }

    if any(keyword in user_message for keyword in ("重写", "改写", "更短", "更学术", "摘要", "总结")):
        parameters["style"] = "concise" if "短" in user_message else "academic"
        return {
            "action": "rewrite_report",
            "parameters": parameters,
            "rationale": "The message asks to rewrite or adjust report wording.",
            "classifier": "rules",
        }

    if any(keyword in user_message for keyword in ("解释", "为什么", "如何", "是什么", "?", "？")):
        return {
            "action": "answer_question",
            "parameters": parameters,
            "rationale": "The message asks a question about the current review.",
            "classifier": "rules",
        }

    return {
        "action": "answer_question",
        "parameters": parameters,
        "rationale": "Default to answering from current evidence.",
        "classifier": "rules",
    }


def _infer_angle(message: str) -> str:
    text = message.lower()
    if "安全" in message or "security" in text or "robust" in text:
        return "security_robustness"
    if "评测" in message or "评价" in message or "benchmark" in text or "eval" in text:
        return "evaluation_benchmark"
    if "综述" in message or "survey" in text or "taxonomy" in text:
        return "survey_taxonomy"
    if "方法" in message or "架构" in message or "method" in text or "architecture" in text:
        return "methods_systems"
    if "应用" in message or "application" in text:
        return "applications_domains"
    return "adjacent_topic"


def _angle_query(topic: str, angle: str, message: str) -> str:
    core = " ".join(topic_terms(topic)[:6]) or topic
    suffixes = {
        "security_robustness": "security robustness hallucination privacy attack defense",
        "evaluation_benchmark": "evaluation benchmark dataset metrics",
        "survey_taxonomy": "survey taxonomy review",
        "methods_systems": "methods systems architecture retriever reranking",
        "applications_domains": "applications case studies deployment",
        "adjacent_topic": normalize_topic(message),
    }
    return normalize_topic(f"{core} {suffixes.get(angle, message)}")


def _paper_matches_domain_application(title: str, abstract: str) -> bool:
    text = f"{title} {abstract}".lower()
    has_method_signal = any(
        signal in text
        for signal in ("survey", "benchmark", "evaluation", "taxonomy", "framework", "architecture")
    )
    return any(term in text for term in DOMAIN_APPLICATION_TERMS) and not has_method_signal


def _excluded_from_parameters(state: ResearchState, parameters: dict[str, Any]) -> list[str]:
    selected = state.get("selected_papers", [])
    excluded: list[str] = []
    for index in parameters.get("paper_indexes", []):
        if 1 <= int(index) <= len(selected):
            excluded.append(selected[int(index) - 1].paper_id)
    if parameters.get("filter") == "domain_applications":
        excluded.extend(
            paper.paper_id
            for paper in selected
            if _paper_matches_domain_application(paper.title, paper.abstract)
        )
    return list(dict.fromkeys(excluded))


def _write_text(path_value: str | None, content: str) -> None:
    if not path_value:
        return
    path = Path(path_value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _append_trace(state: ResearchState, action: str, output_keys: list[str], elapsed_ms: float) -> None:
    trace = list(state.get("node_trace", []))
    trace.append(
        {
            "node": f"conversation:{action}",
            "status": "success",
            "elapsed_ms": round(elapsed_ms, 3),
            "output_keys": output_keys,
        }
    )
    state["node_trace"] = trace


def _rebuild_after_selection_change(state: ResearchState, action: str) -> None:
    effective_topic = state.get("effective_topic", state.get("topic", ""))
    excluded = set(state.get("excluded_paper_ids", []))
    searched = [
        paper
        for paper in filter_papers_by_year(state.get("searched_papers", []), state.get("from_year"))
        if paper.paper_id not in excluded
    ]
    ranked = rank_all_papers(searched, effective_topic)
    selected = ranked[: int(state.get("top_k", 5))]
    state["searched_papers"] = searched
    state["ranked_candidates"] = ranked
    state["selected_papers"] = selected
    state["research_lens"] = build_research_lens(effective_topic, selected)
    state["corpus_profile"] = build_corpus_profile(
        effective_topic,
        ranked,
        selected,
        state.get("from_year"),
    )
    state.update(node_extract_evidence(state))
    state["claims"] = synthesize_claims(effective_topic, state["evidence_items"])
    state["citation_checks"] = check_citations(selected, state["claims"])
    state.update(node_write_report(state))
    state["metrics"] = evaluate_state(state)
    summary_markdown = render_summary_report(state)
    state["summary_markdown"] = summary_markdown
    _write_text(state.get("summary_output_path"), summary_markdown)
    process_markdown = render_process_markdown(state)
    state["process_markdown"] = process_markdown
    _write_text(state.get("process_output_path"), process_markdown)
    state["last_conversation_action"] = action


def _render_concise_summary(state: ResearchState, user_message: str) -> str:
    selected = state.get("selected_papers", [])
    metrics = state.get("metrics", {})
    lines = [
        f"# 对话调整后总结：{state.get('topic', '')}",
        "",
        f"- 用户调整：{user_message}",
        f"- 有效主题：{state.get('effective_topic', state.get('topic', ''))}",
        f"- 核心文献数：{len(selected)}",
        f"- 候选文献数：{metrics.get('searched_paper_count', len(state.get('searched_papers', [])))}",
        f"- 引用校验通过率：{metrics.get('citation_check_pass_rate', 0)}",
        "",
        "## 极简结论",
        "",
        (
            "当前调研结论仍以已检索论文和 Evidence Ledger 为边界；"
            "建议优先阅读综述、评测和安全/鲁棒性相关论文，再展开到具体应用。"
        ),
        "",
        "## 优先阅读",
        "",
    ]
    for index, paper in enumerate(selected[:5], start=1):
        lines.append(f"{index}. {paper.title} ({paper.year}) - {paper.url}")
    lines.extend(["", "## 证据约束", "", "本摘要未新增任何未检索引用；详细证据仍以完整报告和过程记录为准。"])
    return "\n".join(lines) + "\n"


def _answer_from_state(state: ResearchState, user_message: str) -> str:
    selected = state.get("selected_papers", [])
    evidence = state.get("evidence_items", [])
    lens = state.get("research_lens", {})
    top_titles = "；".join(paper.title for paper in selected[:3]) or "暂无核心论文"
    evidence_count = len(evidence)
    missing = lens.get("missing_dimensions", []) if isinstance(lens, dict) else []
    missing_text = "无明显缺口" if not missing else "、".join(missing)
    return (
        f"基于当前会话的 {len(selected)} 篇核心论文和 {evidence_count} 条证据，"
        f"可以先看这几篇：{top_titles}。"
        f"当前领域覆盖缺口：{missing_text}。"
        "如果你要继续收窄范围，可以要求我补充某个方向、排除某类论文或重写报告摘要。"
    )


def apply_conversation_action(
    state: ResearchState,
    action_payload: dict[str, Any],
    user_message: str,
) -> dict[str, Any]:
    action = str(action_payload.get("action", "answer_question"))
    parameters = action_payload.get("parameters", {})
    if not isinstance(parameters, dict):
        parameters = {}
    start = perf_counter()
    updated = False

    if action in {"rewrite_report", "regenerate_section"}:
        summary_markdown = _render_concise_summary(state, user_message)
        state["summary_markdown"] = summary_markdown
        _write_text(state.get("summary_output_path"), summary_markdown)
        if state.get("report_markdown"):
            state["report_markdown"] = (
                state["report_markdown"].rstrip()
                + "\n\n## Conversation Revision\n\n"
                + f"- Request: {user_message}\n"
                + "- The concise summary artifact was regenerated without adding new references.\n"
            )
            _write_text(state.get("report_path"), state["report_markdown"])
        updated = True
        reply = "已基于当前证据重写总结，并保留原始引用和 Evidence Ledger 约束。"
        output_keys = ["summary_markdown", "report_markdown"]

    elif action == "filter_papers":
        excluded = _excluded_from_parameters(state, parameters)
        existing = list(state.get("excluded_paper_ids", []))
        state["excluded_paper_ids"] = list(dict.fromkeys(existing + excluded))
        constraints = dict(state.get("user_constraints", {}))
        constraints["last_filter"] = parameters.get("filter", "paper_ids")
        state["user_constraints"] = constraints
        _rebuild_after_selection_change(state, action)
        updated = True
        reply = f"已排除 {len(excluded)} 篇论文并重新生成核心文献、证据、报告和评估。"
        output_keys = ["excluded_paper_ids", "selected_papers", "report_markdown"]

    elif action == "expand_search":
        angle = str(parameters.get("angle") or "adjacent_topic")
        effective_topic = state.get("effective_topic", state.get("topic", ""))
        query_plan = list(state.get("query_plan", []))
        query = QueryItem(
            query_id=f"q{len(query_plan) + 1}",
            query_text=_angle_query(effective_topic, angle, user_message),
            source=state.get("requested_source", "offline"),
            filters={
                "from_year": state.get("from_year", DEFAULT_FROM_YEAR),
                "angle": angle,
                "distance": "adjacent",
                "conversation": True,
            },
        )
        query_plan.append(query)
        state["query_plan"] = query_plan
        raw_papers, actual_source, fallback_reason = search_selected_sources(
            topic=effective_topic,
            query_plan=[query],
            sources=state.get("selected_sources", [state.get("requested_source", "offline")]),
            limit=int(state.get("candidate_limit", 40)),
        )
        merged = dedupe_papers(list(state.get("searched_papers", [])) + raw_papers)
        state["searched_papers"] = merged
        if actual_source:
            state["actual_source"] = actual_source
        if fallback_reason:
            state["fallback_reason"] = fallback_reason
        included = list(state.get("included_query_angles", []))
        state["included_query_angles"] = list(dict.fromkeys(included + [angle]))
        _rebuild_after_selection_change(state, action)
        updated = True
        reply = f"已追加 `{angle}` 方向检索并刷新候选池、核心论文和报告。"
        output_keys = ["query_plan", "searched_papers", "selected_papers", "report_markdown"]

    elif action == "adjust_scope":
        if parameters.get("from_year"):
            state["from_year"] = int(parameters["from_year"])
        _rebuild_after_selection_change(state, action)
        updated = True
        reply = f"已按新的时间范围 from_year={state.get('from_year')} 重新筛选和生成报告。"
        output_keys = ["from_year", "selected_papers", "report_markdown"]

    else:
        reply = _answer_from_state(state, user_message)
        output_keys = ["reply"]

    revision = {
        "timestamp": _now_iso(),
        "action": action,
        "message": user_message,
        "updated": updated,
        "rationale": action_payload.get("rationale", ""),
        "output_keys": output_keys,
    }
    history = list(state.get("revision_history", []))
    history.append(revision)
    state["revision_history"] = history
    state["last_conversation_action"] = action
    _append_trace(state, action, output_keys, (perf_counter() - start) * 1000)

    if updated:
        process_markdown = render_process_markdown(state)
        state["process_markdown"] = process_markdown
        _write_text(state.get("process_output_path"), process_markdown)

    return {
        "reply": reply,
        "action": action,
        "updated": updated,
        "revision": revision,
    }


def handle_conversation_turn(state: ResearchState, user_message: str) -> dict[str, Any]:
    message = normalize_topic(user_message)
    if not message:
        raise ValueError("Conversation message cannot be empty.")

    messages = list(state.get("conversation_messages", []))
    messages.append({"role": "user", "content": message, "timestamp": _now_iso()})
    action_payload = classify_conversation_intent(state, message)
    result = apply_conversation_action(state, action_payload, message)
    messages.append(
        {
            "role": "assistant",
            "content": result["reply"],
            "timestamp": _now_iso(),
            "action": result["action"],
        }
    )
    state["conversation_messages"] = messages
    state["updated_at"] = _now_iso()
    return {
        **result,
        "state": state,
        "messages": messages,
        "artifacts": {
            "report.md": str(state.get("report_markdown", "")),
            "summary.md": str(state.get("summary_markdown", "")),
            "process.md": str(state.get("process_markdown", "")),
        },
    }
