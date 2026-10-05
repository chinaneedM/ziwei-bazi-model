from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlsplit

from fortune_training.calendar_foundation.models import json_value
from fortune_training.ziwei_chart import (
    JIELAN_1581_CANDIDATE_API_ID,
    JIELAN_1581_CANDIDATE_API_VERSION,
    JIELAN_1581_PRODUCT_FACT_KEYS,
    JIELAN_1581_RULE_SET_ID,
    JIELAN_1581_RULE_SET_VERSION,
    JIELAN_1581_RUNTIME_RESOLVER_ID,
    JIELAN_1581_RUNTIME_RESOLVER_VERSION,
    JIELAN_1581_SELECTION_STATUS,
    resolve_jielan_1581_source_scoped_candidate,
)

from .local_app import MAX_REQUEST_BYTES, LocalCombinedAppRequestError


LOCAL_ZIWEI_JIELAN_1581_CANDIDATE_SCHEMA = (
    "ZIWEI-BAZI-COMBINED-LOCAL-ZIWEI-JIELAN-1581-HISTORICAL-CANDIDATE-R1"
)


class ZiweiJielan1581HistoricalCandidateLocalMixin:
    """Read-only Jielan 1581 natal historical-candidate sidecar."""

    def resolve_ziwei_jielan_1581_candidate_payload(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        combined_resolution, expected_ziwei_hash, bundle = (
            self._resolve_ziwei_sidecar_source(
                payload,
                source_unavailable_code=(
                    "LOCAL_APP_ZIWEI_JIELAN_1581_CANDIDATE_SOURCE_UNAVAILABLE"
                ),
            )
        )
        structure = bundle.candidate.chart.structure
        resolved = resolve_jielan_1581_source_scoped_candidate(
            year_stem=structure.ziwei_birth_year_stem,
            year_branch=structure.ziwei_birth_year_branch,
            birth_hour_branch=structure.birth_hour_branch.branch,
            life_palace_branch=structure.life_address.branch,
            bureau_element=structure.bureau.element,
            sex=bundle.candidate.sex.value,
        )
        if bundle.bundle_hash != expected_ziwei_hash:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_JIELAN_1581_CANDIDATE_SOURCE_BINDING_MISMATCH",
                (
                    f"combined={expected_ziwei_hash};"
                    f"controller_bundle={bundle.bundle_hash}"
                ),
                status=500,
            )

        facts = resolved.get("facts", {})
        released_facts = {
            key: facts[key]
            for key in JIELAN_1581_PRODUCT_FACT_KEYS
            if key in facts
        }
        if tuple(released_facts) != JIELAN_1581_PRODUCT_FACT_KEYS:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_ZIWEI_JIELAN_1581_CANDIDATE_FACT_SET_MISMATCH",
                (
                    f"released={tuple(released_facts)} "
                    f"expected={JIELAN_1581_PRODUCT_FACT_KEYS}"
                ),
                status=500,
            )

        source_bazi = combined_resolution.get("bazi_bundle")
        return {
            "schema": LOCAL_ZIWEI_JIELAN_1581_CANDIDATE_SCHEMA,
            "source_combined_manifest_hash": combined_resolution["manifest_hash"],
            "source_ziwei_bundle_hash": expected_ziwei_hash,
            "source_bazi_bundle_hash": (
                source_bazi["bundle_hash"] if source_bazi is not None else None
            ),
            "source_natal_fact_hash": bundle.candidate.hashes.fact_hash,
            "source_natal_computation_hash": bundle.candidate.hashes.computation_hash,
            "candidate_profile": {
                "candidate_api_id": JIELAN_1581_CANDIDATE_API_ID,
                "candidate_api_version": JIELAN_1581_CANDIDATE_API_VERSION,
                "rule_set_id": JIELAN_1581_RULE_SET_ID,
                "rule_set_version": JIELAN_1581_RULE_SET_VERSION,
                "selection_status": JIELAN_1581_SELECTION_STATUS,
                "runtime_resolver_id": JIELAN_1581_RUNTIME_RESOLVER_ID,
                "runtime_resolver_version": JIELAN_1581_RUNTIME_RESOLVER_VERSION,
                "source_id": resolved["source_id"],
                "registry_hash": resolved["registry_hash"],
                "candidate_runtime_hash": resolved["runtime_hash"],
                "released_fact_keys": JIELAN_1581_PRODUCT_FACT_KEYS,
                "production_winner_selected": False,
                "production_profile_changed": False,
            },
            "input_snapshot": json_value(resolved["inputs"]),
            "released_facts": json_value(released_facts),
        }


class _ZiweiJielan1581HistoricalCandidateHandlerMixin:
    application: ZiweiJielan1581HistoricalCandidateLocalMixin

    def do_POST(self) -> None:  # noqa: N802
        if urlsplit(self.path).path != "/api/ziwei-jielan-1581-candidate":
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
            response = self.application.resolve_ziwei_jielan_1581_candidate_payload(
                payload
            )
        except LocalCombinedAppRequestError as exc:
            self._error(exc)
            return
        self._send_json(200, response)
