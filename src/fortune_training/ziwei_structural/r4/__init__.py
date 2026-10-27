"""Ziwei Structural Runtime V2-R4 named Sanfang/Sizheng semantics."""

from .engine import NamedSemanticGenerationError, ZiweiNamedStructuralSemanticRuntime
from .integrity import (
    NAMED_SEMANTIC_INTEGRITY_ALGORITHM_ID,
    NAMED_SEMANTIC_INTEGRITY_ALGORITHM_VERSION,
    named_semantic_fact_projection,
    named_semantic_hash_bundle,
    validate_named_semantic_components,
    validate_named_semantic_state,
)
from .models import (
    NAMED_STRUCTURAL_SEMANTIC_STATE_SCHEMA,
    NamedSemanticHashBundle,
    NamedSemanticIntegrityDiagnostic,
    NamedSemanticIntegrityReport,
    NamedStructuralSemanticState,
    OppositionAxisFact,
    SanfangSizhengFrameFact,
    TrineGroupFact,
)
from .profile import (
    NAMED_STRUCTURAL_SEMANTIC_ALGORITHM_ID,
    NAMED_STRUCTURAL_SEMANTIC_ALGORITHM_VERSION,
    S04_CANONICAL_MANIFEST_OBJECT_SHA256,
    S04_CANONICAL_SOURCE_ID,
    S04_CANONICAL_SOURCE_SHA256,
    S04_SANFANG_SIZHENG_RULE_SET_ID,
    S04_SANFANG_SIZHENG_RULE_SET_VERSION,
    ZIWEI_STRUCTURAL_V2_R4_PROFILE_ID,
    ZIWEI_STRUCTURAL_V2_R4_PROFILE_VERSION,
    ResolvedNamedStructuralSemanticProfile,
    ziwei_structural_v2_r4_profile,
)
from .semantics import NamedStructuralSemanticCompiler, NamedStructuralSemanticError

__all__ = [
    "NAMED_SEMANTIC_INTEGRITY_ALGORITHM_ID",
    "NAMED_SEMANTIC_INTEGRITY_ALGORITHM_VERSION",
    "NAMED_STRUCTURAL_SEMANTIC_ALGORITHM_ID",
    "NAMED_STRUCTURAL_SEMANTIC_ALGORITHM_VERSION",
    "NAMED_STRUCTURAL_SEMANTIC_STATE_SCHEMA",
    "NamedSemanticGenerationError",
    "NamedSemanticHashBundle",
    "NamedSemanticIntegrityDiagnostic",
    "NamedSemanticIntegrityReport",
    "NamedStructuralSemanticCompiler",
    "NamedStructuralSemanticError",
    "NamedStructuralSemanticState",
    "OppositionAxisFact",
    "ResolvedNamedStructuralSemanticProfile",
    "S04_CANONICAL_MANIFEST_OBJECT_SHA256",
    "S04_CANONICAL_SOURCE_ID",
    "S04_CANONICAL_SOURCE_SHA256",
    "S04_SANFANG_SIZHENG_RULE_SET_ID",
    "S04_SANFANG_SIZHENG_RULE_SET_VERSION",
    "SanfangSizhengFrameFact",
    "TrineGroupFact",
    "ZIWEI_STRUCTURAL_V2_R4_PROFILE_ID",
    "ZIWEI_STRUCTURAL_V2_R4_PROFILE_VERSION",
    "ZiweiNamedStructuralSemanticRuntime",
    "named_semantic_fact_projection",
    "named_semantic_hash_bundle",
    "validate_named_semantic_components",
    "validate_named_semantic_state",
    "ziwei_structural_v2_r4_profile",
]

__version__ = "2.0.0-r4"
