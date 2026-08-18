from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fortune_training.bazi_target_temporal import (
    TargetTemporalCoordinateFoundation,
    TargetTemporalInput,
    bazi_target_temporal_coordinate_r1_profile,
)
from fortune_training.bazi_target_temporal.profile import TARGET_TEMPORAL_PROFILE_ID
from fortune_training.calendar_foundation.models import json_value

from .flow_local_app import _validate_coordinates
from .local_app import (
    MAX_REQUEST_BYTES,
    LocalCombinedAppRequestError,
    _bounded_int,
    _finite_float,
    _parse_precision,
    _required_text,
)
from .service import validate_combined_resolution
from .shared_time_service import (
    SharedZiweiSelectorProjectionError,
    SharedZiweiSelectorProjectionService,
)


LOCAL_SHARED_ZIWEI_PROJECTION_SCHEMA = (
    "ZIWEI-BAZI-COMBINED-LOCAL-SHARED-ZIWEI-PROJECTION-R1"
)


class SharedZiweiProjectionLocalMixin:
    """Loopback adapter over the released shared selector projection contract."""

    def _shared_target_input_from_payload(
        self,
        payload: dict[str, Any],
    ) -> tuple[TargetTemporalInput, object]:
        target_datetime = self._target_datetime(payload)
        target_place = _required_text(payload, "target_place", max_length=160)
        target_latitude = _finite_float(payload, "target_latitude")
        target_longitude = _finite_float(payload, "target_longitude")
        _validate_coordinates(target_latitude, target_longitude, prefix="target_")
        target_timezone_id = _required_text(
            payload,
            "target_timezone_id",
            max_length=120,
        )
        try:
            ZoneInfo(target_timezone_id)
        except ZoneInfoNotFoundError as exc:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_TARGET_TIMEZONE",
                target_timezone_id,
            ) from exc
        target_precision = _parse_precision(
            _required_text(payload, "target_precision", max_length=32)
        )
        target_uncertainty_seconds = _bounded_int(
            payload,
            "target_uncertainty_seconds",
            0,
            86400,
        )
        target_temporal_profile_id = _required_text(
            payload,
            "target_temporal_profile_id",
            max_length=120,
        )
        if target_temporal_profile_id != TARGET_TEMPORAL_PROFILE_ID:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_UNSUPPORTED_TARGET_TEMPORAL_PROFILE",
                target_temporal_profile_id,
            )
        profile = bazi_target_temporal_coordinate_r1_profile()
        return (
            TargetTemporalInput(
                reported_local_datetime=target_datetime,
                target_place=target_place,
                latitude=target_latitude,
                longitude=target_longitude,
                timezone_id=target_timezone_id,
                precision=target_precision,
                uncertainty_seconds=target_uncertainty_seconds,
            ),
            profile,
        )

    def resolve_shared_ziwei_projection_payload(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_JSON",
                "request body must be a JSON object",
            )

        combined_request, location_selection = self._combined_request_from_payload(payload)
        target_input, target_profile = self._shared_target_input_from_payload(payload)

        try:
            base = self.service.resolve(combined_request)
        except ValueError as exc:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_SHARED_ZIWEI_BASE_RESOLUTION_FAILED",
                str(exc),
                status=422,
            ) from exc
        base_report = validate_combined_resolution(base)
        if base_report.status != "PASS" or base_report != base.integrity:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_SHARED_ZIWEI_BASE_INTEGRITY_FAILED",
                ";".join(base_report.diagnostics) or base_report.status,
                status=500,
            )
        if base.ziwei_bundle is None:
            detail = base.ziwei_error.detail if base.ziwei_error is not None else base.status
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_SHARED_ZIWEI_SOURCE_UNAVAILABLE",
                detail,
                status=422,
            )

        target_foundation = TargetTemporalCoordinateFoundation()
        try:
            target_resolution = target_foundation.resolve(target_input, target_profile)
            projection = SharedZiweiSelectorProjectionService().project(
                base.ziwei_bundle,
                target_resolution,
                target_profile,
            )
        except SharedZiweiSelectorProjectionError as exc:
            raise LocalCombinedAppRequestError(exc.code, exc.detail, status=422) from exc
        except ValueError as exc:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_SHARED_ZIWEI_PROJECTION_FAILED",
                str(exc),
                status=422,
            ) from exc

        return {
            "schema": LOCAL_SHARED_ZIWEI_PROJECTION_SCHEMA,
            "location_selection": location_selection,
            "source_combined_manifest_hash": base.manifest_hash,
            "source_ziwei_bundle_hash": base.ziwei_bundle.bundle_hash,
            "target_coordinate_fact_hash": target_resolution.hashes.fact_hash,
            "target_coordinate_computation_hash": target_resolution.hashes.computation_hash,
            "projection": json_value(projection),
        }


class _SharedZiweiProjectionHandlerMixin:
    application: SharedZiweiProjectionLocalMixin

    def do_POST(self) -> None:  # noqa: N802
        if urlsplit(self.path).path != "/api/shared-ziwei-projection":
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
            response = self.application.resolve_shared_ziwei_projection_payload(payload)
        except LocalCombinedAppRequestError as exc:
            self._error(exc)
            return
        self._send_json(200, response)
