from __future__ import annotations


def flow_fusion_index_html(base_html: str) -> str:
    """Add the read-only R2 fusion browser panel to the composed workbench."""

    if "/flow-fusion.css" in base_html or "/flow-fusion.js" in base_html:
        raise ValueError("flow-fusion assets already injected")
    return base_html.replace(
        "</head>",
        '  <link rel="stylesheet" href="/flow-fusion.css">\n</head>',
    ).replace(
        "</body>",
        '<script src="/flow-fusion.js" defer></script>\n</body>',
    )


FLOW_FUSION_CSS = """
.fusion-r2-panel { margin:10px 0; padding:10px; border:1px solid #d9dde2; border-radius:9px; background:#f8fafb; }
.fusion-r2-head { display:flex; align-items:flex-start; justify-content:space-between; gap:12px; margin-bottom:8px; }
.fusion-r2-head strong { font-size:13px; }
.fusion-r2-note,.fusion-r2-status { color:#68707a; font-size:11px; line-height:1.5; }
.fusion-r2-actions { display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin:8px 0; }
.fusion-r2-actions button { padding:7px 11px; }
.fusion-r2-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:6px; margin-top:8px; }
.fusion-r2-fact { min-width:0; padding:7px 8px; border:1px solid #e2e6e9; border-radius:7px; background:#fff; font-size:11px; line-height:1.45; }
.fusion-r2-fact span,.fusion-r2-fact code { display:block; }
.fusion-r2-fact span { color:#717982; margin-bottom:2px; }
.fusion-r2-fact code { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
@media (max-width:620px) { .fusion-r2-grid { grid-template-columns:1fr; } }
"""


FLOW_FUSION_JS = r"""
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const baziRoot = $('bazi-chart');
  if (!baziRoot) return;

  const panel = document.createElement('section');
  panel.id = 'fusion-r2-panel';
  panel.className = 'fusion-r2-panel';
  panel.hidden = true;
  panel.innerHTML = `
    <div class="fusion-r2-head">
      <div>
        <strong>联合目标时点 R2</strong>
        <div class="fusion-r2-note">只读组合八字目标流与紫微目标选择器；共享同一目标时间凭证，但不统一两套换日/历法规则。</div>
      </div>
      <code id="fusion-r2-hash">-</code>
    </div>
    <div class="fusion-r2-actions">
      <button id="resolve-fusion-r2" type="button">校验联合目标时点</button>
    </div>
    <div id="fusion-r2-status" class="fusion-r2-status">请先完成联合排盘并填写目标时点。</div>
    <div id="fusion-r2-grid" class="fusion-r2-grid"></div>
  `;

  const targetPanel = $('bazi-target-flow-panel');
  if (targetPanel && targetPanel.parentNode) {
    targetPanel.parentNode.insertBefore(panel, targetPanel.nextSibling);
  } else {
    baziRoot.parentNode.insertBefore(panel, baziRoot);
  }

  const button = $('resolve-fusion-r2');
  const status = $('fusion-r2-status');
  const grid = $('fusion-r2-grid');
  const hashBox = $('fusion-r2-hash');
  let serial = 0;

  const optionalInt = (id) => {
    const element = $(id);
    const value = element?.value?.trim?.() ?? '';
    return value === '' ? null : Number.parseInt(value, 10);
  };
  const optionalText = (id) => {
    const element = $(id);
    const value = element?.value?.trim?.() ?? '';
    return value === '' ? null : value;
  };
  const clear = (node) => { while (node.firstChild) node.removeChild(node.firstChild); };
  const fact = (label, value) => {
    const box = document.createElement('div');
    box.className = 'fusion-r2-fact';
    const title = document.createElement('span');
    title.textContent = label;
    const code = document.createElement('code');
    code.textContent = value ?? '-';
    code.title = code.textContent;
    box.append(title, code);
    return box;
  };

  function targetFieldsPresent() {
    return Boolean(
      $('target-datetime')?.value &&
      $('target-place')?.value?.trim() &&
      $('target-latitude')?.value !== '' &&
      $('target-longitude')?.value !== '' &&
      $('target-timezone-id')?.value?.trim()
    );
  }

  function payload() {
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
      target_datetime: $('target-datetime').value,
      target_place: $('target-place').value.trim(),
      target_latitude: Number.parseFloat($('target-latitude').value),
      target_longitude: Number.parseFloat($('target-longitude').value),
      target_timezone_id: $('target-timezone-id').value.trim(),
      target_precision: $('target-precision').value,
      target_uncertainty_seconds: Number.parseInt($('target-uncertainty-seconds').value, 10),
      target_temporal_profile_id: 'BAZI-TARGET-TEMPORAL-COORDINATE-FOUNDATION-R1',
    };
  }

  function reset(message) {
    serial += 1;
    clear(grid);
    hashBox.textContent = '-';
    status.textContent = message || '请先完成联合排盘并填写目标时点。';
  }

  function render(data) {
    const r2 = data?.combined_target_flow_fusion_r2;
    const target = data?.target_coordinate_resolution;
    const ziwei = data?.ziwei_selector_projection;
    const bazi = data?.bazi_target_flow_bundle;
    if (!r2 || !target || !ziwei || !bazi) {
      throw new Error('R2 response missing released bundle projections');
    }
    clear(grid);
    hashBox.textContent = (r2.bundle_hash || '-').slice(0, 18);
    hashBox.title = r2.bundle_hash || '-';
    status.textContent = `${r2.status} · ${r2.composition_semantics}`;
    grid.append(
      fact('R2 BundleHash', r2.bundle_hash),
      fact('共享 Target FactHash', r2.target_coordinate_fact_hash),
      fact('八字目标流', `${r2.bazi_target_flow_status} · ${r2.bazi_target_flow_bundle_hash}`),
      fact('紫微目标选择器', `${r2.ziwei_selector_status} · candidates=${r2.ziwei_selector_candidate_count}`),
      fact('紫微 Selector FactHash', r2.ziwei_selector_fact_hash),
      fact('R1 Target Flow Hash', r2.r1_target_flow_bundle_hash),
    );
  }

  button.addEventListener('click', async () => {
    if (!targetFieldsPresent()) {
      reset('目标时点字段不完整，R2 未执行。');
      return;
    }
    const requestSerial = ++serial;
    status.textContent = '正在校验联合目标时点 R2…';
    clear(grid);
    try {
      const response = await fetch('/api/resolve-flow-fusion-r2', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload()),
      });
      const data = await response.json();
      if (requestSerial !== serial) return;
      if (!response.ok) {
        const error = data?.error || {};
        throw new Error(`${error.code || response.status}: ${error.detail || 'R2 resolution failed'}`);
      }
      render(data);
    } catch (error) {
      if (requestSerial !== serial) return;
      reset(`R2 失败：${error.message}`);
    }
  });

  const invalidateIds = [
    'birth-datetime', 'birth-place', 'latitude', 'longitude', 'timezone-id',
    'location-manual', 'sex', 'precision', 'uncertainty-seconds',
    'ziwei-daxian-count', 'ziwei-daxian-frame-id', 'ziwei-annual-year',
    'ziwei-lunar-month', 'ziwei-minor-limit-age', 'bazi-natal-profile',
    'bazi-temporal-profile', 'bazi-dayun-count', 'target-datetime',
    'target-place', 'target-latitude', 'target-longitude', 'target-timezone-id',
    'target-precision', 'target-uncertainty-seconds',
  ];
  invalidateIds.forEach((id) => {
    const element = $(id);
    if (!element) return;
    element.addEventListener('input', () => reset('输入已变化，请重新校验联合目标时点 R2。'));
    element.addEventListener('change', () => reset('输入已变化，请重新校验联合目标时点 R2。'));
  });

  const chartForm = $('chart-form');
  if (chartForm) {
    chartForm.addEventListener('submit', () => {
      panel.hidden = false;
      reset('联合盘已重算；填写或确认目标时点后可校验 R2。');
    });
  }

  panel.hidden = false;
})();
"""
