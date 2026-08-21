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
.bazi-nayin-panel { margin: 10px 0; padding: 10px; border: 1px solid #d8dde2; border-radius: 9px; background: #fafbfc; }
.bazi-nayin-row { display: grid; grid-template-columns: repeat(4,minmax(0,1fr)); gap: 8px; }
.bazi-nayin-item { padding: 7px; border: 1px solid #e0e3e6; border-radius: 7px; background: #fff; font-size: 12px; }
@media (max-width:900px) { .bazi-nayin-row { grid-template-columns: 1fr 1fr; } }
"""


NAYIN_JS = """
(() => {
'use strict';
const root = document.querySelector('#bazi-chart') || document.body;
if (!root) return;
const panel = document.createElement('section');
panel.id = 'bazi-nayin-panel';
panel.className = 'bazi-nayin-panel';
panel.hidden = true;
panel.innerHTML = '<strong>四柱纳音</strong><div class="bazi-nayin-row" id="bazi-nayin-row"></div>';
root.parentNode.insertBefore(panel, root);
window.renderBaziNayinPresentation = function(response) {
  const rows = document.querySelector('#bazi-nayin-row');
  if (!rows) return;
  while (rows.firstChild) rows.removeChild(rows.firstChild);
  const candidates = response.candidates || [];
  const selectedIndex = response.selected_candidate_index;
  if (!Number.isInteger(selectedIndex)) return;
  if (selectedIndex < 0 || selectedIndex >= candidates.length) return;
  const selectedCandidate = candidates[selectedIndex];
  if (!selectedCandidate || !selectedCandidate.nayin_resolution) return;
  const annotations = selectedCandidate.nayin_resolution.annotations || [];
  annotations.forEach((item) => {
    const cell = document.createElement('div');
    cell.className = 'bazi-nayin-item';
    cell.textContent = `${item.source_pillar_position}: ${item.nayin_name}`;
    rows.appendChild(cell);
  });
  panel.hidden = false;
};
})();
"""
