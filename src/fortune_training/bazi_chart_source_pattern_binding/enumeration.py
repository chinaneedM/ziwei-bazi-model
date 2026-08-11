from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
from typing import Any

from fortune_training.bazi_branch_relation_positional import BaziBranchRelationPositionalCandidate
from fortune_training.bazi_chart import BaziChartCandidate
from fortune_training.bazi_relation_incidence import BaziRelationIncidenceCandidate
from fortune_training.bazi_stem_relation_positional import BaziStemRelationPositionalCandidate
from fortune_training.util import object_sha256

from .bindability import (
    FULL_EXACT_BINDING_ENUMERATION,
    NOT_R1_EXACT_BINDABLE,
    PARTIAL_EXACT_BINDING_ENUMERATION,
)
from .models import (
    ChartSpecificExactBindingCandidate,
    SourceGraphBindabilityPlan,
    SourceGraphBindingInventory,
    SourceMultiplicityExactBinding,
    SourceParticipantExactBinding,
    SourcePositionConstraintExactBinding,
    SourceRelationExactBinding,
)


@dataclass(frozen=True)
class _RuntimeParticipant:
    instance_id: str
    kind: str
    value: str
    position_reference_id: str
    participant_layer: str
    source_frame_id: str | None
    raw_position_token: str
    is_natal_day_master: bool = False


@dataclass(frozen=True)
class _RelationOption:
    binding: SourceRelationExactBinding
    assignments: tuple[tuple[str, str], ...]


def _graph_indices(graph: dict[str, Any]):
    return (
        {row["graph_record_id"]: row for row in graph["graph_records"]},
        {row["relation_pattern_node_id"]: row for row in graph["relation_pattern_nodes"]},
        {row["participant_pattern_node_id"]: row for row in graph["participant_pattern_nodes"]},
        {row["position_constraint_id"]: row for row in graph["position_pattern_constraints"]},
        {row["multiplicity_constraint_id"]: row for row in graph["multiplicity_constraints"]},
    )


def _runtime_participants(
    natal: BaziChartCandidate,
    branch: BaziBranchRelationPositionalCandidate,
    stem: BaziStemRelationPositionalCandidate,
) -> dict[str, _RuntimeParticipant]:
    rows: dict[str, _RuntimeParticipant] = {}
    for row in branch.context.participant_position_references:
        rows[row.participant_instance_id] = _RuntimeParticipant(
            row.participant_instance_id, "BRANCH", row.branch, row.reference_id,
            row.participant_layer, row.source_frame_id, row.raw_position_token,
        )
    for row in stem.context.participant_position_references:
        rows[row.participant_instance_id] = _RuntimeParticipant(
            row.participant_instance_id, "STEM", row.stem, row.reference_id,
            row.participant_layer, row.source_frame_id, row.raw_position_token,
            row.is_natal_day_master_participant,
        )
    for row in natal.chart.branches:
        rows.setdefault(row.instance_id, _RuntimeParticipant(
            row.instance_id, "BRANCH", row.branch, f"NATAL_INSTANCE:{row.instance_id}",
            "NATAL", None, row.position,
        ))
    for row in natal.chart.stems:
        rows.setdefault(row.instance_id, _RuntimeParticipant(
            row.instance_id, "STEM", row.stem, f"NATAL_INSTANCE:{row.instance_id}",
            "NATAL", None, row.position, row.position == "DAY",
        ))
    return rows


def _participant_matches(node: dict[str, Any], runtime: _RuntimeParticipant) -> bool:
    kind = node["participant_kind"]
    if kind == "BRANCH_LITERAL_PATTERN":
        return runtime.kind == "BRANCH" and runtime.value == node["literal_value"]
    if kind == "STEM_LITERAL_PATTERN":
        return runtime.kind == "STEM" and runtime.value == node["literal_value"]
    if kind == "DAY_MASTER_STEM_PATTERN":
        return runtime.kind == "STEM" and runtime.value == node["literal_value"] and runtime.is_natal_day_master
    return False


def _relation_options(
    relation_node: dict[str, Any],
    participant_nodes: dict[str, dict[str, Any]],
    incidence: BaziRelationIncidenceCandidate,
    branch: BaziBranchRelationPositionalCandidate,
    stem: BaziStemRelationPositionalCandidate,
    runtime: dict[str, _RuntimeParticipant],
) -> tuple[_RelationOption, ...]:
    occurrence_by_ref = {row.reference_id: row for row in incidence.context.relation_occurrences}
    positional_facts = list(branch.context.branch_relation_positional_facts) + list(stem.context.stem_pair_positional_facts)
    matches = [
        row for row in positional_facts
        if row.source_semantic_relation_id == relation_node["released_neutral_semantic_relation_id"]
    ]
    paths = relation_node.get("compatible_symbolic_participant_paths") or [
        relation_node.get("symbolic_ordered_participant_node_ids", [])
    ]
    options: list[_RelationOption] = []
    for fact in matches:
        occurrence = occurrence_by_ref.get(fact.source_relation_reference_id)
        if occurrence is None:
            raise ValueError(f"POSITIONAL_RELATION_WITHOUT_INCIDENCE_ROOT:{fact.positional_fact_id}")
        expected = (
            fact.source_relation_id,
            fact.source_semantic_relation_id,
            fact.source_relation_type,
            fact.source_relation_family,
            fact.source_orientation,
            fact.source_arity,
            fact.participant_instance_ids,
        )
        actual = (
            occurrence.relation_id,
            occurrence.semantic_relation_id,
            occurrence.relation_type,
            occurrence.relation_family,
            occurrence.orientation,
            occurrence.arity,
            occurrence.participant_instance_ids,
        )
        if expected != actual:
            raise ValueError(f"POSITIONAL_INCIDENCE_RELATION_REPLAY_MISMATCH:{fact.positional_fact_id}")
        if (
            fact.source_relation_family != relation_node["released_neutral_relation_family"]
            or fact.source_arity != relation_node["source_arity"]
            or fact.source_orientation != relation_node["source_orientation"]
        ):
            continue
        if fact.source_relation_type == "BRANCH_CHUAN" and fact.source_relation_family != "BRANCH_CHUAN":
            raise ValueError("CHUAN_HARM_SEMANTIC_LEAKAGE")
        ordered_instances = fact.participant_instance_ids
        if fact.source_orientation == "DIRECTED":
            instance_orders = (ordered_instances,)
        else:
            instance_orders = tuple(dict.fromkeys(permutations(ordered_instances)))
        for path in paths:
            if len(path) != fact.source_arity:
                raise ValueError(f"SOURCE_RELATION_PATH_ARITY_MISMATCH:{relation_node['relation_pattern_node_id']}")
            for instance_order in instance_orders:
                if any(value not in runtime for value in instance_order):
                    raise ValueError(f"POSITIONAL_PARTICIPANT_REFERENCE_MISSING:{fact.positional_fact_id}")
                if not all(_participant_matches(participant_nodes[node_id], runtime[instance_id]) for node_id, instance_id in zip(path, instance_order, strict=True)):
                    continue
                position_by_instance = {
                    instance_id: reference_id
                    for instance_id, reference_id in zip(
                        fact.participant_instance_ids,
                        fact.participant_position_reference_ids,
                        strict=True,
                    )
                }
                options.append(_RelationOption(
                    SourceRelationExactBinding(
                        relation_pattern_node_id=relation_node["relation_pattern_node_id"],
                        source_relation_reference_id=fact.source_relation_reference_id,
                        source_relation_id=fact.source_relation_id,
                        source_semantic_relation_id=fact.source_semantic_relation_id,
                        positional_fact_id=fact.positional_fact_id,
                        source_relation_type=fact.source_relation_type,
                        source_relation_family=fact.source_relation_family,
                        source_orientation=fact.source_orientation,
                        source_arity=fact.source_arity,
                        source_participant_pattern_path=tuple(path),
                        runtime_participant_instance_ids=tuple(instance_order),
                        participant_position_reference_ids=tuple(position_by_instance[value] for value in instance_order),
                        source_evidence_mode=relation_node["source_evidence_mode"],
                    ),
                    tuple(zip(path, instance_order, strict=True)),
                ))
    return tuple(options)


def _merge_assignments(
    selected: tuple[_RelationOption, ...],
) -> dict[str, str] | None:
    result: dict[str, str] = {}
    for option in selected:
        for node_id, instance_id in option.assignments:
            previous = result.get(node_id)
            if previous is not None and previous != instance_id:
                return None
            result[node_id] = instance_id
    return result


def _apply_exact_positions(
    assignments: dict[str, str],
    positions: tuple[dict[str, Any], ...],
    participant_nodes: dict[str, dict[str, Any]],
    natal: BaziChartCandidate,
    runtime: dict[str, _RuntimeParticipant],
) -> tuple[dict[str, str], tuple[SourcePositionConstraintExactBinding, ...]] | None:
    result = dict(assignments)
    bindings: list[SourcePositionConstraintExactBinding] = []
    natal_stems = {row.position: row.instance_id for row in natal.chart.stems}
    natal_branches = {row.position: row.instance_id for row in natal.chart.branches}
    for position in positions:
        node_ids = tuple(position["participant_pattern_node_ids"])
        if position["constraint_status"] != "EXACT_SYMBOLIC_PARTICIPANT_PILLAR_CONSTRAINT":
            bindings.append(SourcePositionConstraintExactBinding(
                position["position_constraint_id"], position["constraint_status"],
                position["evidence_mode"], position.get("natal_pillar"), node_ids,
                (), (), (), "SOURCE_POSITION_CONTEXT_UNRESOLVED",
            ))
            continue
        pillar = position["natal_pillar"]
        runtime_ids: list[str] = []
        for node_id in node_ids:
            node = participant_nodes[node_id]
            target = natal_branches[pillar] if node["participant_kind"] == "BRANCH_LITERAL_PATTERN" else natal_stems[pillar]
            if not _participant_matches(node, runtime[target]):
                return None
            previous = result.get(node_id)
            if previous is not None and previous != target:
                return None
            result[node_id] = target
            runtime_ids.append(target)
        refs = tuple(runtime[value].position_reference_id for value in runtime_ids)
        bindings.append(SourcePositionConstraintExactBinding(
            position["position_constraint_id"], position["constraint_status"],
            position["evidence_mode"], pillar, node_ids, tuple(runtime_ids), refs,
            tuple(runtime[value].raw_position_token for value in runtime_ids),
            "EXACT_COORDINATE_EQUALITY_REPLAYED",
        ))
    return result, tuple(bindings)


def _multiplicity_bindings(
    assignments: dict[str, str],
    constraints: tuple[dict[str, Any], ...],
) -> tuple[SourceMultiplicityExactBinding, ...] | None:
    rows: list[SourceMultiplicityExactBinding] = []
    for constraint in constraints:
        node_ids = tuple(constraint["exchangeable_symbolic_slot_node_ids"])
        if any(value not in assignments for value in node_ids):
            return None
        instance_ids = tuple(sorted(assignments[value] for value in node_ids))
        if len(set(instance_ids)) != constraint["required_symbolic_cardinality"]:
            return None
        rows.append(SourceMultiplicityExactBinding(
            constraint["multiplicity_constraint_id"], node_ids, instance_ids,
            constraint["required_symbolic_cardinality"], constraint["slot_equivalence"],
            constraint["alternative_path_requirement"],
        ))
    return tuple(rows)


def _participant_bindings(
    assignments: dict[str, str],
    participant_nodes: dict[str, dict[str, Any]],
    multiplicities: tuple[dict[str, Any], ...],
    runtime: dict[str, _RuntimeParticipant],
) -> tuple[SourceParticipantExactBinding, ...]:
    grouped_nodes = {value for row in multiplicities for value in row["exchangeable_symbolic_slot_node_ids"]}
    rows: list[SourceParticipantExactBinding] = []
    for constraint in multiplicities:
        node_ids = tuple(constraint["exchangeable_symbolic_slot_node_ids"])
        ordered = tuple(sorted((assignments[value], value) for value in node_ids))
        instances = tuple(value for value, _ in ordered)
        source = participant_nodes[node_ids[0]]
        refs = tuple(runtime[value] for value in instances)
        rows.append(SourceParticipantExactBinding(
            tuple(sorted(node_ids)), source["participant_kind"], source["literal_value"], instances,
            tuple(row.position_reference_id for row in refs), tuple(row.participant_layer for row in refs),
            tuple(row.source_frame_id for row in refs), tuple(row.raw_position_token for row in refs),
            source["source_evidence_mode"],
        ))
    for node_id, instance_id in sorted(assignments.items()):
        if node_id in grouped_nodes:
            continue
        source = participant_nodes[node_id]
        ref = runtime[instance_id]
        rows.append(SourceParticipantExactBinding(
            (node_id,), source["participant_kind"], source["literal_value"], (instance_id,),
            (ref.position_reference_id,), (ref.participant_layer,), (ref.source_frame_id,),
            (ref.raw_position_token,), source["source_evidence_mode"],
        ))
    return tuple(sorted(rows, key=lambda row: row.participant_pattern_node_ids))


def _normalized_signature(
    record: dict[str, Any],
    selected: tuple[_RelationOption, ...],
    assignments: dict[str, str],
    positions: tuple[SourcePositionConstraintExactBinding, ...],
    multiplicities: tuple[SourceMultiplicityExactBinding, ...],
) -> str:
    exchange_node_to_group = {
        node_id: row.multiplicity_constraint_id
        for row in multiplicities for node_id in row.exchangeable_symbolic_slot_node_ids
    }
    relation_rows = []
    for option in selected:
        binding = option.binding
        mapping = [
            (exchange_node_to_group.get(node_id, node_id), instance_id)
            for node_id, instance_id in option.assignments
        ]
        if binding.source_orientation != "DIRECTED":
            mapping.sort()
        relation_rows.append((
            binding.relation_pattern_node_id, binding.source_relation_reference_id,
            binding.positional_fact_id, tuple(mapping),
        ))
    nonexchange = tuple(sorted(
        (node_id, instance_id) for node_id, instance_id in assignments.items()
        if node_id not in exchange_node_to_group
    ))
    payload = {
        "graph_record_id": record["graph_record_id"],
        "graph_record_sha256": record["graph_record_sha256"],
        "relations": sorted(relation_rows),
        "participants": nonexchange,
        "positions": [
            (row.position_constraint_id, row.replay_status, row.runtime_instance_ids)
            for row in positions
        ],
        "multiplicity": [
            (row.multiplicity_constraint_id, row.exact_runtime_instance_ids)
            for row in multiplicities
        ],
    }
    return object_sha256(payload)


def enumerate_graph_inventory(
    graph: dict[str, Any],
    plan: tuple[SourceGraphBindabilityPlan, ...],
    natal: BaziChartCandidate,
    incidence: BaziRelationIncidenceCandidate,
    branch: BaziBranchRelationPositionalCandidate,
    stem: BaziStemRelationPositionalCandidate,
) -> tuple[SourceGraphBindingInventory, ...]:
    records, relations, participants, positions, multiplicities = _graph_indices(graph)
    runtime = _runtime_participants(natal, branch, stem)
    inventories: list[SourceGraphBindingInventory] = []
    for plan_row in plan:
        record = records[plan_row.graph_record_id]
        if plan_row.bindability_class == NOT_R1_EXACT_BINDABLE:
            inventories.append(SourceGraphBindingInventory(
                graph_record_id=plan_row.graph_record_id,
                source_occurrence_id=plan_row.source_occurrence_id,
                bindability_class=plan_row.bindability_class,
                inventory_status="SOURCE_GRAPH_NOT_R1_EXACT_BINDABLE",
                source_unresolved_graph_requirements=plan_row.source_unresolved_graph_requirements,
                structural_reason_ids=plan_row.structural_reason_ids,
                unresolved_structural_constraint_ids=plan_row.unresolved_structural_constraint_ids,
                binding_candidates=(),
            ))
            continue
        relation_nodes = tuple(relations[value] for value in record["relation_pattern_node_ids"])
        position_rows = tuple(positions[value] for value in record["position_constraint_ids"])
        multiplicity_rows = tuple(multiplicities[value] for value in record["multiplicity_constraint_ids"])
        option_domains = tuple(
            _relation_options(row, participants, incidence, branch, stem, runtime)
            for row in relation_nodes
        )
        candidates_by_signature: dict[str, ChartSpecificExactBindingCandidate] = {}
        if all(option_domains):
            for selected in product(*option_domains):
                selected = tuple(selected)
                assignments = _merge_assignments(selected)
                if assignments is None:
                    continue
                positioned = _apply_exact_positions(assignments, position_rows, participants, natal, runtime)
                if positioned is None:
                    continue
                assignments, position_bindings = positioned
                multiplicity_bindings = _multiplicity_bindings(assignments, multiplicity_rows)
                if multiplicity_bindings is None:
                    continue
                signature = _normalized_signature(record, selected, assignments, position_bindings, multiplicity_bindings)
                candidate = ChartSpecificExactBindingCandidate(
                    binding_candidate_id=f"CHART_SOURCE_PATTERN_BINDING:{signature}",
                    normalized_assignment_signature=signature,
                    graph_record_id=record["graph_record_id"],
                    source_occurrence_id=record["source_occurrence_id"],
                    relation_bindings=tuple(option.binding for option in selected),
                    participant_bindings=_participant_bindings(assignments, participants, multiplicity_rows, runtime),
                    position_constraint_bindings=position_bindings,
                    multiplicity_bindings=multiplicity_bindings,
                    residual_unresolved_structural_constraint_ids=plan_row.unresolved_structural_constraint_ids,
                    source_interaction_claim_edge_ids=tuple(record["interaction_claim_edge_ids"]),
                    source_interaction_chain_pattern_ids=tuple(record["chain_pattern_ids"]),
                )
                candidates_by_signature.setdefault(signature, candidate)
        candidates = tuple(candidates_by_signature[value] for value in sorted(candidates_by_signature))
        if plan_row.bindability_class == FULL_EXACT_BINDING_ENUMERATION:
            status = "EXACT_BINDING_CANDIDATES_PRESENT" if candidates else "NO_COMPATIBLE_EXACT_BINDING_ASSIGNMENT"
        elif plan_row.bindability_class == PARTIAL_EXACT_BINDING_ENUMERATION:
            status = "PARTIAL_EXACT_BINDING_CANDIDATES_PRESENT" if candidates else "NO_COMPATIBLE_PARTIAL_EXACT_BINDING_ASSIGNMENT"
        else:
            raise ValueError(f"unsupported bindability class: {plan_row.bindability_class}")
        inventories.append(SourceGraphBindingInventory(
            graph_record_id=plan_row.graph_record_id,
            source_occurrence_id=plan_row.source_occurrence_id,
            bindability_class=plan_row.bindability_class,
            inventory_status=status,
            source_unresolved_graph_requirements=plan_row.source_unresolved_graph_requirements,
            structural_reason_ids=plan_row.structural_reason_ids,
            unresolved_structural_constraint_ids=plan_row.unresolved_structural_constraint_ids,
            binding_candidates=candidates,
        ))
    return tuple(inventories)
