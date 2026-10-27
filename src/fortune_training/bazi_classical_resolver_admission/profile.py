from __future__ import annotations

from dataclasses import dataclass


SOURCE_SEMANTIC_PROFILE_ID = "SHEN-ZPZQ-CH-09-CLASSICAL-INTERACTION-R1"
SOURCE_SEMANTIC_PROFILE_VERSION = "1.0.0"
SOURCE_SEMANTIC_PARTITION_ID = "SHEN_CLASSICAL_SOURCE:ZPZQ-CH-09:R1"
ADMISSION_PROFILE_ID = "BAZI-CLASSICAL-RESOLVER-ADMISSION-STRICT-R1"
ADMISSION_PROFILE_VERSION = "1.0.0"
ADMISSION_ALGORITHM_ID = "BAZI-CLASSICAL-RESOLVER-ADMISSION-SIDECAR-R1"
ADMISSION_ALGORITHM_VERSION = "1.0.0"

SOURCE_MEMBER_OCCURRENCE_IDS = (
    "ZPZQ-CL-09-003-002",
    "ZPZQ-CL-09-003-003",
    "ZPZQ-CL-09-003-004",
    "ZPZQ-CL-09-003-005",
    "ZPZQ-CL-09-003-007",
    "ZPZQ-CL-09-003-008",
    "ZPZQ-CL-09-003-009",
    "ZPZQ-CL-09-003-010",
    "ZPZQ-CL-09-005-002",
    "ZPZQ-CL-09-007-002",
    "ZPZQ-CL-09-007-003",
    "ZPZQ-CL-09-009-003",
    "ZPZQ-CL-09-009-004",
)

SUPPORTED_NEUTRAL_PRIMITIVES = (
    "EXACT_RAW_RELATION_OCCURRENCE_IDENTITY",
    "EXACT_PARTICIPANT_INSTANCE_IDENTITY",
    "RELATION_INCIDENCE_DEGREE",
    "RELATION_PAIR_TOPOLOGY",
    "EXACT_TEMPORAL_LAYER_FRAME",
)

ADMISSION_STATUSES = (
    "ADMITTED",
    "PRESERVED_NOT_ADMITTED",
    "PRESERVED_OUTSIDE_PROFILE",
)

ADMISSION_BLOCKER_CLASSES = (
    "SOURCE_SEMANTIC_PARTITION_MISMATCH",
    "STRUCTURAL_BINDING_PARTIAL",
    "CROSS_LAYER_EXTENSION_UNRESOLVED",
    "RESIDUAL_STRUCTURAL_CONSTRAINT",
    "MATERIALIZED_DEPENDENCY_MISSING",
    "UNEXPECTED_MATERIALIZED_DEPENDENCY",
)


@dataclass(frozen=True)
class ClassicalSourceSemanticProfile:
    profile_id: str = SOURCE_SEMANTIC_PROFILE_ID
    profile_version: str = SOURCE_SEMANTIC_PROFILE_VERSION
    partition_id: str = SOURCE_SEMANTIC_PARTITION_ID
    source_layer: str = "SHEN_CLASSICAL_SOURCE"
    source_id: str = "S14"
    source_chapter_id: str = "ZPZQ-CH-09"
    source_chapter_title: str = "论刑冲会合解法"
    member_source_occurrence_ids: tuple[str, ...] = SOURCE_MEMBER_OCCURRENCE_IDS
    semantic_role: str = "PARTITION_IDENTITY_ONLY"

    def validate(self) -> "ClassicalSourceSemanticProfile":
        if self != ClassicalSourceSemanticProfile():
            raise ValueError(f"unsupported Classical source semantic profile: {self!r}")
        return self


@dataclass(frozen=True)
class ClassicalInteractionResolverAdmissionProfile:
    profile_id: str = ADMISSION_PROFILE_ID
    profile_version: str = ADMISSION_PROFILE_VERSION
    algorithm_id: str = ADMISSION_ALGORITHM_ID
    algorithm_version: str = ADMISSION_ALGORITHM_VERSION
    source_semantic_profile_id: str = SOURCE_SEMANTIC_PROFILE_ID
    source_semantic_partition_id: str = SOURCE_SEMANTIC_PARTITION_ID
    allowed_source_layers: tuple[str, ...] = ("SHEN_CLASSICAL_SOURCE",)
    allowed_scope_compatibility_classes: tuple[str, ...] = ("DIRECT_SOURCE_SCOPE_MATCH",)
    allowed_structural_binding_classes: tuple[str, ...] = ("FULL_EXACT_BINDING_ENUMERATION",)
    partial_fragment_policy: str = "PRESERVE_NOT_ADMIT"
    cross_layer_extension_policy: str = "PRESERVE_NOT_ADMIT"
    source_layer_composition_policy: str = "SINGLE_PROFILE_PARTITION_ONLY"
    lifecycle_dependency_policy: str = "PARALLEL_NOT_GLOBAL_ADMISSION_GATE"
    unresolved_requirement_policy: str = "PASS_THROUGH_CLASSICAL_REQUIREMENTS"
    fragment_candidate_set_policy: str = "PRESERVE_ALL_NO_SELECTION"
    declared_dependency_policy: str = "REQUIRE_EXACT_MATERIALIZATION"
    source_unresolved_graph_requirement_policy: str = "PROVENANCE_ONLY_NEVER_DIRECT_PREDICATE"
    raw_relation_immutability_contract: str = "IMMUTABLE_EXACT_REFERENCE_ONLY"
    transition_separation_contract: str = "RAW_SET_CHANGE_NOT_CLASSICAL_ADMISSION_TRUTH"
    cartesian_expansion_policy: str = "NOT_RELEASED"
    cross_source_composition_policy: str = "NOT_RELEASED"

    def validate(self) -> "ClassicalInteractionResolverAdmissionProfile":
        if self != ClassicalInteractionResolverAdmissionProfile():
            raise ValueError(f"unsupported Classical resolver admission profile: {self!r}")
        return self


def shen_zpzq_ch09_classical_interaction_r1_profile() -> ClassicalSourceSemanticProfile:
    return ClassicalSourceSemanticProfile()


def bazi_classical_resolver_admission_strict_r1_profile() -> ClassicalInteractionResolverAdmissionProfile:
    return ClassicalInteractionResolverAdmissionProfile()
