from __future__ import annotations

from dataclasses import dataclass
from datetime import timezone
from itertools import combinations
from typing import Any

from fortune_training.bazi_chart import BaziChartCandidate
from fortune_training.bazi_flow import BaziFlowCandidate
from fortune_training.bazi_structural import BaziStructuralCandidate
from fortune_training.bazi_structural_support import BaziStructuralSupportCandidate
from fortune_training.util import object_sha256

from .models import (
    BaziRelationIncidenceContext,
    IncidenceParticipantReference,
    ParticipantRelationIncidenceFact,
    RelationIncidenceSnapshot,
    RelationOccurrenceReference,
    RelationPairTopologyFact,
)
from .profile import (
    CANDIDATE_PAIRING_RULE_SET_VERSION,
    OCCURRENCE_REFERENCE_RULE_SET_ID,
    OCCURRENCE_REFERENCE_RULE_SET_VERSION,
    PAIR_TOPOLOGY_RULE_SET_ID,
    PAIR_TOPOLOGY_RULE_SET_VERSION,
    PARTICIPANT_INCIDENCE_RULE_SET_ID,
    PARTICIPANT_INCIDENCE_RULE_SET_VERSION,
    SNAPSHOT_RULE_SET_ID,
    SNAPSHOT_RULE_SET_VERSION,
    SUPPORT_TOUCH_RULE_SET_ID,
    SUPPORT_TOUCH_RULE_SET_VERSION,
    ResolvedBaziRelationIncidenceProfile,
)


SHARED_PARTICIPANT = "SHARED_PARTICIPANT"
DISJOINT = "DISJOINT"
TOPOLOGY_KINDS = (SHARED_PARTICIPANT, DISJOINT)
LAYER_ORDER = ("NATAL", "DAYUN", "ANNUAL", "MONTHLY")
NOMINAL_ONLY = "NOMINAL_TARGET_ONLY_NOT_TRANSFORMATION_SUCCESS"


@dataclass(frozen=True)
class RelationIncidenceSnapshotInputs:
    flow_index: int
    structural_index: int
    support_index: int
    flow: BaziFlowCandidate
    structural: BaziStructuralCandidate
    support: BaziStructuralSupportCandidate


def _instant_fact(value) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("incidence snapshot target must be timezone-aware")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds")


def _relation_type(row) -> str:
    if row.relation_family == "STEM_COMBINATION":
        return "STEM_FIVE_COMBINATION"
    if row.relation_family == "BRANCH_SIX_HARMONY":
        return "BRANCH_LIUHE"
    if row.relation_family == "BRANCH_CLASH":
        return "BRANCH_CHONG"
    if row.relation_family == "BRANCH_TRINE":
        return "BRANCH_SANHE_COMPLETE"
    if row.semantic_relation_id == "BRANCH.PUNISHMENT.ZI_MAO":
        return "BRANCH_ZIMAO_PUNISHMENT"
    if row.orientation == "DIRECTED":
        return "BRANCH_DIRECTIONAL_PUNISHMENT"
    if row.orientation == "SELF":
        return "BRANCH_SELF_PUNISHMENT"
    raise ValueError(f"unsupported released raw relation occurrence: {row.relation_id}")


def _released_relation_rows(
    natal: BaziChartCandidate,
    structural: BaziStructuralCandidate,
) -> tuple[tuple[str, Any], ...]:
    rows = tuple(
        ("NATAL_RELATION_CANDIDATE", row) for row in natal.chart.raw_relations
    ) + tuple(
        ("STRUCTURAL_DYNAMIC_RELATION_OCCURRENCE", row)
        for row in structural.context.dynamic_raw_relations
    )
    ids = [row.relation_id for _, row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("released Natal and Structural raw relation IDs overlap")
    return tuple(sorted(rows, key=lambda item: item[1].relation_id))


def _participant_map(
    natal: BaziChartCandidate,
    flow: BaziFlowCandidate,
    structural: BaziStructuralCandidate,
) -> dict[str, IncidenceParticipantReference]:
    pillar_by_position = {row.position: row.ganzhi for row in natal.chart.pillars}
    result: dict[str, IncidenceParticipantReference] = {}
    for row in natal.chart.stems:
        result[row.instance_id] = IncidenceParticipantReference(
            instance_id=row.instance_id,
            participant_kind="STEM",
            value=row.stem,
            participant_layer="NATAL",
            source_frame_id=None,
            source_upstream_fact_hash=natal.hashes.fact_hash,
            source_ganzhi=pillar_by_position[row.position],
        )
    for row in natal.chart.branches:
        result[row.instance_id] = IncidenceParticipantReference(
            instance_id=row.instance_id,
            participant_kind="BRANCH",
            value=row.branch,
            participant_layer="NATAL",
            source_frame_id=None,
            source_upstream_fact_hash=natal.hashes.fact_hash,
            source_ganzhi=pillar_by_position[row.position],
        )

    provenance = {
        row.instance_id: row
        for row in structural.context.temporal_participant_provenance
    }
    temporal_rows = (
        (
            (row.instance_id, "STEM", row.stem)
            for row in structural.context.active_temporal_stems
        ),
        (
            (row.instance_id, "BRANCH", row.branch)
            for row in structural.context.active_temporal_branches
        ),
    )
    for group in temporal_rows:
        for instance_id, kind, value in group:
            if instance_id in result:
                raise ValueError(f"participant instance ID overlaps Natal: {instance_id}")
            source = provenance[instance_id]
            result[instance_id] = IncidenceParticipantReference(
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
    natal: BaziChartCandidate,
    chain: RelationIncidenceSnapshotInputs,
    raw_relation_ids: tuple[str, ...],
) -> dict[str, Any]:
    return {
        "target_utc": _instant_fact(chain.flow.context.target_utc),
        "upstream_natal_fact_hash": natal.hashes.fact_hash,
        "upstream_temporal_fact_hash": chain.flow.context.upstream_temporal_fact_hash,
        "source_temporal_candidate_indices": sorted(
            chain.support.source_temporal_candidate_indices
        ),
        "source_temporal_seed_ids": sorted(chain.support.source_temporal_seed_ids),
        "upstream_flow_fact_hash": chain.flow.hashes.fact_hash,
        "upstream_structural_fact_hash": chain.structural.hashes.fact_hash,
        "upstream_support_fact_hash": chain.support.hashes.fact_hash,
        "active_dayun_kind": chain.flow.context.active_dayun_kind,
        "active_dayun_source_frame_id": chain.flow.context.active_dayun_frame.frame_id,
        "annual_frame_id": chain.flow.context.annual_frame.frame_id,
        "monthly_frame_id": chain.flow.context.monthly_frame.frame_id,
        "raw_relation_ids": list(raw_relation_ids),
    }


def build_incidence_snapshot(
    natal: BaziChartCandidate,
    chain: RelationIncidenceSnapshotInputs,
) -> RelationIncidenceSnapshot:
    relation_ids = tuple(
        row.relation_id for _, row in _released_relation_rows(natal, chain.structural)
    )
    payload = _snapshot_fact_payload(natal, chain, relation_ids)
    fact_hash = object_sha256(payload)
    return RelationIncidenceSnapshot(
        snapshot_id=f"RELATION_INCIDENCE_SNAPSHOT:{fact_hash}",
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
            "BAZI-TEMPORAL-V1",
            "BAZI-TEMPORAL-FLOW-CONTEXT-R1",
            "BAZI-STRUCTURAL-CONTEXT-R1",
            "BAZI-STRUCTURAL-SUPPORT-FOUNDATION-R1",
        ),
    )


def _relation_occurrence_references(
    natal: BaziChartCandidate,
    chain: RelationIncidenceSnapshotInputs,
    participants: dict[str, IncidenceParticipantReference],
) -> tuple[RelationOccurrenceReference, ...]:
    rows: list[RelationOccurrenceReference] = []
    for source_kind, source in _released_relation_rows(natal, chain.structural):
        provenance = tuple(
            participants[instance_id]
            for instance_id in source.participant_instance_ids
        )
        layers = tuple(
            layer
            for layer in LAYER_ORDER
            if layer in {row.participant_layer for row in provenance}
        )
        if source_kind == "NATAL_RELATION_CANDIDATE":
            relation_scope = "NATAL_ONLY"
            source_hash = natal.hashes.fact_hash
        else:
            relation_scope = source.relation_scope
            source_hash = chain.structural.hashes.fact_hash
            if tuple(source.participant_layers) != layers:
                raise ValueError(
                    f"released participant layers do not replay: {source.relation_id}"
                )
        rows.append(RelationOccurrenceReference(
            reference_id=f"RELATION_OCCURRENCE_REFERENCE:{source.relation_id}",
            relation_id=source.relation_id,
            semantic_relation_id=source.semantic_relation_id,
            relation_type=_relation_type(source),
            relation_family=source.relation_family,
            participant_instance_ids=source.participant_instance_ids,
            participant_layers=layers,
            participant_provenance=provenance,
            relation_scope=relation_scope,
            orientation=source.orientation,
            arity=source.arity,
            nominal_transformation_element=source.nominal_transformation_element,
            nominal_transformation_semantics=(
                NOMINAL_ONLY
                if source.nominal_transformation_element is not None
                else None
            ),
            source_occurrence_kind=source_kind,
            source_upstream_fact_hash=source_hash,
            source_relation_rule_set_id=source.rule_set_id,
            source_relation_rule_set_version=source.rule_set_version,
            reference_rule_set_id=OCCURRENCE_REFERENCE_RULE_SET_ID,
            reference_rule_set_version=OCCURRENCE_REFERENCE_RULE_SET_VERSION,
            source_refs=tuple(dict.fromkeys(
                source.source_refs
                + (
                    "BAZI-CHART-FOUNDATION-V1"
                    if source_kind == "NATAL_RELATION_CANDIDATE"
                    else "BAZI-STRUCTURAL-CONTEXT-R1",
                )
            )),
        ))
    return tuple(rows)


def _support_touch_ids(participant_id: str, chain: RelationIncidenceSnapshotInputs):
    return tuple(sorted(
        row.candidate_id
        for row in chain.support.context.support_evidence_candidates
        if participant_id in {
            row.visible_stem_instance_id,
            row.supporting_branch_instance_id,
        }
    ))


def _seasonal_roles(participant_id: str, chain: RelationIncidenceSnapshotInputs):
    context = chain.support.context
    rows = (
        context.natal_month_command,
        context.active_flow_solar_month,
    )
    bound = []
    for row in rows:
        source_id = getattr(
            row,
            "source_branch_instance_id",
            getattr(row, "source_temporal_branch_instance_id", None),
        )
        if participant_id == source_id:
            bound.append((row.role_id, row.reference_id))
    return (
        tuple(role_id for role_id, _ in bound),
        tuple(reference_id for _, reference_id in bound),
    )


def _participant_incidence_facts(
    snapshot: RelationIncidenceSnapshot,
    chain: RelationIncidenceSnapshotInputs,
    participants: dict[str, IncidenceParticipantReference],
    relations: tuple[RelationOccurrenceReference, ...],
) -> tuple[ParticipantRelationIncidenceFact, ...]:
    active_ids = sorted({
        instance_id
        for relation in relations
        for instance_id in relation.participant_instance_ids
    })
    rows: list[ParticipantRelationIncidenceFact] = []
    for participant_id in active_ids:
        participant = participants[participant_id]
        relation_ids = tuple(sorted(
            row.relation_id
            for row in relations
            if participant_id in row.participant_instance_ids
        ))
        relation_hashes = tuple(sorted({
            row.source_upstream_fact_hash
            for row in relations
            if participant_id in row.participant_instance_ids
        }))
        support_ids = _support_touch_ids(participant_id, chain)
        role_ids, role_reference_ids = _seasonal_roles(participant_id, chain)
        identity = object_sha256({
            "participant_instance_id": participant_id,
            "relation_ids": relation_ids,
            "snapshot_fact_hash": snapshot.snapshot_fact_hash,
        })
        rows.append(ParticipantRelationIncidenceFact(
            incidence_fact_id=f"PARTICIPANT_RELATION_INCIDENCE:{identity}",
            participant_instance_id=participant_id,
            participant_kind=participant.participant_kind,
            value=participant.value,
            participant_layer=participant.participant_layer,
            source_frame_id=participant.source_frame_id,
            source_ganzhi=participant.source_ganzhi,
            relation_ids=relation_ids,
            relation_count=len(relation_ids),
            support_evidence_candidate_ids=support_ids,
            seasonal_role_ids=role_ids,
            seasonal_role_reference_ids=role_reference_ids,
            source_participant_fact_hash=participant.source_upstream_fact_hash,
            source_relation_fact_hashes=relation_hashes,
            source_support_fact_hash=chain.support.hashes.fact_hash,
            snapshot_id=snapshot.snapshot_id,
            snapshot_fact_hash=snapshot.snapshot_fact_hash,
            rule_set_id=PARTICIPANT_INCIDENCE_RULE_SET_ID,
            rule_set_version=PARTICIPANT_INCIDENCE_RULE_SET_VERSION,
            support_touch_rule_set_id=SUPPORT_TOUCH_RULE_SET_ID,
            support_touch_rule_set_version=SUPPORT_TOUCH_RULE_SET_VERSION,
            source_refs=(
                "BAZI-CHART-FOUNDATION-V1",
                "BAZI-STRUCTURAL-CONTEXT-R1",
                "BAZI-STRUCTURAL-SUPPORT-FOUNDATION-R1",
            ),
        ))
    return tuple(rows)


def _relation_pair_topology_facts(
    snapshot: RelationIncidenceSnapshot,
    participants: dict[str, IncidenceParticipantReference],
    relations: tuple[RelationOccurrenceReference, ...],
    profile: ResolvedBaziRelationIncidenceProfile,
) -> tuple[RelationPairTopologyFact, ...]:
    rows: list[RelationPairTopologyFact] = []
    by_id = {row.relation_id: row for row in relations}
    for left_id, right_id in combinations(sorted(by_id), 2):
        left_ids = set(by_id[left_id].participant_instance_ids)
        right_ids = set(by_id[right_id].participant_instance_ids)
        shared = tuple(sorted(left_ids & right_ids))
        left_only = tuple(sorted(left_ids - right_ids))
        right_only = tuple(sorted(right_ids - left_ids))
        topology = SHARED_PARTICIPANT if shared else DISJOINT
        union_ids = tuple(sorted(left_ids | right_ids))
        identity = object_sha256({
            "relation_ids": (left_id, right_id),
            "topology_kind": topology,
            "shared_participant_instance_ids": shared,
            "source_snapshot_fact_hash": snapshot.snapshot_fact_hash,
        })
        rows.append(RelationPairTopologyFact(
            pair_fact_id=f"RELATION_PAIR_TOPOLOGY:{identity}",
            relation_ids=(left_id, right_id),
            topology_kind=topology,
            shared_participant_instance_ids=shared,
            left_only_participant_instance_ids=left_only,
            right_only_participant_instance_ids=right_only,
            participant_layer_provenance=tuple(
                participants[instance_id] for instance_id in union_ids
            ),
            source_snapshot_id=snapshot.snapshot_id,
            source_snapshot_fact_hash=snapshot.snapshot_fact_hash,
            profile_id=profile.profile_id,
            profile_version=profile.profile_version,
            rule_set_id=PAIR_TOPOLOGY_RULE_SET_ID,
            rule_set_version=PAIR_TOPOLOGY_RULE_SET_VERSION,
            source_refs=(
                "BAZI-CHART-FOUNDATION-V1",
                "BAZI-STRUCTURAL-CONTEXT-R1",
            ),
        ))
    return tuple(rows)


def build_relation_incidence_context(
    natal: BaziChartCandidate,
    chain: RelationIncidenceSnapshotInputs,
    profile: ResolvedBaziRelationIncidenceProfile,
) -> BaziRelationIncidenceContext:
    profile.validate()
    snapshot = build_incidence_snapshot(natal, chain)
    participants = _participant_map(natal, chain.flow, chain.structural)
    relations = _relation_occurrence_references(natal, chain, participants)
    incidence = _participant_incidence_facts(
        snapshot, chain, participants, relations
    )
    pairs = _relation_pair_topology_facts(
        snapshot, participants, relations, profile
    )
    return BaziRelationIncidenceContext(
        snapshot=snapshot,
        relation_occurrences=relations,
        participant_incidence_facts=incidence,
        relation_pair_topology_facts=pairs,
        profile_id=profile.profile_id,
        profile_version=profile.profile_version,
        algorithm_versions={
            "incidence": profile.algorithm_version,
            "snapshot": profile.snapshot_rule_set_version,
            "occurrence_reference": profile.occurrence_reference_rule_set_version,
            "participant_incidence": profile.participant_incidence_rule_set_version,
            "pair_topology": profile.pair_topology_rule_set_version,
            "support_touch": SUPPORT_TOUCH_RULE_SET_VERSION,
            "candidate_pairing": CANDIDATE_PAIRING_RULE_SET_VERSION,
        },
    )
