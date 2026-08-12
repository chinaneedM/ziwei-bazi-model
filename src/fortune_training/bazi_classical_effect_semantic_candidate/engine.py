from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fortune_training.bazi_classical_effect_constraint_graph.models import (
    BaziClassicalEffectConstraintGraphResolution,
)
from fortune_training.bazi_classical_resolver_admission.models import (
    BaziClassicalResolverAdmissionResolution,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .integrity import (
    match_effect_envelope,
    replay_admission_envelope_against_effect,
    semantic_projection_hash_bundle,
    validate_semantic_projection_envelope,
)
from .models import (
    BaziClassicalEffectSemanticCandidateProjectionResolution,
    ClassicalEffectSemanticCandidate,
    ClassicalEffectSemanticCandidateProjectionEnvelope,
    ClassicalFragmentSemanticCandidateProjection,
    ExactEffectChannelSemanticCandidateIndexEntry,
    SourceRecordSemanticCandidateSet,
)
from .profile import (
    SOURCE_CLAIM_TO_SEMANTIC_CANDIDATE,
    ClassicalEffectSemanticCandidateProjectionProfile,
)


class BaziClassicalEffectSemanticCandidateProjectionError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class BaziClassicalEffectSemanticCandidateProjectionRequest:
    source_effect_constraint_resolution: BaziClassicalEffectConstraintGraphResolution
    source_resolver_admission_resolution: BaziClassicalResolverAdmissionResolution
    semantic_candidate_profile: ClassicalEffectSemanticCandidateProjectionProfile


def _unique_strings(rows: list[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(rows))


def _semantic_candidate(
    source_admission_envelope: Any,
    admission_projection: Any,
    effect_fragment: Any,
    constraint: Any,
    profile: ClassicalEffectSemanticCandidateProjectionProfile,
) -> ClassicalEffectSemanticCandidate:
    mapping = SOURCE_CLAIM_TO_SEMANTIC_CANDIDATE.get(constraint.source_claim_edge_class)
    if mapping is None:
        raise BaziClassicalEffectSemanticCandidateProjectionError(
            "UNIT2_SOURCE_CLAIM_CLASS_NOT_RELEASED_FOR_UNIT4",
            constraint.source_claim_edge_class,
        )
    expected_facet, candidate_kind = mapping
    if constraint.effect_facet != expected_facet:
        raise BaziClassicalEffectSemanticCandidateProjectionError(
            "UNIT2_CLAIM_FACET_MAPPING_MISMATCH",
            f"{constraint.source_claim_edge_id}:{constraint.effect_facet}:{expected_facet}",
        )
    if constraint.source_claim_edge_class == "SOURCE_ASSERTED_PARTICIPANT_ALLOCATION":
        if not constraint.multiplicity_references:
            raise BaziClassicalEffectSemanticCandidateProjectionError(
                "ALLOCATION_CANDIDATE_WITHOUT_UPSTREAM_MULTIPLICITY",
                constraint.source_claim_edge_id,
            )
        if any(
            row.alternative_path_requirement != "PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS"
            for row in constraint.multiplicity_references
        ):
            raise BaziClassicalEffectSemanticCandidateProjectionError(
                "ALLOCATION_PATH_PRESERVATION_CONTRACT_MISMATCH",
                constraint.source_claim_edge_id,
            )
    elif constraint.multiplicity_references:
        raise BaziClassicalEffectSemanticCandidateProjectionError(
            "NON_ALLOCATION_CANDIDATE_HAS_MULTIPLICITY_REFERENCE",
            constraint.source_claim_edge_id,
        )

    semantic_candidate_id = "CLASSICAL_EFFECT_SEMANTIC_CANDIDATE:" + object_sha256({
        "source_admission_projection_id": admission_projection.admission_projection_id,
        "source_fragment_id": effect_fragment.fragment_id,
        "source_effect_constraint_id": constraint.effect_constraint_id,
        "semantic_candidate_kind": candidate_kind,
        "effect_facet": constraint.effect_facet,
    })
    return ClassicalEffectSemanticCandidate(
        semantic_candidate_id=semantic_candidate_id,
        source_admission_projection_id=admission_projection.admission_projection_id,
        source_effect_envelope_id=source_admission_envelope.source_effect_envelope_id,
        source_effect_envelope_fact_hash=source_admission_envelope.source_effect_fact_hash,
        source_effect_envelope_computation_hash=source_admission_envelope.source_effect_computation_hash,
        source_fragment_id=effect_fragment.fragment_id,
        source_fragment_fact_hash=effect_fragment.hashes.fact_hash,
        source_fragment_computation_hash=effect_fragment.hashes.computation_hash,
        source_effect_constraint_id=constraint.effect_constraint_id,
        binding_candidate_id=constraint.binding_candidate_id,
        source_occurrence_id=constraint.source_occurrence_id,
        graph_record_id=constraint.graph_record_id,
        interaction_assertion_id=constraint.interaction_assertion_id,
        source_claim_edge_id=constraint.source_claim_edge_id,
        source_claim_edge_class=constraint.source_claim_edge_class,
        source_assertion_class=constraint.source_assertion_class,
        source_evidence_mode=constraint.source_evidence_mode,
        exact_source_fragments=constraint.exact_source_fragments,
        target_effect_channel_id=constraint.target_effect_channel_id,
        target_exact_relation_id=constraint.target_exact_relation_id,
        actor_exact_relation_ids=constraint.actor_exact_relation_ids,
        actor_exact_participant_ids=constraint.actor_exact_participant_ids,
        context_exact_participant_ids=constraint.context_exact_participant_ids,
        effect_facet=constraint.effect_facet,
        semantic_candidate_kind=candidate_kind,
        multiplicity_references=constraint.multiplicity_references,
        source_narrative_chain_ids=constraint.source_narrative_chain_ids,
        unresolved_classical_semantic_requirements=constraint.unresolved_classical_semantic_requirements,
        source_unresolved_graph_requirements_provenance=constraint.source_unresolved_graph_requirements,
        source_semantic_profile_id=admission_projection.source_semantic_profile_id,
        source_semantic_partition_id=admission_projection.source_semantic_partition_id,
        candidate_truth_semantics=profile.candidate_truth_semantics,
        candidate_applicability_semantics=profile.candidate_applicability_semantics,
    )


def project_fragment_semantic_candidates(
    source_admission_envelope: Any,
    admission_projection: Any,
    effect_fragment: Any,
    profile: ClassicalEffectSemanticCandidateProjectionProfile,
) -> ClassicalFragmentSemanticCandidateProjection:
    if admission_projection.source_fragment_id != effect_fragment.fragment_id:
        raise BaziClassicalEffectSemanticCandidateProjectionError(
            "ADMISSION_EFFECT_FRAGMENT_ID_MISMATCH", effect_fragment.fragment_id
        )
    if (
        admission_projection.source_fragment_fact_hash != effect_fragment.hashes.fact_hash
        or admission_projection.source_fragment_computation_hash != effect_fragment.hashes.computation_hash
        or admission_projection.binding_candidate_id != effect_fragment.binding_candidate_id
        or admission_projection.source_occurrence_id != effect_fragment.source_occurrence_id
    ):
        raise BaziClassicalEffectSemanticCandidateProjectionError(
            "ADMISSION_EFFECT_FRAGMENT_REPLAY_MISMATCH", effect_fragment.fragment_id
        )

    if admission_projection.admission_status == "ADMITTED":
        candidates = tuple(
            _semantic_candidate(
                source_admission_envelope,
                admission_projection,
                effect_fragment,
                node.constraint,
                profile,
            )
            for node in effect_fragment.effect_constraint_nodes
        )
        projection_status = "SEMANTIC_CANDIDATES_PROJECTED"
    elif admission_projection.admission_status == "PRESERVED_NOT_ADMITTED":
        candidates = ()
        projection_status = "PRESERVED_NO_SEMANTIC_CANDIDATES"
    elif admission_projection.admission_status == "PRESERVED_OUTSIDE_PROFILE":
        candidates = ()
        projection_status = "PRESERVED_OUTSIDE_PROFILE_NO_SEMANTIC_CANDIDATES"
    else:
        raise BaziClassicalEffectSemanticCandidateProjectionError(
            "UNKNOWN_UNIT3_ADMISSION_STATUS", admission_projection.admission_status
        )

    unresolved = _unique_strings([
        requirement
        for node in effect_fragment.effect_constraint_nodes
        for requirement in node.constraint.unresolved_classical_semantic_requirements
    ])
    projection_id = "CLASSICAL_FRAGMENT_SEMANTIC_CANDIDATE_PROJECTION:" + object_sha256({
        "source_admission_projection_id": admission_projection.admission_projection_id,
        "source_fragment_id": effect_fragment.fragment_id,
        "admission_status": admission_projection.admission_status,
        "projection_status": projection_status,
        "semantic_candidate_ids": tuple(row.semantic_candidate_id for row in candidates),
    })
    return ClassicalFragmentSemanticCandidateProjection(
        fragment_semantic_projection_id=projection_id,
        source_admission_projection_id=admission_projection.admission_projection_id,
        source_fragment_id=effect_fragment.fragment_id,
        source_fragment_fact_hash=effect_fragment.hashes.fact_hash,
        source_fragment_computation_hash=effect_fragment.hashes.computation_hash,
        source_occurrence_id=effect_fragment.source_occurrence_id,
        binding_candidate_id=effect_fragment.binding_candidate_id,
        admission_status=admission_projection.admission_status,
        admission_blocker_ids=admission_projection.admission_blocker_ids,
        source_semantic_profile_id=admission_projection.source_semantic_profile_id,
        source_semantic_partition_id=admission_projection.source_semantic_partition_id,
        projection_status=projection_status,
        semantic_candidates=candidates,
        source_unresolved_graph_requirements_provenance=effect_fragment.source_unresolved_graph_requirements,
        unresolved_classical_semantic_requirements=unresolved,
    )


def _source_record_sets(
    source_admission_envelope: Any,
    fragment_projections: tuple[ClassicalFragmentSemanticCandidateProjection, ...],
) -> tuple[SourceRecordSemanticCandidateSet, ...]:
    by_fragment = {row.source_fragment_id: row for row in fragment_projections}
    if len(by_fragment) != len(fragment_projections):
        raise BaziClassicalEffectSemanticCandidateProjectionError(
            "FRAGMENT_SEMANTIC_PROJECTION_ID_DUPLICATE", str(len(fragment_projections))
        )
    rows = []
    for source_set in source_admission_envelope.source_record_candidate_sets:
        if any(value != "NOT_RELEASED" for value in (
            source_set.member_selection_semantics,
            source_set.member_coexistence_semantics,
            source_set.member_exclusivity_semantics,
        )):
            raise BaziClassicalEffectSemanticCandidateProjectionError(
                "UPSTREAM_SOURCE_RECORD_SET_SEMANTICS_OVERRESOLVED",
                source_set.source_record_candidate_set_id,
            )
        projections = tuple(by_fragment[fragment_id] for fragment_id in source_set.source_fragment_ids)
        rows.append(SourceRecordSemanticCandidateSet(
            source_record_candidate_set_id=source_set.source_record_candidate_set_id,
            source_layer=source_set.source_layer,
            source_occurrence_id=source_set.source_occurrence_id,
            source_fragment_ids=source_set.source_fragment_ids,
            fragment_semantic_projection_ids=tuple(row.fragment_semantic_projection_id for row in projections),
            semantic_candidate_ids=tuple(
                candidate.semantic_candidate_id
                for row in projections
                for candidate in row.semantic_candidates
            ),
        ))
    return tuple(rows)


def _effect_channel_index(
    fragment_projections: tuple[ClassicalFragmentSemanticCandidateProjection, ...],
) -> tuple[ExactEffectChannelSemanticCandidateIndexEntry, ...]:
    grouped: dict[tuple[str, str], list[tuple[str, str]]] = {}
    for projection in fragment_projections:
        for candidate in projection.semantic_candidates:
            grouped.setdefault(
                (candidate.target_exact_relation_id, candidate.effect_facet), []
            ).append((projection.source_fragment_id, candidate.semantic_candidate_id))
    rows = []
    for (relation_id, facet), members in sorted(grouped.items()):
        rows.append(ExactEffectChannelSemanticCandidateIndexEntry(
            target_exact_relation_id=relation_id,
            effect_facet=facet,
            source_fragment_ids=_unique_strings([row[0] for row in members]),
            semantic_candidate_ids=tuple(row[1] for row in members),
        ))
    return tuple(rows)


def _project_envelope(
    source_admission_envelope: Any,
    source_effect_envelope: Any,
    profile: ClassicalEffectSemanticCandidateProjectionProfile,
) -> ClassicalEffectSemanticCandidateProjectionEnvelope:
    if not replay_admission_envelope_against_effect(source_admission_envelope, source_effect_envelope):
        raise BaziClassicalEffectSemanticCandidateProjectionError(
            "UPSTREAM_ADMISSION_ENVELOPE_REPLAY_MISMATCH",
            source_admission_envelope.admission_envelope_id,
        )
    admission_by_fragment = {
        row.source_fragment_id: row for row in source_admission_envelope.fragment_admissions
    }
    if len(admission_by_fragment) != len(source_admission_envelope.fragment_admissions):
        raise BaziClassicalEffectSemanticCandidateProjectionError(
            "UPSTREAM_ADMISSION_FRAGMENT_ID_DUPLICATE", str(len(admission_by_fragment))
        )
    fragment_projections = tuple(
        project_fragment_semantic_candidates(
            source_admission_envelope,
            admission_by_fragment[fragment.fragment_id],
            fragment,
            profile,
        )
        for fragment in source_effect_envelope.fragments
    )
    record_sets = _source_record_sets(source_admission_envelope, fragment_projections)
    channel_index = _effect_channel_index(fragment_projections)
    projected_candidate_ids = tuple(
        candidate.semantic_candidate_id
        for row in fragment_projections
        for candidate in row.semantic_candidates
    )
    lineage_binding_keys = (
        *source_admission_envelope.lineage_binding_keys,
        f"SOURCE_ADMISSION_FACT:{source_admission_envelope.hashes.fact_hash}",
        f"SOURCE_ADMISSION_COMPUTATION:{source_admission_envelope.hashes.computation_hash}",
        f"SEMANTIC_CANDIDATE_PROFILE:{profile.profile_id}:{profile.profile_version}",
    )
    hashes = semantic_projection_hash_bundle(
        source_admission_envelope,
        source_effect_envelope,
        fragment_projections,
        record_sets,
        channel_index,
        projected_candidate_ids,
        lineage_binding_keys,
        profile,
    )
    integrity = validate_semantic_projection_envelope(
        source_admission_envelope,
        source_effect_envelope,
        fragment_projections,
        record_sets,
        channel_index,
        projected_candidate_ids,
        lineage_binding_keys,
        profile,
        hashes,
    )
    if integrity.status != "PASS":
        raise BaziClassicalEffectSemanticCandidateProjectionError(
            "SEMANTIC_CANDIDATE_PROJECTION_INTEGRITY_FAILED",
            ";".join(f"{row.code}:{row.path}" for row in integrity.diagnostics),
        )
    envelope_id = "CLASSICAL_EFFECT_SEMANTIC_CANDIDATE_ENVELOPE:" + object_sha256({
        "source_admission_envelope_id": source_admission_envelope.admission_envelope_id,
        "source_admission_fact_hash": source_admission_envelope.hashes.fact_hash,
        "fact_hash": hashes.fact_hash,
    })
    return ClassicalEffectSemanticCandidateProjectionEnvelope(
        semantic_projection_envelope_id=envelope_id,
        source_admission_envelope_id=source_admission_envelope.admission_envelope_id,
        source_admission_fact_hash=source_admission_envelope.hashes.fact_hash,
        source_admission_computation_hash=source_admission_envelope.hashes.computation_hash,
        source_effect_envelope_id=source_effect_envelope.envelope_id,
        source_effect_fact_hash=source_effect_envelope.hashes.fact_hash,
        source_effect_computation_hash=source_effect_envelope.hashes.computation_hash,
        lineage_binding_keys=lineage_binding_keys,
        fragment_projections=fragment_projections,
        source_record_candidate_sets=record_sets,
        effect_channel_candidate_index=channel_index,
        projected_semantic_candidate_ids=projected_candidate_ids,
        fragment_selection_semantics=profile.fragment_selection_semantics,
        cross_outer_composition=profile.cross_outer_composition,
        cartesian_expansion=profile.cartesian_expansion,
        raw_relation_immutability_contract=profile.raw_relation_immutability_contract,
        candidate_truth_semantics=profile.candidate_truth_semantics,
        candidate_coexistence_semantics=profile.candidate_coexistence_semantics,
        candidate_exclusivity_semantics=profile.candidate_exclusivity_semantics,
        candidate_priority_semantics=profile.candidate_priority_semantics,
        candidate_conflict_semantics=profile.candidate_conflict_semantics,
        candidate_rewrite_semantics=profile.candidate_rewrite_semantics,
        candidate_state_transition_semantics=profile.candidate_state_transition_semantics,
        candidate_winner_loser_semantics=profile.candidate_winner_loser_semantics,
        algorithm_versions={"semantic_candidate_projection": profile.algorithm_version},
        integrity=integrity,
        hashes=hashes,
    )


class BaziClassicalEffectSemanticCandidateProjectionEngine:
    schema = "BAZI-CLASSICAL-EFFECT-SEMANTIC-CANDIDATE-PROJECTION-RESULT-R1"
    typed_schema = "BAZI-CLASSICAL-EFFECT-SEMANTIC-CANDIDATE-PROJECTION-TYPED-RESOLUTION-R1"

    def resolve_typed(
        self,
        request: BaziClassicalEffectSemanticCandidateProjectionRequest,
    ) -> BaziClassicalEffectSemanticCandidateProjectionResolution:
        try:
            profile = request.semantic_candidate_profile.validate()
            if request.source_effect_constraint_resolution.status not in {"RESOLVED", "MULTI_CANDIDATE"}:
                raise BaziClassicalEffectSemanticCandidateProjectionError(
                    "UPSTREAM_EFFECT_RESOLUTION_NOT_RESOLVED",
                    request.source_effect_constraint_resolution.status,
                )
            if request.source_resolver_admission_resolution.status not in {"RESOLVED", "MULTI_CANDIDATE"}:
                raise BaziClassicalEffectSemanticCandidateProjectionError(
                    "UPSTREAM_ADMISSION_RESOLUTION_NOT_RESOLVED",
                    request.source_resolver_admission_resolution.status,
                )
            rows = []
            seen_admission_lineages: set[tuple[str, str]] = set()
            for admission_envelope in request.source_resolver_admission_resolution.candidates:
                lineage = (admission_envelope.hashes.fact_hash, admission_envelope.hashes.computation_hash)
                if lineage in seen_admission_lineages:
                    raise BaziClassicalEffectSemanticCandidateProjectionError(
                        "UPSTREAM_ADMISSION_OUTER_LINEAGE_PROJECTED_MORE_THAN_ONCE",
                        f"{lineage[0]}:{lineage[1]}",
                    )
                seen_admission_lineages.add(lineage)
                effect_envelope = match_effect_envelope(
                    admission_envelope,
                    request.source_effect_constraint_resolution,
                )
                rows.append(_project_envelope(admission_envelope, effect_envelope, profile))
            candidates = tuple(rows)
            return BaziClassicalEffectSemanticCandidateProjectionResolution(
                schema=self.typed_schema,
                status="RESOLVED" if len(candidates) == 1 else "MULTI_CANDIDATE",
                candidates=candidates,
                events=("AMBIGUOUS_UPSTREAM_LINEAGES_PRESERVED",) if len(candidates) > 1 else (),
                diagnostics=(),
            )
        except (
            BaziClassicalEffectSemanticCandidateProjectionError,
            KeyError,
            ValueError,
        ) as exc:
            code = getattr(exc, "diagnostic_code", "CLASSICAL_EFFECT_SEMANTIC_CANDIDATE_PROJECTION_FAILED")
            return BaziClassicalEffectSemanticCandidateProjectionResolution(
                self.typed_schema,
                "FAILED",
                (),
                (),
                (f"{code}:{exc}",),
            )

    def resolve(self, request: BaziClassicalEffectSemanticCandidateProjectionRequest) -> dict[str, Any]:
        typed = self.resolve_typed(request)
        return {
            "schema": self.schema,
            "typed_schema": typed.schema,
            "status": typed.status,
            "semantic_candidate_profile": json_value(request.semantic_candidate_profile),
            "candidates": json_value(typed.candidates),
            "events": list(typed.events),
            "diagnostics": list(typed.diagnostics),
        }
