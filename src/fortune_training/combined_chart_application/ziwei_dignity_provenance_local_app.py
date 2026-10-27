from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlsplit

from fortune_training.calendar_foundation.models import json_value
from fortune_training.ziwei_application.dignity_provenance import (
    ZiweiDignityAnnotationProvenanceService,
    ZiweiDignityProvenanceResolutionError,
)

from .local_app import MAX_REQUEST_BYTES, LocalCombinedAppRequestError


LOCAL_ZIWEI_DIGNITY_PROVENANCE_SCHEMA = (
    "ZIWEI-BAZI-COMBINED-LOCAL-ZIWEI-DIGNITY-PROVENANCE-R1"
)


class ZiweiDignityProvenanceLocalMixin:
    """Read-only Dignity annotation provenance sidecar for the Workbench."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ziwei_dignity_provenance_service = ZiweiDignityAnnotationProvenanceService()

    def resolve_ziwei_dignity_provenance_payload(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        combined_resolution, expected_ziwei_hash, bundle = (
            self._resolve_ziwei_sidecar_source(
                payload,
                source_unavailable_code=(
                    "LOCAL_APP_ZIWEI_DIGNITY_PROVENANCE_SOURCE_UNAVAILABLE"
                ),
            )
        )
        try:
            provenance = self.ziwei_dignity_provenance_service.resolve(bundle)
        except ZiweiDignityProvenanceResolutionError as exc:
            raise LocalCombinedAppRequestError(
                exc.diagnostic_code,
                exc.detail,
                status=422,
            ) from exc
        except ValueError as exc:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_DIGNITY_PROVENANCE_FAILED",
                str(exc),
                status=422,
            ) from exc

        if (
            bundle.bundle_hash != expected_ziwei_hash
            or provenance.source_application_bundle_hash != expected_ziwei_hash
        ):
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_DIGNITY_PROVENANCE_SOURCE_BINDING_MISMATCH",
                (
                    f"combined={expected_ziwei_hash};controller_bundle={bundle.bundle_hash};"
                    f"provenance_source={provenance.source_application_bundle_hash}"
                ),
                status=500,
            )
        source_bazi = combined_resolution.get("bazi_bundle")
        return {
            "schema": LOCAL_ZIWEI_DIGNITY_PROVENANCE_SCHEMA,
            "source_combined_manifest_hash": combined_resolution["manifest_hash"],
            "source_ziwei_bundle_hash": expected_ziwei_hash,
            "source_bazi_bundle_hash": (
                source_bazi["bundle_hash"] if source_bazi is not None else None
            ),
            "ziwei_dignity_annotation_provenance": json_value(provenance),
        }


class _ZiweiDignityProvenanceHandlerMixin:
    application: ZiweiDignityProvenanceLocalMixin

    def do_POST(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path
        if path != "/api/ziwei-dignity-provenance":
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
            response = self.application.resolve_ziwei_dignity_provenance_payload(payload)
        except LocalCombinedAppRequestError as exc:
            self._error(exc)
            return
        self._send_json(200, response)
