from __future__ import annotations


def ziwei_jielan_dignity_candidate_index_html(base_html: str) -> str:
    """Inject the read-only Jielan historical dignity source-lexeme surface."""

    if (
        "/ziwei-jielan-dignity-candidate.css" in base_html
        or "/ziwei-jielan-dignity-candidate.js" in base_html
    ):
        raise ValueError("Jielan dignity historical-candidate assets already injected")
    return base_html.replace(
        "</head>",
        '  <link rel="stylesheet" href="/ziwei-jielan-dignity-candidate.css">\n</head>',
    ).replace(
        "</body>",
        '<script src="/ziwei-jielan-dignity-candidate.js" defer></script>\n</body>',
    )


ZIWEI_JIELAN_DIGNITY_CANDIDATE_CSS = """
.ziwei-jielan-dignity-panel { margin-bottom:10px; padding:10px; border:1px solid #d8dde2; border-radius:9px; background:#fafbfc; }
.ziwei-jielan-dignity-head { display:flex; align-items:flex-start; justify-content:space-between; gap:12px; margin-bottom:8px; }
.ziwei-jielan-dignity-note,.ziwei-jielan-dignity-status,.ziwei-jielan-dignity-lineage { color:#68707a; font-size:11px; line-height:1.45; }
.ziwei-jielan-dignity-summary { display:flex; flex-wrap:wrap; gap:5px; margin:7px 0; }
.ziwei-jielan-dignity-chip { padding:2px 6px; border:1px solid #e0e3e6; border-radius:999px; background:#fff; font-size:10px; }
.ziwei-jielan-dignity-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:7px; margin-top:8px; }
.ziwei-jielan-dignity-card { padding:7px; border:1px solid #e0e3e6; border-radius:7px; background:#fff; min-width:0; }
.ziwei-jielan-dignity-card strong { display:block; margin-bottom:4px; font-size:12px; }
.ziwei-jielan-dignity-row { display:grid; grid-template-columns:2em minmax(0,1fr); gap:6px; font-size:10px; line-height:1.45; overflow-wrap:anywhere; }
.ziwei-jielan-dignity-branch { font-weight:600; }
.ziwei-jielan-dignity-lineage { margin-top:8px; overflow-wrap:anywhere; }
@media (max-width:900px) { .ziwei-jielan-dignity-grid { grid-template-columns:1fr; } }
"""


ZIWEI_JIELAN_DIGNITY_CANDIDATE_JS = """
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const root = $('ziwei-chart');
  if (!root) return;

  const panel = document.createElement('section');
  panel.id = 'ziwei-jielan-dignity-panel';
  panel.className = 'ziwei-jielan-dignity-panel';
  panel.hidden = true;
  panel.innerHTML =
    '<div class="ziwei-jielan-dignity-head">' +
      '<div><strong>1581《捷览》庙陷原词历史候选</strong>' +
      '<div class="ziwei-jielan-dignity-note">只读展示后端返回的 CH70 原始语词与 CH69 平行校勘结果。PRESERVED_NOT_SELECTED；不转换生产等级、不跨章补值、不提供 winner 控件。</div></div>' +
      '<code id="ziwei-jielan-dignity-hash">-</code>' +
    '</div>' +
    '<div id="ziwei-jielan-dignity-status" class="ziwei-jielan-dignity-status">等待紫微盘</div>' +
    '<div id="ziwei-jielan-dignity-summary" class="ziwei-jielan-dignity-summary"></div>' +
    '<div id="ziwei-jielan-dignity-grid" class="ziwei-jielan-dignity-grid"></div>' +
    '<div id="ziwei-jielan-dignity-lineage" class="ziwei-jielan-dignity-lineage"></div>';
  root.parentNode.insertBefore(panel, root);

  const statusNode = $('ziwei-jielan-dignity-status');
  const summaryNode = $('ziwei-jielan-dignity-summary');
  const grid = $('ziwei-jielan-dignity-grid');
  const lineage = $('ziwei-jielan-dignity-lineage');
  const hashNode = $('ziwei-jielan-dignity-hash');
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
      combined_profile_id: 'ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1'
    };
  }

  function lexemes(values) {
    return (values || []).length ? values.join('/') : '∅';
  }

  function render(response) {
    const profile = response.candidate_profile;
    panel.hidden = false;
    clear(summaryNode);
    clear(grid);
    hashNode.textContent = profile.cross_collation_hash.slice(0, 16);
    hashNode.title = profile.cross_collation_hash;
    statusNode.textContent =
      profile.selection_status + ' · ' + profile.cross_collation_status;

    Object.entries(response.relation_counts || {}).forEach(([key, value]) => {
      const chip = document.createElement('span');
      chip.className = 'ziwei-jielan-dignity-chip';
      chip.textContent = key + '=' + value;
      summaryNode.append(chip);
    });

    const groups = new Map();
    (response.cross_collation_rows || []).forEach((row) => {
      if (!groups.has(row.display_name)) groups.set(row.display_name, []);
      groups.get(row.display_name).push(row);
    });
    groups.forEach((rows, displayName) => {
      const card = document.createElement('div');
      card.className = 'ziwei-jielan-dignity-card';
      const title = document.createElement('strong');
      title.textContent = displayName;
      card.append(title);
      rows.forEach((row) => {
        const node = document.createElement('div');
        node.className = 'ziwei-jielan-dignity-row';
        const branch = document.createElement('span');
        branch.className = 'ziwei-jielan-dignity-branch';
        branch.textContent = row.branch;
        const value = document.createElement('span');
        value.textContent =
          'CH70=' + lexemes(row.ch70_source_lexemes) +
          ' · CH69=' + lexemes(row.ch69_source_lexemes) +
          ' · ' + row.relation;
        if (row.ch69_unresolved_note) {
          value.title = row.ch69_unresolved_note;
        }
        node.append(branch, value);
        card.append(node);
      });
      grid.append(card);
    });

    lineage.textContent = [
      'candidate_api=' + profile.candidate_api_id + '@' + profile.candidate_api_version,
      'registry=' + profile.rule_set_id + '@' + profile.rule_set_version,
      'runtime_resolver=' + profile.runtime_resolver_id + '@' + profile.runtime_resolver_version,
      'cross_collation=' + profile.cross_collation_id + '@' + profile.cross_collation_version,
      'registry_hash=' + profile.registry_hash,
      'source_ziwei_bundle_hash=' + response.source_ziwei_bundle_hash,
      'source_natal_fact_hash=' + response.source_natal_fact_hash,
      'source_natal_computation_hash=' + response.source_natal_computation_hash,
      'production_grade_mapping_present=' + String(profile.production_grade_mapping_present),
      'ch69_used_to_fill_ch70=' + String(profile.ch69_used_to_fill_ch70),
      'production_winner_selected=' + String(profile.production_winner_selected),
      'production_profile_changed=' + String(profile.production_profile_changed)
    ].join(' · ');
  }

  async function refresh() {
    const ticket = ++serial;
    statusNode.textContent = '读取《捷览》庙陷原词候选…';
    try {
      const response = await fetch('/api/ziwei-jielan-1581-dignity-candidate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(requestPayload())
      });
      const payload = await response.json();
      if (ticket !== serial) return;
      if (!response.ok) {
        panel.hidden = false;
        statusNode.textContent =
          (payload.error?.code || '庙陷候选读取失败') + ': ' +
          (payload.error?.detail || response.status);
        return;
      }
      render(payload);
    } catch (error) {
      if (ticket !== serial) return;
      panel.hidden = false;
      statusNode.textContent = '庙陷候选读取失败：' + String(error);
    }
  }

  const originalFetch = window.fetch.bind(window);
  window.fetch = async (...args) => {
    const response = await originalFetch(...args);
    const url = typeof args[0] === 'string' ? args[0] : args[0]?.url || '';
    if (
      response.ok &&
      (url.endsWith('/api/resolve') || url.endsWith('/api/ziwei-interaction'))
    ) {
      window.setTimeout(refresh, 0);
    }
    return response;
  };
})();
"""
