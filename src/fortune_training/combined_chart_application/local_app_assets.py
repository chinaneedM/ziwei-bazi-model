from __future__ import annotations


INDEX_HTML = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>紫微 + 八字联合排盘 · Local</title>
  <link rel="stylesheet" href="/style.css">
</head>
<body>
<main class="shell">
  <header>
    <div><h1>紫微 + 八字联合排盘</h1><p>同一物理时间底座 · 两套古法规则并列 · 不做预测判断</p></div>
    <span class="badge">LOCAL ONLY</span>
  </header>
  <section class="panel form-panel">
    <form id="chart-form">
      <div class="location-note">出生地使用离线地点库联动经纬度与 IANA 时区，不向外网发送地点。城市坐标是默认值；需要更精确坐标或特殊历史时区时可开启“手动调整”。</div>
      <div class="grid">
        <label>出生时间<input id="birth-datetime" type="datetime-local" value="1994-05-17T14:30" required></label>
        <label class="location-picker">出生地
          <input id="birth-place" value="Beijing" autocomplete="off" aria-autocomplete="list" aria-controls="location-results" required>
          <div id="location-results" class="location-results" role="listbox" hidden></div>
          <small id="location-link-status">正在载入离线地点联动…</small>
        </label>
        <label>纬度<input id="latitude" type="number" step="0.000001" min="-90" max="90" value="39.9042" readonly required></label>
        <label>经度<input id="longitude" type="number" step="0.000001" min="-180" max="180" value="116.4074" readonly required></label>
        <label>时区<input id="timezone-id" value="Asia/Shanghai" readonly required></label>
        <label class="manual-location-toggle"><span>地点输入模式</span><span class="checkbox-line"><input id="location-manual" type="checkbox">手动调整经纬度 / 时区</span></label>
        <label>性别<select id="sex"><option value="MALE">男</option><option value="FEMALE">女</option></select></label>
        <label>时间精度<select id="precision"><option value="EXACT_SECOND">精确到秒</option><option value="NEAREST_MINUTE">约到分钟</option><option value="NEAREST_HOUR">约到小时</option><option value="APPROXIMATE">约略时间</option></select></label>
        <label>不确定范围 ±秒<input id="uncertainty-seconds" type="number" min="0" max="86400" value="0"></label>
        <label>紫微大限数量<input id="ziwei-daxian-count" type="number" min="1" max="20" value="12"></label>
        <label>紫微大限 Frame（可选）<input id="ziwei-daxian-frame-id" placeholder="DAXIAN:index=1"></label>
        <label>紫微流年（可选）<input id="ziwei-annual-year" type="number" min="1" max="9999"></label>
        <label>紫微小限岁数（可选）<input id="ziwei-minor-limit-age" type="number" min="1" max="200"></label>
        <label>八字 Natal Profile<select id="bazi-natal-profile"><option value="BAZI-FOUNDATION-V1-R1">MIDNIGHT / CLASSICAL_CONTINUOUS</option><option value="BAZI-FOUNDATION-ZI-START-23-R1">ZI_START_23 / ZI_START_ROLLOVER</option></select></label>
        <label>八字大运 Profile<select id="bazi-temporal-profile"><option value="BAZI-TEMPORAL-V1-CONTINUOUS-R1">CONTINUOUS-R1</option><option value="BAZI-TEMPORAL-WENZHEN-CHINA-COMPATIBILITY-R1">WENZHEN-COMPATIBILITY-R1</option></select></label>
        <label>八字大运数量<input id="bazi-dayun-count" type="number" min="1" max="20" value="12"></label>
      </div>
      <details class="profiles"><summary>当前显式 Profile</summary><div id="profile-list"></div></details>
      <div class="actions">
        <button id="submit" type="submit">联合排盘</button>
        <button id="download-manifest" type="button" disabled>保存组合清单</button>
        <button id="download-combined" type="button" disabled>保存完整联合盘</button>
        <button id="download-ziwei" type="button" disabled>保存紫微 JSON</button>
        <button id="download-bazi" type="button" disabled>保存八字 JSON</button>
      </div>
    </form>
  </section>
  <section class="status-grid">
    <div><span>组合状态</span><strong id="combined-status">未运行</strong></div>
    <div><span>ManifestHash</span><code id="manifest-hash">-</code></div>
    <div><span>紫微</span><strong id="ziwei-status">-</strong><code id="ziwei-hash">-</code></div>
    <div><span>八字</span><strong id="bazi-status">-</strong><code id="bazi-hash">-</code></div>
    <div><span>共享时间凭证</span><strong id="shared-time-status">-</strong><code id="shared-time-hash">-</code></div>
  </section>
  <section id="shared-time-panel" class="panel shared-time-panel" hidden>
    <div class="card-head"><h2>统一时间轴与规则凭证</h2><span id="candidate-lineage-status">等待排盘</span></div>
    <div id="shared-time-facts" class="shared-time-facts"></div>
  </section>
  <section class="charts">
    <article class="panel chart-card"><div class="card-head"><h2>紫微斗数</h2><span>独立 Bundle</span></div><div id="ziwei-error" class="sub-error" hidden></div><div id="ziwei-chart" class="placeholder">等待排盘</div></article>
    <article class="panel chart-card"><div class="card-head"><h2>八字</h2><span>独立 Bundle</span></div><div id="bazi-error" class="sub-error" hidden></div><div id="bazi-chart" class="placeholder">等待排盘</div></article>
  </section>
  <section id="global-error" class="global-error" hidden></section>
</main>
<script src="/app.js" defer></script>
</body>
</html>
"""


STYLE_CSS = """
:root { font-family: system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; color:#17191c; background:#f4f5f7; }
* { box-sizing:border-box; } body { margin:0; }
.shell { width:min(1700px,calc(100% - 32px)); margin:20px auto 42px; }
header { display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; }
h1,h2 { margin:0; } header p { margin:5px 0 0; color:#68707a; }
.badge { border:1px solid #ccd1d6; border-radius:999px; padding:6px 9px; background:#fff; font-size:12px; }
.panel,.status-grid>div,.global-error { background:#fff; border:1px solid #dde1e5; border-radius:12px; }
.form-panel { padding:15px; } .grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; }
label { display:flex; flex-direction:column; gap:5px; color:#5d6670; font-size:12px; }
input,select { padding:8px 9px; border:1px solid #cbd1d7; border-radius:7px; background:#fff; }
input[readonly] { background:#f5f7f8; color:#42484f; }
.location-note { margin-bottom:10px; padding:8px 10px; border-radius:8px; background:#f6f8fa; color:#59616a; font-size:12px; line-height:1.5; }
.location-picker { position:relative; }
.location-picker small { min-height:16px; color:#68707a; line-height:1.35; }
.location-results { position:absolute; z-index:20; left:0; right:0; top:58px; max-height:310px; overflow:auto; border:1px solid #cbd1d7; border-radius:8px; background:#fff; box-shadow:0 8px 28px rgba(0,0,0,.12); }
.location-option { width:100%; border:0; border-bottom:1px solid #eef0f2; border-radius:0; background:#fff; color:#20252a; text-align:left; padding:9px 10px; }
.location-option:hover,.location-option:focus { background:#f5f7f8; }
.location-option strong,.location-option span { display:block; }
.location-option span { margin-top:2px; color:#737b84; font-size:11px; }
.manual-location-toggle .checkbox-line { display:flex; flex-direction:row; align-items:center; gap:7px; min-height:34px; color:#333; }
.manual-location-toggle input { width:auto; }
.profiles { margin-top:12px; font-size:12px; color:#606872; } #profile-list { margin-top:6px; line-height:1.7; word-break:break-all; }
.actions { display:flex; flex-wrap:wrap; gap:8px; margin-top:13px; }
button { padding:9px 13px; border:1px solid #222; border-radius:7px; background:#222; color:#fff; cursor:pointer; }
button[type=button] { background:#fff; color:#222; border-color:#cbd1d7; } button:disabled { opacity:.45; }
.status-grid { display:grid; grid-template-columns:1fr 1.4fr 1.4fr 1.4fr 1.4fr; gap:9px; margin:12px 0; }
.status-grid>div { min-width:0; padding:9px 11px; } .status-grid span { display:block; color:#777; font-size:11px; margin-bottom:3px; }
.status-grid strong,.status-grid code { display:block; overflow:hidden; white-space:nowrap; text-overflow:ellipsis; font-size:12px; }
.charts { display:grid; grid-template-columns:1fr 1fr; gap:12px; align-items:start; } .chart-card { min-width:0; padding:11px; overflow:auto; }
.shared-time-panel { margin:0 0 12px; padding:11px; }
.shared-time-facts { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:8px; }
.shared-time-fact { min-width:0; padding:8px 9px; border:1px solid #e1e4e7; border-radius:8px; }
.shared-time-fact span { display:block; color:#777; font-size:10px; margin-bottom:3px; }
.shared-time-fact code { display:block; overflow:hidden; text-overflow:ellipsis; font-size:11px; white-space:nowrap; }
.card-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:9px; } .card-head h2 { font-size:18px; } .card-head span { color:#777; font-size:11px; }
#ziwei-chart svg { width:100%; min-width:760px; height:auto; display:block; }
.placeholder { min-height:340px; display:grid; place-items:center; color:#8a9199; }
.sub-error,.global-error { padding:10px 11px; background:#fff5f5; border:1px solid #e1bbbb; border-radius:8px; margin-bottom:9px; font-size:12px; }
.bazi-candidate-bar { display:flex; align-items:center; justify-content:space-between; gap:10px; padding:9px 10px; margin-bottom:10px; border:1px solid #d8c790; border-radius:8px; background:#fffaf0; font-size:12px; }
.bazi-candidate-note { line-height:1.5; }
.bazi-candidate-select { min-width:110px; }
.pillars { display:grid; grid-template-columns:repeat(4,1fr); gap:7px; margin-bottom:10px; } .pillar { border:1px solid #e1e4e7; border-radius:8px; padding:10px 7px; text-align:center; }
.pillar .pos { color:#777; font-size:10px; } .pillar .ganzhi { font-size:23px; margin:4px 0; } .pillar .ten,.pillar .hidden,.pillar .classical-annotations { font-size:11px; line-height:1.6; }
.pillar .classical-annotations { color:#795548; margin-top:4px; }
.bazi-derived { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:7px; margin:8px 0; }
.bazi-derived-card { border:1px solid #ddd7cc; border-radius:8px; padding:8px; background:#fffdf8; }
.bazi-derived-card span { display:block; color:#777; font-size:10px; }
.bazi-derived-card strong { display:block; margin:3px 0; font-size:18px; }
.bazi-derived-card small { color:#795548; font-size:9px; word-break:break-all; }
.xiaoyun-candidates { display:grid; gap:6px; margin:8px 0; }
.xiaoyun-candidate { border:1px solid #e1e4e7; border-radius:8px; padding:7px 9px; background:#fafbfc; }
.xiaoyun-candidate strong { display:block; font-size:11px; margin-bottom:4px; }
.xiaoyun-frames { display:flex; gap:6px; overflow:auto; font-size:10px; }
.xiaoyun-frame { min-width:48px; text-align:center; padding:4px; border-radius:5px; background:#fff; }
.bazi-meta { font-size:12px; line-height:1.7; color:#555; margin:8px 0; } .dayun { overflow:auto; } table { width:100%; border-collapse:collapse; font-size:11px; } th,td { padding:6px 7px; text-align:left; border-bottom:1px solid #e5e7ea; white-space:nowrap; }
.global-error { margin-top:12px; }
@media (max-width:1100px) { .grid { grid-template-columns:repeat(2,1fr); } .charts { grid-template-columns:1fr; } .status-grid,.shared-time-facts { grid-template-columns:1fr 1fr; } }
@media (max-width:620px) { .grid,.status-grid,.pillars { grid-template-columns:1fr; } .bazi-candidate-bar { align-items:stretch; flex-direction:column; } }
"""


APP_JS = """
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  let last = null;
  let locationSelection = null;
  let locationSearchTimer = null;
  const optionalInt = (id) => { const v=$(id).value.trim(); return v===''?null:Number.parseInt(v,10); };
  const optionalText = (id) => { const v=$(id).value.trim(); return v===''?null:v; };
  const shortHash = (v) => v ? v.slice(0,18) : '-';
  const clear = (n) => { while(n.firstChild) n.removeChild(n.firstChild); };
  const node = (name,text,cls) => { const n=document.createElement(name); if(text!==undefined)n.textContent=text; if(cls)n.className=cls; return n; };
  function download(name,data){ const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json;charset=utf-8'}); const url=URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url; a.download=name; document.body.append(a); a.click(); a.remove(); URL.revokeObjectURL(url); }
  function renderXiaoyun(root,set){ if(!set?.candidates?.length)return; const wrap=node('div',undefined,'xiaoyun-candidates'); set.candidates.forEach((candidate)=>{const box=node('div',undefined,'xiaoyun-candidate'); box.append(node('strong',`小运候选 · ${candidate.profile_id} · ${candidate.direction}`)); const frames=node('div',undefined,'xiaoyun-frames'); candidate.frames.slice(0,12).forEach((frame)=>frames.append(node('span',`${frame.nominal_age}岁 ${frame.ganzhi}`,'xiaoyun-frame'))); box.append(frames); wrap.append(box);}); root.append(wrap); }
  function renderBazi(bundle,index=0){ const root=$('bazi-chart'); clear(root); root.className=''; if(!bundle){root.className='placeholder'; root.textContent='八字未解析'; return;} const count=bundle.candidates.length; if(count===0){root.textContent='无八字候选'; return;} if(!Number.isInteger(index)||index<0||index>=count)index=0; const candidate=bundle.candidates[index]; const view=candidate?.view; if(!view){root.textContent='无八字候选'; return;} if(count>1){const bar=node('div',undefined,'bazi-candidate-bar'); const note=node('div',`时间不确定性：共 ${count} 个八字候选；当前候选 ${index+1}/${count}`,'bazi-candidate-note'); const select=node('select',undefined,'bazi-candidate-select'); select.setAttribute('aria-label','八字候选'); bundle.candidates.forEach((item,candidateIndex)=>{const option=node('option',`候选 ${candidateIndex+1}`); option.value=String(candidateIndex); option.selected=candidateIndex===index; select.append(option);}); select.addEventListener('change',()=>renderBazi(bundle,Number.parseInt(select.value,10))); bar.append(note,select); root.append(bar);} const derived=view.derived_coordinates; if(derived){const dwrap=node('div',undefined,'bazi-derived'); [['胎元',derived.taiyuan],['命宫',derived.minggong],['身宫',derived.shengong]].forEach(([label,row])=>{const card=node('div',undefined,'bazi-derived-card'); card.append(node('span',label),node('strong',row?.ganzhi||'-'),node('small',row?.rule_id||'-')); dwrap.append(card);}); root.append(dwrap);} renderXiaoyun(root,view.xiaoyun); const pwrap=node('div',undefined,'pillars'); view.pillars.forEach((p)=>{const box=node('div',undefined,'pillar'); box.append(node('div',p.position,'pos'),node('div',p.ganzhi,'ganzhi'),node('div',p.visible_ten_god,'ten')); box.append(node('div',p.hidden_stems.map((h)=>`${h.stem}·${h.ten_god}`).join(' / '),'hidden')); box.append(node('div',`旬空：${p.xunkong?.display_name||'-'} · 星运：${p.day_master_twelve_growth?.phase||'-'} · 自坐：${p.self_twelve_growth?.phase||'-'}`,'classical-annotations')); pwrap.append(box);}); root.append(pwrap); const t=view.time_provenance[0]; root.append(node('div',`日主：${view.day_master_stem}　真太阳时：${t?.local_apparent_solar_datetime||'-'}　大运：${view.dayun.direction}`,'bazi-meta')); const j=view.dayun.jiaoyun; root.append(node('div',`交运：${j.first_transition_utc}　锚点：${j.anchor_jie_name}`,'bazi-meta')); const wrap=node('div',undefined,'dayun'); const table=node('table'); const h=node('tr'); ['序','大运','开始 UTC','结束 UTC'].forEach((x)=>h.append(node('th',x))); const th=node('thead'); th.append(h); table.append(th); const body=node('tbody'); view.dayun.frames.forEach((f)=>{const tr=node('tr'); [f.index,f.ganzhi,f.start_utc,f.end_utc].forEach((x)=>tr.append(node('td',String(x)))); body.append(tr);}); table.append(body); wrap.append(table); root.append(wrap); }
  function renderSharedTime(credential,lineage){ const panel=$('shared-time-panel'); const root=$('shared-time-facts'); clear(root); if(!credential){panel.hidden=true; return;} panel.hidden=false; const branches=credential.realizations||[]; const first=branches[0]||{}; const policies=credential.selected_policies||{}; const items=[['合法时间分支',String(branches.length)],['出生 UTC',first.birth_utc||'-'],['地方真太阳时',first.local_apparent_solar_datetime||'-'],['IANA 时区 / tzdb',`${first.timezone_id||'-'} / ${first.tzdb_version||'-'}`],['紫微换日',policies.ziwei?.day_boundary_policy||'-'],['紫微历法日期',policies.ziwei?.calendar_date_policy||'-'],['八字换日',policies.bazi?.bazi_day_boundary_policy||'-'],['八字晚子时',policies.bazi?.bazi_late_zi_hour_stem_policy||'-']]; items.forEach(([label,value])=>{const box=node('div',undefined,'shared-time-fact'); box.append(node('span',label),node('code',value)); box.title=value; root.append(box);}); const statuses=(lineage?.branches||[]).map((row)=>row.status); $('candidate-lineage-status').textContent=statuses.length?`候选联动：${statuses.join(' / ')}`:'候选联动：无合法分支'; }
  function showSubError(id,error){ const box=$(id); if(!error){box.hidden=true; box.textContent=''; return;} box.hidden=false; box.textContent=`${error.code}: ${error.detail}`; }
  function resetRenderedResolution(){ last=null; $('manifest-hash').textContent='-'; $('manifest-hash').removeAttribute('title'); $('ziwei-status').textContent='-'; $('ziwei-hash').textContent='-'; $('bazi-status').textContent='-'; $('bazi-hash').textContent='-'; $('shared-time-status').textContent='-'; $('shared-time-hash').textContent='-'; renderSharedTime(null,null); showSubError('ziwei-error',null); showSubError('bazi-error',null); const zroot=$('ziwei-chart'); clear(zroot); zroot.className='placeholder'; zroot.textContent='当前请求未产生紫微结果'; const broot=$('bazi-chart'); clear(broot); broot.className='placeholder'; broot.textContent='当前请求未产生八字结果'; ['download-manifest','download-combined','download-ziwei','download-bazi'].forEach((id)=>$(id).disabled=true); }
  function setLocationFieldsReadonly(readonly){ ['latitude','longitude','timezone-id'].forEach((id)=>$(id).readOnly=readonly); }
  function hideLocationResults(){ const root=$('location-results'); root.hidden=true; clear(root); }
  function locationDetail(row){ return `${row.latitude}, ${row.longitude} · ${row.timezone_id} · ${row.source_kind}`; }
  function applyLocation(row){ locationSelection=row; $('birth-place').value=row.birth_place; $('latitude').value=String(row.latitude); $('longitude').value=String(row.longitude); $('timezone-id').value=row.timezone_id; if(!$('location-manual').checked)setLocationFieldsReadonly(true); $('location-link-status').textContent=`已联动：${row.display_name}`; hideLocationResults(); }
  function renderLocationResults(rows){ const root=$('location-results'); clear(root); if(!rows.length){root.append(node('div','未找到地点；可换关键词，或开启手动调整。','location-empty')); root.hidden=false; return;} rows.forEach((row)=>{const button=node('button',undefined,'location-option'); button.type='button'; button.setAttribute('role','option'); button.append(node('strong',row.display_name),node('span',locationDetail(row))); button.addEventListener('click',()=>applyLocation(row)); root.append(button);}); root.hidden=false; }
  async function searchLocations(query,limit=12){ try{ const r=await fetch(`/api/locations?q=${encodeURIComponent(query)}&limit=${limit}`); const d=await r.json(); if(!r.ok)throw d.error||{detail:'地点查询失败'}; renderLocationResults(d.results||[]); return d.results||[]; }catch(error){ hideLocationResults(); $('location-link-status').textContent=`地点库不可用：${error.detail||String(error)}`; return []; } }
  async function loadDefaultLocation(){ const rows=await searchLocations('Beijing',12); const preferred=rows.find((row)=>row.selection_id==='PRESET:BEIJING')||rows[0]; if(preferred)applyLocation(preferred); else {$('location-manual').checked=true; setLocationFieldsReadonly(false); $('location-link-status').textContent='地点库未返回默认值，已切换手动输入。';} }
  function setManualLocation(enabled){ if(enabled){ locationSelection=null; setLocationFieldsReadonly(false); $('location-link-status').textContent='手动调整模式：出生地、经纬度与时区按当前输入提交。'; }else{ setLocationFieldsReadonly(true); locationSelection=null; $('location-link-status').textContent='联动模式：请从出生地搜索结果中选择一个地点。'; searchLocations($('birth-place').value.trim(),12); } }
  async function loadProfiles(){ try{ const r=await fetch('/api/profiles'); const d=await r.json(); $('profile-list').textContent=Object.entries(d.profiles).map(([k,v])=>`${k}: ${v}`).join('　|　'); }catch(_){ $('profile-list').textContent='Profile metadata unavailable'; } }
  $('birth-place').addEventListener('input',()=>{ const query=$('birth-place').value.trim(); if(!$('location-manual').checked){locationSelection=null; $('location-link-status').textContent='请选择联动搜索结果；经纬度与时区会一起更新。';} if(locationSearchTimer)clearTimeout(locationSearchTimer); locationSearchTimer=setTimeout(()=>searchLocations(query,12),180); });
  $('birth-place').addEventListener('focus',()=>{ if(!$('location-results').childElementCount)searchLocations($('birth-place').value.trim(),12); else $('location-results').hidden=false; });
  document.addEventListener('click',(event)=>{ if(!event.target.closest('.location-picker'))hideLocationResults(); });
  $('location-manual').addEventListener('change',()=>setManualLocation($('location-manual').checked));
  $('chart-form').addEventListener('submit',async(e)=>{ e.preventDefault(); $('global-error').hidden=true; if(!$('location-manual').checked&&!locationSelection){$('global-error').hidden=false; $('global-error').textContent='LOCAL_APP_LOCATION_SELECTION_REQUIRED: 请从出生地联动结果中选择地点，或开启手动调整。'; return;} $('submit').disabled=true; ['download-manifest','download-combined','download-ziwei','download-bazi'].forEach((id)=>$(id).disabled=true); const payload={birth_datetime:$('birth-datetime').value,birth_place:$('birth-place').value.trim(),latitude:Number.parseFloat($('latitude').value),longitude:Number.parseFloat($('longitude').value),timezone_id:$('timezone-id').value.trim(),location_selection_id:$('location-manual').checked?null:locationSelection.selection_id,sex:$('sex').value,precision:$('precision').value,uncertainty_seconds:Number.parseInt($('uncertainty-seconds').value,10),ziwei_daxian_count:Number.parseInt($('ziwei-daxian-count').value,10),ziwei_daxian_frame_id:optionalText('ziwei-daxian-frame-id'),ziwei_annual_year:optionalInt('ziwei-annual-year'),ziwei_minor_limit_age:optionalInt('ziwei-minor-limit-age'),bazi_natal_profile_id:$('bazi-natal-profile').value,bazi_temporal_profile_id:$('bazi-temporal-profile').value,bazi_dayun_count:Number.parseInt($('bazi-dayun-count').value,10),combined_profile_id:'ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1'}; try{ const r=await fetch('/api/resolve',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}); const d=await r.json(); if(!r.ok)throw d.error||{code:`HTTP_${r.status}`,detail:'Request failed'}; last=d; const res=d.combined_resolution; $('combined-status').textContent=res.status; $('manifest-hash').textContent=shortHash(res.manifest_hash); $('manifest-hash').title=res.manifest_hash; const z=res.ziwei_bundle; const b=res.bazi_bundle; const tc=res.shared_time_credential; $('ziwei-status').textContent=z?z.resolution_status:'FAILED'; $('ziwei-hash').textContent=shortHash(z?.bundle_hash); $('bazi-status').textContent=b?b.status:'FAILED'; $('bazi-hash').textContent=shortHash(b?.bundle_hash); $('shared-time-status').textContent=tc?`${tc.realizations.length} 分支`:'FAILED'; $('shared-time-hash').textContent=shortHash(tc?.computation_hash); $('shared-time-hash').title=tc?.computation_hash||''; renderSharedTime(tc,res.candidate_lineage); showSubError('ziwei-error',res.ziwei_error); showSubError('bazi-error',res.bazi_error); const zroot=$('ziwei-chart'); clear(zroot); if(d.ziwei_svg){zroot.className=''; zroot.innerHTML=d.ziwei_svg;}else{zroot.className='placeholder'; zroot.textContent='紫微未解析';} renderBazi(b); $('download-manifest').disabled=false; $('download-combined').disabled=false; $('download-ziwei').disabled=!d.combined_export.ziwei_export; $('download-bazi').disabled=!d.combined_export.bazi_export; }catch(error){resetRenderedResolution(); $('combined-status').textContent='失败'; $('global-error').hidden=false; $('global-error').textContent=`${error.code||'LOCAL_APP_REQUEST_FAILED'}: ${error.detail||String(error)}`;}finally{$('submit').disabled=false;} });
  $('download-manifest').addEventListener('click',()=>{if(last)download('ziwei-bazi-manifest.json',last.combined_export.manifest);});
  $('download-combined').addEventListener('click',()=>{if(last)download('ziwei-bazi-combined-chart.json',last.combined_export);});
  $('download-ziwei').addEventListener('click',()=>{if(last?.combined_export?.ziwei_export)download('ziwei-chart.json',last.combined_export.ziwei_export);});
  $('download-bazi').addEventListener('click',()=>{if(last?.combined_export?.bazi_export)download('bazi-chart.json',last.combined_export.bazi_export);});
  loadProfiles();
  loadDefaultLocation();
})();
"""
