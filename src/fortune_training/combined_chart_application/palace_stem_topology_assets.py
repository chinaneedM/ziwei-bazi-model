from __future__ import annotations


def palace_stem_topology_index_html(base_html: str) -> str:
    """Inject read-only palace-stem topology assets into the combined Workbench."""

    if "/ziwei-palace-stem-topology.css" in base_html or "/ziwei-palace-stem-topology.js" in base_html:
        raise ValueError("palace-stem topology assets already injected")
    return base_html.replace(
        "</head>",
        '  <link rel="stylesheet" href="/ziwei-palace-stem-topology.css">\n</head>',
    ).replace(
        "</body>",
        '<script src="/ziwei-palace-stem-topology.js" defer></script>\n</body>',
    )


PALACE_STEM_TOPOLOGY_CSS = """
.ziwei-palace-stem-topology-panel { margin-bottom:10px; padding:10px; border:1px solid #d8dde2; border-radius:9px; background:#fafbfc; }
.ziwei-palace-stem-topology-head { display:flex; align-items:flex-start; justify-content:space-between; gap:12px; margin-bottom:8px; }
.ziwei-palace-stem-topology-head strong { font-size:13px; }
.ziwei-palace-stem-topology-note,.ziwei-palace-stem-topology-status,.ziwei-palace-stem-topology-lineage { color:#68707a; font-size:11px; line-height:1.45; }
.ziwei-palace-stem-topology-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:7px; margin-top:8px; }
.ziwei-palace-stem-topology-card { padding:7px; border:1px solid #e0e3e6; border-radius:7px; background:#fff; }
.ziwei-palace-stem-topology-card strong { display:block; margin-bottom:4px; font-size:12px; }
.ziwei-palace-stem-topology-row { font-size:11px; line-height:1.5; white-space:pre-wrap; }
.ziwei-palace-stem-topology-lineage { margin-top:8px; overflow-wrap:anywhere; }
@media (max-width:900px) { .ziwei-palace-stem-topology-grid { grid-template-columns:1fr; } }
"""


PALACE_STEM_TOPOLOGY_JS = """
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const root = $('ziwei-chart');
  if (!root) return;

  const panel = document.createElement('section');
  panel.id = 'ziwei-palace-stem-topology-panel';
  panel.className = 'ziwei-palace-stem-topology-panel';
  panel.hidden = true;
  panel.innerHTML = `
    <div class="ziwei-palace-stem-topology-head">
      <div>
        <strong>宫干四化目标拓扑</strong>
        <div class="ziwei-palace-stem-topology-note">仅显示后端已发布的宫干四化目标拓扑。同宫 / 对宫 / 其他宫不等于离心 / 向心自化；方向未裁决，不作吉凶或事件解释。</div>
      </div>
      <code id="ziwei-palace-stem-topology-hash">-</code>
    </div>
    <div id="ziwei-palace-stem-topology-status" class="ziwei-palace-stem-topology-status">等待紫微盘</div>
    <div id="ziwei-palace-stem-topology-grid" class="ziwei-palace-stem-topology-grid"></div>
    <div id="ziwei-palace-stem-topology-lineage" class="ziwei-palace-stem-topology-lineage"></div>
  `;
  root.parentNode.insertBefore(panel, root);

  const status = $('ziwei-palace-stem-topology-status');
  const grid = $('ziwei-palace-stem-topology-grid');
  const lineage = $('ziwei-palace-stem-topology-lineage');
  const hashBox = $('ziwei-palace-stem-topology-hash');
  let serial = 0;

  const optionalInt = (id) => {
    const element = $(id);
    if (!element) return null;
    const value = element.value.trim();
    return value === '' ? null : Number.parseInt(value, 10);
  };
  const optionalText = (id) => {
    const element = $(id);
    if (!element) return null;
    const value = element.value.trim();
    return value === '' ? null : value;
  };
  const clear = (node) => { while (node.firstChild) node.removeChild(node.firstChild); };
  const relationLabel = {
    SAME_PALACE: '同宫',
    OPPOSITE_PALACE: '对宫',
    OTHER_PALACE: '其他宫',
  };

  function requestPayload() {
    return {
      birth_datetime: $('birth-datetime').value,
      birth_place: $('birth-place').value.trim(),
      latitude: Number.parseFloat($('latitude').value),
      longitude: Number.parseFloat($('longitude').value),
      timezone_id: $('timezone-id').value.trim(),
      sex: $('sex').value,
      precision: $('precision').value,
      uncertainty_seconds: Number.parseInt($('uncertainty-seconds').value, 10),
      ziwei_daxian_count: Number.parseInt($('ziwei-daxian-count').value, 10),
      ziwei_daxian_frame_id: optionalText('ziwei-daxian-frame-id'),
      ziwei_annual_year: optionalInt('ziwei-annual-year'),
      ziwei_lunar_month: optionalInt('ziwei-lunar-month'),
      ziwei_minor_limit_age: optionalInt('ziwei-minor-limit-age'),
      bazi_natal_profile_id: $('bazi-natal-profile').value,
      bazi_temporal_profile_id: $('bazi-temporal-profile').value,
      bazi_dayun_count: Number.parseInt($('bazi-dayun-count').value, 10),
      combined_profile_id: 'ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1',
    };
  }

  function render(response) {
    const topology = response.ziwei_palace_stem_transformation_topology;
    panel.hidden = false;
    hashBox.textContent = topology.bundle_hash.slice(0, 16);
    hashBox.title = topology.bundle_hash;
    status.textContent = `后端事实：${topology.rows.length} 条 · ${topology.classification_policy}`;

    const bySource = new Map();
    topology.rows.forEach((row) => {
      if (!bySource.has(row.source_address_index)) bySource.set(row.source_address_index, []);
      bySource.get(row.source_address_index).push(row);
    });
    clear(grid);
    [...bySource.entries()]
      .sort((left, right) => left[0] - right[0])
      .forEach(([, rows]) => {
        const first = rows[0];
        const card = document.createElement('div');
        card.className = 'ziwei-palace-stem-topology-card';
        const title = document.createElement('strong');
        title.textContent = `${first.source_branch}宫 · 宫干 ${first.source_stem}`;
        card.append(title);
        rows.forEach((row) => {
          const line = document.createElement('div');
          line.className = 'ziwei-palace-stem-topology-row';
          line.textContent = `${row.transformation_type} → ${row.target_display_name}（${row.target_branch}） · ${relationLabel[row.topology_relation] || row.topology_relation}`;
          line.title = `${row.assignment_id} · ${row.mechanism_id} · ${row.source_refs.join(',')}`;
          card.append(line);
        });
        grid.append(card);
      });

    lineage.textContent = [
      `semantic_scope=${topology.semantic_scope}`,
      `selection_semantics=${topology.selection_semantics}`,
      `source_rule_set=${topology.source_transformation_rule_set_id}@${topology.source_transformation_rule_set_version}`,
      `source_application_bundle_hash=${topology.source_application_bundle_hash}`,
      `fact_hash=${topology.fact_hash}`,
      `computation_hash=${topology.computation_hash}`,
      `integrity=${topology.integrity?.status || '-'}`,
    ].join(' · ');
  }

  async function refresh() {
    const ticket = ++serial;
    status.textContent = '读取宫干四化目标拓扑…';
    try {
      const response = await fetch('/api/ziwei-palace-stem-topology', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(requestPayload()),
      });
      const payload = await response.json();
      if (ticket !== serial) return;
      if (!response.ok) {
        panel.hidden = false;
        status.textContent = `${payload.error?.code || 'TOPOLOGY_ERROR'}: ${payload.error?.detail || response.status}`;
        return;
      }
      render(payload);
    } catch (error) {
      if (ticket !== serial) return;
      panel.hidden = false;
      status.textContent = `宫干四化目标拓扑读取失败：${String(error)}`;
    }
  }

  const originalFetch = window.fetch.bind(window);
  window.fetch = async (...args) => {
    const response = await originalFetch(...args);
    const url = typeof args[0] === 'string' ? args[0] : args[0]?.url || '';
    if (
      response.ok
      && (url.endsWith('/api/resolve') || url.endsWith('/api/ziwei-interaction'))
    ) {
      window.setTimeout(refresh, 0);
    }
    return response;
  };
})();
"""
