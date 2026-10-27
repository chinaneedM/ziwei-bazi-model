from __future__ import annotations

from fortune_training.bazi_application.temporal_shensha import (
    TEMPORAL_SHENSHA_PROFILE_ID,
    TEMPORAL_SHENSHA_PROFILE_VERSION,
    temporal_shensha_projection_hashes,
)
from fortune_training.util import object_sha256

from .models import (
    TEMPORAL_SHENSHA_SIDECAR_ALGORITHM_ID,
    TEMPORAL_SHENSHA_SIDECAR_ALGORITHM_VERSION,
    TEMPORAL_SHENSHA_SIDECAR_PROFILE_ID,
    TEMPORAL_SHENSHA_SIDECAR_PROFILE_VERSION,
    TEMPORAL_SHENSHA_SIDECAR_SCHEMA,
    TemporalShenshaSidecarCandidate,
    TemporalShenshaSidecarIntegrityReport,
    TemporalShenshaSidecarResolution,
)


EXPECTED_PROJECTION_POLICY = "ENGINEERING_TARGET_MATCH_NOT_CLASSICAL_TEMPORAL_APPLICABILITY"
EXPECTED_SELECTION_SEMANTICS = "SOURCE_CANDIDATES_PRESERVED_NO_WINNER"
EXPECTED_SEMANTIC_SCOPE = "TARGET_IDENTITY_MATCH_ONLY_NO_AUSPICIOUSNESS_OR_TEMPORAL_RULE_ADJUDICATION"


def temporal_shensha_sidecar_candidate_fact_hash(
    candidate: TemporalShenshaSidecarCandidate,
) -> str:
    return object_sha256(
        {
            "source_bazi_target_flow_candidate_id": candidate.source_bazi_target_flow_candidate_id,
            "source_bazi_target_flow_candidate_index": candidate.source_bazi_target_flow_candidate_index,
            "source_flow_candidate_index": candidate.source_flow_candidate_index,
            "source_target_coordinate_candidate_index": candidate.source_target_coordinate_candidate_index,
            "target_coordinate_candidate_id": candidate.target_coordinate_candidate_id,
            "source_application_candidate_ids": list(candidate.source_application_candidate_ids),
            "source_shensha_hash": candidate.source_shensha_hash,
            "projection_fact_hash": candidate.projection.get("fact_hash"),
        }
    )


def temporal_shensha_sidecar_candidate_computation_hash(
    candidate: TemporalShenshaSidecarCandidate,
) -> str:
    return object_sha256(
        {
            "fact_hash": candidate.fact_hash,
            "source_application_view_hashes": list(candidate.source_application_view_hashes),
            "projection_computation_hash": candidate.projection.get("computation_hash"),
            "algorithm": f"{TEMPORAL_SHENSHA_SIDECAR_ALGORITHM_ID}@{TEMPORAL_SHENSHA_SIDECAR_ALGORITHM_VERSION}",
        }
    )


def temporal_shensha_sidecar_candidate_id(
    candidate: TemporalShenshaSidecarCandidate,
) -> str:
    return "BAZI-TEMPORAL-SHENSHA-SIDECAR-CANDIDATE:" + object_sha256(
        {
            "source_bazi_target_flow_candidate_id": candidate.source_bazi_target_flow_candidate_id,
            "source_application_candidate_ids": list(candidate.source_application_candidate_ids),
            "target_coordinate_candidate_id": candidate.target_coordinate_candidate_id,
            "fact_hash": candidate.fact_hash,
            "computation_hash": candidate.computation_hash,
        }
    )


def temporal_shensha_sidecar_fact_hash(
    resolution: TemporalShenshaSidecarResolution,
) -> str:
    return object_sha256(
        {
            "base_application_source_fact_hash": resolution.base_application_source_fact_hash,
            "bazi_target_flow_source_fact_hash": resolution.bazi_target_flow_source_fact_hash,
            "candidate_facts": [
                {
                    "candidate_id": row.candidate_id,
                    "source_shensha_hash": row.source_shensha_hash,
                    "projection_fact_hash": row.projection.get("fact_hash"),
                    "fact_hash": row.fact_hash,
                }
                for row in resolution.candidates
            ],
        }
    )


def temporal_shensha_sidecar_computation_hash(
    resolution: TemporalShenshaSidecarResolution,
) -> str:
    return object_sha256(
        {
            "fact_hash": resolution.fact_hash,
            "base_application_bundle_hash": resolution.base_application_bundle_hash,
            "bazi_target_flow_bundle_hash": resolution.bazi_target_flow_bundle_hash,
            "candidate_computation_hashes": [row.computation_hash for row in resolution.candidates],
            "algorithm": f"{TEMPORAL_SHENSHA_SIDECAR_ALGORITHM_ID}@{TEMPORAL_SHENSHA_SIDECAR_ALGORITHM_VERSION}",
        }
    )


def temporal_shensha_sidecar_bundle_hash(
    resolution: TemporalShenshaSidecarResolution,
) -> str:
    return object_sha256(
        {
            "schema": resolution.schema,
            "profile": [resolution.projection_profile_id, resolution.projection_profile_version],
            "fact_hash": resolution.fact_hash,
            "computation_hash": resolution.computation_hash,
            "candidate_ids": [row.candidate_id for row in resolution.candidates],
        }
    )


def validate_temporal_shensha_sidecar_resolution(
    resolution: TemporalShenshaSidecarResolution,
) -> TemporalShenshaSidecarIntegrityReport:
    diagnostics: list[str] = []
    if resolution.schema != TEMPORAL_SHENSHA_SIDECAR_SCHEMA:
        diagnostics.append("RESOLUTION_SCHEMA_MISMATCH")
    if resolution.projection_profile_id != TEMPORAL_SHENSHA_SIDECAR_PROFILE_ID:
        diagnostics.append("SIDECAR_PROFILE_ID_MISMATCH")
    if resolution.projection_profile_version != TEMPORAL_SHENSHA_SIDECAR_PROFILE_VERSION:
        diagnostics.append("SIDECAR_PROFILE_VERSION_MISMATCH")
    if not resolution.candidates:
        diagnostics.append("NO_SIDECAR_CANDIDATES")
    else:
        expected_status = "RESOLVED" if len(resolution.candidates) == 1 else "MULTI_CANDIDATE"
        if resolution.status != expected_status:
            diagnostics.append("RESOLUTION_STATUS_MISMATCH")
    if resolution.diagnostics:
        diagnostics.append("RESOLVED_WITH_DIAGNOSTICS")

    seen_ids: set[str] = set()
    seen_source_ids: set[str] = set()
    seen_indices: set[int] = set()
    for index, candidate in enumerate(resolution.candidates):
        prefix = f"CANDIDATE:{index}"
        if candidate.candidate_id in seen_ids:
            diagnostics.append(f"{prefix}:DUPLICATE_CANDIDATE_ID")
        seen_ids.add(candidate.candidate_id)
        if candidate.source_bazi_target_flow_candidate_id in seen_source_ids:
            diagnostics.append(f"{prefix}:DUPLICATE_SOURCE_FLOW_CANDIDATE_ID")
        seen_source_ids.add(candidate.source_bazi_target_flow_candidate_id)
        if candidate.source_bazi_target_flow_candidate_index in seen_indices:
            diagnostics.append(f"{prefix}:DUPLICATE_SOURCE_FLOW_CANDIDATE_INDEX")
        seen_indices.add(candidate.source_bazi_target_flow_candidate_index)
        if candidate.source_bazi_target_flow_candidate_index < 0:
            diagnostics.append(f"{prefix}:INVALID_SOURCE_FLOW_CANDIDATE_INDEX")
        if candidate.source_flow_candidate_index < 0:
            diagnostics.append(f"{prefix}:INVALID_SOURCE_FLOW_INDEX")
        if candidate.source_target_coordinate_candidate_index < 0:
            diagnostics.append(f"{prefix}:INVALID_TARGET_INDEX")
        if not candidate.source_application_candidate_ids:
            diagnostics.append(f"{prefix}:EMPTY_SOURCE_APPLICATION_LINEAGE")
        if len(candidate.source_application_candidate_ids) != len(candidate.source_application_view_hashes):
            diagnostics.append(f"{prefix}:SOURCE_APPLICATION_VIEW_HASH_COUNT_MISMATCH")
        if len(set(candidate.source_application_candidate_ids)) != len(candidate.source_application_candidate_ids):
            diagnostics.append(f"{prefix}:DUPLICATE_SOURCE_APPLICATION_ID")

        projection = candidate.projection
        try:
            projection_fact_hash, projection_computation_hash = temporal_shensha_projection_hashes(projection)
        except (KeyError, TypeError, ValueError):
            diagnostics.append(f"{prefix}:PROJECTION_HASH_REPLAY_INVALID")
        else:
            if projection.get("fact_hash") != projection_fact_hash:
                diagnostics.append(f"{prefix}:PROJECTION_FACT_HASH_MISMATCH")
            if projection.get("computation_hash") != projection_computation_hash:
                diagnostics.append(f"{prefix}:PROJECTION_COMPUTATION_HASH_MISMATCH")
        if projection.get("profile_id") != TEMPORAL_SHENSHA_PROFILE_ID:
            diagnostics.append(f"{prefix}:PROJECTION_PROFILE_ID_MISMATCH")
        if projection.get("profile_version") != TEMPORAL_SHENSHA_PROFILE_VERSION:
            diagnostics.append(f"{prefix}:PROJECTION_PROFILE_VERSION_MISMATCH")
        if projection.get("projection_policy") != EXPECTED_PROJECTION_POLICY:
            diagnostics.append(f"{prefix}:PROJECTION_POLICY_MISMATCH")
        if projection.get("selection_semantics") != EXPECTED_SELECTION_SEMANTICS:
            diagnostics.append(f"{prefix}:SELECTION_SEMANTICS_MISMATCH")
        if projection.get("semantic_scope") != EXPECTED_SEMANTIC_SCOPE:
            diagnostics.append(f"{prefix}:SEMANTIC_SCOPE_MISMATCH")

        if candidate.fact_hash != temporal_shensha_sidecar_candidate_fact_hash(candidate):
            diagnostics.append(f"{prefix}:FACT_HASH_MISMATCH")
        if candidate.computation_hash != temporal_shensha_sidecar_candidate_computation_hash(candidate):
            diagnostics.append(f"{prefix}:COMPUTATION_HASH_MISMATCH")
        if candidate.candidate_id != temporal_shensha_sidecar_candidate_id(candidate):
            diagnostics.append(f"{prefix}:CANDIDATE_ID_MISMATCH")

    if seen_indices and seen_indices != set(range(len(resolution.candidates))):
        diagnostics.append("SOURCE_FLOW_CANDIDATE_INDEX_COVERAGE_MISMATCH")
    if resolution.fact_hash != temporal_shensha_sidecar_fact_hash(resolution):
        diagnostics.append("FACT_HASH_MISMATCH")
    if resolution.computation_hash != temporal_shensha_sidecar_computation_hash(resolution):
        diagnostics.append("COMPUTATION_HASH_MISMATCH")
    if resolution.bundle_hash != temporal_shensha_sidecar_bundle_hash(resolution):
        diagnostics.append("BUNDLE_HASH_MISMATCH")

    return TemporalShenshaSidecarIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )
