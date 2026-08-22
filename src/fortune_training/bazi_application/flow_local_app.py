from __future__ import annotations

import argparse
import json
from datetime import datetime
from http.server import HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fortune_training.bazi_chart import (
    ZI_START_23_PROFILE_ID,
    bazi_foundation_zi_start_23_r1_profile,
    build_production_bazi_profile,
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
from fortune_training.calendar_foundation import BirthInput
from fortune_training.calendar_foundation.models import json_value

from .flow_models import BaziApplicationFlowRequest
from .flow_service import BaziApplicationFlowService
from .local_app import (
    LOCAL_APP_ERROR_SCHEMA,
    MAX_REQUEST_BYTES,
    LocalAppRequestError,
    LocalBaziApplication,
    _Handler,
    _bounded_int,
    _finite_float,
    _parse_datetime,
    _parse_precision,
    _parse_sex,
    _required_text,
)
from .models import BaziApplicationRequest
from .profile import APPLICATION_PROFILE_ID, bazi_local_application_v1_profile
from .service import BaziApplicationResolutionError


FLOW_LOCAL_APP_ID = "BAZI-LOCAL-BROWSER-FLOW-APP-R1"
FLOW_LOCAL_APP_VERSION = "1.0.0"
FLOW_LOCAL_APP_HEALTH_SCHEMA = "BAZI-LOCAL-APP-FLOW-HEALTH-R1"
FLOW_LOCAL_APP_RESOLVE_SCHEMA = "BAZI-LOCAL-APP-FLOW-RESOLVE-R1"
FLOW_DEFAULT_PORT = 8768


class FlowLocalBaziApplication(LocalBaziApplication):
    def __init__(self, repository_root: Path) -> None:
        super().__init__(repository_root)
        self.flow_service = BaziApplicationFlowService(self.service)

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
            raise LocalAppRequestError(
                "LOCAL_APP_INVALID_INPUT",
                "target_datetime must be ISO local datetime",
            ) from exc
        if parsed.tzinfo is not None:
            raise LocalAppRequestError(
                "LOCAL_APP_INVALID_INPUT",
                "target_datetime must be a naive local wall-clock value",
            )
        return parsed

    def resolve_flow_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise LocalAppRequestError(
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
            raise LocalAppRequestError(
                "LOCAL_APP_INVALID_TIMEZONE", timezone_id
            ) from exc

        target_datetime = self._target_datetime(payload)
        target_place = _required_text(payload, "target_place", max_length=160)
        target_latitude = _finite_float(payload, "target_latitude")
        target_longitude = _finite_float(payload, "target_longitude")
        target_timezone_id = _required_text(
            payload, "target_timezone_id", max_length=120
        )
        try:
            ZoneInfo(target_timezone_id)
        except ZoneInfoNotFoundError as exc:
            raise LocalAppRequestError(
                "LOCAL_APP_INVALID_TARGET_TIMEZONE", target_timezone_id
            ) from exc

        sex = _parse_sex(_required_text(payload, "sex", max_length=16))
        precision = _parse_precision(
            _required_text(payload, "precision", max_length=32)
        )
        uncertainty_seconds = _bounded_int(
            payload, "uncertainty_seconds", 0, 86400
        )
        target_precision = _parse_precision(
            _required_text(payload, "target_precision", max_length=32)
        )
        target_uncertainty_seconds = _bounded_int(
            payload, "target_uncertainty_seconds", 0, 86400
        )
        dayun_count = _bounded_int(payload, "dayun_count", 1, 20)

        natal_profile_id = _required_text(
            payload, "natal_profile_id", max_length=80
        )
        temporal_profile_id = _required_text(
            payload, "temporal_profile_id", max_length=100
        )
        target_temporal_profile_id = _required_text(
            payload, "target_temporal_profile_id", max_length=100
        )
        application_profile_id = _required_text(
            payload, "application_profile_id", max_length=80
        )

        natal_profiles = {
            "BAZI-FOUNDATION-V1-R1": build_production_bazi_profile,
            ZI_START_23_PROFILE_ID: bazi_foundation_zi_start_23_r1_profile,
        }
        natal_factory = natal_profiles.get(natal_profile_id)
        if natal_factory is None:
            raise LocalAppRequestError(
                "LOCAL_APP_UNSUPPORTED_NATAL_PROFILE", natal_profile_id
            )
        temporal_profiles = {
            "BAZI-TEMPORAL-V1-CONTINUOUS-R1": (
                bazi_temporal_v1_continuous_profile
            ),
            "BAZI-TEMPORAL-WENZHEN-CHINA-COMPATIBILITY-R1": (
                bazi_temporal_wenzhen_china_compatibility_r1_profile
            ),
        }
        temporal_factory = temporal_profiles.get(temporal_profile_id)
        if temporal_factory is None:
            raise LocalAppRequestError(
                "LOCAL_APP_UNSUPPORTED_TEMPORAL_PROFILE", temporal_profile_id
            )
        if target_temporal_profile_id != TARGET_TEMPORAL_PROFILE_ID:
            raise LocalAppRequestError(
                "LOCAL_APP_UNSUPPORTED_TARGET_TEMPORAL_PROFILE",
                target_temporal_profile_id,
            )
        if application_profile_id != APPLICATION_PROFILE_ID:
            raise LocalAppRequestError(
                "LOCAL_APP_UNSUPPORTED_APPLICATION_PROFILE",
                application_profile_id,
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
            base_request = BaziApplicationRequest(
                birth=birth,
                sex=sex,
                natal_profile=natal_factory(self.registry),
                temporal_profile=temporal_factory(),
                application_profile=bazi_local_application_v1_profile(),
                dayun_count=dayun_count,
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
            flow_request = BaziApplicationFlowRequest(
                application_request=base_request,
                target_input=target_input,
                target_coordinate_profile=(
                    bazi_target_temporal_coordinate_r1_profile()
                ),
            )
            base_bundle, target_flow_bundle = self.flow_service.resolve_with_base(
                flow_request
            )
        except BaziApplicationResolutionError as exc:
            raise LocalAppRequestError(exc.code, exc.detail, status=422) from exc
        except ValueError as exc:
            raise LocalAppRequestError(
                "LOCAL_APP_FLOW_RESOLUTION_FAILED", str(exc), status=422
            ) from exc

        return {
            "schema": FLOW_LOCAL_APP_RESOLVE_SCHEMA,
            "application_bundle": json_value(base_bundle),
            "target_flow_bundle": json_value(target_flow_bundle),
        }


class _FlowHandler(_Handler):
    application: FlowLocalBaziApplication

    def do_POST(self) -> None:  # noqa: N802
        if urlsplit(self.path).path != "/api/resolve-flow":
            super().do_POST()
            return
        if (
            self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
            != "application/json"
        ):
            self._error(
                LocalAppRequestError(
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
                LocalAppRequestError(
                    "LOCAL_APP_INVALID_CONTENT_LENGTH", "invalid Content-Length"
                )
            )
            return
        if length <= 0:
            self._error(
                LocalAppRequestError(
                    "LOCAL_APP_EMPTY_BODY", "request body is required"
                )
            )
            return
        if length > MAX_REQUEST_BYTES:
            self._error(
                LocalAppRequestError(
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
                LocalAppRequestError(
                    "LOCAL_APP_INVALID_JSON", "malformed UTF-8 JSON"
                )
            )
            return
        try:
            response = self.application.resolve_flow_payload(payload)
        except LocalAppRequestError as exc:
            self._error(exc)
            return
        self._send_json(200, response)


def flow_handler_for(application: FlowLocalBaziApplication):
    class Handler(_FlowHandler):
        pass

    Handler.application = application
    return Handler


def build_flow_server(
    repository_root: Path, *, port: int = FLOW_DEFAULT_PORT
) -> HTTPServer:
    if not 0 <= port <= 65535:
        raise ValueError("port must be in [0, 65535]")
    from .local_app import DEFAULT_HOST

    return HTTPServer(
        (DEFAULT_HOST, port),
        flow_handler_for(FlowLocalBaziApplication(repository_root)),
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
        description="Run the local-only Bazi target-flow API application"
    )
    parser.add_argument(
        "--repository-root", type=Path, default=_default_repository_root()
    )
    parser.add_argument("--port", type=int, default=FLOW_DEFAULT_PORT)
    args = parser.parse_args(argv)
    server = build_flow_server(args.repository_root, port=args.port)
    host, port = server.server_address[:2]
    print(f"Bazi target-flow local app: http://{host}:{port}/")
    print(f"Target-flow endpoint: http://{host}:{port}/api/resolve-flow")
    print("Legacy resolve endpoint remains available at /api/resolve on this server.")
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
