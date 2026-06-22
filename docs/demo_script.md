# ResearchFlow 现场演示脚本

适用场景：CS599 Final Demo，5 分钟演示 + 3 分钟答辩。

## 1. 开场，约 30 秒

大家好，我的项目是 ResearchFlow，一个面向学术文献调研的多智能体 Research Agent。

它解决的问题是：当我们调研一个新领域时，通常要反复设计关键词、搜索论文、筛选核心文献、阅读摘要或全文、组织方法脉络、检查引用，成本很高，而且普通大模型容易生成没有证据支撑的综述。

ResearchFlow 的目标不是只生成一段总结，而是生成三类可复查成果：

- 中文综合总结。
- 中文完整文献调研报告。
- 可审计调研过程记录。

## 2. 架构说明，约 60 秒

系统采用 Agentic workflow，把调研拆成多个节点：

```text
topic refinement
-> query tree planning
-> multi-source search
-> coverage-aware ranking
-> gap recovery
-> OpenAlex snowball search
-> full-text reading
-> evidence extraction
-> claim synthesis
-> citation checking
-> report writing
-> evaluation
```

核心创新有四点：

- 多源检索：arXiv、Semantic Scholar、Crossref、OpenAlex、可选 Tavily Web。
- 引用雪球：从核心论文沿参考文献和被引论文继续扩展。
- 分层压缩：`paper -> chunks -> PaperReadingNote -> question synthesis -> global synthesis`，缓解大模型上下文有限的问题。
- 证据约束：通过 Evidence Matrix、Claim Graph 和 Citation Checker 约束报告结论。

## 3. CLI 演示，约 90 秒

优先演示离线稳定闭环，保证现场不受网络影响：

```powershell
$env:PYTHONPATH="src"
python -m researchflow run "retrieval augmented generation for large language models" --source offline --top-k 5 --report-style full --summary-style comprehensive --output tmp/demo_report.md --summary-output tmp/demo_summary.md --process-output tmp/demo_process.md
```

展示三个输出：

- `tmp/demo_summary.md`：一页综合总结。
- `tmp/demo_report.md`：完整中文调研报告。
- `tmp/demo_process.md`：调研过程记录，包括 query plan、Top-K、Evidence Ledger、Citation Check 和 metrics。

如果网络稳定，可以展示真实联网命令：

```powershell
$env:PYTHONPATH="src"
python -m researchflow run "retrieval augmented generation for large language models" --source openalex --require-live --llm deepseek --top-k 3 --max-candidates 12 --from-year 2023 --depth 2 --breadth 3 --report-style full --output docs/generated_reports/rag_openalex_deepseek_smoke.md --summary-output docs/generated_reports/rag_openalex_deepseek_summary.md --process-output docs/generated_reports/rag_openalex_deepseek_process.md
```

说明：DeepSeek Key 只从本地 `.env` 或环境变量读取，不写入仓库。

## 4. Web 演示，约 90 秒

启动 Web 控制台：

```powershell
$env:PYTHONPATH="src"
python -m researchflow.web --host 127.0.0.1 --port 7860
```

演示路径：

1. 输入主题，例如 `RAG 怎么样` 或 `retrieval augmented generation for large language models`。
2. 选择数据源和 top-k。
3. 展示节点执行过程和报告区域。
4. 在对话框输入：
   - `多补充 benchmark 方向`
   - `精读第 1 篇`
   - `把方法对比写得更详细`
5. 说明系统不是一次性 skill，而是可恢复 session agent。

## 5. 评估与交付，约 50 秒

测试命令：

```powershell
$env:PYTHONPATH="src"
python -m pytest tests
```

当前结果：`40 passed`。

评估命令：

```powershell
$env:PYTHONPATH="src"
python -m researchflow evaluate --benchmark examples/benchmarks/basic.jsonl --output examples/evaluation/results.json
```

评估维度包括：

- 任务完成。
- 检索质量。
- 证据可信度。
- 报告质量。
- Agent 行为 trace。

最终交付物：

- `README.md`
- `src/`
- `docs/product_spec.md`
- `docs/architecture_spec.md`
- `docs/api_spec.md`
- `docs/CS599_大作业报告.pdf`
- tag：`v0.1`

## 6. 答辩可用回答

Q：为什么不用普通大模型直接写综述？

A：普通大模型的问题是过程不可复现、引用容易幻觉、结论缺少证据绑定。ResearchFlow 先检索、再抽证据、再写报告，并保留 Citation Check 和 Evidence Matrix。

Q：分层压缩会不会失真？

A：会有信息损失，所以系统不把压缩结果当作无损事实，而是保留 evidence_id、PaperReadingNote、chunk、citation check 和 process 记录，让每个结论可以追溯。后续还可以加入 claim-level faithfulness 检查和冲突证据检测。

Q：相比 Deep Research / GPT Researcher 的优势是什么？

A：ResearchFlow 更聚焦学术调研和课程交付，支持学术 API、引用校验、Evidence Matrix、Claim Graph、中文报告和本地可复现评估。不足是通用网页浏览、多模态理解和大规模商业级检索覆盖不如成熟系统。

Q：如果现场 API 失败怎么办？

A：系统有离线 fixture 和 fallback 机制。联网失败时不会伪装成真实调研，会在 process 和 metrics 中记录 fallback reason。现场可以先演示离线闭环，再展示仓库中已有真实联网样例。
