from __future__ import annotations

from fortune_training.bazi_target_temporal import (
    ResolvedTargetTemporalCoordinateProfile,
    TargetTemporalCoordinateFoundation,
    TargetTemporalCoordinateResolution,
    validate_target_temporal_resolution,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256
from fortune_training.ziwei_application import (
    ApplicationChartBundle,
    ApplicationResolutionError,
    validate_application_bundle,
)

from .shared_time_models import (
    SHARED_ZIWEI_SELECTOR_PROJECTION_ALGORITHM_ID,
    SHARED_ZIWEI_SELECTOR_PROJECTION_ALGORITHM_VERSION,
    SHARED_ZIWEI_SELECTOR_PROJECTION_HASH_ALGORITHM_ID,
    SHARED_ZIWEI_SELECTOR_PROJECTION_HASH_ALGORITHM_VERSION,
    SHARED_ZIWEI_SELECTOR_PROJECTION_SCHEMA,
    SharedZiweiSelectorProjectionCandidate,
    SharedZiweiSelectorProjectionHashBundle,
    SharedZiweiSelectorProjectionIntegrityReport,
    SharedZiweiSelectorProjectionResolution,
)


def shared_selector_candidate_hash(candidate: SharedZiweiSelectorProjectionCandidate) -> str:
    return object_sha256(
        {
            "source_target_candidate_index": candidate.source_target_candidate_index,
            "source_target_candidate_id": candidate.source_target_candidate_id,
            "source_sample_index": candidate.source_sample_index,
            "sample_reported_local_datetime": json_value(candidate.sample_reported_local_datetime),
            "target_utc": json_value(candidate.target_utc),
            "fold": candidate.fold,
            "civil_year": candidate.civil_year,
            "source_annual_frame_id": candidate.source_annual_frame_id,
            "annual_year": candidate.annual_year,
            "minor_limit_age": candidate.minor_limit_age,
            "daxian_frame_id": candidate.daxian_frame_id,
        }
    )


def shared_selector_hash_bundle(
    resolution: SharedZiweiSelectorProjectionResolution,
) -> SharedZiweiSelectorProjectionHashBundle:
    fact_hash = object_sha256(
        {
            "schema": resolution.schema,
            "status": resolution.status,
            "source_ziwei_application_bundle_hash": resolution.source_ziwei_application_bundle_hash,
            "source_ziwei_temporal_fact_hash": resolution.source_ziwei_temporal_fact_hash,
            "source_target_coordinate_fact_hash": resolution.source_target_coordinate_fact_hash,
            "candidates": [json_value(row) for row in resolution.candidates],
        }
    )
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "source_ziwei_temporal_computation_hash": resolution.source_ziwei_temporal_computation_hash,
            "source_target_coordinate_computation_hash": resolution.source_target_coordinate_computation_hash,
            "source_target_coordinate_profile_id": resolution.source_target_coordinate_profile_id,
            "source_target_coordinate_profile_version": resolution.source_target_coordinate_profile_version,
            "algorithm": (
                f"{SHARED_ZIWEI_SELECTOR_PROJECTION_ALGORITHM_ID}@"
                f"{SHARED_ZIWEI_SELECTOR_PROJECTION_ALGORITHM_VERSION}"
            ),
            "hash_algorithm": (
                f"{SHARED_ZIWEI_SELECTOR_PROJECTION_HASH_ALGORITHM_ID}@"
                f"{SHARED_ZIWEI_SELECTOR_PROJECTION_HASH_ALGORITHM_VERSION}"
            ),
        }
    )
    return SharedZiweiSelectorProjectionHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
    )


def validate_shared_ziwei_selector_projection(
    ziwei_bundle: ApplicationChartBundle,
    target_resolution: TargetTemporalCoordinateResolution,
    target_profile: ResolvedTargetTemporalCoordinateProfile,
    resolution: SharedZiweiSelectorProjectionResolution,
) -> SharedZiweiSelectorProjectionIntegrityReport:
    diagnostics: list[str] = []

    try:
        validate_application_bundle(ziwei_bundle)
    except ApplicationResolutionError as exc:
        diagnostics.append(f"SOURCE_ZIWEI_APPLICATION_INVALID:{exc.diagnostic_code}:{exc}")

    target_foundation = TargetTemporalCoordinateFoundation()
    target_report = validate_target_temporal_resolution(
        target_resolution,
        target_profile,
        target_foundation.civil,
        target_foundation.solar,
    )
    if target_report.status != "PASS":
        diagnostics.append("SOURCE_TARGET_COORDINATE_INVALID")
    if target_resolution.integrity != target_report:
        diagnostics.append("SOURCE_TARGET_EMBEDDED_INTEGRITY_MISMATCH")

    if resolution.schema != SHARED_ZIWEI_SELECTOR_PROJECTION_SCHEMA:
        diagnostics.append("RESOLUTION_SCHEMA_MISMATCH")
    expected_status = "RESOLVED" if resolution.candidates else "FAILED"
    if resolution.status != expected_status:
        diagnostics.append("RESOLUTION_STATUS_MISMATCH")

    expected_bindings = {
        "source_ziwei_application_bundle_hash": ziwei_bundle.bundle_hash,
        "source_ziwei_temporal_fact_hash": ziwei_bundle.temporal_hashes.fact_hash,
        "source_ziwei_temporal_computation_hash": ziwei_bundle.temporal_hashes.computation_hash,
        "source_target_coordinate_fact_hash": target_resolution.hashes.fact_hash,
        "source_target_coordinate_computation_hash": target_resolution.hashes.computation_hash,
        "source_target_coordinate_profile_id": target_resolution.profile_id,
        "source_target_coordinate_profile_version": target_resolution.profile_version,
    }
    for field_name, expected in expected_bindings.items():
        if getattr(resolution, field_name) != expected:
            diagnostics.append(f"{field_name.upper()}_MISMATCH")

    if (target_profile.profile_id, target_profile.profile_version) != (
        target_resolution.profile_id,
        target_resolution.profile_version,
    ):
        diagnostics.append("TARGET_PROFILE_LINEAGE_MISMATCH")

    annual_by_year: dict[int, list[object]] = {}
    for frame in ziwei_bundle.temporal_state.annual_frames:
        annual_by_year.setdefault(frame.absolute_year, []).append(frame)

    if len(resolution.candidates) != len(target_resolution.candidates):
        diagnostics.append(
            f"PROJECTION_CANDIDATE_COUNT_MISMATCH:{len(resolution.candidates)}:"
            f"{len(target_resolution.candidates)}"
        )

    for index, target_candidate in enumerate(target_resolution.candidates):
        if index >= len(resolution.candidates):
            break
        projected = resolution.candidates[index]
        civil_year = target_candidate.sample_reported_local_datetime.year
        matches = annual_by_year.get(civil_year, [])
        if len(matches) != 1:
            diagnostics.append(f"ANNUAL_FRAME_CARDINALITY_MISMATCH:{index}:{civil_year}:{len(matches)}")
            continue
        annual = matches[0]
        expected = {
            "source_target_candidate_index": index,
            "source_target_candidate_id": target_candidate.candidate_id,
            "source_sample_index": target_candidate.source_sample_index,
            "sample_reported_local_datetime": target_candidate.sample_reported_local_datetime,
            "target_utc": target_candidate.target_utc,
            "fold": target_candidate.fold,
            "civil_year": civil_year,
            "source_annual_frame_id": annual.frame_id,
            "annual_year": annual.absolute_year,
            "minor_limit_age": annual.nominal_age,
            "daxian_frame_id": annual.parent_daxian_frame_id,
        }
        for field_name, expected_value in expected.items():
            if getattr(projected, field_name) != expected_value:
                diagnostics.append(f"CANDIDATE_{index}_{field_name.upper()}_MISMATCH")
        if projected.candidate_hash != shared_selector_candidate_hash(projected):
            diagnostics.append(f"CANDIDATE_{index}_HASH_MISMATCH")

    if len(resolution.candidates) > len(target_resolution.candidates):
        diagnostics.append("EXTRA_PROJECTION_CANDIDATES")

    expected_hashes = shared_selector_hash_bundle(resolution)
    if resolution.hashes != expected_hashes:
        diagnostics.append("PROJECTION_HASH_MISMATCH")

    return SharedZiweiSelectorProjectionIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )
