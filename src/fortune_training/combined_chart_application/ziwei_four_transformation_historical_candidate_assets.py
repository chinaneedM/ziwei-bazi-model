from __future__ import annotations


def ziwei_four_transformation_candidate_index_html(base_html: str) -> str:
    """Inject read-only whole-table Four-Transformation historical candidates."""

    if (
        "/ziwei-four-transformation-candidates.css" in base_html
        or "/ziwei-four-transformation-candidates.js" in base_html
    ):
        raise ValueError("Four-Transformation historical-candidate assets already injected")
    return base_html.replace(
        "</head>",
        '  <link rel="stylesheet" href="/ziwei-four-transformation-candidates.css">\n</head>',
    ).replace(
        "</body>",
        '<script src="/ziwei-four-transformation-candidates.js" defer></script>\n</body>',
    )


ZIWEI_FOUR_TRANSFORMATION_CANDIDATE_CSS = """
.ziwei-four-transform-candidate-panel { margin-bottom:10px; padding:10px; border:1px solid #d8dde2; border-radius:9px; background:#fafbfc; }
.ziwei-four-transform-candidate-head { display:flex; align-items:flex-start; justify-content:space-between; gap:12px; margin-bottom:8px; }
.ziwei-four-transform-candidate-note,.ziwei-four-transform-candidate-status,.ziwei-four-transform-candidate-lineage { color:#68707a; font-size:11px; line-height:1.45; }
.ziwei-four-transform-candidate-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:7px; margin-top:8px; }
.ziwei-four-transform-candidate-card { padding:7px; border:1px solid #e0e3e6; border-radius:7px; background:#fff; min-width:0; }
.ziwei-four-transform-candidate-card strong { display:block; margin-bottom:4px; font-size:12px; }
.ziwei-four-transform-candidate-row { font-size:11px; line-height:1.5; overflow-wrap:anywhere; }
.ziwei-four-transform-candidate-lineage { margin-top:8px; overflow-wrap:anywhere; }
@media (max-width:900px) { .ziwei-four-transform-candidate-grid { grid-template-columns:1fr; } }
"""


ZIWEI_FOUR_TRANSFORMATION_CANDIDATE_JS = """
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const root = $('ziwei-chart');
  if (!root) return;

  const panel = document.createElement('section');
  panel.id = 'ziwei-four-transform-candidate-panel';
  panel.className = 'ziwei-four-transform-candidate-panel';
  panel.hidden = true;
  panel.innerHTML =
    '<div class="ziwei-four-transform-candidate-head">' +
      '<div><strong>四化整表历史候选</strong>' +
      '<div class="ziwei-four-transform-candidate-note">同一已验证紫微盘的两套 source-scoped 整表候选并列只读展示。whole_table_only=true；cell_level_hybridization_allowed=false；selection_status=PRESERVED_NOT_SELECTED。不改变生产 S08，不选择 winner。</div></div>' +
      '<code id="ziwei-four-transform-candidate-hash">-</code>' +
    '</div>' +
    '<div id="ziwei-four-transform-candidate-status" class="ziwei-four-transform-candidate-status">等待紫微盘</div>' +
    '<div id="ziwei-four-transform-candidate-grid" class="ziwei-four-transform-candidate-grid"></div>' +
    '<div id="ziwei-four-transform-candidate-lineage" class="ziwei-four-transform-candidate-lineage"></div>';
  root.parentNode.insertBefore(panel, root);

  const statusNode = $('ziwei-four-transform-candidate-status');
  const grid = $('ziwei-four-transform-candidate-grid');
  const lineage = $('ziwei-four-transform-candidate-lineage');
  const hashNode = $('ziwei-four-transform-candidate-hash');
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

  function render(response) {
    const profile = response.candidate_profile;
    panel.hidden = false;
    clear(grid);
    hashNode.textContent = profile.registry_hash.slice(0, 16);
    hashNode.title = profile.registry_hash;
    statusNode.textContent =
      profile.selection_status + ' · 生年干=' + response.input_snapshot.source_stem;

    (response.candidate_tables || []).forEach((candidate) => {
      const node = document.createElement('div');
      node.className = 'ziwei-four-transform-candidate-card';
      const title = document.createElement('strong');
      title.textContent = candidate.candidate_id;
      node.append(title);
      (candidate.assignments || []).forEach((assignment) => {
        const row = document.createElement('div');
        row.className = 'ziwei-four-transform-candidate-row';
        row.textContent =
          assignment.transformation_type + ': ' + assignment.target_display_name;
        node.append(row);
      });
      const source = document.createElement('div');
      source.className = 'ziwei-four-transform-candidate-row';
      source.textContent = '来源: ' + (candidate.source_refs || []).join(', ');
      node.append(source);
      grid.append(node);
    });

    lineage.textContent = [
      'candidate_api=' + profile.candidate_api_id + '@' + profile.candidate_api_version,
      'registry=' + profile.rule_set_id + '@' + profile.rule_set_version,
      'runtime_resolver=' + profile.runtime_resolver_id + '@' + profile.runtime_resolver_version,
      'whole_table_only=' + String(profile.whole_table_only),
      'cell_level_hybridization_allowed=' + String(profile.cell_level_hybridization_allowed),
      'source_ziwei_bundle_hash=' + response.source_ziwei_bundle_hash,
      'source_natal_fact_hash=' + response.source_natal_fact_hash,
      'source_natal_computation_hash=' + response.source_natal_computation_hash,
      'production_winner_selected=' + String(profile.production_winner_selected),
      'production_profile_changed=' + String(profile.production_profile_changed)
    ].join(' · ');
  }

  async function refresh() {
    const ticket = ++serial;
    statusNode.textContent = '读取四化整表历史候选…';
    try {
      const response = await fetch('/api/ziwei-four-transformation-candidates', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(requestPayload())
      });
      const payload = await response.json();
      if (ticket !== serial) return;
      if (!response.ok) {
        panel.hidden = false;
        statusNode.textContent =
          (payload.error?.code || '四化候选读取失败') + ': ' +
          (payload.error?.detail || response.status);
        return;
      }
      render(payload);
    } catch (error) {
      if (ticket !== serial) return;
      panel.hidden = false;
      statusNode.textContent = '四化候选读取失败：' + String(error);
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
