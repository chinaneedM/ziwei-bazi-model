from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Mapping


class BaziSex(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


@dataclass(frozen=True)
class DayunDirectionResolution:
    direction: str
    year_stem: str
    year_stem_polarity: str
    sex: BaziSex
    rule_set_id: str
    rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class SymbolicLuckAge:
    total_symbolic_microseconds: int
    years_360: int
    months_30: int
    days: int
    residual_microseconds: int
    rule_set_id: str
    rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class JiaoyunResolution:
    temporal_seed_id: str
    direction: str
    anchor_kind: str
    anchor_jie_name: str
    anchor_jie_utc: datetime
    birth_utc: datetime
    raw_interval_microseconds: int
    symbolic_age: SymbolicLuckAge
    first_transition_utc: datetime
    interval_coordinate_policy: str
    interval_granularity_rule_set: str
    calendar_realization_rule_set: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class PreDayunFrame:
    frame_id: str
    start_utc: datetime
    end_utc: datetime
    interval_semantics: str


@dataclass(frozen=True)
class DayunFrame:
    frame_id: str
    index: int
    ganzhi: str
    sexagenary_index: int
    start_utc: datetime
    end_utc: datetime
    interval_semantics: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class BaziDayunState:
    upstream_natal_fact_hash: str
    direction: DayunDirectionResolution
    jiaoyun: JiaoyunResolution
    pre_dayun: PreDayunFrame
    dayun_frames: tuple[DayunFrame, ...]
    profile_id: str
    profile_version: str
    algorithm_versions: Mapping[str, str]


@dataclass(frozen=True)
class TemporalIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class TemporalIntegrityReport:
    status: str
    diagnostics: tuple[TemporalIntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-TEMPORAL-INTEGRITY-V1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class TemporalHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-TEMPORAL-HASH-V1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class BaziTemporalCandidate:
    source_temporal_seed_ids: tuple[str, ...]
    state: BaziDayunState
    integrity: TemporalIntegrityReport
    hashes: TemporalHashBundle


@dataclass(frozen=True)
class BaziTemporalResolution:
    schema: str
    status: str
    candidates: tuple[BaziTemporalCandidate, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
