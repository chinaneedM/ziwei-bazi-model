from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Mapping

from fortune_training.bazi_chart import ResolvedBaziCalculationProfile
from fortune_training.bazi_flow import BaziFlowCandidate
from fortune_training.bazi_target_temporal import (
    ResolvedTargetTemporalCoordinateProfile,
    TargetTemporalCoordinateResolution,
)


@dataclass(frozen=True)
class DailyFrame:
    frame_id: str
    ganzhi: str
    sexagenary_index: int
    effective_day_date: date
    start_las: datetime
    end_las: datetime
    interval_semantics: str
    day_boundary_policy: str
    source_flow_fact_hash: str
    source_target_coordinate_fact_hash: str
    source_target_coordinate_candidate_id: str
    natal_profile_id: str
    natal_profile_version: str


@dataclass(frozen=True)
class HourlyFrame:
    frame_id: str
    ganzhi: str
    sexagenary_index: int
    branch: str
    start_las: datetime
    end_las: datetime
    interval_semantics: str
    hour_stem_source_date: date
    late_zi_hour_stem_policy: str
    daily_frame_id: str
    source_flow_fact_hash: str
    source_target_coordinate_fact_hash: str
    source_target_coordinate_candidate_id: str
    natal_profile_id: str
    natal_profile_version: str


@dataclass(frozen=True)
class BaziDailyHourlyFlowContext:
    upstream_natal_fact_hash: str
    upstream_temporal_fact_hash: str
    source_flow_fact_hash: str
    source_flow_computation_hash: str
    source_target_coordinate_fact_hash: str
    source_target_coordinate_computation_hash: str
    source_target_coordinate_candidate_id: str
    source_target_coordinate_candidate_index: int
    target_utc: datetime
    target_local_apparent_solar_datetime: datetime
    target_longitude: float
    daily_frame: DailyFrame
    hourly_frame: HourlyFrame
    natal_profile_id: str
    natal_profile_version: str
    day_boundary_policy: str
    late_zi_hour_stem_policy: str
    year_boundary_policy: str
    algorithm_versions: Mapping[str, str]


@dataclass(frozen=True)
class DailyHourlyIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class DailyHourlyIntegrityReport:
    status: str
    diagnostics: tuple[DailyHourlyIntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-DAILY-HOURLY-FLOW-INTEGRITY-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class DailyHourlyHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-DAILY-HOURLY-FLOW-HASH-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class BaziDailyHourlyFlowCandidate:
    source_flow_candidate_index: int
    source_target_coordinate_candidate_index: int
    context: BaziDailyHourlyFlowContext
    integrity: DailyHourlyIntegrityReport
    hashes: DailyHourlyHashBundle


@dataclass(frozen=True)
class BaziDailyHourlyFlowResolution:
    schema: str
    status: str
    candidates: tuple[BaziDailyHourlyFlowCandidate, ...]
    diagnostics: tuple[str, ...]


@dataclass(frozen=True)
class BaziDailyHourlyFlowRequest:
    flow_candidates: tuple[BaziFlowCandidate, ...]
    target_coordinate_resolution: TargetTemporalCoordinateResolution
    target_coordinate_profile: ResolvedTargetTemporalCoordinateProfile
    calculation_profile: ResolvedBaziCalculationProfile
