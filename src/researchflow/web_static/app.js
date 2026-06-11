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
const reportPreview = document.querySelector("#report-preview");
const refreshRuns = document.querySelector("#refresh-runs");
const downloadActions = document.querySelector(".download-actions");

let activeRun = null;
let selectedStepId = "understand_topic";
let pollTimer = null;
let activeReportKey = "report_markdown";

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
  if (status === "running") return "●";
  if (status === "failed" || status === "error") return "!";
  if (status === "queued") return "…";
  return "·";
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
  if (number >= 1000) return `${(number / 1000).toFixed(2)} s`;
  return `${Math.round(number)} ms`;
}

function compactValue(value) {
  if (Array.isArray(value)) return value.join(", ");
  if (typeof value === "object" && value !== null) return JSON.stringify(value);
  return String(value ?? "");
}

function getSelectedStep(run) {
  if (!run?.steps?.length) return null;
  return run.steps.find((step) => step.id === selectedStepId) || run.steps.find((step) => step.status === "running") || run.steps[0];
}

function renderRuns(runs = []) {
  if (!runs.length) {
    runList.innerHTML = '<div class="empty-state">暂无运行</div>';
    return;
  }
  runList.innerHTML = runs
    .map((run) => {
      const active = activeRun?.id === run.id ? " active" : "";
      return `
        <button class="run-item${active}" data-run-id="${escapeText(run.id)}" type="button">
          <strong>${escapeText(run.request.topic)}</strong>
          <small>${escapeText(run.status)} · ${escapeText(shortId(run.id))}</small>
        </button>
      `;
    })
    .join("");
}

function renderSteps(run) {
  if (!run?.steps?.length) {
    stepList.innerHTML = "";
    return;
  }

  stepList.innerHTML = run.steps
    .map((step, index) => {
      const selected = step.id === selectedStepId ? " selected" : "";
      return `
        <li class="step-card ${escapeText(step.status)}${selected}" data-step-id="${escapeText(step.id)}">
          <div class="step-node">${statusMark(step.status)}</div>
          <div class="step-main">
            <div class="step-title">
              <strong>${index + 1}. ${escapeText(step.name)}</strong>
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
  if (!step) return;

  inspectorTitle.textContent = step.name;
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
  if (!queries.length) {
    queryPlan.className = "query-plan empty-state";
    queryPlan.textContent = "暂无数据";
    return;
  }
  queryPlan.className = "query-plan";
  queryPlan.innerHTML = queries
    .map(
      (query) => `
        <div class="query-row">
          <strong>${escapeText(query.query_id)} · ${escapeText(query.source)}</strong>
          <p>${escapeText(query.query_text)}</p>
        </div>
      `,
    )
    .join("");
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
  paperList.innerHTML = papers
    .map(
      (paper) => `
        <article class="paper-row">
          <h3>${escapeText(paper.title)}</h3>
          <p>${escapeText(paper.abstract || "").slice(0, 220)}</p>
          <div class="paper-meta">
            <span>${escapeText(paper.source)}</span>
            <span>${escapeText(paper.year)}</span>
            <span>score ${Number(paper.score || 0).toFixed(2)}</span>
            <span>${escapeText(paper.paper_id)}</span>
          </div>
        </article>
      `,
    )
    .join("");
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
          <h3>${escapeText(item.category)} · ${escapeText(item.evidence_id)}</h3>
          <p>${escapeText(item.claim)}</p>
        </article>
      `,
    )
    .join("");
}

function renderReport(run) {
  const text = run?.snapshots?.[activeReportKey] || "";
  const fallback = run?.error ? `Error: ${run.error}` : "暂无报告";
  reportPreview.textContent = text || fallback;
}

function renderRun(run) {
  activeRun = run;
  const status = run?.status || "idle";
  setStatus(statusChip, status);
  subtitle.textContent = run
    ? `${run.request.topic} · ${(run.request.sources || [run.request.source]).join(" + ")} · ${run.request.llm} · ${shortId(run.id)}`
    : "提交一个研究主题，查看可追踪的理解、检索、证据和报告生成流程。";
  processCaption.textContent = run?.current_step ? `正在执行 ${run.current_step}` : status === "success" ? "任务完成" : "等待任务开始";

  const elapsed = (run?.snapshots?.node_trace || []).reduce((sum, item) => sum + Number(item.elapsed_ms || 0), 0);
  traceRuntime.textContent = formatMs(elapsed) || "0 ms";

  if (run?.current_step) selectedStepId = run.current_step;
  renderSteps(run);
  renderInspector(run);
  renderQueryPlan(run);
  renderPapers(run);
  renderEvidence(run);
  renderReport(run);
  updateDownloadButtons(run);
}

function updateDownloadButtons(run) {
  const ready = run?.status === "success" || run?.status === "failed";
  downloadActions.querySelectorAll("[data-download]").forEach((button) => {
    button.disabled = !ready;
  });
}

async function refreshRunList() {
  const payload = await fetchJSON("./api/runs");
  renderRuns(payload.runs || []);
}

async function loadRun(runId) {
  const run = await fetchJSON(`./api/runs/${encodeURIComponent(runId)}`);
  renderRun(run);
  await refreshRunList();
  return run;
}

function startPolling(runId) {
  if (pollTimer) clearInterval(pollTimer);
  pollTimer = setInterval(async () => {
    try {
      const run = await loadRun(runId);
      if (!["queued", "running"].includes(run.status)) {
        clearInterval(pollTimer);
        pollTimer = null;
        runButton.disabled = false;
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
    require_live: formData.get("require_live") === "on",
    llm: formData.get("llm_deepseek") === "on" ? "deepseek" : "off",
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
    reportPreview.textContent = `Error: ${error.message}`;
  }
});

runList.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-run-id]");
  if (!button) return;
  selectedStepId = "understand_topic";
  await loadRun(button.dataset.runId);
});

stepList.addEventListener("click", (event) => {
  const card = event.target.closest("[data-step-id]");
  if (!card || !activeRun) return;
  selectedStepId = card.dataset.stepId;
  renderRun(activeRun);
});

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((item) => item.classList.remove("active"));
    tab.classList.add("active");
    activeReportKey = tab.dataset.report;
    renderReport(activeRun);
  });
});

refreshRuns.addEventListener("click", refreshRunList);

downloadActions.addEventListener("click", (event) => {
  const button = event.target.closest("[data-download]");
  if (!button || !activeRun || button.disabled) return;
  const kind = button.dataset.download;
  window.location.href = apiPath(`./api/runs/${encodeURIComponent(activeRun.id)}/download/${kind}`);
});

updateDownloadButtons(null);

refreshRunList().catch((error) => {
  reportPreview.textContent = `Error: ${error.message}`;
});
