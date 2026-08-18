from __future__ import annotations


def shared_apply_index_html(base_html: str) -> str:
    if "/shared-apply.css" in base_html or "/shared-apply.js" in base_html:
        raise ValueError("shared apply assets already injected")
    return base_html.replace(
        "</head>",
        '  <link rel="stylesheet" href="/shared-apply.css">\n</head>',
    ).replace(
        "</body>",
        '<script src="/shared-apply.js" defer></script>\n</body>',
    )


SHARED_APPLY_CSS = """
.shared-apply-panel { margin:10px 0; padding:10px; border:1px solid #d8dde2; border-radius:9px; background:#fafbfc; }
.shared-apply-head { display:flex; justify-content:space-between; gap:12px; align-items:flex-start; margin-bottom:8px; }
.shared-apply-head strong { font-size:13px; }
.shared-apply-note,.shared-apply-status { color:#68707a; font-size:11px; line-height:1.45; }
.shared-apply-controls { display:grid; grid-template-columns:minmax(0,1fr) auto auto; gap:7px; align-items:end; }
.shared-apply-controls label { font-size:11px; }
.shared-apply-controls select,.shared-apply-controls button { min-height:32px; }
.shared-apply-lineage { margin-top:7px; font-size:10px; line-height:1.4; white-space:pre-wrap; }
@media (max-width:900px) { .shared-apply-controls { grid-template-columns:1fr; } }
"""


SHARED_APPLY_JS = r"""
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const ziweiRoot = $('ziwei-chart');
  const targetPanel = $('bazi-target-flow-panel');
  if (!ziweiRoot || !targetPanel) return;

  const panel = document.createElement('section');
  panel.id = 'shared-ziwei-apply-panel';
  panel.className = 'shared-apply-panel';
  panel.innerHTML = `
    <div class="shared-apply-head">
      <div><strong>共享目标时间 → 紫微</strong><div class="shared-apply-note">仅在你显式点击“应用到紫微”后，才把服务端 projection 写入紫微大限/流年、小限。解析八字 flow 或编辑目标时间不会自动同步。</div></div>
      <code id="shared-ziwei-projection-hash">-</code>
    </div>
    <div class="shared-apply-controls">
      <label>Projection 候选<select id="shared-ziwei-projection-candidate" disabled><option value="">尚未计算</option></select></label>
      <button type="button" id="resolve-shared-ziwei-projection">计算共享 Projection</button>
      <button type="button" id="apply-shared-ziwei-projection" disabled>应用目标时间到紫微</button>
    </div>
    <div id="shared-ziwei-projection-status" class="shared-apply-status">等待显式计算</div>
    <div id="shared-ziwei-projection-lineage" class="shared-apply-lineage"></div>
  `;
  targetPanel.parentNode.insertBefore(panel, targetPanel);

  const calculateButton = $('resolve-shared-ziwei-projection');
  const applyButton = $('apply-shared-ziwei-projection');
  const candidateSelect = $('shared-ziwei-projection-candidate');
  const status = $('shared-ziwei-projection-status');
  const hashBox = $('shared-ziwei-projection-hash');
  const lineage = $('shared-ziwei-projection-lineage');

  const sourceFieldIds = [
    'birth-datetime', 'birth-place', 'latitude', 'longitude', 'timezone-id',
    'location-manual', 'sex', 'precision', 'uncertainty-seconds',
    'ziwei-daxian-count', 'ziwei-daxian-frame-id', 'ziwei-annual-year',
    'ziwei-minor-limit-age', 'bazi-natal-profile', 'bazi-temporal-profile',
    'bazi-dayun-count',
  ];
  const targetFieldIds = [
    'target-datetime', 'target-place', 'target-latitude', 'target-longitude',
    'target-timezone-id', 'target-precision', 'target-uncertainty-seconds',
    'target-temporal-profile',
  ];

  let displayedSourceFingerprint = null;
  let projectionSourceFingerprint = null;
  let projectionTargetFingerprint = null;
  let projectionResponse = null;
  let serial = 0;

  const fingerprint = (ids) => JSON.stringify(ids.map((id) => {
    const element = $(id);
    return [id, element?.value ?? '', element?.checked ?? null];
  }));
  const sourceFingerprint = () => fingerprint(sourceFieldIds);
  const targetFingerprint = () => fingerprint(targetFieldIds);
  const sourceChartIsPresent = () => Boolean(ziweiRoot.querySelector('svg'));

  function clearSelect() {
    while (candidateSelect.firstChild) candidateSelect.removeChild(candidateSelect.firstChild);
  }

  function invalidate(detail) {
    projectionResponse = null;
    projectionSourceFingerprint = null;
    projectionTargetFingerprint = null;
    clearSelect();
    const option = document.createElement('option');
    option.value = '';
    option.textContent = '尚未计算';
    candidateSelect.append(option);
    candidateSelect.disabled = true;
    applyButton.disabled = true;
    hashBox.textContent = '-';
    hashBox.title = '';
    lineage.textContent = '';
    if (detail) status.textContent = detail;
  }

  function captureDisplayedSource() {
    displayedSourceFingerprint = sourceChartIsPresent() ? sourceFingerprint() : null;
  }

  function displayedSourceIsCurrent() {
    return displayedSourceFingerprint !== null
      && displayedSourceFingerprint === sourceFingerprint();
  }

  function payload() {
    const textOrNull = (id) => {
      const value = $(id).value.trim();
      return value === '' ? null : value;
    };
    const intOrNull = (id) => {
      const value = $(id).value.trim();
      return value === '' ? null : Number.parseInt(value, 10);
    };
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
      ziwei_daxian_frame_id: textOrNull('ziwei-daxian-frame-id'),
      ziwei_annual_year: intOrNull('ziwei-annual-year'),
      ziwei_minor_limit_age: intOrNull('ziwei-minor-limit-age'),
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
      target_temporal_profile_id: $('target-temporal-profile').value,
    };
  }

  function candidateLabel(row) {
    const daxian = row.daxian_frame_id || 'PRE_DAXIAN';
    return `#${row.source_target_candidate_index} · ${row.sample_reported_local_datetime} · fold=${row.fold} · ${row.annual_year}年 / ${row.minor_limit_age}岁 / ${daxian}`;
  }

  function responseLineageIsConsistent(data) {
    const projection = data?.projection;
    if (!projection) return false;
    if (data.source_ziwei_bundle_hash !== projection.source_ziwei_application_bundle_hash) return false;
    if (data.target_coordinate_fact_hash !== projection.source_target_coordinate_fact_hash) return false;
    if (data.target_coordinate_computation_hash !== projection.source_target_coordinate_computation_hash) return false;
    if (!Array.isArray(projection.candidates) || projection.candidates.length === 0) return false;
    return projection.candidates.every((row, index) => (
      row.source_target_candidate_index === index
      && typeof row.source_target_candidate_id === 'string'
      && row.source_target_candidate_id.length > 0
      && typeof row.candidate_hash === 'string'
      && row.candidate_hash.length === 64
    ));
  }

  function renderCandidateDetail() {
    if (!projectionResponse || candidateSelect.value === '') {
      lineage.textContent = '';
      applyButton.disabled = true;
      return;
    }
    const index = Number.parseInt(candidateSelect.value, 10);
    const row = projectionResponse.projection.candidates[index];
    if (!row || row.source_target_candidate_index !== index) {
      invalidate('候选 lineage 与索引不一致；已拒绝应用。请重新计算。');
      return;
    }
    lineage.textContent = [
      `target_candidate=${row.source_target_candidate_id}`,
      `sample_index=${row.source_sample_index} · UTC=${row.target_utc}`,
      `annual_frame=${row.source_annual_frame_id}`,
      `projection_candidate_hash=${row.candidate_hash}`,
    ].join('\n');
    applyButton.disabled = false;
  }

  function renderProjection(data) {
    if (!responseLineageIsConsistent(data)) {
      invalidate('Projection source/hash lineage 不一致；已拒绝使用服务端响应。');
      return;
    }
    projectionResponse = data;
    projectionSourceFingerprint = sourceFingerprint();
    projectionTargetFingerprint = targetFingerprint();
    const rows = data.projection.candidates;
    clearSelect();
    if (rows.length > 1) {
      const placeholder = document.createElement('option');
      placeholder.value = '';
      placeholder.textContent = `请选择候选（${rows.length}）`;
      candidateSelect.append(placeholder);
    }
    rows.forEach((row, index) => {
      const option = document.createElement('option');
      option.value = String(index);
      option.textContent = candidateLabel(row);
      candidateSelect.append(option);
    });
    candidateSelect.disabled = false;
    candidateSelect.value = rows.length === 1 ? '0' : '';
    hashBox.textContent = data.projection.hashes.fact_hash.slice(0, 16);
    hashBox.title = data.projection.hashes.fact_hash;
    status.textContent = rows.length === 1
      ? 'Projection 已计算；仍需显式点击“应用目标时间到紫微”。'
      : `Projection 保留 ${rows.length} 个候选；请先显式选择一个 lineage，再应用。`;
    renderCandidateDetail();
  }

  async function calculateProjection() {
    if (!displayedSourceIsCurrent()) {
      invalidate('当前表单与屏幕上的紫微基盘不一致。请先点击“联合排盘”，再计算共享 Projection。');
      return;
    }
    const requestSerial = ++serial;
    status.textContent = '正在计算 shared target → Ziwei selector projection…';
    applyButton.disabled = true;
    try {
      const response = await fetch('/api/shared-ziwei-projection', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload()),
      });
      const data = await response.json();
      if (!response.ok) throw data.error || {code: `HTTP_${response.status}`, detail: 'Shared projection request failed'};
      if (requestSerial !== serial) return;
      if (!displayedSourceIsCurrent()) {
        invalidate('计算期间紫微基盘已变化；已丢弃旧 Projection。');
        return;
      }
      renderProjection(data);
    } catch (error) {
      if (requestSerial !== serial) return;
      invalidate(`${error.code || 'LOCAL_APP_SHARED_ZIWEI_PROJECTION_FAILED'}: ${error.detail || String(error)}`);
    }
  }

  function applyProjection() {
    if (!projectionResponse || candidateSelect.value === '') return;
    if (!displayedSourceIsCurrent()
        || projectionSourceFingerprint !== sourceFingerprint()
        || projectionTargetFingerprint !== targetFingerprint()) {
      invalidate('源盘或目标输入已变化；旧 Projection 已失效，不能应用。');
      return;
    }
    if (!responseLineageIsConsistent(projectionResponse)) {
      invalidate('Projection source/hash lineage 已失效；拒绝应用。');
      return;
    }
    const index = Number.parseInt(candidateSelect.value, 10);
    const row = projectionResponse.projection.candidates[index];
    if (!row || row.source_target_candidate_index !== index) {
      invalidate('候选 lineage 与索引不一致；拒绝应用。');
      return;
    }
    const daxianNav = $('ziwei-daxian-nav');
    const annualNav = $('ziwei-annual-nav');
    const minorNav = $('ziwei-minor-nav');
    if (!daxianNav || !annualNav || !minorNav) {
      invalidate('Ziwei interaction navigator 尚未就绪。');
      return;
    }
    daxianNav.value = row.daxian_frame_id || '';
    annualNav.value = String(row.annual_year);
    minorNav.value = String(row.minor_limit_age);
    if (annualNav.value !== String(row.annual_year)
        || minorNav.value !== String(row.minor_limit_age)
        || daxianNav.value !== (row.daxian_frame_id || '')) {
      invalidate('服务端 projection 不在当前 Ziwei navigator materialized domain；拒绝应用。');
      return;
    }
    status.textContent = '已显式应用所选 Projection；正在复用现有 Ziwei interaction 刷新。';
    annualNav.dispatchEvent(new Event('change', {bubbles: true}));
  }

  candidateSelect.addEventListener('change', renderCandidateDetail);
  calculateButton.addEventListener('click', calculateProjection);
  applyButton.addEventListener('click', applyProjection);

  [...sourceFieldIds, ...targetFieldIds].forEach((id) => {
    const element = $(id);
    if (!element) return;
    const invalidateOnEdit = () => {
      if (projectionResponse) invalidate('输入已变化；已清除旧 Projection。');
    };
    element.addEventListener('input', invalidateOnEdit);
    element.addEventListener('change', invalidateOnEdit);
  });

  const observer = new MutationObserver(() => {
    const hadProjection = Boolean(projectionResponse);
    captureDisplayedSource();
    if (hadProjection) invalidate('紫微显示源已刷新；旧 Projection 已失效。');
  });
  observer.observe(ziweiRoot, {childList: true, subtree: true});
  captureDisplayedSource();
})();
"""
