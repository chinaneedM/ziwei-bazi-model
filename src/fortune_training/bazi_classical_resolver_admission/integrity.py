from __future__ import annotations

from typing import Any

from fortune_training.bazi_classical_effect_constraint_graph.integrity import (
    composition_hash_bundle as effect_composition_hash_bundle,
    match_source_binding_outer,
    replay_fragment_hashes,
    replay_source_projection_outer,
)
from fortune_training.bazi_classical_effect_constraint_graph.profile import (
    bazi_classical_effect_constraint_graph_factorized_composition_r1_profile,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .models import (
    ResolverAdmissionHashBundle,
    ResolverAdmissionIntegrityDiagnostic,
    ResolverAdmissionIntegrityReport,
)
from .profile import (
    ClassicalInteractionResolverAdmissionProfile,
    ClassicalSourceSemanticProfile,
)


def match_projection_outer(source_effect_envelope: Any, source_projection_resolution: Any) -> Any:
    matches = [
        outer for outer in source_projection_resolution.candidates
        if outer.hashes.fact_hash == source_effect_envelope.source_projection_fact_hash
        and outer.hashes.computation_hash == source_effect_envelope.source_projection_computation_hash
    ]
    if len(matches) != 1:
        raise ValueError(f"SOURCE_PROJECTION_OUTER_MATCH_NOT_UNIQUE:{len(matches)}")
    return matches[0]


def replay_effect_envelope(
    source_effect_envelope: Any,
    source_projection_outer: Any,
    source_binding_resolution: Any,
) -> bool:
    if source_effect_envelope.integrity.status != "PASS":
        return False
    source_binding_outer = match_source_binding_outer(
        source_projection_outer, source_binding_resolution
    )
    if not replay_source_projection_outer(source_projection_outer, source_binding_outer):
        return False
    if (
        source_effect_envelope.source_projection_fact_hash != source_projection_outer.hashes.fact_hash
        or source_effect_envelope.source_projection_computation_hash != source_projection_outer.hashes.computation_hash
        or source_effect_envelope.source_binding_fact_hash != source_binding_outer.hashes.fact_hash
        or source_effect_envelope.source_binding_computation_hash != source_binding_outer.hashes.computation_hash
    ):
        return False
    effect_profile = bazi_classical_effect_constraint_graph_factorized_composition_r1_profile()
    if any(
        replay_fragment_hashes(
            fragment,
            source_effect_envelope.source_projection_fact_hash,
            effect_profile,
        ) != fragment.hashes
        for fragment in source_effect_envelope.fragments
    ):
        return False
    expected = effect_composition_hash_bundle(
        source_projection_outer,
        source_effect_envelope.fragments,
        source_effect_envelope.source_layer_partitions,
        source_effect_envelope.raw_relation_reference_index,
        source_effect_envelope.effect_channel_coordinate_index,
        source_effect_envelope.lineage_binding_keys,
        effect_profile,
    )
    return expected == source_effect_envelope.hashes


def admission_hash_bundle(
    source_effect_envelope: Any,
    fragment_admissions: tuple[Any, ...],
    source_record_candidate_sets: tuple[Any, ...],
    admitted_fragment_ids: tuple[str, ...],
    preserved_not_admitted_fragment_ids: tuple[str, ...],
    preserved_outside_profile_fragment_ids: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    source_profile: ClassicalSourceSemanticProfile,
    admission_profile: ClassicalInteractionResolverAdmissionProfile,
) -> ResolverAdmissionHashBundle:
    fact_payload = {
        "source_effect_envelope_id": source_effect_envelope.envelope_id,
        "source_effect_fact_hash": source_effect_envelope.hashes.fact_hash,
        "source_projection_fact_hash": source_effect_envelope.source_projection_fact_hash,
        "source_binding_fact_hash": source_effect_envelope.source_binding_fact_hash,
        "source_semantic_profile_id": source_profile.profile_id,
        "source_semantic_partition_id": source_profile.partition_id,
        "fragment_admissions": json_value(fragment_admissions),
        "source_record_candidate_sets": json_value(source_record_candidate_sets),
        "admitted_fragment_ids": admitted_fragment_ids,
        "preserved_not_admitted_fragment_ids": preserved_not_admitted_fragment_ids,
        "preserved_outside_profile_fragment_ids": preserved_outside_profile_fragment_ids,
        "fragment_selection_semantics": "NOT_RELEASED",
        "cross_outer_composition": "NOT_RELEASED",
        "cartesian_expansion": "NOT_RELEASED",
        "raw_relation_immutability_contract": admission_profile.raw_relation_immutability_contract,
        "transition_separation_contract": admission_profile.transition_separation_contract,
    }
    computation_payload = {
        "facts": fact_payload,
        "source_effect_computation_hash": source_effect_envelope.hashes.computation_hash,
        "source_projection_computation_hash": source_effect_envelope.source_projection_computation_hash,
        "source_binding_computation_hash": source_effect_envelope.source_binding_computation_hash,
        "source_effect_lineage_binding_keys": source_effect_envelope.lineage_binding_keys,
        "lineage_binding_keys": lineage_binding_keys,
        "source_profile": json_value(source_profile),
        "admission_profile": json_value(admission_profile),
    }
    return ResolverAdmissionHashBundle(
        fact_hash=object_sha256(fact_payload),
        computation_hash=object_sha256(computation_payload),
    )


def validate_admission_envelope(
    source_effect_envelope: Any,
    source_projection_outer: Any,
    source_binding_resolution: Any,
    fragment_admissions: tuple[Any, ...],
    source_record_candidate_sets: tuple[Any, ...],
    admitted_fragment_ids: tuple[str, ...],
    preserved_not_admitted_fragment_ids: tuple[str, ...],
    preserved_outside_profile_fragment_ids: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    source_profile: ClassicalSourceSemanticProfile,
    admission_profile: ClassicalInteractionResolverAdmissionProfile,
    hashes: ResolverAdmissionHashBundle,
) -> ResolverAdmissionIntegrityReport:
    diagnostics: list[ResolverAdmissionIntegrityDiagnostic] = []

    def diag(code: str, path: str, detail: str) -> None:
        diagnostics.append(ResolverAdmissionIntegrityDiagnostic(code, path, detail))

    if not replay_effect_envelope(
        source_effect_envelope, source_projection_outer, source_binding_resolution
    ):
        diag("UPSTREAM_EFFECT_ENVELOPE_REPLAY_MISMATCH", "source_effect_envelope", source_effect_envelope.envelope_id)

    if len(fragment_admissions) != len(source_effect_envelope.fragments):
        diag("FRAGMENT_ADMISSION_CARDINALITY_MISMATCH", "fragment_admissions", f"{len(source_effect_envelope.fragments)}->{len(fragment_admissions)}")
    if tuple(row.source_fragment_id for row in fragment_admissions) != tuple(row.fragment_id for row in source_effect_envelope.fragments):
        diag("FRAGMENT_ADMISSION_IDENTITY_OR_ORDER_MISMATCH", "fragment_admissions", "one sidecar row per source fragment required")

    status_partition = {
        "ADMITTED": tuple(row.source_fragment_id for row in fragment_admissions if row.admission_status == "ADMITTED"),
        "PRESERVED_NOT_ADMITTED": tuple(row.source_fragment_id for row in fragment_admissions if row.admission_status == "PRESERVED_NOT_ADMITTED"),
        "PRESERVED_OUTSIDE_PROFILE": tuple(row.source_fragment_id for row in fragment_admissions if row.admission_status == "PRESERVED_OUTSIDE_PROFILE"),
    }
    if status_partition["ADMITTED"] != admitted_fragment_ids:
        diag("ADMITTED_FRAGMENT_INDEX_MISMATCH", "admitted_fragment_ids", str(admitted_fragment_ids))
    if status_partition["PRESERVED_NOT_ADMITTED"] != preserved_not_admitted_fragment_ids:
        diag("PRESERVED_NOT_ADMITTED_INDEX_MISMATCH", "preserved_not_admitted_fragment_ids", str(preserved_not_admitted_fragment_ids))
    if status_partition["PRESERVED_OUTSIDE_PROFILE"] != preserved_outside_profile_fragment_ids:
        diag("PRESERVED_OUTSIDE_PROFILE_INDEX_MISMATCH", "preserved_outside_profile_fragment_ids", str(preserved_outside_profile_fragment_ids))

    for row in fragment_admissions:
        if any("SOURCE_UNRESOLVED_GRAPH" in blocker for blocker in row.admission_blocker_ids):
            diag("SOURCE_UNRESOLVED_GRAPH_REQUIREMENT_USED_AS_PREDICATE", row.admission_projection_id, str(row.admission_blocker_ids))
        if row.admission_status == "ADMITTED" and row.admission_blocker_ids:
            diag("ADMITTED_FRAGMENT_HAS_BLOCKERS", row.admission_projection_id, str(row.admission_blocker_ids))
        if row.admission_status == "PRESERVED_OUTSIDE_PROFILE" and row.partition_match:
            diag("OUTSIDE_PROFILE_FRAGMENT_MARKED_PARTITION_MATCH", row.admission_projection_id, row.source_occurrence_id)
        if row.admission_status != "PRESERVED_OUTSIDE_PROFILE" and not row.partition_match:
            diag("PARTITION_MISMATCH_NOT_PRESERVED_OUTSIDE", row.admission_projection_id, row.source_occurrence_id)

    source_sets = {
        record_set.source_record_candidate_set_id: record_set
        for partition in source_effect_envelope.source_layer_partitions
        for record_set in partition.source_record_candidate_sets
    }
    if len(source_record_candidate_sets) != len(source_sets):
        diag("SOURCE_RECORD_SET_CARDINALITY_MISMATCH", "source_record_candidate_sets", str(len(source_sets)))
    admission_by_fragment = {row.source_fragment_id: row for row in fragment_admissions}
    for row in source_record_candidate_sets:
        source_set = source_sets.get(row.source_record_candidate_set_id)
        if source_set is None:
            diag("SOURCE_RECORD_SET_IDENTITY_MISSING", row.source_record_candidate_set_id, row.source_occurrence_id)
            continue
        if row.source_fragment_ids != source_set.fragment_ids:
            diag("SOURCE_RECORD_SET_FRAGMENT_IDENTITY_MISMATCH", row.source_record_candidate_set_id, str(row.source_fragment_ids))
        expected_projection_ids = tuple(admission_by_fragment[fragment_id].admission_projection_id for fragment_id in row.source_fragment_ids)
        if row.admission_projection_ids != expected_projection_ids:
            diag("SOURCE_RECORD_SET_ADMISSION_PROJECTION_MISMATCH", row.source_record_candidate_set_id, str(row.admission_projection_ids))
        if (
            row.member_selection_semantics != "NOT_RELEASED"
            or row.member_coexistence_semantics != "NOT_RELEASED"
            or row.member_exclusivity_semantics != "NOT_RELEASED"
        ):
            diag("SOURCE_RECORD_SET_SEMANTICS_OVERRESOLVED", row.source_record_candidate_set_id, "member semantics")

    expected_hashes = admission_hash_bundle(
        source_effect_envelope,
        fragment_admissions,
        source_record_candidate_sets,
        admitted_fragment_ids,
        preserved_not_admitted_fragment_ids,
        preserved_outside_profile_fragment_ids,
        lineage_binding_keys,
        source_profile,
        admission_profile,
    )
    if hashes != expected_hashes:
        diag("ADMISSION_HASH_REPLAY_MISMATCH", "hashes", hashes.fact_hash)
    return ResolverAdmissionIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )
