# Literature Review: retrieval augmented generation for large language models

## Executive Summary

ResearchFlow generated this literature review on 2026-06-11 06:22 UTC. The agent searched `arxiv` sources, selected 15 core papers, extracted 51 evidence items, and linked 2 synthesis claims back to retrieved sources.

Selected source coverage: arxiv. LLM mode: deepseek; LLM used: true.

## Search Method and Scope

The agent follows a traceable workflow: query planning, live paper search, ranking, evidence extraction, claim synthesis, citation checking, and report writing.

| Query ID | Search Query | Source Intent |
| --- | --- | --- |
| `q1` | retrieval augmented generation for large language models | arxiv |
| `q2` | retrieval augmented generation large language models survey | arxiv |
| `q3` | retrieval augmented generation large language models methods | arxiv |
| `q4` | retrieval augmented generation large language models evaluation benchmark | arxiv |
| `q5` | retrieval augmented generation large language models challenges limitations | arxiv |

## 1. Research Background

Retrieval-Augmented Generation (RAG) has emerged as a prominent paradigm to address the limitations of large language models (LLMs) by integrating external knowledge retrieval. Early RAG systems rely on static retrieval workflows, which often struggle with complex queries requiring multi-step reasoning and dynamic evidence gathering. Recent advancements have introduced iterative and autonomous retrieval mechanisms that leverage LLMs' reasoning capabilities to plan and refine queries. Additionally, graph-based RAG methods incorporate structural information to capture relationships between knowledge pieces, improving multi-hop reasoning. Agentic RAG frameworks embed autonomous agents for adaptive retrieval and synthesis. Despite these improvements, challenges remain in handling temporal, noisy, or heterogeneous data, as well as ensuring faithful generation and efficient retrieval. Evaluation platforms and benchmarks are being developed to systematically assess RAG systems across domains.

## 2. Core Papers

### P1. Auto-RAG: Autonomous Retrieval-Augmented Generation for Large Language Models

- Authors: Tian Yu, Shaolei Zhang, Yang Feng
- Year: 2024
- Source: arxiv
- URL: http://arxiv.org/abs/2411.19443v1
- Citations: 0
- Citation check: passed
- Summary: Iterative retrieval refers to the process in which the model continuously queries the retriever during generation to enhance the relevance of the retrieved knowledge, thereby improving the performance of Retrieval-Augmented Generation (RAG). Existing work typically employs few-shot prompting or manually constructed rules to implement iterative retrieval. This introduces additional inference overhead and overlooks the remarkable reasoning capabilities of Large Language Models (LLMs). In this paper, we introduce Auto-RAG, an autonomous iterative retrieval model centered on the LLM's powerful decision-making capabilities. Auto-RAG engages in multi-turn dialogues with the retriever, systematically planning retrievals and refining queries to acquire valuable knowledge. This process continues until sufficient external information is gathered, at which point the results are presented to the user. To this end, we develop a method for autonomously synthesizing reasoning-based decision-making instructions in iterative retrieval and fine-tuned the latest open-source LLMs. The experimental results indicate that Auto-RAG is capable of autonomous iterative interaction with the retriever, effectively leveraging the remarkable reasoning and decision-making abilities of LLMs, which lead to outstanding performance across six benchmarks. Further analysis reveals that Auto-RAG can autonomously adjust the number of iterations based on the difficulty of the questions and the utility of the retrieved knowledge, without requiring any human intervention. Moreover, Auto-RAG expresses the iterative retrieval process in natural language, enhancing interpretability while providing users with a more intuitive experience\footnote{Code is available at \url{https://github.com/ictnlp/Auto-RAG}.

### P2. Investigating Retrieval-Augmented Generation in Quranic Studies: A Study of 13 Open-Source Large Language Models

- Authors: Zahra Khalila, Arbi Haza Nasution, Winda Monika, Aytug Onan, Yohei Murakami, Yasir Bin Ismail Radi, Noor Mohammad Osmani
- Year: 2025
- Source: arxiv
- URL: http://arxiv.org/abs/2503.16581v1
- Citations: 0
- Citation check: passed
- Summary: Accurate and contextually faithful responses are critical when applying large language models (LLMs) to sensitive and domain-specific tasks, such as answering queries related to quranic studies. General-purpose LLMs often struggle with hallucinations, where generated responses deviate from authoritative sources, raising concerns about their reliability in religious contexts. This challenge highlights the need for systems that can integrate domain-specific knowledge while maintaining response accuracy, relevance, and faithfulness. In this study, we investigate 13 open-source LLMs categorized into large (e.g., Llama3:70b, Gemma2:27b, QwQ:32b), medium (e.g., Gemma2:9b, Llama3:8b), and small (e.g., Llama3.2:3b, Phi3:3.8b). A Retrieval-Augmented Generation (RAG) is used to make up for the problems that come with using separate models. This research utilizes a descriptive dataset of Quranic surahs including the meanings, historical context, and qualities of the 114 surahs, allowing the model to gather relevant knowledge before responding. The models are evaluated using three key metrics set by human evaluators: context relevance, answer faithfulness, and answer relevance. The findings reveal that large models consistently outperform smaller models in capturing query semantics and producing accurate, contextually grounded responses. The Llama3.2:3b model, even though it is considered small, does very well on faithfulness (4.619) and relevance (4.857), showing the promise of smaller architectures that have been well optimized. This article examines the trade-offs between model size, computational efficiency, and response quality while using LLMs in domain-specific applications.

### P3. MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries

- Authors: Yixuan Tang, Yi Yang
- Year: 2024
- Source: arxiv
- URL: http://arxiv.org/abs/2401.15391v1
- Citations: 0
- Citation check: passed
- Summary: Retrieval-augmented generation (RAG) augments large language models (LLM) by retrieving relevant knowledge, showing promising potential in mitigating LLM hallucinations and enhancing response quality, thereby facilitating the great adoption of LLMs in practice. However, we find that existing RAG systems are inadequate in answering multi-hop queries, which require retrieving and reasoning over multiple pieces of supporting evidence. Furthermore, to our knowledge, no existing RAG benchmarking dataset focuses on multi-hop queries. In this paper, we develop a novel dataset, MultiHop-RAG, which consists of a knowledge base, a large collection of multi-hop queries, their ground-truth answers, and the associated supporting evidence. We detail the procedure of building the dataset, utilizing an English news article dataset as the underlying RAG knowledge base. We demonstrate the benchmarking utility of MultiHop-RAG in two experiments. The first experiment compares different embedding models for retrieving evidence for multi-hop queries. In the second experiment, we examine the capabilities of various state-of-the-art LLMs, including GPT-4, PaLM, and Llama2-70B, in reasoning and answering multi-hop queries given the evidence. Both experiments reveal that existing RAG methods perform unsatisfactorily in retrieving and answering multi-hop queries. We hope MultiHop-RAG will be a valuable resource for the community in developing effective RAG systems, thereby facilitating greater adoption of LLMs in practice. The MultiHop-RAG and implemented RAG system is publicly available at https://github.com/yixuantt/MultiHop-RAG/.

### P4. Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG

- Authors: Aditi Singh, Abul Ehtesham, Saket Kumar, Tala Talaei Khoei, Athanasios V. Vasilakos
- Year: 2025
- Source: arxiv
- URL: http://arxiv.org/abs/2501.09136v4
- Citations: 0
- Citation check: passed
- Summary: Large Language Models (LLMs) have advanced artificial intelligence by enabling human-like text generation and natural language understanding. However, their reliance on static training data limits their ability to respond to dynamic, real-time queries, resulting in outdated or inaccurate outputs. Retrieval-Augmented Generation (RAG) has emerged as a solution, enhancing LLMs by integrating real-time data retrieval to provide contextually relevant and up-to-date responses. Despite its promise, traditional RAG systems are constrained by static workflows and lack the adaptability required for multi-step reasoning and complex task management. Agentic Retrieval-Augmented Generation (Agentic RAG) transcends these limitations by embedding autonomous AI agents into the RAG pipeline. These agents leverage agentic design patterns reflection, planning, tool use, and multi-agent collaboration to dynamically manage retrieval strategies, iteratively refine contextual understanding, and adapt workflows through operational structures ranging from sequential steps to adaptive collaboration. This integration enables Agentic RAG systems to deliver flexibility, scalability, and context-awareness across diverse applications. This paper presents an analytical survey of Agentic RAG systems. It traces the evolution of RAG paradigms, introduces a principled taxonomy of Agentic RAG architectures based on agent cardinality, control structure, autonomy, and knowledge representation, and provides a comparative analysis of design trade-offs across existing frameworks. The survey examines applications in healthcare, finance, education, and enterprise document processing, and distills practical lessons for system designers and practitioners. Finally, it identifies key open research challenges related to evaluation, coordination, memory management, efficiency, and governance, outlining directions for future research.

### P5. DA-RAG: Dynamic Attributed Community Search for Retrieval-Augmented Generation

- Authors: Xingyuan Zeng, Zuohan Wu, Yue Wang, Chen Zhang, Quanming Yao, Libin Zheng, Jian Yin
- Year: 2026
- Source: arxiv
- URL: http://arxiv.org/abs/2602.08545v1
- Citations: 0
- Citation check: passed
- Summary: Owing to their unprecedented comprehension capabilities, large language models (LLMs) have become indispensable components of modern web search engines. From a technical perspective, this integration represents retrieval-augmented generation (RAG), which enhances LLMs by grounding them in external knowledge bases. A prevalent technical approach in this context is graph-based RAG (G-RAG). However, current G-RAG methodologies frequently underutilize graph topology, predominantly focusing on low-order structures or pre-computed static communities. This limitation affects their effectiveness in addressing dynamic and complex queries. Thus, we propose DA-RAG, which leverages attributed community search (ACS) to extract relevant subgraphs based on the queried question dynamically. DA-RAG captures high-order graph structures, allowing for the retrieval of self-complementary knowledge. Furthermore, DA-RAG is equipped with a chunk-layer oriented graph index, which facilitates efficient multi-granularity retrieval while significantly reducing both computational and economic costs. We evaluate DA-RAG on multiple datasets, demonstrating that it outperforms existing RAG methods by up to 40% in head-to-head comparisons across four metrics while reducing index construction time and token overhead by up to 37% and 41%, respectively.

### P6. Bridge-RAG: An Abstract Bridge Tree Based Retrieval Augmented Generation Algorithm

- Authors: Zihang Li, Wenjun Liu, Yikun Zong, Jiawen Tao, Siying Dai, Songcheng Ren, Zirui Liu, Yuhang Wang, Yanbing Jiang, Tong Yang
- Year: 2026
- Source: arxiv
- URL: http://arxiv.org/abs/2603.26668v2
- Citations: 0
- Citation check: passed
- Summary: As an important paradigm for enhancing the generation quality of Large Language Models (LLMs), retrieval-augmented generation (RAG) faces the two challenges regarding retrieval accuracy and computational efficiency. This paper presents a novel RAG framework called Bridge-RAG. To overcome the accuracy challenge, we introduce the concept of abstract to bridge query entities and document chunks, providing robust semantic understanding. We organize the abstracts into a tree structure and design a multi-level retrieval strategy to ensure the inclusion of sufficient contextual information. While this hierarchical organization substantially improves answer quality, traversing the tree to locate the abstracts that contain a query entity inevitably introduces additional retrieval overhead. To restore retrieval efficiency, we further integrate the Cuckoo Filter in CFT-RAG, which provides O(1) entity lookup and naturally fits the entity-to-abstract pathway of our framework. Extensive experiments show that Bridge-RAG achieves consistent accuracy improvements across all metrics and up to $1.9\times$ faster retrieval compared to structured RAG baselines.

### P7. FAIR-RAG: Faithful Adaptive Iterative Refinement for Retrieval-Augmented Generation

- Authors: Mohammad Aghajani Asl, Majid Asgari-Bidhendi, Behrooz Minaei-Bidgoli
- Year: 2025
- Source: arxiv
- URL: http://arxiv.org/abs/2510.22344v1
- Citations: 0
- Citation check: passed
- Summary: While Retrieval-Augmented Generation (RAG) mitigates hallucination and knowledge staleness in Large Language Models (LLMs), existing frameworks often falter on complex, multi-hop queries that require synthesizing information from disparate sources. Current advanced RAG methods, employing iterative or adaptive strategies, lack a robust mechanism to systematically identify and fill evidence gaps, often propagating noise or failing to gather a comprehensive context. We introduce FAIR-RAG, a novel agentic framework that transforms the standard RAG pipeline into a dynamic, evidence-driven reasoning process. At its core is an Iterative Refinement Cycle governed by a module we term Structured Evidence Assessment (SEA). The SEA acts as an analytical gating mechanism: it deconstructs the initial query into a checklist of required findings and audits the aggregated evidence to identify confirmed facts and, critically, explicit informational gaps. These gaps provide a precise signal to an Adaptive Query Refinement agent, which generates new, targeted sub-queries to retrieve missing information. This cycle repeats until the evidence is verified as sufficient, ensuring a comprehensive context for a final, strictly faithful generation. We conducted experiments on challenging multi-hop QA benchmarks, including HotpotQA, 2WikiMultiHopQA, and MusiQue. In a unified experimental setup, FAIR-RAG significantly outperforms strong baselines. On HotpotQA, it achieves an F1-score of 0.453 -- an absolute improvement of 8.3 points over the strongest iterative baseline -- establishing a new state-of-the-art for this class of methods on these benchmarks. Our work demonstrates that a structured, evidence-driven refinement process with explicit gap analysis is crucial for unlocking reliable and accurate reasoning in advanced RAG systems for complex, knowledge-intensive tasks.

### P8. RAG-Check: Evaluating Multimodal Retrieval Augmented Generation Performance

- Authors: Matin Mortaheb, Mohammad A. Amir Khojastepour, Srimat T. Chakradhar, Sennur Ulukus
- Year: 2025
- Source: arxiv
- URL: http://arxiv.org/abs/2501.03995v1
- Citations: 0
- Citation check: passed
- Summary: Retrieval-augmented generation (RAG) improves large language models (LLMs) by using external knowledge to guide response generation, reducing hallucinations. However, RAG, particularly multi-modal RAG, can introduce new hallucination sources: (i) the retrieval process may select irrelevant pieces (e.g., documents, images) as raw context from the database, and (ii) retrieved images are processed into text-based context via vision-language models (VLMs) or directly used by multi-modal language models (MLLMs) like GPT-4o, which may hallucinate. To address this, we propose a novel framework to evaluate the reliability of multi-modal RAG using two performance measures: (i) the relevancy score (RS), assessing the relevance of retrieved entries to the query, and (ii) the correctness score (CS), evaluating the accuracy of the generated response. We train RS and CS models using a ChatGPT-derived database and human evaluator samples. Results show that both models achieve ~88% accuracy on test data. Additionally, we construct a 5000-sample human-annotated database evaluating the relevancy of retrieved pieces and the correctness of response statements. Our RS model aligns with human preferences 20% more often than CLIP in retrieval, and our CS model matches human preferences ~91% of the time. Finally, we assess various RAG systems' selection and generation performances using RS and CS.

### P9. MASS-RAG: Multi-Agent Synthesis Retrieval-Augmented Generation

- Authors: Xingchen Xiao, Heyan Huang, Runheng Liu, Jincheng Xie
- Year: 2026
- Source: arxiv
- URL: http://arxiv.org/abs/2604.18509v2
- Citations: 0
- Citation check: passed
- Summary: Large language models (LLMs) are widely used in retrieval-augmented generation (RAG) to incorporate external knowledge at inference time. However, when retrieved contexts are noisy, incomplete, or heterogeneous, a single generation process often struggles to reconcile evidence effectively. We propose \textbf{MASS-RAG}, a multi-agent synthesis approach to retrieval-augmented generation that structures evidence processing into multiple role-specialized agents. MASS-RAG applies distinct agents for evidence summarization, evidence extraction, and reasoning over retrieved documents, and combines their outputs through a dedicated synthesis stage to produce the final answer. This design exposes multiple intermediate evidence views, allowing the model to compare and integrate complementary information before answer generation. Experiments on four benchmarks show that MASS-RAG consistently improves performance over strong RAG baselines, particularly in settings where relevant evidence is distributed across retrieved contexts.

### P10. Structure-Aware RAG: Structured Retrieval Augmented Generation from Noisy Data for Conversational Agents

- Authors: Kaiqiao Han, LuAn Tang, Renliang Sun, Peng Yuan, Wei Cheng, Haoyu Wang, Wei Wang, Yizhou Sun, Haifeng Chen
- Year: 2026
- Source: arxiv
- URL: http://arxiv.org/abs/2605.24366v1
- Citations: 0
- Citation check: passed
- Summary: Large Language Models (LLMs) have been widely adopted in conversational applications. However, their reliance on parametric knowledge limits reliability in real-world scenarios that require dynamic or domain-specific information. Retrieval-Augmented Generation (RAG) addresses this limitation by incorporating external knowledge during generation, but existing text-based and graph-based RAG methods often struggle with noisy or irrelevant contexts. In this work, we propose Structure-aware Retrieval Augmented Generation (SA-RAG), which uses tables as an intermediate structured representation to provide a compact and controllable interface that reduces noise while preserving essential information. We introduce a quality-aware table metadata generation framework that models metadata normalization and effectiveness, improving metadata quality and downstream performance. Furthermore, we explore both training-free and training-based table generation methods. Generation validation and direct preference optimization further improve table quality while maintaining semantic and structural consistency. Experiments on two noisy real-world datasets show that SA-RAG significantly outperforms existing RAG baselines. Our code is publicly available at a public repository.

### P11. FD-RAG: Federated Dual-System Retrieval-Augmented Generation

- Authors: Tianhao Gao, Kai Yang, Yiyang Li
- Year: 2026
- Source: arxiv
- URL: http://arxiv.org/abs/2605.27432v1
- Citations: 0
- Citation check: passed
- Summary: Retrieval-augmented generation (RAG) has emerged as a paradigm for grounding large language models in external knowledge, yet most existing RAG systems assume centralized knowledge access and ample computation. These assumptions break down in edge environments, where knowledge is fragmented across devices, raw data cannot be shared, and repeated LLM calls are prohibitively expensive. We propose FD-RAG, a federated dual-system RAG framework that decouples lightweight memory access from on-demand LLM reasoning for decentralized deployment. Specifically, FD-RAG learns semantic-aware adaptive hypergraphs over local corpora and distills them into compact QA memories. At inference time, it answers well-covered queries via direct memory matching and invokes LLM-based reasoning only when necessary, while tracing retrieved memories to hypergraph-grounded evidence. To mitigate cross-device knowledge fragmentation, FD-RAG aggregates anonymized memories across devices without exposing raw documents. Experiments on QA benchmarks show that FD-RAG improves accuracy by up to 7.8\% while reducing latency by 8.4$\times$ compared with strong local and federated baselines. We also provide theoretical analysis establishing an $\mathcal{O}(1/ε^{2})$ convergence rate for the proposed hypergraph learning, supporting its tractable deployment in edge settings.

### P12. SPD-RAG: Sub-Agent Per Document Retrieval-Augmented Generation

- Authors: Yagiz Can Akay, Muhammed Yusuf Kartal, Esra Alparslan, Faruk Ortakoyluoglu, Arda Akpinar
- Year: 2026
- Source: arxiv
- URL: http://arxiv.org/abs/2603.08329v1
- Citations: 0
- Citation check: passed
- Summary: Answering complex, real-world queries often requires synthesizing facts scattered across vast document corpora. In these settings, standard retrieval-augmented generation (RAG) pipelines suffer from incomplete evidence coverage, while long-context large language models (LLMs) struggle to reason reliably over massive inputs. We introduce SPD-RAG, a hierarchical multi-agent framework for exhaustive cross-document question answering that decomposes the problem along the document axis. Each document is processed by a dedicated document-level agent operating only on its own content, enabling focused retrieval, while a coordinator dispatches tasks to relevant agents and aggregates their partial answers. Agent outputs are synthesized by merging partial answers through a token-bounded synthesis layer (which supports recursive map-reduce for massive corpora). This document-level specialization with centralized fusion improves scalability and answer quality in heterogeneous multidocument settings while yielding a modular, extensible retrieval pipeline. On the LOONG benchmark (EMNLP 2024) for long-context multi-document QA, SPD-RAG achieves an Avg Score of 58.1 (GPT-5 evaluation), outperforming Normal RAG (33.0) and Agentic RAG (32.8) while using only 38% of the API cost of a full-context baseline (68.0).

### P13. GFM-RAG: Graph Foundation Model for Retrieval Augmented Generation

- Authors: Linhao Luo, Zicheng Zhao, Gholamreza Haffari, Dinh Phung, Chen Gong, Shirui Pan
- Year: 2025
- Source: arxiv
- URL: http://arxiv.org/abs/2502.01113v3
- Citations: 0
- Citation check: passed
- Summary: Retrieval-augmented generation (RAG) has proven effective in integrating knowledge into large language models (LLMs). However, conventional RAGs struggle to capture complex relationships between pieces of knowledge, limiting their performance in intricate reasoning that requires integrating knowledge from multiple sources. Recently, graph-enhanced retrieval augmented generation (GraphRAG) builds graph structure to explicitly model these relationships, enabling more effective and efficient retrievers. Nevertheless, its performance is still hindered by the noise and incompleteness within the graph structure. To address this, we introduce GFM-RAG, a novel graph foundation model (GFM) for retrieval augmented generation. GFM-RAG is powered by an innovative graph neural network that reasons over graph structure to capture complex query-knowledge relationships. The GFM with 8M parameters undergoes a two-stage training process on large-scale datasets, comprising 60 knowledge graphs with over 14M triples and 700k documents. This results in impressive performance and generalizability for GFM-RAG, making it the first graph foundation model applicable to unseen datasets for retrieval without any fine-tuning required. Extensive experiments on three multi-hop QA datasets and seven domain-specific RAG datasets demonstrate that GFM-RAG achieves state-of-the-art performance while maintaining efficiency and alignment with neural scaling laws, highlighting its potential for further improvement.

### P14. DyG-RAG: Dynamic Graph Retrieval-Augmented Generation with Event-Centric Reasoning

- Authors: Qingyun Sun, Jiaqi Yuan, Shan He, Xiao Guan, Haonan Yuan, Xingcheng Fu, Jianxin Li, Philip S. Yu
- Year: 2025
- Source: arxiv
- URL: http://arxiv.org/abs/2507.13396v1
- Citations: 0
- Citation check: passed
- Summary: Graph Retrieval-Augmented Generation has emerged as a powerful paradigm for grounding large language models with external structured knowledge. However, existing Graph RAG methods struggle with temporal reasoning, due to their inability to model the evolving structure and order of real-world events. In this work, we introduce DyG-RAG, a novel event-centric dynamic graph retrieval-augmented generation framework designed to capture and reason over temporal knowledge embedded in unstructured text. To eliminate temporal ambiguity in traditional retrieval units, DyG-RAG proposes Dynamic Event Units (DEUs) that explicitly encode both semantic content and precise temporal anchors, enabling accurate and interpretable time-aware retrieval. To capture temporal and causal dependencies across events, DyG-RAG constructs an event graph by linking DEUs that share entities and occur close in time, supporting efficient and meaningful multi-hop reasoning. To ensure temporally consistent generation, DyG-RAG introduces an event timeline retrieval pipeline that retrieves event sequences via time-aware traversal, and proposes a Time Chain-of-Thought strategy for temporally grounded answer generation. This unified pipeline enables DyG-RAG to retrieve coherent, temporally ordered event sequences and to answer complex, time-sensitive queries that standard RAG systems cannot resolve. Extensive experiments on temporal QA benchmarks demonstrate that DyG-RAG significantly improves the accuracy and recall of three typical types of temporal reasoning questions, paving the way for more faithful and temporal-aware generation. DyG-RAG is available at https://github.com/RingBDStack/DyG-RAG.

### P15. OmniBench-RAG: A Multi-Domain Evaluation Platform for Retrieval-Augmented Generation Tools

- Authors: Jiaxuan Liang, Shide Zhou, Kailong Wang
- Year: 2025
- Source: arxiv
- URL: http://arxiv.org/abs/2508.05650v1
- Citations: 0
- Citation check: passed
- Summary: While Retrieval Augmented Generation (RAG) is now widely adopted to enhance LLMs, evaluating its true performance benefits in a reproducible and interpretable way remains a major hurdle. Existing methods often fall short: they lack domain coverage, employ coarse metrics that miss sub document precision, and fail to capture computational trade offs. Most critically, they provide no standardized framework for comparing RAG effectiveness across different models and domains. We introduce OmniBench RAG, a novel automated platform for multi domain evaluation of RAG systems. The platform quantifies performance gains across accuracy and efficiency dimensions, spanning nine knowledge fields including culture, geography, and health. We introduce two standardized metrics: Improvements (accuracy gains) and Transformation (efficiency differences between pre RAG and post RAG models), enabling reproducible comparisons across models and tasks. The platform features dynamic test generation, modular evaluation pipelines, and automated knowledge base construction. Our evaluation reveals striking variability in RAG effectiveness, from significant gains in culture to declines in mathematics, highlighting the critical importance of systematic, domain aware assessment. A demonstration video is available at: https://www.youtube.com/watch?v=BZx83QFcTCI. Code and datasets: https://github.com/Garnett-Liang/Omnibench-RAG.

## 3. Key Claims and Evidence

| Claim ID | Type | Claim | Evidence IDs |
| --- | --- | --- | --- |
| `c1` | Synthesis | Research on retrieval augmented generation for large language models is moving from single-step generation toward tool-using, evidence-grounded workflows. | `llm-arxiv-2411-19443v1-1`, `llm-arxiv-2411-19443v1-2`, `llm-arxiv-2503-16581v1-1`, `llm-arxiv-2503-16581v1-2` |
| `c2` | Hypothesis | A promising research gap is to make the literature review process auditable through claim-evidence alignment and citation checking. | `llm-arxiv-2503-16581v1-3`, `llm-arxiv-2401-15391v1-3`, `llm-arxiv-2501-09136v4-2` |

## RAG Research Lens

A domain-aware lens that checks whether selected RAG papers cover survey, retrieval, grounding, evaluation, security, structured RAG, and applications.

- Coverage: 1.000
- Missing dimensions: None

| Dimension | Paper Count |
| --- | ---: |
| Domain Applications | 5 |
| Evaluation & Benchmarks | 15 |
| Generation & Grounding | 15 |
| Graph & Structured RAG | 8 |
| Retrieval & Indexing | 15 |
| Security & Robustness | 2 |
| Survey & Taxonomy | 4 |

| Paper ID | Lens Dimensions |
| --- | --- |
| `arxiv:2411.19443v1` | Survey & Taxonomy, Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks |
| `arxiv:2503.16581v1` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Domain Applications |
| `arxiv:2401.15391v1` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks |
| `arxiv:2501.09136v4` | Survey & Taxonomy, Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Domain Applications |
| `arxiv:2602.08545v1` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Graph & Structured RAG |
| `arxiv:2603.26668v2` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Security & Robustness, Graph & Structured RAG |
| `arxiv:2510.22344v1` | Survey & Taxonomy, Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Security & Robustness, Graph & Structured RAG |
| `arxiv:2501.03995v1` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks |
| `arxiv:2604.18509v2` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks |
| `arxiv:2605.24366v1` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Graph & Structured RAG, Domain Applications |
| `arxiv:2605.27432v1` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Graph & Structured RAG |
| `arxiv:2603.08329v1` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks |
| `arxiv:2502.01113v3` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Graph & Structured RAG, Domain Applications |
| `arxiv:2507.13396v1` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Graph & Structured RAG |
| `arxiv:2508.05650v1` | Survey & Taxonomy, Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Graph & Structured RAG, Domain Applications |

## 4. Method Taxonomy

### Contribution

- Auto-RAG is an autonomous iterative retrieval model that leverages LLM's decision-making to iteratively interact with the retriever. (`llm-arxiv-2411-19443v1-1`)
- Investigates 13 open-source LLMs with RAG for Quranic studies. (`llm-arxiv-2503-16581v1-1`)
- Develops MultiHop-RAG, a benchmark dataset for multi-hop queries in RAG. (`llm-arxiv-2401-15391v1-1`)
- Provides a comprehensive survey and taxonomy of Agentic RAG systems. (`llm-arxiv-2501-09136v4-1`)
- Bridge-RAG introduces abstract to bridge query entities and document chunks. (`llm-arxiv-2603-26668v2-1`)

### Experiment

- Auto-RAG outperforms existing methods across six benchmarks. (`llm-arxiv-2411-19443v1-2`)
- Large models consistently outperform smaller models in capturing query semantics. (`llm-arxiv-2503-16581v1-2`)
- Existing RAG methods perform unsatisfactorily in retrieving and answering multi-hop queries. (`llm-arxiv-2401-15391v1-2`)
- DA-RAG outperforms existing RAG methods by up to 40% in head-to-head comparisons. (`llm-arxiv-2602-08545v1-3`)
- DA-RAG reduces index construction time and token overhead by up to 37% and 41%. (`llm-arxiv-2602-08545v1-4`)

### Limitation

- General-purpose LLMs often struggle with hallucinations in religious contexts. (`llm-arxiv-2503-16581v1-3`)
- Current G-RAG methodologies underutilize graph topology, focusing on low-order structures or pre-computed static communities. (`llm-arxiv-2602-08545v1-5`)
- Current advanced RAG methods lack a robust mechanism to identify and fill evidence gaps. (`llm-arxiv-2510-22344v1-4`)
- Multi-modal RAG can introduce new hallucination sources from retrieval and VLM processing. (`llm-arxiv-2501-03995v1-4`)
- Single generation process struggles to reconcile evidence when contexts are noisy or heterogeneous. (`llm-arxiv-2604-18509v2-5`)

### Future Work

- MultiHop-RAG will be a valuable resource for developing effective RAG systems. (`llm-arxiv-2401-15391v1-3`)
- Identifies key open research challenges including evaluation, coordination, memory management, efficiency, and governance. (`llm-arxiv-2501-09136v4-2`)

### Method

- DA-RAG uses attributed community search to dynamically extract relevant subgraphs based on the query. (`llm-arxiv-2602-08545v1-1`)
- DA-RAG captures high-order graph structures for self-complementary knowledge retrieval. (`llm-arxiv-2602-08545v1-2`)
- Bridge-RAG uses a multi-level retrieval strategy with abstracts organized in a tree structure. (`llm-arxiv-2603-26668v2-2`)
- Bridge-RAG integrates Cuckoo Filter for O(1) entity lookup. (`llm-arxiv-2603-26668v2-3`)
- FAIR-RAG uses Structured Evidence Assessment (SEA) to identify explicit informational gaps. (`llm-arxiv-2510-22344v1-2`)

## Evidence Ledger

| Evidence ID | Paper ID | Category | Confidence | Support Text |
| --- | --- | --- | ---: | --- |
| `llm-arxiv-2411-19443v1-1` | `arxiv:2411.19443v1` | contribution | 0.65 | we introduce Auto-RAG, an autonomous iterative retrieval model centered on the LLM's powerful decision-making capabilities. |
| `llm-arxiv-2411-19443v1-2` | `arxiv:2411.19443v1` | experiment | 0.65 | The experimental results indicate that Auto-RAG ... lead to outstanding performance across six benchmarks. |
| `llm-arxiv-2503-16581v1-1` | `arxiv:2503.16581v1` | contribution | 0.65 | In this study, we investigate 13 open-source LLMs categorized into large, medium, and small. |
| `llm-arxiv-2503-16581v1-2` | `arxiv:2503.16581v1` | experiment | 0.65 | The findings reveal that large models consistently outperform smaller models in capturing query semantics and producing accurate, contextually grounded responses. |
| `llm-arxiv-2503-16581v1-3` | `arxiv:2503.16581v1` | limitation | 0.65 | General-purpose LLMs often struggle with hallucinations, where generated responses deviate from authoritative sources, raising concerns about their reliability in religious contexts. |
| `llm-arxiv-2401-15391v1-1` | `arxiv:2401.15391v1` | contribution | 0.65 | we develop a novel dataset, MultiHop-RAG, which consists of a knowledge base, a large collection of multi-hop queries, their ground-truth answers, and the associated supporting evidence. |
| `llm-arxiv-2401-15391v1-2` | `arxiv:2401.15391v1` | experiment | 0.65 | Both experiments reveal that existing RAG methods perform unsatisfactorily in retrieving and answering multi-hop queries. |
| `llm-arxiv-2401-15391v1-3` | `arxiv:2401.15391v1` | future_work | 0.65 | We hope MultiHop-RAG will be a valuable resource for the community in developing effective RAG systems, thereby facilitating greater adoption of LLMs in practice. |
| `llm-arxiv-2501-09136v4-1` | `arxiv:2501.09136v4` | contribution | 0.65 | This paper presents an analytical survey of Agentic RAG systems. It traces the evolution of RAG paradigms, introduces a principled taxonomy of Agentic RAG architectures. |
| `llm-arxiv-2501-09136v4-2` | `arxiv:2501.09136v4` | future_work | 0.65 | it identifies key open research challenges related to evaluation, coordination, memory management, efficiency, and governance, outlining directions for future research. |
| `llm-arxiv-2602-08545v1-1` | `arxiv:2602.08545v1` | method | 0.65 | Thus, we propose DA-RAG, which leverages attributed community search (ACS) to extract relevant subgraphs based on the queried question dynamically. |
| `llm-arxiv-2602-08545v1-2` | `arxiv:2602.08545v1` | method | 0.65 | DA-RAG captures high-order graph structures, allowing for the retrieval of self-complementary knowledge. |
| `llm-arxiv-2602-08545v1-3` | `arxiv:2602.08545v1` | experiment | 0.65 | We evaluate DA-RAG on multiple datasets, demonstrating that it outperforms existing RAG methods by up to 40% in head-to-head comparisons across four metrics |
| `llm-arxiv-2602-08545v1-4` | `arxiv:2602.08545v1` | experiment | 0.65 | while reducing index construction time and token overhead by up to 37% and 41%, respectively. |
| `llm-arxiv-2602-08545v1-5` | `arxiv:2602.08545v1` | limitation | 0.65 | However, current G-RAG methodologies frequently underutilize graph topology, predominantly focusing on low-order structures or pre-computed static communities. |
| `llm-arxiv-2603-26668v2-1` | `arxiv:2603.26668v2` | contribution | 0.65 | To overcome the accuracy challenge, we introduce the concept of abstract to bridge query entities and document chunks, providing robust semantic understanding. |
| `llm-arxiv-2603-26668v2-2` | `arxiv:2603.26668v2` | method | 0.65 | We organize the abstracts into a tree structure and design a multi-level retrieval strategy to ensure the inclusion of sufficient contextual information. |
| `llm-arxiv-2603-26668v2-3` | `arxiv:2603.26668v2` | method | 0.65 | To restore retrieval efficiency, we further integrate the Cuckoo Filter in CFT-RAG, which provides O(1) entity lookup |
| `llm-arxiv-2603-26668v2-4` | `arxiv:2603.26668v2` | experiment | 0.65 | Extensive experiments show that Bridge-RAG achieves consistent accuracy improvements across all metrics and up to $1.9\times$ faster retrieval compared to structured RAG baselines. |
| `llm-arxiv-2510-22344v1-1` | `arxiv:2510.22344v1` | contribution | 0.65 | We introduce FAIR-RAG, a novel agentic framework that transforms the standard RAG pipeline into a dynamic, evidence-driven reasoning process. |
| `llm-arxiv-2510-22344v1-2` | `arxiv:2510.22344v1` | method | 0.65 | At its core is an Iterative Refinement Cycle governed by a module we term Structured Evidence Assessment (SEA). ... it deconstructs the initial query into a checklist of required findings and audits the aggregated evidence to identify confirmed facts and, critically, explicit... |
| `llm-arxiv-2510-22344v1-3` | `arxiv:2510.22344v1` | experiment | 0.65 | On HotpotQA, it achieves an F1-score of 0.453 -- an absolute improvement of 8.3 points over the strongest iterative baseline |
| `llm-arxiv-2510-22344v1-4` | `arxiv:2510.22344v1` | limitation | 0.65 | Current advanced RAG methods, employing iterative or adaptive strategies, lack a robust mechanism to systematically identify and fill evidence gaps, often propagating noise or failing to gather a comprehensive context. |
| `llm-arxiv-2501-03995v1-1` | `arxiv:2501.03995v1` | contribution | 0.65 | To address this, we propose a novel framework to evaluate the reliability of multi-modal RAG using two performance measures: (i) the relevancy score (RS), assessing the relevance of retrieved entries to the query, and (ii) the correctness score (CS), evaluating the accuracy of... |
| `llm-arxiv-2501-03995v1-2` | `arxiv:2501.03995v1` | experiment | 0.65 | Results show that both models achieve ~88% accuracy on test data. |
| `llm-arxiv-2501-03995v1-3` | `arxiv:2501.03995v1` | experiment | 0.65 | Our RS model aligns with human preferences 20% more often than CLIP in retrieval |
| `llm-arxiv-2501-03995v1-4` | `arxiv:2501.03995v1` | limitation | 0.65 | However, RAG, particularly multi-modal RAG, can introduce new hallucination sources: (i) the retrieval process may select irrelevant pieces ... and (ii) retrieved images are processed ... which may hallucinate. |
| `llm-arxiv-2604-18509v2-1` | `arxiv:2604.18509v2` | contribution | 0.65 | We propose MASS-RAG, a multi-agent synthesis approach to retrieval-augmented generation that structures evidence processing into multiple role-specialized agents. |
| `llm-arxiv-2604-18509v2-2` | `arxiv:2604.18509v2` | method | 0.65 | MASS-RAG applies distinct agents for evidence summarization, evidence extraction, and reasoning over retrieved documents |
| `llm-arxiv-2604-18509v2-3` | `arxiv:2604.18509v2` | method | 0.65 | This design exposes multiple intermediate evidence views, allowing the model to compare and integrate complementary information before answer generation. |
| `llm-arxiv-2604-18509v2-4` | `arxiv:2604.18509v2` | experiment | 0.65 | Experiments on four benchmarks show that MASS-RAG consistently improves performance over strong RAG baselines, particularly in settings where relevant evidence is distributed across retrieved contexts. |
| `llm-arxiv-2604-18509v2-5` | `arxiv:2604.18509v2` | limitation | 0.65 | However, when retrieved contexts are noisy, incomplete, or heterogeneous, a single generation process often struggles to reconcile evidence effectively. |
| `llm-arxiv-2605-24366v1-1` | `arxiv:2605.24366v1` | contribution | 0.65 | We propose Structure-aware Retrieval Augmented Generation (SA-RAG), which uses tables as an intermediate structured representation to provide a compact and controllable interface that reduces noise while preserving essential information. |
| `llm-arxiv-2605-24366v1-2` | `arxiv:2605.24366v1` | method | 0.65 | We introduce a quality-aware table metadata generation framework that models metadata normalization and effectiveness, improving metadata quality and downstream performance. |
| `llm-arxiv-2605-24366v1-3` | `arxiv:2605.24366v1` | experiment | 0.65 | Experiments on two noisy real-world datasets show that SA-RAG significantly outperforms existing RAG baselines. |
| `llm-arxiv-2605-27432v1-1` | `arxiv:2605.27432v1` | contribution | 0.65 | We propose FD-RAG, a federated dual-system RAG framework that decouples lightweight memory access from on-demand LLM reasoning for decentralized deployment. |
| `llm-arxiv-2605-27432v1-2` | `arxiv:2605.27432v1` | method | 0.65 | FD-RAG learns semantic-aware adaptive hypergraphs over local corpora and distills them into compact QA memories. |
| `llm-arxiv-2605-27432v1-3` | `arxiv:2605.27432v1` | experiment | 0.65 | Experiments on QA benchmarks show that FD-RAG improves accuracy by up to 7.8\% while reducing latency by 8.4$\times$ compared with strong local and federated baselines. |
| `llm-arxiv-2603-08329v1-1` | `arxiv:2603.08329v1` | contribution | 0.65 | We introduce SPD-RAG, a hierarchical multi-agent framework for exhaustive cross-document question answering that decomposes the problem along the document axis. |
| `llm-arxiv-2603-08329v1-2` | `arxiv:2603.08329v1` | method | 0.65 | Each document is processed by a dedicated document-level agent operating only on its own content, enabling focused retrieval, while a coordinator dispatches tasks to relevant agents and aggregates their partial answers. |
| `llm-arxiv-2603-08329v1-3` | `arxiv:2603.08329v1` | experiment | 0.65 | On the LOONG benchmark (EMNLP 2024) for long-context multi-document QA, SPD-RAG achieves an Avg Score of 58.1 (GPT-5 evaluation), outperforming Normal RAG (33.0) and Agentic RAG (32.8) while using only 38% of the API cost of a full-context baseline (68.0). |
| `llm-arxiv-2502-01113v3-1` | `arxiv:2502.01113v3` | contribution | 0.65 | We introduce GFM-RAG, a novel graph foundation model (GFM) for retrieval augmented generation. ... making it the first graph foundation model applicable to unseen datasets for retrieval without any fine-tuning required. |
| `llm-arxiv-2502-01113v3-2` | `arxiv:2502.01113v3` | method | 0.65 | GFM-RAG is powered by an innovative graph neural network that reasons over graph structure to capture complex query-knowledge relationships. |
| `llm-arxiv-2502-01113v3-3` | `arxiv:2502.01113v3` | experiment | 0.65 | Extensive experiments on three multi-hop QA datasets and seven domain-specific RAG datasets demonstrate that GFM-RAG achieves state-of-the-art performance while maintaining efficiency and alignment with neural scaling laws. |
| `llm-arxiv-2507-13396v1-1` | `arxiv:2507.13396v1` | contribution | 0.65 | We introduce DyG-RAG, a novel event-centric dynamic graph retrieval-augmented generation framework designed to capture and reason over temporal knowledge embedded in unstructured text. |
| `llm-arxiv-2507-13396v1-2` | `arxiv:2507.13396v1` | method | 0.65 | DyG-RAG proposes Dynamic Event Units (DEUs) that explicitly encode both semantic content and precise temporal anchors, enabling accurate and interpretable time-aware retrieval. |
| `llm-arxiv-2507-13396v1-3` | `arxiv:2507.13396v1` | experiment | 0.65 | Extensive experiments on temporal QA benchmarks demonstrate that DyG-RAG significantly improves the accuracy and recall of three typical types of temporal reasoning questions. |
| `llm-arxiv-2508-05650v1-1` | `arxiv:2508.05650v1` | contribution | 0.65 | We introduce OmniBench RAG, a novel automated platform for multi domain evaluation of RAG systems. The platform quantifies performance gains across accuracy and efficiency dimensions, spanning nine knowledge fields including culture, geography, and health. |
| `llm-arxiv-2508-05650v1-2` | `arxiv:2508.05650v1` | method | 0.65 | We introduce two standardized metrics: Improvements (accuracy gains) and Transformation (efficiency differences between pre RAG and post RAG models), enabling reproducible comparisons across models and tasks. |
| `llm-arxiv-2508-05650v1-3` | `arxiv:2508.05650v1` | experiment | 0.65 | Our evaluation reveals striking variability in RAG effectiveness, from significant gains in culture to declines in mathematics, highlighting the critical importance of systematic, domain aware assessment. |
| `llm-arxiv-2508-05650v1-4` | `arxiv:2508.05650v1` | limitation | 0.65 | Existing methods often fall short: they lack domain coverage, employ coarse metrics that miss sub document precision, and fail to capture computational trade offs. |

## 5. Comparative Analysis

| Paper | Main Evidence | Confidence |
| --- | --- | --- |
| Auto-RAG: Autonomous Retrieval-Augmented Generation for Large Language Models | Auto-RAG is an autonomous iterative retrieval model that leverages LLM's decision-making to iteratively interact with the retriever. | 0.65 |
| Investigating Retrieval-Augmented Generation in Quranic Studies: A Study of 13 Open-Source Large Language Models | Investigates 13 open-source LLMs with RAG for Quranic studies. | 0.65 |
| MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries | Develops MultiHop-RAG, a benchmark dataset for multi-hop queries in RAG. | 0.65 |
| Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG | Provides a comprehensive survey and taxonomy of Agentic RAG systems. | 0.65 |
| DA-RAG: Dynamic Attributed Community Search for Retrieval-Augmented Generation | DA-RAG uses attributed community search to dynamically extract relevant subgraphs based on the query. | 0.65 |
| Bridge-RAG: An Abstract Bridge Tree Based Retrieval Augmented Generation Algorithm | Bridge-RAG introduces abstract to bridge query entities and document chunks. | 0.65 |
| FAIR-RAG: Faithful Adaptive Iterative Refinement for Retrieval-Augmented Generation | FAIR-RAG transforms the standard RAG pipeline into a dynamic, evidence-driven reasoning process. | 0.65 |
| RAG-Check: Evaluating Multimodal Retrieval Augmented Generation Performance | RAG-Check is a framework to evaluate the reliability of multi-modal RAG using relevancy and correctness scores. | 0.65 |
| MASS-RAG: Multi-Agent Synthesis Retrieval-Augmented Generation | MASS-RAG is a multi-agent synthesis approach that structures evidence processing into specialized agents. | 0.65 |
| Structure-Aware RAG: Structured Retrieval Augmented Generation from Noisy Data for Conversational Agents | SA-RAG uses tables as an intermediate structured representation to reduce noise while preserving essential information. | 0.65 |
| FD-RAG: Federated Dual-System Retrieval-Augmented Generation | FD-RAG is a federated dual-system RAG framework that decouples memory access from LLM reasoning. | 0.65 |
| SPD-RAG: Sub-Agent Per Document Retrieval-Augmented Generation | SPD-RAG is a hierarchical multi-agent framework for exhaustive cross-document QA. | 0.65 |
| GFM-RAG: Graph Foundation Model for Retrieval Augmented Generation | GFM-RAG is the first graph foundation model for RAG applicable to unseen datasets without fine-tuning. | 0.65 |
| DyG-RAG: Dynamic Graph Retrieval-Augmented Generation with Event-Centric Reasoning | DyG-RAG is an event-centric dynamic graph RAG framework for temporal reasoning. | 0.65 |
| OmniBench-RAG: A Multi-Domain Evaluation Platform for Retrieval-Augmented Generation Tools | The platform quantifies performance gains across accuracy and efficiency dimensions, spanning nine knowledge fields including culture, geography, and health. | 0.65 |

## 6. Research Gaps

- A promising research gap is to make the literature review process auditable through claim-evidence alignment and citation checking. Evidence: `llm-arxiv-2503-16581v1-3`, `llm-arxiv-2401-15391v1-3`, `llm-arxiv-2501-09136v4-2`

## 7. Limitations of This Automated Review

- MVP mode may rely on metadata and abstracts rather than full paper text.
- Offline fixture mode is deterministic and intended for demo stability.
- Citation checks validate metadata availability, not peer-review quality.

## Citation Checks

| Check ID | Paper ID | Status | Message |
| --- | --- | --- | --- |
| `check-1` | `arxiv:2411.19443v1` | passed | Citation metadata is available. |
| `check-2` | `arxiv:2503.16581v1` | passed | Citation metadata is available. |
| `check-3` | `arxiv:2401.15391v1` | passed | Citation metadata is available. |
| `check-4` | `arxiv:2501.09136v4` | passed | Citation metadata is available. |
| `check-5` | `arxiv:2602.08545v1` | passed | Citation metadata is available. |
| `check-6` | `arxiv:2603.26668v2` | passed | Citation metadata is available. |
| `check-7` | `arxiv:2510.22344v1` | passed | Citation metadata is available. |
| `check-8` | `arxiv:2501.03995v1` | passed | Citation metadata is available. |
| `check-9` | `arxiv:2604.18509v2` | passed | Citation metadata is available. |
| `check-10` | `arxiv:2605.24366v1` | passed | Citation metadata is available. |
| `check-11` | `arxiv:2605.27432v1` | passed | Citation metadata is available. |
| `check-12` | `arxiv:2603.08329v1` | passed | Citation metadata is available. |
| `check-13` | `arxiv:2502.01113v3` | passed | Citation metadata is available. |
| `check-14` | `arxiv:2507.13396v1` | passed | Citation metadata is available. |
| `check-15` | `arxiv:2508.05650v1` | passed | Citation metadata is available. |

## References

[P1] Tian Yu, Shaolei Zhang, Yang Feng. (2024). Auto-RAG: Autonomous Retrieval-Augmented Generation for Large Language Models. http://arxiv.org/abs/2411.19443v1
[P2] Zahra Khalila, Arbi Haza Nasution, Winda Monika, Aytug Onan, Yohei Murakami, Yasir Bin Ismail Radi, Noor Mohammad Osmani. (2025). Investigating Retrieval-Augmented Generation in Quranic Studies: A Study of 13 Open-Source Large Language Models. http://arxiv.org/abs/2503.16581v1
[P3] Yixuan Tang, Yi Yang. (2024). MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries. http://arxiv.org/abs/2401.15391v1
[P4] Aditi Singh, Abul Ehtesham, Saket Kumar, Tala Talaei Khoei, Athanasios V. Vasilakos. (2025). Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG. http://arxiv.org/abs/2501.09136v4
[P5] Xingyuan Zeng, Zuohan Wu, Yue Wang, Chen Zhang, Quanming Yao, Libin Zheng, Jian Yin. (2026). DA-RAG: Dynamic Attributed Community Search for Retrieval-Augmented Generation. http://arxiv.org/abs/2602.08545v1
[P6] Zihang Li, Wenjun Liu, Yikun Zong, Jiawen Tao, Siying Dai, Songcheng Ren, Zirui Liu, Yuhang Wang, Yanbing Jiang, Tong Yang. (2026). Bridge-RAG: An Abstract Bridge Tree Based Retrieval Augmented Generation Algorithm. http://arxiv.org/abs/2603.26668v2
[P7] Mohammad Aghajani Asl, Majid Asgari-Bidhendi, Behrooz Minaei-Bidgoli. (2025). FAIR-RAG: Faithful Adaptive Iterative Refinement for Retrieval-Augmented Generation. http://arxiv.org/abs/2510.22344v1
[P8] Matin Mortaheb, Mohammad A. Amir Khojastepour, Srimat T. Chakradhar, Sennur Ulukus. (2025). RAG-Check: Evaluating Multimodal Retrieval Augmented Generation Performance. http://arxiv.org/abs/2501.03995v1
[P9] Xingchen Xiao, Heyan Huang, Runheng Liu, Jincheng Xie. (2026). MASS-RAG: Multi-Agent Synthesis Retrieval-Augmented Generation. http://arxiv.org/abs/2604.18509v2
[P10] Kaiqiao Han, LuAn Tang, Renliang Sun, Peng Yuan, Wei Cheng, Haoyu Wang, Wei Wang, Yizhou Sun, Haifeng Chen. (2026). Structure-Aware RAG: Structured Retrieval Augmented Generation from Noisy Data for Conversational Agents. http://arxiv.org/abs/2605.24366v1
[P11] Tianhao Gao, Kai Yang, Yiyang Li. (2026). FD-RAG: Federated Dual-System Retrieval-Augmented Generation. http://arxiv.org/abs/2605.27432v1
[P12] Yagiz Can Akay, Muhammed Yusuf Kartal, Esra Alparslan, Faruk Ortakoyluoglu, Arda Akpinar. (2026). SPD-RAG: Sub-Agent Per Document Retrieval-Augmented Generation. http://arxiv.org/abs/2603.08329v1
[P13] Linhao Luo, Zicheng Zhao, Gholamreza Haffari, Dinh Phung, Chen Gong, Shirui Pan. (2025). GFM-RAG: Graph Foundation Model for Retrieval Augmented Generation. http://arxiv.org/abs/2502.01113v3
[P14] Qingyun Sun, Jiaqi Yuan, Shan He, Xiao Guan, Haonan Yuan, Xingcheng Fu, Jianxin Li, Philip S. Yu. (2025). DyG-RAG: Dynamic Graph Retrieval-Augmented Generation with Event-Centric Reasoning. http://arxiv.org/abs/2507.13396v1
[P15] Jiaxuan Liang, Shide Zhou, Kailong Wang. (2025). OmniBench-RAG: A Multi-Domain Evaluation Platform for Retrieval-Augmented Generation Tools. http://arxiv.org/abs/2508.05650v1
