from __future__ import annotations

from fortune_training.calendar_foundation import CivilTimeResolver, SolarTimeEngine
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .models import (
    TargetTemporalCoordinate,
    TargetTemporalHashBundle,
    TargetTemporalInput,
    TargetTemporalIntegrityDiagnostic,
    TargetTemporalIntegrityReport,
    TargetTemporalProfile,
)


def _fact_payload(target_input: TargetTemporalInput, coordinate: TargetTemporalCoordinate) -> dict:
    return {
        "target_input": json_value(target_input),
        "coordinate": json_value(coordinate),
    }


def target_coordinate_hash_bundle(
    target_input: TargetTemporalInput,
    coordinate: TargetTemporalCoordinate,
    profile: TargetTemporalProfile,
) -> TargetTemporalHashBundle:
    fact_hash = object_sha256(_fact_payload(target_input, coordinate))
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "profile": json_value(profile),
            "coordinate_algorithm_id": profile.coordinate_algorithm_id,
            "coordinate_algorithm_version": profile.coordinate_algorithm_version,
            "civil_algorithm_id": profile.civil_algorithm_id,
            "civil_algorithm_version": coordinate.tzdb_version,
            "solar_algorithm_id": coordinate.solar_time.algorithm_id,
            "solar_algorithm_version": coordinate.solar_time.algorithm_version,
        }
    )
    return TargetTemporalHashBundle(fact_hash=fact_hash, computation_hash=computation_hash)


def validate_target_coordinate(
    target_input: TargetTemporalInput,
    coordinate: TargetTemporalCoordinate,
    profile: TargetTemporalProfile,
    civil: CivilTimeResolver | None = None,
    solar: SolarTimeEngine | None = None,
) -> TargetTemporalIntegrityReport:
    civil_engine = civil or CivilTimeResolver()
    solar_engine = solar or SolarTimeEngine()
    diagnostics: list[TargetTemporalIntegrityDiagnostic] = []

    def mismatch(code: str, path: str, expected: object, actual: object) -> None:
        if expected != actual:
            diagnostics.append(
                TargetTemporalIntegrityDiagnostic(
                    code=code,
                    path=path,
                    detail=f"expected={expected!r} actual={actual!r}",
                )
            )

    mismatch("TARGET_PLACE_MISMATCH", "target_place", target_input.target_place, coordinate.target_place)
    mismatch("LATITUDE_MISMATCH", "latitude", target_input.latitude, coordinate.latitude)
    mismatch("LONGITUDE_MISMATCH", "longitude", target_input.longitude, coordinate.longitude)
    mismatch("TIMEZONE_MISMATCH", "timezone_id", target_input.timezone_id, coordinate.timezone_id)

    try:
        resolved = civil_engine.resolve_wall_time(
            coordinate.sample_reported_local_datetime,
            target_input.timezone_id,
            input_time_type=target_input.input_time_type,
            ambiguous_time_policy=profile.civil_ambiguous_time_policy,
        )
    except ValueError as exc:
        diagnostics.append(
            TargetTemporalIntegrityDiagnostic(
                code="CIVIL_REPLAY_FAILED",
                path="civil",
                detail=str(exc),
            )
        )
        return TargetTemporalIntegrityReport(status="FAIL", diagnostics=tuple(diagnostics))

    mismatch("CIVIL_STATUS_MISMATCH", "civil_status", resolved.status.value, coordinate.civil_status)
    mismatch("TZDB_VERSION_MISMATCH", "tzdb_version", resolved.tzdb_version, coordinate.tzdb_version)
    mismatch(
        "HISTORICAL_CONFIDENCE_MISMATCH",
        "historical_confidence",
        resolved.historical_confidence.value,
        coordinate.historical_confidence,
    )
    mismatch("WARNINGS_MISMATCH", "warnings", resolved.warnings, coordinate.warnings)

    legal = tuple(resolved.candidates)
    if coordinate.civil_candidate not in legal:
        diagnostics.append(
            TargetTemporalIntegrityDiagnostic(
                code="CIVIL_REALIZATION_NOT_REPLAYED",
                path="civil_candidate",
                detail=repr(json_value(coordinate.civil_candidate)),
            )
        )
    else:
        replay_solar = solar_engine.resolve(
            coordinate.civil_candidate.utc_instant,
            target_input.longitude,
            coordinate.civil_candidate.utc_offset_seconds,
        )
        mismatch(
            "SOLAR_TIME_MISMATCH",
            "solar_time",
            json_value(replay_solar),
            json_value(coordinate.solar_time),
        )

    expected_id_payload = {
        "target_input": json_value(target_input),
        "source_sample_index": coordinate.source_sample_index,
        "source_civil_candidate_index": coordinate.source_civil_candidate_index,
        "sample_reported_local_datetime": json_value(coordinate.sample_reported_local_datetime),
        "civil_candidate": json_value(coordinate.civil_candidate),
        "solar_time": json_value(coordinate.solar_time),
    }
    expected_id = f"TARGET-COORDINATE:{object_sha256(expected_id_payload)}"
    mismatch("COORDINATE_ID_MISMATCH", "coordinate_id", expected_id, coordinate.coordinate_id)

    return TargetTemporalIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )
