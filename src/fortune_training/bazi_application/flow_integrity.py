from __future__ import annotations

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .flow_models import (
    FLOW_APPLICATION_ALGORITHM_ID,
    FLOW_APPLICATION_ALGORITHM_VERSION,
    FLOW_APPLICATION_SCHEMA,
    FLOW_APPLICATION_VIEW_SCHEMA,
    BaziApplicationFlowCandidate,
    BaziApplicationFlowIntegrityReport,
    BaziApplicationFlowResolution,
)


def application_flow_candidate_id(candidate: BaziApplicationFlowCandidate) -> str:
    return "BAZI-APPLICATION-FLOW-CANDIDATE:" + object_sha256(
        {
            "natal_candidate_index": candidate.natal_candidate_index,
            "source_temporal_candidate_indices": list(
                candidate.source_temporal_candidate_indices
            ),
            "source_application_candidate_ids": list(
                candidate.source_application_candidate_ids
            ),
            "source_flow_candidate_index": candidate.source_flow_candidate_index,
            "source_target_coordinate_candidate_index": (
                candidate.source_target_coordinate_candidate_index
            ),
            "target_coordinate_candidate_id": candidate.target_coordinate_candidate_id,
            "natal_fact_hash": candidate.natal_fact_hash,
            "temporal_fact_hash": candidate.temporal_fact_hash,
            "flow_fact_hash": candidate.flow_fact_hash,
            "flow_computation_hash": candidate.flow_computation_hash,
            "daily_hourly_fact_hash": candidate.daily_hourly_fact_hash,
            "daily_hourly_computation_hash": candidate.daily_hourly_computation_hash,
            "view_hash": candidate.view_hash,
        }
    )


def application_flow_source_fact_hash(
    resolution: BaziApplicationFlowResolution,
) -> str:
    return object_sha256(
        {
            "base_application_source_fact_hash": resolution.base_application_source_fact_hash,
            "target_coordinate_fact_hash": resolution.target_coordinate_fact_hash,
            "candidate_facts": [
                {
                    "natal_candidate_index": row.natal_candidate_index,
                    "source_temporal_candidate_indices": list(
                        row.source_temporal_candidate_indices
                    ),
                    "source_flow_candidate_index": row.source_flow_candidate_index,
                    "source_target_coordinate_candidate_index": (
                        row.source_target_coordinate_candidate_index
                    ),
                    "target_coordinate_candidate_id": (
                        row.target_coordinate_candidate_id
                    ),
                    "natal_fact_hash": row.natal_fact_hash,
                    "temporal_fact_hash": row.temporal_fact_hash,
                    "flow_fact_hash": row.flow_fact_hash,
                    "daily_hourly_fact_hash": row.daily_hourly_fact_hash,
                }
                for row in resolution.candidates
            ],
        }
    )


def application_flow_view_hash(resolution: BaziApplicationFlowResolution) -> str:
    return object_sha256(
        {
            "view_schema": FLOW_APPLICATION_VIEW_SCHEMA,
            "candidate_view_hashes": [row.view_hash for row in resolution.candidates],
        }
    )


def application_flow_bundle_hash(resolution: BaziApplicationFlowResolution) -> str:
    return object_sha256(
        {
            "source_fact_hash": resolution.source_fact_hash,
            "view_hash": resolution.view_hash,
            "base_application_bundle_hash": resolution.base_application_bundle_hash,
            "target_coordinate_computation_hash": (
                resolution.target_coordinate_computation_hash
            ),
            "application_profile": [
                resolution.application_profile_id,
                resolution.application_profile_version,
            ],
            "natal_profile": [
                resolution.natal_profile_id,
                resolution.natal_profile_version,
            ],
            "temporal_profile": [
                resolution.temporal_profile_id,
                resolution.temporal_profile_version,
            ],
            "target_coordinate_profile": [
                resolution.target_coordinate_profile_id,
                resolution.target_coordinate_profile_version,
            ],
            "dayun_count": resolution.dayun_count,
            "target_input": json_value(resolution.target_input),
            "algorithm_id": FLOW_APPLICATION_ALGORITHM_ID,
            "algorithm_version": FLOW_APPLICATION_ALGORITHM_VERSION,
            "candidate_ids": [row.candidate_id for row in resolution.candidates],
            "candidate_computation_hashes": [
                {
                    "flow": row.flow_computation_hash,
                    "daily_hourly": row.daily_hourly_computation_hash,
                }
                for row in resolution.candidates
            ],
        }
    )


def validate_application_flow_resolution(
    resolution: BaziApplicationFlowResolution,
) -> BaziApplicationFlowIntegrityReport:
    diagnostics: list[str] = []

    if resolution.schema != FLOW_APPLICATION_SCHEMA:
        diagnostics.append("RESOLUTION_SCHEMA_MISMATCH")
    expected_status = "RESOLVED" if len(resolution.candidates) == 1 else "MULTI_CANDIDATE"
    if not resolution.candidates:
        diagnostics.append("NO_APPLICATION_FLOW_CANDIDATES")
    elif resolution.status != expected_status:
        diagnostics.append("RESOLUTION_STATUS_MISMATCH")
    if resolution.diagnostics:
        diagnostics.append("RESOLVED_WITH_DIAGNOSTICS")
    if resolution.target_coordinate_status == "FAILED":
        diagnostics.append("TARGET_COORDINATE_STATUS_FAILED")
    if resolution.dayun_count < 1:
        diagnostics.append("INVALID_DAYUN_COUNT")
    if resolution.target_coordinate_sample_count < 1:
        diagnostics.append("INVALID_TARGET_SAMPLE_COUNT")
    if resolution.target_coordinate_ambiguous_sample_count < 0:
        diagnostics.append("INVALID_TARGET_AMBIGUOUS_SAMPLE_COUNT")
    if resolution.target_coordinate_effective_uncertainty_seconds_each_side < 0:
        diagnostics.append("INVALID_TARGET_UNCERTAINTY")

    seen_ids: set[str] = set()
    seen_source_keys: set[tuple[int, tuple[int, ...], int, int, str]] = set()
    for index, candidate in enumerate(resolution.candidates):
        prefix = f"CANDIDATE:{index}"
        if candidate.candidate_id in seen_ids:
            diagnostics.append(f"{prefix}:DUPLICATE_CANDIDATE_ID")
        seen_ids.add(candidate.candidate_id)
        if not candidate.source_temporal_candidate_indices:
            diagnostics.append(f"{prefix}:EMPTY_TEMPORAL_LINEAGE")
        if len(set(candidate.source_temporal_candidate_indices)) != len(
            candidate.source_temporal_candidate_indices
        ):
            diagnostics.append(f"{prefix}:DUPLICATE_TEMPORAL_LINEAGE_INDEX")
        if len(candidate.source_application_candidate_ids) != len(
            candidate.source_temporal_candidate_indices
        ):
            diagnostics.append(f"{prefix}:APPLICATION_TEMPORAL_LINEAGE_COUNT_MISMATCH")
        if candidate.source_flow_candidate_index < 0:
            diagnostics.append(f"{prefix}:INVALID_FLOW_INDEX")
        if candidate.source_target_coordinate_candidate_index < 0:
            diagnostics.append(f"{prefix}:INVALID_TARGET_INDEX")

        source_key = (
            candidate.natal_candidate_index,
            candidate.source_temporal_candidate_indices,
            candidate.source_flow_candidate_index,
            candidate.source_target_coordinate_candidate_index,
            candidate.target_coordinate_candidate_id,
        )
        if source_key in seen_source_keys:
            diagnostics.append(f"{prefix}:DUPLICATE_SOURCE_LINEAGE")
        seen_source_keys.add(source_key)

        expected_view_hash = object_sha256(
            {"view_schema": candidate.view_schema, "view": candidate.view}
        )
        if candidate.view_schema != FLOW_APPLICATION_VIEW_SCHEMA:
            diagnostics.append(f"{prefix}:VIEW_SCHEMA_MISMATCH")
        if candidate.view_hash != expected_view_hash:
            diagnostics.append(f"{prefix}:VIEW_HASH_MISMATCH")
        if candidate.candidate_id != application_flow_candidate_id(candidate):
            diagnostics.append(f"{prefix}:CANDIDATE_ID_MISMATCH")

        target = candidate.view.get("target", {})
        lineage = candidate.view.get("lineage", {})
        hashes = candidate.view.get("source_hashes", {})
        integrity = candidate.view.get("integrity", {})
        if target.get("target_coordinate_candidate_index") != (
            candidate.source_target_coordinate_candidate_index
        ):
            diagnostics.append(f"{prefix}:VIEW_TARGET_INDEX_LINEAGE_MISMATCH")
        if target.get("target_coordinate_candidate_id") != (
            candidate.target_coordinate_candidate_id
        ):
            diagnostics.append(f"{prefix}:VIEW_TARGET_ID_LINEAGE_MISMATCH")
        if target.get("target_place") != resolution.target_input.target_place:
            diagnostics.append(f"{prefix}:VIEW_TARGET_PLACE_MISMATCH")
        if target.get("longitude") != resolution.target_input.longitude:
            diagnostics.append(f"{prefix}:VIEW_TARGET_LONGITUDE_MISMATCH")
        if target.get("timezone_id") != resolution.target_input.timezone_id:
            diagnostics.append(f"{prefix}:VIEW_TARGET_TIMEZONE_MISMATCH")

        if lineage.get("natal_candidate_index") != candidate.natal_candidate_index:
            diagnostics.append(f"{prefix}:VIEW_NATAL_INDEX_LINEAGE_MISMATCH")
        if tuple(lineage.get("source_temporal_candidate_indices", ())) != (
            candidate.source_temporal_candidate_indices
        ):
            diagnostics.append(f"{prefix}:VIEW_TEMPORAL_INDEX_LINEAGE_MISMATCH")
        if tuple(lineage.get("source_application_candidate_ids", ())) != (
            candidate.source_application_candidate_ids
        ):
            diagnostics.append(f"{prefix}:VIEW_APPLICATION_ID_LINEAGE_MISMATCH")
        if lineage.get("source_flow_candidate_index") != (
            candidate.source_flow_candidate_index
        ):
            diagnostics.append(f"{prefix}:VIEW_FLOW_INDEX_LINEAGE_MISMATCH")
        if lineage.get("source_target_coordinate_candidate_index") != (
            candidate.source_target_coordinate_candidate_index
        ):
            diagnostics.append(f"{prefix}:VIEW_TARGET_SOURCE_INDEX_LINEAGE_MISMATCH")

        expected_hashes = {
            "natal_fact_hash": candidate.natal_fact_hash,
            "temporal_fact_hash": candidate.temporal_fact_hash,
            "flow_fact_hash": candidate.flow_fact_hash,
            "flow_computation_hash": candidate.flow_computation_hash,
            "target_coordinate_fact_hash": resolution.target_coordinate_fact_hash,
            "target_coordinate_computation_hash": (
                resolution.target_coordinate_computation_hash
            ),
            "daily_hourly_fact_hash": candidate.daily_hourly_fact_hash,
            "daily_hourly_computation_hash": candidate.daily_hourly_computation_hash,
        }
        if hashes != expected_hashes:
            diagnostics.append(f"{prefix}:VIEW_SOURCE_HASH_LINEAGE_MISMATCH")
        if integrity != {
            "target_coordinate": "PASS",
            "flow": "PASS",
            "daily_hourly": "PASS",
        }:
            diagnostics.append(f"{prefix}:VIEW_UPSTREAM_INTEGRITY_NOT_PASS")

    expected_source_fact_hash = application_flow_source_fact_hash(resolution)
    if resolution.source_fact_hash != expected_source_fact_hash:
        diagnostics.append("SOURCE_FACT_HASH_MISMATCH")
    expected_view_hash = application_flow_view_hash(resolution)
    if resolution.view_hash != expected_view_hash:
        diagnostics.append("AGGREGATE_VIEW_HASH_MISMATCH")
    expected_bundle_hash = application_flow_bundle_hash(resolution)
    if resolution.bundle_hash != expected_bundle_hash:
        diagnostics.append("BUNDLE_HASH_MISMATCH")

    return BaziApplicationFlowIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )
