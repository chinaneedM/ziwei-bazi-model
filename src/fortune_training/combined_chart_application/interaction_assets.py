from __future__ import annotations


def interaction_index_html(base_html: str) -> str:
    """Add the R1 Sanhe sidecar assets without mutating the frozen base asset constants."""

    if "/interaction.css" in base_html or "/interaction.js" in base_html:
        raise ValueError("interaction assets already injected")
    return base_html.replace(
        "</head>",
        '  <link rel="stylesheet" href="/interaction.css">\n</head>',
    ).replace(
        "</body>",
        '<script src="/interaction.js" defer></script>\n</body>',
    )


INTERACTION_CSS = """
.ziwei-interaction-panel { margin-bottom:10px; padding:10px; border:1px solid #d8dde2; border-radius:9px; background:#fafbfc; }
.ziwei-interaction-head { display:flex; align-items:flex-start; justify-content:space-between; gap:12px; margin-bottom:8px; }
.ziwei-interaction-head strong { font-size:13px; }
.ziwei-interaction-note,.ziwei-interaction-status { color:#68707a; font-size:11px; line-height:1.45; }
.ziwei-interaction-controls { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:7px; margin-bottom:8px; }
.ziwei-interaction-controls label { font-size:11px; }
.ziwei-interaction-origin { margin:7px 0; font-size:12px; font-weight:600; }
.ziwei-interaction-members { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:6px; margin:7px 0; }
.ziwei-interaction-member { padding:7px; border:1px solid #e0e3e6; border-radius:7px; background:#fff; font-size:11px; line-height:1.45; }
.ziwei-relative-roles { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:5px; }
.ziwei-relative-role { padding:6px 7px; border:1px solid #e7e9eb; border-radius:6px; background:#fff; font-size:10px; line-height:1.4; }
#ziwei-chart g[data-address-index] { cursor:pointer; }
#ziwei-chart g[data-address-index] > rect { transition:stroke-width .12s ease, fill .12s ease; }
#ziwei-chart g.sanhe-self > rect { stroke-width:4; fill:#fff6d6; }
#ziwei-chart g.sanhe-trine > rect { stroke-width:3; fill:#eef7ff; }
#ziwei-chart g.sanhe-opposition > rect { stroke-width:3; fill:#f7efff; }
#ziwei-chart g.sanhe-selected-origin > rect { stroke-dasharray:7 4; }
@media (max-width:900px) { .ziwei-interaction-controls,.ziwei-relative-roles { grid-template-columns:1fr; } .ziwei-interaction-members { grid-template-columns:1fr 1fr; } }
"""


INTERACTION_JS = """
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const root = $('ziwei-chart');
  if (!root) return;

  const state = {
    origin: 'LIFE',
    response: null,
    serial: 0,
    sidecarDirty: false,
    displayedInputFingerprint: null,
  };

  const panel = document.createElement('section');
  panel.id = 'ziwei-interaction-panel';
  panel.className = 'ziwei-interaction-panel';
  panel.hidden = true;
  panel.innerHTML = `
    <div class="ziwei-interaction-head">
      <div><strong>三合交互视图</strong><div class="ziwei-interaction-note">Sidecar 只更新紫微交互视图；不改写八字显示状态。宫位与三方四正均来自已发布 R2/R5。</div></div>
      <code id="ziwei-interaction-hash">-</code>
    </div>
    <div class="ziwei-interaction-controls">
      <label>大限<select id="ziwei-daxian-nav"></select></label>
      <label>流年<select id="ziwei-annual-nav"></select></label>
      <label>流月（常规月）<select id="ziwei-month-nav"></select></label>
      <label>小限<select id="ziwei-minor-nav"></select></label>
    </div>
    <div id="ziwei-interaction-status" class="ziwei-interaction-status">等待紫微盘</div>
    <div id="ziwei-interaction-origin" class="ziwei-interaction-origin"></div>
    <div id="ziwei-interaction-members" class="ziwei-interaction-members"></div>
    <div id="ziwei-relative-roles" class="ziwei-relative-roles"></div>
  `;
  root.parentNode.insertBefore(panel, root);

  const daxianNav = $('ziwei-daxian-nav');
  const annualNav = $('ziwei-annual-nav');
  const monthNav = $('ziwei-month-nav');
  const minorNav = $('ziwei-minor-nav');
  const status = $('ziwei-interaction-status');
  const originBox = $('ziwei-interaction-origin');
  const memberBox = $('ziwei-interaction-members');
  const roleBox = $('ziwei-relative-roles');
  const hashBox = $('ziwei-interaction-hash');

  const optionalInt = (id) => {
    const value = $(id).value.trim();
    return value === '' ? null : Number.parseInt(value, 10);
  };
  const optionalText = (id) => {
    const value = $(id).value.trim();
    return value === '' ? null : value;
  };
  const clear = (node) => { while (node.firstChild) node.removeChild(node.firstChild); };
  const textNode = (name, text, cls) => {
    const element = document.createElement(name);
    if (text !== undefined) element.textContent = text;
    if (cls) element.className = cls;
    return element;
  };

  function inputFingerprint() {
    const ids = [
      'birth-datetime', 'birth-place', 'latitude', 'longitude', 'timezone-id',
      'location-manual', 'sex', 'precision', 'uncertainty-seconds',
      'ziwei-daxian-count', 'ziwei-daxian-frame-id', 'ziwei-annual-year',
      'ziwei-lunar-month', 'ziwei-minor-limit-age', 'bazi-natal-profile', 'bazi-temporal-profile',
      'bazi-dayun-count',
    ];
    return JSON.stringify(ids.map((id) => {
      const element = $(id);
      return [id, element?.value ?? '', element?.checked ?? null];
    }));
  }

  function displayedInputIsCurrent() {
    return state.displayedInputFingerprint !== null
      && state.displayedInputFingerprint === inputFingerprint();
  }

  function staleSourceMessage() {
    status.textContent = '当前表单已改变，但画面仍是上一次排盘。请先点击“联合排盘”，再进行三合交互。';
  }

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
      ziwei_origin_designation_id: state.origin,
    };
  }

  function setOptions(select, rows, valueOf, labelOf, selectedValue) {
    clear(select);
    const none = document.createElement('option');
    none.value = '';
    none.textContent = '不选择';
    select.append(none);
    rows.forEach((row) => {
      const option = document.createElement('option');
      option.value = String(valueOf(row));
      option.textContent = labelOf(row);
      select.append(option);
    });
    select.value = selectedValue === null || selectedValue === undefined ? '' : String(selectedValue);
  }

  function renderTemporalOptions(response) {
    const options = response.temporal_options;
    const interaction = response.interaction;
    setOptions(
      daxianNav,
      options.daxian,
      (row) => row.frame_id,
      (row) => `${row.index} · ${row.nominal_age_start}-${row.nominal_age_end}岁 · ${row.active_palace_ganzhi}`,
      interaction.selected_daxian_frame_id,
    );
    setOptions(
      annualNav,
      options.annual,
      (row) => row.absolute_year,
      (row) => `${row.absolute_year} · ${row.year_stem}${row.year_branch} · ${row.nominal_age}岁`,
      interaction.selected_annual_year,
    );
    setOptions(
      monthNav,
      Array.from({length: 12}, (_, index) => index + 1),
      (month) => month,
      (month) => `${month}月`,
      optionalInt('ziwei-lunar-month'),
    );
    setOptions(
      minorNav,
      options.minor_limit,
      (row) => row.nominal_age,
      (row) => `${row.nominal_age}岁 · ${row.active_address.branch}`,
      interaction.selected_minor_limit_age,
    );
  }

  function designationMaps(response) {
    const byId = new Map();
    const byAddress = new Map();
    response.origin_options.forEach((row) => {
      byId.set(row.designation_id, row);
      byAddress.set(row.address_index, row);
    });
    return {byId, byAddress};
  }

  function renderInteraction(response) {
    const interaction = response.interaction;
    const maps = designationMaps(response);
    const origin = maps.byId.get(interaction.selected_origin_designation_id);
    hashBox.textContent = interaction.bundle_hash.slice(0, 16);
    hashBox.title = interaction.bundle_hash;
    status.textContent = state.sidecarDirty
      ? '当前为 Ziwei sidecar 交互视图；顶部组合哈希与下载仍对应最近一次“联合排盘”。'
      : '与最近一次联合排盘的 Ziwei bundle 一致。';
    originBox.textContent = `当前立太极：${origin?.designation_label || interaction.selected_origin_designation_id} · ${interaction.selected_origin_address.branch}`;

    clear(memberBox);
    interaction.sanfang_sizheng_frame.members.forEach((member) => {
      const target = maps.byId.get(member.target_designation_id);
      const borrow = member.borrowed_from_raw_address
        ? `借自 ${member.borrowed_from_raw_address.branch}；实体源 ${member.physical_source_address?.branch || '-'}`
        : '本宫实体';
      memberBox.append(textNode(
        'div',
        `${member.semantic_role} · ${target?.designation_label || member.target_designation_id} · ${member.target_raw_address.branch}\n${member.closure_status} · ${borrow}`,
        'ziwei-interaction-member',
      ));
    });

    clear(roleBox);
    interaction.relative_roles.forEach((row) => {
      const role = maps.byId.get(row.relative_role_designation_id);
      const target = maps.byId.get(row.target_designation_id);
      roleBox.append(textNode(
        'div',
        `${origin?.designation_label || interaction.selected_origin_designation_id}之${role?.designation_label || row.relative_role_designation_id} → ${target?.designation_label || row.target_designation_id} · ${row.target_address.branch}`,
        'ziwei-relative-role',
      ));
    });
  }

  function clearHighlights() {
    root.querySelectorAll('g[data-address-index]').forEach((group) => {
      group.classList.remove('sanhe-self', 'sanhe-trine', 'sanhe-opposition', 'sanhe-selected-origin');
      group.removeAttribute('data-sanhe-role');
    });
  }

  function applyHighlights(response) {
    clearHighlights();
    const interaction = response.interaction;
    interaction.sanfang_sizheng_frame.members.forEach((member) => {
      const addressIndex = member.target_raw_address.index;
      const group = root.querySelector(`g[data-address-index="${addressIndex}"]`);
      if (!group) return;
      group.dataset.sanheRole = member.semantic_role;
      if (member.semantic_role === 'SELF') group.classList.add('sanhe-self');
      else if (member.semantic_role === 'OPPOSITION') group.classList.add('sanhe-opposition');
      else group.classList.add('sanhe-trine');
    });
    const selected = root.querySelector(`g[data-address-index="${interaction.selected_origin_address.index}"]`);
    if (selected) selected.classList.add('sanhe-selected-origin');
  }

  let observer;
  function replaceZiweiSvg(svg) {
    if (observer) observer.disconnect();
    root.className = '';
    root.innerHTML = svg;
    state.displayedInputFingerprint = inputFingerprint();
    if (observer) observer.observe(root, {childList: true});
  }

  function bindPalaceClicks(response) {
    const maps = designationMaps(response);
    root.querySelectorAll('g[data-address-index]').forEach((group) => {
      if (group.dataset.sanheClickBound === '1') return;
      group.dataset.sanheClickBound = '1';
      group.setAttribute('role', 'button');
      group.setAttribute('tabindex', '0');
      const activate = () => {
        if (!displayedInputIsCurrent()) {
          staleSourceMessage();
          return;
        }
        const addressIndex = Number.parseInt(group.dataset.addressIndex, 10);
        const row = maps.byAddress.get(addressIndex);
        if (!row) return;
        state.origin = row.designation_id;
        resolveInteraction({replaceSvg: false, temporalChange: false});
      };
      group.addEventListener('click', activate);
      group.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          activate();
        }
      });
    });
  }

  async function resolveInteraction({replaceSvg, temporalChange}) {
    if (!root.querySelector('svg')) return;
    const serial = ++state.serial;
    panel.hidden = false;
    status.textContent = '正在更新三合交互视图…';
    const payload = requestPayload();
    try {
      const response = await fetch('/api/ziwei-interaction', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) throw data.error || {code: `HTTP_${response.status}`, detail: 'Interaction request failed'};
      if (serial !== state.serial) return;
      if (temporalChange) {
        state.sidecarDirty = true;
        $('download-manifest').disabled = true;
        $('download-ziwei').disabled = true;
      }
      state.response = data;
      if (replaceSvg) replaceZiweiSvg(data.ziwei_svg);
      renderTemporalOptions(data);
      renderInteraction(data);
      bindPalaceClicks(data);
      applyHighlights(data);
    } catch (error) {
      if (serial !== state.serial) return;
      status.textContent = `${error.code || 'LOCAL_APP_ZIWEI_INTERACTION_FAILED'}: ${error.detail || String(error)}`;
    }
  }

  function commitTemporalNavigation() {
    if (!displayedInputIsCurrent()) {
      staleSourceMessage();
      if (state.response) renderTemporalOptions(state.response);
      return;
    }
    $('ziwei-daxian-frame-id').value = daxianNav.value;
    $('ziwei-annual-year').value = annualNav.value;
    $('ziwei-lunar-month').value = monthNav.value;
    $('ziwei-minor-limit-age').value = minorNav.value;
    resolveInteraction({replaceSvg: true, temporalChange: true});
  }
  daxianNav.addEventListener('change', commitTemporalNavigation);
  annualNav.addEventListener('change', commitTemporalNavigation);
  monthNav.addEventListener('change', commitTemporalNavigation);
  minorNav.addEventListener('change', commitTemporalNavigation);

  observer = new MutationObserver(() => {
    if (!root.querySelector('svg')) {
      panel.hidden = true;
      state.response = null;
      state.displayedInputFingerprint = null;
      return;
    }
    state.sidecarDirty = false;
    state.displayedInputFingerprint = inputFingerprint();
    resolveInteraction({replaceSvg: false, temporalChange: false});
  });
  observer.observe(root, {childList: true});

  if (root.querySelector('svg')) {
    panel.hidden = false;
    state.displayedInputFingerprint = inputFingerprint();
    resolveInteraction({replaceSvg: false, temporalChange: false});
  }
})();
"""
