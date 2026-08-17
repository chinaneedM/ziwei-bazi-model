from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from fortune_training.calendar_foundation import TimePrecision


@dataclass(frozen=True)
class TargetTemporalInput:
    reported_local_datetime: datetime
    target_place: str
    latitude: float
    longitude: float
    timezone_id: str
    precision: TimePrecision = TimePrecision.EXACT_SECOND
    uncertainty_seconds: int = 0

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
        floors = {
            TimePrecision.EXACT_SECOND: 0,
            TimePrecision.NEAREST_MINUTE: 30,
            TimePrecision.NEAREST_HOUR: 1800,
            TimePrecision.APPROXIMATE: 0,
        }
        return max(self.uncertainty_seconds, floors[self.precision])


@dataclass(frozen=True)
class TargetTemporalCoordinateCandidate:
    candidate_id: str
    source_sample_index: int
    sample_reported_local_datetime: datetime
    civil_status: str
    timezone_id: str
    tzdb_version: str
    historical_confidence: str
    warnings: tuple[str, ...]
    target_utc: datetime
    fold: int
    utc_offset_seconds: int
    daylight_saving_seconds: int
    timezone_abbreviation: str
    local_mean_solar_datetime: datetime
    local_apparent_solar_datetime: datetime
    longitude_correction_seconds_from_civil: float
    equation_of_time_seconds: float
    apparent_solar_offset_from_utc_seconds: float
    solar_time_algorithm_id: str
    solar_time_algorithm_version: str
    time_scale_assumption: str


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
    algorithm_id: str = "BAZI-TARGET-TEMPORAL-COORDINATE-INTEGRITY-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class TargetTemporalHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-TARGET-TEMPORAL-COORDINATE-HASH-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class TargetTemporalCoordinateResolution:
    schema: str
    status: str
    target_input: TargetTemporalInput
    profile_id: str
    profile_version: str
    effective_uncertainty_seconds_each_side: int
    sample_count: int
    ambiguous_sample_count: int
    candidates: tuple[TargetTemporalCoordinateCandidate, ...]
    unresolved_samples: tuple[TargetTemporalUnresolvedSample, ...]
    diagnostics: tuple[str, ...]
    integrity: TargetTemporalIntegrityReport
    hashes: TargetTemporalHashBundle
