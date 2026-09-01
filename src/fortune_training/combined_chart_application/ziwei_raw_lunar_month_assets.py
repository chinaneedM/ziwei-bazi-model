from __future__ import annotations


def ziwei_raw_lunar_month_index_html(base_html: str) -> str:
    """Inject released Ziwei natal-coordinate copy projections into the Workbench."""

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

  const RAW_MONTH_ITEM_ID = 'ziwei-raw-lunar-month-item';
  const MONTH_ANCHOR_ITEM_ID = 'ziwei-month-anchor-item';

  function clearItems() {
    [RAW_MONTH_ITEM_ID, MONTH_ANCHOR_ITEM_ID].forEach((itemId) => {
      const existing = $(itemId);
      if (existing) existing.remove();
    });
  }

  function appendItem(grid, itemId, labelText, valueText) {
    const box = document.createElement('div');
    box.id = itemId;
    box.className = 'ziwei-basic-info-item';

    const label = document.createElement('span');
    label.textContent = labelText;

    const content = document.createElement('strong');
    content.textContent = valueText;
    content.title = content.textContent;

    box.append(label, content);
    grid.append(box);
  }

  function renderFromResolvePayload(payload) {
    clearItems();
    const structure = payload?.combined_resolution?.ziwei_bundle?.candidate?.chart?.structure;
    const grid = $('ziwei-basic-info-grid');
    if (!structure || !grid) return;

    const rawLunarMonth = structure?.raw_lunar_month;
    if (Number.isInteger(rawLunarMonth) && rawLunarMonth >= 1 && rawLunarMonth <= 12) {
      appendItem(grid, RAW_MONTH_ITEM_ID, '原始农历月', String(rawLunarMonth));
    }

    const monthAnchor = structure?.month_anchor;
    if (
      Number.isInteger(monthAnchor?.index) && monthAnchor.index >= 0 && monthAnchor.index < 12 &&
      typeof monthAnchor?.branch === 'string' && monthAnchor.branch
    ) {
      appendItem(grid, MONTH_ANCHOR_ITEM_ID, '命身月锚', monthAnchor.branch);
    }
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
          clearItems();
        }
      }, 0);
    }
    return response;
  };

  const form = $('chart-form');
  if (form) form.addEventListener('submit', clearItems);
})();
"""
