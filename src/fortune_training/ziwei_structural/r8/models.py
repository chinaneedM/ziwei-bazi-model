from __future__ import annotations

from dataclasses import dataclass

from fortune_training.ziwei_chart.models import Address

from .profile import ResolvedAdjacentPalacePairProfile


ADJACENT_PALACE_PAIR_STATE_SCHEMA = "ZIWEI-ADJACENT-PALACE-PAIR-STATE-V2-R8"


@dataclass(frozen=True)
class AdjacentPalacePairFact:
    source_term_id: str
    origin_designation_id: str
    origin_address: Address
    counterclockwise_designation_id: str
    counterclockwise_address: Address
    counterclockwise_relative_ordinal: int
    counterclockwise_clockwise_offset: int
    clockwise_designation_id: str
    clockwise_address: Address
    clockwise_relative_ordinal: int
    clockwise_clockwise_offset: int
    semantic_scope: str
    direct_event_permission: bool
    direct_endpoint_permission: bool
    direct_score_permission: bool
    flank_semantics_permission: bool


@dataclass(frozen=True)
class AdjacentPalaceIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class AdjacentPalaceIntegrityReport:
    status: str
    diagnostics: tuple[AdjacentPalaceIntegrityDiagnostic, ...]
    algorithm_id: str
    algorithm_version: str


@dataclass(frozen=True)
class AdjacentPalaceHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str
    algorithm_version: str


@dataclass(frozen=True)
class AdjacentPalacePairState:
    upstream_r2_fact_hash: str
    upstream_r2_computation_hash: str
    profile: ResolvedAdjacentPalacePairProfile
    time_layer: str
    adjacent_palace_pairs: tuple[AdjacentPalacePairFact, ...]
    integrity: AdjacentPalaceIntegrityReport
    hashes: AdjacentPalaceHashBundle
    schema: str = ADJACENT_PALACE_PAIR_STATE_SCHEMA
