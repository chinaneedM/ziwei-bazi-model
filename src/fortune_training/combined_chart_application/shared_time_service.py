from __future__ import annotations

from dataclasses import replace

from fortune_training.bazi_target_temporal import (
    ResolvedTargetTemporalCoordinateProfile,
    TargetTemporalCoordinateFoundation,
    TargetTemporalCoordinateResolution,
    validate_target_temporal_resolution,
)
from fortune_training.ziwei_application import (
    ApplicationChartBundle,
    ApplicationResolutionError,
    validate_application_bundle,
)

from .shared_time_integrity import (
    shared_selector_candidate_hash,
    shared_selector_hash_bundle,
    validate_shared_ziwei_selector_projection,
)
from .shared_time_models import (
    SHARED_ZIWEI_SELECTOR_PROJECTION_SCHEMA,
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

        candidates: list[SharedZiweiSelectorProjectionCandidate] = []
        for index, target_candidate in enumerate(target_resolution.candidates):
            civil_year = target_candidate.sample_reported_local_datetime.year
            annual_matches = annual_by_year.get(civil_year, [])
            if len(annual_matches) != 1:
                raise SharedZiweiSelectorProjectionError(
                    "SHARED_ZIWEI_ANNUAL_FRAME_NOT_EXACTLY_ONE",
                    f"candidate_index={index};civil_year={civil_year};matches={len(annual_matches)}",
                )
            annual = annual_matches[0]
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
                daxian_frame_id=annual.parent_daxian_frame_id,
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
