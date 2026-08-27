from __future__ import annotations


TARGET_FLOW_ZIWEI_PROJECTION_CSS = """
.ziwei-target-projection { margin:8px 0; padding:8px; border:1px solid #dfe3e6; border-radius:7px; background:#fff; font-size:11px; line-height:1.55; }
.ziwei-target-projection-head { display:flex; align-items:flex-start; justify-content:space-between; gap:10px; margin-bottom:6px; }
.ziwei-target-projection-head strong { font-size:12px; }
.ziwei-target-projection-note { color:#68707a; font-size:10px; line-height:1.45; }
.ziwei-target-projection-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:6px; margin-top:7px; }
.ziwei-target-projection-card { padding:6px; border:1px solid #edf0f2; border-radius:5px; background:#fafbfb; min-width:0; }
.ziwei-target-projection-card strong,.ziwei-target-projection-card code { display:block; }
.ziwei-target-hourly { margin-top:7px; padding-top:7px; border-top:1px dashed #e1e4e7; }
.ziwei-target-hourly-candidate { margin-top:5px; padding:6px; border:1px solid #edf0f2; border-radius:5px; background:#fafbfb; word-break:break-word; }
.ziwei-target-hourly-candidate code { display:block; }
.ziwei-target-projection-lineage { margin-top:7px; color:#59616b; word-break:break-word; }
.ziwei-target-projection-lineage code { display:block; }
@media (max-width:900px) { .ziwei-target-projection-grid { grid-template-columns:1fr 1fr; } }
@media (max-width:620px) { .ziwei-target-projection-grid { grid-template-columns:1fr; } }
"""


TARGET_FLOW_ZIWEI_PROJECTION_JS = r"""
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const panel = $('bazi-target-flow-panel');
  const candidateSelect = $('bazi-flow-candidate');
  const lineageRoot = $('bazi-flow-lineage');
  const resolveButton = $('resolve-target-flow');
  if (!panel || !candidateSelect || !lineageRoot || !resolveButton) return;

  const projectionRoot = document.createElement('section');
  projectionRoot.id = 'ziwei-target-projection';
  projectionRoot.className = 'ziwei-target-projection';
  projectionRoot.hidden = true;
  lineageRoot.parentNode.insertBefore(projectionRoot, lineageRoot);

  const projectionState = {
    response: null,
    serial: 0,
    requestFingerprint: null,
  };

  const projectionDependencyIds = [
    'birth-datetime', 'birth-place', 'latitude', 'longitude', 'timezone-id',
    'location-manual', 'sex', 'precision', 'uncertainty-seconds',
    'ziwei-daxian-count', 'ziwei-daxian-frame-id', 'ziwei-annual-year',
    'ziwei-minor-limit-age', 'bazi-natal-profile', 'bazi-temporal-profile',
    'bazi-dayun-count', 'target-datetime', 'target-place', 'target-latitude',
    'target-longitude', 'target-timezone-id', 'target-precision',
    'target-uncertainty-seconds',
  ];

  const display = (value) => value === null || value === undefined || value === '' ? '-' : String(value);
  const clear = (element) => { while (element.firstChild) element.removeChild(element.firstChild); };
  const node = (name, text, className) => {
    const element = document.createElement(name);
    if (text !== undefined) element.textContent = text;
    if (className) element.className = className;
    return element;
  };

  function projectionFingerprint() {
    return JSON.stringify(projectionDependencyIds.map((id) => {
      const element = $(id);
      return [id, element?.value ?? '', element?.checked ?? null];
    }));
  }

  function clearProjectionView() {
    clear(projectionRoot);
    projectionRoot.hidden = true;
  }

  function projectionHeader(noteText) {
    const head = node('div', undefined, 'ziwei-target-projection-head');
    const copy = node('div');
    copy.append(node('strong', '紫微目标时点投影（只读）'));
    copy.append(node(
      'div',
      noteText || '复用共享目标坐标与已发布紫微 projection；不改写紫微选择器。',
      'ziwei-target-projection-note',
    ));
    head.append(copy);
    projectionRoot.append(head);
  }

  function renderBindingUnavailable(message) {
    clear(projectionRoot);
    projectionRoot.hidden = false;
    projectionHeader('目标坐标身份必须与紫微 projection 唯一匹配；不按数组位置推断。');
    projectionRoot.append(node('div', message, 'ziwei-target-projection-note'));
  }

  function layerCard(label, lines) {
    const card = node('div', undefined, 'ziwei-target-projection-card');
    card.append(node('strong', label));
    lines.forEach((line) => card.append(node('div', line)));
    return card;
  }

  function currentBaziCandidate() {
    const rows = projectionState.response?.bazi_target_flow_bundle?.candidates;
    const candidates = Array.isArray(rows) ? rows : [];
    if (candidates.length === 1) return candidates[0];
    if (candidateSelect.value === '') return null;
    const index = Number.parseInt(candidateSelect.value, 10);
    if (!Number.isInteger(index) || index < 0 || index >= candidates.length) return null;
    return candidates[index];
  }

  function projectionCandidateFor(baziCandidate) {
    const projection = projectionState.response?.shared_ziwei_selector_projection;
    if (!projection || !Array.isArray(projection.candidates)) return null;
    const targetCandidateId = baziCandidate?.view?.target?.target_coordinate_candidate_id;
    if (!targetCandidateId) return null;
    const matches = projection.candidates.filter(
      (row) => row.source_target_candidate_id === targetCandidateId,
    );
    return matches.length === 1 ? matches[0] : null;
  }

  function renderProjectionCandidate(row, baziCandidate) {
    clear(projectionRoot);
    projectionRoot.hidden = false;
    projectionHeader('共享目标坐标只读投影；条文流日与案例方法流时候选明确分层。');

    const grid = node('div', undefined, 'ziwei-target-projection-grid');
    grid.append(
      layerCard('大限', [
        `frame ${display(row.daxian_frame_id)}`,
      ]),
      layerCard('流年', [
        `年份 ${display(row.annual_year)}`,
        `frame ${display(row.source_annual_frame_id)}`,
      ]),
      layerCard('小限', [
        `虚岁 ${display(row.minor_limit_age)}`,
        `frame ${display(row.minor_limit_ring_projection?.frame_id)}`,
      ]),
      layerCard('流月', [
        `状态 ${display(row.monthly_projection_status)}`,
        `${display(row.monthly_ganzhi)} · ${display(row.monthly_active_address_branch)}`,
        `frame ${display(row.monthly_frame_id)}`,
      ]),
    );
    projectionRoot.append(grid);

    const daily = node('div', undefined, 'ziwei-target-projection-card');
    daily.append(node('strong', '紫微流日（条文规则）'));
    daily.append(node('div', `状态 ${display(row.daily_projection_status)}`));
    daily.append(node(
      'div',
      `${display(row.daily_effective_gregorian_date)} · ${display(row.daily_ganzhi)} · ${display(row.daily_active_address_branch)}`,
    ));
    daily.append(node('code', `frame=${display(row.daily_frame_id)}`));
    daily.append(node('code', `rule=${display(row.daily_rule_id)}`));
    daily.append(node('code', `sources=${Array.isArray(row.daily_source_refs) ? row.daily_source_refs.join(',') : '-'}`));
    projectionRoot.append(daily);

    const hourly = node('div', undefined, 'ziwei-target-hourly');
    hourly.append(node('strong', '紫微流时候选（案例方法；未作流派裁决）'));
    hourly.append(node(
      'div',
      `状态 ${display(row.hourly_projection_status)} · 全部候选并列展示，不自动选定任何流时。`,
      'ziwei-target-projection-note',
    ));
    const hourlyCandidates = Array.isArray(row.hourly_method_candidates)
      ? row.hourly_method_candidates
      : [];
    if (hourlyCandidates.length === 0) {
      hourly.append(node('div', '当前 projection 没有可展示的流时候选。'));
    }
    hourlyCandidates.forEach((hourlyCandidate) => {
      const box = node('div', undefined, 'ziwei-target-hourly-candidate');
      box.append(node(
        'div',
        `${display(hourlyCandidate.time_standard)} · ${display(hourlyCandidate.source_local_datetime)}`,
      ));
      box.append(node(
        'div',
        `${display(hourlyCandidate.day_ganzhi)}日 · ${display(hourlyCandidate.hour_ganzhi)} · ${display(hourlyCandidate.hour_branch)}时`,
      ));
      box.append(node('div', `宫位 ${display(hourlyCandidate.active_address_branch)}`));
      box.append(node('code', `candidate_id=${display(hourlyCandidate.candidate_id)}`));
      box.append(node('code', `authority=${display(hourlyCandidate.authority_status)}`));
      box.append(node('code', `rule=${display(hourlyCandidate.rule_id)}`));
      box.append(node('code', `sources=${Array.isArray(hourlyCandidate.source_refs) ? hourlyCandidate.source_refs.join(',') : '-'}`));
      hourly.append(box);
    });
    projectionRoot.append(hourly);

    const projection = projectionState.response.shared_ziwei_selector_projection;
    const lineage = node('div', undefined, 'ziwei-target-projection-lineage');
    lineage.append(node('code', `target_candidate_id=${display(row.source_target_candidate_id)}`));
    lineage.append(node('code', `bazi_target_candidate_id=${display(baziCandidate?.view?.target?.target_coordinate_candidate_id)}`));
    lineage.append(node('code', `projection_candidate_hash=${display(row.candidate_hash)}`));
    lineage.append(node('code', `projection_fact=${display(projection?.hashes?.fact_hash)}`));
    lineage.append(node('code', `integrity=${display(projection?.integrity?.status)}`));
    projectionRoot.append(lineage);
  }

  function renderForCurrentSelection() {
    const projection = projectionState.response?.shared_ziwei_selector_projection;
    if (!projection || !Array.isArray(projection.candidates)) {
      clearProjectionView();
      return;
    }
    const baziCandidate = currentBaziCandidate();
    if (!baziCandidate) {
      clearProjectionView();
      return;
    }
    const row = projectionCandidateFor(baziCandidate);
    if (!row) {
      renderBindingUnavailable('当前目标候选未获得唯一紫微 projection 绑定；已拒绝位置式回退。');
      return;
    }
    renderProjectionCandidate(row, baziCandidate);
  }

  function invalidateProjectionOnly(message) {
    projectionState.serial += 1;
    projectionState.response = null;
    projectionState.requestFingerprint = null;
    clearProjectionView();
    if (message) projectionRoot.dataset.invalidatedReason = message;
  }

  candidateSelect.addEventListener('change', () => {
    if (!projectionState.response) {
      clearProjectionView();
      return;
    }
    renderForCurrentSelection();
  });

  projectionDependencyIds.forEach((id) => {
    const element = $(id);
    if (!element) return;
    const invalidate = () => invalidateProjectionOnly(
      '输入或紫微选择器已改变；当前紫微目标投影已失效。',
    );
    element.addEventListener('input', invalidate);
    element.addEventListener('change', invalidate);
  });

  const ziweiRoot = $('ziwei-chart');
  if (ziweiRoot) {
    const observer = new MutationObserver(() => invalidateProjectionOnly(
      '紫微显示源已刷新；当前紫微目标投影已失效。',
    ));
    observer.observe(ziweiRoot, {childList: true, subtree: true});
  }

  resolveButton.addEventListener('click', () => {
    projectionState.response = null;
    projectionState.requestFingerprint = null;
    clearProjectionView();
  });

  const originalFetch = window.fetch.bind(window);
  window.fetch = async (...args) => {
    const requestUrl = typeof args[0] === 'string' ? args[0] : args[0]?.url;
    const isUnifiedFlow = requestUrl === '/api/resolve-flow';
    const requestSerial = isUnifiedFlow ? ++projectionState.serial : null;
    const requestFingerprint = isUnifiedFlow ? projectionFingerprint() : null;
    const response = await originalFetch(...args);
    if (!isUnifiedFlow) return response;
    if (!response.ok) {
      if (requestSerial === projectionState.serial) invalidateProjectionOnly();
      return response;
    }
    const copy = response.clone();
    void copy.json().then((data) => {
      if (requestSerial !== projectionState.serial) return;
      if (requestFingerprint !== projectionFingerprint()) return;
      projectionState.response = data;
      projectionState.requestFingerprint = requestFingerprint;
      window.setTimeout(() => {
        if (requestSerial !== projectionState.serial) return;
        if (requestFingerprint !== projectionFingerprint()) return;
        renderForCurrentSelection();
      }, 0);
    }).catch(() => {
      if (requestSerial === projectionState.serial) invalidateProjectionOnly();
    });
    return response;
  };
})();
"""
