from __future__ import annotations


def ziwei_basic_info_index_html(base_html: str) -> str:
    """Add a read-only Ziwei natal/basic temporal projection to the workbench."""

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
@media (max-width:620px) { .ziwei-basic-info-grid { grid-template-columns:1fr 1fr; } }
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
  `;
  chartRoot.parentNode.insertBefore(panel, chartRoot);
  const grid = $('ziwei-basic-info-grid');

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

  function renderFromResolvePayload(payload) {
    const ziweiBundle = payload?.combined_resolution?.ziwei_bundle;
    const candidate = ziweiBundle?.candidate;
    const chart = candidate?.chart;
    const structure = chart?.structure;
    if (!chart || !structure) {
      clear(grid);
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
      panel.hidden = true;
    });
  }
})();
"""
