from __future__ import annotations

from dataclasses import dataclass

from fortune_training.ziwei_chart.models import Address

from .profile import ResolvedRelativePalaceFrameProfile


RELATIVE_PALACE_FRAME_STATE_SCHEMA = "ZIWEI-RELATIVE-PALACE-FRAME-STATE-V2-R2"


@dataclass(frozen=True)
class RelativePalaceRoleFact:
    origin_designation_id: str
    origin_address: Address
    relative_ordinal: int
    relative_role_designation_id: str
    target_designation_id: str
    target_address: Address
    clockwise_offset: int

    def __post_init__(self) -> None:
        if not 1 <= self.relative_ordinal <= 12:
            raise ValueError("relative_ordinal must be in [1, 12]")
        if not 0 <= self.clockwise_offset < 12:
            raise ValueError("clockwise_offset must be in [0, 11]")


@dataclass(frozen=True)
class RelativeFrameIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class RelativeFrameIntegrityReport:
    status: str
    diagnostics: tuple[RelativeFrameIntegrityDiagnostic, ...]
    algorithm_id: str
    algorithm_version: str


@dataclass(frozen=True)
class RelativeFrameHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str
    algorithm_version: str


@dataclass(frozen=True)
class RelativePalaceFrameState:
    upstream_structural_fact_hash: str
    upstream_structural_computation_hash: str
    profile: ResolvedRelativePalaceFrameProfile
    frame_facts: tuple[RelativePalaceRoleFact, ...]
    integrity: RelativeFrameIntegrityReport
    hashes: RelativeFrameHashBundle
    schema: str = RELATIVE_PALACE_FRAME_STATE_SCHEMA
