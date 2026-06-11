# Literature Review: Retrieval-Augmented Generation (RAG) in NLP: Methodologies, Applications, and Evaluation

## Executive Summary

ResearchFlow generated this literature review on 2026-06-11 15:34 UTC. The agent searched `arxiv+crossref` sources, selected 12 core papers, extracted 30 evidence items, and linked 2 synthesis claims back to retrieved sources.

Selected source coverage: arxiv, crossref. LLM mode: deepseek; LLM used: true.

Fallback note: Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: 

## Search Method and Scope

The agent follows a traceable workflow: query planning, live paper search, ranking, evidence extraction, claim synthesis, citation checking, and report writing.

| Query ID | Search Query | Source Intent | Angle | Distance |
| --- | --- | --- | --- | --- |
| `q1` | Retrieval-Augmented Generation (RAG) in NLP: Methodologies, Applications, and Evaluation | hybrid | core | direct |
| `q2` | retrieval-augmented generation rag nlp methodologies applications survey taxonomy | hybrid | survey_taxonomy | direct |
| `q3` | retrieval-augmented generation rag nlp methodologies applications methods systems architecture | hybrid | methods_systems | direct |
| `q4` | retrieval-augmented generation rag nlp methodologies applications evaluation benchmark dataset | hybrid | evaluation_benchmark | direct |
| `q5` | retrieval-augmented generation rag nlp methodologies applications challenges limitations open problems | hybrid | limitations_challenges | direct |
| `q6` | retrieval-augmented generation rag nlp methodologies applications applications case studies | hybrid | applications_domains | adjacent |
| `q7` | retrieval-augmented generation rag nlp methodologies applications security robustness hallucination | hybrid | security_robustness | adjacent |
| `q8` | Retrieval-Augmented Generation survey | hybrid | llm_hint | adjacent |
| `q9` | RAG evaluation benchmarks | hybrid | llm_hint | adjacent |
| `q10` | dense retrieval vs sparse retrieval RAG | hybrid | llm_hint | adjacent |

## 1. Research Background

Retrieval-Augmented Generation (RAG) has emerged as a prominent paradigm to enhance large language models (LLMs) by integrating external knowledge retrieval, addressing issues such as hallucination and outdated knowledge. RAG systems combine a retriever that fetches relevant documents from a knowledge base with a generator that produces responses conditioned on the retrieved context. Recent advancements have explored various architectures, including agentic RAG with autonomous agents for dynamic retrieval and multi-hop reasoning, as well as domain-specific applications in education, healthcare, fintech, and space operations. Evaluation of RAG systems focuses on accuracy, reliability, and efficiency, with benchmarks like MultiHop-RAG and OmniBench-RAG highlighting challenges in multi-hop queries and domain variability. Despite progress, issues remain in retrieval precision, latency, and adaptability to complex tasks, motivating further research into robust and scalable RAG frameworks.

## 2. Core Papers

### P1. Building a Security and Reliability Evaluation Suite for Retrieval-Augmented Generation (RAG) Systems

- Authors: Pronoy Roy, Debayan Roy
- Year: 2025
- Source: crossref
- URL: https://doi.org/10.20944/preprints202510.0418.v2
- Citations: 0
- Citation check: passed
- Summary: Retrieval-Augmented Generation (RAG) enables large language models (LLMs) to produce domain-aware, up-to-date answers by conditioning on retrieved evidence. However, the additional retrieval stage introduces new failure modes, hence, evaluating security and reliability in Retrieval-Augmented Generation (RAG) systems is critical to deploying trustworthy applications. In this paper, we present Secure-RAG, a modular, security-first evaluation suite for multi-dimensional assessment of RAG systems, including factual accuracy, hallucination avoidance, adversarial robustness, bias and fairness, toxicity, security, and calibration. Secure-RAG instruments each stage (query, retrieval, generation) with lightweight monitors that compute standardized metrics. In an illustrative evaluation, we demonstrate Secure-RAG improves reliability without sacrificing utility. Secure-RAG’s integrated perspective security-utility tradeoffs that siloed tools often miss, and offers a practical template for continuous evaluation of RAG systems in risk-sensitive settings.

### P2. Development and Evaluation of a Chatbot to Support Pre-Mission Planning in a Launch and Re-entry Coordination Center Using Retrieval-Augmented Generation (RAG)

- Authors: Jens Hampe
- Year: 2026
- Source: crossref
- URL: https://doi.org/10.21203/rs.3.rs-9427085/v1
- Citations: 0
- Citation check: passed
- Summary: Abstract The growing number of orbital launch and re-entry operations demands precise and well-coordinated planning, particularly by institutions such as a Launch and Re-entry Coordination Center. In the pre-mission phase, fast and reliable access to mission-critical knowledge is essential to ensure safe and efficient coordination. This work presents the development of an AI-based chatbot that supports planning activities by providing relevant information on demand. The chatbot utilizes Retrieval-Augmented Generation (RAG), a technique that combines generative language models with document-based information retrieval. This allows for the generation of context-specific responses grounded in domain-specific resources such as coordination procedures, mission documentation, and regulatory requirements. The technical implementation is based on a modular RAG stack consisting of a vector database, retriever, and Lage Language Model (LLM) component. The evaluation focuses on system architecture, response quality, context relevance, and user acceptance. Initial tests in a simulated coordination environment indicate that the chatbot can reliably answer typical pre-mission planning queries, contributing to more efficient workflows and error reduction. The results highlight the potential of LLM-based assistance systems in safety-critical space coordination tasks and provide a basis for further automation in mission planning and operational support.

### P3. Retrieval-Augmented Generation (RAG) Chatbots for Education: A Survey of Applications

- Authors: Jakub Swacha, Michał Gracel
- Year: 2025
- Source: crossref
- URL: https://doi.org/10.3390/app15084234
- Citations: 74
- Citation check: passed
- Summary: Retrieval-Augmented Generation (RAG) overcomes the main barrier for the adoption of LLM-based chatbots in education: hallucinations. The uncomplicated architecture of RAG chatbots makes it relatively easy to implement chatbots that serve specific purposes and thus are capable of addressing various needs in the educational domain. With five years having passed since the introduction of RAG, the time has come to check the progress attained in its adoption in education. This paper identifies 47 papers dedicated to RAG chatbots’ uses for various kinds of educational purposes, which are analyzed in terms of their character, the target of the support provided by the chatbots, the thematic scope of the knowledge accessible via the chatbots, the underlying large language model, and the character of their evaluation.

### P4. To RAG, or Not to RAG? A Comparative Evaluation of Retrieval-Augmented Generation for ICD Coding of German Tumor Diagnoses

- Authors: Fatma Alickovic, Stefan Lenz, Arsenij Ustjanzew, Lakisha Ortiz Rosario, Georg Vollmar, Thomas Kindler, Torsten Panholzer
- Year: 2026
- Source: crossref
- URL: https://doi.org/10.64898/2026.05.27.26353695
- Citations: 0
- Citation check: passed
- Summary: Abstract Introduction Coding tumor diagnoses from free-text clinical documentation currently requires substantial manual effort. Promising approaches for automating this process include large language models (LLMs), embedding models, and retrieval-augmented generation (RAG). While previous studies often focus on a single method, we directly compare these approaches on a real-world dataset of tumor diagnosis descriptions to assess their strengths and limitations. Methods We evaluated nine different embedding models using similarity search and embedding-based classification, as well as LLM-based coding, with and without RAG, on a real-world dataset of 2,024 unique German tumor diagnosis descriptions labeled with ICD-10 and ICD-O topography codes. The retrieval knowledge base was constructed exclusively from standardized Alpha-ID, ICD-10-GM, and ICD-O-3 classifications. Performance was assessed for exact (full-code) and partial (three-character) code prediction. For RAG, we evaluated base and fine-tuned versions of Llama 3.1 8B and Llama 3.3 70B. Results Qwen3-Embedding-8B, the largest embedding model, yielded the best results. It achieved 47.8% exact-match and 72.1% partial-match accuracy for ICD-10 coding with classification, and 42.7% exact-match and 73.5% partial-match accuracy for ICD-O coding with similarity search. The other embedding models, including medically specialized ones, showed varied but lower performance. RAG improved base LLM performance and outperformed embedding-based approaches on partial-match accuracy (80.6% partial-match accuracy for ICD-10 and 75.0% for ICD-O with Llama 3.3 70B), but not on exact-match accuracy. Conclusion A direct comparison with embedding-based approaches is essential to determine whether the additional effort of RAG is justified. The strong variation in performance also highlights the importance of model selection. Further advances in embedding-based methods, potentially supported by larger and more diverse training data, may offer a promising direction for future work.

### P5. OmniBench-RAG: A Multi-Domain Evaluation Platform for Retrieval-Augmented Generation Tools

- Authors: Jiaxuan Liang, Shide Zhou, Kailong Wang
- Year: 2025
- Source: arxiv
- URL: http://arxiv.org/abs/2508.05650v1
- Citations: 0
- Citation check: passed
- Summary: While Retrieval Augmented Generation (RAG) is now widely adopted to enhance LLMs, evaluating its true performance benefits in a reproducible and interpretable way remains a major hurdle. Existing methods often fall short: they lack domain coverage, employ coarse metrics that miss sub document precision, and fail to capture computational trade offs. Most critically, they provide no standardized framework for comparing RAG effectiveness across different models and domains. We introduce OmniBench RAG, a novel automated platform for multi domain evaluation of RAG systems. The platform quantifies performance gains across accuracy and efficiency dimensions, spanning nine knowledge fields including culture, geography, and health. We introduce two standardized metrics: Improvements (accuracy gains) and Transformation (efficiency differences between pre RAG and post RAG models), enabling reproducible comparisons across models and tasks. The platform features dynamic test generation, modular evaluation pipelines, and automated knowledge base construction. Our evaluation reveals striking variability in RAG effectiveness, from significant gains in culture to declines in mathematics, highlighting the critical importance of systematic, domain aware assessment. A demonstration video is available at: https://www.youtube.com/watch?v=BZx83QFcTCI. Code and datasets: https://github.com/Garnett-Liang/Omnibench-RAG.

### P6. Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG

- Authors: Aditi Singh, Abul Ehtesham, Saket Kumar, Tala Talaei Khoei, Athanasios V. Vasilakos
- Year: 2025
- Source: arxiv
- URL: http://arxiv.org/abs/2501.09136v4
- Citations: 0
- Citation check: passed
- Summary: Large Language Models (LLMs) have advanced artificial intelligence by enabling human-like text generation and natural language understanding. However, their reliance on static training data limits their ability to respond to dynamic, real-time queries, resulting in outdated or inaccurate outputs. Retrieval-Augmented Generation (RAG) has emerged as a solution, enhancing LLMs by integrating real-time data retrieval to provide contextually relevant and up-to-date responses. Despite its promise, traditional RAG systems are constrained by static workflows and lack the adaptability required for multi-step reasoning and complex task management. Agentic Retrieval-Augmented Generation (Agentic RAG) transcends these limitations by embedding autonomous AI agents into the RAG pipeline. These agents leverage agentic design patterns reflection, planning, tool use, and multi-agent collaboration to dynamically manage retrieval strategies, iteratively refine contextual understanding, and adapt workflows through operational structures ranging from sequential steps to adaptive collaboration. This integration enables Agentic RAG systems to deliver flexibility, scalability, and context-awareness across diverse applications. This paper presents an analytical survey of Agentic RAG systems. It traces the evolution of RAG paradigms, introduces a principled taxonomy of Agentic RAG architectures based on agent cardinality, control structure, autonomy, and knowledge representation, and provides a comparative analysis of design trade-offs across existing frameworks. The survey examines applications in healthcare, finance, education, and enterprise document processing, and distills practical lessons for system designers and practitioners. Finally, it identifies key open research challenges related to evaluation, coordination, memory management, efficiency, and governance, outlining directions for future research.

### P7. MedRAG: Retrieval-Augmented Generation for Medical QA-Comparing Base and RAG-Augmented LLM Performance on Evidence from Peer-Reviewed Clinical Research

- Authors: Kunal Dhanda
- Year: 2026
- Source: crossref
- URL: https://doi.org/10.2139/ssrn.6608518
- Citations: 0
- Citation check: passed
- Summary: Large language models (LLMs) deployed for medical question answering must provide precise, evidencegrounded responses-yet their parametric knowledge frequently fails on specific quantitative findings from recent clinical trials and systematic reviews. We build a medical retrieval-augmented generation (MedRAG) system by indexing 5025 peer-reviewed papers across 104 clinical domains-retrieved via PubMed and the Consensus academic search engine, embedded using sentence-transformers, and stored in a ChromaDB vector database. We evaluate a local LLaMA 3.2 base model against its RAG-augmented counterpart on 25 medical QA questions stratified by domain and difficulty. The base model achieves 0.760 accuracy while the RAG-augmented system achieves 1.000, a gain of 24 percentage points. Qualitative analysis of the 6 base-model failures reveals two distinct hallucination patterns: (i) fabrication, where the model invents specific trial names, authors, and effect sizes with confident language; and (ii) confident substitution, where the model returns plausible but numerically wrong statistics. RAG eliminates both patterns by grounding responses in retrieved evidence. Mean gold-keyword hit rate improves from 2.36 to 4.20 keywords per question. These results demonstrate that lightweight RAG over curated clinical literature substantially improves LLM factual accuracy for medical QA on consumer hardware.

### P8. Engineering the RAG Stack: A Comprehensive Review of the Architecture and Trust Frameworks for Retrieval-Augmented Generation Systems

- Authors: Dean Wampler, Dave Nielson, Alireza Seddighi
- Year: 2025
- Source: arxiv
- URL: http://arxiv.org/abs/2601.05264v1
- Citations: 0
- Citation check: passed
- Summary: This article provides a comprehensive systematic literature review of academic studies, industrial applications, and real-world deployments from 2018 to 2025, providing a practical guide and detailed overview of modern Retrieval-Augmented Generation (RAG) architectures. RAG offers a modular approach for integrating external knowledge without increasing the capacity of the model as LLM systems expand. Research and engineering practices have been fragmented as a result of the increasing diversity of RAG methodologies, which encompasses a variety of fusion mechanisms, retrieval strategies, and orchestration approaches. We provide quantitative assessment frameworks, analyze the implications for trust and alignment, and systematically consolidate existing RAG techniques into a unified taxonomy. This document is a practical framework for the deployment of resilient, secure, and domain-adaptable RAG systems, synthesizing insights from academic literature, industry reports, and technical implementation guides. It also functions as a technical reference.

### P9. Retrieval Augmented Generation (RAG) for Fintech: Agentic Design and Evaluation

- Authors: Thomas Cook, Richard Osuagwu, Liman Tsatiashvili, Vrynsia Vrynsia, Koustav Ghosal, Maraim Masoud, Riccardo Mattivi
- Year: 2025
- Source: arxiv
- URL: http://arxiv.org/abs/2510.25518v1
- Citations: 0
- Citation check: passed
- Summary: Retrieval-Augmented Generation (RAG) systems often face limitations in specialized domains such as fintech, where domain-specific ontologies, dense terminology, and acronyms complicate effective retrieval and synthesis. This paper introduces an agentic RAG architecture designed to address these challenges through a modular pipeline of specialized agents. The proposed system supports intelligent query reformulation, iterative sub-query decomposition guided by keyphrase extraction, contextual acronym resolution, and cross-encoder-based context re-ranking. We evaluate our approach against a standard RAG baseline using a curated dataset of 85 question--answer--reference triples derived from an enterprise fintech knowledge base. Experimental results demonstrate that the agentic RAG system outperforms the baseline in retrieval precision and relevance, albeit with increased latency. These findings suggest that structured, multi-agent methodologies offer a promising direction for enhancing retrieval robustness in complex, domain-specific settings.

### P10. MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries

- Authors: Yixuan Tang, Yi Yang
- Year: 2024
- Source: arxiv
- URL: http://arxiv.org/abs/2401.15391v1
- Citations: 0
- Citation check: passed
- Summary: Retrieval-augmented generation (RAG) augments large language models (LLM) by retrieving relevant knowledge, showing promising potential in mitigating LLM hallucinations and enhancing response quality, thereby facilitating the great adoption of LLMs in practice. However, we find that existing RAG systems are inadequate in answering multi-hop queries, which require retrieving and reasoning over multiple pieces of supporting evidence. Furthermore, to our knowledge, no existing RAG benchmarking dataset focuses on multi-hop queries. In this paper, we develop a novel dataset, MultiHop-RAG, which consists of a knowledge base, a large collection of multi-hop queries, their ground-truth answers, and the associated supporting evidence. We detail the procedure of building the dataset, utilizing an English news article dataset as the underlying RAG knowledge base. We demonstrate the benchmarking utility of MultiHop-RAG in two experiments. The first experiment compares different embedding models for retrieving evidence for multi-hop queries. In the second experiment, we examine the capabilities of various state-of-the-art LLMs, including GPT-4, PaLM, and Llama2-70B, in reasoning and answering multi-hop queries given the evidence. Both experiments reveal that existing RAG methods perform unsatisfactorily in retrieving and answering multi-hop queries. We hope MultiHop-RAG will be a valuable resource for the community in developing effective RAG systems, thereby facilitating greater adoption of LLMs in practice. The MultiHop-RAG and implemented RAG system is publicly available at https://github.com/yixuantt/MultiHop-RAG/.

### P11. ENHANCING KNOWLEDGE-INTENSIVE CUSTOMER SUPPORT IN REGULATED INDUSTRIES THROUGH RETRIEVAL-AUGMENTED GENERATION (RAG): ARCHITECTURE, ALGORITHMS, AND EMPIRICAL EVALUATION

- Authors: Ramesh Chandra Aditya Komperla
- Year: 2026
- Source: crossref
- URL: https://doi.org/10.34218/ijaiap_05_01_001
- Citations: 0
- Citation check: passed
- Summary: Crossref metadata record for journal article published in INTERNATIONAL JOURNAL OF ARTIFICIAL INTELLIGENCE &amp; APPLICATIONS. Abstract is not available in this metadata response.

### P12. RAG-Fusion: a New Take on Retrieval-Augmented Generation

- Authors: Zackary Rackauckas
- Year: 2024
- Source: arxiv
- URL: http://arxiv.org/abs/2402.03367v2
- Citations: 0
- Citation check: passed
- Summary: Infineon has identified a need for engineers, account managers, and customers to rapidly obtain product information. This problem is traditionally addressed with retrieval-augmented generation (RAG) chatbots, but in this study, I evaluated the use of the newly popularized RAG-Fusion method. RAG-Fusion combines RAG and reciprocal rank fusion (RRF) by generating multiple queries, reranking them with reciprocal scores and fusing the documents and scores. Through manually evaluating answers on accuracy, relevance, and comprehensiveness, I found that RAG-Fusion was able to provide accurate and comprehensive answers due to the generated queries contextualizing the original query from various perspectives. However, some answers strayed off topic when the generated queries' relevance to the original query is insufficient. This research marks significant progress in artificial intelligence (AI) and natural language processing (NLP) applications and demonstrates transformations in a global and multi-industry context.

## 3. Key Claims and Evidence

| Claim ID | Type | Claim | Evidence IDs |
| --- | --- | --- | --- |
| `c1` | Synthesis | Research on Retrieval-Augmented Generation (RAG) in NLP: Methodologies, Applications, and Evaluation is moving from single-step generation toward tool-using, evidence-grounded workflows. | `llm-crossref-10-20944-1`, `llm-crossref-10-20944-2`, `llm-crossref-10-20944-3`, `llm-crossref-10-21203-1` |
| `c2` | Hypothesis | A promising research gap is to make the literature review process auditable through claim-evidence alignment and citation checking. | `llm-crossref-10-64898-4`, `llm-crossref-10-64898-5`, `llm-arxiv-2501-09136v4-2` |

## RAG Research Lens

A domain-aware lens that checks whether selected RAG papers cover survey, retrieval, grounding, evaluation, security, structured RAG, and applications.

- Coverage: 1.000
- Missing dimensions: None

| Dimension | Paper Count |
| --- | ---: |
| Domain Applications | 10 |
| Evaluation & Benchmarks | 10 |
| Generation & Grounding | 12 |
| Graph & Structured RAG | 3 |
| Retrieval & Indexing | 12 |
| Security & Robustness | 3 |
| Survey & Taxonomy | 5 |

| Paper ID | Lens Dimensions |
| --- | --- |
| `crossref:10.20944/preprints202510.0418.v2` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Security & Robustness, Domain Applications |
| `crossref:10.21203/rs.3.rs-9427085/v1` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Domain Applications |
| `crossref:10.3390/app15084234` | Survey & Taxonomy, Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Domain Applications |
| `crossref:10.64898/2026.05.27.26353695` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Graph & Structured RAG |
| `arxiv:2508.05650v1` | Survey & Taxonomy, Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Graph & Structured RAG, Domain Applications |
| `arxiv:2501.09136v4` | Survey & Taxonomy, Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Domain Applications |
| `crossref:10.2139/ssrn.6608518` | Survey & Taxonomy, Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Domain Applications |
| `arxiv:2601.05264v1` | Survey & Taxonomy, Retrieval & Indexing, Generation & Grounding, Security & Robustness, Domain Applications |
| `arxiv:2510.25518v1` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Security & Robustness, Graph & Structured RAG, Domain Applications |
| `arxiv:2401.15391v1` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks |
| `crossref:10.34218/ijaiap_05_01_001` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Domain Applications |
| `arxiv:2402.03367v2` | Retrieval & Indexing, Generation & Grounding, Domain Applications |

## 4. Method Taxonomy

### Contribution

- Secure-RAG is a modular, security-first evaluation suite for RAG systems. (`llm-crossref-10-20944-1`)
- Development of an AI-based chatbot for pre-mission planning using RAG. (`llm-crossref-10-21203-1`)
- The survey identifies 47 papers on RAG chatbot uses in education. (`llm-crossref-10-3390-a-1`)
- Direct comparison of embedding, LLM, and RAG approaches for ICD coding on a real-world dataset. (`llm-crossref-10-64898-1`)
- Introduction of OmniBench-RAG, an automated multi-domain evaluation platform for RAG. (`llm-arxiv-2508-05650v1-1`)

### Method

- Secure-RAG instruments each stage with lightweight monitors for standardized metrics. (`llm-crossref-10-20944-2`)
- The chatbot uses a modular RAG stack with vector database, retriever, and LLM. (`llm-crossref-10-21203-2`)
- Papers are analyzed across character, target, scope, LLM, and evaluation. (`llm-crossref-10-3390-a-2`)
- Evaluated nine embedding models and LLM-based coding with and without RAG. (`llm-crossref-10-64898-2`)
- Platform features dynamic test generation, modular pipelines, and automated knowledge base construction. (`llm-arxiv-2508-05650v1-2`)

### Experiment

- Secure-RAG improves reliability without sacrificing utility in an illustrative evaluation. (`llm-crossref-10-20944-3`)
- Initial tests show the chatbot reliably answers pre-mission planning queries in a simulated environment. (`llm-crossref-10-21203-3`)
- Best embedding model (Qwen3-Embedding-8B) achieved 47.8% exact-match accuracy for ICD-10. (`llm-crossref-10-64898-3`)
- Evaluation reveals striking variability in RAG effectiveness across domains, from gains in culture to declines in math. (`llm-arxiv-2508-05650v1-3`)
- RAG-augmented system achieves 1.000 accuracy vs base model 0.760 on 25 medical QA questions. (`llm-crossref-10-2139-s-1`)

### Limitation

- RAG outperforms embedding on partial-match but not exact-match accuracy. (`llm-crossref-10-64898-4`)
- Some answers stray off topic when generated queries' relevance to original query is insufficient. (`llm-arxiv-2402-03367v2-2`)

### Future Work

- Future advances in embedding-based methods with larger data may be promising. (`llm-crossref-10-64898-5`)
- Key open research challenges include evaluation, coordination, memory management, efficiency, and governance. (`llm-arxiv-2501-09136v4-2`)

## Evidence Ledger

| Evidence ID | Paper ID | Category | Confidence | Support Text |
| --- | --- | --- | ---: | --- |
| `llm-crossref-10-20944-1` | `crossref:10.20944/preprints202510.0418.v2` | contribution | 0.65 | we present Secure-RAG, a modular, security-first evaluation suite for multi-dimensional assessment of RAG systems |
| `llm-crossref-10-20944-2` | `crossref:10.20944/preprints202510.0418.v2` | method | 0.65 | Secure-RAG instruments each stage (query, retrieval, generation) with lightweight monitors that compute standardized metrics. |
| `llm-crossref-10-20944-3` | `crossref:10.20944/preprints202510.0418.v2` | experiment | 0.65 | In an illustrative evaluation, we demonstrate Secure-RAG improves reliability without sacrificing utility. |
| `llm-crossref-10-21203-1` | `crossref:10.21203/rs.3.rs-9427085/v1` | contribution | 0.65 | This work presents the development of an AI-based chatbot that supports planning activities by providing relevant information on demand. |
| `llm-crossref-10-21203-2` | `crossref:10.21203/rs.3.rs-9427085/v1` | method | 0.65 | The technical implementation is based on a modular RAG stack consisting of a vector database, retriever, and Lage Language Model (LLM) component. |
| `llm-crossref-10-21203-3` | `crossref:10.21203/rs.3.rs-9427085/v1` | experiment | 0.65 | Initial tests in a simulated coordination environment indicate that the chatbot can reliably answer typical pre-mission planning queries |
| `llm-crossref-10-3390-a-1` | `crossref:10.3390/app15084234` | contribution | 0.65 | This paper identifies 47 papers dedicated to RAG chatbots’ uses for various kinds of educational purposes |
| `llm-crossref-10-3390-a-2` | `crossref:10.3390/app15084234` | method | 0.65 | which are analyzed in terms of their character, the target of the support provided by the chatbots, the thematic scope of the knowledge accessible via the chatbots, the underlying large language model, and the character of their evaluation. |
| `llm-crossref-10-64898-1` | `crossref:10.64898/2026.05.27.26353695` | contribution | 0.65 | we directly compare these approaches on a real-world dataset of tumor diagnosis descriptions to assess their strengths and limitations. |
| `llm-crossref-10-64898-2` | `crossref:10.64898/2026.05.27.26353695` | method | 0.65 | Methods We evaluated nine different embedding models using similarity search and embedding-based classification, as well as LLM-based coding, with and without RAG |
| `llm-crossref-10-64898-3` | `crossref:10.64898/2026.05.27.26353695` | experiment | 0.65 | Qwen3-Embedding-8B, the largest embedding model, yielded the best results. It achieved 47.8% exact-match and 72.1% partial-match accuracy for ICD-10 coding with classification |
| `llm-crossref-10-64898-4` | `crossref:10.64898/2026.05.27.26353695` | limitation | 0.65 | RAG improved base LLM performance and outperformed embedding-based approaches on partial-match accuracy (80.6% partial-match accuracy for ICD-10 and 75.0% for ICD-O with Llama 3.3 70B), but not on exact-match accuracy. |
| `llm-crossref-10-64898-5` | `crossref:10.64898/2026.05.27.26353695` | future_work | 0.65 | Further advances in embedding-based methods, potentially supported by larger and more diverse training data, may offer a promising direction for future work. |
| `llm-arxiv-2508-05650v1-1` | `arxiv:2508.05650v1` | contribution | 0.65 | We introduce OmniBench RAG, a novel automated platform for multi domain evaluation of RAG systems. |
| `llm-arxiv-2508-05650v1-2` | `arxiv:2508.05650v1` | method | 0.65 | The platform features dynamic test generation, modular evaluation pipelines, and automated knowledge base construction. |
| `llm-arxiv-2508-05650v1-3` | `arxiv:2508.05650v1` | experiment | 0.65 | Our evaluation reveals striking variability in RAG effectiveness, from significant gains in culture to declines in mathematics |
| `llm-arxiv-2501-09136v4-1` | `arxiv:2501.09136v4` | contribution | 0.65 | Agentic Retrieval-Augmented Generation (Agentic RAG) transcends these limitations by embedding autonomous AI agents into the RAG pipeline. These agents leverage agentic design patterns reflection, planning, tool use, and multi-agent collaboration to dynamically manage retrieva... |
| `llm-arxiv-2501-09136v4-2` | `arxiv:2501.09136v4` | future_work | 0.65 | Finally, it identifies key open research challenges related to evaluation, coordination, memory management, efficiency, and governance, outlining directions for future research. |
| `llm-crossref-10-2139-s-1` | `crossref:10.2139/ssrn.6608518` | experiment | 0.65 | The base model achieves 0.760 accuracy while the RAG-augmented system achieves 1.000, a gain of 24 percentage points. |
| `llm-crossref-10-2139-s-2` | `crossref:10.2139/ssrn.6608518` | contribution | 0.65 | Qualitative analysis of the 6 base-model failures reveals two distinct hallucination patterns: (i) fabrication, where the model invents specific trial names, authors, and effect sizes with confident language; and (ii) confident substitution, where the model returns plausible b... |
| `llm-arxiv-2601-05264v1-1` | `arxiv:2601.05264v1` | contribution | 0.65 | This article provides a comprehensive systematic literature review of academic studies, industrial applications, and real-world deployments from 2018 to 2025, providing a practical guide and detailed overview of modern Retrieval-Augmented Generation (RAG) architectures. |
| `llm-arxiv-2601-05264v1-2` | `arxiv:2601.05264v1` | method | 0.65 | We provide quantitative assessment frameworks, analyze the implications for trust and alignment, and systematically consolidate existing RAG techniques into a unified taxonomy. |
| `llm-arxiv-2510-25518v1-1` | `arxiv:2510.25518v1` | method | 0.65 | This paper introduces an agentic RAG architecture designed to address these challenges through a modular pipeline of specialized agents. The proposed system supports intelligent query reformulation, iterative sub-query decomposition guided by keyphrase extraction, contextual a... |
| `llm-arxiv-2510-25518v1-2` | `arxiv:2510.25518v1` | experiment | 0.65 | Experimental results demonstrate that the agentic RAG system outperforms the baseline in retrieval precision and relevance, albeit with increased latency. |
| `llm-arxiv-2401-15391v1-1` | `arxiv:2401.15391v1` | contribution | 0.65 | In this paper, we develop a novel dataset, MultiHop-RAG, which consists of a knowledge base, a large collection of multi-hop queries, their ground-truth answers, and the associated supporting evidence. |
| `llm-arxiv-2401-15391v1-2` | `arxiv:2401.15391v1` | experiment | 0.65 | Both experiments reveal that existing RAG methods perform unsatisfactorily in retrieving and answering multi-hop queries. |
| `llm-arxiv-2402-03367v2-1` | `arxiv:2402.03367v2` | contribution | 0.65 | Through manually evaluating answers on accuracy, relevance, and comprehensiveness, I found that RAG-Fusion was able to provide accurate and comprehensive answers due to the generated queries contextualizing the original query from various perspectives. |
| `llm-arxiv-2402-03367v2-2` | `arxiv:2402.03367v2` | limitation | 0.65 | However, some answers strayed off topic when the generated queries' relevance to the original query is insufficient. |
| `llm-arxiv-2402-03367v2-3` | `arxiv:2402.03367v2` | method | 0.65 | RAG-Fusion combines RAG and reciprocal rank fusion (RRF) by generating multiple queries, reranking them with reciprocal scores and fusing the documents and scores. |
| `llm-arxiv-2402-03367v2-4` | `arxiv:2402.03367v2` | experiment | 0.65 | Through manually evaluating answers on accuracy, relevance, and comprehensiveness |

## 5. Comparative Analysis

| Paper | Main Evidence | Confidence |
| --- | --- | --- |
| Building a Security and Reliability Evaluation Suite for Retrieval-Augmented Generation (RAG) Systems | Secure-RAG is a modular, security-first evaluation suite for RAG systems. | 0.65 |
| Development and Evaluation of a Chatbot to Support Pre-Mission Planning in a Launch and Re-entry Coordination Center Using Retrieval-Augmented Generation (RAG) | Development of an AI-based chatbot for pre-mission planning using RAG. | 0.65 |
| Retrieval-Augmented Generation (RAG) Chatbots for Education: A Survey of Applications | The survey identifies 47 papers on RAG chatbot uses in education. | 0.65 |
| To RAG, or Not to RAG? A Comparative Evaluation of Retrieval-Augmented Generation for ICD Coding of German Tumor Diagnoses | Direct comparison of embedding, LLM, and RAG approaches for ICD coding on a real-world dataset. | 0.65 |
| OmniBench-RAG: A Multi-Domain Evaluation Platform for Retrieval-Augmented Generation Tools | Introduction of OmniBench-RAG, an automated multi-domain evaluation platform for RAG. | 0.65 |
| Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG | Agentic RAG systems embed autonomous AI agents into the RAG pipeline to dynamically manage retrieval strategies and adapt workflows. | 0.65 |
| MedRAG: Retrieval-Augmented Generation for Medical QA-Comparing Base and RAG-Augmented LLM Performance on Evidence from Peer-Reviewed Clinical Research | RAG-augmented system achieves 1.000 accuracy vs base model 0.760 on 25 medical QA questions. | 0.65 |
| Engineering the RAG Stack: A Comprehensive Review of the Architecture and Trust Frameworks for Retrieval-Augmented Generation Systems | The paper provides a comprehensive systematic literature review and practical guide for modern RAG architectures. | 0.65 |
| Retrieval Augmented Generation (RAG) for Fintech: Agentic Design and Evaluation | The proposed system supports intelligent query reformulation, iterative sub-query decomposition, contextual acronym resolution, and cross-encoder-based context re-ranking. | 0.65 |
| MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries | The paper introduces MultiHop-RAG, a novel dataset for multi-hop queries consisting of a knowledge base, queries, answers, and supporting evidence. | 0.65 |
| RAG-Fusion: a New Take on Retrieval-Augmented Generation | RAG-Fusion provides accurate and comprehensive answers due to generated queries contextualizing from various perspectives. | 0.65 |

## 6. Research Gaps

- A promising research gap is to make the literature review process auditable through claim-evidence alignment and citation checking. Evidence: `llm-crossref-10-64898-4`, `llm-crossref-10-64898-5`, `llm-arxiv-2501-09136v4-2`

## 7. Limitations of This Automated Review

- MVP mode may rely on metadata and abstracts rather than full paper text.
- Offline fixture mode is deterministic and intended for demo stability.
- Citation checks validate metadata availability, not peer-review quality.

## Citation Checks

| Check ID | Paper ID | Status | Message |
| --- | --- | --- | --- |
| `check-1` | `crossref:10.20944/preprints202510.0418.v2` | passed | Citation metadata is available. |
| `check-2` | `crossref:10.21203/rs.3.rs-9427085/v1` | passed | Citation metadata is available. |
| `check-3` | `crossref:10.3390/app15084234` | passed | Citation metadata is available. |
| `check-4` | `crossref:10.64898/2026.05.27.26353695` | passed | Citation metadata is available. |
| `check-5` | `arxiv:2508.05650v1` | passed | Citation metadata is available. |
| `check-6` | `arxiv:2501.09136v4` | passed | Citation metadata is available. |
| `check-7` | `crossref:10.2139/ssrn.6608518` | passed | Citation metadata is available. |
| `check-8` | `arxiv:2601.05264v1` | passed | Citation metadata is available. |
| `check-9` | `arxiv:2510.25518v1` | passed | Citation metadata is available. |
| `check-10` | `arxiv:2401.15391v1` | passed | Citation metadata is available. |
| `check-11` | `crossref:10.34218/ijaiap_05_01_001` | passed | Citation metadata is available. |
| `check-12` | `arxiv:2402.03367v2` | passed | Citation metadata is available. |

## References

[P1] Pronoy Roy, Debayan Roy. (2025). Building a Security and Reliability Evaluation Suite for Retrieval-Augmented Generation (RAG) Systems. https://doi.org/10.20944/preprints202510.0418.v2
[P2] Jens Hampe. (2026). Development and Evaluation of a Chatbot to Support Pre-Mission Planning in a Launch and Re-entry Coordination Center Using Retrieval-Augmented Generation (RAG). https://doi.org/10.21203/rs.3.rs-9427085/v1
[P3] Jakub Swacha, Michał Gracel. (2025). Retrieval-Augmented Generation (RAG) Chatbots for Education: A Survey of Applications. https://doi.org/10.3390/app15084234
[P4] Fatma Alickovic, Stefan Lenz, Arsenij Ustjanzew, Lakisha Ortiz Rosario, Georg Vollmar, Thomas Kindler, Torsten Panholzer. (2026). To RAG, or Not to RAG? A Comparative Evaluation of Retrieval-Augmented Generation for ICD Coding of German Tumor Diagnoses. https://doi.org/10.64898/2026.05.27.26353695
[P5] Jiaxuan Liang, Shide Zhou, Kailong Wang. (2025). OmniBench-RAG: A Multi-Domain Evaluation Platform for Retrieval-Augmented Generation Tools. http://arxiv.org/abs/2508.05650v1
[P6] Aditi Singh, Abul Ehtesham, Saket Kumar, Tala Talaei Khoei, Athanasios V. Vasilakos. (2025). Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG. http://arxiv.org/abs/2501.09136v4
[P7] Kunal Dhanda. (2026). MedRAG: Retrieval-Augmented Generation for Medical QA-Comparing Base and RAG-Augmented LLM Performance on Evidence from Peer-Reviewed Clinical Research. https://doi.org/10.2139/ssrn.6608518
[P8] Dean Wampler, Dave Nielson, Alireza Seddighi. (2025). Engineering the RAG Stack: A Comprehensive Review of the Architecture and Trust Frameworks for Retrieval-Augmented Generation Systems. http://arxiv.org/abs/2601.05264v1
[P9] Thomas Cook, Richard Osuagwu, Liman Tsatiashvili, Vrynsia Vrynsia, Koustav Ghosal, Maraim Masoud, Riccardo Mattivi. (2025). Retrieval Augmented Generation (RAG) for Fintech: Agentic Design and Evaluation. http://arxiv.org/abs/2510.25518v1
[P10] Yixuan Tang, Yi Yang. (2024). MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries. http://arxiv.org/abs/2401.15391v1
[P11] Ramesh Chandra Aditya Komperla. (2026). ENHANCING KNOWLEDGE-INTENSIVE CUSTOMER SUPPORT IN REGULATED INDUSTRIES THROUGH RETRIEVAL-AUGMENTED GENERATION (RAG): ARCHITECTURE, ALGORITHMS, AND EMPIRICAL EVALUATION. https://doi.org/10.34218/ijaiap_05_01_001
[P12] Zackary Rackauckas. (2024). RAG-Fusion: a New Take on Retrieval-Augmented Generation. http://arxiv.org/abs/2402.03367v2
