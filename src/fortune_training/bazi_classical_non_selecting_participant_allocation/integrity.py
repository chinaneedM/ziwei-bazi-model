from __future__ import annotations

from typing import Any

from fortune_training.bazi_classical_effect_semantic_candidate.models import (
    BaziClassicalEffectSemanticCandidateProjectionResolution,
)
from fortune_training.bazi_classical_semantic_closure_governance.integrity import (
    mechanism_closure_hash_bundle,
    replay_unit4_semantic_envelope,
    validate_mechanism_closure_envelope,
)
from fortune_training.bazi_classical_semantic_closure_governance.profile import (
    bazi_classical_semantic_mechanism_closure_governance_r1_profile,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .domain import build_unordered_path_candidate, classify_allocation_domain
from .models import (
    AllocationHashBundle,
    AllocationIntegrityDiagnostic,
    AllocationIntegrityReport,
)
from .profile import (
    ALLOCATION_MECHANISM_PROPOSAL_KIND,
    ALLOCATION_SEMANTIC_CANDIDATE_KIND,
    EXPECTED_ALLOCATION_CLOSURE_ROWS,
    ClassicalNonSelectingParticipantAllocationProfile,
)


def match_semantic_envelope(source_mechanism_envelope: Any, semantic_resolution: Any) -> Any:
    matches = [
        row
        for row in semantic_resolution.candidates
        if row.semantic_projection_envelope_id
        == source_mechanism_envelope.source_semantic_projection_envelope_id
        and row.hashes.fact_hash
        == source_mechanism_envelope.source_semantic_projection_fact_hash
        and row.hashes.computation_hash
        == source_mechanism_envelope.source_semantic_projection_computation_hash
    ]
    if len(matches) != 1:
        raise ValueError(f"SOURCE_SEMANTIC_ENVELOPE_MATCH_NOT_UNIQUE:{len(matches)}")
    return matches[0]


def match_admission_envelope(source_semantic_envelope: Any, admission_resolution: Any) -> Any:
    matches = [
        row
        for row in admission_resolution.candidates
        if row.admission_envelope_id == source_semantic_envelope.source_admission_envelope_id
        and row.hashes.fact_hash == source_semantic_envelope.source_admission_fact_hash
        and row.hashes.computation_hash
        == source_semantic_envelope.source_admission_computation_hash
    ]
    if len(matches) != 1:
        raise ValueError(f"SOURCE_ADMISSION_ENVELOPE_MATCH_NOT_UNIQUE:{len(matches)}")
    return matches[0]


def match_effect_envelope(source_semantic_envelope: Any, effect_resolution: Any) -> Any:
    matches = [
        row
        for row in effect_resolution.candidates
        if row.envelope_id == source_semantic_envelope.source_effect_envelope_id
        and row.hashes.fact_hash == source_semantic_envelope.source_effect_fact_hash
        and row.hashes.computation_hash
        == source_semantic_envelope.source_effect_computation_hash
    ]
    if len(matches) != 1:
        raise ValueError(f"SOURCE_EFFECT_ENVELOPE_MATCH_NOT_UNIQUE:{len(matches)}")
    return matches[0]


def replay_unit5_mechanism_closure_envelope(
    source_mechanism_envelope: Any,
    source_semantic_envelope: Any,
    admission_envelope: Any,
    effect_envelope: Any,
) -> bool:
    if source_mechanism_envelope.integrity.status != "PASS":
        return False
    if not replay_unit4_semantic_envelope(
        source_semantic_envelope,
        admission_envelope,
        effect_envelope,
    ):
        return False
    profile = bazi_classical_semantic_mechanism_closure_governance_r1_profile()
    expected_lineage = (
        *source_semantic_envelope.lineage_binding_keys,
        f"SOURCE_SEMANTIC_PROJECTION_FACT:{source_semantic_envelope.hashes.fact_hash}",
        f"SOURCE_SEMANTIC_PROJECTION_COMPUTATION:{source_semantic_envelope.hashes.computation_hash}",
        f"MECHANISM_CLOSURE_PROFILE:{profile.profile_id}:{profile.profile_version}",
    )
    if (
        source_mechanism_envelope.source_semantic_projection_envelope_id
        != source_semantic_envelope.semantic_projection_envelope_id
        or source_mechanism_envelope.source_semantic_projection_fact_hash
        != source_semantic_envelope.hashes.fact_hash
        or source_mechanism_envelope.source_semantic_projection_computation_hash
        != source_semantic_envelope.hashes.computation_hash
        or source_mechanism_envelope.source_admission_envelope_id
        != source_semantic_envelope.source_admission_envelope_id
        or source_mechanism_envelope.source_effect_envelope_id
        != source_semantic_envelope.source_effect_envelope_id
        or source_mechanism_envelope.lineage_binding_keys != expected_lineage
        or source_mechanism_envelope.algorithm_versions
        != {"mechanism_closure_governance": profile.algorithm_version}
        or source_mechanism_envelope.mechanism_proposal_semantics
        != profile.mechanism_proposal_semantics
        or source_mechanism_envelope.mechanism_execution_semantics
        != profile.mechanism_execution_semantics
        or source_mechanism_envelope.rewrite_application_semantics
        != profile.rewrite_application_semantics
        or source_mechanism_envelope.candidate_truth_semantics
        != profile.candidate_truth_semantics
        or source_mechanism_envelope.candidate_applicability_semantics
        != profile.candidate_applicability_semantics
        or source_mechanism_envelope.candidate_coexistence_semantics
        != profile.candidate_coexistence_semantics
        or source_mechanism_envelope.candidate_exclusivity_semantics
        != profile.candidate_exclusivity_semantics
        or source_mechanism_envelope.candidate_conflict_semantics
        != profile.candidate_conflict_semantics
        or source_mechanism_envelope.precedence_semantics != profile.precedence_semantics
        or source_mechanism_envelope.priority_semantics != profile.priority_semantics
        or source_mechanism_envelope.winner_loser_semantics
        != profile.winner_loser_semantics
        or source_mechanism_envelope.state_transition_semantics
        != profile.state_transition_semantics
        or source_mechanism_envelope.lifecycle_truth_gate != profile.lifecycle_truth_gate
        or source_mechanism_envelope.fragment_selection_semantics
        != profile.fragment_selection_semantics
        or source_mechanism_envelope.cross_outer_composition
        != profile.cross_outer_composition
        or source_mechanism_envelope.cartesian_expansion != profile.cartesian_expansion
        or source_mechanism_envelope.raw_relation_immutability_contract
        != profile.raw_relation_immutability_contract
    ):
        return False

    expected_hashes = mechanism_closure_hash_bundle(
        source_semantic_envelope,
        source_mechanism_envelope.fragment_governance_projections,
        source_mechanism_envelope.source_record_candidate_sets,
        source_mechanism_envelope.closure_requirement_index,
        source_mechanism_envelope.mechanism_proposal_index,
        source_mechanism_envelope.projected_mechanism_proposal_ids,
        source_mechanism_envelope.lineage_binding_keys,
        profile,
    )
    if expected_hashes != source_mechanism_envelope.hashes:
        return False
    validation = validate_mechanism_closure_envelope(
        source_semantic_envelope,
        admission_envelope,
        effect_envelope,
        source_mechanism_envelope.fragment_governance_projections,
        source_mechanism_envelope.source_record_candidate_sets,
        source_mechanism_envelope.closure_requirement_index,
        source_mechanism_envelope.mechanism_proposal_index,
        source_mechanism_envelope.projected_mechanism_proposal_ids,
        source_mechanism_envelope.lineage_binding_keys,
        profile,
        source_mechanism_envelope.hashes,
    )
    if validation.status != "PASS":
        return False
    expected_id = "CLASSICAL_SEMANTIC_MECHANISM_CLOSURE_ENVELOPE:" + object_sha256({
        "source_semantic_projection_envelope_id": (
            source_semantic_envelope.semantic_projection_envelope_id
        ),
        "source_semantic_projection_fact_hash": source_semantic_envelope.hashes.fact_hash,
        "fact_hash": source_mechanism_envelope.hashes.fact_hash,
    })
    return source_mechanism_envelope.mechanism_closure_envelope_id == expected_id


def _allocation_closure_rows_valid(proposal: Any) -> bool:
    actual = {
        row.closure_requirement_id: row.runtime_dependency_status
        for row in proposal.closure_governance_rows
    }
    return (
        len(actual) == len(proposal.closure_governance_rows)
        and actual == EXPECTED_ALLOCATION_CLOSURE_ROWS
        and tuple(proposal.unresolved_classical_semantic_requirements)
        == tuple(EXPECTED_ALLOCATION_CLOSURE_ROWS)
    )


def replay_allocation_domain_observation(
    observation: Any,
    semantic_candidate: Any,
    mechanism_proposal: Any,
    multiplicity_reference: Any,
    profile: ClassicalNonSelectingParticipantAllocationProfile,
) -> bool:
    if (
        semantic_candidate.semantic_candidate_kind
        != ALLOCATION_SEMANTIC_CANDIDATE_KIND
        or mechanism_proposal.mechanism_proposal_kind
        != ALLOCATION_MECHANISM_PROPOSAL_KIND
        or mechanism_proposal.source_semantic_candidate_id
        != semantic_candidate.semantic_candidate_id
        or not _allocation_closure_rows_valid(mechanism_proposal)
    ):
        return False
    classification, blockers = classify_allocation_domain(multiplicity_reference)
    expected_paths = ()
    if classification == "EXACT_INSTANCE_SET_CARDINALITY_MATCH":
        expected_paths = (
            build_unordered_path_candidate(
                semantic_candidate.semantic_candidate_id,
                mechanism_proposal.mechanism_proposal_id,
                multiplicity_reference,
                profile,
            ),
        )
    expected_id = "CLASSICAL_ALLOCATION_DOMAIN_OBSERVATION:" + object_sha256({
        "source_semantic_candidate_id": semantic_candidate.semantic_candidate_id,
        "source_mechanism_proposal_id": mechanism_proposal.mechanism_proposal_id,
        "multiplicity_constraint_id": multiplicity_reference.multiplicity_constraint_id,
        "classification": classification,
        "blockers": blockers,
        "path_candidate_ids": tuple(row.path_candidate_id for row in expected_paths),
    })
    return (
        observation.allocation_domain_observation_id == expected_id
        and observation.source_semantic_candidate_id
        == semantic_candidate.semantic_candidate_id
        and observation.source_mechanism_proposal_id
        == mechanism_proposal.mechanism_proposal_id
        and observation.source_occurrence_id == semantic_candidate.source_occurrence_id
        and observation.binding_candidate_id == semantic_candidate.binding_candidate_id
        and observation.graph_record_id == semantic_candidate.graph_record_id
        and observation.interaction_assertion_id
        == semantic_candidate.interaction_assertion_id
        and observation.source_claim_edge_id == semantic_candidate.source_claim_edge_id
        and observation.target_exact_relation_id
        == semantic_candidate.target_exact_relation_id
        and observation.effect_facet == semantic_candidate.effect_facet
        and observation.multiplicity_constraint_id
        == multiplicity_reference.multiplicity_constraint_id
        and observation.exchangeable_symbolic_slot_node_ids
        == multiplicity_reference.exchangeable_symbolic_slot_node_ids
        and observation.exact_runtime_instance_ids
        == multiplicity_reference.exact_runtime_instance_ids
        and observation.required_symbolic_cardinality
        == multiplicity_reference.required_symbolic_cardinality
        and observation.slot_equivalence == multiplicity_reference.slot_equivalence
        and observation.alternative_path_requirement
        == multiplicity_reference.alternative_path_requirement
        and observation.allocation_domain_classification == classification
        and observation.domain_blocker_ids == blockers
        and observation.path_candidates == expected_paths
        and observation.unit5_allocation_closure_rows
        == mechanism_proposal.closure_governance_rows
        and observation.source_unresolved_graph_requirements_provenance
        == mechanism_proposal.source_unresolved_graph_requirements_provenance
        and observation.source_narrative_chain_ids_provenance
        == mechanism_proposal.source_narrative_chain_ids_provenance
    )


def allocation_hash_bundle(
    source_mechanism_envelope: Any,
    fragment_allocation_projections: tuple[Any, ...],
    source_record_candidate_sets: tuple[Any, ...],
    multiplicity_domain_index: tuple[Any, ...],
    projected_allocation_domain_observation_ids: tuple[str, ...],
    projected_path_candidate_ids: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ClassicalNonSelectingParticipantAllocationProfile,
) -> AllocationHashBundle:
    fact_payload = {
        "source_mechanism_closure_envelope_id": (
            source_mechanism_envelope.mechanism_closure_envelope_id
        ),
        "source_mechanism_closure_fact_hash": source_mechanism_envelope.hashes.fact_hash,
        "source_semantic_projection_envelope_id": (
            source_mechanism_envelope.source_semantic_projection_envelope_id
        ),
        "source_admission_envelope_id": source_mechanism_envelope.source_admission_envelope_id,
        "source_effect_envelope_id": source_mechanism_envelope.source_effect_envelope_id,
        "fragment_allocation_projections": json_value(fragment_allocation_projections),
        "source_record_candidate_sets": json_value(source_record_candidate_sets),
        "multiplicity_domain_index": json_value(multiplicity_domain_index),
        "projected_allocation_domain_observation_ids": (
            projected_allocation_domain_observation_ids
        ),
        "projected_path_candidate_ids": projected_path_candidate_ids,
        "synthetic_permutation_generation": profile.synthetic_permutation_generation,
        "synthetic_combination_generation": profile.synthetic_combination_generation,
        "inferred_slot_instance_compatibility": profile.inferred_slot_instance_compatibility,
        "participant_path_selection_semantics": (
            profile.participant_path_selection_semantics
        ),
        "allocation_truth_semantics": profile.allocation_truth_semantics,
        "allocation_operability_semantics": profile.allocation_operability_semantics,
        "coexistence_semantics": profile.coexistence_semantics,
        "exclusivity_semantics": profile.exclusivity_semantics,
        "precedence_semantics": profile.precedence_semantics,
        "priority_semantics": profile.priority_semantics,
        "winner_loser_semantics": profile.winner_loser_semantics,
        "relation_effect_state_semantics": profile.relation_effect_state_semantics,
        "rewrite_application_semantics": profile.rewrite_application_semantics,
        "fragment_selection_semantics": profile.fragment_selection_semantics,
        "cross_outer_composition": profile.cross_outer_composition,
        "cartesian_expansion": profile.cartesian_expansion,
        "raw_relation_immutability_contract": profile.raw_relation_immutability_contract,
    }
    computation_payload = {
        "facts": fact_payload,
        "source_mechanism_closure_computation_hash": (
            source_mechanism_envelope.hashes.computation_hash
        ),
        "source_mechanism_closure_lineage_binding_keys": (
            source_mechanism_envelope.lineage_binding_keys
        ),
        "lineage_binding_keys": lineage_binding_keys,
        "profile": json_value(profile),
    }
    return AllocationHashBundle(
        fact_hash=object_sha256(fact_payload),
        computation_hash=object_sha256(computation_payload),
    )


def validate_allocation_envelope(
    source_mechanism_envelope: Any,
    source_semantic_envelope: Any,
    admission_envelope: Any,
    effect_envelope: Any,
    fragment_allocation_projections: tuple[Any, ...],
    source_record_candidate_sets: tuple[Any, ...],
    multiplicity_domain_index: tuple[Any, ...],
    projected_allocation_domain_observation_ids: tuple[str, ...],
    projected_path_candidate_ids: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ClassicalNonSelectingParticipantAllocationProfile,
    hashes: AllocationHashBundle,
) -> AllocationIntegrityReport:
    diagnostics: list[AllocationIntegrityDiagnostic] = []

    def diag(code: str, path: str, detail: str) -> None:
        diagnostics.append(AllocationIntegrityDiagnostic(code, path, detail))

    if not replay_unit5_mechanism_closure_envelope(
        source_mechanism_envelope,
        source_semantic_envelope,
        admission_envelope,
        effect_envelope,
    ):
        diag(
            "UPSTREAM_UNIT5_MECHANISM_CLOSURE_REPLAY_MISMATCH",
            "source_mechanism_envelope",
            source_mechanism_envelope.mechanism_closure_envelope_id,
        )
    expected_lineage = (
        *source_mechanism_envelope.lineage_binding_keys,
        f"SOURCE_MECHANISM_CLOSURE_FACT:{source_mechanism_envelope.hashes.fact_hash}",
        f"SOURCE_MECHANISM_CLOSURE_COMPUTATION:{source_mechanism_envelope.hashes.computation_hash}",
        f"NON_SELECTING_ALLOCATION_PROFILE:{profile.profile_id}:{profile.profile_version}",
    )
    if lineage_binding_keys != expected_lineage:
        diag("ALLOCATION_LINEAGE_MISMATCH", "lineage_binding_keys", str(lineage_binding_keys))

    semantic_fragment_by_id = {
        row.fragment_semantic_projection_id: row
        for row in source_semantic_envelope.fragment_projections
    }
    source_fragment_by_id = {
        row.fragment_governance_projection_id: row
        for row in source_mechanism_envelope.fragment_governance_projections
    }
    if tuple(
        row.source_fragment_governance_projection_id
        for row in fragment_allocation_projections
    ) != tuple(source_fragment_by_id):
        diag(
            "FRAGMENT_ALLOCATION_IDENTITY_OR_ORDER_MISMATCH",
            "fragment_allocation_projections",
            "one Unit 6 row per Unit 5 fragment required",
        )

    all_domain_ids: list[str] = []
    all_path_ids: list[str] = []
    allocation_by_fragment: dict[str, Any] = {}
    for projected in fragment_allocation_projections:
        source_fragment = source_fragment_by_id.get(
            projected.source_fragment_governance_projection_id
        )
        if source_fragment is None:
            diag(
                "SOURCE_UNIT5_FRAGMENT_MISSING",
                projected.fragment_allocation_projection_id,
                projected.source_fragment_governance_projection_id,
            )
            continue
        allocation_by_fragment[source_fragment.source_fragment_id] = projected
        semantic_fragment = semantic_fragment_by_id.get(
            source_fragment.source_fragment_semantic_projection_id
        )
        if semantic_fragment is None:
            diag(
                "SOURCE_UNIT4_FRAGMENT_MISSING",
                projected.fragment_allocation_projection_id,
                source_fragment.source_fragment_semantic_projection_id,
            )
            continue
        proposal_by_id = {
            row.mechanism_proposal_id: row
            for row in source_fragment.mechanism_proposals
        }
        candidate_by_id = {
            row.semantic_candidate_id: row for row in semantic_fragment.semantic_candidates
        }
        if (
            projected.source_fragment_semantic_projection_id
            != source_fragment.source_fragment_semantic_projection_id
            or projected.source_fragment_id != source_fragment.source_fragment_id
            or projected.source_occurrence_id != source_fragment.source_occurrence_id
            or projected.binding_candidate_id != source_fragment.binding_candidate_id
            or projected.source_governance_status != source_fragment.governance_status
            or projected.source_mechanism_proposal_ids
            != tuple(row.mechanism_proposal_id for row in source_fragment.mechanism_proposals)
            or len(projected.proposal_elaborations)
            != len(source_fragment.mechanism_proposals)
        ):
            diag(
                "FRAGMENT_ALLOCATION_SOURCE_REPLAY_MISMATCH",
                projected.fragment_allocation_projection_id,
                source_fragment.source_fragment_id,
            )

        expected_domains_for_fragment: list[str] = []
        expected_paths_for_fragment: list[str] = []
        for proposal_elab, source_proposal in zip(
            projected.proposal_elaborations,
            source_fragment.mechanism_proposals,
            strict=False,
        ):
            semantic_candidate = candidate_by_id.get(
                source_proposal.source_semantic_candidate_id
            )
            if semantic_candidate is None:
                diag(
                    "SOURCE_UNIT4_CANDIDATE_MISSING",
                    proposal_elab.proposal_allocation_elaboration_id,
                    source_proposal.source_semantic_candidate_id,
                )
                continue
            is_allocation = (
                source_proposal.mechanism_proposal_kind
                == ALLOCATION_MECHANISM_PROPOSAL_KIND
            )
            if (
                proposal_elab.source_mechanism_proposal_id
                != source_proposal.mechanism_proposal_id
                or proposal_elab.source_semantic_candidate_id
                != source_proposal.source_semantic_candidate_id
                or proposal_elab.source_fragment_governance_projection_id
                != source_fragment.fragment_governance_projection_id
                or proposal_elab.source_fragment_semantic_projection_id
                != source_fragment.source_fragment_semantic_projection_id
                or proposal_elab.source_fragment_id != source_fragment.source_fragment_id
                or proposal_elab.source_occurrence_id != source_fragment.source_occurrence_id
                or proposal_elab.binding_candidate_id != source_fragment.binding_candidate_id
                or proposal_elab.semantic_candidate_kind
                != semantic_candidate.semantic_candidate_kind
                or proposal_elab.mechanism_proposal_kind
                != source_proposal.mechanism_proposal_kind
            ):
                diag(
                    "PROPOSAL_ALLOCATION_SOURCE_REPLAY_MISMATCH",
                    proposal_elab.proposal_allocation_elaboration_id,
                    source_proposal.mechanism_proposal_id,
                )
            if is_allocation:
                if (
                    semantic_candidate.semantic_candidate_kind
                    != ALLOCATION_SEMANTIC_CANDIDATE_KIND
                    or not semantic_candidate.multiplicity_references
                    or len(proposal_elab.allocation_domain_observations)
                    != len(semantic_candidate.multiplicity_references)
                    or proposal_elab.allocation_elaboration_semantics
                    != "NON_SELECTING_ALLOCATION_DOMAIN_ELABORATION_ONLY"
                ):
                    diag(
                        "ALLOCATION_PROPOSAL_DOMAIN_CARDINALITY_OR_KIND_MISMATCH",
                        proposal_elab.proposal_allocation_elaboration_id,
                        source_proposal.mechanism_proposal_id,
                    )
                for observation, multiplicity_reference in zip(
                    proposal_elab.allocation_domain_observations,
                    semantic_candidate.multiplicity_references,
                    strict=False,
                ):
                    try:
                        valid = replay_allocation_domain_observation(
                            observation,
                            semantic_candidate,
                            source_proposal,
                            multiplicity_reference,
                            profile,
                        )
                    except ValueError as exc:
                        valid = False
                        diag(
                            "INVALID_UPSTREAM_MULTIPLICITY_CONTRACT",
                            source_proposal.mechanism_proposal_id,
                            str(exc),
                        )
                    if not valid:
                        diag(
                            "ALLOCATION_DOMAIN_REPLAY_MISMATCH",
                            observation.allocation_domain_observation_id,
                            multiplicity_reference.multiplicity_constraint_id,
                        )
                    expected_domains_for_fragment.append(
                        observation.allocation_domain_observation_id
                    )
                    expected_paths_for_fragment.extend(
                        row.path_candidate_id for row in observation.path_candidates
                    )
            elif (
                proposal_elab.allocation_domain_observations
                or proposal_elab.allocation_elaboration_semantics
                != "NON_ALLOCATION_PROPOSAL_PRESERVED_ZERO_DOMAINS"
            ):
                diag(
                    "NON_ALLOCATION_PROPOSAL_EMITTED_DOMAIN",
                    proposal_elab.proposal_allocation_elaboration_id,
                    source_proposal.mechanism_proposal_kind,
                )

            expected_proposal_elab_id = "CLASSICAL_PROPOSAL_ALLOCATION_ELABORATION:" + object_sha256({
                "source_mechanism_proposal_id": source_proposal.mechanism_proposal_id,
                "source_semantic_candidate_id": semantic_candidate.semantic_candidate_id,
                "allocation_domain_observation_ids": tuple(
                    row.allocation_domain_observation_id
                    for row in proposal_elab.allocation_domain_observations
                ),
                "allocation_elaboration_semantics": (
                    proposal_elab.allocation_elaboration_semantics
                ),
            })
            if proposal_elab.proposal_allocation_elaboration_id != expected_proposal_elab_id:
                diag(
                    "PROPOSAL_ALLOCATION_ID_REPLAY_MISMATCH",
                    proposal_elab.proposal_allocation_elaboration_id,
                    expected_proposal_elab_id,
                )

        if projected.allocation_domain_observation_ids != tuple(
            expected_domains_for_fragment
        ):
            diag(
                "FRAGMENT_DOMAIN_ID_INDEX_MISMATCH",
                projected.fragment_allocation_projection_id,
                str(projected.allocation_domain_observation_ids),
            )
        has_allocation = bool(expected_domains_for_fragment)
        expected_status = (
            "ALLOCATION_DOMAIN_ELABORATION_PROJECTED"
            if has_allocation
            else (
                "PRESERVED_ZERO_PROPOSALS_NO_ALLOCATION_DOMAINS"
                if not source_fragment.mechanism_proposals
                else "PRESERVED_NO_ALLOCATION_DOMAINS"
            )
        )
        if projected.allocation_status != expected_status:
            diag(
                "FRAGMENT_ALLOCATION_STATUS_MISMATCH",
                projected.fragment_allocation_projection_id,
                projected.allocation_status,
            )
        expected_fragment_id = "CLASSICAL_FRAGMENT_ALLOCATION_ELABORATION:" + object_sha256({
            "source_fragment_governance_projection_id": (
                source_fragment.fragment_governance_projection_id
            ),
            "source_mechanism_proposal_ids": projected.source_mechanism_proposal_ids,
            "proposal_allocation_elaboration_ids": tuple(
                row.proposal_allocation_elaboration_id
                for row in projected.proposal_elaborations
            ),
            "allocation_status": expected_status,
        })
        if projected.fragment_allocation_projection_id != expected_fragment_id:
            diag(
                "FRAGMENT_ALLOCATION_ID_REPLAY_MISMATCH",
                projected.fragment_allocation_projection_id,
                expected_fragment_id,
            )
        all_domain_ids.extend(expected_domains_for_fragment)
        all_path_ids.extend(expected_paths_for_fragment)

    if len(all_domain_ids) != len(set(all_domain_ids)):
        diag("ALLOCATION_DOMAIN_ID_DUPLICATE", "allocation_domains", str(len(all_domain_ids)))
    if len(all_path_ids) != len(set(all_path_ids)):
        diag("PATH_CANDIDATE_ID_DUPLICATE", "path_candidates", str(len(all_path_ids)))
    if tuple(all_domain_ids) != projected_allocation_domain_observation_ids:
        diag(
            "ALLOCATION_DOMAIN_GLOBAL_INDEX_MISMATCH",
            "projected_allocation_domain_observation_ids",
            str(projected_allocation_domain_observation_ids),
        )
    if tuple(all_path_ids) != projected_path_candidate_ids:
        diag(
            "PATH_CANDIDATE_GLOBAL_INDEX_MISMATCH",
            "projected_path_candidate_ids",
            str(projected_path_candidate_ids),
        )

    upstream_sets = {
        row.source_record_candidate_set_id: row
        for row in source_mechanism_envelope.source_record_candidate_sets
    }
    if len(source_record_candidate_sets) != len(upstream_sets):
        diag(
            "SOURCE_RECORD_SET_CARDINALITY_MISMATCH",
            "source_record_candidate_sets",
            str(len(source_record_candidate_sets)),
        )
    for row in source_record_candidate_sets:
        upstream = upstream_sets.get(row.source_record_candidate_set_id)
        if upstream is None:
            diag("SOURCE_RECORD_SET_UPSTREAM_MISSING", row.source_record_candidate_set_id, row.source_occurrence_id)
            continue
        if (
            row.source_layer != upstream.source_layer
            or row.source_occurrence_id != upstream.source_occurrence_id
            or row.source_fragment_ids != upstream.source_fragment_ids
        ):
            diag(
                "SOURCE_RECORD_SET_SOURCE_REPLAY_MISMATCH",
                row.source_record_candidate_set_id,
                row.source_occurrence_id,
            )
        expected_fragment_ids = tuple(
            allocation_by_fragment[fragment_id].fragment_allocation_projection_id
            for fragment_id in row.source_fragment_ids
        )
        expected_proposal_ids = tuple(
            proposal_id
            for fragment_id in row.source_fragment_ids
            for proposal_id in allocation_by_fragment[
                fragment_id
            ].source_mechanism_proposal_ids
        )
        expected_domain_ids = tuple(
            domain_id
            for fragment_id in row.source_fragment_ids
            for domain_id in allocation_by_fragment[
                fragment_id
            ].allocation_domain_observation_ids
        )
        expected_path_ids = tuple(
            path.path_candidate_id
            for fragment_id in row.source_fragment_ids
            for proposal in allocation_by_fragment[fragment_id].proposal_elaborations
            for observation in proposal.allocation_domain_observations
            for path in observation.path_candidates
        )
        if (
            row.fragment_allocation_projection_ids != expected_fragment_ids
            or row.source_mechanism_proposal_ids != expected_proposal_ids
            or row.allocation_domain_observation_ids != expected_domain_ids
            or row.path_candidate_ids != expected_path_ids
            or any(
                value != "NOT_RELEASED"
                for value in (
                    row.member_selection_semantics,
                    row.member_coexistence_semantics,
                    row.member_exclusivity_semantics,
                    row.allocation_priority_semantics,
                    row.allocation_conflict_semantics,
                )
            )
        ):
            diag(
                "SOURCE_RECORD_SET_ALLOCATION_REPLAY_MISMATCH",
                row.source_record_candidate_set_id,
                row.source_occurrence_id,
            )

    expected_index_groups: dict[str, dict[str, list[str]]] = {}
    for fragment in fragment_allocation_projections:
        for proposal in fragment.proposal_elaborations:
            for observation in proposal.allocation_domain_observations:
                group = expected_index_groups.setdefault(
                    observation.multiplicity_constraint_id,
                    {"candidates": [], "proposals": [], "domains": [], "paths": []},
                )
                group["candidates"].append(observation.source_semantic_candidate_id)
                group["proposals"].append(observation.source_mechanism_proposal_id)
                group["domains"].append(observation.allocation_domain_observation_id)
                group["paths"].extend(
                    row.path_candidate_id for row in observation.path_candidates
                )
    expected_index = tuple(
        (
            constraint_id,
            tuple(dict.fromkeys(group["candidates"])),
            tuple(dict.fromkeys(group["proposals"])),
            tuple(group["domains"]),
            tuple(group["paths"]),
            "IDENTITY_ONLY_NO_SYNTHESIS_OR_SELECTION",
        )
        for constraint_id, group in sorted(expected_index_groups.items())
    )
    actual_index = tuple(
        (
            row.multiplicity_constraint_id,
            row.source_semantic_candidate_ids,
            row.source_mechanism_proposal_ids,
            row.allocation_domain_observation_ids,
            row.path_candidate_ids,
            row.index_semantics,
        )
        for row in multiplicity_domain_index
    )
    if actual_index != expected_index:
        diag(
            "MULTIPLICITY_DOMAIN_INDEX_REPLAY_MISMATCH",
            "multiplicity_domain_index",
            str(actual_index),
        )

    expected_hashes = allocation_hash_bundle(
        source_mechanism_envelope,
        fragment_allocation_projections,
        source_record_candidate_sets,
        multiplicity_domain_index,
        projected_allocation_domain_observation_ids,
        projected_path_candidate_ids,
        lineage_binding_keys,
        profile,
    )
    if expected_hashes != hashes:
        diag("ALLOCATION_HASH_REPLAY_MISMATCH", "hashes", hashes.fact_hash)

    return AllocationIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )
