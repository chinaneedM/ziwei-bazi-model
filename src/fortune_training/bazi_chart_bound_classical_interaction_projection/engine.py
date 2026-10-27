from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fortune_training.bazi_chart_source_pattern_binding.bindability import validate_graph_identity
from fortune_training.bazi_chart_source_pattern_binding.models import BaziChartSourcePatternBindingResolution
from fortune_training.bazi_chart_source_pattern_binding.profile import bazi_chart_specific_exact_source_pattern_binding_candidates_r1_profile
from fortune_training.bazi_relation_incidence import BaziRelationIncidenceCandidate
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .integrity import projection_hash_bundle, validate_projection_outer_candidate
from .models import (
    BaziChartBoundClassicalInteractionProjectionResolution,
    ChartBoundClassicalInteractionBundle,
    ChartBoundClassicalInteractionOuterCandidate,
)
from .observation import NeutralObservationError, materialize_neutral_observation_bundle
from .profile import (
    ResolvedBaziChartBoundClassicalInteractionProjectionProfile,
)
from .projection import ChartBoundClaimProjectionError, project_chart_bound_claims
from .scope import (
    EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED,
    SourceScopeSpecificationError,
    derive_source_scope_specifications,
    project_runtime_scope_compatibility,
)


class BaziChartBoundClassicalInteractionProjectionError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class BaziChartBoundClassicalInteractionProjectionRequest:
    source_binding_resolution: BaziChartSourcePatternBindingResolution
    incidence_candidates: tuple[BaziRelationIncidenceCandidate, ...]
    source_graph: dict[str, Any]
    assertion_matrix: dict[str, Any]
    projection_profile: ResolvedBaziChartBoundClassicalInteractionProjectionProfile


def _validate_matrix_identity(matrix: dict[str, Any]) -> None:
    records = matrix.get("records")
    if not isinstance(records, list) or len(records) != 24:
        raise BaziChartBoundClassicalInteractionProjectionError("ASSERTION_MATRIX_RECORD_UNIVERSE_MISMATCH", str(type(records)))
    for record in records:
        expected = object_sha256({key: value for key, value in record.items() if key != "record_sha256"})
        if record.get("record_sha256") != expected:
            raise BaziChartBoundClassicalInteractionProjectionError(
                "ASSERTION_MATRIX_RECORD_HASH_REPLAY_MISMATCH", str(record.get("source_occurrence_id"))
            )
    determinism = matrix.get("determinism", {})
    if determinism.get("record_hash_chain_sha256") != object_sha256([row["record_sha256"] for row in records]):
        raise BaziChartBoundClassicalInteractionProjectionError("ASSERTION_MATRIX_RECORD_CHAIN_REPLAY_MISMATCH", "records")
    if determinism.get("records_semantics_sha256") != object_sha256(records):
        raise BaziChartBoundClassicalInteractionProjectionError("ASSERTION_MATRIX_RECORDS_SEMANTICS_REPLAY_MISMATCH", "records")
    closed_payload = {
        "closed_vocabularies": matrix.get("closed_vocabularies"),
        "neutral_runtime_dependency_registry": matrix.get("neutral_runtime_dependency_registry"),
    }
    if determinism.get("closed_registry_sha256") != object_sha256(closed_payload):
        raise BaziChartBoundClassicalInteractionProjectionError("ASSERTION_MATRIX_CLOSED_REGISTRY_REPLAY_MISMATCH", "closed_registry")
    replay = {key: value for key, value in matrix.items() if key != "determinism"}
    if determinism.get("artifact_semantics_sha256") != object_sha256(replay):
        raise BaziChartBoundClassicalInteractionProjectionError("ASSERTION_MATRIX_ARTIFACT_SEMANTICS_REPLAY_MISMATCH", "matrix")


def _validate_authority(request: BaziChartBoundClassicalInteractionProjectionRequest) -> None:
    profile = request.projection_profile.validate()
    validate_graph_identity(
        request.source_graph, bazi_chart_specific_exact_source_pattern_binding_candidates_r1_profile()
    )
    _validate_matrix_identity(request.assertion_matrix)
    graph_determinism = request.source_graph.get("determinism", {})
    matrix_determinism = request.assertion_matrix.get("determinism", {})
    if graph_determinism.get("artifact_semantics_sha256") != profile.graph_artifact_semantics_sha256:
        raise BaziChartBoundClassicalInteractionProjectionError("SOURCE_GRAPH_SEMANTICS_MISMATCH", str(graph_determinism.get("artifact_semantics_sha256")))
    if graph_determinism.get("graph_record_hash_chain_sha256") != profile.graph_record_hash_chain_sha256:
        raise BaziChartBoundClassicalInteractionProjectionError("SOURCE_GRAPH_RECORD_CHAIN_MISMATCH", str(graph_determinism.get("graph_record_hash_chain_sha256")))
    if matrix_determinism.get("artifact_semantics_sha256") != profile.matrix_artifact_semantics_sha256:
        raise BaziChartBoundClassicalInteractionProjectionError("ASSERTION_MATRIX_SEMANTICS_MISMATCH", str(matrix_determinism.get("artifact_semantics_sha256")))
    if matrix_determinism.get("record_hash_chain_sha256") != profile.matrix_record_hash_chain_sha256:
        raise BaziChartBoundClassicalInteractionProjectionError("ASSERTION_MATRIX_RECORD_CHAIN_MISMATCH", str(matrix_determinism.get("record_hash_chain_sha256")))


def _indices(source_graph: dict[str, Any], assertion_matrix: dict[str, Any]):
    claims = {row["interaction_claim_edge_id"]: row for row in source_graph["interaction_claim_edges"]}
    matrix = {row["source_occurrence_id"]: row for row in assertion_matrix["records"]}
    graph_records = {row["source_occurrence_id"]: row for row in source_graph["graph_records"]}
    if len(claims) != len(source_graph["interaction_claim_edges"]):
        raise BaziChartBoundClassicalInteractionProjectionError("SOURCE_CLAIM_EDGE_ID_DUPLICATE", "interaction_claim_edges")
    if len(matrix) != 24 or len(graph_records) != 24:
        raise BaziChartBoundClassicalInteractionProjectionError("UPSTREAM_SOURCE_UNIVERSE_COUNT_MISMATCH", f"matrix={len(matrix)},graph={len(graph_records)}")
    if tuple(matrix) != tuple(graph_records):
        raise BaziChartBoundClassicalInteractionProjectionError("MATRIX_GRAPH_SOURCE_ORDER_MISMATCH", "24 source occurrence IDs")
    return claims, matrix, graph_records


def _incidence_for_outer(
    source_binding_outer: Any,
    incidence_candidates: tuple[BaziRelationIncidenceCandidate, ...],
) -> BaziRelationIncidenceCandidate:
    indices = source_binding_outer.source_incidence_candidate_indices
    if not indices:
        raise BaziChartBoundClassicalInteractionProjectionError("SOURCE_INCIDENCE_LINEAGE_EMPTY", source_binding_outer.snapshot.snapshot_id)
    selected: list[BaziRelationIncidenceCandidate] = []
    for index in indices:
        if index < 0 or index >= len(incidence_candidates):
            raise BaziChartBoundClassicalInteractionProjectionError("SOURCE_INCIDENCE_INDEX_OUT_OF_RANGE", str(index))
        selected.append(incidence_candidates[index])
    first = selected[0]
    if first.integrity.status != "PASS":
        raise BaziChartBoundClassicalInteractionProjectionError("SOURCE_INCIDENCE_INTEGRITY_FAILED", str(indices[0]))
    if any(row.hashes != first.hashes or row.context != first.context for row in selected[1:]):
        raise BaziChartBoundClassicalInteractionProjectionError("SOURCE_INCIDENCE_DUPLICATE_LINEAGE_COLLISION", str(indices))
    snapshot = source_binding_outer.snapshot
    if (
        snapshot.source_incidence_fact_hash != first.hashes.fact_hash
        or snapshot.source_incidence_computation_hash != first.hashes.computation_hash
        or snapshot.source_incidence_snapshot_id != first.context.snapshot.snapshot_id
        or snapshot.source_incidence_snapshot_fact_hash != first.context.snapshot.snapshot_fact_hash
    ):
        raise BaziChartBoundClassicalInteractionProjectionError("SOURCE_INCIDENCE_BINDING_SNAPSHOT_MISMATCH", str(indices))
    return first


def _project_outer(
    source_binding_outer: Any,
    incidence: BaziRelationIncidenceCandidate,
    scope_by_source: dict[str, Any],
    graph_claim_by_id: dict[str, dict[str, Any]],
    matrix_by_source: dict[str, dict[str, Any]],
    profile: ResolvedBaziChartBoundClassicalInteractionProjectionProfile,
) -> ChartBoundClassicalInteractionOuterCandidate:
    bundles: list[ChartBoundClassicalInteractionBundle] = []
    for inventory in source_binding_outer.graph_binding_inventory:
        specification = scope_by_source[inventory.source_occurrence_id]
        if inventory.binding_candidates and specification.scope_specification_status != EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED:
            raise BaziChartBoundClassicalInteractionProjectionError(
                "EXACT_BINDING_WITHOUT_R1_SOURCE_SCOPE_SPECIFICATION", inventory.source_occurrence_id
            )
        for binding_candidate in inventory.binding_candidates:
            matrix_record = matrix_by_source[binding_candidate.source_occurrence_id]
            scope_compatibility = project_runtime_scope_compatibility(specification, binding_candidate)
            observations = materialize_neutral_observation_bundle(
                binding_candidate, matrix_record, graph_claim_by_id, incidence
            )
            claims = project_chart_bound_claims(
                binding_candidate, graph_claim_by_id, inventory.source_unresolved_graph_requirements
            )
            bundle_hash = object_sha256({
                "binding_candidate_id": binding_candidate.binding_candidate_id,
                "scope_specification": json_value(specification),
                "scope_compatibility": json_value(scope_compatibility),
                "observation_bundle_id": observations.observation_bundle_id,
                "chart_bound_claim_ids": tuple(row.chart_bound_claim_id for row in claims),
                "residual_unresolved_structural_constraint_ids": binding_candidate.residual_unresolved_structural_constraint_ids,
                "source_unresolved_graph_requirements": inventory.source_unresolved_graph_requirements,
            })
            bundles.append(ChartBoundClassicalInteractionBundle(
                bundle_id=f"CHART_BOUND_CLASSICAL_INTERACTION_BUNDLE:{bundle_hash}",
                binding_candidate_id=binding_candidate.binding_candidate_id,
                source_occurrence_id=binding_candidate.source_occurrence_id,
                graph_record_id=binding_candidate.graph_record_id,
                structural_binding_class=inventory.bindability_class,
                source_scope_specification=specification,
                source_scope_compatibility=scope_compatibility,
                neutral_observation_bundle=observations,
                chart_bound_claims=claims,
                residual_unresolved_structural_constraint_ids=binding_candidate.residual_unresolved_structural_constraint_ids,
                source_unresolved_graph_requirements=inventory.source_unresolved_graph_requirements,
                source_interaction_chain_pattern_ids=binding_candidate.source_interaction_chain_pattern_ids,
            ))
    bundle_rows = tuple(bundles)
    lineage_binding_keys = (
        *source_binding_outer.lineage_binding_keys,
        f"SOURCE_BINDING_FACT:{source_binding_outer.hashes.fact_hash}",
        f"SOURCE_BINDING_COMPUTATION:{source_binding_outer.hashes.computation_hash}",
        f"PROJECTION_PROFILE:{profile.profile_id}:{profile.profile_version}",
    )
    hashes = projection_hash_bundle(source_binding_outer, bundle_rows, lineage_binding_keys, profile)
    integrity = validate_projection_outer_candidate(source_binding_outer, bundle_rows, lineage_binding_keys, profile, hashes)
    if integrity.status != "PASS":
        raise BaziChartBoundClassicalInteractionProjectionError(
            "PROJECTION_INTEGRITY_FAILED",
            ";".join(f"{row.code}:{row.path}" for row in integrity.diagnostics),
        )
    return ChartBoundClassicalInteractionOuterCandidate(
        source_binding_snapshot_id=source_binding_outer.snapshot.snapshot_id,
        source_binding_snapshot_fact_hash=source_binding_outer.snapshot.snapshot_fact_hash,
        source_binding_fact_hash=source_binding_outer.hashes.fact_hash,
        source_binding_computation_hash=source_binding_outer.hashes.computation_hash,
        source_incidence_candidate_indices=source_binding_outer.source_incidence_candidate_indices,
        source_branch_positional_candidate_index=source_binding_outer.source_branch_positional_candidate_index,
        source_stem_positional_candidate_index=source_binding_outer.source_stem_positional_candidate_index,
        source_flow_candidate_indices=source_binding_outer.source_flow_candidate_indices,
        source_structural_candidate_indices=source_binding_outer.source_structural_candidate_indices,
        source_support_candidate_indices=source_binding_outer.source_support_candidate_indices,
        source_temporal_candidate_indices=source_binding_outer.source_temporal_candidate_indices,
        source_temporal_seed_ids=source_binding_outer.source_temporal_seed_ids,
        source_incidence_lineage_binding_keys=source_binding_outer.source_incidence_lineage_binding_keys,
        lineage_binding_keys=lineage_binding_keys,
        bundles=bundle_rows,
        algorithm_versions={
            "projection": profile.algorithm_version,
            "scope": profile.scope_rule_set_version,
            "observation": profile.observation_rule_set_version,
            "claim_projection": profile.claim_projection_rule_set_version,
        },
        integrity=integrity,
        hashes=hashes,
    )


class BaziChartBoundClassicalInteractionProjectionEngine:
    schema = "BAZI-CHART-BOUND-CLASSICAL-INTERACTION-PROJECTION-RESULT-R1"
    typed_schema = "BAZI-CHART-BOUND-CLASSICAL-INTERACTION-PROJECTION-TYPED-RESOLUTION-R1"

    def resolve_typed(
        self,
        request: BaziChartBoundClassicalInteractionProjectionRequest,
    ) -> BaziChartBoundClassicalInteractionProjectionResolution:
        try:
            _validate_authority(request)
            if request.source_binding_resolution.status not in {"RESOLVED", "MULTI_CANDIDATE"}:
                raise BaziChartBoundClassicalInteractionProjectionError(
                    "UPSTREAM_BINDING_RESOLUTION_NOT_RESOLVED", request.source_binding_resolution.status
                )
            scope_rows = derive_source_scope_specifications(request.source_graph)
            scope_by_source = {row.source_occurrence_id: row for row in scope_rows}
            graph_claim_by_id, matrix_by_source, _ = _indices(request.source_graph, request.assertion_matrix)
            rows: list[ChartBoundClassicalInteractionOuterCandidate] = []
            for source_binding_outer in request.source_binding_resolution.candidates:
                incidence = _incidence_for_outer(source_binding_outer, request.incidence_candidates)
                rows.append(_project_outer(
                    source_binding_outer, incidence, scope_by_source, graph_claim_by_id, matrix_by_source,
                    request.projection_profile,
                ))
            candidates = tuple(rows)
            return BaziChartBoundClassicalInteractionProjectionResolution(
                schema=self.typed_schema,
                status="RESOLVED" if len(candidates) == 1 else "MULTI_CANDIDATE",
                candidates=candidates,
                events=("AMBIGUOUS_UPSTREAM_LINEAGES_PRESERVED",) if len(candidates) > 1 else (),
                diagnostics=(),
            )
        except (
            BaziChartBoundClassicalInteractionProjectionError,
            SourceScopeSpecificationError,
            NeutralObservationError,
            ChartBoundClaimProjectionError,
            ValueError,
            KeyError,
        ) as exc:
            code = getattr(exc, "diagnostic_code", "CHART_BOUND_CLASSICAL_INTERACTION_PROJECTION_FAILED")
            return BaziChartBoundClassicalInteractionProjectionResolution(
                self.typed_schema, "FAILED", (), (), (f"{code}:{exc}",)
            )

    def resolve(self, request: BaziChartBoundClassicalInteractionProjectionRequest) -> dict[str, Any]:
        typed = self.resolve_typed(request)
        return {
            "schema": self.schema,
            "typed_schema": typed.schema,
            "status": typed.status,
            "projection_profile": json_value(request.projection_profile),
            "candidates": json_value(typed.candidates),
            "events": list(typed.events),
            "diagnostics": list(typed.diagnostics),
        }
