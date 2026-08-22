from __future__ import annotations

import argparse
import json
import math
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fortune_training.bazi_application import bazi_local_application_v1_profile
from fortune_training.bazi_chart import (
    ZI_START_23_PROFILE_ID,
    bazi_foundation_zi_start_23_r1_profile,
    build_production_bazi_profile,
)
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
from fortune_training.ziwei_chart import build_production_ziwei_profile

from .local_app_assets import APP_JS, INDEX_HTML, STYLE_CSS
from .location_catalog import OfflineLocationCatalog
from .models import CombinedChartApplicationRequest
from .profile import COMBINED_PROFILE_ID, combined_chart_application_v1_profile
from .service import CombinedApplicationResolutionError, CombinedChartService


LOCAL_APP_ID = "ZIWEI-BAZI-COMBINED-LOCAL-BROWSER-APP-V1"
LOCAL_APP_VERSION = "1.1.0"
LOCAL_APP_HEALTH_SCHEMA = "ZIWEI-BAZI-COMBINED-LOCAL-APP-HEALTH-V1"
LOCAL_APP_RESOLVE_SCHEMA = "ZIWEI-BAZI-COMBINED-LOCAL-APP-RESOLVE-V1"
LOCAL_APP_LOCATION_SEARCH_SCHEMA = "ZIWEI-BAZI-COMBINED-LOCAL-LOCATION-SEARCH-V1"
LOCAL_APP_LOCATION_SELECTION_SCHEMA = "ZIWEI-BAZI-COMBINED-LOCAL-LOCATION-SELECTION-V1"
LOCAL_APP_ERROR_SCHEMA = "ZIWEI-BAZI-COMBINED-LOCAL-APP-ERROR-V1"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8767
MAX_REQUEST_BYTES = 96 * 1024

CSP = (
    "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
    "connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; "
    "form-action 'self'"
)


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
        raise LocalCombinedAppRequestError(
            "LOCAL_APP_INVALID_INPUT",
            f"{key} must be an integer in [{minimum}, {maximum}]",
        )
    return value


def _optional_int(
    payload: dict[str, Any], key: str, minimum: int, maximum: int
) -> int | None:
    value = payload.get(key)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= maximum:
        raise LocalCombinedAppRequestError(
            "LOCAL_APP_INVALID_INPUT",
            f"{key} must be null or an integer in [{minimum}, {maximum}]",
        )
    return value


def _optional_text(payload: dict[str, Any], key: str, max_length: int) -> str | None:
    value = payload.get(key)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip() or len(value.strip()) > max_length:
        raise LocalCombinedAppRequestError(
            "LOCAL_APP_INVALID_INPUT",
            f"{key} must be null or non-empty text",
        )
    return value.strip()


def _parse_datetime(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise LocalCombinedAppRequestError(
            "LOCAL_APP_INVALID_INPUT",
            "birth_datetime must be ISO local datetime",
        ) from exc
    if parsed.tzinfo is not None:
        raise LocalCombinedAppRequestError(
            "LOCAL_APP_INVALID_INPUT",
            "birth_datetime must be a naive local wall-clock value",
        )
    return parsed


def _parse_precision(value: str) -> TimePrecision:
    try:
        return TimePrecision(value.strip().upper())
    except ValueError as exc:
        raise LocalCombinedAppRequestError(
            "LOCAL_APP_INVALID_INPUT", "unsupported precision"
        ) from exc


class LocalCombinedChartApplication:
    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root.resolve()
        registry_path = self.repository_root / "config" / "time-calendar-policies.json"
        if not registry_path.is_file():
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_REPOSITORY_ROOT_INVALID",
                f"missing {registry_path}",
                status=500,
            )
        self.registry = PolicyRegistry.from_file(registry_path)
        self.ziwei_calculation_profile = build_production_ziwei_profile(self.registry)
        self.ziwei_application_profile = ziwei_application_v1_profile()
        self.ziwei_presentation_profile = ziwei_application_default_presentation_profile()
        self.bazi_natal_profile = build_production_bazi_profile(self.registry)
        self.bazi_natal_profiles = {
            self.bazi_natal_profile.profile_id: build_production_bazi_profile,
            ZI_START_23_PROFILE_ID: bazi_foundation_zi_start_23_r1_profile,
        }
        self.bazi_application_profile = bazi_local_application_v1_profile()
        self.combined_profile = combined_chart_application_v1_profile()
        self.service = CombinedChartService.from_repository(self.repository_root)
        self.renderer = ZiweiTwelvePalaceSvgRenderer()
        self.renderer_profile = SvgRendererProfile()
        self.location_catalog = OfflineLocationCatalog()

    def profile_metadata(self) -> dict[str, Any]:
        return {
            "schema": "ZIWEI-BAZI-COMBINED-LOCAL-PROFILES-V1",
            "profiles": {
                "combined": self.combined_profile.profile_id,
                "ziwei_calculation": self.ziwei_calculation_profile.profile_id,
                "ziwei_application": self.ziwei_application_profile.profile_id,
                "ziwei_presentation": self.ziwei_presentation_profile.profile_id,
                "bazi_natal": self.bazi_natal_profile.profile_id,
                "bazi_natal_options": (
                    "BAZI-FOUNDATION-V1-R1 | BAZI-FOUNDATION-ZI-START-23-R1"
                ),
                "bazi_application": self.bazi_application_profile.profile_id,
                "bazi_temporal_options": (
                    "BAZI-TEMPORAL-V1-CONTINUOUS-R1 | "
                    "BAZI-TEMPORAL-WENZHEN-CHINA-COMPATIBILITY-R1"
                ),
            },
            "location_catalog": self.location_catalog.metadata(),
        }

    def health(self) -> dict[str, Any]:
        return {
            "schema": LOCAL_APP_HEALTH_SCHEMA,
            "status": "ok",
            "application_id": LOCAL_APP_ID,
            "application_version": LOCAL_APP_VERSION,
            "bind_policy": "LOOPBACK_ONLY",
            "location_lookup_network_access": False,
        }

    def search_locations(self, query: str, *, limit: int = 12) -> dict[str, Any]:
        try:
            rows = self.location_catalog.search(query, limit=limit)
        except ValueError as exc:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_LOCATION_SEARCH", str(exc)
            ) from exc
        return {
            "schema": LOCAL_APP_LOCATION_SEARCH_SCHEMA,
            "query": query,
            "catalog": self.location_catalog.metadata(),
            "results": [row.json_dict() for row in rows],
        }

    def _validate_location_selection(
        self,
        selection_id: str | None,
        *,
        birth_place: str,
        latitude: float,
        longitude: float,
        timezone_id: str,
    ) -> dict[str, Any]:
        if selection_id is None:
            return {
                "schema": LOCAL_APP_LOCATION_SELECTION_SCHEMA,
                "mode": "MANUAL",
                "selection_id": None,
                "record": None,
            }
        row = self.location_catalog.get(selection_id)
        if row is None:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_LOCATION_SELECTION_UNKNOWN", selection_id
            )
        mismatch = (
            birth_place != row.birth_place
            or not math.isclose(latitude, row.latitude, rel_tol=0.0, abs_tol=1e-9)
            or not math.isclose(longitude, row.longitude, rel_tol=0.0, abs_tol=1e-9)
            or timezone_id != row.timezone_id
        )
        if mismatch:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_LOCATION_SELECTION_MISMATCH",
                "linked birth_place/latitude/longitude/timezone_id no longer match the selected location",
            )
        return {
            "schema": LOCAL_APP_LOCATION_SELECTION_SCHEMA,
            "mode": "LINKED",
            "selection_id": row.selection_id,
            "record": row.json_dict(),
        }

    def resolve_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_JSON", "request body must be a JSON object"
            )
        birth_datetime = _parse_datetime(
            _required_text(payload, "birth_datetime", max_length=64)
        )
        birth_place = _required_text(payload, "birth_place", max_length=160)
        latitude = _finite_float(payload, "latitude")
        longitude = _finite_float(payload, "longitude")
        timezone_id = _required_text(payload, "timezone_id", max_length=120)
        try:
            ZoneInfo(timezone_id)
        except ZoneInfoNotFoundError as exc:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_TIMEZONE", timezone_id
            ) from exc
        selection_id = _optional_text(payload, "location_selection_id", 120)
        location_selection = self._validate_location_selection(
            selection_id,
            birth_place=birth_place,
            latitude=latitude,
            longitude=longitude,
            timezone_id=timezone_id,
        )

        sex = _required_text(payload, "sex", max_length=16).upper()
        if sex not in {"MALE", "FEMALE", "M", "F", "男", "女"}:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_INPUT", "sex must be MALE or FEMALE"
            )
        precision = _parse_precision(
            _required_text(payload, "precision", max_length=32)
        )
        uncertainty_seconds = _bounded_int(payload, "uncertainty_seconds", 0, 86400)
        ziwei_daxian_count = _bounded_int(payload, "ziwei_daxian_count", 1, 20)
        bazi_dayun_count = _bounded_int(payload, "bazi_dayun_count", 1, 20)
        ziwei_daxian_frame_id = _optional_text(payload, "ziwei_daxian_frame_id", 80)
        ziwei_annual_year = _optional_int(payload, "ziwei_annual_year", 1, 9999)
        ziwei_lunar_month = _optional_int(payload, "ziwei_lunar_month", 1, 12)
        if ziwei_lunar_month is not None and ziwei_annual_year is None:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_INPUT", "ziwei_lunar_month requires ziwei_annual_year"
            )
        ziwei_minor_limit_age = _optional_int(payload, "ziwei_minor_limit_age", 1, 200)
        combined_profile_id = _required_text(
            payload, "combined_profile_id", max_length=100
        )
        if combined_profile_id != COMBINED_PROFILE_ID:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_UNSUPPORTED_COMBINED_PROFILE", combined_profile_id
            )

        natal_id = payload.get("bazi_natal_profile_id", self.bazi_natal_profile.profile_id)
        if not isinstance(natal_id, str) or not natal_id.strip():
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_INPUT",
                "bazi_natal_profile_id must be non-empty text",
            )
        natal_factory = self.bazi_natal_profiles.get(natal_id.strip())
        if natal_factory is None:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_UNSUPPORTED_BAZI_NATAL_PROFILE", natal_id.strip()
            )

        temporal_id = _required_text(
            payload, "bazi_temporal_profile_id", max_length=120
        )
        temporal_factories = {
            "BAZI-TEMPORAL-V1-CONTINUOUS-R1": bazi_temporal_v1_continuous_profile,
            "BAZI-TEMPORAL-WENZHEN-CHINA-COMPATIBILITY-R1": (
                bazi_temporal_wenzhen_china_compatibility_r1_profile
            ),
        }
        factory = temporal_factories.get(temporal_id)
        if factory is None:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_UNSUPPORTED_BAZI_TEMPORAL_PROFILE", temporal_id
            )

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
            request = CombinedChartApplicationRequest(
                birth=birth,
                sex=sex,
                ziwei_calculation_profile=self.ziwei_calculation_profile,
                bazi_natal_profile=natal_factory(self.registry),
                bazi_temporal_profile=factory(),
                combined_profile=self.combined_profile,
                ziwei_application_profile=self.ziwei_application_profile,
                ziwei_presentation_profile=self.ziwei_presentation_profile,
                bazi_application_profile=self.bazi_application_profile,
                ziwei_daxian_frame_id=ziwei_daxian_frame_id,
                ziwei_annual_year=ziwei_annual_year,
                ziwei_lunar_month=ziwei_lunar_month,
                ziwei_minor_limit_age=ziwei_minor_limit_age,
                ziwei_daxian_count=ziwei_daxian_count,
                bazi_dayun_count=bazi_dayun_count,
            )
            resolution = self.service.resolve(request)
            export = self.service.export(resolution)
            ziwei_svg = None
            if resolution.ziwei_bundle is not None:
                ziwei_svg = self.renderer.render(
                    resolution.ziwei_bundle.view_model, self.renderer_profile
                ).svg
        except CombinedApplicationResolutionError as exc:
            raise LocalCombinedAppRequestError(exc.code, exc.detail, status=422) from exc
        except ValueError as exc:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_RESOLUTION_FAILED", str(exc), status=422
            ) from exc

        return {
            "schema": LOCAL_APP_RESOLVE_SCHEMA,
            "location_selection": location_selection,
            "combined_resolution": json_value(resolution),
            "combined_export": export,
            "ziwei_svg": ziwei_svg,
        }


class _Handler(BaseHTTPRequestHandler):
    application: LocalCombinedChartApplication
    server_version = "CombinedChartLocalApp/1.1"
    sys_version = ""

    def log_message(self, format: str, *args: object) -> None:
        return

    def _headers(self) -> None:
        self.send_header("Content-Security-Policy", CSP)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cache-Control", "no-store")

    def _send_bytes(self, status: int, content_type: str, payload: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self._headers()
        self.end_headers()
        self.wfile.write(payload)

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        self._send_bytes(
            status,
            "application/json; charset=utf-8",
            json.dumps(
                payload,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode(),
        )

    def _error(self, error: LocalCombinedAppRequestError) -> None:
        self._send_json(
            error.status,
            {
                "schema": LOCAL_APP_ERROR_SCHEMA,
                "error": {"code": error.code, "detail": error.detail},
            },
        )

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlsplit(self.path)
        path = parsed.path
        if path == "/":
            self._send_bytes(200, "text/html; charset=utf-8", INDEX_HTML.encode())
            return
        if path == "/style.css":
            self._send_bytes(200, "text/css; charset=utf-8", STYLE_CSS.encode())
            return
        if path == "/app.js":
            self._send_bytes(
                200, "application/javascript; charset=utf-8", APP_JS.encode()
            )
            return
        if path == "/health":
            self._send_json(200, self.application.health())
            return
        if path == "/api/profiles":
            self._send_json(200, self.application.profile_metadata())
            return
        if path == "/api/locations":
            params = parse_qs(parsed.query, keep_blank_values=True)
            query = params.get("q", [""])[0]
            raw_limit = params.get("limit", ["12"])[0]
            try:
                limit = int(raw_limit)
            except ValueError:
                self._error(
                    LocalCombinedAppRequestError(
                        "LOCAL_APP_INVALID_LOCATION_SEARCH",
                        "limit must be an integer",
                    )
                )
                return
            try:
                result = self.application.search_locations(query, limit=limit)
            except LocalCombinedAppRequestError as exc:
                self._error(exc)
                return
            self._send_json(200, result)
            return
        self._error(LocalCombinedAppRequestError("LOCAL_APP_NOT_FOUND", path, status=404))

    def do_POST(self) -> None:  # noqa: N802
        if urlsplit(self.path).path != "/api/resolve":
            self._error(
                LocalCombinedAppRequestError(
                    "LOCAL_APP_NOT_FOUND", self.path, status=404
                )
            )
            return
        if (
            self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
            != "application/json"
        ):
            self._error(
                LocalCombinedAppRequestError(
                    "LOCAL_APP_JSON_REQUIRED",
                    "Content-Type must be application/json",
                    status=415,
                )
            )
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._error(
                LocalCombinedAppRequestError(
                    "LOCAL_APP_INVALID_CONTENT_LENGTH", "invalid Content-Length"
                )
            )
            return
        if length <= 0:
            self._error(
                LocalCombinedAppRequestError(
                    "LOCAL_APP_EMPTY_BODY", "request body is required"
                )
            )
            return
        if length > MAX_REQUEST_BYTES:
            self._error(
                LocalCombinedAppRequestError(
                    "LOCAL_APP_REQUEST_TOO_LARGE",
                    "request body exceeds local limit",
                    status=413,
                )
            )
            return
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._error(
                LocalCombinedAppRequestError(
                    "LOCAL_APP_INVALID_JSON", "malformed UTF-8 JSON"
                )
            )
            return
        try:
            result = self.application.resolve_payload(payload)
        except LocalCombinedAppRequestError as exc:
            self._error(exc)
            return
        self._send_json(200, result)


def handler_for(application: LocalCombinedChartApplication):
    class Handler(_Handler):
        pass

    Handler.application = application
    return Handler


def build_server(repository_root: Path, *, port: int = DEFAULT_PORT) -> HTTPServer:
    if not 0 <= port <= 65535:
        raise ValueError("port must be in [0, 65535]")
    return HTTPServer(
        (DEFAULT_HOST, port), handler_for(LocalCombinedChartApplication(repository_root))
    )


def _default_repository_root() -> Path:
    root = Path(__file__).resolve().parents[3]
    return (
        root
        if (root / "config" / "time-calendar-policies.json").is_file()
        else Path.cwd()
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the local-only combined Ziwei + Bazi chart shell"
    )
    parser.add_argument(
        "--repository-root", type=Path, default=_default_repository_root()
    )
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args(argv)
    server = build_server(args.repository_root, port=args.port)
    host, port = server.server_address[:2]
    url = f"http://{host}:{port}/"
    print(f"Combined chart local app: {url}")
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
