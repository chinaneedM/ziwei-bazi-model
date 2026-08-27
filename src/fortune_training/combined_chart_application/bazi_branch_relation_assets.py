from __future__ import annotations


def bazi_branch_relation_index_html(base_html: str) -> str:
    if "/bazi-branch-relations.js" in base_html or "/bazi-branch-relations.css" in base_html:
        raise ValueError("bazi branch relation assets already injected")
    marker = '<div id="bazi-chart" class="placeholder">等待排盘</div>'
    if marker not in base_html:
        raise ValueError("bazi chart mount point is unavailable")
    panel = (
        marker
        + '<section id="bazi-branch-relations" class="bazi-branch-relations" hidden></section>'
    )
    return (
        base_html.replace(marker, panel, 1)
        .replace(
            "</head>",
            '  <link rel="stylesheet" href="/bazi-branch-relations.css">\n</head>',
        )
        .replace(
            "</body>",
            '<script src="/bazi-branch-relations.js" defer></script>\n</body>',
        )
    )


BAZI_BRANCH_RELATION_CSS = """
.bazi-branch-relations {
  margin-top:12px;
  padding:10px 12px;
  border:1px solid #e1e4e7;
  border-radius:10px;
  background:rgba(127,127,127,.035);
}
.bazi-branch-relations-head {
  display:flex;
  align-items:baseline;
  justify-content:space-between;
  gap:10px;
  flex-wrap:wrap;
  margin-bottom:7px;
}
.bazi-branch-relations-head strong { font-size:13px; }
.bazi-branch-relations-note { color:#69727c; font-size:11px; }
.bazi-branch-relation-items { display:flex; gap:6px; flex-wrap:wrap; }
.bazi-branch-relation-item {
  display:inline-flex;
  gap:6px;
  align-items:center;
  padding:5px 8px;
  border:1px solid #dfe3e7;
  border-radius:8px;
  font-size:12px;
  line-height:1.35;
}
.bazi-branch-relation-item small { color:#737d86; }
"""


BAZI_BRANCH_RELATION_JS = r"""
(() => {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const baziRoot = $('bazi-chart');
  const panel = $('bazi-branch-relations');
  if (!baziRoot || !panel) return;

  const sourceFieldIds = [
    'birth-datetime', 'birth-place', 'latitude', 'longitude', 'timezone-id',
    'location-manual', 'sex', 'precision', 'uncertainty-seconds',
    'ziwei-daxian-count', 'ziwei-daxian-frame-id', 'ziwei-annual-year',
    'ziwei-lunar-month', 'ziwei-minor-limit-age', 'bazi-natal-profile',
    'bazi-temporal-profile', 'bazi-dayun-count',
  ];
  const familyLabels = {
    BRANCH_SIX_HARMONY: '六合',
    BRANCH_TRINE: '三合',
    BRANCH_CLASH: '六冲',
    BRANCH_CHUAN: '相穿 / 六害',
    BRANCH_PUNISHMENT: '相刑',
  };
  const positionLabels = {YEAR: '年', MONTH: '月', DAY: '日', HOUR: '时'};
  const state = {
    response: null,
    responseFingerprint: null,
    serial: 0,
    refreshTimer: null,
  };

  const optionalInt = (id) => {
    const value = $(id).value.trim();
    return value === '' ? null : Number.parseInt(value, 10);
  };
  const optionalText = (id) => {
    const value = $(id).value.trim();
    return value === '' ? null : value;
  };

  function fingerprint() {
    return JSON.stringify(sourceFieldIds.map((id) => {
      const element = $(id);
      return [id, element?.value ?? '', element?.checked ?? null];
    }));
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
    };
  }

  function clearPanel() {
    panel.replaceChildren();
    panel.hidden = true;
  }

  function sourceChartIsPresent() {
    return baziRoot.querySelectorAll('.pillars .pillar').length === 4;
  }

  function selectedApplicationCandidateIndex() {
    const selector = baziRoot.querySelector('.bazi-candidate-select');
    if (!selector) return 0;
    const index = Number.parseInt(selector.value, 10);
    return Number.isInteger(index) ? index : null;
  }

  function participantText(participant) {
    if (!participant || typeof participant.branch !== 'string') return null;
    const position = positionLabels[participant.position];
    if (!position) return null;
    return `${position}·${participant.branch}`;
  }

  function renderFromResponse(response) {
    clearPanel();
    if (!response || response.semantics !== 'RELATION_IDENTITY_ONLY') return;
    if (!Array.isArray(response.candidates)) return;
    const selectedIndex = selectedApplicationCandidateIndex();
    if (!Number.isInteger(selectedIndex)) return;
    const candidate = response.candidates.find(
      (row) => row && row.application_candidate_index === selectedIndex
    );
    if (!candidate || !Array.isArray(candidate.branch_relations)) return;

    const head = document.createElement('div');
    head.className = 'bazi-branch-relations-head';
    const title = document.createElement('strong');
    title.textContent = '本命地支关系事实';
    const note = document.createElement('span');
    note.className = 'bazi-branch-relations-note';
    note.textContent = '仅显示已发布关系身份；不判合化、成败、强弱或吉凶。';
    head.append(title, note);

    const items = document.createElement('div');
    items.className = 'bazi-branch-relation-items';
    candidate.branch_relations.forEach((relation) => {
      const family = familyLabels[relation?.relation_family];
      if (!family || !Array.isArray(relation.participants)) return;
      const participants = relation.participants.map(participantText);
      if (participants.some((value) => value === null)) return;
      const item = document.createElement('span');
      item.className = 'bazi-branch-relation-item';
      const body = document.createElement('span');
      const separator = relation.orientation === 'DIRECTED' ? ' → ' : ' · ';
      body.textContent = `${family}：${participants.join(separator)}`;
      item.append(body);
      if (Array.isArray(relation.source_refs) && relation.source_refs.length) {
        const source = document.createElement('small');
        source.textContent = relation.source_refs.join(' / ');
        item.append(source);
      }
      items.append(item);
    });
    if (!items.childElementCount) {
      const empty = document.createElement('span');
      empty.className = 'bazi-branch-relation-item';
      empty.textContent = '当前四支未命中已发布关系事实';
      items.append(empty);
    }
    panel.append(head, items);
    panel.dataset.natalCandidateIndex = String(candidate.natal_candidate_index);
    panel.hidden = false;
  }

  async function refresh() {
    clearPanel();
    if (!sourceChartIsPresent()) return;
    const currentFingerprint = fingerprint();
    if (state.response && state.responseFingerprint === currentFingerprint) {
      renderFromResponse(state.response);
      return;
    }
    const serial = ++state.serial;
    try {
      const response = await fetch('/api/bazi-branch-relations-presentation', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload()),
      });
      const data = await response.json();
      if (!response.ok) return;
      if (serial !== state.serial || currentFingerprint !== fingerprint()) return;
      state.response = data;
      state.responseFingerprint = currentFingerprint;
      renderFromResponse(data);
    } catch (_error) {
      if (serial === state.serial) clearPanel();
    }
  }

  function scheduleRefresh() {
    if (state.refreshTimer !== null) window.clearTimeout(state.refreshTimer);
    state.refreshTimer = window.setTimeout(() => {
      state.refreshTimer = null;
      void refresh();
    }, 0);
  }

  sourceFieldIds.forEach((id) => {
    const element = $(id);
    if (!element) return;
    const invalidate = () => {
      state.serial += 1;
      state.response = null;
      state.responseFingerprint = null;
      clearPanel();
    };
    element.addEventListener('input', invalidate);
    element.addEventListener('change', invalidate);
  });

  const observer = new MutationObserver(() => scheduleRefresh());
  observer.observe(baziRoot, {childList: true});
  scheduleRefresh();
})();
"""
