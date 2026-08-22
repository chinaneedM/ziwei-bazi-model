from __future__ import annotations


def nayin_index_html(base_html: str) -> str:
    if "/nayin.js" in base_html or "/nayin.css" in base_html:
        raise ValueError("nayin assets already injected")
    return base_html.replace(
        "</head>",
        '  <link rel="stylesheet" href="/nayin.css">\n</head>',
    ).replace(
        "</body>",
        '<script src="/nayin.js" defer></script>\n</body>',
    )


NAYIN_CSS = """
.pillar .bazi-nayin {
  margin-top:6px;
  padding-top:5px;
  border-top:1px dashed #e1e4e7;
  color:#5c6670;
  font-size:11px;
  line-height:1.35;
}
"""


NAYIN_JS = r"""
(() => {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const baziRoot = $('bazi-chart');
  if (!baziRoot) return;

  const expectedPositions = ['YEAR', 'MONTH', 'DAY', 'HOUR'];
  const sourceFieldIds = [
    'birth-datetime', 'birth-place', 'latitude', 'longitude', 'timezone-id',
    'location-manual', 'sex', 'precision', 'uncertainty-seconds',
    'ziwei-daxian-count', 'ziwei-daxian-frame-id', 'ziwei-annual-year',
    'ziwei-minor-limit-age', 'bazi-natal-profile', 'bazi-temporal-profile',
    'bazi-dayun-count',
  ];
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
      ziwei_minor_limit_age: optionalInt('ziwei-minor-limit-age'),
      bazi_natal_profile_id: $('bazi-natal-profile').value,
      bazi_temporal_profile_id: $('bazi-temporal-profile').value,
      bazi_dayun_count: Number.parseInt($('bazi-dayun-count').value, 10),
      combined_profile_id: 'ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1',
    };
  }

  function clearLabels() {
    baziRoot.querySelectorAll('.bazi-nayin').forEach((label) => label.remove());
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

  function renderFromResponse(response) {
    clearLabels();
    if (!response || !Array.isArray(response.candidates)) return;

    const selectedIndex = selectedApplicationCandidateIndex();
    if (!Number.isInteger(selectedIndex)) return;

    const selectedCandidate = response.candidates.find(
      (row) => row && row.application_candidate_index === selectedIndex
    );
    if (
      !selectedCandidate ||
      !Number.isInteger(selectedCandidate.natal_candidate_index) ||
      !selectedCandidate.nayin_resolution
    ) {
      return;
    }

    const annotations = selectedCandidate.nayin_resolution.annotations;
    const pillars = Array.from(baziRoot.querySelectorAll('.pillars .pillar'));
    if (!Array.isArray(annotations) || annotations.length !== 4 || pillars.length !== 4) {
      return;
    }

    const validated = [];
    for (let index = 0; index < expectedPositions.length; index += 1) {
      const annotation = annotations[index];
      const pillar = pillars[index];
      const position = pillar.querySelector('.pos')?.textContent?.trim();
      const ganzhi = pillar.querySelector('.ganzhi')?.textContent?.trim();
      if (
        !annotation ||
        annotation.source_pillar_position !== expectedPositions[index] ||
        position !== expectedPositions[index] ||
        ganzhi !== annotation.source_pillar_ganzhi ||
        typeof annotation.display_name !== 'string' ||
        annotation.display_name.trim() === ''
      ) {
        return;
      }
      validated.push([pillar, annotation.display_name.trim()]);
    }

    validated.forEach(([pillar, displayName]) => {
      const label = document.createElement('div');
      label.className = 'bazi-nayin';
      label.dataset.natalCandidateIndex = String(selectedCandidate.natal_candidate_index);
      label.textContent = `纳音：${displayName}`;
      pillar.append(label);
    });
  }

  async function refresh() {
    clearLabels();
    if (!sourceChartIsPresent()) return;

    const currentFingerprint = fingerprint();
    if (
      state.response &&
      state.responseFingerprint === currentFingerprint
    ) {
      renderFromResponse(state.response);
      return;
    }

    const serial = ++state.serial;
    try {
      const response = await fetch('/api/bazi-nayin-presentation', {
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
      if (serial === state.serial) clearLabels();
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
      clearLabels();
    };
    element.addEventListener('input', invalidate);
    element.addEventListener('change', invalidate);
  });

  const observer = new MutationObserver(() => scheduleRefresh());
  observer.observe(baziRoot, {childList: true});
  scheduleRefresh();
})();
"""
