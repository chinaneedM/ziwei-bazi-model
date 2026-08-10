from __future__ import annotations

from dataclasses import dataclass

from fortune_training.ziwei_chart.models import Address

from .profile import ResolvedZiweiStructuralProfile


STRUCTURAL_STATE_SCHEMA = "ZIWEI-STRUCTURAL-STATE-V2-R1"


@dataclass(frozen=True)
class AddressOffsetFact:
    source: Address
    target: Address
    clockwise_offset: int

    def __post_init__(self) -> None:
        if not 0 <= self.clockwise_offset < 12:
            raise ValueError("clockwise_offset must be in [0, 11]")


@dataclass(frozen=True)
class StructuralIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class StructuralIntegrityReport:
    status: str
    diagnostics: tuple[StructuralIntegrityDiagnostic, ...]
    algorithm_id: str
    algorithm_version: str


@dataclass(frozen=True)
class StructuralHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str
    algorithm_version: str


@dataclass(frozen=True)
class StructuralState:
    upstream_natal_fact_hash: str
    upstream_natal_computation_hash: str
    profile: ResolvedZiweiStructuralProfile
    topology_facts: tuple[AddressOffsetFact, ...]
    integrity: StructuralIntegrityReport
    hashes: StructuralHashBundle
    schema: str = STRUCTURAL_STATE_SCHEMA
