from __future__ import annotations

from dataclasses import dataclass

from fortune_training.ziwei_chart.models import Address

from .profile import ResolvedOneSixCommonRootProfile


ONE_SIX_COMMON_ROOT_STATE_SCHEMA = "ZIWEI-ONE-SIX-COMMON-ROOT-STATE-V2-R7"


@dataclass(frozen=True)
class OneSixCommonRootFact:
    source_technique_id: str
    origin_designation_id: str
    origin_address: Address
    relative_role_designation_id: str
    target_designation_id: str
    target_address: Address
    relative_ordinal: int
    clockwise_offset: int
    semantic_scope: str
    direct_event_permission: bool
    direct_endpoint_permission: bool


@dataclass(frozen=True)
class OneSixIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class OneSixIntegrityReport:
    status: str
    diagnostics: tuple[OneSixIntegrityDiagnostic, ...]
    algorithm_id: str
    algorithm_version: str


@dataclass(frozen=True)
class OneSixHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str
    algorithm_version: str


@dataclass(frozen=True)
class OneSixCommonRootState:
    upstream_r2_fact_hash: str
    upstream_r2_computation_hash: str
    profile: ResolvedOneSixCommonRootProfile
    time_layer: str
    one_six_facts: tuple[OneSixCommonRootFact, ...]
    integrity: OneSixIntegrityReport
    hashes: OneSixHashBundle
    schema: str = ONE_SIX_COMMON_ROOT_STATE_SCHEMA
