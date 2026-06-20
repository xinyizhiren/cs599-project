# ResearchFlow

ResearchFlow 是一个证据可追溯的多智能体文献调研 Agent，面向研究生和科研初学者，自动完成论文检索、证据抽取、跨论文综合、引用校验和调研报告生成。

## 项目简介

用户输入研究主题后，ResearchFlow 会规划检索式、调用开放学术数据源获取候选论文，抽取贡献、方法、实验和局限等结构化证据，并生成带来源约束的中文 Markdown 文献调研报告。系统同时输出一份更面向阅读决策的中文综合总结，用来快速了解领域地图、关键共识、主要难点、可信度风险和后续追问方向。

本项目强调“可追溯、可复查、可复现”的 Agentic AI 工作流，避免普通大模型综述中常见的虚假引用和无依据结论。

## 方向

方向一：Agentic AI 原生开发。

## 技术栈

- AI IDE: Trae CN
- 语言: Python
- LLM: DeepSeek API / OpenAI API / Ollama 备用
- Agent 框架: LangGraph 可选；无依赖时使用顺序 graph fallback
- 工具调用: arXiv API, Semantic Scholar API, Crossref REST API, OpenAlex Works API, 可选 Tavily Web API
- 存储: SQLite，后续可扩展 Chroma / FAISS
- 测试: pytest
- 容器: Docker
- 版本管理: Git + GitHub

## 核心能力

- Query Planner：将研究主题拆解为检索关键词和检索策略。
- Paper Searcher：从 arXiv、Semantic Scholar、Crossref 等开放学术数据源召回候选论文。
- Paper Ranker：按相关性、年份、引用信息和去重规则筛选 Top-K 文献。
- Corpus Profiler：记录候选池规模、年份分布、近三年/近五年占比和领域覆盖。
- Evidence Extractor：抽取论文贡献、方法、实验、局限和结论。
- Full-Text Reader：可选读取公开 PDF/OA URL，将核心论文切分为 chunk 并生成 PaperReadingNote；失败时回退到摘要级证据。
- Snowball Searcher：基于 OpenAlex 从核心论文扩展参考文献和被引论文，提升深度调研召回。
- Research Synthesizer：生成主题分类、方法对比和研究空白。
- Citation Checker：校验引用元数据与 Claim-Evidence 对齐关系。
- Report Writer：生成结构化 Markdown 调研报告。
- Conversational Session：保存可恢复调研会话，支持在 Web 中继续对话调整范围、补充方向、过滤论文和重写摘要。

## 任务特有创新

- RAG-aware ranking：针对 RAG 主题提高标题短语、`RAG` 缩写、survey/review/benchmark/security 等信号权重，降低纯领域应用论文误排在前的概率。
- RAG Research Lens：将选中文献映射到 Survey & Taxonomy、Retrieval & Indexing、Generation & Grounding、Evaluation & Benchmarks、Security & Robustness、Graph & Structured RAG、Domain Applications 七个维度。
- Lens coverage：在报告和过程记录中输出 RAG 维度覆盖率和缺失维度，使“研究空白”不只是大模型生成文字，而是可审计的任务特定分析结果。
- Large-corpus compression：先检索较大的候选池，再用时间画像、领域 lens、Top-K 精排和分批 LLM 证据抽取压缩信息，缓解海量资料与上下文窗口有限之间的矛盾。
- Mixed Research Retrieval：`hybrid` 覆盖 arXiv、Semantic Scholar、Crossref、OpenAlex；`mixed` 进一步接入可选 Tavily Web 背景源，在无 Web Key 时自动跳过。
- Query Tree + Gap Recovery：把主题拆成 research questions、subtopics、query tree，并在发现综述/方法/评测/安全等方向缺失时自动补搜一轮。
- Evidence Matrix / Claim Graph：按“研究问题 × 文献 × 证据类型”组织证据，并把 claim、supporting evidence、limitations 和 confidence 显式连接起来。
- Open Full-Text Reading：只读取公开 PDF / OA URL，不绕过付费墙；通过 paper -> chunks -> PaperReadingNote -> question synthesis -> global synthesis 的层级压缩缓解上下文窗口限制。
- OpenAlex Snowball Search：从高相关核心论文出发做 backward references / forward citations 扩展，并把新增候选重新纳入 coverage-aware ranking。
- Full Chinese Report：默认生成完整中文调研报告，章节覆盖检索策略、时间分布、方法谱系、核心论文精读、方法对比、评测指标、结论证据、争议空白和未来方向。
- Fuzzy topic refinement：当用户只给出“RAG 怎么样”这类模糊主题时，可用 DeepSeek 将其修正为英文可检索学术主题，并生成研究问题、相邻主题和查询提示。
- Multi-angle adjacent search：查询计划不只包含完全贴合主题的检索式，还覆盖综述分类、方法系统、评测基准、开放问题、应用案例、安全鲁棒和相邻高相关方向。
- Conversational research loop：把一次性报告升级为可持续调研会话，后续指令会被分类为回答问题、重写报告、调整范围、扩展检索或过滤论文，并记录在过程报告中。

## 目录结构

```text
cs599-project/
├── docs/
│   ├── assets/                               # 架构图、截图、Demo 图片等
│   ├── project_plan.md                       # 项目执行规划
│   ├── researchflow_analysis_architecture.md # 选题分析与系统架构设计
│   ├── product_spec.md                       # Product Spec
│   ├── architecture_spec.md                  # Architecture Spec
│   └── api_spec.md                           # API Spec
├── examples/                                 # Demo 输入、样例报告和离线数据
├── src/
│   └── researchflow/                         # Agent 系统源码
├── tests/                                    # 自动化测试
├── README.md
├── .gitignore
└── LICENSE
```

## 环境搭建

### 1. 创建虚拟环境

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. 安装依赖

```powershell
pip install -e ".[dev]"
```

### 3. 配置环境变量

不要在代码中硬编码 API Key。请在本地创建 `.env` 文件或通过系统环境变量配置。`.env` 已被 `.gitignore` 忽略，不会提交到 GitHub：

```text
DEEPSEEK_API_KEY=your_deepseek_api_key
OPENAI_API_KEY=your_openai_api_key
SEMANTIC_SCHOLAR_API_KEY=optional_semantic_scholar_api_key
TAVILY_API_KEY=optional_tavily_web_search_key
OPENALEX_MAILTO=optional_email_for_openalex_polite_pool
RESEARCHFLOW_MODEL=deepseek-v4-flash
RESEARCHFLOW_LLM_TIMEOUT=30
```

MVP 阶段允许只使用公开论文 API 和离线样例数据运行基础流程。

### 4. 运行离线 Demo

```powershell
python -m researchflow run "Agentic RAG for enterprise knowledge management" --source offline --top-k 5 --output examples/reports/agentic_rag.md
```

离线模式使用内置样例论文，适合课堂 Demo 和断网兜底。

### 5. 运行真实联网调研报告

```powershell
python -m researchflow run "retrieval augmented generation for large language models" --source arxiv --require-live --top-k 15 --candidate-multiplier 8 --from-year 2020 --output docs/generated_reports/rag_live_literature_review.md --summary-output docs/generated_reports/rag_final_summary.md --process-output docs/generated_reports/rag_live_research_process.md
```

该命令会真实调用 arXiv API，先召回较大的候选池，再筛选核心文献，生成中文最终综合总结、中文 Markdown 文献调研报告和可审计调研过程记录。`--require-live` 会拒绝离线 fallback，避免把离线样例误认为联网调研。`--candidate-multiplier` 控制候选池规模，`--from-year` 控制时效窗口。当前仓库已包含生成样例：

- `docs/generated_reports/rag_live_literature_review.md`
- `docs/generated_reports/rag_final_summary.md`
- `docs/generated_reports/rag_live_research_process.md`

如果 arXiv 请求失败，系统会自动降级到离线样例，并在 metrics 中记录 fallback 原因。

### 6. 运行混合检索

```powershell
python -m researchflow run "agentic literature review agents" --source hybrid --top-k 5 --output docs/generated_reports/hybrid_literature_agents.md
```

`hybrid` 会同时尝试 arXiv、Semantic Scholar、Crossref 和 OpenAlex。arXiv 偏预印本和最新研究，Semantic Scholar 偏论文图谱和引用信息，Crossref 偏正式出版物、DOI 和出版社元数据，OpenAlex 用于补充正式论文、引用数和概念信息。Semantic Scholar 公共接口可能限流；如遇 429，系统会保留错误原因并尝试其他来源或 fallback。

### 6.1 运行 Deep Research 风格 mixed 调研

```powershell
python -m researchflow run "retrieval augmented generation for large language models" --source mixed --web-provider tavily --top-k 12 --max-candidates 120 --from-year 2020 --depth 2 --breadth 4 --report-style full --output docs/generated_reports/rag_mixed_full_report.md --summary-output docs/generated_reports/rag_mixed_summary.md --process-output docs/generated_reports/rag_mixed_process.md
```

`mixed` 表示学术源 + 可选 Web 背景源。若未配置 `TAVILY_API_KEY`，Web 源会自动跳过，不影响 arXiv / Semantic Scholar / Crossref / OpenAlex 调研。完整报告默认是中文长报告，过程记录会展示 query tree、source coverage、coverage gaps、expansion rounds、Evidence Matrix 和 Citation Check。

深度研究增强 Demo：

```powershell
python -m researchflow run "retrieval augmented generation for large language models" --source mixed --web-provider off --require-live --llm deepseek --top-k 12 --max-candidates 120 --from-year 2020 --depth 2 --breadth 4 --report-style full --read-depth auto --max-fulltext-papers 6 --reading-budget-chars 80000 --snowball both --expansion-rounds 1 --summary-style comprehensive --output docs/generated_reports/rag_deep_full_report.md --summary-output docs/generated_reports/rag_deep_summary.md --process-output docs/generated_reports/rag_deep_process.md
```

`--read-depth auto` 会尝试读取公开全文，失败时记录原因并回退摘要；`--snowball both` 会基于 OpenAlex 对核心论文做参考文献和被引论文扩展；`--summary-style comprehensive` 生成更完整的中文综合总结。

### 7. 运行 DeepSeek 增强模式

```powershell
$env:DEEPSEEK_API_KEY="your_deepseek_api_key"
python -m researchflow run "retrieval augmented generation for large language models" --source arxiv --require-live --llm deepseek --top-k 15 --candidate-multiplier 8 --from-year 2020 --output docs/generated_reports/rag_live_literature_review.md --summary-output docs/generated_reports/rag_final_summary.md --process-output docs/generated_reports/rag_live_research_process.md
```

DeepSeek 只用于证据抽取和报告背景段落润色。证据抽取会按批次处理核心论文，避免把大量摘要一次性塞进上下文窗口。若未配置 Key、网络超时或模型输出无法解析，系统会自动回退到规则实现，并在 metrics 中记录 `llm_fallback_reason`。过程记录输出的是可审计 Agent 行为，不包含大模型隐藏思考链。

OpenAlex + DeepSeek 轻量 smoke test：

```powershell
python -m researchflow run "retrieval augmented generation for large language models" --source openalex --require-live --llm deepseek --top-k 3 --max-candidates 12 --from-year 2023 --depth 2 --breadth 3 --report-style full --output docs/generated_reports/rag_openalex_deepseek_smoke.md --summary-output docs/generated_reports/rag_openalex_deepseek_summary.md --process-output docs/generated_reports/rag_openalex_deepseek_process.md
```

当前仓库已包含一次成功运行样例：`actual_source=openalex`，`llm_used=true`，用于证明真实学术源检索和 DeepSeek 证据抽取可以闭环。

### 8. 运行模糊主题修正与多角度调研

```powershell
python -m researchflow run "RAG 怎么样" --source hybrid --require-live --llm deepseek --refine-topic --top-k 12 --candidate-multiplier 8 --from-year 2020 --output docs/generated_reports/rag_fuzzy_hybrid_literature_review.md --summary-output docs/generated_reports/rag_fuzzy_hybrid_summary.md --process-output docs/generated_reports/rag_fuzzy_hybrid_process.md
```

`--refine-topic` 会先把模糊主题修正为可检索的学术主题，再生成核心查询、综述查询、方法查询、评测查询、问题查询、应用查询、安全查询和相邻主题查询。过程记录会显示 original topic、effective search topic、research questions、adjacent topics 和每条 query 的 angle/distance。

### 9. 运行 Web 对话式调研控制台

```powershell
python -m researchflow.web --host 127.0.0.1 --port 7860
```

Web 控制台支持初次调研、流程 trace、核心论文/证据查看、Markdown 下载，以及围绕同一份调研继续对话调整。会话会保存到 `data/sessions/{session_id}/`，包括 `state.json`、`messages.jsonl`、`report.md`、`summary.md`、`process.md` 和 `revision_history.jsonl`。当前对话动作包括补充方向、过滤论文、重写摘要、全文精读、引用雪球扩展和方法对比。

### 10. 运行评估

```powershell
python -m researchflow evaluate --benchmark examples/benchmarks/basic.jsonl --output examples/evaluation/results.json
```

评估会同时生成 `results.json` 和 `results.md`，指标包括综合得分、引用校验通过率、证据覆盖率、报告章节完整率和 Agent 节点 trace 完整度。

## 项目状态

- [x] Proposal
- [x] SDD Specs
- [x] MVP
- [x] Evaluation
- [x] 真实联网文献调研报告样例
- [x] 可审计调研过程记录
- [ ] Final Report

## 课程交付要求跟踪

- [x] GitHub 仓库命名为 `cs599-project`
- [x] Public Repository 包含开源协议文件
- [x] 包含 `docs/` 目录
- [x] 包含 `src/` 目录
- [x] 包含 README
- [x] 包含 `.gitignore`
- [x] 包含 Product / Architecture / API Spec 初稿
- [x] 包含本地 benchmark 与评估输出能力
- [ ] `docs/CS599_大作业报告.pdf`
- [ ] MVP tag: `v0.1`

## 参考资料

- Elicit: <https://elicit.com/>
- Semantic Scholar Academic Graph API: <https://www.semanticscholar.org/product/api>
- OpenAlex API: <https://developers.openalex.org/api-reference/introduction>
- arXiv API User Manual: <https://info.arxiv.org/help/api/user-manual.html>
- Crossref REST API: <https://www.crossref.org/documentation/retrieve-metadata/rest-api/>
- Crossref REST API Swagger: <https://api.crossref.org/swagger-ui/index.html>
- LangGraph: <https://langchain-ai.github.io/langgraph/>

## License

This project is licensed under the MIT License.
