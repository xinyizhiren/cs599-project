# ResearchFlow 项目工作规划

制定日期：2026-06-05  
项目仓库：cs599-project  
选题方向：方向一：Agentic AI 原生开发

## 1. 项目定位

ResearchFlow 是一个面向研究生和科研初学者的文献调研 Agent 系统。用户输入一个研究主题后，系统自动完成检索式规划、论文检索、相关性筛选、证据抽取、跨论文综合、引用校验和调研报告生成。

本项目的核心目标不是做一个普通的论文摘要工具，而是构建一个“证据可追溯、流程可复现、结果可评估”的多智能体文献调研工作流。

## 2. 课程要求映射

| 课程要求 | ResearchFlow 对应设计 |
| --- | --- |
| SDD 规格驱动开发 | 编写 Product Spec、Architecture Spec、API Spec，并用规格约束实现 |
| 工具使用 / Function Calling | 封装论文检索、元数据获取、PDF/摘要解析、引用检查、报告生成等工具 |
| 记忆机制 | 使用 SQLite 保存调研任务、论文元数据、证据片段和历史报告；后续可加入向量检索 |
| 状态管理与多步骤推理 | 使用 LangGraph 编排 ResearchGraph 状态流 |
| 多智能体协作 | Planner、Searcher、Reader、Extractor、Synthesizer、Citation Checker、Reporter 分工协作 |
| 可观测性与评估 | 记录每一步输入输出、耗时、工具调用结果，并设计 benchmark 任务集 |

## 3. MVP 范围

MVP 只解决一个可演示的闭环问题：

```text
输入研究主题
→ 生成检索关键词
→ 检索候选论文
→ 筛选 Top-K 文献
→ 提取结构化证据
→ 生成 Markdown 调研报告
→ 给出参考文献列表
```

MVP 阶段暂不追求大规模全文阅读，不做复杂 Web UI，不做多领域通用系统。优先保证流程完整、结果可解释、演示稳定。

## 4. 时间计划

### 2026-06-05：项目初始化与选题固化

- [x] 确定项目主题为 ResearchFlow 文献调研 Agent
- [x] 创建 GitHub 仓库 `cs599-project`
- [ ] 初始化仓库目录结构
- [ ] 创建 README、LICENSE、.gitignore
- [ ] 固化项目工作规划文档
- [ ] 固化市场分析、研究现状、问题难点、系统架构文档

交付物：

- `docs/project_plan.md`
- `docs/researchflow_analysis_architecture.md`
- 仓库基础结构

### 2026-06-06：SDD 规格设计

- [x] 编写 `docs/product_spec.md`
- [x] 编写 `docs/architecture_spec.md`
- [x] 编写 `docs/api_spec.md`
- [x] 明确系统输入输出格式
- [x] 明确 ResearchGraph 状态字段
- [x] 明确每个 Agent 节点的职责、输入、输出和失败处理方式
- [x] 实现 arXiv API 工具层与 XML 解析器
- [x] 将 source 路由接入 pipeline，并保留离线降级

交付物：

- Product Spec：用户画像、核心场景、功能边界、验收标准
- Architecture Spec：系统分层、Agent 协作、状态流、数据流
- API Spec：CLI/API 参数、工具接口、报告数据结构
- arXiv Tool：真实论文检索工具初版

### 2026-06-07 至 2026-06-10：核心闭环实现

- [x] 搭建 Python 项目结构
- [x] 实现配置管理，禁止硬编码 API Key
- [x] 实现论文检索工具，优先接入 arXiv
- [x] 实现候选论文去重、排序和 Top-K 筛选
- [x] 实现结构化证据抽取
- [x] 实现 Markdown 报告生成
- [x] 实现最小 graph 工作流，LangGraph 可用时优先使用，否则顺序 fallback
- [x] 实现本地 evaluator 和 100 分制评估指标

交付物：

- 可运行的命令行 Demo
- 示例输入主题
- 示例调研报告
- JSON/Markdown 评估输出

### 2026-06-08：MVP 提交

- [x] 完成 README 启动说明
- [x] 添加基础测试
- [ ] 准备 Demo 截图
- [x] 推送 GitHub
- [ ] 创建 `v0.1` tag

MVP 验收标准：

- 用户输入一个研究主题后，系统能生成一份结构化 Markdown 调研报告
- 报告至少包含 5 篇候选论文
- 每个核心结论至少关联一个论文来源
- 运行过程有日志或可追踪记录
- 仓库结构满足课程要求

### 2026-06-09 至 2026-06-16：增强与评估

- [ ] 加入 SQLite 研究记忆库
- [ ] 加入向量检索或全文片段检索
- [ ] 加入引用校验和 DOI/arXiv ID 校验
- [ ] 加入失败重试、限流、缓存和降级策略
- [ ] 设计 5-10 个 benchmark 调研任务
- [ ] 统计相关性、引用准确性、报告完整性、工具调用成功率
- [ ] 增加可观测日志或 tracing 视图

增强目标：

- 让 ResearchFlow 不只“生成报告”，还能够证明报告中的结论来自哪些论文证据
- 让系统输出可复查、可复现、可比较

### 2026-06-17 至 2026-06-21：报告与展示

- [ ] 完成 `docs/CS599_大作业报告.md`
- [ ] 转换为带导航目录的 PDF
- [ ] 绘制系统架构图、Agent 交互图、数据流图
- [ ] 补充关键代码截图和 AI IDE 使用截图
- [ ] 准备 5 分钟 Demo 讲稿
- [ ] 准备录屏作为 API 异常时的备用演示

最终报告章节：

1. 选题背景与设计思想
2. Specs 规格文档
3. 系统架构与设计
4. 关键实现与代码展示
5. 测试与评估
6. 系统升级与扩展
7. 课程总结

### 2026-06-22：最终提交

- [ ] 检查 GitHub 公开仓库是否可访问
- [ ] 检查 `LICENSE` 是否存在
- [ ] 检查无 API Key、Token、Cookie 泄露
- [ ] 检查最终 PDF 文件路径是否符合要求
- [ ] 推送最终版本
- [ ] 确认提交截止时间前完成交付

最终交付物：

- `README.md`
- `LICENSE`
- `.gitignore`
- `src/`
- `docs/CS599_大作业报告.pdf`
- `docs/architecture.md` 或等价架构文档
- 示例 Demo 输出和测试材料

## 5. 任务拆解

| 模块 | 主要职责 | 优先级 |
| --- | --- | --- |
| CLI/API 入口 | 接收研究主题、参数、输出路径 | P0 |
| ResearchGraph | 编排 Agent 节点和状态转移 | P0 |
| Query Planner | 将研究问题拆成检索关键词和检索式 | P0 |
| Paper Searcher | 调用论文检索 API 获取候选论文 | P0 |
| Paper Ranker | 去重、排序、筛选 Top-K 文献 | P0 |
| Evidence Extractor | 提取贡献、方法、实验、局限、结论 | P0 |
| Citation Checker | 校验引用是否能对应到真实论文元数据 | P1 |
| Report Writer | 生成结构化 Markdown 调研报告 | P0 |
| Memory Store | 保存论文、证据、报告和任务历史 | P1 |
| Evaluation | 运行 benchmark 并输出评估指标 | P1 |
| Web UI | 可视化调研过程和报告 | P2 |

## 6. 技术选型

| 类别 | 选择 |
| --- | --- |
| 语言 | Python |
| Agent 编排 | LangGraph |
| LLM | DeepSeek API / OpenAI API / Ollama 备用 |
| 论文检索 | arXiv API、Semantic Scholar API、OpenAlex API |
| 存储 | SQLite，后续可加入 Chroma 或 FAISS |
| 报告格式 | Markdown，最终报告可转 PDF |
| 测试 | pytest |
| 容器 | Docker |

## 7. 风险与应对

| 风险 | 影响 | 应对 |
| --- | --- | --- |
| API 不稳定或限流 | Demo 失败 | 加缓存、准备离线样例数据、提供 Ollama 备用 |
| LLM 生成虚假引用 | 影响可信度 | 引入 Citation Checker，报告中只允许引用检索结果中的论文 |
| 文献检索相关性不足 | 报告质量低 | Query Planner 生成多组检索式，Paper Ranker 二次排序 |
| 全文获取困难 | 无法深度阅读论文 | MVP 以标题、摘要、元数据为主，Final 阶段只处理开放获取全文 |
| 项目范围过大 | 赶不上节点 | MVP 聚焦命令行闭环，Web UI 和大规模检索放到扩展 |
| 报告不符合课程格式 | 影响评分 | 提前按课程七章结构编写，并确保 PDF 有导航目录 |

## 8. Demo 主题候选

优先选择 AI Agent 相关主题，既贴合课程，也容易找到近期论文。

- Agentic RAG for enterprise knowledge management
- Multi-agent collaboration in LLM systems
- LLM agents for software engineering
- Citation hallucination detection in scientific writing
- Long-term memory mechanisms for LLM agents

## 9. 当前最近行动

下一步优先完成以下事项：

1. 初始化仓库基础文件。
2. 编写三份 SDD 初稿。
3. 实现最小 CLI 闭环。
4. 准备一组离线样例数据，保证演示稳定。
5. 在 2026-06-08 前推送 `v0.1`。
