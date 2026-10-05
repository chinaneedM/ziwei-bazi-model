from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlsplit

from fortune_training.calendar_foundation.models import json_value
from fortune_training.ziwei_chart import (
    FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_API_ID,
    FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_API_VERSION,
    FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_IDS,
    FOUR_TRANSFORMATION_HISTORICAL_REGISTRY_ID,
    FOUR_TRANSFORMATION_HISTORICAL_REGISTRY_VERSION,
    FOUR_TRANSFORMATION_HISTORICAL_RESOLVER_ID,
    FOUR_TRANSFORMATION_HISTORICAL_RESOLVER_VERSION,
    FOUR_TRANSFORMATION_HISTORICAL_SELECTION_STATUS,
    historical_four_transformation_candidate_registry_hash,
    resolve_historical_four_transformation_candidate,
)

from .local_app import MAX_REQUEST_BYTES, LocalCombinedAppRequestError


LOCAL_ZIWEI_FOUR_TRANSFORMATION_CANDIDATE_SCHEMA = (
    "ZIWEI-BAZI-COMBINED-LOCAL-ZIWEI-FOUR-TRANSFORMATION-HISTORICAL-CANDIDATE-R1"
)


class ZiweiFourTransformationHistoricalCandidateLocalMixin:
    """Read-only source-scoped Four-Transformation whole-table candidates."""

    def resolve_ziwei_four_transformation_candidate_payload(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        combined_resolution, expected_ziwei_hash, bundle = (
            self._resolve_ziwei_sidecar_source(
                payload,
                source_unavailable_code=(
                    "LOCAL_APP_ZIWEI_FOUR_TRANSFORMATION_CANDIDATE_SOURCE_UNAVAILABLE"
                ),
            )
        )
        if bundle.bundle_hash != expected_ziwei_hash:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_FOUR_TRANSFORMATION_CANDIDATE_SOURCE_BINDING_MISMATCH",
                (
                    f"combined={expected_ziwei_hash};"
                    f"controller_bundle={bundle.bundle_hash}"
                ),
                status=500,
            )

        source_stem = bundle.candidate.chart.structure.ziwei_birth_year_stem
        candidates = tuple(
            resolve_historical_four_transformation_candidate(
                candidate_id=candidate_id,
                source_stem=source_stem,
            )
            for candidate_id in FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_IDS
        )
        if tuple(row["candidate_id"] for row in candidates) != (
            FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_IDS
        ):
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_FOUR_TRANSFORMATION_CANDIDATE_SET_MISMATCH",
                "resolved candidate family order does not match the released registry",
                status=500,
            )

        source_bazi = combined_resolution.get("bazi_bundle")
        return {
            "schema": LOCAL_ZIWEI_FOUR_TRANSFORMATION_CANDIDATE_SCHEMA,
            "source_combined_manifest_hash": combined_resolution["manifest_hash"],
            "source_ziwei_bundle_hash": expected_ziwei_hash,
            "source_bazi_bundle_hash": (
                source_bazi["bundle_hash"] if source_bazi is not None else None
            ),
            "source_natal_fact_hash": bundle.candidate.hashes.fact_hash,
            "source_natal_computation_hash": bundle.candidate.hashes.computation_hash,
            "candidate_profile": {
                "candidate_api_id": FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_API_ID,
                "candidate_api_version": FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_API_VERSION,
                "rule_set_id": FOUR_TRANSFORMATION_HISTORICAL_REGISTRY_ID,
                "rule_set_version": FOUR_TRANSFORMATION_HISTORICAL_REGISTRY_VERSION,
                "selection_status": FOUR_TRANSFORMATION_HISTORICAL_SELECTION_STATUS,
                "runtime_resolver_id": FOUR_TRANSFORMATION_HISTORICAL_RESOLVER_ID,
                "runtime_resolver_version": FOUR_TRANSFORMATION_HISTORICAL_RESOLVER_VERSION,
                "registry_hash": historical_four_transformation_candidate_registry_hash(),
                "candidate_ids": FOUR_TRANSFORMATION_HISTORICAL_CANDIDATE_IDS,
                "whole_table_only": True,
                "cell_level_hybridization_allowed": False,
                "production_winner_selected": False,
                "production_profile_changed": False,
            },
            "input_snapshot": {"source_stem": source_stem},
            "candidate_tables": json_value(candidates),
        }


class _ZiweiFourTransformationHistoricalCandidateHandlerMixin:
    application: ZiweiFourTransformationHistoricalCandidateLocalMixin

    def do_POST(self) -> None:  # noqa: N802
        if urlsplit(self.path).path != "/api/ziwei-four-transformation-candidates":
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
            response = self.application.resolve_ziwei_four_transformation_candidate_payload(
                payload
            )
        except LocalCombinedAppRequestError as exc:
            self._error(exc)
            return
        self._send_json(200, response)
