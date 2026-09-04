from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlsplit

from fortune_training.bazi_chart import BaziChartRequest

from .local_app import MAX_REQUEST_BYTES, LocalCombinedAppRequestError, _Handler
from .service import CombinedApplicationResolutionError


BAZI_HIDDEN_EXPOSURE_PRESENTATION_ENDPOINT = "/api/bazi-hidden-exposure-presentation"
BAZI_HIDDEN_EXPOSURE_PRESENTATION_SCHEMA = (
    "COMBINED-BAZI-HIDDEN-EXPOSURE-PRESENTATION-R1"
)
_EXACT_MATCH_KIND = "EXACT_STEM"


def _hidden_exposure_rows(chart: Any) -> list[dict[str, Any]]:
    hidden_by_id = {row.instance_id: row for row in chart.hidden_stems}
    visible_by_id = {row.instance_id: row for row in chart.stems}
    rows: list[dict[str, Any]] = []
    for link in chart.exposures:
        hidden = hidden_by_id.get(link.hidden_stem_instance_id)
        visible = visible_by_id.get(link.visible_stem_instance_id)
        if hidden is None or visible is None:
            raise ValueError(
                f"exposure {link.link_id} references an unknown hidden/visible stem"
            )
        if (
            link.match_kind != _EXACT_MATCH_KIND
            or hidden.stem != visible.stem
            or link.stem != hidden.stem
        ):
            raise ValueError(
                f"exposure {link.link_id} is not an exact same-stem identity match"
            )
        rows.append(
            {
                "link_id": link.link_id,
                "match_kind": link.match_kind,
                "stem": link.stem,
                "hidden_stem": {
                    "instance_id": hidden.instance_id,
                    "branch_instance_id": hidden.branch_instance_id,
                    "branch_position": hidden.branch_position,
                    "stem": hidden.stem,
                },
                "visible_stem": {
                    "instance_id": visible.instance_id,
                    "position": visible.position,
                    "stem": visible.stem,
                },
                "source_refs": list(link.source_refs),
            }
        )
    return rows


class BaziHiddenExposurePresentationLocalMixin:
    """Read-only exact hidden/visible same-stem facts over the released natal state."""

    def resolve_bazi_hidden_exposure_presentation_payload(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_JSON", "request body must be a JSON object"
            )

        combined_request, _location_selection = self._combined_request_from_payload(payload)
        try:
            combined = self.service.resolve(combined_request)
        except CombinedApplicationResolutionError as exc:
            raise LocalCombinedAppRequestError(exc.code, exc.detail, status=422) from exc
        except ValueError as exc:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_BAZI_HIDDEN_EXPOSURE_SOURCE_RESOLUTION_FAILED",
                str(exc),
                status=422,
            ) from exc

        bazi_bundle = combined.bazi_bundle
        if bazi_bundle is None:
            error = combined.bazi_error
            raise LocalCombinedAppRequestError(
                error.code
                if error is not None
                else "LOCAL_APP_BAZI_HIDDEN_EXPOSURE_BAZI_MISSING",
                error.detail
                if error is not None
                else "Bazi application bundle is unavailable",
                status=422,
            )

        natal_resolution = self.service.bazi_service.chart_foundation.resolve_typed(
            BaziChartRequest(
                birth=combined_request.birth,
                profile=combined_request.bazi_natal_profile,
            )
        )
        if natal_resolution.status == "FAILED" or not natal_resolution.candidates:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_BAZI_HIDDEN_EXPOSURE_NATAL_REPLAY_FAILED",
                ";".join(natal_resolution.diagnostics) or natal_resolution.status,
                status=422,
            )

        candidate_rows: list[dict[str, Any]] = []
        for application_index, application_candidate in enumerate(bazi_bundle.candidates):
            natal_index = application_candidate.natal_candidate_index
            if natal_index < 0 or natal_index >= len(natal_resolution.candidates):
                raise LocalCombinedAppRequestError(
                    "LOCAL_APP_BAZI_HIDDEN_EXPOSURE_NATAL_INDEX_MISMATCH",
                    (
                        f"application_candidate_index={application_index} "
                        f"natal_candidate_index={natal_index}"
                    ),
                    status=422,
                )
            natal_candidate = natal_resolution.candidates[natal_index]
            if natal_candidate.hashes.fact_hash != application_candidate.natal_fact_hash:
                raise LocalCombinedAppRequestError(
                    "LOCAL_APP_BAZI_HIDDEN_EXPOSURE_NATAL_FACT_HASH_MISMATCH",
                    f"application_candidate_index={application_index}",
                    status=422,
                )
            if (
                natal_candidate.hashes.computation_hash
                != application_candidate.natal_computation_hash
            ):
                raise LocalCombinedAppRequestError(
                    "LOCAL_APP_BAZI_HIDDEN_EXPOSURE_NATAL_COMPUTATION_HASH_MISMATCH",
                    f"application_candidate_index={application_index}",
                    status=422,
                )
            try:
                exposures = _hidden_exposure_rows(natal_candidate.chart)
            except ValueError as exc:
                raise LocalCombinedAppRequestError(
                    "LOCAL_APP_BAZI_HIDDEN_EXPOSURE_IDENTITY_INVALID",
                    str(exc),
                    status=422,
                ) from exc

            candidate_rows.append(
                {
                    "application_candidate_index": application_index,
                    "candidate_id": application_candidate.candidate_id,
                    "natal_candidate_index": natal_index,
                    "source_natal_fact_hash": application_candidate.natal_fact_hash,
                    "source_natal_computation_hash": (
                        application_candidate.natal_computation_hash
                    ),
                    "exposures": exposures,
                }
            )

        return {
            "schema": BAZI_HIDDEN_EXPOSURE_PRESENTATION_SCHEMA,
            "semantics": "EXACT_STEM_IDENTITY_MATCH_ONLY",
            "source_combined_manifest_hash": combined.manifest_hash,
            "source_bazi_bundle_hash": bazi_bundle.bundle_hash,
            "candidates": candidate_rows,
        }


class _BaziHiddenExposurePresentationHandlerMixin(_Handler):
    application: BaziHiddenExposurePresentationLocalMixin

    def do_POST(self) -> None:  # noqa: N802
        if urlsplit(self.path).path != BAZI_HIDDEN_EXPOSURE_PRESENTATION_ENDPOINT:
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
            response = self.application.resolve_bazi_hidden_exposure_presentation_payload(
                payload
            )
        except LocalCombinedAppRequestError as exc:
            self._error(exc)
            return
        self._send_json(200, response)
