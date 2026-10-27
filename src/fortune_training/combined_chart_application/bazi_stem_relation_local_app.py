from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlsplit

from fortune_training.bazi_chart import BaziChartRequest

from .local_app import MAX_REQUEST_BYTES, LocalCombinedAppRequestError, _Handler
from .service import CombinedApplicationResolutionError


BAZI_STEM_RELATION_PRESENTATION_ENDPOINT = "/api/bazi-stem-relations-presentation"
BAZI_STEM_RELATION_PRESENTATION_SCHEMA = (
    "COMBINED-BAZI-STEM-RELATION-PRESENTATION-R1"
)
_STEM_RELATION_FAMILY = "STEM_COMBINATION"


def _stem_relation_rows(chart: Any) -> list[dict[str, Any]]:
    stems = {stem.instance_id: stem for stem in chart.stems}
    rows: list[dict[str, Any]] = []
    for relation in chart.raw_relations:
        if relation.relation_family != _STEM_RELATION_FAMILY:
            continue
        participants: list[dict[str, str]] = []
        for instance_id in relation.participant_instance_ids:
            stem = stems.get(instance_id)
            if stem is None:
                raise ValueError(
                    f"relation {relation.relation_id} references unknown stem {instance_id}"
                )
            participants.append(
                {
                    "instance_id": stem.instance_id,
                    "position": stem.position,
                    "stem": stem.stem,
                }
            )
        if len(participants) != relation.arity:
            raise ValueError(
                f"relation {relation.relation_id} arity={relation.arity} "
                f"participants={len(participants)}"
            )
        rows.append(
            {
                "relation_id": relation.relation_id,
                "semantic_relation_id": relation.semantic_relation_id,
                "relation_family": relation.relation_family,
                "orientation": relation.orientation,
                "arity": relation.arity,
                "participants": participants,
                "rule_set_id": relation.rule_set_id,
                "rule_set_version": relation.rule_set_version,
                "source_refs": list(relation.source_refs),
            }
        )
    return rows


class BaziStemRelationPresentationLocalMixin:
    """Read-only natal stem-combination facts over the released Ba Zi foundation."""

    def resolve_bazi_stem_relation_presentation_payload(
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
                "LOCAL_APP_BAZI_STEM_RELATION_SOURCE_RESOLUTION_FAILED",
                str(exc),
                status=422,
            ) from exc

        bazi_bundle = combined.bazi_bundle
        if bazi_bundle is None:
            error = combined.bazi_error
            raise LocalCombinedAppRequestError(
                error.code
                if error is not None
                else "LOCAL_APP_BAZI_STEM_RELATION_BAZI_MISSING",
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
                "LOCAL_APP_BAZI_STEM_RELATION_NATAL_REPLAY_FAILED",
                ";".join(natal_resolution.diagnostics) or natal_resolution.status,
                status=422,
            )

        candidate_rows: list[dict[str, Any]] = []
        for application_index, application_candidate in enumerate(bazi_bundle.candidates):
            natal_index = application_candidate.natal_candidate_index
            if natal_index < 0 or natal_index >= len(natal_resolution.candidates):
                raise LocalCombinedAppRequestError(
                    "LOCAL_APP_BAZI_STEM_RELATION_NATAL_INDEX_MISMATCH",
                    (
                        f"application_candidate_index={application_index} "
                        f"natal_candidate_index={natal_index}"
                    ),
                    status=422,
                )
            natal_candidate = natal_resolution.candidates[natal_index]
            if natal_candidate.hashes.fact_hash != application_candidate.natal_fact_hash:
                raise LocalCombinedAppRequestError(
                    "LOCAL_APP_BAZI_STEM_RELATION_NATAL_FACT_HASH_MISMATCH",
                    f"application_candidate_index={application_index}",
                    status=422,
                )
            if (
                natal_candidate.hashes.computation_hash
                != application_candidate.natal_computation_hash
            ):
                raise LocalCombinedAppRequestError(
                    "LOCAL_APP_BAZI_STEM_RELATION_NATAL_COMPUTATION_HASH_MISMATCH",
                    f"application_candidate_index={application_index}",
                    status=422,
                )
            try:
                relations = _stem_relation_rows(natal_candidate.chart)
            except ValueError as exc:
                raise LocalCombinedAppRequestError(
                    "LOCAL_APP_BAZI_STEM_RELATION_IDENTITY_INVALID",
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
                    "stem_relations": relations,
                }
            )

        return {
            "schema": BAZI_STEM_RELATION_PRESENTATION_SCHEMA,
            "semantics": "RELATION_IDENTITY_ONLY",
            "source_combined_manifest_hash": combined.manifest_hash,
            "source_bazi_bundle_hash": bazi_bundle.bundle_hash,
            "candidates": candidate_rows,
        }


class _BaziStemRelationPresentationHandlerMixin(_Handler):
    application: BaziStemRelationPresentationLocalMixin

    def do_POST(self) -> None:  # noqa: N802
        if urlsplit(self.path).path != BAZI_STEM_RELATION_PRESENTATION_ENDPOINT:
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
            response = self.application.resolve_bazi_stem_relation_presentation_payload(
                payload
            )
        except LocalCombinedAppRequestError as exc:
            self._error(exc)
            return
        self._send_json(200, response)
