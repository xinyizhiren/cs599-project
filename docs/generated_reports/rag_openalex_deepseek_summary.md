# 领域调研总结：retrieval augmented generation for large language models

- 生成时间：2026-06-19 16:57 UTC
- 联网来源：`openalex`
- 候选文献池：32
- 核心文献数：3
- 查询计划数：9
- 时间范围：2023-2026
- 引用校验通过率：1.000
- Claim-Evidence 覆盖率：1.000

## 调研范围与问题

- 原始主题：`retrieval augmented generation for large language models`
- 有效检索主题：`retrieval augmented generation for large language models`
- 核心研究问题：系统根据主题、论文标题和摘要自动归纳。
- 相邻扩展方向：暂无显式相邻扩展方向。
- 本次目标：不是替代完整人工综述，而是快速建立领域地图、识别优先阅读材料、抽取可追溯证据，并给出下一步调研入口。

## 一句话结论

围绕 `retrieval augmented generation for large language models`，当前更值得优先理解的不是单篇论文细节，而是 RAG 从“检索增强生成技巧”演进为一套可评测、可审计、需安全治理的系统工程方法；本次样本文献主要覆盖领域应用、生成与事实约束、检索与索引、评测与基准，待补充方向为：安全与鲁棒性、图结构与结构化 RAG。

## 关键发现

- Agent 从真实开放学术源中检索并筛选了 3 篇核心文献，最终总结只保留结论、脉络和证据入口，降低逐篇阅读成本。
- RAG 的主线已经从“把文档塞进上下文”转向检索、重排、生成、事实约束、评测和安全的端到端设计。
- 综述、评测和安全相关论文应优先阅读，因为它们决定领域地图、可靠性边界和落地风险。
- Citation 与 evidence 绑定是本项目的关键约束：总结中的判断不直接脱离检索文献生成。
- 从时间窗口看，本次候选池覆盖 2023-2026，近三年论文占比为 0.688，因此总结会优先提醒近期方向是否足够覆盖。
- 仅基于标题和摘要仍不足以做最终学术结论；需要在后续版本接入全文解析和人工复核。

## 分层结论

- 技术层：RAG 的核心能力不只是“检索 + 生成”，而是围绕查询改写、召回、重排、上下文组织、生成约束和引用输出形成流水线。
- 评测层：需要同时评估检索相关性、证据覆盖、回答忠实度、引用真实性和任务完成度，单一自然语言打分不够可靠。
- 可信层：报告可信度来自 Evidence Ledger、Citation Check 和来源白名单，而不是来自大模型语言流畅度。
- 工程层：真正可用的调研 Agent 需要会话状态、增量检索、局部重写和过程记录，否则容易退化成一次性自动写作脚本。

## 技术脉络

| 方向 | 覆盖论文数 | 代表性文献 | 读者应关注的问题 |
| --- | ---: | --- | --- |
| 领域应用 | 3 | Retrieval augmented generation for large language models in healthcare: A systematic re... | 哪些场景已经接近工程应用，哪些只是案例验证。 |
| 生成与事实约束 | 3 | Retrieval augmented generation for large language models in healthcare: A systematic re... | 生成结果如何被上下文证据约束并减少幻觉。 |
| 检索与索引 | 3 | Retrieval augmented generation for large language models in healthcare: A systematic re... | 检索器、索引、chunk 与重排如何影响最终答案。 |
| 评测与基准 | 2 | Retrieval augmented generation for large language models in healthcare: A systematic re... | 如何用可复现基准评估 RAG 的有效性。 |
| 综述与分类 | 1 | Retrieval augmented generation for large language models in healthcare: A systematic re... | 先建立术语、分类和领域边界。 |

Lens coverage: 0.714；缺失方向：安全与鲁棒性、图结构与结构化 RAG。

## 代表性阅读路线

建议不要按检索顺序逐篇阅读，而是先建立地图，再看评测，再看方法细节，最后处理应用与风险：

1. Retrieval augmented generation for large language models in healthcare: A systematic review（2025，openalex）：78.9% of studies used English datasets and 21.1% are in Chinese
2. Integrating Retrieval-Augmented Generation with Large Language Models in Nephrology: Advancing Practical Applications（2024，openalex）：RAG strategy helps address hallucinations by integrating external data, enhancing output accuracy and relevance
3. CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of Large Language Models（2024，openalex）：Develops a comprehensive benchmark evaluating all components of RAG systems across four CRUD application scenarios

## 信息规模与时间窗口

本次调研先从候选池中收集 32 篇文献，再筛选 3 篇进入细读证据层。候选池年份范围为 2023-2026；近三年占比 0.688，近五年占比 1.000。

| 年份 | 候选论文数 |
| ---: | ---: |
| 2023 | 10 |
| 2024 | 16 |
| 2025 | 5 |
| 2026 | 1 |

## 上下文压缩策略

- 先用较大的候选池建立领域覆盖图，而不是直接让模型读取全部论文。
- 用年份分布判断材料是否足够新，避免只总结过时资料或只看最新短期噪声。
- 用 Research Lens 将候选文献映射到综述、检索、生成、评测、安全、结构化和应用等方向。
- 只把筛选后的核心文献送入 Evidence Ledger，LLM 按批次抽取证据，避免上下文窗口溢出。
- 最终总结只引用可追溯 evidence_id 和真实论文 URL，降低幻觉引用风险。

## 当前共识

- RAG 的价值在于把外部知识、可追溯证据和生成模型连接起来，从而缓解静态参数知识和上下文窗口限制。
- 检索质量会直接决定生成质量；坏检索会放大幻觉、遗漏和错误归因。
- 评测不能只看最终回答是否流畅，还要看来源是否有效、证据是否覆盖 claim、引用是否真实。
- 安全和隐私不再是附加项，RAG 系统中的检索库、查询日志、上下文注入和文档投毒都可能成为风险入口。

## 主要难点

- 相关论文筛选难：RAG 已经成为热门关键词，纯应用案例容易挤占真正的综述、评测和方法论文。
- 证据粒度不足：摘要级证据适合初筛，但不足以支撑细粒度方法比较和实验结论。
- 评价标准分散：faithfulness、context precision、answer relevancy、citation validity 等指标需要组合使用。
- 工程落地复杂：检索、重排、生成、缓存、权限、监控和安全策略需要协同设计。

## 后续研究机会

- 全文级 Evidence Ledger：从摘要级证据升级到段落级证据，并保留页码、章节和原文片段位置。
- Claim-Citation 自动审计：把每个关键结论映射到可验证 citation，统计 unsupported claim rate。
- 面向 RAG 的领域覆盖度评价：继续扩展 Research Lens，让系统能指出当前调研还缺哪些方向。
- 多源交叉验证：结合 arXiv、Semantic Scholar、Crossref、OpenAlex 和出版元数据降低单源偏差。

## 工程落地建议

1. 先读综述和 taxonomy，建立领域地图；再读 benchmark 和 security，确定评价与风险边界。
2. 对每个候选方案建立 Evidence Ledger，只把有 evidence_id 的结论写入正式报告。
3. 把调研产物分成三层：本总结用于快速决策，完整文献报告用于展开阅读，过程记录用于复核与复现。
4. 对重要结论安排人工复核，尤其是实验指标、对比结论和安全风险判断。

## 风险与可信度判断

- 引用可信度：当前引用校验通过率为 1.000，低于阈值时应优先复查参考文献元数据。
- 证据覆盖度：当前 Claim-Evidence 覆盖率为 1.000，无证据 claim 不应进入最终强结论。
- 来源偏差：开放学术源覆盖速度快，但可能缺少正式出版版本、系统综述和工业报告，需要后续多源交叉验证。
- 上下文风险：大模型无法一次性可靠阅读海量论文，因此系统采用候选池筛选、Research Lens 分桶、Evidence Ledger 压缩和局部重写。
- 人工复核点：实验指标、对比优劣、安全风险和研究空白判断最需要人工二次检查。

## 可继续追问的问题

- “只保留近三年的论文，并重新生成总结。”
- “多补充安全与鲁棒性方向的文献。”
- “去掉纯应用案例，只看方法、评测和综述论文。”
- “把总结改成课程报告里的学术写法。”
- “解释某一篇论文为什么被选入核心文献。”

## 证据来源

| 序号 | 论文 | 年份 | 来源 | 关键证据摘要 | URL |
| ---: | --- | ---: | --- | --- | --- |
| 1 | Retrieval augmented generation for large language models in healthcare: A systematic re... | 2025 | openalex | 78.9% of studies used English datasets and 21.1% are in Chinese | https://doi.org/10.1371/journal.pdig.0000877 |
| 2 | Integrating Retrieval-Augmented Generation with Large Language Models in Nephrology: Ad... | 2024 | openalex | RAG strategy helps address hallucinations by integrating external data, enhancing output accuracy and relevance | https://doi.org/10.3390/medicina60030445 |
| 3 | CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of Large... | 2024 | openalex | Develops a comprehensive benchmark evaluating all components of RAG systems across four CRUD application scenarios | https://doi.org/10.1145/3701228 |

## 可追溯性

- 完整文献调研报告：`docs\generated_reports\rag_openalex_deepseek_smoke.md`
- 调研过程记录：`docs\generated_reports\rag_openalex_deepseek_process.md`
- Trace：`见 data/runtime 目录`
- LLM provider：`deepseek`；LLM used：`true`

## Claim-Evidence 索引

| Claim | Evidence IDs |
| --- | --- |
| Research on retrieval augmented generation for large language models is moving from single-step generation toward tool-using, evidence-grounded wor... | `llm-openalex-w44112036-1`, `llm-openalex-w43925973-1`, `llm-openalex-w43925973-2`, `llm-openalex-w44035603-1` |
| A promising research gap is to make the literature review process auditable through claim-evidence alignment and citation checking. | `llm-openalex-w44112036-2`, `llm-openalex-w44112036-3` |
