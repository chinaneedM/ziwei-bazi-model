from __future__ import annotations

from typing import Any

from fortune_training.util import object_sha256

from .models import ChartBoundSourceInteractionClaim


class ChartBoundClaimProjectionError(ValueError):
    pass


def _relation_by_pattern(binding_candidate: Any) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for binding in binding_candidate.relation_bindings:
        if binding.relation_pattern_node_id in result:
            raise ChartBoundClaimProjectionError(
                f"DUPLICATE_RELATION_PATTERN_BINDING:{binding.relation_pattern_node_id}"
            )
        result[binding.relation_pattern_node_id] = binding
    return result


def _participant_by_pattern(binding_candidate: Any) -> dict[str, tuple[str, ...]]:
    result: dict[str, tuple[str, ...]] = {}
    for binding in binding_candidate.participant_bindings:
        for node_id in binding.participant_pattern_node_ids:
            if node_id in result:
                raise ChartBoundClaimProjectionError(f"DUPLICATE_PARTICIPANT_PATTERN_BINDING:{node_id}")
            result[node_id] = binding.runtime_instance_ids
    return result


def _map_relations(
    pattern_ids: tuple[str, ...],
    relation_by_pattern: dict[str, Any],
    claim_edge_id: str,
    role: str,
) -> tuple[str, ...]:
    exact: list[str] = []
    for pattern_id in pattern_ids:
        binding = relation_by_pattern.get(pattern_id)
        if binding is None:
            raise ChartBoundClaimProjectionError(
                f"CLAIM_{role}_RELATION_PATTERN_NOT_BOUND:{claim_edge_id}:{pattern_id}"
            )
        exact.append(binding.source_relation_id)
    return tuple(exact)


def _map_participants(
    pattern_ids: tuple[str, ...],
    participant_by_pattern: dict[str, tuple[str, ...]],
    claim_edge_id: str,
    role: str,
) -> tuple[str, ...]:
    exact: list[str] = []
    for pattern_id in pattern_ids:
        values = participant_by_pattern.get(pattern_id)
        if values is None:
            raise ChartBoundClaimProjectionError(
                f"CLAIM_{role}_PARTICIPANT_PATTERN_NOT_BOUND:{claim_edge_id}:{pattern_id}"
            )
        exact.extend(values)
    return tuple(dict.fromkeys(exact))


def project_chart_bound_claims(
    binding_candidate: Any,
    graph_claim_by_id: dict[str, dict[str, Any]],
    source_unresolved_graph_requirements: tuple[str, ...],
) -> tuple[ChartBoundSourceInteractionClaim, ...]:
    relation_by_pattern = _relation_by_pattern(binding_candidate)
    participant_by_pattern = _participant_by_pattern(binding_candidate)
    rows: list[ChartBoundSourceInteractionClaim] = []
    for claim_edge_id in binding_candidate.source_interaction_claim_edge_ids:
        claim = graph_claim_by_id.get(claim_edge_id)
        if claim is None:
            raise ChartBoundClaimProjectionError(f"SOURCE_CLAIM_EDGE_MISSING:{claim_edge_id}")
        if claim["source_occurrence_id"] != binding_candidate.source_occurrence_id:
            raise ChartBoundClaimProjectionError(f"SOURCE_CLAIM_OCCURRENCE_MISMATCH:{claim_edge_id}")
        if claim["graph_record_id"] != binding_candidate.graph_record_id:
            raise ChartBoundClaimProjectionError(f"SOURCE_CLAIM_GRAPH_RECORD_MISMATCH:{claim_edge_id}")
        actor_relations = _map_relations(
            tuple(claim.get("actor_relation_pattern_node_ids", ())), relation_by_pattern, claim_edge_id, "ACTOR"
        )
        target_relations = _map_relations(
            tuple(claim.get("target_relation_pattern_node_ids", ())), relation_by_pattern, claim_edge_id, "TARGET"
        )
        actor_participants = _map_participants(
            tuple(claim.get("actor_participant_pattern_node_ids", ())), participant_by_pattern, claim_edge_id, "ACTOR"
        )
        context_participants = _map_participants(
            tuple(claim.get("context_participant_pattern_node_ids", ())), participant_by_pattern, claim_edge_id, "CONTEXT"
        )
        target_participants = _map_participants(
            tuple(claim.get("target_participant_pattern_node_ids", ())), participant_by_pattern, claim_edge_id, "TARGET"
        )
        actor_kind = claim["actor_reference_kind"]
        target_kind = claim["target_reference_kind"]
        if actor_kind == "RELATION_PATTERN_ACTOR" and not actor_relations:
            raise ChartBoundClaimProjectionError(f"RELATION_PATTERN_ACTOR_WITHOUT_EXACT_RELATION:{claim_edge_id}")
        if target_kind == "SOURCE_NAMED_RELATION_OR_EFFECT_TARGET" and not (target_relations or target_participants):
            raise ChartBoundClaimProjectionError(f"SOURCE_NAMED_TARGET_WITHOUT_EXACT_RUNTIME_TARGET:{claim_edge_id}")
        claim_hash = object_sha256({
            "binding_candidate_id": binding_candidate.binding_candidate_id,
            "source_claim_edge_id": claim_edge_id,
            "source_claim_edge_class": claim["edge_class"],
            "actor_exact_relation_ids": actor_relations,
            "actor_exact_participant_ids": actor_participants,
            "context_exact_participant_ids": context_participants,
            "target_exact_relation_ids": target_relations,
            "target_exact_participant_ids": target_participants,
        })
        rows.append(ChartBoundSourceInteractionClaim(
            chart_bound_claim_id=f"CHART_BOUND_SOURCE_INTERACTION_CLAIM:{claim_hash}",
            binding_candidate_id=binding_candidate.binding_candidate_id,
            source_occurrence_id=binding_candidate.source_occurrence_id,
            graph_record_id=binding_candidate.graph_record_id,
            source_claim_edge_id=claim_edge_id,
            source_claim_edge_class=claim["edge_class"],
            source_assertion_class=claim["source_assertion_class"],
            source_evidence_mode=claim["source_evidence_mode"],
            exact_source_fragments=tuple(claim.get("exact_source_fragments", ())),
            actor_reference_kind=actor_kind,
            actor_exact_relation_ids=actor_relations,
            actor_exact_participant_ids=actor_participants,
            context_exact_participant_ids=context_participants,
            target_reference_kind=target_kind,
            target_exact_relation_ids=target_relations,
            target_exact_participant_ids=target_participants,
            unresolved_classical_semantic_requirements=tuple(claim.get("unresolved_requirements", ())),
            residual_unresolved_structural_constraint_ids=binding_candidate.residual_unresolved_structural_constraint_ids,
            source_unresolved_graph_requirements=source_unresolved_graph_requirements,
            source_interaction_chain_pattern_ids=binding_candidate.source_interaction_chain_pattern_ids,
        ))
    if tuple(row.source_claim_edge_id for row in rows) != binding_candidate.source_interaction_claim_edge_ids:
        raise ChartBoundClaimProjectionError("CLAIM_EDGE_ONE_TO_ONE_PROJECTION_MISMATCH")
    return tuple(rows)
