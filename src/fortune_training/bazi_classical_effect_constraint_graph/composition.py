from __future__ import annotations

from collections import defaultdict

from fortune_training.util import object_sha256

from .models import (
    ClassicalInteractionEffectConstraintGraphFragmentCandidate,
    ExactEffectChannelCoordinateIndexEntry,
    ExactRawRelationConstraintReferenceIndexEntry,
    SourceLayerEffectFragmentPartition,
    SourceRecordEffectFragmentCandidateSet,
)


class EffectFragmentCompositionError(ValueError):
    pass


def build_source_layer_partitions(
    fragments: tuple[ClassicalInteractionEffectConstraintGraphFragmentCandidate, ...],
) -> tuple[SourceLayerEffectFragmentPartition, ...]:
    by_layer: dict[str, dict[str, list[str]]] = {}
    for fragment in fragments:
        layer_records = by_layer.setdefault(fragment.source_layer, {})
        layer_records.setdefault(fragment.source_occurrence_id, []).append(fragment.fragment_id)
    if set(by_layer) - {"SHEN_CLASSICAL_SOURCE"}:
        raise EffectFragmentCompositionError(
            f"CROSS_SOURCE_LAYER_COMPOSITION_NOT_RELEASED:{tuple(by_layer)}"
        )

    partitions: list[SourceLayerEffectFragmentPartition] = []
    for source_layer, source_records in by_layer.items():
        record_sets: list[SourceRecordEffectFragmentCandidateSet] = []
        for source_occurrence_id, fragment_ids in source_records.items():
            unique_ids = tuple(dict.fromkeys(fragment_ids))
            if len(unique_ids) != len(fragment_ids):
                raise EffectFragmentCompositionError(
                    f"DUPLICATE_FRAGMENT_ID_IN_SOURCE_RECORD_SET:{source_occurrence_id}"
                )
            set_id = "SOURCE_RECORD_EFFECT_FRAGMENT_CANDIDATE_SET:" + object_sha256({
                "source_layer": source_layer,
                "source_occurrence_id": source_occurrence_id,
                "fragment_ids": unique_ids,
                "member_selection_semantics": "NOT_RELEASED",
                "member_coexistence_semantics": "NOT_RELEASED",
                "member_exclusivity_semantics": "NOT_RELEASED",
            })
            record_sets.append(SourceRecordEffectFragmentCandidateSet(
                source_record_candidate_set_id=set_id,
                source_layer=source_layer,
                source_occurrence_id=source_occurrence_id,
                fragment_ids=unique_ids,
            ))
        partitions.append(SourceLayerEffectFragmentPartition(
            source_layer_partition_id="SOURCE_LAYER_EFFECT_FRAGMENT_PARTITION:" + object_sha256({
                "source_layer": source_layer,
                "source_record_candidate_set_ids": tuple(row.source_record_candidate_set_id for row in record_sets),
            }),
            source_layer=source_layer,
            source_record_candidate_sets=tuple(record_sets),
        ))
    return tuple(partitions)


def build_raw_relation_reference_index(
    fragments: tuple[ClassicalInteractionEffectConstraintGraphFragmentCandidate, ...],
) -> tuple[ExactRawRelationConstraintReferenceIndexEntry, ...]:
    fragment_ids: dict[str, set[str]] = defaultdict(set)
    actor_constraint_ids: dict[str, set[str]] = defaultdict(set)
    target_channel_ids: dict[str, set[str]] = defaultdict(set)

    for fragment in fragments:
        present_raw_relations = {row.exact_relation_id for row in fragment.raw_relation_reference_nodes}
        for relation_id in present_raw_relations:
            fragment_ids[relation_id].add(fragment.fragment_id)
        for node in fragment.effect_constraint_nodes:
            constraint = node.constraint
            for relation_id in constraint.actor_exact_relation_ids:
                if relation_id not in present_raw_relations:
                    raise EffectFragmentCompositionError(
                        f"ACTOR_INDEX_RELATION_NOT_IN_FRAGMENT:{fragment.fragment_id}:{relation_id}"
                    )
                actor_constraint_ids[relation_id].add(constraint.effect_constraint_id)
            if constraint.target_exact_relation_id not in present_raw_relations:
                raise EffectFragmentCompositionError(
                    f"TARGET_INDEX_RELATION_NOT_IN_FRAGMENT:{fragment.fragment_id}:{constraint.target_exact_relation_id}"
                )
            target_channel_ids[constraint.target_exact_relation_id].add(constraint.target_effect_channel_id)

    relation_ids = sorted(set(fragment_ids) | set(actor_constraint_ids) | set(target_channel_ids))
    return tuple(
        ExactRawRelationConstraintReferenceIndexEntry(
            exact_relation_id=relation_id,
            referencing_fragment_ids=tuple(sorted(fragment_ids[relation_id])),
            actor_constraint_ids=tuple(sorted(actor_constraint_ids[relation_id])),
            target_effect_channel_ids=tuple(sorted(target_channel_ids[relation_id])),
        )
        for relation_id in relation_ids
    )


def build_effect_channel_coordinate_index(
    fragments: tuple[ClassicalInteractionEffectConstraintGraphFragmentCandidate, ...],
) -> tuple[ExactEffectChannelCoordinateIndexEntry, ...]:
    channel_ids: dict[tuple[str, str], set[str]] = defaultdict(set)
    fragment_ids: dict[tuple[str, str], set[str]] = defaultdict(set)
    for fragment in fragments:
        for channel in fragment.effect_channel_nodes:
            coordinate = (channel.target_exact_relation_id, channel.effect_facet)
            channel_ids[coordinate].add(channel.effect_channel_id)
            fragment_ids[coordinate].add(fragment.fragment_id)
    return tuple(
        ExactEffectChannelCoordinateIndexEntry(
            exact_relation_id=relation_id,
            effect_facet=facet,
            referencing_fragment_ids=tuple(sorted(fragment_ids[(relation_id, facet)])),
            fragment_local_effect_channel_ids=tuple(sorted(channel_ids[(relation_id, facet)])),
        )
        for relation_id, facet in sorted(channel_ids)
    )
