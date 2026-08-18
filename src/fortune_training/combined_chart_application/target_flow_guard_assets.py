from __future__ import annotations


TARGET_FLOW_GUARD_JS = """
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const baziRoot = $('bazi-chart');
  const button = $('resolve-target-flow');
  const status = $('bazi-target-flow-status');
  const hashBox = $('bazi-flow-hash');
  const candidateSelect = $('bazi-flow-candidate');
  const targetMeta = $('bazi-flow-target-meta');
  const framesRoot = $('bazi-flow-frames');
  const lineageRoot = $('bazi-flow-lineage');
  if (!baziRoot || !button || !status) return;

  const sourceFieldIds = [
    'birth-datetime', 'birth-place', 'latitude', 'longitude', 'timezone-id',
    'location-manual', 'sex', 'precision', 'uncertainty-seconds',
    'bazi-natal-profile', 'bazi-temporal-profile', 'bazi-dayun-count',
  ];
  let displayedSourceFingerprint = null;

  function sourceFingerprint() {
    return JSON.stringify(sourceFieldIds.map((id) => {
      const element = $(id);
      return [id, element?.value ?? '', element?.checked ?? null];
    }));
  }

  function sourceChartIsPresent() {
    return Boolean(baziRoot.querySelector('.pillars, .bazi-candidate-bar, table'));
  }

  function captureDisplayedSource() {
    displayedSourceFingerprint = sourceChartIsPresent() ? sourceFingerprint() : null;
  }

  function sourceIsCurrent() {
    return displayedSourceFingerprint !== null
      && displayedSourceFingerprint === sourceFingerprint();
  }

  function clearVisibleFlow(detail) {
    if (hashBox) {
      hashBox.textContent = '-';
      hashBox.title = '';
    }
    if (candidateSelect) {
      candidateSelect.hidden = true;
      candidateSelect.value = '';
    }
    if (targetMeta) {
      targetMeta.hidden = true;
      targetMeta.textContent = '';
    }
    if (framesRoot) {
      while (framesRoot.firstChild) framesRoot.removeChild(framesRoot.firstChild);
    }
    if (lineageRoot) {
      lineageRoot.hidden = true;
      lineageRoot.textContent = '';
    }
    status.textContent = detail;
  }

  const sourceObserver = new MutationObserver(() => {
    captureDisplayedSource();
  });
  sourceObserver.observe(baziRoot, {childList: true, subtree: true});
  captureDisplayedSource();

  document.addEventListener('click', (event) => {
    if (event.target !== button) return;
    if (sourceIsCurrent()) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    clearVisibleFlow('当前表单与屏幕上的八字基盘不一致。请先点击“联合排盘”，再解析目标时点。');
  }, true);

  setInterval(() => {
    const flowVisible = Boolean(
      (hashBox && hashBox.textContent !== '-')
      || (targetMeta && !targetMeta.hidden)
      || (framesRoot && framesRoot.childElementCount > 0)
      || (candidateSelect && !candidateSelect.hidden)
    );
    if (flowVisible && !sourceIsCurrent()) {
      clearVisibleFlow('基盘输入已改变；已清除旧目标 flow。请先重新“联合排盘”，再显式解析目标时点。');
    }
  }, 250);
})();
"""
