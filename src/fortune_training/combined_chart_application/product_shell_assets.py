from __future__ import annotations


DESKTOP_PRODUCT_SHELL_SCHEMA = "FUSION-CHART-DESKTOP-PRODUCT-SHELL-R1"


def product_shell_index_html(base_html: str) -> str:
    """Inject the presentation-only desktop product shell over released Workbench surfaces."""

    if "/product-shell.css" in base_html or "/product-shell.js" in base_html:
        raise ValueError("product shell assets already injected")
    return base_html.replace(
        "</head>",
        (
            f'  <meta name="fortune-chart-product-shell" content="{DESKTOP_PRODUCT_SHELL_SCHEMA}">\n'
            '  <link rel="stylesheet" href="/product-shell.css">\n</head>'
        ),
    ).replace(
        "</body>",
        '<script src="/product-shell.js" defer></script>\n</body>',
    )


PRODUCT_SHELL_CSS = """
:root {
  --fc-ink:#17212b;
  --fc-muted:#697582;
  --fc-line:#dfe4e8;
  --fc-soft:#f5f7f8;
  --fc-paper:#ffffff;
  --fc-warm:#f6f1e8;
  --fc-accent:#8b5e2b;
  --fc-accent-soft:#f4eadc;
  --fc-shadow:0 12px 32px rgba(23,33,43,.07);
}
body.fortune-chart-product-shell { background:#f2f3f4; color:var(--fc-ink); }
body.fortune-chart-product-shell .shell { width:min(1840px,calc(100% - 34px)); margin:16px auto 42px; }
body.fortune-chart-product-shell header {
  padding:18px 20px; margin:0 0 12px; border:1px solid var(--fc-line); border-radius:14px;
  background:linear-gradient(120deg,#fff 0%,#fff 58%,var(--fc-warm) 100%); box-shadow:var(--fc-shadow);
}
body.fortune-chart-product-shell header h1 { font-size:27px; letter-spacing:.02em; }
body.fortune-chart-product-shell header p { color:var(--fc-muted); font-size:13px; }
body.fortune-chart-product-shell .badge { border-color:#d7c7b4; background:#fffaf4; color:#69451f; font-weight:600; }

.product-identity { display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin-top:9px; }
.product-chip { padding:4px 8px; border-radius:999px; background:#f7f8f9; border:1px solid var(--fc-line); color:#5e6872; font-size:10px; }
.product-chip.emphasis { background:var(--fc-accent-soft); border-color:#dfc7aa; color:#6f451d; }

body.fortune-chart-product-shell .form-panel { padding:14px 16px; box-shadow:var(--fc-shadow); }
.product-form-heading { display:flex; align-items:flex-start; justify-content:space-between; gap:18px; margin-bottom:12px; }
.product-form-heading strong { display:block; font-size:16px; }
.product-form-heading span { display:block; margin-top:3px; color:var(--fc-muted); font-size:11px; line-height:1.5; }
.product-primary-grid { display:grid; grid-template-columns:1.1fr 1.45fr .8fr; gap:10px; }
.product-option-details { margin-top:10px; border:1px solid var(--fc-line); border-radius:9px; background:#fafbfb; }
.product-option-details > summary { padding:9px 11px; cursor:pointer; color:#4f5963; font-size:11px; font-weight:600; }
.product-option-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:9px; padding:0 11px 11px; }
.product-option-grid .manual-location-toggle { justify-content:end; }
body.fortune-chart-product-shell .location-note { display:none; }
body.fortune-chart-product-shell .profiles { margin:9px 0 0; padding:7px 9px; border-radius:8px; background:#f7f8f9; }
body.fortune-chart-product-shell .actions { align-items:center; border-top:1px solid #eceff1; padding-top:11px; }
body.fortune-chart-product-shell #submit { min-width:128px; background:#1c2731; border-color:#1c2731; font-weight:700; }
body.fortune-chart-product-shell .actions button[type=button] { padding:8px 10px; font-size:11px; }

.product-resolution-summary {
  display:grid; grid-template-columns:1.2fr 1fr 1fr 1fr; gap:8px; margin:11px 0;
}
.product-resolution-card {
  min-width:0; padding:10px 12px; border:1px solid var(--fc-line); border-radius:10px; background:var(--fc-paper);
}
.product-resolution-card span { display:block; color:var(--fc-muted); font-size:10px; margin-bottom:3px; }
.product-resolution-card strong { display:block; overflow:hidden; white-space:nowrap; text-overflow:ellipsis; font-size:12px; }
.product-resolution-card.primary { background:#1d2832; border-color:#1d2832; color:#fff; }
.product-resolution-card.primary span { color:#cbd3da; }

.product-workspace { margin-top:12px; }
.product-nav {
  position:sticky; top:8px; z-index:30; display:flex; gap:5px; padding:5px;
  border:1px solid var(--fc-line); border-radius:11px; background:rgba(255,255,255,.94);
  box-shadow:0 8px 24px rgba(23,33,43,.06); backdrop-filter:blur(8px);
}
.product-nav button {
  flex:0 0 auto; padding:8px 13px; border:0; border-radius:8px; background:transparent; color:#4b5660; font-size:12px; font-weight:600;
}
.product-nav button[aria-selected=true] { background:#1d2832; color:#fff; }
.product-nav .product-nav-spacer { flex:1; }
.product-nav .product-nav-note { align-self:center; padding:0 7px; color:#7a838b; font-size:10px; }

.product-view { margin-top:10px; }
.product-view[hidden] { display:none !important; }
.product-view-heading {
  display:flex; justify-content:space-between; align-items:flex-end; gap:12px; margin:5px 2px 10px;
}
.product-view-heading h2 { font-size:17px; }
.product-view-heading p { margin:2px 0 0; color:var(--fc-muted); font-size:11px; line-height:1.45; }
.product-view-heading code { color:#7d674e; font-size:10px; }
.product-view-hint { margin:0 0 10px; padding:9px 11px; border:1px dashed #d9dee2; border-radius:9px; background:#fafbfb; color:#6c757e; font-size:11px; }

body.fortune-chart-product-shell .charts { grid-template-columns:minmax(0,1.16fr) minmax(420px,.84fr); gap:10px; }
body.fortune-chart-product-shell .chart-card { padding:12px; box-shadow:var(--fc-shadow); }
body.fortune-chart-product-shell .card-head h2 { font-size:17px; }
body.fortune-chart-product-shell .card-head span { color:#8a6b49; font-weight:600; }
body.fortune-chart-product-shell #ziwei-chart svg { min-width:700px; }
body.fortune-chart-product-shell .shared-time-panel { box-shadow:none; }
body.fortune-chart-product-shell .shared-time-facts { grid-template-columns:repeat(4,minmax(0,1fr)); }

.product-flow-stack,.product-fusion-stack,.product-audit-stack { display:grid; gap:10px; }
.product-flow-stack > section,.product-fusion-stack > section,.product-audit-stack > section,
.product-audit-stack > .status-grid { margin:0 !important; box-shadow:var(--fc-shadow); }
.product-fusion-intro {
  padding:14px 16px; border:1px solid #dfd2c2; border-radius:11px; background:linear-gradient(110deg,#fff,#fbf5ec);
}
.product-fusion-intro strong { display:block; margin-bottom:4px; font-size:14px; }
.product-fusion-intro span { color:#6d7278; font-size:11px; line-height:1.55; }
body.fortune-chart-product-shell .status-grid { grid-template-columns:repeat(5,minmax(0,1fr)); }
body.fortune-chart-product-shell .status-grid > div { box-shadow:none; }
.product-audit-stack .resolved-profile-lineage-panel { order:-2; }
.product-audit-stack .status-grid { order:-1; }

.product-source-caption { margin:8px 2px 0; color:#7c858e; font-size:10px; line-height:1.45; }
.product-hidden-by-shell { display:none !important; }

@media (max-width:1180px) {
  .product-primary-grid { grid-template-columns:1fr 1fr; }
  .product-option-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }
  .product-resolution-summary { grid-template-columns:1fr 1fr; }
  body.fortune-chart-product-shell .charts { grid-template-columns:1fr; }
}
@media (max-width:720px) {
  body.fortune-chart-product-shell .shell { width:min(100% - 18px,1840px); }
  body.fortune-chart-product-shell header { padding:14px; }
  .product-primary-grid,.product-option-grid,.product-resolution-summary { grid-template-columns:1fr; }
  .product-nav { overflow-x:auto; }
  .product-nav .product-nav-spacer,.product-nav .product-nav-note { display:none; }
  body.fortune-chart-product-shell .status-grid,body.fortune-chart-product-shell .shared-time-facts { grid-template-columns:1fr; }
}
"""


PRODUCT_SHELL_JS = r"""
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const shell = document.querySelector('.shell');
  const formPanel = document.querySelector('.form-panel');
  const form = $('chart-form');
  const charts = document.querySelector('.charts');
  if (!shell || !formPanel || !form || !charts) return;

  document.body.classList.add('fortune-chart-product-shell');

  const header = shell.querySelector('header');
  const headerCopy = header?.querySelector('div');
  const headerTitle = header?.querySelector('h1');
  const headerSubtitle = header?.querySelector('p');
  if (headerTitle) headerTitle.textContent = '紫微 · 八字融合排盘';
  if (headerSubtitle) headerSubtitle.textContent = '本命、运限、目标时点与跨系统融合 · 确定性计算 · 本地运行';
  if (headerCopy && !headerCopy.querySelector('.product-identity')) {
    const chips = document.createElement('div');
    chips.className = 'product-identity';
    [
      ['确定性 R1', 'product-chip emphasis'],
      ['候选规则保留', 'product-chip'],
      ['紫微 / 八字独立换日', 'product-chip'],
      ['LOCAL ONLY', 'product-chip'],
    ].forEach(([label, cls]) => {
      const chip = document.createElement('span');
      chip.className = cls;
      chip.textContent = label;
      chips.append(chip);
    });
    headerCopy.append(chips);
  }
  const legacyBadge = header?.querySelector('.badge');
  if (legacyBadge) legacyBadge.textContent = '专业排盘工作台';

  function moveLabel(id, target) {
    const element = $(id);
    const label = element?.closest('label');
    if (label) target.append(label);
  }

  const oldGrid = form.querySelector('.grid');
  if (oldGrid && !form.querySelector('.product-primary-grid')) {
    const heading = document.createElement('div');
    heading.className = 'product-form-heading';
    const copy = document.createElement('div');
    const title = document.createElement('strong');
    title.textContent = '出生资料';
    const note = document.createElement('span');
    note.textContent = '先完成基础资料即可排盘；坐标、时间精度与规则 Profile 收入高级设置。';
    copy.append(title, note);
    heading.append(copy);
    form.insertBefore(heading, oldGrid);

    const primary = document.createElement('div');
    primary.className = 'product-primary-grid';
    const locationDetails = document.createElement('details');
    locationDetails.className = 'product-option-details';
    const locationSummary = document.createElement('summary');
    locationSummary.textContent = '地点 / 时区 / 真太阳时参数';
    const locationGrid = document.createElement('div');
    locationGrid.className = 'product-option-grid';
    locationDetails.append(locationSummary, locationGrid);

    const ruleDetails = document.createElement('details');
    ruleDetails.className = 'product-option-details';
    const ruleSummary = document.createElement('summary');
    ruleSummary.textContent = '排盘口径与高级 Profile';
    const ruleGrid = document.createElement('div');
    ruleGrid.className = 'product-option-grid';
    ruleDetails.append(ruleSummary, ruleGrid);

    moveLabel('birth-datetime', primary);
    moveLabel('birth-place', primary);
    moveLabel('sex', primary);

    ['latitude','longitude','timezone-id','location-manual'].forEach((id) => moveLabel(id, locationGrid));
    [
      'precision','uncertainty-seconds','ziwei-daxian-count','ziwei-daxian-frame-id',
      'ziwei-annual-year','ziwei-lunar-month','ziwei-minor-limit-age',
      'bazi-natal-profile','bazi-temporal-profile','bazi-dayun-count'
    ].forEach((id) => moveLabel(id, ruleGrid));

    oldGrid.replaceWith(primary);
    primary.insertAdjacentElement('afterend', locationDetails);
    locationDetails.insertAdjacentElement('afterend', ruleDetails);
    const profileDetails = form.querySelector('.profiles');
    if (profileDetails) ruleDetails.append(profileDetails);
  }

  const chartCards = charts.querySelectorAll('.chart-card');
  const ziweiCardMeta = chartCards[0]?.querySelector('.card-head span');
  const baziCardMeta = chartCards[1]?.querySelector('.card-head span');
  if (ziweiCardMeta) ziweiCardMeta.textContent = '共享出生事实 · 紫微独立规则';
  if (baziCardMeta) baziCardMeta.textContent = '共享出生事实 · 八字独立规则';

  const statusGrid = document.querySelector('.status-grid');
  const sharedTime = $('shared-time-panel');
  const resolvedLineage = $('resolved-profile-lineage-panel');
  const globalError = $('global-error');

  const summary = document.createElement('section');
  summary.className = 'product-resolution-summary';
  const summarySpecs = [
    ['联合状态','product-summary-combined','未运行','primary'],
    ['紫微','product-summary-ziwei','-',''],
    ['八字','product-summary-bazi','-',''],
    ['共享时间','product-summary-time','-',''],
  ];
  summarySpecs.forEach(([label, id, value, extra]) => {
    const card = document.createElement('div');
    card.className = 'product-resolution-card' + (extra ? ' ' + extra : '');
    const key = document.createElement('span');
    key.textContent = label;
    const val = document.createElement('strong');
    val.id = id;
    val.textContent = value;
    card.append(key, val);
    summary.append(card);
  });
  formPanel.insertAdjacentElement('afterend', summary);

  const workspace = document.createElement('section');
  workspace.className = 'product-workspace';
  workspace.id = 'product-workspace';

  const nav = document.createElement('nav');
  nav.className = 'product-nav';
  nav.setAttribute('aria-label', '排盘工作区');
  const tabs = [
    ['natal','本命总览'],
    ['flow','时运联动'],
    ['fusion','融合视图'],
    ['audit','专业审计'],
  ];
  tabs.forEach(([id, label], index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.dataset.productView = id;
    button.textContent = label;
    button.setAttribute('aria-selected', index === 0 ? 'true' : 'false');
    nav.append(button);
  });
  const spacer = document.createElement('span');
  spacer.className = 'product-nav-spacer';
  const navNote = document.createElement('span');
  navNote.className = 'product-nav-note';
  navNote.textContent = '算法事实不在浏览器重算';
  nav.append(spacer, navNote);
  workspace.append(nav);

  function makeView(id, titleText, noteText, codeText) {
    const view = document.createElement('section');
    view.className = 'product-view';
    view.id = 'product-view-' + id;
    view.dataset.view = id;
    view.hidden = id !== 'natal';
    const heading = document.createElement('div');
    heading.className = 'product-view-heading';
    const copy = document.createElement('div');
    const title = document.createElement('h2');
    title.textContent = titleText;
    const note = document.createElement('p');
    note.textContent = noteText;
    copy.append(title, note);
    const code = document.createElement('code');
    code.textContent = codeText;
    heading.append(copy, code);
    view.append(heading);
    workspace.append(view);
    return view;
  }

  const natalView = makeView('natal','联合本命盘','紫微十二宫与八字四柱在同一出生事实下并列，保留各自历法与换日规则。','NATAL');
  const flowView = makeView('flow','时运与目标时点','以显式目标时间驱动八字 flow、紫微运限导航及共享目标 Projection。','TARGET TIME');
  const fusionView = makeView('fusion','跨系统融合','只组合已经发布并通过完整性验证的紫微与八字事实，不执行预测判断。','FUSION R2');
  const auditView = makeView('audit','规则、谱系与完整性','Profile、RuleSet、Algorithm、Hash 与 provenance 集中到专业审计区。','AUDIT');

  const flowStack = document.createElement('div');
  flowStack.className = 'product-flow-stack';
  flowView.append(flowStack);
  const fusionStack = document.createElement('div');
  fusionStack.className = 'product-fusion-stack';
  const fusionIntro = document.createElement('div');
  fusionIntro.className = 'product-fusion-intro';
  const fusionTitle = document.createElement('strong');
  fusionTitle.textContent = '同一目标时间，两套规则独立计算，再进行只读组合';
  const fusionNote = document.createElement('span');
  fusionNote.textContent = '融合层绑定目标时间凭证与两侧 bundle lineage；不会把紫微换日规则强加给八字，也不会把八字候选静默裁决为唯一答案。';
  fusionIntro.append(fusionTitle, fusionNote);
  fusionStack.append(fusionIntro);
  fusionView.append(fusionStack);
  const auditStack = document.createElement('div');
  auditStack.className = 'product-audit-stack';
  auditView.append(auditStack);

  summary.insertAdjacentElement('afterend', workspace);
  if (globalError) workspace.insertAdjacentElement('afterend', globalError);

  if (sharedTime) natalView.append(sharedTime);
  natalView.append(charts);

  [
    'bazi-target-flow-panel',
    'shared-ziwei-apply-panel',
    'ziwei-interaction-panel',
  ].forEach((id) => {
    const panel = $(id);
    if (panel) flowStack.append(panel);
  });

  const fusionPanel = $('fusion-r2-panel');
  if (fusionPanel) fusionStack.append(fusionPanel);

  if (resolvedLineage) auditStack.append(resolvedLineage);
  if (statusGrid) auditStack.append(statusGrid);
  [
    'ziwei-structural-relations-panel',
    'ziwei-star-provenance-panel',
    'ziwei-palace-stem-topology-panel',
    'ziwei-dignity-provenance-panel',
    'ziwei-transformation-provenance-panel',
  ].forEach((id) => {
    const panel = $(id);
    if (panel) auditStack.append(panel);
  });

  const sourceCaption = document.createElement('div');
  sourceCaption.className = 'product-source-caption';
  sourceCaption.textContent = '高级审计区只读展示后端已发布事实与计算身份；不在浏览器选择争议规则 winner，不推导吉凶、旺衰或预测结论。';
  auditStack.append(sourceCaption);

  function activateView(id) {
    document.querySelectorAll('.product-view').forEach((view) => {
      view.hidden = view.dataset.view !== id;
    });
    nav.querySelectorAll('button[data-product-view]').forEach((button) => {
      button.setAttribute('aria-selected', button.dataset.productView === id ? 'true' : 'false');
    });
  }
  nav.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-product-view]');
    if (button) activateView(button.dataset.productView);
  });

  const bindings = [
    ['combined-status','product-summary-combined'],
    ['ziwei-status','product-summary-ziwei'],
    ['bazi-status','product-summary-bazi'],
    ['shared-time-status','product-summary-time'],
  ];
  function mirrorStatus() {
    bindings.forEach(([sourceId, targetId]) => {
      const source = $(sourceId);
      const target = $(targetId);
      if (source && target) target.textContent = source.textContent || '-';
    });
  }
  mirrorStatus();
  bindings.forEach(([sourceId]) => {
    const source = $(sourceId);
    if (source) new MutationObserver(mirrorStatus).observe(source, {subtree:true,childList:true,characterData:true});
  });

  const submit = $('submit');
  if (submit) submit.addEventListener('click', () => activateView('natal'));
  const targetButton = $('resolve-target-flow');
  if (targetButton) targetButton.addEventListener('click', () => activateView('flow'));
  const fusionButton = $('resolve-fusion-r2');
  if (fusionButton) fusionButton.addEventListener('click', () => activateView('fusion'));

  const legacyBadgeText = document.querySelector('.badge');
  if (legacyBadgeText) legacyBadgeText.title = '本地 loopback 桌面运行；不向外网发送出生资料';
})();
"""
