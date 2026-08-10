"""Ziwei Structural Runtime V2-R5 borrow-resolved Sanfang/Sizheng composition view."""

from .composition import (
    ResolvedStructuralComposer,
    ResolvedStructuralCompositionError,
    physical_source_address,
    r3_member_key,
)
from .engine import ResolvedStructuralGenerationError, ZiweiResolvedStructuralRuntime
from .integrity import (
    RESOLVED_STRUCTURAL_INTEGRITY_ALGORITHM_ID,
    RESOLVED_STRUCTURAL_INTEGRITY_ALGORITHM_VERSION,
    resolved_structural_fact_projection,
    resolved_structural_hash_bundle,
    validate_resolved_structural_components,
    validate_resolved_structural_state,
)
from .models import (
    RESOLVED_MEMBER_OFFSETS,
    RESOLVED_MEMBER_ROLE_BY_OFFSET,
    RESOLVED_MEMBER_ROLES,
    RESOLVED_STRUCTURAL_VIEW_STATE_SCHEMA,
    ResolvedSanfangSizhengFrameFact,
    ResolvedSanfangSizhengViewState,
    ResolvedStructuralHashBundle,
    ResolvedStructuralIntegrityDiagnostic,
    ResolvedStructuralIntegrityReport,
    ResolvedStructuralMemberRef,
)
from .profile import (
    RESOLVED_STRUCTURAL_COMPOSITION_ALGORITHM_ID,
    RESOLVED_STRUCTURAL_COMPOSITION_ALGORITHM_VERSION,
    ZIWEI_STRUCTURAL_V2_R5_PROFILE_ID,
    ZIWEI_STRUCTURAL_V2_R5_PROFILE_VERSION,
    ResolvedStructuralCompositionProfile,
    ziwei_structural_v2_r5_profile,
)

__all__ = [
    "RESOLVED_MEMBER_OFFSETS",
    "RESOLVED_MEMBER_ROLE_BY_OFFSET",
    "RESOLVED_MEMBER_ROLES",
    "RESOLVED_STRUCTURAL_COMPOSITION_ALGORITHM_ID",
    "RESOLVED_STRUCTURAL_COMPOSITION_ALGORITHM_VERSION",
    "RESOLVED_STRUCTURAL_INTEGRITY_ALGORITHM_ID",
    "RESOLVED_STRUCTURAL_INTEGRITY_ALGORITHM_VERSION",
    "RESOLVED_STRUCTURAL_VIEW_STATE_SCHEMA",
    "ResolvedSanfangSizhengFrameFact",
    "ResolvedSanfangSizhengViewState",
    "ResolvedStructuralComposer",
    "ResolvedStructuralCompositionError",
    "ResolvedStructuralCompositionProfile",
    "ResolvedStructuralGenerationError",
    "ResolvedStructuralHashBundle",
    "ResolvedStructuralIntegrityDiagnostic",
    "ResolvedStructuralIntegrityReport",
    "ResolvedStructuralMemberRef",
    "ZIWEI_STRUCTURAL_V2_R5_PROFILE_ID",
    "ZIWEI_STRUCTURAL_V2_R5_PROFILE_VERSION",
    "ZiweiResolvedStructuralRuntime",
    "physical_source_address",
    "r3_member_key",
    "resolved_structural_fact_projection",
    "resolved_structural_hash_bundle",
    "validate_resolved_structural_components",
    "validate_resolved_structural_state",
    "ziwei_structural_v2_r5_profile",
]

__version__ = "2.0.0-r5"
