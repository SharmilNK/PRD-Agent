// PRD-Agent dashboard. Plain JavaScript, no build step.
// All text from data.json is AI output or file content: it is inserted with textContent, never innerHTML
// (the PRD viewer is the one exception, and it goes through DOMPurify).

const SVG_NS = "http://www.w3.org/2000/svg";
const STATUS = {
  go: ["Go", "--good"], pivot: ["Pivot", "--warning"], no_go: ["No-Go", "--critical"],
  pass: ["Pass", "--good"], fail: ["Fail", "--critical"],
  allow: ["Allow", "--good"], warn: ["Warn", "--warning"], block: ["Block", "--critical"],
  completed: ["Completed", "--good"], blocked: ["Blocked", "--critical"],
  critical: ["Critical", "--critical"], major: ["Major", "--serious"],
};
let DATA = null;

// ---------- small helpers ----------
const $ = (id) => document.getElementById(id);
function el(tag, attrs = {}, text) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  if (text !== undefined) node.textContent = text;
  return node;
}
function svg(tag, attrs = {}, text) {
  const node = document.createElementNS(SVG_NS, tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  if (text !== undefined) node.textContent = text;
  return node;
}
function badge(key) {
  const [label, color] = STATUS[key] || [key ?? "-", "--text-muted"];
  const span = el("span", { class: "badge" }, label);
  span.style.setProperty("--c", `var(${color})`);
  return span;
}
const money = (v) => (v == null ? "-" : `$${v.toFixed(2)}`);
const runDate = (id) => `${id.slice(4, 6)}/${id.slice(6, 8)} ${id.slice(9, 11)}:${id.slice(11, 13)}`;

// ---------- tooltip (hover and keyboard focus) ----------
function showTip(evt, rows) {
  const tip = $("tooltip");
  tip.replaceChildren();
  for (const [k, v, strong] of rows) {
    const line = el("div");
    if (strong) line.append(el("div", { class: "v" }, v), el("div", { class: "k" }, k));
    else line.append(el("span", { class: "k" }, `${k}: `), document.createTextNode(v));
    tip.append(line);
  }
  tip.hidden = false;
  const r = evt.target.getBoundingClientRect?.() || { left: 0, top: 0 };
  const x = evt.clientX ?? r.left + 10, y = evt.clientY ?? r.top;
  tip.style.left = `${Math.min(x + 14, window.innerWidth - tip.offsetWidth - 8)}px`;
  tip.style.top = `${Math.max(8, y - tip.offsetHeight - 10)}px`;
}
const hideTip = () => { $("tooltip").hidden = true; };
function hoverable(node, rows) {
  node.setAttribute("tabindex", "0");
  node.setAttribute("class", `${node.getAttribute("class") || ""} mark`);
  node.setAttribute("aria-label", rows.map(([k, v]) => `${k} ${v}`).join(", "));
  node.addEventListener("pointermove", (e) => showTip(e, rows));
  node.addEventListener("pointerleave", hideTip);
  node.addEventListener("focus", (e) => showTip(e, rows));
  node.addEventListener("blur", hideTip);
}
function note(container, text) { container.replaceChildren(el("p", { class: "note" }, text)); }

// ---------- charts ----------
// Vertical bars, one series (cost per run).
function barChart(container, items, { format, max }) {
  if (!items.length) return note(container, "No runs yet.");
  const W = container.clientWidth || 480, H = 200, m = { t: 12, r: 8, b: 26, l: 44 };
  const top = max || Math.max(...items.map((d) => d.value)) * 1.15 || 1;
  const s = svg("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Bar chart" });
  for (let i = 0; i <= 4; i++) {
    const v = (top / 4) * i, y = H - m.b - ((H - m.t - m.b) * v) / top;
    s.append(svg("line", { x1: m.l, x2: W - m.r, y1: y, y2: y, class: i ? "gridline" : "baseline" }));
    s.append(svg("text", { x: m.l - 6, y: y + 4, "text-anchor": "end" }, format(v)));
  }
  const band = (W - m.l - m.r) / items.length, bw = Math.max(4, Math.min(48, band - 2));
  items.forEach((d, i) => {
    const h = ((H - m.t - m.b) * d.value) / top, x = m.l + band * i + (band - bw) / 2, y = H - m.b - h;
    const bar = svg("path", { d: roundedTop(x, y, bw, h, Math.min(4, bw / 2)), fill: "var(--series-1)" });
    hoverable(bar, d.tip);
    s.append(bar);
    if (items.length <= 12) s.append(svg("text", { x: x + bw / 2, y: H - m.b + 16, "text-anchor": "middle" }, d.label));
  });
  container.replaceChildren(s);
}
function roundedTop(x, y, w, h, r) {
  if (h <= 0) return "";
  r = Math.min(r, h);
  return `M${x},${y + h}V${y + r}Q${x},${y} ${x + r},${y}H${x + w - r}Q${x + w},${y} ${x + w},${y + r}V${y + h}Z`;
}

// Line with markers, one series, fixed 1-5 scale, crosshair tooltip (rubric per run).
function lineChart(container, items, { ref }) {
  const pts = items.filter((d) => d.value != null);
  if (!pts.length) return note(container, "No reviewed runs yet.");
  const W = container.clientWidth || 480, H = 200, m = { t: 12, r: 12, b: 26, l: 32 };
  const x = (i) => m.l + (pts.length === 1 ? (W - m.l - m.r) / 2 : ((W - m.l - m.r) * i) / (pts.length - 1));
  const y = (v) => H - m.b - ((H - m.t - m.b) * (v - 1)) / 4;
  const s = svg("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Line chart" });
  for (let v = 1; v <= 5; v++) {
    s.append(svg("line", { x1: m.l, x2: W - m.r, y1: y(v), y2: y(v), class: v === 1 ? "baseline" : "gridline" }));
    s.append(svg("text", { x: m.l - 6, y: y(v) + 4, "text-anchor": "end" }, String(v)));
  }
  s.append(svg("line", { x1: m.l, x2: W - m.r, y1: y(ref), y2: y(ref), class: "refline" }));
  s.append(svg("path", {
    d: pts.map((d, i) => `${i ? "L" : "M"}${x(i)},${y(d.value)}`).join(""),
    fill: "none", stroke: "var(--series-1)", "stroke-width": 2, "stroke-linejoin": "round",
  }));
  const cross = svg("line", { y1: m.t, y2: H - m.b, class: "crosshair", visibility: "hidden" });
  s.append(cross);
  pts.forEach((d, i) => {
    s.append(svg("circle", { cx: x(i), cy: y(d.value), r: 4, fill: "var(--series-1)", stroke: "var(--surface-1)", "stroke-width": 2 }));
    // Edge labels anchor inward so they never spill past the chart.
    const anchor = pts.length === 1 ? "middle" : i === 0 ? "start" : i === pts.length - 1 ? "end" : "middle";
    if (pts.length <= 12) s.append(svg("text", { x: x(i), y: H - m.b + 16, "text-anchor": anchor }, d.label));
  });
  // Crosshair: snap to the nearest run, so the reader aims at a run, not a 2px line.
  const hit = svg("rect", { x: m.l, y: m.t, width: W - m.l - m.r, height: H - m.t - m.b, fill: "transparent" });
  hit.addEventListener("pointermove", (e) => {
    const box = s.getBoundingClientRect(), px = ((e.clientX - box.left) / box.width) * W;
    let best = 0;
    pts.forEach((_, i) => { if (Math.abs(x(i) - px) < Math.abs(x(best) - px)) best = i; });
    cross.setAttribute("x1", x(best)); cross.setAttribute("x2", x(best)); cross.setAttribute("visibility", "visible");
    showTip(e, pts[best].tip);
  });
  hit.addEventListener("pointerleave", () => { cross.setAttribute("visibility", "hidden"); hideTip(); });
  s.append(hit);
  container.replaceChildren(s);
}

// Horizontal bars on a fixed 1-5 scale, one series (scorecard).
function hbarChart(container, items, { ref }) {
  if (!items.length) return note(container, "No scorecard yet (the debate and Scorer have not run).");
  const W = container.clientWidth || 480, row = 26, m = { t: 6, r: 28, b: 22, l: 150 };
  const H = m.t + m.b + row * items.length, x = (v) => m.l + ((W - m.l - m.r) * v) / 5;
  const s = svg("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Horizontal bar chart" });
  for (let v = 0; v <= 5; v++) {
    s.append(svg("line", { x1: x(v), x2: x(v), y1: m.t, y2: H - m.b, class: v ? "gridline" : "baseline" }));
    s.append(svg("text", { x: x(v), y: H - 6, "text-anchor": "middle" }, String(v)));
  }
  items.forEach((d, i) => {
    const y = m.t + row * i + 4, h = row - 8, w = x(d.value) - x(0);
    s.append(svg("text", { x: m.l - 8, y: y + h / 2 + 4, "text-anchor": "end" }, d.label));
    const bar = svg("path", { d: roundedRight(x(0), y, w, h, 4), fill: "var(--series-1)" });
    hoverable(bar, [[d.label, `${d.value} / 5`, true]]);
    s.append(bar);
    s.append(svg("text", { x: x(d.value) + 6, y: y + h / 2 + 4, class: "value" }, String(d.value)));
  });
  s.append(svg("line", { x1: x(ref), x2: x(ref), y1: m.t, y2: H - m.b, class: "refline" }));
  container.replaceChildren(s);
}
function roundedRight(x, y, w, h, r) {
  if (w <= 0) return "";
  r = Math.min(r, w, h / 2);
  return `M${x},${y}H${x + w - r}Q${x + w},${y} ${x + w},${y + r}V${y + h - r}Q${x + w},${y + h} ${x + w - r},${y + h}H${x}Z`;
}

// Horizontal bars with their own scale, one series (cost per agent).
function hbarValues(container, items, { format }) {
  if (!items.length) return note(container, "No runs yet.");
  const W = container.clientWidth || 480, row = 26, m = { t: 6, r: 56, b: 6, l: 150 };
  const H = m.t + m.b + row * items.length, top = Math.max(...items.map((d) => d.value)) || 1;
  const x = (v) => m.l + ((W - m.l - m.r) * v) / top;
  const s = svg("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Horizontal bar chart" });
  s.append(svg("line", { x1: x(0), x2: x(0), y1: m.t, y2: H - m.b, class: "baseline" }));
  items.forEach((d, i) => {
    const y = m.t + row * i + 4, h = row - 8;
    s.append(svg("text", { x: m.l - 8, y: y + h / 2 + 4, "text-anchor": "end" }, d.label));
    const bar = svg("path", { d: roundedRight(x(0), y, x(d.value) - x(0), h, 4), fill: "var(--series-1)" });
    hoverable(bar, d.tip);
    s.append(bar);
    s.append(svg("text", { x: x(d.value) + 6, y: y + h / 2 + 4, class: "value" }, format(d.value)));
  });
  container.replaceChildren(s);
}

function opsTable(ops) {
  const t = $("ops");
  t.replaceChildren();
  const head = el("tr");
  for (const h of ["Agent", "Calls", "p50 time", "p95 time", "Avg cost", "Errors", "Cache hit"]) head.append(el("th", { scope: "col" }, h));
  const thead = el("thead");
  thead.append(head);
  const body = el("tbody");
  for (const a of ops?.agents || []) {
    const tr = el("tr");
    const cells = [a.agent, a.calls, `${a.p50_s}s`, `${a.p95_s}s`, money(a.avg_cost_usd),
      `${Math.round(a.error_rate * 100)}%`, `${Math.round(a.cache_hit_rate * 100)}%`];
    cells.forEach((c, i) => tr.append(el("td", i ? { class: "num" } : {}, String(c))));
    body.append(tr);
  }
  t.append(thead, body);
}

// One stacked bar, ordinal grades A-D (source quality), with legend and direct labels.
function gradeBar(container, grades) {
  const total = Object.values(grades || {}).reduce((a, b) => a + b, 0);
  if (!total) return note(container, "No research claims in the latest run.");
  const W = container.clientWidth || 480, H = 44, gap = 2;
  const s = svg("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Source grades" });
  const names = { A: "A official", B: "B respected", C: "C community", D: "D unknown" };
  let x = 0;
  for (const g of ["A", "B", "C", "D"]) {
    const n = grades[g] || 0;
    if (!n) continue;
    const w = (W * n) / total - gap;
    const seg = svg("rect", { x, y: 4, width: Math.max(1, w), height: 22, rx: 4, fill: `var(--ord-${g.toLowerCase()})` });
    hoverable(seg, [[names[g], `${n} claim${n === 1 ? "" : "s"}`, true], ["Share", `${Math.round((100 * n) / total)}%`]]);
    s.append(seg);
    if (w > 28) s.append(svg("text", { x: x + w / 2, y: 42, "text-anchor": "middle", class: "value" }, `${g}: ${n}`));
    x += w + gap;
  }
  const legend = el("div", { class: "legend" });
  for (const g of ["A", "B", "C", "D"]) {
    const item = el("span");
    const sw = el("i");
    sw.style.background = `var(--ord-${g.toLowerCase()})`;
    item.append(sw, document.createTextNode(`${names[g]} (${grades[g] || 0})`));
    legend.append(item);
  }
  container.replaceChildren(s, legend);
}

// ---------- page sections ----------
function kpis(runs, latestByTranscript) {
  const box = $("kpis");
  box.replaceChildren();
  const latest = Object.values(latestByTranscript);
  const passed = latest.filter((r) => r.quality_gate === "pass").length;
  const total = runs.reduce((a, r) => a + (r.cost_usd || 0), 0);
  const tiles = [
    ["Runs", String(runs.length), `${latest.length} transcript${latest.length === 1 ? "" : "s"}`],
    ["Quality gate passed", `${passed} / ${latest.length}`, "latest run per transcript"],
    ["Latest verdict", null, runs[0] ? runs[0].transcript : "-", runs[0]?.verdict],
    ["Average cost per run", money(runs.length ? total / runs.length : null), "tokens + web searches"],
    ["Total cost", money(total), "all runs shown"],
  ];
  for (const [label, value, sub, status] of tiles) {
    const t = el("div", { class: "kpi" });
    const v = el("div", { class: "value" });
    if (status !== undefined) v.append(status ? badge(status) : document.createTextNode("-"));
    else v.textContent = value;
    t.append(el("div", { class: "label" }, label), v, el("div", { class: "sub" }, sub));
    box.append(t);
  }
}

function runsTable(runs) {
  const t = $("runs");
  t.replaceChildren();
  const head = el("tr");
  for (const h of ["Run", "Transcript", "Status", "Guardrails", "Verdict", "Avg", "Quality", "Rubric", "Revised", "Cost", "Issues"])
    head.append(el("th", { scope: "col" }, h));
  const thead = el("thead");
  thead.append(head);
  t.append(thead);
  const body = el("tbody");
  for (const r of runs) {
    const tr = el("tr");
    const cells = [r.run_id, r.transcript, badge(r.status), badge(r.guardrails), r.verdict ? badge(r.verdict) : "-",
      r.average ?? "-", r.quality_gate ? badge(r.quality_gate) : "-", r.rubric_average ?? "-",
      r.revised ? "yes" : "no", money(r.cost_usd), (r.issues || []).map((n) => `#${n}`).join(", ") || "-"];
    cells.forEach((c, i) => {
      const td = el("td", [5, 7, 9].includes(i) ? { class: "num" } : {});
      td.append(c instanceof Node ? c : document.createTextNode(String(c)));
      tr.append(td);
    });
    body.append(tr);
  }
  t.append(body);
}

function findings(details) {
  const list = $("findings");
  list.replaceChildren();
  const items = [...(details?.findings || [])];
  for (const l of details?.link_checks || []) {
    if (l.status === "not_found") items.push({ severity: "major", section: "Sources", category: "evidence",
      issue: `Quote not found on ${l.url}`, fix: "Remove the claim or mark it [NEEDS RESEARCH]." });
  }
  if (!items.length) { list.append(el("li", {}, "No critical or major problems in the latest review.")); return; }
  for (const f of items) {
    const li = el("li");
    const head = el("div");
    head.append(badge(f.severity), document.createTextNode(` Section ${f.section} · ${f.category}: ${f.issue}`));
    li.append(head, el("div", { class: "fix" }, `Fix: ${f.fix}`));
    list.append(li);
  }
}

function prdView(name, details) {
  const box = $("prd");
  $("prd-sub").textContent = details?.has_prd ? `Latest PRD for ${name}` : "No PRD for this transcript yet.";
  if (!details?.has_prd) { box.replaceChildren(); return; }
  if (window.marked && window.DOMPurify) {
    box.innerHTML = window.DOMPurify.sanitize(window.marked.parse(details.prd));
  } else {
    box.replaceChildren(el("pre", {}, details.prd)); // offline fallback: plain text
  }
}

// ---------- render ----------
function render() {
  const pick = $("transcript").value;
  const runs = DATA.runs.filter((r) => pick === "__all" || r.transcript === pick);
  const latest = {};
  for (const r of runs) if (!latest[r.transcript]) latest[r.transcript] = r; // runs are newest first
  const focus = pick === "__all" ? runs[0]?.transcript : pick;
  const details = focus ? DATA.transcripts[focus] : null;
  const oldestFirst = [...runs].reverse();

  kpis(runs, latest);
  barChart($("chart-cost"), oldestFirst.map((r) => ({
    value: r.cost_usd || 0, label: runDate(r.run_id),
    tip: [["Cost", money(r.cost_usd), true], ["Run", r.run_id], ["Verdict", r.verdict || "-"], ["Quality", r.quality_gate || "-"]],
  })), { format: (v) => `$${v.toFixed(v < 10 ? 1 : 0)}` });
  lineChart($("chart-rubric"), oldestFirst.map((r) => ({
    value: r.rubric_average, label: runDate(r.run_id),
    tip: [["Rubric average", r.rubric_average == null ? "-" : `${r.rubric_average} / 5`, true], ["Run", r.run_id],
          ["Revised", r.revised ? "yes" : "no"]],
  })), { ref: DATA.labels.rubric_pass });
  $("scorecard-sub").textContent = `${focus || "No transcript"}, latest run, 1–5. Dashed line = 3 (Go needs every score ≥ 3)`;
  hbarChart($("chart-scorecard"), Object.entries(details?.scores || {}).map(([id, v]) => ({
    label: DATA.labels.criteria[id] || id, value: v })), { ref: 3 });
  gradeBar($("chart-grades"), latest[focus]?.source_grades);
  const ops = DATA.ops;
  $("ops-sub").textContent = ops?.runs
    ? `US dollars per call, across ${ops.runs} run${ops.runs === 1 ? "" : "s"} (all transcripts). Budget skips: ${ops.budget_skips}`
    : "US dollars per call, across all runs";
  hbarValues($("chart-ops"), [...(ops?.agents || [])].sort((a, b) => b.avg_cost_usd - a.avg_cost_usd).map((a) => ({
    label: a.agent, value: a.avg_cost_usd,
    tip: [["Avg cost per call", money(a.avg_cost_usd), true], ["Total", money(a.total_cost_usd)], ["Calls", String(a.calls)],
          ["Typical time", `${a.p50_s}s`], ["Cache hit", `${Math.round(a.cache_hit_rate * 100)}%`]],
  })), { format: (v) => `$${v.toFixed(2)}` });
  opsTable(ops);
  findings(details);
  runsTable(runs);
  prdView(focus, details);
}

function setup(data) {
  DATA = data;
  $("updated").textContent = `Updated ${new Date(data.generated_at).toLocaleString()}`;
  $("demo-banner").hidden = !data.demo;
  $("empty").hidden = data.runs.length > 0;
  const select = $("transcript"), keep = select.value || "__all";
  select.replaceChildren(el("option", { value: "__all" }, "All transcripts"));
  for (const name of Object.keys(data.transcripts)) select.append(el("option", { value: name }, name));
  select.value = [...select.options].some((o) => o.value === keep) ? keep : "__all";
  render();
}

async function load() {
  const res = await fetch(`data.json?t=${Date.now()}`, { cache: "no-store" });
  setup(await res.json());
}

// Live reload when served by apps/dashboard/serve.py (local only): poll a version number.
async function watch() {
  let version = null;
  try {
    const first = await fetch("__version", { cache: "no-store" });
    if (!first.ok) return; // GitHub Pages: no live server
    version = await first.text();
  } catch { return; }
  $("live").hidden = false;
  setInterval(async () => {
    try {
      const v = await (await fetch("__version", { cache: "no-store" })).text();
      if (v !== version) { version = v; await load(); }
    } catch { /* server stopped; keep the last view */ }
  }, 1500);
}

document.addEventListener("DOMContentLoaded", () => {
  $("transcript").addEventListener("change", render);
  let resizeTimer;
  window.addEventListener("resize", () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(() => DATA && render(), 150); });
  load().then(watch).catch((e) => { $("updated").textContent = `Could not load data.json (${e.message})`; });
});
