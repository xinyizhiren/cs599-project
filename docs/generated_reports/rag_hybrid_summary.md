# 领域调研总结：retrieval augmented generation for large language models

- 生成时间：2026-06-11 09:14 UTC
- 联网来源：`hybrid`
- 候选文献池：24
- 核心文献数：8
- 时间范围：2023-2026
- 引用校验通过率：1.000
- Claim-Evidence 覆盖率：1.000

## 一句话结论

围绕 `retrieval augmented generation for large language models`，当前更值得优先理解的不是单篇论文细节，而是 RAG 从“检索增强生成技巧”演进为一套可评测、可审计、需安全治理的系统工程方法；本次样本文献主要覆盖生成与事实约束、检索与索引、领域应用、评测与基准，待补充方向为：无明显缺口。

## 关键发现

- Agent 从真实开放学术源中检索并筛选了 8 篇核心文献，最终总结只保留结论、脉络和证据入口，降低逐篇阅读成本。
- RAG 的主线已经从“把文档塞进上下文”转向检索、重排、生成、事实约束、评测和安全的端到端设计。
- 综述、评测和安全相关论文应优先阅读，因为它们决定领域地图、可靠性边界和落地风险。
- Citation 与 evidence 绑定是本项目的关键约束：总结中的判断不直接脱离检索文献生成。
- 仅基于标题和摘要仍不足以做最终学术结论；需要在后续版本接入全文解析和人工复核。

## 技术脉络

| 方向 | 覆盖论文数 | 代表性文献 | 读者应关注的问题 |
| --- | ---: | --- | --- |
| 生成与事实约束 | 8 | Can Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) Generate New... | 生成结果如何被上下文证据约束并减少幻觉。 |
| 检索与索引 | 8 | Can Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) Generate New... | 检索器、索引、chunk 与重排如何影响最终答案。 |
| 领域应用 | 7 | Can Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) Generate New... | 哪些场景已经接近工程应用，哪些只是案例验证。 |
| 评测与基准 | 7 | Can Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) Generate New... | 如何用可复现基准评估 RAG 的有效性。 |
| 安全与鲁棒性 | 4 | Retrieval Augmented Generation via Context Compression Techniques for Large Language Mo... | 如何处理投毒、隐私泄露和对抗样本风险。 |
| 综述与分类 | 2 | Can Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) Generate New... | 先建立术语、分类和领域边界。 |
| 图结构与结构化 RAG | 1 | Large Language Models in Clinical Advice: Direct Generation and Retrieval Augmented Gen... | 何时需要图结构、知识图谱或因果结构增强。 |

Lens coverage: 1.000；缺失方向：无明显缺口。

## 信息规模与时间窗口

本次调研先从候选池中收集 24 篇文献，再筛选 8 篇进入细读证据层。候选池年份范围为 2023-2026；近三年占比 0.958，近五年占比 1.000。

| 年份 | 候选论文数 |
| ---: | ---: |
| 2023 | 1 |
| 2024 | 9 |
| 2025 | 11 |
| 2026 | 3 |

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
| 1 | Can Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) Generate New... | 2025 | crossref | Can Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) Generate New Knowledge for Urban Studies? contributes... | https://doi.org/10.21203/rs.3.rs-6551928/v1 |
| 2 | AI-Powered Smart Advisory System for Precision Agriculture Using Large Language Models... | 2026 | crossref | AI-Powered Smart Advisory System for Precision Agriculture Using Large Language Models and Retrieval-Augmented Generation contr... | https://doi.org/10.2139/ssrn.6761739 |
| 3 | Investigating Retrieval-Augmented Generation in Quranic Studies: A Study of 13 Open-Sou... | 2025 | arxiv | Investigating Retrieval-Augmented Generation in Quranic Studies: A Study of 13 Open-Source Large Language Models contributes ev... | http://arxiv.org/abs/2503.16581v1 |
| 4 | Retrieval Augmented Generation via Context Compression Techniques for Large Language Mo... | 2024 | crossref | Retrieval Augmented Generation via Context Compression Techniques for Large Language Models contributes evidence about natural... | https://doi.org/10.31219/osf.io/ua6j5 |
| 5 | Large Language Models in Clinical Advice: Direct Generation and Retrieval Augmented Gen... | 2025 | crossref | Large Language Models in Clinical Advice: Direct Generation and Retrieval Augmented Generation vs Expert Advice contributes evi... | https://doi.org/10.5121/csit.2025.150904 |
| 6 | Hallucination Reduction in Large Language Models with Retrieval-Augmented Generation Us... | 2024 | crossref | Hallucination Reduction in Large Language Models with Retrieval-Augmented Generation Using Wikipedia Knowledge contributes evid... | https://doi.org/10.31219/osf.io/pv7r5 |
| 7 | A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large Langu... | 2026 | crossref | A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large Language Models contributes evidence about cr... | https://doi.org/10.36227/techrxiv.177272838.89432844/v1 |
| 8 | Retrieval-Augmented Generation in Large Language Models through Selective Augmentation | 2024 | crossref | Retrieval-Augmented Generation in Large Language Models through Selective Augmentation contributes evidence about abstract the... | https://doi.org/10.21203/rs.3.rs-4652959/v1 |

## 可追溯性

- 完整文献调研报告：`docs\generated_reports\rag_hybrid_literature_review.md`
- 调研过程记录：`docs\generated_reports\rag_hybrid_research_process.md`
- Trace：`见 data/runtime 目录`
- LLM provider：`off`；LLM used：`false`
- LLM fallback：LLM provider is disabled.

## Claim-Evidence 索引

| Claim | Evidence IDs |
| --- | --- |
| Research on retrieval augmented generation for large language models is moving from single-step generation toward tool-using, evidence-grounded wor... | `e1-contribution`, `e2-contribution`, `e3-contribution`, `e4-contribution` |
| A promising research gap is to make the literature review process auditable through claim-evidence alignment and citation checking. | `e1-limitation`, `e2-limitation`, `e3-limitation` |
