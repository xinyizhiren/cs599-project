# Research Process: RAG 怎么样

This file records observable Agent actions and artifacts. It is not a hidden chain-of-thought transcript.

## Run Summary

- Task ID: `20260611153240-rag`
- Original topic: `RAG 怎么样`
- Effective search topic: `Retrieval-Augmented Generation (RAG) in NLP: Methodologies, Applications, and Evaluation`
- Topic refinement enabled: `true`
- Topic refinement used: `true`
- Topic refinement fallback: None
- Requested source: `hybrid`
- Actual source: `arxiv+crossref`
- Candidate limit: `96`
- Candidate multiplier: `8`
- From year: `2020`
- Fallback reason: Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: 
- Report path: `docs\generated_reports\rag_fuzzy_hybrid_literature_review.md`
- Summary path: `docs\generated_reports\rag_fuzzy_hybrid_summary.md`
- Graph runtime: `sequential`
- LLM provider: `deepseek`
- LLM used: `true`
- LLM chunk count: `3`
- LLM fallback reason: None

## Topic Understanding

- Refined topic: `Retrieval-Augmented Generation (RAG) in NLP: Methodologies, Applications, and Evaluation`
- Scope notes: Focus on peer-reviewed papers and authoritative surveys from the last 3 years. Include both theoretical frameworks and empirical studies. Exclude industry-specific applications unless they provide general insights.
- Research questions: What are the key architectural components and design choices in RAG systems?; How does RAG improve factual accuracy and reduce hallucination in language models?; What are the primary evaluation metrics and benchmarks for RAG performance?; How do different retrieval strategies (e.g., dense vs. sparse) affect RAG outcomes?; What are the current limitations and emerging trends in RAG research?
- Adjacent topics: Retrieval-based approaches in dialogue systems; Knowledge augmentation for large language models; Evaluation of factual correctness in generated text

## Query Plan

| Query ID | Search Query | Source Intent | Filters |
| --- | --- | --- | --- |
| `q1` | Retrieval-Augmented Generation (RAG) in NLP: Methodologies, Applications, and Evaluation | hybrid | `{'from_year': 2020, 'angle': 'core', 'distance': 'direct'}` |
| `q2` | retrieval-augmented generation rag nlp methodologies applications survey taxonomy | hybrid | `{'from_year': 2020, 'angle': 'survey_taxonomy', 'distance': 'direct'}` |
| `q3` | retrieval-augmented generation rag nlp methodologies applications methods systems architecture | hybrid | `{'from_year': 2020, 'angle': 'methods_systems', 'distance': 'direct'}` |
| `q4` | retrieval-augmented generation rag nlp methodologies applications evaluation benchmark dataset | hybrid | `{'from_year': 2020, 'angle': 'evaluation_benchmark', 'distance': 'direct'}` |
| `q5` | retrieval-augmented generation rag nlp methodologies applications challenges limitations open problems | hybrid | `{'from_year': 2020, 'angle': 'limitations_challenges', 'distance': 'direct'}` |
| `q6` | retrieval-augmented generation rag nlp methodologies applications applications case studies | hybrid | `{'from_year': 2020, 'angle': 'applications_domains', 'distance': 'adjacent'}` |
| `q7` | retrieval-augmented generation rag nlp methodologies applications security robustness hallucination | hybrid | `{'from_year': 2020, 'angle': 'security_robustness', 'distance': 'adjacent'}` |
| `q8` | Retrieval-Augmented Generation survey | hybrid | `{'from_year': 2020, 'angle': 'llm_hint', 'distance': 'adjacent'}` |
| `q9` | RAG evaluation benchmarks | hybrid | `{'from_year': 2020, 'angle': 'llm_hint', 'distance': 'adjacent'}` |
| `q10` | dense retrieval vs sparse retrieval RAG | hybrid | `{'from_year': 2020, 'angle': 'llm_hint', 'distance': 'adjacent'}` |

## Search Results

- Retrieved candidates before ranking: 96
- Candidate source counts: arxiv=48, crossref=48
- Candidate year range: 2022-2026
- Last 3 year ratio: 0.979
- Last 5 year ratio: 1.000

| Year | Candidate Count |
| ---: | ---: |
| 2022 | 1 |
| 2023 | 1 |
| 2024 | 24 |
| 2025 | 49 |
| 2026 | 21 |

## Information Compression Strategy

- Retrieve a broad candidate pool before ranking.
- Use temporal profiling to expose whether the review is recent enough.
- Map the candidate pool to domain dimensions before writing conclusions.
- Extract evidence from selected papers in LLM-sized batches.
- Keep claim-evidence-citation links as the auditable final surface.

## Top-K Selection

Ranking uses title-weighted topic matching, RAG phrase/acronym signals, survey/benchmark/security bonuses, recency, citation count when available, and duplicate removal.

| Rank | Paper ID | Title | Year | Source | Score | URL |
| ---: | --- | --- | ---: | --- | ---: | --- |
| 1 | `crossref:10.20944/preprints202510.0418.v2` | Building a Security and Reliability Evaluation Suite for Retrieval-Augmented Generation (RAG) Systems | 2025 | crossref | 36.400 | https://doi.org/10.20944/preprints202510.0418.v2 |
| 2 | `crossref:10.21203/rs.3.rs-9427085/v1` | Development and Evaluation of a Chatbot to Support Pre-Mission Planning in a Launch and Re-entry Coordination Center... | 2026 | crossref | 34.480 | https://doi.org/10.21203/rs.3.rs-9427085/v1 |
| 3 | `crossref:10.3390/app15084234` | Retrieval-Augmented Generation (RAG) Chatbots for Education: A Survey of Applications | 2025 | crossref | 34.140 | https://doi.org/10.3390/app15084234 |
| 4 | `crossref:10.64898/2026.05.27.26353695` | To RAG, or Not to RAG? A Comparative Evaluation of Retrieval-Augmented Generation for ICD Coding of German Tumor Diag... | 2026 | crossref | 32.980 | https://doi.org/10.64898/2026.05.27.26353695 |
| 5 | `arxiv:2508.05650v1` | OmniBench-RAG: A Multi-Domain Evaluation Platform for Retrieval-Augmented Generation Tools | 2025 | arxiv | 32.400 | http://arxiv.org/abs/2508.05650v1 |
| 6 | `arxiv:2501.09136v4` | Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG | 2025 | arxiv | 31.900 | http://arxiv.org/abs/2501.09136v4 |
| 7 | `crossref:10.2139/ssrn.6608518` | MedRAG: Retrieval-Augmented Generation for Medical QA-Comparing Base and RAG-Augmented LLM Performance on Evidence fr... | 2026 | crossref | 30.980 | https://doi.org/10.2139/ssrn.6608518 |
| 8 | `arxiv:2601.05264v1` | Engineering the RAG Stack: A Comprehensive Review of the Architecture and Trust Frameworks for Retrieval-Augmented Ge... | 2025 | arxiv | 30.900 | http://arxiv.org/abs/2601.05264v1 |
| 9 | `arxiv:2510.25518v1` | Retrieval Augmented Generation (RAG) for Fintech: Agentic Design and Evaluation | 2025 | arxiv | 30.900 | http://arxiv.org/abs/2510.25518v1 |
| 10 | `arxiv:2401.15391v1` | MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries | 2024 | arxiv | 30.320 | http://arxiv.org/abs/2401.15391v1 |
| 11 | `crossref:10.34218/ijaiap_05_01_001` | ENHANCING KNOWLEDGE-INTENSIVE CUSTOMER SUPPORT IN REGULATED INDUSTRIES THROUGH RETRIEVAL-AUGMENTED GENERATION (RAG):... | 2026 | crossref | 29.980 | https://doi.org/10.34218/ijaiap_05_01_001 |
| 12 | `arxiv:2402.03367v2` | RAG-Fusion: a New Take on Retrieval-Augmented Generation | 2024 | arxiv | 29.820 | http://arxiv.org/abs/2402.03367v2 |

## Research Lens

A domain-aware lens that checks whether selected RAG papers cover survey, retrieval, grounding, evaluation, security, structured RAG, and applications.

- Lens name: RAG Research Lens
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

## Evidence Extraction

| Evidence ID | Paper ID | Category | Confidence | Claim |
| --- | --- | --- | ---: | --- |
| `llm-crossref-10-20944-1` | `crossref:10.20944/preprints202510.0418.v2` | contribution | 0.65 | Secure-RAG is a modular, security-first evaluation suite for RAG systems. |
| `llm-crossref-10-20944-2` | `crossref:10.20944/preprints202510.0418.v2` | method | 0.65 | Secure-RAG instruments each stage with lightweight monitors for standardized metrics. |
| `llm-crossref-10-20944-3` | `crossref:10.20944/preprints202510.0418.v2` | experiment | 0.65 | Secure-RAG improves reliability without sacrificing utility in an illustrative evaluation. |
| `llm-crossref-10-21203-1` | `crossref:10.21203/rs.3.rs-9427085/v1` | contribution | 0.65 | Development of an AI-based chatbot for pre-mission planning using RAG. |
| `llm-crossref-10-21203-2` | `crossref:10.21203/rs.3.rs-9427085/v1` | method | 0.65 | The chatbot uses a modular RAG stack with vector database, retriever, and LLM. |
| `llm-crossref-10-21203-3` | `crossref:10.21203/rs.3.rs-9427085/v1` | experiment | 0.65 | Initial tests show the chatbot reliably answers pre-mission planning queries in a simulated environment. |
| `llm-crossref-10-3390-a-1` | `crossref:10.3390/app15084234` | contribution | 0.65 | The survey identifies 47 papers on RAG chatbot uses in education. |
| `llm-crossref-10-3390-a-2` | `crossref:10.3390/app15084234` | method | 0.65 | Papers are analyzed across character, target, scope, LLM, and evaluation. |
| `llm-crossref-10-64898-1` | `crossref:10.64898/2026.05.27.26353695` | contribution | 0.65 | Direct comparison of embedding, LLM, and RAG approaches for ICD coding on a real-world dataset. |
| `llm-crossref-10-64898-2` | `crossref:10.64898/2026.05.27.26353695` | method | 0.65 | Evaluated nine embedding models and LLM-based coding with and without RAG. |
| `llm-crossref-10-64898-3` | `crossref:10.64898/2026.05.27.26353695` | experiment | 0.65 | Best embedding model (Qwen3-Embedding-8B) achieved 47.8% exact-match accuracy for ICD-10. |
| `llm-crossref-10-64898-4` | `crossref:10.64898/2026.05.27.26353695` | limitation | 0.65 | RAG outperforms embedding on partial-match but not exact-match accuracy. |
| `llm-crossref-10-64898-5` | `crossref:10.64898/2026.05.27.26353695` | future_work | 0.65 | Future advances in embedding-based methods with larger data may be promising. |
| `llm-arxiv-2508-05650v1-1` | `arxiv:2508.05650v1` | contribution | 0.65 | Introduction of OmniBench-RAG, an automated multi-domain evaluation platform for RAG. |
| `llm-arxiv-2508-05650v1-2` | `arxiv:2508.05650v1` | method | 0.65 | Platform features dynamic test generation, modular pipelines, and automated knowledge base construction. |
| `llm-arxiv-2508-05650v1-3` | `arxiv:2508.05650v1` | experiment | 0.65 | Evaluation reveals striking variability in RAG effectiveness across domains, from gains in culture to declines in math. |
| `llm-arxiv-2501-09136v4-1` | `arxiv:2501.09136v4` | contribution | 0.65 | Agentic RAG systems embed autonomous AI agents into the RAG pipeline to dynamically manage retrieval strategies and adapt workflows. |
| `llm-arxiv-2501-09136v4-2` | `arxiv:2501.09136v4` | future_work | 0.65 | Key open research challenges include evaluation, coordination, memory management, efficiency, and governance. |
| `llm-crossref-10-2139-s-1` | `crossref:10.2139/ssrn.6608518` | experiment | 0.65 | RAG-augmented system achieves 1.000 accuracy vs base model 0.760 on 25 medical QA questions. |
| `llm-crossref-10-2139-s-2` | `crossref:10.2139/ssrn.6608518` | contribution | 0.65 | RAG eliminates fabrication and confident substitution hallucination patterns by grounding responses in retrieved evidence. |
| `llm-arxiv-2601-05264v1-1` | `arxiv:2601.05264v1` | contribution | 0.65 | The paper provides a comprehensive systematic literature review and practical guide for modern RAG architectures. |
| `llm-arxiv-2601-05264v1-2` | `arxiv:2601.05264v1` | method | 0.65 | The paper provides quantitative assessment frameworks and systematically consolidates existing RAG techniques into a unified taxonomy. |
| `llm-arxiv-2510-25518v1-1` | `arxiv:2510.25518v1` | method | 0.65 | The proposed system supports intelligent query reformulation, iterative sub-query decomposition, contextual acronym resolution, and cross-encoder-based context re-ranking. |
| `llm-arxiv-2510-25518v1-2` | `arxiv:2510.25518v1` | experiment | 0.65 | The agentic RAG system outperforms the standard RAG baseline in retrieval precision and relevance, albeit with increased latency. |
| `llm-arxiv-2401-15391v1-1` | `arxiv:2401.15391v1` | contribution | 0.65 | The paper introduces MultiHop-RAG, a novel dataset for multi-hop queries consisting of a knowledge base, queries, answers, and supporting evidence. |
| `llm-arxiv-2401-15391v1-2` | `arxiv:2401.15391v1` | experiment | 0.65 | Existing RAG methods perform unsatisfactorily in retrieving and answering multi-hop queries. |
| `llm-arxiv-2402-03367v2-1` | `arxiv:2402.03367v2` | contribution | 0.65 | RAG-Fusion provides accurate and comprehensive answers due to generated queries contextualizing from various perspectives. |
| `llm-arxiv-2402-03367v2-2` | `arxiv:2402.03367v2` | limitation | 0.65 | Some answers stray off topic when generated queries' relevance to original query is insufficient. |
| `llm-arxiv-2402-03367v2-3` | `arxiv:2402.03367v2` | method | 0.65 | RAG-Fusion combines RAG and reciprocal rank fusion by generating multiple queries, reranking them with reciprocal scores and fusing documents and scores. |
| `llm-arxiv-2402-03367v2-4` | `arxiv:2402.03367v2` | experiment | 0.65 | Evaluation was done manually on accuracy, relevance, and comprehensiveness. |

## Claim-Evidence Alignment

| Claim ID | Type | Claim | Evidence IDs |
| --- | --- | --- | --- |
| `c1` | Synthesis | Research on Retrieval-Augmented Generation (RAG) in NLP: Methodologies, Applications, and Evaluation is moving from single-step generation toward tool-using, evidence-grounded w... | `llm-crossref-10-20944-1`, `llm-crossref-10-20944-2`, `llm-crossref-10-20944-3`, `llm-crossref-10-21203-1` |
| `c2` | Hypothesis | A promising research gap is to make the literature review process auditable through claim-evidence alignment and citation checking. | `llm-crossref-10-64898-4`, `llm-crossref-10-64898-5`, `llm-arxiv-2501-09136v4-2` |

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

## Agent Trace

| Step | Node | Status | Output Keys |
| ---: | --- | --- | --- |
| 1 | `plan_queries` | success | `effective_topic, query_plan, refined_topic, topic_refinement, topic_refinement_fallback_reason, topic_refinement_used` |
| 2 | `search_papers` | success | `actual_source, fallback_reason, searched_papers, temporal_profile` |
| 3 | `rank_papers` | success | `corpus_profile, ranked_candidates, research_lens, selected_papers` |
| 4 | `extract_evidence` | success | `evidence_items, llm_chunk_count, llm_fallback_reason, llm_used` |
| 5 | `synthesize_claims` | success | `claims` |
| 6 | `check_citations` | success | `citation_checks` |
| 7 | `write_report` | success | `llm_fallback_reason, llm_used, report_markdown, report_path` |
| 8 | `evaluate_result` | success | `metrics` |

## Metrics

| Metric | Value |
| --- | --- |
| `query_count` | `10` |
| `query_angle_count` | `8` |
| `adjacent_query_count` | `5` |
| `searched_paper_count` | `96` |
| `selected_paper_count` | `12` |
| `candidate_limit` | `96` |
| `candidate_multiplier` | `8` |
| `from_year` | `2020` |
| `evidence_count` | `30` |
| `claim_count` | `2` |
| `citation_check_count` | `12` |
| `citation_check_pass_rate` | `1.0` |
| `claim_evidence_coverage` | `1.0` |
| `unsupported_claim_rate` | `0.0` |
| `hallucinated_reference_count` | `0` |
| `report_section_completeness` | `1.0` |
| `node_trace_count` | `7` |
| `requested_source` | `hybrid` |
| `actual_source` | `arxiv+crossref` |
| `fallback_reason` | `Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ` |
| `llm_provider` | `deepseek` |
| `llm_used` | `True` |
| `llm_fallback_reason` | `` |
| `llm_chunk_count` | `3` |
| `refine_topic` | `True` |
| `effective_topic` | `Retrieval-Augmented Generation (RAG) in NLP: Methodologies, Applications, and Evaluation` |
| `topic_refinement_used` | `True` |
| `topic_refinement_fallback_reason` | `` |
| `earliest_candidate_year` | `2022` |
| `latest_candidate_year` | `2026` |
| `recent_3_year_ratio` | `0.979` |
| `recent_5_year_ratio` | `1.0` |
| `research_lens_coverage` | `1.0` |
| `graph_runtime` | `sequential` |
| `dimension_scores` | `task_completion: 20.0, retrieval_quality: 20.0, evidence_trust: 25.0, report_quality: 20.0, agent_behavior: 15.0` |
| `overall_score` | `100.0` |
| `live_requirement_met` | `True` |
