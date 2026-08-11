from __future__ import annotations

from collections import defaultdict
from typing import Any

from fortune_training.util import object_sha256

from .models import (
    BindingScopedNeutralObservationBundle,
    BoundParticipantIdentityObservation,
    BoundParticipantIncidenceObservation,
    BoundRelationIdentityObservation,
    BoundRelationPairTopologyObservation,
    BoundTemporalLayerFrameObservation,
)


EXACT_RAW_RELATION_OCCURRENCE_IDENTITY = "EXACT_RAW_RELATION_OCCURRENCE_IDENTITY"
EXACT_PARTICIPANT_INSTANCE_IDENTITY = "EXACT_PARTICIPANT_INSTANCE_IDENTITY"
RELATION_INCIDENCE_DEGREE = "RELATION_INCIDENCE_DEGREE"
RELATION_PAIR_TOPOLOGY = "RELATION_PAIR_TOPOLOGY"
EXACT_TEMPORAL_LAYER_FRAME = "EXACT_TEMPORAL_LAYER_FRAME"
RELATION_TRANSITION_SET_CHANGE = "RELATION_TRANSITION_SET_CHANGE"
SUPPORTED_NEUTRAL_PRIMITIVES = {
    EXACT_RAW_RELATION_OCCURRENCE_IDENTITY,
    EXACT_PARTICIPANT_INSTANCE_IDENTITY,
    RELATION_INCIDENCE_DEGREE,
    RELATION_PAIR_TOPOLOGY,
    EXACT_TEMPORAL_LAYER_FRAME,
}


class NeutralObservationError(ValueError):
    pass


def matrix_dependency_primitives(matrix_record: dict[str, Any]) -> tuple[str, ...]:
    primitives = tuple(row["primitive"] for row in matrix_record.get("neutral_runtime_dependency_map", ()))
    if len(set(primitives)) != len(primitives):
        raise NeutralObservationError(
            f"MATRIX_NEUTRAL_PRIMITIVE_DUPLICATE:{matrix_record.get('source_occurrence_id')}"
        )
    if RELATION_TRANSITION_SET_CHANGE in primitives:
        raise NeutralObservationError(
            f"RELATION_TRANSITION_OBSERVATION_NOT_SUPPORTED_R1:{matrix_record.get('source_occurrence_id')}"
        )
    unsupported = tuple(sorted(set(primitives) - SUPPORTED_NEUTRAL_PRIMITIVES))
    if unsupported:
        raise NeutralObservationError(f"UNSUPPORTED_NEUTRAL_PRIMITIVE:{unsupported}")
    return primitives


def _pattern_to_relation(binding_candidate: Any) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for binding in binding_candidate.relation_bindings:
        if binding.relation_pattern_node_id in rows:
            raise NeutralObservationError(
                f"DUPLICATE_EXACT_RELATION_PATTERN_BINDING:{binding.relation_pattern_node_id}"
            )
        rows[binding.relation_pattern_node_id] = binding
    return rows


def _pattern_to_participant_instances(binding_candidate: Any) -> dict[str, tuple[str, ...]]:
    rows: dict[str, tuple[str, ...]] = {}
    for binding in binding_candidate.participant_bindings:
        for node_id in binding.participant_pattern_node_ids:
            if node_id in rows:
                raise NeutralObservationError(f"DUPLICATE_EXACT_PARTICIPANT_PATTERN_BINDING:{node_id}")
            rows[node_id] = tuple(binding.runtime_instance_ids)
    return rows


def _claim_scoped_topology_pairs(
    binding_candidate: Any,
    graph_claim_by_id: dict[str, dict[str, Any]],
) -> dict[tuple[str, str], set[str]]:
    relation_by_pattern = _pattern_to_relation(binding_candidate)
    referenced_pairs: dict[tuple[str, str], set[str]] = defaultdict(set)
    for claim_edge_id in binding_candidate.source_interaction_claim_edge_ids:
        claim = graph_claim_by_id.get(claim_edge_id)
        if claim is None:
            raise NeutralObservationError(f"SOURCE_CLAIM_EDGE_MISSING:{claim_edge_id}")
        actor_patterns = tuple(claim.get("actor_relation_pattern_node_ids", ()))
        target_patterns = tuple(claim.get("target_relation_pattern_node_ids", ()))
        for actor_pattern in actor_patterns:
            actor = relation_by_pattern.get(actor_pattern)
            if actor is None:
                raise NeutralObservationError(f"CLAIM_ACTOR_RELATION_NOT_EXACTLY_BOUND:{claim_edge_id}:{actor_pattern}")
            for target_pattern in target_patterns:
                target = relation_by_pattern.get(target_pattern)
                if target is None:
                    raise NeutralObservationError(f"CLAIM_TARGET_RELATION_NOT_EXACTLY_BOUND:{claim_edge_id}:{target_pattern}")
                if actor.source_relation_id == target.source_relation_id:
                    raise NeutralObservationError(f"CLAIM_TOPOLOGY_SELF_PAIR_NOT_SUPPORTED:{claim_edge_id}")
                pair = tuple(sorted((actor.source_relation_id, target.source_relation_id)))
                referenced_pairs[pair].add(claim_edge_id)
    return referenced_pairs


def materialize_neutral_observation_bundle(
    binding_candidate: Any,
    matrix_record: dict[str, Any],
    graph_claim_by_id: dict[str, dict[str, Any]],
    incidence_candidate: Any,
) -> BindingScopedNeutralObservationBundle:
    primitives = matrix_dependency_primitives(matrix_record)
    relation_observations: list[BoundRelationIdentityObservation] = []
    participant_observations: list[BoundParticipantIdentityObservation] = []
    topology_observations: list[BoundRelationPairTopologyObservation] = []
    incidence_observations: list[BoundParticipantIncidenceObservation] = []
    temporal_observations: list[BoundTemporalLayerFrameObservation] = []

    if EXACT_RAW_RELATION_OCCURRENCE_IDENTITY in primitives:
        for binding in binding_candidate.relation_bindings:
            relation_observations.append(BoundRelationIdentityObservation(
                observation_id=f"BOUND_RELATION_IDENTITY:{binding_candidate.binding_candidate_id}:{binding.relation_pattern_node_id}",
                relation_pattern_node_id=binding.relation_pattern_node_id,
                exact_relation_id=binding.source_relation_id,
                exact_semantic_relation_id=binding.source_semantic_relation_id,
                relation_type=binding.source_relation_type,
                relation_family=binding.source_relation_family,
                participant_instance_ids=binding.runtime_participant_instance_ids,
                source_relation_reference_id=binding.source_relation_reference_id,
                positional_fact_id=binding.positional_fact_id,
            ))
        if not relation_observations:
            raise NeutralObservationError(f"REQUIRED_RELATION_IDENTITY_UNAVAILABLE:{binding_candidate.binding_candidate_id}")

    if EXACT_PARTICIPANT_INSTANCE_IDENTITY in primitives:
        for binding in binding_candidate.participant_bindings:
            participant_observations.append(BoundParticipantIdentityObservation(
                observation_id=(
                    f"BOUND_PARTICIPANT_IDENTITY:{binding_candidate.binding_candidate_id}:"
                    f"{object_sha256((binding.participant_pattern_node_ids, binding.runtime_instance_ids))}"
                ),
                participant_pattern_node_ids=binding.participant_pattern_node_ids,
                participant_kind=binding.participant_kind,
                literal_value=binding.literal_value,
                exact_participant_instance_ids=binding.runtime_instance_ids,
            ))
        if not participant_observations:
            raise NeutralObservationError(f"REQUIRED_PARTICIPANT_IDENTITY_UNAVAILABLE:{binding_candidate.binding_candidate_id}")

    if RELATION_PAIR_TOPOLOGY in primitives:
        requested_pairs = _claim_scoped_topology_pairs(binding_candidate, graph_claim_by_id)
        if not requested_pairs:
            raise NeutralObservationError(f"REQUIRED_CLAIM_SCOPED_TOPOLOGY_PAIR_UNAVAILABLE:{binding_candidate.binding_candidate_id}")
        topology_by_pair: dict[tuple[str, str], Any] = {}
        for fact in incidence_candidate.context.relation_pair_topology_facts:
            pair = tuple(sorted(fact.relation_ids))
            if pair in requested_pairs:
                if pair in topology_by_pair and topology_by_pair[pair] != fact:
                    raise NeutralObservationError(f"TOPOLOGY_PAIR_FACT_COLLISION:{pair}")
                topology_by_pair[pair] = fact
        for pair, claim_edge_ids in sorted(requested_pairs.items()):
            fact = topology_by_pair.get(pair)
            if fact is None:
                raise NeutralObservationError(f"REQUIRED_CLAIM_SCOPED_TOPOLOGY_FACT_UNAVAILABLE:{pair}")
            topology_observations.append(BoundRelationPairTopologyObservation(
                observation_id=f"BOUND_RELATION_PAIR_TOPOLOGY:{binding_candidate.binding_candidate_id}:{fact.pair_fact_id}",
                pair_fact_id=fact.pair_fact_id,
                exact_relation_ids=tuple(fact.relation_ids),
                topology_kind=fact.topology_kind,
                shared_participant_instance_ids=fact.shared_participant_instance_ids,
                left_only_participant_instance_ids=fact.left_only_participant_instance_ids,
                right_only_participant_instance_ids=fact.right_only_participant_instance_ids,
                referencing_claim_edge_ids=tuple(sorted(claim_edge_ids)),
            ))

    if RELATION_INCIDENCE_DEGREE in primitives:
        participant_ids = {
            instance_id
            for binding in binding_candidate.participant_bindings
            for instance_id in binding.runtime_instance_ids
        }
        incidence_by_participant = {
            fact.participant_instance_id: fact
            for fact in incidence_candidate.context.participant_incidence_facts
            if fact.participant_instance_id in participant_ids
        }
        if not incidence_by_participant:
            raise NeutralObservationError(f"REQUIRED_PARTICIPANT_INCIDENCE_UNAVAILABLE:{binding_candidate.binding_candidate_id}")
        for participant_id in sorted(incidence_by_participant):
            fact = incidence_by_participant[participant_id]
            if fact.relation_count != len(fact.relation_ids):
                raise NeutralObservationError(f"INCIDENCE_COUNT_REPLAY_MISMATCH:{fact.incidence_fact_id}")
            incidence_observations.append(BoundParticipantIncidenceObservation(
                observation_id=f"BOUND_PARTICIPANT_INCIDENCE:{binding_candidate.binding_candidate_id}:{fact.incidence_fact_id}",
                incidence_fact_id=fact.incidence_fact_id,
                participant_instance_id=fact.participant_instance_id,
                relation_ids=fact.relation_ids,
                relation_count=fact.relation_count,
            ))

    if EXACT_TEMPORAL_LAYER_FRAME in primitives:
        for binding in binding_candidate.participant_bindings:
            if not (
                len(binding.runtime_instance_ids)
                == len(binding.participant_layers)
                == len(binding.source_frame_ids)
                == len(binding.position_reference_ids)
            ):
                raise NeutralObservationError(
                    f"TEMPORAL_OBSERVATION_PARTICIPANT_CARDINALITY_MISMATCH:{binding_candidate.binding_candidate_id}"
                )
            for instance_id, layer, frame_id, position_reference_id in zip(
                binding.runtime_instance_ids,
                binding.participant_layers,
                binding.source_frame_ids,
                binding.position_reference_ids,
                strict=True,
            ):
                temporal_observations.append(BoundTemporalLayerFrameObservation(
                    observation_id=(
                        f"BOUND_TEMPORAL_LAYER_FRAME:{binding_candidate.binding_candidate_id}:"
                        f"{object_sha256((instance_id, layer, frame_id, position_reference_id))}"
                    ),
                    participant_instance_id=instance_id,
                    participant_layer=layer,
                    source_frame_id=frame_id,
                    position_reference_id=position_reference_id,
                ))
        if not temporal_observations:
            raise NeutralObservationError(f"REQUIRED_TEMPORAL_LAYER_FRAME_UNAVAILABLE:{binding_candidate.binding_candidate_id}")

    bundle_hash = object_sha256({
        "binding_candidate_id": binding_candidate.binding_candidate_id,
        "source_occurrence_id": binding_candidate.source_occurrence_id,
        "required_neutral_primitives": primitives,
        "relation_identity_observation_ids": tuple(row.observation_id for row in relation_observations),
        "participant_identity_observation_ids": tuple(row.observation_id for row in participant_observations),
        "topology_observation_ids": tuple(row.observation_id for row in topology_observations),
        "incidence_observation_ids": tuple(row.observation_id for row in incidence_observations),
        "temporal_observation_ids": tuple(row.observation_id for row in temporal_observations),
    })
    return BindingScopedNeutralObservationBundle(
        observation_bundle_id=f"BINDING_SCOPED_NEUTRAL_OBSERVATION:{bundle_hash}",
        binding_candidate_id=binding_candidate.binding_candidate_id,
        source_occurrence_id=binding_candidate.source_occurrence_id,
        required_neutral_primitives=primitives,
        relation_identity_observations=tuple(relation_observations),
        participant_identity_observations=tuple(participant_observations),
        relation_pair_topology_observations=tuple(topology_observations),
        participant_incidence_observations=tuple(incidence_observations),
        temporal_layer_frame_observations=tuple(temporal_observations),
    )
