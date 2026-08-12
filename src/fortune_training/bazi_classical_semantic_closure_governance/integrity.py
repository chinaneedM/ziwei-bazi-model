from __future__ import annotations

from typing import Any

from fortune_training.bazi_classical_effect_semantic_candidate.integrity import (
    replay_admission_envelope_against_effect,
    semantic_projection_hash_bundle,
    validate_semantic_projection_envelope,
)
from fortune_training.bazi_classical_effect_semantic_candidate.profile import (
    SOURCE_CLAIM_TO_SEMANTIC_CANDIDATE,
    bazi_classical_effect_semantic_candidate_projection_r1_profile,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .models import (
    MechanismClosureHashBundle,
    MechanismClosureIntegrityDiagnostic,
    MechanismClosureIntegrityReport,
)
from .profile import ClassicalSemanticMechanismClosureGovernanceProfile


def match_admission_envelope(source_semantic_envelope: Any, admission_resolution: Any) -> Any:
    matches = [
        row for row in admission_resolution.candidates
        if row.admission_envelope_id == source_semantic_envelope.source_admission_envelope_id
        and row.hashes.fact_hash == source_semantic_envelope.source_admission_fact_hash
        and row.hashes.computation_hash == source_semantic_envelope.source_admission_computation_hash
    ]
    if len(matches) != 1:
        raise ValueError(f"SOURCE_ADMISSION_ENVELOPE_MATCH_NOT_UNIQUE:{len(matches)}")
    return matches[0]


def match_effect_envelope(source_semantic_envelope: Any, effect_resolution: Any) -> Any:
    matches = [
        row for row in effect_resolution.candidates
        if row.envelope_id == source_semantic_envelope.source_effect_envelope_id
        and row.hashes.fact_hash == source_semantic_envelope.source_effect_fact_hash
        and row.hashes.computation_hash == source_semantic_envelope.source_effect_computation_hash
    ]
    if len(matches) != 1:
        raise ValueError(f"SOURCE_EFFECT_ENVELOPE_MATCH_NOT_UNIQUE:{len(matches)}")
    return matches[0]


def _unique_strings(rows: list[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(rows))


def replay_unit4_semantic_envelope(
    source_semantic_envelope: Any,
    admission_envelope: Any,
    effect_envelope: Any,
) -> bool:
    if source_semantic_envelope.integrity.status != "PASS":
        return False
    if not replay_admission_envelope_against_effect(admission_envelope, effect_envelope):
        return False
    if (
        source_semantic_envelope.source_admission_envelope_id != admission_envelope.admission_envelope_id
        or source_semantic_envelope.source_admission_fact_hash != admission_envelope.hashes.fact_hash
        or source_semantic_envelope.source_admission_computation_hash != admission_envelope.hashes.computation_hash
        or source_semantic_envelope.source_effect_envelope_id != effect_envelope.envelope_id
        or source_semantic_envelope.source_effect_fact_hash != effect_envelope.hashes.fact_hash
        or source_semantic_envelope.source_effect_computation_hash != effect_envelope.hashes.computation_hash
    ):
        return False

    profile = bazi_classical_effect_semantic_candidate_projection_r1_profile()
    expected_lineage = (
        *admission_envelope.lineage_binding_keys,
        f"SOURCE_ADMISSION_FACT:{admission_envelope.hashes.fact_hash}",
        f"SOURCE_ADMISSION_COMPUTATION:{admission_envelope.hashes.computation_hash}",
        f"SEMANTIC_CANDIDATE_PROFILE:{profile.profile_id}:{profile.profile_version}",
    )
    if source_semantic_envelope.lineage_binding_keys != expected_lineage:
        return False
    if source_semantic_envelope.algorithm_versions != {
        "semantic_candidate_projection": profile.algorithm_version
    }:
        return False

    admission_by_fragment = {
        row.source_fragment_id: row for row in admission_envelope.fragment_admissions
    }
    effect_by_fragment = {row.fragment_id: row for row in effect_envelope.fragments}
    if (
        len(admission_by_fragment) != len(admission_envelope.fragment_admissions)
        or len(effect_by_fragment) != len(effect_envelope.fragments)
        or tuple(row.source_fragment_id for row in source_semantic_envelope.fragment_projections)
        != tuple(row.fragment_id for row in effect_envelope.fragments)
    ):
        return False

    for fragment_projection in source_semantic_envelope.fragment_projections:
        admission = admission_by_fragment.get(fragment_projection.source_fragment_id)
        effect_fragment = effect_by_fragment.get(fragment_projection.source_fragment_id)
        if admission is None or effect_fragment is None:
            return False
        if (
            fragment_projection.source_admission_projection_id != admission.admission_projection_id
            or fragment_projection.source_fragment_fact_hash != effect_fragment.hashes.fact_hash
            or fragment_projection.source_fragment_computation_hash != effect_fragment.hashes.computation_hash
            or fragment_projection.source_occurrence_id != effect_fragment.source_occurrence_id
            or fragment_projection.binding_candidate_id != effect_fragment.binding_candidate_id
            or fragment_projection.admission_status != admission.admission_status
            or fragment_projection.admission_blocker_ids != admission.admission_blocker_ids
            or fragment_projection.source_unresolved_graph_requirements_provenance
            != effect_fragment.source_unresolved_graph_requirements
        ):
            return False

        expected_fragment_requirements = _unique_strings([
            requirement
            for node in effect_fragment.effect_constraint_nodes
            for requirement in node.constraint.unresolved_classical_semantic_requirements
        ])
        if fragment_projection.unresolved_classical_semantic_requirements != expected_fragment_requirements:
            return False

        constraint_by_id = {
            node.constraint.effect_constraint_id: node.constraint
            for node in effect_fragment.effect_constraint_nodes
        }
        if len(constraint_by_id) != len(effect_fragment.effect_constraint_nodes):
            return False
        if admission.admission_status == "ADMITTED":
            if len(fragment_projection.semantic_candidates) != len(effect_fragment.effect_constraint_nodes):
                return False
        elif fragment_projection.semantic_candidates:
            return False

        for candidate in fragment_projection.semantic_candidates:
            constraint = constraint_by_id.get(candidate.source_effect_constraint_id)
            if constraint is None:
                return False
            mapping = SOURCE_CLAIM_TO_SEMANTIC_CANDIDATE.get(candidate.source_claim_edge_class)
            if mapping is None:
                return False
            expected_facet, expected_kind = mapping
            expected_candidate_id = "CLASSICAL_EFFECT_SEMANTIC_CANDIDATE:" + object_sha256({
                "source_admission_projection_id": admission.admission_projection_id,
                "source_fragment_id": effect_fragment.fragment_id,
                "source_effect_constraint_id": constraint.effect_constraint_id,
                "semantic_candidate_kind": expected_kind,
                "effect_facet": expected_facet,
            })
            if (
                candidate.semantic_candidate_id != expected_candidate_id
                or candidate.source_admission_projection_id != admission.admission_projection_id
                or candidate.source_effect_envelope_id != effect_envelope.envelope_id
                or candidate.source_effect_envelope_fact_hash != effect_envelope.hashes.fact_hash
                or candidate.source_effect_envelope_computation_hash != effect_envelope.hashes.computation_hash
                or candidate.source_fragment_id != effect_fragment.fragment_id
                or candidate.source_fragment_fact_hash != effect_fragment.hashes.fact_hash
                or candidate.source_fragment_computation_hash != effect_fragment.hashes.computation_hash
                or candidate.binding_candidate_id != constraint.binding_candidate_id
                or candidate.source_occurrence_id != constraint.source_occurrence_id
                or candidate.graph_record_id != constraint.graph_record_id
                or candidate.interaction_assertion_id != constraint.interaction_assertion_id
                or candidate.source_claim_edge_id != constraint.source_claim_edge_id
                or candidate.source_claim_edge_class != constraint.source_claim_edge_class
                or candidate.effect_facet != expected_facet
                or candidate.semantic_candidate_kind != expected_kind
                or candidate.target_effect_channel_id != constraint.target_effect_channel_id
                or candidate.target_exact_relation_id != constraint.target_exact_relation_id
                or candidate.actor_exact_relation_ids != constraint.actor_exact_relation_ids
                or candidate.actor_exact_participant_ids != constraint.actor_exact_participant_ids
                or candidate.context_exact_participant_ids != constraint.context_exact_participant_ids
                or candidate.multiplicity_references != constraint.multiplicity_references
                or candidate.source_narrative_chain_ids != constraint.source_narrative_chain_ids
                or candidate.unresolved_classical_semantic_requirements
                != constraint.unresolved_classical_semantic_requirements
                or candidate.source_unresolved_graph_requirements_provenance
                != constraint.source_unresolved_graph_requirements
                or candidate.candidate_truth_semantics != "NOT_RELEASED"
                or candidate.candidate_applicability_semantics
                != "NOT_RELEASED_BEYOND_UNIT3_ADMISSION"
            ):
                return False

        expected_fragment_id = "CLASSICAL_FRAGMENT_SEMANTIC_CANDIDATE_PROJECTION:" + object_sha256({
            "source_admission_projection_id": admission.admission_projection_id,
            "source_fragment_id": effect_fragment.fragment_id,
            "admission_status": admission.admission_status,
            "projection_status": fragment_projection.projection_status,
            "semantic_candidate_ids": tuple(
                row.semantic_candidate_id for row in fragment_projection.semantic_candidates
            ),
        })
        if fragment_projection.fragment_semantic_projection_id != expected_fragment_id:
            return False

    expected_hashes = semantic_projection_hash_bundle(
        admission_envelope,
        effect_envelope,
        source_semantic_envelope.fragment_projections,
        source_semantic_envelope.source_record_candidate_sets,
        source_semantic_envelope.effect_channel_candidate_index,
        source_semantic_envelope.projected_semantic_candidate_ids,
        source_semantic_envelope.lineage_binding_keys,
        profile,
    )
    if expected_hashes != source_semantic_envelope.hashes:
        return False
    validation = validate_semantic_projection_envelope(
        admission_envelope,
        effect_envelope,
        source_semantic_envelope.fragment_projections,
        source_semantic_envelope.source_record_candidate_sets,
        source_semantic_envelope.effect_channel_candidate_index,
        source_semantic_envelope.projected_semantic_candidate_ids,
        source_semantic_envelope.lineage_binding_keys,
        profile,
        source_semantic_envelope.hashes,
    )
    if validation.status != "PASS":
        return False
    expected_envelope_id = "CLASSICAL_EFFECT_SEMANTIC_CANDIDATE_ENVELOPE:" + object_sha256({
        "source_admission_envelope_id": admission_envelope.admission_envelope_id,
        "source_admission_fact_hash": admission_envelope.hashes.fact_hash,
        "fact_hash": source_semantic_envelope.hashes.fact_hash,
    })
    return source_semantic_envelope.semantic_projection_envelope_id == expected_envelope_id


def mechanism_closure_hash_bundle(
    source_semantic_envelope: Any,
    fragment_governance_projections: tuple[Any, ...],
    source_record_candidate_sets: tuple[Any, ...],
    closure_requirement_index: tuple[Any, ...],
    mechanism_proposal_index: tuple[Any, ...],
    projected_mechanism_proposal_ids: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ClassicalSemanticMechanismClosureGovernanceProfile,
) -> MechanismClosureHashBundle:
    fact_payload = {
        "source_semantic_projection_envelope_id": source_semantic_envelope.semantic_projection_envelope_id,
        "source_semantic_projection_fact_hash": source_semantic_envelope.hashes.fact_hash,
        "source_admission_envelope_id": source_semantic_envelope.source_admission_envelope_id,
        "source_effect_envelope_id": source_semantic_envelope.source_effect_envelope_id,
        "fragment_governance_projections": json_value(fragment_governance_projections),
        "source_record_candidate_sets": json_value(source_record_candidate_sets),
        "closure_requirement_index": json_value(closure_requirement_index),
        "mechanism_proposal_index": json_value(mechanism_proposal_index),
        "projected_mechanism_proposal_ids": projected_mechanism_proposal_ids,
        "mechanism_proposal_semantics": profile.mechanism_proposal_semantics,
        "mechanism_execution_semantics": profile.mechanism_execution_semantics,
        "rewrite_application_semantics": profile.rewrite_application_semantics,
        "candidate_truth_semantics": profile.candidate_truth_semantics,
        "candidate_applicability_semantics": profile.candidate_applicability_semantics,
        "candidate_coexistence_semantics": profile.candidate_coexistence_semantics,
        "candidate_exclusivity_semantics": profile.candidate_exclusivity_semantics,
        "candidate_conflict_semantics": profile.candidate_conflict_semantics,
        "precedence_semantics": profile.precedence_semantics,
        "priority_semantics": profile.priority_semantics,
        "winner_loser_semantics": profile.winner_loser_semantics,
        "state_transition_semantics": profile.state_transition_semantics,
        "lifecycle_truth_gate": profile.lifecycle_truth_gate,
        "fragment_selection_semantics": profile.fragment_selection_semantics,
        "cross_outer_composition": profile.cross_outer_composition,
        "cartesian_expansion": profile.cartesian_expansion,
        "raw_relation_immutability_contract": profile.raw_relation_immutability_contract,
    }
    computation_payload = {
        "facts": fact_payload,
        "source_semantic_projection_computation_hash": source_semantic_envelope.hashes.computation_hash,
        "source_semantic_projection_lineage_binding_keys": source_semantic_envelope.lineage_binding_keys,
        "lineage_binding_keys": lineage_binding_keys,
        "profile": json_value(profile),
    }
    return MechanismClosureHashBundle(
        fact_hash=object_sha256(fact_payload),
        computation_hash=object_sha256(computation_payload),
    )


def validate_mechanism_closure_envelope(
    source_semantic_envelope: Any,
    admission_envelope: Any,
    effect_envelope: Any,
    fragment_governance_projections: tuple[Any, ...],
    source_record_candidate_sets: tuple[Any, ...],
    closure_requirement_index: tuple[Any, ...],
    mechanism_proposal_index: tuple[Any, ...],
    projected_mechanism_proposal_ids: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ClassicalSemanticMechanismClosureGovernanceProfile,
    hashes: MechanismClosureHashBundle,
) -> MechanismClosureIntegrityReport:
    diagnostics: list[MechanismClosureIntegrityDiagnostic] = []

    def diag(code: str, path: str, detail: str) -> None:
        diagnostics.append(MechanismClosureIntegrityDiagnostic(code, path, detail))

    if not replay_unit4_semantic_envelope(source_semantic_envelope, admission_envelope, effect_envelope):
        diag(
            "UPSTREAM_UNIT4_SEMANTIC_ENVELOPE_REPLAY_MISMATCH",
            "source_semantic_envelope",
            source_semantic_envelope.semantic_projection_envelope_id,
        )

    source_fragments = source_semantic_envelope.fragment_projections
    if tuple(row.source_fragment_semantic_projection_id for row in fragment_governance_projections) != tuple(
        row.fragment_semantic_projection_id for row in source_fragments
    ):
        diag("FRAGMENT_GOVERNANCE_IDENTITY_OR_ORDER_MISMATCH", "fragment_governance_projections", "one row per Unit 4 fragment required")

    source_by_fragment = {row.source_fragment_id: row for row in source_fragments}
    governance_by_fragment = {row.source_fragment_id: row for row in fragment_governance_projections}
    if len(governance_by_fragment) != len(fragment_governance_projections):
        diag("FRAGMENT_GOVERNANCE_SOURCE_ID_DUPLICATE", "fragment_governance_projections", str(len(governance_by_fragment)))

    all_proposal_ids: list[str] = []
    for row in fragment_governance_projections:
        source = source_by_fragment.get(row.source_fragment_id)
        if source is None:
            diag("SOURCE_UNIT4_FRAGMENT_MISSING", row.fragment_governance_projection_id, row.source_fragment_id)
            continue
        expected_candidate_ids = tuple(candidate.semantic_candidate_id for candidate in source.semantic_candidates)
        if row.source_semantic_candidate_ids != expected_candidate_ids:
            diag("FRAGMENT_SOURCE_CANDIDATE_ID_MISMATCH", row.fragment_governance_projection_id, str(row.source_semantic_candidate_ids))
        if source.semantic_candidates:
            if row.governance_status != "MECHANISM_CLOSURE_GOVERNANCE_PROJECTED":
                diag("CANDIDATE_FRAGMENT_NOT_GOVERNED", row.fragment_governance_projection_id, row.governance_status)
            if len(row.mechanism_proposals) != len(source.semantic_candidates):
                diag("CANDIDATE_TO_PROPOSAL_CARDINALITY_MISMATCH", row.fragment_governance_projection_id, f"{len(source.semantic_candidates)}->{len(row.mechanism_proposals)}")
        elif row.mechanism_proposals:
            diag("ZERO_CANDIDATE_FRAGMENT_EMITTED_PROPOSAL", row.fragment_governance_projection_id, row.governance_status)
        all_proposal_ids.extend(proposal.mechanism_proposal_id for proposal in row.mechanism_proposals)

    if len(all_proposal_ids) != len(set(all_proposal_ids)):
        diag("MECHANISM_PROPOSAL_ID_DUPLICATE", "mechanism_proposals", str(len(all_proposal_ids)))
    if tuple(all_proposal_ids) != projected_mechanism_proposal_ids:
        diag("MECHANISM_PROPOSAL_ID_INDEX_MISMATCH", "projected_mechanism_proposal_ids", str(projected_mechanism_proposal_ids))

    upstream_sets = {
        row.source_record_candidate_set_id: row for row in source_semantic_envelope.source_record_candidate_sets
    }
    if len(source_record_candidate_sets) != len(upstream_sets):
        diag("SOURCE_RECORD_SET_CARDINALITY_MISMATCH", "source_record_candidate_sets", str(len(source_record_candidate_sets)))
    for row in source_record_candidate_sets:
        upstream = upstream_sets.get(row.source_record_candidate_set_id)
        if upstream is None:
            diag("SOURCE_RECORD_SET_UPSTREAM_MISSING", row.source_record_candidate_set_id, row.source_occurrence_id)
            continue
        if row.source_fragment_ids != upstream.source_fragment_ids:
            diag("SOURCE_RECORD_SET_FRAGMENT_IDENTITY_MISMATCH", row.source_record_candidate_set_id, str(row.source_fragment_ids))
        expected_projection_ids = tuple(
            governance_by_fragment[fragment_id].fragment_governance_projection_id
            for fragment_id in row.source_fragment_ids
        )
        if row.fragment_governance_projection_ids != expected_projection_ids:
            diag("SOURCE_RECORD_SET_GOVERNANCE_PROJECTION_MISMATCH", row.source_record_candidate_set_id, str(row.fragment_governance_projection_ids))
        expected_proposal_ids = tuple(
            proposal.mechanism_proposal_id
            for fragment_id in row.source_fragment_ids
            for proposal in governance_by_fragment[fragment_id].mechanism_proposals
        )
        if row.mechanism_proposal_ids != expected_proposal_ids:
            diag("SOURCE_RECORD_SET_PROPOSAL_ID_MISMATCH", row.source_record_candidate_set_id, str(row.mechanism_proposal_ids))
        if any(value != "NOT_RELEASED" for value in (
            row.member_selection_semantics,
            row.member_coexistence_semantics,
            row.member_exclusivity_semantics,
            row.proposal_priority_semantics,
            row.proposal_conflict_semantics,
        )):
            diag("SOURCE_RECORD_SET_SEMANTICS_OVERRESOLVED", row.source_record_candidate_set_id, "selection/coexistence/exclusivity/priority/conflict")

    indexed_requirement_proposals = {
        proposal_id
        for row in closure_requirement_index
        for proposal_id in row.mechanism_proposal_ids
    }
    indexed_kind_proposals = {
        proposal_id
        for row in mechanism_proposal_index
        for proposal_id in row.mechanism_proposal_ids
    }
    expected_proposal_set = set(projected_mechanism_proposal_ids)
    if indexed_requirement_proposals != expected_proposal_set:
        diag("CLOSURE_REQUIREMENT_INDEX_COVERAGE_MISMATCH", "closure_requirement_index", str(len(indexed_requirement_proposals)))
    if indexed_kind_proposals != expected_proposal_set:
        diag("MECHANISM_PROPOSAL_INDEX_COVERAGE_MISMATCH", "mechanism_proposal_index", str(len(indexed_kind_proposals)))
    if any(row.index_semantics != "AUDIT_IDENTITY_ONLY_NO_INFERENCE" for row in (*closure_requirement_index, *mechanism_proposal_index)):
        diag("GOVERNANCE_INDEX_SEMANTICS_OVERRESOLVED", "indexes", "identity-only required")

    expected_hashes = mechanism_closure_hash_bundle(
        source_semantic_envelope,
        fragment_governance_projections,
        source_record_candidate_sets,
        closure_requirement_index,
        mechanism_proposal_index,
        projected_mechanism_proposal_ids,
        lineage_binding_keys,
        profile,
    )
    if expected_hashes != hashes:
        diag("MECHANISM_CLOSURE_HASH_REPLAY_MISMATCH", "hashes", hashes.fact_hash)

    return MechanismClosureIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )
