from __future__ import annotations

from typing import Any

from fortune_training.bazi_classical_final_effect_candidate_envelope.engine import (
    BaziClassicalFinalEffectCandidateEnvelopeEngine,
    BaziClassicalFinalEffectCandidateEnvelopeRequest,
)
from fortune_training.bazi_classical_final_effect_candidate_envelope.profile import (
    bazi_classical_final_effect_candidate_envelope_r1_profile,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .models import (
    CandidateLocalReversalReappearanceEffectDisposition,
    EffectChannelReversalReappearanceDispositionIndexEntry,
    LocalReversalReappearanceClosureResolutionIndexEntry,
    ReversalReappearanceClosureResolutionRow,
    ReversalReappearanceEffectCandidateProjection,
    ReversalReappearanceEffectDispositionHashBundle,
    ReversalReappearanceEffectDispositionIntegrityDiagnostic,
    ReversalReappearanceEffectDispositionIntegrityReport,
    ReversalReappearanceEffectFragmentProjection,
    SourceOccurrenceReversalReappearanceDispositionIndexEntry,
    SourceRecordReversalReappearanceEffectCandidateSet,
)
from .profile import (
    CANDIDATE_PROJECTION_STATUSES,
    DISPOSITION_KIND,
    DISPOSITION_SEMANTIC_SCOPE,
    EXPECTED_UPSTREAM_CLOSURE_STATUS,
    HANDLED_EFFECT_FACET,
    HANDLED_MECHANISM_PROPOSAL_KIND,
    HANDLED_SEMANTIC_CANDIDATE_KIND,
    HANDLED_SOURCE_CLAIM_EDGE_CLASS,
    INDEX_SEMANTICS,
    LOCAL_CLOSURE_RESULT,
    REVERSAL_REAPPEARANCE_CLOSURE_REQUIREMENT_ID,
    SOURCE_ASSERTED_DISPOSITION,
    SOURCE_ASSERTION_SUBTYPE_SPLIT,
    ClassicalReversalReappearanceEffectDispositionProfile,
)


def replay_unit7_resolution(
    source_effect_constraint_resolution: Any,
    source_resolver_admission_resolution: Any,
    source_semantic_candidate_resolution: Any,
    source_mechanism_closure_resolution: Any,
    source_allocation_resolution: Any,
    source_final_effect_resolution: Any,
) -> bool:
    expected = BaziClassicalFinalEffectCandidateEnvelopeEngine().resolve_typed(
        BaziClassicalFinalEffectCandidateEnvelopeRequest(
            source_effect_constraint_resolution=source_effect_constraint_resolution,
            source_resolver_admission_resolution=source_resolver_admission_resolution,
            source_semantic_candidate_resolution=source_semantic_candidate_resolution,
            source_mechanism_closure_resolution=source_mechanism_closure_resolution,
            source_allocation_resolution=source_allocation_resolution,
            final_effect_profile=bazi_classical_final_effect_candidate_envelope_r1_profile(),
        )
    )
    return expected == source_final_effect_resolution


def _reversal_reappearance_closure_row(candidate: Any) -> Any:
    matches = tuple(
        row
        for row in candidate.closure_governance_rows
        if row.closure_requirement_id
        == REVERSAL_REAPPEARANCE_CLOSURE_REQUIREMENT_ID
    )
    if len(matches) != 1:
        raise ValueError(
            "REVERSAL_REAPPEARANCE_CLOSURE_ROW_CARDINALITY_MISMATCH:"
            f"{candidate.final_candidate_id}:{len(matches)}"
        )
    row = matches[0]
    if row.runtime_dependency_status != EXPECTED_UPSTREAM_CLOSURE_STATUS:
        raise ValueError(
            "REVERSAL_REAPPEARANCE_CLOSURE_UPSTREAM_STATUS_MISMATCH:"
            f"{candidate.final_candidate_id}:{row.runtime_dependency_status}"
        )
    if (
        REVERSAL_REAPPEARANCE_CLOSURE_REQUIREMENT_ID
        not in candidate.unresolved_classical_semantic_requirements
    ):
        raise ValueError(
            "REVERSAL_REAPPEARANCE_CLOSURE_REQUIREMENT_NOT_DECLARED:"
            f"{candidate.final_candidate_id}"
        )
    return row


def candidate_is_handled_reversal_reappearance(candidate: Any) -> bool:
    if candidate.semantic_candidate_kind != HANDLED_SEMANTIC_CANDIDATE_KIND:
        return False
    if candidate.mechanism_proposal_kind != HANDLED_MECHANISM_PROPOSAL_KIND:
        raise ValueError(
            "REVERSAL_REAPPEARANCE_MECHANISM_PROPOSAL_KIND_MISMATCH:"
            f"{candidate.final_candidate_id}"
        )
    if candidate.source_claim_edge_class != HANDLED_SOURCE_CLAIM_EDGE_CLASS:
        raise ValueError(
            "REVERSAL_REAPPEARANCE_SOURCE_CLAIM_EDGE_CLASS_MISMATCH:"
            f"{candidate.final_candidate_id}"
        )
    if candidate.effect_facet != HANDLED_EFFECT_FACET:
        raise ValueError(
            "REVERSAL_REAPPEARANCE_EFFECT_FACET_MISMATCH:"
            f"{candidate.final_candidate_id}"
        )
    _reversal_reappearance_closure_row(candidate)
    return True


def reversal_reappearance_effect_disposition_id(candidate: Any) -> str:
    return "CLASSICAL_REVERSAL_REAPPEARANCE_EFFECT_DISPOSITION:" + object_sha256({
        "source_final_candidate_id": candidate.final_candidate_id,
        "source_claim_edge_id": candidate.source_claim_edge_id,
        "target_effect_channel_id": candidate.target_effect_channel_id,
        "target_exact_relation_id": candidate.target_exact_relation_id,
        "effect_facet": candidate.effect_facet,
        "disposition_kind": DISPOSITION_KIND,
        "semantic_scope": DISPOSITION_SEMANTIC_SCOPE,
        "source_asserted_disposition": SOURCE_ASSERTED_DISPOSITION,
        "source_assertion_subtype_split": SOURCE_ASSERTION_SUBTYPE_SPLIT,
    })


def expected_candidate_projection(
    candidate: Any,
    profile: ClassicalReversalReappearanceEffectDispositionProfile,
) -> ReversalReappearanceEffectCandidateProjection:
    handled = candidate_is_handled_reversal_reappearance(candidate)
    closure_rows: tuple[ReversalReappearanceClosureResolutionRow, ...] = ()
    dispositions: tuple[CandidateLocalReversalReappearanceEffectDisposition, ...] = ()
    if handled:
        _reversal_reappearance_closure_row(candidate)
        closure_rows = (
            ReversalReappearanceClosureResolutionRow(
                closure_requirement_id=REVERSAL_REAPPEARANCE_CLOSURE_REQUIREMENT_ID,
                upstream_runtime_dependency_status=EXPECTED_UPSTREAM_CLOSURE_STATUS,
                unit10_local_closure_result=LOCAL_CLOSURE_RESULT,
                semantic_scope=DISPOSITION_SEMANTIC_SCOPE,
            ),
        )
        disposition_id = reversal_reappearance_effect_disposition_id(candidate)
        dispositions = (
            CandidateLocalReversalReappearanceEffectDisposition(
                reversal_reappearance_effect_disposition_id=disposition_id,
                source_final_candidate_id=candidate.final_candidate_id,
                source_occurrence_id=candidate.source_occurrence_id,
                graph_record_id=candidate.graph_record_id,
                interaction_assertion_id=candidate.interaction_assertion_id,
                source_claim_edge_id=candidate.source_claim_edge_id,
                source_claim_edge_class=candidate.source_claim_edge_class,
                exact_source_fragments=candidate.exact_source_fragments,
                target_effect_channel_id=candidate.target_effect_channel_id,
                target_exact_relation_id=candidate.target_exact_relation_id,
                effect_facet=candidate.effect_facet,
                disposition_kind=profile.disposition_kind,
                semantic_scope=profile.disposition_semantic_scope,
                source_asserted_disposition=profile.source_asserted_disposition,
                source_assertion_subtype_split=profile.source_assertion_subtype_split,
                raw_relation_action=profile.raw_relation_action,
                raw_relation_presence_semantics=profile.raw_relation_presence_semantics,
                source_narrative_chain_ids_provenance=(
                    candidate.source_narrative_chain_ids_provenance
                ),
                source_unresolved_graph_requirements_provenance=(
                    candidate.source_unresolved_graph_requirements_provenance
                ),
            ),
        )
        status = "REVERSAL_REAPPEARANCE_EFFECT_DISPOSITION_PROJECTED"
    else:
        status = "PRESERVED_NON_REVERSAL_REAPPEARANCE_CANDIDATE"
    if status not in CANDIDATE_PROJECTION_STATUSES:
        raise ValueError(f"UNKNOWN_UNIT10_CANDIDATE_PROJECTION_STATUS:{status}")
    disposition_ids = tuple(
        row.reversal_reappearance_effect_disposition_id for row in dispositions
    )
    projection_id = (
        "CLASSICAL_REVERSAL_REAPPEARANCE_EFFECT_CANDIDATE_PROJECTION:"
        + object_sha256({
            "source_final_candidate_id": candidate.final_candidate_id,
            "projection_status": status,
            "reversal_reappearance_closure_rows": json_value(closure_rows),
            "reversal_reappearance_effect_disposition_ids": disposition_ids,
        })
    )
    return ReversalReappearanceEffectCandidateProjection(
        candidate_projection_id=projection_id,
        source_final_candidate_id=candidate.final_candidate_id,
        source_final_candidate=candidate,
        projection_status=status,
        reversal_reappearance_closure_rows=closure_rows,
        reversal_reappearance_effect_dispositions=dispositions,
        reversal_reappearance_effect_disposition_ids=disposition_ids,
    )


def expected_fragment_projection(
    fragment: Any,
    profile: ClassicalReversalReappearanceEffectDispositionProfile,
) -> ReversalReappearanceEffectFragmentProjection:
    candidates = tuple(
        expected_candidate_projection(candidate, profile)
        for candidate in fragment.final_candidates
    )
    disposition_ids = tuple(
        disposition_id
        for candidate in candidates
        for disposition_id in candidate.reversal_reappearance_effect_disposition_ids
    )
    if not fragment.final_candidates:
        status = "PRESERVED_ZERO_CANDIDATES"
    elif disposition_ids:
        status = "REVERSAL_REAPPEARANCE_EFFECT_DISPOSITIONS_PROJECTED"
    else:
        status = "PRESERVED_NO_REVERSAL_REAPPEARANCE_EFFECT_DISPOSITIONS"
    projection_id = (
        "CLASSICAL_REVERSAL_REAPPEARANCE_EFFECT_FRAGMENT_PROJECTION:"
        + object_sha256({
            "source_final_fragment_id": fragment.final_fragment_id,
            "candidate_projection_ids": tuple(
                row.candidate_projection_id for row in candidates
            ),
            "reversal_reappearance_effect_disposition_ids": disposition_ids,
            "projection_status": status,
        })
    )
    return ReversalReappearanceEffectFragmentProjection(
        fragment_projection_id=projection_id,
        source_final_fragment_id=fragment.final_fragment_id,
        source_fragment_id=fragment.source_fragment_id,
        source_occurrence_id=fragment.source_occurrence_id,
        binding_candidate_id=fragment.binding_candidate_id,
        source_final_fragment_status=fragment.final_fragment_status,
        projection_status=status,
        source_final_candidate_ids=fragment.final_candidate_ids,
        candidate_projections=candidates,
        candidate_projection_ids=tuple(
            row.candidate_projection_id for row in candidates
        ),
        reversal_reappearance_effect_disposition_ids=disposition_ids,
    )


def build_expected_source_record_candidate_sets(
    source_final_envelope: Any,
    fragment_projections: tuple[ReversalReappearanceEffectFragmentProjection, ...],
) -> tuple[SourceRecordReversalReappearanceEffectCandidateSet, ...]:
    by_final_fragment_id = {
        row.source_final_fragment_id: row for row in fragment_projections
    }
    if len(by_final_fragment_id) != len(fragment_projections):
        raise ValueError("DUPLICATE_UNIT10_SOURCE_FINAL_FRAGMENT_ID")
    rows: list[SourceRecordReversalReappearanceEffectCandidateSet] = []
    for source_set in source_final_envelope.source_record_candidate_sets:
        try:
            selected = tuple(
                by_final_fragment_id[fragment_id]
                for fragment_id in source_set.final_fragment_ids
            )
        except KeyError as exc:
            raise ValueError(
                f"UNIT10_SOURCE_RECORD_FRAGMENT_LINEAGE_MISSING:{exc.args[0]}"
            ) from exc
        candidate_projection_ids = tuple(
            candidate_id
            for fragment in selected
            for candidate_id in fragment.candidate_projection_ids
        )
        disposition_ids = tuple(
            disposition_id
            for fragment in selected
            for disposition_id in fragment.reversal_reappearance_effect_disposition_ids
        )
        set_id = (
            "CLASSICAL_REVERSAL_REAPPEARANCE_EFFECT_SOURCE_RECORD_SET:"
            + object_sha256({
                "source_final_candidate_set_id": source_set.source_record_candidate_set_id,
                "source_final_fragment_ids": source_set.final_fragment_ids,
                "fragment_projection_ids": tuple(
                    row.fragment_projection_id for row in selected
                ),
                "candidate_projection_ids": candidate_projection_ids,
                "reversal_reappearance_effect_disposition_ids": disposition_ids,
            })
        )
        rows.append(SourceRecordReversalReappearanceEffectCandidateSet(
            source_record_candidate_set_id=set_id,
            source_final_candidate_set_id=source_set.source_record_candidate_set_id,
            source_layer=source_set.source_layer,
            source_occurrence_id=source_set.source_occurrence_id,
            source_final_fragment_ids=source_set.final_fragment_ids,
            fragment_projection_ids=tuple(
                row.fragment_projection_id for row in selected
            ),
            candidate_projection_ids=candidate_projection_ids,
            reversal_reappearance_effect_disposition_ids=disposition_ids,
        ))
    return tuple(rows)


def build_expected_indexes(
    candidate_projections: tuple[ReversalReappearanceEffectCandidateProjection, ...],
) -> tuple[tuple[Any, ...], tuple[Any, ...], tuple[Any, ...]]:
    by_effect: dict[tuple[str, str], dict[str, list[str]]] = {}
    by_occurrence: dict[str, dict[str, list[str]]] = {}
    by_closure: dict[tuple[str, str], list[str]] = {}
    for projection in candidate_projections:
        for disposition in projection.reversal_reappearance_effect_dispositions:
            effect = by_effect.setdefault(
                (disposition.target_exact_relation_id, disposition.effect_facet),
                {"projections": [], "dispositions": []},
            )
            effect["projections"].append(projection.candidate_projection_id)
            effect["dispositions"].append(
                disposition.reversal_reappearance_effect_disposition_id
            )
            occurrence = by_occurrence.setdefault(
                disposition.source_occurrence_id,
                {"projections": [], "dispositions": []},
            )
            occurrence["projections"].append(projection.candidate_projection_id)
            occurrence["dispositions"].append(
                disposition.reversal_reappearance_effect_disposition_id
            )
        for row in projection.reversal_reappearance_closure_rows:
            by_closure.setdefault(
                (row.closure_requirement_id, row.unit10_local_closure_result), []
            ).append(projection.candidate_projection_id)
    effect_index = tuple(
        EffectChannelReversalReappearanceDispositionIndexEntry(
            target_exact_relation_id=key[0],
            effect_facet=key[1],
            candidate_projection_ids=tuple(value["projections"]),
            reversal_reappearance_effect_disposition_ids=tuple(value["dispositions"]),
            index_semantics=INDEX_SEMANTICS,
        )
        for key, value in sorted(by_effect.items())
    )
    occurrence_index = tuple(
        SourceOccurrenceReversalReappearanceDispositionIndexEntry(
            source_occurrence_id=key,
            candidate_projection_ids=tuple(value["projections"]),
            reversal_reappearance_effect_disposition_ids=tuple(value["dispositions"]),
            index_semantics=INDEX_SEMANTICS,
        )
        for key, value in sorted(by_occurrence.items())
    )
    closure_index = tuple(
        LocalReversalReappearanceClosureResolutionIndexEntry(
            closure_requirement_id=key[0],
            unit10_local_closure_result=key[1],
            candidate_projection_ids=tuple(value),
            index_semantics=INDEX_SEMANTICS,
        )
        for key, value in sorted(by_closure.items())
    )
    return effect_index, occurrence_index, closure_index


def reversal_reappearance_effect_hash_bundle(
    source_final_envelope: Any,
    fragment_projections: tuple[Any, ...],
    source_record_candidate_sets: tuple[Any, ...],
    effect_channel_index: tuple[Any, ...],
    source_occurrence_index: tuple[Any, ...],
    local_closure_index: tuple[Any, ...],
    projected_candidate_projection_ids: tuple[str, ...],
    projected_reversal_reappearance_effect_disposition_ids: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ClassicalReversalReappearanceEffectDispositionProfile,
) -> ReversalReappearanceEffectDispositionHashBundle:
    fact_payload = {
        "source_final_effect_envelope_id": source_final_envelope.final_effect_envelope_id,
        "source_final_effect_fact_hash": source_final_envelope.hashes.fact_hash,
        "source_allocation_envelope_id": source_final_envelope.source_allocation_envelope_id,
        "source_mechanism_closure_envelope_id": source_final_envelope.source_mechanism_closure_envelope_id,
        "source_semantic_projection_envelope_id": source_final_envelope.source_semantic_projection_envelope_id,
        "source_admission_envelope_id": source_final_envelope.source_admission_envelope_id,
        "source_effect_envelope_id": source_final_envelope.source_effect_envelope_id,
        "fragment_projections": json_value(fragment_projections),
        "source_record_candidate_sets": json_value(source_record_candidate_sets),
        "effect_channel_index": json_value(effect_channel_index),
        "source_occurrence_index": json_value(source_occurrence_index),
        "local_closure_index": json_value(local_closure_index),
        "projected_candidate_projection_ids": projected_candidate_projection_ids,
        "projected_reversal_reappearance_effect_disposition_ids": (
            projected_reversal_reappearance_effect_disposition_ids
        ),
        "disposition_semantic_scope": profile.disposition_semantic_scope,
        "source_asserted_disposition": profile.source_asserted_disposition,
        "source_assertion_subtype_split": profile.source_assertion_subtype_split,
        "candidate_global_truth_semantics": profile.candidate_global_truth_semantics,
        "global_target_relation_restored_state_semantics": (
            profile.global_target_relation_restored_state_semantics
        ),
        "global_target_relation_active_in_force_state_semantics": (
            profile.global_target_relation_active_in_force_state_semantics
        ),
        "prior_resolution_execution_semantics": (
            profile.prior_resolution_execution_semantics
        ),
        "prior_resolution_failure_execution_semantics": (
            profile.prior_resolution_failure_execution_semantics
        ),
        "interaction_chain_execution_semantics": (
            profile.interaction_chain_execution_semantics
        ),
        "global_operability_semantics": profile.global_operability_semantics,
        "candidate_applicability_semantics": profile.candidate_applicability_semantics,
        "execution_readiness_semantics": profile.execution_readiness_semantics,
        "candidate_selection_semantics": profile.candidate_selection_semantics,
        "candidate_coexistence_semantics": profile.candidate_coexistence_semantics,
        "candidate_exclusivity_semantics": profile.candidate_exclusivity_semantics,
        "candidate_conflict_semantics": profile.candidate_conflict_semantics,
        "precedence_semantics": profile.precedence_semantics,
        "priority_semantics": profile.priority_semantics,
        "winner_loser_semantics": profile.winner_loser_semantics,
        "global_relation_effect_state_semantics": (
            profile.global_relation_effect_state_semantics
        ),
        "attenuation_grade_semantics": profile.attenuation_grade_semantics,
        "participant_allocation_semantics": profile.participant_allocation_semantics,
        "participant_path_selection_semantics": profile.participant_path_selection_semantics,
        "inferred_slot_instance_compatibility": profile.inferred_slot_instance_compatibility,
        "source_narrative_execution": profile.source_narrative_execution,
        "graph_mutation_fixpoint_semantics": profile.graph_mutation_fixpoint_semantics,
        "fragment_selection_semantics": profile.fragment_selection_semantics,
        "cross_outer_composition": profile.cross_outer_composition,
        "cross_source_composition": profile.cross_source_composition,
        "cartesian_expansion": profile.cartesian_expansion,
        "final_classical_verdict_semantics": profile.final_classical_verdict_semantics,
        "raw_relation_immutability_contract": profile.raw_relation_immutability_contract,
    }
    computation_payload = {
        "facts": fact_payload,
        "source_final_effect_computation_hash": (
            source_final_envelope.hashes.computation_hash
        ),
        "source_final_effect_lineage_binding_keys": (
            source_final_envelope.lineage_binding_keys
        ),
        "lineage_binding_keys": lineage_binding_keys,
        "profile": json_value(profile),
    }
    return ReversalReappearanceEffectDispositionHashBundle(
        fact_hash=object_sha256(fact_payload),
        computation_hash=object_sha256(computation_payload),
    )


def validate_reversal_reappearance_effect_envelope(
    source_final_envelope: Any,
    fragment_projections: tuple[Any, ...],
    source_record_candidate_sets: tuple[Any, ...],
    effect_channel_index: tuple[Any, ...],
    source_occurrence_index: tuple[Any, ...],
    local_closure_index: tuple[Any, ...],
    projected_candidate_projection_ids: tuple[str, ...],
    projected_reversal_reappearance_effect_disposition_ids: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ClassicalReversalReappearanceEffectDispositionProfile,
    hashes: ReversalReappearanceEffectDispositionHashBundle,
) -> ReversalReappearanceEffectDispositionIntegrityReport:
    diagnostics: list[ReversalReappearanceEffectDispositionIntegrityDiagnostic] = []
    expected_fragments = tuple(
        expected_fragment_projection(fragment, profile)
        for fragment in source_final_envelope.fragment_envelopes
    )
    if fragment_projections != expected_fragments:
        diagnostics.append(ReversalReappearanceEffectDispositionIntegrityDiagnostic(
            "UNIT10_FRAGMENT_SEMANTIC_REPLAY_MISMATCH",
            "fragment_projections",
            "Unit 10 fragments do not replay exactly from Unit 7",
        ))
    expected_source_sets = build_expected_source_record_candidate_sets(
        source_final_envelope,
        expected_fragments,
    )
    if source_record_candidate_sets != expected_source_sets:
        diagnostics.append(ReversalReappearanceEffectDispositionIntegrityDiagnostic(
            "UNIT10_SOURCE_RECORD_FACTORIZATION_REPLAY_MISMATCH",
            "source_record_candidate_sets",
            "Unit 10 source-record factorization differs from exact Unit 7 lineage replay",
        ))
    expected_candidate_projections = tuple(
        candidate
        for fragment in expected_fragments
        for candidate in fragment.candidate_projections
    )
    expected_indexes = build_expected_indexes(expected_candidate_projections)
    if (
        effect_channel_index,
        source_occurrence_index,
        local_closure_index,
    ) != expected_indexes:
        diagnostics.append(ReversalReappearanceEffectDispositionIntegrityDiagnostic(
            "UNIT10_INDEX_REPLAY_MISMATCH",
            "indexes",
            "identity-only indexes differ from exact candidate projection replay",
        ))
    expected_projection_ids = tuple(
        row.candidate_projection_id for row in expected_candidate_projections
    )
    expected_disposition_ids = tuple(
        disposition_id
        for row in expected_candidate_projections
        for disposition_id in row.reversal_reappearance_effect_disposition_ids
    )
    if projected_candidate_projection_ids != expected_projection_ids:
        diagnostics.append(ReversalReappearanceEffectDispositionIntegrityDiagnostic(
            "UNIT10_CANDIDATE_PROJECTION_ID_REPLAY_MISMATCH",
            "projected_candidate_projection_ids",
            "candidate projection identity set/order drifted",
        ))
    if (
        projected_reversal_reappearance_effect_disposition_ids
        != expected_disposition_ids
    ):
        diagnostics.append(ReversalReappearanceEffectDispositionIntegrityDiagnostic(
            "UNIT10_REVERSAL_REAPPEARANCE_DISPOSITION_ID_REPLAY_MISMATCH",
            "projected_reversal_reappearance_effect_disposition_ids",
            "reversal/reappearance disposition identity set/order drifted",
        ))
    expected_hashes = reversal_reappearance_effect_hash_bundle(
        source_final_envelope,
        fragment_projections,
        source_record_candidate_sets,
        effect_channel_index,
        source_occurrence_index,
        local_closure_index,
        projected_candidate_projection_ids,
        projected_reversal_reappearance_effect_disposition_ids,
        lineage_binding_keys,
        profile,
    )
    if hashes != expected_hashes:
        diagnostics.append(ReversalReappearanceEffectDispositionIntegrityDiagnostic(
            "UNIT10_HASH_REPLAY_MISMATCH",
            "hashes",
            "Unit 10 FactHash/ComputationHash mismatch",
        ))
    return ReversalReappearanceEffectDispositionIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )
