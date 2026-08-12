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
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .integrity import (
    match_admission_envelope,
    match_effect_envelope,
    mechanism_closure_hash_bundle,
    replay_unit4_semantic_envelope,
    validate_mechanism_closure_envelope,
)
from .models import (
    BaziClassicalSemanticMechanismClosureGovernanceResolution,
    ClassicalFragmentMechanismClosureGovernanceProjection,
    ClassicalMechanismProposalGovernance,
    ClassicalSemanticClosureGovernanceRow,
    ClassicalSemanticMechanismClosureGovernanceEnvelope,
    ClosureRequirementGovernanceIndexEntry,
    MechanismProposalGovernanceIndexEntry,
    SourceRecordMechanismClosureGovernanceSet,
)
from .profile import (
    CLOSURE_REQUIREMENT_REGISTRY,
    SEMANTIC_CANDIDATE_TO_MECHANISM_PROPOSAL,
    ClassicalSemanticMechanismClosureGovernanceProfile,
)


class BaziClassicalSemanticMechanismClosureGovernanceError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class BaziClassicalSemanticMechanismClosureGovernanceRequest:
    source_effect_constraint_resolution: BaziClassicalEffectConstraintGraphResolution
    source_resolver_admission_resolution: BaziClassicalResolverAdmissionResolution
    source_semantic_candidate_resolution: BaziClassicalEffectSemanticCandidateProjectionResolution
    mechanism_closure_profile: ClassicalSemanticMechanismClosureGovernanceProfile


def _unique_strings(rows: list[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(rows))


def _support_for_requirement(candidate: Any, requirement_id: str) -> tuple[str, tuple[str, ...]]:
    if requirement_id == "CLASSICAL_INTERACTION_CHAIN_RESOLUTION":
        if candidate.source_narrative_chain_ids:
            return (
                "SOURCE_NARRATIVE_CHAIN_IDENTITY_PROVENANCE_ONLY",
                candidate.source_narrative_chain_ids,
            )
        return ("NO_MECHANICALLY_PROVEN_SUPPORT_BEYOND_CANDIDATE_IDENTITY", ())

    if requirement_id in {
        "CLASSICAL_PARTICIPANT_ALLOCATION",
        "COMPATIBLE_EXACT_INSTANCE_PATH_ENUMERATION",
    }:
        if not candidate.multiplicity_references:
            raise BaziClassicalSemanticMechanismClosureGovernanceError(
                "ALLOCATION_CLOSURE_WITHOUT_UPSTREAM_MULTIPLICITY",
                candidate.semantic_candidate_id,
            )
        constraint_ids = tuple(
            reference.multiplicity_constraint_id
            for reference in candidate.multiplicity_references
        )
        runtime_ids = _unique_strings([
            runtime_id
            for reference in candidate.multiplicity_references
            for runtime_id in reference.exact_runtime_instance_ids
        ])
        if requirement_id == "COMPATIBLE_EXACT_INSTANCE_PATH_ENUMERATION":
            if not runtime_ids or any(
                reference.alternative_path_requirement
                != "PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS"
                for reference in candidate.multiplicity_references
            ):
                raise BaziClassicalSemanticMechanismClosureGovernanceError(
                    "ALLOCATION_PATH_PARTIAL_SUPPORT_CONTRACT_MISMATCH",
                    candidate.semantic_candidate_id,
                )
            return (
                "EXACT_MULTIPLICITY_RUNTIME_INSTANCE_PROVENANCE_PARTIAL_PATH_SUPPORT",
                (*constraint_ids, *runtime_ids),
            )
        return (
            "EXACT_MULTIPLICITY_IDENTITY_WITHOUT_ALLOCATION_SEMANTICS",
            (*constraint_ids, *runtime_ids),
        )

    relation_ids = _unique_strings([
        *candidate.actor_exact_relation_ids,
        candidate.target_exact_relation_id,
    ])
    if not relation_ids:
        return (
            "SOURCE_GROUNDED_CANDIDATE_IDENTITY_ONLY",
            (candidate.semantic_candidate_id,),
        )
    return (
        "EXACT_SOURCE_GROUNDED_RELATION_IDENTITY_WITHOUT_CLASSICAL_SEMANTIC_CLOSURE",
        relation_ids,
    )


def project_mechanism_proposal(
    source_semantic_envelope: Any,
    fragment_projection: Any,
    candidate: Any,
    profile: ClassicalSemanticMechanismClosureGovernanceProfile,
) -> ClassicalMechanismProposalGovernance:
    mechanism_kind = SEMANTIC_CANDIDATE_TO_MECHANISM_PROPOSAL.get(
        candidate.semantic_candidate_kind
    )
    if mechanism_kind is None:
        raise BaziClassicalSemanticMechanismClosureGovernanceError(
            "UNIT4_SEMANTIC_CANDIDATE_KIND_NOT_RELEASED_FOR_UNIT5",
            candidate.semantic_candidate_kind,
        )
    requirements = tuple(candidate.unresolved_classical_semantic_requirements)
    if not requirements:
        raise BaziClassicalSemanticMechanismClosureGovernanceError(
            "SEMANTIC_CANDIDATE_WITHOUT_DECLARED_CLOSURE_REQUIREMENT",
            candidate.semantic_candidate_id,
        )
    if len(requirements) != len(set(requirements)):
        raise BaziClassicalSemanticMechanismClosureGovernanceError(
            "DUPLICATE_DECLARED_CLOSURE_REQUIREMENT",
            candidate.semantic_candidate_id,
        )

    rows: list[ClassicalSemanticClosureGovernanceRow] = []
    for requirement_id in requirements:
        registry = CLOSURE_REQUIREMENT_REGISTRY.get(requirement_id)
        if registry is None:
            raise BaziClassicalSemanticMechanismClosureGovernanceError(
                "UNKNOWN_UNIT5_CLOSURE_REQUIREMENT",
                f"{candidate.semantic_candidate_id}:{requirement_id}",
            )
        support_class, support_ids = _support_for_requirement(candidate, requirement_id)
        rows.append(ClassicalSemanticClosureGovernanceRow(
            closure_requirement_id=requirement_id,
            runtime_dependency_status=registry["runtime_dependency_status"],
            governance_class=registry["governance_class"],
            future_owner=registry["future_owner"],
            upstream_support_class=support_class,
            upstream_support_reference_ids=support_ids,
        ))
    closure_rows = tuple(rows)
    proposal_id = "CLASSICAL_SEMANTIC_MECHANISM_PROPOSAL:" + object_sha256({
        "source_semantic_candidate_id": candidate.semantic_candidate_id,
        "semantic_candidate_kind": candidate.semantic_candidate_kind,
        "mechanism_proposal_kind": mechanism_kind,
        "closure_requirements": tuple(
            (
                row.closure_requirement_id,
                row.runtime_dependency_status,
                row.governance_class,
                row.future_owner,
                row.upstream_support_class,
                row.upstream_support_reference_ids,
            )
            for row in closure_rows
        ),
    })
    return ClassicalMechanismProposalGovernance(
        mechanism_proposal_id=proposal_id,
        source_semantic_candidate_id=candidate.semantic_candidate_id,
        source_semantic_projection_envelope_id=source_semantic_envelope.semantic_projection_envelope_id,
        source_semantic_projection_fact_hash=source_semantic_envelope.hashes.fact_hash,
        source_semantic_projection_computation_hash=source_semantic_envelope.hashes.computation_hash,
        source_fragment_semantic_projection_id=fragment_projection.fragment_semantic_projection_id,
        source_fragment_id=candidate.source_fragment_id,
        source_fragment_fact_hash=candidate.source_fragment_fact_hash,
        source_fragment_computation_hash=candidate.source_fragment_computation_hash,
        binding_candidate_id=candidate.binding_candidate_id,
        source_occurrence_id=candidate.source_occurrence_id,
        graph_record_id=candidate.graph_record_id,
        interaction_assertion_id=candidate.interaction_assertion_id,
        source_claim_edge_id=candidate.source_claim_edge_id,
        target_exact_relation_id=candidate.target_exact_relation_id,
        effect_facet=candidate.effect_facet,
        semantic_candidate_kind=candidate.semantic_candidate_kind,
        mechanism_proposal_kind=mechanism_kind,
        unresolved_classical_semantic_requirements=requirements,
        closure_governance_rows=closure_rows,
        source_unresolved_graph_requirements_provenance=candidate.source_unresolved_graph_requirements_provenance,
        source_narrative_chain_ids_provenance=candidate.source_narrative_chain_ids,
        source_semantic_profile_id=candidate.source_semantic_profile_id,
        source_semantic_partition_id=candidate.source_semantic_partition_id,
        mechanism_proposal_semantics=profile.mechanism_proposal_semantics,
        mechanism_execution_semantics=profile.mechanism_execution_semantics,
        rewrite_application_semantics=profile.rewrite_application_semantics,
    )


def project_fragment_governance(
    source_semantic_envelope: Any,
    source_fragment_projection: Any,
    profile: ClassicalSemanticMechanismClosureGovernanceProfile,
) -> ClassicalFragmentMechanismClosureGovernanceProjection:
    candidates = tuple(source_fragment_projection.semantic_candidates)
    if source_fragment_projection.projection_status == "SEMANTIC_CANDIDATES_PROJECTED":
        if not candidates:
            raise BaziClassicalSemanticMechanismClosureGovernanceError(
                "PROJECTED_UNIT4_FRAGMENT_WITHOUT_SEMANTIC_CANDIDATE",
                source_fragment_projection.fragment_semantic_projection_id,
            )
        proposals = tuple(
            project_mechanism_proposal(
                source_semantic_envelope,
                source_fragment_projection,
                candidate,
                profile,
            )
            for candidate in candidates
        )
        governance_status = "MECHANISM_CLOSURE_GOVERNANCE_PROJECTED"
    elif source_fragment_projection.projection_status == "PRESERVED_NO_SEMANTIC_CANDIDATES":
        if candidates:
            raise BaziClassicalSemanticMechanismClosureGovernanceError(
                "PRESERVED_UNIT4_FRAGMENT_HAS_SEMANTIC_CANDIDATE",
                source_fragment_projection.fragment_semantic_projection_id,
            )
        proposals = ()
        governance_status = "PRESERVED_ZERO_MECHANISM_PROPOSALS"
    elif source_fragment_projection.projection_status == "PRESERVED_OUTSIDE_PROFILE_NO_SEMANTIC_CANDIDATES":
        if candidates:
            raise BaziClassicalSemanticMechanismClosureGovernanceError(
                "OUTSIDE_PROFILE_UNIT4_FRAGMENT_HAS_SEMANTIC_CANDIDATE",
                source_fragment_projection.fragment_semantic_projection_id,
            )
        proposals = ()
        governance_status = "PRESERVED_OUTSIDE_PROFILE_ZERO_MECHANISM_PROPOSALS"
    else:
        raise BaziClassicalSemanticMechanismClosureGovernanceError(
            "UNKNOWN_UNIT4_FRAGMENT_PROJECTION_STATUS",
            source_fragment_projection.projection_status,
        )

    projection_id = "CLASSICAL_FRAGMENT_MECHANISM_CLOSURE_GOVERNANCE:" + object_sha256({
        "source_fragment_semantic_projection_id": source_fragment_projection.fragment_semantic_projection_id,
        "source_semantic_candidate_ids": tuple(
            candidate.semantic_candidate_id for candidate in candidates
        ),
        "mechanism_proposal_ids": tuple(
            proposal.mechanism_proposal_id for proposal in proposals
        ),
        "governance_status": governance_status,
    })
    return ClassicalFragmentMechanismClosureGovernanceProjection(
        fragment_governance_projection_id=projection_id,
        source_fragment_semantic_projection_id=source_fragment_projection.fragment_semantic_projection_id,
        source_fragment_id=source_fragment_projection.source_fragment_id,
        source_occurrence_id=source_fragment_projection.source_occurrence_id,
        binding_candidate_id=source_fragment_projection.binding_candidate_id,
        source_projection_status=source_fragment_projection.projection_status,
        governance_status=governance_status,
        source_semantic_candidate_ids=tuple(
            candidate.semantic_candidate_id for candidate in candidates
        ),
        mechanism_proposals=proposals,
        source_unresolved_graph_requirements_provenance=source_fragment_projection.source_unresolved_graph_requirements_provenance,
        unresolved_classical_semantic_requirements=source_fragment_projection.unresolved_classical_semantic_requirements,
    )


def _source_record_sets(
    source_semantic_envelope: Any,
    fragment_governance: tuple[ClassicalFragmentMechanismClosureGovernanceProjection, ...],
) -> tuple[SourceRecordMechanismClosureGovernanceSet, ...]:
    by_fragment = {row.source_fragment_id: row for row in fragment_governance}
    if len(by_fragment) != len(fragment_governance):
        raise BaziClassicalSemanticMechanismClosureGovernanceError(
            "DUPLICATE_UNIT5_FRAGMENT_SOURCE_ID",
            str(len(fragment_governance)),
        )
    rows = []
    for source_set in source_semantic_envelope.source_record_candidate_sets:
        if any(value != "NOT_RELEASED" for value in (
            source_set.member_selection_semantics,
            source_set.member_coexistence_semantics,
            source_set.member_exclusivity_semantics,
            source_set.semantic_candidate_priority_semantics,
            source_set.semantic_candidate_conflict_semantics,
        )):
            raise BaziClassicalSemanticMechanismClosureGovernanceError(
                "UPSTREAM_UNIT4_SOURCE_RECORD_SET_SEMANTICS_OVERRESOLVED",
                source_set.source_record_candidate_set_id,
            )
        fragments = tuple(by_fragment[fragment_id] for fragment_id in source_set.source_fragment_ids)
        rows.append(SourceRecordMechanismClosureGovernanceSet(
            source_record_candidate_set_id=source_set.source_record_candidate_set_id,
            source_layer=source_set.source_layer,
            source_occurrence_id=source_set.source_occurrence_id,
            source_fragment_ids=source_set.source_fragment_ids,
            fragment_governance_projection_ids=tuple(
                row.fragment_governance_projection_id for row in fragments
            ),
            mechanism_proposal_ids=tuple(
                proposal.mechanism_proposal_id
                for row in fragments
                for proposal in row.mechanism_proposals
            ),
        ))
    return tuple(rows)


def _closure_requirement_index(
    fragment_governance: tuple[ClassicalFragmentMechanismClosureGovernanceProjection, ...],
) -> tuple[ClosureRequirementGovernanceIndexEntry, ...]:
    grouped: dict[tuple[str, str], list[str]] = {}
    for fragment in fragment_governance:
        for proposal in fragment.mechanism_proposals:
            for row in proposal.closure_governance_rows:
                grouped.setdefault(
                    (row.closure_requirement_id, row.runtime_dependency_status), []
                ).append(proposal.mechanism_proposal_id)
    return tuple(
        ClosureRequirementGovernanceIndexEntry(
            closure_requirement_id=requirement_id,
            runtime_dependency_status=status,
            mechanism_proposal_ids=_unique_strings(proposal_ids),
        )
        for (requirement_id, status), proposal_ids in sorted(grouped.items())
    )


def _mechanism_proposal_index(
    fragment_governance: tuple[ClassicalFragmentMechanismClosureGovernanceProjection, ...],
) -> tuple[MechanismProposalGovernanceIndexEntry, ...]:
    grouped: dict[str, list[str]] = {}
    for fragment in fragment_governance:
        for proposal in fragment.mechanism_proposals:
            grouped.setdefault(proposal.mechanism_proposal_kind, []).append(
                proposal.mechanism_proposal_id
            )
    return tuple(
        MechanismProposalGovernanceIndexEntry(
            mechanism_proposal_kind=kind,
            mechanism_proposal_ids=tuple(proposal_ids),
        )
        for kind, proposal_ids in sorted(grouped.items())
    )


def _project_envelope(
    source_semantic_envelope: Any,
    admission_envelope: Any,
    effect_envelope: Any,
    profile: ClassicalSemanticMechanismClosureGovernanceProfile,
) -> ClassicalSemanticMechanismClosureGovernanceEnvelope:
    if not replay_unit4_semantic_envelope(
        source_semantic_envelope,
        admission_envelope,
        effect_envelope,
    ):
        raise BaziClassicalSemanticMechanismClosureGovernanceError(
            "UPSTREAM_UNIT4_SEMANTIC_ENVELOPE_REPLAY_MISMATCH",
            source_semantic_envelope.semantic_projection_envelope_id,
        )
    fragment_governance = tuple(
        project_fragment_governance(
            source_semantic_envelope,
            fragment,
            profile,
        )
        for fragment in source_semantic_envelope.fragment_projections
    )
    source_record_sets = _source_record_sets(source_semantic_envelope, fragment_governance)
    requirement_index = _closure_requirement_index(fragment_governance)
    mechanism_index = _mechanism_proposal_index(fragment_governance)
    proposal_ids = tuple(
        proposal.mechanism_proposal_id
        for fragment in fragment_governance
        for proposal in fragment.mechanism_proposals
    )
    lineage_binding_keys = (
        *source_semantic_envelope.lineage_binding_keys,
        f"SOURCE_SEMANTIC_PROJECTION_FACT:{source_semantic_envelope.hashes.fact_hash}",
        f"SOURCE_SEMANTIC_PROJECTION_COMPUTATION:{source_semantic_envelope.hashes.computation_hash}",
        f"MECHANISM_CLOSURE_PROFILE:{profile.profile_id}:{profile.profile_version}",
    )
    hashes = mechanism_closure_hash_bundle(
        source_semantic_envelope,
        fragment_governance,
        source_record_sets,
        requirement_index,
        mechanism_index,
        proposal_ids,
        lineage_binding_keys,
        profile,
    )
    integrity = validate_mechanism_closure_envelope(
        source_semantic_envelope,
        admission_envelope,
        effect_envelope,
        fragment_governance,
        source_record_sets,
        requirement_index,
        mechanism_index,
        proposal_ids,
        lineage_binding_keys,
        profile,
        hashes,
    )
    if integrity.status != "PASS":
        raise BaziClassicalSemanticMechanismClosureGovernanceError(
            "MECHANISM_CLOSURE_GOVERNANCE_INTEGRITY_FAILED",
            ";".join(f"{row.code}:{row.path}" for row in integrity.diagnostics),
        )
    envelope_id = "CLASSICAL_SEMANTIC_MECHANISM_CLOSURE_ENVELOPE:" + object_sha256({
        "source_semantic_projection_envelope_id": source_semantic_envelope.semantic_projection_envelope_id,
        "source_semantic_projection_fact_hash": source_semantic_envelope.hashes.fact_hash,
        "fact_hash": hashes.fact_hash,
    })
    return ClassicalSemanticMechanismClosureGovernanceEnvelope(
        mechanism_closure_envelope_id=envelope_id,
        source_semantic_projection_envelope_id=source_semantic_envelope.semantic_projection_envelope_id,
        source_semantic_projection_fact_hash=source_semantic_envelope.hashes.fact_hash,
        source_semantic_projection_computation_hash=source_semantic_envelope.hashes.computation_hash,
        source_admission_envelope_id=source_semantic_envelope.source_admission_envelope_id,
        source_effect_envelope_id=source_semantic_envelope.source_effect_envelope_id,
        lineage_binding_keys=lineage_binding_keys,
        fragment_governance_projections=fragment_governance,
        source_record_candidate_sets=source_record_sets,
        closure_requirement_index=requirement_index,
        mechanism_proposal_index=mechanism_index,
        projected_mechanism_proposal_ids=proposal_ids,
        mechanism_proposal_semantics=profile.mechanism_proposal_semantics,
        mechanism_execution_semantics=profile.mechanism_execution_semantics,
        rewrite_application_semantics=profile.rewrite_application_semantics,
        candidate_truth_semantics=profile.candidate_truth_semantics,
        candidate_applicability_semantics=profile.candidate_applicability_semantics,
        candidate_coexistence_semantics=profile.candidate_coexistence_semantics,
        candidate_exclusivity_semantics=profile.candidate_exclusivity_semantics,
        candidate_conflict_semantics=profile.candidate_conflict_semantics,
        precedence_semantics=profile.precedence_semantics,
        priority_semantics=profile.priority_semantics,
        winner_loser_semantics=profile.winner_loser_semantics,
        state_transition_semantics=profile.state_transition_semantics,
        lifecycle_truth_gate=profile.lifecycle_truth_gate,
        fragment_selection_semantics=profile.fragment_selection_semantics,
        cross_outer_composition=profile.cross_outer_composition,
        cartesian_expansion=profile.cartesian_expansion,
        raw_relation_immutability_contract=profile.raw_relation_immutability_contract,
        algorithm_versions={"mechanism_closure_governance": profile.algorithm_version},
        integrity=integrity,
        hashes=hashes,
    )


class BaziClassicalSemanticMechanismClosureGovernanceEngine:
    schema = "BAZI-CLASSICAL-SEMANTIC-MECHANISM-CLOSURE-GOVERNANCE-RESULT-R1"
    typed_schema = "BAZI-CLASSICAL-SEMANTIC-MECHANISM-CLOSURE-GOVERNANCE-TYPED-RESOLUTION-R1"

    def resolve_typed(
        self,
        request: BaziClassicalSemanticMechanismClosureGovernanceRequest,
    ) -> BaziClassicalSemanticMechanismClosureGovernanceResolution:
        try:
            profile = request.mechanism_closure_profile.validate()
            if request.source_effect_constraint_resolution.status not in {"RESOLVED", "MULTI_CANDIDATE"}:
                raise BaziClassicalSemanticMechanismClosureGovernanceError(
                    "UPSTREAM_EFFECT_RESOLUTION_NOT_RESOLVED",
                    request.source_effect_constraint_resolution.status,
                )
            if request.source_resolver_admission_resolution.status not in {"RESOLVED", "MULTI_CANDIDATE"}:
                raise BaziClassicalSemanticMechanismClosureGovernanceError(
                    "UPSTREAM_ADMISSION_RESOLUTION_NOT_RESOLVED",
                    request.source_resolver_admission_resolution.status,
                )
            if request.source_semantic_candidate_resolution.status not in {"RESOLVED", "MULTI_CANDIDATE"}:
                raise BaziClassicalSemanticMechanismClosureGovernanceError(
                    "UPSTREAM_SEMANTIC_CANDIDATE_RESOLUTION_NOT_RESOLVED",
                    request.source_semantic_candidate_resolution.status,
                )

            rows = []
            seen_lineages: set[tuple[str, str]] = set()
            for source_semantic_envelope in request.source_semantic_candidate_resolution.candidates:
                lineage = (
                    source_semantic_envelope.hashes.fact_hash,
                    source_semantic_envelope.hashes.computation_hash,
                )
                if lineage in seen_lineages:
                    raise BaziClassicalSemanticMechanismClosureGovernanceError(
                        "UPSTREAM_UNIT4_OUTER_LINEAGE_PROJECTED_MORE_THAN_ONCE",
                        f"{lineage[0]}:{lineage[1]}",
                    )
                seen_lineages.add(lineage)
                admission_envelope = match_admission_envelope(
                    source_semantic_envelope,
                    request.source_resolver_admission_resolution,
                )
                effect_envelope = match_effect_envelope(
                    source_semantic_envelope,
                    request.source_effect_constraint_resolution,
                )
                rows.append(_project_envelope(
                    source_semantic_envelope,
                    admission_envelope,
                    effect_envelope,
                    profile,
                ))
            candidates = tuple(rows)
            return BaziClassicalSemanticMechanismClosureGovernanceResolution(
                schema=self.typed_schema,
                status="RESOLVED" if len(candidates) == 1 else "MULTI_CANDIDATE",
                candidates=candidates,
                events=("AMBIGUOUS_UPSTREAM_LINEAGES_PRESERVED",) if len(candidates) > 1 else (),
                diagnostics=(),
            )
        except (
            BaziClassicalSemanticMechanismClosureGovernanceError,
            KeyError,
            ValueError,
        ) as exc:
            code = getattr(
                exc,
                "diagnostic_code",
                "CLASSICAL_SEMANTIC_MECHANISM_CLOSURE_GOVERNANCE_FAILED",
            )
            return BaziClassicalSemanticMechanismClosureGovernanceResolution(
                self.typed_schema,
                "FAILED",
                (),
                (),
                (f"{code}:{exc}",),
            )

    def resolve(self, request: BaziClassicalSemanticMechanismClosureGovernanceRequest) -> dict[str, Any]:
        typed = self.resolve_typed(request)
        return {
            "schema": self.schema,
            "typed_schema": typed.schema,
            "status": typed.status,
            "mechanism_closure_profile": json_value(request.mechanism_closure_profile),
            "candidates": json_value(typed.candidates),
            "events": list(typed.events),
            "diagnostics": list(typed.diagnostics),
        }
