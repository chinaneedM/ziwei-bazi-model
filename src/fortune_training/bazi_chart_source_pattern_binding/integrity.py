from __future__ import annotations

from typing import Any

from fortune_training.bazi_branch_relation_positional import BaziBranchRelationPositionalCandidate
from fortune_training.bazi_chart import BaziChartCandidate
from fortune_training.bazi_relation_incidence import BaziRelationIncidenceCandidate
from fortune_training.bazi_stem_relation_positional import BaziStemRelationPositionalCandidate
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .models import (
    BindingHashBundle,
    BindingIntegrityDiagnostic,
    BindingIntegrityReport,
    ChartSourcePatternBindingSnapshot,
    SourceGraphBindabilityPlan,
    SourceGraphBindingInventory,
)
from .profile import ResolvedBaziChartSourcePatternBindingProfile


def binding_snapshot_fact_payload(snapshot: ChartSourcePatternBindingSnapshot) -> dict[str, Any]:
    return {
        "target_utc": snapshot.target_utc.isoformat(),
        "source_graph_artifact_semantics_sha256": snapshot.source_graph_artifact_semantics_sha256,
        "source_graph_record_hash_chain_sha256": snapshot.source_graph_record_hash_chain_sha256,
        "source_natal_fact_hash": snapshot.source_natal_fact_hash,
        "source_incidence_snapshot_id": snapshot.source_incidence_snapshot_id,
        "source_incidence_snapshot_fact_hash": snapshot.source_incidence_snapshot_fact_hash,
        "source_incidence_fact_hash": snapshot.source_incidence_fact_hash,
        "source_branch_positional_snapshot_id": snapshot.source_branch_positional_snapshot_id,
        "source_branch_positional_fact_hash": snapshot.source_branch_positional_fact_hash,
        "source_stem_positional_snapshot_id": snapshot.source_stem_positional_snapshot_id,
        "source_stem_positional_fact_hash": snapshot.source_stem_positional_fact_hash,
    }


def binding_hash_bundle(
    snapshot: ChartSourcePatternBindingSnapshot,
    inventories: tuple[SourceGraphBindingInventory, ...],
    source_incidence_candidate_indices: tuple[int, ...],
    source_branch_positional_candidate_index: int,
    source_stem_positional_candidate_index: int,
    source_flow_candidate_indices: tuple[int, ...],
    source_structural_candidate_indices: tuple[int, ...],
    source_support_candidate_indices: tuple[int, ...],
    source_temporal_candidate_indices: tuple[int, ...],
    source_temporal_seed_ids: tuple[str, ...],
    source_incidence_lineage_binding_keys: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ResolvedBaziChartSourcePatternBindingProfile,
) -> BindingHashBundle:
    fact_payload = {
        "snapshot": binding_snapshot_fact_payload(snapshot),
        "graph_binding_inventory": json_value(inventories),
    }
    computation_payload = {
        "facts": fact_payload,
        "source_natal_computation_hash": snapshot.source_natal_computation_hash,
        "source_incidence_computation_hash": snapshot.source_incidence_computation_hash,
        "source_branch_positional_computation_hash": snapshot.source_branch_positional_computation_hash,
        "source_stem_positional_computation_hash": snapshot.source_stem_positional_computation_hash,
        "source_incidence_candidate_indices": source_incidence_candidate_indices,
        "source_branch_positional_candidate_index": source_branch_positional_candidate_index,
        "source_stem_positional_candidate_index": source_stem_positional_candidate_index,
        "source_flow_candidate_indices": source_flow_candidate_indices,
        "source_structural_candidate_indices": source_structural_candidate_indices,
        "source_support_candidate_indices": source_support_candidate_indices,
        "source_temporal_candidate_indices": source_temporal_candidate_indices,
        "source_temporal_seed_ids": source_temporal_seed_ids,
        "source_incidence_lineage_binding_keys": source_incidence_lineage_binding_keys,
        "lineage_binding_keys": lineage_binding_keys,
        "profile": json_value(profile),
    }
    return BindingHashBundle(
        fact_hash=object_sha256(fact_payload),
        computation_hash=object_sha256(computation_payload),
    )


def _diag(rows: list[BindingIntegrityDiagnostic], code: str, path: str, detail: str) -> None:
    rows.append(BindingIntegrityDiagnostic(code, path, detail))


def validate_outer_candidate(
    snapshot: ChartSourcePatternBindingSnapshot,
    inventories: tuple[SourceGraphBindingInventory, ...],
    plan: tuple[SourceGraphBindabilityPlan, ...],
    natal: BaziChartCandidate,
    incidence: BaziRelationIncidenceCandidate,
    branch: BaziBranchRelationPositionalCandidate,
    stem: BaziStemRelationPositionalCandidate,
    source_incidence_candidate_indices: tuple[int, ...],
    source_branch_positional_candidate_index: int,
    source_stem_positional_candidate_index: int,
    source_flow_candidate_indices: tuple[int, ...],
    source_structural_candidate_indices: tuple[int, ...],
    source_support_candidate_indices: tuple[int, ...],
    source_temporal_candidate_indices: tuple[int, ...],
    source_temporal_seed_ids: tuple[str, ...],
    source_incidence_lineage_binding_keys: tuple[str, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ResolvedBaziChartSourcePatternBindingProfile,
    hashes: BindingHashBundle,
) -> BindingIntegrityReport:
    diagnostics: list[BindingIntegrityDiagnostic] = []
    if natal.integrity.status != "PASS" or incidence.integrity.status != "PASS" or branch.integrity.status != "PASS" or stem.integrity.status != "PASS":
        _diag(diagnostics, "UPSTREAM_INTEGRITY_FAILED", "upstream", "all joined contracts must pass")
    if source_incidence_candidate_indices != branch.source_incidence_candidate_indices or source_incidence_candidate_indices != stem.source_incidence_candidate_indices:
        _diag(diagnostics, "INCIDENCE_LINEAGE_MULTIPLICITY_MISMATCH", "source_incidence_candidate_indices", str(source_incidence_candidate_indices))
    lineage_fields = (
        (source_flow_candidate_indices, incidence.source_flow_candidate_indices, branch.source_flow_candidate_indices, stem.source_flow_candidate_indices),
        (source_structural_candidate_indices, incidence.source_structural_candidate_indices, branch.source_structural_candidate_indices, stem.source_structural_candidate_indices),
        (source_support_candidate_indices, incidence.source_support_candidate_indices, branch.source_support_candidate_indices, stem.source_support_candidate_indices),
        (source_temporal_candidate_indices, incidence.source_temporal_candidate_indices, branch.source_temporal_candidate_indices, stem.source_temporal_candidate_indices),
        (source_temporal_seed_ids, incidence.source_temporal_seed_ids, branch.source_temporal_seed_ids, stem.source_temporal_seed_ids),
        (source_incidence_lineage_binding_keys, incidence.lineage_binding_keys, branch.source_incidence_lineage_binding_keys, stem.source_incidence_lineage_binding_keys),
    )
    if any(len(set(values)) != 1 for values in lineage_fields):
        _diag(diagnostics, "COMPLETE_UPSTREAM_LINEAGE_MISMATCH", "lineage", "Flow/Structural/Support/Temporal lineage differs")
    if snapshot.source_natal_fact_hash != natal.hashes.fact_hash or snapshot.source_natal_computation_hash != natal.hashes.computation_hash:
        _diag(diagnostics, "NATAL_HASH_LINEAGE_MISMATCH", "snapshot", snapshot.source_natal_fact_hash)
    incidence_snapshot = incidence.context.snapshot
    branch_snapshot = branch.context.snapshot
    stem_snapshot = stem.context.snapshot
    if not (
        snapshot.source_incidence_snapshot_id == incidence_snapshot.snapshot_id == branch_snapshot.source_incidence_snapshot_id == stem_snapshot.source_incidence_snapshot_id
        and snapshot.source_incidence_snapshot_fact_hash == incidence_snapshot.snapshot_fact_hash == branch_snapshot.source_incidence_snapshot_fact_hash == stem_snapshot.source_incidence_snapshot_fact_hash
        and snapshot.target_utc == incidence_snapshot.target_utc == branch_snapshot.target_utc == stem_snapshot.target_utc
    ):
        _diag(diagnostics, "SINGLE_SNAPSHOT_BOUNDARY_MISMATCH", "snapshot", snapshot.snapshot_id)
    if len(inventories) != 24 or tuple(row.graph_record_id for row in inventories) != tuple(row.graph_record_id for row in plan):
        _diag(diagnostics, "GRAPH_INVENTORY_MULTIPLICITY_OR_ORDER_MISMATCH", "graph_binding_inventory", str(len(inventories)))
    for index, (inventory, plan_row) in enumerate(zip(inventories, plan)):
        if inventory.source_occurrence_id != plan_row.source_occurrence_id or inventory.bindability_class != plan_row.bindability_class:
            _diag(diagnostics, "BINDABILITY_PLAN_REPLAY_MISMATCH", f"graph_binding_inventory[{index}]", inventory.graph_record_id)
        if plan_row.bindability_class == "NOT_R1_EXACT_BINDABLE" and (inventory.inventory_status != "SOURCE_GRAPH_NOT_R1_EXACT_BINDABLE" or inventory.binding_candidates):
            _diag(diagnostics, "NON_BINDABLE_GRAPH_ENUMERATED", f"graph_binding_inventory[{index}]", inventory.graph_record_id)
        for candidate in inventory.binding_candidates:
            if candidate.binding_candidate_id != f"CHART_SOURCE_PATTERN_BINDING:{candidate.normalized_assignment_signature}":
                _diag(diagnostics, "BINDING_CANDIDATE_ID_MISMATCH", candidate.binding_candidate_id, candidate.normalized_assignment_signature)
            node_assignments: dict[str, str] = {}
            for relation in candidate.relation_bindings:
                if relation.source_arity != len(relation.runtime_participant_instance_ids) or relation.source_arity != len(relation.source_participant_pattern_path):
                    _diag(diagnostics, "RELATION_BINDING_ARITY_MISMATCH", relation.relation_pattern_node_id, str(relation.source_arity))
                for node_id, instance_id in zip(relation.source_participant_pattern_path, relation.runtime_participant_instance_ids):
                    previous = node_assignments.get(node_id)
                    if previous is not None and previous != instance_id:
                        _diag(diagnostics, "SYMBOLIC_PARTICIPANT_UNIFICATION_MISMATCH", node_id, instance_id)
                    node_assignments[node_id] = instance_id
                if relation.source_relation_family == "BRANCH_TRINE" and relation.source_arity != 3:
                    _diag(diagnostics, "COMPLETE_SANHE_ARITY_MISMATCH", relation.relation_pattern_node_id, str(relation.source_arity))
                if relation.source_relation_type == "BRANCH_CHUAN" and relation.source_relation_family != "BRANCH_CHUAN":
                    _diag(diagnostics, "CHUAN_HARM_SEMANTIC_LEAKAGE", relation.relation_pattern_node_id, relation.source_relation_family)
            for multiplicity in candidate.multiplicity_bindings:
                if len(multiplicity.exact_runtime_instance_ids) != multiplicity.required_symbolic_cardinality or len(set(multiplicity.exact_runtime_instance_ids)) != multiplicity.required_symbolic_cardinality:
                    _diag(diagnostics, "MULTIPLICITY_DISTINCT_INSTANCE_MISMATCH", multiplicity.multiplicity_constraint_id, str(multiplicity.exact_runtime_instance_ids))
            for position in candidate.position_constraint_bindings:
                if position.constraint_status == "UNRESOLVED_SOURCE_TIME_CONTEXT" and (position.runtime_instance_ids or position.replay_status != "SOURCE_POSITION_CONTEXT_UNRESOLVED"):
                    _diag(diagnostics, "UNRESOLVED_SOURCE_TIME_OVER_RESOLVED", position.position_constraint_id, position.replay_status)

    expected_hashes = binding_hash_bundle(
        snapshot, inventories, source_incidence_candidate_indices,
        source_branch_positional_candidate_index, source_stem_positional_candidate_index,
        source_flow_candidate_indices, source_structural_candidate_indices,
        source_support_candidate_indices, source_temporal_candidate_indices,
        source_temporal_seed_ids, source_incidence_lineage_binding_keys,
        lineage_binding_keys, profile,
    )
    if hashes != expected_hashes:
        _diag(diagnostics, "BINDING_HASH_REPLAY_MISMATCH", "hashes", hashes.fact_hash)
    return BindingIntegrityReport("PASS" if not diagnostics else "FAIL", tuple(diagnostics))
