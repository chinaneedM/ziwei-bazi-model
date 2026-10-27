from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlsplit

from fortune_training.calendar_foundation.models import json_value
from fortune_training.ziwei_chart import (
    JIELAN_1581_DIGNITY_CANDIDATE_API_ID,
    JIELAN_1581_DIGNITY_CANDIDATE_API_VERSION,
    JIELAN_1581_DIGNITY_CROSS_COLLATION_ID,
    JIELAN_1581_DIGNITY_CROSS_COLLATION_STATUS,
    JIELAN_1581_DIGNITY_CROSS_COLLATION_VERSION,
    JIELAN_1581_DIGNITY_LEXEME_CANDIDATE_ID,
    JIELAN_1581_DIGNITY_LEXEME_REGISTRY_ID,
    JIELAN_1581_DIGNITY_LEXEME_REGISTRY_VERSION,
    JIELAN_1581_DIGNITY_LEXEME_RESOLVER_ID,
    JIELAN_1581_DIGNITY_LEXEME_RESOLVER_VERSION,
    JIELAN_1581_DIGNITY_SELECTION_STATUS,
    jielan_1581_dignity_ch69_ch70_cross_collation_payload,
    jielan_1581_dignity_lexeme_registry_hash,
    resolve_jielan_1581_dignity_lexeme_candidate,
)

from .local_app import MAX_REQUEST_BYTES, LocalCombinedAppRequestError


LOCAL_ZIWEI_JIELAN_DIGNITY_CANDIDATE_SCHEMA = (
    "ZIWEI-BAZI-COMBINED-LOCAL-ZIWEI-JIELAN-DIGNITY-HISTORICAL-CANDIDATE-R1"
)


class ZiweiJielanDignityHistoricalCandidateLocalMixin:
    """Read-only Jielan dignity raw-lexeme candidate and source cross-collation."""

    def resolve_ziwei_jielan_dignity_candidate_payload(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        combined_resolution, expected_ziwei_hash, bundle = (
            self._resolve_ziwei_sidecar_source(
                payload,
                source_unavailable_code=(
                    "LOCAL_APP_ZIWEI_JIELAN_DIGNITY_CANDIDATE_SOURCE_UNAVAILABLE"
                ),
            )
        )
        if bundle.bundle_hash != expected_ziwei_hash:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_JIELAN_DIGNITY_CANDIDATE_SOURCE_BINDING_MISMATCH",
                (
                    f"combined={expected_ziwei_hash};"
                    f"controller_bundle={bundle.bundle_hash}"
                ),
                status=500,
            )

        candidate = resolve_jielan_1581_dignity_lexeme_candidate()
        cross = jielan_1581_dignity_ch69_ch70_cross_collation_payload()
        registry_hash = jielan_1581_dignity_lexeme_registry_hash()
        if candidate["registry_hash"] != registry_hash:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_JIELAN_DIGNITY_REGISTRY_HASH_MISMATCH",
                "candidate resolver registry hash does not match released registry",
                status=500,
            )
        if cross["registry_id"] != candidate["registry_id"]:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_JIELAN_DIGNITY_CROSS_COLLATION_REGISTRY_MISMATCH",
                (
                    f"candidate={candidate['registry_id']};"
                    f"cross={cross['registry_id']}"
                ),
                status=500,
            )

        source_bazi = combined_resolution.get("bazi_bundle")
        return {
            "schema": LOCAL_ZIWEI_JIELAN_DIGNITY_CANDIDATE_SCHEMA,
            "source_combined_manifest_hash": combined_resolution["manifest_hash"],
            "source_ziwei_bundle_hash": expected_ziwei_hash,
            "source_bazi_bundle_hash": (
                source_bazi["bundle_hash"] if source_bazi is not None else None
            ),
            "source_natal_fact_hash": bundle.candidate.hashes.fact_hash,
            "source_natal_computation_hash": bundle.candidate.hashes.computation_hash,
            "candidate_profile": {
                "candidate_api_id": JIELAN_1581_DIGNITY_CANDIDATE_API_ID,
                "candidate_api_version": JIELAN_1581_DIGNITY_CANDIDATE_API_VERSION,
                "rule_set_id": JIELAN_1581_DIGNITY_LEXEME_REGISTRY_ID,
                "rule_set_version": JIELAN_1581_DIGNITY_LEXEME_REGISTRY_VERSION,
                "candidate_id": JIELAN_1581_DIGNITY_LEXEME_CANDIDATE_ID,
                "selection_status": JIELAN_1581_DIGNITY_SELECTION_STATUS,
                "runtime_resolver_id": JIELAN_1581_DIGNITY_LEXEME_RESOLVER_ID,
                "runtime_resolver_version": JIELAN_1581_DIGNITY_LEXEME_RESOLVER_VERSION,
                "registry_hash": registry_hash,
                "candidate_runtime_hash": candidate["runtime_hash"],
                "cross_collation_id": JIELAN_1581_DIGNITY_CROSS_COLLATION_ID,
                "cross_collation_version": JIELAN_1581_DIGNITY_CROSS_COLLATION_VERSION,
                "cross_collation_status": JIELAN_1581_DIGNITY_CROSS_COLLATION_STATUS,
                "cross_collation_hash": cross["cross_collation_hash"],
                "production_grade_mapping_present": False,
                "ch69_used_to_fill_ch70": False,
                "ch70_used_to_overwrite_ch69": False,
                "production_winner_selected": False,
                "production_profile_changed": False,
            },
            "source_lexeme_rows": json_value(candidate["rows"]),
            "cross_collation_rows": json_value(cross["rows"]),
            "relation_counts": json_value(cross["relation_counts"]),
        }


class _ZiweiJielanDignityHistoricalCandidateHandlerMixin:
    application: ZiweiJielanDignityHistoricalCandidateLocalMixin

    def do_POST(self) -> None:  # noqa: N802
        if urlsplit(self.path).path != "/api/ziwei-jielan-1581-dignity-candidate":
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
            response = self.application.resolve_ziwei_jielan_dignity_candidate_payload(
                payload
            )
        except LocalCombinedAppRequestError as exc:
            self._error(exc)
            return
        self._send_json(200, response)
