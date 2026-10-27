from __future__ import annotations

from typing import Any

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .models import (
    ClassicalEffectConstraintNode,
    ClassicalEffectGraphEdge,
    ClassicalInteractionEffectConstraintCandidate,
    ClassicalInteractionEffectConstraintGraphFragmentCandidate,
    ClassicalRelationEffectChannelReference,
    EffectConstraintMultiplicityReference,
    FragmentHashBundle,
    RawRelationReferenceNode,
)
from .profile import (
    GRAPH_EDGE_CLASSES,
    HARD_EXCLUDED_EDGE_OR_STATE_SEMANTICS,
    SOURCE_CLAIM_TO_EFFECT_FACET,
    ResolvedBaziClassicalEffectConstraintGraphProfile,
)


class EffectConstraintGraphProjectionError(ValueError):
    pass


def _multiplicity_reference(binding: Any) -> EffectConstraintMultiplicityReference:
    if binding.alternative_path_requirement != "PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS":
        raise EffectConstraintGraphProjectionError(
            f"MULTIPLICITY_PATH_PRESERVATION_CONTRACT_MISMATCH:{binding.multiplicity_constraint_id}"
        )
    if len(set(binding.exact_runtime_instance_ids)) != binding.required_symbolic_cardinality:
        raise EffectConstraintGraphProjectionError(
            f"MULTIPLICITY_EXACT_INSTANCE_CARDINALITY_MISMATCH:{binding.multiplicity_constraint_id}"
        )
    return EffectConstraintMultiplicityReference(
        multiplicity_constraint_id=binding.multiplicity_constraint_id,
        exchangeable_symbolic_slot_node_ids=binding.exchangeable_symbolic_slot_node_ids,
        exact_runtime_instance_ids=binding.exact_runtime_instance_ids,
        required_symbolic_cardinality=binding.required_symbolic_cardinality,
        slot_equivalence=binding.slot_equivalence,
        alternative_path_requirement=binding.alternative_path_requirement,
    )


def _raw_relation_node(binding_candidate: Any, exact_relation_id: str) -> RawRelationReferenceNode:
    matches = [row for row in binding_candidate.relation_bindings if row.source_relation_id == exact_relation_id]
    if len(matches) != 1:
        raise EffectConstraintGraphProjectionError(
            f"EXACT_RELATION_REFERENCE_NOT_UNIQUE_IN_BINDING:{binding_candidate.binding_candidate_id}:{exact_relation_id}:{len(matches)}"
        )
    row = matches[0]
    node_id = "RAW_RELATION_REFERENCE:" + object_sha256({
        "binding_candidate_id": binding_candidate.binding_candidate_id,
        "exact_relation_id": exact_relation_id,
    })
    return RawRelationReferenceNode(
        raw_relation_node_id=node_id,
        binding_candidate_id=binding_candidate.binding_candidate_id,
        exact_relation_id=row.source_relation_id,
        exact_semantic_relation_id=row.source_semantic_relation_id,
        relation_type=row.source_relation_type,
        relation_family=row.source_relation_family,
        participant_instance_ids=row.runtime_participant_instance_ids,
    )


def _effect_channel_id(binding_candidate_id: str, target_relation_id: str, effect_facet: str) -> str:
    return "CLASSICAL_EFFECT_CHANNEL:" + object_sha256({
        "binding_candidate_id": binding_candidate_id,
        "target_exact_relation_id": target_relation_id,
        "effect_facet": effect_facet,
    })


def _edge(
    kind: str,
    source_node_id: str,
    target_node_id: str,
    *,
    claim_id: str | None = None,
    chain_id: str | None = None,
) -> ClassicalEffectGraphEdge:
    if kind not in GRAPH_EDGE_CLASSES:
        raise EffectConstraintGraphProjectionError(f"UNRELEASED_EFFECT_GRAPH_EDGE_CLASS:{kind}")
    return ClassicalEffectGraphEdge(
        edge_id="CLASSICAL_EFFECT_GRAPH_EDGE:" + object_sha256({
            "edge_kind": kind,
            "source_node_id": source_node_id,
            "target_node_id": target_node_id,
            "source_claim_edge_id": claim_id,
            "source_chain_pattern_id": chain_id,
        }),
        edge_kind=kind,
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        source_claim_edge_id=claim_id,
        source_chain_pattern_id=chain_id,
    )


def project_effect_constraint_graph_fragment(
    bundle: Any,
    binding_candidate: Any,
    graph_record: dict[str, Any],
    graph_chain_by_id: dict[str, dict[str, Any]],
    profile: ResolvedBaziClassicalEffectConstraintGraphProfile,
    source_projection_fact_hash: str,
) -> ClassicalInteractionEffectConstraintGraphFragmentCandidate:
    if bundle.binding_candidate_id != binding_candidate.binding_candidate_id:
        raise EffectConstraintGraphProjectionError("BUNDLE_BINDING_CANDIDATE_ID_MISMATCH")
    if bundle.source_occurrence_id != binding_candidate.source_occurrence_id:
        raise EffectConstraintGraphProjectionError("BUNDLE_BINDING_SOURCE_OCCURRENCE_MISMATCH")
    if graph_record["source_occurrence_id"] != bundle.source_occurrence_id:
        raise EffectConstraintGraphProjectionError("GRAPH_RECORD_SOURCE_OCCURRENCE_MISMATCH")
    if graph_record["graph_record_id"] != bundle.graph_record_id:
        raise EffectConstraintGraphProjectionError("GRAPH_RECORD_ID_MISMATCH")
    if graph_record["source_layer"] != "SHEN_CLASSICAL_SOURCE":
        raise EffectConstraintGraphProjectionError(
            f"CROSS_SOURCE_LAYER_EFFECT_GRAPH_NOT_RELEASED:{graph_record['source_layer']}"
        )

    multiplicity_references = tuple(_multiplicity_reference(row) for row in binding_candidate.multiplicity_bindings)
    raw_relation_ids: set[str] = set()
    channel_by_coordinate: dict[tuple[str, str], ClassicalRelationEffectChannelReference] = {}
    constraint_nodes: list[ClassicalEffectConstraintNode] = []
    constraint_node_by_claim: dict[str, ClassicalEffectConstraintNode] = {}

    for claim in bundle.chart_bound_claims:
        if claim.binding_candidate_id != bundle.binding_candidate_id:
            raise EffectConstraintGraphProjectionError(f"CLAIM_BINDING_ID_MISMATCH:{claim.source_claim_edge_id}")
        facet = SOURCE_CLAIM_TO_EFFECT_FACET.get(claim.source_claim_edge_class)
        if facet is None:
            raise EffectConstraintGraphProjectionError(
                f"SOURCE_CLAIM_CLASS_NOT_RELEASED_FOR_EFFECT_GRAPH:{claim.source_claim_edge_class}"
            )
        if len(claim.target_exact_relation_ids) != 1:
            raise EffectConstraintGraphProjectionError(
                f"EFFECT_GRAPH_REQUIRES_ONE_EXACT_RELATION_TARGET:{claim.source_claim_edge_id}:{len(claim.target_exact_relation_ids)}"
            )
        target_relation_id = claim.target_exact_relation_ids[0]
        raw_relation_ids.add(target_relation_id)
        raw_relation_ids.update(claim.actor_exact_relation_ids)
        coordinate = (target_relation_id, facet)
        channel = channel_by_coordinate.get(coordinate)
        if channel is None:
            channel = ClassicalRelationEffectChannelReference(
                effect_channel_id=_effect_channel_id(bundle.binding_candidate_id, target_relation_id, facet),
                binding_candidate_id=bundle.binding_candidate_id,
                target_exact_relation_id=target_relation_id,
                effect_facet=facet,
            )
            channel_by_coordinate[coordinate] = channel

        claim_multiplicity = multiplicity_references if claim.source_claim_edge_class == "SOURCE_ASSERTED_PARTICIPANT_ALLOCATION" else ()
        if claim.source_claim_edge_class == "SOURCE_ASSERTED_PARTICIPANT_ALLOCATION" and not claim_multiplicity:
            raise EffectConstraintGraphProjectionError(
                f"PARTICIPANT_ALLOCATION_WITHOUT_EXACT_MULTIPLICITY_BINDING:{claim.source_claim_edge_id}"
            )
        constraint_id = "CLASSICAL_EFFECT_CONSTRAINT:" + object_sha256({
            "binding_candidate_id": bundle.binding_candidate_id,
            "source_claim_edge_id": claim.source_claim_edge_id,
            "target_effect_channel_id": channel.effect_channel_id,
            "actor_exact_relation_ids": claim.actor_exact_relation_ids,
            "actor_exact_participant_ids": claim.actor_exact_participant_ids,
            "context_exact_participant_ids": claim.context_exact_participant_ids,
            "multiplicity_constraint_ids": tuple(row.multiplicity_constraint_id for row in claim_multiplicity),
        })
        constraint = ClassicalInteractionEffectConstraintCandidate(
            effect_constraint_id=constraint_id,
            binding_candidate_id=bundle.binding_candidate_id,
            source_occurrence_id=bundle.source_occurrence_id,
            graph_record_id=bundle.graph_record_id,
            interaction_assertion_id=graph_record["interaction_assertion_id"],
            source_claim_edge_id=claim.source_claim_edge_id,
            source_claim_edge_class=claim.source_claim_edge_class,
            source_assertion_class=claim.source_assertion_class,
            source_evidence_mode=claim.source_evidence_mode,
            exact_source_fragments=claim.exact_source_fragments,
            target_effect_channel_id=channel.effect_channel_id,
            target_exact_relation_id=target_relation_id,
            actor_exact_relation_ids=claim.actor_exact_relation_ids,
            actor_exact_participant_ids=claim.actor_exact_participant_ids,
            context_exact_participant_ids=claim.context_exact_participant_ids,
            effect_facet=facet,
            constraint_kind=claim.source_claim_edge_class,
            structural_binding_class=bundle.structural_binding_class,
            source_scope_compatibility=bundle.source_scope_compatibility.source_scope_compatibility,
            residual_unresolved_structural_constraint_ids=bundle.residual_unresolved_structural_constraint_ids,
            unresolved_classical_semantic_requirements=claim.unresolved_classical_semantic_requirements,
            source_unresolved_graph_requirements=bundle.source_unresolved_graph_requirements,
            multiplicity_references=claim_multiplicity,
            source_narrative_chain_ids=bundle.source_interaction_chain_pattern_ids,
        )
        node = ClassicalEffectConstraintNode(
            constraint_node_id="CLASSICAL_EFFECT_CONSTRAINT_NODE:" + object_sha256(constraint_id),
            constraint=constraint,
        )
        if claim.source_claim_edge_id in constraint_node_by_claim:
            raise EffectConstraintGraphProjectionError(f"DUPLICATE_SOURCE_CLAIM_IN_FRAGMENT:{claim.source_claim_edge_id}")
        constraint_node_by_claim[claim.source_claim_edge_id] = node
        constraint_nodes.append(node)

    if len(constraint_nodes) != len(bundle.chart_bound_claims):
        raise EffectConstraintGraphProjectionError("SOURCE_CLAIM_TO_CONSTRAINT_CARDINALITY_MISMATCH")

    raw_nodes = tuple(_raw_relation_node(binding_candidate, relation_id) for relation_id in sorted(raw_relation_ids))
    raw_node_by_relation = {row.exact_relation_id: row for row in raw_nodes}
    channels = tuple(sorted(channel_by_coordinate.values(), key=lambda row: (row.target_exact_relation_id, row.effect_facet)))
    edges: list[ClassicalEffectGraphEdge] = []
    for node in constraint_nodes:
        constraint = node.constraint
        for actor_relation_id in constraint.actor_exact_relation_ids:
            raw = raw_node_by_relation.get(actor_relation_id)
            if raw is None:
                raise EffectConstraintGraphProjectionError(
                    f"ACTOR_RAW_RELATION_REFERENCE_MISSING:{constraint.source_claim_edge_id}:{actor_relation_id}"
                )
            edges.append(_edge(
                "RAW_RELATION_ACTOR_REFERENCE", raw.raw_relation_node_id, node.constraint_node_id,
                claim_id=constraint.source_claim_edge_id,
            ))
        edges.append(_edge(
            "CONSTRAINT_TARGETS_EFFECT_CHANNEL", node.constraint_node_id, constraint.target_effect_channel_id,
            claim_id=constraint.source_claim_edge_id,
        ))

    for channel in channels:
        target_raw = raw_node_by_relation.get(channel.target_exact_relation_id)
        if target_raw is None:
            raise EffectConstraintGraphProjectionError(
                f"TARGET_RAW_RELATION_REFERENCE_MISSING:{channel.target_exact_relation_id}"
            )
        edges.append(_edge(
            "EFFECT_CHANNEL_REFERENCES_RAW_RELATION", channel.effect_channel_id, target_raw.raw_relation_node_id,
        ))

    for chain_id in bundle.source_interaction_chain_pattern_ids:
        chain = graph_chain_by_id.get(chain_id)
        if chain is None:
            raise EffectConstraintGraphProjectionError(f"SOURCE_NARRATIVE_CHAIN_MISSING:{chain_id}")
        if chain["source_occurrence_id"] != bundle.source_occurrence_id:
            raise EffectConstraintGraphProjectionError(f"SOURCE_NARRATIVE_CHAIN_OCCURRENCE_MISMATCH:{chain_id}")
        if (
            chain.get("sequence_semantics") != "SOURCE_NARRATIVE_ORDER_ONLY"
            or chain.get("runtime_state_transition_emitted") is not False
            or chain.get("suppression_or_activation_emitted") is not False
        ):
            raise EffectConstraintGraphProjectionError(f"SOURCE_NARRATIVE_CHAIN_SEMANTICS_DRIFT:{chain_id}")
        ordered_claim_ids = tuple(chain["ordered_interaction_claim_edge_ids"])
        if any(claim_id not in constraint_node_by_claim for claim_id in ordered_claim_ids):
            raise EffectConstraintGraphProjectionError(f"SOURCE_NARRATIVE_CHAIN_CLAIM_NOT_PROJECTED:{chain_id}")
        for left_claim_id, right_claim_id in zip(ordered_claim_ids, ordered_claim_ids[1:]):
            edges.append(_edge(
                "SOURCE_NARRATIVE_PRECEDES",
                constraint_node_by_claim[left_claim_id].constraint_node_id,
                constraint_node_by_claim[right_claim_id].constraint_node_id,
                chain_id=chain_id,
            ))

    if any(edge.edge_kind in HARD_EXCLUDED_EDGE_OR_STATE_SEMANTICS for edge in edges):
        raise EffectConstraintGraphProjectionError("HARD_EXCLUDED_EFFECT_GRAPH_SEMANTICS_EMITTED")

    fact_payload = {
        "binding_candidate_id": bundle.binding_candidate_id,
        "source_occurrence_id": bundle.source_occurrence_id,
        "graph_record_id": bundle.graph_record_id,
        "interaction_assertion_id": graph_record["interaction_assertion_id"],
        "source_layer": graph_record["source_layer"],
        "structural_binding_class": bundle.structural_binding_class,
        "source_scope_compatibility": bundle.source_scope_compatibility.source_scope_compatibility,
        "raw_relation_reference_nodes": json_value(raw_nodes),
        "effect_channel_nodes": json_value(channels),
        "effect_constraint_nodes": json_value(tuple(constraint_nodes)),
        "graph_edges": json_value(tuple(edges)),
        "multiplicity_references": json_value(multiplicity_references),
        "residual_unresolved_structural_constraint_ids": bundle.residual_unresolved_structural_constraint_ids,
        "source_unresolved_graph_requirements": bundle.source_unresolved_graph_requirements,
        "source_narrative_chain_ids": bundle.source_interaction_chain_pattern_ids,
    }
    hashes = FragmentHashBundle(
        fact_hash=object_sha256(fact_payload),
        computation_hash=object_sha256({
            "facts": fact_payload,
            "source_projection_fact_hash": source_projection_fact_hash,
            "profile": json_value(profile),
        }),
    )
    fragment_id = "CLASSICAL_EFFECT_GRAPH_FRAGMENT:" + object_sha256({
        "binding_candidate_id": bundle.binding_candidate_id,
        "fact_hash": hashes.fact_hash,
    })
    return ClassicalInteractionEffectConstraintGraphFragmentCandidate(
        fragment_id=fragment_id,
        binding_candidate_id=bundle.binding_candidate_id,
        source_occurrence_id=bundle.source_occurrence_id,
        graph_record_id=bundle.graph_record_id,
        interaction_assertion_id=graph_record["interaction_assertion_id"],
        source_layer=graph_record["source_layer"],
        structural_binding_class=bundle.structural_binding_class,
        source_scope_compatibility=bundle.source_scope_compatibility.source_scope_compatibility,
        raw_relation_reference_nodes=raw_nodes,
        effect_channel_nodes=channels,
        effect_constraint_nodes=tuple(constraint_nodes),
        graph_edges=tuple(edges),
        multiplicity_references=multiplicity_references,
        residual_unresolved_structural_constraint_ids=bundle.residual_unresolved_structural_constraint_ids,
        source_unresolved_graph_requirements=bundle.source_unresolved_graph_requirements,
        source_narrative_chain_ids=bundle.source_interaction_chain_pattern_ids,
        hashes=hashes,
    )
