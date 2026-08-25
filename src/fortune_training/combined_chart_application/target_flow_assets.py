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
.bazi-flow-annotation { margin-top:5px; padding-top:5px; border-top:1px dashed #e1e4e7; color:#4f5863; }
.bazi-flow-structural { margin:8px 0; padding:8px; border:1px solid #dfe3e6; border-radius:7px; background:#fff; font-size:11px; line-height:1.55; }
.bazi-flow-structural strong,.bazi-flow-structural code { display:block; }
.bazi-flow-structural-layer { margin-top:6px; padding:6px; border:1px solid #edf0f2; border-radius:5px; background:#fafbfb; }
.bazi-flow-support { margin:8px 0; padding:8px; border:1px solid #dfe3e6; border-radius:7px; background:#fffdf8; font-size:11px; line-height:1.55; }
.bazi-flow-support strong,.bazi-flow-support code { display:block; }
.bazi-flow-support-role { margin-top:5px; padding:5px; border:1px solid #eee6d8; border-radius:5px; background:#fff; }
.bazi-flow-relation { margin-top:5px; padding-top:5px; border-top:1px dashed #e1e4e7; word-break:break-word; }
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
      <div><strong>八字目标时点</strong><div class="bazi-target-flow-note">显式解析大运 / 小运候选 / 流年 / 流月 / 流日 / 流时。不会自动同步或改写紫微时间选择器。</div></div>
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
    <div id="bazi-flow-structural" class="bazi-flow-structural" hidden></div>
    <div id="bazi-flow-structural-support" class="bazi-flow-support" hidden></div>
    <div id="bazi-flow-lineage" class="bazi-flow-lineage" hidden></div>
  `;
  baziRoot.parentNode.insertBefore(panel, baziRoot);

  const button = $('resolve-target-flow');
  const candidateSelect = $('bazi-flow-candidate');
  const status = $('bazi-target-flow-status');
  const targetMeta = $('bazi-flow-target-meta');
  const framesRoot = $('bazi-flow-frames');
  const structuralRoot = $('bazi-flow-structural');
  const structuralSupportRoot = $('bazi-flow-structural-support');
  const lineageRoot = $('bazi-flow-lineage');
  const hashBox = $('bazi-flow-hash');

  const sourceFieldIds = [
    'birth-datetime', 'birth-place', 'latitude', 'longitude', 'timezone-id',
    'location-manual', 'sex', 'precision', 'uncertainty-seconds',
    'bazi-natal-profile', 'bazi-temporal-profile', 'bazi-dayun-count',
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

  function frameCard(label, frame, extra = '', annotationSlot = null) {
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
    if (annotationSlot?.status === 'RESOLVED' && annotationSlot.annotation) {
      const annotation = annotationSlot.annotation;
      const hidden = annotation.hidden_stems.map((row) => `${row.stem}·${row.ten_god}`).join(' / ');
      box.append(node(
        'div',
        `十神 ${annotation.visible_ten_god.display_name} · 藏干 ${hidden} · 纳音 ${annotation.nayin.display_name} · 旬空 ${annotation.xunkong.display_name} · 星运 ${annotation.day_master_twelve_growth.phase} · 自坐 ${annotation.self_twelve_growth.phase}`,
        'bazi-flow-annotation',
      ));
      box.append(node('code', `annotation_fact=${annotation.fact_hash}`));
    } else if (annotationSlot?.status) {
      box.append(node('div', `注释状态 ${annotationSlot.status}`, 'bazi-flow-annotation'));
    }
    return box;
  }

  function clearCandidateView() {
    clear(framesRoot);
    clear(structuralRoot);
    structuralRoot.hidden = true;
    clear(structuralSupportRoot);
    structuralSupportRoot.hidden = true;
    targetMeta.hidden = true;
    targetMeta.textContent = '';
    lineageRoot.hidden = true;
    lineageRoot.textContent = '';
  }

  function renderStructural(structural) {
    structuralRoot.hidden = false;
    structuralRoot.append(node('strong', '中性结构事实（当前版本仅大运 / 流年 / 流月）'));
    structuralRoot.append(node(
      'div',
      `覆盖 ${structural.active_layers.join(' / ')} · 未覆盖 ${structural.excluded_layers.join(' / ')} · 不判强弱、作用或合化成败`,
    ));
    const tenGodByTarget = new Map(
      structural.temporal_ten_gods.map((binding) => [binding.target_instance_id, binding]),
    );
    structural.active_temporal_stems.forEach((stem) => {
      const branch = structural.active_temporal_branches.find(
        (candidate) => candidate.position === stem.position,
      );
      const hidden = structural.temporal_hidden_stems.filter(
        (candidate) => candidate.branch_instance_id === branch?.instance_id,
      );
      const visibleTenGod = tenGodByTarget.get(stem.instance_id);
      const hiddenText = hidden.map((candidate) => {
        const binding = tenGodByTarget.get(candidate.instance_id);
        return `${candidate.stem}·${display(binding?.display_name)}`;
      }).join(' / ');
      const box = node('div', undefined, 'bazi-flow-structural-layer');
      box.append(node(
        'div',
        `${stem.position} ${stem.stem}${display(branch?.branch)} · 十神 ${display(visibleTenGod?.display_name)} · 藏干 ${hiddenText}`,
      ));
      box.append(node('code', `stem=${stem.instance_id}`));
      box.append(node('code', `branch=${display(branch?.instance_id)}`));
      structuralRoot.append(box);
    });
    structural.dynamic_exposures.forEach((exposure) => {
      const row = node(
        'div',
        `透干事实 ${exposure.stem} · ${exposure.hidden_stem_instance_id} → ${exposure.visible_stem_instance_id}`,
        'bazi-flow-relation',
      );
      row.append(node('code', `link_id=${exposure.link_id}`));
      row.append(node('code', `sources=${exposure.source_refs.join(',')}`));
      structuralRoot.append(row);
    });
    structural.dynamic_affinities.forEach((affinity) => {
      const exact = affinity.exact_hidden_stem_instance_ids.join(',') || '-';
      const sameElement = affinity.same_element_hidden_stem_instance_ids.join(',') || '-';
      const row = node(
        'div',
        `干支亲和 ${affinity.visible_stem_instance_id} ↔ ${affinity.branch_instance_id}`,
        'bazi-flow-relation',
      );
      row.append(node('code', `exact_hidden=${exact}`));
      row.append(node('code', `same_element_hidden=${sameElement}`));
      row.append(node('code', `fact_id=${affinity.fact_id}`));
      row.append(node('code', `rule=${affinity.rule_set_id}@${affinity.rule_set_version}`));
      row.append(node('code', `sources=${affinity.source_refs.join(',')}`));
      structuralRoot.append(row);
    });
    if (structural.relations.length === 0) {
      structuralRoot.append(node('div', '当前层组合没有结构关系事实。'));
    }
    structural.relations.forEach((relation) => {
      const nominal = relation.nominal_transformation_element
        ? ` · 名义目标五行 ${relation.nominal_transformation_element}（非成化结论）`
        : '';
      const row = node(
        'div',
        `${relation.relation_family} · ${relation.participant_layers.join(' + ')} · ${relation.relation_scope}${nominal}`,
        'bazi-flow-relation',
      );
      row.append(node('code', `participants=${relation.participant_instance_ids.join(',')}`));
      row.append(node('code', `relation_id=${relation.relation_id}`));
      row.append(node('code', `rule=${relation.rule_set_id}@${relation.rule_set_version}`));
      row.append(node('code', `sources=${relation.source_refs.join(',')}`));
      structuralRoot.append(row);
    });
    structuralRoot.append(node('code', `structural_projection_fact=${structural.fact_hash}`));
  }

  function renderStructuralSupport(support) {
    structuralSupportRoot.hidden = false;
    structuralSupportRoot.append(node('strong', '中性支持证据（原局月令与当前流月分列）'));
    structuralSupportRoot.append(node(
      'div',
      '仅列精确藏干匹配／同五行藏干候选；不判有根、强弱、权重或得令。',
    ));
    [support.natal_month_command, support.active_flow_solar_month].forEach((role) => {
      const label = role.role_id === 'NATAL_MONTH_COMMAND' ? '原局月令' : '当前流月';
      const ganzhi = role.natal_month_ganzhi || role.active_month_ganzhi;
      const box = node('div', `${label} · ${ganzhi} · ${role.branch}`, 'bazi-flow-support-role');
      box.append(node('code', `reference_id=${role.reference_id}`));
      box.append(node('code', `rule=${role.rule_set_id}@${role.rule_set_version}`));
      box.append(node('code', `sources=${role.source_refs.join(',')}`));
      structuralSupportRoot.append(box);
    });
    structuralSupportRoot.append(node(
      'div',
      `月令候选 ${support.natal_month_command_support_candidate_ids.length} · 当前流月候选 ${support.active_flow_solar_month_support_candidate_ids.length} · 全部候选 ${support.support_evidence_candidates.length}`,
    ));
    support.support_evidence_candidates.forEach((candidate) => {
      const roles = candidate.supporting_branch_role_ids.join(',') || '-';
      const exposures = candidate.source_exposure_link_ids.join(',') || '-';
      const row = node(
        'div',
        `${candidate.evidence_class} · ${candidate.visible_participant_layer} ${candidate.visible_stem_instance_id} ↔ ${candidate.supporting_branch_participant_layer} ${candidate.supporting_branch_instance_id}`,
        'bazi-flow-relation',
      );
      row.append(node('code', `hidden=${candidate.matching_hidden_stem_instance_ids.join(',')}`));
      row.append(node('code', `seasonal_roles=${roles}`));
      row.append(node('code', `affinity=${candidate.source_affinity_fact_id}`));
      row.append(node('code', `exposures=${exposures}`));
      row.append(node('code', `candidate_id=${candidate.candidate_id}`));
      row.append(node('code', `rule=${candidate.rule_set_id}@${candidate.rule_set_version}`));
      row.append(node('code', `sources=${candidate.source_refs.join(',')}`));
      structuralSupportRoot.append(row);
    });
    structuralSupportRoot.append(node('code', `support_projection_fact=${support.fact_hash}`));
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
    const annotations = view.timeline.classical_annotations;
    framesRoot.append(frameCard('大运', dayun, flow.active_dayun_kind, annotations.dayun));
    view.timeline.xiaoyun.candidates.forEach((row, rowIndex) => {
      framesRoot.append(frameCard(
        `小运候选 · ${row.profile_id}`,
        row.active_frame,
        `${row.direction} · ${row.activation_status}`,
        annotations.xiaoyun_candidates[rowIndex],
      ));
    });
    framesRoot.append(
      frameCard('流年', flow.annual, `${display(flow.annual?.start_term_chinese_name)} → ${display(flow.annual?.end_term_chinese_name)}`, annotations.annual),
      frameCard('流月', flow.monthly, `${display(flow.monthly?.start_jie_chinese_name)} → ${display(flow.monthly?.end_jie_chinese_name)}`, annotations.monthly),
      frameCard('流日', view.daily, display(view.daily?.effective_day_date), annotations.daily),
      frameCard('流时', view.hourly, display(view.hourly?.branch), annotations.hourly),
    );
    renderStructural(view.structural);
    renderStructuralSupport(view.structural_support);

    lineageRoot.hidden = false;
    lineageRoot.textContent = [
      `candidate_id=${candidate.candidate_id}`,
      `view_hash=${candidate.view_hash}`,
      `natal_fact=${candidate.natal_fact_hash}`,
      `temporal_fact=${candidate.temporal_fact_hash}`,
      `flow_fact=${candidate.flow_fact_hash}`,
      `structural_fact=${candidate.structural_fact_hash}`,
      `structural_support_fact=${candidate.structural_support_fact_hash}`,
      `daily_hourly_fact=${candidate.daily_hourly_fact_hash}`,
      `temporal_annotation_fact=${display(annotations.fact_hash)}`,
      `integrity target=${display(view.integrity?.target_coordinate)} flow=${display(view.integrity?.flow)} structural=${display(view.integrity?.structural)} daily_hourly=${display(view.integrity?.daily_hourly)}`,
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
