from __future__ import annotations

from datetime import timezone

from fortune_training.calendar_foundation import CivilTimeResolver, SolarTimeEngine, TimeCalendarFoundation
from fortune_training.calendar_foundation.models import CivilTimeStatus, InputTimeType, json_value
from fortune_training.util import object_sha256

from .models import (
    TargetTemporalCoordinateCandidate,
    TargetTemporalCoordinateResolution,
    TargetTemporalHashBundle,
    TargetTemporalIntegrityDiagnostic,
    TargetTemporalIntegrityReport,
    TargetTemporalUnresolvedSample,
)
from .profile import ResolvedTargetTemporalCoordinateProfile


INTEGRITY_ALGORITHM_ID = "BAZI-TARGET-TEMPORAL-COORDINATE-INTEGRITY-R1"
INTEGRITY_ALGORITHM_VERSION = "1.0.0"
HASH_ALGORITHM_ID = "BAZI-TARGET-TEMPORAL-COORDINATE-HASH-R1"
HASH_ALGORITHM_VERSION = "1.0.0"


def _diag(rows: list[TargetTemporalIntegrityDiagnostic], code: str, path: str, detail: str) -> None:
    rows.append(TargetTemporalIntegrityDiagnostic(code=code, path=path, detail=detail))


def target_candidate_fact(candidate: TargetTemporalCoordinateCandidate) -> dict[str, object]:
    return {
        "source_sample_index": candidate.source_sample_index,
        "sample_reported_local_datetime": json_value(candidate.sample_reported_local_datetime),
        "civil_status": candidate.civil_status,
        "timezone_id": candidate.timezone_id,
        "tzdb_version": candidate.tzdb_version,
        "historical_confidence": candidate.historical_confidence,
        "warnings": list(candidate.warnings),
        "target_utc": json_value(candidate.target_utc),
        "fold": candidate.fold,
        "utc_offset_seconds": candidate.utc_offset_seconds,
        "daylight_saving_seconds": candidate.daylight_saving_seconds,
        "timezone_abbreviation": candidate.timezone_abbreviation,
        "local_mean_solar_datetime": json_value(candidate.local_mean_solar_datetime),
        "local_apparent_solar_datetime": json_value(candidate.local_apparent_solar_datetime),
        "longitude_correction_seconds_from_civil": candidate.longitude_correction_seconds_from_civil,
        "equation_of_time_seconds": candidate.equation_of_time_seconds,
        "apparent_solar_offset_from_utc_seconds": candidate.apparent_solar_offset_from_utc_seconds,
        "solar_time_algorithm_id": candidate.solar_time_algorithm_id,
        "solar_time_algorithm_version": candidate.solar_time_algorithm_version,
        "time_scale_assumption": candidate.time_scale_assumption,
    }


def target_candidate_id(candidate: TargetTemporalCoordinateCandidate) -> str:
    return "BAZI-TARGET-TEMPORAL-CANDIDATE:" + object_sha256(target_candidate_fact(candidate))


def unresolved_sample_fact(sample: TargetTemporalUnresolvedSample) -> dict[str, object]:
    return {
        "source_sample_index": sample.source_sample_index,
        "sample_reported_local_datetime": json_value(sample.sample_reported_local_datetime),
        "civil_status": sample.civil_status,
        "timezone_id": sample.timezone_id,
        "tzdb_version": sample.tzdb_version,
        "historical_confidence": sample.historical_confidence,
        "warnings": list(sample.warnings),
    }


def target_resolution_fact_projection(resolution: TargetTemporalCoordinateResolution) -> dict[str, object]:
    return {
        "schema": resolution.schema,
        "status": resolution.status,
        "target_input": json_value(resolution.target_input),
        "effective_uncertainty_seconds_each_side": resolution.effective_uncertainty_seconds_each_side,
        "sample_count": resolution.sample_count,
        "ambiguous_sample_count": resolution.ambiguous_sample_count,
        "candidates": [
            {"candidate_id": row.candidate_id, **target_candidate_fact(row)}
            for row in resolution.candidates
        ],
        "unresolved_samples": [unresolved_sample_fact(row) for row in resolution.unresolved_samples],
        "diagnostics": list(resolution.diagnostics),
    }


def target_hash_bundle(
    resolution: TargetTemporalCoordinateResolution,
    profile: ResolvedTargetTemporalCoordinateProfile,
) -> TargetTemporalHashBundle:
    fact_hash = object_sha256(target_resolution_fact_projection(resolution))
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "resolved_profile": json_value(profile),
            "hash_algorithm": f"{HASH_ALGORITHM_ID}@{HASH_ALGORITHM_VERSION}",
            "civil_algorithm": profile.civil_time_algorithm_id,
            "solar_algorithm": profile.solar_time_algorithm_id,
            "sampling_lineage": profile.sampling_lineage_id,
        }
    )
    return TargetTemporalHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=HASH_ALGORITHM_ID,
        algorithm_version=HASH_ALGORITHM_VERSION,
    )


def validate_target_temporal_resolution(
    resolution: TargetTemporalCoordinateResolution,
    profile: ResolvedTargetTemporalCoordinateProfile,
    civil: CivilTimeResolver,
    solar: SolarTimeEngine,
) -> TargetTemporalIntegrityReport:
    diagnostics: list[TargetTemporalIntegrityDiagnostic] = []
    target = resolution.target_input
    sampled_wall_times = TimeCalendarFoundation._sample_wall_times(target)  # shared released sampler

    if resolution.sample_count != len(sampled_wall_times):
        _diag(diagnostics, "SAMPLE_COUNT_MISMATCH", "sample_count", str(len(sampled_wall_times)))
    if resolution.effective_uncertainty_seconds_each_side != target.effective_uncertainty_seconds:
        _diag(
            diagnostics,
            "UNCERTAINTY_MISMATCH",
            "effective_uncertainty_seconds_each_side",
            str(target.effective_uncertainty_seconds),
        )
    if (resolution.profile_id, resolution.profile_version) != (profile.profile_id, profile.profile_version):
        _diag(diagnostics, "PROFILE_LINEAGE_MISMATCH", "profile_id", resolution.profile_id)

    expected_candidates: list[dict[str, object]] = []
    expected_unresolved: list[dict[str, object]] = []
    expected_ambiguous = 0
    for sample_index, wall_time in enumerate(sampled_wall_times):
        resolved = civil.resolve_local_time(
            wall_time,
            target.timezone_id,
            input_time_type=InputTimeType.CIVIL,
            ambiguous_time_policy=profile.ambiguous_time_policy,
        )
        if resolved.status is CivilTimeStatus.AMBIGUOUS:
            expected_ambiguous += 1
        if resolved.status in {CivilTimeStatus.NONEXISTENT, CivilTimeStatus.NOT_APPLICABLE}:
            expected_unresolved.append(
                {
                    "source_sample_index": sample_index,
                    "sample_reported_local_datetime": json_value(wall_time),
                    "civil_status": resolved.status.value,
                    "timezone_id": resolved.timezone_id,
                    "tzdb_version": resolved.tzdb_version,
                    "historical_confidence": resolved.historical_confidence.value,
                    "warnings": list(resolved.warnings),
                }
            )
            continue
        candidates = (resolved.selected_candidate,) if resolved.selected_candidate is not None else resolved.candidates
        for civil_candidate in candidates:
            if civil_candidate is None:
                continue
            solar_result = solar.resolve(
                civil_candidate.utc_instant,
                target.longitude,
                civil_candidate.utc_offset_seconds,
            )
            expected_candidates.append(
                {
                    "source_sample_index": sample_index,
                    "sample_reported_local_datetime": json_value(wall_time),
                    "civil_status": resolved.status.value,
                    "timezone_id": resolved.timezone_id,
                    "tzdb_version": resolved.tzdb_version,
                    "historical_confidence": resolved.historical_confidence.value,
                    "warnings": list(resolved.warnings),
                    "target_utc": json_value(civil_candidate.utc_instant.astimezone(timezone.utc)),
                    "fold": civil_candidate.fold,
                    "utc_offset_seconds": civil_candidate.utc_offset_seconds,
                    "daylight_saving_seconds": civil_candidate.daylight_saving_seconds,
                    "timezone_abbreviation": civil_candidate.timezone_abbreviation,
                    "local_mean_solar_datetime": json_value(solar_result.local_mean_solar_datetime),
                    "local_apparent_solar_datetime": json_value(solar_result.local_apparent_solar_datetime),
                    "longitude_correction_seconds_from_civil": solar_result.longitude_correction_seconds_from_civil,
                    "equation_of_time_seconds": solar_result.equation_of_time_seconds,
                    "apparent_solar_offset_from_utc_seconds": solar_result.apparent_solar_offset_from_utc_seconds,
                    "solar_time_algorithm_id": solar_result.algorithm_id,
                    "solar_time_algorithm_version": solar_result.algorithm_version,
                    "time_scale_assumption": solar_result.time_scale_assumption,
                }
            )

    actual_candidates = [target_candidate_fact(row) for row in resolution.candidates]
    if actual_candidates != expected_candidates:
        _diag(diagnostics, "TARGET_CANDIDATE_REPLAY_MISMATCH", "candidates", "civil/solar replay differs")
    actual_unresolved = [unresolved_sample_fact(row) for row in resolution.unresolved_samples]
    if actual_unresolved != expected_unresolved:
        _diag(diagnostics, "UNRESOLVED_SAMPLE_REPLAY_MISMATCH", "unresolved_samples", "civil replay differs")
    if resolution.ambiguous_sample_count != expected_ambiguous:
        _diag(diagnostics, "AMBIGUOUS_SAMPLE_COUNT_MISMATCH", "ambiguous_sample_count", str(expected_ambiguous))

    for index, candidate in enumerate(resolution.candidates):
        expected_id = target_candidate_id(candidate)
        if candidate.candidate_id != expected_id:
            _diag(diagnostics, "CANDIDATE_ID_MISMATCH", f"candidates[{index}].candidate_id", expected_id)
        if candidate.target_utc.tzinfo is None or candidate.target_utc.utcoffset() is None:
            _diag(diagnostics, "TARGET_UTC_NOT_AWARE", f"candidates[{index}].target_utc", "timezone-aware UTC required")

    if not resolution.candidates and resolution.status != "FAILED":
        _diag(diagnostics, "EMPTY_CANDIDATES_NOT_FAILED", "status", resolution.status)
    if resolution.candidates and resolution.status == "FAILED":
        _diag(diagnostics, "LEGAL_CANDIDATES_MARKED_FAILED", "status", resolution.status)

    return TargetTemporalIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=INTEGRITY_ALGORITHM_ID,
        algorithm_version=INTEGRITY_ALGORITHM_VERSION,
    )
