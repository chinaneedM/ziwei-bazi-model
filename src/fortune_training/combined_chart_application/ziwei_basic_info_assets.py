from __future__ import annotations


def ziwei_basic_info_index_html(base_html: str) -> str:
    """Add released Ziwei natal/basic temporal projections to the workbench."""

    if "/ziwei-basic-info.css" in base_html or "/ziwei-basic-info.js" in base_html:
        raise ValueError("ziwei-basic-info assets already injected")
    return base_html.replace(
        "</head>",
        '  <link rel="stylesheet" href="/ziwei-basic-info.css">\n</head>',
    ).replace(
        "</body>",
        '<script src="/ziwei-basic-info.js" defer></script>\n</body>',
    )


ZIWEI_BASIC_INFO_CSS = """
.ziwei-basic-info { margin:0 0 9px; padding:8px; border:1px solid #dfe3e6; border-radius:8px; background:#fafbfc; }
.ziwei-basic-info-head { display:flex; justify-content:space-between; gap:8px; margin-bottom:6px; font-size:11px; }
.ziwei-basic-info-head span { color:#6e7680; }
.ziwei-basic-info-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:6px; }
.ziwei-basic-info-item { min-width:0; padding:6px 7px; border:1px solid #e5e8eb; border-radius:6px; background:#fff; }
.ziwei-basic-info-item span { display:block; color:#777; font-size:9px; margin-bottom:2px; }
.ziwei-basic-info-item strong,.ziwei-basic-info-item code { display:block; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:11px; }
.ziwei-daxian-sequence,.ziwei-annual-sequence,.ziwei-monthly-sequence,.ziwei-minor-limit-sequence { margin-top:8px; padding-top:7px; border-top:1px solid #e5e8eb; }
.ziwei-daxian-sequence-head,.ziwei-annual-sequence-head,.ziwei-monthly-sequence-head,.ziwei-minor-limit-sequence-head { display:flex; justify-content:space-between; gap:8px; margin-bottom:5px; font-size:10px; }
.ziwei-daxian-sequence-head span,.ziwei-annual-sequence-head span,.ziwei-monthly-sequence-head span,.ziwei-minor-limit-sequence-head span { color:#777; }
.ziwei-daxian-sequence-list,.ziwei-annual-sequence-list,.ziwei-monthly-sequence-list,.ziwei-minor-limit-sequence-list { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:4px 6px; }
.ziwei-annual-sequence-list,.ziwei-monthly-sequence-list,.ziwei-minor-limit-sequence-list { max-height:280px; overflow:auto; padding-right:2px; }
.ziwei-daxian-sequence-row[type=button],.ziwei-annual-sequence-row[type=button],.ziwei-monthly-sequence-row[type=button],.ziwei-minor-limit-sequence-row[type=button] { width:100%; min-width:0; padding:5px 6px; border:1px solid #e8ebee; border-radius:5px; background:#fff; color:inherit; text-align:left; cursor:pointer; font:inherit; font-size:10px; line-height:1.35; }
.ziwei-daxian-sequence-row[type=button]:focus-visible,.ziwei-annual-sequence-row[type=button]:focus-visible,.ziwei-monthly-sequence-row[type=button]:focus-visible,.ziwei-minor-limit-sequence-row[type=button]:focus-visible { outline:2px solid #6b7280; outline-offset:1px; }
.ziwei-monthly-sequence-row[data-selected=true],.ziwei-minor-limit-sequence-row[data-selected=true] { border-width:2px; font-weight:600; }
.ziwei-daxian-sequence-row strong,.ziwei-annual-sequence-row strong,.ziwei-monthly-sequence-row strong,.ziwei-minor-limit-sequence-row strong { display:block; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:10px; }
.ziwei-daxian-sequence-row span,.ziwei-annual-sequence-row span,.ziwei-monthly-sequence-row span,.ziwei-minor-limit-sequence-row span { display:block; color:#666; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:9px; }
@media (max-width:620px) { .ziwei-basic-info-grid,.ziwei-daxian-sequence-list,.ziwei-annual-sequence-list,.ziwei-monthly-sequence-list,.ziwei-minor-limit-sequence-list { grid-template-columns:1fr 1fr; } }
@media (max-width:440px) { .ziwei-daxian-sequence-list,.ziwei-annual-sequence-list,.ziwei-monthly-sequence-list,.ziwei-minor-limit-sequence-list { grid-template-columns:1fr; } }
"""


ZIWEI_BASIC_INFO_JS = r"""
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const chartRoot = $('ziwei-chart');
  if (!chartRoot || typeof window.fetch !== 'function') return;

  const panel = document.createElement('section');
  panel.id = 'ziwei-basic-info';
  panel.className = 'ziwei-basic-info';
  panel.hidden = true;
  panel.innerHTML = `
    <div class="ziwei-basic-info-head">
      <strong>紫微基本信息</strong>
      <span>直接读取已发布 Natal / Temporal Bundle · 不在浏览器重算</span>
    </div>
    <div id="ziwei-basic-info-grid" class="ziwei-basic-info-grid"></div>
    <div id="ziwei-daxian-sequence" class="ziwei-daxian-sequence" hidden>
      <div class="ziwei-daxian-sequence-head">
        <strong>完整大限序列</strong>
        <span>released 大限帧 · 点击填入目标</span>
      </div>
      <div id="ziwei-daxian-sequence-list" class="ziwei-daxian-sequence-list"></div>
    </div>
    <div id="ziwei-annual-sequence" class="ziwei-annual-sequence" hidden>
      <div class="ziwei-annual-sequence-head">
        <strong>完整流年序列</strong>
        <span>released 流年帧 · 点击填入流年目标</span>
      </div>
      <div id="ziwei-annual-sequence-list" class="ziwei-annual-sequence-list"></div>
    </div>
    <div id="ziwei-monthly-sequence" class="ziwei-monthly-sequence" hidden>
      <div class="ziwei-monthly-sequence-head">
        <strong>完整流月序列</strong>
        <span>released 常规农历月帧 · 点击填入流月目标</span>
      </div>
      <div id="ziwei-monthly-sequence-list" class="ziwei-monthly-sequence-list"></div>
    </div>
    <div id="ziwei-minor-limit-sequence" class="ziwei-minor-limit-sequence" hidden>
      <div class="ziwei-minor-limit-sequence-head">
        <strong>完整小限序列</strong>
        <span>released 小限帧 · 点击填入小限岁数</span>
      </div>
      <div id="ziwei-minor-limit-sequence-list" class="ziwei-minor-limit-sequence-list"></div>
    </div>
  `;
  chartRoot.parentNode.insertBefore(panel, chartRoot);
  const grid = $('ziwei-basic-info-grid');
  const daxianSection = $('ziwei-daxian-sequence');
  const daxianList = $('ziwei-daxian-sequence-list');
  const annualSection = $('ziwei-annual-sequence');
  const annualList = $('ziwei-annual-sequence-list');
  const monthlySection = $('ziwei-monthly-sequence');
  const monthlyList = $('ziwei-monthly-sequence-list');
  const minorLimitSection = $('ziwei-minor-limit-sequence');
  const minorLimitList = $('ziwei-minor-limit-sequence-list');

  const elementLabels = {
    WOOD: '木', FIRE: '火', EARTH: '土', METAL: '金', WATER: '水',
    木: '木', 火: '火', 土: '土', 金: '金', 水: '水',
  };
  const temporalFrameOrder = ['DAXIAN', 'ANNUAL', 'MONTH'];
  const temporalFrameLabels = {DAXIAN: '大限', ANNUAL: '流年', MONTH: '流月'};
  const clear = (node) => { while (node.firstChild) node.removeChild(node.firstChild); };
  const item = (label, value, useCode = false) => {
    const box = document.createElement('div');
    box.className = 'ziwei-basic-info-item';
    const key = document.createElement('span');
    key.textContent = label;
    const content = document.createElement(useCode ? 'code' : 'strong');
    content.textContent = value ?? '-';
    content.title = content.textContent;
    box.append(key, content);
    return box;
  };

  function role(chart, roleId) {
    const row = (chart?.role_bindings || []).find((candidate) => candidate.role_id === roleId);
    return row?.entity_display_name || '-';
  }

  function palaceGanzhi(structure, palaceAddress) {
    if (
      !structure ||
      !Number.isInteger(palaceAddress?.index) ||
      typeof palaceAddress?.branch !== 'string' ||
      !palaceAddress.branch
    ) return '-';
    const matches = (structure.address_attributes || []).filter((row) => (
      row?.address?.index === palaceAddress.index &&
      row?.address?.branch === palaceAddress.branch &&
      typeof row?.stem === 'string' &&
      row.stem
    ));
    if (matches.length !== 1) return '-';
    return `${matches[0].stem}${palaceAddress.branch}`;
  }

  function ziYearDoujun(temporalState) {
    const rows = (temporalState?.annual_frames || []).filter((row) => row?.year_branch === '子');
    if (!rows.length) return '-';
    if (rows.some((row) => (
      !Number.isInteger(row?.doujun_address?.index) ||
      typeof row?.doujun_address?.branch !== 'string' ||
      !row.doujun_address.branch
    ))) return '-';
    const expected = rows[0].doujun_address;
    if (!rows.every((row) => (
      row.doujun_address.index === expected.index &&
      row.doujun_address.branch === expected.branch
    ))) return '-';
    return expected.branch;
  }

  function daxianSequence(temporalState) {
    const rows = temporalState?.daxian_frames;
    if (!Array.isArray(rows) || !rows.length) return null;
    const frameIds = new Set();
    const indexes = new Set();
    const released = [];
    for (const row of rows) {
      if (
        typeof row?.frame_id !== 'string' || !row.frame_id ||
        !Number.isInteger(row?.index) ||
        !Number.isInteger(row?.nominal_age_start) ||
        !Number.isInteger(row?.nominal_age_end) ||
        !Number.isInteger(row?.absolute_year_start) ||
        !Number.isInteger(row?.absolute_year_end) ||
        !Number.isInteger(row?.active_address?.index) ||
        typeof row?.active_address?.branch !== 'string' || !row.active_address.branch ||
        typeof row?.active_palace_ganzhi !== 'string' || !row.active_palace_ganzhi ||
        row.nominal_age_start > row.nominal_age_end ||
        row.absolute_year_start > row.absolute_year_end ||
        frameIds.has(row.frame_id) || indexes.has(row.index)
      ) return null;
      frameIds.add(row.frame_id);
      indexes.add(row.index);
      released.push({
        frameId: row.frame_id,
        index: row.index,
        nominalAgeStart: row.nominal_age_start,
        nominalAgeEnd: row.nominal_age_end,
        absoluteYearStart: row.absolute_year_start,
        absoluteYearEnd: row.absolute_year_end,
        activeAddressIndex: row.active_address.index,
        activeBranch: row.active_address.branch,
        activePalaceGanzhi: row.active_palace_ganzhi,
      });
    }
    return released;
  }

  function fillDaxianTarget(frameId) {
    const target = $('ziwei-daxian-frame-id');
    if (!target || typeof frameId !== 'string' || !frameId) return;
    target.value = frameId;
    target.dispatchEvent(new Event('input', { bubbles: true }));
    target.dispatchEvent(new Event('change', { bubbles: true }));
    target.focus();
  }

  function renderDaxianSequence(temporalState) {
    clear(daxianList);
    const rows = daxianSequence(temporalState);
    if (!rows) {
      daxianSection.hidden = true;
      return;
    }
    rows.forEach((row) => {
      const box = document.createElement('button');
      box.type = 'button';
      box.className = 'ziwei-daxian-sequence-row';
      box.dataset.frameId = row.frameId;
      box.dataset.frameIndex = String(row.index);
      box.dataset.addressIndex = String(row.activeAddressIndex);
      box.addEventListener('click', () => fillDaxianTarget(row.frameId));
      const period = document.createElement('strong');
      period.textContent = `${row.frameId} · 虚岁 ${row.nominalAgeStart}–${row.nominalAgeEnd}`;
      const coordinate = document.createElement('span');
      coordinate.textContent = `${row.absoluteYearStart}–${row.absoluteYearEnd} · 落宫 ${row.activePalaceGanzhi}（${row.activeBranch}）`;
      box.append(period, coordinate);
      daxianList.appendChild(box);
    });
    daxianSection.hidden = false;
  }

  function annualSequence(temporalState) {
    const rows = temporalState?.annual_frames;
    if (!Array.isArray(rows) || !rows.length) return null;
    const frameIds = new Set();
    const years = new Set();
    const released = [];
    for (const row of rows) {
      const parentDaxianFrameId = row?.parent_daxian_frame_id;
      if (
        typeof row?.frame_id !== 'string' || !row.frame_id ||
        !Number.isInteger(row?.absolute_year) ||
        !Number.isInteger(row?.nominal_age) || row.nominal_age < 1 ||
        typeof row?.year_stem !== 'string' || !row.year_stem ||
        typeof row?.year_branch !== 'string' || !row.year_branch ||
        !Number.isInteger(row?.active_address?.index) ||
        typeof row?.active_address?.branch !== 'string' || !row.active_address.branch ||
        typeof row?.active_palace_ganzhi !== 'string' || !row.active_palace_ganzhi ||
        !Number.isInteger(row?.doujun_address?.index) ||
        typeof row?.doujun_address?.branch !== 'string' || !row.doujun_address.branch ||
        typeof row?.doujun_rule_id !== 'string' || !row.doujun_rule_id ||
        (parentDaxianFrameId !== null && (
          typeof parentDaxianFrameId !== 'string' || !parentDaxianFrameId
        )) ||
        frameIds.has(row.frame_id) || years.has(row.absolute_year)
      ) return null;
      frameIds.add(row.frame_id);
      years.add(row.absolute_year);
      released.push({
        frameId: row.frame_id,
        absoluteYear: row.absolute_year,
        nominalAge: row.nominal_age,
        yearStem: row.year_stem,
        yearBranch: row.year_branch,
        activeAddressIndex: row.active_address.index,
        activeBranch: row.active_address.branch,
        activePalaceGanzhi: row.active_palace_ganzhi,
        doujunAddressIndex: row.doujun_address.index,
        doujunBranch: row.doujun_address.branch,
        doujunRuleId: row.doujun_rule_id,
        parentDaxianFrameId,
      });
    }
    return released;
  }

  function fillAnnualTarget(absoluteYear) {
    const target = $('ziwei-annual-year');
    if (!target || !Number.isInteger(absoluteYear)) return;
    target.value = String(absoluteYear);
    target.dispatchEvent(new Event('input', { bubbles: true }));
    target.dispatchEvent(new Event('change', { bubbles: true }));
    target.focus();
  }

  function renderAnnualSequence(temporalState) {
    clear(annualList);
    const rows = annualSequence(temporalState);
    if (!rows) {
      annualSection.hidden = true;
      return;
    }
    rows.forEach((row) => {
      const box = document.createElement('button');
      box.type = 'button';
      box.className = 'ziwei-annual-sequence-row';
      box.dataset.frameId = row.frameId;
      box.dataset.absoluteYear = String(row.absoluteYear);
      box.dataset.nominalAge = String(row.nominalAge);
      box.dataset.addressIndex = String(row.activeAddressIndex);
      if (row.parentDaxianFrameId) box.dataset.parentDaxianFrameId = row.parentDaxianFrameId;
      box.addEventListener('click', () => fillAnnualTarget(row.absoluteYear));
      const period = document.createElement('strong');
      period.textContent = `${row.frameId} · ${row.yearStem}${row.yearBranch} · 虚岁 ${row.nominalAge}`;
      const coordinate = document.createElement('span');
      coordinate.textContent = `${row.absoluteYear} · 落宫 ${row.activePalaceGanzhi}（${row.activeBranch}） · 斗君 ${row.doujunBranch}`;
      box.append(period, coordinate);
      annualList.appendChild(box);
    });
    annualSection.hidden = false;
  }

  function monthlySequence(temporalState) {
    const rows = temporalState?.monthly_frames;
    if (!Array.isArray(rows) || rows.length !== 12) return null;
    const frameIds = new Set();
    const lunarMonths = new Set();
    const years = new Set();
    const parentAnnualFrameIds = new Set();
    const released = [];
    for (const row of rows) {
      const sourceRefs = row?.source_refs;
      if (
        typeof row?.frame_id !== 'string' || !row.frame_id ||
        !Number.isInteger(row?.absolute_year) ||
        !Number.isInteger(row?.lunar_month) || row.lunar_month < 1 || row.lunar_month > 12 ||
        typeof row?.month_stem !== 'string' || !row.month_stem ||
        typeof row?.month_branch !== 'string' || !row.month_branch ||
        typeof row?.month_ganzhi !== 'string' || !row.month_ganzhi ||
        !Number.isInteger(row?.active_address?.index) ||
        typeof row?.active_address?.branch !== 'string' || !row.active_address.branch ||
        typeof row?.parent_annual_frame_id !== 'string' || !row.parent_annual_frame_id ||
        typeof row?.monthly_rule_id !== 'string' || !row.monthly_rule_id ||
        typeof row?.month_ganzhi_rule_id !== 'string' || !row.month_ganzhi_rule_id ||
        typeof row?.calendar_scope !== 'string' || !row.calendar_scope ||
        typeof row?.leap_month_policy_status !== 'string' || !row.leap_month_policy_status ||
        !Array.isArray(sourceRefs) || !sourceRefs.length ||
        sourceRefs.some((sourceRef) => typeof sourceRef !== 'string' || !sourceRef) ||
        frameIds.has(row.frame_id) || lunarMonths.has(row.lunar_month)
      ) return null;
      frameIds.add(row.frame_id);
      lunarMonths.add(row.lunar_month);
      years.add(row.absolute_year);
      parentAnnualFrameIds.add(row.parent_annual_frame_id);
      released.push({
        frameId: row.frame_id,
        absoluteYear: row.absolute_year,
        lunarMonth: row.lunar_month,
        monthStem: row.month_stem,
        monthBranch: row.month_branch,
        monthGanzhi: row.month_ganzhi,
        activeAddressIndex: row.active_address.index,
        activeBranch: row.active_address.branch,
        parentAnnualFrameId: row.parent_annual_frame_id,
        monthlyRuleId: row.monthly_rule_id,
        monthGanzhiRuleId: row.month_ganzhi_rule_id,
        calendarScope: row.calendar_scope,
        leapMonthPolicyStatus: row.leap_month_policy_status,
        sourceRefs: [...sourceRefs],
      });
    }
    if (years.size !== 1 || parentAnnualFrameIds.size !== 1 || lunarMonths.size !== 12) return null;
    return released;
  }

  function fillMonthlyTarget(lunarMonth) {
    const target = $('ziwei-lunar-month');
    if (!target || !Number.isInteger(lunarMonth) || lunarMonth < 1 || lunarMonth > 12) return;
    target.value = String(lunarMonth);
    target.dispatchEvent(new Event('input', { bubbles: true }));
    target.dispatchEvent(new Event('change', { bubbles: true }));
    target.focus();
  }

  function renderMonthlySequence(temporalState, selectedMonthly) {
    clear(monthlyList);
    const rows = monthlySequence(temporalState);
    if (!rows) {
      monthlySection.hidden = true;
      return;
    }
    rows.forEach((row) => {
      const box = document.createElement('button');
      box.type = 'button';
      box.className = 'ziwei-monthly-sequence-row';
      box.dataset.frameId = row.frameId;
      box.dataset.absoluteYear = String(row.absoluteYear);
      box.dataset.lunarMonth = String(row.lunarMonth);
      box.dataset.addressIndex = String(row.activeAddressIndex);
      box.dataset.parentAnnualFrameId = row.parentAnnualFrameId;
      const selected = (
        selectedMonthly?.frame_id === row.frameId &&
        selectedMonthly?.absolute_year === row.absoluteYear &&
        selectedMonthly?.lunar_month === row.lunarMonth
      );
      if (selected) {
        box.dataset.selected = 'true';
        box.setAttribute('aria-current', 'true');
      }
      box.addEventListener('click', () => fillMonthlyTarget(row.lunarMonth));
      const period = document.createElement('strong');
      period.textContent = `${row.frameId} · ${row.monthGanzhi} · 农历 ${row.lunarMonth}月`;
      const coordinate = document.createElement('span');
      coordinate.textContent = `${row.absoluteYear} · 落宫 ${row.activeBranch} · ${row.calendarScope} · 闰月 ${row.leapMonthPolicyStatus}`;
      box.append(period, coordinate);
      monthlyList.appendChild(box);
    });
    monthlySection.hidden = false;
  }

  function minorLimitSequence(temporalState) {
    const rows = temporalState?.minor_limit_frames;
    if (!Array.isArray(rows) || !rows.length) return null;
    const frameIds = new Set();
    const ages = new Set();
    const released = [];
    for (const row of rows) {
      const sourceRefs = row?.source_refs;
      if (
        typeof row?.frame_id !== 'string' || !row.frame_id ||
        !Number.isInteger(row?.nominal_age) || row.nominal_age < 1 ||
        !Number.isInteger(row?.active_address?.index) ||
        typeof row?.active_address?.branch !== 'string' || !row.active_address.branch ||
        !Array.isArray(sourceRefs) || !sourceRefs.length ||
        sourceRefs.some((sourceRef) => typeof sourceRef !== 'string' || !sourceRef) ||
        frameIds.has(row.frame_id) || ages.has(row.nominal_age)
      ) return null;
      frameIds.add(row.frame_id);
      ages.add(row.nominal_age);
      released.push({
        frameId: row.frame_id,
        nominalAge: row.nominal_age,
        activeAddressIndex: row.active_address.index,
        activeBranch: row.active_address.branch,
        sourceRefs: [...sourceRefs],
      });
    }
    return released;
  }

  function fillMinorLimitTarget(nominalAge) {
    const target = $('ziwei-minor-limit-age');
    if (!target || !Number.isInteger(nominalAge) || nominalAge < 1) return;
    target.value = String(nominalAge);
    target.dispatchEvent(new Event('input', { bubbles: true }));
    target.dispatchEvent(new Event('change', { bubbles: true }));
    target.focus();
  }

  function renderMinorLimitSequence(temporalState, selectedMinorLimit) {
    clear(minorLimitList);
    const rows = minorLimitSequence(temporalState);
    if (!rows) {
      minorLimitSection.hidden = true;
      return;
    }
    rows.forEach((row) => {
      const box = document.createElement('button');
      box.type = 'button';
      box.className = 'ziwei-minor-limit-sequence-row';
      box.dataset.frameId = row.frameId;
      box.dataset.nominalAge = String(row.nominalAge);
      box.dataset.addressIndex = String(row.activeAddressIndex);
      const selected = (
        selectedMinorLimit?.frame_id === row.frameId &&
        selectedMinorLimit?.nominal_age === row.nominalAge
      );
      if (selected) {
        box.dataset.selected = 'true';
        box.setAttribute('aria-current', 'true');
      }
      box.addEventListener('click', () => fillMinorLimitTarget(row.nominalAge));
      const period = document.createElement('strong');
      period.textContent = `${row.frameId} · 虚岁 ${row.nominalAge}`;
      const coordinate = document.createElement('span');
      coordinate.textContent = `落宫 ${row.activeBranch} · 来源 ${row.sourceRefs.join(' / ')}`;
      box.append(period, coordinate);
      minorLimitList.appendChild(box);
    });
    minorLimitSection.hidden = false;
  }

  function limitFlowOverlap(view) {
    const grouped = new Map();
    (view?.cells || []).forEach((cell) => {
      const byType = new Map();
      (cell.temporal_designations || []).forEach((row) => {
        if (row.designation_id !== 'LIFE' || !temporalFrameOrder.includes(row.frame_type)) return;
        if (!byType.has(row.frame_type)) byType.set(row.frame_type, row.frame_id);
      });
      if (byType.size >= 2) {
        const types = temporalFrameOrder.filter((frameType) => byType.has(frameType));
        grouped.set(cell.address_index, {
          types,
          address: `${cell.stem || ''}${cell.branch || ''}` || String(cell.address_index),
        });
      }
    });
    const overlaps = [...grouped.entries()]
      .sort(([left], [right]) => left - right)
      .map(([, row]) => `${row.types.map((frameType) => temporalFrameLabels[frameType]).join('/')}@${row.address}`);
    return overlaps.length ? overlaps.join('；') : '无';
  }

  function clearTemporalSequences() {
    clear(daxianList);
    clear(annualList);
    clear(monthlyList);
    clear(minorLimitList);
    daxianSection.hidden = true;
    annualSection.hidden = true;
    monthlySection.hidden = true;
    minorLimitSection.hidden = true;
  }

  function renderFromResolvePayload(payload) {
    const ziweiBundle = payload?.combined_resolution?.ziwei_bundle;
    const candidate = ziweiBundle?.candidate;
    const chart = candidate?.chart;
    const structure = chart?.structure;
    if (!chart || !structure) {
      clear(grid);
      clearTemporalSequences();
      panel.hidden = true;
      return;
    }
    const bureau = structure.bureau || {};
    const element = elementLabels[bureau.element] || bureau.element || '-';
    const bureauText = bureau.number ? `${element}${bureau.number}局` : '-';
    clear(grid);
    grid.append(
      item('五行局', bureauText),
      item('命宫干支', bureau.life_palace_ganzhi || '-'),
      item('局纳音', bureau.nayin_name || '-'),
      item('命主', role(chart, 'ROLE.MINGZHU')),
      item('身主', role(chart, 'ROLE.SHENZHU')),
      item('命宫', structure.life_address?.branch || '-'),
      item('身宫', structure.body_address?.branch || '-'),
      item('身宫干支', palaceGanzhi(structure, structure.body_address)),
      item('子年斗君', ziYearDoujun(ziweiBundle?.temporal_state)),
      item('紫微年', `${structure.ziwei_birth_year_stem || ''}${structure.ziwei_birth_year_branch || ''}` || '-'),
      item('农历月坐标', String(structure.natal_month_coordinate ?? '-')),
      item('农历日', String(structure.lunar_birth_day ?? '-')),
      item('出生时支', structure.birth_hour_branch?.branch || '-'),
      item('限流叠宫', limitFlowOverlap(ziweiBundle?.view_model)),
      item('Natal FactHash', candidate.hashes?.fact_hash || '-', true),
      item('Natal ComputationHash', candidate.hashes?.computation_hash || '-', true),
    );
    renderDaxianSequence(ziweiBundle?.temporal_state);
    renderAnnualSequence(ziweiBundle?.temporal_state);
    renderMonthlySequence(
      ziweiBundle?.temporal_state,
      ziweiBundle?.view_model?.selected_temporal_frame_summary?.monthly,
    );
    renderMinorLimitSequence(
      ziweiBundle?.temporal_state,
      ziweiBundle?.view_model?.selected_temporal_frame_summary?.minor_limit,
    );
    panel.hidden = false;
  }

  const nativeFetch = window.fetch.bind(window);
  window.fetch = async (...args) => {
    const response = await nativeFetch(...args);
    const input = args[0];
    const rawUrl = typeof input === 'string' ? input : input?.url;
    let path = '';
    try {
      path = new URL(rawUrl, window.location.href).pathname;
    } catch (_) {
      return response;
    }
    if (path === '/api/resolve' && response.ok) {
      const copy = response.clone();
      window.setTimeout(async () => {
        try {
          renderFromResolvePayload(await copy.json());
        } catch (_) {
          clear(grid);
          clearTemporalSequences();
          panel.hidden = true;
        }
      }, 0);
    }
    return response;
  };

  const form = $('chart-form');
  if (form) {
    form.addEventListener('submit', () => {
      clear(grid);
      clearTemporalSequences();
      panel.hidden = true;
    });
  }
})();
"""
