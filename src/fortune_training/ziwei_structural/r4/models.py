from __future__ import annotations

from dataclasses import dataclass

from fortune_training.ziwei_chart.models import Address

from .profile import ResolvedNamedStructuralSemanticProfile


NAMED_STRUCTURAL_SEMANTIC_STATE_SCHEMA = "ZIWEI-NAMED-STRUCTURAL-SEMANTIC-STATE-V2-R4"


@dataclass(frozen=True)
class OppositionAxisFact:
    axis_key: str
    member_designation_ids: tuple[str, str]
    member_addresses: tuple[Address, Address]


@dataclass(frozen=True)
class TrineGroupFact:
    group_key: str
    member_designation_ids: tuple[str, str, str]
    member_addresses: tuple[Address, Address, Address]


@dataclass(frozen=True)
class SanfangSizhengFrameFact:
    origin_designation_id: str
    origin_address: Address
    trine_group_key: str
    trine_partner_designation_ids: tuple[str, str]
    trine_partner_addresses: tuple[Address, Address]
    trine_offsets: tuple[int, int]
    opposition_axis_key: str
    opposition_designation_id: str
    opposition_address: Address
    opposition_offset: int


@dataclass(frozen=True)
class NamedSemanticIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class NamedSemanticIntegrityReport:
    status: str
    diagnostics: tuple[NamedSemanticIntegrityDiagnostic, ...]
    algorithm_id: str
    algorithm_version: str


@dataclass(frozen=True)
class NamedSemanticHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str
    algorithm_version: str


@dataclass(frozen=True)
class NamedStructuralSemanticState:
    upstream_r2_fact_hash: str
    upstream_r2_computation_hash: str
    profile: ResolvedNamedStructuralSemanticProfile
    opposition_axes: tuple[OppositionAxisFact, ...]
    trine_groups: tuple[TrineGroupFact, ...]
    sanfang_sizheng_frames: tuple[SanfangSizhengFrameFact, ...]
    integrity: NamedSemanticIntegrityReport
    hashes: NamedSemanticHashBundle
    schema: str = NAMED_STRUCTURAL_SEMANTIC_STATE_SCHEMA
