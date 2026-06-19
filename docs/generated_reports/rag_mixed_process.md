# Research Process: retrieval augmented generation for large language models

This file records observable Agent actions and artifacts. It is not a hidden chain-of-thought transcript.

## Run Summary

- Task ID: `20260619142048-retrieval-augmented-generation-f`
- Original topic: `retrieval augmented generation for large language models`
- Effective search topic: `retrieval augmented generation for large language models`
- Topic refinement enabled: `false`
- Topic refinement used: `false`
- Topic refinement fallback: None
- Requested source: `mixed`
- Actual source: `arxiv+crossref+openalex`
- Candidate limit: `80`
- Candidate multiplier: `8`
- From year: `2020`
- Fallback reason: Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: 
- Report path: `docs\generated_reports\rag_mixed_full_report.md`
- Summary path: `docs\generated_reports\rag_mixed_summary.md`
- Graph runtime: `sequential`
- LLM provider: `off`
- LLM used: `false`
- LLM chunk count: `0`
- LLM fallback reason: LLM provider is disabled.

## Topic Understanding

- Refined topic: `retrieval augmented generation for large language models`
- Scope notes: None
- Research questions: None
- Adjacent topics: None

## Query Plan

| Query ID | Search Query | Source Intent | Filters |
| --- | --- | --- | --- |
| `q1` | retrieval augmented generation for large language models | mixed | `{'from_year': 2020, 'angle': 'core', 'distance': 'direct'}` |
| `q2` | retrieval augmented generation large language models survey taxonomy | mixed | `{'from_year': 2020, 'angle': 'survey_taxonomy', 'distance': 'direct'}` |
| `q3` | retrieval augmented generation large language models methods systems architecture | mixed | `{'from_year': 2020, 'angle': 'methods_systems', 'distance': 'direct'}` |
| `q4` | retrieval augmented generation large language models evaluation benchmark dataset | mixed | `{'from_year': 2020, 'angle': 'evaluation_benchmark', 'distance': 'direct'}` |
| `q5` | retrieval augmented generation large language models challenges limitations open problems | mixed | `{'from_year': 2020, 'angle': 'limitations_challenges', 'distance': 'direct'}` |
| `q6` | retrieval augmented generation large language models applications case studies | mixed | `{'from_year': 2020, 'angle': 'applications_domains', 'distance': 'adjacent'}` |
| `q7` | retrieval augmented generation large language models security robustness hallucination | mixed | `{'from_year': 2020, 'angle': 'security_robustness', 'distance': 'adjacent'}` |

## Query Tree

| Research Question | Subquery Count | Angles |
| --- | ---: | --- |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | 4 | application, core, method, survey |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | 4 | application, core, limitation, security |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | 4 | application, benchmark, method, survey |
| retrieval augmented generation for large language models 的主要局限、风险和未来研究方向是什么？ | 4 | application, core, security, survey |

## Search Results

- Retrieved candidates before ranking: 80
- Candidate source counts: arxiv=27, crossref=27, openalex=26
- Source results: `actual_source: arxiv+crossref+openalex, source_counts: {'arxiv': 27, 'crossref': 27, 'openalex': 26}, paper_type_counts: {'benchmark': 38, 'method': 28, 'survey': 14}, fallback_reason: Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: `
- Candidate year range: 2023-2026
- Last 3 year ratio: 0.925
- Last 5 year ratio: 1.000

| Year | Candidate Count |
| ---: | ---: |
| 2023 | 6 |
| 2024 | 34 |
| 2025 | 30 |
| 2026 | 10 |

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
| 1 | `crossref:10.36227/techrxiv.177272838.89432844/v1` | A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large Language Models | 2026 | crossref | 46.380 | https://doi.org/10.36227/techrxiv.177272838.89432844/v1 |
| 2 | `openalex:W4404694648` | Adaptive Control of Retrieval-Augmented Generation for Large Language Models Through Reflective Tags | 2024 | openalex | 39.950 | https://doi.org/10.3390/electronics13234643 |
| 3 | `openalex:W4403560390` | CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of Large Language Models | 2024 | openalex | 48.000 | https://doi.org/10.1145/3701228 |
| 4 | `crossref:10.36227/techrxiv.176297583.39945193/v1` | A Multi-Agent Cybersecurity Assessment System Leveraging Large Language Models with Retrieval-Augmented Generation, I... | 2025 | crossref | 46.600 | https://doi.org/10.36227/techrxiv.176297583.39945193/v1 |
| 5 | `openalex:W4411203672` | Retrieval augmented generation for large language models in healthcare: A systematic review | 2025 | openalex | 44.000 | https://doi.org/10.1371/journal.pdig.0000877 |
| 6 | `openalex:W4395050972` | Optimization of hepatological clinical guidelines interpretation by large language models: a retrieval augmented gene... | 2024 | openalex | 43.420 | https://doi.org/10.1038/s41746-024-01091-y |
| 7 | `openalex:W4389984066` | Retrieval-Augmented Generation for Large Language Models: A Survey | 2023 | openalex | 43.340 | http://arxiv.org/abs/2312.10997 |
| 8 | `openalex:W4393147129` | Benchmarking Large Language Models in Retrieval-Augmented Generation | 2024 | openalex | 43.220 | https://doi.org/10.1609/aaai.v38i16.29728 |

## Research Lens

A domain-aware lens that checks whether selected RAG papers cover survey, retrieval, grounding, evaluation, security, structured RAG, and applications.

- Lens name: RAG Research Lens
- Coverage: 1.000
- Missing dimensions: None

| Dimension | Paper Count |
| --- | ---: |
| Domain Applications | 5 |
| Evaluation & Benchmarks | 6 |
| Generation & Grounding | 8 |
| Graph & Structured RAG | 3 |
| Retrieval & Indexing | 8 |
| Security & Robustness | 2 |
| Survey & Taxonomy | 5 |

| Paper ID | Lens Dimensions |
| --- | --- |
| `crossref:10.36227/techrxiv.177272838.89432844/v1` | Survey & Taxonomy, Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Graph & Structured RAG |
| `openalex:W4404694648` | Retrieval & Indexing, Generation & Grounding |
| `openalex:W4403560390` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Domain Applications |
| `crossref:10.36227/techrxiv.176297583.39945193/v1` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Security & Robustness, Graph & Structured RAG, Domain Applications |
| `openalex:W4411203672` | Survey & Taxonomy, Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Domain Applications |
| `openalex:W4395050972` | Survey & Taxonomy, Retrieval & Indexing, Generation & Grounding, Graph & Structured RAG, Domain Applications |
| `openalex:W4389984066` | Survey & Taxonomy, Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Domain Applications |
| `openalex:W4393147129` | Survey & Taxonomy, Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Security & Robustness |

## Coverage Gaps and Expansion

- No remaining structural coverage gaps detected.
- No expansion round was needed or executed.

## Evidence Extraction

| Evidence ID | Paper ID | Category | Confidence | Claim |
| --- | --- | --- | ---: | --- |
| `e1-contribution` | `crossref:10.36227/techrxiv.177272838.89432844/v1` | contribution | 0.78 | A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large Language Models contributes evidence about retrieval-augmented generation (rag) has emerged as... |
| `e1-limitation` | `crossref:10.36227/techrxiv.177272838.89432844/v1` | limitation | 0.62 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large L... |
| `e2-contribution` | `openalex:W4404694648` | contribution | 0.78 | Adaptive Control of Retrieval-Augmented Generation for Large Language Models Through Reflective Tags contributes evidence about while retrieval-augmented generation (rag) enhanc... |
| `e2-limitation` | `openalex:W4404694648` | limitation | 0.62 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for Adaptive Control of Retrieval-Augmented Generation for Large Language Models Throug... |
| `e3-contribution` | `openalex:W4403560390` | contribution | 0.78 | CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of Large Language Models contributes evidence about retrieval-augmented generation (rag) is a tech... |
| `e3-limitation` | `openalex:W4403560390` | limitation | 0.62 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of L... |
| `e4-contribution` | `crossref:10.36227/techrxiv.176297583.39945193/v1` | contribution | 0.78 | A Multi-Agent Cybersecurity Assessment System Leveraging Large Language Models with Retrieval-Augmented Generation, IOC Extraction, and SIEM Integration contributes evidence abo... |
| `e4-limitation` | `crossref:10.36227/techrxiv.176297583.39945193/v1` | limitation | 0.62 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for A Multi-Agent Cybersecurity Assessment System Leveraging Large Language Models with... |
| `e5-contribution` | `openalex:W4411203672` | contribution | 0.78 | Retrieval augmented generation for large language models in healthcare: A systematic review contributes evidence about large language models (llms) have demonstrated promising c... |
| `e5-limitation` | `openalex:W4411203672` | limitation | 0.62 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for Retrieval augmented generation for large language models in healthcare: A systemati... |
| `e6-contribution` | `openalex:W4395050972` | contribution | 0.78 | Optimization of hepatological clinical guidelines interpretation by large language models: a retrieval augmented generation-based framework contributes evidence about large lang... |
| `e6-limitation` | `openalex:W4395050972` | limitation | 0.62 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for Optimization of hepatological clinical guidelines interpretation by large language... |
| `e7-contribution` | `openalex:W4389984066` | contribution | 0.78 | Retrieval-Augmented Generation for Large Language Models: A Survey contributes evidence about large language models (llms) showcase impressive capabilities but encounter challen... |
| `e7-limitation` | `openalex:W4389984066` | limitation | 0.62 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for Retrieval-Augmented Generation for Large Language Models: A Survey. |
| `e8-contribution` | `openalex:W4393147129` | contribution | 0.78 | Benchmarking Large Language Models in Retrieval-Augmented Generation contributes evidence about retrieval-augmented generation (rag) is a promising approach for mitigating the h... |
| `e8-limitation` | `openalex:W4393147129` | limitation | 0.62 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for Benchmarking Large Language Models in Retrieval-Augmented Generation. |

## Evidence Matrix

| Research Question | Paper ID | Evidence IDs |
| --- | --- | --- |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | `crossref:10.36227/techrxiv.177272838.89432844/v1` | `e1-contribution`, `e1-limitation` |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | `openalex:W4404694648` | `e2-contribution`, `e2-limitation` |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | `openalex:W4403560390` | `e3-contribution`, `e3-limitation` |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | `crossref:10.36227/techrxiv.176297583.39945193/v1` | `e4-contribution`, `e4-limitation` |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | `openalex:W4411203672` | `e5-contribution`, `e5-limitation` |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | `openalex:W4395050972` | `e6-contribution`, `e6-limitation` |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | `openalex:W4389984066` | `e7-contribution`, `e7-limitation` |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | `openalex:W4393147129` | `e8-contribution`, `e8-limitation` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | `crossref:10.36227/techrxiv.177272838.89432844/v1` | `e1-contribution`, `e1-limitation` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | `openalex:W4404694648` | `e2-contribution`, `e2-limitation` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | `openalex:W4403560390` | `e3-contribution`, `e3-limitation` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | `crossref:10.36227/techrxiv.176297583.39945193/v1` | `e4-contribution`, `e4-limitation` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | `openalex:W4411203672` | `e5-contribution`, `e5-limitation` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | `openalex:W4395050972` | `e6-contribution`, `e6-limitation` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | `openalex:W4389984066` | `e7-contribution`, `e7-limitation` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | `openalex:W4393147129` | `e8-contribution`, `e8-limitation` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | `crossref:10.36227/techrxiv.177272838.89432844/v1` | `e1-contribution`, `e1-limitation` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | `openalex:W4404694648` | `e2-contribution`, `e2-limitation` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | `openalex:W4403560390` | `e3-contribution`, `e3-limitation` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | `crossref:10.36227/techrxiv.176297583.39945193/v1` | `e4-contribution`, `e4-limitation` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | `openalex:W4411203672` | `e5-contribution`, `e5-limitation` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | `openalex:W4395050972` | `e6-contribution`, `e6-limitation` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | `openalex:W4389984066` | `e7-contribution`, `e7-limitation` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | `openalex:W4393147129` | `e8-contribution`, `e8-limitation` |
| retrieval augmented generation for large language models 的主要局限、风险和未来研究方向是什么？ | `crossref:10.36227/techrxiv.177272838.89432844/v1` | `e1-contribution`, `e1-limitation` |
| retrieval augmented generation for large language models 的主要局限、风险和未来研究方向是什么？ | `openalex:W4404694648` | `e2-contribution`, `e2-limitation` |
| retrieval augmented generation for large language models 的主要局限、风险和未来研究方向是什么？ | `openalex:W4403560390` | `e3-contribution`, `e3-limitation` |
| retrieval augmented generation for large language models 的主要局限、风险和未来研究方向是什么？ | `crossref:10.36227/techrxiv.176297583.39945193/v1` | `e4-contribution`, `e4-limitation` |
| retrieval augmented generation for large language models 的主要局限、风险和未来研究方向是什么？ | `openalex:W4411203672` | `e5-contribution`, `e5-limitation` |
| retrieval augmented generation for large language models 的主要局限、风险和未来研究方向是什么？ | `openalex:W4395050972` | `e6-contribution`, `e6-limitation` |
| retrieval augmented generation for large language models 的主要局限、风险和未来研究方向是什么？ | `openalex:W4389984066` | `e7-contribution`, `e7-limitation` |
| retrieval augmented generation for large language models 的主要局限、风险和未来研究方向是什么？ | `openalex:W4393147129` | `e8-contribution`, `e8-limitation` |

## Claim-Evidence Alignment

| Claim ID | Type | Claim | Evidence IDs |
| --- | --- | --- | --- |
| `c1` | Synthesis | Research on retrieval augmented generation for large language models is moving from single-step generation toward tool-using, evidence-grounded workflows. | `e1-contribution`, `e2-contribution`, `e3-contribution`, `e4-contribution` |
| `c2` | Hypothesis | A promising research gap is to make the literature review process auditable through claim-evidence alignment and citation checking. | `e1-limitation`, `e2-limitation`, `e3-limitation` |

## Citation Checks

| Check ID | Paper ID | Status | Message |
| --- | --- | --- | --- |
| `check-1` | `crossref:10.36227/techrxiv.177272838.89432844/v1` | passed | Citation metadata is available. |
| `check-2` | `openalex:W4404694648` | passed | Citation metadata is available. |
| `check-3` | `openalex:W4403560390` | passed | Citation metadata is available. |
| `check-4` | `crossref:10.36227/techrxiv.176297583.39945193/v1` | passed | Citation metadata is available. |
| `check-5` | `openalex:W4411203672` | passed | Citation metadata is available. |
| `check-6` | `openalex:W4395050972` | passed | Citation metadata is available. |
| `check-7` | `openalex:W4389984066` | passed | Citation metadata is available. |
| `check-8` | `openalex:W4393147129` | passed | Citation metadata is available. |

## Agent Trace

| Step | Node | Status | Output Keys |
| ---: | --- | --- | --- |
| 1 | `plan_queries` | success | `effective_topic, query_plan, query_tree, refined_topic, subtopics, topic_refinement, topic_refinement_fallback_reason, topic_refinement_used` |
| 2 | `search_papers` | success | `actual_source, fallback_reason, searched_papers, source_results, temporal_profile` |
| 3 | `rank_papers` | success | `corpus_profile, coverage_gaps, ranked_candidates, research_lens, selected_papers` |
| 4 | `expand_search` | success | `expansion_rounds` |
| 5 | `extract_evidence` | success | `evidence_items, llm_chunk_count, llm_fallback_reason, llm_used` |
| 6 | `synthesize_claims` | success | `claim_graph, claims, evidence_matrix` |
| 7 | `check_citations` | success | `citation_checks` |
| 8 | `write_report` | success | `llm_fallback_reason, llm_used, report_markdown, report_path` |
| 9 | `evaluate_result` | success | `metrics` |

## Metrics

| Metric | Value |
| --- | --- |
| `query_count` | `7` |
| `query_angle_count` | `7` |
| `adjacent_query_count` | `2` |
| `searched_paper_count` | `80` |
| `selected_paper_count` | `8` |
| `candidate_limit` | `80` |
| `candidate_multiplier` | `8` |
| `from_year` | `2020` |
| `evidence_count` | `16` |
| `claim_count` | `2` |
| `citation_check_count` | `8` |
| `citation_check_pass_rate` | `1.0` |
| `claim_evidence_coverage` | `1.0` |
| `evidence_matrix_coverage` | `1.0` |
| `unsupported_claim_rate` | `0.0` |
| `hallucinated_reference_count` | `0` |
| `report_section_completeness` | `1.0` |
| `source_diversity` | `0.112` |
| `paper_type_diversity` | `1.0` |
| `coverage_gap_count` | `0` |
| `query_gap_recovery` | `1.0` |
| `node_trace_count` | `8` |
| `requested_source` | `mixed` |
| `actual_source` | `arxiv+crossref+openalex` |
| `fallback_reason` | `Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ; Semantic Scholar request failed: HTTP Error 429: ` |
| `llm_provider` | `off` |
| `llm_used` | `False` |
| `llm_fallback_reason` | `LLM provider is disabled.` |
| `llm_chunk_count` | `0` |
| `refine_topic` | `False` |
| `effective_topic` | `retrieval augmented generation for large language models` |
| `topic_refinement_used` | `False` |
| `topic_refinement_fallback_reason` | `` |
| `earliest_candidate_year` | `2023` |
| `latest_candidate_year` | `2026` |
| `recent_3_year_ratio` | `0.925` |
| `recent_5_year_ratio` | `1.0` |
| `research_lens_coverage` | `1.0` |
| `graph_runtime` | `sequential` |
| `dimension_scores` | `task_completion: 20.0, retrieval_quality: 18.58, evidence_trust: 25.0, report_quality: 20.0, agent_behavior: 15.0` |
| `overall_score` | `98.58` |
| `live_requirement_met` | `True` |
