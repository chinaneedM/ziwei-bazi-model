from __future__ import annotations

import json
from dataclasses import replace
from typing import Any
from urllib.parse import urlsplit

from fortune_training.calendar_foundation.models import json_value
from fortune_training.ziwei_application.palace_stem_topology import (
    ZiweiPalaceStemTopologyResolutionError,
    ZiweiPalaceStemTransformationTopologyService,
)
from fortune_training.ziwei_application.service import ApplicationResolutionError

from .local_app import (
    MAX_REQUEST_BYTES,
    LocalCombinedAppRequestError,
    _optional_int,
)


LOCAL_ZIWEI_PALACE_STEM_TOPOLOGY_SCHEMA = (
    "ZIWEI-BAZI-COMBINED-LOCAL-ZIWEI-PALACE-STEM-TOPOLOGY-R1"
)


class ZiweiPalaceStemTopologyLocalMixin:
    """Additive palace-stem transformation topology sidecar for the Workbench."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ziwei_palace_stem_topology_service = (
            ZiweiPalaceStemTransformationTopologyService()
        )

    def resolve_ziwei_palace_stem_topology_payload(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_JSON",
                "request body must be a JSON object",
            )

        combined_response = self.resolve_payload(dict(payload))
        combined_resolution = combined_response["combined_resolution"]
        source_ziwei = combined_resolution.get("ziwei_bundle")
        if source_ziwei is None:
            error = combined_resolution.get("ziwei_error") or {}
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_PALACE_STEM_TOPOLOGY_SOURCE_UNAVAILABLE",
                str(error.get("detail") or "combined resolution has no Ziwei bundle"),
                status=422,
            )
        expected_ziwei_hash = source_ziwei["bundle_hash"]

        request = self._ziwei_application_request_from_payload(payload)
        lunar_month = _optional_int(payload, "ziwei_lunar_month", 1, 12)
        if lunar_month is not None and request.annual_year is None:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_INPUT",
                "ziwei_lunar_month requires ziwei_annual_year",
            )
        request = replace(request, lunar_month=lunar_month)

        try:
            bundle = self.ziwei_service.resolve(request)
            topology = self.ziwei_palace_stem_topology_service.resolve(bundle)
        except ApplicationResolutionError as exc:
            raise LocalCombinedAppRequestError(
                exc.diagnostic_code,
                str(exc),
                status=422,
            ) from exc
        except ZiweiPalaceStemTopologyResolutionError as exc:
            raise LocalCombinedAppRequestError(
                exc.diagnostic_code,
                exc.detail,
                status=422,
            ) from exc
        except ValueError as exc:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_PALACE_STEM_TOPOLOGY_FAILED",
                str(exc),
                status=422,
            ) from exc

        if (
            bundle.bundle_hash != expected_ziwei_hash
            or topology.source_application_bundle_hash != expected_ziwei_hash
        ):
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_PALACE_STEM_TOPOLOGY_SOURCE_BINDING_MISMATCH",
                (
                    f"combined={expected_ziwei_hash};controller_bundle={bundle.bundle_hash};"
                    f"topology_source={topology.source_application_bundle_hash}"
                ),
                status=500,
            )

        source_bazi = combined_resolution.get("bazi_bundle")
        return {
            "schema": LOCAL_ZIWEI_PALACE_STEM_TOPOLOGY_SCHEMA,
            "source_combined_manifest_hash": combined_resolution["manifest_hash"],
            "source_ziwei_bundle_hash": expected_ziwei_hash,
            "source_bazi_bundle_hash": (
                source_bazi["bundle_hash"] if source_bazi is not None else None
            ),
            "ziwei_palace_stem_transformation_topology": json_value(topology),
        }


class _ZiweiPalaceStemTopologyHandlerMixin:
    application: ZiweiPalaceStemTopologyLocalMixin

    def do_POST(self) -> None:  # noqa: N802
        if urlsplit(self.path).path != "/api/ziwei-palace-stem-topology":
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
            response = self.application.resolve_ziwei_palace_stem_topology_payload(
                payload
            )
        except LocalCombinedAppRequestError as exc:
            self._error(exc)
            return
        self._send_json(200, response)
