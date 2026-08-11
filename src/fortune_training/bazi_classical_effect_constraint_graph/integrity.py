from __future__ import annotations

from typing import Any

from fortune_training.bazi_chart_bound_classical_interaction_projection.integrity import projection_hash_bundle
from fortune_training.bazi_chart_bound_classical_interaction_projection.profile import (
    bazi_chart_bound_classical_interaction_projection_foundation_r1_profile,
)
from fortune_training.bazi_chart_bound_classical_interaction_projection.integrity import replay_source_binding_hashes
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .models import (
    ClassicalInteractionEffectConstraintGraphFragmentCandidate,
    EffectCompositionHashBundle,
    EffectCompositionIntegrityDiagnostic,
    EffectCompositionIntegrityReport,
    FragmentHashBundle,
)
from .profile import GRAPH_EDGE_CLASSES, SOURCE_CLAIM_TO_EFFECT_FACET, ResolvedBaziClassicalEffectConstraintGraphProfile


def _diag(rows: list[EffectCompositionIntegrityDiagnostic], code: str, path: str, detail: str) -> None:
    rows.append(EffectCompositionIntegrityDiagnostic(code, path, detail))


def match_source_binding_outer(source_projection_outer: Any, source_binding_resolution: Any) -> Any:
    matches = [
        outer for outer in source_binding_resolution.candidates
        if outer.hashes.fact_hash == source_projection_outer.source_binding_fact_hash
        and outer.hashes.computation_hash == source_projection_outer.source_binding_computation_hash
        and outer.snapshot.snapshot_id == source_projection_outer.source_binding_snapshot_id
        and outer.snapshot.snapshot_fact_hash == source_projection_outer.source_binding_snapshot_fact_hash
        and outer.source_incidence_candidate_indices == source_projection_outer.source_incidence_candidate_indices
        and outer.source_branch_positional_candidate_index == source_projection_outer.source_branch_positional_candidate_index
        and outer.source_stem_positional_candidate_index == source_projection_outer.source_stem_positional_candidate_index
        and outer.source_flow_candidate_indices == source_projection_outer.source_flow_candidate_indices
        and outer.source_structural_candidate_indices == source_projection_outer.source_structural_candidate_indices
        and outer.source_support_candidate_indices == source_projection_outer.source_support_candidate_indices
        and outer.source_temporal_candidate_indices == source_projection_outer.source_temporal_candidate_indices
        and outer.source_temporal_seed_ids == source_projection_outer.source_temporal_seed_ids
        and outer.source_incidence_lineage_binding_keys == source_projection_outer.source_incidence_lineage_binding_keys
    ]
    if len(matches) != 1:
        raise ValueError(f"SOURCE_BINDING_OUTER_MATCH_NOT_UNIQUE:{len(matches)}")
    return matches[0]


def replay_source_projection_outer(source_projection_outer: Any, source_binding_outer: Any) -> bool:
    if source_projection_outer.integrity.status != "PASS" or source_binding_outer.integrity.status != "PASS":
        return False
    if not replay_source_binding_hashes(source_binding_outer):
        return False
    expected = projection_hash_bundle(
        source_binding_outer,
        source_projection_outer.bundles,
        source_projection_outer.lineage_binding_keys,
        bazi_chart_bound_classical_interaction_projection_foundation_r1_profile(),
    )
    return expected == source_projection_outer.hashes


def replay_fragment_hashes(
    fragment: ClassicalInteractionEffectConstraintGraphFragmentCandidate,
    source_projection_fact_hash: str,
    profile: ResolvedBaziClassicalEffectConstraintGraphProfile,
) -> FragmentHashBundle:
    fact_payload = {
        "binding_candidate_id": fragment.binding_candidate_id,
        "source_occurrence_id": fragment.source_occurrence_id,
        "graph_record_id": fragment.graph_record_id,
        "interaction_assertion_id": fragment.interaction_assertion_id,
        "source_layer": fragment.source_layer,
        "structural_binding_class": fragment.structural_binding_class,
        "source_scope_compatibility": fragment.source_scope_compatibility,
        "raw_relation_reference_nodes": json_value(fragment.raw_relation_reference_nodes),
        "effect_channel_nodes": json_value(fragment.effect_channel_nodes),
        "effect_constraint_nodes": json_value(fragment.effect_constraint_nodes),
        "graph_edges": json_value(fragment.graph_edges),
        "multiplicity_references": json_value(fragment.multiplicity_references),
        "residual_unresolved_structural_constraint_ids": fragment.residual_unresolved_structural_constraint_ids,
        "source_unresolved_graph_requirements": fragment.source_unresolved_graph_requirements,
        "source_narrative_chain_ids": fragment.source_narrative_chain_ids,
    }
    return FragmentHashBundle(
        fact_hash=object_sha256(fact_payload),
        computation_hash=object_sha256({
            "facts": fact_payload,
            "source_projection_fact_hash": source_projection_fact_hash,
            "profile": json_value(profile),
        }),
    )


def composition_hash_bundle(
    source_projection_outer: Any,
    fragments: tuple[Any, ...],
    source_layer_partitions: tuple[Any, ...],
    raw_relation_reference_index: tuple[Any, ...],
    effect_channel_coordinate_index: tuple[Any, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ResolvedBaziClassicalEffectConstraintGraphProfile,
) -> EffectCompositionHashBundle:
    fact_payload = {
        "source_projection_fact_hash": source_projection_outer.hashes.fact_hash,
        "source_binding_snapshot_id": source_projection_outer.source_binding_snapshot_id,
        "source_binding_snapshot_fact_hash": source_projection_outer.source_binding_snapshot_fact_hash,
        "fragments": json_value(fragments),
        "source_layer_partitions": json_value(source_layer_partitions),
        "raw_relation_reference_index": json_value(raw_relation_reference_index),
        "effect_channel_coordinate_index": json_value(effect_channel_coordinate_index),
        "cross_source_layer_composition": "NOT_RELEASED",
        "cartesian_expansion": "NOT_RELEASED",
        "raw_relation_immutability_contract": "IMMUTABLE_EXACT_REFERENCE_ONLY",
    }
    computation_payload = {
        "facts": fact_payload,
        "source_projection_computation_hash": source_projection_outer.hashes.computation_hash,
        "source_projection_lineage_binding_keys": source_projection_outer.lineage_binding_keys,
        "lineage_binding_keys": lineage_binding_keys,
        "profile": json_value(profile),
    }
    return EffectCompositionHashBundle(
        fact_hash=object_sha256(fact_payload),
        computation_hash=object_sha256(computation_payload),
    )


def validate_composition_candidate(
    source_projection_outer: Any,
    source_binding_outer: Any,
    fragments: tuple[Any, ...],
    source_layer_partitions: tuple[Any, ...],
    raw_relation_reference_index: tuple[Any, ...],
    effect_channel_coordinate_index: tuple[Any, ...],
    lineage_binding_keys: tuple[str, ...],
    profile: ResolvedBaziClassicalEffectConstraintGraphProfile,
    hashes: EffectCompositionHashBundle,
) -> EffectCompositionIntegrityReport:
    diagnostics: list[EffectCompositionIntegrityDiagnostic] = []
    if not replay_source_projection_outer(source_projection_outer, source_binding_outer):
        _diag(diagnostics, "UPSTREAM_PROJECTION_HASH_REPLAY_MISMATCH", "source_projection", source_projection_outer.hashes.fact_hash)

    bundles = source_projection_outer.bundles
    if len(fragments) != len(bundles):
        _diag(diagnostics, "BUNDLE_TO_FRAGMENT_CARDINALITY_MISMATCH", "fragments", f"{len(bundles)}->{len(fragments)}")
    if tuple(row.binding_candidate_id for row in fragments) != tuple(row.binding_candidate_id for row in bundles):
        _diag(diagnostics, "BUNDLE_TO_FRAGMENT_ORDER_OR_IDENTITY_MISMATCH", "fragments", "one fragment per exact binding candidate required")

    for fragment, bundle in zip(fragments, bundles):
        if fragment.source_occurrence_id != bundle.source_occurrence_id:
            _diag(diagnostics, "FRAGMENT_SOURCE_OCCURRENCE_MISMATCH", fragment.fragment_id, bundle.source_occurrence_id)
        if fragment.source_layer != "SHEN_CLASSICAL_SOURCE":
            _diag(diagnostics, "UNRELEASED_SOURCE_LAYER_IN_FRAGMENT", fragment.fragment_id, fragment.source_layer)
        if fragment.hashes != replay_fragment_hashes(fragment, source_projection_outer.hashes.fact_hash, profile):
            _diag(diagnostics, "FRAGMENT_HASH_REPLAY_MISMATCH", fragment.fragment_id, fragment.hashes.fact_hash)
        if len(fragment.effect_constraint_nodes) != len(bundle.chart_bound_claims):
            _diag(diagnostics, "CLAIM_TO_EFFECT_CONSTRAINT_CARDINALITY_MISMATCH", fragment.fragment_id, str(len(bundle.chart_bound_claims)))
        projected_claim_ids = tuple(row.constraint.source_claim_edge_id for row in fragment.effect_constraint_nodes)
        if projected_claim_ids != tuple(row.source_claim_edge_id for row in bundle.chart_bound_claims):
            _diag(diagnostics, "CLAIM_TO_EFFECT_CONSTRAINT_IDENTITY_MISMATCH", fragment.fragment_id, str(projected_claim_ids))
        for node in fragment.effect_constraint_nodes:
            constraint = node.constraint
            expected_facet = SOURCE_CLAIM_TO_EFFECT_FACET.get(constraint.source_claim_edge_class)
            if expected_facet != constraint.effect_facet:
                _diag(diagnostics, "SOURCE_CLAIM_EFFECT_FACET_RECLASSIFIED", constraint.effect_constraint_id, constraint.effect_facet)
            if constraint.source_claim_edge_class == "SOURCE_ASSERTED_ATTENUATION" and constraint.effect_facet != "RELATION_EFFECT_GRADE":
                _diag(diagnostics, "ATTENUATION_SYNTHESIZED_NON_GRADE_EFFECT", constraint.effect_constraint_id, constraint.effect_facet)
            if constraint.source_claim_edge_class == "SOURCE_ASSERTED_PARTICIPANT_ALLOCATION":
                if not constraint.multiplicity_references:
                    _diag(diagnostics, "PARTICIPANT_ALLOCATION_MULTIPLICITY_PROVENANCE_MISSING", constraint.effect_constraint_id, "no multiplicity reference")
                for ref in constraint.multiplicity_references:
                    if ref.alternative_path_requirement != "PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS":
                        _diag(diagnostics, "PARTICIPANT_ALLOCATION_PATH_PRESERVATION_WEAKENED", constraint.effect_constraint_id, ref.alternative_path_requirement)
            elif constraint.multiplicity_references:
                _diag(diagnostics, "MULTIPLICITY_ATTACHED_TO_NON_ALLOCATION_CONSTRAINT", constraint.effect_constraint_id, constraint.source_claim_edge_class)
        for edge in fragment.graph_edges:
            if edge.edge_kind not in GRAPH_EDGE_CLASSES:
                _diag(diagnostics, "UNRELEASED_GRAPH_EDGE_KIND", edge.edge_id, edge.edge_kind)

    partition_fragment_ids = [
        fragment_id
        for partition in source_layer_partitions
        for record_set in partition.source_record_candidate_sets
        for fragment_id in record_set.fragment_ids
    ]
    if tuple(partition_fragment_ids) != tuple(row.fragment_id for row in fragments):
        _diag(diagnostics, "FACTORIZED_PARTITION_FRAGMENT_COVERAGE_MISMATCH", "source_layer_partitions", str(len(partition_fragment_ids)))
    for partition in source_layer_partitions:
        if partition.source_layer != "SHEN_CLASSICAL_SOURCE":
            _diag(diagnostics, "CROSS_SOURCE_LAYER_COMPOSITION_RELEASED", partition.source_layer_partition_id, partition.source_layer)
        for record_set in partition.source_record_candidate_sets:
            if (
                record_set.member_selection_semantics != "NOT_RELEASED"
                or record_set.member_coexistence_semantics != "NOT_RELEASED"
                or record_set.member_exclusivity_semantics != "NOT_RELEASED"
            ):
                _diag(diagnostics, "SOURCE_RECORD_FRAGMENT_SET_SEMANTICS_OVERRESOLVED", record_set.source_record_candidate_set_id, "member semantics")

    expected_hashes = composition_hash_bundle(
        source_projection_outer,
        fragments,
        source_layer_partitions,
        raw_relation_reference_index,
        effect_channel_coordinate_index,
        lineage_binding_keys,
        profile,
    )
    if hashes != expected_hashes:
        _diag(diagnostics, "COMPOSITION_HASH_REPLAY_MISMATCH", "hashes", hashes.fact_hash)
    return EffectCompositionIntegrityReport("PASS" if not diagnostics else "FAIL", tuple(diagnostics))
