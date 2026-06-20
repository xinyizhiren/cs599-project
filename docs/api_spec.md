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
| --candidate-multiplier | int | 否 | 8 | 候选池规模倍数，候选池约为 top_k * multiplier |
| --max-candidates | int | 否 | 无 | 显式候选池上限，优先级高于 candidate multiplier |
| --from-year | int | 否 | 2020 | 候选论文起始年份；设为 0 可关闭年份过滤 |
| --source | string | 否 | offline | 数据源，支持 offline、arxiv、semantic_scholar、crossref、openalex、web、hybrid、mixed |
| --min-year | int | 否 | 2020 | `--from-year` 的别名 |
| --depth | int | 否 | 2 | Query tree 深度，控制 Deep Research 风格递归规划 |
| --breadth | int | 否 | 4 | 每层研究问题/子查询宽度 |
| --report-style | string | 否 | full | 报告风格，支持 full、summary、course；full 默认输出完整中文调研报告 |
| --web-provider | string | 否 | tavily | Web 检索提供方，支持 off、tavily；无 `TAVILY_API_KEY` 时自动跳过 |
| --read-depth | string | 否 | abstract | 阅读深度，支持 abstract、auto、fulltext；auto/fulltext 尝试读取公开 PDF/OA URL |
| --max-fulltext-papers | int | 否 | 6 | 单次任务最多尝试全文精读的核心论文数 |
| --reading-budget-chars | int | 否 | 80000 | 全文 chunk 与阅读笔记的字符预算 |
| --snowball | string | 否 | none | OpenAlex 引用雪球扩展，支持 none、backward、forward、both |
| --expansion-rounds | int | 否 | 1 | 覆盖缺口自动补搜轮数，0 表示关闭 |
| --summary-style | string | 否 | comprehensive | 总结详细度，支持 brief、comprehensive |
| --output | path | 否 | examples/reports/{task_id}.md | 报告输出路径 |
| --summary-output | path | 否 | 无 | 最终综合总结 Markdown 输出路径 |
| --process-output | path | 否 | 无 | 调研过程记录 Markdown 输出路径 |
| --offline | bool | 否 | false | 是否使用离线样例数据 |
| --require-live | bool | 否 | false | 联网源 fallback 到 offline 时返回失败 |
| --trace | bool | 否 | true | 是否保存 trace |
| --llm | string | 否 | off | 可选 LLM，支持 off 和 deepseek |
| --refine-topic | bool | 否 | false | 使用 LLM 将模糊主题修正为可检索学术主题，并生成相邻查询角度 |

输出：

```text
Task ID: 20260605-agentic-rag
Status: success
Selected Papers: 5
Report: examples/reports/agentic_rag.md
Summary: docs/generated_reports/rag_final_summary.md
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

### 2.4 Web 对话接口

启动：

```powershell
python -m researchflow.web --host 127.0.0.1 --port 7860
```

新增继续对话接口：

```http
POST /api/runs/{id}/messages
Content-Type: application/json

{
  "message": "多补充 security robustness 方向"
}
```

返回：

```json
{
  "reply": "已追加 `security_robustness` 方向检索并刷新候选池、核心论文和报告。",
  "action": "expand_search",
  "updated": true,
  "revision": {},
  "run": {},
  "snapshots": {}
}
```

`action` 支持 `answer_question`、`rewrite_report`、`adjust_scope`、`expand_search`、`filter_papers`、`regenerate_section`、`deepen_reading`、`add_snowball_search`、`compare_methods`、`rewrite_section`、`expand_question`。接口不返回隐藏推理链，只返回 action、回复和可审计 revision。

## 3. 环境变量

| 变量 | 必填 | 说明 |
| --- | --- | --- |
| DEEPSEEK_API_KEY | 否 | DeepSeek API Key |
| OPENAI_API_KEY | 否 | OpenAI API Key |
| SEMANTIC_SCHOLAR_API_KEY | 否 | Semantic Scholar API Key，可提高限额 |
| TAVILY_API_KEY | 否 | Tavily Web 检索 Key；未配置时 Web 源自动跳过 |
| OPENALEX_MAILTO | 否 | OpenAlex polite pool 邮箱标识 |
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
    summary_output: str | None = None,
    process_output: str | None = None,
    offline: bool = False,
    llm: str = "off",
    require_live: bool = False,
    candidate_multiplier: int = 8,
    max_candidates: int | None = None,
    from_year: int | None = 2020,
    refine_topic: bool = False,
    depth: int = 2,
    breadth: int = 4,
    report_style: str = "full",
    web_provider: str = "tavily",
    read_depth: str = "abstract",
    max_fulltext_papers: int = 6,
    reading_budget_chars: int = 80000,
    snowball: str = "none",
    expansion_rounds: int = 1,
    summary_style: str = "comprehensive",
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
    summary_path: str | None
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

### 4.3 会话接口

```python
def load_session(session_id: str) -> dict:
    ...

def save_session(state: ResearchState, messages: list[dict], artifacts: dict[str, str]) -> Path:
    ...

def handle_conversation_turn(state: ResearchState, user_message: str) -> dict:
    ...
```

会话文件位于 `data/sessions/{session_id}/`，包含 `state.json`、`messages.jsonl`、`report.md`、`summary.md`、`process.md` 和 `revision_history.jsonl`。

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
    "angle": "evaluation_benchmark",
    "distance": "direct"
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
    "source": "arxiv",
    "paper_type": "survey|benchmark|method|system|dataset|application|position|web_background|unknown"
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
# {topic}：中文文献调研报告

## 1. 摘要
## 2. 调研问题与检索策略
## 3. 文献覆盖与时间分布
## 4. 研究脉络与方法分类
## 5. 核心论文精读
## 6. 方法对比表
## 7. 数据集与评测指标
## 8. 主要结论与证据
## 9. 争议、局限与研究空白
## 10. 未来方向
## 11. 参考文献
## 12. 附录：Evidence Matrix 与调研过程
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
  "citation_count": 0,
  "paper_type": "survey|benchmark|method|system|dataset|application|position|web_background|unknown",
  "pdf_url": "string|null",
  "open_access_url": "string|null",
  "merged_sources": ["arxiv", "openalex"],
  "metadata_confidence": 0.88
}
```

### 6.2 FullTextChunk

```json
{
  "chunk_id": "string",
  "paper_id": "string",
  "text": "string",
  "source_url": "string",
  "section_hint": "abstract|introduction|method|experiment|evaluation|discussion|conclusion|body",
  "token_estimate": 600,
  "char_start": 0,
  "char_end": 2600
}
```

### 6.3 PaperReadingNote

```json
{
  "note_id": "string",
  "paper_id": "string",
  "status": "full_text|abstract_fallback|llm_full_text|llm_abstract",
  "summary": "string",
  "methods": ["string"],
  "experiments": ["string"],
  "limitations": ["string"],
  "future_work": ["string"],
  "evidence_chunk_ids": ["ft-paper-1"],
  "source": "full_text|abstract|llm",
  "fallback_reason": "string"
}
```

### 6.4 SnowballRecord

```json
{
  "seed_paper_id": "openalex:W123",
  "direction": "backward|forward",
  "added_paper_ids": ["openalex:W456"],
  "query_url": "string",
  "fallback_reason": "string"
}
```

### 6.5 EvidenceItem

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

### 6.6 ClaimRecord

```json
{
  "claim_id": "string",
  "claim_text": "string",
  "claim_type": "Fact|Synthesis|Hypothesis",
  "evidence_ids": ["string"]
}
```

### 6.7 CitationCheck

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
| llm_chunk_count | LLM 证据抽取批次数，用于观察上下文窗口分批策略 |
| source_diversity | 候选来源多样性 |
| paper_type_diversity | 核心论文类型多样性 |
| evidence_matrix_coverage | Evidence Matrix 覆盖核心论文比例 |
| reading_note_coverage | PaperReadingNote 覆盖核心论文比例 |
| full_text_chunk_count | 公开全文解析得到的 chunk 数量 |
| full_text_success_rate | 尝试全文读取的论文中成功读取比例 |
| snowball_record_count | 引用雪球检索记录数量 |
| snowball_added_candidate_count | 引用雪球新增候选论文数量 |
| research_memory_count | 本轮生成的研究记忆条目数量 |
| coverage_gap_count | 覆盖检测剩余缺口数 |
| query_gap_recovery | 覆盖缺口补搜恢复指标 |
| refine_topic | 是否启用模糊主题修正 |
| effective_topic | 实际用于检索和排序的主题 |
| topic_refinement_used | 是否成功使用 LLM 修正主题 |
| topic_refinement_fallback_reason | 主题修正降级原因 |
| query_angle_count | 查询计划覆盖的角度数量 |
| adjacent_query_count | 相邻主题或扩展角度查询数量 |
| research_lens_coverage | RAG Research Lens 维度覆盖率 |
| candidate_limit | 候选池目标规模 |
| candidate_multiplier | 候选池规模倍数 |
| from_year | 年份过滤起点 |
| earliest_candidate_year | 候选池最早年份 |
| latest_candidate_year | 候选池最新年份 |
| recent_3_year_ratio | 近三年候选论文占比 |
| recent_5_year_ratio | 近五年候选论文占比 |

## 9. 兼容性计划

MVP 使用 CLI 和内部 Python API。当前已实现 offline fixture、arXiv XML 解析/检索、Semantic Scholar JSON 解析/检索、Crossref DOI 元数据检索、OpenAlex Works 检索、可选 Tavily Web 检索，以及 hybrid/mixed 多源检索。后续可将 Tool 层暴露为 MCP server：

| MCP Tool | 对应内部函数 |
| --- | --- |
| researchflow.search_papers | search_papers |
| researchflow.extract_evidence | extract_evidence |
| researchflow.check_citations | check_citations |
| researchflow.write_report | write_report |
