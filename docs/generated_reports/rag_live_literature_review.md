# 文献调研报告：Retrieval-Augmented Generation (RAG) for Large Language Models: Advances, Challenges, and Architectures

## 执行摘要

ResearchFlow 于 2026-06-14 09:08 UTC 生成本次文献调研报告。Agent 检索 `arxiv` 来源，筛选出 12 篇核心文献，抽取 27 条证据，并将 2 条综合结论绑定回可追溯来源。

核心文献来源覆盖：arxiv。LLM 模式：deepseek；是否实际使用 LLM：true。

## 检索方法与范围

Agent 采用可追踪工作流：查询规划、联网文献检索、排序筛选、证据抽取、结论综合、引用校验和报告生成。报告中的关键判断尽量绑定到 Evidence ID，参考文献仅来自检索和筛选后的论文集合。

| Query ID | 检索式 | 来源意图 | 查询角度 | 距离 |
| --- | --- | --- | --- | --- |
| `q1` | Retrieval-Augmented Generation (RAG) for Large Language Models: Advances, Challenges, and Architectures | arxiv | core | direct |
| `q2` | retrieval-augmented generation rag large language models survey taxonomy | arxiv | survey_taxonomy | direct |
| `q3` | retrieval-augmented generation rag large language models methods systems architecture | arxiv | methods_systems | direct |
| `q4` | retrieval-augmented generation rag large language models evaluation benchmark dataset | arxiv | evaluation_benchmark | direct |
| `q5` | retrieval-augmented generation rag large language models challenges limitations open problems | arxiv | limitations_challenges | direct |
| `q6` | retrieval-augmented generation rag large language models applications case studies | arxiv | applications_domains | adjacent |
| `q7` | retrieval-augmented generation rag large language models security robustness hallucination | arxiv | security_robustness | adjacent |
| `q8` | retrieval augmented generation survey | arxiv | llm_hint | adjacent |
| `q9` | RAG architectures large language models | arxiv | llm_hint | adjacent |
| `q10` | retrieval augmented generation challenges | arxiv | llm_hint | adjacent |

## 1. 研究背景

检索增强生成（RAG）通过集成外部知识检索来增强大语言模型，有效缓解了模型幻觉和知识过时问题。然而，传统RAG系统在处理复杂多跳查询时表现不足，缺乏动态适应性和多步推理能力。近年来，研究者提出了自主迭代检索、智能体驱动的RAG架构以及动态图检索等方法，以提升检索质量、推理准确性和可解释性。这些进展推动RAG系统向更灵活、更可靠的生成方向发展。

## 2. 核心文献

### P1. Auto-RAG: Autonomous Retrieval-Augmented Generation for Large Language Models

- 作者：Tian Yu, Shaolei Zhang, Yang Feng
- 年份：2024
- 来源：arxiv
- URL: http://arxiv.org/abs/2411.19443v1
- 引用数：0
- 引用校验：passed
- 摘要：Iterative retrieval refers to the process in which the model continuously queries the retriever during generation to enhance the relevance of the retrieved knowledge, thereby improving the performance of Retrieval-Augmented Generation (RAG). Existing work typically employs few-shot prompting or manually constructed rules to implement iterative retrieval. This introduces additional inference overhead and overlooks the remarkable reasoning capabilities of Large Language Models (LLMs). In this paper, we introduce Auto-RAG, an autonomous iterative retrieval model centered on the LLM's powerful decision-making capabilities. Auto-RAG engages in multi-turn dialogues with the retriever, systematically planning retrievals and refining queries to acquire valuable knowledge. This process continues until sufficient external information is gathered, at which point the results are presented to the user. To this end, we develop a method for autonomously synthesizing reasoning-based decision-making instructions in iterative retrieval and fine-tuned the latest open-source LLMs. The experimental results indicate that Auto-RAG is capable of autonomous iterative interaction with the retriever, effectively leveraging the remarkable reasoning and decision-making abilities of LLMs, which lead to outstanding performance across six benchmarks. Further analysis reveals that Auto-RAG can autonomously adjust the number of iterations based on the difficulty of the questions and the utility of the retrieved knowledge, without requiring any human intervention. Moreover, Auto-RAG expresses the iterative retrieval process in natural language, enhancing interpretability while providing users with a more intuitive experience\footnote{Code is available at \url{https://github.com/ictnlp/Auto-RAG}.

### P2. Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG

- 作者：Aditi Singh, Abul Ehtesham, Saket Kumar, Tala Talaei Khoei, Athanasios V. Vasilakos
- 年份：2025
- 来源：arxiv
- URL: http://arxiv.org/abs/2501.09136v4
- 引用数：0
- 引用校验：passed
- 摘要：Large Language Models (LLMs) have advanced artificial intelligence by enabling human-like text generation and natural language understanding. However, their reliance on static training data limits their ability to respond to dynamic, real-time queries, resulting in outdated or inaccurate outputs. Retrieval-Augmented Generation (RAG) has emerged as a solution, enhancing LLMs by integrating real-time data retrieval to provide contextually relevant and up-to-date responses. Despite its promise, traditional RAG systems are constrained by static workflows and lack the adaptability required for multi-step reasoning and complex task management. Agentic Retrieval-Augmented Generation (Agentic RAG) transcends these limitations by embedding autonomous AI agents into the RAG pipeline. These agents leverage agentic design patterns reflection, planning, tool use, and multi-agent collaboration to dynamically manage retrieval strategies, iteratively refine contextual understanding, and adapt workflows through operational structures ranging from sequential steps to adaptive collaboration. This integration enables Agentic RAG systems to deliver flexibility, scalability, and context-awareness across diverse applications. This paper presents an analytical survey of Agentic RAG systems. It traces the evolution of RAG paradigms, introduces a principled taxonomy of Agentic RAG architectures based on agent cardinality, control structure, autonomy, and knowledge representation, and provides a comparative analysis of design trade-offs across existing frameworks. The survey examines applications in healthcare, finance, education, and enterprise document processing, and distills practical lessons for system designers and practitioners. Finally, it identifies key open research challenges related to evaluation, coordination, memory management, efficiency, and governance, outlining directions for future research.

### P3. MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries

- 作者：Yixuan Tang, Yi Yang
- 年份：2024
- 来源：arxiv
- URL: http://arxiv.org/abs/2401.15391v1
- 引用数：0
- 引用校验：passed
- 摘要：Retrieval-augmented generation (RAG) augments large language models (LLM) by retrieving relevant knowledge, showing promising potential in mitigating LLM hallucinations and enhancing response quality, thereby facilitating the great adoption of LLMs in practice. However, we find that existing RAG systems are inadequate in answering multi-hop queries, which require retrieving and reasoning over multiple pieces of supporting evidence. Furthermore, to our knowledge, no existing RAG benchmarking dataset focuses on multi-hop queries. In this paper, we develop a novel dataset, MultiHop-RAG, which consists of a knowledge base, a large collection of multi-hop queries, their ground-truth answers, and the associated supporting evidence. We detail the procedure of building the dataset, utilizing an English news article dataset as the underlying RAG knowledge base. We demonstrate the benchmarking utility of MultiHop-RAG in two experiments. The first experiment compares different embedding models for retrieving evidence for multi-hop queries. In the second experiment, we examine the capabilities of various state-of-the-art LLMs, including GPT-4, PaLM, and Llama2-70B, in reasoning and answering multi-hop queries given the evidence. Both experiments reveal that existing RAG methods perform unsatisfactorily in retrieving and answering multi-hop queries. We hope MultiHop-RAG will be a valuable resource for the community in developing effective RAG systems, thereby facilitating greater adoption of LLMs in practice. The MultiHop-RAG and implemented RAG system is publicly available at https://github.com/yixuantt/MultiHop-RAG/.

### P4. FAIR-RAG: Faithful Adaptive Iterative Refinement for Retrieval-Augmented Generation

- 作者：Mohammad Aghajani Asl, Majid Asgari-Bidhendi, Behrooz Minaei-Bidgoli
- 年份：2025
- 来源：arxiv
- URL: http://arxiv.org/abs/2510.22344v1
- 引用数：0
- 引用校验：passed
- 摘要：While Retrieval-Augmented Generation (RAG) mitigates hallucination and knowledge staleness in Large Language Models (LLMs), existing frameworks often falter on complex, multi-hop queries that require synthesizing information from disparate sources. Current advanced RAG methods, employing iterative or adaptive strategies, lack a robust mechanism to systematically identify and fill evidence gaps, often propagating noise or failing to gather a comprehensive context. We introduce FAIR-RAG, a novel agentic framework that transforms the standard RAG pipeline into a dynamic, evidence-driven reasoning process. At its core is an Iterative Refinement Cycle governed by a module we term Structured Evidence Assessment (SEA). The SEA acts as an analytical gating mechanism: it deconstructs the initial query into a checklist of required findings and audits the aggregated evidence to identify confirmed facts and, critically, explicit informational gaps. These gaps provide a precise signal to an Adaptive Query Refinement agent, which generates new, targeted sub-queries to retrieve missing information. This cycle repeats until the evidence is verified as sufficient, ensuring a comprehensive context for a final, strictly faithful generation. We conducted experiments on challenging multi-hop QA benchmarks, including HotpotQA, 2WikiMultiHopQA, and MusiQue. In a unified experimental setup, FAIR-RAG significantly outperforms strong baselines. On HotpotQA, it achieves an F1-score of 0.453 -- an absolute improvement of 8.3 points over the strongest iterative baseline -- establishing a new state-of-the-art for this class of methods on these benchmarks. Our work demonstrates that a structured, evidence-driven refinement process with explicit gap analysis is crucial for unlocking reliable and accurate reasoning in advanced RAG systems for complex, knowledge-intensive tasks.

### P5. Engineering the RAG Stack: A Comprehensive Review of the Architecture and Trust Frameworks for Retrieval-Augmented Generation Systems

- 作者：Dean Wampler, Dave Nielson, Alireza Seddighi
- 年份：2025
- 来源：arxiv
- URL: http://arxiv.org/abs/2601.05264v1
- 引用数：0
- 引用校验：passed
- 摘要：This article provides a comprehensive systematic literature review of academic studies, industrial applications, and real-world deployments from 2018 to 2025, providing a practical guide and detailed overview of modern Retrieval-Augmented Generation (RAG) architectures. RAG offers a modular approach for integrating external knowledge without increasing the capacity of the model as LLM systems expand. Research and engineering practices have been fragmented as a result of the increasing diversity of RAG methodologies, which encompasses a variety of fusion mechanisms, retrieval strategies, and orchestration approaches. We provide quantitative assessment frameworks, analyze the implications for trust and alignment, and systematically consolidate existing RAG techniques into a unified taxonomy. This document is a practical framework for the deployment of resilient, secure, and domain-adaptable RAG systems, synthesizing insights from academic literature, industry reports, and technical implementation guides. It also functions as a technical reference.

### P6. DA-RAG: Dynamic Attributed Community Search for Retrieval-Augmented Generation

- 作者：Xingyuan Zeng, Zuohan Wu, Yue Wang, Chen Zhang, Quanming Yao, Libin Zheng, Jian Yin
- 年份：2026
- 来源：arxiv
- URL: http://arxiv.org/abs/2602.08545v1
- 引用数：0
- 引用校验：passed
- 摘要：Owing to their unprecedented comprehension capabilities, large language models (LLMs) have become indispensable components of modern web search engines. From a technical perspective, this integration represents retrieval-augmented generation (RAG), which enhances LLMs by grounding them in external knowledge bases. A prevalent technical approach in this context is graph-based RAG (G-RAG). However, current G-RAG methodologies frequently underutilize graph topology, predominantly focusing on low-order structures or pre-computed static communities. This limitation affects their effectiveness in addressing dynamic and complex queries. Thus, we propose DA-RAG, which leverages attributed community search (ACS) to extract relevant subgraphs based on the queried question dynamically. DA-RAG captures high-order graph structures, allowing for the retrieval of self-complementary knowledge. Furthermore, DA-RAG is equipped with a chunk-layer oriented graph index, which facilitates efficient multi-granularity retrieval while significantly reducing both computational and economic costs. We evaluate DA-RAG on multiple datasets, demonstrating that it outperforms existing RAG methods by up to 40% in head-to-head comparisons across four metrics while reducing index construction time and token overhead by up to 37% and 41%, respectively.

### P7. FD-RAG: Federated Dual-System Retrieval-Augmented Generation

- 作者：Tianhao Gao, Kai Yang, Yiyang Li
- 年份：2026
- 来源：arxiv
- URL: http://arxiv.org/abs/2605.27432v1
- 引用数：0
- 引用校验：passed
- 摘要：Retrieval-augmented generation (RAG) has emerged as a paradigm for grounding large language models in external knowledge, yet most existing RAG systems assume centralized knowledge access and ample computation. These assumptions break down in edge environments, where knowledge is fragmented across devices, raw data cannot be shared, and repeated LLM calls are prohibitively expensive. We propose FD-RAG, a federated dual-system RAG framework that decouples lightweight memory access from on-demand LLM reasoning for decentralized deployment. Specifically, FD-RAG learns semantic-aware adaptive hypergraphs over local corpora and distills them into compact QA memories. At inference time, it answers well-covered queries via direct memory matching and invokes LLM-based reasoning only when necessary, while tracing retrieved memories to hypergraph-grounded evidence. To mitigate cross-device knowledge fragmentation, FD-RAG aggregates anonymized memories across devices without exposing raw documents. Experiments on QA benchmarks show that FD-RAG improves accuracy by up to 7.8\% while reducing latency by 8.4$\times$ compared with strong local and federated baselines. We also provide theoretical analysis establishing an $\mathcal{O}(1/ε^{2})$ convergence rate for the proposed hypergraph learning, supporting its tractable deployment in edge settings.

### P8. DyG-RAG: Dynamic Graph Retrieval-Augmented Generation with Event-Centric Reasoning

- 作者：Qingyun Sun, Jiaqi Yuan, Shan He, Xiao Guan, Haonan Yuan, Xingcheng Fu, Jianxin Li, Philip S. Yu
- 年份：2025
- 来源：arxiv
- URL: http://arxiv.org/abs/2507.13396v1
- 引用数：0
- 引用校验：passed
- 摘要：Graph Retrieval-Augmented Generation has emerged as a powerful paradigm for grounding large language models with external structured knowledge. However, existing Graph RAG methods struggle with temporal reasoning, due to their inability to model the evolving structure and order of real-world events. In this work, we introduce DyG-RAG, a novel event-centric dynamic graph retrieval-augmented generation framework designed to capture and reason over temporal knowledge embedded in unstructured text. To eliminate temporal ambiguity in traditional retrieval units, DyG-RAG proposes Dynamic Event Units (DEUs) that explicitly encode both semantic content and precise temporal anchors, enabling accurate and interpretable time-aware retrieval. To capture temporal and causal dependencies across events, DyG-RAG constructs an event graph by linking DEUs that share entities and occur close in time, supporting efficient and meaningful multi-hop reasoning. To ensure temporally consistent generation, DyG-RAG introduces an event timeline retrieval pipeline that retrieves event sequences via time-aware traversal, and proposes a Time Chain-of-Thought strategy for temporally grounded answer generation. This unified pipeline enables DyG-RAG to retrieve coherent, temporally ordered event sequences and to answer complex, time-sensitive queries that standard RAG systems cannot resolve. Extensive experiments on temporal QA benchmarks demonstrate that DyG-RAG significantly improves the accuracy and recall of three typical types of temporal reasoning questions, paving the way for more faithful and temporal-aware generation. DyG-RAG is available at https://github.com/RingBDStack/DyG-RAG.

### P9. CDF-RAG: Causal Dynamic Feedback for Adaptive Retrieval-Augmented Generation

- 作者：Elahe Khatibi, Ziyu Wang, Amir M. Rahmani
- 年份：2025
- 来源：arxiv
- URL: http://arxiv.org/abs/2504.12560v1
- 引用数：0
- 引用校验：passed
- 摘要：Retrieval-Augmented Generation (RAG) has significantly enhanced large language models (LLMs) in knowledge-intensive tasks by incorporating external knowledge retrieval. However, existing RAG frameworks primarily rely on semantic similarity and correlation-driven retrieval, limiting their ability to distinguish true causal relationships from spurious associations. This results in responses that may be factually grounded but fail to establish cause-and-effect mechanisms, leading to incomplete or misleading insights. To address this issue, we introduce Causal Dynamic Feedback for Adaptive Retrieval-Augmented Generation (CDF-RAG), a framework designed to improve causal consistency, factual accuracy, and explainability in generative reasoning. CDF-RAG iteratively refines queries, retrieves structured causal graphs, and enables multi-hop causal reasoning across interconnected knowledge sources. Additionally, it validates responses against causal pathways, ensuring logically coherent and factually grounded outputs. We evaluate CDF-RAG on four diverse datasets, demonstrating its ability to improve response accuracy and causal correctness over existing RAG-based methods. Our code is publicly available at https://github.com/ elakhatibi/CDF-RAG.

### P10. MASS-RAG: Multi-Agent Synthesis Retrieval-Augmented Generation

- 作者：Xingchen Xiao, Heyan Huang, Runheng Liu, Jincheng Xie
- 年份：2026
- 来源：arxiv
- URL: http://arxiv.org/abs/2604.18509v2
- 引用数：0
- 引用校验：passed
- 摘要：Large language models (LLMs) are widely used in retrieval-augmented generation (RAG) to incorporate external knowledge at inference time. However, when retrieved contexts are noisy, incomplete, or heterogeneous, a single generation process often struggles to reconcile evidence effectively. We propose \textbf{MASS-RAG}, a multi-agent synthesis approach to retrieval-augmented generation that structures evidence processing into multiple role-specialized agents. MASS-RAG applies distinct agents for evidence summarization, evidence extraction, and reasoning over retrieved documents, and combines their outputs through a dedicated synthesis stage to produce the final answer. This design exposes multiple intermediate evidence views, allowing the model to compare and integrate complementary information before answer generation. Experiments on four benchmarks show that MASS-RAG consistently improves performance over strong RAG baselines, particularly in settings where relevant evidence is distributed across retrieved contexts.

### P11. MAIN-RAG: Multi-Agent Filtering Retrieval-Augmented Generation

- 作者：Chia-Yuan Chang, Zhimeng Jiang, Vineeth Rakesh, Menghai Pan, Chin-Chia Michael Yeh, Guanchu Wang, Mingzhi Hu, Zhichao Xu, Yan Zheng, Mahashweta Das, Na Zou
- 年份：2024
- 来源：arxiv
- URL: http://arxiv.org/abs/2501.00332v1
- 引用数：0
- 引用校验：passed
- 摘要：Large Language Models (LLMs) are becoming essential tools for various natural language processing tasks but often suffer from generating outdated or incorrect information. Retrieval-Augmented Generation (RAG) addresses this issue by incorporating external, real-time information retrieval to ground LLM responses. However, the existing RAG systems frequently struggle with the quality of retrieval documents, as irrelevant or noisy documents degrade performance, increase computational overhead, and undermine response reliability. To tackle this problem, we propose Multi-Agent Filtering Retrieval-Augmented Generation (MAIN-RAG), a training-free RAG framework that leverages multiple LLM agents to collaboratively filter and score retrieved documents. Specifically, MAIN-RAG introduces an adaptive filtering mechanism that dynamically adjusts the relevance filtering threshold based on score distributions, effectively minimizing noise while maintaining high recall of relevant documents. The proposed approach leverages inter-agent consensus to ensure robust document selection without requiring additional training data or fine-tuning. Experimental results across four QA benchmarks demonstrate that MAIN-RAG consistently outperforms traditional RAG approaches, achieving a 2-11% improvement in answer accuracy while reducing the number of irrelevant retrieved documents. Quantitative analysis further reveals that our approach achieves superior response consistency and answer accuracy over baseline methods, offering a competitive and practical alternative to training-based solutions.

### P12. Retrieval Augmented Generation (RAG) for Fintech: Agentic Design and Evaluation

- 作者：Thomas Cook, Richard Osuagwu, Liman Tsatiashvili, Vrynsia Vrynsia, Koustav Ghosal, Maraim Masoud, Riccardo Mattivi
- 年份：2025
- 来源：arxiv
- URL: http://arxiv.org/abs/2510.25518v1
- 引用数：0
- 引用校验：passed
- 摘要：Retrieval-Augmented Generation (RAG) systems often face limitations in specialized domains such as fintech, where domain-specific ontologies, dense terminology, and acronyms complicate effective retrieval and synthesis. This paper introduces an agentic RAG architecture designed to address these challenges through a modular pipeline of specialized agents. The proposed system supports intelligent query reformulation, iterative sub-query decomposition guided by keyphrase extraction, contextual acronym resolution, and cross-encoder-based context re-ranking. We evaluate our approach against a standard RAG baseline using a curated dataset of 85 question--answer--reference triples derived from an enterprise fintech knowledge base. Experimental results demonstrate that the agentic RAG system outperforms the baseline in retrieval precision and relevance, albeit with increased latency. These findings suggest that structured, multi-agent methodologies offer a promising direction for enhancing retrieval robustness in complex, domain-specific settings.

## 3. 关键结论与证据

| Claim ID | 类型 | 结论 | Evidence IDs |
| --- | --- | --- | --- |
| `c1` | Synthesis | Research on Retrieval-Augmented Generation (RAG) for Large Language Models: Advances, Challenges, and Architectures is moving from single-step generation toward tool-using, evidence-grounded workflows. | `llm-arxiv-2411-19443v1-1`, `llm-arxiv-2411-19443v1-2`, `llm-arxiv-2501-09136v4-1`, `llm-arxiv-2401-15391v1-1` |
| `c2` | Hypothesis | A promising research gap is to make the literature review process auditable through claim-evidence alignment and citation checking. | `llm-arxiv-2501-09136v4-2`, `llm-arxiv-2510-25518v1-2` |

## RAG 研究透镜

A domain-aware lens that checks whether selected RAG papers cover survey, retrieval, grounding, evaluation, security, structured RAG, and applications.

- 覆盖度：1.000
- 缺失方向：无

| 方向 | 论文数 |
| --- | ---: |
| 领域应用 | 3 |
| 评测与基准 | 11 |
| 生成与事实约束 | 12 |
| 图结构与结构化 RAG | 6 |
| 检索与索引 | 12 |
| 安全与鲁棒性 | 4 |
| 综述与分类 | 4 |

| Paper ID | 研究方向 |
| --- | --- |
| `arxiv:2411.19443v1` | 综述与分类、检索与索引、生成与事实约束、评测与基准 |
| `arxiv:2501.09136v4` | 综述与分类、检索与索引、生成与事实约束、评测与基准、领域应用 |
| `arxiv:2401.15391v1` | 检索与索引、生成与事实约束、评测与基准 |
| `arxiv:2510.22344v1` | 综述与分类、检索与索引、生成与事实约束、评测与基准、安全与鲁棒性、图结构与结构化 RAG |
| `arxiv:2601.05264v1` | 综述与分类、检索与索引、生成与事实约束、安全与鲁棒性、领域应用 |
| `arxiv:2602.08545v1` | 检索与索引、生成与事实约束、评测与基准、图结构与结构化 RAG |
| `arxiv:2605.27432v1` | 检索与索引、生成与事实约束、评测与基准、图结构与结构化 RAG |
| `arxiv:2507.13396v1` | 检索与索引、生成与事实约束、评测与基准、图结构与结构化 RAG |
| `arxiv:2504.12560v1` | 检索与索引、生成与事实约束、评测与基准、图结构与结构化 RAG |
| `arxiv:2604.18509v2` | 检索与索引、生成与事实约束、评测与基准 |
| `arxiv:2501.00332v1` | 检索与索引、生成与事实约束、评测与基准、安全与鲁棒性 |
| `arxiv:2510.25518v1` | 检索与索引、生成与事实约束、评测与基准、安全与鲁棒性、图结构与结构化 RAG、领域应用 |

## 4. 方法与主题分类

### 贡献

- Auto-RAG achieves outstanding performance across six benchmarks. (`llm-arxiv-2411-19443v1-1`)
- This paper presents an analytical survey of Agentic RAG systems and introduces a principled taxonomy. (`llm-arxiv-2501-09136v4-1`)
- The paper develops a novel dataset, MultiHop-RAG, consisting of a knowledge base, multi-hop queries, ground-truth answers, and supporting evidence. (`llm-arxiv-2401-15391v1-1`)
- FAIR-RAG achieves a new state-of-the-art on multi-hop QA benchmarks, with an F1-score of 0.453 on HotpotQA. (`llm-arxiv-2510-22344v1-1`)
- Provides a comprehensive systematic literature review and practical guide for modern RAG architectures. (`llm-arxiv-2601-05264v1-1`)

### 方法

- Auto-RAG engages in multi-turn dialogues with the retriever, systematically planning retrievals and refining queries. (`llm-arxiv-2411-19443v1-2`)
- FAIR-RAG uses an Iterative Refinement Cycle governed by Structured Evidence Assessment (SEA) to identify evidence gaps and generate targeted sub-queries. (`llm-arxiv-2510-22344v1-2`)
- DA-RAG captures high-order graph structures and uses a chunk-layer oriented graph index for efficient multi-granularity retrieval. (`llm-arxiv-2602-08545v1-2`)
- FD-RAG learns semantic-aware adaptive hypergraphs and distills them into compact QA memories, using direct memory matching and selective LLM invocation. (`llm-arxiv-2605-27432v1-2`)
- DyG-RAG proposes Dynamic Event Units (DEUs) and Time Chain-of-Thought for temporally grounded generation. (`llm-arxiv-2507-13396v1-2`)

### 未来工作

- Key open research challenges include evaluation, coordination, memory management, efficiency, and governance. (`llm-arxiv-2501-09136v4-2`)

### 实验与评测

- Both experiments reveal that existing RAG methods perform unsatisfactorily in retrieving and answering multi-hop queries. (`llm-arxiv-2401-15391v1-2`)
- DA-RAG outperforms existing RAG methods by up to 40% across four metrics and reduces index construction time and token overhead by up to 37% and 41%. (`llm-arxiv-2602-08545v1-3`)
- FD-RAG shows improved accuracy and latency on QA benchmarks. (`llm-arxiv-2605-27432v1-3`)
- DyG-RAG significantly improves accuracy and recall of temporal reasoning questions on temporal QA benchmarks. (`llm-arxiv-2507-13396v1-3`)
- CDF-RAG improves response accuracy and causal correctness over existing RAG methods on four diverse datasets. (`llm-arxiv-2504-12560v1-3`)

### 局限

- The agentic RAG system outperforms baseline in precision and relevance but with increased latency. (`llm-arxiv-2510-25518v1-2`)

## 证据台账

| Evidence ID | Paper ID | 类型 | 置信度 | 支撑文本 |
| --- | --- | --- | ---: | --- |
| `llm-arxiv-2411-19443v1-1` | `arxiv:2411.19443v1` | 贡献 | 0.65 | The experimental results indicate that Auto-RAG is capable of autonomous iterative interaction with the retriever, effectively leveraging the remarkable reasoning and decision-making abilities of LLMs, which lead to outstanding performance across six benchmarks. |
| `llm-arxiv-2411-19443v1-2` | `arxiv:2411.19443v1` | 方法 | 0.65 | Auto-RAG engages in multi-turn dialogues with the retriever, systematically planning retrievals and refining queries to acquire valuable knowledge. |
| `llm-arxiv-2501-09136v4-1` | `arxiv:2501.09136v4` | 贡献 | 0.65 | This paper presents an analytical survey of Agentic RAG systems. It traces the evolution of RAG paradigms, introduces a principled taxonomy of Agentic RAG architectures based on agent cardinality, control structure, autonomy, and knowledge representation. |
| `llm-arxiv-2501-09136v4-2` | `arxiv:2501.09136v4` | 未来工作 | 0.65 | Finally, it identifies key open research challenges related to evaluation, coordination, memory management, efficiency, and governance, outlining directions for future research. |
| `llm-arxiv-2401-15391v1-1` | `arxiv:2401.15391v1` | 贡献 | 0.65 | In this paper, we develop a novel dataset, MultiHop-RAG, which consists of a knowledge base, a large collection of multi-hop queries, their ground-truth answers, and the associated supporting evidence. |
| `llm-arxiv-2401-15391v1-2` | `arxiv:2401.15391v1` | 实验与评测 | 0.65 | Both experiments reveal that existing RAG methods perform unsatisfactorily in retrieving and answering multi-hop queries. |
| `llm-arxiv-2510-22344v1-1` | `arxiv:2510.22344v1` | 贡献 | 0.65 | On HotpotQA, it achieves an F1-score of 0.453 -- an absolute improvement of 8.3 points over the strongest iterative baseline -- establishing a new state-of-the-art for this class of methods on these benchmarks. |
| `llm-arxiv-2510-22344v1-2` | `arxiv:2510.22344v1` | 方法 | 0.65 | At its core is an Iterative Refinement Cycle governed by a module we term Structured Evidence Assessment (SEA). The SEA acts as an analytical gating mechanism: it deconstructs the initial query into a checklist of required findings and audits the aggregated evidence to identif... |
| `llm-arxiv-2601-05264v1-1` | `arxiv:2601.05264v1` | 贡献 | 0.65 | This article provides a comprehensive systematic literature review of academic studies, industrial applications, and real-world deployments from 2018 to 2025, providing a practical guide and detailed overview of modern Retrieval-Augmented Generation (RAG) architectures. |
| `llm-arxiv-2602-08545v1-1` | `arxiv:2602.08545v1` | 贡献 | 0.65 | Thus, we propose DA-RAG, which leverages attributed community search (ACS) to extract relevant subgraphs based on the queried question dynamically. |
| `llm-arxiv-2602-08545v1-2` | `arxiv:2602.08545v1` | 方法 | 0.65 | DA-RAG captures high-order graph structures, allowing for the retrieval of self-complementary knowledge. Furthermore, DA-RAG is equipped with a chunk-layer oriented graph index, which facilitates efficient multi-granularity retrieval while significantly reducing both computati... |
| `llm-arxiv-2602-08545v1-3` | `arxiv:2602.08545v1` | 实验与评测 | 0.65 | We evaluate DA-RAG on multiple datasets, demonstrating that it outperforms existing RAG methods by up to 40% in head-to-head comparisons across four metrics while reducing index construction time and token overhead by up to 37% and 41%, respectively. |
| `llm-arxiv-2605-27432v1-1` | `arxiv:2605.27432v1` | 贡献 | 0.65 | Experiments on QA benchmarks show that FD-RAG improves accuracy by up to 7.8% while reducing latency by 8.4× compared with strong local and federated baselines. |
| `llm-arxiv-2605-27432v1-2` | `arxiv:2605.27432v1` | 方法 | 0.65 | Specifically, FD-RAG learns semantic-aware adaptive hypergraphs over local corpora and distills them into compact QA memories. At inference time, it answers well-covered queries via direct memory matching and invokes LLM-based reasoning only when necessary. |
| `llm-arxiv-2605-27432v1-3` | `arxiv:2605.27432v1` | 实验与评测 | 0.65 | Experiments on QA benchmarks show that FD-RAG improves accuracy by up to 7.8% while reducing latency by 8.4× compared with strong local and federated baselines. |
| `llm-arxiv-2507-13396v1-1` | `arxiv:2507.13396v1` | 贡献 | 0.65 | we introduce DyG-RAG, a novel event-centric dynamic graph retrieval-augmented generation framework designed to capture and reason over temporal knowledge embedded in unstructured text. |
| `llm-arxiv-2507-13396v1-2` | `arxiv:2507.13396v1` | 方法 | 0.65 | To eliminate temporal ambiguity in traditional retrieval units, DyG-RAG proposes Dynamic Event Units (DEUs) that explicitly encode both semantic content and precise temporal anchors... and proposes a Time Chain-of-Thought strategy for temporally grounded answer generation. |
| `llm-arxiv-2507-13396v1-3` | `arxiv:2507.13396v1` | 实验与评测 | 0.65 | Extensive experiments on temporal QA benchmarks demonstrate that DyG-RAG significantly improves the accuracy and recall of three typical types of temporal reasoning questions. |
| `llm-arxiv-2504-12560v1-1` | `arxiv:2504.12560v1` | 贡献 | 0.65 | we introduce Causal Dynamic Feedback for Adaptive Retrieval-Augmented Generation (CDF-RAG), a framework designed to improve causal consistency, factual accuracy, and explainability in generative reasoning. |
| `llm-arxiv-2504-12560v1-2` | `arxiv:2504.12560v1` | 方法 | 0.65 | CDF-RAG iteratively refines queries, retrieves structured causal graphs, and enables multi-hop causal reasoning across interconnected knowledge sources. Additionally, it validates responses against causal pathways. |
| `llm-arxiv-2504-12560v1-3` | `arxiv:2504.12560v1` | 实验与评测 | 0.65 | We evaluate CDF-RAG on four diverse datasets, demonstrating its ability to improve response accuracy and causal correctness over existing RAG-based methods. |
| `llm-arxiv-2604-18509v2-1` | `arxiv:2604.18509v2` | 贡献 | 0.65 | We propose MASS-RAG, a multi-agent synthesis approach to retrieval-augmented generation that structures evidence processing into multiple role-specialized agents. |
| `llm-arxiv-2604-18509v2-2` | `arxiv:2604.18509v2` | 实验与评测 | 0.65 | Experiments on four benchmarks show that MASS-RAG consistently improves performance over strong RAG baselines |
| `llm-arxiv-2501-00332v1-1` | `arxiv:2501.00332v1` | 贡献 | 0.65 | propose Multi-Agent Filtering Retrieval-Augmented Generation (MAIN-RAG), a training-free RAG framework that leverages multiple LLM agents to collaboratively filter and score retrieved documents. |
| `llm-arxiv-2501-00332v1-2` | `arxiv:2501.00332v1` | 实验与评测 | 0.65 | Experimental results across four QA benchmarks demonstrate that MAIN-RAG consistently outperforms traditional RAG approaches, achieving a 2-11% improvement in answer accuracy while reducing the number of irrelevant retrieved documents. |
| `llm-arxiv-2510-25518v1-1` | `arxiv:2510.25518v1` | 贡献 | 0.65 | This paper introduces an agentic RAG architecture designed to address these challenges through a modular pipeline of specialized agents. The proposed system supports intelligent query reformulation, iterative sub-query decomposition guided by keyphrase extraction, contextual a... |
| `llm-arxiv-2510-25518v1-2` | `arxiv:2510.25518v1` | 局限 | 0.65 | Experimental results demonstrate that the agentic RAG system outperforms the baseline in retrieval precision and relevance, albeit with increased latency. |

## 5. 对比分析

| 论文 | 主要证据 | 置信度 |
| --- | --- | --- |
| Auto-RAG: Autonomous Retrieval-Augmented Generation for Large Language Models | Auto-RAG achieves outstanding performance across six benchmarks. | 0.65 |
| Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG | This paper presents an analytical survey of Agentic RAG systems and introduces a principled taxonomy. | 0.65 |
| MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries | The paper develops a novel dataset, MultiHop-RAG, consisting of a knowledge base, multi-hop queries, ground-truth answers, and supporting evidence. | 0.65 |
| FAIR-RAG: Faithful Adaptive Iterative Refinement for Retrieval-Augmented Generation | FAIR-RAG achieves a new state-of-the-art on multi-hop QA benchmarks, with an F1-score of 0.453 on HotpotQA. | 0.65 |
| Engineering the RAG Stack: A Comprehensive Review of the Architecture and Trust Frameworks for Retrieval-Augmented Generation Systems | Provides a comprehensive systematic literature review and practical guide for modern RAG architectures. | 0.65 |
| DA-RAG: Dynamic Attributed Community Search for Retrieval-Augmented Generation | DA-RAG leverages attributed community search to dynamically extract relevant subgraphs for retrieval. | 0.65 |
| FD-RAG: Federated Dual-System Retrieval-Augmented Generation | FD-RAG improves accuracy by up to 7.8% and reduces latency by 8.4× compared to baselines. | 0.65 |
| DyG-RAG: Dynamic Graph Retrieval-Augmented Generation with Event-Centric Reasoning | DyG-RAG is a novel event-centric dynamic graph RAG framework that captures temporal knowledge. | 0.65 |
| CDF-RAG: Causal Dynamic Feedback for Adaptive Retrieval-Augmented Generation | CDF-RAG is a causal dynamic feedback framework for adaptive RAG that improves causal consistency and factual accuracy. | 0.65 |
| MASS-RAG: Multi-Agent Synthesis Retrieval-Augmented Generation | MASS-RAG introduces a multi-agent synthesis approach for RAG that structures evidence processing into multiple role-specialized agents. | 0.65 |
| MAIN-RAG: Multi-Agent Filtering Retrieval-Augmented Generation | MAIN-RAG is a training-free multi-agent filtering framework that improves RAG by adaptively filtering irrelevant documents. | 0.65 |
| Retrieval Augmented Generation (RAG) for Fintech: Agentic Design and Evaluation | The paper introduces an agentic RAG architecture for fintech with query reformulation, sub-query decomposition, acronym resolution, and re-ranking. | 0.65 |

## 6. 研究空白

- A promising research gap is to make the literature review process auditable through claim-evidence alignment and citation checking. 证据：`llm-arxiv-2501-09136v4-2`, `llm-arxiv-2510-25518v1-2`

## 7. 自动化调研局限

- 当前版本主要依赖论文元数据和摘要，尚未全面解析 PDF 正文。
- 离线 fixture 模式用于稳定演示，不代表真实联网调研覆盖度。
- 引用校验主要验证元数据可追溯性，不等同于同行评审质量判断。

## 引用校验

| Check ID | Paper ID | 状态 | 信息 |
| --- | --- | --- | --- |
| `check-1` | `arxiv:2411.19443v1` | passed | Citation metadata is available. |
| `check-2` | `arxiv:2501.09136v4` | passed | Citation metadata is available. |
| `check-3` | `arxiv:2401.15391v1` | passed | Citation metadata is available. |
| `check-4` | `arxiv:2510.22344v1` | passed | Citation metadata is available. |
| `check-5` | `arxiv:2601.05264v1` | passed | Citation metadata is available. |
| `check-6` | `arxiv:2602.08545v1` | passed | Citation metadata is available. |
| `check-7` | `arxiv:2605.27432v1` | passed | Citation metadata is available. |
| `check-8` | `arxiv:2507.13396v1` | passed | Citation metadata is available. |
| `check-9` | `arxiv:2504.12560v1` | passed | Citation metadata is available. |
| `check-10` | `arxiv:2604.18509v2` | passed | Citation metadata is available. |
| `check-11` | `arxiv:2501.00332v1` | passed | Citation metadata is available. |
| `check-12` | `arxiv:2510.25518v1` | passed | Citation metadata is available. |

## 参考文献

[P1] Tian Yu, Shaolei Zhang, Yang Feng. (2024). Auto-RAG: Autonomous Retrieval-Augmented Generation for Large Language Models. http://arxiv.org/abs/2411.19443v1
[P2] Aditi Singh, Abul Ehtesham, Saket Kumar, Tala Talaei Khoei, Athanasios V. Vasilakos. (2025). Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG. http://arxiv.org/abs/2501.09136v4
[P3] Yixuan Tang, Yi Yang. (2024). MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries. http://arxiv.org/abs/2401.15391v1
[P4] Mohammad Aghajani Asl, Majid Asgari-Bidhendi, Behrooz Minaei-Bidgoli. (2025). FAIR-RAG: Faithful Adaptive Iterative Refinement for Retrieval-Augmented Generation. http://arxiv.org/abs/2510.22344v1
[P5] Dean Wampler, Dave Nielson, Alireza Seddighi. (2025). Engineering the RAG Stack: A Comprehensive Review of the Architecture and Trust Frameworks for Retrieval-Augmented Generation Systems. http://arxiv.org/abs/2601.05264v1
[P6] Xingyuan Zeng, Zuohan Wu, Yue Wang, Chen Zhang, Quanming Yao, Libin Zheng, Jian Yin. (2026). DA-RAG: Dynamic Attributed Community Search for Retrieval-Augmented Generation. http://arxiv.org/abs/2602.08545v1
[P7] Tianhao Gao, Kai Yang, Yiyang Li. (2026). FD-RAG: Federated Dual-System Retrieval-Augmented Generation. http://arxiv.org/abs/2605.27432v1
[P8] Qingyun Sun, Jiaqi Yuan, Shan He, Xiao Guan, Haonan Yuan, Xingcheng Fu, Jianxin Li, Philip S. Yu. (2025). DyG-RAG: Dynamic Graph Retrieval-Augmented Generation with Event-Centric Reasoning. http://arxiv.org/abs/2507.13396v1
[P9] Elahe Khatibi, Ziyu Wang, Amir M. Rahmani. (2025). CDF-RAG: Causal Dynamic Feedback for Adaptive Retrieval-Augmented Generation. http://arxiv.org/abs/2504.12560v1
[P10] Xingchen Xiao, Heyan Huang, Runheng Liu, Jincheng Xie. (2026). MASS-RAG: Multi-Agent Synthesis Retrieval-Augmented Generation. http://arxiv.org/abs/2604.18509v2
[P11] Chia-Yuan Chang, Zhimeng Jiang, Vineeth Rakesh, Menghai Pan, Chin-Chia Michael Yeh, Guanchu Wang, Mingzhi Hu, Zhichao Xu, Yan Zheng, Mahashweta Das, Na Zou. (2024). MAIN-RAG: Multi-Agent Filtering Retrieval-Augmented Generation. http://arxiv.org/abs/2501.00332v1
[P12] Thomas Cook, Richard Osuagwu, Liman Tsatiashvili, Vrynsia Vrynsia, Koustav Ghosal, Maraim Masoud, Riccardo Mattivi. (2025). Retrieval Augmented Generation (RAG) for Fintech: Agentic Design and Evaluation. http://arxiv.org/abs/2510.25518v1
