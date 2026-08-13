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
class BaziApplicationResolution:
    schema: str
    status: str
    application_profile: BaziApplicationProfile
    natal_profile: ResolvedBaziCalculationProfile
    temporal_profile: ResolvedBaziTemporalProfile
    sex: BaziSex
    dayun_count: int
    candidates: tuple[BaziApplicationCandidate, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
    source_fact_hash: str
    view_hash: str
    bundle_hash: str
