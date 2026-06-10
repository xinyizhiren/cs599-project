# ResearchFlow

ResearchFlow 是一个证据可追溯的多智能体文献调研 Agent，面向研究生和科研初学者，自动完成论文检索、证据抽取、跨论文综合、引用校验和调研报告生成。

## 项目简介

用户输入研究主题后，ResearchFlow 会规划检索式、调用开放学术数据源获取候选论文，抽取贡献、方法、实验和局限等结构化证据，并生成带来源约束的 Markdown 文献调研报告。

本项目强调“可追溯、可复查、可复现”的 Agentic AI 工作流，避免普通大模型综述中常见的虚假引用和无依据结论。

## 方向

方向一：Agentic AI 原生开发。

## 技术栈

- AI IDE: Trae CN
- 语言: Python
- LLM: DeepSeek API / OpenAI API / Ollama 备用
- Agent 框架: LangGraph 可选；无依赖时使用顺序 graph fallback
- 工具调用: arXiv API, Semantic Scholar API；OpenAlex / Crossref 作为后续扩展
- 存储: SQLite，后续可扩展 Chroma / FAISS
- 测试: pytest
- 容器: Docker
- 版本管理: Git + GitHub

## 核心能力

- Query Planner：将研究主题拆解为检索关键词和检索策略。
- Paper Searcher：从开放学术数据源召回候选论文。
- Paper Ranker：按相关性、年份、引用信息和去重规则筛选 Top-K 文献。
- Evidence Extractor：抽取论文贡献、方法、实验、局限和结论。
- Research Synthesizer：生成主题分类、方法对比和研究空白。
- Citation Checker：校验引用元数据与 Claim-Evidence 对齐关系。
- Report Writer：生成结构化 Markdown 调研报告。

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
python -m researchflow run "retrieval augmented generation for large language models" --source arxiv --require-live --top-k 8 --output docs/generated_reports/rag_live_literature_review.md --process-output docs/generated_reports/rag_live_research_process.md
```

该命令会真实调用 arXiv API，生成一份 Markdown 文献调研报告和一份可审计调研过程记录。`--require-live` 会拒绝离线 fallback，避免把离线样例误认为联网调研。当前仓库已包含生成样例：

- `docs/generated_reports/rag_live_literature_review.md`
- `docs/generated_reports/rag_live_research_process.md`

如果 arXiv 请求失败，系统会自动降级到离线样例，并在 metrics 中记录 fallback 原因。

### 6. 运行混合检索

```powershell
python -m researchflow run "agentic literature review agents" --source hybrid --top-k 5 --output docs/generated_reports/hybrid_literature_agents.md
```

`hybrid` 会同时尝试 arXiv 和 Semantic Scholar。Semantic Scholar 公共接口可能限流；如遇 429，系统会保留错误原因并尝试其他来源或 fallback。

### 7. 运行 DeepSeek 增强模式

```powershell
$env:DEEPSEEK_API_KEY="your_deepseek_api_key"
python -m researchflow run "retrieval augmented generation for large language models" --source arxiv --require-live --llm deepseek --top-k 8 --output docs/generated_reports/rag_live_literature_review.md --process-output docs/generated_reports/rag_live_research_process.md
```

DeepSeek 只用于证据抽取和报告背景段落润色。若未配置 Key、网络超时或模型输出无法解析，系统会自动回退到规则实现，并在 metrics 中记录 `llm_fallback_reason`。过程记录输出的是可审计 Agent 行为，不包含大模型隐藏思考链。

### 8. 运行评估

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
- LangGraph: <https://langchain-ai.github.io/langgraph/>

## License

This project is licensed under the MIT License.
