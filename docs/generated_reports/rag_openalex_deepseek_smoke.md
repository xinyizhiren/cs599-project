# retrieval augmented generation for large language models：中文文献调研报告

- 生成时间：2026-06-19 16:57 UTC
- 有效检索主题：`retrieval augmented generation for large language models`
- 检索来源：`openalex`
- 候选文献数：32
- 核心文献数：3
- Evidence 条目数：7
- Citation validity：1.000
- Claim-Evidence coverage：0.000

## 1. 摘要

本报告围绕“retrieval augmented generation for large language models”开展自动化学术调研。ResearchFlow 先将模糊主题规范化为可检索的问题树，再从 {'openalex': 32} 等来源召回候选材料，经过去重、年份过滤、覆盖感知排序、论文类型平衡和覆盖缺口补搜后，抽取 Evidence Ledger，并把关键结论绑定到可追溯证据。

调研的重点不是把所有论文逐篇堆叠，而是回答三个问题：这个领域正在解决什么问题、已有方法如何形成谱系、哪些结论有证据支持以及哪些方向仍然存在研究空白。由于当前版本主要读取标题、摘要和开放元数据，报告适合作为快速建立领域地图和确定精读清单的初稿；涉及实验数值、方法细节和强因果判断时仍需要人工复核全文。

## 2. 调研问题与检索策略

本次调研采用 Deep Research 风格的分层查询：先生成研究问题，再为每个问题展开直接查询和相邻角度查询。相邻角度会覆盖综述、方法、评测、数据集、应用、安全、局限和近期进展，避免只检索与主题字面完全一致的论文。

| 研究问题 | 子查询数量 | 查询角度 |
| --- | ---: | --- |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | 3 | application、core、survey |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | 3 | application、benchmark、limitation |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | 3 | core、security、survey |

检索过程保留了可审计记录：每条查询包含 query id、查询文本、来源意图、年份过滤和查询角度；若覆盖检测发现缺少综述、方法、评测或安全等方向，会自动追加一次补搜。

## 3. 文献覆盖与时间分布

候选池共包含 32 条去重后记录，核心集合包含 3 篇。年份范围为 2023-2026，近三年占比为 0.688，近五年占比为 1.000。

| 来源 | 候选数量 |
| --- | ---: |
| openalex | 32 |

| 核心论文类型 | 数量 |
| --- | ---: |
| benchmark | 1 |
| method | 1 |
| survey | 1 |

| 年份 | 候选数量 |
| ---: | ---: |
| 2023 | 10 |
| 2024 | 16 |
| 2025 | 5 |
| 2026 | 1 |

## 4. 研究脉络与方法分类

本报告用 Research Lens 将核心论文映射到研究方向，而不是按检索结果顺序阅读。这样可以快速判断调研是否覆盖了领域地图中的关键板块。

- Lens 覆盖度：0.714
- 尚未充分覆盖的方向：Security & Robustness、Graph & Structured RAG

| 方向 | 覆盖论文数 | 代表论文 |
| --- | ---: | --- |
| 领域应用 | 3 | Retrieval augmented generation for large language models in healthcare: A systematic re... |
| 评测与基准 | 2 | Retrieval augmented generation for large language models in healthcare: A systematic re... |
| 生成与事实约束 | 3 | Retrieval augmented generation for large language models in healthcare: A systematic re... |
| 检索与索引 | 3 | Retrieval augmented generation for large language models in healthcare: A systematic re... |
| 综述与分类 | 1 | Retrieval augmented generation for large language models in healthcare: A systematic re... |

## 5. 核心论文精读

### P1. Retrieval augmented generation for large language models in healthcare: A systematic review

- 年份：2025
- 来源：openalex
- 类型：survey
- 作者：Lameck Mbangula Amugongo, Pietro Mascheroni, Steven E. Brooks, Stefan Doering, Jan Seidel
- URL：https://doi.org/10.1371/journal.pdig.0000877
- 引用校验：passed
- 摘要压缩：Large Language Models (LLMs) have demonstrated promising capabilities to solve complex tasks in critical sectors such as healthcare.
- 证据摘要：
  - `llm-openalex-w44112036-1` experiment: 78.9% of studies used English datasets and 21.1% are in Chinese
  - `llm-openalex-w44112036-2` limitation: There is a lack of standardised evaluation frameworks for RAG-based applications
  - `llm-openalex-w44112036-3` future_work: Need for further research and development to ensure responsible and effective adoption of RAG in the medical domain

### P2. Integrating Retrieval-Augmented Generation with Large Language Models in Nephrology: Advancing Practical Applications

- 年份：2024
- 来源：openalex
- 类型：method
- 作者：Jing Miao, Charat Thongprayoon, Supawadee Suppadungsuk, Oscar A. Garcia Valencia, Wisit Cheungpasitporn
- URL：https://doi.org/10.3390/medicina60030445
- 引用校验：passed
- 摘要压缩：The integration of large language models (LLMs) into healthcare, particularly in nephrology, represents a significant advancement in applying advanced technology to patient care, medical research, and education.
- 证据摘要：
  - `llm-openalex-w43925973-1` method: RAG strategy helps address hallucinations by integrating external data, enhancing output accuracy and relevance
  - `llm-openalex-w43925973-2` contribution: Showcase creation of a specialized ChatGPT model integrated with a RAG system tailored to KDIGO 2023 guidelines

### P3. CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of Large Language Models

- 年份：2024
- 来源：openalex
- 类型：benchmark
- 作者：Yuanjie Lyu, Zhiyu Li, Simin Niu, Feiyu Xiong, Bo Tang, Wenjin Wang, Hao Wu, Huanyong Liu
- URL：https://doi.org/10.1145/3701228
- 引用校验：passed
- 摘要压缩：Retrieval-augmented generation (RAG) is a technique that enhances the capabilities of large language models (LLMs) by incorporating external knowledge sources.
- 证据摘要：
  - `llm-openalex-w44035603-1` contribution: Develops a comprehensive benchmark evaluating all components of RAG systems across four CRUD application scenarios
  - `llm-openalex-w44035603-2` experiment: Analyzes effects of various components of the RAG system such as retriever, context length, knowledge base construction, and LLM

## 6. 方法对比表

| 论文 | 类型 | 主要贡献/方法 | 局限或需复核点 |
| --- | --- | --- | --- |
| P1. Retrieval augmented generation for large language models in healthc... | survey | 78.9% of studies used English datasets and 21.1% are in Chinese | There is a lack of standardised evaluation frameworks for RAG-based applications |
| P2. Integrating Retrieval-Augmented Generation with Large Language Mode... | method | RAG strategy helps address hallucinations by integrating external data, enhancing output accuracy and relevance | 需要进一步阅读全文确认实验设置与适用边界。 |
| P3. CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented... | benchmark | Develops a comprehensive benchmark evaluating all components of RAG systems across four CRUD application scenarios | 需要进一步阅读全文确认实验设置与适用边界。 |

## 7. 数据集与评测指标

当前版本不会凭空生成论文没有提供的数据集或数值指标，而是从标题、摘要和证据条目中抽取与 benchmark、dataset、evaluation、metric 相关的信息。若核心集合中缺少评测论文，系统会把它标记为覆盖缺口并触发补搜。

| 证据 | 论文 | 评测相关线索 |
| --- | --- | --- |
| `llm-openalex-w44112036-1` | P1 | 78.9% of studies used English datasets and 21.1% are in Chinese |
| `llm-openalex-w44112036-2` | P1 | There is a lack of standardised evaluation frameworks for RAG-based applications |
| `llm-openalex-w44035603-1` | P3 | Develops a comprehensive benchmark evaluating all components of RAG systems across four CRUD application scenarios |
| `llm-openalex-w44035603-2` | P3 | Analyzes effects of various components of the RAG system such as retriever, context length, knowledge base construction, and LLM |

## 8. 主要结论与证据

| Claim ID | 结论 | 支持证据 | 置信提示 |
| --- | --- | --- | ---: |
| `c1` | Research on retrieval augmented generation for large language models is moving from single-step generation toward tool-using, evidence-grounded workflows. | `llm-openalex-w44112036-1`, `llm-openalex-w43925973-1`, `llm-openalex-w43925973-2`, `llm-openalex-w44035603-1` | 0.650 |
| `c2` | A promising research gap is to make the literature review process auditable through claim-evidence alignment and citation checking. | `llm-openalex-w44112036-2`, `llm-openalex-w44112036-3` | 0.650 |

## 9. 争议、局限与研究空白

自动覆盖检测发现以下缺口，这些缺口不等同于最终学术结论，而是下一轮调研的优先入口：

- Security & Robustness: Selected papers do not cover Security & Robustness.
- Graph & Structured RAG: Selected papers do not cover Graph & Structured RAG.

此外，当前系统仍受三类限制影响：第一，主要依赖开放元数据和摘要，缺少全文段落级证据；第二，不同数据库的引用数、出版状态和 DOI 完整度并不一致；第三，LLM 只参与主题修正、证据抽取或润色，最终报告仍需要 Citation Check 与人工复核共同约束。

## 10. 未来方向

1. 引入 PDF/HTML 全文解析，把 Evidence Ledger 从摘要级升级为段落级，并记录页码、章节和原文定位。
2. 增加学术数据库交叉验证，把 arXiv、OpenAlex、Semantic Scholar、Crossref 与可选网页检索形成互证。
3. 将 Evidence Matrix 扩展为可交互视图，允许用户按研究问题、年份、论文类型和证据类别过滤。
4. 对每个重要 claim 进行反证搜索，区分“已有共识”“存在争议”和“证据不足”。
5. 在对话式 Session 中支持局部重跑：只补搜 benchmark、安全或近三年论文，而不重做整个流程。

## 11. 参考文献

[P1] Lameck Mbangula Amugongo, Pietro Mascheroni, Steven E. Brooks, Stefan Doering, Jan Seidel. (2025). Retrieval augmented generation for large language models in healthcare: A systematic review. https://doi.org/10.1371/journal.pdig.0000877
[P2] Jing Miao, Charat Thongprayoon, Supawadee Suppadungsuk, Oscar A. Garcia Valencia, Wisit Cheungpasitporn. (2024). Integrating Retrieval-Augmented Generation with Large Language Models in Nephrology: Advancing Practical Applications. https://doi.org/10.3390/medicina60030445
[P3] Yuanjie Lyu, Zhiyu Li, Simin Niu, Feiyu Xiong, Bo Tang, Wenjin Wang et al.. (2024). CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of Large Language Models. https://doi.org/10.1145/3701228

## 12. 附录：Evidence Matrix 与调研过程

### Evidence Matrix

| 研究问题 | 论文 | 类型 | Evidence IDs |
| --- | --- | --- | --- |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | Retrieval augmented generation for large language models in healthcare: A sys... | survey | `llm-openalex-w44112036-1`, `llm-openalex-w44112036-2`, `llm-openalex-w44112036-3` |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | Integrating Retrieval-Augmented Generation with Large Language Models in Neph... | method | `llm-openalex-w43925973-1`, `llm-openalex-w43925973-2` |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generatio... | benchmark | `llm-openalex-w44035603-1`, `llm-openalex-w44035603-2` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | Retrieval augmented generation for large language models in healthcare: A sys... | survey | `llm-openalex-w44112036-1`, `llm-openalex-w44112036-2`, `llm-openalex-w44112036-3` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | Integrating Retrieval-Augmented Generation with Large Language Models in Neph... | method | `llm-openalex-w43925973-1`, `llm-openalex-w43925973-2` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generatio... | benchmark | `llm-openalex-w44035603-1`, `llm-openalex-w44035603-2` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | Retrieval augmented generation for large language models in healthcare: A sys... | survey | `llm-openalex-w44112036-1`, `llm-openalex-w44112036-2`, `llm-openalex-w44112036-3` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | Integrating Retrieval-Augmented Generation with Large Language Models in Neph... | method | `llm-openalex-w43925973-1`, `llm-openalex-w43925973-2` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generatio... | benchmark | `llm-openalex-w44035603-1`, `llm-openalex-w44035603-2` |

### 补搜记录

- 第 1 轮补搜：新增候选 20 条；来源 `openalex`；原因：覆盖缺口补偿。

### Citation Check

| Check ID | Paper ID | 状态 | 信息 |
| --- | --- | --- | --- |
| `check-1` | `openalex:W4411203672` | passed | Citation metadata is available. |
| `check-2` | `openalex:W4392597393` | passed | Citation metadata is available. |
| `check-3` | `openalex:W4403560390` | passed | Citation metadata is available. |

### 可追溯产物

- 完整报告：``
- 快速总结：`未指定输出路径`
- 调研过程记录：`未指定输出路径`
- LLM：`deepseek`；实际使用：`true`
