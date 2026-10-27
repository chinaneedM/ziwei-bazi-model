from __future__ import annotations

from dataclasses import dataclass

from fortune_training.ziwei_chart.models import Address, Placement, TransformationActivation

from .profile import ResolvedBorrowProjectionProfile


BORROW_PROJECTION_STATE_SCHEMA = "ZIWEI-BORROW-PROJECTION-STATE-V2-R3"
BORROW_MEMBER_OFFSETS = (0, 4, 6, 8)
BORROW_CLOSURE_STATUSES = frozenset(
    {"DIRECT_PHYSICAL", "BORROWED_DIRECT", "BORROW_SOURCE_EMPTY_OR_UNKNOWN"}
)


@dataclass(frozen=True)
class BorrowClosureMemberFact:
    evaluation_origin_designation_id: str
    evaluation_origin_address: Address
    time_layer: str
    member_offset: int
    target_designation_id: str
    target_raw_address: Address
    target_main_star_empty: bool
    closure_status: str
    borrowed_from_raw_address: Address | None
    projected_placements: tuple[Placement, ...]
    projected_transformations: tuple[TransformationActivation, ...]
    structure_physical_key: str
    zero_second_contribution: bool

    def __post_init__(self) -> None:
        if self.member_offset not in BORROW_MEMBER_OFFSETS:
            raise ValueError(f"unsupported member_offset: {self.member_offset}")
        if self.closure_status not in BORROW_CLOSURE_STATUSES:
            raise ValueError(f"unsupported closure_status: {self.closure_status}")


@dataclass(frozen=True)
class BorrowProjectionIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class BorrowProjectionIntegrityReport:
    status: str
    diagnostics: tuple[BorrowProjectionIntegrityDiagnostic, ...]
    algorithm_id: str
    algorithm_version: str


@dataclass(frozen=True)
class BorrowProjectionHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str
    algorithm_version: str


@dataclass(frozen=True)
class BorrowProjectionState:
    upstream_relative_frame_fact_hash: str
    upstream_relative_frame_computation_hash: str
    profile: ResolvedBorrowProjectionProfile
    time_layer: str
    member_facts: tuple[BorrowClosureMemberFact, ...]
    integrity: BorrowProjectionIntegrityReport
    hashes: BorrowProjectionHashBundle
    schema: str = BORROW_PROJECTION_STATE_SCHEMA
