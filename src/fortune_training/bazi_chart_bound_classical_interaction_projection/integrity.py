from __future__ import annotations

from collections import Counter
from typing import Any

from fortune_training.bazi_chart_source_pattern_binding.integrity import binding_hash_bundle
from fortune_training.bazi_chart_source_pattern_binding.profile import (
    bazi_chart_specific_exact_source_pattern_binding_candidates_r1_profile,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .models import (
    ChartBoundClassicalInteractionBundle,
    ProjectionHashBundle,
    ProjectionIntegrityDiagnostic,
    ProjectionIntegrityReport,
)
from .profile import ResolvedBaziChartBoundClassicalInteractionProjectionProfile
from .scope import (
    CROSS_LAYER_EXTENSION_UNRESOLVED,
    DIRECT_SOURCE_SCOPE_MATCH,
    EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED,
)


EXPECTED_PROJECTED_CLAIM_CLASS_COUNTS = Counter({
    "SOURCE_ASSERTED_RESOLUTION": 12,
    "SOURCE_ASSERTED_RESOLUTION_FAILURE": 2,
    "SOURCE_ASSERTED_REVERSAL_OR_REAPPEARANCE": 3,
    "SOURCE_ASSERTED_PARTICIPANT_ALLOCATION": 1,
    "SOURCE_ASSERTED_ATTENUATION": 1,
})


def projection_hash_bundle(
    source_binding_outer: Any,
    bundles: tuple[ChartBoundClassicalInteractionBundle, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ResolvedBaziChartBoundClassicalInteractionProjectionProfile,
) -> ProjectionHashBundle:
    fact_payload = {
        "source_binding_snapshot_id": source_binding_outer.snapshot.snapshot_id,
        "source_binding_snapshot_fact_hash": source_binding_outer.snapshot.snapshot_fact_hash,
        "source_binding_fact_hash": source_binding_outer.hashes.fact_hash,
        "bundles": json_value(bundles),
    }
    computation_payload = {
        "facts": fact_payload,
        "source_binding_computation_hash": source_binding_outer.hashes.computation_hash,
        "source_incidence_candidate_indices": source_binding_outer.source_incidence_candidate_indices,
        "source_branch_positional_candidate_index": source_binding_outer.source_branch_positional_candidate_index,
        "source_stem_positional_candidate_index": source_binding_outer.source_stem_positional_candidate_index,
        "source_flow_candidate_indices": source_binding_outer.source_flow_candidate_indices,
        "source_structural_candidate_indices": source_binding_outer.source_structural_candidate_indices,
        "source_support_candidate_indices": source_binding_outer.source_support_candidate_indices,
        "source_temporal_candidate_indices": source_binding_outer.source_temporal_candidate_indices,
        "source_temporal_seed_ids": source_binding_outer.source_temporal_seed_ids,
        "source_incidence_lineage_binding_keys": source_binding_outer.source_incidence_lineage_binding_keys,
        "source_binding_lineage_binding_keys": source_binding_outer.lineage_binding_keys,
        "lineage_binding_keys": lineage_binding_keys,
        "profile": json_value(profile),
    }
    return ProjectionHashBundle(
        fact_hash=object_sha256(fact_payload),
        computation_hash=object_sha256(computation_payload),
    )


def replay_source_binding_hashes(source_binding_outer: Any) -> bool:
    expected = binding_hash_bundle(
        source_binding_outer.snapshot,
        source_binding_outer.graph_binding_inventory,
        source_binding_outer.source_incidence_candidate_indices,
        source_binding_outer.source_branch_positional_candidate_index,
        source_binding_outer.source_stem_positional_candidate_index,
        source_binding_outer.source_flow_candidate_indices,
        source_binding_outer.source_structural_candidate_indices,
        source_binding_outer.source_support_candidate_indices,
        source_binding_outer.source_temporal_candidate_indices,
        source_binding_outer.source_temporal_seed_ids,
        source_binding_outer.source_incidence_lineage_binding_keys,
        source_binding_outer.lineage_binding_keys,
        bazi_chart_specific_exact_source_pattern_binding_candidates_r1_profile(),
    )
    return expected == source_binding_outer.hashes


def _diag(rows: list[ProjectionIntegrityDiagnostic], code: str, path: str, detail: str) -> None:
    rows.append(ProjectionIntegrityDiagnostic(code, path, detail))


def validate_projection_outer_candidate(
    source_binding_outer: Any,
    bundles: tuple[ChartBoundClassicalInteractionBundle, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ResolvedBaziChartBoundClassicalInteractionProjectionProfile,
    hashes: ProjectionHashBundle,
) -> ProjectionIntegrityReport:
    diagnostics: list[ProjectionIntegrityDiagnostic] = []
    if source_binding_outer.integrity.status != "PASS":
        _diag(diagnostics, "UPSTREAM_BINDING_INTEGRITY_FAILED", "source_binding", source_binding_outer.integrity.status)
    if not replay_source_binding_hashes(source_binding_outer):
        _diag(diagnostics, "UPSTREAM_BINDING_HASH_REPLAY_MISMATCH", "source_binding.hashes", source_binding_outer.hashes.fact_hash)

    upstream_candidates = [
        binding
        for inventory in source_binding_outer.graph_binding_inventory
        for binding in inventory.binding_candidates
    ]
    if len(bundles) != len(upstream_candidates):
        _diag(diagnostics, "BINDING_TO_BUNDLE_CARDINALITY_MISMATCH", "bundles", f"{len(upstream_candidates)}->{len(bundles)}")
    if tuple(row.binding_candidate_id for row in bundles) != tuple(row.binding_candidate_id for row in upstream_candidates):
        _diag(diagnostics, "BINDING_TO_BUNDLE_ORDER_OR_IDENTITY_MISMATCH", "bundles", "one-to-one identity projection required")

    bundle_by_binding = {row.binding_candidate_id: row for row in bundles}
    if len(bundle_by_binding) != len(bundles):
        _diag(diagnostics, "DUPLICATE_BUNDLE_BINDING_CANDIDATE_ID", "bundles", str(len(bundles)))

    inventory_by_source = {row.source_occurrence_id: row for row in source_binding_outer.graph_binding_inventory}
    for binding in upstream_candidates:
        bundle = bundle_by_binding.get(binding.binding_candidate_id)
        if bundle is None:
            continue
        inventory = inventory_by_source[binding.source_occurrence_id]
        if bundle.structural_binding_class != inventory.bindability_class:
            _diag(diagnostics, "STRUCTURAL_BINDING_CLASS_RECLASSIFIED", bundle.bundle_id, bundle.structural_binding_class)
        if bundle.source_scope_specification.scope_specification_status != EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED:
            _diag(diagnostics, "BUNDLE_WITHOUT_EXACT_SOURCE_SCOPE_SPECIFICATION", bundle.bundle_id, binding.source_occurrence_id)
        if bundle.source_scope_compatibility.source_scope_compatibility not in {
            DIRECT_SOURCE_SCOPE_MATCH,
            CROSS_LAYER_EXTENSION_UNRESOLVED,
        }:
            _diag(diagnostics, "SOURCE_SCOPE_COMPATIBILITY_INVALID", bundle.bundle_id, bundle.source_scope_compatibility.source_scope_compatibility)
        if bundle.residual_unresolved_structural_constraint_ids != binding.residual_unresolved_structural_constraint_ids:
            _diag(diagnostics, "RESIDUAL_STRUCTURAL_CONTEXT_REPLAY_MISMATCH", bundle.bundle_id, binding.binding_candidate_id)
        if bundle.source_unresolved_graph_requirements != inventory.source_unresolved_graph_requirements:
            _diag(diagnostics, "SOURCE_UNRESOLVED_GRAPH_PROVENANCE_REPLAY_MISMATCH", bundle.bundle_id, binding.source_occurrence_id)
        if bundle.neutral_observation_bundle.binding_candidate_id != binding.binding_candidate_id:
            _diag(diagnostics, "OBSERVATION_BUNDLE_BINDING_ID_MISMATCH", bundle.bundle_id, binding.binding_candidate_id)
        if tuple(row.source_claim_edge_id for row in bundle.chart_bound_claims) != binding.source_interaction_claim_edge_ids:
            _diag(diagnostics, "CLAIM_ONE_TO_ONE_IDENTITY_MISMATCH", bundle.bundle_id, binding.binding_candidate_id)
        for claim in bundle.chart_bound_claims:
            if claim.binding_candidate_id != binding.binding_candidate_id:
                _diag(diagnostics, "CLAIM_BINDING_ID_MISMATCH", claim.chart_bound_claim_id, binding.binding_candidate_id)
            if claim.source_unresolved_graph_requirements != inventory.source_unresolved_graph_requirements:
                _diag(diagnostics, "CLAIM_SOURCE_GRAPH_PROVENANCE_REPLAY_MISMATCH", claim.chart_bound_claim_id, claim.source_occurrence_id)

    expected_hashes = projection_hash_bundle(source_binding_outer, bundles, lineage_binding_keys, profile)
    if hashes != expected_hashes:
        _diag(diagnostics, "PROJECTION_HASH_REPLAY_MISMATCH", "hashes", hashes.fact_hash)
    return ProjectionIntegrityReport("PASS" if not diagnostics else "FAIL", tuple(diagnostics))
