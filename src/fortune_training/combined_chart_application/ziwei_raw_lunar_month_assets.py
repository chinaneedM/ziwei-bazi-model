from __future__ import annotations


def ziwei_raw_lunar_month_index_html(base_html: str) -> str:
    """Inject the released Ziwei raw-lunar-month copy projection into the Workbench."""

    if "/ziwei-raw-lunar-month.js" in base_html:
        raise ValueError("Ziwei raw lunar month asset already injected")
    return base_html.replace(
        "</body>",
        '<script src="/ziwei-raw-lunar-month.js" defer></script>\n</body>',
    )


ZIWEI_RAW_LUNAR_MONTH_JS = r"""
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const chartRoot = $('ziwei-chart');
  if (!chartRoot || typeof window.fetch !== 'function') return;

  const ITEM_ID = 'ziwei-raw-lunar-month-item';

  function clearItem() {
    const existing = $(ITEM_ID);
    if (existing) existing.remove();
  }

  function renderFromResolvePayload(payload) {
    clearItem();
    const structure = payload?.combined_resolution?.ziwei_bundle?.candidate?.chart?.structure;
    const rawLunarMonth = structure?.raw_lunar_month;
    if (!Number.isInteger(rawLunarMonth) || rawLunarMonth < 1 || rawLunarMonth > 12) return;

    const grid = $('ziwei-basic-info-grid');
    if (!grid) return;

    const box = document.createElement('div');
    box.id = ITEM_ID;
    box.className = 'ziwei-basic-info-item';

    const label = document.createElement('span');
    label.textContent = '原始农历月';

    const content = document.createElement('strong');
    content.textContent = String(rawLunarMonth);
    content.title = content.textContent;

    box.append(label, content);
    grid.append(box);
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
          clearItem();
        }
      }, 0);
    }
    return response;
  };

  const form = $('chart-form');
  if (form) form.addEventListener('submit', clearItem);
})();
"""
