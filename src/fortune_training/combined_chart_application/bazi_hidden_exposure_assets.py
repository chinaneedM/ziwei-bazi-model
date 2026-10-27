from __future__ import annotations


def bazi_hidden_exposure_index_html(base_html: str) -> str:
    if "/bazi-hidden-exposure.js" in base_html or "/bazi-hidden-exposure.css" in base_html:
        raise ValueError("bazi hidden exposure assets already injected")
    marker = '<div id="bazi-chart" class="placeholder">等待排盘</div>'
    if marker not in base_html:
        raise ValueError("bazi chart mount point is unavailable")
    panel = (
        marker
        + '<section id="bazi-hidden-exposure" class="bazi-hidden-exposure" hidden></section>'
    )
    return (
        base_html.replace(marker, panel, 1)
        .replace(
            "</head>",
            '  <link rel="stylesheet" href="/bazi-hidden-exposure.css">\n</head>',
        )
        .replace(
            "</body>",
            '<script src="/bazi-hidden-exposure.js" defer></script>\n</body>',
        )
    )


BAZI_HIDDEN_EXPOSURE_CSS = """
.bazi-hidden-exposure {
  margin-top:12px;
  padding:10px 12px;
  border:1px solid #e1e4e7;
  border-radius:10px;
  background:rgba(127,127,127,.035);
}
.bazi-hidden-exposure-head {
  display:flex;
  align-items:baseline;
  justify-content:space-between;
  gap:10px;
  flex-wrap:wrap;
  margin-bottom:7px;
}
.bazi-hidden-exposure-head strong { font-size:13px; }
.bazi-hidden-exposure-note { color:#69727c; font-size:11px; }
.bazi-hidden-exposure-items { display:flex; gap:6px; flex-wrap:wrap; }
.bazi-hidden-exposure-item {
  display:inline-flex;
  gap:6px;
  align-items:center;
  padding:5px 8px;
  border:1px solid #dfe3e7;
  border-radius:8px;
  font-size:12px;
  line-height:1.35;
}
.bazi-hidden-exposure-item small { color:#737d86; }
"""


BAZI_HIDDEN_EXPOSURE_JS = r"""
(() => {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const baziRoot = $('bazi-chart');
  const panel = $('bazi-hidden-exposure');
  if (!baziRoot || !panel) return;

  const sourceFieldIds = [
    'birth-datetime', 'birth-place', 'latitude', 'longitude', 'timezone-id',
    'location-manual', 'sex', 'precision', 'uncertainty-seconds',
    'ziwei-daxian-count', 'ziwei-daxian-frame-id', 'ziwei-annual-year',
    'ziwei-lunar-month', 'ziwei-minor-limit-age', 'bazi-natal-profile',
    'bazi-temporal-profile', 'bazi-dayun-count',
  ];
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

  function exposureText(exposure) {
    if (!exposure || exposure.match_kind !== 'EXACT_STEM') return null;
    const hidden = exposure.hidden_stem;
    const visible = exposure.visible_stem;
    if (!hidden || !visible || typeof exposure.stem !== 'string') return null;
    if (hidden.stem !== exposure.stem || visible.stem !== exposure.stem) return null;
    const hiddenPosition = positionLabels[hidden.branch_position];
    const visiblePosition = positionLabels[visible.position];
    if (!hiddenPosition || !visiblePosition) return null;
    return `${hiddenPosition}支藏·${exposure.stem} ↔ ${visiblePosition}干·${exposure.stem}`;
  }

  function renderFromResponse(response) {
    clearPanel();
    if (!response || response.semantics !== 'EXACT_STEM_IDENTITY_MATCH_ONLY') return;
    if (!Array.isArray(response.candidates)) return;
    const selectedIndex = selectedApplicationCandidateIndex();
    if (!Number.isInteger(selectedIndex)) return;
    const candidate = response.candidates.find(
      (row) => row && row.application_candidate_index === selectedIndex
    );
    if (!candidate || !Array.isArray(candidate.exposures)) return;

    const head = document.createElement('div');
    head.className = 'bazi-hidden-exposure-head';
    const title = document.createElement('strong');
    title.textContent = '本命藏干同干显干匹配';
    const note = document.createElement('span');
    note.className = 'bazi-hidden-exposure-note';
    note.textContent = '仅显示藏干与四柱显干的同干身份匹配；不判通根、得地、旺衰、喜用或吉凶。';
    head.append(title, note);

    const items = document.createElement('div');
    items.className = 'bazi-hidden-exposure-items';
    candidate.exposures.forEach((exposure) => {
      const text = exposureText(exposure);
      if (!text) return;
      const item = document.createElement('span');
      item.className = 'bazi-hidden-exposure-item';
      const body = document.createElement('span');
      body.textContent = text;
      item.append(body);
      if (Array.isArray(exposure.source_refs) && exposure.source_refs.length) {
        const source = document.createElement('small');
        source.textContent = exposure.source_refs.join(' / ');
        item.append(source);
      }
      items.append(item);
    });
    if (!items.childElementCount) {
      const empty = document.createElement('span');
      empty.className = 'bazi-hidden-exposure-item';
      empty.textContent = '当前四柱未命中藏干同干显干匹配';
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
      const response = await fetch('/api/bazi-hidden-exposure-presentation', {
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
