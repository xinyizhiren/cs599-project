# ResearchFlow API Spec

版本：v0.1  
日期：2026-06-05

## 1. 接口范围

MVP 阶段提供命令行接口和内部 Python 接口。Final 阶段可扩展为 HTTP API 或 MCP 工具服务。

## 2. CLI 接口

### 2.1 运行调研任务

```powershell
python -m researchflow run "<topic>" --top-k 5 --output examples/reports/report.md
```

参数：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| topic | string | 是 | 无 | 研究主题 |
| --top-k | int | 否 | 5 | 最终选择论文数量 |
| --source | string | 否 | offline | 数据源，支持 offline、arxiv、semantic_scholar、hybrid |
| --output | path | 否 | examples/reports/{task_id}.md | 报告输出路径 |
| --process-output | path | 否 | 无 | 调研过程记录 Markdown 输出路径 |
| --offline | bool | 否 | false | 是否使用离线样例数据 |
| --require-live | bool | 否 | false | 联网源 fallback 到 offline 时返回失败 |
| --trace | bool | 否 | true | 是否保存 trace |
| --llm | string | 否 | off | 可选 LLM，支持 off 和 deepseek |

输出：

```text
Task ID: 20260605-agentic-rag
Status: success
Selected Papers: 5
Report: examples/reports/agentic_rag.md
Process: docs/generated_reports/rag_live_research_process.md
Trace: data/runtime/20260605-agentic-rag/trace.json
```

### 2.2 运行评估

```powershell
python -m researchflow evaluate --benchmark examples/benchmarks/basic.jsonl
```

参数：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| --benchmark | path | 是 | 无 | benchmark 文件路径 |
| --output | path | 否 | examples/evaluation/results.json | JSON 评估结果路径；系统同时生成同名 Markdown 报告 |

输出 JSON 摘要：

```json
{
  "task_count": 5,
  "success_count": 5,
  "average_score": 100.0,
  "results": []
}
```

### 2.3 查看版本

```powershell
python -m researchflow version
```

## 3. 环境变量

| 变量 | 必填 | 说明 |
| --- | --- | --- |
| DEEPSEEK_API_KEY | 否 | DeepSeek API Key |
| OPENAI_API_KEY | 否 | OpenAI API Key |
| SEMANTIC_SCHOLAR_API_KEY | 否 | Semantic Scholar API Key，可提高限额 |
| RESEARCHFLOW_MODEL | 否 | 默认模型名称 |
| RESEARCHFLOW_LLM_TIMEOUT | 否 | LLM 请求超时时间，默认 30 秒 |
| RESEARCHFLOW_CACHE_DIR | 否 | 缓存目录 |

规则：

- 代码不得硬编码 API Key。
- `.env` 文件不得提交到仓库。
- CLI 会自动读取本地 `.env`，但不会覆盖系统环境变量。
- 离线模式不需要任何 API Key。

## 4. 内部 Python 接口

### 4.1 run_research

```python
def run_research(
    topic: str,
    top_k: int = 5,
    source: str = "offline",
    output: str | None = None,
    process_output: str | None = None,
    offline: bool = False,
    llm: str = "off",
    require_live: bool = False,
) -> ResearchResult:
    ...
```

返回：

```python
class ResearchResult(BaseModel):
    task_id: str
    status: str
    selected_papers: list[PaperRecord]
    report_path: str
    process_path: str | None
    metrics: dict
```

### 4.2 evaluate_benchmark

```python
def evaluate_benchmark(
    benchmark_path: str,
    output_path: str | None = None,
) -> EvaluationSummary:
    ...
```

## 5. Tool 接口

### 5.1 search_papers

```python
def search_papers(query: QueryItem, limit: int = 20) -> list[PaperRecord]:
    ...
```

输入：

```json
{
  "query_id": "q1",
  "query_text": "agentic RAG enterprise knowledge management",
  "source": "arxiv",
  "filters": {
    "from_year": 2020,
    "category": "cs.AI"
  }
}
```

输出：

```json
[
  {
    "paper_id": "arxiv:2401.00001",
    "title": "Example Paper",
    "authors": ["A. Author"],
    "year": 2024,
    "abstract": "Paper abstract...",
    "url": "https://arxiv.org/abs/2401.00001",
    "doi": null,
    "arxiv_id": "2401.00001",
    "source": "arxiv"
  }
]
```

### 5.2 rank_papers

```python
def rank_papers(
    papers: list[PaperRecord],
    topic: str,
    top_k: int,
) -> list[PaperRecord]:
    ...
```

排序信号：

- 标题和摘要关键词匹配。
- 发表年份。
- DOI/arXiv ID 是否存在。
- 数据源可信度。
- 引用数，若数据源提供。

### 5.3 extract_evidence

```python
def extract_evidence(paper: PaperRecord) -> list[EvidenceItem]:
    ...
```

输出字段：

| 字段 | 说明 |
| --- | --- |
| evidence_id | 证据 ID |
| paper_id | 所属论文 |
| category | contribution, method, experiment, limitation, future_work |
| claim | 归纳后的证据陈述 |
| support_text | 原摘要或正文片段 |
| confidence | 置信度 |

### 5.4 check_citations

```python
def check_citations(
    papers: list[PaperRecord],
    claims: list[ClaimRecord],
) -> list[CitationCheck]:
    ...
```

检查项：

- 论文实体是否存在。
- DOI/arXiv ID 是否格式合理。
- claim 是否至少有一个 evidence_id。
- evidence_id 是否能映射到 PaperRecord。

### 5.5 write_report

```python
def write_report(
    topic: str,
    selected_papers: list[PaperRecord],
    evidence_items: list[EvidenceItem],
    synthesis: dict,
    citation_checks: list[CitationCheck],
    output_path: str,
) -> str:
    ...
```

输出 Markdown 结构：

```markdown
# Literature Review: {topic}

## 1. Research Background
## 2. Core Papers
## 3. Key Claims and Evidence
## 4. Method Taxonomy
## 5. Comparative Analysis
## 6. Research Gaps
## 7. Limitations of This Automated Review
## Citation Checks
## References
```

## 6. 数据 Schema

### 6.1 PaperRecord

```json
{
  "paper_id": "string",
  "title": "string",
  "authors": ["string"],
  "year": 2024,
  "abstract": "string",
  "url": "string",
  "doi": "string|null",
  "arxiv_id": "string|null",
  "source": "string",
  "citation_count": 0
}
```

### 6.2 EvidenceItem

```json
{
  "evidence_id": "string",
  "paper_id": "string",
  "category": "method",
  "claim": "string",
  "support_text": "string",
  "confidence": 0.8
}
```

### 6.3 ClaimRecord

```json
{
  "claim_id": "string",
  "claim_text": "string",
  "claim_type": "Fact|Synthesis|Hypothesis",
  "evidence_ids": ["string"]
}
```

### 6.4 CitationCheck

```json
{
  "check_id": "string",
  "paper_id": "string",
  "status": "passed|warning|failed",
  "message": "string"
}
```

## 7. 错误码

| 错误码 | 说明 | 处理 |
| --- | --- | --- |
| RF001 | 研究主题为空 | 返回参数错误 |
| RF002 | 论文 API 调用失败 | 重试或切换离线样例 |
| RF003 | 候选论文数量不足 | 回到 Query Planner 扩展检索式 |
| RF004 | LLM 输出解析失败 | 重试格式修复 |
| RF005 | 引用校验失败 | 标记低可信，不进入强结论 |
| RF006 | 报告写入失败 | 保存中间状态并返回错误 |

## 8. 评估指标

| 指标 | 说明 |
| --- | --- |
| overall_score | 100 分制综合分 |
| citation_check_pass_rate | 引用校验通过率 |
| claim_evidence_coverage | 有证据支持的 claim 比例 |
| unsupported_claim_rate | 无证据 claim 比例 |
| hallucinated_reference_count | 不来自候选论文的引用数量 |
| report_section_completeness | 报告章节完整率 |
| node_trace_count | Agent 节点 trace 数量 |
| graph_runtime | langgraph / sequential / sequential_fallback |
| llm_provider | off / deepseek |
| llm_used | 是否实际使用 LLM 输出 |
| llm_fallback_reason | LLM 降级原因 |
| research_lens_coverage | RAG Research Lens 维度覆盖率 |

## 9. 兼容性计划

MVP 使用 CLI 和内部 Python API。当前已实现 offline fixture、arXiv XML 解析/检索、Semantic Scholar JSON 解析/检索和 hybrid 多源检索；OpenAlex 和 Crossref 校验作为后续工具接入。后续可将 Tool 层暴露为 MCP server：

| MCP Tool | 对应内部函数 |
| --- | --- |
| researchflow.search_papers | search_papers |
| researchflow.extract_evidence | extract_evidence |
| researchflow.check_citations | check_citations |
| researchflow.write_report | write_report |
