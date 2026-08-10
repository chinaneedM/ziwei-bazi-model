from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping

from fortune_training.bazi_temporal import DayunFrame, PreDayunFrame


@dataclass(frozen=True)
class AnnualFrame:
    frame_id: str
    pillar_year: int
    ganzhi: str
    sexagenary_index: int
    start_term_name: str
    start_term_chinese_name: str
    start_utc: datetime
    end_term_name: str
    end_term_chinese_name: str
    end_utc: datetime
    interval_semantics: str
    year_boundary_policy: str
    solar_term_algorithm_id: str
    solar_term_algorithm_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class MonthlyFrame:
    frame_id: str
    ganzhi: str
    sexagenary_index: int
    start_jie_name: str
    start_jie_chinese_name: str
    start_jie_longitude_degrees: int
    start_utc: datetime
    end_jie_name: str
    end_jie_chinese_name: str
    end_jie_longitude_degrees: int
    end_utc: datetime
    interval_semantics: str
    solar_term_algorithm_id: str
    solar_term_algorithm_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class BaziFlowContext:
    upstream_natal_fact_hash: str
    upstream_temporal_fact_hash: str
    target_utc: datetime
    active_dayun_kind: str
    active_dayun_frame: PreDayunFrame | DayunFrame
    annual_frame: AnnualFrame
    monthly_frame: MonthlyFrame
    natal_profile_id: str
    natal_profile_version: str
    temporal_profile_id: str
    temporal_profile_version: str
    time_calendar_policy_registry_version: str
    year_boundary_policy: str
    algorithm_versions: Mapping[str, str]


@dataclass(frozen=True)
class FlowIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class FlowIntegrityReport:
    status: str
    diagnostics: tuple[FlowIntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-FLOW-INTEGRITY-V1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class FlowHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-FLOW-HASH-V1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class BaziFlowCandidate:
    source_temporal_candidate_indices: tuple[int, ...]
    source_temporal_seed_ids: tuple[str, ...]
    context: BaziFlowContext
    integrity: FlowIntegrityReport
    hashes: FlowHashBundle


@dataclass(frozen=True)
class BaziFlowResolution:
    schema: str
    status: str
    candidates: tuple[BaziFlowCandidate, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
