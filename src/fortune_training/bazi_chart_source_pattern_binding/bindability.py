from __future__ import annotations

from collections import Counter
from copy import deepcopy
from typing import Any

from fortune_training.util import object_sha256

from .models import SourceGraphBindabilityPlan
from .profile import ResolvedBaziChartSourcePatternBindingProfile


FULL_EXACT_BINDING_ENUMERATION = "FULL_EXACT_BINDING_ENUMERATION"
PARTIAL_EXACT_BINDING_ENUMERATION = "PARTIAL_EXACT_BINDING_ENUMERATION"
NOT_R1_EXACT_BINDABLE = "NOT_R1_EXACT_BINDABLE"

SUPPORTED_PARTICIPANT_KINDS = {
    "BRANCH_LITERAL_PATTERN",
    "STEM_LITERAL_PATTERN",
    "DAY_MASTER_STEM_PATTERN",
}
EXACT_POSITION_STATUS = "EXACT_SYMBOLIC_PARTICIPANT_PILLAR_CONSTRAINT"
UNRESOLVED_POSITION_STATUSES = {
    "SOURCE_PILLAR_CONTEXT_ONLY",
    "UNRESOLVED_SOURCE_TIME_CONTEXT",
}
EXPECTED_CLASS_COUNTS = {
    FULL_EXACT_BINDING_ENUMERATION: 11,
    PARTIAL_EXACT_BINDING_ENUMERATION: 2,
    NOT_R1_EXACT_BINDABLE: 11,
}


class BindingPlanError(ValueError):
    pass


def _index(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    result = {row[key]: row for row in rows}
    if len(result) != len(rows):
        raise BindingPlanError(f"duplicate graph object identity: {key}")
    return result


def validate_graph_identity(
    graph: dict[str, Any],
    profile: ResolvedBaziChartSourcePatternBindingProfile,
) -> None:
    profile.validate()
    determinism = graph.get("determinism", {})
    semantic_keys = (
        "participant_pattern_nodes", "position_pattern_constraints",
        "relation_pattern_nodes", "interaction_claim_edges",
        "context_inheritance_edges", "interaction_chain_patterns",
        "multiplicity_constraints",
    )
    for key in semantic_keys:
        for row in graph.get(key, []):
            if row.get("semantic_sha256") != object_sha256({name: value for name, value in row.items() if name != "semantic_sha256"}):
                raise BindingPlanError(f"GRAPH_OBJECT_SEMANTIC_HASH_MISMATCH:{key}")
    for row in graph.get("graph_records", []):
        if row.get("graph_record_sha256") != object_sha256({name: value for name, value in row.items() if name != "graph_record_sha256"}):
            raise BindingPlanError(f"GRAPH_RECORD_SEMANTIC_HASH_MISMATCH:{row.get('graph_record_id')}")
    replay = deepcopy(graph)
    replay.pop("determinism", None)
    if determinism.get("artifact_semantics_sha256") != object_sha256(replay):
        raise BindingPlanError("GRAPH_ARTIFACT_SEMANTICS_REPLAY_MISMATCH")
    if determinism.get("graph_record_hash_chain_sha256") != object_sha256([row["graph_record_sha256"] for row in graph.get("graph_records", [])]):
        raise BindingPlanError("GRAPH_RECORD_HASH_CHAIN_REPLAY_MISMATCH")
    if determinism.get("node_edge_constraint_semantics_sha256") != object_sha256([row["semantic_sha256"] for key in semantic_keys for row in graph.get(key, [])]):
        raise BindingPlanError("GRAPH_NODE_EDGE_SEMANTICS_REPLAY_MISMATCH")
    if determinism.get("artifact_semantics_sha256") != profile.graph_artifact_semantics_sha256:
        raise BindingPlanError("GRAPH_ARTIFACT_SEMANTICS_IDENTITY_MISMATCH")
    if determinism.get("graph_record_hash_chain_sha256") != profile.graph_record_hash_chain_sha256:
        raise BindingPlanError("GRAPH_RECORD_HASH_CHAIN_IDENTITY_MISMATCH")
    records = graph.get("graph_records")
    if not isinstance(records, list) or len(records) != 24:
        raise BindingPlanError("GRAPH_RECORD_UNIVERSE_MISMATCH")
    ids = [row.get("graph_record_id") for row in records]
    if len(set(ids)) != len(ids) or any(not value for value in ids):
        raise BindingPlanError("GRAPH_RECORD_ID_MULTIPLICITY_MISMATCH")


def derive_bindability_plan(
    graph: dict[str, Any],
    profile: ResolvedBaziChartSourcePatternBindingProfile,
) -> tuple[SourceGraphBindabilityPlan, ...]:
    """Derive R1 binding classes from graph objects only; claims/chains are ignored."""
    validate_graph_identity(graph, profile)
    relation_by_id = _index(graph["relation_pattern_nodes"], "relation_pattern_node_id")
    participant_by_id = _index(graph["participant_pattern_nodes"], "participant_pattern_node_id")
    position_by_id = _index(graph["position_pattern_constraints"], "position_constraint_id")
    multiplicity_by_id = _index(graph["multiplicity_constraints"], "multiplicity_constraint_id")

    plan: list[SourceGraphBindabilityPlan] = []
    for record in graph["graph_records"]:
        try:
            relations = tuple(relation_by_id[value] for value in record["relation_pattern_node_ids"])
            participants = tuple(participant_by_id[value] for value in record["participant_pattern_node_ids"])
            positions = tuple(position_by_id[value] for value in record["position_constraint_ids"])
            multiplicities = tuple(multiplicity_by_id[value] for value in record["multiplicity_constraint_ids"])
        except KeyError as exc:
            raise BindingPlanError(f"GRAPH_OBJECT_REFERENCE_MISSING:{exc}") from exc

        exact_relations = tuple(
            row for row in relations
            if row.get("pattern_resolution_status") == "EXACT_RELEASED_RELATION_PATTERN"
        )
        relation_participant_ids: set[str] = set()
        for row in exact_relations:
            paths = row.get("compatible_symbolic_participant_paths") or [
                row.get("symbolic_ordered_participant_node_ids", [])
            ]
            for path in paths:
                relation_participant_ids.update(path)
        constrained_ids = {
            value for row in positions for value in row.get("participant_pattern_node_ids", [])
        }
        needed_ids = relation_participant_ids | constrained_ids
        participant_map = {row["participant_pattern_node_id"]: row for row in participants}
        unsupported_ids = sorted(
            value for value in needed_ids
            if value not in participant_map
            or participant_map[value].get("participant_kind") not in SUPPORTED_PARTICIPANT_KINDS
        )
        nonexact_relations = tuple(
            row for row in relations
            if row.get("pattern_resolution_status") != "EXACT_RELEASED_RELATION_PATTERN"
        )
        unresolved_positions = tuple(
            row for row in positions if row.get("constraint_status") != EXACT_POSITION_STATUS
        )
        invalid_positions = tuple(
            row for row in unresolved_positions
            if row.get("constraint_status") not in UNRESOLVED_POSITION_STATUSES
        )
        invalid_multiplicity = tuple(
            row for row in multiplicities
            if row.get("required_symbolic_cardinality") != len(row.get("exchangeable_symbolic_slot_node_ids", []))
            or row.get("slot_equivalence") != "EXCHANGEABLE_SOURCE_EQUIVALENT"
            or row.get("alternative_path_requirement") != "PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS"
        )

        reasons: list[str] = []
        unresolved_ids: list[str] = []
        if not exact_relations:
            reasons.append("NO_SAFE_EXACT_RELATION_ANCHOR")
        if nonexact_relations:
            reasons.extend(
                f"NON_EXACT_RELATION_PATTERN:{row['relation_pattern_node_id']}:{row['pattern_resolution_status']}"
                for row in nonexact_relations
            )
            unresolved_ids.extend(row["relation_pattern_node_id"] for row in nonexact_relations)
        if unsupported_ids:
            reasons.extend(f"UNSUPPORTED_PARTICIPANT_DOMAIN:{value}" for value in unsupported_ids)
            unresolved_ids.extend(unsupported_ids)
        if invalid_positions:
            reasons.extend(f"UNSUPPORTED_POSITION_CONSTRAINT:{row['position_constraint_id']}" for row in invalid_positions)
            unresolved_ids.extend(row["position_constraint_id"] for row in invalid_positions)
        if invalid_multiplicity:
            reasons.extend(f"UNSUPPORTED_MULTIPLICITY_CONSTRAINT:{row['multiplicity_constraint_id']}" for row in invalid_multiplicity)
            unresolved_ids.extend(row["multiplicity_constraint_id"] for row in invalid_multiplicity)

        complete_exact_relation_substrate = bool(exact_relations) and not nonexact_relations
        if not complete_exact_relation_substrate or unsupported_ids or invalid_positions or invalid_multiplicity:
            binding_class = NOT_R1_EXACT_BINDABLE
        elif unresolved_positions:
            binding_class = PARTIAL_EXACT_BINDING_ENUMERATION
            reasons.append("SOURCE_POSITION_CONTEXT_REMAINS_UNRESOLVED")
            unresolved_ids.extend(row["position_constraint_id"] for row in unresolved_positions)
        else:
            binding_class = FULL_EXACT_BINDING_ENUMERATION

        plan.append(SourceGraphBindabilityPlan(
            graph_record_id=record["graph_record_id"],
            source_occurrence_id=record["source_occurrence_id"],
            graph_record_sha256=record["graph_record_sha256"],
            source_unresolved_graph_requirements=tuple(record["unresolved_graph_requirements"]),
            bindability_class=binding_class,
            exact_relation_pattern_node_ids=tuple(row["relation_pattern_node_id"] for row in exact_relations),
            exact_position_constraint_ids=tuple(
                row["position_constraint_id"] for row in positions
                if row.get("constraint_status") == EXACT_POSITION_STATUS
            ),
            unresolved_structural_constraint_ids=tuple(dict.fromkeys(unresolved_ids)),
            structural_reason_ids=tuple(dict.fromkeys(reasons)),
        ))

    counts = Counter(row.bindability_class for row in plan)
    if dict(counts) != EXPECTED_CLASS_COUNTS:
        raise BindingPlanError(f"BINDABILITY_PLAN_REGRESSION_MISMATCH:{dict(counts)}")
    partial_ids = tuple(row.source_occurrence_id for row in plan if row.bindability_class == PARTIAL_EXACT_BINDING_ENUMERATION)
    if partial_ids != ("ZPZQ-CL-09-007-002", "ZPZQ-CL-09-007-003"):
        raise BindingPlanError(f"PARTIAL_BINDABILITY_REGRESSION_MISMATCH:{partial_ids}")
    return tuple(plan)
