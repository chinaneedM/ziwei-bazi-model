from __future__ import annotations

from datetime import timedelta

from fortune_training.bazi_target_temporal import (
    ResolvedTargetTemporalCoordinateProfile,
    TargetTemporalCoordinateFoundation,
    TargetTemporalCoordinateResolution,
    validate_target_temporal_resolution,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.calendar_foundation import ZiweiCalendarResolver
from fortune_training.util import object_sha256
from fortune_training.ziwei_application import (
    ApplicationChartBundle,
    ApplicationResolutionError,
    validate_application_bundle,
)
from fortune_training.ziwei_chart import ZiweiTargetTemporalEngine, ZiweiTemporalEngine

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
            "ziwei_calendar_date_policy": candidate.ziwei_calendar_date_policy,
            "ziwei_day_boundary_policy": candidate.ziwei_day_boundary_policy,
            "effective_lunar_year": candidate.effective_lunar_year,
            "effective_lunar_month": candidate.effective_lunar_month,
            "effective_lunar_day": candidate.effective_lunar_day,
            "effective_lunar_is_leap_month": candidate.effective_lunar_is_leap_month,
            "monthly_projection_status": candidate.monthly_projection_status,
            "monthly_frame_id": candidate.monthly_frame_id,
            "monthly_ganzhi": candidate.monthly_ganzhi,
            "monthly_active_address_branch": candidate.monthly_active_address_branch,
            "daily_projection_status": candidate.daily_projection_status,
            "daily_frame_id": candidate.daily_frame_id,
            "daily_effective_gregorian_date": candidate.daily_effective_gregorian_date,
            "daily_ganzhi": candidate.daily_ganzhi,
            "daily_active_address_branch": candidate.daily_active_address_branch,
            "daily_designation_overlay": [json_value(row) for row in candidate.daily_designation_overlay],
            "daily_rule_id": candidate.daily_rule_id,
            "daily_source_refs": candidate.daily_source_refs,
            "daily_transformation_status": candidate.daily_transformation_status,
            "daily_transformation_rule_set_id": candidate.daily_transformation_rule_set_id,
            "daily_transformation_rule_set_version": candidate.daily_transformation_rule_set_version,
            "daily_transformations": [json_value(row) for row in candidate.daily_transformations],
            "daily_transformation_source_refs": candidate.daily_transformation_source_refs,
            "hourly_projection_status": candidate.hourly_projection_status,
            "hourly_method_candidates": [json_value(row) for row in candidate.hourly_method_candidates],
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

    target_temporal = ZiweiTargetTemporalEngine()
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
        profile = ziwei_bundle.calculation_profile
        resolver = ZiweiCalendarResolver()
        calendar_result = resolver.resolve(
            target_candidate.sample_reported_local_datetime.date(),
            target_candidate.local_apparent_solar_datetime,
            calendar_date_policy=(
                profile.time_calendar_policies.ziwei_calendar_date_policy
            ),
            life_body_leap_month_policy=(
                profile.time_calendar_policies.ziwei_life_body_leap_month_policy
            ),
        )
        lunar = calendar_result.effective_ziwei_lunar_date
        if (
            profile.ziwei_day_boundary_policy == "ZI_START_23"
            and target_candidate.local_apparent_solar_datetime.hour == 23
        ):
            lunar = resolver.calendar.from_gregorian_date(
                target_candidate.local_apparent_solar_datetime.date()
                + timedelta(days=1)
            )
        if lunar.is_leap_month:
            monthly = None
            monthly_status = "LEAP_MONTH_UNRESOLVED_NO_FRAME"
            daily = None
            daily_status = "PARENT_LEAP_MONTH_UNRESOLVED_NO_FRAME"
        else:
            monthly = ZiweiTemporalEngine().monthly_frame(
                ziwei_bundle.temporal_context,
                profile,
                annual,
                lunar.month,
            )
            monthly_status = "REGULAR_LUNAR_MONTH_RESOLVED"
            daily = target_temporal.daily_frame(
                monthly,
                effective_gregorian_date=lunar.source_gregorian_date,
                effective_lunar_day=lunar.day,
                profile=profile,
                placements=ziwei_bundle.temporal_context.placements,
            )
            daily_status = "REGULAR_LUNAR_DAY_RESOLVED"
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
            "ziwei_calendar_date_policy": (
                profile.time_calendar_policies.ziwei_calendar_date_policy
            ),
            "ziwei_day_boundary_policy": profile.ziwei_day_boundary_policy,
            "effective_lunar_year": lunar.year,
            "effective_lunar_month": lunar.month,
            "effective_lunar_day": lunar.day,
            "effective_lunar_is_leap_month": lunar.is_leap_month,
            "monthly_projection_status": monthly_status,
            "monthly_frame_id": monthly.frame_id if monthly is not None else None,
            "monthly_ganzhi": monthly.month_ganzhi if monthly is not None else None,
            "monthly_active_address_branch": (
                monthly.active_address.branch if monthly is not None else None
            ),
            "daily_projection_status": daily_status,
            "daily_frame_id": daily.frame_id if daily is not None else None,
            "daily_effective_gregorian_date": (
                daily.effective_gregorian_date.isoformat() if daily is not None else None
            ),
            "daily_ganzhi": daily.day_ganzhi if daily is not None else None,
            "daily_active_address_branch": (
                daily.active_address.branch if daily is not None else None
            ),
            "daily_designation_overlay": daily.designation_overlay if daily is not None else (),
            "daily_rule_id": daily.rule_id if daily is not None else None,
            "daily_source_refs": daily.source_refs if daily is not None else (),
            "daily_transformation_status": (
                daily.transformation_status
                if daily is not None
                else "PARENT_DAILY_FRAME_UNRESOLVED"
            ),
            "daily_transformation_rule_set_id": (
                daily.transformation_rule_set_id if daily is not None else None
            ),
            "daily_transformation_rule_set_version": (
                daily.transformation_rule_set_version if daily is not None else None
            ),
            "daily_transformations": daily.transformations if daily is not None else (),
            "daily_transformation_source_refs": (
                daily.transformation_source_refs if daily is not None else ()
            ),
            "hourly_projection_status": "CANDIDATES_PRESERVED_NO_SELECTED_FRAME",
        }
        for field_name, expected_value in expected.items():
            if getattr(projected, field_name) != expected_value:
                diagnostics.append(f"CANDIDATE_{index}_{field_name.upper()}_MISMATCH")
        hourly_expected = target_temporal.hourly_method_candidates(
            target_utc=target_candidate.target_utc,
            local_apparent_solar_datetime=target_candidate.local_apparent_solar_datetime,
            ziwei_day_boundary_policy=profile.ziwei_day_boundary_policy,
            profile=profile,
            placements=ziwei_bundle.temporal_context.placements,
        )
        if len(projected.hourly_method_candidates) != len(hourly_expected):
            diagnostics.append(f"CANDIDATE_{index}_HOURLY_CANDIDATE_COUNT_MISMATCH")
        for hourly_index, expected_hourly in enumerate(hourly_expected):
            if hourly_index >= len(projected.hourly_method_candidates):
                break
            actual_hourly = projected.hourly_method_candidates[hourly_index]
            hourly_fields = {
                "candidate_id": expected_hourly.candidate_id,
                "time_standard": expected_hourly.time_standard,
                "source_local_datetime": expected_hourly.source_local_datetime,
                "ziwei_day_boundary_policy": expected_hourly.ziwei_day_boundary_policy,
                "effective_gregorian_date": expected_hourly.effective_gregorian_date.isoformat(),
                "day_ganzhi": expected_hourly.day_ganzhi,
                "hour_branch": expected_hourly.hour_branch,
                "hour_ganzhi": expected_hourly.hour_ganzhi,
                "frame_status": expected_hourly.frame_status,
                "active_address_branch": expected_hourly.active_address.branch,
                "designation_overlay": expected_hourly.designation_overlay,
                "active_address_rule_id": expected_hourly.active_address_rule_id,
                "active_address_source_refs": expected_hourly.active_address_source_refs,
                "transformation_status": expected_hourly.transformation_status,
                "transformation_rule_set_id": expected_hourly.transformation_rule_set_id,
                "transformation_rule_set_version": expected_hourly.transformation_rule_set_version,
                "transformations": expected_hourly.transformations,
                "transformation_source_refs": expected_hourly.transformation_source_refs,
                "rule_id": expected_hourly.rule_id,
                "authority_status": expected_hourly.authority_status,
                "source_refs": expected_hourly.source_refs,
            }
            for field_name, expected_value in hourly_fields.items():
                if getattr(actual_hourly, field_name) != expected_value:
                    diagnostics.append(
                        f"CANDIDATE_{index}_HOURLY_{hourly_index}_{field_name.upper()}_MISMATCH"
                    )
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
