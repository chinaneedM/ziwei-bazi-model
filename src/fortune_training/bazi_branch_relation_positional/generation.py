from __future__ import annotations

from datetime import timezone
from typing import Any

from fortune_training.bazi_chart import BaziChartCandidate, BranchInstance
from fortune_training.bazi_relation_incidence import BaziRelationIncidenceCandidate
from fortune_training.bazi_structural import BaziStructuralCandidate
from fortune_training.util import object_sha256

from .models import (
    BaziBranchRelationPositionalContext,
    BranchParticipantPositionReference,
    BranchRelationPositionalFact,
    BranchRelationPositionalSnapshot,
)
from .profile import (
    CANDIDATE_LINEAGE_RULE_SET_VERSION,
    PARTICIPANT_POSITION_RULE_SET_ID,
    PARTICIPANT_POSITION_RULE_SET_VERSION,
    RELATION_POSITION_RULE_SET_ID,
    RELATION_POSITION_RULE_SET_VERSION,
    SNAPSHOT_RULE_SET_ID,
    SNAPSHOT_RULE_SET_VERSION,
    ResolvedBaziBranchRelationPositionalProfile,
)


NATAL_PILLAR = "NATAL_PILLAR"
TEMPORAL_FRAME = "TEMPORAL_FRAME"
POSITION_DOMAINS = (NATAL_PILLAR, TEMPORAL_FRAME)
NATAL_PILLAR_ORDINALS = {"YEAR": 0, "MONTH": 1, "DAY": 2, "HOUR": 3}
TEMPORAL_POSITION_TOKENS = ("DAYUN", "ANNUAL", "MONTHLY")
IN_SCOPE_RELATION_TYPES = (
    "BRANCH_LIUHE",
    "BRANCH_CHONG",
    "BRANCH_CHUAN",
    "BRANCH_SANHE_COMPLETE",
    "BRANCH_ZIMAO_PUNISHMENT",
    "BRANCH_DIRECTIONAL_PUNISHMENT",
    "BRANCH_SELF_PUNISHMENT",
)


def _instant_fact(value) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("positional snapshot target must be timezone-aware")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds")


def _in_scope_relations(incidence: BaziRelationIncidenceCandidate):
    rows = tuple(
        row for row in incidence.context.relation_occurrences
        if row.relation_type in IN_SCOPE_RELATION_TYPES
    )
    for row in rows:
        if row.arity not in (2, 3) or row.arity != len(row.participant_instance_ids):
            raise ValueError(f"invalid released branch arity: {row.relation_id}")
        if len(row.participant_provenance) != row.arity or any(
            item.participant_kind != "BRANCH" for item in row.participant_provenance
        ):
            raise ValueError(f"invalid released branch participant kind: {row.relation_id}")
        if row.relation_type == "BRANCH_SANHE_COMPLETE" and row.arity != 3:
            raise ValueError(f"complete Sanhe must retain arity 3: {row.relation_id}")
        if row.relation_type == "BRANCH_DIRECTIONAL_PUNISHMENT" and row.orientation != "DIRECTED":
            raise ValueError(f"directed punishment orientation mismatch: {row.relation_id}")
        if row.relation_type == "BRANCH_SELF_PUNISHMENT":
            values = tuple(item.value for item in row.participant_provenance)
            if row.orientation != "SELF" or row.arity != 2 or len(set(row.participant_instance_ids)) != 2 or len(set(values)) != 1:
                raise ValueError(f"self punishment identity mismatch: {row.relation_id}")
        if row.relation_type == "BRANCH_CHUAN" and (
            row.relation_family != "BRANCH_CHUAN"
            or not row.semantic_relation_id.startswith("BRANCH.CHUAN.")
            or "HARM" in row.semantic_relation_id
        ):
            raise ValueError(f"Chuan semantic identity mismatch: {row.relation_id}")
    return rows


def _branch_instances(
    natal: BaziChartCandidate,
    structural: BaziStructuralCandidate,
) -> dict[str, tuple[BranchInstance, str, str | None, str]]:
    rows: dict[str, tuple[BranchInstance, str, str | None, str]] = {}
    for branch in natal.chart.branches:
        if branch.position not in NATAL_PILLAR_ORDINALS:
            raise ValueError(f"unsupported Natal branch position: {branch.position}")
        rows[branch.instance_id] = (branch, "NATAL", None, natal.hashes.fact_hash)

    provenance = {
        row.instance_id: row
        for row in structural.context.temporal_participant_provenance
    }
    for branch in structural.context.active_temporal_branches:
        if branch.instance_id in rows:
            raise ValueError(f"temporal branch overlaps Natal identity: {branch.instance_id}")
        if branch.position not in TEMPORAL_POSITION_TOKENS:
            raise ValueError(f"unsupported temporal branch position: {branch.position}")
        source = provenance.get(branch.instance_id)
        if source is None or source.layer != branch.position or not source.source_frame_id:
            raise ValueError(f"temporal branch provenance mismatch: {branch.instance_id}")
        rows[branch.instance_id] = (
            branch,
            source.layer,
            source.source_frame_id,
            structural.hashes.fact_hash,
        )
    return rows


def _position_reference(
    branch: BranchInstance,
    participant_layer: str,
    source_frame_id: str | None,
    source_upstream_fact_hash: str,
    source_incidence_reference_ids: tuple[str, ...],
) -> BranchParticipantPositionReference:
    if participant_layer == "NATAL":
        domain = NATAL_PILLAR
        ordinal = NATAL_PILLAR_ORDINALS[branch.position]
        if source_frame_id is not None:
            raise ValueError("Natal branch cannot bind a temporal frame")
    else:
        domain = TEMPORAL_FRAME
        ordinal = None
        if branch.position != participant_layer or source_frame_id is None:
            raise ValueError(f"temporal branch frame binding mismatch: {branch.instance_id}")
    identity = object_sha256({
        "participant_instance_id": branch.instance_id,
        "source_incidence_reference_ids": source_incidence_reference_ids,
        "raw_position_token": branch.position,
        "position_domain": domain,
        "source_frame_id": source_frame_id,
    })
    return BranchParticipantPositionReference(
        reference_id=f"BRANCH_PARTICIPANT_POSITION_REFERENCE:{identity}",
        participant_instance_id=branch.instance_id,
        branch=branch.branch,
        element_affiliation=branch.element_affiliation,
        participant_layer=participant_layer,
        source_frame_id=source_frame_id,
        raw_position_token=branch.position,
        position_domain=domain,
        natal_pillar_ordinal=ordinal,
        source_upstream_fact_hash=source_upstream_fact_hash,
        source_incidence_reference_ids=source_incidence_reference_ids,
        rule_set_id=PARTICIPANT_POSITION_RULE_SET_ID,
        rule_set_version=PARTICIPANT_POSITION_RULE_SET_VERSION,
        source_refs=(
            "BAZI-CHART-FOUNDATION-V1",
            "BAZI-TEMPORAL-FLOW-CONTEXT-R1",
            "BAZI-STRUCTURAL-CONTEXT-R1",
            "BAZI-RELATION-INCIDENCE-FOUNDATION-R1",
        ),
    )


def _relation_positional_fact(
    relation,
    positions: tuple[BranchParticipantPositionReference, ...],
    incidence: BaziRelationIncidenceCandidate,
) -> BranchRelationPositionalFact:
    participant_ids = tuple(row.participant_instance_id for row in positions)
    if participant_ids != relation.participant_instance_ids or len(positions) != relation.arity:
        raise ValueError(f"position order does not match relation: {relation.relation_id}")
    all_natal = all(row.position_domain == NATAL_PILLAR for row in positions)
    ordinals = tuple(int(row.natal_pillar_ordinal) for row in positions) if all_natal else ()
    identity = object_sha256({
        "source_relation_reference_id": relation.reference_id,
        "participant_instance_ids": participant_ids,
        "participant_position_reference_ids": tuple(row.reference_id for row in positions),
        "raw_position_tokens": tuple(row.raw_position_token for row in positions),
        "position_domains": tuple(row.position_domain for row in positions),
        "participant_layers": tuple(row.participant_layer for row in positions),
        "source_frame_ids": tuple(row.source_frame_id for row in positions),
        "source_orientation": relation.orientation,
        "source_arity": relation.arity,
        "natal_pillar_ordinals": ordinals,
        "source_incidence_fact_hash": incidence.hashes.fact_hash,
    })
    return BranchRelationPositionalFact(
        positional_fact_id=f"BRANCH_RELATION_POSITIONAL_FACT:{identity}",
        source_relation_reference_id=relation.reference_id,
        source_relation_id=relation.relation_id,
        source_semantic_relation_id=relation.semantic_relation_id,
        source_relation_type=relation.relation_type,
        source_relation_family=relation.relation_family,
        participant_instance_ids=participant_ids,
        participant_position_reference_ids=tuple(row.reference_id for row in positions),
        raw_position_tokens=tuple(row.raw_position_token for row in positions),
        position_domains=tuple(row.position_domain for row in positions),
        participant_layers=tuple(row.participant_layer for row in positions),
        source_frame_ids=tuple(row.source_frame_id for row in positions),
        source_orientation=relation.orientation,
        source_arity=relation.arity,
        all_participants_natal_pillar=all_natal,
        natal_pillar_ordinals=ordinals,
        source_occurrence_kind=relation.source_occurrence_kind,
        source_occurrence_upstream_fact_hash=relation.source_upstream_fact_hash,
        source_relation_rule_set_id=relation.source_relation_rule_set_id,
        source_relation_rule_set_version=relation.source_relation_rule_set_version,
        source_incidence_snapshot_id=incidence.context.snapshot.snapshot_id,
        source_incidence_snapshot_fact_hash=incidence.context.snapshot.snapshot_fact_hash,
        source_incidence_fact_hash=incidence.hashes.fact_hash,
        rule_set_id=RELATION_POSITION_RULE_SET_ID,
        rule_set_version=RELATION_POSITION_RULE_SET_VERSION,
        source_refs=tuple(dict.fromkeys(
            relation.source_refs
            + (
                "BAZI-CHART-FOUNDATION-V1",
                "BAZI-STRUCTURAL-CONTEXT-R1",
                "BAZI-RELATION-INCIDENCE-FOUNDATION-R1",
            )
        )),
    )


def _snapshot_fact_payload(
    natal: BaziChartCandidate,
    structural: BaziStructuralCandidate,
    incidence: BaziRelationIncidenceCandidate,
) -> dict[str, Any]:
    source = incidence.context.snapshot
    return {
        "source_incidence_snapshot_id": source.snapshot_id,
        "source_incidence_snapshot_fact_hash": source.snapshot_fact_hash,
        "source_incidence_fact_hash": incidence.hashes.fact_hash,
        "source_natal_fact_hash": natal.hashes.fact_hash,
        "source_temporal_fact_hash": source.upstream_temporal_fact_hash,
        "source_flow_fact_hash": source.upstream_flow_fact_hash,
        "source_structural_fact_hash": structural.hashes.fact_hash,
        "source_support_fact_hash": source.upstream_support_fact_hash,
        "target_utc": _instant_fact(source.target_utc),
    }


def build_branch_relation_positional_context(
    natal: BaziChartCandidate,
    structural: BaziStructuralCandidate,
    incidence: BaziRelationIncidenceCandidate,
    profile: ResolvedBaziBranchRelationPositionalProfile,
) -> BaziBranchRelationPositionalContext:
    profile.validate()
    source_snapshot = incidence.context.snapshot
    snapshot_hash = object_sha256(_snapshot_fact_payload(natal, structural, incidence))
    snapshot = BranchRelationPositionalSnapshot(
        snapshot_id=f"BRANCH_RELATION_POSITIONAL_SNAPSHOT:{snapshot_hash}",
        snapshot_fact_hash=snapshot_hash,
        source_incidence_snapshot_id=source_snapshot.snapshot_id,
        source_incidence_snapshot_fact_hash=source_snapshot.snapshot_fact_hash,
        source_incidence_fact_hash=incidence.hashes.fact_hash,
        source_incidence_computation_hash=incidence.hashes.computation_hash,
        source_natal_fact_hash=natal.hashes.fact_hash,
        source_natal_computation_hash=natal.hashes.computation_hash,
        source_temporal_fact_hash=source_snapshot.upstream_temporal_fact_hash,
        source_flow_fact_hash=source_snapshot.upstream_flow_fact_hash,
        source_flow_computation_hash=source_snapshot.upstream_flow_computation_hash,
        source_structural_fact_hash=structural.hashes.fact_hash,
        source_structural_computation_hash=structural.hashes.computation_hash,
        source_support_fact_hash=source_snapshot.upstream_support_fact_hash,
        source_support_computation_hash=source_snapshot.upstream_support_computation_hash,
        target_utc=source_snapshot.target_utc,
        profile_id=profile.profile_id,
        profile_version=profile.profile_version,
        rule_set_id=SNAPSHOT_RULE_SET_ID,
        rule_set_version=SNAPSHOT_RULE_SET_VERSION,
        source_refs=(
            "BAZI-CHART-FOUNDATION-V1",
            "BAZI-TEMPORAL-FLOW-CONTEXT-R1",
            "BAZI-STRUCTURAL-CONTEXT-R1",
            "BAZI-STRUCTURAL-SUPPORT-FOUNDATION-R1",
            "BAZI-RELATION-INCIDENCE-FOUNDATION-R1",
        ),
    )

    branches = _branch_instances(natal, structural)
    relations = _in_scope_relations(incidence)
    incidence_refs_by_participant: dict[str, set[str]] = {}
    for relation in relations:
        for participant in relation.participant_instance_ids:
            incidence_refs_by_participant.setdefault(participant, set()).add(relation.reference_id)

    references: dict[str, BranchParticipantPositionReference] = {}
    facts: list[BranchRelationPositionalFact] = []
    for relation in relations:
        relation_positions = []
        for participant, provenance in zip(
            relation.participant_instance_ids,
            relation.participant_provenance,
            strict=True,
        ):
            if provenance.instance_id != participant or provenance.participant_kind != "BRANCH":
                raise ValueError(f"incidence branch provenance mismatch: {relation.relation_id}")
            if participant not in branches:
                raise ValueError(f"released branch participant is unavailable: {participant}")
            branch, layer, frame_id, _ = branches[participant]
            expected_participant_hash = (
                natal.hashes.fact_hash
                if layer == "NATAL"
                else incidence.context.snapshot.upstream_flow_fact_hash
            )
            if (
                provenance.value != branch.branch
                or provenance.participant_layer != layer
                or provenance.source_frame_id != frame_id
                or provenance.source_upstream_fact_hash != expected_participant_hash
            ):
                raise ValueError(f"incidence participant identity mismatch: {participant}")
            reference = references.get(participant)
            if reference is None:
                reference = _position_reference(
                    branch,
                    layer,
                    frame_id,
                    provenance.source_upstream_fact_hash,
                    tuple(sorted(incidence_refs_by_participant[participant])),
                )
                references[participant] = reference
            relation_positions.append(reference)
        facts.append(_relation_positional_fact(relation, tuple(relation_positions), incidence))

    return BaziBranchRelationPositionalContext(
        snapshot=snapshot,
        participant_position_references=tuple(
            sorted(references.values(), key=lambda row: row.reference_id)
        ),
        branch_relation_positional_facts=tuple(
            sorted(facts, key=lambda row: row.source_relation_id)
        ),
        profile_id=profile.profile_id,
        profile_version=profile.profile_version,
        algorithm_versions={
            "positional": profile.algorithm_version,
            "snapshot": profile.snapshot_rule_set_version,
            "participant_position": profile.participant_position_rule_set_version,
            "relation_position": profile.relation_position_rule_set_version,
            "candidate_lineage": CANDIDATE_LINEAGE_RULE_SET_VERSION,
        },
    )
