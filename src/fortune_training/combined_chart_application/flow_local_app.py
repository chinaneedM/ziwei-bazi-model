from __future__ import annotations

import argparse
import json
from datetime import datetime
from http.server import HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fortune_training.bazi_application import (
    BaziApplicationResolutionError,
)
from fortune_training.bazi_target_temporal import (
    TargetTemporalInput,
    bazi_target_temporal_coordinate_r1_profile,
)
from fortune_training.bazi_target_temporal.profile import TARGET_TEMPORAL_PROFILE_ID
from fortune_training.bazi_temporal import (
    bazi_temporal_v1_continuous_profile,
    bazi_temporal_wenzhen_china_compatibility_r1_profile,
)
from fortune_training.bazi_temporal_shensha_sidecar import (
    BaziTemporalShenshaSidecarService,
    TemporalShenshaSidecarResolutionError,
)
from fortune_training.calendar_foundation import BirthInput
from fortune_training.calendar_foundation.models import json_value

from .flow_models import CombinedTargetFlowRequest
from .flow_service import (
    CombinedTargetFlowResolutionError,
    CombinedTargetFlowService,
)
from .local_app import (
    DEFAULT_HOST,
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
from .models import CombinedChartApplicationRequest
from .profile import COMBINED_PROFILE_ID
from .service import CombinedApplicationResolutionError
from .shared_time_replay import validate_shared_ziwei_selector_full_replay
from .shared_time_service import (
    SharedZiweiSelectorProjectionError,
    SharedZiweiSelectorProjectionService,
)


FLOW_LOCAL_APP_ID = "ZIWEI-BAZI-COMBINED-LOCAL-FLOW-APP-R1"
FLOW_LOCAL_APP_VERSION = "1.0.0"
FLOW_LOCAL_APP_HEALTH_SCHEMA = "ZIWEI-BAZI-COMBINED-LOCAL-FLOW-HEALTH-R1"
FLOW_LOCAL_APP_RESOLVE_SCHEMA = "ZIWEI-BAZI-COMBINED-LOCAL-FLOW-RESOLVE-R1"
FLOW_DEFAULT_PORT = 8769


def _validate_coordinates(latitude: float, longitude: float, *, prefix: str) -> None:
    if not -90.0 <= latitude <= 90.0:
        raise LocalCombinedAppRequestError(
            "LOCAL_APP_INVALID_INPUT",
            f"{prefix}latitude must be in [-90, 90]",
        )
    if not -180.0 <= longitude <= 180.0:
        raise LocalCombinedAppRequestError(
            "LOCAL_APP_INVALID_INPUT",
            f"{prefix}longitude must be in [-180, 180]",
        )


class FlowLocalCombinedChartApplication(LocalCombinedChartApplication):
    def __init__(self, repository_root: Path) -> None:
        super().__init__(repository_root)
        self.flow_service = CombinedTargetFlowService(self.service)
        self.temporal_shensha_sidecar_service = BaziTemporalShenshaSidecarService()
        self.shared_ziwei_projection_service = SharedZiweiSelectorProjectionService()

    def health(self) -> dict[str, Any]:
        payload = super().health()
        return {
            **payload,
            "schema": FLOW_LOCAL_APP_HEALTH_SCHEMA,
            "application_id": FLOW_LOCAL_APP_ID,
            "application_version": FLOW_LOCAL_APP_VERSION,
            "target_flow_endpoint": "/api/resolve-flow",
            "legacy_resolve_endpoint": "/api/resolve",
        }

    @staticmethod
    def _target_datetime(payload: dict[str, Any]) -> datetime:
        value = _required_text(payload, "target_datetime", max_length=64)
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError as exc:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_INPUT",
                "target_datetime must be ISO local datetime",
            ) from exc
        if parsed.tzinfo is not None:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_INPUT",
                "target_datetime must be a naive local wall-clock value",
            )
        return parsed

    def _combined_request_from_payload(
        self,
        payload: dict[str, Any],
    ) -> tuple[CombinedChartApplicationRequest, dict[str, Any]]:
        birth_datetime = _parse_datetime(
            _required_text(payload, "birth_datetime", max_length=64)
        )
        birth_place = _required_text(payload, "birth_place", max_length=160)
        latitude = _finite_float(payload, "latitude")
        longitude = _finite_float(payload, "longitude")
        _validate_coordinates(latitude, longitude, prefix="")
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
        uncertainty_seconds = _bounded_int(
            payload, "uncertainty_seconds", 0, 86400
        )
        ziwei_daxian_count = _bounded_int(payload, "ziwei_daxian_count", 1, 20)
        bazi_dayun_count = _bounded_int(payload, "bazi_dayun_count", 1, 20)
        ziwei_daxian_frame_id = _optional_text(
            payload, "ziwei_daxian_frame_id", 80
        )
        ziwei_annual_year = _optional_int(payload, "ziwei_annual_year", 1, 9999)
        ziwei_minor_limit_age = _optional_int(
            payload, "ziwei_minor_limit_age", 1, 200
        )
        combined_profile_id = _required_text(
            payload, "combined_profile_id", max_length=100
        )
        if combined_profile_id != COMBINED_PROFILE_ID:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_UNSUPPORTED_COMBINED_PROFILE", combined_profile_id
            )

        natal_id = payload.get(
            "bazi_natal_profile_id", self.bazi_natal_profile.profile_id
        )
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
        temporal_factory = temporal_factories.get(temporal_id)
        if temporal_factory is None:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_UNSUPPORTED_BAZI_TEMPORAL_PROFILE", temporal_id
            )

        birth = BirthInput(
            reported_local_datetime=birth_datetime,
            birth_place=birth_place,
            latitude=latitude,
            longitude=longitude,
            timezone_id=timezone_id,
            precision=precision,
            uncertainty_seconds=uncertainty_seconds,
        )
        return (
            CombinedChartApplicationRequest(
                birth=birth,
                sex=sex,
                ziwei_calculation_profile=self.ziwei_calculation_profile,
                bazi_natal_profile=natal_factory(self.registry),
                bazi_temporal_profile=temporal_factory(),
                combined_profile=self.combined_profile,
                ziwei_application_profile=self.ziwei_application_profile,
                ziwei_presentation_profile=self.ziwei_presentation_profile,
                bazi_application_profile=self.bazi_application_profile,
                ziwei_daxian_frame_id=ziwei_daxian_frame_id,
                ziwei_annual_year=ziwei_annual_year,
                ziwei_minor_limit_age=ziwei_minor_limit_age,
                ziwei_daxian_count=ziwei_daxian_count,
                bazi_dayun_count=bazi_dayun_count,
            ),
            location_selection,
        )

    def resolve_flow_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_JSON", "request body must be a JSON object"
            )
        combined_request, location_selection = self._combined_request_from_payload(
            payload
        )

        target_datetime = self._target_datetime(payload)
        target_place = _required_text(payload, "target_place", max_length=160)
        target_latitude = _finite_float(payload, "target_latitude")
        target_longitude = _finite_float(payload, "target_longitude")
        _validate_coordinates(
            target_latitude,
            target_longitude,
            prefix="target_",
        )
        target_timezone_id = _required_text(
            payload, "target_timezone_id", max_length=120
        )
        try:
            ZoneInfo(target_timezone_id)
        except ZoneInfoNotFoundError as exc:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_TARGET_TIMEZONE", target_timezone_id
            ) from exc
        target_precision = _parse_precision(
            _required_text(payload, "target_precision", max_length=32)
        )
        target_uncertainty_seconds = _bounded_int(
            payload, "target_uncertainty_seconds", 0, 86400
        )
        target_temporal_profile_id = _required_text(
            payload, "target_temporal_profile_id", max_length=120
        )
        if target_temporal_profile_id != TARGET_TEMPORAL_PROFILE_ID:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_UNSUPPORTED_TARGET_TEMPORAL_PROFILE",
                target_temporal_profile_id,
            )

        target_input = TargetTemporalInput(
            reported_local_datetime=target_datetime,
            target_place=target_place,
            latitude=target_latitude,
            longitude=target_longitude,
            timezone_id=target_timezone_id,
            precision=target_precision,
            uncertainty_seconds=target_uncertainty_seconds,
        )
        request = CombinedTargetFlowRequest(
            combined_request=combined_request,
            target_input=target_input,
            target_coordinate_profile=bazi_target_temporal_coordinate_r1_profile(),
        )
        try:
            base, bazi_flow, combined_flow = self.flow_service.resolve_with_bundles(
                request
            )
        except CombinedTargetFlowResolutionError as exc:
            raise LocalCombinedAppRequestError(exc.code, exc.detail, status=422) from exc
        except BaziApplicationResolutionError as exc:
            raise LocalCombinedAppRequestError(exc.code, exc.detail, status=422) from exc
        except CombinedApplicationResolutionError as exc:
            raise LocalCombinedAppRequestError(exc.code, exc.detail, status=422) from exc
        except ValueError as exc:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_FLOW_RESOLUTION_FAILED", str(exc), status=422
            ) from exc

        if base.bazi_bundle is None:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_TEMPORAL_SHENSHA_BASE_BUNDLE_MISSING",
                "combined target-flow resolution did not retain the Bazi base bundle",
                status=422,
            )
        try:
            temporal_shensha_sidecar = self.temporal_shensha_sidecar_service.resolve(
                base.bazi_bundle,
                bazi_flow,
            )
        except TemporalShenshaSidecarResolutionError as exc:
            raise LocalCombinedAppRequestError(exc.code, exc.detail, status=422) from exc

        if base.ziwei_bundle is None:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_SHARED_ZIWEI_SOURCE_UNAVAILABLE",
                "combined target-flow resolution did not retain the Ziwei base bundle",
                status=422,
            )
        target_profile = request.target_coordinate_profile.validate()
        target_foundation = self.flow_service.bazi_flow_service.target_foundation
        try:
            target_resolution = target_foundation.resolve(target_input, target_profile)
            if (
                target_resolution.hashes.fact_hash
                != bazi_flow.target_coordinate_fact_hash
                or target_resolution.hashes.computation_hash
                != bazi_flow.target_coordinate_computation_hash
            ):
                raise LocalCombinedAppRequestError(
                    "LOCAL_APP_SHARED_ZIWEI_TARGET_COORDINATE_MISMATCH",
                    (
                        f"bazi={bazi_flow.target_coordinate_fact_hash}:"
                        f"{bazi_flow.target_coordinate_computation_hash};"
                        f"ziwei={target_resolution.hashes.fact_hash}:"
                        f"{target_resolution.hashes.computation_hash}"
                    ),
                    status=422,
                )
            shared_ziwei_projection = self.shared_ziwei_projection_service.project(
                base.ziwei_bundle,
                target_resolution,
                target_profile,
            )
            replay = validate_shared_ziwei_selector_full_replay(
                self.shared_ziwei_projection_service,
                base.ziwei_bundle,
                target_resolution,
                target_profile,
                shared_ziwei_projection,
            )
            if replay.status != "PASS":
                raise LocalCombinedAppRequestError(
                    "LOCAL_APP_SHARED_ZIWEI_FULL_REPLAY_FAILED",
                    ";".join(replay.diagnostics) or replay.status,
                    status=422,
                )
        except LocalCombinedAppRequestError:
            raise
        except SharedZiweiSelectorProjectionError as exc:
            raise LocalCombinedAppRequestError(exc.code, exc.detail, status=422) from exc
        except ValueError as exc:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_SHARED_ZIWEI_PROJECTION_FAILED",
                str(exc),
                status=422,
            ) from exc

        return {
            "schema": FLOW_LOCAL_APP_RESOLVE_SCHEMA,
            "location_selection": location_selection,
            "combined_resolution": json_value(base),
            "bazi_target_flow_bundle": json_value(bazi_flow),
            "bazi_temporal_shensha_projection_bundle": json_value(
                temporal_shensha_sidecar
            ),
            "shared_ziwei_selector_projection": json_value(
                shared_ziwei_projection
            ),
            "combined_target_flow_resolution": json_value(combined_flow),
        }


class _FlowHandler(_Handler):
    application: FlowLocalCombinedChartApplication

    def do_POST(self) -> None:  # noqa: N802
        if urlsplit(self.path).path != "/api/resolve-flow":
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
            response = self.application.resolve_flow_payload(payload)
        except LocalCombinedAppRequestError as exc:
            self._error(exc)
            return
        self._send_json(200, response)


def flow_handler_for(application: FlowLocalCombinedChartApplication):
    class Handler(_FlowHandler):
        pass

    Handler.application = application
    return Handler


def build_flow_server(
    repository_root: Path, *, port: int = FLOW_DEFAULT_PORT
) -> HTTPServer:
    if not 0 <= port <= 65535:
        raise ValueError("port must be in [0, 65535]")
    return HTTPServer(
        (DEFAULT_HOST, port),
        flow_handler_for(FlowLocalCombinedChartApplication(repository_root)),
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
        description="Run the local-only combined Ziwei + Bazi target-flow API"
    )
    parser.add_argument(
        "--repository-root", type=Path, default=_default_repository_root()
    )
    parser.add_argument("--port", type=int, default=FLOW_DEFAULT_PORT)
    args = parser.parse_args(argv)
    server = build_flow_server(args.repository_root, port=args.port)
    host, port = server.server_address[:2]
    print(f"Combined target-flow local app: http://{host}:{port}/")
    print(f"Target-flow endpoint: http://{host}:{port}/api/resolve-flow")
    print("Legacy combined resolve remains available at /api/resolve.")
    print("Bind policy: 127.0.0.1 only. Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
