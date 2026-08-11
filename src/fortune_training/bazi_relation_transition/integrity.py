from __future__ import annotations

from dataclasses import fields
from datetime import timezone
from typing import Any

from fortune_training.bazi_chart import BaziChartCandidate
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .generation import (
    AFTER,
    BEFORE,
    ENTERED,
    EXITED,
    PERSISTING,
    RelationTransitionSnapshotInputs,
    _participant_map,
    _relation_map,
    _snapshot_fact_payload,
    build_relation_transition_context,
)
from .models import (
    BaziRelationTransitionContext,
    TransitionHashBundle,
    TransitionIntegrityDiagnostic,
    TransitionIntegrityReport,
)
from .profile import ResolvedBaziRelationTransitionProfile


INTEGRITY_ALGORITHM_ID = "BAZI-RELATION-TRANSITION-INTEGRITY-V1"
INTEGRITY_ALGORITHM_VERSION = "1.0.0"
HASH_ALGORITHM_ID = "BAZI-RELATION-TRANSITION-HASH-V1"
HASH_ALGORITHM_VERSION = "1.0.0"

PROHIBITED_EFFECT_FIELDS = {
    "activated",
    "reactivated",
    "suppressed",
    "cancelled",
    "rescued",
    "released",
    "effective",
    "dominant",
    "strength",
    "weight",
    "winner",
    "loser",
    "transformation_succeeded",
    "transformation_success",
}


def _diag(rows, code: str, path: str, detail: str) -> None:
    rows.append(TransitionIntegrityDiagnostic(code=code, path=path, detail=detail))


def _instant_fact(value) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("transition fact instant must be timezone-aware")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds")


def _participant_fact(row) -> dict[str, Any]:
    return {
        "instance_id": row.instance_id,
        "participant_kind": row.participant_kind,
        "value": row.value,
        "participant_layer": row.participant_layer,
        "source_frame_id": row.source_frame_id,
        "source_upstream_fact_hash": row.source_upstream_fact_hash,
        "source_ganzhi": row.source_ganzhi,
    }


def _snapshot_fact(row) -> dict[str, Any]:
    return {
        "snapshot_id": row.snapshot_id,
        "snapshot_role": row.snapshot_role,
        "snapshot_fact_hash": row.snapshot_fact_hash,
        "target_utc": _instant_fact(row.target_utc),
        "upstream_natal_fact_hash": row.upstream_natal_fact_hash,
        "upstream_temporal_fact_hash": row.upstream_temporal_fact_hash,
        "source_temporal_candidate_indices": sorted(row.source_temporal_candidate_indices),
        "source_temporal_seed_ids": sorted(row.source_temporal_seed_ids),
        "upstream_flow_fact_hash": row.upstream_flow_fact_hash,
        "upstream_structural_fact_hash": row.upstream_structural_fact_hash,
        "upstream_support_fact_hash": row.upstream_support_fact_hash,
        "active_dayun_kind": row.active_dayun_kind,
        "active_dayun_source_frame_id": row.active_dayun_source_frame_id,
        "annual_frame_id": row.annual_frame_id,
        "monthly_frame_id": row.monthly_frame_id,
        "raw_relation_ids": sorted(row.raw_relation_ids),
    }


def _frame_evidence_fact(row) -> dict[str, Any]:
    return {
        "evidence_id": row.evidence_id,
        "evidence_type": row.evidence_type,
        "participant_layer": row.participant_layer,
        "before_source_frame_id": row.before_source_frame_id,
        "after_source_frame_id": row.after_source_frame_id,
        "exited_participant_instance_ids": sorted(row.exited_participant_instance_ids),
        "entered_participant_instance_ids": sorted(row.entered_participant_instance_ids),
        "before_flow_fact_hash": row.before_flow_fact_hash,
        "after_flow_fact_hash": row.after_flow_fact_hash,
    }


def _transition_fact(row) -> dict[str, Any]:
    return {
        "transition_fact_id": row.transition_fact_id,
        "relation_id": row.relation_id,
        "semantic_relation_id": row.semantic_relation_id,
        "relation_type": row.relation_type,
        "relation_family": row.relation_family,
        "participant_instance_ids": list(row.participant_instance_ids),
        "participant_layers": list(row.participant_layers),
        "occurrence_scope": row.occurrence_scope,
        "orientation": row.orientation,
        "arity": row.arity,
        "nominal_transformation_element": row.nominal_transformation_element,
        "transition_state": row.transition_state,
        "before_snapshot_id": row.before_snapshot_id,
        "before_snapshot_fact_hash": row.before_snapshot_fact_hash,
        "after_snapshot_id": row.after_snapshot_id,
        "after_snapshot_fact_hash": row.after_snapshot_fact_hash,
        "before_participant_provenance": [
            _participant_fact(item) for item in row.before_participant_provenance
        ],
        "after_participant_provenance": [
            _participant_fact(item) for item in row.after_participant_provenance
        ],
        "bound_frame_change_evidence_ids": sorted(
            row.bound_frame_change_evidence_ids
        ),
    }


def relation_transition_fact_projection(
    context: BaziRelationTransitionContext,
) -> dict[str, Any]:
    return {
        "before_snapshot": _snapshot_fact(context.before_snapshot),
        "after_snapshot": _snapshot_fact(context.after_snapshot),
        "frame_change_evidence": [
            _frame_evidence_fact(row) for row in context.frame_change_evidence
        ],
        "transition_facts": [
            _transition_fact(row) for row in context.transition_facts
        ],
    }


def relation_transition_hash_bundle(
    context: BaziRelationTransitionContext,
    natal: BaziChartCandidate,
    before: RelationTransitionSnapshotInputs,
    after: RelationTransitionSnapshotInputs,
    paired_temporal_candidate_indices: tuple[int, ...],
    paired_temporal_seed_ids: tuple[str, ...],
    lineage_pairing_keys: tuple[str, ...],
    profile: ResolvedBaziRelationTransitionProfile,
) -> TransitionHashBundle:
    fact_hash = object_sha256(relation_transition_fact_projection(context))
    computation_hash = object_sha256({
        "fact_hash": fact_hash,
        "upstream_computation_hashes": {
            "natal": natal.hashes.computation_hash,
            "before_flow": before.flow.hashes.computation_hash,
            "before_structural": before.structural.hashes.computation_hash,
            "before_support": before.support.hashes.computation_hash,
            "after_flow": after.flow.hashes.computation_hash,
            "after_structural": after.structural.hashes.computation_hash,
            "after_support": after.support.hashes.computation_hash,
        },
        "paired_temporal_candidate_indices": sorted(
            paired_temporal_candidate_indices
        ),
        "paired_temporal_seed_ids": sorted(paired_temporal_seed_ids),
        "lineage_pairing_keys": sorted(lineage_pairing_keys),
        "resolved_transition_profile": json_value(profile),
        "algorithm_versions": dict(sorted(context.algorithm_versions.items())),
        "rule_and_source_lineage": [
            {
                "rule_set_id": row.rule_set_id,
                "rule_set_version": row.rule_set_version,
                "source_refs": sorted(row.source_refs),
            }
            for row in (
                context.before_snapshot,
                context.after_snapshot,
                *context.frame_change_evidence,
            )
        ] + [
            {
                "source_relation_rule_set_id": row.source_relation_rule_set_id,
                "source_relation_rule_set_version": row.source_relation_rule_set_version,
                "transition_rule_set_id": row.transition_rule_set_id,
                "transition_rule_set_version": row.transition_rule_set_version,
                "source_refs": sorted(row.source_refs),
            }
            for row in context.transition_facts
        ],
        "hash_algorithm": f"{HASH_ALGORITHM_ID}@{HASH_ALGORITHM_VERSION}",
    })
    return TransitionHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=HASH_ALGORITHM_ID,
        algorithm_version=HASH_ALGORITHM_VERSION,
    )


def validate_relation_transition_context(
    context: BaziRelationTransitionContext,
    natal: BaziChartCandidate,
    before: RelationTransitionSnapshotInputs,
    after: RelationTransitionSnapshotInputs,
    paired_temporal_candidate_indices: tuple[int, ...],
    paired_temporal_seed_ids: tuple[str, ...],
    lineage_pairing_keys: tuple[str, ...],
    profile: ResolvedBaziRelationTransitionProfile,
    hashes: TransitionHashBundle | None = None,
) -> TransitionIntegrityReport:
    diagnostics: list[TransitionIntegrityDiagnostic] = []
    try:
        profile.validate()
    except ValueError as exc:
        _diag(diagnostics, "PROFILE_INVALID", "profile", str(exc))

    before_value = context.before_snapshot.target_utc
    after_value = context.after_snapshot.target_utc
    if (
        before_value.tzinfo is None
        or before_value.utcoffset() is None
        or after_value.tzinfo is None
        or after_value.utcoffset() is None
    ):
        _diag(
            diagnostics,
            "INVALID_TARGET_INSTANT",
            "snapshots.target_utc",
            "timezone-aware instants required",
        )
        before_target = before_value.replace(tzinfo=timezone.utc)
        after_target = after_value.replace(tzinfo=timezone.utc)
    else:
        before_target = before_value.astimezone(timezone.utc)
        after_target = after_value.astimezone(timezone.utc)
    if before_target >= after_target:
        _diag(
            diagnostics,
            "INVALID_TARGET_ORDER",
            "before_snapshot.target_utc",
            f"{before_target.isoformat()} >= {after_target.isoformat()}",
        )
    if (
        context.before_snapshot.snapshot_role != BEFORE
        or context.after_snapshot.snapshot_role != AFTER
    ):
        _diag(diagnostics, "SNAPSHOT_ROLE_INVALID", "snapshots", "BEFORE/AFTER required")
    if (context.profile_id, context.profile_version) != (
        profile.profile_id,
        profile.profile_version,
    ):
        _diag(diagnostics, "PROFILE_BINDING_MISMATCH", "profile_id", context.profile_id)

    snapshot_chains = (
        ("before_snapshot", context.before_snapshot, before),
        ("after_snapshot", context.after_snapshot, after),
    )
    for path, snapshot, chain in snapshot_chains:
        expected_relation_ids = tuple(sorted(_relation_map(natal, chain.structural)))
        expected_payload = _snapshot_fact_payload(
            snapshot.snapshot_role, natal, chain, expected_relation_ids
        )
        expected_snapshot_hash = object_sha256(expected_payload)
        if snapshot.snapshot_fact_hash != expected_snapshot_hash:
            _diag(diagnostics, "SNAPSHOT_FACT_HASH_MISMATCH", path, snapshot.snapshot_fact_hash)
        if snapshot.snapshot_id != f"RELATION_SNAPSHOT:{snapshot.snapshot_role}:{expected_snapshot_hash}":
            _diag(diagnostics, "SNAPSHOT_ID_MISMATCH", path, snapshot.snapshot_id)
        if snapshot.raw_relation_ids != expected_relation_ids:
            _diag(
                diagnostics,
                "SNAPSHOT_RELATION_REPLAY_MISMATCH",
                f"{path}.raw_relation_ids",
                "must equal released Natal plus Structural relation IDs",
            )
        upstream_expected = {
            "upstream_natal_fact_hash": natal.hashes.fact_hash,
            "upstream_natal_computation_hash": natal.hashes.computation_hash,
            "upstream_temporal_fact_hash": chain.flow.context.upstream_temporal_fact_hash,
            "upstream_flow_fact_hash": chain.flow.hashes.fact_hash,
            "upstream_flow_computation_hash": chain.flow.hashes.computation_hash,
            "upstream_structural_fact_hash": chain.structural.hashes.fact_hash,
            "upstream_structural_computation_hash": chain.structural.hashes.computation_hash,
            "upstream_support_fact_hash": chain.support.hashes.fact_hash,
            "upstream_support_computation_hash": chain.support.hashes.computation_hash,
        }
        for field_name, expected_value in upstream_expected.items():
            if getattr(snapshot, field_name) != expected_value:
                _diag(
                    diagnostics,
                    "UPSTREAM_HASH_BINDING_MISMATCH",
                    f"{path}.{field_name}",
                    str(getattr(snapshot, field_name)),
                )
        if (
            chain.flow.integrity.status != "PASS"
            or chain.structural.integrity.status != "PASS"
            or chain.support.integrity.status != "PASS"
        ):
            _diag(diagnostics, "UPSTREAM_INTEGRITY_FAILED", path, "Flow/Structural/Support")

    if context.before_snapshot.upstream_natal_fact_hash != context.after_snapshot.upstream_natal_fact_hash:
        _diag(diagnostics, "NATAL_LINEAGE_MISMATCH", "snapshots", "Natal FactHash differs")
    if context.before_snapshot.upstream_temporal_fact_hash != context.after_snapshot.upstream_temporal_fact_hash:
        _diag(diagnostics, "TEMPORAL_LINEAGE_MISMATCH", "snapshots", "Temporal FactHash differs")
    expected_indices = tuple(sorted(
        set(before.support.source_temporal_candidate_indices)
        & set(after.support.source_temporal_candidate_indices)
    ))
    expected_seeds = tuple(sorted(
        set(before.support.source_temporal_seed_ids)
        & set(after.support.source_temporal_seed_ids)
    ))
    if tuple(sorted(paired_temporal_candidate_indices)) != expected_indices:
        _diag(diagnostics, "TEMPORAL_CANDIDATE_PAIRING_MISMATCH", "paired_temporal_candidate_indices", str(paired_temporal_candidate_indices))
    if tuple(sorted(paired_temporal_seed_ids)) != expected_seeds:
        _diag(diagnostics, "TEMPORAL_SEED_PAIRING_MISMATCH", "paired_temporal_seed_ids", str(paired_temporal_seed_ids))
    if not expected_indices or not expected_seeds:
        _diag(diagnostics, "INCOMPATIBLE_CANDIDATE_LINEAGE", "pairing", "empty lineage intersection")
    expected_pairing_keys = (
        f"TEMPORAL_FACT:{before.flow.context.upstream_temporal_fact_hash}",
        *(f"TEMPORAL_CANDIDATE_INDEX:{index}" for index in expected_indices),
        *(f"TEMPORAL_SEED:{seed_id}" for seed_id in expected_seeds),
    )
    if lineage_pairing_keys != expected_pairing_keys:
        _diag(
            diagnostics,
            "PAIRING_KEYS_REPLAY_MISMATCH",
            "lineage_pairing_keys",
            "Temporal Fact/seed/candidate lineage does not replay",
        )

    before_ids = set(context.before_snapshot.raw_relation_ids)
    after_ids = set(context.after_snapshot.raw_relation_ids)
    expected_states = {
        PERSISTING: before_ids & after_ids,
        ENTERED: after_ids - before_ids,
        EXITED: before_ids - after_ids,
    }
    facts_by_state = {
        state: {row.relation_id for row in context.transition_facts if row.transition_state == state}
        for state in expected_states
    }
    for state, expected_ids in expected_states.items():
        if facts_by_state[state] != expected_ids:
            _diag(
                diagnostics,
                f"{state}_SET_REPLAY_MISMATCH",
                "transition_facts",
                f"expected {len(expected_ids)} exact relation IDs",
            )
    if len(context.transition_facts) != len(before_ids | after_ids):
        _diag(diagnostics, "TRANSITION_FACT_CARDINALITY_MISMATCH", "transition_facts", str(len(context.transition_facts)))

    before_relations = _relation_map(natal, before.structural)
    after_relations = _relation_map(natal, after.structural)
    before_participants = _participant_map(natal, before.flow, before.structural)
    after_participants = _participant_map(natal, after.flow, after.structural)
    evidence_ids = {row.evidence_id for row in context.frame_change_evidence}
    seen_fact_ids: set[str] = set()
    allowed_relation_types = {
        "STEM_FIVE_COMBINATION",
        "BRANCH_LIUHE",
        "BRANCH_CHONG",
        "BRANCH_CHUAN",
        "BRANCH_SANHE_COMPLETE",
        "BRANCH_ZIMAO_PUNISHMENT",
        "BRANCH_DIRECTIONAL_PUNISHMENT",
        "BRANCH_SELF_PUNISHMENT",
    }
    for index, row in enumerate(context.transition_facts):
        path = f"transition_facts[{index}]"
        if row.transition_fact_id in seen_fact_ids:
            _diag(diagnostics, "DUPLICATE_TRANSITION_FACT_ID", path, row.transition_fact_id)
        seen_fact_ids.add(row.transition_fact_id)
        if row.relation_type not in allowed_relation_types:
            _diag(diagnostics, "RELATION_TYPE_INVALID", path, row.relation_type)
        if row.arity != len(row.participant_instance_ids):
            _diag(diagnostics, "RELATION_ARITY_MISMATCH", path, row.relation_id)
        if row.transition_state in {PERSISTING, EXITED} and row.relation_id not in before_relations:
            _diag(diagnostics, "BEFORE_RELATION_OCCURRENCE_MISSING", path, row.relation_id)
        if row.transition_state in {PERSISTING, ENTERED} and row.relation_id not in after_relations:
            _diag(diagnostics, "AFTER_RELATION_OCCURRENCE_MISSING", path, row.relation_id)
        expected_before_provenance = tuple(
            before_participants[item] for item in row.participant_instance_ids
        ) if row.relation_id in before_relations else ()
        expected_after_provenance = tuple(
            after_participants[item] for item in row.participant_instance_ids
        ) if row.relation_id in after_relations else ()
        if row.before_participant_provenance != expected_before_provenance:
            _diag(diagnostics, "BEFORE_PARTICIPANT_PROVENANCE_MISMATCH", path, row.relation_id)
        if row.after_participant_provenance != expected_after_provenance:
            _diag(diagnostics, "AFTER_PARTICIPANT_PROVENANCE_MISMATCH", path, row.relation_id)
        if not set(row.bound_frame_change_evidence_ids) <= evidence_ids:
            _diag(diagnostics, "FRAME_CHANGE_EVIDENCE_REF_MISSING", path, row.relation_id)
        if row.occurrence_scope == "NATAL_ONLY" and row.participant_layers != ("NATAL",):
            _diag(diagnostics, "NATAL_ONLY_SCOPE_INVALID", path, row.relation_id)
        if row.transition_state == PERSISTING and row.bound_frame_change_evidence_ids:
            _diag(diagnostics, "PERSISTING_HAS_FRAME_CHANGE_BINDING", path, row.relation_id)
        present_fields = {field.name.lower() for field in fields(row)}
        prohibited = present_fields & PROHIBITED_EFFECT_FIELDS
        if prohibited:
            _diag(diagnostics, "CLASSICAL_EFFECT_FIELD_PRESENT", path, ",".join(sorted(prohibited)))

    try:
        expected_context = build_relation_transition_context(natal, before, after, profile)
    except ValueError as exc:
        _diag(diagnostics, "TRANSITION_REPLAY_FAILED", "context", str(exc))
        expected_context = None
    if expected_context is not None:
        replay_checks = (
            ("BEFORE_SNAPSHOT_REPLAY_MISMATCH", "before_snapshot"),
            ("AFTER_SNAPSHOT_REPLAY_MISMATCH", "after_snapshot"),
            ("FRAME_CHANGE_REPLAY_MISMATCH", "frame_change_evidence"),
            ("TRANSITION_FACT_REPLAY_MISMATCH", "transition_facts"),
            ("TRANSITION_ALGORITHM_VERSION_MISMATCH", "algorithm_versions"),
        )
        for code, field_name in replay_checks:
            if getattr(context, field_name) != getattr(expected_context, field_name):
                _diag(diagnostics, code, field_name, "deterministic transition replay mismatch")

    if hashes is not None:
        expected_hashes = relation_transition_hash_bundle(
            context,
            natal,
            before,
            after,
            paired_temporal_candidate_indices,
            paired_temporal_seed_ids,
            lineage_pairing_keys,
            profile,
        )
        if hashes != expected_hashes:
            _diag(diagnostics, "TRANSITION_HASH_REPLAY_MISMATCH", "hashes", hashes.fact_hash)

    return TransitionIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=INTEGRITY_ALGORITHM_ID,
        algorithm_version=INTEGRITY_ALGORITHM_VERSION,
    )
