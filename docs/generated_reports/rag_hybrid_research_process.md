# Research Process: retrieval augmented generation for large language models

This file records observable Agent actions and artifacts. It is not a hidden chain-of-thought transcript.

## Run Summary

- Task ID: `20260611091358-retrieval-augmented-generation-f`
- Requested source: `hybrid`
- Actual source: `hybrid`
- Candidate limit: `24`
- Candidate multiplier: `8`
- From year: `2020`
- Fallback reason: None
- Report path: `docs\generated_reports\rag_hybrid_literature_review.md`
- Summary path: `docs\generated_reports\rag_hybrid_summary.md`
- Graph runtime: `sequential`
- LLM provider: `off`
- LLM used: `false`
- LLM chunk count: `0`
- LLM fallback reason: LLM provider is disabled.

## Query Plan

| Query ID | Search Query | Source Intent | Filters |
| --- | --- | --- | --- |
| `q1` | retrieval augmented generation for large language models | hybrid | `{'from_year': 2020}` |
| `q2` | retrieval augmented generation large language models survey | hybrid | `{'from_year': 2020}` |
| `q3` | retrieval augmented generation large language models methods | hybrid | `{'from_year': 2020}` |
| `q4` | retrieval augmented generation large language models evaluation benchmark | hybrid | `{'from_year': 2020}` |
| `q5` | retrieval augmented generation large language models challenges limitations | hybrid | `{'from_year': 2020}` |

## Search Results

- Retrieved candidates before ranking: 24
- Candidate source counts: arxiv=12, crossref=12
- Candidate year range: 2023-2026
- Last 3 year ratio: 0.958
- Last 5 year ratio: 1.000

| Year | Candidate Count |
| ---: | ---: |
| 2023 | 1 |
| 2024 | 9 |
| 2025 | 11 |
| 2026 | 3 |

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
| 1 | `crossref:10.21203/rs.3.rs-6551928/v1` | Can Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) Generate New Knowledge for Urban Studies? | 2025 | crossref | 39.900 | https://doi.org/10.21203/rs.3.rs-6551928/v1 |
| 2 | `crossref:10.2139/ssrn.6761739` | AI-Powered Smart Advisory System for Precision Agriculture Using Large Language Models and Retrieval-Augmented Genera... | 2026 | crossref | 35.980 | https://doi.org/10.2139/ssrn.6761739 |
| 3 | `arxiv:2503.16581v1` | Investigating Retrieval-Augmented Generation in Quranic Studies: A Study of 13 Open-Source Large Language Models | 2025 | arxiv | 35.900 | http://arxiv.org/abs/2503.16581v1 |
| 4 | `crossref:10.31219/osf.io/ua6j5` | Retrieval Augmented Generation via Context Compression Techniques for Large Language Models | 2024 | crossref | 35.840 | https://doi.org/10.31219/osf.io/ua6j5 |
| 5 | `crossref:10.5121/csit.2025.150904` | Large Language Models in Clinical Advice: Direct Generation and Retrieval Augmented Generation vs Expert Advice | 2025 | crossref | 35.420 | https://doi.org/10.5121/csit.2025.150904 |
| 6 | `crossref:10.31219/osf.io/pv7r5` | Hallucination Reduction in Large Language Models with Retrieval-Augmented Generation Using Wikipedia Knowledge | 2024 | crossref | 35.400 | https://doi.org/10.31219/osf.io/pv7r5 |
| 7 | `crossref:10.36227/techrxiv.177272838.89432844/v1` | A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large Language Models | 2026 | crossref | 34.980 | https://doi.org/10.36227/techrxiv.177272838.89432844/v1 |
| 8 | `crossref:10.21203/rs.3.rs-4652959/v1` | Retrieval-Augmented Generation in Large Language Models through Selective Augmentation | 2024 | crossref | 34.340 | https://doi.org/10.21203/rs.3.rs-4652959/v1 |

## Research Lens

A domain-aware lens that checks whether selected RAG papers cover survey, retrieval, grounding, evaluation, security, structured RAG, and applications.

- Lens name: RAG Research Lens
- Coverage: 1.000
- Missing dimensions: None

| Dimension | Paper Count |
| --- | ---: |
| Domain Applications | 7 |
| Evaluation & Benchmarks | 7 |
| Generation & Grounding | 8 |
| Graph & Structured RAG | 1 |
| Retrieval & Indexing | 8 |
| Security & Robustness | 4 |
| Survey & Taxonomy | 2 |

| Paper ID | Lens Dimensions |
| --- | --- |
| `crossref:10.21203/rs.3.rs-6551928/v1` | Survey & Taxonomy, Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Domain Applications |
| `crossref:10.2139/ssrn.6761739` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Domain Applications |
| `arxiv:2503.16581v1` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Domain Applications |
| `crossref:10.31219/osf.io/ua6j5` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Security & Robustness, Domain Applications |
| `crossref:10.5121/csit.2025.150904` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Security & Robustness, Graph & Structured RAG, Domain Applications |
| `crossref:10.31219/osf.io/pv7r5` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Security & Robustness, Domain Applications |
| `crossref:10.36227/techrxiv.177272838.89432844/v1` | Survey & Taxonomy, Retrieval & Indexing, Generation & Grounding |
| `crossref:10.21203/rs.3.rs-4652959/v1` | Retrieval & Indexing, Generation & Grounding, Evaluation & Benchmarks, Security & Robustness, Domain Applications |

## Evidence Extraction

| Evidence ID | Paper ID | Category | Confidence | Claim |
| --- | --- | --- | ---: | --- |
| `e1-contribution` | `crossref:10.21203/rs.3.rs-6551928/v1` | contribution | 0.78 | Can Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) Generate New Knowledge for Urban Studies? contributes evidence about abstract retrieval-augmented gener... |
| `e1-limitation` | `crossref:10.21203/rs.3.rs-6551928/v1` | limitation | 0.62 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for Can Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) Generate... |
| `e2-contribution` | `crossref:10.2139/ssrn.6761739` | contribution | 0.78 | AI-Powered Smart Advisory System for Precision Agriculture Using Large Language Models and Retrieval-Augmented Generation contributes evidence about an ai-powered smart advisory... |
| `e2-limitation` | `crossref:10.2139/ssrn.6761739` | limitation | 0.62 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for AI-Powered Smart Advisory System for Precision Agriculture Using Large Language Mod... |
| `e3-contribution` | `arxiv:2503.16581v1` | contribution | 0.78 | Investigating Retrieval-Augmented Generation in Quranic Studies: A Study of 13 Open-Source Large Language Models contributes evidence about accurate and contextually faithful re... |
| `e3-limitation` | `arxiv:2503.16581v1` | limitation | 0.62 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for Investigating Retrieval-Augmented Generation in Quranic Studies: A Study of 13 Open... |
| `e4-contribution` | `crossref:10.31219/osf.io/ua6j5` | contribution | 0.78 | Retrieval Augmented Generation via Context Compression Techniques for Large Language Models contributes evidence about natural language processing has seen lots of improvements,... |
| `e4-limitation` | `crossref:10.31219/osf.io/ua6j5` | limitation | 0.62 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for Retrieval Augmented Generation via Context Compression Techniques for Large Languag... |
| `e5-contribution` | `crossref:10.5121/csit.2025.150904` | contribution | 0.78 | Large Language Models in Clinical Advice: Direct Generation and Retrieval Augmented Generation vs Expert Advice contributes evidence about the nhs faces mounting pressures, resu... |
| `e5-limitation` | `crossref:10.5121/csit.2025.150904` | limitation | 0.62 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for Large Language Models in Clinical Advice: Direct Generation and Retrieval Augmented... |
| `e6-contribution` | `crossref:10.31219/osf.io/pv7r5` | contribution | 0.78 | Hallucination Reduction in Large Language Models with Retrieval-Augmented Generation Using Wikipedia Knowledge contributes evidence about natural language understanding and gene... |
| `e6-limitation` | `crossref:10.31219/osf.io/pv7r5` | limitation | 0.62 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for Hallucination Reduction in Large Language Models with Retrieval-Augmented Generatio... |
| `e7-contribution` | `crossref:10.36227/techrxiv.177272838.89432844/v1` | contribution | 0.78 | A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large Language Models contributes evidence about crossref metadata record for posted content. |
| `e7-limitation` | `crossref:10.36227/techrxiv.177272838.89432844/v1` | limitation | 0.62 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for A Survey of (Deep RAG) Deep Retrieval Augmented Generation and Reasoning in Large L... |
| `e8-contribution` | `crossref:10.21203/rs.3.rs-4652959/v1` | contribution | 0.78 | Retrieval-Augmented Generation in Large Language Models through Selective Augmentation contributes evidence about abstract the increasing complexity and demands of natural langu... |
| `e8-limitation` | `crossref:10.21203/rs.3.rs-4652959/v1` | limitation | 0.62 | The current MVP only sees metadata and abstracts, so full-text validation is still needed for Retrieval-Augmented Generation in Large Language Models through Selective Augmentat... |

## Claim-Evidence Alignment

| Claim ID | Type | Claim | Evidence IDs |
| --- | --- | --- | --- |
| `c1` | Synthesis | Research on retrieval augmented generation for large language models is moving from single-step generation toward tool-using, evidence-grounded workflows. | `e1-contribution`, `e2-contribution`, `e3-contribution`, `e4-contribution` |
| `c2` | Hypothesis | A promising research gap is to make the literature review process auditable through claim-evidence alignment and citation checking. | `e1-limitation`, `e2-limitation`, `e3-limitation` |

## Citation Checks

| Check ID | Paper ID | Status | Message |
| --- | --- | --- | --- |
| `check-1` | `crossref:10.21203/rs.3.rs-6551928/v1` | passed | Citation metadata is available. |
| `check-2` | `crossref:10.2139/ssrn.6761739` | passed | Citation metadata is available. |
| `check-3` | `arxiv:2503.16581v1` | passed | Citation metadata is available. |
| `check-4` | `crossref:10.31219/osf.io/ua6j5` | passed | Citation metadata is available. |
| `check-5` | `crossref:10.5121/csit.2025.150904` | passed | Citation metadata is available. |
| `check-6` | `crossref:10.31219/osf.io/pv7r5` | passed | Citation metadata is available. |
| `check-7` | `crossref:10.36227/techrxiv.177272838.89432844/v1` | passed | Citation metadata is available. |
| `check-8` | `crossref:10.21203/rs.3.rs-4652959/v1` | passed | Citation metadata is available. |

## Agent Trace

| Step | Node | Status | Output Keys |
| ---: | --- | --- | --- |
| 1 | `plan_queries` | success | `query_plan` |
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
| `query_count` | `5` |
| `searched_paper_count` | `24` |
| `selected_paper_count` | `8` |
| `candidate_limit` | `24` |
| `candidate_multiplier` | `8` |
| `from_year` | `2020` |
| `evidence_count` | `16` |
| `claim_count` | `2` |
| `citation_check_count` | `8` |
| `citation_check_pass_rate` | `1.0` |
| `claim_evidence_coverage` | `1.0` |
| `unsupported_claim_rate` | `0.0` |
| `hallucinated_reference_count` | `0` |
| `report_section_completeness` | `1.0` |
| `node_trace_count` | `7` |
| `requested_source` | `hybrid` |
| `actual_source` | `hybrid` |
| `fallback_reason` | `` |
| `llm_provider` | `off` |
| `llm_used` | `False` |
| `llm_fallback_reason` | `LLM provider is disabled.` |
| `llm_chunk_count` | `0` |
| `earliest_candidate_year` | `2023` |
| `latest_candidate_year` | `2026` |
| `recent_3_year_ratio` | `0.958` |
| `recent_5_year_ratio` | `1.0` |
| `research_lens_coverage` | `1.0` |
| `graph_runtime` | `sequential` |
| `dimension_scores` | `task_completion: 20.0, retrieval_quality: 20.0, evidence_trust: 25.0, report_quality: 20.0, agent_behavior: 15.0` |
| `overall_score` | `100.0` |
| `live_requirement_met` | `True` |
