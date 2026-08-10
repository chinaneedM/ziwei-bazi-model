from __future__ import annotations

from dataclasses import dataclass

from fortune_training.ziwei_chart.models import Address

from .profile import ResolvedStructuralCompositionProfile


RESOLVED_STRUCTURAL_VIEW_STATE_SCHEMA = "ZIWEI-RESOLVED-STRUCTURAL-VIEW-STATE-V2-R5"
RESOLVED_MEMBER_OFFSETS = (0, 4, 6, 8)
RESOLVED_MEMBER_ROLE_BY_OFFSET = {
    0: "SELF",
    4: "TRINE_PLUS_4",
    6: "OPPOSITION",
    8: "TRINE_PLUS_8",
}
RESOLVED_MEMBER_ROLES = frozenset(RESOLVED_MEMBER_ROLE_BY_OFFSET.values())


@dataclass(frozen=True)
class ResolvedStructuralMemberRef:
    semantic_role: str
    member_offset: int
    target_designation_id: str
    target_raw_address: Address
    closure_status: str
    borrowed_from_raw_address: Address | None
    physical_source_address: Address | None
    structure_physical_key: str
    r3_member_key: str

    def __post_init__(self) -> None:
        if self.member_offset not in RESOLVED_MEMBER_OFFSETS:
            raise ValueError(f"unsupported member_offset: {self.member_offset}")
        expected_role = RESOLVED_MEMBER_ROLE_BY_OFFSET[self.member_offset]
        if self.semantic_role != expected_role:
            raise ValueError(
                f"semantic_role {self.semantic_role} does not match offset {self.member_offset}"
            )


@dataclass(frozen=True)
class ResolvedSanfangSizhengFrameFact:
    origin_designation_id: str
    origin_address: Address
    trine_group_key: str
    opposition_axis_key: str
    members: tuple[ResolvedStructuralMemberRef, ...]


@dataclass(frozen=True)
class ResolvedStructuralIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class ResolvedStructuralIntegrityReport:
    status: str
    diagnostics: tuple[ResolvedStructuralIntegrityDiagnostic, ...]
    algorithm_id: str
    algorithm_version: str


@dataclass(frozen=True)
class ResolvedStructuralHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str
    algorithm_version: str


@dataclass(frozen=True)
class ResolvedSanfangSizhengViewState:
    upstream_r3_fact_hash: str
    upstream_r3_computation_hash: str
    upstream_r4_fact_hash: str
    upstream_r4_computation_hash: str
    profile: ResolvedStructuralCompositionProfile
    time_layer: str
    frames: tuple[ResolvedSanfangSizhengFrameFact, ...]
    integrity: ResolvedStructuralIntegrityReport
    hashes: ResolvedStructuralHashBundle
    schema: str = RESOLVED_STRUCTURAL_VIEW_STATE_SCHEMA
