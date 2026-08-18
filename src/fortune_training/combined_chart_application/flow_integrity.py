from __future__ import annotations

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .flow_models import (
    COMBINED_TARGET_FLOW_ALGORITHM_ID,
    COMBINED_TARGET_FLOW_ALGORITHM_VERSION,
    COMBINED_TARGET_FLOW_SCHEMA,
    CombinedTargetFlowIntegrityReport,
    CombinedTargetFlowResolution,
)


def combined_target_flow_source_fact_hash(
    resolution: CombinedTargetFlowResolution,
) -> str:
    return object_sha256(
        {
            "base_combined_manifest_hash": resolution.base_combined_manifest_hash,
            "ziwei_bundle_hash": resolution.ziwei_bundle_hash,
            "bazi_base_bundle_hash": resolution.bazi_base_bundle_hash,
            "bazi_target_flow_source_fact_hash": (
                resolution.bazi_target_flow_source_fact_hash
            ),
            "target_coordinate_fact_hash": resolution.target_coordinate_fact_hash,
        }
    )


def combined_target_flow_view_hash(resolution: CombinedTargetFlowResolution) -> str:
    return object_sha256(
        {
            "composition_semantics": resolution.composition_semantics,
            "ziwei_selection": {
                "daxian_frame_id": resolution.ziwei_selected_daxian_frame_id,
                "annual_year": resolution.ziwei_selected_annual_year,
                "minor_limit_age": resolution.ziwei_selected_minor_limit_age,
            },
            "target_input": json_value(resolution.target_input),
            "bazi_target_flow_view_hash": resolution.bazi_target_flow_view_hash,
        }
    )


def combined_target_flow_bundle_hash(
    resolution: CombinedTargetFlowResolution,
) -> str:
    return object_sha256(
        {
            "schema": resolution.schema,
            "source_fact_hash": resolution.source_fact_hash,
            "view_hash": resolution.view_hash,
            "combined_profile": [
                resolution.combined_profile_id,
                resolution.combined_profile_version,
            ],
            "composition_semantics": resolution.composition_semantics,
            "base_combined_status": resolution.base_combined_status,
            "ziwei_resolution_status": resolution.ziwei_resolution_status,
            "bazi_target_flow_status": resolution.bazi_target_flow_status,
            "bazi_target_flow_bundle_hash": resolution.bazi_target_flow_bundle_hash,
            "target_coordinate_computation_hash": (
                resolution.target_coordinate_computation_hash
            ),
            "target_coordinate_profile": [
                resolution.target_coordinate_profile_id,
                resolution.target_coordinate_profile_version,
            ],
            "bazi_dayun_count": resolution.bazi_dayun_count,
            "algorithm_id": COMBINED_TARGET_FLOW_ALGORITHM_ID,
            "algorithm_version": COMBINED_TARGET_FLOW_ALGORITHM_VERSION,
        }
    )


def validate_combined_target_flow_resolution(
    resolution: CombinedTargetFlowResolution,
) -> CombinedTargetFlowIntegrityReport:
    diagnostics: list[str] = []
    if resolution.schema != COMBINED_TARGET_FLOW_SCHEMA:
        diagnostics.append("RESOLUTION_SCHEMA_MISMATCH")
    if resolution.composition_semantics != "INDEPENDENT_BUNDLE_IDENTITY_COMPOSITION_ONLY":
        diagnostics.append("COMPOSITION_SEMANTICS_MISMATCH")
    if resolution.base_combined_status not in {
        "RESOLVED_BOTH",
        "UNCERTAINTY_PRESENT",
    }:
        diagnostics.append("BASE_COMBINED_STATUS_NOT_BOTH")
    if resolution.ziwei_resolution_status not in {"RESOLVED", "MULTI_CANDIDATE"}:
        diagnostics.append("ZIWEI_RESOLUTION_STATUS_INVALID")
    if resolution.bazi_target_flow_status not in {"RESOLVED", "MULTI_CANDIDATE"}:
        diagnostics.append("BAZI_TARGET_FLOW_STATUS_INVALID")
    expected_status = (
        "RESOLVED"
        if resolution.base_combined_status == "RESOLVED_BOTH"
        and resolution.ziwei_resolution_status == "RESOLVED"
        and resolution.bazi_target_flow_status == "RESOLVED"
        else "UNCERTAINTY_PRESENT"
    )
    if resolution.status != expected_status:
        diagnostics.append("RESOLUTION_STATUS_MISMATCH")
    if resolution.bazi_dayun_count < 1:
        diagnostics.append("BAZI_DAYUN_COUNT_INVALID")
    if not resolution.base_combined_manifest_hash:
        diagnostics.append("BASE_COMBINED_MANIFEST_HASH_MISSING")
    if not resolution.ziwei_bundle_hash:
        diagnostics.append("ZIWEI_BUNDLE_HASH_MISSING")
    if not resolution.bazi_base_bundle_hash:
        diagnostics.append("BAZI_BASE_BUNDLE_HASH_MISSING")
    if not resolution.bazi_target_flow_bundle_hash:
        diagnostics.append("BAZI_TARGET_FLOW_BUNDLE_HASH_MISSING")

    if resolution.source_fact_hash != combined_target_flow_source_fact_hash(resolution):
        diagnostics.append("SOURCE_FACT_HASH_MISMATCH")
    if resolution.view_hash != combined_target_flow_view_hash(resolution):
        diagnostics.append("VIEW_HASH_MISMATCH")
    if resolution.bundle_hash != combined_target_flow_bundle_hash(resolution):
        diagnostics.append("BUNDLE_HASH_MISMATCH")

    return CombinedTargetFlowIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )
