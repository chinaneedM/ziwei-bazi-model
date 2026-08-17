from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from fortune_training.calendar_foundation.models import (
    CivilCandidate,
    InputTimeType,
    SolarTimeResult,
    TimePrecision,
    effective_uncertainty_seconds,
)


@dataclass(frozen=True)
class TargetTemporalInput:
    reported_local_datetime: datetime
    target_place: str
    latitude: float
    longitude: float
    timezone_id: str
    precision: TimePrecision = TimePrecision.EXACT_SECOND
    uncertainty_seconds: int = 0
    input_time_type: InputTimeType = InputTimeType.CIVIL

    def __post_init__(self) -> None:
        if self.reported_local_datetime.tzinfo is not None:
            raise ValueError("reported_local_datetime must be a naive wall-clock value")
        if not self.target_place.strip():
            raise ValueError("target_place must not be empty")
        if not -90.0 <= self.latitude <= 90.0:
            raise ValueError("latitude must be in [-90, 90]")
        if not -180.0 <= self.longitude <= 180.0:
            raise ValueError("longitude must be in [-180, 180]")
        if not self.timezone_id.strip():
            raise ValueError("timezone_id must not be empty")
        if self.uncertainty_seconds < 0:
            raise ValueError("uncertainty_seconds must be non-negative")
        if self.precision is TimePrecision.APPROXIMATE and self.uncertainty_seconds == 0:
            raise ValueError("APPROXIMATE precision requires uncertainty_seconds > 0")

    @property
    def effective_uncertainty_seconds(self) -> int:
        return effective_uncertainty_seconds(self.precision, self.uncertainty_seconds)


@dataclass(frozen=True)
class TargetTemporalProfile:
    profile_id: str
    profile_version: str
    civil_ambiguous_time_policy: str
    coordinate_algorithm_id: str
    coordinate_algorithm_version: str
    civil_algorithm_id: str
    solar_algorithm_id: str


@dataclass(frozen=True)
class TargetTemporalCoordinate:
    coordinate_id: str
    source_sample_index: int
    source_civil_candidate_index: int
    sample_reported_local_datetime: datetime
    target_place: str
    latitude: float
    longitude: float
    timezone_id: str
    tzdb_version: str
    historical_confidence: str
    warnings: tuple[str, ...]
    civil_status: str
    civil_candidate: CivilCandidate
    solar_time: SolarTimeResult


@dataclass(frozen=True)
class TargetTemporalUnresolvedSample:
    source_sample_index: int
    sample_reported_local_datetime: datetime
    civil_status: str
    timezone_id: str
    tzdb_version: str
    historical_confidence: str
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class TargetTemporalIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class TargetTemporalIntegrityReport:
    status: str
    diagnostics: tuple[TargetTemporalIntegrityDiagnostic, ...]
    algorithm_id: str = "TARGET-TEMPORAL-COORDINATE-INTEGRITY-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class TargetTemporalHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "TARGET-TEMPORAL-COORDINATE-HASH-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class TargetTemporalResolvedCandidate:
    coordinate: TargetTemporalCoordinate
    integrity: TargetTemporalIntegrityReport
    hashes: TargetTemporalHashBundle


@dataclass(frozen=True)
class TargetTemporalCoordinateResolution:
    schema: str
    status: str
    target_input: TargetTemporalInput
    profile: TargetTemporalProfile
    effective_uncertainty_seconds_each_side: int
    sample_count: int
    ambiguous_sample_count: int
    legal_realization_count: int
    candidates: tuple[TargetTemporalResolvedCandidate, ...]
    unresolved_samples: tuple[TargetTemporalUnresolvedSample, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
    fact_hash: str
    computation_hash: str
