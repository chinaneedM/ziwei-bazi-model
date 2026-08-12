from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fortune_training.bazi_classical_effect_constraint_graph.models import (
    BaziClassicalEffectConstraintGraphResolution,
)
from fortune_training.bazi_classical_effect_semantic_candidate.models import (
    BaziClassicalEffectSemanticCandidateProjectionResolution,
)
from fortune_training.bazi_classical_non_selecting_participant_allocation.integrity import (
    match_admission_envelope,
    match_effect_envelope,
    match_semantic_envelope,
)
from fortune_training.bazi_classical_non_selecting_participant_allocation.models import (
    BaziClassicalNonSelectingParticipantAllocationResolution,
)
from fortune_training.bazi_classical_resolver_admission.models import (
    BaziClassicalResolverAdmissionResolution,
)
from fortune_training.bazi_classical_semantic_closure_governance.models import (
    BaziClassicalSemanticMechanismClosureGovernanceResolution,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .integrity import (
    build_expected_indexes,
    final_candidate_id,
    final_effect_hash_bundle,
    match_mechanism_envelope,
    replay_unit6_allocation_envelope,
    validate_final_effect_envelope,
)
from .models import (
    BaziClassicalFinalEffectCandidateEnvelopeResolution,
    ClassicalFinalEffectCandidateEnvelope,
    FinalClassicalEffectCandidate,
    FinalEffectCandidateFragmentEnvelope,
    SourceRecordFinalEffectCandidateSet,
)
from .profile import (
    SEMANTIC_TO_MECHANISM,
    ClassicalFinalEffectCandidateEnvelopeProfile,
)


class BaziClassicalFinalEffectCandidateEnvelopeError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class BaziClassicalFinalEffectCandidateEnvelopeRequest:
    source_effect_constraint_resolution: BaziClassicalEffectConstraintGraphResolution
    source_resolver_admission_resolution: BaziClassicalResolverAdmissionResolution
    source_semantic_candidate_resolution: BaziClassicalEffectSemanticCandidateProjectionResolution
    source_mechanism_closure_resolution: BaziClassicalSemanticMechanismClosureGovernanceResolution
    source_allocation_resolution: BaziClassicalNonSelectingParticipantAllocationResolution
    final_effect_profile: ClassicalFinalEffectCandidateEnvelopeProfile


def _project_candidate(
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
    expected_mechanism_kind = SEMANTIC_TO_MECHANISM.get(
        semantic_candidate.semantic_candidate_kind
    )
    if expected_mechanism_kind != mechanism_proposal.mechanism_proposal_kind:
        raise BaziClassicalFinalEffectCandidateEnvelopeError(
            "SEMANTIC_MECHANISM_KIND_MISMATCH",
            semantic_candidate.semantic_candidate_id,
        )
    if (
        mechanism_proposal.source_semantic_candidate_id
        != semantic_candidate.semantic_candidate_id
        or allocation_elaboration.source_semantic_candidate_id
        != semantic_candidate.semantic_candidate_id
        or allocation_elaboration.source_mechanism_proposal_id
        != mechanism_proposal.mechanism_proposal_id
        or allocation_elaboration.mechanism_proposal_kind
        != mechanism_proposal.mechanism_proposal_kind
        or tuple(mechanism_proposal.unresolved_classical_semantic_requirements)
        != tuple(semantic_candidate.unresolved_classical_semantic_requirements)
    ):
        raise BaziClassicalFinalEffectCandidateEnvelopeError(
            "CANDIDATE_PROPOSAL_ALLOCATION_CHAIN_MISMATCH",
            semantic_candidate.semantic_candidate_id,
        )
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


def _project_fragment(
    allocation_fragment: Any,
    mechanism_fragment: Any,
    semantic_fragment: Any,
    semantic_envelope: Any,
    mechanism_envelope: Any,
    allocation_envelope: Any,
    profile: ClassicalFinalEffectCandidateEnvelopeProfile,
) -> FinalEffectCandidateFragmentEnvelope:
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
        or set(candidate_by_id) != set(proposal_by_candidate)
        or set(candidate_by_id) != set(elaboration_by_candidate)
    ):
        raise BaziClassicalFinalEffectCandidateEnvelopeError(
            "FRAGMENT_CANDIDATE_CHAIN_NOT_ONE_TO_ONE",
            allocation_fragment.source_fragment_id,
        )
    ordered_candidate_ids = tuple(
        row.semantic_candidate_id for row in semantic_fragment.semantic_candidates
    )
    final_candidates = tuple(
        _project_candidate(
            candidate_by_id[candidate_id],
            proposal_by_candidate[candidate_id],
            elaboration_by_candidate[candidate_id],
            semantic_envelope,
            mechanism_envelope,
            allocation_envelope,
            semantic_fragment,
            mechanism_fragment,
            allocation_fragment,
            profile,
        )
        for candidate_id in ordered_candidate_ids
    )
    final_status = (
        "FINAL_EFFECT_CANDIDATES_ASSEMBLED"
        if final_candidates
        else "PRESERVED_ZERO_FINAL_EFFECT_CANDIDATES"
    )
    final_ids = tuple(row.final_candidate_id for row in final_candidates)
    fragment_id = "CLASSICAL_FINAL_EFFECT_FRAGMENT:" + object_sha256({
        "source_fragment_semantic_projection_id": semantic_fragment.fragment_semantic_projection_id,
        "source_fragment_governance_projection_id": mechanism_fragment.fragment_governance_projection_id,
        "source_fragment_allocation_projection_id": allocation_fragment.fragment_allocation_projection_id,
        "final_candidate_ids": final_ids,
        "final_fragment_status": final_status,
    })
    return FinalEffectCandidateFragmentEnvelope(
        final_fragment_id=fragment_id,
        source_fragment_semantic_projection_id=semantic_fragment.fragment_semantic_projection_id,
        source_fragment_governance_projection_id=mechanism_fragment.fragment_governance_projection_id,
        source_fragment_allocation_projection_id=allocation_fragment.fragment_allocation_projection_id,
        source_fragment_id=allocation_fragment.source_fragment_id,
        source_occurrence_id=allocation_fragment.source_occurrence_id,
        binding_candidate_id=allocation_fragment.binding_candidate_id,
        source_projection_status=semantic_fragment.projection_status,
        source_governance_status=mechanism_fragment.governance_status,
        source_allocation_status=allocation_fragment.allocation_status,
        final_fragment_status=final_status,
        source_semantic_candidate_ids=ordered_candidate_ids,
        source_mechanism_proposal_ids=tuple(
            proposal_by_candidate[candidate_id].mechanism_proposal_id
            for candidate_id in ordered_candidate_ids
        ),
        source_allocation_elaboration_ids=tuple(
            elaboration_by_candidate[candidate_id].proposal_allocation_elaboration_id
            for candidate_id in ordered_candidate_ids
        ),
        final_candidates=final_candidates,
        final_candidate_ids=final_ids,
    )


def _source_record_sets(
    allocation_envelope: Any,
    fragments: tuple[FinalEffectCandidateFragmentEnvelope, ...],
) -> tuple[SourceRecordFinalEffectCandidateSet, ...]:
    by_source_fragment = {row.source_fragment_id: row for row in fragments}
    if len(by_source_fragment) != len(fragments):
        raise BaziClassicalFinalEffectCandidateEnvelopeError(
            "DUPLICATE_UNIT7_SOURCE_FRAGMENT_ID",
            str(len(fragments)),
        )
    rows = []
    for source_set in allocation_envelope.source_record_candidate_sets:
        selected = tuple(
            by_source_fragment[source_fragment_id]
            for source_fragment_id in source_set.source_fragment_ids
        )
        rows.append(
            SourceRecordFinalEffectCandidateSet(
                source_record_candidate_set_id=source_set.source_record_candidate_set_id,
                source_layer=source_set.source_layer,
                source_occurrence_id=source_set.source_occurrence_id,
                source_fragment_ids=source_set.source_fragment_ids,
                final_fragment_ids=tuple(row.final_fragment_id for row in selected),
                final_candidate_ids=tuple(
                    candidate_id
                    for row in selected
                    for candidate_id in row.final_candidate_ids
                ),
            )
        )
    return tuple(rows)


def _project_envelope(
    allocation_envelope: Any,
    mechanism_envelope: Any,
    semantic_envelope: Any,
    admission_envelope: Any,
    effect_envelope: Any,
    profile: ClassicalFinalEffectCandidateEnvelopeProfile,
) -> ClassicalFinalEffectCandidateEnvelope:
    if not replay_unit6_allocation_envelope(
        allocation_envelope,
        mechanism_envelope,
        semantic_envelope,
        admission_envelope,
        effect_envelope,
    ):
        raise BaziClassicalFinalEffectCandidateEnvelopeError(
            "UPSTREAM_UNIT6_ALLOCATION_REPLAY_MISMATCH",
            allocation_envelope.allocation_envelope_id,
        )
    mechanism_fragments = {
        row.fragment_governance_projection_id: row
        for row in mechanism_envelope.fragment_governance_projections
    }
    semantic_fragments = {
        row.fragment_semantic_projection_id: row
        for row in semantic_envelope.fragment_projections
    }
    fragments = []
    for allocation_fragment in allocation_envelope.fragment_allocation_projections:
        mechanism_fragment = mechanism_fragments.get(
            allocation_fragment.source_fragment_governance_projection_id
        )
        semantic_fragment = semantic_fragments.get(
            allocation_fragment.source_fragment_semantic_projection_id
        )
        if mechanism_fragment is None or semantic_fragment is None:
            raise BaziClassicalFinalEffectCandidateEnvelopeError(
                "UPSTREAM_FRAGMENT_CHAIN_MISSING",
                allocation_fragment.source_fragment_id,
            )
        fragments.append(
            _project_fragment(
                allocation_fragment,
                mechanism_fragment,
                semantic_fragment,
                semantic_envelope,
                mechanism_envelope,
                allocation_envelope,
                profile,
            )
        )
    fragment_envelopes = tuple(fragments)
    source_sets = _source_record_sets(allocation_envelope, fragment_envelopes)
    final_candidates = tuple(
        candidate
        for fragment in fragment_envelopes
        for candidate in fragment.final_candidates
    )
    (
        effect_index,
        semantic_index,
        mechanism_index,
        closure_index,
        multiplicity_index,
    ) = build_expected_indexes(final_candidates)
    final_ids = tuple(row.final_candidate_id for row in final_candidates)
    lineage = (
        *allocation_envelope.lineage_binding_keys,
        f"SOURCE_ALLOCATION_FACT:{allocation_envelope.hashes.fact_hash}",
        f"SOURCE_ALLOCATION_COMPUTATION:{allocation_envelope.hashes.computation_hash}",
        f"FINAL_EFFECT_ENVELOPE_PROFILE:{profile.profile_id}:{profile.profile_version}",
    )
    hashes = final_effect_hash_bundle(
        allocation_envelope,
        fragment_envelopes,
        source_sets,
        effect_index,
        semantic_index,
        mechanism_index,
        closure_index,
        multiplicity_index,
        final_ids,
        lineage,
        profile,
    )
    integrity = validate_final_effect_envelope(
        allocation_envelope,
        mechanism_envelope,
        semantic_envelope,
        admission_envelope,
        effect_envelope,
        fragment_envelopes,
        source_sets,
        effect_index,
        semantic_index,
        mechanism_index,
        closure_index,
        multiplicity_index,
        final_ids,
        lineage,
        profile,
        hashes,
    )
    if integrity.status != "PASS":
        raise BaziClassicalFinalEffectCandidateEnvelopeError(
            "FINAL_EFFECT_ENVELOPE_INTEGRITY_FAILED",
            ";".join(f"{row.code}:{row.path}" for row in integrity.diagnostics),
        )
    envelope_id = "CLASSICAL_FINAL_EFFECT_ENVELOPE:" + object_sha256({
        "source_allocation_envelope_id": allocation_envelope.allocation_envelope_id,
        "source_allocation_fact_hash": allocation_envelope.hashes.fact_hash,
        "fact_hash": hashes.fact_hash,
    })
    return ClassicalFinalEffectCandidateEnvelope(
        final_effect_envelope_id=envelope_id,
        source_allocation_envelope_id=allocation_envelope.allocation_envelope_id,
        source_allocation_fact_hash=allocation_envelope.hashes.fact_hash,
        source_allocation_computation_hash=allocation_envelope.hashes.computation_hash,
        source_mechanism_closure_envelope_id=allocation_envelope.source_mechanism_closure_envelope_id,
        source_mechanism_closure_fact_hash=allocation_envelope.source_mechanism_closure_fact_hash,
        source_mechanism_closure_computation_hash=(
            allocation_envelope.source_mechanism_closure_computation_hash
        ),
        source_semantic_projection_envelope_id=allocation_envelope.source_semantic_projection_envelope_id,
        source_semantic_projection_fact_hash=mechanism_envelope.source_semantic_projection_fact_hash,
        source_semantic_projection_computation_hash=(
            mechanism_envelope.source_semantic_projection_computation_hash
        ),
        source_admission_envelope_id=allocation_envelope.source_admission_envelope_id,
        source_effect_envelope_id=allocation_envelope.source_effect_envelope_id,
        lineage_binding_keys=lineage,
        fragment_envelopes=fragment_envelopes,
        source_record_candidate_sets=source_sets,
        effect_channel_index=effect_index,
        semantic_kind_index=semantic_index,
        mechanism_kind_index=mechanism_index,
        closure_status_index=closure_index,
        multiplicity_index=multiplicity_index,
        projected_final_candidate_ids=final_ids,
        final_candidate_semantics=profile.final_candidate_semantics,
        candidate_truth_semantics=profile.candidate_truth_semantics,
        candidate_operability_semantics=profile.candidate_operability_semantics,
        candidate_applicability_semantics=profile.candidate_applicability_semantics,
        mechanism_execution_semantics=profile.mechanism_execution_semantics,
        rewrite_application_semantics=profile.rewrite_application_semantics,
        lifecycle_truth_gate=profile.lifecycle_truth_gate,
        candidate_coexistence_semantics=profile.candidate_coexistence_semantics,
        candidate_exclusivity_semantics=profile.candidate_exclusivity_semantics,
        candidate_conflict_semantics=profile.candidate_conflict_semantics,
        precedence_semantics=profile.precedence_semantics,
        priority_semantics=profile.priority_semantics,
        winner_loser_semantics=profile.winner_loser_semantics,
        participant_path_selection_semantics=profile.participant_path_selection_semantics,
        relation_effect_state_semantics=profile.relation_effect_state_semantics,
        graph_mutation_fixpoint_semantics=profile.graph_mutation_fixpoint_semantics,
        execution_readiness_semantics=profile.execution_readiness_semantics,
        synthetic_permutation_generation=profile.synthetic_permutation_generation,
        synthetic_combination_generation=profile.synthetic_combination_generation,
        inferred_slot_instance_compatibility=profile.inferred_slot_instance_compatibility,
        fragment_selection_semantics=profile.fragment_selection_semantics,
        cross_outer_composition=profile.cross_outer_composition,
        cross_source_composition=profile.cross_source_composition,
        cartesian_expansion=profile.cartesian_expansion,
        raw_relation_immutability_contract=profile.raw_relation_immutability_contract,
        algorithm_versions={"final_effect_envelope": profile.algorithm_version},
        integrity=integrity,
        hashes=hashes,
    )


class BaziClassicalFinalEffectCandidateEnvelopeEngine:
    schema = "BAZI-CLASSICAL-FINAL-EFFECT-CANDIDATE-ENVELOPE-RESULT-R1"
    typed_schema = "BAZI-CLASSICAL-FINAL-EFFECT-CANDIDATE-ENVELOPE-TYPED-RESOLUTION-R1"

    def resolve_typed(
        self,
        request: BaziClassicalFinalEffectCandidateEnvelopeRequest,
    ) -> BaziClassicalFinalEffectCandidateEnvelopeResolution:
        try:
            profile = request.final_effect_profile.validate()
            for status, code in (
                (request.source_effect_constraint_resolution.status, "UPSTREAM_EFFECT_RESOLUTION_NOT_RESOLVED"),
                (request.source_resolver_admission_resolution.status, "UPSTREAM_ADMISSION_RESOLUTION_NOT_RESOLVED"),
                (request.source_semantic_candidate_resolution.status, "UPSTREAM_SEMANTIC_RESOLUTION_NOT_RESOLVED"),
                (request.source_mechanism_closure_resolution.status, "UPSTREAM_MECHANISM_RESOLUTION_NOT_RESOLVED"),
                (request.source_allocation_resolution.status, "UPSTREAM_ALLOCATION_RESOLUTION_NOT_RESOLVED"),
            ):
                if status not in {"RESOLVED", "MULTI_CANDIDATE"}:
                    raise BaziClassicalFinalEffectCandidateEnvelopeError(code, status)
            rows = []
            seen_lineages: set[tuple[str, str]] = set()
            for allocation_envelope in request.source_allocation_resolution.candidates:
                lineage = (
                    allocation_envelope.hashes.fact_hash,
                    allocation_envelope.hashes.computation_hash,
                )
                if lineage in seen_lineages:
                    raise BaziClassicalFinalEffectCandidateEnvelopeError(
                        "UPSTREAM_UNIT6_OUTER_LINEAGE_PROJECTED_MORE_THAN_ONCE",
                        f"{lineage[0]}:{lineage[1]}",
                    )
                seen_lineages.add(lineage)
                mechanism_envelope = match_mechanism_envelope(
                    allocation_envelope,
                    request.source_mechanism_closure_resolution,
                )
                semantic_envelope = match_semantic_envelope(
                    mechanism_envelope,
                    request.source_semantic_candidate_resolution,
                )
                admission_envelope = match_admission_envelope(
                    semantic_envelope,
                    request.source_resolver_admission_resolution,
                )
                effect_envelope = match_effect_envelope(
                    semantic_envelope,
                    request.source_effect_constraint_resolution,
                )
                rows.append(
                    _project_envelope(
                        allocation_envelope,
                        mechanism_envelope,
                        semantic_envelope,
                        admission_envelope,
                        effect_envelope,
                        profile,
                    )
                )
            candidates = tuple(rows)
            return BaziClassicalFinalEffectCandidateEnvelopeResolution(
                schema=self.typed_schema,
                status="RESOLVED" if len(candidates) == 1 else "MULTI_CANDIDATE",
                candidates=candidates,
                events=("AMBIGUOUS_UPSTREAM_LINEAGES_PRESERVED",)
                if len(candidates) > 1
                else (),
                diagnostics=(),
            )
        except (BaziClassicalFinalEffectCandidateEnvelopeError, KeyError, ValueError) as exc:
            code = getattr(
                exc,
                "diagnostic_code",
                "CLASSICAL_FINAL_EFFECT_CANDIDATE_ENVELOPE_FAILED",
            )
            return BaziClassicalFinalEffectCandidateEnvelopeResolution(
                self.typed_schema,
                "FAILED",
                (),
                (),
                (f"{code}:{exc}",),
            )

    def resolve(self, request: BaziClassicalFinalEffectCandidateEnvelopeRequest) -> dict[str, Any]:
        typed = self.resolve_typed(request)
        return {
            "schema": self.schema,
            "typed_schema": typed.schema,
            "status": typed.status,
            "final_effect_profile": json_value(request.final_effect_profile),
            "candidates": json_value(typed.candidates),
            "events": list(typed.events),
            "diagnostics": list(typed.diagnostics),
        }
