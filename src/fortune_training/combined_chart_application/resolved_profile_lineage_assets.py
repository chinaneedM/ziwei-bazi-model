from __future__ import annotations


def resolved_profile_lineage_index_html(base_html: str) -> str:
    """Inject the read-only resolved profile/rule/algorithm lineage surface."""

    if "/resolved-profile-lineage.css" in base_html or "/resolved-profile-lineage.js" in base_html:
        raise ValueError("resolved profile lineage assets already injected")
    return base_html.replace(
        "</head>",
        '  <link rel="stylesheet" href="/resolved-profile-lineage.css">\n</head>',
    ).replace(
        '<section class="charts">',
        '''<section id="resolved-profile-lineage-panel" class="panel resolved-profile-lineage-panel" hidden>
    <div class="card-head"><h2>已解析计算身份 / 规则版本</h2><span id="resolved-profile-lineage-status">等待排盘</span></div>
    <div class="resolved-profile-lineage-note">只读显示本次后端 combined resolution 已验证的 Profile / RuleSet / Algorithm 身份。ManifestHash 绑定组合及六个子系统 Profile 的 id/version；RuleSet / Algorithm 来自同一已验证 resolved profile 快照。浏览器不重算规则、不选择候选 winner，也不把兼容性 Profile 提升为 canonical authority。</div>
    <div id="resolved-profile-lineage-grid" class="resolved-profile-lineage-grid"></div>
    <div id="resolved-profile-lineage-manifest" class="resolved-profile-lineage-manifest"></div>
  </section>
  <section class="charts">''',
    ).replace(
        "</body>",
        '<script src="/resolved-profile-lineage.js" defer></script>\n</body>',
    )


RESOLVED_PROFILE_LINEAGE_CSS = """
.resolved-profile-lineage-panel { margin:0 0 12px; padding:11px; }
.resolved-profile-lineage-note,.resolved-profile-lineage-manifest { color:#68707a; font-size:11px; line-height:1.5; overflow-wrap:anywhere; }
.resolved-profile-lineage-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:8px; margin:9px 0; }
.resolved-profile-lineage-card { min-width:0; padding:8px 9px; border:1px solid #e1e4e7; border-radius:8px; background:#fafbfc; }
.resolved-profile-lineage-card strong { display:block; margin-bottom:4px; font-size:12px; }
.resolved-profile-lineage-card code,.resolved-profile-lineage-row { display:block; font-size:10px; line-height:1.5; overflow-wrap:anywhere; white-space:normal; }
.resolved-profile-lineage-row { color:#59616a; }
@media (max-width:1100px) { .resolved-profile-lineage-grid { grid-template-columns:repeat(2,minmax(0,1fr)); } }
@media (max-width:700px) { .resolved-profile-lineage-grid { grid-template-columns:1fr; } }
"""


RESOLVED_PROFILE_LINEAGE_JS = """
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const panel = $('resolved-profile-lineage-panel');
  if (!panel) return;
  const statusNode = $('resolved-profile-lineage-status');
  const grid = $('resolved-profile-lineage-grid');
  const manifestNode = $('resolved-profile-lineage-manifest');
  let serial = 0;

  const clear = (node) => { while (node.firstChild) node.removeChild(node.firstChild); };
  const text = (value) => value === null || value === undefined || value === '' ? '-' : String(value);
  const pair = (id, version) => `${text(id)}@${text(version)}`;

  function addCard(label, profile, rows = []) {
    if (!profile || typeof profile !== 'object') return;
    const card = document.createElement('div');
    card.className = 'resolved-profile-lineage-card';
    const title = document.createElement('strong');
    title.textContent = label;
    const identity = document.createElement('code');
    identity.textContent = pair(profile.profile_id, profile.profile_version);
    card.append(title, identity);
    rows.forEach(([rowLabel, value]) => {
      if (value === undefined || value === null || value === '') return;
      const row = document.createElement('div');
      row.className = 'resolved-profile-lineage-row';
      row.textContent = `${rowLabel}: ${value}`;
      card.append(row);
    });
    grid.append(card);
  }

  function ruleBinding(profile, prefix) {
    const ruleId = profile?.[`${prefix}_rule_set_id`];
    const ruleVersion = profile?.[`${prefix}_rule_set_version`];
    const algorithmId = profile?.[`${prefix}_algorithm_id`];
    const algorithmVersion = profile?.[`${prefix}_algorithm_version`];
    if (!ruleId && !algorithmId) return null;
    return [ruleId ? pair(ruleId, ruleVersion) : null, algorithmId ? pair(algorithmId, algorithmVersion) : null]
      .filter(Boolean).join(' · ');
  }

  function render(payload) {
    const resolution = payload?.combined_resolution;
    if (!resolution || resolution.integrity?.status !== 'PASS' || !resolution.manifest_hash) {
      panel.hidden = false;
      statusNode.textContent = '后端组合完整性未通过；不展示 Profile lineage';
      clear(grid);
      manifestNode.textContent = '';
      return;
    }
    clear(grid);
    const z = resolution.ziwei_calculation_profile;
    const bn = resolution.bazi_natal_profile;
    const bt = resolution.bazi_temporal_profile;
    addCard('联合组合', resolution.combined_profile, [
      ['Algorithm', pair(resolution.combined_profile?.algorithm_id, resolution.combined_profile?.algorithm_version)],
      ['Semantics', resolution.combined_profile?.composition_semantics],
    ]);
    addCard('紫微计算', z, [
      ['Time registry', z?.time_calendar_policy_registry_version],
      ['Day boundary', z?.ziwei_day_boundary_policy],
      ['Natal', pair(z?.natal_structure_algorithm_id, z?.natal_structure_algorithm_version)],
      ['Main stars', pair(z?.main_star_algorithm_id, z?.main_star_algorithm_version)],
      ['Auxiliary', ruleBinding(z, 'auxiliary')],
      ['Minor stars', ruleBinding(z, 'minor')],
      ['Dignity', ruleBinding(z, 'dignity')],
      ['Transformations', ruleBinding(z, 'transformation')],
      ['Temporal', ruleBinding(z, 'temporal')],
      ['Rings', ruleBinding(z, 'ring')],
      ['Roles', ruleBinding(z, 'role')],
    ]);
    addCard('紫微应用', resolution.ziwei_application_profile);
    addCard('紫微呈现', resolution.ziwei_presentation_profile);
    addCard('八字原局', bn, [
      ['Time registry', bn?.time_calendar_policy_registry_version],
      ['Time coordinate', bn?.time_coordinate_policy],
      ['Sexagenary', pair(bn?.sexagenary_registry_id, bn?.sexagenary_registry_version)],
      ['Hidden stems', ruleBinding(bn, 'hidden_stem')],
      ['Ten Gods', ruleBinding(bn, 'ten_god')],
      ['Affinity', ruleBinding(bn, 'affinity')],
      ['Raw relations', ruleBinding(bn, 'raw_relation')],
      ['Natal algorithm', pair(bn?.natal_algorithm_id, bn?.natal_algorithm_version)],
    ]);
    addCard('八字时态', bt, [
      ['Direction', pair(bt?.direction_rule_set_id, bt?.direction_rule_set_version)],
      ['Jie anchor', pair(bt?.anchor_rule_set_id, bt?.anchor_rule_set_version)],
      ['Symbolic age', pair(bt?.symbolic_age_rule_set_id, bt?.symbolic_age_rule_set_version)],
      ['Dayun sequence', pair(bt?.dayun_sequence_rule_set_id, bt?.dayun_sequence_rule_set_version)],
      ['Interval coordinate', bt?.interval_coordinate_policy],
      ['Interval granularity', bt?.interval_granularity_rule_set],
      ['Calendar realization', bt?.calendar_realization_rule_set],
      ['Calendar source class', bt?.calendar_realization_source_class],
      ['Dayun boundary', bt?.dayun_boundary_rule_set],
      ['Algorithm', pair(bt?.algorithm_id, bt?.algorithm_version)],
    ]);
    addCard('八字应用', resolution.bazi_application_profile);
    panel.hidden = false;
    statusNode.textContent = `${resolution.status} · integrity PASS`;
    manifestNode.textContent = `ManifestHash=${resolution.manifest_hash} · ManifestHash 绑定 Profile identity；RuleSet / Algorithm 来自同一已验证后端快照。Profile identity 本身不表示 doctrine winner。`;
  }

  const originalFetch = window.fetch.bind(window);
  window.fetch = async (...args) => {
    const response = await originalFetch(...args);
    const url = typeof args[0] === 'string' ? args[0] : args[0]?.url || '';
    if (response.ok && url.endsWith('/api/resolve')) {
      const ticket = ++serial;
      response.clone().json().then((payload) => {
        if (ticket === serial) render(payload);
      }).catch(() => {});
    }
    return response;
  };
})();
"""
