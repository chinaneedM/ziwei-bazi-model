from __future__ import annotations

from dataclasses import dataclass

from fortune_training.ziwei_chart.models import Address

from .profile import ResolvedQiShuPositionProfile


QISHU_POSITION_STATE_SCHEMA = "ZIWEI-QISHU-POSITION-STATE-V2-R6"


@dataclass(frozen=True)
class QiShuPositionFact:
    source_mapping_id: str
    origin_designation_id: str
    origin_address: Address
    target_designation_id: str
    target_address: Address
    relative_ordinal: int
    clockwise_offset: int
    fixed_support_meaning: str


@dataclass(frozen=True)
class QiShuIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class QiShuIntegrityReport:
    status: str
    diagnostics: tuple[QiShuIntegrityDiagnostic, ...]
    algorithm_id: str
    algorithm_version: str


@dataclass(frozen=True)
class QiShuHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str
    algorithm_version: str


@dataclass(frozen=True)
class QiShuPositionState:
    upstream_r2_fact_hash: str
    upstream_r2_computation_hash: str
    profile: ResolvedQiShuPositionProfile
    time_layer: str
    qishu_facts: tuple[QiShuPositionFact, ...]
    integrity: QiShuIntegrityReport
    hashes: QiShuHashBundle
    schema: str = QISHU_POSITION_STATE_SCHEMA
