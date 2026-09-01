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
from fortune_training.ziwei_application.star_provenance import (
    ZiweiStarPlacementProvenanceService,
    ZiweiStarProvenanceResolutionError,
)

from .local_app import (
    MAX_REQUEST_BYTES,
    LocalCombinedAppRequestError,
    _optional_int,
)


LOCAL_ZIWEI_PALACE_STEM_TOPOLOGY_SCHEMA = (
    "ZIWEI-BAZI-COMBINED-LOCAL-ZIWEI-PALACE-STEM-TOPOLOGY-R1"
)
LOCAL_ZIWEI_STAR_PROVENANCE_SCHEMA = (
    "ZIWEI-BAZI-COMBINED-LOCAL-ZIWEI-STAR-PROVENANCE-R1"
)


class ZiweiPalaceStemTopologyLocalMixin:
    """Additive deterministic Ziwei sidecars for the local Workbench."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ziwei_palace_stem_topology_service = (
            ZiweiPalaceStemTransformationTopologyService()
        )
        self.ziwei_star_provenance_service = ZiweiStarPlacementProvenanceService()

    def _resolve_ziwei_sidecar_source(
        self,
        payload: dict[str, Any],
    ):
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
        except ApplicationResolutionError as exc:
            raise LocalCombinedAppRequestError(
                exc.diagnostic_code,
                str(exc),
                status=422,
            ) from exc
        return combined_resolution, expected_ziwei_hash, bundle

    @staticmethod
    def _source_hash_envelope(
        combined_resolution: dict[str, Any],
        expected_ziwei_hash: str,
    ) -> dict[str, Any]:
        source_bazi = combined_resolution.get("bazi_bundle")
        return {
            "source_combined_manifest_hash": combined_resolution["manifest_hash"],
            "source_ziwei_bundle_hash": expected_ziwei_hash,
            "source_bazi_bundle_hash": (
                source_bazi["bundle_hash"] if source_bazi is not None else None
            ),
        }

    def resolve_ziwei_palace_stem_topology_payload(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        combined_resolution, expected_ziwei_hash, bundle = (
            self._resolve_ziwei_sidecar_source(payload)
        )
        try:
            topology = self.ziwei_palace_stem_topology_service.resolve(bundle)
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
        return {
            "schema": LOCAL_ZIWEI_PALACE_STEM_TOPOLOGY_SCHEMA,
            **self._source_hash_envelope(combined_resolution, expected_ziwei_hash),
            "ziwei_palace_stem_transformation_topology": json_value(topology),
        }

    def resolve_ziwei_star_provenance_payload(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        combined_resolution, expected_ziwei_hash, bundle = (
            self._resolve_ziwei_sidecar_source(payload)
        )
        try:
            provenance = self.ziwei_star_provenance_service.resolve(bundle)
        except ZiweiStarProvenanceResolutionError as exc:
            raise LocalCombinedAppRequestError(
                exc.diagnostic_code,
                exc.detail,
                status=422,
            ) from exc
        except ValueError as exc:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_STAR_PROVENANCE_FAILED",
                str(exc),
                status=422,
            ) from exc

        if (
            bundle.bundle_hash != expected_ziwei_hash
            or provenance.source_application_bundle_hash != expected_ziwei_hash
        ):
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_STAR_PROVENANCE_SOURCE_BINDING_MISMATCH",
                (
                    f"combined={expected_ziwei_hash};controller_bundle={bundle.bundle_hash};"
                    f"provenance_source={provenance.source_application_bundle_hash}"
                ),
                status=500,
            )
        return {
            "schema": LOCAL_ZIWEI_STAR_PROVENANCE_SCHEMA,
            **self._source_hash_envelope(combined_resolution, expected_ziwei_hash),
            "ziwei_star_placement_provenance": json_value(provenance),
        }


class _ZiweiPalaceStemTopologyHandlerMixin:
    application: ZiweiPalaceStemTopologyLocalMixin

    def do_POST(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path
        if path not in {
            "/api/ziwei-palace-stem-topology",
            "/api/ziwei-star-provenance",
        }:
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
            if path == "/api/ziwei-star-provenance":
                response = self.application.resolve_ziwei_star_provenance_payload(payload)
            else:
                response = self.application.resolve_ziwei_palace_stem_topology_payload(payload)
        except LocalCombinedAppRequestError as exc:
            self._error(exc)
            return
        self._send_json(200, response)
