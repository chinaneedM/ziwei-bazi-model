from __future__ import annotations

from typing import Any

from fortune_training.bazi_classical_non_selecting_participant_allocation.integrity import (
    allocation_hash_bundle,
    match_admission_envelope,
    match_effect_envelope,
    match_semantic_envelope,
    validate_allocation_envelope,
)
from fortune_training.bazi_classical_non_selecting_participant_allocation.profile import (
    bazi_classical_non_selecting_participant_allocation_r1_profile,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .models import (
    ClosureStatusFinalCandidateIndexEntry,
    ExactEffectChannelFinalCandidateIndexEntry,
    FinalClassicalEffectCandidate,
    FinalEffectEnvelopeHashBundle,
    FinalEffectEnvelopeIntegrityDiagnostic,
    FinalEffectEnvelopeIntegrityReport,
    MechanismKindFinalCandidateIndexEntry,
    MultiplicityFinalCandidateIndexEntry,
    SemanticKindFinalCandidateIndexEntry,
)
from .profile import (
    INDEX_SEMANTICS,
    SEMANTIC_TO_MECHANISM,
    ClassicalFinalEffectCandidateEnvelopeProfile,
)


def match_mechanism_envelope(source_allocation_envelope: Any, mechanism_resolution: Any) -> Any:
    matches = [
        row
        for row in mechanism_resolution.candidates
        if row.mechanism_closure_envelope_id
        == source_allocation_envelope.source_mechanism_closure_envelope_id
        and row.hashes.fact_hash == source_allocation_envelope.source_mechanism_closure_fact_hash
        and row.hashes.computation_hash
        == source_allocation_envelope.source_mechanism_closure_computation_hash
    ]
    if len(matches) != 1:
        raise ValueError(f"SOURCE_MECHANISM_ENVELOPE_MATCH_NOT_UNIQUE:{len(matches)}")
    return matches[0]


def replay_unit6_allocation_envelope(
    source_allocation_envelope: Any,
    source_mechanism_envelope: Any,
    source_semantic_envelope: Any,
    admission_envelope: Any,
    effect_envelope: Any,
) -> bool:
    if source_allocation_envelope.integrity.status != "PASS":
        return False
    profile = bazi_classical_non_selecting_participant_allocation_r1_profile()
    expected_lineage = (
        *source_mechanism_envelope.lineage_binding_keys,
        f"SOURCE_MECHANISM_CLOSURE_FACT:{source_mechanism_envelope.hashes.fact_hash}",
        f"SOURCE_MECHANISM_CLOSURE_COMPUTATION:{source_mechanism_envelope.hashes.computation_hash}",
        f"NON_SELECTING_ALLOCATION_PROFILE:{profile.profile_id}:{profile.profile_version}",
    )
    if (
        source_allocation_envelope.source_mechanism_closure_envelope_id
        != source_mechanism_envelope.mechanism_closure_envelope_id
        or source_allocation_envelope.source_mechanism_closure_fact_hash
        != source_mechanism_envelope.hashes.fact_hash
        or source_allocation_envelope.source_mechanism_closure_computation_hash
        != source_mechanism_envelope.hashes.computation_hash
        or source_allocation_envelope.source_semantic_projection_envelope_id
        != source_mechanism_envelope.source_semantic_projection_envelope_id
        or source_allocation_envelope.source_admission_envelope_id
        != source_mechanism_envelope.source_admission_envelope_id
        or source_allocation_envelope.source_effect_envelope_id
        != source_mechanism_envelope.source_effect_envelope_id
        or source_allocation_envelope.lineage_binding_keys != expected_lineage
        or source_allocation_envelope.algorithm_versions
        != {"non_selecting_allocation": profile.algorithm_version}
        or source_allocation_envelope.synthetic_permutation_generation
        != profile.synthetic_permutation_generation
        or source_allocation_envelope.synthetic_combination_generation
        != profile.synthetic_combination_generation
        or source_allocation_envelope.inferred_slot_instance_compatibility
        != profile.inferred_slot_instance_compatibility
        or source_allocation_envelope.participant_path_selection_semantics
        != profile.participant_path_selection_semantics
        or source_allocation_envelope.allocation_truth_semantics
        != profile.allocation_truth_semantics
        or source_allocation_envelope.allocation_operability_semantics
        != profile.allocation_operability_semantics
        or source_allocation_envelope.coexistence_semantics != profile.coexistence_semantics
        or source_allocation_envelope.exclusivity_semantics != profile.exclusivity_semantics
        or source_allocation_envelope.precedence_semantics != profile.precedence_semantics
        or source_allocation_envelope.priority_semantics != profile.priority_semantics
        or source_allocation_envelope.winner_loser_semantics != profile.winner_loser_semantics
        or source_allocation_envelope.relation_effect_state_semantics
        != profile.relation_effect_state_semantics
        or source_allocation_envelope.rewrite_application_semantics
        != profile.rewrite_application_semantics
        or source_allocation_envelope.fragment_selection_semantics
        != profile.fragment_selection_semantics
        or source_allocation_envelope.cross_outer_composition != profile.cross_outer_composition
        or source_allocation_envelope.cartesian_expansion != profile.cartesian_expansion
        or source_allocation_envelope.raw_relation_immutability_contract
        != profile.raw_relation_immutability_contract
    ):
        return False
    expected_hashes = allocation_hash_bundle(
        source_mechanism_envelope,
        source_allocation_envelope.fragment_allocation_projections,
        source_allocation_envelope.source_record_candidate_sets,
        source_allocation_envelope.multiplicity_domain_index,
        source_allocation_envelope.projected_allocation_domain_observation_ids,
        source_allocation_envelope.projected_path_candidate_ids,
        source_allocation_envelope.lineage_binding_keys,
        profile,
    )
    if expected_hashes != source_allocation_envelope.hashes:
        return False
    integrity = validate_allocation_envelope(
        source_mechanism_envelope,
        source_semantic_envelope,
        admission_envelope,
        effect_envelope,
        source_allocation_envelope.fragment_allocation_projections,
        source_allocation_envelope.source_record_candidate_sets,
        source_allocation_envelope.multiplicity_domain_index,
        source_allocation_envelope.projected_allocation_domain_observation_ids,
        source_allocation_envelope.projected_path_candidate_ids,
        source_allocation_envelope.lineage_binding_keys,
        profile,
        source_allocation_envelope.hashes,
    )
    if integrity.status != "PASS":
        return False
    expected_id = "CLASSICAL_NON_SELECTING_ALLOCATION_ENVELOPE:" + object_sha256({
        "source_mechanism_closure_envelope_id": source_mechanism_envelope.mechanism_closure_envelope_id,
        "source_mechanism_closure_fact_hash": source_mechanism_envelope.hashes.fact_hash,
        "fact_hash": source_allocation_envelope.hashes.fact_hash,
    })
    return source_allocation_envelope.allocation_envelope_id == expected_id


def final_candidate_id(
    semantic_candidate: Any,
    mechanism_proposal: Any,
    allocation_elaboration: Any,
) -> str:
    return "CLASSICAL_FINAL_EFFECT_CANDIDATE:" + object_sha256({
        "source_semantic_candidate_id": semantic_candidate.semantic_candidate_id,
        "source_mechanism_proposal_id": mechanism_proposal.mechanism_proposal_id,
        "source_allocation_elaboration_id": allocation_elaboration.proposal_allocation_elaboration_id,
        "source_fragment_id": semantic_candidate.source_fragment_id,
        "binding_candidate_id": semantic_candidate.binding_candidate_id,
        "target_exact_relation_id": semantic_candidate.target_exact_relation_id,
        "effect_facet": semantic_candidate.effect_facet,
    })


def expected_final_candidate(
    semantic_candidate: Any,
    mechanism_proposal: Any,
    allocation_elaboration: Any,
    semantic_envelope: Any,
    mechanism_envelope: Any,
    allocation_envelope: Any,
    semantic_fragment: Any,
    mechanism_fragment: Any,
    allocation_fragment: Any,
    profile: ClassicalFinalEffectCandidateEnvelopeProfile,
) -> FinalClassicalEffectCandidate:
    return FinalClassicalEffectCandidate(
        final_candidate_id=final_candidate_id(
            semantic_candidate, mechanism_proposal, allocation_elaboration
        ),
        source_semantic_candidate_id=semantic_candidate.semantic_candidate_id,
        source_mechanism_proposal_id=mechanism_proposal.mechanism_proposal_id,
        source_allocation_elaboration_id=(
            allocation_elaboration.proposal_allocation_elaboration_id
        ),
        source_semantic_projection_envelope_id=semantic_envelope.semantic_projection_envelope_id,
        source_semantic_projection_fact_hash=semantic_envelope.hashes.fact_hash,
        source_semantic_projection_computation_hash=semantic_envelope.hashes.computation_hash,
        source_mechanism_closure_envelope_id=mechanism_envelope.mechanism_closure_envelope_id,
        source_mechanism_closure_fact_hash=mechanism_envelope.hashes.fact_hash,
        source_mechanism_closure_computation_hash=mechanism_envelope.hashes.computation_hash,
        source_allocation_envelope_id=allocation_envelope.allocation_envelope_id,
        source_allocation_fact_hash=allocation_envelope.hashes.fact_hash,
        source_allocation_computation_hash=allocation_envelope.hashes.computation_hash,
        source_admission_envelope_id=semantic_envelope.source_admission_envelope_id,
        source_effect_envelope_id=semantic_envelope.source_effect_envelope_id,
        source_fragment_semantic_projection_id=semantic_fragment.fragment_semantic_projection_id,
        source_fragment_governance_projection_id=mechanism_fragment.fragment_governance_projection_id,
        source_fragment_allocation_projection_id=allocation_fragment.fragment_allocation_projection_id,
        source_fragment_id=semantic_candidate.source_fragment_id,
        source_fragment_fact_hash=semantic_candidate.source_fragment_fact_hash,
        source_fragment_computation_hash=semantic_candidate.source_fragment_computation_hash,
        binding_candidate_id=semantic_candidate.binding_candidate_id,
        source_occurrence_id=semantic_candidate.source_occurrence_id,
        graph_record_id=semantic_candidate.graph_record_id,
        interaction_assertion_id=semantic_candidate.interaction_assertion_id,
        source_claim_edge_id=semantic_candidate.source_claim_edge_id,
        source_claim_edge_class=semantic_candidate.source_claim_edge_class,
        source_assertion_class=semantic_candidate.source_assertion_class,
        source_evidence_mode=semantic_candidate.source_evidence_mode,
        exact_source_fragments=semantic_candidate.exact_source_fragments,
        source_semantic_profile_id=semantic_candidate.source_semantic_profile_id,
        source_semantic_partition_id=semantic_candidate.source_semantic_partition_id,
        target_effect_channel_id=semantic_candidate.target_effect_channel_id,
        target_exact_relation_id=semantic_candidate.target_exact_relation_id,
        actor_exact_relation_ids=semantic_candidate.actor_exact_relation_ids,
        actor_exact_participant_ids=semantic_candidate.actor_exact_participant_ids,
        context_exact_participant_ids=semantic_candidate.context_exact_participant_ids,
        effect_facet=semantic_candidate.effect_facet,
        semantic_candidate_kind=semantic_candidate.semantic_candidate_kind,
        mechanism_proposal_kind=mechanism_proposal.mechanism_proposal_kind,
        unresolved_classical_semantic_requirements=(
            semantic_candidate.unresolved_classical_semantic_requirements
        ),
        closure_governance_rows=mechanism_proposal.closure_governance_rows,
        multiplicity_references=semantic_candidate.multiplicity_references,
        allocation_domain_observations=(
            allocation_elaboration.allocation_domain_observations
        ),
        source_narrative_chain_ids_provenance=(
            mechanism_proposal.source_narrative_chain_ids_provenance
        ),
        source_unresolved_graph_requirements_provenance=(
            mechanism_proposal.source_unresolved_graph_requirements_provenance
        ),
        final_candidate_semantics=profile.final_candidate_semantics,
    )


def final_effect_hash_bundle(
    source_allocation_envelope: Any,
    fragment_envelopes: tuple[Any, ...],
    source_record_candidate_sets: tuple[Any, ...],
    effect_channel_index: tuple[Any, ...],
    semantic_kind_index: tuple[Any, ...],
    mechanism_kind_index: tuple[Any, ...],
    closure_status_index: tuple[Any, ...],
    multiplicity_index: tuple[Any, ...],
    projected_final_candidate_ids: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ClassicalFinalEffectCandidateEnvelopeProfile,
) -> FinalEffectEnvelopeHashBundle:
    fact_payload = {
        "source_allocation_envelope_id": source_allocation_envelope.allocation_envelope_id,
        "source_allocation_fact_hash": source_allocation_envelope.hashes.fact_hash,
        "source_mechanism_closure_envelope_id": (
            source_allocation_envelope.source_mechanism_closure_envelope_id
        ),
        "source_semantic_projection_envelope_id": (
            source_allocation_envelope.source_semantic_projection_envelope_id
        ),
        "source_admission_envelope_id": source_allocation_envelope.source_admission_envelope_id,
        "source_effect_envelope_id": source_allocation_envelope.source_effect_envelope_id,
        "fragment_envelopes": json_value(fragment_envelopes),
        "source_record_candidate_sets": json_value(source_record_candidate_sets),
        "effect_channel_index": json_value(effect_channel_index),
        "semantic_kind_index": json_value(semantic_kind_index),
        "mechanism_kind_index": json_value(mechanism_kind_index),
        "closure_status_index": json_value(closure_status_index),
        "multiplicity_index": json_value(multiplicity_index),
        "projected_final_candidate_ids": projected_final_candidate_ids,
        "final_candidate_semantics": profile.final_candidate_semantics,
        "candidate_truth_semantics": profile.candidate_truth_semantics,
        "candidate_operability_semantics": profile.candidate_operability_semantics,
        "candidate_applicability_semantics": profile.candidate_applicability_semantics,
        "mechanism_execution_semantics": profile.mechanism_execution_semantics,
        "rewrite_application_semantics": profile.rewrite_application_semantics,
        "lifecycle_truth_gate": profile.lifecycle_truth_gate,
        "candidate_coexistence_semantics": profile.candidate_coexistence_semantics,
        "candidate_exclusivity_semantics": profile.candidate_exclusivity_semantics,
        "candidate_conflict_semantics": profile.candidate_conflict_semantics,
        "precedence_semantics": profile.precedence_semantics,
        "priority_semantics": profile.priority_semantics,
        "winner_loser_semantics": profile.winner_loser_semantics,
        "participant_path_selection_semantics": profile.participant_path_selection_semantics,
        "relation_effect_state_semantics": profile.relation_effect_state_semantics,
        "graph_mutation_fixpoint_semantics": profile.graph_mutation_fixpoint_semantics,
        "execution_readiness_semantics": profile.execution_readiness_semantics,
        "synthetic_permutation_generation": profile.synthetic_permutation_generation,
        "synthetic_combination_generation": profile.synthetic_combination_generation,
        "inferred_slot_instance_compatibility": profile.inferred_slot_instance_compatibility,
        "fragment_selection_semantics": profile.fragment_selection_semantics,
        "cross_outer_composition": profile.cross_outer_composition,
        "cross_source_composition": profile.cross_source_composition,
        "cartesian_expansion": profile.cartesian_expansion,
        "raw_relation_immutability_contract": profile.raw_relation_immutability_contract,
    }
    computation_payload = {
        "facts": fact_payload,
        "source_allocation_computation_hash": source_allocation_envelope.hashes.computation_hash,
        "source_allocation_lineage_binding_keys": source_allocation_envelope.lineage_binding_keys,
        "lineage_binding_keys": lineage_binding_keys,
        "profile": json_value(profile),
    }
    return FinalEffectEnvelopeHashBundle(
        fact_hash=object_sha256(fact_payload),
        computation_hash=object_sha256(computation_payload),
    )


def build_expected_indexes(final_candidates: tuple[Any, ...]) -> tuple[tuple[Any, ...], ...]:
    effect: dict[tuple[str, str], list[str]] = {}
    semantic: dict[str, list[str]] = {}
    mechanism: dict[str, list[str]] = {}
    closure: dict[tuple[str, str], list[str]] = {}
    multiplicity: dict[str, dict[str, list[str]]] = {}
    for candidate in final_candidates:
        effect.setdefault(
            (candidate.target_exact_relation_id, candidate.effect_facet), []
        ).append(candidate.final_candidate_id)
        semantic.setdefault(candidate.semantic_candidate_kind, []).append(
            candidate.final_candidate_id
        )
        mechanism.setdefault(candidate.mechanism_proposal_kind, []).append(
            candidate.final_candidate_id
        )
        for row in candidate.closure_governance_rows:
            closure.setdefault(
                (row.closure_requirement_id, row.runtime_dependency_status), []
            ).append(candidate.final_candidate_id)
        for observation in candidate.allocation_domain_observations:
            group = multiplicity.setdefault(
                observation.multiplicity_constraint_id,
                {"candidates": [], "domains": [], "paths": []},
            )
            group["candidates"].append(candidate.final_candidate_id)
            group["domains"].append(observation.allocation_domain_observation_id)
            group["paths"].extend(
                path.path_candidate_id for path in observation.path_candidates
            )
    effect_index = tuple(
        ExactEffectChannelFinalCandidateIndexEntry(
            target_exact_relation_id=key[0],
            effect_facet=key[1],
            final_candidate_ids=tuple(ids),
            index_semantics=INDEX_SEMANTICS,
        )
        for key, ids in sorted(effect.items())
    )
    semantic_index = tuple(
        SemanticKindFinalCandidateIndexEntry(
            semantic_candidate_kind=key,
            final_candidate_ids=tuple(ids),
            index_semantics=INDEX_SEMANTICS,
        )
        for key, ids in sorted(semantic.items())
    )
    mechanism_index = tuple(
        MechanismKindFinalCandidateIndexEntry(
            mechanism_proposal_kind=key,
            final_candidate_ids=tuple(ids),
            index_semantics=INDEX_SEMANTICS,
        )
        for key, ids in sorted(mechanism.items())
    )
    closure_index = tuple(
        ClosureStatusFinalCandidateIndexEntry(
            closure_requirement_id=key[0],
            runtime_dependency_status=key[1],
            final_candidate_ids=tuple(ids),
            index_semantics=INDEX_SEMANTICS,
        )
        for key, ids in sorted(closure.items())
    )
    multiplicity_index = tuple(
        MultiplicityFinalCandidateIndexEntry(
            multiplicity_constraint_id=key,
            final_candidate_ids=tuple(group["candidates"]),
            allocation_domain_observation_ids=tuple(group["domains"]),
            path_candidate_ids=tuple(group["paths"]),
            index_semantics=INDEX_SEMANTICS,
        )
        for key, group in sorted(multiplicity.items())
    )
    return (
        effect_index,
        semantic_index,
        mechanism_index,
        closure_index,
        multiplicity_index,
    )


def validate_final_effect_envelope(
    source_allocation_envelope: Any,
    source_mechanism_envelope: Any,
    source_semantic_envelope: Any,
    admission_envelope: Any,
    effect_envelope: Any,
    fragment_envelopes: tuple[Any, ...],
    source_record_candidate_sets: tuple[Any, ...],
    effect_channel_index: tuple[Any, ...],
    semantic_kind_index: tuple[Any, ...],
    mechanism_kind_index: tuple[Any, ...],
    closure_status_index: tuple[Any, ...],
    multiplicity_index: tuple[Any, ...],
    projected_final_candidate_ids: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ClassicalFinalEffectCandidateEnvelopeProfile,
    hashes: FinalEffectEnvelopeHashBundle,
) -> FinalEffectEnvelopeIntegrityReport:
    diagnostics: list[FinalEffectEnvelopeIntegrityDiagnostic] = []

    def diag(code: str, path: str, detail: str) -> None:
        diagnostics.append(FinalEffectEnvelopeIntegrityDiagnostic(code, path, detail))

    if not replay_unit6_allocation_envelope(
        source_allocation_envelope,
        source_mechanism_envelope,
        source_semantic_envelope,
        admission_envelope,
        effect_envelope,
    ):
        diag(
            "UPSTREAM_UNIT6_ALLOCATION_REPLAY_MISMATCH",
            "source_allocation_envelope",
            source_allocation_envelope.allocation_envelope_id,
        )

    expected_lineage = (
        *source_allocation_envelope.lineage_binding_keys,
        f"SOURCE_ALLOCATION_FACT:{source_allocation_envelope.hashes.fact_hash}",
        f"SOURCE_ALLOCATION_COMPUTATION:{source_allocation_envelope.hashes.computation_hash}",
        f"FINAL_EFFECT_ENVELOPE_PROFILE:{profile.profile_id}:{profile.profile_version}",
    )
    if lineage_binding_keys != expected_lineage:
        diag("FINAL_EFFECT_LINEAGE_MISMATCH", "lineage_binding_keys", str(lineage_binding_keys))

    semantic_fragments = {
        row.fragment_semantic_projection_id: row
        for row in source_semantic_envelope.fragment_projections
    }
    mechanism_fragments = {
        row.fragment_governance_projection_id: row
        for row in source_mechanism_envelope.fragment_governance_projections
    }
    allocation_fragments = {
        row.fragment_allocation_projection_id: row
        for row in source_allocation_envelope.fragment_allocation_projections
    }
    if (
        len(semantic_fragments) != len(source_semantic_envelope.fragment_projections)
        or len(mechanism_fragments)
        != len(source_mechanism_envelope.fragment_governance_projections)
        or len(allocation_fragments)
        != len(source_allocation_envelope.fragment_allocation_projections)
    ):
        diag("UPSTREAM_FRAGMENT_ID_DUPLICATE", "upstream_fragments", "duplicate fragment id")

    if len(fragment_envelopes) != len(source_allocation_envelope.fragment_allocation_projections):
        diag(
            "FINAL_FRAGMENT_CARDINALITY_MISMATCH",
            "fragment_envelopes",
            str(len(fragment_envelopes)),
        )

    all_final_candidates: list[FinalClassicalEffectCandidate] = []
    seen_final_ids: set[str] = set()
    final_by_source_fragment: dict[str, Any] = {}
    for final_fragment, allocation_fragment in zip(
        fragment_envelopes,
        source_allocation_envelope.fragment_allocation_projections,
        strict=False,
    ):
        mechanism_fragment = mechanism_fragments.get(
            allocation_fragment.source_fragment_governance_projection_id
        )
        semantic_fragment = semantic_fragments.get(
            allocation_fragment.source_fragment_semantic_projection_id
        )
        if mechanism_fragment is None or semantic_fragment is None:
            diag(
                "UPSTREAM_FRAGMENT_CHAIN_MISSING",
                final_fragment.final_fragment_id,
                allocation_fragment.source_fragment_id,
            )
            continue
        final_by_source_fragment[allocation_fragment.source_fragment_id] = final_fragment
        candidate_by_id = {
            row.semantic_candidate_id: row for row in semantic_fragment.semantic_candidates
        }
        proposal_by_candidate = {
            row.source_semantic_candidate_id: row
            for row in mechanism_fragment.mechanism_proposals
        }
        elaboration_by_candidate = {
            row.source_semantic_candidate_id: row
            for row in allocation_fragment.proposal_elaborations
        }
        if (
            len(candidate_by_id) != len(semantic_fragment.semantic_candidates)
            or len(proposal_by_candidate) != len(mechanism_fragment.mechanism_proposals)
            or len(elaboration_by_candidate) != len(allocation_fragment.proposal_elaborations)
        ):
            diag(
                "UPSTREAM_CANDIDATE_CHAIN_ID_DUPLICATE",
                allocation_fragment.source_fragment_id,
                "candidate/proposal/elaboration identity duplicate",
            )
        expected_source_ids = tuple(row.semantic_candidate_id for row in semantic_fragment.semantic_candidates)
        expected_proposal_ids = tuple(
            proposal_by_candidate[candidate_id].mechanism_proposal_id
            for candidate_id in expected_source_ids
            if candidate_id in proposal_by_candidate
        )
        expected_elab_ids = tuple(
            elaboration_by_candidate[candidate_id].proposal_allocation_elaboration_id
            for candidate_id in expected_source_ids
            if candidate_id in elaboration_by_candidate
        )
        if (
            set(candidate_by_id) != set(proposal_by_candidate)
            or set(candidate_by_id) != set(elaboration_by_candidate)
            or final_fragment.source_fragment_semantic_projection_id
            != semantic_fragment.fragment_semantic_projection_id
            or final_fragment.source_fragment_governance_projection_id
            != mechanism_fragment.fragment_governance_projection_id
            or final_fragment.source_fragment_allocation_projection_id
            != allocation_fragment.fragment_allocation_projection_id
            or final_fragment.source_fragment_id != allocation_fragment.source_fragment_id
            or final_fragment.source_occurrence_id != allocation_fragment.source_occurrence_id
            or final_fragment.binding_candidate_id != allocation_fragment.binding_candidate_id
            or final_fragment.source_projection_status != semantic_fragment.projection_status
            or final_fragment.source_governance_status != mechanism_fragment.governance_status
            or final_fragment.source_allocation_status != allocation_fragment.allocation_status
            or final_fragment.source_semantic_candidate_ids != expected_source_ids
            or final_fragment.source_mechanism_proposal_ids != expected_proposal_ids
            or final_fragment.source_allocation_elaboration_ids != expected_elab_ids
            or len(final_fragment.final_candidates) != len(expected_source_ids)
        ):
            diag(
                "FINAL_FRAGMENT_SOURCE_CHAIN_REPLAY_MISMATCH",
                final_fragment.final_fragment_id,
                allocation_fragment.source_fragment_id,
            )
        expected_status = (
            "FINAL_EFFECT_CANDIDATES_ASSEMBLED"
            if expected_source_ids
            else "PRESERVED_ZERO_FINAL_EFFECT_CANDIDATES"
        )
        if final_fragment.final_fragment_status != expected_status:
            diag(
                "FINAL_FRAGMENT_STATUS_MISMATCH",
                final_fragment.final_fragment_id,
                final_fragment.final_fragment_status,
            )
        expected_entries: list[FinalClassicalEffectCandidate] = []
        for candidate_id in expected_source_ids:
            semantic_candidate = candidate_by_id.get(candidate_id)
            mechanism_proposal = proposal_by_candidate.get(candidate_id)
            allocation_elaboration = elaboration_by_candidate.get(candidate_id)
            if semantic_candidate is None or mechanism_proposal is None or allocation_elaboration is None:
                continue
            if SEMANTIC_TO_MECHANISM.get(semantic_candidate.semantic_candidate_kind) != mechanism_proposal.mechanism_proposal_kind:
                diag(
                    "SEMANTIC_MECHANISM_KIND_MISMATCH",
                    candidate_id,
                    mechanism_proposal.mechanism_proposal_kind,
                )
            if tuple(mechanism_proposal.unresolved_classical_semantic_requirements) != tuple(
                semantic_candidate.unresolved_classical_semantic_requirements
            ):
                diag(
                    "CLOSURE_REQUIREMENT_PASS_THROUGH_MISMATCH",
                    candidate_id,
                    str(mechanism_proposal.unresolved_classical_semantic_requirements),
                )
            if allocation_elaboration.mechanism_proposal_kind != mechanism_proposal.mechanism_proposal_kind:
                diag(
                    "UNIT6_MECHANISM_KIND_MISMATCH",
                    candidate_id,
                    allocation_elaboration.mechanism_proposal_kind,
                )
            expected_entry = expected_final_candidate(
                semantic_candidate,
                mechanism_proposal,
                allocation_elaboration,
                source_semantic_envelope,
                source_mechanism_envelope,
                source_allocation_envelope,
                semantic_fragment,
                mechanism_fragment,
                allocation_fragment,
                profile,
            )
            expected_entries.append(expected_entry)
        if tuple(expected_entries) != final_fragment.final_candidates:
            diag(
                "FINAL_CANDIDATE_SEMANTIC_REPLAY_MISMATCH",
                final_fragment.final_fragment_id,
                "candidate chain payload differs from independently replayed upstream",
            )
        expected_ids = tuple(row.final_candidate_id for row in expected_entries)
        if final_fragment.final_candidate_ids != expected_ids:
            diag(
                "FINAL_FRAGMENT_CANDIDATE_ID_INDEX_MISMATCH",
                final_fragment.final_fragment_id,
                str(final_fragment.final_candidate_ids),
            )
        expected_fragment_id = "CLASSICAL_FINAL_EFFECT_FRAGMENT:" + object_sha256({
            "source_fragment_semantic_projection_id": semantic_fragment.fragment_semantic_projection_id,
            "source_fragment_governance_projection_id": mechanism_fragment.fragment_governance_projection_id,
            "source_fragment_allocation_projection_id": allocation_fragment.fragment_allocation_projection_id,
            "final_candidate_ids": expected_ids,
            "final_fragment_status": expected_status,
        })
        if final_fragment.final_fragment_id != expected_fragment_id:
            diag(
                "FINAL_FRAGMENT_ID_REPLAY_MISMATCH",
                final_fragment.final_fragment_id,
                expected_fragment_id,
            )
        for row in final_fragment.final_candidates:
            if row.final_candidate_id in seen_final_ids:
                diag("FINAL_CANDIDATE_ID_DUPLICATE", row.final_candidate_id, row.source_semantic_candidate_id)
            seen_final_ids.add(row.final_candidate_id)
            all_final_candidates.append(row)

    expected_global_ids = tuple(row.final_candidate_id for row in all_final_candidates)
    if projected_final_candidate_ids != expected_global_ids:
        diag(
            "FINAL_CANDIDATE_GLOBAL_INDEX_MISMATCH",
            "projected_final_candidate_ids",
            str(projected_final_candidate_ids),
        )

    upstream_sets = {
        row.source_record_candidate_set_id: row
        for row in source_allocation_envelope.source_record_candidate_sets
    }
    if len(source_record_candidate_sets) != len(upstream_sets):
        diag(
            "FINAL_SOURCE_RECORD_SET_CARDINALITY_MISMATCH",
            "source_record_candidate_sets",
            str(len(source_record_candidate_sets)),
        )
    for row in source_record_candidate_sets:
        upstream = upstream_sets.get(row.source_record_candidate_set_id)
        if upstream is None:
            diag("FINAL_SOURCE_RECORD_SET_UPSTREAM_MISSING", row.source_record_candidate_set_id, row.source_occurrence_id)
            continue
        expected_fragments = tuple(
            final_by_source_fragment[source_fragment_id].final_fragment_id
            for source_fragment_id in upstream.source_fragment_ids
            if source_fragment_id in final_by_source_fragment
        )
        expected_candidates = tuple(
            candidate_id
            for source_fragment_id in upstream.source_fragment_ids
            if source_fragment_id in final_by_source_fragment
            for candidate_id in final_by_source_fragment[source_fragment_id].final_candidate_ids
        )
        if (
            row.source_layer != upstream.source_layer
            or row.source_occurrence_id != upstream.source_occurrence_id
            or row.source_fragment_ids != upstream.source_fragment_ids
            or row.final_fragment_ids != expected_fragments
            or row.final_candidate_ids != expected_candidates
            or any(
                value != "NOT_RELEASED"
                for value in (
                    row.member_selection_semantics,
                    row.member_coexistence_semantics,
                    row.member_exclusivity_semantics,
                    row.member_priority_semantics,
                    row.member_conflict_semantics,
                )
            )
        ):
            diag(
                "FINAL_SOURCE_RECORD_SET_REPLAY_MISMATCH",
                row.source_record_candidate_set_id,
                row.source_occurrence_id,
            )

    expected_indexes = build_expected_indexes(tuple(all_final_candidates))
    actual_indexes = (
        effect_channel_index,
        semantic_kind_index,
        mechanism_kind_index,
        closure_status_index,
        multiplicity_index,
    )
    if actual_indexes != expected_indexes:
        diag("FINAL_INDEX_REPLAY_MISMATCH", "indexes", "identity-only index mismatch")

    expected_hashes = final_effect_hash_bundle(
        source_allocation_envelope,
        fragment_envelopes,
        source_record_candidate_sets,
        effect_channel_index,
        semantic_kind_index,
        mechanism_kind_index,
        closure_status_index,
        multiplicity_index,
        projected_final_candidate_ids,
        lineage_binding_keys,
        profile,
    )
    if expected_hashes != hashes:
        diag("FINAL_EFFECT_HASH_REPLAY_MISMATCH", "hashes", hashes.fact_hash)

    return FinalEffectEnvelopeIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )
