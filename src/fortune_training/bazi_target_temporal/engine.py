from __future__ import annotations

from dataclasses import replace
from datetime import timezone

from fortune_training.calendar_foundation import CivilTimeResolver, SolarTimeEngine, TimeCalendarFoundation
from fortune_training.calendar_foundation.models import CivilTimeStatus, InputTimeType

from .integrity import target_candidate_id, target_hash_bundle, validate_target_temporal_resolution
from .models import (
    TargetTemporalCoordinateCandidate,
    TargetTemporalCoordinateResolution,
    TargetTemporalHashBundle,
    TargetTemporalIntegrityReport,
    TargetTemporalUnresolvedSample,
)
from .profile import (
    ResolvedTargetTemporalCoordinateProfile,
    bazi_target_temporal_coordinate_r1_profile,
)


class TargetTemporalCoordinateFoundation:
    schema = "BAZI-TARGET-TEMPORAL-COORDINATE-RESOLUTION-R1"

    def __init__(
        self,
        civil: CivilTimeResolver | None = None,
        solar: SolarTimeEngine | None = None,
    ) -> None:
        self.civil = civil or CivilTimeResolver()
        self.solar = solar or SolarTimeEngine()

    def resolve(
        self,
        target_input,
        profile: ResolvedTargetTemporalCoordinateProfile | None = None,
    ) -> TargetTemporalCoordinateResolution:
        resolved_profile = (profile or bazi_target_temporal_coordinate_r1_profile()).validate()
        sampled_wall_times = TimeCalendarFoundation._sample_wall_times(target_input)
        candidates: list[TargetTemporalCoordinateCandidate] = []
        unresolved_samples: list[TargetTemporalUnresolvedSample] = []
        ambiguous_sample_count = 0

        for sample_index, wall_time in enumerate(sampled_wall_times):
            civil_resolution = self.civil.resolve_local_time(
                wall_time,
                target_input.timezone_id,
                input_time_type=InputTimeType.CIVIL,
                ambiguous_time_policy=resolved_profile.ambiguous_time_policy,
            )
            if civil_resolution.status is CivilTimeStatus.AMBIGUOUS:
                ambiguous_sample_count += 1
            if civil_resolution.status in {
                CivilTimeStatus.NONEXISTENT,
                CivilTimeStatus.NOT_APPLICABLE,
            }:
                unresolved_samples.append(
                    TargetTemporalUnresolvedSample(
                        source_sample_index=sample_index,
                        sample_reported_local_datetime=wall_time,
                        civil_status=civil_resolution.status.value,
                        timezone_id=civil_resolution.timezone_id,
                        tzdb_version=civil_resolution.tzdb_version,
                        historical_confidence=civil_resolution.historical_confidence.value,
                        warnings=civil_resolution.warnings,
                    )
                )
                continue

            legal = (
                (civil_resolution.selected_candidate,)
                if civil_resolution.selected_candidate is not None
                else civil_resolution.candidates
            )
            for civil_candidate in legal:
                if civil_candidate is None:
                    continue
                solar = self.solar.resolve(
                    civil_candidate.utc_instant,
                    target_input.longitude,
                    civil_candidate.utc_offset_seconds,
                )
                candidate = TargetTemporalCoordinateCandidate(
                    candidate_id="",
                    source_sample_index=sample_index,
                    sample_reported_local_datetime=wall_time,
                    civil_status=civil_resolution.status.value,
                    timezone_id=civil_resolution.timezone_id,
                    tzdb_version=civil_resolution.tzdb_version,
                    historical_confidence=civil_resolution.historical_confidence.value,
                    warnings=civil_resolution.warnings,
                    target_utc=civil_candidate.utc_instant.astimezone(timezone.utc),
                    fold=civil_candidate.fold,
                    utc_offset_seconds=civil_candidate.utc_offset_seconds,
                    daylight_saving_seconds=civil_candidate.daylight_saving_seconds,
                    timezone_abbreviation=civil_candidate.timezone_abbreviation,
                    local_mean_solar_datetime=solar.local_mean_solar_datetime,
                    local_apparent_solar_datetime=solar.local_apparent_solar_datetime,
                    longitude_correction_seconds_from_civil=solar.longitude_correction_seconds_from_civil,
                    equation_of_time_seconds=solar.equation_of_time_seconds,
                    apparent_solar_offset_from_utc_seconds=solar.apparent_solar_offset_from_utc_seconds,
                    solar_time_algorithm_id=solar.algorithm_id,
                    solar_time_algorithm_version=solar.algorithm_version,
                    time_scale_assumption=solar.time_scale_assumption,
                )
                candidates.append(replace(candidate, candidate_id=target_candidate_id(candidate)))

        if not candidates:
            status = "FAILED"
            diagnostics = ("TARGET_CIVIL_TIME_UNRESOLVED",)
        elif (
            len(candidates) == 1
            and not unresolved_samples
            and ambiguous_sample_count == 0
            and target_input.effective_uncertainty_seconds == 0
        ):
            status = "RESOLVED"
            diagnostics = ()
        else:
            status = "MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY"
            diagnostics = ()

        pending_integrity = TargetTemporalIntegrityReport(status="PENDING", diagnostics=())
        pending_hashes = TargetTemporalHashBundle(fact_hash="", computation_hash="")
        provisional = TargetTemporalCoordinateResolution(
            schema=self.schema,
            status=status,
            target_input=target_input,
            profile_id=resolved_profile.profile_id,
            profile_version=resolved_profile.profile_version,
            effective_uncertainty_seconds_each_side=target_input.effective_uncertainty_seconds,
            sample_count=len(sampled_wall_times),
            ambiguous_sample_count=ambiguous_sample_count,
            candidates=tuple(candidates),
            unresolved_samples=tuple(unresolved_samples),
            diagnostics=diagnostics,
            integrity=pending_integrity,
            hashes=pending_hashes,
        )
        integrity = validate_target_temporal_resolution(
            provisional,
            resolved_profile,
            self.civil,
            self.solar,
        )
        if integrity.status != "PASS":
            integrity_diagnostics = tuple(
                f"INTEGRITY:{row.code}:{row.path}:{row.detail}"
                for row in integrity.diagnostics
            )
            provisional = replace(
                provisional,
                status="FAILED",
                diagnostics=provisional.diagnostics + integrity_diagnostics,
                integrity=integrity,
            )
            return replace(
                provisional,
                hashes=target_hash_bundle(provisional, resolved_profile),
            )

        provisional = replace(provisional, integrity=integrity)
        return replace(
            provisional,
            hashes=target_hash_bundle(provisional, resolved_profile),
        )
