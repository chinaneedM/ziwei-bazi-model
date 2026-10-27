from __future__ import annotations

from typing import Any

from fortune_training.bazi_classical_effect_constraint_graph.integrity import replay_fragment_hashes
from fortune_training.bazi_classical_effect_constraint_graph.models import EffectCompositionHashBundle
from fortune_training.bazi_classical_effect_constraint_graph.profile import (
    bazi_classical_effect_constraint_graph_factorized_composition_r1_profile,
)
from fortune_training.bazi_classical_resolver_admission.integrity import admission_hash_bundle
from fortune_training.bazi_classical_resolver_admission.profile import (
    bazi_classical_resolver_admission_strict_r1_profile,
    shen_zpzq_ch09_classical_interaction_r1_profile,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .models import (
    SemanticCandidateHashBundle,
    SemanticCandidateIntegrityDiagnostic,
    SemanticCandidateIntegrityReport,
)
from .profile import ClassicalEffectSemanticCandidateProjectionProfile


def match_effect_envelope(source_admission_envelope: Any, source_effect_resolution: Any) -> Any:
    matches = [
        row for row in source_effect_resolution.candidates
        if row.envelope_id == source_admission_envelope.source_effect_envelope_id
        and row.hashes.fact_hash == source_admission_envelope.source_effect_fact_hash
        and row.hashes.computation_hash == source_admission_envelope.source_effect_computation_hash
    ]
    if len(matches) != 1:
        raise ValueError(f"SOURCE_EFFECT_ENVELOPE_MATCH_NOT_UNIQUE:{len(matches)}")
    return matches[0]


def replay_effect_envelope_self_contained(source_effect_envelope: Any) -> bool:
    """Replay the complete Unit 2 payload without requiring the earlier #249 projection input."""
    if source_effect_envelope.integrity.status != "PASS":
        return False
    profile = bazi_classical_effect_constraint_graph_factorized_composition_r1_profile()
    expected_lineage_tail = (
        f"SOURCE_PROJECTION_FACT:{source_effect_envelope.source_projection_fact_hash}",
        f"SOURCE_PROJECTION_COMPUTATION:{source_effect_envelope.source_projection_computation_hash}",
        f"EFFECT_GRAPH_PROFILE:{profile.profile_id}:{profile.profile_version}",
    )
    if (
        len(source_effect_envelope.lineage_binding_keys) < 3
        or source_effect_envelope.lineage_binding_keys[-3:] != expected_lineage_tail
        or source_effect_envelope.cross_source_layer_composition != "NOT_RELEASED"
        or source_effect_envelope.cartesian_expansion != "NOT_RELEASED"
        or source_effect_envelope.raw_relation_immutability_contract != "IMMUTABLE_EXACT_REFERENCE_ONLY"
        or source_effect_envelope.algorithm_versions != {
            "graph_projection": profile.graph_algorithm_version,
            "factorized_composition": profile.composition_algorithm_version,
        }
    ):
        return False

    if any(
        replay_fragment_hashes(
            fragment,
            source_effect_envelope.source_projection_fact_hash,
            profile,
        ) != fragment.hashes
        for fragment in source_effect_envelope.fragments
    ):
        return False

    fact_payload = {
        "source_projection_fact_hash": source_effect_envelope.source_projection_fact_hash,
        "source_binding_snapshot_id": source_effect_envelope.source_binding_snapshot_id,
        "source_binding_snapshot_fact_hash": source_effect_envelope.source_binding_snapshot_fact_hash,
        "fragments": json_value(source_effect_envelope.fragments),
        "source_layer_partitions": json_value(source_effect_envelope.source_layer_partitions),
        "raw_relation_reference_index": json_value(source_effect_envelope.raw_relation_reference_index),
        "effect_channel_coordinate_index": json_value(source_effect_envelope.effect_channel_coordinate_index),
        "cross_source_layer_composition": "NOT_RELEASED",
        "cartesian_expansion": "NOT_RELEASED",
        "raw_relation_immutability_contract": "IMMUTABLE_EXACT_REFERENCE_ONLY",
    }
    source_projection_lineage_binding_keys = source_effect_envelope.lineage_binding_keys[:-3]
    computation_payload = {
        "facts": fact_payload,
        "source_projection_computation_hash": source_effect_envelope.source_projection_computation_hash,
        "source_projection_lineage_binding_keys": source_projection_lineage_binding_keys,
        "lineage_binding_keys": source_effect_envelope.lineage_binding_keys,
        "profile": json_value(profile),
    }
    expected = EffectCompositionHashBundle(
        fact_hash=object_sha256(fact_payload),
        computation_hash=object_sha256(computation_payload),
    )
    return expected == source_effect_envelope.hashes


def replay_admission_envelope_against_effect(
    source_admission_envelope: Any,
    source_effect_envelope: Any,
) -> bool:
    if (
        source_admission_envelope.integrity.status != "PASS"
        or not replay_effect_envelope_self_contained(source_effect_envelope)
    ):
        return False
    if (
        source_admission_envelope.source_effect_envelope_id != source_effect_envelope.envelope_id
        or source_admission_envelope.source_effect_fact_hash != source_effect_envelope.hashes.fact_hash
        or source_admission_envelope.source_effect_computation_hash != source_effect_envelope.hashes.computation_hash
        or source_admission_envelope.source_projection_fact_hash != source_effect_envelope.source_projection_fact_hash
        or source_admission_envelope.source_projection_computation_hash != source_effect_envelope.source_projection_computation_hash
        or source_admission_envelope.source_binding_fact_hash != source_effect_envelope.source_binding_fact_hash
        or source_admission_envelope.source_binding_computation_hash != source_effect_envelope.source_binding_computation_hash
    ):
        return False
    source_profile = shen_zpzq_ch09_classical_interaction_r1_profile()
    admission_profile = bazi_classical_resolver_admission_strict_r1_profile()
    expected = admission_hash_bundle(
        source_effect_envelope,
        source_admission_envelope.fragment_admissions,
        source_admission_envelope.source_record_candidate_sets,
        source_admission_envelope.admitted_fragment_ids,
        source_admission_envelope.preserved_not_admitted_fragment_ids,
        source_admission_envelope.preserved_outside_profile_fragment_ids,
        source_admission_envelope.lineage_binding_keys,
        source_profile,
        admission_profile,
    )
    return expected == source_admission_envelope.hashes


def semantic_projection_hash_bundle(
    source_admission_envelope: Any,
    source_effect_envelope: Any,
    fragment_projections: tuple[Any, ...],
    source_record_candidate_sets: tuple[Any, ...],
    effect_channel_candidate_index: tuple[Any, ...],
    projected_semantic_candidate_ids: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ClassicalEffectSemanticCandidateProjectionProfile,
) -> SemanticCandidateHashBundle:
    fact_payload = {
        "source_admission_envelope_id": source_admission_envelope.admission_envelope_id,
        "source_admission_fact_hash": source_admission_envelope.hashes.fact_hash,
        "source_effect_envelope_id": source_effect_envelope.envelope_id,
        "source_effect_fact_hash": source_effect_envelope.hashes.fact_hash,
        "fragment_projections": json_value(fragment_projections),
        "source_record_candidate_sets": json_value(source_record_candidate_sets),
        "effect_channel_candidate_index": json_value(effect_channel_candidate_index),
        "projected_semantic_candidate_ids": projected_semantic_candidate_ids,
        "fragment_selection_semantics": profile.fragment_selection_semantics,
        "cross_outer_composition": profile.cross_outer_composition,
        "cartesian_expansion": profile.cartesian_expansion,
        "raw_relation_immutability_contract": profile.raw_relation_immutability_contract,
        "candidate_truth_semantics": profile.candidate_truth_semantics,
        "candidate_coexistence_semantics": profile.candidate_coexistence_semantics,
        "candidate_exclusivity_semantics": profile.candidate_exclusivity_semantics,
        "candidate_priority_semantics": profile.candidate_priority_semantics,
        "candidate_conflict_semantics": profile.candidate_conflict_semantics,
        "candidate_rewrite_semantics": profile.candidate_rewrite_semantics,
        "candidate_state_transition_semantics": profile.candidate_state_transition_semantics,
        "candidate_winner_loser_semantics": profile.candidate_winner_loser_semantics,
    }
    computation_payload = {
        "facts": fact_payload,
        "source_admission_computation_hash": source_admission_envelope.hashes.computation_hash,
        "source_effect_computation_hash": source_effect_envelope.hashes.computation_hash,
        "source_admission_lineage_binding_keys": source_admission_envelope.lineage_binding_keys,
        "lineage_binding_keys": lineage_binding_keys,
        "profile": json_value(profile),
    }
    return SemanticCandidateHashBundle(
        fact_hash=object_sha256(fact_payload),
        computation_hash=object_sha256(computation_payload),
    )


def validate_semantic_projection_envelope(
    source_admission_envelope: Any,
    source_effect_envelope: Any,
    fragment_projections: tuple[Any, ...],
    source_record_candidate_sets: tuple[Any, ...],
    effect_channel_candidate_index: tuple[Any, ...],
    projected_semantic_candidate_ids: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ClassicalEffectSemanticCandidateProjectionProfile,
    hashes: SemanticCandidateHashBundle,
) -> SemanticCandidateIntegrityReport:
    diagnostics: list[SemanticCandidateIntegrityDiagnostic] = []

    def diag(code: str, path: str, detail: str) -> None:
        diagnostics.append(SemanticCandidateIntegrityDiagnostic(code, path, detail))

    if not replay_effect_envelope_self_contained(source_effect_envelope):
        diag("UPSTREAM_EFFECT_ENVELOPE_SELF_REPLAY_MISMATCH", "source_effect_envelope", source_effect_envelope.envelope_id)
    if not replay_admission_envelope_against_effect(source_admission_envelope, source_effect_envelope):
        diag("UPSTREAM_ADMISSION_ENVELOPE_REPLAY_MISMATCH", "source_admission_envelope", source_admission_envelope.admission_envelope_id)

    source_fragment_ids = tuple(row.fragment_id for row in source_effect_envelope.fragments)
    if tuple(row.source_fragment_id for row in fragment_projections) != source_fragment_ids:
        diag("FRAGMENT_PROJECTION_IDENTITY_OR_ORDER_MISMATCH", "fragment_projections", str(source_fragment_ids))
    if len(fragment_projections) != len(source_admission_envelope.fragment_admissions):
        diag("FRAGMENT_PROJECTION_CARDINALITY_MISMATCH", "fragment_projections", str(len(fragment_projections)))

    admission_by_fragment = {
        row.source_fragment_id: row for row in source_admission_envelope.fragment_admissions
    }
    if len(admission_by_fragment) != len(source_admission_envelope.fragment_admissions):
        diag("UPSTREAM_ADMISSION_FRAGMENT_ID_DUPLICATE", "fragment_admissions", str(len(admission_by_fragment)))
    effect_by_fragment = {row.fragment_id: row for row in source_effect_envelope.fragments}

    all_candidate_ids: list[str] = []
    for row in fragment_projections:
        admission = admission_by_fragment.get(row.source_fragment_id)
        effect_fragment = effect_by_fragment.get(row.source_fragment_id)
        if admission is None or effect_fragment is None:
            diag("FRAGMENT_SOURCE_MATCH_MISSING", row.fragment_semantic_projection_id, row.source_fragment_id)
            continue
        if (
            row.source_fragment_fact_hash != effect_fragment.hashes.fact_hash
            or row.source_fragment_computation_hash != effect_fragment.hashes.computation_hash
            or row.source_admission_projection_id != admission.admission_projection_id
            or row.admission_status != admission.admission_status
            or row.admission_blocker_ids != admission.admission_blocker_ids
        ):
            diag("FRAGMENT_SOURCE_REPLAY_MISMATCH", row.fragment_semantic_projection_id, row.source_fragment_id)
        if admission.admission_status == "ADMITTED":
            if row.projection_status != "SEMANTIC_CANDIDATES_PROJECTED":
                diag("ADMITTED_FRAGMENT_NOT_PROJECTED", row.fragment_semantic_projection_id, row.projection_status)
            if len(row.semantic_candidates) != len(effect_fragment.effect_constraint_nodes):
                diag("ADMITTED_CONSTRAINT_TO_CANDIDATE_CARDINALITY_MISMATCH", row.fragment_semantic_projection_id, f"{len(effect_fragment.effect_constraint_nodes)}->{len(row.semantic_candidates)}")
        elif admission.admission_status == "PRESERVED_NOT_ADMITTED":
            if row.projection_status != "PRESERVED_NO_SEMANTIC_CANDIDATES" or row.semantic_candidates:
                diag("NOT_ADMITTED_FRAGMENT_EMITTED_CANDIDATE", row.fragment_semantic_projection_id, row.projection_status)
        elif admission.admission_status == "PRESERVED_OUTSIDE_PROFILE":
            if row.projection_status != "PRESERVED_OUTSIDE_PROFILE_NO_SEMANTIC_CANDIDATES" or row.semantic_candidates:
                diag("OUTSIDE_PROFILE_FRAGMENT_EMITTED_CANDIDATE", row.fragment_semantic_projection_id, row.projection_status)
        else:
            diag("UNKNOWN_ADMISSION_STATUS", row.fragment_semantic_projection_id, admission.admission_status)
        all_candidate_ids.extend(candidate.semantic_candidate_id for candidate in row.semantic_candidates)

    if len(all_candidate_ids) != len(set(all_candidate_ids)):
        diag("SEMANTIC_CANDIDATE_ID_DUPLICATE", "semantic_candidates", str(len(all_candidate_ids)))
    if tuple(all_candidate_ids) != projected_semantic_candidate_ids:
        diag("SEMANTIC_CANDIDATE_ID_INDEX_MISMATCH", "projected_semantic_candidate_ids", str(projected_semantic_candidate_ids))

    upstream_record_sets = {
        row.source_record_candidate_set_id: row
        for row in source_admission_envelope.source_record_candidate_sets
    }
    projection_by_fragment = {row.source_fragment_id: row for row in fragment_projections}
    if len(source_record_candidate_sets) != len(upstream_record_sets):
        diag("SOURCE_RECORD_SET_CARDINALITY_MISMATCH", "source_record_candidate_sets", str(len(source_record_candidate_sets)))
    for row in source_record_candidate_sets:
        upstream = upstream_record_sets.get(row.source_record_candidate_set_id)
        if upstream is None:
            diag("SOURCE_RECORD_SET_UPSTREAM_MISSING", row.source_record_candidate_set_id, row.source_occurrence_id)
            continue
        if row.source_fragment_ids != upstream.source_fragment_ids:
            diag("SOURCE_RECORD_SET_FRAGMENT_IDENTITY_MISMATCH", row.source_record_candidate_set_id, str(row.source_fragment_ids))
        expected_projection_ids = tuple(
            projection_by_fragment[fragment_id].fragment_semantic_projection_id
            for fragment_id in row.source_fragment_ids
        )
        if row.fragment_semantic_projection_ids != expected_projection_ids:
            diag("SOURCE_RECORD_SET_PROJECTION_ID_MISMATCH", row.source_record_candidate_set_id, str(row.fragment_semantic_projection_ids))
        expected_candidate_ids = tuple(
            candidate.semantic_candidate_id
            for fragment_id in row.source_fragment_ids
            for candidate in projection_by_fragment[fragment_id].semantic_candidates
        )
        if row.semantic_candidate_ids != expected_candidate_ids:
            diag("SOURCE_RECORD_SET_CANDIDATE_ID_MISMATCH", row.source_record_candidate_set_id, str(row.semantic_candidate_ids))
        if any(value != "NOT_RELEASED" for value in (
            row.member_selection_semantics,
            row.member_coexistence_semantics,
            row.member_exclusivity_semantics,
            row.semantic_candidate_priority_semantics,
            row.semantic_candidate_conflict_semantics,
        )):
            diag("SOURCE_RECORD_SET_SEMANTICS_OVERRESOLVED", row.source_record_candidate_set_id, "selection/coexistence/exclusivity/priority/conflict")

    indexed_candidate_ids = tuple(
        candidate_id for row in effect_channel_candidate_index for candidate_id in row.semantic_candidate_ids
    )
    if set(indexed_candidate_ids) != set(projected_semantic_candidate_ids):
        diag("EFFECT_CHANNEL_INDEX_COVERAGE_MISMATCH", "effect_channel_candidate_index", str(len(indexed_candidate_ids)))
    if any(row.index_semantics != "IDENTITY_ONLY_NO_MERGE_OR_ARBITRATION" for row in effect_channel_candidate_index):
        diag("EFFECT_CHANNEL_INDEX_SEMANTICS_OVERRESOLVED", "effect_channel_candidate_index", "index semantics")

    expected_hashes = semantic_projection_hash_bundle(
        source_admission_envelope,
        source_effect_envelope,
        fragment_projections,
        source_record_candidate_sets,
        effect_channel_candidate_index,
        projected_semantic_candidate_ids,
        lineage_binding_keys,
        profile,
    )
    if expected_hashes != hashes:
        diag("SEMANTIC_PROJECTION_HASH_REPLAY_MISMATCH", "hashes", hashes.fact_hash)

    return SemanticCandidateIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )
