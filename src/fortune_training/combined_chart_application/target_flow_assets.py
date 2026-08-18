from __future__ import annotations


def target_flow_index_html(base_html: str) -> str:
    """Add Bazi target-flow browser assets to an already composed local page."""

    if "/target-flow.css" in base_html or "/target-flow.js" in base_html:
        raise ValueError("target-flow assets already injected")
    return base_html.replace(
        "</head>",
        '  <link rel="stylesheet" href="/target-flow.css">\n</head>',
    ).replace(
        "</body>",
        '<script src="/target-flow.js" defer></script>\n</body>',
    )


TARGET_FLOW_CSS = """
.bazi-target-flow-panel { margin-bottom:10px; padding:10px; border:1px solid #d8dde2; border-radius:9px; background:#fbfbfa; }
.bazi-target-flow-head { display:flex; align-items:flex-start; justify-content:space-between; gap:12px; margin-bottom:8px; }
.bazi-target-flow-head strong { font-size:13px; }
.bazi-target-flow-note,.bazi-target-flow-status { color:#68707a; font-size:11px; line-height:1.45; }
.bazi-target-flow-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:7px; margin:8px 0; }
.bazi-target-flow-grid label { font-size:11px; }
.bazi-target-flow-actions { display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin:8px 0; }
.bazi-target-flow-actions button { padding:7px 11px; }
.bazi-flow-candidate-select { min-width:180px; }
.bazi-flow-target-meta,.bazi-flow-lineage { margin:8px 0; padding:7px 8px; border:1px solid #e5e7e9; border-radius:7px; background:#fff; font-size:11px; line-height:1.55; word-break:break-word; }
.bazi-flow-frames { display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:6px; margin:8px 0; }
.bazi-flow-frame { padding:7px; border:1px solid #e0e3e6; border-radius:7px; background:#fff; font-size:11px; line-height:1.5; min-width:0; }
.bazi-flow-frame strong { display:block; margin-bottom:3px; }
.bazi-flow-frame code { display:block; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
@media (max-width:900px) { .bazi-target-flow-grid { grid-template-columns:1fr; } .bazi-flow-frames { grid-template-columns:1fr 1fr; } }
@media (max-width:620px) { .bazi-flow-frames { grid-template-columns:1fr; } }
"""


TARGET_FLOW_JS = r"""
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const baziRoot = $('bazi-chart');
  if (!baziRoot) return;

  const state = {
    response: null,
    displayedFingerprint: null,
    serial: 0,
  };

  const panel = document.createElement('section');
  panel.id = 'bazi-target-flow-panel';
  panel.className = 'bazi-target-flow-panel';
  panel.hidden = true;
  panel.innerHTML = `
    <div class="bazi-target-flow-head">
      <div><strong>八字目标时点</strong><div class="bazi-target-flow-note">显式解析大运 / 流年 / 流月 / 流日 / 流时。不会自动同步或改写紫微大限、流年、小限。</div></div>
      <code id="bazi-flow-hash">-</code>
    </div>
    <div class="bazi-target-flow-grid">
      <label>目标当地时间<input id="target-datetime" type="datetime-local"></label>
      <label>目标地点<input id="target-place" placeholder="例如 Beijing / Tokyo / Greenwich"></label>
      <label>目标纬度<input id="target-latitude" type="number" step="0.000001" min="-90" max="90"></label>
      <label>目标经度<input id="target-longitude" type="number" step="0.000001" min="-180" max="180"></label>
      <label>目标时区<input id="target-timezone-id" placeholder="例如 Asia/Shanghai"></label>
      <label>目标时间精度<select id="target-precision"><option value="EXACT_SECOND">精确到秒</option><option value="NEAREST_MINUTE">约到分钟</option><option value="NEAREST_HOUR">约到小时</option><option value="APPROXIMATE">约略时间</option></select></label>
      <label>目标不确定范围 ±秒<input id="target-uncertainty-seconds" type="number" min="0" max="86400" value="0"></label>
    </div>
    <div class="bazi-target-flow-actions">
      <button id="resolve-target-flow" type="button">解析目标时点</button>
      <select id="bazi-flow-candidate" class="bazi-flow-candidate-select" hidden aria-label="目标时点候选"></select>
    </div>
    <div id="bazi-target-flow-status" class="bazi-target-flow-status">请先完成联合排盘，再显式输入目标时点。</div>
    <div id="bazi-flow-target-meta" class="bazi-flow-target-meta" hidden></div>
    <div id="bazi-flow-frames" class="bazi-flow-frames"></div>
    <div id="bazi-flow-lineage" class="bazi-flow-lineage" hidden></div>
  `;
  baziRoot.parentNode.insertBefore(panel, baziRoot);

  const button = $('resolve-target-flow');
  const candidateSelect = $('bazi-flow-candidate');
  const status = $('bazi-target-flow-status');
  const targetMeta = $('bazi-flow-target-meta');
  const framesRoot = $('bazi-flow-frames');
  const lineageRoot = $('bazi-flow-lineage');
  const hashBox = $('bazi-flow-hash');

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
  ];
  const allFingerprintIds = [...sourceFieldIds, ...targetFieldIds];

  const optionalInt = (id) => {
    const value = $(id).value.trim();
    return value === '' ? null : Number.parseInt(value, 10);
  };
  const optionalText = (id) => {
    const value = $(id).value.trim();
    return value === '' ? null : value;
  };
  const clear = (node) => { while (node.firstChild) node.removeChild(node.firstChild); };
  const node = (name, text, cls) => {
    const element = document.createElement(name);
    if (text !== undefined) element.textContent = text;
    if (cls) element.className = cls;
    return element;
  };
  const shortHash = (value) => value ? value.slice(0, 16) : '-';
  const display = (value) => value === null || value === undefined || value === '' ? '-' : String(value);

  function fingerprint() {
    return JSON.stringify(allFingerprintIds.map((id) => {
      const element = $(id);
      return [id, element?.value ?? '', element?.checked ?? null];
    }));
  }

  function sourceChartIsPresent() {
    return Boolean(baziRoot.querySelector('.pillars, .bazi-candidate-bar, table'));
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

  function frameCard(label, frame, extra = '') {
    const box = node('div', undefined, 'bazi-flow-frame');
    box.append(node('strong', label));
    if (!frame) {
      box.append(node('span', '-'));
      return box;
    }
    const ganzhi = frame.ganzhi || frame.frame_id || '-';
    box.append(node('div', ganzhi));
    if (extra) box.append(node('div', extra));
    if (frame.start_utc) box.append(node('code', `起 ${frame.start_utc}`));
    if (frame.end_utc) box.append(node('code', `止 ${frame.end_utc}`));
    if (frame.start_las) box.append(node('code', `LAS 起 ${frame.start_las}`));
    if (frame.end_las) box.append(node('code', `LAS 止 ${frame.end_las}`));
    return box;
  }

  function clearCandidateView() {
    clear(framesRoot);
    targetMeta.hidden = true;
    targetMeta.textContent = '';
    lineageRoot.hidden = true;
    lineageRoot.textContent = '';
  }

  function renderCandidate(candidate, index, count) {
    clearCandidateView();
    const view = candidate.view;
    const target = view.target;
    targetMeta.hidden = false;
    targetMeta.textContent = [
      `候选 ${index + 1}/${count}`,
      `目标：${display(target.target_place)} · ${display(target.sample_reported_local_datetime)}`,
      `时区：${display(target.timezone_id)} · fold=${display(target.fold)} · UTC offset=${display(target.utc_offset_seconds)}s`,
      `UTC：${display(target.target_utc)}`,
      `真太阳时：${display(target.local_apparent_solar_datetime)}`,
      `Target ID：${display(target.target_coordinate_candidate_id)}`,
    ].join('\n');

    const flow = view.flow;
    const dayun = flow.active_dayun_frame;
    framesRoot.append(
      frameCard('大运', dayun, flow.active_dayun_kind),
      frameCard('流年', flow.annual, `${display(flow.annual?.start_term_chinese_name)} → ${display(flow.annual?.end_term_chinese_name)}`),
      frameCard('流月', flow.monthly, `${display(flow.monthly?.start_jie_chinese_name)} → ${display(flow.monthly?.end_jie_chinese_name)}`),
      frameCard('流日', view.daily, display(view.daily?.effective_day_date)),
      frameCard('流时', view.hourly, display(view.hourly?.branch)),
    );

    lineageRoot.hidden = false;
    lineageRoot.textContent = [
      `candidate_id=${candidate.candidate_id}`,
      `view_hash=${candidate.view_hash}`,
      `natal_fact=${candidate.natal_fact_hash}`,
      `temporal_fact=${candidate.temporal_fact_hash}`,
      `flow_fact=${candidate.flow_fact_hash}`,
      `daily_hourly_fact=${candidate.daily_hourly_fact_hash}`,
      `integrity target=${display(view.integrity?.target_coordinate)} flow=${display(view.integrity?.flow)} daily_hourly=${display(view.integrity?.daily_hourly)}`,
    ].join('\n');
  }

  function configureCandidates(bundle) {
    const candidates = bundle.candidates || [];
    clear(candidateSelect);
    clearCandidateView();
    if (candidates.length === 0) {
      candidateSelect.hidden = true;
      status.textContent = '目标时点没有可显示候选。';
      return;
    }
    if (candidates.length === 1) {
      candidateSelect.hidden = true;
      renderCandidate(candidates[0], 0, 1);
      status.textContent = '目标时点已解析：单一候选。';
      return;
    }

    candidateSelect.hidden = false;
    const prompt = document.createElement('option');
    prompt.value = '';
    prompt.textContent = `请选择候选（共 ${candidates.length} 个）`;
    prompt.selected = true;
    candidateSelect.append(prompt);
    candidates.forEach((candidate, index) => {
      const option = document.createElement('option');
      option.value = String(index);
      const target = candidate.view?.target || {};
      option.textContent = `候选 ${index + 1} · ${display(target.sample_reported_local_datetime)} · fold=${display(target.fold)}`;
      candidateSelect.append(option);
    });
    status.textContent = `目标时点保留 ${candidates.length} 个候选；请选择后查看，未自动锁定第 1 个。`;
  }

  candidateSelect.addEventListener('change', () => {
    if (!state.response || state.displayedFingerprint !== fingerprint()) {
      clearCandidateView();
      status.textContent = '输入已改变；当前 flow 已失效，请重新解析目标时点。';
      candidateSelect.value = '';
      return;
    }
    if (candidateSelect.value === '') {
      clearCandidateView();
      return;
    }
    const index = Number.parseInt(candidateSelect.value, 10);
    const candidates = state.response.bazi_target_flow_bundle.candidates;
    if (!Number.isInteger(index) || index < 0 || index >= candidates.length) return;
    renderCandidate(candidates[index], index, candidates.length);
  });

  function invalidateFlow() {
    if (!state.response) return;
    state.displayedFingerprint = null;
    hashBox.textContent = '-';
    hashBox.title = '';
    candidateSelect.hidden = true;
    clearCandidateView();
    status.textContent = '输入已改变；当前目标 flow 已失效，请显式重新解析。';
  }

  allFingerprintIds.forEach((id) => {
    const element = $(id);
    if (!element) return;
    element.addEventListener('input', invalidateFlow);
    element.addEventListener('change', invalidateFlow);
  });

  button.addEventListener('click', async () => {
    if (!sourceChartIsPresent()) {
      status.textContent = '请先完成联合排盘，再解析目标时点。';
      return;
    }
    const serial = ++state.serial;
    status.textContent = '正在解析八字目标时点…';
    clearCandidateView();
    candidateSelect.hidden = true;
    try {
      const response = await fetch('/api/resolve-flow', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload()),
      });
      const data = await response.json();
      if (!response.ok) throw data.error || {code: `HTTP_${response.status}`, detail: 'Target-flow request failed'};
      if (serial !== state.serial) return;
      state.response = data;
      state.displayedFingerprint = fingerprint();
      const bundle = data.bazi_target_flow_bundle;
      hashBox.textContent = shortHash(bundle.bundle_hash);
      hashBox.title = bundle.bundle_hash;
      configureCandidates(bundle);
    } catch (error) {
      if (serial !== state.serial) return;
      state.response = null;
      state.displayedFingerprint = null;
      hashBox.textContent = '-';
      status.textContent = `${error.code || 'LOCAL_APP_TARGET_FLOW_FAILED'}: ${error.detail || String(error)}`;
    }
  });

  const chartObserver = new MutationObserver(() => {
    if (sourceChartIsPresent()) {
      panel.hidden = false;
    } else {
      panel.hidden = true;
      invalidateFlow();
    }
  });
  chartObserver.observe(baziRoot, {childList: true, subtree: true});
  if (sourceChartIsPresent()) panel.hidden = false;
})();
"""
