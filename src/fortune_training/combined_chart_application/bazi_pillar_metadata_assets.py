from __future__ import annotations


def bazi_pillar_metadata_index_html(base_html: str) -> str:
    if "/bazi-pillar-metadata.js" in base_html or "/bazi-pillar-metadata.css" in base_html:
        raise ValueError("bazi pillar metadata assets already injected")
    return base_html.replace(
        "</head>",
        '  <link rel="stylesheet" href="/bazi-pillar-metadata.css">\n</head>',
    ).replace(
        "</body>",
        '<script src="/bazi-pillar-metadata.js" defer></script>\n</body>',
    )


BAZI_PILLAR_METADATA_CSS = """
.pillar .bazi-pillar-metadata {
  margin-top:5px;
  padding-top:5px;
  border-top:1px dashed #e1e4e7;
  color:#56606a;
  font-size:10px;
  line-height:1.45;
}
"""


BAZI_PILLAR_METADATA_JS = r"""
(() => {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const baziRoot = $('bazi-chart');
  if (!baziRoot) return;

  const expectedPositions = ['YEAR', 'MONTH', 'DAY', 'HOUR'];
  const state = {
    response: null,
    serial: 0,
    renderTimer: null,
  };

  function clearMetadata() {
    baziRoot.querySelectorAll('.bazi-pillar-metadata').forEach((row) => row.remove());
  }

  function selectedApplicationCandidateIndex() {
    const selector = baziRoot.querySelector('.bazi-candidate-select');
    if (!selector) return 0;
    const index = Number.parseInt(selector.value, 10);
    return Number.isInteger(index) ? index : null;
  }

  function validatedPillarBindings(candidate) {
    const sourcePillars = candidate?.view?.pillars;
    const renderedPillars = Array.from(baziRoot.querySelectorAll('.pillars .pillar'));
    if (
      !Array.isArray(sourcePillars) ||
      sourcePillars.length !== expectedPositions.length ||
      renderedPillars.length !== expectedPositions.length
    ) {
      return null;
    }

    const bindings = [];
    for (let index = 0; index < expectedPositions.length; index += 1) {
      const source = sourcePillars[index];
      const rendered = renderedPillars[index];
      const renderedPosition = rendered.querySelector('.pos')?.textContent?.trim();
      const renderedGanzhi = rendered.querySelector('.ganzhi')?.textContent?.trim();
      if (
        !source ||
        source.position !== expectedPositions[index] ||
        renderedPosition !== source.position ||
        renderedGanzhi !== source.ganzhi ||
        typeof source.stem_element !== 'string' ||
        source.stem_element.trim() === '' ||
        typeof source.stem_polarity !== 'string' ||
        source.stem_polarity.trim() === '' ||
        typeof source.branch_element_affiliation !== 'string' ||
        source.branch_element_affiliation.trim() === ''
      ) {
        return null;
      }
      bindings.push([rendered, source]);
    }
    return bindings;
  }

  function renderFromResponse(response) {
    clearMetadata();
    const bundle = response?.combined_resolution?.bazi_bundle;
    if (!bundle || !Array.isArray(bundle.candidates)) return;

    const selectedIndex = selectedApplicationCandidateIndex();
    if (
      !Number.isInteger(selectedIndex) ||
      selectedIndex < 0 ||
      selectedIndex >= bundle.candidates.length
    ) {
      return;
    }

    const candidate = bundle.candidates[selectedIndex];
    const bindings = validatedPillarBindings(candidate);
    if (!bindings) return;

    bindings.forEach(([pillar, source]) => {
      const row = document.createElement('div');
      row.className = 'bazi-pillar-metadata';
      row.dataset.applicationCandidateIndex = String(selectedIndex);
      row.dataset.pillarPosition = source.position;
      row.textContent = (
        `干五行：${source.stem_element} · 阴阳：${source.stem_polarity} · ` +
        `支五行：${source.branch_element_affiliation}`
      );
      pillar.append(row);
    });
  }

  function scheduleRender() {
    if (state.renderTimer !== null) window.clearTimeout(state.renderTimer);
    state.renderTimer = window.setTimeout(() => {
      state.renderTimer = null;
      renderFromResponse(state.response);
    }, 0);
  }

  baziRoot.addEventListener('change', (event) => {
    if (event.target?.classList?.contains('bazi-candidate-select')) scheduleRender();
  });

  const form = $('chart-form');
  if (form) {
    form.addEventListener('submit', () => {
      state.serial += 1;
      state.response = null;
      clearMetadata();
    });
  }

  const observer = new MutationObserver(() => scheduleRender());
  observer.observe(baziRoot, {childList: true, subtree: true});

  const originalFetch = window.fetch.bind(window);
  window.fetch = async (...args) => {
    const response = await originalFetch(...args);
    const request = args[0];
    const url = typeof request === 'string' ? request : request?.url;
    let pathname = null;
    try {
      pathname = url ? new URL(url, window.location.href).pathname : null;
    } catch (_error) {
      pathname = null;
    }
    if (pathname !== '/api/resolve') return response;

    const serial = ++state.serial;
    if (!response.ok) {
      state.response = null;
      clearMetadata();
      return response;
    }

    const copy = response.clone();
    void copy.json().then((data) => {
      if (serial !== state.serial) return;
      state.response = data;
      scheduleRender();
    }).catch(() => {
      if (serial === state.serial) {
        state.response = null;
        clearMetadata();
      }
    });
    return response;
  };
})();
"""
