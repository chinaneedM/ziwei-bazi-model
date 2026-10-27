from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from fortune_training.bazi_chart import ResolvedBaziCalculationProfile
from fortune_training.bazi_temporal import BaziSex, ResolvedBaziTemporalProfile
from fortune_training.calendar_foundation import BirthInput

from .profile import BaziApplicationProfile


@dataclass(frozen=True)
class BaziApplicationRequest:
    birth: BirthInput
    sex: BaziSex
    natal_profile: ResolvedBaziCalculationProfile
    temporal_profile: ResolvedBaziTemporalProfile
    application_profile: BaziApplicationProfile
    dayun_count: int = 12


@dataclass(frozen=True)
class BaziApplicationCandidate:
    candidate_id: str
    natal_candidate_index: int
    temporal_candidate_index: int
    natal_fact_hash: str
    natal_computation_hash: str
    temporal_fact_hash: str
    temporal_computation_hash: str
    source_temporal_seed_ids: tuple[str, ...]
    view_schema: str
    view: Mapping[str, Any]
    view_hash: str


@dataclass(frozen=True)
class BaziApplicationLegalTimeRealization:
    source_time_branch_index: int
    sample_reported_local_datetime: str
    civil_status: str
    timezone_id: str
    tzdb_version: str
    historical_confidence: str
    warnings: tuple[str, ...]
    birth_utc: str
    fold: int
    utc_offset_seconds: int
    daylight_saving_seconds: int
    timezone_abbreviation: str


@dataclass(frozen=True)
class BaziApplicationUnresolvedTimeSample:
    sample_reported_local_datetime: str
    civil_status: str
    timezone_id: str
    tzdb_version: str
    historical_confidence: str
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class BaziApplicationTimeCalendarProvenance:
    status: str
    effective_uncertainty_seconds_each_side: int
    sample_count: int
    ambiguous_sample_count: int
    legal_realization_count: int
    legal_realizations: tuple[BaziApplicationLegalTimeRealization, ...]
    unresolved_sample_count: int
    unresolved_samples: tuple[BaziApplicationUnresolvedTimeSample, ...]


@dataclass(frozen=True)
class BaziApplicationIntegrityReport:
    status: str
    diagnostics: tuple[str, ...]
    algorithm_id: str = "BAZI-LOCAL-APPLICATION-INTEGRITY-V1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class BaziApplicationResolution:
    schema: str
    status: str
    birth: BirthInput
    application_profile: BaziApplicationProfile
    natal_profile: ResolvedBaziCalculationProfile
    temporal_profile: ResolvedBaziTemporalProfile
    sex: BaziSex
    dayun_count: int
    time_calendar_provenance: BaziApplicationTimeCalendarProvenance
    candidates: tuple[BaziApplicationCandidate, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
    source_fact_hash: str
    view_hash: str
    bundle_hash: str
    integrity: BaziApplicationIntegrityReport
