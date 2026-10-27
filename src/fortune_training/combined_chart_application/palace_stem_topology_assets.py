from __future__ import annotations


def palace_stem_topology_index_html(base_html: str) -> str:
    """Inject read-only Ziwei topology/provenance/structural assets into the combined Workbench."""

    if "/ziwei-palace-stem-topology.css" in base_html or "/ziwei-palace-stem-topology.js" in base_html:
        raise ValueError("palace-stem topology assets already injected")
    return base_html.replace(
        "</head>",
        '  <link rel="stylesheet" href="/ziwei-palace-stem-topology.css">\n</head>',
    ).replace(
        "</body>",
        '<script src="/ziwei-palace-stem-topology.js" defer></script>\n</body>',
    )


PALACE_STEM_TOPOLOGY_CSS = """
.ziwei-palace-stem-topology-panel,.ziwei-star-provenance-panel,.ziwei-structural-relations-panel { margin-bottom:10px; padding:10px; border:1px solid #d8dde2; border-radius:9px; background:#fafbfc; }
.ziwei-palace-stem-topology-head,.ziwei-star-provenance-head,.ziwei-structural-relations-head { display:flex; align-items:flex-start; justify-content:space-between; gap:12px; margin-bottom:8px; }
.ziwei-palace-stem-topology-head strong,.ziwei-star-provenance-head strong,.ziwei-structural-relations-head strong { font-size:13px; }
.ziwei-palace-stem-topology-note,.ziwei-palace-stem-topology-status,.ziwei-palace-stem-topology-lineage,.ziwei-star-provenance-note,.ziwei-star-provenance-status,.ziwei-star-provenance-lineage,.ziwei-structural-relations-note,.ziwei-structural-relations-status,.ziwei-structural-relations-lineage { color:#68707a; font-size:11px; line-height:1.45; }
.ziwei-palace-stem-topology-grid,.ziwei-star-provenance-grid,.ziwei-structural-relations-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:7px; margin-top:8px; }
.ziwei-palace-stem-topology-card,.ziwei-star-provenance-card,.ziwei-structural-relations-card { padding:7px; border:1px solid #e0e3e6; border-radius:7px; background:#fff; }
.ziwei-palace-stem-topology-card strong,.ziwei-star-provenance-card strong,.ziwei-structural-relations-card strong { display:block; margin-bottom:4px; font-size:12px; }
.ziwei-palace-stem-topology-row,.ziwei-star-provenance-row,.ziwei-structural-relations-row { font-size:11px; line-height:1.5; white-space:pre-wrap; }
.ziwei-palace-stem-topology-lineage,.ziwei-star-provenance-lineage,.ziwei-structural-relations-lineage { margin-top:8px; overflow-wrap:anywhere; }
.ziwei-star-provenance-system { margin:5px 0 2px; font-size:11px; font-weight:600; }
@media (max-width:900px) { .ziwei-palace-stem-topology-grid,.ziwei-star-provenance-grid,.ziwei-structural-relations-grid { grid-template-columns:1fr; } }
"""


PALACE_STEM_TOPOLOGY_JS = """
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const root = $('ziwei-chart');
  if (!root) return;

  const topologyPanel = document.createElement('section');
  topologyPanel.id = 'ziwei-palace-stem-topology-panel';
  topologyPanel.className = 'ziwei-palace-stem-topology-panel';
  topologyPanel.hidden = true;
  topologyPanel.innerHTML = `
    <div class="ziwei-palace-stem-topology-head">
      <div>
        <strong>宫干四化目标拓扑</strong>
        <div class="ziwei-palace-stem-topology-note">仅显示后端已发布的宫干四化目标拓扑。同宫 / 对宫 / 其他宫不等于离心 / 向心自化；方向未裁决，不作吉凶或事件解释。</div>
      </div>
      <code id="ziwei-palace-stem-topology-hash">-</code>
    </div>
    <div id="ziwei-palace-stem-topology-status" class="ziwei-palace-stem-topology-status">等待紫微盘</div>
    <div id="ziwei-palace-stem-topology-grid" class="ziwei-palace-stem-topology-grid"></div>
    <div id="ziwei-palace-stem-topology-lineage" class="ziwei-palace-stem-topology-lineage"></div>
  `;
  root.parentNode.insertBefore(topologyPanel, root);

  const provenancePanel = document.createElement('section');
  provenancePanel.id = 'ziwei-star-provenance-panel';
  provenancePanel.className = 'ziwei-star-provenance-panel';
  provenancePanel.hidden = true;
  provenancePanel.innerHTML = `
    <div class="ziwei-star-provenance-head">
      <div>
        <strong>星曜生成来源</strong>
        <div class="ziwei-star-provenance-note">仅按后端已发布的生成器来源与主星来源系分组；不把来源分组解释为吉凶、强弱或流派性质分类。</div>
      </div>
      <code id="ziwei-star-provenance-hash">-</code>
    </div>
    <div id="ziwei-star-provenance-status" class="ziwei-star-provenance-status">等待紫微盘</div>
    <div id="ziwei-star-provenance-grid" class="ziwei-star-provenance-grid"></div>
    <div id="ziwei-star-provenance-lineage" class="ziwei-star-provenance-lineage"></div>
  `;
  root.parentNode.insertBefore(provenancePanel, topologyPanel);

  const structuralPanel = document.createElement('section');
  structuralPanel.id = 'ziwei-structural-relations-panel';
  structuralPanel.className = 'ziwei-structural-relations-panel';
  structuralPanel.hidden = true;
  structuralPanel.innerHTML = `
    <div class="ziwei-structural-relations-head">
      <div>
        <strong>结构关系 R6–R8</strong>
        <div class="ziwei-structural-relations-note">只读展示已发布的气数位、一六共宗与邻宫双侧几何。这里不成立夹宫/夹格，不作事件、端点、评分或吉凶判断。</div>
      </div>
      <code id="ziwei-structural-relations-hash">-</code>
    </div>
    <div id="ziwei-structural-relations-status" class="ziwei-structural-relations-status">等待紫微盘</div>
    <div id="ziwei-structural-relations-grid" class="ziwei-structural-relations-grid"></div>
    <div id="ziwei-structural-relations-lineage" class="ziwei-structural-relations-lineage"></div>
  `;
  root.parentNode.insertBefore(structuralPanel, provenancePanel);

  const topologyStatus = $('ziwei-palace-stem-topology-status');
  const topologyGrid = $('ziwei-palace-stem-topology-grid');
  const topologyLineage = $('ziwei-palace-stem-topology-lineage');
  const topologyHash = $('ziwei-palace-stem-topology-hash');
  const provenanceStatus = $('ziwei-star-provenance-status');
  const provenanceGrid = $('ziwei-star-provenance-grid');
  const provenanceLineage = $('ziwei-star-provenance-lineage');
  const provenanceHash = $('ziwei-star-provenance-hash');
  const structuralStatus = $('ziwei-structural-relations-status');
  const structuralGrid = $('ziwei-structural-relations-grid');
  const structuralLineage = $('ziwei-structural-relations-lineage');
  const structuralHash = $('ziwei-structural-relations-hash');
  let serial = 0;

  const optionalInt = (id) => {
    const element = $(id);
    if (!element) return null;
    const value = element.value.trim();
    return value === '' ? null : Number.parseInt(value, 10);
  };
  const optionalText = (id) => {
    const element = $(id);
    if (!element) return null;
    const value = element.value.trim();
    return value === '' ? null : value;
  };
  const clear = (node) => { while (node.firstChild) node.removeChild(node.firstChild); };
  const relationLabel = {
    SAME_PALACE: '同宫',
    OPPOSITE_PALACE: '对宫',
    OTHER_PALACE: '其他宫',
  };

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
    };
  }

  function renderTopology(response) {
    const topology = response.ziwei_palace_stem_transformation_topology;
    topologyPanel.hidden = false;
    topologyHash.textContent = topology.bundle_hash.slice(0, 16);
    topologyHash.title = topology.bundle_hash;
    topologyStatus.textContent = `后端事实：${topology.rows.length} 条 · ${topology.classification_policy}`;

    const bySource = new Map();
    topology.rows.forEach((row) => {
      if (!bySource.has(row.source_address_index)) bySource.set(row.source_address_index, []);
      bySource.get(row.source_address_index).push(row);
    });
    clear(topologyGrid);
    [...bySource.entries()]
      .sort((left, right) => left[0] - right[0])
      .forEach(([, rows]) => {
        const first = rows[0];
        const card = document.createElement('div');
        card.className = 'ziwei-palace-stem-topology-card';
        const title = document.createElement('strong');
        title.textContent = `${first.source_branch}宫 · 宫干 ${first.source_stem}`;
        card.append(title);
        rows.forEach((row) => {
          const line = document.createElement('div');
          line.className = 'ziwei-palace-stem-topology-row';
          line.textContent = `${row.transformation_type} → ${row.target_display_name}（${row.target_branch}） · ${relationLabel[row.topology_relation] || row.topology_relation}`;
          line.title = `${row.assignment_id} · ${row.mechanism_id} · ${row.source_refs.join(',')}`;
          card.append(line);
        });
        topologyGrid.append(card);
      });

    topologyLineage.textContent = [
      `semantic_scope=${topology.semantic_scope}`,
      `selection_semantics=${topology.selection_semantics}`,
      `source_rule_set=${topology.source_transformation_rule_set_id}@${topology.source_transformation_rule_set_version}`,
      `source_application_bundle_hash=${topology.source_application_bundle_hash}`,
      `fact_hash=${topology.fact_hash}`,
      `computation_hash=${topology.computation_hash}`,
      `integrity=${topology.integrity?.status || '-'}`,
    ].join(' · ');
  }

  function renderStarProvenance(response) {
    const provenance = response.ziwei_star_placement_provenance;
    provenancePanel.hidden = false;
    provenanceHash.textContent = provenance.bundle_hash.slice(0, 16);
    provenanceHash.title = provenance.bundle_hash;
    provenanceStatus.textContent = `后端事实：${provenance.rows.length} 星 · ${provenance.classification_policy}`;

    const families = new Map();
    provenance.rows.forEach((row) => {
      if (!families.has(row.generator_family_id)) {
        families.set(row.generator_family_id, {
          label: row.generator_family_label,
          rows: [],
        });
      }
      families.get(row.generator_family_id).rows.push(row);
    });
    clear(provenanceGrid);
    [...families.values()].forEach((family) => {
      const card = document.createElement('div');
      card.className = 'ziwei-star-provenance-card';
      const title = document.createElement('strong');
      title.textContent = `${family.label} · ${family.rows.length}`;
      card.append(title);

      let currentSystem = null;
      family.rows
        .slice()
        .sort((left, right) => (left.main_star_system_id || '').localeCompare(right.main_star_system_id || '') || left.address_index - right.address_index || left.entity_id.localeCompare(right.entity_id))
        .forEach((row) => {
          const systemKey = row.main_star_system_id || '';
          if (systemKey && systemKey !== currentSystem) {
            const system = document.createElement('div');
            system.className = 'ziwei-star-provenance-system';
            system.textContent = row.main_star_system_label;
            card.append(system);
            currentSystem = systemKey;
          }
          const line = document.createElement('div');
          line.className = 'ziwei-star-provenance-row';
          line.textContent = `${row.display_name} · ${row.branch}宫`;
          line.title = `${row.generator_id}@${row.algorithm_version} · ${row.source_refs.join(',')}`;
          card.append(line);
        });
      provenanceGrid.append(card);
    });

    provenanceLineage.textContent = [
      `semantic_scope=${provenance.semantic_scope}`,
      `source_application_bundle_hash=${provenance.source_application_bundle_hash}`,
      `fact_hash=${provenance.fact_hash}`,
      `computation_hash=${provenance.computation_hash}`,
      `integrity=${provenance.integrity?.status || '-'}`,
    ].join(' · ');
  }

  function relationCard(titleText, facts, lineBuilder) {
    const card = document.createElement('div');
    card.className = 'ziwei-structural-relations-card';
    const title = document.createElement('strong');
    title.textContent = `${titleText} · ${facts.length}`;
    card.append(title);
    facts.forEach((fact) => {
      const line = document.createElement('div');
      line.className = 'ziwei-structural-relations-row';
      line.textContent = lineBuilder(fact);
      card.append(line);
    });
    structuralGrid.append(card);
  }

  function renderStructuralRelations(response) {
    const resolution = response.ziwei_structural_relation_projections;
    structuralPanel.hidden = false;
    structuralHash.textContent = resolution.bundle_hash.slice(0, 16);
    structuralHash.title = resolution.bundle_hash;
    structuralStatus.textContent = '后端事实：R6 气数位 · R7 一六共宗 · R8 邻宫双侧';
    clear(structuralGrid);

    relationCard('R6 气数位', resolution.qishu.qishu_facts, (fact) =>
      `${fact.origin_address.branch} → ${fact.target_address.branch} · 第${fact.relative_ordinal}位 · 顺时针偏移${fact.clockwise_offset}`
    );
    relationCard('R7 一六共宗', resolution.one_six.one_six_facts, (fact) =>
      `${fact.origin_address.branch} → ${fact.target_address.branch} · 第${fact.relative_ordinal}位 · 顺时针偏移${fact.clockwise_offset}`
    );
    relationCard('R8 邻宫双侧', resolution.adjacent_palace.adjacent_palace_pairs, (fact) =>
      `${fact.origin_address.branch} · 逆邻${fact.counterclockwise_address.branch} / 顺邻${fact.clockwise_address.branch}`
    );

    structuralLineage.textContent = [
      `semantic_scope=${resolution.semantic_scope}`,
      `source_application_bundle_hash=${resolution.source_application_bundle_hash}`,
      `source_r2_fact_hash=${resolution.source_r2_fact_hash}`,
      `source_r2_computation_hash=${resolution.source_r2_computation_hash}`,
      `r6=${resolution.qishu.hashes.fact_hash}`,
      `r7=${resolution.one_six.hashes.fact_hash}`,
      `r8=${resolution.adjacent_palace.hashes.fact_hash}`,
      `integrity=${resolution.integrity?.status || '-'}`,
    ].join(' · ');
  }

  async function readSidecar(url, ticket, onSuccess, panel, statusNode, errorLabel) {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(requestPayload()),
      });
      const payload = await response.json();
      if (ticket !== serial) return;
      if (!response.ok) {
        panel.hidden = false;
        statusNode.textContent = `${payload.error?.code || errorLabel}: ${payload.error?.detail || response.status}`;
        return;
      }
      onSuccess(payload);
    } catch (error) {
      if (ticket !== serial) return;
      panel.hidden = false;
      statusNode.textContent = `${errorLabel}：${String(error)}`;
    }
  }

  function refresh() {
    const ticket = ++serial;
    topologyStatus.textContent = '读取宫干四化目标拓扑…';
    provenanceStatus.textContent = '读取星曜生成来源…';
    structuralStatus.textContent = '读取结构关系 R6–R8…';
    readSidecar('/api/ziwei-palace-stem-topology', ticket, renderTopology, topologyPanel, topologyStatus, '宫干四化目标拓扑读取失败');
    readSidecar('/api/ziwei-star-provenance', ticket, renderStarProvenance, provenancePanel, provenanceStatus, '星曜生成来源读取失败');
    readSidecar('/api/ziwei-structural-relations', ticket, renderStructuralRelations, structuralPanel, structuralStatus, '结构关系读取失败');
  }

  const originalFetch = window.fetch.bind(window);
  window.fetch = async (...args) => {
    const response = await originalFetch(...args);
    const url = typeof args[0] === 'string' ? args[0] : args[0]?.url || '';
    if (
      response.ok
      && (url.endsWith('/api/resolve') || url.endsWith('/api/ziwei-interaction'))
    ) {
      window.setTimeout(refresh, 0);
    }
    return response;
  };
})();
"""
