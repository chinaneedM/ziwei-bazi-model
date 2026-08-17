from __future__ import annotations

from typing import Iterable

from fortune_training.calendar_foundation import CivilTimeResolver, SolarTimeEngine
from fortune_training.calendar_foundation.models import CivilTimeStatus, json_value
from fortune_training.util import object_sha256

from .integrity import target_coordinate_hash_bundle, validate_target_coordinate
from .models import (
    TargetTemporalCoordinate,
    TargetTemporalCoordinateResolution,
    TargetTemporalInput,
    TargetTemporalProfile,
    TargetTemporalResolvedCandidate,
    TargetTemporalUnresolvedSample,
)
from .profile import validate_target_temporal_profile
from .sampling import sample_target_wall_times


class TargetTemporalCoordinateEngine:
    schema = "TARGET-TEMPORAL-COORDINATE-RESOLUTION-R1"

    def __init__(
        self,
        civil: CivilTimeResolver | None = None,
        solar: SolarTimeEngine | None = None,
    ) -> None:
        self.civil = civil or CivilTimeResolver()
        self.solar = solar or SolarTimeEngine()

    @staticmethod
    def _resolution_hashes(
        target_input: TargetTemporalInput,
        profile: TargetTemporalProfile,
        candidates: Iterable[TargetTemporalResolvedCandidate],
        unresolved: Iterable[TargetTemporalUnresolvedSample],
    ) -> tuple[str, str]:
        candidate_rows = tuple(candidates)
        unresolved_rows = tuple(unresolved)
        fact_hash = object_sha256(
            {
                "target_input": json_value(target_input),
                "candidate_fact_hashes": [row.hashes.fact_hash for row in candidate_rows],
                "unresolved_samples": json_value(unresolved_rows),
            }
        )
        computation_hash = object_sha256(
            {
                "fact_hash": fact_hash,
                "profile": json_value(profile),
                "candidate_computation_hashes": [row.hashes.computation_hash for row in candidate_rows],
            }
        )
        return fact_hash, computation_hash

    def resolve(
        self,
        target_input: TargetTemporalInput,
        profile: TargetTemporalProfile,
    ) -> TargetTemporalCoordinateResolution:
        validated_profile = validate_target_temporal_profile(profile)
        sampled_wall_times = sample_target_wall_times(target_input)
        ambiguous_sample_count = 0
        unresolved: list[TargetTemporalUnresolvedSample] = []
        resolved_candidates: list[TargetTemporalResolvedCandidate] = []

        for sample_index, wall_time in enumerate(sampled_wall_times):
            civil_resolution = self.civil.resolve_wall_time(
                wall_time,
                target_input.timezone_id,
                input_time_type=target_input.input_time_type,
                ambiguous_time_policy=validated_profile.civil_ambiguous_time_policy,
            )
            if civil_resolution.status is CivilTimeStatus.AMBIGUOUS:
                ambiguous_sample_count += 1
            if civil_resolution.status in {CivilTimeStatus.NONEXISTENT, CivilTimeStatus.NOT_APPLICABLE}:
                unresolved.append(
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

            for civil_candidate_index, civil_candidate in enumerate(civil_resolution.candidates):
                solar_time = self.solar.resolve(
                    civil_candidate.utc_instant,
                    target_input.longitude,
                    civil_candidate.utc_offset_seconds,
                )
                coordinate_id_payload = {
                    "target_input": json_value(target_input),
                    "source_sample_index": sample_index,
                    "source_civil_candidate_index": civil_candidate_index,
                    "sample_reported_local_datetime": json_value(wall_time),
                    "civil_candidate": json_value(civil_candidate),
                    "solar_time": json_value(solar_time),
                }
                coordinate = TargetTemporalCoordinate(
                    coordinate_id=f"TARGET-COORDINATE:{object_sha256(coordinate_id_payload)}",
                    source_sample_index=sample_index,
                    source_civil_candidate_index=civil_candidate_index,
                    sample_reported_local_datetime=wall_time,
                    target_place=target_input.target_place,
                    latitude=target_input.latitude,
                    longitude=target_input.longitude,
                    timezone_id=civil_resolution.timezone_id,
                    tzdb_version=civil_resolution.tzdb_version,
                    historical_confidence=civil_resolution.historical_confidence.value,
                    warnings=civil_resolution.warnings,
                    civil_status=civil_resolution.status.value,
                    civil_candidate=civil_candidate,
                    solar_time=solar_time,
                )
                integrity = validate_target_coordinate(
                    target_input,
                    coordinate,
                    validated_profile,
                    self.civil,
                    self.solar,
                )
                if integrity.status != "PASS":
                    fact_hash, computation_hash = self._resolution_hashes(
                        target_input,
                        validated_profile,
                        (),
                        unresolved,
                    )
                    return TargetTemporalCoordinateResolution(
                        schema=self.schema,
                        status="FAILED",
                        target_input=target_input,
                        profile=validated_profile,
                        effective_uncertainty_seconds_each_side=target_input.effective_uncertainty_seconds,
                        sample_count=len(sampled_wall_times),
                        ambiguous_sample_count=ambiguous_sample_count,
                        legal_realization_count=0,
                        candidates=(),
                        unresolved_samples=tuple(unresolved),
                        events=(),
                        diagnostics=tuple(
                            f"INTEGRITY:{row.code}:{row.path}:{row.detail}" for row in integrity.diagnostics
                        ),
                        fact_hash=fact_hash,
                        computation_hash=computation_hash,
                    )
                hashes = target_coordinate_hash_bundle(target_input, coordinate, validated_profile)
                resolved_candidates.append(
                    TargetTemporalResolvedCandidate(
                        coordinate=coordinate,
                        integrity=integrity,
                        hashes=hashes,
                    )
                )

        if not resolved_candidates:
            status = "FAILED"
            events = ("TARGET_CIVIL_TIME_UNRESOLVED",)
            diagnostics = ("TARGET_CIVIL_TIME_UNRESOLVED",)
        elif len(resolved_candidates) > 1 or unresolved or ambiguous_sample_count:
            status = "MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY"
            events = ("TARGET_TIME_UNCERTAINTY_PRESERVED",)
            diagnostics = ()
        elif target_input.effective_uncertainty_seconds:
            status = "RESOLVED_RANGE_SINGLE_COORDINATE"
            events = ("TARGET_TIME_RANGE_SINGLE_COORDINATE",)
            diagnostics = ()
        else:
            status = "RESOLVED"
            events = ()
            diagnostics = ()

        fact_hash, computation_hash = self._resolution_hashes(
            target_input,
            validated_profile,
            resolved_candidates,
            unresolved,
        )
        return TargetTemporalCoordinateResolution(
            schema=self.schema,
            status=status,
            target_input=target_input,
            profile=validated_profile,
            effective_uncertainty_seconds_each_side=target_input.effective_uncertainty_seconds,
            sample_count=len(sampled_wall_times),
            ambiguous_sample_count=ambiguous_sample_count,
            legal_realization_count=len(resolved_candidates),
            candidates=tuple(resolved_candidates),
            unresolved_samples=tuple(unresolved),
            events=events,
            diagnostics=diagnostics,
            fact_hash=fact_hash,
            computation_hash=computation_hash,
        )
