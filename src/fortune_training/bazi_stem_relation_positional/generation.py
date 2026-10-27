from __future__ import annotations

from datetime import timezone
from typing import Any

from fortune_training.bazi_chart import BaziChartCandidate, StemInstance
from fortune_training.bazi_relation_incidence import BaziRelationIncidenceCandidate
from fortune_training.bazi_structural import BaziStructuralCandidate
from fortune_training.util import object_sha256

from .models import (
    BaziStemRelationPositionalContext,
    StemPairPositionalFact,
    StemParticipantPositionReference,
    StemRelationPositionalSnapshot,
)
from .profile import (
    CANDIDATE_LINEAGE_RULE_SET_VERSION,
    PAIR_POSITION_RULE_SET_ID,
    PAIR_POSITION_RULE_SET_VERSION,
    PARTICIPANT_POSITION_RULE_SET_ID,
    PARTICIPANT_POSITION_RULE_SET_VERSION,
    SNAPSHOT_RULE_SET_ID,
    SNAPSHOT_RULE_SET_VERSION,
    ResolvedBaziStemRelationPositionalProfile,
)


NATAL_PILLAR = "NATAL_PILLAR"
TEMPORAL_FRAME = "TEMPORAL_FRAME"
POSITION_DOMAINS = (NATAL_PILLAR, TEMPORAL_FRAME)
NATAL_PILLAR_ORDINALS = {"YEAR": 0, "MONTH": 1, "DAY": 2, "HOUR": 3}
TEMPORAL_POSITION_TOKENS = ("DAYUN", "ANNUAL", "MONTHLY")
IN_SCOPE_RELATION_TYPE = "STEM_FIVE_COMBINATION"
IN_SCOPE_RELATION_FAMILY = "STEM_COMBINATION"


def _instant_fact(value) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("positional snapshot target must be timezone-aware")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds")


def _in_scope_relations(incidence: BaziRelationIncidenceCandidate):
    return tuple(
        row for row in incidence.context.relation_occurrences
        if row.relation_type == IN_SCOPE_RELATION_TYPE
        and row.relation_family == IN_SCOPE_RELATION_FAMILY
        and row.arity == 2
        and all(item.participant_kind == "STEM" for item in row.participant_provenance)
    )


def _stem_instances(
    natal: BaziChartCandidate,
    structural: BaziStructuralCandidate,
) -> dict[str, tuple[StemInstance, str, str | None, str]]:
    rows: dict[str, tuple[StemInstance, str, str | None, str]] = {}
    for stem in natal.chart.stems:
        if stem.position not in NATAL_PILLAR_ORDINALS:
            raise ValueError(f"unsupported Natal stem position: {stem.position}")
        rows[stem.instance_id] = (stem, "NATAL", None, natal.hashes.fact_hash)

    provenance = {
        row.instance_id: row
        for row in structural.context.temporal_participant_provenance
    }
    for stem in structural.context.active_temporal_stems:
        if stem.instance_id in rows:
            raise ValueError(f"temporal stem overlaps Natal identity: {stem.instance_id}")
        if stem.position not in TEMPORAL_POSITION_TOKENS:
            raise ValueError(f"unsupported temporal stem position: {stem.position}")
        source = provenance.get(stem.instance_id)
        if source is None or source.layer != stem.position:
            raise ValueError(f"temporal stem provenance mismatch: {stem.instance_id}")
        rows[stem.instance_id] = (
            stem,
            source.layer,
            source.source_frame_id,
            structural.hashes.fact_hash,
        )
    if structural.context.dynamic_raw_relations and not rows:
        raise ValueError("dynamic relations require visible stem/branch participants")
    return rows


def _position_reference(
    stem: StemInstance,
    participant_layer: str,
    source_frame_id: str | None,
    source_upstream_fact_hash: str,
    source_incidence_reference_ids: tuple[str, ...],
    day_master_instance_id: str,
) -> StemParticipantPositionReference:
    if participant_layer == "NATAL":
        domain = NATAL_PILLAR
        ordinal = NATAL_PILLAR_ORDINALS[stem.position]
        if source_frame_id is not None:
            raise ValueError("Natal stem cannot bind a temporal frame")
    else:
        domain = TEMPORAL_FRAME
        ordinal = None
        if stem.position != participant_layer or source_frame_id is None:
            raise ValueError(f"temporal stem frame binding mismatch: {stem.instance_id}")
    identity = object_sha256({
        "participant_instance_id": stem.instance_id,
        "source_incidence_reference_ids": source_incidence_reference_ids,
        "raw_position_token": stem.position,
        "position_domain": domain,
    })
    return StemParticipantPositionReference(
        reference_id=f"STEM_PARTICIPANT_POSITION_REFERENCE:{identity}",
        participant_instance_id=stem.instance_id,
        stem=stem.stem,
        element=stem.element,
        polarity=stem.polarity,
        participant_layer=participant_layer,
        source_frame_id=source_frame_id,
        raw_position_token=stem.position,
        position_domain=domain,
        natal_pillar_ordinal=ordinal,
        is_natal_day_master_participant=(
            stem.instance_id == day_master_instance_id
            and stem.position == "DAY"
            and participant_layer == "NATAL"
        ),
        source_upstream_fact_hash=source_upstream_fact_hash,
        source_incidence_reference_ids=source_incidence_reference_ids,
        rule_set_id=PARTICIPANT_POSITION_RULE_SET_ID,
        rule_set_version=PARTICIPANT_POSITION_RULE_SET_VERSION,
        source_refs=(
            "BAZI-CHART-FOUNDATION-V1",
            "BAZI-STRUCTURAL-CONTEXT-R1",
            "BAZI-RELATION-INCIDENCE-FOUNDATION-R1",
        ),
    )


def _pair_positional_fact(
    relation,
    positions: tuple[StemParticipantPositionReference, StemParticipantPositionReference],
    natal_stems: tuple[StemInstance, ...],
    incidence: BaziRelationIncidenceCandidate,
) -> StemPairPositionalFact:
    if tuple(row.participant_instance_id for row in positions) != relation.participant_instance_ids:
        raise ValueError(f"position order does not match relation: {relation.relation_id}")
    comparable = all(row.position_domain == NATAL_PILLAR for row in positions)
    if comparable:
        ordinals = tuple(int(row.natal_pillar_ordinal) for row in positions)
        low, high = sorted(ordinals)
        distance = high - low
        interveners = tuple(
            row.instance_id
            for row in sorted(
                natal_stems,
                key=lambda item: NATAL_PILLAR_ORDINALS[item.position],
            )
            if low < NATAL_PILLAR_ORDINALS[row.position] < high
        )
    else:
        ordinals = ()
        distance = None
        interveners = ()
    day_master_ids = tuple(
        row.participant_instance_id
        for row in positions
        if row.is_natal_day_master_participant
    )
    identity = object_sha256({
        "source_relation_reference_id": relation.reference_id,
        "participant_instance_ids": relation.participant_instance_ids,
        "position_domain_pair": tuple(row.position_domain for row in positions),
        "natal_pillar_ordinals": ordinals,
        "natal_ordinal_distance": distance,
        "intervening_natal_visible_stem_instance_ids": interveners,
        "source_incidence_fact_hash": incidence.hashes.fact_hash,
    })
    return StemPairPositionalFact(
        positional_fact_id=f"STEM_PAIR_POSITIONAL_FACT:{identity}",
        source_relation_reference_id=relation.reference_id,
        source_relation_id=relation.relation_id,
        source_semantic_relation_id=relation.semantic_relation_id,
        source_relation_type=relation.relation_type,
        source_relation_family=relation.relation_family,
        participant_instance_ids=relation.participant_instance_ids,
        participant_position_reference_ids=tuple(row.reference_id for row in positions),
        position_domain_pair=tuple(row.position_domain for row in positions),
        natal_linear_order_comparable=comparable,
        natal_pillar_ordinals=ordinals,
        natal_ordinal_distance=distance,
        intervening_natal_visible_stem_instance_ids=interveners,
        contains_natal_day_master_participant=bool(day_master_ids),
        natal_day_master_participant_instance_ids=day_master_ids,
        source_incidence_snapshot_id=incidence.context.snapshot.snapshot_id,
        source_incidence_snapshot_fact_hash=incidence.context.snapshot.snapshot_fact_hash,
        source_incidence_fact_hash=incidence.hashes.fact_hash,
        rule_set_id=PAIR_POSITION_RULE_SET_ID,
        rule_set_version=PAIR_POSITION_RULE_SET_VERSION,
        source_refs=(
            "BAZI-CHART-FOUNDATION-V1",
            "BAZI-STRUCTURAL-CONTEXT-R1",
            "BAZI-RELATION-INCIDENCE-FOUNDATION-R1",
        ),
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


def build_stem_relation_positional_context(
    natal: BaziChartCandidate,
    structural: BaziStructuralCandidate,
    incidence: BaziRelationIncidenceCandidate,
    profile: ResolvedBaziStemRelationPositionalProfile,
) -> BaziStemRelationPositionalContext:
    profile.validate()
    source_snapshot = incidence.context.snapshot
    payload = _snapshot_fact_payload(natal, structural, incidence)
    snapshot_hash = object_sha256(payload)
    snapshot = StemRelationPositionalSnapshot(
        snapshot_id=f"STEM_RELATION_POSITIONAL_SNAPSHOT:{snapshot_hash}",
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

    stems = _stem_instances(natal, structural)
    natal_day_rows = tuple(row for row in natal.chart.stems if row.position == "DAY")
    if len(natal_day_rows) != 1 or natal_day_rows[0].instance_id != "DAY.STEM":
        raise ValueError("exact Natal Day-Master identity DAY.STEM is required")
    day_master_id = natal_day_rows[0].instance_id
    relations = _in_scope_relations(incidence)
    reference_ids_by_participant: dict[str, set[str]] = {}
    for relation in relations:
        for participant in relation.participant_instance_ids:
            reference_ids_by_participant.setdefault(participant, set()).add(
                relation.reference_id
            )
    references: dict[str, StemParticipantPositionReference] = {}
    pairs: list[StemPairPositionalFact] = []
    for relation in relations:
        relation_positions = []
        for participant, provenance in zip(
            relation.participant_instance_ids,
            relation.participant_provenance,
            strict=True,
        ):
            if provenance.instance_id != participant or provenance.participant_kind != "STEM":
                raise ValueError(f"incidence stem provenance mismatch: {relation.relation_id}")
            if participant not in stems:
                raise ValueError(f"released stem participant is unavailable: {participant}")
            stem, layer, frame_id, source_hash = stems[participant]
            if (
                provenance.value != stem.stem
                or provenance.participant_layer != layer
                or provenance.source_frame_id != frame_id
            ):
                raise ValueError(f"incidence participant identity mismatch: {participant}")
            reference = references.get(participant)
            if reference is None:
                reference = _position_reference(
                    stem,
                    layer,
                    frame_id,
                    source_hash,
                    tuple(sorted(reference_ids_by_participant[participant])),
                    day_master_id,
                )
                references[participant] = reference
            relation_positions.append(reference)
        pairs.append(_pair_positional_fact(
            relation,
            tuple(relation_positions),
            natal.chart.stems,
            incidence,
        ))

    return BaziStemRelationPositionalContext(
        snapshot=snapshot,
        participant_position_references=tuple(
            sorted(references.values(), key=lambda row: row.reference_id)
        ),
        stem_pair_positional_facts=tuple(
            sorted(pairs, key=lambda row: row.source_relation_id)
        ),
        profile_id=profile.profile_id,
        profile_version=profile.profile_version,
        algorithm_versions={
            "positional": profile.algorithm_version,
            "snapshot": profile.snapshot_rule_set_version,
            "participant_position": profile.participant_position_rule_set_version,
            "pair_position": profile.pair_position_rule_set_version,
            "candidate_lineage": CANDIDATE_LINEAGE_RULE_SET_VERSION,
        },
    )
