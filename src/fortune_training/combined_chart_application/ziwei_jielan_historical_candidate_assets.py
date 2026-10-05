from __future__ import annotations


def ziwei_jielan_1581_candidate_index_html(base_html: str) -> str:
    """Inject the read-only Jielan 1581 historical-candidate surface."""

    if (
        "/ziwei-jielan-1581-candidate.css" in base_html
        or "/ziwei-jielan-1581-candidate.js" in base_html
    ):
        raise ValueError("Jielan 1581 historical-candidate assets already injected")
    return base_html.replace(
        "</head>",
        '  <link rel="stylesheet" href="/ziwei-jielan-1581-candidate.css">\n</head>',
    ).replace(
        "</body>",
        '<script src="/ziwei-jielan-1581-candidate.js" defer></script>\n</body>',
    )


ZIWEI_JIELAN_1581_CANDIDATE_CSS = """
.ziwei-jielan-candidate-panel { margin-bottom:10px; padding:10px; border:1px solid #d8dde2; border-radius:9px; background:#fafbfc; }
.ziwei-jielan-candidate-head { display:flex; align-items:flex-start; justify-content:space-between; gap:12px; margin-bottom:8px; }
.ziwei-jielan-candidate-note,.ziwei-jielan-candidate-status,.ziwei-jielan-candidate-lineage { color:#68707a; font-size:11px; line-height:1.45; }
.ziwei-jielan-candidate-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:7px; margin-top:8px; }
.ziwei-jielan-candidate-card { padding:7px; border:1px solid #e0e3e6; border-radius:7px; background:#fff; min-width:0; }
.ziwei-jielan-candidate-card strong { display:block; margin-bottom:4px; font-size:12px; }
.ziwei-jielan-candidate-row { font-size:11px; line-height:1.5; overflow-wrap:anywhere; }
.ziwei-jielan-candidate-lineage { margin-top:8px; overflow-wrap:anywhere; }
@media (max-width:900px) { .ziwei-jielan-candidate-grid { grid-template-columns:1fr; } }
"""


ZIWEI_JIELAN_1581_CANDIDATE_JS = """
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const root = $('ziwei-chart');
  if (!root) return;

  const panel = document.createElement('section');
  panel.id = 'ziwei-jielan-candidate-panel';
  panel.className = 'ziwei-jielan-candidate-panel';
  panel.hidden = true;
  panel.innerHTML =
    '<div class="ziwei-jielan-candidate-head">' +
      '<div><strong>1581《捷览》历史候选旁路</strong>' +
      '<div class="ziwei-jielan-candidate-note">只读展示同一已验证紫微盘上由后端 source-scoped resolver 返回的候选事实。selection_status=PRESERVED_NOT_SELECTED；此面板不改变生产 Profile、不选择 winner、不在浏览器重算安星规则。</div></div>' +
      '<code id="ziwei-jielan-candidate-hash">-</code>' +
    '</div>' +
    '<div id="ziwei-jielan-candidate-status" class="ziwei-jielan-candidate-status">等待紫微盘</div>' +
    '<div id="ziwei-jielan-candidate-grid" class="ziwei-jielan-candidate-grid"></div>' +
    '<div id="ziwei-jielan-candidate-lineage" class="ziwei-jielan-candidate-lineage"></div>';
  root.parentNode.insertBefore(panel, root);

  const statusNode = $('ziwei-jielan-candidate-status');
  const grid = $('ziwei-jielan-candidate-grid');
  const lineage = $('ziwei-jielan-candidate-lineage');
  const hashNode = $('ziwei-jielan-candidate-hash');
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

  function card(titleText, rows) {
    const node = document.createElement('div');
    node.className = 'ziwei-jielan-candidate-card';
    const title = document.createElement('strong');
    title.textContent = titleText;
    node.append(title);
    rows.forEach((pair) => {
      const row = document.createElement('div');
      row.className = 'ziwei-jielan-candidate-row';
      const value = pair[1] === null || pair[1] === undefined || pair[1] === '' ? '-' : pair[1];
      row.textContent = pair[0] + ': ' + value;
      node.append(row);
    });
    grid.append(node);
  }

  function render(response) {
    const profile = response.candidate_profile;
    const facts = response.released_facts;
    panel.hidden = false;
    clear(grid);
    hashNode.textContent = profile.candidate_runtime_hash.slice(0, 16);
    hashNode.title = profile.candidate_runtime_hash;
    statusNode.textContent = profile.selection_status + ' · ' + profile.rule_set_id + '@' + profile.rule_set_version;

    card('魁钺候选', [
      ['落宫', (facts.kui_yue?.branches || []).join(' / ')],
      ['来源', (facts.kui_yue?.source_refs || []).join(', ')]
    ]);
    card('火铃候选', [
      ['子时起宫', (facts.fire_bell?.start_branches || []).join(' / ')],
      ['按生时解析', (facts.fire_bell?.resolved_branches || []).join(' / ')],
      ['来源', (facts.fire_bell?.source_refs || []).join(', ')]
    ]);
    card('命主候选', [
      ['基准', facts.mingzhu?.basis],
      ['基准值', facts.mingzhu?.basis_value],
      ['命主', facts.mingzhu?.display_name],
      ['来源', (facts.mingzhu?.source_refs || []).join(', ')]
    ]);

    lineage.textContent = [
      'candidate_api=' + profile.candidate_api_id + '@' + profile.candidate_api_version,
      'runtime_resolver=' + profile.runtime_resolver_id + '@' + profile.runtime_resolver_version,
      'source=' + profile.source_id,
      'registry_hash=' + profile.registry_hash,
      'source_ziwei_bundle_hash=' + response.source_ziwei_bundle_hash,
      'source_natal_fact_hash=' + response.source_natal_fact_hash,
      'source_natal_computation_hash=' + response.source_natal_computation_hash,
      'production_winner_selected=' + String(profile.production_winner_selected),
      'production_profile_changed=' + String(profile.production_profile_changed)
    ].join(' · ');
  }

  async function refresh() {
    const ticket = ++serial;
    statusNode.textContent = '读取《捷览》历史候选…';
    try {
      const response = await fetch('/api/ziwei-jielan-1581-candidate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(requestPayload())
      });
      const payload = await response.json();
      if (ticket !== serial) return;
      if (!response.ok) {
        panel.hidden = false;
        statusNode.textContent = (payload.error?.code || '历史候选读取失败') + ': ' + (payload.error?.detail || response.status);
        return;
      }
      render(payload);
    } catch (error) {
      if (ticket !== serial) return;
      panel.hidden = false;
      statusNode.textContent = '历史候选读取失败：' + String(error);
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
