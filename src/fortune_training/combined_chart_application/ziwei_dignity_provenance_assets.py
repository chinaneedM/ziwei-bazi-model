from __future__ import annotations


def ziwei_dignity_provenance_index_html(base_html: str) -> str:
    """Inject the read-only Ziwei Dignity provenance surface."""

    if "/ziwei-dignity-provenance.css" in base_html or "/ziwei-dignity-provenance.js" in base_html:
        raise ValueError("Ziwei Dignity provenance assets already injected")
    return base_html.replace(
        "</head>",
        '  <link rel="stylesheet" href="/ziwei-dignity-provenance.css">\n</head>',
    ).replace(
        "</body>",
        '<script src="/ziwei-dignity-provenance.js" defer></script>\n</body>',
    )


ZIWEI_DIGNITY_PROVENANCE_CSS = """
.ziwei-dignity-provenance-panel { margin-bottom:10px; padding:10px; border:1px solid #d8dde2; border-radius:9px; background:#fafbfc; }
.ziwei-dignity-provenance-head { display:flex; align-items:flex-start; justify-content:space-between; gap:12px; margin-bottom:8px; }
.ziwei-dignity-provenance-head strong { font-size:13px; }
.ziwei-dignity-provenance-note,.ziwei-dignity-provenance-status,.ziwei-dignity-provenance-lineage { color:#68707a; font-size:11px; line-height:1.45; }
.ziwei-dignity-provenance-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:7px; margin-top:8px; }
.ziwei-dignity-provenance-card { padding:7px; border:1px solid #e0e3e6; border-radius:7px; background:#fff; }
.ziwei-dignity-provenance-card strong { display:block; margin-bottom:4px; font-size:12px; }
.ziwei-dignity-provenance-row { font-size:11px; line-height:1.5; overflow-wrap:anywhere; }
.ziwei-dignity-provenance-lineage { margin-top:8px; overflow-wrap:anywhere; }
@media (max-width:1100px) { .ziwei-dignity-provenance-grid { grid-template-columns:repeat(2,minmax(0,1fr)); } }
@media (max-width:700px) { .ziwei-dignity-provenance-grid { grid-template-columns:1fr; } }
"""


ZIWEI_DIGNITY_PROVENANCE_JS = """
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const root = $('ziwei-chart');
  if (!root) return;

  const panel = document.createElement('section');
  panel.id = 'ziwei-dignity-provenance-panel';
  panel.className = 'ziwei-dignity-provenance-panel';
  panel.hidden = true;
  panel.innerHTML = `
    <div class="ziwei-dignity-provenance-head">
      <div>
        <strong>庙旺注解来源 / 权威边界</strong>
        <div class="ziwei-dignity-provenance-note">只读展示后端既有 Dignity annotation 的 RuleSet、生成器与 source lineage。该 operational registry 不是 S01 冻结原盘亮度权威，不在浏览器重算亮度，也不作吉凶、强弱或预测解释。</div>
      </div>
      <code id="ziwei-dignity-provenance-hash">-</code>
    </div>
    <div id="ziwei-dignity-provenance-status" class="ziwei-dignity-provenance-status">等待紫微盘</div>
    <div id="ziwei-dignity-provenance-grid" class="ziwei-dignity-provenance-grid"></div>
    <div id="ziwei-dignity-provenance-lineage" class="ziwei-dignity-provenance-lineage"></div>
  `;
  root.parentNode.insertBefore(panel, root);

  const statusNode = $('ziwei-dignity-provenance-status');
  const grid = $('ziwei-dignity-provenance-grid');
  const lineage = $('ziwei-dignity-provenance-lineage');
  const hashNode = $('ziwei-dignity-provenance-hash');
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
      combined_profile_id: 'ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1',
    };
  }

  function render(response) {
    const provenance = response.ziwei_dignity_annotation_provenance;
    panel.hidden = false;
    hashNode.textContent = provenance.bundle_hash.slice(0, 16);
    hashNode.title = provenance.bundle_hash;
    statusNode.textContent = `后端事实：${provenance.rows.length} 条 · ${provenance.source_dignity_rule_set_id}@${provenance.source_dignity_rule_set_version}`;

    clear(grid);
    provenance.rows.forEach((row) => {
      const card = document.createElement('div');
      card.className = 'ziwei-dignity-provenance-card';
      const title = document.createElement('strong');
      title.textContent = `${row.target_display_name} · ${row.branch}宫`;
      const fact = document.createElement('div');
      fact.className = 'ziwei-dignity-provenance-row';
      fact.textContent = row.status === 'GRADED' ? `评级：${row.grade}` : `评级状态：${row.status}`;
      const source = document.createElement('div');
      source.className = 'ziwei-dignity-provenance-row';
      source.textContent = `${row.rule_set_id}@${row.rule_set_version}`;
      source.title = `${row.generator_id}@${row.algorithm_version} · ${row.scale_id}@${row.scale_version} · ${row.source_refs.join(',')}`;
      card.append(title, fact, source);
      grid.append(card);
    });

    lineage.textContent = [
      `authority_class=${provenance.authority_class}`,
      `s01_brightness_authority=${provenance.s01_brightness_authority}`,
      `semantic_scope=${provenance.semantic_scope}`,
      `source_application_bundle_hash=${provenance.source_application_bundle_hash}`,
      `fact_hash=${provenance.fact_hash}`,
      `computation_hash=${provenance.computation_hash}`,
      `integrity=${provenance.integrity?.status || '-'}`,
    ].join(' · ');
  }

  async function refresh() {
    const ticket = ++serial;
    statusNode.textContent = '读取庙旺注解来源…';
    try {
      const response = await fetch('/api/ziwei-dignity-provenance', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(requestPayload()),
      });
      const payload = await response.json();
      if (ticket !== serial) return;
      if (!response.ok) {
        panel.hidden = false;
        statusNode.textContent = `${payload.error?.code || '庙旺注解来源读取失败'}: ${payload.error?.detail || response.status}`;
        return;
      }
      render(payload);
    } catch (error) {
      if (ticket !== serial) return;
      panel.hidden = false;
      statusNode.textContent = `庙旺注解来源读取失败：${String(error)}`;
    }
  }

  const originalFetch = window.fetch.bind(window);
  window.fetch = async (...args) => {
    const response = await originalFetch(...args);
    const url = typeof args[0] === 'string' ? args[0] : args[0]?.url || '';
    if (response.ok && (url.endsWith('/api/resolve') || url.endsWith('/api/ziwei-interaction'))) {
      window.setTimeout(refresh, 0);
    }
    return response;
  };
})();
"""
