from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlsplit

from fortune_training.bazi_chart import BaziChartRequest
from fortune_training.bazi_chart.registries import PILLAR_POSITIONS
from fortune_training.bazi_nayin_annotation import BaziNayinAnnotationService
from fortune_training.calendar_foundation.models import json_value

from .local_app import (
    MAX_REQUEST_BYTES,
    LocalCombinedAppRequestError,
    _Handler,
)
from .service import CombinedApplicationResolutionError


NAYIN_PRESENTATION_ENDPOINT = "/api/bazi-nayin-presentation"
NAYIN_PRESENTATION_SCHEMA = "COMBINED-BAZI-NAYIN-PRESENTATION-R1"


class BaziNayinPresentationLocalMixin:
    """Additive FortuneChart presentation over the released Nayin sidecar."""

    def resolve_bazi_nayin_presentation_payload(
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
                "LOCAL_APP_NAYIN_SOURCE_RESOLUTION_FAILED", str(exc), status=422
            ) from exc

        bazi_bundle = combined.bazi_bundle
        if bazi_bundle is None:
            error = combined.bazi_error
            raise LocalCombinedAppRequestError(
                error.code if error is not None else "LOCAL_APP_NAYIN_BAZI_MISSING",
                error.detail if error is not None else "Bazi application bundle is unavailable",
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
                "LOCAL_APP_NAYIN_NATAL_REPLAY_FAILED",
                ";".join(natal_resolution.diagnostics) or natal_resolution.status,
                status=422,
            )

        nayin_service = BaziNayinAnnotationService()
        candidate_rows: list[dict[str, Any]] = []
        for application_index, application_candidate in enumerate(
            bazi_bundle.candidates
        ):
            natal_index = application_candidate.natal_candidate_index
            if natal_index < 0 or natal_index >= len(natal_resolution.candidates):
                raise LocalCombinedAppRequestError(
                    "LOCAL_APP_NAYIN_NATAL_INDEX_MISMATCH",
                    f"application_candidate_index={application_index} natal_candidate_index={natal_index}",
                    status=422,
                )
            natal_candidate = natal_resolution.candidates[natal_index]
            if (
                natal_candidate.hashes.fact_hash
                != application_candidate.natal_fact_hash
            ):
                raise LocalCombinedAppRequestError(
                    "LOCAL_APP_NAYIN_NATAL_FACT_HASH_MISMATCH",
                    f"application_candidate_index={application_index}",
                    status=422,
                )
            if (
                natal_candidate.hashes.computation_hash
                != application_candidate.natal_computation_hash
            ):
                raise LocalCombinedAppRequestError(
                    "LOCAL_APP_NAYIN_NATAL_COMPUTATION_HASH_MISMATCH",
                    f"application_candidate_index={application_index}",
                    status=422,
                )

            try:
                nayin_resolution = nayin_service.resolve(
                    natal_candidate.chart,
                    combined_request.bazi_natal_profile,
                )
            except ValueError as exc:
                raise LocalCombinedAppRequestError(
                    "LOCAL_APP_NAYIN_ANNOTATION_FAILED",
                    str(exc),
                    status=422,
                ) from exc

            if (
                nayin_resolution.source_natal_fact_hash
                != application_candidate.natal_fact_hash
                or nayin_resolution.source_natal_computation_hash
                != application_candidate.natal_computation_hash
            ):
                raise LocalCombinedAppRequestError(
                    "LOCAL_APP_NAYIN_SOURCE_HASH_BINDING_MISMATCH",
                    f"application_candidate_index={application_index}",
                    status=422,
                )

            annotations = nayin_resolution.annotations
            if tuple(row.source_pillar_position for row in annotations) != PILLAR_POSITIONS:
                raise LocalCombinedAppRequestError(
                    "LOCAL_APP_NAYIN_PILLAR_ORDER_MISMATCH",
                    f"application_candidate_index={application_index}",
                    status=422,
                )

            view_pillars = application_candidate.view.get("pillars")
            if not isinstance(view_pillars, (list, tuple)) or len(view_pillars) != len(
                PILLAR_POSITIONS
            ):
                raise LocalCombinedAppRequestError(
                    "LOCAL_APP_NAYIN_APPLICATION_VIEW_PILLARS_INVALID",
                    f"application_candidate_index={application_index}",
                    status=422,
                )

            for pillar, annotation, view_pillar in zip(
                natal_candidate.chart.pillars,
                annotations,
                view_pillars,
                strict=True,
            ):
                if not isinstance(view_pillar, Mapping):
                    raise LocalCombinedAppRequestError(
                        "LOCAL_APP_NAYIN_APPLICATION_VIEW_PILLAR_INVALID",
                        f"application_candidate_index={application_index}",
                        status=422,
                    )
                exact_identity = (
                    annotation.source_pillar_position == pillar.position
                    and annotation.source_pillar_ganzhi == pillar.ganzhi
                    and annotation.source_pillar_sexagenary_index
                    == pillar.sexagenary_index
                    and annotation.source_stem_instance_id == pillar.stem_instance_id
                    and annotation.source_branch_instance_id == pillar.branch_instance_id
                    and view_pillar.get("position") == pillar.position
                    and view_pillar.get("ganzhi") == pillar.ganzhi
                    and view_pillar.get("sexagenary_index") == pillar.sexagenary_index
                )
                if not exact_identity:
                    raise LocalCombinedAppRequestError(
                        "LOCAL_APP_NAYIN_PILLAR_IDENTITY_MISMATCH",
                        (
                            f"application_candidate_index={application_index} "
                            f"pillar={pillar.position}"
                        ),
                        status=422,
                    )

            candidate_rows.append(
                {
                    "application_candidate_index": application_index,
                    "candidate_id": application_candidate.candidate_id,
                    "natal_candidate_index": natal_index,
                    "source_natal_fact_hash": application_candidate.natal_fact_hash,
                    "source_natal_computation_hash": (
                        application_candidate.natal_computation_hash
                    ),
                    "nayin_resolution": json_value(nayin_resolution),
                }
            )

        return {
            "schema": NAYIN_PRESENTATION_SCHEMA,
            "source_combined_manifest_hash": combined.manifest_hash,
            "source_bazi_bundle_hash": bazi_bundle.bundle_hash,
            "candidates": candidate_rows,
        }


class _NayinPresentationHandlerMixin(_Handler):
    application: BaziNayinPresentationLocalMixin

    def do_POST(self) -> None:  # noqa: N802
        if urlsplit(self.path).path != NAYIN_PRESENTATION_ENDPOINT:
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
            response = self.application.resolve_bazi_nayin_presentation_payload(payload)
        except LocalCombinedAppRequestError as exc:
            self._error(exc)
            return
        self._send_json(200, response)
