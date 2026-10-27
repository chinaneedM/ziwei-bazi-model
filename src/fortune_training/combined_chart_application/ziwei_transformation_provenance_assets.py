from __future__ import annotations


def ziwei_transformation_provenance_index_html(base_html: str) -> str:
    """Inject the read-only Ziwei transformation provenance surface."""

    if (
        "/ziwei-transformation-provenance.css" in base_html
        or "/ziwei-transformation-provenance.js" in base_html
    ):
        raise ValueError("Ziwei transformation provenance assets already injected")
    return base_html.replace(
        "</head>",
        '  <link rel="stylesheet" href="/ziwei-transformation-provenance.css">\n</head>',
    ).replace(
        "</body>",
        '<script src="/ziwei-transformation-provenance.js" defer></script>\n</body>',
    )


ZIWEI_TRANSFORMATION_PROVENANCE_CSS = """
.ziwei-transformation-provenance-panel { margin-bottom:10px; padding:10px; border:1px solid #d8dde2; border-radius:9px; background:#fafbfc; }
.ziwei-transformation-provenance-head { display:flex; align-items:flex-start; justify-content:space-between; gap:12px; margin-bottom:8px; }
.ziwei-transformation-provenance-head strong { font-size:13px; }
.ziwei-transformation-provenance-note,.ziwei-transformation-provenance-status { color:#68707a; font-size:11px; line-height:1.45; }
.ziwei-transformation-provenance-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:7px; margin-top:8px; }
.ziwei-transformation-provenance-card { padding:8px; border:1px solid #e0e3e6; border-radius:7px; background:#fff; min-width:0; }
.ziwei-transformation-provenance-card > strong { display:block; margin-bottom:4px; font-size:12px; }
.ziwei-transformation-provenance-row { font-size:11px; line-height:1.5; overflow-wrap:anywhere; }
.ziwei-transformation-provenance-trace { margin-top:5px; font-size:10px; color:#68707a; overflow-wrap:anywhere; }
.ziwei-transformation-provenance-trace summary { cursor:pointer; }
@media (max-width:800px) { .ziwei-transformation-provenance-grid { grid-template-columns:1fr; } }
"""


ZIWEI_TRANSFORMATION_PROVENANCE_JS = r"""
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const root = $('ziwei-chart');
  if (!root || typeof window.fetch !== 'function') return;

  const panel = document.createElement('section');
  panel.id = 'ziwei-transformation-provenance-panel';
  panel.className = 'ziwei-transformation-provenance-panel';
  panel.hidden = true;

  const head = document.createElement('div');
  head.className = 'ziwei-transformation-provenance-head';
  const headCopy = document.createElement('div');
  const title = document.createElement('strong');
  title.textContent = '四化激活来源 / 生成谱系';
  const note = document.createElement('div');
  note.className = 'ziwei-transformation-provenance-note';
  note.textContent = '只读展示 /api/resolve 已发布的 TransformationActivation；浏览器不重算四化表、不选择规则、不推导自化方向。';
  headCopy.append(title, note);
  const statusNode = document.createElement('code');
  statusNode.id = 'ziwei-transformation-provenance-status';
  statusNode.className = 'ziwei-transformation-provenance-status';
  head.append(headCopy, statusNode);

  const grid = document.createElement('div');
  grid.id = 'ziwei-transformation-provenance-grid';
  grid.className = 'ziwei-transformation-provenance-grid';
  panel.append(head, grid);
  root.parentNode.insertBefore(panel, root);

  const clear = () => {
    panel.hidden = true;
    statusNode.textContent = '';
    while (grid.firstChild) grid.removeChild(grid.firstChild);
  };

  const nonEmptyText = (value) => typeof value === 'string' && value.trim() ? value.trim() : null;

  function addressText(address) {
    const branch = nonEmptyText(address?.branch);
    if (!branch) return '-';
    return Number.isInteger(address?.index) ? `${branch}宫 (#${address.index})` : `${branch}宫`;
  }

  function validActivation(row) {
    return row && typeof row === 'object' &&
      nonEmptyText(row.transformation_type) &&
      nonEmptyText(row.target_display_name) &&
      nonEmptyText(row.source_layer) &&
      nonEmptyText(row.source_stem) &&
      nonEmptyText(row.context_id) &&
      nonEmptyText(row.assignment_id) &&
      nonEmptyText(row.mechanism_id) &&
      nonEmptyText(row.generator_id) &&
      nonEmptyText(row.algorithm_version) &&
      Array.isArray(row.source_refs);
  }

  function appendLine(card, text) {
    const line = document.createElement('div');
    line.className = 'ziwei-transformation-provenance-row';
    line.textContent = text;
    card.append(line);
  }

  function appendActivation(row) {
    const card = document.createElement('div');
    card.className = 'ziwei-transformation-provenance-card';

    const heading = document.createElement('strong');
    heading.textContent = `${row.transformation_type} · ${row.target_display_name} · ${addressText(row.target_address)}`;
    card.append(heading);
    appendLine(card, `来源层：${row.source_layer} · 来源干：${row.source_stem}`);
    appendLine(card, `context_id=${row.context_id}`);
    appendLine(card, `assignment=${row.assignment_id} · mechanism=${row.mechanism_id}`);
    appendLine(card, `generator=${row.generator_id}@${row.algorithm_version}`);
    appendLine(card, `source_refs=${row.source_refs.map((value) => String(value)).join(', ') || '-'}`);

    const details = document.createElement('details');
    details.className = 'ziwei-transformation-provenance-trace';
    const summary = document.createElement('summary');
    summary.textContent = '技术标识';
    const trace = document.createElement('div');
    trace.textContent = `activation_id=${nonEmptyText(row.activation_id) || '-'} · target_entity_id=${nonEmptyText(row.target_entity_id) || '-'}`;
    details.append(summary, trace);
    card.append(details);
    grid.append(card);
  }

  function renderFromResolvePayload(payload) {
    clear();
    const transformations = payload?.combined_resolution?.ziwei_bundle?.candidate?.chart?.transformations;
    if (!Array.isArray(transformations) || transformations.length === 0) return;
    const rows = transformations.filter(validActivation);
    if (rows.length === 0) return;

    panel.hidden = false;
    statusNode.textContent = `${rows.length} 条 canonical activation`;
    rows.forEach(appendActivation);
  }

  const nativeFetch = window.fetch.bind(window);
  window.fetch = async (...args) => {
    const response = await nativeFetch(...args);
    const input = args[0];
    const rawUrl = typeof input === 'string' ? input : input?.url;
    let path = '';
    try {
      path = new URL(rawUrl, window.location.href).pathname;
    } catch (_) {
      return response;
    }
    if (path === '/api/resolve' && response.ok) {
      const copy = response.clone();
      window.setTimeout(async () => {
        try {
          renderFromResolvePayload(await copy.json());
        } catch (_) {
          clear();
        }
      }, 0);
    }
    return response;
  };

  const form = $('chart-form');
  if (form) form.addEventListener('submit', clear);
})();
"""
