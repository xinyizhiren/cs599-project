# retrieval augmented generation for large language models：中文文献调研报告

- 生成时间：2026-06-19 14:22 UTC
- 有效检索主题：`retrieval augmented generation for large language models`
- 检索来源：`arxiv+crossref+openalex`
- 候选文献数：80
- 核心文献数：8
- Evidence 条目数：16
- Citation validity：1.000
- Claim-Evidence coverage：0.000

## 1. 摘要

本报告围绕“retrieval augmented generation for large language models”开展自动化学术调研。ResearchFlow 先将模糊主题规范化为可检索的问题树，再从 {'arxiv': 27, 'crossref': 27, 'openalex': 26} 等来源召回候选材料，经过去重、年份过滤、覆盖感知排序、论文类型平衡和覆盖缺口补搜后，抽取 Evidence Ledger，并把关键结论绑定到可追溯证据。

调研的重点不是把所有论文逐篇堆叠，而是回答三个问题：这个领域正在解决什么问题、已有方法如何形成谱系、哪些结论有证据支持以及哪些方向仍然存在研究空白。由于当前版本主要读取标题、摘要和开放元数据，报告适合作为快速建立领域地图和确定精读清单的初稿；涉及实验数值、方法细节和强因果判断时仍需要人工复核全文。

## 2. 调研问题与检索策略

本次调研采用 Deep Research 风格的分层查询：先生成研究问题，再为每个问题展开直接查询和相邻角度查询。相邻角度会覆盖综述、方法、评测、数据集、应用、安全、局限和近期进展，避免只检索与主题字面完全一致的论文。

| 研究问题 | 子查询数量 | 查询角度 |
| --- | ---: | --- |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | 4 | application、core、method、survey |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | 4 | application、core、limitation、security |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | 4 | application、benchmark、method、survey |
| retrieval augmented generation for large language models 的主要局限、风险和未来研究方向是什么？ | 4 | application、core、security、survey |

检索过程保留了可审计记录：每条查询包含 query id、查询文本、来源意图、年份过滤和查询角度；若覆盖检测发现缺少综述、方法、评测或安全等方向，会自动追加一次补搜。

## 3. 文献覆盖与时间分布

候选池共包含 80 条去重后记录，核心集合包含 8 篇。年份范围为 2023-2026，近三年占比为 0.925，近五年占比为 1.000。

| 来源 | 候选数量 |
| --- | ---: |
| arxiv | 27 |
| crossref | 27 |
| openalex | 26 |

| 核心论文类型 | 数量 |
| --- | ---: |
| benchmark | 3 |
| method | 1 |
| survey | 4 |

| 年份 | 候选数量 |
| ---: | ---: |
| 2023 | 6 |
| 2024 | 34 |
| 2025 | 30 |
| 2026 | 10 |

## 4. 研究脉络与方法分类

本报告用 Research Lens 将核心论文映射到研究方向，而不是按检索结果顺序阅读。这样可以快速判断调研是否覆盖了领域地图中的关键板块。

- Lens 覆盖度：1.000
- 尚未充分覆盖的方向：无明显缺口

| 方向 | 覆盖论文数 | 代表论文 |
| --- | ---: | --- |
| 领域应用 | 5 | CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of Large... |
| 评测与基准 | 6 | A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large Langu... |
| 生成与事实约束 | 8 | A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large Langu... |
| 图结构与结构化 RAG | 3 | A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large Langu... |
| 检索与索引 | 8 | A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large Langu... |
| 安全与鲁棒性 | 2 | A Multi-Agent Cybersecurity Assessment System Leveraging Large Language Models with Ret... |
| 综述与分类 | 5 | A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large Langu... |

## 5. 核心论文精读

### P1. A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large Language Models

- 年份：2026
- 来源：crossref
- 类型：survey
- 作者：Lihui Liu
- URL：https://doi.org/10.36227/techrxiv.177272838.89432844/v1
- 引用校验：passed
- 摘要压缩：Retrieval-Augmented Generation (RAG) has emerged as a powerful paradigm for combining large language models with external knowledge sources to produce accurate, context-aware, and verifiable outputs.
- 证据摘要：
  - `e1-contribution` contribution: A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large Language Models contributes evidence about retrieval-augmented generation (rag) has emerged as a powerful paradigm for combining large...
  - `e1-limitation` limitation: The current MVP only sees metadata and abstracts, so full-text validation is still needed for A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large Language Models.

### P2. Adaptive Control of Retrieval-Augmented Generation for Large Language Models Through Reflective Tags

- 年份：2024
- 来源：openalex
- 类型：method
- 作者：Chengyuan Yao, Satoshi Fujita
- URL：https://doi.org/10.3390/electronics13234643
- 引用校验：passed
- 摘要压缩：While retrieval-augmented generation (RAG) enhances large language models (LLMs), it also introduces challenges that can impact accuracy and performance.
- 证据摘要：
  - `e2-contribution` contribution: Adaptive Control of Retrieval-Augmented Generation for Large Language Models Through Reflective Tags contributes evidence about while retrieval-augmented generation (rag) enhances large language models (llms), it also...
  - `e2-limitation` limitation: The current MVP only sees metadata and abstracts, so full-text validation is still needed for Adaptive Control of Retrieval-Augmented Generation for Large Language Models Through Reflective Tags.

### P3. CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of Large Language Models

- 年份：2024
- 来源：openalex
- 类型：benchmark
- 作者：Yuanjie Lyu, Zhiyu Li, Simin Niu, Feiyu Xiong, Bo Tang, Wenjin Wang, Hao Wu, Huanyong Liu
- URL：https://doi.org/10.1145/3701228
- 引用校验：passed
- 摘要压缩：Retrieval-augmented generation (RAG) is a technique that enhances the capabilities of large language models (LLMs) by incorporating external knowledge sources.
- 证据摘要：
  - `e3-contribution` contribution: CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of Large Language Models contributes evidence about retrieval-augmented generation (rag) is a technique that enhances the capabilities of...
  - `e3-limitation` limitation: The current MVP only sees metadata and abstracts, so full-text validation is still needed for CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of Large Language Models.

### P4. A Multi-Agent Cybersecurity Assessment System Leveraging Large Language Models with Retrieval-Augmented Generation, IOC Extraction, and SIEM Integration

- 年份：2025
- 来源：crossref
- 类型：benchmark
- 作者：Rasoul Abaryan
- URL：https://doi.org/10.36227/techrxiv.176297583.39945193/v1
- 引用校验：passed
- 摘要压缩：Security teams are increasingly challenged to interpret complex threat data and respond rapidly with accurate, context-aware guidance.
- 证据摘要：
  - `e4-contribution` contribution: A Multi-Agent Cybersecurity Assessment System Leveraging Large Language Models with Retrieval-Augmented Generation, IOC Extraction, and SIEM Integration contributes evidence about security teams are increasingly chall...
  - `e4-limitation` limitation: The current MVP only sees metadata and abstracts, so full-text validation is still needed for A Multi-Agent Cybersecurity Assessment System Leveraging Large Language Models with Retrieval-Augmented Generation, IOC Ext...

### P5. Retrieval augmented generation for large language models in healthcare: A systematic review

- 年份：2025
- 来源：openalex
- 类型：survey
- 作者：Lameck Mbangula Amugongo, Pietro Mascheroni, Steven E. Brooks, Stefan Doering, Jan Seidel
- URL：https://doi.org/10.1371/journal.pdig.0000877
- 引用校验：passed
- 摘要压缩：Large Language Models (LLMs) have demonstrated promising capabilities to solve complex tasks in critical sectors such as healthcare.
- 证据摘要：
  - `e5-contribution` contribution: Retrieval augmented generation for large language models in healthcare: A systematic review contributes evidence about large language models (llms) have demonstrated promising capabilities to solve complex tasks in cr...
  - `e5-limitation` limitation: The current MVP only sees metadata and abstracts, so full-text validation is still needed for Retrieval augmented generation for large language models in healthcare: A systematic review.

### P6. Optimization of hepatological clinical guidelines interpretation by large language models: a retrieval augmented generation-based framework

- 年份：2024
- 来源：openalex
- 类型：survey
- 作者：Simone Kresevic, Mauro Giuffrè, Miloš Ajčević, Agostino Accardo, Lory Saveria Crocè, Dennis Shung
- URL：https://doi.org/10.1038/s41746-024-01091-y
- 引用校验：passed
- 摘要压缩：Large language models (LLMs) can potentially transform healthcare, particularly in providing the right information to the right provider at the right time in the hospital workflow.
- 证据摘要：
  - `e6-contribution` contribution: Optimization of hepatological clinical guidelines interpretation by large language models: a retrieval augmented generation-based framework contributes evidence about large language models (llms) can potentially trans...
  - `e6-limitation` limitation: The current MVP only sees metadata and abstracts, so full-text validation is still needed for Optimization of hepatological clinical guidelines interpretation by large language models: a retrieval augmented generation...

### P7. Retrieval-Augmented Generation for Large Language Models: A Survey

- 年份：2023
- 来源：openalex
- 类型：survey
- 作者：Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai, Jiawei Sun
- URL：http://arxiv.org/abs/2312.10997
- 引用校验：passed
- 摘要压缩：Large Language Models (LLMs) showcase impressive capabilities but encounter challenges like hallucination, outdated knowledge, and non-transparent, untraceable reasoning processes.
- 证据摘要：
  - `e7-contribution` contribution: Retrieval-Augmented Generation for Large Language Models: A Survey contributes evidence about large language models (llms) showcase impressive capabilities but encounter challenges like hallucination, outdated knowled...
  - `e7-limitation` limitation: The current MVP only sees metadata and abstracts, so full-text validation is still needed for Retrieval-Augmented Generation for Large Language Models: A Survey.

### P8. Benchmarking Large Language Models in Retrieval-Augmented Generation

- 年份：2024
- 来源：openalex
- 类型：benchmark
- 作者：Jiawei Chen, Hongyu Lin, Xianpei Han, Le Sun
- URL：https://doi.org/10.1609/aaai.v38i16.29728
- 引用校验：passed
- 摘要压缩：Retrieval-Augmented Generation (RAG) is a promising approach for mitigating the hallucination of large language models (LLMs).
- 证据摘要：
  - `e8-contribution` contribution: Benchmarking Large Language Models in Retrieval-Augmented Generation contributes evidence about retrieval-augmented generation (rag) is a promising approach for mitigating the hallucination of large language models (l...
  - `e8-limitation` limitation: The current MVP only sees metadata and abstracts, so full-text validation is still needed for Benchmarking Large Language Models in Retrieval-Augmented Generation.

## 6. 方法对比表

| 论文 | 类型 | 主要贡献/方法 | 局限或需复核点 |
| --- | --- | --- | --- |
| P1. A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reas... | survey | A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large Language Models contributes evidence about retrieval-augmented ge... | The current MVP only sees metadata and abstracts, so full-text validation is still needed for A Survey of (Deep RAG) Deep Retri... |
| P2. Adaptive Control of Retrieval-Augmented Generation for Large Langua... | method | Adaptive Control of Retrieval-Augmented Generation for Large Language Models Through Reflective Tags contributes evidence about while retrieval-aug... | The current MVP only sees metadata and abstracts, so full-text validation is still needed for Adaptive Control of Retrieval-Aug... |
| P3. CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented... | benchmark | CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of Large Language Models contributes evidence about retrieval-augmen... | The current MVP only sees metadata and abstracts, so full-text validation is still needed for CRUD-RAG: A Comprehensive Chinese... |
| P4. A Multi-Agent Cybersecurity Assessment System Leveraging Large Lang... | benchmark | A Multi-Agent Cybersecurity Assessment System Leveraging Large Language Models with Retrieval-Augmented Generation, IOC Extraction, and SIEM Integr... | The current MVP only sees metadata and abstracts, so full-text validation is still needed for A Multi-Agent Cybersecurity Asses... |
| P5. Retrieval augmented generation for large language models in healthc... | survey | Retrieval augmented generation for large language models in healthcare: A systematic review contributes evidence about large language models (llms)... | The current MVP only sees metadata and abstracts, so full-text validation is still needed for Retrieval augmented generation fo... |
| P6. Optimization of hepatological clinical guidelines interpretation by... | survey | Optimization of hepatological clinical guidelines interpretation by large language models: a retrieval augmented generation-based framework contrib... | The current MVP only sees metadata and abstracts, so full-text validation is still needed for Optimization of hepatological cli... |
| P7. Retrieval-Augmented Generation for Large Language Models: A Survey | survey | Retrieval-Augmented Generation for Large Language Models: A Survey contributes evidence about large language models (llms) showcase impressive capa... | The current MVP only sees metadata and abstracts, so full-text validation is still needed for Retrieval-Augmented Generation fo... |
| P8. Benchmarking Large Language Models in Retrieval-Augmented Generation | benchmark | Benchmarking Large Language Models in Retrieval-Augmented Generation contributes evidence about retrieval-augmented generation (rag) is a promising... | The current MVP only sees metadata and abstracts, so full-text validation is still needed for Benchmarking Large Language Model... |

## 7. 数据集与评测指标

当前版本不会凭空生成论文没有提供的数据集或数值指标，而是从标题、摘要和证据条目中抽取与 benchmark、dataset、evaluation、metric 相关的信息。若核心集合中缺少评测论文，系统会把它标记为覆盖缺口并触发补搜。

| 证据 | 论文 | 评测相关线索 |
| --- | --- | --- |
| `e1-contribution` | P1 | A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large Language Models contributes evidence about retrieval-augmented generation (rag) has emerged as... |
| `e1-limitation` | P1 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large L... |
| `e3-contribution` | P3 | CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of Large Language Models contributes evidence about retrieval-augmented generation (rag) is a tech... |
| `e3-limitation` | P3 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of L... |
| `e4-contribution` | P4 | A Multi-Agent Cybersecurity Assessment System Leveraging Large Language Models with Retrieval-Augmented Generation, IOC Extraction, and SIEM Integration contributes evidence abo... |
| `e4-limitation` | P4 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for A Multi-Agent Cybersecurity Assessment System Leveraging Large Language Models with... |
| `e5-contribution` | P5 | Retrieval augmented generation for large language models in healthcare: A systematic review contributes evidence about large language models (llms) have demonstrated promising c... |
| `e5-limitation` | P5 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for Retrieval augmented generation for large language models in healthcare: A systemati... |
| `e7-contribution` | P7 | Retrieval-Augmented Generation for Large Language Models: A Survey contributes evidence about large language models (llms) showcase impressive capabilities but encounter challen... |
| `e7-limitation` | P7 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for Retrieval-Augmented Generation for Large Language Models: A Survey. |

## 8. 主要结论与证据

| Claim ID | 结论 | 支持证据 | 置信提示 |
| --- | --- | --- | ---: |
| `c1` | Research on retrieval augmented generation for large language models is moving from single-step generation toward tool-using, evidence-grounded workflows. | `e1-contribution`, `e2-contribution`, `e3-contribution`, `e4-contribution` | 0.780 |
| `c2` | A promising research gap is to make the literature review process auditable through claim-evidence alignment and citation checking. | `e1-limitation`, `e2-limitation`, `e3-limitation` | 0.620 |

## 9. 争议、局限与研究空白

本轮核心文献在预设 Lens 上没有明显结构性缺口，但这只说明摘要级覆盖较均衡，不代表全文证据已经充分。

此外，当前系统仍受三类限制影响：第一，主要依赖开放元数据和摘要，缺少全文段落级证据；第二，不同数据库的引用数、出版状态和 DOI 完整度并不一致；第三，LLM 只参与主题修正、证据抽取或润色，最终报告仍需要 Citation Check 与人工复核共同约束。

## 10. 未来方向

1. 引入 PDF/HTML 全文解析，把 Evidence Ledger 从摘要级升级为段落级，并记录页码、章节和原文定位。
2. 增加学术数据库交叉验证，把 arXiv、OpenAlex、Semantic Scholar、Crossref 与可选网页检索形成互证。
3. 将 Evidence Matrix 扩展为可交互视图，允许用户按研究问题、年份、论文类型和证据类别过滤。
4. 对每个重要 claim 进行反证搜索，区分“已有共识”“存在争议”和“证据不足”。
5. 在对话式 Session 中支持局部重跑：只补搜 benchmark、安全或近三年论文，而不重做整个流程。

## 11. 参考文献

[P1] Lihui Liu. (2026). A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large Language Models. https://doi.org/10.36227/techrxiv.177272838.89432844/v1
[P2] Chengyuan Yao, Satoshi Fujita. (2024). Adaptive Control of Retrieval-Augmented Generation for Large Language Models Through Reflective Tags. https://doi.org/10.3390/electronics13234643
[P3] Yuanjie Lyu, Zhiyu Li, Simin Niu, Feiyu Xiong, Bo Tang, Wenjin Wang et al.. (2024). CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of Large Language Models. https://doi.org/10.1145/3701228
[P4] Rasoul Abaryan. (2025). A Multi-Agent Cybersecurity Assessment System Leveraging Large Language Models with Retrieval-Augmented Generation, IOC Extraction, and SIEM Integration. https://doi.org/10.36227/techrxiv.176297583.39945193/v1
[P5] Lameck Mbangula Amugongo, Pietro Mascheroni, Steven E. Brooks, Stefan Doering, Jan Seidel. (2025). Retrieval augmented generation for large language models in healthcare: A systematic review. https://doi.org/10.1371/journal.pdig.0000877
[P6] Simone Kresevic, Mauro Giuffrè, Miloš Ajčević, Agostino Accardo, Lory Saveria Crocè, Dennis Shung. (2024). Optimization of hepatological clinical guidelines interpretation by large language models: a retrieval augmented generation-based framework. https://doi.org/10.1038/s41746-024-01091-y
[P7] Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi et al.. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey. http://arxiv.org/abs/2312.10997
[P8] Jiawei Chen, Hongyu Lin, Xianpei Han, Le Sun. (2024). Benchmarking Large Language Models in Retrieval-Augmented Generation. https://doi.org/10.1609/aaai.v38i16.29728

## 12. 附录：Evidence Matrix 与调研过程

### Evidence Matrix

| 研究问题 | 论文 | 类型 | Evidence IDs |
| --- | --- | --- | --- |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in L... | survey | `e1-contribution`, `e1-limitation` |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | Adaptive Control of Retrieval-Augmented Generation for Large Language Models... | method | `e2-contribution`, `e2-limitation` |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generatio... | benchmark | `e3-contribution`, `e3-limitation` |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | A Multi-Agent Cybersecurity Assessment System Leveraging Large Language Model... | benchmark | `e4-contribution`, `e4-limitation` |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | Retrieval augmented generation for large language models in healthcare: A sys... | survey | `e5-contribution`, `e5-limitation` |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | Optimization of hepatological clinical guidelines interpretation by large lan... | survey | `e6-contribution`, `e6-limitation` |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | Retrieval-Augmented Generation for Large Language Models: A Survey | survey | `e7-contribution`, `e7-limitation` |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | Benchmarking Large Language Models in Retrieval-Augmented Generation | benchmark | `e8-contribution`, `e8-limitation` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in L... | survey | `e1-contribution`, `e1-limitation` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | Adaptive Control of Retrieval-Augmented Generation for Large Language Models... | method | `e2-contribution`, `e2-limitation` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generatio... | benchmark | `e3-contribution`, `e3-limitation` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | A Multi-Agent Cybersecurity Assessment System Leveraging Large Language Model... | benchmark | `e4-contribution`, `e4-limitation` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | Retrieval augmented generation for large language models in healthcare: A sys... | survey | `e5-contribution`, `e5-limitation` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | Optimization of hepatological clinical guidelines interpretation by large lan... | survey | `e6-contribution`, `e6-limitation` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | Retrieval-Augmented Generation for Large Language Models: A Survey | survey | `e7-contribution`, `e7-limitation` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | Benchmarking Large Language Models in Retrieval-Augmented Generation | benchmark | `e8-contribution`, `e8-limitation` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in L... | survey | `e1-contribution`, `e1-limitation` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | Adaptive Control of Retrieval-Augmented Generation for Large Language Models... | method | `e2-contribution`, `e2-limitation` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generatio... | benchmark | `e3-contribution`, `e3-limitation` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | A Multi-Agent Cybersecurity Assessment System Leveraging Large Language Model... | benchmark | `e4-contribution`, `e4-limitation` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | Retrieval augmented generation for large language models in healthcare: A sys... | survey | `e5-contribution`, `e5-limitation` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | Optimization of hepatological clinical guidelines interpretation by large lan... | survey | `e6-contribution`, `e6-limitation` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | Retrieval-Augmented Generation for Large Language Models: A Survey | survey | `e7-contribution`, `e7-limitation` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | Benchmarking Large Language Models in Retrieval-Augmented Generation | benchmark | `e8-contribution`, `e8-limitation` |
| retrieval augmented generation for large language models 的主要局限、风险和未来研究方向是什么？ | A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in L... | survey | `e1-contribution`, `e1-limitation` |
| retrieval augmented generation for large language models 的主要局限、风险和未来研究方向是什么？ | Adaptive Control of Retrieval-Augmented Generation for Large Language Models... | method | `e2-contribution`, `e2-limitation` |
| retrieval augmented generation for large language models 的主要局限、风险和未来研究方向是什么？ | CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generatio... | benchmark | `e3-contribution`, `e3-limitation` |
| retrieval augmented generation for large language models 的主要局限、风险和未来研究方向是什么？ | A Multi-Agent Cybersecurity Assessment System Leveraging Large Language Model... | benchmark | `e4-contribution`, `e4-limitation` |
| retrieval augmented generation for large language models 的主要局限、风险和未来研究方向是什么？ | Retrieval augmented generation for large language models in healthcare: A sys... | survey | `e5-contribution`, `e5-limitation` |
| retrieval augmented generation for large language models 的主要局限、风险和未来研究方向是什么？ | Optimization of hepatological clinical guidelines interpretation by large lan... | survey | `e6-contribution`, `e6-limitation` |
| retrieval augmented generation for large language models 的主要局限、风险和未来研究方向是什么？ | Retrieval-Augmented Generation for Large Language Models: A Survey | survey | `e7-contribution`, `e7-limitation` |
| retrieval augmented generation for large language models 的主要局限、风险和未来研究方向是什么？ | Benchmarking Large Language Models in Retrieval-Augmented Generation | benchmark | `e8-contribution`, `e8-limitation` |

### 补搜记录

- 本轮未触发补搜，或请求为离线模式。

### Citation Check

| Check ID | Paper ID | 状态 | 信息 |
| --- | --- | --- | --- |
| `check-1` | `crossref:10.36227/techrxiv.177272838.89432844/v1` | passed | Citation metadata is available. |
| `check-2` | `openalex:W4404694648` | passed | Citation metadata is available. |
| `check-3` | `openalex:W4403560390` | passed | Citation metadata is available. |
| `check-4` | `crossref:10.36227/techrxiv.176297583.39945193/v1` | passed | Citation metadata is available. |
| `check-5` | `openalex:W4411203672` | passed | Citation metadata is available. |
| `check-6` | `openalex:W4395050972` | passed | Citation metadata is available. |
| `check-7` | `openalex:W4389984066` | passed | Citation metadata is available. |
| `check-8` | `openalex:W4393147129` | passed | Citation metadata is available. |

### 可追溯产物

- 完整报告：``
- 快速总结：`未指定输出路径`
- 调研过程记录：`未指定输出路径`
- LLM：`off`；实际使用：`false`
- 降级或部分失败说明：Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: 
- LLM fallback：LLM provider is disabled.
