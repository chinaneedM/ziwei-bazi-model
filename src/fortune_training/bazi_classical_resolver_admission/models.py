from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class NeutralDependencyMaterializationEvidence:
    primitive: str
    observation_ids: tuple[str, ...]
    materialization_status: str


@dataclass(frozen=True)
class ClassicalFragmentResolverAdmissionProjection:
    admission_projection_id: str
    source_envelope_id: str
    source_envelope_fact_hash: str
    source_envelope_computation_hash: str
    source_fragment_id: str
    source_fragment_fact_hash: str
    source_fragment_computation_hash: str
    binding_candidate_id: str
    source_occurrence_id: str
    source_layer: str
    source_semantic_profile_id: str
    source_semantic_partition_id: str
    partition_match: bool
    structural_binding_class: str
    source_scope_compatibility: str
    residual_unresolved_structural_constraint_ids: tuple[str, ...]
    neutral_observation_bundle_id: str
    required_neutral_primitives: tuple[str, ...]
    dependency_materialization_evidence: tuple[NeutralDependencyMaterializationEvidence, ...]
    unresolved_classical_semantic_requirements: tuple[str, ...]
    source_unresolved_graph_requirements_provenance: tuple[str, ...]
    admission_blocker_ids: tuple[str, ...]
    admission_status: str


@dataclass(frozen=True)
class SourceRecordResolverAdmissionCandidateSet:
    source_record_candidate_set_id: str
    source_layer: str
    source_occurrence_id: str
    source_fragment_ids: tuple[str, ...]
    admission_projection_ids: tuple[str, ...]
    member_selection_semantics: str = "NOT_RELEASED"
    member_coexistence_semantics: str = "NOT_RELEASED"
    member_exclusivity_semantics: str = "NOT_RELEASED"


@dataclass(frozen=True)
class ResolverAdmissionIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class ResolverAdmissionIntegrityReport:
    status: str
    diagnostics: tuple[ResolverAdmissionIntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-CLASSICAL-RESOLVER-ADMISSION-INTEGRITY-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class ResolverAdmissionHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-CLASSICAL-RESOLVER-ADMISSION-HASH-R1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class ClassicalResolverAdmissionEnvelopeCandidate:
    admission_envelope_id: str
    source_effect_envelope_id: str
    source_effect_fact_hash: str
    source_effect_computation_hash: str
    source_projection_fact_hash: str
    source_projection_computation_hash: str
    source_binding_fact_hash: str
    source_binding_computation_hash: str
    lineage_binding_keys: tuple[str, ...]
    fragment_admissions: tuple[ClassicalFragmentResolverAdmissionProjection, ...]
    source_record_candidate_sets: tuple[SourceRecordResolverAdmissionCandidateSet, ...]
    admitted_fragment_ids: tuple[str, ...]
    preserved_not_admitted_fragment_ids: tuple[str, ...]
    preserved_outside_profile_fragment_ids: tuple[str, ...]
    fragment_selection_semantics: str
    cross_outer_composition: str
    cartesian_expansion: str
    raw_relation_immutability_contract: str
    transition_separation_contract: str
    algorithm_versions: Mapping[str, str]
    integrity: ResolverAdmissionIntegrityReport
    hashes: ResolverAdmissionHashBundle


@dataclass(frozen=True)
class BaziClassicalResolverAdmissionResolution:
    schema: str
    status: str
    candidates: tuple[ClassicalResolverAdmissionEnvelopeCandidate, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
