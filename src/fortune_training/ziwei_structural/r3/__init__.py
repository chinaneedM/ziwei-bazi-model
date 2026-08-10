"""Ziwei Structural Runtime V2-R3 borrow-projection structural view."""

from .engine import BorrowProjectionGenerationError, ZiweiBorrowProjectionRuntime
from .integrity import (
    BORROW_PROJECTION_INTEGRITY_ALGORITHM_ID,
    BORROW_PROJECTION_INTEGRITY_ALGORITHM_VERSION,
    borrow_projection_fact_projection,
    borrow_projection_hash_bundle,
    validate_borrow_projection_components,
    validate_borrow_projection_state,
)
from .models import (
    BORROW_CLOSURE_STATUSES,
    BORROW_MEMBER_OFFSETS,
    BORROW_PROJECTION_STATE_SCHEMA,
    BorrowClosureMemberFact,
    BorrowProjectionHashBundle,
    BorrowProjectionIntegrityDiagnostic,
    BorrowProjectionIntegrityReport,
    BorrowProjectionState,
)
from .profile import (
    BORROW_PROJECTION_ALGORITHM_ID,
    BORROW_PROJECTION_ALGORITHM_VERSION,
    BORROW_PROJECTION_RULE_SET_ID,
    BORROW_PROJECTION_RULE_SET_VERSION,
    ZIWEI_STRUCTURAL_V2_R3_PROFILE_ID,
    ZIWEI_STRUCTURAL_V2_R3_PROFILE_VERSION,
    ResolvedBorrowProjectionProfile,
    ziwei_structural_v2_r3_profile,
)
from .projection import (
    BORROW_PROJECTION_SOURCE_REFS,
    FOURTEEN_MAIN_STAR_ENTITY_IDS,
    BorrowProjectionError,
    BorrowProjectionGenerator,
)


__all__ = [
    "BORROW_CLOSURE_STATUSES",
    "BORROW_MEMBER_OFFSETS",
    "BORROW_PROJECTION_ALGORITHM_ID",
    "BORROW_PROJECTION_ALGORITHM_VERSION",
    "BORROW_PROJECTION_INTEGRITY_ALGORITHM_ID",
    "BORROW_PROJECTION_INTEGRITY_ALGORITHM_VERSION",
    "BORROW_PROJECTION_RULE_SET_ID",
    "BORROW_PROJECTION_RULE_SET_VERSION",
    "BORROW_PROJECTION_SOURCE_REFS",
    "BORROW_PROJECTION_STATE_SCHEMA",
    "FOURTEEN_MAIN_STAR_ENTITY_IDS",
    "BorrowClosureMemberFact",
    "BorrowProjectionError",
    "BorrowProjectionGenerationError",
    "BorrowProjectionGenerator",
    "BorrowProjectionHashBundle",
    "BorrowProjectionIntegrityDiagnostic",
    "BorrowProjectionIntegrityReport",
    "BorrowProjectionState",
    "ResolvedBorrowProjectionProfile",
    "ZIWEI_STRUCTURAL_V2_R3_PROFILE_ID",
    "ZIWEI_STRUCTURAL_V2_R3_PROFILE_VERSION",
    "ZiweiBorrowProjectionRuntime",
    "borrow_projection_fact_projection",
    "borrow_projection_hash_bundle",
    "validate_borrow_projection_components",
    "validate_borrow_projection_state",
    "ziwei_structural_v2_r3_profile",
]

__version__ = "2.0.0-r3"
