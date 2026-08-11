from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fortune_training.bazi_chart_bound_classical_interaction_projection.models import (
    BaziChartBoundClassicalInteractionProjectionResolution,
)
from fortune_training.bazi_chart_source_pattern_binding.bindability import validate_graph_identity
from fortune_training.bazi_chart_source_pattern_binding.models import BaziChartSourcePatternBindingResolution
from fortune_training.bazi_chart_source_pattern_binding.profile import (
    bazi_chart_specific_exact_source_pattern_binding_candidates_r1_profile,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .composition import (
    EffectFragmentCompositionError,
    build_effect_channel_coordinate_index,
    build_raw_relation_reference_index,
    build_source_layer_partitions,
)
from .graph import EffectConstraintGraphProjectionError, project_effect_constraint_graph_fragment
from .integrity import (
    composition_hash_bundle,
    match_source_binding_outer,
    replay_source_projection_outer,
    validate_composition_candidate,
)
from .models import (
    BaziClassicalEffectConstraintGraphResolution,
    ClassicalEffectConstraintCompositionEnvelopeCandidate,
)
from .profile import ResolvedBaziClassicalEffectConstraintGraphProfile


class BaziClassicalEffectConstraintGraphError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class BaziClassicalEffectConstraintGraphRequest:
    source_projection_resolution: BaziChartBoundClassicalInteractionProjectionResolution
    source_binding_resolution: BaziChartSourcePatternBindingResolution
    source_graph: dict[str, Any]
    effect_graph_profile: ResolvedBaziClassicalEffectConstraintGraphProfile


def _validate_authority(request: BaziClassicalEffectConstraintGraphRequest) -> None:
    profile = request.effect_graph_profile.validate()
    validate_graph_identity(
        request.source_graph,
        bazi_chart_specific_exact_source_pattern_binding_candidates_r1_profile(),
    )
    determinism = request.source_graph.get("determinism", {})
    if determinism.get("artifact_semantics_sha256") != profile.source_graph_artifact_semantics_sha256:
        raise BaziClassicalEffectConstraintGraphError(
            "SOURCE_GRAPH_SEMANTICS_MISMATCH", str(determinism.get("artifact_semantics_sha256"))
        )
    if determinism.get("graph_record_hash_chain_sha256") != profile.source_graph_record_hash_chain_sha256:
        raise BaziClassicalEffectConstraintGraphError(
            "SOURCE_GRAPH_RECORD_CHAIN_MISMATCH", str(determinism.get("graph_record_hash_chain_sha256"))
        )
    if request.source_projection_resolution.status not in {"RESOLVED", "MULTI_CANDIDATE"}:
        raise BaziClassicalEffectConstraintGraphError(
            "UPSTREAM_PROJECTION_NOT_RESOLVED", request.source_projection_resolution.status
        )
    if request.source_binding_resolution.status not in {"RESOLVED", "MULTI_CANDIDATE"}:
        raise BaziClassicalEffectConstraintGraphError(
            "UPSTREAM_BINDING_NOT_RESOLVED", request.source_binding_resolution.status
        )


def _graph_indices(source_graph: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    graph_records = {row["source_occurrence_id"]: row for row in source_graph.get("graph_records", ())}
    chains = {row["chain_pattern_id"]: row for row in source_graph.get("interaction_chain_patterns", ())}
    if len(graph_records) != 24:
        raise BaziClassicalEffectConstraintGraphError(
            "SOURCE_GRAPH_RECORD_UNIVERSE_MISMATCH", str(len(graph_records))
        )
    if len(chains) != len(source_graph.get("interaction_chain_patterns", ())):
        raise BaziClassicalEffectConstraintGraphError("SOURCE_GRAPH_CHAIN_ID_DUPLICATE", str(len(chains)))
    return graph_records, chains


def _binding_candidates_by_id(source_binding_outer: Any) -> dict[str, Any]:
    rows = [
        candidate
        for inventory in source_binding_outer.graph_binding_inventory
        for candidate in inventory.binding_candidates
    ]
    result = {row.binding_candidate_id: row for row in rows}
    if len(result) != len(rows):
        raise BaziClassicalEffectConstraintGraphError(
            "SOURCE_BINDING_CANDIDATE_ID_DUPLICATE", str(len(rows))
        )
    return result


def _project_outer(
    source_projection_outer: Any,
    source_binding_outer: Any,
    graph_record_by_source: dict[str, dict[str, Any]],
    graph_chain_by_id: dict[str, dict[str, Any]],
    profile: ResolvedBaziClassicalEffectConstraintGraphProfile,
) -> ClassicalEffectConstraintCompositionEnvelopeCandidate:
    if not replay_source_projection_outer(source_projection_outer, source_binding_outer):
        raise BaziClassicalEffectConstraintGraphError(
            "UPSTREAM_PROJECTION_HASH_REPLAY_MISMATCH", source_projection_outer.hashes.fact_hash
        )
    binding_by_id = _binding_candidates_by_id(source_binding_outer)
    fragments = []
    for bundle in source_projection_outer.bundles:
        binding_candidate = binding_by_id.get(bundle.binding_candidate_id)
        if binding_candidate is None:
            raise BaziClassicalEffectConstraintGraphError(
                "SOURCE_BINDING_CANDIDATE_MISSING_FOR_PROJECTED_BUNDLE", bundle.binding_candidate_id
            )
        graph_record = graph_record_by_source.get(bundle.source_occurrence_id)
        if graph_record is None:
            raise BaziClassicalEffectConstraintGraphError(
                "SOURCE_GRAPH_RECORD_MISSING_FOR_PROJECTED_BUNDLE", bundle.source_occurrence_id
            )
        fragments.append(project_effect_constraint_graph_fragment(
            bundle,
            binding_candidate,
            graph_record,
            graph_chain_by_id,
            profile,
            source_projection_outer.hashes.fact_hash,
        ))
    fragment_rows = tuple(fragments)
    partitions = build_source_layer_partitions(fragment_rows)
    raw_relation_index = build_raw_relation_reference_index(fragment_rows)
    effect_channel_index = build_effect_channel_coordinate_index(fragment_rows)
    lineage_binding_keys = (
        *source_projection_outer.lineage_binding_keys,
        f"SOURCE_PROJECTION_FACT:{source_projection_outer.hashes.fact_hash}",
        f"SOURCE_PROJECTION_COMPUTATION:{source_projection_outer.hashes.computation_hash}",
        f"EFFECT_GRAPH_PROFILE:{profile.profile_id}:{profile.profile_version}",
    )
    hashes = composition_hash_bundle(
        source_projection_outer,
        fragment_rows,
        partitions,
        raw_relation_index,
        effect_channel_index,
        lineage_binding_keys,
        profile,
    )
    integrity = validate_composition_candidate(
        source_projection_outer,
        source_binding_outer,
        fragment_rows,
        partitions,
        raw_relation_index,
        effect_channel_index,
        lineage_binding_keys,
        profile,
        hashes,
    )
    if integrity.status != "PASS":
        raise BaziClassicalEffectConstraintGraphError(
            "EFFECT_GRAPH_COMPOSITION_INTEGRITY_FAILED",
            ";".join(f"{row.code}:{row.path}" for row in integrity.diagnostics),
        )
    envelope_id = "CLASSICAL_EFFECT_CONSTRAINT_COMPOSITION_ENVELOPE:" + object_sha256({
        "source_projection_fact_hash": source_projection_outer.hashes.fact_hash,
        "fact_hash": hashes.fact_hash,
    })
    return ClassicalEffectConstraintCompositionEnvelopeCandidate(
        envelope_id=envelope_id,
        source_projection_fact_hash=source_projection_outer.hashes.fact_hash,
        source_projection_computation_hash=source_projection_outer.hashes.computation_hash,
        source_binding_snapshot_id=source_projection_outer.source_binding_snapshot_id,
        source_binding_snapshot_fact_hash=source_projection_outer.source_binding_snapshot_fact_hash,
        source_binding_fact_hash=source_projection_outer.source_binding_fact_hash,
        source_binding_computation_hash=source_projection_outer.source_binding_computation_hash,
        source_incidence_candidate_indices=source_projection_outer.source_incidence_candidate_indices,
        source_branch_positional_candidate_index=source_projection_outer.source_branch_positional_candidate_index,
        source_stem_positional_candidate_index=source_projection_outer.source_stem_positional_candidate_index,
        source_flow_candidate_indices=source_projection_outer.source_flow_candidate_indices,
        source_structural_candidate_indices=source_projection_outer.source_structural_candidate_indices,
        source_support_candidate_indices=source_projection_outer.source_support_candidate_indices,
        source_temporal_candidate_indices=source_projection_outer.source_temporal_candidate_indices,
        source_temporal_seed_ids=source_projection_outer.source_temporal_seed_ids,
        source_incidence_lineage_binding_keys=source_projection_outer.source_incidence_lineage_binding_keys,
        lineage_binding_keys=lineage_binding_keys,
        fragments=fragment_rows,
        source_layer_partitions=partitions,
        raw_relation_reference_index=raw_relation_index,
        effect_channel_coordinate_index=effect_channel_index,
        cross_source_layer_composition="NOT_RELEASED",
        cartesian_expansion="NOT_RELEASED",
        raw_relation_immutability_contract="IMMUTABLE_EXACT_REFERENCE_ONLY",
        algorithm_versions={
            "graph_projection": profile.graph_algorithm_version,
            "factorized_composition": profile.composition_algorithm_version,
        },
        integrity=integrity,
        hashes=hashes,
    )


class BaziClassicalEffectConstraintGraphEngine:
    schema = "BAZI-CLASSICAL-EFFECT-CONSTRAINT-GRAPH-FACTORIZED-COMPOSITION-RESULT-R1"
    typed_schema = "BAZI-CLASSICAL-EFFECT-CONSTRAINT-GRAPH-FACTORIZED-COMPOSITION-TYPED-RESOLUTION-R1"

    def resolve_typed(
        self,
        request: BaziClassicalEffectConstraintGraphRequest,
    ) -> BaziClassicalEffectConstraintGraphResolution:
        try:
            _validate_authority(request)
            graph_record_by_source, graph_chain_by_id = _graph_indices(request.source_graph)
            rows = []
            seen_binding_outer_fact_hashes: set[str] = set()
            for source_projection_outer in request.source_projection_resolution.candidates:
                source_binding_outer = match_source_binding_outer(
                    source_projection_outer, request.source_binding_resolution
                )
                if source_binding_outer.hashes.fact_hash in seen_binding_outer_fact_hashes:
                    raise BaziClassicalEffectConstraintGraphError(
                        "UPSTREAM_OUTER_LINEAGE_COMPOSED_MORE_THAN_ONCE", source_binding_outer.hashes.fact_hash
                    )
                seen_binding_outer_fact_hashes.add(source_binding_outer.hashes.fact_hash)
                rows.append(_project_outer(
                    source_projection_outer,
                    source_binding_outer,
                    graph_record_by_source,
                    graph_chain_by_id,
                    request.effect_graph_profile,
                ))
            candidates = tuple(rows)
            return BaziClassicalEffectConstraintGraphResolution(
                schema=self.typed_schema,
                status="RESOLVED" if len(candidates) == 1 else "MULTI_CANDIDATE",
                candidates=candidates,
                events=("AMBIGUOUS_UPSTREAM_LINEAGES_PRESERVED",) if len(candidates) > 1 else (),
                diagnostics=(),
            )
        except (
            BaziClassicalEffectConstraintGraphError,
            EffectConstraintGraphProjectionError,
            EffectFragmentCompositionError,
            ValueError,
            KeyError,
        ) as exc:
            code = getattr(exc, "diagnostic_code", "CLASSICAL_EFFECT_CONSTRAINT_GRAPH_FAILED")
            return BaziClassicalEffectConstraintGraphResolution(
                self.typed_schema, "FAILED", (), (), (f"{code}:{exc}",)
            )

    def resolve(self, request: BaziClassicalEffectConstraintGraphRequest) -> dict[str, Any]:
        typed = self.resolve_typed(request)
        return {
            "schema": self.schema,
            "typed_schema": typed.schema,
            "status": typed.status,
            "effect_graph_profile": json_value(request.effect_graph_profile),
            "candidates": json_value(typed.candidates),
            "events": list(typed.events),
            "diagnostics": list(typed.diagnostics),
        }
