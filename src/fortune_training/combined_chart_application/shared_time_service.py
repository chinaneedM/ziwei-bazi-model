from __future__ import annotations

from dataclasses import replace
from datetime import timedelta

from fortune_training.bazi_target_temporal import (
    ResolvedTargetTemporalCoordinateProfile,
    TargetTemporalCoordinateFoundation,
    TargetTemporalCoordinateResolution,
    validate_target_temporal_resolution,
)
from fortune_training.calendar_foundation import ZiweiCalendarResolver
from fortune_training.ziwei_application import (
    ApplicationChartBundle,
    ApplicationResolutionError,
    validate_application_bundle,
)
from fortune_training.ziwei_chart import (
    ZiweiTargetTemporalEngine,
    ZiweiTemporalEngine,
    resolve_jielan_1581_day_anchored_flow_hour_candidate,
    resolve_zhongzhou_leap_month_half_split_candidate,
)

from .shared_time_integrity import (
    project_shared_ziwei_minor_limit_ring_encounters,
    project_shared_ziwei_temporal_layer,
    shared_selector_candidate_hash,
    shared_selector_hash_bundle,
    validate_shared_ziwei_selector_projection,
)
from .shared_time_models import (
    SHARED_ZIWEI_SELECTOR_PROJECTION_SCHEMA,
    SharedZiweiHourlyMethodCandidate,
    SharedZiweiSelectorProjectionCandidate,
    SharedZiweiSelectorProjectionHashBundle,
    SharedZiweiSelectorProjectionIntegrityReport,
    SharedZiweiSelectorProjectionResolution,
)


class SharedZiweiSelectorProjectionError(ValueError):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


class SharedZiweiSelectorProjectionService:
    schema = SHARED_ZIWEI_SELECTOR_PROJECTION_SCHEMA

    @staticmethod
    def _effective_lunar_date_for_clock(
        ziwei_bundle,
        reported_civil_date,
        source_local_datetime,
    ):
        profile = ziwei_bundle.calculation_profile
        resolver = ZiweiCalendarResolver()
        resolved = resolver.resolve(
            reported_civil_date,
            source_local_datetime,
            calendar_date_policy=(
                profile.time_calendar_policies.ziwei_calendar_date_policy
            ),
            life_body_leap_month_policy=(
                profile.time_calendar_policies.ziwei_life_body_leap_month_policy
            ),
        )
        effective = resolved.effective_ziwei_lunar_date
        if (
            profile.ziwei_day_boundary_policy == "ZI_START_23"
            and source_local_datetime.hour == 23
        ):
            effective = resolver.calendar.from_gregorian_date(
                source_local_datetime.date() + timedelta(days=1)
            )
        return effective

    @classmethod
    def _effective_lunar_date(cls, ziwei_bundle, target_candidate):
        return cls._effective_lunar_date_for_clock(
            ziwei_bundle,
            target_candidate.sample_reported_local_datetime.date(),
            target_candidate.local_apparent_solar_datetime,
        )

    @staticmethod
    def _validate_upstream(
        ziwei_bundle: ApplicationChartBundle,
        target_resolution: TargetTemporalCoordinateResolution,
        target_profile: ResolvedTargetTemporalCoordinateProfile,
    ) -> None:
        try:
            validate_application_bundle(ziwei_bundle)
        except ApplicationResolutionError as exc:
            raise SharedZiweiSelectorProjectionError(
                "SHARED_ZIWEI_SOURCE_APPLICATION_INVALID",
                f"{exc.diagnostic_code}:{exc}",
            ) from exc

        try:
            target_profile.validate()
        except ValueError as exc:
            raise SharedZiweiSelectorProjectionError(
                "SHARED_ZIWEI_TARGET_PROFILE_INVALID",
                str(exc),
            ) from exc
        if (target_resolution.profile_id, target_resolution.profile_version) != (
            target_profile.profile_id,
            target_profile.profile_version,
        ):
            raise SharedZiweiSelectorProjectionError(
                "SHARED_ZIWEI_TARGET_PROFILE_LINEAGE_MISMATCH",
                f"resolution={target_resolution.profile_id}@{target_resolution.profile_version};"
                f"profile={target_profile.profile_id}@{target_profile.profile_version}",
            )

        foundation = TargetTemporalCoordinateFoundation()
        report = validate_target_temporal_resolution(
            target_resolution,
            target_profile,
            foundation.civil,
            foundation.solar,
        )
        if report.status != "PASS" or target_resolution.integrity != report:
            raise SharedZiweiSelectorProjectionError(
                "SHARED_ZIWEI_TARGET_COORDINATE_INVALID",
                ";".join(row.code for row in report.diagnostics) or "embedded integrity mismatch",
            )
        if not target_resolution.candidates:
            raise SharedZiweiSelectorProjectionError(
                "SHARED_ZIWEI_TARGET_CANDIDATE_REQUIRED",
                f"target status={target_resolution.status}",
            )

    def project(
        self,
        ziwei_bundle: ApplicationChartBundle,
        target_resolution: TargetTemporalCoordinateResolution,
        target_profile: ResolvedTargetTemporalCoordinateProfile,
    ) -> SharedZiweiSelectorProjectionResolution:
        self._validate_upstream(ziwei_bundle, target_resolution, target_profile)

        annual_by_year: dict[int, list[object]] = {}
        for frame in ziwei_bundle.temporal_state.annual_frames:
            annual_by_year.setdefault(frame.absolute_year, []).append(frame)
        daxian_by_id = {
            frame.frame_id: frame for frame in ziwei_bundle.temporal_state.daxian_frames
        }
        minor_by_age = {
            frame.nominal_age: frame
            for frame in ziwei_bundle.temporal_state.minor_limit_frames
        }

        candidates: list[SharedZiweiSelectorProjectionCandidate] = []
        target_temporal = ZiweiTargetTemporalEngine()
        temporal_engine = ZiweiTemporalEngine()
        for index, target_candidate in enumerate(target_resolution.candidates):
            civil_year = target_candidate.sample_reported_local_datetime.year
            annual_matches = annual_by_year.get(civil_year, [])
            if len(annual_matches) != 1:
                raise SharedZiweiSelectorProjectionError(
                    "SHARED_ZIWEI_ANNUAL_FRAME_NOT_EXACTLY_ONE",
                    f"candidate_index={index};civil_year={civil_year};matches={len(annual_matches)}",
                )
            annual = annual_matches[0]
            minor = minor_by_age.get(annual.nominal_age)
            if minor is None:
                raise SharedZiweiSelectorProjectionError(
                    "SHARED_ZIWEI_MINOR_LIMIT_FRAME_NOT_EXACTLY_ONE",
                    f"candidate_index={index};nominal_age={annual.nominal_age}",
                )
            daxian = (
                daxian_by_id.get(annual.parent_daxian_frame_id)
                if annual.parent_daxian_frame_id is not None
                else None
            )
            if annual.parent_daxian_frame_id is not None and daxian is None:
                raise SharedZiweiSelectorProjectionError(
                    "SHARED_ZIWEI_DAXIAN_FRAME_NOT_EXACTLY_ONE",
                    f"candidate_index={index};frame_id={annual.parent_daxian_frame_id}",
                )
            lunar = self._effective_lunar_date(ziwei_bundle, target_candidate)
            leap_month_candidate_status = "NOT_APPLICABLE_REGULAR_MONTH"
            leap_month_method_candidates: tuple[dict[str, object], ...] = ()
            if lunar.is_leap_month:
                monthly_status = "LEAP_MONTH_UNRESOLVED_NO_FRAME"
                monthly = None
                daily_status = "PARENT_LEAP_MONTH_UNRESOLVED_NO_FRAME"
                daily = None

                previous_month = temporal_engine.monthly_frame(
                    ziwei_bundle.temporal_context,
                    ziwei_bundle.calculation_profile,
                    annual,
                    lunar.month,
                )
                if lunar.month == 12:
                    following_matches = annual_by_year.get(annual.absolute_year + 1, [])
                    following_annual = following_matches[0] if len(following_matches) == 1 else None
                    following_month_number = 1
                else:
                    following_annual = annual
                    following_month_number = lunar.month + 1
                if following_annual is None:
                    leap_month_candidate_status = "FOLLOWING_REGULAR_MONTH_FRAME_UNAVAILABLE"
                else:
                    following_month = temporal_engine.monthly_frame(
                        ziwei_bundle.temporal_context,
                        ziwei_bundle.calculation_profile,
                        following_annual,
                        following_month_number,
                    )
                    leap_month_method_candidates = (
                        resolve_zhongzhou_leap_month_half_split_candidate(
                            leap_lunar_year=lunar.year,
                            leap_lunar_month=lunar.month,
                            leap_lunar_day=lunar.day,
                            previous_month_temporal_year=annual.absolute_year,
                            previous_month_number=lunar.month,
                            previous_month_frame_id=previous_month.frame_id,
                            previous_month_ganzhi=previous_month.month_ganzhi,
                            previous_month_active_branch=previous_month.active_address.branch,
                            following_month_temporal_year=following_annual.absolute_year,
                            following_month_number=following_month_number,
                            following_month_frame_id=following_month.frame_id,
                            following_month_ganzhi=following_month.month_ganzhi,
                            following_month_active_branch=following_month.active_address.branch,
                        ),
                    )
                    leap_month_candidate_status = "CANDIDATE_PRESERVED_NO_SELECTION"
            else:
                monthly_status = "REGULAR_LUNAR_MONTH_RESOLVED"
                monthly = temporal_engine.monthly_frame(
                    ziwei_bundle.temporal_context,
                    ziwei_bundle.calculation_profile,
                    annual,
                    lunar.month,
                )
                daily_status = "REGULAR_LUNAR_DAY_RESOLVED"
                daily = target_temporal.daily_frame(
                    monthly,
                    effective_gregorian_date=lunar.source_gregorian_date,
                    effective_lunar_day=lunar.day,
                    profile=ziwei_bundle.calculation_profile,
                    placements=ziwei_bundle.temporal_context.placements,
                )
            hourly_source_rows = target_temporal.hourly_method_candidates(
                target_utc=target_candidate.target_utc,
                local_apparent_solar_datetime=target_candidate.local_apparent_solar_datetime,
                ziwei_day_boundary_policy=(
                    ziwei_bundle.calculation_profile.ziwei_day_boundary_policy
                ),
                profile=ziwei_bundle.calculation_profile,
                placements=ziwei_bundle.temporal_context.placements,
            )
            hourly_candidates = tuple(
                SharedZiweiHourlyMethodCandidate(
                    candidate_id=row.candidate_id,
                    time_standard=row.time_standard,
                    source_local_datetime=row.source_local_datetime,
                    ziwei_day_boundary_policy=row.ziwei_day_boundary_policy,
                    effective_gregorian_date=row.effective_gregorian_date.isoformat(),
                    day_ganzhi=row.day_ganzhi,
                    hour_branch=row.hour_branch,
                    hour_ganzhi=row.hour_ganzhi,
                    frame_status=row.frame_status,
                    active_address_branch=(
                        row.active_address.branch if row.active_address is not None else None
                    ),
                    designation_overlay=row.designation_overlay,
                    active_address_rule_id=row.active_address_rule_id,
                    active_address_source_refs=row.active_address_source_refs,
                    auxiliary_status=row.auxiliary_status,
                    auxiliary_activations=row.auxiliary_activations,
                    auxiliary_source_refs=row.auxiliary_source_refs,
                    auxiliary_candidate_sets=row.auxiliary_candidate_sets,
                    transformation_status=row.transformation_status,
                    transformation_rule_set_id=row.transformation_rule_set_id,
                    transformation_rule_set_version=row.transformation_rule_set_version,
                    transformations=row.transformations,
                    transformation_source_refs=row.transformation_source_refs,
                    rule_id=row.rule_id,
                    authority_status=row.authority_status,
                    source_refs=row.source_refs,
                )
                for row in hourly_source_rows
            )

            historical_hourly_rows: list[dict[str, object]] = []
            for hourly_source in hourly_source_rows:
                hourly_lunar = self._effective_lunar_date_for_clock(
                    ziwei_bundle,
                    target_candidate.sample_reported_local_datetime.date(),
                    hourly_source.source_local_datetime,
                )
                if hourly_lunar.is_leap_month:
                    continue
                parent_annual_matches = annual_by_year.get(
                    hourly_lunar.source_gregorian_date.year,
                    [],
                )
                if len(parent_annual_matches) != 1:
                    continue
                parent_annual = parent_annual_matches[0]
                parent_month = temporal_engine.monthly_frame(
                    ziwei_bundle.temporal_context,
                    ziwei_bundle.calculation_profile,
                    parent_annual,
                    hourly_lunar.month,
                )
                parent_daily = target_temporal.daily_frame(
                    parent_month,
                    effective_gregorian_date=hourly_lunar.source_gregorian_date,
                    effective_lunar_day=hourly_lunar.day,
                    profile=ziwei_bundle.calculation_profile,
                    placements=ziwei_bundle.temporal_context.placements,
                )
                historical_hourly_rows.append(
                    resolve_jielan_1581_day_anchored_flow_hour_candidate(
                        parent_daily_frame_id=parent_daily.frame_id,
                        parent_daily_effective_gregorian_date=(
                            parent_daily.effective_gregorian_date
                        ),
                        parent_daily_active_branch=parent_daily.active_address.branch,
                        source_local_datetime=hourly_source.source_local_datetime,
                        reported_civil_date=(
                            target_candidate.sample_reported_local_datetime.date()
                        ),
                        ziwei_calendar_date_policy=(
                            ziwei_bundle.calculation_profile.time_calendar_policies
                            .ziwei_calendar_date_policy
                        ),
                        ziwei_day_boundary_policy=(
                            ziwei_bundle.calculation_profile.ziwei_day_boundary_policy
                        ),
                        time_standard=hourly_source.time_standard,
                    )
                )
            historical_hourly_method_candidates = tuple(historical_hourly_rows)
            historical_hourly_projection_status = (
                "CANDIDATES_PRESERVED_NO_SELECTED_FRAME"
                if historical_hourly_method_candidates
                else "NO_SOURCE_SCOPED_PARENT_DAILY_FRAME"
            )
            candidate = SharedZiweiSelectorProjectionCandidate(
                source_target_candidate_index=index,
                source_target_candidate_id=target_candidate.candidate_id,
                source_sample_index=target_candidate.source_sample_index,
                sample_reported_local_datetime=target_candidate.sample_reported_local_datetime,
                target_utc=target_candidate.target_utc,
                fold=target_candidate.fold,
                civil_year=civil_year,
                source_annual_frame_id=annual.frame_id,
                annual_year=annual.absolute_year,
                minor_limit_age=annual.nominal_age,
                minor_limit_ring_projection=(
                    project_shared_ziwei_minor_limit_ring_encounters(
                        minor,
                        ziwei_bundle.temporal_state,
                        ziwei_bundle.candidate.chart.rings,
                    )
                ),
                daxian_frame_id=annual.parent_daxian_frame_id,
                daxian_layer_projection=(
                    project_shared_ziwei_temporal_layer(
                        "DAXIAN", daxian, ziwei_bundle.temporal_state
                    )
                    if daxian is not None
                    else None
                ),
                annual_layer_projection=project_shared_ziwei_temporal_layer(
                    "ANNUAL", annual, ziwei_bundle.temporal_state
                ),
                ziwei_calendar_date_policy=(
                    ziwei_bundle.calculation_profile.time_calendar_policies.ziwei_calendar_date_policy
                ),
                ziwei_day_boundary_policy=(
                    ziwei_bundle.calculation_profile.ziwei_day_boundary_policy
                ),
                effective_lunar_year=lunar.year,
                effective_lunar_month=lunar.month,
                effective_lunar_day=lunar.day,
                effective_lunar_is_leap_month=lunar.is_leap_month,
                monthly_projection_status=monthly_status,
                monthly_frame_id=monthly.frame_id if monthly is not None else None,
                monthly_ganzhi=monthly.month_ganzhi if monthly is not None else None,
                monthly_active_address_branch=(
                    monthly.active_address.branch if monthly is not None else None
                ),
                monthly_layer_projection=(
                    project_shared_ziwei_temporal_layer(
                        "MONTH", monthly, ziwei_bundle.temporal_state
                    )
                    if monthly is not None
                    else None
                ),
                daily_projection_status=daily_status,
                daily_frame_id=daily.frame_id if daily is not None else None,
                daily_effective_gregorian_date=(
                    daily.effective_gregorian_date.isoformat() if daily is not None else None
                ),
                daily_ganzhi=daily.day_ganzhi if daily is not None else None,
                daily_active_address_branch=(
                    daily.active_address.branch if daily is not None else None
                ),
                daily_designation_overlay=(
                    daily.designation_overlay if daily is not None else ()
                ),
                daily_auxiliary_status=(
                    daily.auxiliary_status
                    if daily is not None
                    else "PARENT_DAILY_FRAME_UNRESOLVED"
                ),
                daily_auxiliary_activations=(
                    daily.auxiliary_activations if daily is not None else ()
                ),
                daily_auxiliary_source_refs=(
                    daily.auxiliary_source_refs if daily is not None else ()
                ),
                daily_auxiliary_candidate_sets=(
                    daily.auxiliary_candidate_sets if daily is not None else ()
                ),
                daily_rule_id=daily.rule_id if daily is not None else None,
                daily_source_refs=daily.source_refs if daily is not None else (),
                daily_transformation_status=(
                    daily.transformation_status
                    if daily is not None
                    else "PARENT_DAILY_FRAME_UNRESOLVED"
                ),
                daily_transformation_rule_set_id=(
                    daily.transformation_rule_set_id if daily is not None else None
                ),
                daily_transformation_rule_set_version=(
                    daily.transformation_rule_set_version if daily is not None else None
                ),
                daily_transformations=daily.transformations if daily is not None else (),
                daily_transformation_source_refs=(
                    daily.transformation_source_refs if daily is not None else ()
                ),
                hourly_projection_status="CANDIDATES_PRESERVED_NO_SELECTED_FRAME",
                hourly_method_candidates=hourly_candidates,
                historical_hourly_projection_status=historical_hourly_projection_status,
                historical_hourly_method_candidates=historical_hourly_method_candidates,
                leap_month_candidate_status=leap_month_candidate_status,
                leap_month_method_candidates=leap_month_method_candidates,
                candidate_hash="",
            )
            candidates.append(
                replace(candidate, candidate_hash=shared_selector_candidate_hash(candidate))
            )

        provisional = SharedZiweiSelectorProjectionResolution(
            schema=self.schema,
            status="RESOLVED",
            source_ziwei_application_bundle_hash=ziwei_bundle.bundle_hash,
            source_ziwei_temporal_fact_hash=ziwei_bundle.temporal_hashes.fact_hash,
            source_ziwei_temporal_computation_hash=ziwei_bundle.temporal_hashes.computation_hash,
            source_target_coordinate_fact_hash=target_resolution.hashes.fact_hash,
            source_target_coordinate_computation_hash=target_resolution.hashes.computation_hash,
            source_target_coordinate_profile_id=target_resolution.profile_id,
            source_target_coordinate_profile_version=target_resolution.profile_version,
            candidates=tuple(candidates),
            hashes=SharedZiweiSelectorProjectionHashBundle(fact_hash="", computation_hash=""),
            integrity=SharedZiweiSelectorProjectionIntegrityReport(status="PENDING", diagnostics=()),
        )
        provisional = replace(provisional, hashes=shared_selector_hash_bundle(provisional))
        report = validate_shared_ziwei_selector_projection(
            ziwei_bundle,
            target_resolution,
            target_profile,
            provisional,
        )
        if report.status != "PASS":
            raise SharedZiweiSelectorProjectionError(
                "SHARED_ZIWEI_PROJECTION_INTEGRITY_FAILED",
                ";".join(report.diagnostics),
            )
        return replace(provisional, integrity=report)
