from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fortune_training.bazi_classical_effect_constraint_graph.models import (
    BaziClassicalEffectConstraintGraphResolution,
)
from fortune_training.bazi_classical_effect_semantic_candidate.models import (
    BaziClassicalEffectSemanticCandidateProjectionResolution,
)
from fortune_training.bazi_classical_resolver_admission.models import (
    BaziClassicalResolverAdmissionResolution,
)
from fortune_training.bazi_classical_semantic_closure_governance.models import (
    BaziClassicalSemanticMechanismClosureGovernanceResolution,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .domain import (
    AllocationMultiplicityContractError,
    build_unordered_path_candidate,
    classify_allocation_domain,
)
from .integrity import (
    allocation_hash_bundle,
    match_admission_envelope,
    match_effect_envelope,
    match_semantic_envelope,
    replay_unit5_mechanism_closure_envelope,
    validate_allocation_envelope,
)
from .models import (
    AllocationDomainObservation,
    BaziClassicalNonSelectingParticipantAllocationResolution,
    ClassicalNonSelectingParticipantAllocationEnvelope,
    FragmentAllocationElaborationProjection,
    MultiplicityAllocationDomainIndexEntry,
    ProposalAllocationElaboration,
    SourceRecordAllocationElaborationSet,
)
from .profile import (
    ALLOCATION_MECHANISM_PROPOSAL_KIND,
    ALLOCATION_SEMANTIC_CANDIDATE_KIND,
    ClassicalNonSelectingParticipantAllocationProfile,
)


class BaziClassicalNonSelectingParticipantAllocationError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class BaziClassicalNonSelectingParticipantAllocationRequest:
    source_effect_constraint_resolution: BaziClassicalEffectConstraintGraphResolution
    source_resolver_admission_resolution: BaziClassicalResolverAdmissionResolution
    source_semantic_candidate_resolution: BaziClassicalEffectSemanticCandidateProjectionResolution
    source_mechanism_closure_resolution: BaziClassicalSemanticMechanismClosureGovernanceResolution
    allocation_profile: ClassicalNonSelectingParticipantAllocationProfile


def _unique_strings(rows: list[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(rows))


def _allocation_observation(
    semantic_candidate: Any,
    mechanism_proposal: Any,
    multiplicity_reference: Any,
    profile: ClassicalNonSelectingParticipantAllocationProfile,
) -> AllocationDomainObservation:
    try:
        classification, blockers = classify_allocation_domain(multiplicity_reference)
    except AllocationMultiplicityContractError as exc:
        raise BaziClassicalNonSelectingParticipantAllocationError(
            exc.diagnostic_code,
            str(exc),
        ) from exc
    paths = ()
    if classification == "EXACT_INSTANCE_SET_CARDINALITY_MATCH":
        paths = (
            build_unordered_path_candidate(
                semantic_candidate.semantic_candidate_id,
                mechanism_proposal.mechanism_proposal_id,
                multiplicity_reference,
                profile,
            ),
        )
    observation_id = "CLASSICAL_ALLOCATION_DOMAIN_OBSERVATION:" + object_sha256({
        "source_semantic_candidate_id": semantic_candidate.semantic_candidate_id,
        "source_mechanism_proposal_id": mechanism_proposal.mechanism_proposal_id,
        "multiplicity_constraint_id": multiplicity_reference.multiplicity_constraint_id,
        "classification": classification,
        "blockers": blockers,
        "path_candidate_ids": tuple(row.path_candidate_id for row in paths),
    })
    return AllocationDomainObservation(
        allocation_domain_observation_id=observation_id,
        source_semantic_candidate_id=semantic_candidate.semantic_candidate_id,
        source_mechanism_proposal_id=mechanism_proposal.mechanism_proposal_id,
        source_occurrence_id=semantic_candidate.source_occurrence_id,
        binding_candidate_id=semantic_candidate.binding_candidate_id,
        graph_record_id=semantic_candidate.graph_record_id,
        interaction_assertion_id=semantic_candidate.interaction_assertion_id,
        source_claim_edge_id=semantic_candidate.source_claim_edge_id,
        target_exact_relation_id=semantic_candidate.target_exact_relation_id,
        effect_facet=semantic_candidate.effect_facet,
        multiplicity_constraint_id=multiplicity_reference.multiplicity_constraint_id,
        exchangeable_symbolic_slot_node_ids=(
            multiplicity_reference.exchangeable_symbolic_slot_node_ids
        ),
        exact_runtime_instance_ids=multiplicity_reference.exact_runtime_instance_ids,
        required_symbolic_cardinality=multiplicity_reference.required_symbolic_cardinality,
        slot_equivalence=multiplicity_reference.slot_equivalence,
        alternative_path_requirement=multiplicity_reference.alternative_path_requirement,
        allocation_domain_classification=classification,
        domain_blocker_ids=blockers,
        path_candidates=paths,
        unit5_allocation_closure_rows=mechanism_proposal.closure_governance_rows,
        source_unresolved_graph_requirements_provenance=(
            mechanism_proposal.source_unresolved_graph_requirements_provenance
        ),
        source_narrative_chain_ids_provenance=(
            mechanism_proposal.source_narrative_chain_ids_provenance
        ),
    )


def project_proposal_allocation_elaboration(
    source_fragment: Any,
    semantic_candidate: Any,
    mechanism_proposal: Any,
    profile: ClassicalNonSelectingParticipantAllocationProfile,
) -> ProposalAllocationElaboration:
    if mechanism_proposal.source_semantic_candidate_id != semantic_candidate.semantic_candidate_id:
        raise BaziClassicalNonSelectingParticipantAllocationError(
            "UNIT5_PROPOSAL_UNIT4_CANDIDATE_ID_MISMATCH",
            mechanism_proposal.mechanism_proposal_id,
        )
    is_allocation = mechanism_proposal.mechanism_proposal_kind == ALLOCATION_MECHANISM_PROPOSAL_KIND
    if is_allocation:
        if semantic_candidate.semantic_candidate_kind != ALLOCATION_SEMANTIC_CANDIDATE_KIND:
            raise BaziClassicalNonSelectingParticipantAllocationError(
                "ALLOCATION_PROPOSAL_SEMANTIC_CANDIDATE_KIND_MISMATCH",
                mechanism_proposal.mechanism_proposal_id,
            )
        if not semantic_candidate.multiplicity_references:
            raise BaziClassicalNonSelectingParticipantAllocationError(
                "ALLOCATION_PROPOSAL_WITHOUT_MULTIPLICITY_REFERENCE",
                mechanism_proposal.mechanism_proposal_id,
            )
        observations = tuple(
            _allocation_observation(
                semantic_candidate,
                mechanism_proposal,
                reference,
                profile,
            )
            for reference in semantic_candidate.multiplicity_references
        )
        semantics = "NON_SELECTING_ALLOCATION_DOMAIN_ELABORATION_ONLY"
    else:
        observations = ()
        semantics = "NON_ALLOCATION_PROPOSAL_PRESERVED_ZERO_DOMAINS"

    elaboration_id = "CLASSICAL_PROPOSAL_ALLOCATION_ELABORATION:" + object_sha256({
        "source_mechanism_proposal_id": mechanism_proposal.mechanism_proposal_id,
        "source_semantic_candidate_id": semantic_candidate.semantic_candidate_id,
        "allocation_domain_observation_ids": tuple(
            row.allocation_domain_observation_id for row in observations
        ),
        "allocation_elaboration_semantics": semantics,
    })
    return ProposalAllocationElaboration(
        proposal_allocation_elaboration_id=elaboration_id,
        source_mechanism_proposal_id=mechanism_proposal.mechanism_proposal_id,
        source_semantic_candidate_id=semantic_candidate.semantic_candidate_id,
        source_fragment_governance_projection_id=(
            source_fragment.fragment_governance_projection_id
        ),
        source_fragment_semantic_projection_id=(
            source_fragment.source_fragment_semantic_projection_id
        ),
        source_fragment_id=source_fragment.source_fragment_id,
        source_occurrence_id=source_fragment.source_occurrence_id,
        binding_candidate_id=source_fragment.binding_candidate_id,
        semantic_candidate_kind=semantic_candidate.semantic_candidate_kind,
        mechanism_proposal_kind=mechanism_proposal.mechanism_proposal_kind,
        allocation_domain_observations=observations,
        allocation_elaboration_semantics=semantics,
    )


def _project_fragment(
    source_fragment: Any,
    semantic_fragment: Any,
    profile: ClassicalNonSelectingParticipantAllocationProfile,
) -> FragmentAllocationElaborationProjection:
    candidate_by_id = {
        row.semantic_candidate_id: row for row in semantic_fragment.semantic_candidates
    }
    if len(candidate_by_id) != len(semantic_fragment.semantic_candidates):
        raise BaziClassicalNonSelectingParticipantAllocationError(
            "DUPLICATE_UNIT4_SEMANTIC_CANDIDATE_ID",
            source_fragment.source_fragment_id,
        )
    elaborations = []
    for proposal in source_fragment.mechanism_proposals:
        candidate = candidate_by_id.get(proposal.source_semantic_candidate_id)
        if candidate is None:
            raise BaziClassicalNonSelectingParticipantAllocationError(
                "UNIT5_PROPOSAL_SOURCE_UNIT4_CANDIDATE_MISSING",
                proposal.mechanism_proposal_id,
            )
        elaborations.append(
            project_proposal_allocation_elaboration(
                source_fragment,
                candidate,
                proposal,
                profile,
            )
        )
    proposal_elaborations = tuple(elaborations)
    domain_ids = tuple(
        observation.allocation_domain_observation_id
        for row in proposal_elaborations
        for observation in row.allocation_domain_observations
    )
    if domain_ids:
        status = "ALLOCATION_DOMAIN_ELABORATION_PROJECTED"
    elif source_fragment.mechanism_proposals:
        status = "PRESERVED_NO_ALLOCATION_DOMAINS"
    else:
        status = "PRESERVED_ZERO_PROPOSALS_NO_ALLOCATION_DOMAINS"
    source_proposal_ids = tuple(
        row.mechanism_proposal_id for row in source_fragment.mechanism_proposals
    )
    projection_id = "CLASSICAL_FRAGMENT_ALLOCATION_ELABORATION:" + object_sha256({
        "source_fragment_governance_projection_id": (
            source_fragment.fragment_governance_projection_id
        ),
        "source_mechanism_proposal_ids": source_proposal_ids,
        "proposal_allocation_elaboration_ids": tuple(
            row.proposal_allocation_elaboration_id for row in proposal_elaborations
        ),
        "allocation_status": status,
    })
    return FragmentAllocationElaborationProjection(
        fragment_allocation_projection_id=projection_id,
        source_fragment_governance_projection_id=(
            source_fragment.fragment_governance_projection_id
        ),
        source_fragment_semantic_projection_id=(
            source_fragment.source_fragment_semantic_projection_id
        ),
        source_fragment_id=source_fragment.source_fragment_id,
        source_occurrence_id=source_fragment.source_occurrence_id,
        binding_candidate_id=source_fragment.binding_candidate_id,
        source_governance_status=source_fragment.governance_status,
        allocation_status=status,
        source_mechanism_proposal_ids=source_proposal_ids,
        proposal_elaborations=proposal_elaborations,
        allocation_domain_observation_ids=domain_ids,
    )


def _source_record_sets(
    source_mechanism_envelope: Any,
    fragment_projections: tuple[FragmentAllocationElaborationProjection, ...],
) -> tuple[SourceRecordAllocationElaborationSet, ...]:
    by_fragment = {row.source_fragment_id: row for row in fragment_projections}
    if len(by_fragment) != len(fragment_projections):
        raise BaziClassicalNonSelectingParticipantAllocationError(
            "DUPLICATE_UNIT6_FRAGMENT_SOURCE_ID",
            str(len(fragment_projections)),
        )
    rows = []
    for source_set in source_mechanism_envelope.source_record_candidate_sets:
        if any(
            value != "NOT_RELEASED"
            for value in (
                source_set.member_selection_semantics,
                source_set.member_coexistence_semantics,
                source_set.member_exclusivity_semantics,
                source_set.proposal_priority_semantics,
                source_set.proposal_conflict_semantics,
            )
        ):
            raise BaziClassicalNonSelectingParticipantAllocationError(
                "UPSTREAM_SOURCE_RECORD_SET_SEMANTICS_OVERRESOLVED",
                source_set.source_record_candidate_set_id,
            )
        fragments = tuple(by_fragment[row] for row in source_set.source_fragment_ids)
        rows.append(
            SourceRecordAllocationElaborationSet(
                source_record_candidate_set_id=source_set.source_record_candidate_set_id,
                source_layer=source_set.source_layer,
                source_occurrence_id=source_set.source_occurrence_id,
                source_fragment_ids=source_set.source_fragment_ids,
                fragment_allocation_projection_ids=tuple(
                    row.fragment_allocation_projection_id for row in fragments
                ),
                source_mechanism_proposal_ids=tuple(
                    proposal_id
                    for row in fragments
                    for proposal_id in row.source_mechanism_proposal_ids
                ),
                allocation_domain_observation_ids=tuple(
                    domain_id
                    for row in fragments
                    for domain_id in row.allocation_domain_observation_ids
                ),
                path_candidate_ids=tuple(
                    path.path_candidate_id
                    for row in fragments
                    for proposal in row.proposal_elaborations
                    for observation in proposal.allocation_domain_observations
                    for path in observation.path_candidates
                ),
            )
        )
    return tuple(rows)


def _multiplicity_index(
    fragment_projections: tuple[FragmentAllocationElaborationProjection, ...],
) -> tuple[MultiplicityAllocationDomainIndexEntry, ...]:
    grouped: dict[str, dict[str, list[str]]] = {}
    for fragment in fragment_projections:
        for proposal in fragment.proposal_elaborations:
            for observation in proposal.allocation_domain_observations:
                group = grouped.setdefault(
                    observation.multiplicity_constraint_id,
                    {"candidates": [], "proposals": [], "domains": [], "paths": []},
                )
                group["candidates"].append(observation.source_semantic_candidate_id)
                group["proposals"].append(observation.source_mechanism_proposal_id)
                group["domains"].append(observation.allocation_domain_observation_id)
                group["paths"].extend(
                    path.path_candidate_id for path in observation.path_candidates
                )
    return tuple(
        MultiplicityAllocationDomainIndexEntry(
            multiplicity_constraint_id=constraint_id,
            source_semantic_candidate_ids=_unique_strings(group["candidates"]),
            source_mechanism_proposal_ids=_unique_strings(group["proposals"]),
            allocation_domain_observation_ids=tuple(group["domains"]),
            path_candidate_ids=tuple(group["paths"]),
        )
        for constraint_id, group in sorted(grouped.items())
    )


def _project_envelope(
    source_mechanism_envelope: Any,
    source_semantic_envelope: Any,
    admission_envelope: Any,
    effect_envelope: Any,
    profile: ClassicalNonSelectingParticipantAllocationProfile,
) -> ClassicalNonSelectingParticipantAllocationEnvelope:
    if not replay_unit5_mechanism_closure_envelope(
        source_mechanism_envelope,
        source_semantic_envelope,
        admission_envelope,
        effect_envelope,
    ):
        raise BaziClassicalNonSelectingParticipantAllocationError(
            "UPSTREAM_UNIT5_MECHANISM_CLOSURE_REPLAY_MISMATCH",
            source_mechanism_envelope.mechanism_closure_envelope_id,
        )
    semantic_by_fragment = {
        row.fragment_semantic_projection_id: row
        for row in source_semantic_envelope.fragment_projections
    }
    fragments = tuple(
        _project_fragment(
            source_fragment,
            semantic_by_fragment[source_fragment.source_fragment_semantic_projection_id],
            profile,
        )
        for source_fragment in source_mechanism_envelope.fragment_governance_projections
    )
    source_sets = _source_record_sets(source_mechanism_envelope, fragments)
    multiplicity_index = _multiplicity_index(fragments)
    domain_ids = tuple(
        domain_id for row in fragments for domain_id in row.allocation_domain_observation_ids
    )
    path_ids = tuple(
        path.path_candidate_id
        for row in fragments
        for proposal in row.proposal_elaborations
        for observation in proposal.allocation_domain_observations
        for path in observation.path_candidates
    )
    lineage = (
        *source_mechanism_envelope.lineage_binding_keys,
        f"SOURCE_MECHANISM_CLOSURE_FACT:{source_mechanism_envelope.hashes.fact_hash}",
        f"SOURCE_MECHANISM_CLOSURE_COMPUTATION:{source_mechanism_envelope.hashes.computation_hash}",
        f"NON_SELECTING_ALLOCATION_PROFILE:{profile.profile_id}:{profile.profile_version}",
    )
    hashes = allocation_hash_bundle(
        source_mechanism_envelope,
        fragments,
        source_sets,
        multiplicity_index,
        domain_ids,
        path_ids,
        lineage,
        profile,
    )
    integrity = validate_allocation_envelope(
        source_mechanism_envelope,
        source_semantic_envelope,
        admission_envelope,
        effect_envelope,
        fragments,
        source_sets,
        multiplicity_index,
        domain_ids,
        path_ids,
        lineage,
        profile,
        hashes,
    )
    if integrity.status != "PASS":
        raise BaziClassicalNonSelectingParticipantAllocationError(
            "NON_SELECTING_ALLOCATION_INTEGRITY_FAILED",
            ";".join(f"{row.code}:{row.path}" for row in integrity.diagnostics),
        )
    envelope_id = "CLASSICAL_NON_SELECTING_ALLOCATION_ENVELOPE:" + object_sha256({
        "source_mechanism_closure_envelope_id": (
            source_mechanism_envelope.mechanism_closure_envelope_id
        ),
        "source_mechanism_closure_fact_hash": source_mechanism_envelope.hashes.fact_hash,
        "fact_hash": hashes.fact_hash,
    })
    return ClassicalNonSelectingParticipantAllocationEnvelope(
        allocation_envelope_id=envelope_id,
        source_mechanism_closure_envelope_id=(
            source_mechanism_envelope.mechanism_closure_envelope_id
        ),
        source_mechanism_closure_fact_hash=source_mechanism_envelope.hashes.fact_hash,
        source_mechanism_closure_computation_hash=(
            source_mechanism_envelope.hashes.computation_hash
        ),
        source_semantic_projection_envelope_id=(
            source_mechanism_envelope.source_semantic_projection_envelope_id
        ),
        source_admission_envelope_id=source_mechanism_envelope.source_admission_envelope_id,
        source_effect_envelope_id=source_mechanism_envelope.source_effect_envelope_id,
        lineage_binding_keys=lineage,
        fragment_allocation_projections=fragments,
        source_record_candidate_sets=source_sets,
        multiplicity_domain_index=multiplicity_index,
        projected_allocation_domain_observation_ids=domain_ids,
        projected_path_candidate_ids=path_ids,
        synthetic_permutation_generation=profile.synthetic_permutation_generation,
        synthetic_combination_generation=profile.synthetic_combination_generation,
        inferred_slot_instance_compatibility=profile.inferred_slot_instance_compatibility,
        participant_path_selection_semantics=profile.participant_path_selection_semantics,
        allocation_truth_semantics=profile.allocation_truth_semantics,
        allocation_operability_semantics=profile.allocation_operability_semantics,
        coexistence_semantics=profile.coexistence_semantics,
        exclusivity_semantics=profile.exclusivity_semantics,
        precedence_semantics=profile.precedence_semantics,
        priority_semantics=profile.priority_semantics,
        winner_loser_semantics=profile.winner_loser_semantics,
        relation_effect_state_semantics=profile.relation_effect_state_semantics,
        rewrite_application_semantics=profile.rewrite_application_semantics,
        fragment_selection_semantics=profile.fragment_selection_semantics,
        cross_outer_composition=profile.cross_outer_composition,
        cartesian_expansion=profile.cartesian_expansion,
        raw_relation_immutability_contract=profile.raw_relation_immutability_contract,
        algorithm_versions={"non_selecting_allocation": profile.algorithm_version},
        integrity=integrity,
        hashes=hashes,
    )


class BaziClassicalNonSelectingParticipantAllocationEngine:
    schema = "BAZI-CLASSICAL-NON-SELECTING-PARTICIPANT-ALLOCATION-RESULT-R1"
    typed_schema = "BAZI-CLASSICAL-NON-SELECTING-PARTICIPANT-ALLOCATION-TYPED-RESOLUTION-R1"

    def resolve_typed(
        self,
        request: BaziClassicalNonSelectingParticipantAllocationRequest,
    ) -> BaziClassicalNonSelectingParticipantAllocationResolution:
        try:
            profile = request.allocation_profile.validate()
            for status, code in (
                (
                    request.source_effect_constraint_resolution.status,
                    "UPSTREAM_EFFECT_RESOLUTION_NOT_RESOLVED",
                ),
                (
                    request.source_resolver_admission_resolution.status,
                    "UPSTREAM_ADMISSION_RESOLUTION_NOT_RESOLVED",
                ),
                (
                    request.source_semantic_candidate_resolution.status,
                    "UPSTREAM_SEMANTIC_CANDIDATE_RESOLUTION_NOT_RESOLVED",
                ),
                (
                    request.source_mechanism_closure_resolution.status,
                    "UPSTREAM_MECHANISM_CLOSURE_RESOLUTION_NOT_RESOLVED",
                ),
            ):
                if status not in {"RESOLVED", "MULTI_CANDIDATE"}:
                    raise BaziClassicalNonSelectingParticipantAllocationError(code, status)

            rows = []
            seen_lineages: set[tuple[str, str]] = set()
            for source_mechanism_envelope in request.source_mechanism_closure_resolution.candidates:
                lineage = (
                    source_mechanism_envelope.hashes.fact_hash,
                    source_mechanism_envelope.hashes.computation_hash,
                )
                if lineage in seen_lineages:
                    raise BaziClassicalNonSelectingParticipantAllocationError(
                        "UPSTREAM_UNIT5_OUTER_LINEAGE_PROJECTED_MORE_THAN_ONCE",
                        f"{lineage[0]}:{lineage[1]}",
                    )
                seen_lineages.add(lineage)
                semantic_envelope = match_semantic_envelope(
                    source_mechanism_envelope,
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
                        source_mechanism_envelope,
                        semantic_envelope,
                        admission_envelope,
                        effect_envelope,
                        profile,
                    )
                )
            candidates = tuple(rows)
            return BaziClassicalNonSelectingParticipantAllocationResolution(
                schema=self.typed_schema,
                status="RESOLVED" if len(candidates) == 1 else "MULTI_CANDIDATE",
                candidates=candidates,
                events=("AMBIGUOUS_UPSTREAM_LINEAGES_PRESERVED",)
                if len(candidates) > 1
                else (),
                diagnostics=(),
            )
        except (
            AllocationMultiplicityContractError,
            BaziClassicalNonSelectingParticipantAllocationError,
            KeyError,
            ValueError,
        ) as exc:
            code = getattr(
                exc,
                "diagnostic_code",
                "CLASSICAL_NON_SELECTING_PARTICIPANT_ALLOCATION_FAILED",
            )
            return BaziClassicalNonSelectingParticipantAllocationResolution(
                self.typed_schema,
                "FAILED",
                (),
                (),
                (f"{code}:{exc}",),
            )

    def resolve(self, request: BaziClassicalNonSelectingParticipantAllocationRequest) -> dict[str, Any]:
        typed = self.resolve_typed(request)
        return {
            "schema": self.schema,
            "typed_schema": typed.schema,
            "status": typed.status,
            "allocation_profile": json_value(request.allocation_profile),
            "candidates": json_value(typed.candidates),
            "events": list(typed.events),
            "diagnostics": list(typed.diagnostics),
        }
