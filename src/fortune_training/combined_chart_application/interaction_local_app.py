from __future__ import annotations

import argparse
import json
import webbrowser
from http.server import HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fortune_training.calendar_foundation import BirthInput
from fortune_training.calendar_foundation.models import json_value
from fortune_training.ziwei_application import (
    ApplicationBirthRequest,
    SanheInteractionRequest,
    SanheInteractionResolutionError,
    ZiweiChartService,
    ZiweiSanheInteractionService,
)
from fortune_training.ziwei_chart import Sex

from .interaction_assets import INTERACTION_CSS, INTERACTION_JS, interaction_index_html
from .local_app import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    INDEX_HTML,
    MAX_REQUEST_BYTES,
    LocalCombinedAppRequestError,
    LocalCombinedChartApplication,
    _Handler,
    _bounded_int,
    _finite_float,
    _optional_int,
    _optional_text,
    _parse_datetime,
    _parse_precision,
    _required_text,
)


LOCAL_ZIWEI_INTERACTION_SCHEMA = (
    "ZIWEI-BAZI-COMBINED-LOCAL-ZIWEI-SANHE-INTERACTION-R1"
)


class InteractionLocalCombinedChartApplication(LocalCombinedChartApplication):
    """Additive Sanhe browser sidecar over the frozen combined local application."""

    def __init__(self, repository_root: Path) -> None:
        super().__init__(repository_root)
        self.ziwei_service = ZiweiChartService(
            self.service.ziwei_foundation,
            self.ziwei_application_profile,
        )
        self.ziwei_interaction_service = ZiweiSanheInteractionService(
            self.ziwei_service
        )

    @staticmethod
    def _normalize_ziwei_sex(value: str) -> Sex:
        normalized = value.strip().upper()
        normalized = {"男": "MALE", "女": "FEMALE", "M": "MALE", "F": "FEMALE"}.get(
            normalized,
            normalized,
        )
        if normalized not in {"MALE", "FEMALE"}:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_INPUT",
                "sex must be MALE or FEMALE",
            )
        return Sex(normalized)

    def _ziwei_application_request_from_payload(
        self,
        payload: dict[str, Any],
    ) -> ApplicationBirthRequest:
        birth_datetime = _parse_datetime(
            _required_text(payload, "birth_datetime", max_length=64)
        )
        birth_place = _required_text(payload, "birth_place", max_length=160)
        latitude = _finite_float(payload, "latitude")
        longitude = _finite_float(payload, "longitude")
        if not -90.0 <= latitude <= 90.0:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_INPUT",
                "latitude must be in [-90, 90]",
            )
        if not -180.0 <= longitude <= 180.0:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_INPUT",
                "longitude must be in [-180, 180]",
            )
        timezone_id = _required_text(payload, "timezone_id", max_length=120)
        try:
            ZoneInfo(timezone_id)
        except ZoneInfoNotFoundError as exc:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_TIMEZONE",
                timezone_id,
            ) from exc

        birth = BirthInput(
            reported_local_datetime=birth_datetime,
            birth_place=birth_place,
            latitude=latitude,
            longitude=longitude,
            timezone_id=timezone_id,
            precision=_parse_precision(
                _required_text(payload, "precision", max_length=32)
            ),
            uncertainty_seconds=_bounded_int(
                payload,
                "uncertainty_seconds",
                0,
                86400,
            ),
        )
        return ApplicationBirthRequest(
            birth=birth,
            sex=self._normalize_ziwei_sex(
                _required_text(payload, "sex", max_length=16)
            ),
            calculation_profile=self.ziwei_calculation_profile,
            presentation_profile=self.ziwei_presentation_profile,
            daxian_frame_id=_optional_text(
                payload,
                "ziwei_daxian_frame_id",
                80,
            ),
            annual_year=_optional_int(payload, "ziwei_annual_year", 1, 9999),
            minor_limit_age=_optional_int(
                payload,
                "ziwei_minor_limit_age",
                1,
                200,
            ),
            daxian_count=_bounded_int(payload, "ziwei_daxian_count", 1, 20),
        )

    @staticmethod
    def _origin_options(bundle) -> list[dict[str, Any]]:
        rows = sorted(bundle.view_model.cells, key=lambda row: row.address_index)
        if len(rows) != 12:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_INTERACTION_ORIGIN_DOMAIN_INVALID",
                f"expected 12 palace cells, found {len(rows)}",
                status=500,
            )
        addresses = {row.address_index for row in rows}
        designation_ids = {row.natal_designation_id for row in rows}
        if addresses != set(range(12)) or len(designation_ids) != 12:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_INTERACTION_ORIGIN_DOMAIN_INVALID",
                "palace address/designation domain is not one-to-one and complete",
                status=500,
            )
        return [
            {
                "address_index": row.address_index,
                "branch": row.branch,
                "designation_id": row.natal_designation_id,
                "designation_label": row.natal_designation_label,
            }
            for row in rows
        ]

    @staticmethod
    def _temporal_options(bundle) -> dict[str, Any]:
        return {
            "daxian": [
                {
                    "frame_id": row.frame_id,
                    "index": row.index,
                    "nominal_age_start": row.nominal_age_start,
                    "nominal_age_end": row.nominal_age_end,
                    "absolute_year_start": row.absolute_year_start,
                    "absolute_year_end": row.absolute_year_end,
                    "active_address": json_value(row.active_address),
                    "active_palace_ganzhi": row.active_palace_ganzhi,
                }
                for row in bundle.temporal_state.daxian_frames
            ],
            "annual": [
                {
                    "frame_id": row.frame_id,
                    "absolute_year": row.absolute_year,
                    "nominal_age": row.nominal_age,
                    "year_stem": row.year_stem,
                    "year_branch": row.year_branch,
                    "active_address": json_value(row.active_address),
                    "active_palace_ganzhi": row.active_palace_ganzhi,
                    "parent_daxian_frame_id": row.parent_daxian_frame_id,
                }
                for row in bundle.temporal_state.annual_frames
            ],
            "minor_limit": [
                {
                    "frame_id": row.frame_id,
                    "nominal_age": row.nominal_age,
                    "active_address": json_value(row.active_address),
                }
                for row in bundle.temporal_state.minor_limit_frames
            ],
        }

    def resolve_ziwei_interaction_payload(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_JSON",
                "request body must be a JSON object",
            )
        origin_designation_id = _required_text(
            payload,
            "ziwei_origin_designation_id",
            max_length=80,
        )
        base_payload = dict(payload)
        base_payload.pop("ziwei_origin_designation_id", None)

        # First replay the frozen combined boundary. This preserves all existing
        # input/profile validation and establishes the authoritative Ziwei bundle
        # identity the sidecar must match.
        combined_response = self.resolve_payload(base_payload)
        combined_resolution = combined_response["combined_resolution"]
        source_ziwei = combined_resolution.get("ziwei_bundle")
        if source_ziwei is None:
            error = combined_resolution.get("ziwei_error") or {}
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_INTERACTION_SOURCE_UNAVAILABLE",
                str(error.get("detail") or "combined resolution has no Ziwei bundle"),
                status=422,
            )
        expected_ziwei_hash = source_ziwei["bundle_hash"]

        request = self._ziwei_application_request_from_payload(base_payload)
        try:
            bundle, interaction = self.ziwei_interaction_service.resolve_with_bundle(
                SanheInteractionRequest(
                    application_request=request,
                    origin_designation_id=origin_designation_id,
                )
            )
        except SanheInteractionResolutionError as exc:
            raise LocalCombinedAppRequestError(
                exc.code,
                exc.detail,
                status=422,
            ) from exc
        except ValueError as exc:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_INTERACTION_FAILED",
                str(exc),
                status=422,
            ) from exc

        if (
            bundle.bundle_hash != expected_ziwei_hash
            or interaction.source_application_bundle_hash != expected_ziwei_hash
        ):
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_INTERACTION_SOURCE_BINDING_MISMATCH",
                (
                    f"combined={expected_ziwei_hash};controller_bundle={bundle.bundle_hash};"
                    f"controller_source={interaction.source_application_bundle_hash}"
                ),
                status=500,
            )

        source_bazi = combined_resolution.get("bazi_bundle")
        return {
            "schema": LOCAL_ZIWEI_INTERACTION_SCHEMA,
            "source_combined_manifest_hash": combined_resolution["manifest_hash"],
            "source_ziwei_bundle_hash": expected_ziwei_hash,
            "source_bazi_bundle_hash": (
                source_bazi["bundle_hash"] if source_bazi is not None else None
            ),
            "interaction": json_value(interaction),
            "origin_options": self._origin_options(bundle),
            "temporal_options": self._temporal_options(bundle),
            "ziwei_svg": self.renderer.render(
                bundle.view_model,
                self.renderer_profile,
            ).svg,
        }


class _InteractionHandler(_Handler):
    application: InteractionLocalCombinedChartApplication
    server_version = "CombinedChartInteractionLocalApp/1.0"

    def do_GET(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path
        if path == "/":
            self._send_bytes(
                200,
                "text/html; charset=utf-8",
                interaction_index_html(INDEX_HTML).encode(),
            )
            return
        if path == "/interaction.css":
            self._send_bytes(
                200,
                "text/css; charset=utf-8",
                INTERACTION_CSS.encode(),
            )
            return
        if path == "/interaction.js":
            self._send_bytes(
                200,
                "application/javascript; charset=utf-8",
                INTERACTION_JS.encode(),
            )
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        if urlsplit(self.path).path != "/api/ziwei-interaction":
            super().do_POST()
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
                    "LOCAL_APP_INVALID_CONTENT_LENGTH",
                    "invalid Content-Length",
                )
            )
            return
        if length <= 0:
            self._error(
                LocalCombinedAppRequestError(
                    "LOCAL_APP_EMPTY_BODY",
                    "request body is required",
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
                    "LOCAL_APP_INVALID_JSON",
                    "malformed UTF-8 JSON",
                )
            )
            return
        try:
            response = self.application.resolve_ziwei_interaction_payload(payload)
        except LocalCombinedAppRequestError as exc:
            self._error(exc)
            return
        self._send_json(200, response)


def interaction_handler_for(application: InteractionLocalCombinedChartApplication):
    class Handler(_InteractionHandler):
        pass

    Handler.application = application
    return Handler


def build_interaction_server(
    repository_root: Path,
    *,
    port: int = DEFAULT_PORT,
) -> HTTPServer:
    if not 0 <= port <= 65535:
        raise ValueError("port must be in [0, 65535]")
    return HTTPServer(
        (DEFAULT_HOST, port),
        interaction_handler_for(InteractionLocalCombinedChartApplication(repository_root)),
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
        description="Run the local-only combined Ziwei + Bazi chart shell with Sanhe interaction"
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=_default_repository_root(),
    )
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args(argv)
    server = build_interaction_server(args.repository_root, port=args.port)
    host, port = server.server_address[:2]
    url = f"http://{host}:{port}/"
    print(f"Combined chart local app: {url}")
    print("Ziwei interaction: SANHE sidecar. Bind policy: 127.0.0.1 only.")
    print("Press Ctrl+C to stop.")
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
