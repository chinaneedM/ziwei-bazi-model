from __future__ import annotations

from dataclasses import dataclass
from datetime import timezone
from typing import Any

from fortune_training.bazi_chart import BaziChartCandidate
from fortune_training.bazi_flow import BaziFlowCandidate
from fortune_training.bazi_structural import BaziStructuralCandidate
from fortune_training.bazi_structural_support import BaziStructuralSupportCandidate
from fortune_training.util import object_sha256

from .models import (
    BaziRelationTransitionContext,
    FrameChangeEvidence,
    RawRelationTransitionFact,
    RelationParticipantReference,
    RelationSnapshotReference,
)
from .profile import (
    CANDIDATE_PAIRING_RULE_SET_VERSION,
    FRAME_DIFFERENCE_RULE_SET_ID,
    FRAME_DIFFERENCE_RULE_SET_VERSION,
    SET_REPLAY_RULE_SET_ID,
    SET_REPLAY_RULE_SET_VERSION,
    SNAPSHOT_RULE_SET_ID,
    SNAPSHOT_RULE_SET_VERSION,
    ResolvedBaziRelationTransitionProfile,
)


BEFORE = "BEFORE"
AFTER = "AFTER"
PERSISTING = "PERSISTING"
ENTERED = "ENTERED"
EXITED = "EXITED"
TRANSITION_STATES = (PERSISTING, ENTERED, EXITED)
LAYER_ORDER = ("NATAL", "DAYUN", "ANNUAL", "MONTHLY")


@dataclass(frozen=True)
class RelationTransitionSnapshotInputs:
    flow_index: int
    structural_index: int
    support_index: int
    flow: BaziFlowCandidate
    structural: BaziStructuralCandidate
    support: BaziStructuralSupportCandidate


def _instant_fact(value) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("transition snapshot target must be timezone-aware")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds")


def _relation_type(row) -> str:
    if row.relation_family == "STEM_COMBINATION":
        return "STEM_FIVE_COMBINATION"
    if row.relation_family == "BRANCH_SIX_HARMONY":
        return "BRANCH_LIUHE"
    if row.relation_family == "BRANCH_CLASH":
        return "BRANCH_CHONG"
    if row.relation_family == "BRANCH_CHUAN":
        return "BRANCH_CHUAN"
    if row.relation_family == "BRANCH_TRINE":
        return "BRANCH_SANHE_COMPLETE"
    if row.semantic_relation_id == "BRANCH.PUNISHMENT.ZI_MAO":
        return "BRANCH_ZIMAO_PUNISHMENT"
    if row.orientation == "DIRECTED":
        return "BRANCH_DIRECTIONAL_PUNISHMENT"
    if row.orientation == "SELF":
        return "BRANCH_SELF_PUNISHMENT"
    raise ValueError(f"unsupported released raw relation occurrence: {row.relation_id}")


def _relation_map(natal: BaziChartCandidate, structural: BaziStructuralCandidate):
    rows = natal.chart.raw_relations + structural.context.dynamic_raw_relations
    mapped = {row.relation_id: row for row in rows}
    if len(mapped) != len(rows):
        raise ValueError("released Natal and Structural raw relation IDs overlap")
    return mapped


def _participant_map(
    natal: BaziChartCandidate,
    flow: BaziFlowCandidate,
    structural: BaziStructuralCandidate,
) -> dict[str, RelationParticipantReference]:
    pillar_by_position = {row.position: row.ganzhi for row in natal.chart.pillars}
    result: dict[str, RelationParticipantReference] = {}
    for row in natal.chart.stems:
        result[row.instance_id] = RelationParticipantReference(
            instance_id=row.instance_id,
            participant_kind="STEM",
            value=row.stem,
            participant_layer="NATAL",
            source_frame_id=None,
            source_upstream_fact_hash=natal.hashes.fact_hash,
            source_ganzhi=pillar_by_position[row.position],
        )
    for row in natal.chart.branches:
        result[row.instance_id] = RelationParticipantReference(
            instance_id=row.instance_id,
            participant_kind="BRANCH",
            value=row.branch,
            participant_layer="NATAL",
            source_frame_id=None,
            source_upstream_fact_hash=natal.hashes.fact_hash,
            source_ganzhi=pillar_by_position[row.position],
        )

    provenance = {
        row.instance_id: row for row in structural.context.temporal_participant_provenance
    }
    temporal_rows = (
        ((row.instance_id, "STEM", row.stem) for row in structural.context.active_temporal_stems),
        ((row.instance_id, "BRANCH", row.branch) for row in structural.context.active_temporal_branches),
    )
    for group in temporal_rows:
        for instance_id, kind, value in group:
            source = provenance[instance_id]
            result[instance_id] = RelationParticipantReference(
                instance_id=instance_id,
                participant_kind=kind,
                value=value,
                participant_layer=source.layer,
                source_frame_id=source.source_frame_id,
                source_upstream_fact_hash=flow.hashes.fact_hash,
                source_ganzhi=source.source_ganzhi,
            )
    return result


def _snapshot_fact_payload(
    role: str,
    natal: BaziChartCandidate,
    chain: RelationTransitionSnapshotInputs,
    raw_relation_ids: tuple[str, ...],
) -> dict[str, Any]:
    flow = chain.flow
    structural = chain.structural
    support = chain.support
    return {
        "snapshot_role": role,
        "target_utc": _instant_fact(flow.context.target_utc),
        "upstream_natal_fact_hash": natal.hashes.fact_hash,
        "upstream_temporal_fact_hash": flow.context.upstream_temporal_fact_hash,
        "source_temporal_candidate_indices": sorted(
            support.source_temporal_candidate_indices
        ),
        "source_temporal_seed_ids": sorted(support.source_temporal_seed_ids),
        "upstream_flow_fact_hash": flow.hashes.fact_hash,
        "upstream_structural_fact_hash": structural.hashes.fact_hash,
        "upstream_support_fact_hash": support.hashes.fact_hash,
        "active_dayun_kind": flow.context.active_dayun_kind,
        "active_dayun_source_frame_id": flow.context.active_dayun_frame.frame_id,
        "annual_frame_id": flow.context.annual_frame.frame_id,
        "monthly_frame_id": flow.context.monthly_frame.frame_id,
        "raw_relation_ids": list(raw_relation_ids),
    }


def build_snapshot_reference(
    role: str,
    natal: BaziChartCandidate,
    chain: RelationTransitionSnapshotInputs,
) -> RelationSnapshotReference:
    if role not in {BEFORE, AFTER}:
        raise ValueError(f"unsupported snapshot role: {role}")
    relation_ids = tuple(sorted(_relation_map(natal, chain.structural)))
    payload = _snapshot_fact_payload(role, natal, chain, relation_ids)
    fact_hash = object_sha256(payload)
    return RelationSnapshotReference(
        snapshot_id=f"RELATION_SNAPSHOT:{role}:{fact_hash}",
        snapshot_role=role,
        snapshot_fact_hash=fact_hash,
        target_utc=chain.flow.context.target_utc,
        upstream_natal_fact_hash=natal.hashes.fact_hash,
        upstream_natal_computation_hash=natal.hashes.computation_hash,
        upstream_temporal_fact_hash=chain.flow.context.upstream_temporal_fact_hash,
        source_temporal_candidate_indices=tuple(
            sorted(chain.support.source_temporal_candidate_indices)
        ),
        source_temporal_seed_ids=tuple(sorted(chain.support.source_temporal_seed_ids)),
        upstream_flow_fact_hash=chain.flow.hashes.fact_hash,
        upstream_flow_computation_hash=chain.flow.hashes.computation_hash,
        upstream_structural_fact_hash=chain.structural.hashes.fact_hash,
        upstream_structural_computation_hash=chain.structural.hashes.computation_hash,
        upstream_support_fact_hash=chain.support.hashes.fact_hash,
        upstream_support_computation_hash=chain.support.hashes.computation_hash,
        active_dayun_kind=chain.flow.context.active_dayun_kind,
        active_dayun_source_frame_id=chain.flow.context.active_dayun_frame.frame_id,
        annual_frame_id=chain.flow.context.annual_frame.frame_id,
        monthly_frame_id=chain.flow.context.monthly_frame.frame_id,
        raw_relation_ids=relation_ids,
        rule_set_id=SNAPSHOT_RULE_SET_ID,
        rule_set_version=SNAPSHOT_RULE_SET_VERSION,
        source_refs=(
            "BAZI-CHART-FOUNDATION-V1",
            "BAZI-TEMPORAL-FLOW-CONTEXT-R1",
            "BAZI-STRUCTURAL-CONTEXT-R1",
            "BAZI-STRUCTURAL-SUPPORT-FOUNDATION-R1",
        ),
    )


def _layer_participant_ids(structural: BaziStructuralCandidate, layer: str) -> tuple[str, ...]:
    return tuple(sorted(
        row.instance_id
        for row in structural.context.temporal_participant_provenance
        if row.layer == layer
    ))


def _frame_change_evidence(
    before: RelationTransitionSnapshotInputs,
    after: RelationTransitionSnapshotInputs,
) -> tuple[FrameChangeEvidence, ...]:
    frames = (
        (
            "DAYUN_FRAME_CHANGED",
            "DAYUN",
            before.flow.context.active_dayun_frame.frame_id,
            after.flow.context.active_dayun_frame.frame_id,
        ),
        (
            "ANNUAL_FRAME_CHANGED",
            "ANNUAL",
            before.flow.context.annual_frame.frame_id,
            after.flow.context.annual_frame.frame_id,
        ),
        (
            "MONTHLY_FRAME_CHANGED",
            "MONTHLY",
            before.flow.context.monthly_frame.frame_id,
            after.flow.context.monthly_frame.frame_id,
        ),
    )
    rows: list[FrameChangeEvidence] = []
    for evidence_type, layer, before_id, after_id in frames:
        if before_id == after_id:
            continue
        exited = _layer_participant_ids(before.structural, layer)
        entered = _layer_participant_ids(after.structural, layer)
        identity = object_sha256({
            "evidence_type": evidence_type,
            "before_source_frame_id": before_id,
            "after_source_frame_id": after_id,
            "exited_participant_instance_ids": exited,
            "entered_participant_instance_ids": entered,
        })
        rows.append(FrameChangeEvidence(
            evidence_id=f"FRAME_CHANGE:{evidence_type}:{identity}",
            evidence_type=evidence_type,
            participant_layer=layer,
            before_source_frame_id=before_id,
            after_source_frame_id=after_id,
            exited_participant_instance_ids=exited,
            entered_participant_instance_ids=entered,
            before_flow_fact_hash=before.flow.hashes.fact_hash,
            after_flow_fact_hash=after.flow.hashes.fact_hash,
            rule_set_id=FRAME_DIFFERENCE_RULE_SET_ID,
            rule_set_version=FRAME_DIFFERENCE_RULE_SET_VERSION,
            source_refs=(
                "BAZI-TEMPORAL-V1",
                "BAZI-TEMPORAL-FLOW-CONTEXT-R1",
                "BAZI-STRUCTURAL-CONTEXT-R1",
            ),
        ))
    return tuple(rows)


def _relation_core(row) -> tuple[Any, ...]:
    return (
        row.semantic_relation_id,
        row.relation_family,
        row.participant_instance_ids,
        row.orientation,
        row.arity,
        row.nominal_transformation_element,
        row.rule_set_id,
        row.rule_set_version,
        row.source_refs,
    )


def _participant_layers(
    participant_ids: tuple[str, ...],
    *maps: dict[str, RelationParticipantReference],
) -> tuple[str, ...]:
    active = {
        mapping[instance_id].participant_layer
        for mapping in maps
        for instance_id in participant_ids
        if instance_id in mapping
    }
    return tuple(layer for layer in LAYER_ORDER if layer in active)


def _transition_facts(
    before_snapshot: RelationSnapshotReference,
    after_snapshot: RelationSnapshotReference,
    before: RelationTransitionSnapshotInputs,
    after: RelationTransitionSnapshotInputs,
    natal: BaziChartCandidate,
    evidence: tuple[FrameChangeEvidence, ...],
) -> tuple[RawRelationTransitionFact, ...]:
    before_relations = _relation_map(natal, before.structural)
    after_relations = _relation_map(natal, after.structural)
    before_participants = _participant_map(natal, before.flow, before.structural)
    after_participants = _participant_map(natal, after.flow, after.structural)
    before_ids = set(before_relations)
    after_ids = set(after_relations)
    state_by_id = {
        **{relation_id: PERSISTING for relation_id in before_ids & after_ids},
        **{relation_id: ENTERED for relation_id in after_ids - before_ids},
        **{relation_id: EXITED for relation_id in before_ids - after_ids},
    }
    rows: list[RawRelationTransitionFact] = []
    for relation_id in sorted(state_by_id):
        state = state_by_id[relation_id]
        before_row = before_relations.get(relation_id)
        after_row = after_relations.get(relation_id)
        if before_row is not None and after_row is not None and _relation_core(before_row) != _relation_core(after_row):
            raise ValueError(f"exact relation ID changed released payload: {relation_id}")
        source = before_row or after_row
        assert source is not None
        before_provenance = tuple(
            before_participants[instance_id]
            for instance_id in source.participant_instance_ids
        ) if before_row is not None else ()
        after_provenance = tuple(
            after_participants[instance_id]
            for instance_id in source.participant_instance_ids
        ) if after_row is not None else ()
        layers = _participant_layers(
            source.participant_instance_ids,
            before_participants,
            after_participants,
        )
        changed_ids: set[str] = set()
        if state == ENTERED:
            changed_ids = {
                instance_id
                for row in evidence
                for instance_id in row.entered_participant_instance_ids
            }
        elif state == EXITED:
            changed_ids = {
                instance_id
                for row in evidence
                for instance_id in row.exited_participant_instance_ids
            }
        bound_evidence = tuple(
            row.evidence_id for row in evidence
            if set(source.participant_instance_ids) & changed_ids
            and (
                set(source.participant_instance_ids) & set(row.entered_participant_instance_ids)
                if state == ENTERED
                else set(source.participant_instance_ids) & set(row.exited_participant_instance_ids)
            )
        ) if state != PERSISTING else ()
        identity_payload = {
            "relation_id": relation_id,
            "transition_state": state,
            "before_snapshot_fact_hash": before_snapshot.snapshot_fact_hash,
            "after_snapshot_fact_hash": after_snapshot.snapshot_fact_hash,
        }
        rows.append(RawRelationTransitionFact(
            transition_fact_id=f"RELATION_TRANSITION:{object_sha256(identity_payload)}",
            relation_id=relation_id,
            semantic_relation_id=source.semantic_relation_id,
            relation_type=_relation_type(source),
            relation_family=source.relation_family,
            participant_instance_ids=source.participant_instance_ids,
            participant_layers=layers,
            occurrence_scope=(
                "NATAL_ONLY" if layers == ("NATAL",) else "INVOLVES_TEMPORAL"
            ),
            orientation=source.orientation,
            arity=source.arity,
            nominal_transformation_element=source.nominal_transformation_element,
            transition_state=state,
            before_snapshot_id=before_snapshot.snapshot_id,
            before_snapshot_fact_hash=before_snapshot.snapshot_fact_hash,
            after_snapshot_id=after_snapshot.snapshot_id,
            after_snapshot_fact_hash=after_snapshot.snapshot_fact_hash,
            before_participant_provenance=before_provenance,
            after_participant_provenance=after_provenance,
            bound_frame_change_evidence_ids=bound_evidence,
            source_relation_rule_set_id=source.rule_set_id,
            source_relation_rule_set_version=source.rule_set_version,
            transition_rule_set_id=SET_REPLAY_RULE_SET_ID,
            transition_rule_set_version=SET_REPLAY_RULE_SET_VERSION,
            source_refs=tuple(dict.fromkeys(
                source.source_refs + (
                    "BAZI-CHART-FOUNDATION-V1",
                    "BAZI-STRUCTURAL-CONTEXT-R1",
                )
            )),
        ))
    return tuple(rows)


def build_relation_transition_context(
    natal: BaziChartCandidate,
    before: RelationTransitionSnapshotInputs,
    after: RelationTransitionSnapshotInputs,
    profile: ResolvedBaziRelationTransitionProfile,
) -> BaziRelationTransitionContext:
    profile.validate()
    before_target = before.flow.context.target_utc.astimezone(timezone.utc)
    after_target = after.flow.context.target_utc.astimezone(timezone.utc)
    if before_target >= after_target:
        raise ValueError("before_target_utc must be strictly earlier than after_target_utc")
    before_snapshot = build_snapshot_reference(BEFORE, natal, before)
    after_snapshot = build_snapshot_reference(AFTER, natal, after)
    evidence = _frame_change_evidence(before, after)
    facts = _transition_facts(
        before_snapshot,
        after_snapshot,
        before,
        after,
        natal,
        evidence,
    )
    return BaziRelationTransitionContext(
        before_snapshot=before_snapshot,
        after_snapshot=after_snapshot,
        frame_change_evidence=evidence,
        transition_facts=facts,
        profile_id=profile.profile_id,
        profile_version=profile.profile_version,
        algorithm_versions={
            "transition": profile.algorithm_version,
            "snapshot": profile.snapshot_rule_set_version,
            "set_replay": profile.set_replay_rule_set_version,
            "frame_difference": profile.frame_difference_rule_set_version,
            "candidate_pairing": CANDIDATE_PAIRING_RULE_SET_VERSION,
        },
    )
