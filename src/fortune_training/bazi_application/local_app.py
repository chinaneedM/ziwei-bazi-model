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

from fortune_training.bazi_chart import (
    ZI_START_23_PROFILE_ID,
    bazi_foundation_zi_start_23_r1_profile,
    build_production_bazi_profile,
)
from fortune_training.bazi_temporal import (
    BaziSex,
    bazi_temporal_v1_continuous_profile,
    bazi_temporal_wenzhen_china_compatibility_r1_profile,
)
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimePrecision
from fortune_training.calendar_foundation.models import json_value

from .models import BaziApplicationRequest
from .profile import APPLICATION_PROFILE_ID, bazi_local_application_v1_profile
from .service import BaziApplicationResolutionError, BaziChartService


LOCAL_APP_ID = "BAZI-LOCAL-BROWSER-APP-V1"
LOCAL_APP_VERSION = "1.0.0"
LOCAL_APP_HEALTH_SCHEMA = "BAZI-LOCAL-APP-HEALTH-V1"
LOCAL_APP_RESOLVE_SCHEMA = "BAZI-LOCAL-APP-RESOLVE-V1"
LOCAL_APP_ERROR_SCHEMA = "BAZI-LOCAL-APP-ERROR-V1"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8766
MAX_REQUEST_BYTES = 64 * 1024

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
  <title>八字排盘 · Local</title>
  <link rel="stylesheet" href="/style.css">
</head>
<body>
<main class="shell">
  <header><div><h1>八字排盘</h1><p>Natal + 大运 · Local Application V1</p></div><span>LOCAL ONLY</span></header>
  <section class="panel form-panel">
    <form id="chart-form">
      <div class="grid">
        <label>出生时间<input id="birth-datetime" type="datetime-local" value="1984-02-10T10:30" required></label>
        <label>出生地<input id="birth-place" value="Beijing" required></label>
        <label>纬度<input id="latitude" type="number" step="0.000001" min="-90" max="90" value="39.9042" required></label>
        <label>经度<input id="longitude" type="number" step="0.000001" min="-180" max="180" value="116.4074" required></label>
        <label>时区<input id="timezone-id" value="Asia/Shanghai" required></label>
        <label>性别<select id="sex"><option value="MALE">男</option><option value="FEMALE">女</option></select></label>
        <label>时间精度<select id="precision"><option value="EXACT_SECOND">精确到秒</option><option value="NEAREST_MINUTE">约到分钟</option><option value="NEAREST_HOUR">约到小时</option><option value="APPROXIMATE">约略时间</option></select></label>
        <label>不确定范围 ±秒<input id="uncertainty-seconds" type="number" min="0" max="86400" value="0"></label>
        <label>Natal Profile<select id="natal-profile"><option value="BAZI-FOUNDATION-V1-R1">MIDNIGHT / CLASSICAL_CONTINUOUS</option><option value="BAZI-FOUNDATION-ZI-START-23-R1">ZI_START_23 / ZI_START_ROLLOVER</option></select></label>
        <label>大运 Profile<select id="temporal-profile"><option value="BAZI-TEMPORAL-V1-CONTINUOUS-R1">CONTINUOUS-R1</option><option value="BAZI-TEMPORAL-WENZHEN-CHINA-COMPATIBILITY-R1">WENZHEN-COMPATIBILITY-R1</option></select></label>
        <label>大运数量<input id="dayun-count" type="number" min="1" max="20" value="12"></label>
      </div>
      <div class="actions"><button id="submit" type="submit">排盘</button><button id="download" type="button" disabled>保存 JSON</button></div>
    </form>
  </section>
  <section class="status-grid">
    <div><span>状态</span><strong id="status">未运行</strong></div>
    <div><span>BundleHash</span><code id="bundle-hash">-</code></div>
    <div><span>ViewHash</span><code id="view-hash">-</code></div>
  </section>
  <section id="error" class="error" hidden><strong id="error-code"></strong><span id="error-detail"></span></section>
  <section id="results" class="results"><div class="placeholder">输入出生信息后点击“排盘”</div></section>
</main>
<script src="/app.js" defer></script>
</body>
</html>
"""

STYLE_CSS = """
:root { font-family: system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; color: #17191c; background: #f5f6f8; }
* { box-sizing: border-box; }
body { margin: 0; }
.shell { width: min(1320px, calc(100% - 32px)); margin: 22px auto 48px; }
header { display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; }
h1 { margin:0; } header p { margin:5px 0 0; color:#666; } header span { border:1px solid #ccc; border-radius:999px; padding:6px 9px; font-size:12px; background:#fff; }
.panel,.status-grid>div,.candidate,.error { background:#fff; border:1px solid #dfe2e6; border-radius:12px; }
.form-panel { padding:16px; }
.grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:11px; }
label { display:flex; flex-direction:column; gap:5px; font-size:12px; color:#59616a; }
input,select { padding:9px 10px; border:1px solid #ccd2d8; border-radius:7px; background:#fff; }
.actions { display:flex; gap:9px; margin-top:14px; }
button { padding:9px 15px; border:1px solid #222; border-radius:7px; background:#222; color:#fff; cursor:pointer; }
button[type=button] { background:#fff; color:#222; border-color:#ccd2d8; } button:disabled { opacity:.45; }
.status-grid { display:grid; grid-template-columns:1fr 2fr 2fr; gap:10px; margin:12px 0; }
.status-grid>div { padding:10px 12px; min-width:0; } .status-grid span { display:block; color:#777; font-size:11px; } code { display:block; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.error { padding:12px; margin-bottom:12px; } .error strong { margin-right:8px; }
.results { display:grid; gap:12px; } .candidate { padding:16px; }
.candidate-head { display:flex; justify-content:space-between; gap:12px; align-items:flex-start; margin-bottom:12px; } .candidate h2 { margin:0; font-size:18px; }
.meta { color:#666; font-size:12px; line-height:1.6; }
.pillars { display:grid; grid-template-columns:repeat(4,1fr); gap:8px; margin:12px 0; }
.pillar { border:1px solid #e0e3e7; border-radius:9px; padding:12px; text-align:center; } .pillar .pos { font-size:11px; color:#777; } .pillar .ganzhi { font-size:25px; margin:5px 0; } .pillar .ten { font-size:12px; }
.hidden { margin-top:7px; font-size:12px; color:#555; line-height:1.7; }
.shensha { margin:10px 0; padding:10px; border:1px solid #e2d7bd; border-radius:9px; background:#fffdf7; }
.shensha strong { display:block; margin-bottom:6px; font-size:12px; color:#795548; }
.shensha-items { display:flex; flex-wrap:wrap; gap:6px; }
.shensha-item { padding:5px 7px; border:1px solid #eadfc8; border-radius:6px; background:#fff; font-size:11px; }
.dayun { overflow:auto; } table { width:100%; border-collapse:collapse; font-size:12px; } th,td { padding:7px 8px; border-bottom:1px solid #e5e7ea; text-align:left; white-space:nowrap; }
.placeholder { min-height:260px; display:grid; place-items:center; color:#888; }
@media (max-width:900px) { .grid { grid-template-columns:1fr 1fr; } .pillars { grid-template-columns:1fr 1fr; } .status-grid { grid-template-columns:1fr; } }
"""

APP_JS = """
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  let lastBundle = null;
  const shortHash = (value) => value ? value.slice(0, 18) : '-';
  const el = (name, text, className) => { const node = document.createElement(name); if (text !== undefined) node.textContent = text; if (className) node.className = className; return node; };
  function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }
  function showError(code, detail) { $('error-code').textContent = code; $('error-detail').textContent = detail; $('error').hidden = false; }
  function renderCandidate(candidate, index) {
    const card = el('article', undefined, 'candidate');
    const head = el('div', undefined, 'candidate-head');
    const titleWrap = el('div'); titleWrap.append(el('h2', `候选 ${index + 1}`));
    titleWrap.append(el('div', `日主：${candidate.view.day_master_stem} · ${candidate.view.dayun.direction} · ${candidate.view.dayun.sex}`, 'meta'));
    head.append(titleWrap, el('div', `Natal ${shortHash(candidate.natal_fact_hash)}\nDayun ${shortHash(candidate.temporal_fact_hash)}`, 'meta'));
    card.append(head);
    const time = candidate.view.time_provenance[0];
    card.append(el('div', `报告时间：${candidate.view.birth.reported_local_datetime}　真太阳时：${time?.local_apparent_solar_datetime || '-'}　UTC：${time?.birth_utc || '-'}`, 'meta'));
    const pillars = el('div', undefined, 'pillars');
    candidate.view.pillars.forEach((p) => {
      const box = el('div', undefined, 'pillar');
      box.append(el('div', p.position, 'pos'), el('div', p.ganzhi, 'ganzhi'), el('div', p.visible_ten_god, 'ten'));
      const hidden = el('div', undefined, 'hidden');
      hidden.textContent = p.hidden_stems.length ? p.hidden_stems.map((h) => `${h.stem}·${h.ten_god}`).join(' / ') : '无藏干';
      box.append(hidden); pillars.append(box);
    });
    card.append(pillars);
    const shensha = candidate.view.shensha;
    if (shensha?.candidates?.length) {
      const section = el('section', undefined, 'shensha');
      section.append(el('strong', '神煞事实候选（年柱法 / 日柱法分列，不裁决、不合并）'));
      const items = el('div', undefined, 'shensha-items');
      const basis = {DAY_STEM:'日干',YEAR_STEM:'年干',DAY_BRANCH:'日支',YEAR_BRANCH:'年支'};
      shensha.candidates.filter((row) => row.present).forEach((row) => items.append(el('span', `${row.display_name}｜${basis[row.anchor_basis] || row.anchor_basis} ${row.anchor_value} → ${row.occurrences.map((hit) => hit.pillar_position).join('、')}`, 'shensha-item')));
      if (!items.childElementCount) items.append(el('span', '当前四柱无匹配', 'shensha-item'));
      section.append(items); card.append(section);
    }
    const j = candidate.view.dayun.jiaoyun;
    card.append(el('div', `交运：${j.first_transition_utc}　锚点：${j.anchor_jie_name}　象征岁数：${j.symbolic_age.years_360}年${j.symbolic_age.months_30}月${j.symbolic_age.days}日`, 'meta'));
    const wrap = el('div', undefined, 'dayun'); const table = el('table');
    const trh = el('tr'); ['序','大运','开始 UTC','结束 UTC'].forEach((x) => trh.append(el('th', x))); const thead = el('thead'); thead.append(trh); table.append(thead);
    const tbody = el('tbody'); candidate.view.dayun.frames.forEach((f) => { const tr = el('tr'); [f.index,f.ganzhi,f.start_utc,f.end_utc].forEach((x) => tr.append(el('td', String(x)))); tbody.append(tr); }); table.append(tbody); wrap.append(table); card.append(wrap);
    return card;
  }
  $('chart-form').addEventListener('submit', async (event) => {
    event.preventDefault(); $('error').hidden = true; $('submit').disabled = true; $('status').textContent = '计算中'; $('download').disabled = true;
    const payload = {
      birth_datetime: $('birth-datetime').value,
      birth_place: $('birth-place').value.trim(), latitude: Number.parseFloat($('latitude').value), longitude: Number.parseFloat($('longitude').value),
      timezone_id: $('timezone-id').value.trim(), sex: $('sex').value, precision: $('precision').value,
      uncertainty_seconds: Number.parseInt($('uncertainty-seconds').value, 10), natal_profile_id: $('natal-profile').value,
      temporal_profile_id: $('temporal-profile').value, application_profile_id: 'BAZI-LOCAL-APPLICATION-V1-R1', dayun_count: Number.parseInt($('dayun-count').value, 10)
    };
    try {
      const response = await fetch('/api/resolve', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload) });
      const data = await response.json(); if (!response.ok) throw data.error || {code:`HTTP_${response.status}`, detail:'Request failed'};
      lastBundle = data.application_bundle; $('status').textContent = lastBundle.status; $('bundle-hash').textContent = shortHash(lastBundle.bundle_hash); $('bundle-hash').title = lastBundle.bundle_hash; $('view-hash').textContent = shortHash(lastBundle.view_hash); $('view-hash').title = lastBundle.view_hash;
      const results = $('results'); clear(results); lastBundle.candidates.forEach((candidate, index) => results.append(renderCandidate(candidate,index))); $('download').disabled = false;
    } catch (error) { lastBundle = null; $('status').textContent = '失败'; showError(error.code || 'LOCAL_APP_REQUEST_FAILED', error.detail || String(error)); }
    finally { $('submit').disabled = false; }
  });
  $('download').addEventListener('click', () => { if (!lastBundle) return; const blob = new Blob([JSON.stringify(lastBundle,null,2)],{type:'application/json;charset=utf-8'}); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href=url; a.download='bazi-chart.json'; document.body.append(a); a.click(); a.remove(); URL.revokeObjectURL(url); });
})();
"""


class LocalAppRequestError(ValueError):
    def __init__(self, code: str, detail: str, *, status: int = 400) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail
        self.status = status


def _required_text(payload: dict[str, Any], key: str, *, max_length: int) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise LocalAppRequestError("LOCAL_APP_INVALID_INPUT", f"{key} is required")
    value = value.strip()
    if len(value) > max_length:
        raise LocalAppRequestError("LOCAL_APP_INVALID_INPUT", f"{key} is too long")
    return value


def _finite_float(payload: dict[str, Any], key: str) -> float:
    value = payload.get(key)
    if isinstance(value, bool):
        raise LocalAppRequestError("LOCAL_APP_INVALID_INPUT", f"{key} must be numeric")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise LocalAppRequestError("LOCAL_APP_INVALID_INPUT", f"{key} must be numeric") from exc
    if not math.isfinite(result):
        raise LocalAppRequestError("LOCAL_APP_INVALID_INPUT", f"{key} must be finite")
    return result


def _bounded_int(payload: dict[str, Any], key: str, minimum: int, maximum: int) -> int:
    value = payload.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= maximum:
        raise LocalAppRequestError("LOCAL_APP_INVALID_INPUT", f"{key} must be an integer in [{minimum}, {maximum}]")
    return value


def _parse_datetime(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise LocalAppRequestError("LOCAL_APP_INVALID_INPUT", "birth_datetime must be ISO local datetime") from exc
    if parsed.tzinfo is not None:
        raise LocalAppRequestError("LOCAL_APP_INVALID_INPUT", "birth_datetime must be a naive local wall-clock value")
    return parsed


def _parse_sex(value: str) -> BaziSex:
    aliases = {"男": "MALE", "女": "FEMALE", "M": "MALE", "F": "FEMALE"}
    normalized = aliases.get(value.strip().upper(), value.strip().upper())
    try:
        return BaziSex(normalized)
    except ValueError as exc:
        raise LocalAppRequestError("LOCAL_APP_INVALID_INPUT", "sex must be MALE or FEMALE") from exc


def _parse_precision(value: str) -> TimePrecision:
    try:
        return TimePrecision(value.strip().upper())
    except ValueError as exc:
        raise LocalAppRequestError("LOCAL_APP_INVALID_INPUT", "unsupported precision") from exc


class LocalBaziApplication:
    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root.resolve()
        registry_path = self.repository_root / "config" / "time-calendar-policies.json"
        if not registry_path.is_file():
            raise LocalAppRequestError("LOCAL_APP_REPOSITORY_ROOT_INVALID", f"missing {registry_path}", status=500)
        self.registry = PolicyRegistry.from_file(registry_path)
        self.service = BaziChartService.from_repository(self.repository_root)

    def health(self) -> dict[str, Any]:
        return {"schema":LOCAL_APP_HEALTH_SCHEMA,"status":"ok","application_id":LOCAL_APP_ID,"application_version":LOCAL_APP_VERSION,"bind_policy":"LOOPBACK_ONLY"}

    def resolve_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise LocalAppRequestError("LOCAL_APP_INVALID_JSON", "request body must be a JSON object")
        birth_datetime = _parse_datetime(_required_text(payload, "birth_datetime", max_length=64))
        birth_place = _required_text(payload, "birth_place", max_length=160)
        latitude = _finite_float(payload, "latitude")
        longitude = _finite_float(payload, "longitude")
        timezone_id = _required_text(payload, "timezone_id", max_length=120)
        try:
            ZoneInfo(timezone_id)
        except ZoneInfoNotFoundError as exc:
            raise LocalAppRequestError("LOCAL_APP_INVALID_TIMEZONE", timezone_id) from exc
        sex = _parse_sex(_required_text(payload, "sex", max_length=16))
        precision = _parse_precision(_required_text(payload, "precision", max_length=32))
        uncertainty_seconds = _bounded_int(payload, "uncertainty_seconds", 0, 86400)
        dayun_count = _bounded_int(payload, "dayun_count", 1, 20)
        natal_profile_id = _required_text(payload, "natal_profile_id", max_length=80)
        temporal_profile_id = _required_text(payload, "temporal_profile_id", max_length=100)
        application_profile_id = _required_text(payload, "application_profile_id", max_length=80)
        natal_profiles = {
            "BAZI-FOUNDATION-V1-R1": build_production_bazi_profile,
            ZI_START_23_PROFILE_ID: bazi_foundation_zi_start_23_r1_profile,
        }
        natal_factory = natal_profiles.get(natal_profile_id)
        if natal_factory is None:
            raise LocalAppRequestError("LOCAL_APP_UNSUPPORTED_NATAL_PROFILE", natal_profile_id)
        if application_profile_id != APPLICATION_PROFILE_ID:
            raise LocalAppRequestError("LOCAL_APP_UNSUPPORTED_APPLICATION_PROFILE", application_profile_id)
        temporal_profiles = {
            "BAZI-TEMPORAL-V1-CONTINUOUS-R1": bazi_temporal_v1_continuous_profile,
            "BAZI-TEMPORAL-WENZHEN-CHINA-COMPATIBILITY-R1": bazi_temporal_wenzhen_china_compatibility_r1_profile,
        }
        factory = temporal_profiles.get(temporal_profile_id)
        if factory is None:
            raise LocalAppRequestError("LOCAL_APP_UNSUPPORTED_TEMPORAL_PROFILE", temporal_profile_id)
        try:
            birth = BirthInput(
                reported_local_datetime=birth_datetime,
                birth_place=birth_place,
                latitude=latitude,
                longitude=longitude,
                timezone_id=timezone_id,
                precision=precision,
                uncertainty_seconds=uncertainty_seconds,
            )
            request = BaziApplicationRequest(
                birth=birth,
                sex=sex,
                natal_profile=natal_factory(self.registry),
                temporal_profile=factory(),
                application_profile=bazi_local_application_v1_profile(),
                dayun_count=dayun_count,
            )
            bundle = self.service.resolve(request)
        except BaziApplicationResolutionError as exc:
            raise LocalAppRequestError(exc.code, exc.detail, status=422) from exc
        except ValueError as exc:
            raise LocalAppRequestError("LOCAL_APP_RESOLUTION_FAILED", str(exc), status=422) from exc
        return {"schema": LOCAL_APP_RESOLVE_SCHEMA, "application_bundle": json_value(bundle)}


class _Handler(BaseHTTPRequestHandler):
    application: LocalBaziApplication
    server_version = "BaziLocalApp/1.0"
    sys_version = ""
    def log_message(self, format: str, *args: object) -> None: return
    def _headers(self) -> None:
        self.send_header("Content-Security-Policy", CSP); self.send_header("X-Content-Type-Options", "nosniff"); self.send_header("Referrer-Policy", "no-referrer"); self.send_header("Cache-Control", "no-store")
    def _send_bytes(self, status: int, content_type: str, payload: bytes) -> None:
        self.send_response(status); self.send_header("Content-Type", content_type); self.send_header("Content-Length", str(len(payload))); self._headers(); self.end_headers(); self.wfile.write(payload)
    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        self._send_bytes(status, "application/json; charset=utf-8", json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8"))
    def _error(self, error: LocalAppRequestError) -> None:
        self._send_json(error.status,{"schema":LOCAL_APP_ERROR_SCHEMA,"error":{"code":error.code,"detail":error.detail}})
    def do_GET(self) -> None:  # noqa: N802
        path=urlsplit(self.path).path
        if path=="/": self._send_bytes(200,"text/html; charset=utf-8",INDEX_HTML.encode()); return
        if path=="/style.css": self._send_bytes(200,"text/css; charset=utf-8",STYLE_CSS.encode()); return
        if path=="/app.js": self._send_bytes(200,"application/javascript; charset=utf-8",APP_JS.encode()); return
        if path=="/health": self._send_json(200,self.application.health()); return
        self._error(LocalAppRequestError("LOCAL_APP_NOT_FOUND",path,status=404))
    def do_POST(self) -> None:  # noqa: N802
        if urlsplit(self.path).path!="/api/resolve": self._error(LocalAppRequestError("LOCAL_APP_NOT_FOUND",self.path,status=404)); return
        if self.headers.get("Content-Type","").split(";",1)[0].strip().lower()!="application/json": self._error(LocalAppRequestError("LOCAL_APP_JSON_REQUIRED","Content-Type must be application/json",status=415)); return
        try: length=int(self.headers.get("Content-Length","0"))
        except ValueError: self._error(LocalAppRequestError("LOCAL_APP_INVALID_CONTENT_LENGTH","invalid Content-Length")); return
        if length<=0: self._error(LocalAppRequestError("LOCAL_APP_EMPTY_BODY","request body is required")); return
        if length>MAX_REQUEST_BYTES: self._error(LocalAppRequestError("LOCAL_APP_REQUEST_TOO_LARGE","request body exceeds local limit",status=413)); return
        try: payload=json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError,json.JSONDecodeError): self._error(LocalAppRequestError("LOCAL_APP_INVALID_JSON","malformed UTF-8 JSON")); return
        try: response=self.application.resolve_payload(payload)
        except LocalAppRequestError as exc: self._error(exc); return
        self._send_json(200,response)


def handler_for(application: LocalBaziApplication):
    class Handler(_Handler): pass
    Handler.application=application
    return Handler


def build_server(repository_root: Path, *, port: int = DEFAULT_PORT) -> HTTPServer:
    if not 0 <= port <= 65535: raise ValueError("port must be in [0, 65535]")
    return HTTPServer((DEFAULT_HOST,port),handler_for(LocalBaziApplication(repository_root)))


def _default_repository_root() -> Path:
    root=Path(__file__).resolve().parents[3]
    return root if (root/"config"/"time-calendar-policies.json").is_file() else Path.cwd()


def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(description="Run the local-only Bazi browser application")
    parser.add_argument("--repository-root",type=Path,default=_default_repository_root())
    parser.add_argument("--port",type=int,default=DEFAULT_PORT)
    parser.add_argument("--no-browser",action="store_true")
    args=parser.parse_args(argv); server=build_server(args.repository_root,port=args.port); host,port=server.server_address[:2]; url=f"http://{host}:{port}/"; print(f"Bazi local app: {url}"); print("Bind policy: 127.0.0.1 only. Press Ctrl+C to stop.")
    if not args.no_browser: webbrowser.open(url)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
