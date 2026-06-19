# Research Process: retrieval augmented generation for large language models

This file records observable Agent actions and artifacts. It is not a hidden chain-of-thought transcript.

## Run Summary

- Task ID: `20260619165706-retrieval-augmented-generation-f`
- Original topic: `retrieval augmented generation for large language models`
- Effective search topic: `retrieval augmented generation for large language models`
- Topic refinement enabled: `false`
- Topic refinement used: `false`
- Topic refinement fallback: None
- Requested source: `openalex`
- Actual source: `openalex`
- Candidate limit: `12`
- Candidate multiplier: `8`
- From year: `2023`
- Fallback reason: None
- Report path: `docs\generated_reports\rag_openalex_deepseek_smoke.md`
- Summary path: `docs\generated_reports\rag_openalex_deepseek_summary.md`
- Graph runtime: `sequential`
- LLM provider: `deepseek`
- LLM used: `true`
- LLM chunk count: `1`
- LLM fallback reason: None

## Topic Understanding

- Refined topic: `retrieval augmented generation for large language models`
- Scope notes: None
- Research questions: None
- Adjacent topics: None

## Query Plan

| Query ID | Search Query | Source Intent | Filters |
| --- | --- | --- | --- |
| `q1` | retrieval augmented generation for large language models | openalex | `{'from_year': 2023, 'angle': 'core', 'distance': 'direct'}` |
| `q2` | retrieval augmented generation large language models survey taxonomy | openalex | `{'from_year': 2023, 'angle': 'survey_taxonomy', 'distance': 'direct'}` |
| `q3` | retrieval augmented generation large language models methods systems architecture | openalex | `{'from_year': 2023, 'angle': 'methods_systems', 'distance': 'direct'}` |
| `q4` | retrieval augmented generation large language models evaluation benchmark dataset | openalex | `{'from_year': 2023, 'angle': 'evaluation_benchmark', 'distance': 'direct'}` |
| `q5` | retrieval augmented generation large language models challenges limitations open problems | openalex | `{'from_year': 2023, 'angle': 'limitations_challenges', 'distance': 'direct'}` |
| `q6` | retrieval augmented generation large language models applications case studies | openalex | `{'from_year': 2023, 'angle': 'applications_domains', 'distance': 'adjacent'}` |
| `q7` | retrieval augmented generation large language models security robustness hallucination | openalex | `{'from_year': 2023, 'angle': 'security_robustness', 'distance': 'adjacent'}` |
| `expansion-1` | retrieval augmented generation for large language models security robustness attack defense | expansion | `{'angle': 'security', 'distance': 'gap_recovery', 'from_year': 2023, 'gap_id': 'lens:Security & Robustness'}` |
| `expansion-2` | retrieval augmented generation for large language models methods architecture framework | expansion | `{'angle': 'method', 'distance': 'gap_recovery', 'from_year': 2023, 'gap_id': 'lens:Graph & Structured RAG'}` |

## Query Tree

| Research Question | Subquery Count | Angles |
| --- | ---: | --- |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | 3 | application, core, survey |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | 3 | application, benchmark, limitation |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | 3 | core, security, survey |

## Search Results

- Retrieved candidates before ranking: 32
- Candidate source counts: openalex=32
- Source results: `actual_source: openalex, source_counts: {'openalex': 32}, paper_type_counts: {'benchmark': 6, 'method': 9, 'survey': 17}, fallback_reason: `
- Candidate year range: 2023-2026
- Last 3 year ratio: 0.688
- Last 5 year ratio: 1.000

| Year | Candidate Count |
| ---: | ---: |
| 2023 | 10 |
| 2024 | 16 |
| 2025 | 5 |
| 2026 | 1 |

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
| 1 | `openalex:W4411203672` | Retrieval augmented generation for large language models in healthcare: A systematic review | 2025 | openalex | 44.000 | https://doi.org/10.1371/journal.pdig.0000877 |
| 2 | `openalex:W4392597393` | Integrating Retrieval-Augmented Generation with Large Language Models in Nephrology: Advancing Practical Applications | 2024 | openalex | 39.820 | https://doi.org/10.3390/medicina60030445 |
| 3 | `openalex:W4403560390` | CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of Large Language Models | 2024 | openalex | 48.000 | https://doi.org/10.1145/3701228 |

## Research Lens

A domain-aware lens that checks whether selected RAG papers cover survey, retrieval, grounding, evaluation, security, structured RAG, and applications.

- Lens name: RAG Research Lens
- Coverage: 0.714
- Missing dimensions: Security & Robustness, Graph & Structured RAG

| Dimension | Paper Count |
| --- | ---: |
| Domain Applications | 3 |
| Evaluation & Benchmarks | 2 |
| Generation & Grounding | 3 |
| Retrieval & Indexing | 3 |
| Survey & Taxonomy | 1 |

| Paper ID | Lens Dimensions |
| --- | --- |
| `openalex:W4411203672` | Survey & Taxonomy, Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Domain Applications |
| `openalex:W4392597393` | Retrieval & Indexing, Generation & Grounding, Domain Applications |
| `openalex:W4403560390` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Domain Applications |

## Coverage Gaps and Expansion

| Gap | Type | Suggested Angle | Reason |
| --- | --- | --- | --- |
| Security & Robustness | lens_dimension | security | Selected papers do not cover Security & Robustness. |
| Graph & Structured RAG | lens_dimension | method | Selected papers do not cover Graph & Structured RAG. |

| Round | Added Candidates | Source | Query Count |
| ---: | ---: | --- | ---: |
| 1 | 20 | openalex | 2 |

## Evidence Extraction

| Evidence ID | Paper ID | Category | Confidence | Claim |
| --- | --- | --- | ---: | --- |
| `llm-openalex-w44112036-1` | `openalex:W4411203672` | experiment | 0.65 | 78.9% of studies used English datasets and 21.1% are in Chinese |
| `llm-openalex-w44112036-2` | `openalex:W4411203672` | limitation | 0.65 | There is a lack of standardised evaluation frameworks for RAG-based applications |
| `llm-openalex-w44112036-3` | `openalex:W4411203672` | future_work | 0.65 | Need for further research and development to ensure responsible and effective adoption of RAG in the medical domain |
| `llm-openalex-w43925973-1` | `openalex:W4392597393` | method | 0.65 | RAG strategy helps address hallucinations by integrating external data, enhancing output accuracy and relevance |
| `llm-openalex-w43925973-2` | `openalex:W4392597393` | contribution | 0.65 | Showcase creation of a specialized ChatGPT model integrated with a RAG system tailored to KDIGO 2023 guidelines |
| `llm-openalex-w44035603-1` | `openalex:W4403560390` | contribution | 0.65 | Develops a comprehensive benchmark evaluating all components of RAG systems across four CRUD application scenarios |
| `llm-openalex-w44035603-2` | `openalex:W4403560390` | experiment | 0.65 | Analyzes effects of various components of the RAG system such as retriever, context length, knowledge base construction, and LLM |

## Evidence Matrix

| Research Question | Paper ID | Evidence IDs |
| --- | --- | --- |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | `openalex:W4411203672` | `llm-openalex-w44112036-1`, `llm-openalex-w44112036-2`, `llm-openalex-w44112036-3` |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | `openalex:W4392597393` | `llm-openalex-w43925973-1`, `llm-openalex-w43925973-2` |
| retrieval augmented generation for large language models 的核心研究问题和技术边界是什么？ | `openalex:W4403560390` | `llm-openalex-w44035603-1`, `llm-openalex-w44035603-2` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | `openalex:W4411203672` | `llm-openalex-w44112036-1`, `llm-openalex-w44112036-2`, `llm-openalex-w44112036-3` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | `openalex:W4392597393` | `llm-openalex-w43925973-1`, `llm-openalex-w43925973-2` |
| retrieval augmented generation for large language models 目前有哪些主流方法、系统架构和代表性路线？ | `openalex:W4403560390` | `llm-openalex-w44035603-1`, `llm-openalex-w44035603-2` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | `openalex:W4411203672` | `llm-openalex-w44112036-1`, `llm-openalex-w44112036-2`, `llm-openalex-w44112036-3` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | `openalex:W4392597393` | `llm-openalex-w43925973-1`, `llm-openalex-w43925973-2` |
| retrieval augmented generation for large language models 通常如何评测，关键数据集和指标是什么？ | `openalex:W4403560390` | `llm-openalex-w44035603-1`, `llm-openalex-w44035603-2` |

## Claim-Evidence Alignment

| Claim ID | Type | Claim | Evidence IDs |
| --- | --- | --- | --- |
| `c1` | Synthesis | Research on retrieval augmented generation for large language models is moving from single-step generation toward tool-using, evidence-grounded workflows. | `llm-openalex-w44112036-1`, `llm-openalex-w43925973-1`, `llm-openalex-w43925973-2`, `llm-openalex-w44035603-1` |
| `c2` | Hypothesis | A promising research gap is to make the literature review process auditable through claim-evidence alignment and citation checking. | `llm-openalex-w44112036-2`, `llm-openalex-w44112036-3` |

## Citation Checks

| Check ID | Paper ID | Status | Message |
| --- | --- | --- | --- |
| `check-1` | `openalex:W4411203672` | passed | Citation metadata is available. |
| `check-2` | `openalex:W4392597393` | passed | Citation metadata is available. |
| `check-3` | `openalex:W4403560390` | passed | Citation metadata is available. |

## Agent Trace

| Step | Node | Status | Output Keys |
| ---: | --- | --- | --- |
| 1 | `plan_queries` | success | `effective_topic, query_plan, query_tree, refined_topic, subtopics, topic_refinement, topic_refinement_fallback_reason, topic_refinement_used` |
| 2 | `search_papers` | success | `actual_source, fallback_reason, searched_papers, source_results, temporal_profile` |
| 3 | `rank_papers` | success | `corpus_profile, coverage_gaps, ranked_candidates, research_lens, selected_papers` |
| 4 | `expand_search` | success | `actual_source, corpus_profile, coverage_gaps, expansion_rounds, fallback_reason, query_plan, ranked_candidates, research_lens, searched_papers, selected_papers, source_results, temporal_profile` |
| 5 | `extract_evidence` | success | `evidence_items, llm_chunk_count, llm_fallback_reason, llm_used` |
| 6 | `synthesize_claims` | success | `claim_graph, claims, evidence_matrix` |
| 7 | `check_citations` | success | `citation_checks` |
| 8 | `write_report` | success | `llm_fallback_reason, llm_used, report_markdown, report_path` |
| 9 | `evaluate_result` | success | `metrics` |

## Metrics

| Metric | Value |
| --- | --- |
| `query_count` | `9` |
| `query_angle_count` | `9` |
| `adjacent_query_count` | `2` |
| `searched_paper_count` | `32` |
| `selected_paper_count` | `3` |
| `candidate_limit` | `12` |
| `candidate_multiplier` | `8` |
| `from_year` | `2023` |
| `evidence_count` | `7` |
| `claim_count` | `2` |
| `citation_check_count` | `3` |
| `citation_check_pass_rate` | `1.0` |
| `claim_evidence_coverage` | `1.0` |
| `evidence_matrix_coverage` | `1.0` |
| `unsupported_claim_rate` | `0.0` |
| `hallucinated_reference_count` | `0` |
| `report_section_completeness` | `1.0` |
| `source_diversity` | `0.094` |
| `paper_type_diversity` | `1.0` |
| `coverage_gap_count` | `2` |
| `query_gap_recovery` | `0.7` |
| `node_trace_count` | `8` |
| `requested_source` | `openalex` |
| `actual_source` | `openalex` |
| `fallback_reason` | `` |
| `llm_provider` | `deepseek` |
| `llm_used` | `True` |
| `llm_fallback_reason` | `` |
| `llm_chunk_count` | `1` |
| `refine_topic` | `False` |
| `effective_topic` | `retrieval augmented generation for large language models` |
| `topic_refinement_used` | `False` |
| `topic_refinement_fallback_reason` | `` |
| `earliest_candidate_year` | `2023` |
| `latest_candidate_year` | `2026` |
| `recent_3_year_ratio` | `0.688` |
| `recent_5_year_ratio` | `1.0` |
| `research_lens_coverage` | `0.714` |
| `graph_runtime` | `sequential` |
| `dimension_scores` | `task_completion: 20.0, retrieval_quality: 18.55, evidence_trust: 25.0, report_quality: 20.0, agent_behavior: 15.0` |
| `overall_score` | `98.55` |
| `live_requirement_met` | `True` |
