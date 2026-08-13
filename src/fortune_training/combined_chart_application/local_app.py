from __future__ import annotations

import argparse
import json
import math
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fortune_training.bazi_application import (
    bazi_local_application_v1_profile,
)
from fortune_training.bazi_chart import bazi_foundation_v1_profile
from fortune_training.bazi_temporal import (
    bazi_temporal_v1_continuous_profile,
    bazi_temporal_wenzhen_china_compatibility_r1_profile,
)
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimePrecision
from fortune_training.calendar_foundation.models import json_value
from fortune_training.ziwei_application import (
    SvgRendererProfile,
    ZiweiTwelvePalaceSvgRenderer,
    ziwei_application_default_presentation_profile,
    ziwei_application_v1_profile,
)
from fortune_training.ziwei_chart import ziwei_chart_engine_v1_profile

from .models import CombinedChartApplicationRequest
from .profile import COMBINED_PROFILE_ID, combined_chart_application_v1_profile
from .service import CombinedApplicationResolutionError, CombinedChartService


LOCAL_APP_ID = "ZIWEI-BAZI-COMBINED-LOCAL-BROWSER-APP-V1"
LOCAL_APP_VERSION = "1.0.0"
LOCAL_APP_HEALTH_SCHEMA = "ZIWEI-BAZI-COMBINED-LOCAL-APP-HEALTH-V1"
LOCAL_APP_RESOLVE_SCHEMA = "ZIWEI-BAZI-COMBINED-LOCAL-APP-RESOLVE-V1"
LOCAL_APP_ERROR_SCHEMA = "ZIWEI-BAZI-COMBINED-LOCAL-APP-ERROR-V1"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8767
MAX_REQUEST_BYTES = 96 * 1024

CSP = (
    "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
    "connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; "
    "form-action 'self'"
)

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
    <div><h1>紫微 + 八字联合排盘</h1><p>同一出生事实 · 两套引擎独立计算 · 不做交叉判断</p></div>
    <span class="badge">LOCAL ONLY</span>
  </header>
  <section class="panel form-panel">
    <form id="chart-form">
      <div class="grid">
        <label>出生时间<input id="birth-datetime" type="datetime-local" value="1994-05-17T14:30" required></label>
        <label>出生地<input id="birth-place" value="Beijing" required></label>
        <label>纬度<input id="latitude" type="number" step="0.000001" min="-90" max="90" value="39.9042" required></label>
        <label>经度<input id="longitude" type="number" step="0.000001" min="-180" max="180" value="116.4074" required></label>
        <label>时区<input id="timezone-id" value="Asia/Shanghai" required></label>
        <label>性别<select id="sex"><option value="MALE">男</option><option value="FEMALE">女</option></select></label>
        <label>时间精度<select id="precision"><option value="EXACT_SECOND">精确到秒</option><option value="NEAREST_MINUTE">约到分钟</option><option value="NEAREST_HOUR">约到小时</option><option value="APPROXIMATE">约略时间</option></select></label>
        <label>不确定范围 ±秒<input id="uncertainty-seconds" type="number" min="0" max="86400" value="0"></label>
        <label>紫微大限数量<input id="ziwei-daxian-count" type="number" min="1" max="20" value="12"></label>
        <label>紫微大限 Frame（可选）<input id="ziwei-daxian-frame-id" placeholder="DAXIAN:index=1"></label>
        <label>紫微流年（可选）<input id="ziwei-annual-year" type="number" min="1" max="9999"></label>
        <label>紫微小限岁数（可选）<input id="ziwei-minor-limit-age" type="number" min="1" max="200"></label>
        <label>八字大运 Profile<select id="bazi-temporal-profile"><option value="BAZI-TEMPORAL-V1-CONTINUOUS-R1">CONTINUOUS-R1</option><option value="BAZI-TEMPORAL-WENZHEN-CHINA-COMPATIBILITY-R1">WENZHEN-COMPATIBILITY-R1</option></select></label>
        <label>八字大运数量<input id="bazi-dayun-count" type="number" min="1" max="20" value="12"></label>
      </div>
      <details class="profiles"><summary>当前显式 Profile</summary><div id="profile-list"></div></details>
      <div class="actions">
        <button id="submit" type="submit">联合排盘</button>
        <button id="download-manifest" type="button" disabled>保存组合清单</button>
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
.profiles { margin-top:12px; font-size:12px; color:#606872; } #profile-list { margin-top:6px; line-height:1.7; word-break:break-all; }
.actions { display:flex; flex-wrap:wrap; gap:8px; margin-top:13px; }
button { padding:9px 13px; border:1px solid #222; border-radius:7px; background:#222; color:#fff; cursor:pointer; }
button[type=button] { background:#fff; color:#222; border-color:#cbd1d7; } button:disabled { opacity:.45; }
.status-grid { display:grid; grid-template-columns:1fr 1.5fr 1.5fr 1.5fr; gap:9px; margin:12px 0; }
.status-grid>div { min-width:0; padding:9px 11px; } .status-grid span { display:block; color:#777; font-size:11px; margin-bottom:3px; }
.status-grid strong,.status-grid code { display:block; overflow:hidden; white-space:nowrap; text-overflow:ellipsis; font-size:12px; }
.charts { display:grid; grid-template-columns:1fr 1fr; gap:12px; align-items:start; } .chart-card { min-width:0; padding:11px; overflow:auto; }
.card-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:9px; } .card-head h2 { font-size:18px; } .card-head span { color:#777; font-size:11px; }
#ziwei-chart svg { width:100%; min-width:760px; height:auto; display:block; }
.placeholder { min-height:340px; display:grid; place-items:center; color:#8a9199; }
.sub-error,.global-error { padding:10px 11px; background:#fff5f5; border:1px solid #e1bbbb; border-radius:8px; margin-bottom:9px; font-size:12px; }
.pillars { display:grid; grid-template-columns:repeat(4,1fr); gap:7px; margin-bottom:10px; } .pillar { border:1px solid #e1e4e7; border-radius:8px; padding:10px 7px; text-align:center; }
.pillar .pos { color:#777; font-size:10px; } .pillar .ganzhi { font-size:23px; margin:4px 0; } .pillar .ten,.pillar .hidden { font-size:11px; line-height:1.6; }
.bazi-meta { font-size:12px; line-height:1.7; color:#555; margin:8px 0; } .dayun { overflow:auto; } table { width:100%; border-collapse:collapse; font-size:11px; } th,td { padding:6px 7px; text-align:left; border-bottom:1px solid #e5e7ea; white-space:nowrap; }
.global-error { margin-top:12px; }
@media (max-width:1100px) { .grid { grid-template-columns:repeat(2,1fr); } .charts { grid-template-columns:1fr; } .status-grid { grid-template-columns:1fr 1fr; } }
@media (max-width:620px) { .grid,.status-grid,.pillars { grid-template-columns:1fr; } }
"""

APP_JS = """
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  let last = null;
  const optionalInt = (id) => { const v=$(id).value.trim(); return v===''?null:Number.parseInt(v,10); };
  const optionalText = (id) => { const v=$(id).value.trim(); return v===''?null:v; };
  const shortHash = (v) => v ? v.slice(0,18) : '-';
  const clear = (n) => { while(n.firstChild) n.removeChild(n.firstChild); };
  const node = (name,text,cls) => { const n=document.createElement(name); if(text!==undefined)n.textContent=text; if(cls)n.className=cls; return n; };
  function download(name,data){ const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json;charset=utf-8'}); const url=URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url; a.download=name; document.body.append(a); a.click(); a.remove(); URL.revokeObjectURL(url); }
  function renderBazi(bundle){ const root=$('bazi-chart'); clear(root); root.className=''; if(!bundle){root.className='placeholder'; root.textContent='八字未解析'; return;} const view=bundle.candidates[0]?.view; if(!view){root.textContent='无八字候选'; return;} const pwrap=node('div',undefined,'pillars'); view.pillars.forEach((p)=>{const box=node('div',undefined,'pillar'); box.append(node('div',p.position,'pos'),node('div',p.ganzhi,'ganzhi'),node('div',p.visible_ten_god,'ten')); box.append(node('div',p.hidden_stems.map((h)=>`${h.stem}·${h.ten_god}`).join(' / '),'hidden')); pwrap.append(box);}); root.append(pwrap); const t=view.time_provenance[0]; root.append(node('div',`日主：${view.day_master_stem}　真太阳时：${t?.local_apparent_solar_datetime||'-'}　大运：${view.dayun.direction}`,'bazi-meta')); const j=view.dayun.jiaoyun; root.append(node('div',`交运：${j.first_transition_utc}　锚点：${j.anchor_jie_name}`,'bazi-meta')); const wrap=node('div',undefined,'dayun'); const table=node('table'); const h=node('tr'); ['序','大运','开始 UTC','结束 UTC'].forEach((x)=>h.append(node('th',x))); const th=node('thead'); th.append(h); table.append(th); const body=node('tbody'); view.dayun.frames.forEach((f)=>{const tr=node('tr'); [f.index,f.ganzhi,f.start_utc,f.end_utc].forEach((x)=>tr.append(node('td',String(x)))); body.append(tr);}); table.append(body); wrap.append(table); root.append(wrap); }
  function showSubError(id,error){ const box=$(id); if(!error){box.hidden=true; box.textContent=''; return;} box.hidden=false; box.textContent=`${error.code}: ${error.detail}`; }
  async function loadProfiles(){ try{ const r=await fetch('/api/profiles'); const d=await r.json(); $('profile-list').textContent=Object.entries(d.profiles).map(([k,v])=>`${k}: ${v}`).join('　|　'); }catch(_){ $('profile-list').textContent='Profile metadata unavailable'; } }
  $('chart-form').addEventListener('submit',async(e)=>{ e.preventDefault(); $('global-error').hidden=true; $('submit').disabled=true; ['download-manifest','download-ziwei','download-bazi'].forEach((id)=>$(id).disabled=true); const payload={birth_datetime:$('birth-datetime').value,birth_place:$('birth-place').value.trim(),latitude:Number.parseFloat($('latitude').value),longitude:Number.parseFloat($('longitude').value),timezone_id:$('timezone-id').value.trim(),sex:$('sex').value,precision:$('precision').value,uncertainty_seconds:Number.parseInt($('uncertainty-seconds').value,10),ziwei_daxian_count:Number.parseInt($('ziwei-daxian-count').value,10),ziwei_daxian_frame_id:optionalText('ziwei-daxian-frame-id'),ziwei_annual_year:optionalInt('ziwei-annual-year'),ziwei_minor_limit_age:optionalInt('ziwei-minor-limit-age'),bazi_temporal_profile_id:$('bazi-temporal-profile').value,bazi_dayun_count:Number.parseInt($('bazi-dayun-count').value,10),combined_profile_id:'ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1'}; try{ const r=await fetch('/api/resolve',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}); const d=await r.json(); if(!r.ok)throw d.error||{code:`HTTP_${r.status}`,detail:'Request failed'}; last=d; const res=d.combined_resolution; $('combined-status').textContent=res.status; $('manifest-hash').textContent=shortHash(res.manifest_hash); $('manifest-hash').title=res.manifest_hash; const z=res.ziwei_bundle; const b=res.bazi_bundle; $('ziwei-status').textContent=z?z.resolution_status:'FAILED'; $('ziwei-hash').textContent=shortHash(z?.bundle_hash); $('bazi-status').textContent=b?b.status:'FAILED'; $('bazi-hash').textContent=shortHash(b?.bundle_hash); showSubError('ziwei-error',res.ziwei_error); showSubError('bazi-error',res.bazi_error); const zroot=$('ziwei-chart'); clear(zroot); if(d.ziwei_svg){zroot.className=''; zroot.innerHTML=d.ziwei_svg;}else{zroot.className='placeholder'; zroot.textContent='紫微未解析';} renderBazi(b); $('download-manifest').disabled=false; $('download-ziwei').disabled=!d.combined_export.ziwei_export; $('download-bazi').disabled=!d.combined_export.bazi_export; }catch(error){last=null; $('combined-status').textContent='失败'; $('global-error').hidden=false; $('global-error').textContent=`${error.code||'LOCAL_APP_REQUEST_FAILED'}: ${error.detail||String(error)}`;}finally{$('submit').disabled=false;} });
  $('download-manifest').addEventListener('click',()=>{if(last)download('ziwei-bazi-manifest.json',last.combined_export.manifest);});
  $('download-ziwei').addEventListener('click',()=>{if(last?.combined_export?.ziwei_export)download('ziwei-chart.json',last.combined_export.ziwei_export);});
  $('download-bazi').addEventListener('click',()=>{if(last?.combined_export?.bazi_export)download('bazi-chart.json',last.combined_export.bazi_export);});
  loadProfiles();
})();
"""


class LocalCombinedAppRequestError(ValueError):
    def __init__(self, code: str, detail: str, *, status: int = 400) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail
        self.status = status


def _required_text(payload: dict[str, Any], key: str, *, max_length: int) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise LocalCombinedAppRequestError("LOCAL_APP_INVALID_INPUT", f"{key} is required")
    value = value.strip()
    if len(value) > max_length:
        raise LocalCombinedAppRequestError("LOCAL_APP_INVALID_INPUT", f"{key} is too long")
    return value


def _finite_float(payload: dict[str, Any], key: str) -> float:
    value = payload.get(key)
    if isinstance(value, bool):
        raise LocalCombinedAppRequestError("LOCAL_APP_INVALID_INPUT", f"{key} must be numeric")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise LocalCombinedAppRequestError("LOCAL_APP_INVALID_INPUT", f"{key} must be numeric") from exc
    if not math.isfinite(result):
        raise LocalCombinedAppRequestError("LOCAL_APP_INVALID_INPUT", f"{key} must be finite")
    return result


def _bounded_int(payload: dict[str, Any], key: str, minimum: int, maximum: int) -> int:
    value = payload.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= maximum:
        raise LocalCombinedAppRequestError("LOCAL_APP_INVALID_INPUT", f"{key} must be an integer in [{minimum}, {maximum}]")
    return value


def _optional_int(payload: dict[str, Any], key: str, minimum: int, maximum: int) -> int | None:
    value = payload.get(key)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= maximum:
        raise LocalCombinedAppRequestError("LOCAL_APP_INVALID_INPUT", f"{key} must be null or an integer in [{minimum}, {maximum}]")
    return value


def _optional_text(payload: dict[str, Any], key: str, max_length: int) -> str | None:
    value = payload.get(key)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip() or len(value.strip()) > max_length:
        raise LocalCombinedAppRequestError("LOCAL_APP_INVALID_INPUT", f"{key} must be null or non-empty text")
    return value.strip()


def _parse_datetime(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise LocalCombinedAppRequestError("LOCAL_APP_INVALID_INPUT", "birth_datetime must be ISO local datetime") from exc
    if parsed.tzinfo is not None:
        raise LocalCombinedAppRequestError("LOCAL_APP_INVALID_INPUT", "birth_datetime must be a naive local wall-clock value")
    return parsed


def _parse_precision(value: str) -> TimePrecision:
    try:
        return TimePrecision(value.strip().upper())
    except ValueError as exc:
        raise LocalCombinedAppRequestError("LOCAL_APP_INVALID_INPUT", "unsupported precision") from exc


class LocalCombinedChartApplication:
    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root.resolve()
        registry_path = self.repository_root / "config" / "time-calendar-policies.json"
        if not registry_path.is_file():
            raise LocalCombinedAppRequestError("LOCAL_APP_REPOSITORY_ROOT_INVALID", f"missing {registry_path}", status=500)
        self.registry = PolicyRegistry.from_file(registry_path)
        self.ziwei_calculation_profile = ziwei_chart_engine_v1_profile(self.registry)
        self.ziwei_application_profile = ziwei_application_v1_profile()
        self.ziwei_presentation_profile = ziwei_application_default_presentation_profile()
        self.bazi_natal_profile = bazi_foundation_v1_profile(self.registry)
        self.bazi_application_profile = bazi_local_application_v1_profile()
        self.combined_profile = combined_chart_application_v1_profile()
        self.service = CombinedChartService.from_repository(self.repository_root)
        self.renderer = ZiweiTwelvePalaceSvgRenderer()
        self.renderer_profile = SvgRendererProfile()

    def profile_metadata(self) -> dict[str, Any]:
        return {
            "schema": "ZIWEI-BAZI-COMBINED-LOCAL-PROFILES-V1",
            "profiles": {
                "combined": self.combined_profile.profile_id,
                "ziwei_calculation": self.ziwei_calculation_profile.profile_id,
                "ziwei_application": self.ziwei_application_profile.profile_id,
                "ziwei_presentation": self.ziwei_presentation_profile.profile_id,
                "bazi_natal": self.bazi_natal_profile.profile_id,
                "bazi_application": self.bazi_application_profile.profile_id,
                "bazi_temporal_options": "BAZI-TEMPORAL-V1-CONTINUOUS-R1 | BAZI-TEMPORAL-WENZHEN-CHINA-COMPATIBILITY-R1",
            },
        }

    def health(self) -> dict[str, Any]:
        return {"schema":LOCAL_APP_HEALTH_SCHEMA,"status":"ok","application_id":LOCAL_APP_ID,"application_version":LOCAL_APP_VERSION,"bind_policy":"LOOPBACK_ONLY"}

    def resolve_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise LocalCombinedAppRequestError("LOCAL_APP_INVALID_JSON", "request body must be a JSON object")
        birth_datetime = _parse_datetime(_required_text(payload,"birth_datetime",max_length=64))
        birth_place = _required_text(payload,"birth_place",max_length=160)
        latitude = _finite_float(payload,"latitude")
        longitude = _finite_float(payload,"longitude")
        timezone_id = _required_text(payload,"timezone_id",max_length=120)
        try: ZoneInfo(timezone_id)
        except ZoneInfoNotFoundError as exc: raise LocalCombinedAppRequestError("LOCAL_APP_INVALID_TIMEZONE",timezone_id) from exc
        sex = _required_text(payload,"sex",max_length=16).upper()
        if sex not in {"MALE","FEMALE","M","F","男","女"}: raise LocalCombinedAppRequestError("LOCAL_APP_INVALID_INPUT","sex must be MALE or FEMALE")
        precision = _parse_precision(_required_text(payload,"precision",max_length=32))
        uncertainty_seconds = _bounded_int(payload,"uncertainty_seconds",0,86400)
        ziwei_daxian_count = _bounded_int(payload,"ziwei_daxian_count",1,20)
        bazi_dayun_count = _bounded_int(payload,"bazi_dayun_count",1,20)
        ziwei_daxian_frame_id = _optional_text(payload,"ziwei_daxian_frame_id",80)
        ziwei_annual_year = _optional_int(payload,"ziwei_annual_year",1,9999)
        ziwei_minor_limit_age = _optional_int(payload,"ziwei_minor_limit_age",1,200)
        combined_profile_id = _required_text(payload,"combined_profile_id",max_length=100)
        if combined_profile_id != COMBINED_PROFILE_ID: raise LocalCombinedAppRequestError("LOCAL_APP_UNSUPPORTED_COMBINED_PROFILE",combined_profile_id)
        temporal_id = _required_text(payload,"bazi_temporal_profile_id",max_length=120)
        temporal_factories = {"BAZI-TEMPORAL-V1-CONTINUOUS-R1":bazi_temporal_v1_continuous_profile,"BAZI-TEMPORAL-WENZHEN-CHINA-COMPATIBILITY-R1":bazi_temporal_wenzhen_china_compatibility_r1_profile}
        factory = temporal_factories.get(temporal_id)
        if factory is None: raise LocalCombinedAppRequestError("LOCAL_APP_UNSUPPORTED_BAZI_TEMPORAL_PROFILE",temporal_id)
        try:
            birth = BirthInput(reported_local_datetime=birth_datetime,birth_place=birth_place,latitude=latitude,longitude=longitude,timezone_id=timezone_id,precision=precision,uncertainty_seconds=uncertainty_seconds)
            request = CombinedChartApplicationRequest(birth=birth,sex=sex,ziwei_calculation_profile=self.ziwei_calculation_profile,bazi_natal_profile=self.bazi_natal_profile,bazi_temporal_profile=factory(),combined_profile=self.combined_profile,ziwei_application_profile=self.ziwei_application_profile,ziwei_presentation_profile=self.ziwei_presentation_profile,bazi_application_profile=self.bazi_application_profile,ziwei_daxian_frame_id=ziwei_daxian_frame_id,ziwei_annual_year=ziwei_annual_year,ziwei_minor_limit_age=ziwei_minor_limit_age,ziwei_daxian_count=ziwei_daxian_count,bazi_dayun_count=bazi_dayun_count)
            resolution = self.service.resolve(request)
            export = self.service.export(resolution)
            ziwei_svg = None
            if resolution.ziwei_bundle is not None:
                ziwei_svg = self.renderer.render(resolution.ziwei_bundle.view_model,self.renderer_profile).svg
        except CombinedApplicationResolutionError as exc:
            raise LocalCombinedAppRequestError(exc.code,exc.detail,status=422) from exc
        except ValueError as exc:
            raise LocalCombinedAppRequestError("LOCAL_APP_RESOLUTION_FAILED",str(exc),status=422) from exc
        return {"schema":LOCAL_APP_RESOLVE_SCHEMA,"combined_resolution":json_value(resolution),"combined_export":export,"ziwei_svg":ziwei_svg}


class _Handler(BaseHTTPRequestHandler):
    application: LocalCombinedChartApplication
    server_version="CombinedChartLocalApp/1.0"; sys_version=""
    def log_message(self, format: str, *args: object) -> None: return
    def _headers(self) -> None: self.send_header("Content-Security-Policy",CSP); self.send_header("X-Content-Type-Options","nosniff"); self.send_header("Referrer-Policy","no-referrer"); self.send_header("Cache-Control","no-store")
    def _send_bytes(self,status:int,content_type:str,payload:bytes)->None: self.send_response(status); self.send_header("Content-Type",content_type); self.send_header("Content-Length",str(len(payload))); self._headers(); self.end_headers(); self.wfile.write(payload)
    def _send_json(self,status:int,payload:dict[str,Any])->None: self._send_bytes(status,"application/json; charset=utf-8",json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode())
    def _error(self,error:LocalCombinedAppRequestError)->None: self._send_json(error.status,{"schema":LOCAL_APP_ERROR_SCHEMA,"error":{"code":error.code,"detail":error.detail}})
    def do_GET(self)->None:  # noqa: N802
        path=urlsplit(self.path).path
        if path=="/": self._send_bytes(200,"text/html; charset=utf-8",INDEX_HTML.encode()); return
        if path=="/style.css": self._send_bytes(200,"text/css; charset=utf-8",STYLE_CSS.encode()); return
        if path=="/app.js": self._send_bytes(200,"application/javascript; charset=utf-8",APP_JS.encode()); return
        if path=="/health": self._send_json(200,self.application.health()); return
        if path=="/api/profiles": self._send_json(200,self.application.profile_metadata()); return
        self._error(LocalCombinedAppRequestError("LOCAL_APP_NOT_FOUND",path,status=404))
    def do_POST(self)->None:  # noqa: N802
        if urlsplit(self.path).path!="/api/resolve": self._error(LocalCombinedAppRequestError("LOCAL_APP_NOT_FOUND",self.path,status=404)); return
        if self.headers.get("Content-Type","").split(";",1)[0].strip().lower()!="application/json": self._error(LocalCombinedAppRequestError("LOCAL_APP_JSON_REQUIRED","Content-Type must be application/json",status=415)); return
        try: length=int(self.headers.get("Content-Length","0"))
        except ValueError: self._error(LocalCombinedAppRequestError("LOCAL_APP_INVALID_CONTENT_LENGTH","invalid Content-Length")); return
        if length<=0: self._error(LocalCombinedAppRequestError("LOCAL_APP_EMPTY_BODY","request body is required")); return
        if length>MAX_REQUEST_BYTES: self._error(LocalCombinedAppRequestError("LOCAL_APP_REQUEST_TOO_LARGE","request body exceeds local limit",status=413)); return
        try: payload=json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError,json.JSONDecodeError): self._error(LocalCombinedAppRequestError("LOCAL_APP_INVALID_JSON","malformed UTF-8 JSON")); return
        try: result=self.application.resolve_payload(payload)
        except LocalCombinedAppRequestError as exc: self._error(exc); return
        self._send_json(200,result)


def handler_for(application:LocalCombinedChartApplication):
    class Handler(_Handler): pass
    Handler.application=application
    return Handler


def build_server(repository_root:Path,*,port:int=DEFAULT_PORT)->HTTPServer:
    if not 0<=port<=65535: raise ValueError("port must be in [0, 65535]")
    return HTTPServer((DEFAULT_HOST,port),handler_for(LocalCombinedChartApplication(repository_root)))


def _default_repository_root()->Path:
    root=Path(__file__).resolve().parents[3]
    return root if (root/"config"/"time-calendar-policies.json").is_file() else Path.cwd()


def main(argv:list[str]|None=None)->int:
    parser=argparse.ArgumentParser(description="Run the local-only combined Ziwei + Bazi chart shell")
    parser.add_argument("--repository-root",type=Path,default=_default_repository_root()); parser.add_argument("--port",type=int,default=DEFAULT_PORT); parser.add_argument("--no-browser",action="store_true"); args=parser.parse_args(argv)
    server=build_server(args.repository_root,port=args.port); host,port=server.server_address[:2]; url=f"http://{host}:{port}/"; print(f"Combined chart local app: {url}"); print("Bind policy: 127.0.0.1 only. Press Ctrl+C to stop.")
    if not args.no_browser: webbrowser.open(url)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
    return 0


if __name__=="__main__": raise SystemExit(main())
