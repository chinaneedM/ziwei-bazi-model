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

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry
from fortune_training.calendar_foundation.models import json_value
from fortune_training.ziwei_chart import Sex, build_production_ziwei_profile

from .models import ApplicationBirthRequest
from .service import ApplicationResolutionError, ZiweiChartService
from .svg import SvgRendererProfile, ZiweiTwelvePalaceSvgRenderer


LOCAL_APP_ID = "ZIWEI-LOCAL-BROWSER-APP-V1"
LOCAL_APP_VERSION = "1.0.0"
LOCAL_APP_HEALTH_SCHEMA = "ZIWEI-LOCAL-APP-HEALTH-V1"
LOCAL_APP_RESOLVE_SCHEMA = "ZIWEI-LOCAL-APP-RESOLVE-V1"
LOCAL_APP_ERROR_SCHEMA = "ZIWEI-LOCAL-APP-ERROR-V1"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
MAX_REQUEST_BYTES = 64 * 1024

CSP = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self'; "
    "img-src 'self' data:; "
    "connect-src 'self'; "
    "object-src 'none'; "
    "base-uri 'none'; "
    "frame-ancestors 'none'; "
    "form-action 'self'"
)

INDEX_HTML = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>紫微排盘 · Local</title>
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  <main class="shell">
    <header>
      <div>
        <h1>紫微排盘</h1>
        <p>本地 Application V1 · 计算、结构与显示分层</p>
      </div>
      <span class="local-badge">LOCAL ONLY</span>
    </header>

    <section class="panel input-panel">
      <form id="chart-form">
        <div class="grid">
          <label>出生时间
            <input id="birth-datetime" type="datetime-local" value="1994-05-17T14:30" required>
          </label>
          <label>出生地
            <input id="birth-place" type="text" value="Beijing" maxlength="160" required>
          </label>
          <label>纬度
            <input id="latitude" type="number" step="0.000001" value="39.9042" min="-90" max="90" required>
          </label>
          <label>经度
            <input id="longitude" type="number" step="0.000001" value="116.4074" min="-180" max="180" required>
          </label>
          <label>时区
            <input id="timezone-id" type="text" value="Asia/Shanghai" maxlength="120" required>
          </label>
          <label>性别
            <select id="sex" required>
              <option value="MALE">男</option>
              <option value="FEMALE">女</option>
            </select>
          </label>
          <label>大限 Frame（可选）
            <input id="daxian-frame-id" type="text" value="DAXIAN:index=1" maxlength="80">
          </label>
          <label>流年（可选）
            <input id="annual-year" type="number" value="2001" min="1" max="9999">
          </label>
          <label>小限岁数（可选）
            <input id="minor-limit-age" type="number" value="8" min="1" max="200">
          </label>
        </div>
        <div class="actions">
          <button id="submit-button" type="submit">排盘</button>
          <button id="download-svg" type="button" disabled>保存 SVG</button>
          <button id="download-json" type="button" disabled>保存 JSON</button>
        </div>
      </form>
    </section>

    <section class="status-row" aria-live="polite">
      <div><span>状态</span><strong id="status">未运行</strong></div>
      <div><span>BundleHash</span><code id="bundle-hash">-</code></div>
      <div><span>ViewHash</span><code id="view-hash">-</code></div>
      <div><span>RenderHash</span><code id="render-hash">-</code></div>
    </section>

    <section class="panel chart-panel">
      <div id="chart" class="chart-placeholder">输入出生信息后点击“排盘”</div>
    </section>

    <section id="error-panel" class="error-panel" hidden>
      <strong id="error-code"></strong>
      <span id="error-detail"></span>
    </section>
  </main>
  <script src="/app.js" defer></script>
</body>
</html>
"""

STYLE_CSS = """
:root { color-scheme: light; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
* { box-sizing: border-box; }
body { margin: 0; background: #f5f6f8; color: #17191c; }
.shell { width: min(1480px, calc(100% - 40px)); margin: 24px auto 48px; }
header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; }
h1 { margin: 0; font-size: 28px; }
header p { margin: 5px 0 0; color: #666d76; }
.local-badge { font-size: 12px; letter-spacing: .08em; border: 1px solid #c8ccd2; border-radius: 999px; padding: 7px 10px; background: #fff; }
.panel { background: #fff; border: 1px solid #dfe2e6; border-radius: 14px; box-shadow: 0 3px 16px rgba(0,0,0,.04); }
.input-panel { padding: 18px; margin-bottom: 14px; }
.grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
label { display: flex; flex-direction: column; gap: 6px; font-size: 12px; color: #555d66; }
input, select { width: 100%; border: 1px solid #cfd4da; border-radius: 8px; background: #fff; color: #111; padding: 10px 11px; font: inherit; }
input:focus, select:focus { outline: 2px solid #8998aa; outline-offset: 1px; }
.actions { display: flex; gap: 10px; margin-top: 16px; }
button { border: 1px solid #222; border-radius: 8px; padding: 10px 16px; background: #202327; color: #fff; cursor: pointer; }
button[type="button"] { background: #fff; color: #202327; border-color: #c9ced5; }
button:disabled { opacity: .45; cursor: default; }
.status-row { display: grid; grid-template-columns: 1fr 1.3fr 1.3fr 1.3fr; gap: 10px; margin: 14px 0; }
.status-row > div { min-width: 0; background: #fff; border: 1px solid #dfe2e6; border-radius: 10px; padding: 11px 12px; }
.status-row span { display: block; color: #737a83; font-size: 11px; margin-bottom: 4px; }
.status-row strong, .status-row code { display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 12px; }
.chart-panel { padding: 12px; overflow: auto; }
.chart-panel svg { display: block; width: 100%; height: auto; min-width: 900px; }
.chart-placeholder { min-height: 560px; display: grid; place-items: center; color: #8b9199; }
.error-panel { margin-top: 12px; border: 1px solid #d8b4b4; background: #fff6f6; border-radius: 10px; padding: 12px 14px; }
.error-panel strong { margin-right: 8px; }
@media (max-width: 900px) { .grid { grid-template-columns: 1fr 1fr; } .status-row { grid-template-columns: 1fr 1fr; } }
"""

APP_JS = """
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const form = $('chart-form');
  const submit = $('submit-button');
  const errorPanel = $('error-panel');
  const downloadSvg = $('download-svg');
  const downloadJson = $('download-json');
  let lastResult = null;

  const optionalInteger = (id) => {
    const value = $(id).value.trim();
    return value === '' ? null : Number.parseInt(value, 10);
  };

  const optionalText = (id) => {
    const value = $(id).value.trim();
    return value === '' ? null : value;
  };

  const shortHash = (value) => value ? value.slice(0, 16) : '-';

  function showError(code, detail) {
    $('error-code').textContent = code || 'ERROR';
    $('error-detail').textContent = detail || 'Unknown error';
    errorPanel.hidden = false;
  }

  function clearError() {
    errorPanel.hidden = true;
    $('error-code').textContent = '';
    $('error-detail').textContent = '';
  }

  function download(name, content, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = name;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearError();
    submit.disabled = true;
    submit.textContent = '计算中…';
    downloadSvg.disabled = true;
    downloadJson.disabled = true;
    $('status').textContent = '计算中';

    const payload = {
      birth_datetime: $('birth-datetime').value,
      birth_place: $('birth-place').value.trim(),
      latitude: Number.parseFloat($('latitude').value),
      longitude: Number.parseFloat($('longitude').value),
      timezone_id: $('timezone-id').value.trim(),
      sex: $('sex').value,
      daxian_frame_id: optionalText('daxian-frame-id'),
      annual_year: optionalInteger('annual-year'),
      minor_limit_age: optionalInteger('minor-limit-age')
    };

    try {
      const response = await fetch('/api/resolve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await response.json();
      if (!response.ok) {
        throw { code: data.error?.code || `HTTP_${response.status}`, detail: data.error?.detail || 'Request failed' };
      }
      lastResult = data;
      const parsed = new DOMParser().parseFromString(data.svg, 'image/svg+xml');
      if (parsed.querySelector('parsererror')) {
        throw { code: 'LOCAL_APP_SVG_PARSE_FAILED', detail: 'Generated SVG could not be parsed by the browser.' };
      }
      const chart = $('chart');
      chart.classList.remove('chart-placeholder');
      chart.replaceChildren(document.importNode(parsed.documentElement, true));
      $('status').textContent = data.application_export.resolution_status;
      $('bundle-hash').textContent = shortHash(data.application_export.bundle_hash);
      $('bundle-hash').title = data.application_export.bundle_hash;
      $('view-hash').textContent = shortHash(data.application_export.view_hash);
      $('view-hash').title = data.application_export.view_hash;
      $('render-hash').textContent = shortHash(data.svg_artifact.render_hash);
      $('render-hash').title = data.svg_artifact.render_hash;
      downloadSvg.disabled = false;
      downloadJson.disabled = false;
    } catch (error) {
      lastResult = null;
      $('status').textContent = '失败';
      showError(error.code || 'LOCAL_APP_REQUEST_FAILED', error.detail || String(error));
    } finally {
      submit.disabled = false;
      submit.textContent = '排盘';
    }
  });

  downloadSvg.addEventListener('click', () => {
    if (lastResult) download('ziwei-chart.svg', lastResult.svg, 'image/svg+xml;charset=utf-8');
  });

  downloadJson.addEventListener('click', () => {
    if (lastResult) download('ziwei-chart.json', JSON.stringify(lastResult, null, 2), 'application/json;charset=utf-8');
  });
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


def _optional_text(payload: dict[str, Any], key: str, *, max_length: int) -> str | None:
    value = payload.get(key)
    if value is None or value == "":
        return None
    if not isinstance(value, str):
        raise LocalAppRequestError("LOCAL_APP_INVALID_INPUT", f"{key} must be text or null")
    value = value.strip()
    if not value:
        return None
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


def _optional_int(payload: dict[str, Any], key: str, *, minimum: int, maximum: int) -> int | None:
    value = payload.get(key)
    if value is None or value == "":
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise LocalAppRequestError("LOCAL_APP_INVALID_INPUT", f"{key} must be an integer or null")
    if not minimum <= value <= maximum:
        raise LocalAppRequestError("LOCAL_APP_INVALID_INPUT", f"{key} is outside the supported range")
    return value


def _parse_datetime(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise LocalAppRequestError("LOCAL_APP_INVALID_INPUT", "birth_datetime must be ISO local datetime") from exc
    if parsed.tzinfo is not None:
        raise LocalAppRequestError("LOCAL_APP_INVALID_INPUT", "birth_datetime must not include a timezone offset")
    return parsed


def _parse_sex(value: str) -> Sex:
    normalized = value.strip().upper()
    aliases = {"男": "MALE", "女": "FEMALE", "M": "MALE", "F": "FEMALE"}
    normalized = aliases.get(normalized, normalized)
    try:
        return Sex(normalized)
    except ValueError as exc:
        raise LocalAppRequestError("LOCAL_APP_INVALID_INPUT", "sex must be MALE or FEMALE") from exc


class LocalZiweiApplication:
    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root.resolve()
        registry_path = self.repository_root / "config" / "time-calendar-policies.json"
        if not registry_path.is_file():
            raise LocalAppRequestError(
                "LOCAL_APP_REPOSITORY_ROOT_INVALID",
                f"missing {registry_path}",
                status=500,
            )
        self.registry = PolicyRegistry.from_file(registry_path)
        self.calculation_profile = build_production_ziwei_profile(self.registry)
        self.service = ZiweiChartService.from_repository(self.repository_root)
        self.renderer = ZiweiTwelvePalaceSvgRenderer()
        self.renderer_profile = SvgRendererProfile()

    def health(self) -> dict[str, Any]:
        return {
            "schema": LOCAL_APP_HEALTH_SCHEMA,
            "status": "ok",
            "application_id": LOCAL_APP_ID,
            "application_version": LOCAL_APP_VERSION,
            "bind_policy": "LOOPBACK_ONLY",
        }

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
        daxian_frame_id = _optional_text(payload, "daxian_frame_id", max_length=80)
        annual_year = _optional_int(payload, "annual_year", minimum=1, maximum=9999)
        minor_limit_age = _optional_int(payload, "minor_limit_age", minimum=1, maximum=200)

        try:
            birth = BirthInput(
                reported_local_datetime=birth_datetime,
                birth_place=birth_place,
                latitude=latitude,
                longitude=longitude,
                timezone_id=timezone_id,
            )
            request = ApplicationBirthRequest(
                birth=birth,
                sex=sex,
                calculation_profile=self.calculation_profile,
                daxian_frame_id=daxian_frame_id,
                annual_year=annual_year,
                minor_limit_age=minor_limit_age,
            )
            bundle = self.service.resolve(request)
            export = self.service.export(bundle)
            artifact = self.renderer.render(bundle.view_model, self.renderer_profile)
        except ApplicationResolutionError as exc:
            raise LocalAppRequestError(exc.diagnostic_code, str(exc), status=422) from exc
        except ValueError as exc:
            code = getattr(exc, "diagnostic_code", None) or "LOCAL_APP_RESOLUTION_FAILED"
            raise LocalAppRequestError(str(code), str(exc), status=422) from exc

        return {
            "schema": LOCAL_APP_RESOLVE_SCHEMA,
            "application_export": export,
            "svg_artifact": {
                "schema": artifact.schema,
                "renderer_profile": json_value(artifact.renderer_profile),
                "source_view_hash": artifact.source_view_hash,
                "render_hash": artifact.render_hash,
            },
            "svg": artifact.svg,
        }


class _LocalAppHandler(BaseHTTPRequestHandler):
    application: LocalZiweiApplication
    server_version = "ZiweiLocalApp/1.0"
    sys_version = ""

    def log_message(self, format: str, *args: object) -> None:
        return

    def _security_headers(self) -> None:
        self.send_header("Content-Security-Policy", CSP)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cache-Control", "no-store")

    def _send_bytes(self, status: int, content_type: str, payload: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self._security_headers()
        self.end_headers()
        self.wfile.write(payload)

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        self._send_bytes(status, "application/json; charset=utf-8", body)

    def _send_error_payload(self, error: LocalAppRequestError) -> None:
        self._send_json(
            error.status,
            {
                "schema": LOCAL_APP_ERROR_SCHEMA,
                "error": {"code": error.code, "detail": error.detail},
            },
        )

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler contract
        path = urlsplit(self.path).path
        if path == "/":
            self._send_bytes(200, "text/html; charset=utf-8", INDEX_HTML.encode("utf-8"))
            return
        if path == "/style.css":
            self._send_bytes(200, "text/css; charset=utf-8", STYLE_CSS.encode("utf-8"))
            return
        if path == "/app.js":
            self._send_bytes(200, "application/javascript; charset=utf-8", APP_JS.encode("utf-8"))
            return
        if path == "/health":
            self._send_json(200, self.application.health())
            return
        self._send_error_payload(LocalAppRequestError("LOCAL_APP_NOT_FOUND", path, status=404))

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler contract
        path = urlsplit(self.path).path
        if path != "/api/resolve":
            self._send_error_payload(LocalAppRequestError("LOCAL_APP_NOT_FOUND", path, status=404))
            return
        content_type = self.headers.get("Content-Type", "")
        if content_type.split(";", 1)[0].strip().lower() != "application/json":
            self._send_error_payload(
                LocalAppRequestError("LOCAL_APP_JSON_REQUIRED", "Content-Type must be application/json", status=415)
            )
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_error_payload(LocalAppRequestError("LOCAL_APP_INVALID_CONTENT_LENGTH", "invalid Content-Length"))
            return
        if content_length <= 0:
            self._send_error_payload(LocalAppRequestError("LOCAL_APP_EMPTY_BODY", "request body is required"))
            return
        if content_length > MAX_REQUEST_BYTES:
            self._send_error_payload(
                LocalAppRequestError("LOCAL_APP_REQUEST_TOO_LARGE", "request body exceeds local limit", status=413)
            )
            return
        raw = self.rfile.read(content_length)
        try:
            decoded = raw.decode("utf-8")
            payload = json.loads(decoded)
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_error_payload(LocalAppRequestError("LOCAL_APP_INVALID_JSON", "malformed UTF-8 JSON"))
            return
        try:
            response = self.application.resolve_payload(payload)
        except LocalAppRequestError as exc:
            self._send_error_payload(exc)
            return
        self._send_json(200, response)


def handler_for(application: LocalZiweiApplication):
    class Handler(_LocalAppHandler):
        pass

    Handler.application = application
    return Handler


def build_server(repository_root: Path, *, port: int = DEFAULT_PORT) -> HTTPServer:
    if not 0 <= port <= 65535:
        raise ValueError("port must be in [0, 65535]")
    application = LocalZiweiApplication(repository_root)
    return HTTPServer((DEFAULT_HOST, port), handler_for(application))


def _default_repository_root() -> Path:
    source_root = Path(__file__).resolve().parents[3]
    if (source_root / "config" / "time-calendar-policies.json").is_file():
        return source_root
    return Path.cwd()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the local-only Ziwei browser application")
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=_default_repository_root(),
        help="repository root containing config/ and sources/",
    )
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="loopback port (default: 8765)")
    parser.add_argument("--no-browser", action="store_true", help="do not open the default browser automatically")
    args = parser.parse_args(argv)

    server = build_server(args.repository_root, port=args.port)
    host, port = server.server_address[:2]
    url = f"http://{host}:{port}/"
    print(f"Ziwei local app: {url}")
    print("Bind policy: 127.0.0.1 only. Press Ctrl+C to stop.")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
