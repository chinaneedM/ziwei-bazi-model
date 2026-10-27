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
.bazi-jiaoyun-symbolic-age {
  margin:8px 0;
  padding:7px 9px;
  border:1px solid #e1e4e7;
  border-radius:7px;
  background:#fafbfc;
  color:#4f5863;
  font-size:11px;
  line-height:1.5;
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
    baziRoot.querySelectorAll('.bazi-jiaoyun-symbolic-age').forEach((row) => row.remove());
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

  function validNonNegativeInteger(value) {
    return Number.isInteger(value) && value >= 0;
  }

  function renderJiaoyunSymbolicAge(candidate, selectedIndex) {
    const jiaoyun = candidate?.view?.dayun?.jiaoyun;
    const symbolic = jiaoyun?.symbolic_age;
    if (
      !symbolic ||
      !validNonNegativeInteger(symbolic.years_360) ||
      !validNonNegativeInteger(symbolic.months_30) ||
      !validNonNegativeInteger(symbolic.days) ||
      !validNonNegativeInteger(symbolic.residual_microseconds)
    ) {
      return;
    }

    const row = document.createElement('div');
    row.className = 'bazi-jiaoyun-symbolic-age';
    row.dataset.applicationCandidateIndex = String(selectedIndex);
    row.textContent = (
      `起运岁数（符号年龄；360日年 / 30日月）：` +
      `${symbolic.years_360}年 ${symbolic.months_30}月 ${symbolic.days}日`
    );
    row.title = (
      `原始符号年龄余量：${symbolic.residual_microseconds} 微秒；` +
      `交运时点：${jiaoyun.first_transition_utc || '-'}；` +
      `节气锚点：${jiaoyun.anchor_jie_name || '-'}`
    );

    const dayunTable = baziRoot.querySelector('.dayun');
    baziRoot.insertBefore(row, dayunTable || null);
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
    renderJiaoyunSymbolicAge(candidate, selectedIndex);
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