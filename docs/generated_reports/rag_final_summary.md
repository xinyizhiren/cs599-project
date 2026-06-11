# 领域调研总结：retrieval augmented generation for large language models

- 生成时间：2026-06-11 06:22 UTC
- 联网来源：`arxiv`
- 候选文献池：50
- 核心文献数：15
- 时间范围：2022-2026
- 引用校验通过率：1.000
- Claim-Evidence 覆盖率：1.000

## 一句话结论

围绕 `retrieval augmented generation for large language models`，当前更值得优先理解的不是单篇论文细节，而是 RAG 从“检索增强生成技巧”演进为一套可评测、可审计、需安全治理的系统工程方法；本次样本文献主要覆盖评测与基准、生成与事实约束、检索与索引、图结构与结构化 RAG，待补充方向为：无明显缺口。

## 关键发现

- Agent 从真实开放学术源中检索并筛选了 15 篇核心文献，最终总结只保留结论、脉络和证据入口，降低逐篇阅读成本。
- RAG 的主线已经从“把文档塞进上下文”转向检索、重排、生成、事实约束、评测和安全的端到端设计。
- 综述、评测和安全相关论文应优先阅读，因为它们决定领域地图、可靠性边界和落地风险。
- Citation 与 evidence 绑定是本项目的关键约束：总结中的判断不直接脱离检索文献生成。
- 仅基于标题和摘要仍不足以做最终学术结论；需要在后续版本接入全文解析和人工复核。

## 技术脉络

| 方向 | 覆盖论文数 | 代表性文献 | 读者应关注的问题 |
| --- | ---: | --- | --- |
| 评测与基准 | 15 | Auto-RAG: Autonomous Retrieval-Augmented Generation for Large Language Models | 如何用可复现基准评估 RAG 的有效性。 |
| 生成与事实约束 | 15 | Auto-RAG: Autonomous Retrieval-Augmented Generation for Large Language Models | 生成结果如何被上下文证据约束并减少幻觉。 |
| 检索与索引 | 15 | Auto-RAG: Autonomous Retrieval-Augmented Generation for Large Language Models | 检索器、索引、chunk 与重排如何影响最终答案。 |
| 图结构与结构化 RAG | 8 | DA-RAG: Dynamic Attributed Community Search for Retrieval-Augmented Generation | 何时需要图结构、知识图谱或因果结构增强。 |
| 领域应用 | 5 | Investigating Retrieval-Augmented Generation in Quranic Studies: A Study of 13 Open-Sou... | 哪些场景已经接近工程应用，哪些只是案例验证。 |
| 综述与分类 | 4 | Auto-RAG: Autonomous Retrieval-Augmented Generation for Large Language Models | 先建立术语、分类和领域边界。 |
| 安全与鲁棒性 | 2 | Bridge-RAG: An Abstract Bridge Tree Based Retrieval Augmented Generation Algorithm | 如何处理投毒、隐私泄露和对抗样本风险。 |

Lens coverage: 1.000；缺失方向：无明显缺口。

## 信息规模与时间窗口

本次调研先从候选池中收集 50 篇文献，再筛选 15 篇进入细读证据层。候选池年份范围为 2022-2026；近三年占比 0.960，近五年占比 1.000。

| 年份 | 候选论文数 |
| ---: | ---: |
| 2022 | 1 |
| 2023 | 1 |
| 2024 | 15 |
| 2025 | 22 |
| 2026 | 11 |

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

## 证据来源

| 序号 | 论文 | 年份 | 来源 | 关键证据摘要 | URL |
| ---: | --- | ---: | --- | --- | --- |
| 1 | Auto-RAG: Autonomous Retrieval-Augmented Generation for Large Language Models | 2024 | arxiv | Auto-RAG is an autonomous iterative retrieval model that leverages LLM's decision-making to iteratively interact with the retri... | http://arxiv.org/abs/2411.19443v1 |
| 2 | Investigating Retrieval-Augmented Generation in Quranic Studies: A Study of 13 Open-Sou... | 2025 | arxiv | Investigates 13 open-source LLMs with RAG for Quranic studies. | http://arxiv.org/abs/2503.16581v1 |
| 3 | MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries | 2024 | arxiv | Develops MultiHop-RAG, a benchmark dataset for multi-hop queries in RAG. | http://arxiv.org/abs/2401.15391v1 |
| 4 | Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG | 2025 | arxiv | Provides a comprehensive survey and taxonomy of Agentic RAG systems. | http://arxiv.org/abs/2501.09136v4 |
| 5 | DA-RAG: Dynamic Attributed Community Search for Retrieval-Augmented Generation | 2026 | arxiv | DA-RAG uses attributed community search to dynamically extract relevant subgraphs based on the query. | http://arxiv.org/abs/2602.08545v1 |
| 6 | Bridge-RAG: An Abstract Bridge Tree Based Retrieval Augmented Generation Algorithm | 2026 | arxiv | Bridge-RAG introduces abstract to bridge query entities and document chunks. | http://arxiv.org/abs/2603.26668v2 |
| 7 | FAIR-RAG: Faithful Adaptive Iterative Refinement for Retrieval-Augmented Generation | 2025 | arxiv | FAIR-RAG transforms the standard RAG pipeline into a dynamic, evidence-driven reasoning process. | http://arxiv.org/abs/2510.22344v1 |
| 8 | RAG-Check: Evaluating Multimodal Retrieval Augmented Generation Performance | 2025 | arxiv | RAG-Check is a framework to evaluate the reliability of multi-modal RAG using relevancy and correctness scores. | http://arxiv.org/abs/2501.03995v1 |
| 9 | MASS-RAG: Multi-Agent Synthesis Retrieval-Augmented Generation | 2026 | arxiv | MASS-RAG is a multi-agent synthesis approach that structures evidence processing into specialized agents. | http://arxiv.org/abs/2604.18509v2 |
| 10 | Structure-Aware RAG: Structured Retrieval Augmented Generation from Noisy Data for Conv... | 2026 | arxiv | SA-RAG uses tables as an intermediate structured representation to reduce noise while preserving essential information. | http://arxiv.org/abs/2605.24366v1 |
| 11 | FD-RAG: Federated Dual-System Retrieval-Augmented Generation | 2026 | arxiv | FD-RAG is a federated dual-system RAG framework that decouples memory access from LLM reasoning. | http://arxiv.org/abs/2605.27432v1 |
| 12 | SPD-RAG: Sub-Agent Per Document Retrieval-Augmented Generation | 2026 | arxiv | SPD-RAG is a hierarchical multi-agent framework for exhaustive cross-document QA. | http://arxiv.org/abs/2603.08329v1 |
| 13 | GFM-RAG: Graph Foundation Model for Retrieval Augmented Generation | 2025 | arxiv | GFM-RAG is the first graph foundation model for RAG applicable to unseen datasets without fine-tuning. | http://arxiv.org/abs/2502.01113v3 |
| 14 | DyG-RAG: Dynamic Graph Retrieval-Augmented Generation with Event-Centric Reasoning | 2025 | arxiv | DyG-RAG is an event-centric dynamic graph RAG framework for temporal reasoning. | http://arxiv.org/abs/2507.13396v1 |
| 15 | OmniBench-RAG: A Multi-Domain Evaluation Platform for Retrieval-Augmented Generation Tools | 2025 | arxiv | The platform quantifies performance gains across accuracy and efficiency dimensions, spanning nine knowledge fields including c... | http://arxiv.org/abs/2508.05650v1 |

## 可追溯性

- 完整文献调研报告：`docs\generated_reports\rag_live_literature_review.md`
- 调研过程记录：`docs\generated_reports\rag_live_research_process.md`
- Trace：`见 data/runtime 目录`
- LLM provider：`deepseek`；LLM used：`true`

## Claim-Evidence 索引

| Claim | Evidence IDs |
| --- | --- |
| Research on retrieval augmented generation for large language models is moving from single-step generation toward tool-using, evidence-grounded wor... | `llm-arxiv-2411-19443v1-1`, `llm-arxiv-2411-19443v1-2`, `llm-arxiv-2503-16581v1-1`, `llm-arxiv-2503-16581v1-2` |
| A promising research gap is to make the literature review process auditable through claim-evidence alignment and citation checking. | `llm-arxiv-2503-16581v1-3`, `llm-arxiv-2401-15391v1-3`, `llm-arxiv-2501-09136v4-2` |
