from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Any


class InputTimeType(str, Enum):
    CIVIL = "CIVIL"
    ALREADY_TRUE_SOLAR = "ALREADY_TRUE_SOLAR"
    UNKNOWN = "UNKNOWN"


class TimePrecision(str, Enum):
    EXACT_SECOND = "EXACT_SECOND"
    NEAREST_MINUTE = "NEAREST_MINUTE"
    NEAREST_HOUR = "NEAREST_HOUR"
    APPROXIMATE = "APPROXIMATE"


class CivilTimeStatus(str, Enum):
    UNIQUE = "UNIQUE"
    AMBIGUOUS = "AMBIGUOUS"
    NONEXISTENT = "NONEXISTENT"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class HistoricalTimezoneConfidence(str, Enum):
    TZDB_POST_1970 = "TZDB_POST_1970"
    TZDB_PRE_1970_REDUCED = "TZDB_PRE_1970_REDUCED"
    NOT_RESOLVED = "NOT_RESOLVED"


@dataclass(frozen=True)
class BirthInput:
    reported_local_datetime: datetime
    birth_place: str
    latitude: float
    longitude: float
    timezone_id: str
    precision: TimePrecision = TimePrecision.EXACT_SECOND
    uncertainty_seconds: int = 0
    input_time_type: InputTimeType = InputTimeType.CIVIL

    def __post_init__(self) -> None:
        if self.reported_local_datetime.tzinfo is not None:
            raise ValueError("reported_local_datetime must be a naive wall-clock value")
        if not self.birth_place.strip():
            raise ValueError("birth_place must not be empty")
        if not -90.0 <= self.latitude <= 90.0:
            raise ValueError("latitude must be in [-90, 90]")
        if not -180.0 <= self.longitude <= 180.0:
            raise ValueError("longitude must be in [-180, 180]")
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
class CivilCandidate:
    fold: int
    utc_instant: datetime
    utc_offset_seconds: int
    daylight_saving_seconds: int
    timezone_abbreviation: str


@dataclass(frozen=True)
class CivilResolution:
    status: CivilTimeStatus
    candidates: tuple[CivilCandidate, ...]
    selected_candidate: CivilCandidate | None
    timezone_id: str
    tzdb_version: str
    historical_confidence: HistoricalTimezoneConfidence
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class SolarTimeResult:
    utc_instant: datetime
    local_mean_solar_datetime: datetime
    local_apparent_solar_datetime: datetime
    longitude_correction_seconds_from_civil: float
    equation_of_time_seconds: float
    apparent_solar_offset_from_utc_seconds: float
    algorithm_id: str
    algorithm_version: str
    time_scale_assumption: str


@dataclass(frozen=True)
class SolarTerm:
    name: str
    chinese_name: str
    longitude_degrees: int
    kind: str
    utc_instant: datetime
    algorithm_id: str
    algorithm_version: str
    advertised_angular_accuracy_arcminutes: float
    time_scale_assumption: str


@dataclass(frozen=True)
class LunarDate:
    year: int
    month: int
    day: int
    is_leap_month: bool
    month_length_days: int
    source_gregorian_date: date
    calendar_zone: str
    algorithm_id: str
    algorithm_version: str
    month_start_utc: datetime
    next_month_start_utc: datetime
    contains_principal_term: bool


@dataclass(frozen=True)
class TraceStep:
    sequence: int
    operation: str
    fact_or_policy: str
    inputs: dict[str, Any]
    outputs: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditTrace:
    schema: str = "TIME-CALENDAR-AUDIT-TRACE-V1"
    steps: list[TraceStep] = field(default_factory=list)

    def add(
        self,
        operation: str,
        fact_or_policy: str,
        inputs: dict[str, Any],
        outputs: dict[str, Any],
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.steps.append(
            TraceStep(
                sequence=len(self.steps) + 1,
                operation=operation,
                fact_or_policy=fact_or_policy,
                inputs=inputs,
                outputs=outputs,
                metadata=metadata or {},
            )
        )


def json_value(value: Any) -> Any:
    """Convert foundation dataclasses to stable JSON-compatible values."""
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        suffix = "Z" if value.tzinfo is not None and value.utcoffset().total_seconds() == 0 else ""
        base = value.replace(tzinfo=None).isoformat(timespec="microseconds").rstrip("0").rstrip(".")
        return base + suffix
    if isinstance(value, date):
        return value.isoformat()
    if hasattr(value, "__dataclass_fields__"):
        return json_value(asdict(value))
    if isinstance(value, dict):
        return {str(key): json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_value(item) for item in value]
    return value
