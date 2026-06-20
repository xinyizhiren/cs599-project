const form = document.querySelector("#run-form");
const runButton = document.querySelector(".run-button");
const runList = document.querySelector("#run-list");
const stepList = document.querySelector("#step-list");
const statusChip = document.querySelector("#run-status");
const subtitle = document.querySelector("#run-subtitle");
const processCaption = document.querySelector("#process-caption");
const traceRuntime = document.querySelector("#trace-runtime");
const inspectorTitle = document.querySelector("#inspector-title");
const inspectorState = document.querySelector("#inspector-state");
const stepSummary = document.querySelector("#step-summary");
const stepStats = document.querySelector("#step-stats");
const queryPlan = document.querySelector("#query-plan");
const paperList = document.querySelector("#paper-list");
const evidenceList = document.querySelector("#evidence-list");
const paperCount = document.querySelector("#paper-count");
const evidenceCount = document.querySelector("#evidence-count");
const downloadStatus = document.querySelector("#download-status");
const refreshRuns = document.querySelector("#refresh-runs");
const downloadActions = document.querySelector(".download-actions");
const metricSources = document.querySelector("#metric-sources");
const metricQueries = document.querySelector("#metric-queries");
const metricReading = document.querySelector("#metric-reading");
const metricGaps = document.querySelector("#metric-gaps");
const resultTitle = document.querySelector("#result-title");
const resultBanner = document.querySelector(".result-banner");
const viewReportButton = document.querySelector("#view-report-button");
const exportCurrent = document.querySelector("#export-current");
const clearSession = document.querySelector("#clear-session");
const selectAllSources = document.querySelector("#select-all-sources");
const sourceInputs = Array.from(document.querySelectorAll('input[name="sources"]'));
const sourcesSummary = document.querySelector("#sources-summary");
const chatMessages = document.querySelector("#chat-messages");
const chatForm = document.querySelector("#chat-form");
const chatInput = document.querySelector("#chat-input");
const chatSend = document.querySelector("#chat-send");
const chatStatus = document.querySelector("#chat-status");
const quickActions = document.querySelector(".quick-actions");

let activeRun = null;
let selectedStepId = "understand_topic";
let pollTimer = null;

const DEFAULT_STEP_MILESTONES = [
  { id: "understand_topic", name: "理解主题", label: "", description: "", status: "idle", elapsed_ms: null },
  { id: "plan_queries", name: "生成查询计划", label: "", description: "", status: "idle", elapsed_ms: null },
  { id: "search_papers", name: "检索文献", label: "", description: "", status: "idle", elapsed_ms: null },
  { id: "rank_papers", name: "去重与聚类", label: "", description: "", status: "idle", elapsed_ms: null },
  { id: "read_full_text", name: "阅读与提炼", label: "", description: "", status: "idle", elapsed_ms: null },
  { id: "write_report", name: "生成报告", label: "", description: "", status: "idle", elapsed_ms: null },
  { id: "evaluate_result", name: "完成", label: "", description: "", status: "idle", elapsed_ms: null },
];

function apiPath(path) {
  return new URL(path, window.location.href).toString();
}

async function fetchJSON(path, options = {}) {
  const response = await fetch(apiPath(path), {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || `HTTP ${response.status}`);
  }
  return payload;
}

function shortId(id) {
  return id ? id.split("-").slice(0, 2).join("-") : "";
}

function setStatus(element, status) {
  element.textContent = status || "idle";
  element.className = element.className
    .split(" ")
    .filter((name) => !["idle", "queued", "running", "success", "failed", "error"].includes(name))
    .join(" ");
  element.classList.add(status || "idle");
}

function statusMark(status) {
  if (status === "success") return "✓";
  if (status === "running") return "⌕";
  if (status === "failed" || status === "error") return "!";
  if (status === "queued") return "…";
  return "○";
}

function escapeText(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => {
    const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" };
    return map[char];
  });
}

function formatMs(value) {
  if (value === null || value === undefined) return "";
  const number = Number(value);
  if (!Number.isFinite(number)) return "";
  if (number >= 60000) {
    const minutes = Math.floor(number / 60000);
    const seconds = Math.round((number % 60000) / 1000)
      .toString()
      .padStart(2, "0");
    return `${minutes}:${seconds}`;
  }
  if (number >= 1000) return `${(number / 1000).toFixed(2)} s`;
  return `${Math.round(number)} ms`;
}

function compactValue(value) {
  if (Array.isArray(value)) return value.join(", ");
  if (typeof value === "object" && value !== null) return JSON.stringify(value);
  return String(value ?? "");
}

function formatAuthors(authors) {
  if (Array.isArray(authors)) return authors.slice(0, 2).join(", ");
  return String(authors || "");
}

function selectedSources(run) {
  return run?.request?.sources || [run?.request?.source || "offline"];
}

function updateSourcesSummary() {
  if (!sourcesSummary) return;
  const selected = sourceInputs.filter((input) => input.checked).length;
  sourcesSummary.textContent = `已选择 ${selected} / ${sourceInputs.length} 个数据源`;
}

function getSelectedStep(run) {
  if (!run?.steps?.length) return null;
  return (
    run.steps.find((step) => step.id === selectedStepId) ||
    run.steps.find((step) => step.status === "running") ||
    run.steps[0]
  );
}

function renderRuns(runs = []) {
  if (!runs.length) {
    runList.innerHTML = '<div class="empty-state">暂无运行</div>';
    return;
  }

  runList.innerHTML = runs
    .map((run) => {
      const active = activeRun?.id === run.id ? " active" : "";
      const sources = selectedSources(run).join(" + ");
      return `
        <button class="run-item${active}" data-run-id="${escapeText(run.id)}" type="button">
          <strong>${escapeText(run.request.topic)}</strong>
          <span class="run-badge ${escapeText(run.status)}">${escapeText(run.status)}</span>
          <small>${escapeText(run.status)} / ${escapeText(sources)} / ${escapeText(shortId(run.id))}</small>
        </button>
      `;
    })
    .join("");
}

function markActiveRun(runId) {
  runList.querySelectorAll("[data-run-id]").forEach((button) => {
    button.classList.toggle("active", button.dataset.runId === runId);
  });
}

function renderSteps(run) {
  const milestoneIds = [
    "understand_topic",
    "plan_queries",
    "search_papers",
    "rank_papers",
    "read_full_text",
    "write_report",
    "evaluate_result",
  ];
  const sourceSteps = run?.steps?.length ? run.steps : DEFAULT_STEP_MILESTONES;
  stepList.className = `step-list ${run?.status || "idle"}`;
  const visibleSteps = milestoneIds
    .map((id) => sourceSteps.find((step) => step.id === id))
    .filter(Boolean);

  stepList.innerHTML = visibleSteps
    .map((step, index) => {
      const selected = run && step.id === selectedStepId ? " selected" : "";
      return `
        <li class="step-card ${escapeText(step.status)}${selected}" data-step-id="${escapeText(step.id)}">
          <div class="step-node">${statusMark(step.status)}</div>
          <div class="step-main">
            <div class="step-title">
              <strong>${escapeText(step.label || step.name)}</strong>
              <span>${escapeText(step.label)}</span>
            </div>
            <p class="step-summary">${escapeText(step.summary || step.description)}</p>
          </div>
          <div class="step-meta">
            <span>${escapeText(step.status)}</span>
            <span>${escapeText(formatMs(step.elapsed_ms))}</span>
          </div>
        </li>
      `;
    })
    .join("");
}

function renderInspector(run) {
  const step = getSelectedStep(run);
  if (!step) {
    inspectorTitle.textContent = "节点详情";
    setStatus(inspectorState, "idle");
    stepSummary.textContent = "选择一次运行后会显示节点输出。";
    stepStats.innerHTML = "";
    return;
  }

  inspectorTitle.textContent = step.label || step.name;
  setStatus(inspectorState, step.status);
  stepSummary.textContent = step.summary || step.description;

  const stats = { ...(step.stats || {}) };
  if (step.output_keys?.length) {
    stats.output_keys = step.output_keys;
  }
  stepStats.innerHTML = Object.entries(stats)
    .map(([key, value]) => `<dt>${escapeText(key)}</dt><dd>${escapeText(compactValue(value))}</dd>`)
    .join("");
}

function renderQueryPlan(run) {
  const queries = run?.snapshots?.query_plan || [];
  const queryTree = run?.snapshots?.query_tree || {};
  const coverageGaps = run?.snapshots?.coverage_gaps || [];
  const expansionRounds = run?.snapshots?.expansion_rounds || [];
  const evidenceMatrix = run?.snapshots?.evidence_matrix || [];
  const snowballRecords = run?.snapshots?.snowball_records || [];
  const readingNotes = run?.snapshots?.reading_notes || [];
  const readingBudget = run?.snapshots?.reading_budget || {};
  if (!queries.length && !(queryTree.branches || []).length) {
    queryPlan.className = "query-plan empty-state";
    queryPlan.textContent = "暂无数据";
    return;
  }
  queryPlan.className = "query-plan";
  const queryRows = queries
    .map(
      (query) => `
        <div class="query-row">
          <strong>${escapeText(query.query_id || query.source || "Q")}</strong>
          <p>${escapeText(query.query_text)}</p>
          <small>✓</small>
        </div>
      `,
    )
    .join("");
  const treeRows = (queryTree.branches || [])
    .slice(0, 5)
    .map((branch) => {
      const angles = [...new Set((branch.subtopics || []).map((item) => item.angle).filter(Boolean))];
      return `
        <div class="query-row">
          <strong>${escapeText(branch.question_id || "rq")}</strong>
          <p>${escapeText(branch.question || "")}</p>
          <small>✓</small>
        </div>
      `;
    })
    .join("");
  const gapRows = coverageGaps
    .slice(0, 6)
    .map(
      (gap) => `
        <div class="query-row">
          <strong>Gap</strong>
          <p>${escapeText(gap.reason || "")}</p>
          <small>!</small>
        </div>
      `,
    )
    .join("");
  const matrixRows = evidenceMatrix
    .slice(0, 5)
    .map(
      (row) => `
        <div class="query-row">
          <strong>${escapeText(row.question_id || "E")}</strong>
          <p>${escapeText(row.question || "")}</p>
          <small>✓</small>
        </div>
      `,
    )
    .join("");
  const expansionText = expansionRounds.length
    ? `<div class="query-row"><strong>EX</strong><p>补搜 ${escapeText(expansionRounds.length)} 轮，新增 ${escapeText(expansionRounds.map((item) => item.added_candidates || 0).join(" + "))} 条候选</p><small>✓</small></div>`
    : "";
  const snowballRows = snowballRecords
    .slice(0, 5)
    .map(
      (record) => `
        <div class="query-row">
          <strong>SB</strong>
          <p>${escapeText(record.seed_paper_id || "")}</p>
          <small>✓</small>
        </div>
      `,
    )
    .join("");
  const readingRows = readingNotes
    .slice(0, 5)
    .map(
      (note) => `
        <div class="query-row">
          <strong>R</strong>
          <p>${escapeText(note.summary || "")}</p>
          <small>✓</small>
        </div>
      `,
    )
    .join("");
  const readingText =
    readingBudget.attempted_papers !== undefined
      ? `<div class="query-row"><strong>FT</strong><p>全文阅读 ${escapeText(readingBudget.successful_papers || 0)} / ${escapeText(readingBudget.attempted_papers || 0)} 篇，${escapeText(run?.snapshots?.full_text_chunks?.length || 0)} 个片段</p><small>✓</small></div>`
      : "";
  queryPlan.innerHTML = `
    ${queryRows}
    ${treeRows ? `<h4>查询树</h4>${treeRows}` : ""}
    ${gapRows ? `<h4>覆盖缺口</h4>${gapRows}` : ""}
    ${expansionText}
    ${snowballRows ? `<h4>引用雪球</h4>${snowballRows}` : ""}
    ${readingText}
    ${readingRows ? `<h4>阅读笔记</h4>${readingRows}` : ""}
    ${matrixRows ? `<h4>证据矩阵</h4>${matrixRows}` : ""}
  `;
}

function renderPapers(run) {
  const papers = run?.snapshots?.selected_papers || [];
  paperCount.textContent = String(papers.length);
  if (!papers.length) {
    paperList.className = "paper-list empty-state";
    paperList.textContent = "暂无数据";
    return;
  }

  paperList.className = "paper-list";
  const rows = papers
    .slice(0, 8)
    .map(
      (paper, index) => `
        <tr>
          <td class="paper-index">${index + 1}</td>
          <td class="paper-title-cell">
            <a href="${escapeText(paper.url || "#")}" target="_blank" rel="noreferrer">
              ${escapeText(paper.title)}
            </a>
          </td>
          <td>${escapeText(formatAuthors(paper.authors) || "未知作者")}</td>
          <td>${escapeText(paper.source || "-")}</td>
          <td>${escapeText(paper.year || "-")}</td>
          <td>${Number(paper.score || 0).toFixed(2)}</td>
          <td>
            <span class="paper-actions" aria-label="论文操作">
              <svg class="icon"><use href="#icon-eye"></use></svg>
              <svg class="icon"><use href="#icon-doc"></use></svg>
              <svg class="icon"><use href="#icon-bookmark"></use></svg>
            </span>
          </td>
        </tr>
      `,
    )
    .join("");
  const end = Math.min(papers.length, 8);
  paperList.innerHTML = `
    <table class="paper-table">
      <thead>
        <tr>
          <th class="paper-index">#</th>
          <th>标题</th>
          <th>作者</th>
          <th>来源</th>
          <th>年份</th>
          <th>相关度</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
    <div class="table-footer">
      <span>显示 1-${end} 条，共 ${papers.length} 条</span>
      <span class="pager"><span class="active">1</span><span>2</span><span>3</span><span>›</span></span>
    </div>
  `;
}

function renderEvidence(run) {
  const evidence = run?.snapshots?.evidence_items || [];
  evidenceCount.textContent = String(evidence.length);
  if (!evidence.length) {
    evidenceList.className = "evidence-list empty-state";
    evidenceList.textContent = "暂无数据";
    return;
  }

  evidenceList.className = "evidence-list";
  evidenceList.innerHTML = evidence
    .slice(0, 8)
    .map(
      (item) => `
        <article class="evidence-row">
          <h3>${escapeText(item.category)} / ${escapeText(item.evidence_id)}</h3>
          <p>${escapeText(item.claim)}</p>
        </article>
      `,
    )
    .join("");
}

function renderOverview(run) {
  const snapshots = run?.snapshots || {};
  const queryCount =
    (snapshots.query_plan || []).length +
    ((snapshots.query_tree || {}).branches || []).reduce(
      (sum, branch) => sum + (branch.subtopics || []).length,
      0,
    );
  metricSources.textContent = run ? String(selectedSources(run).length) : "0";
  metricQueries.textContent = String(queryCount || 0);
  metricReading.textContent = String((snapshots.reading_notes || []).length);
  metricGaps.textContent = String((snapshots.coverage_gaps || []).length);
}

function updateDownloadButtons(run) {
  const documents = run?.snapshots?.documents || {};
  const readyCount = Object.values(documents).filter((document) => document?.ready).length;
  const reportReady = Boolean(documents.report?.ready);

  downloadActions.querySelectorAll("[data-download]").forEach((button) => {
    const document = documents[button.dataset.download];
    button.disabled = !document?.ready;
  });
  exportCurrent.disabled = !reportReady;
  viewReportButton.disabled = !reportReady;

  if (!run) {
    downloadStatus.textContent = "任务完成后可下载 Markdown 文件。";
  } else if (run.error) {
    downloadStatus.textContent = `Error: ${run.error}`;
  } else if (readyCount) {
    downloadStatus.textContent = `${readyCount} 个 Markdown 文件已生成，可直接下载。`;
  } else {
    downloadStatus.textContent = "任务运行中，Markdown 文件生成后会启用下载按钮。";
  }
}

function renderChat(run) {
  const messages = run?.messages || run?.snapshots?.conversation_messages || [];
  if (!messages.length) {
    chatMessages.className = "chat-messages empty-state";
    chatMessages.textContent = run?.status === "success" ? "可以继续提出调整要求。" : "任务完成后可以继续对话调整。";
  } else {
    chatMessages.className = "chat-messages";
    chatMessages.innerHTML = messages
      .map(
        (message) => `
          <article class="chat-message ${escapeText(message.role || "user")}">
            <strong>${escapeText(message.role || "user")}${message.action ? ` / ${escapeText(message.action)}` : ""}</strong>
            <p>${escapeText(message.content || "")}</p>
          </article>
        `,
      )
      .join("");
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  const ready = run?.status === "success" || run?.status === "failed";
  chatInput.disabled = !ready;
  chatSend.disabled = !ready;
  quickActions.querySelectorAll("button").forEach((button) => {
    button.disabled = !ready;
  });
  chatStatus.textContent = ready ? "会话已就绪，可以基于当前调研继续调整。" : "等待可继续的调研会话。";
}

function renderRun(run) {
  activeRun = run;
  markActiveRun(run?.id);
  const status = run?.status || "idle";
  setStatus(statusChip, status);
  resultBanner.className = `result-banner ${status}`;
  subtitle.textContent = run
    ? `${run.request.topic} / ${selectedSources(run).join(" + ")} / ${run.request.llm} / ${shortId(run.id)}`
    : "提交一个研究主题，查看可追踪的理解、检索、证据和报告生成流程。";
  processCaption.textContent = run?.current_step
    ? `正在执行 ${run.current_step}`
      : status === "success"
        ? "任务完成"
        : "等待任务开始";

  const papers = run?.snapshots?.selected_papers || [];
  const evidence = run?.snapshots?.evidence_items || [];
  if (!run) {
    resultTitle.textContent = "等待任务开始";
  } else if (status === "success") {
    resultTitle.textContent = "研究完成";
    processCaption.textContent = `共检索到 ${papers.length} 篇文献，沉淀 ${evidence.length} 条证据，使用 ${selectedSources(run).length} 个数据源。`;
  } else if (status === "running" || status === "queued") {
    resultTitle.textContent = "研究进行中";
  } else if (status === "failed" || status === "error") {
    resultTitle.textContent = "研究失败";
  } else {
    resultTitle.textContent = "等待任务开始";
  }

  const elapsed = (run?.snapshots?.node_trace || []).reduce(
    (sum, item) => sum + Number(item.elapsed_ms || 0),
    0,
  );
  traceRuntime.textContent = formatMs(elapsed) || "0 ms";

  if (run?.current_step) selectedStepId = run.current_step;
  renderSteps(run);
  renderInspector(run);
  renderQueryPlan(run);
  renderPapers(run);
  renderEvidence(run);
  renderOverview(run);
  updateDownloadButtons(run);
  renderChat(run);
}

async function refreshRunList() {
  const payload = await fetchJSON("./api/runs");
  renderRuns(payload.runs || []);
}

async function loadRun(runId) {
  const run = await fetchJSON(`./api/runs/${encodeURIComponent(runId)}`);
  renderRun(run);
  return run;
}

function startPolling(runId) {
  if (pollTimer) clearInterval(pollTimer);
  pollTimer = setInterval(async () => {
    try {
      const run = await fetchJSON(`./api/runs/${encodeURIComponent(runId)}`);
      renderRun(run);
      if (!["queued", "running"].includes(run.status)) {
        clearInterval(pollTimer);
        pollTimer = null;
        runButton.disabled = false;
        await refreshRunList();
      }
    } catch (error) {
      console.error(error);
      clearInterval(pollTimer);
      pollTimer = null;
      runButton.disabled = false;
    }
  }, 850);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  runButton.disabled = true;
  const formData = new FormData(form);
  const sources = formData.getAll("sources");
  const payload = {
    topic: formData.get("topic"),
    sources: sources.length ? sources : ["offline"],
    top_k: Number(formData.get("top_k")),
    from_year: Number(formData.get("from_year")),
    depth: Number(formData.get("depth")),
    breadth: Number(formData.get("breadth")),
    report_style: formData.get("report_style"),
    web_provider: formData.get("web_provider"),
    read_depth: formData.get("read_depth"),
    max_fulltext_papers: Number(formData.get("max_fulltext_papers")),
    reading_budget_chars: Number(formData.get("reading_budget_chars")),
    snowball: formData.get("snowball"),
    expansion_rounds: Number(formData.get("expansion_rounds")),
    summary_style: formData.get("summary_style"),
    require_live: formData.get("require_live") === "on",
    llm: formData.get("llm_deepseek") === "on" ? "deepseek" : "off",
    refine_topic: formData.get("refine_topic") === "on",
  };

  try {
    const run = await fetchJSON("./api/runs", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    selectedStepId = "understand_topic";
    renderRun(run);
    await refreshRunList();
    startPolling(run.id);
  } catch (error) {
    runButton.disabled = false;
    downloadStatus.textContent = `Error: ${error.message}`;
  }
});

runList.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-run-id]");
  if (!button) return;
  selectedStepId = "understand_topic";
  try {
    await loadRun(button.dataset.runId);
  } catch (error) {
    downloadStatus.textContent = `Error: ${error.message}`;
  }
});

stepList.addEventListener("click", (event) => {
  const card = event.target.closest("[data-step-id]");
  if (!card || !activeRun) return;
  selectedStepId = card.dataset.stepId;
  renderRun(activeRun);
});

refreshRuns.addEventListener("click", refreshRunList);

selectAllSources.addEventListener("click", () => {
  sourceInputs.forEach((input) => {
    input.checked = true;
  });
  updateSourcesSummary();
});

sourceInputs.forEach((input) => {
  input.addEventListener("change", updateSourcesSummary);
});

clearSession.addEventListener("click", () => {
  activeRun = null;
  selectedStepId = "understand_topic";
  renderRun(null);
  markActiveRun("");
});

function downloadReportIfReady() {
  if (!activeRun || exportCurrent.disabled) return;
  window.location.href = apiPath(`./api/runs/${encodeURIComponent(activeRun.id)}/download/report`);
}

exportCurrent.addEventListener("click", downloadReportIfReady);
viewReportButton.addEventListener("click", downloadReportIfReady);

downloadActions.addEventListener("click", (event) => {
  const button = event.target.closest("[data-download]");
  if (!button || !activeRun || button.disabled) return;
  const kind = button.dataset.download;
  window.location.href = apiPath(`./api/runs/${encodeURIComponent(activeRun.id)}/download/${kind}`);
});

updateDownloadButtons(null);
renderChat(null);
renderOverview(null);
renderSteps(null);
updateSourcesSummary();

async function sendChatMessage(message) {
  if (!activeRun || !message.trim()) return;
  chatSend.disabled = true;
  chatStatus.textContent = "Agent 正在处理调整...";
  try {
    const response = await fetchJSON(`./api/runs/${encodeURIComponent(activeRun.id)}/messages`, {
      method: "POST",
      body: JSON.stringify({ message }),
    });
    chatInput.value = "";
    renderRun(response.run);
    await refreshRunList();
    chatStatus.textContent = `已执行：${response.action}`;
  } catch (error) {
    chatStatus.textContent = `Error: ${error.message}`;
  } finally {
    chatSend.disabled = false;
  }
}

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  await sendChatMessage(chatInput.value);
});

quickActions.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-chat-prompt]");
  if (!button || button.disabled) return;
  await sendChatMessage(button.dataset.chatPrompt || "");
});

refreshRunList().catch((error) => {
  downloadStatus.textContent = `Error: ${error.message}`;
});
