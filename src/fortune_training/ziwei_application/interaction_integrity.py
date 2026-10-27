from __future__ import annotations

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256
from fortune_training.ziwei_structural.r5 import (
    RESOLVED_MEMBER_OFFSETS,
    RESOLVED_MEMBER_ROLE_BY_OFFSET,
)

from .interaction_models import (
    SANHE_INTERACTION_ALGORITHM_ID,
    SANHE_INTERACTION_ALGORITHM_VERSION,
    SANHE_INTERACTION_MODE,
    SANHE_INTERACTION_SCHEMA,
    SanheInteractionIntegrityReport,
    SanheInteractionResolution,
)
from .models import ApplicationChartBundle
from .service import ApplicationResolutionError, validate_application_bundle


def sanhe_interaction_source_fact_hash(
    resolution: SanheInteractionResolution,
) -> str:
    return object_sha256(
        {
            "source_application_bundle_hash": resolution.source_application_bundle_hash,
            "r2_fact_hash": resolution.r2_fact_hash,
            "r3_fact_hash": resolution.r3_fact_hash,
            "r4_fact_hash": resolution.r4_fact_hash,
            "r5_fact_hash": resolution.r5_fact_hash,
        }
    )


def sanhe_interaction_view_hash(resolution: SanheInteractionResolution) -> str:
    return object_sha256(
        {
            "interaction_mode": resolution.interaction_mode,
            "selection": {
                "daxian_frame_id": resolution.selected_daxian_frame_id,
                "annual_year": resolution.selected_annual_year,
                "minor_limit_age": resolution.selected_minor_limit_age,
                "origin_designation_id": resolution.selected_origin_designation_id,
                "origin_address": json_value(resolution.selected_origin_address),
            },
            "relative_roles": json_value(resolution.relative_roles),
            "sanfang_sizheng_frame": json_value(resolution.sanfang_sizheng_frame),
        }
    )


def sanhe_interaction_bundle_hash(resolution: SanheInteractionResolution) -> str:
    return object_sha256(
        {
            "schema": resolution.schema,
            "status": resolution.status,
            "source_fact_hash": resolution.source_fact_hash,
            "view_hash": resolution.view_hash,
            "source_application_resolution_status": (
                resolution.source_application_resolution_status
            ),
            "r2_computation_hash": resolution.r2_computation_hash,
            "r3_computation_hash": resolution.r3_computation_hash,
            "r4_computation_hash": resolution.r4_computation_hash,
            "r5_computation_hash": resolution.r5_computation_hash,
            "algorithm_id": SANHE_INTERACTION_ALGORITHM_ID,
            "algorithm_version": SANHE_INTERACTION_ALGORITHM_VERSION,
        }
    )


def validate_sanhe_interaction_resolution(
    bundle: ApplicationChartBundle,
    resolution: SanheInteractionResolution,
) -> SanheInteractionIntegrityReport:
    diagnostics: list[str] = []
    try:
        validate_application_bundle(bundle)
    except ApplicationResolutionError as exc:
        diagnostics.append(
            f"SOURCE_APPLICATION_BUNDLE_INVALID:{exc.diagnostic_code}:{exc}"
        )

    if resolution.schema != SANHE_INTERACTION_SCHEMA:
        diagnostics.append("RESOLUTION_SCHEMA_MISMATCH")
    if resolution.status != "RESOLVED":
        diagnostics.append("RESOLUTION_STATUS_MISMATCH")
    if resolution.interaction_mode != SANHE_INTERACTION_MODE:
        diagnostics.append("INTERACTION_MODE_MISMATCH")
    if resolution.source_application_bundle_hash != bundle.bundle_hash:
        diagnostics.append("SOURCE_APPLICATION_BUNDLE_HASH_MISMATCH")
    if resolution.source_application_resolution_status != bundle.resolution_status:
        diagnostics.append("SOURCE_APPLICATION_STATUS_MISMATCH")
    if resolution.selected_daxian_frame_id != bundle.selected_daxian_frame_id:
        diagnostics.append("DAXIAN_SELECTION_MISMATCH")
    if resolution.selected_annual_year != bundle.selected_annual_year:
        diagnostics.append("ANNUAL_SELECTION_MISMATCH")
    if resolution.selected_minor_limit_age != bundle.selected_minor_limit_age:
        diagnostics.append("MINOR_LIMIT_SELECTION_MISMATCH")

    expected_hashes = {
        "r2_fact_hash": bundle.r2_state.hashes.fact_hash,
        "r2_computation_hash": bundle.r2_state.hashes.computation_hash,
        "r3_fact_hash": bundle.r3_state.hashes.fact_hash,
        "r3_computation_hash": bundle.r3_state.hashes.computation_hash,
        "r4_fact_hash": bundle.r4_state.hashes.fact_hash,
        "r4_computation_hash": bundle.r4_state.hashes.computation_hash,
        "r5_fact_hash": bundle.r5_state.hashes.fact_hash,
        "r5_computation_hash": bundle.r5_state.hashes.computation_hash,
    }
    for field_name, expected in expected_hashes.items():
        if getattr(resolution, field_name) != expected:
            diagnostics.append(f"{field_name.upper()}_MISMATCH")

    r2_rows = tuple(
        row
        for row in bundle.r2_state.frame_facts
        if row.origin_designation_id == resolution.selected_origin_designation_id
    )
    if len(r2_rows) != 12:
        diagnostics.append(f"R2_ORIGIN_CARDINALITY_MISMATCH:{len(r2_rows)}")
    if resolution.relative_roles != r2_rows:
        diagnostics.append("R2_RELATIVE_ROLE_SUBSET_MISMATCH")
    r2_addresses = {row.origin_address for row in r2_rows}
    if len(r2_addresses) != 1:
        diagnostics.append(f"R2_ORIGIN_ADDRESS_CARDINALITY_MISMATCH:{len(r2_addresses)}")
    elif resolution.selected_origin_address not in r2_addresses:
        diagnostics.append("R2_ORIGIN_ADDRESS_MISMATCH")

    r4_frames = tuple(
        row
        for row in bundle.r4_state.sanfang_sizheng_frames
        if row.origin_designation_id == resolution.selected_origin_designation_id
    )
    if len(r4_frames) != 1:
        diagnostics.append(f"R4_ORIGIN_CARDINALITY_MISMATCH:{len(r4_frames)}")

    r5_frames = tuple(
        row
        for row in bundle.r5_state.frames
        if row.origin_designation_id == resolution.selected_origin_designation_id
    )
    if len(r5_frames) != 1:
        diagnostics.append(f"R5_ORIGIN_CARDINALITY_MISMATCH:{len(r5_frames)}")
    elif resolution.sanfang_sizheng_frame != r5_frames[0]:
        diagnostics.append("R5_FRAME_MISMATCH")
    elif resolution.sanfang_sizheng_frame.origin_address != resolution.selected_origin_address:
        diagnostics.append("R5_ORIGIN_ADDRESS_MISMATCH")

    if len(resolution.sanfang_sizheng_frame.members) != 4:
        diagnostics.append("R5_MEMBER_COUNT_MISMATCH")
    else:
        offsets = tuple(row.member_offset for row in resolution.sanfang_sizheng_frame.members)
        if offsets != RESOLVED_MEMBER_OFFSETS:
            diagnostics.append("R5_MEMBER_OFFSETS_MISMATCH")
        for row in resolution.sanfang_sizheng_frame.members:
            if row.semantic_role != RESOLVED_MEMBER_ROLE_BY_OFFSET.get(row.member_offset):
                diagnostics.append(f"R5_MEMBER_ROLE_MISMATCH:{row.member_offset}")

    if resolution.source_fact_hash != sanhe_interaction_source_fact_hash(resolution):
        diagnostics.append("SOURCE_FACT_HASH_MISMATCH")
    if resolution.view_hash != sanhe_interaction_view_hash(resolution):
        diagnostics.append("VIEW_HASH_MISMATCH")
    if resolution.bundle_hash != sanhe_interaction_bundle_hash(resolution):
        diagnostics.append("BUNDLE_HASH_MISMATCH")

    return SanheInteractionIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )
