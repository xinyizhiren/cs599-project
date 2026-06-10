# ResearchFlow 评估方案

日期：2026-06-10

## 1. 评估原则

ResearchFlow 是文献调研 Agent，不适合只用“回答是否好看”来评价。系统评估采用分层方法：

```text
功能正确性 + 检索质量 + 证据可信度 + 报告质量 + Agent 行为
```

评估参考 RAGAS、DeepEval、LangSmith Evaluation 和 OpenAI Evals 的思路，但 MVP 阶段不强依赖外部商业平台，而是在本地实现轻量 evaluator。

## 2. 100 分制评分

| 维度 | 权重 | 指标 |
| --- | ---: | --- |
| 任务完成 | 20 | run success rate、report generated、node failure recovery |
| 检索质量 | 20 | Top-K relevance、duplicate rate、source success rate |
| 证据可信 | 25 | citation validity、claim evidence coverage、unsupported claim rate、hallucinated reference count |
| 报告质量 | 20 | section completeness、method taxonomy quality、research gap usefulness、readability |
| Agent 行为 | 15 | tool call correctness、plan adherence、step efficiency、trace completeness |

## 3. Final 阈值

| 指标 | 目标 |
| --- | ---: |
| Benchmark 任务数 | >= 5 |
| 离线 benchmark 成功率 | 100% |
| arXiv 模式成功率 | >= 80% |
| Citation validity | >= 90% |
| Claim evidence coverage | >= 85% |
| Hallucinated reference count | 0 |
| Report section completeness | 100% |

## 4. 当前实现

当前 `researchflow evaluate` 会读取 JSONL benchmark，运行每个调研任务，并输出：

- `results.json`：机器可读的逐任务指标和总体得分。
- `results.md`：适合放入报告或截图的评估表。
- LLM 相关字段：`llm_provider`、`llm_used`、`llm_fallback_reason`。

示例：

```powershell
python -m researchflow evaluate --benchmark examples/benchmarks/basic.jsonl --output examples/evaluation/results.json
```

## 5. 指标解释

| 指标 | 含义 |
| --- | --- |
| `overall_score` | 100 分制综合分 |
| `citation_check_pass_rate` | 引用校验通过率 |
| `claim_evidence_coverage` | 有证据支持的 claim 比例 |
| `unsupported_claim_rate` | 无证据 claim 比例 |
| `hallucinated_reference_count` | 不来自候选论文的引用数量 |
| `report_section_completeness` | 报告章节完整率 |
| `node_trace_count` | Agent 节点 trace 数量 |
| `graph_runtime` | `langgraph`、`sequential` 或 `sequential_fallback` |
| `llm_provider` | `off` 或 `deepseek` |
| `llm_used` | 是否实际采用 LLM 输出 |
| `llm_fallback_reason` | LLM 未使用或降级的原因 |

## 6. 参考依据

- RAGAS metrics: <https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/>
- DeepEval metrics: <https://deepeval.com/docs/metrics-introduction>
- LangSmith Evaluation: <https://docs.langchain.com/langsmith/evaluation>
- OpenAI Evals: <https://developers.openai.com/api/docs/guides/evals>
- LangGraph Persistence: <https://docs.langchain.com/oss/python/langgraph/persistence>
