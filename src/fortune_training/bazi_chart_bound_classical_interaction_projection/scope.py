from __future__ import annotations

from collections import Counter
from typing import Any

from .models import SourceScopeCompatibilityProjection, SourceScopeSpecification


EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED = "EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED"
NO_R1_RUNTIME_SOURCE_SCOPE_SPECIFICATION = "NO_R1_RUNTIME_SOURCE_SCOPE_SPECIFICATION"
DIRECT_SOURCE_RECORD_NATAL_CONTEXT = "DIRECT_SOURCE_RECORD_NATAL_CONTEXT"
SOURCE_CONTEXT_INHERITED_NATAL_CONTEXT = "SOURCE_CONTEXT_INHERITED_NATAL_CONTEXT"
NATAL_FOUR_PILLAR = "NATAL_FOUR_PILLAR"
ALL_BOUND_SOURCE_PARTICIPANTS = "ALL_BOUND_SOURCE_PARTICIPANTS"
NATAL = "NATAL"
PRESERVE_AS_UNRESOLVED_EXTENSION = "PRESERVE_AS_UNRESOLVED_EXTENSION"
DIRECT_SOURCE_SCOPE_MATCH = "DIRECT_SOURCE_SCOPE_MATCH"
CROSS_LAYER_EXTENSION_UNRESOLVED = "CROSS_LAYER_EXTENSION_UNRESOLVED"

DIRECT_NATAL_SOURCE_OCCURRENCE_IDS = (
    "ZPZQ-CL-09-003-002",
    "ZPZQ-CL-09-003-007",
    "ZPZQ-CL-09-005-002",
    "ZPZQ-CL-09-007-002",
    "ZPZQ-CL-09-007-003",
    "ZPZQ-CL-09-009-003",
    "ZPZQ-CL-09-009-004",
)
INHERITED_NATAL_SOURCE_OCCURRENCE_IDS = (
    "ZPZQ-CL-09-003-003",
    "ZPZQ-CL-09-003-004",
    "ZPZQ-CL-09-003-005",
    "ZPZQ-CL-09-003-008",
    "ZPZQ-CL-09-003-009",
    "ZPZQ-CL-09-003-010",
)
EXACT_SCOPED_SOURCE_OCCURRENCE_IDS = (
    *DIRECT_NATAL_SOURCE_OCCURRENCE_IDS,
    *INHERITED_NATAL_SOURCE_OCCURRENCE_IDS,
)
EXPECTED_INHERITANCE_EDGE_IDS = {
    source_occurrence_id: f"BSSIPG-R1-CTX-{source_occurrence_id}-01"
    for source_occurrence_id in INHERITED_NATAL_SOURCE_OCCURRENCE_IDS
}


class SourceScopeSpecificationError(ValueError):
    pass


def _graph_record_order(graph: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    rows = tuple(graph.get("graph_records", ()))
    if len(rows) != 24:
        raise SourceScopeSpecificationError(f"SOURCE_GRAPH_RECORD_COUNT_MISMATCH:{len(rows)}")
    ids = tuple(row.get("source_occurrence_id") for row in rows)
    if len(set(ids)) != len(ids):
        raise SourceScopeSpecificationError("SOURCE_GRAPH_SOURCE_OCCURRENCE_DUPLICATE")
    return rows


def derive_source_scope_specifications(graph: dict[str, Any]) -> tuple[SourceScopeSpecification, ...]:
    records = _graph_record_order(graph)
    inheritance_by_source: dict[str, list[str]] = {}
    for edge in graph.get("context_inheritance_edges", ()):  # exact released #245 edges only
        source_occurrence_id = edge.get("inheriting_source_occurrence_id")
        edge_id = edge.get("context_inheritance_edge_id")
        if source_occurrence_id and edge_id:
            inheritance_by_source.setdefault(source_occurrence_id, []).append(edge_id)

    rows: list[SourceScopeSpecification] = []
    for record in records:
        source_occurrence_id = record["source_occurrence_id"]
        graph_record_id = record["graph_record_id"]
        if source_occurrence_id in DIRECT_NATAL_SOURCE_OCCURRENCE_IDS:
            rows.append(SourceScopeSpecification(
                source_occurrence_id=source_occurrence_id,
                graph_record_id=graph_record_id,
                scope_specification_status=EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED,
                source_scope_evidence_mode=DIRECT_SOURCE_RECORD_NATAL_CONTEXT,
                source_chart_domain=NATAL_FOUR_PILLAR,
                runtime_scope_subject=ALL_BOUND_SOURCE_PARTICIPANTS,
                required_runtime_participant_layer=NATAL,
                cross_layer_extension_policy=PRESERVE_AS_UNRESOLVED_EXTENSION,
                context_inheritance_edge_ids=(),
            ))
            continue
        if source_occurrence_id in INHERITED_NATAL_SOURCE_OCCURRENCE_IDS:
            edge_ids = tuple(sorted(inheritance_by_source.get(source_occurrence_id, ())))
            expected = (EXPECTED_INHERITANCE_EDGE_IDS[source_occurrence_id],)
            if edge_ids != expected:
                raise SourceScopeSpecificationError(
                    f"SOURCE_SCOPE_INHERITANCE_EDGE_REPLAY_MISMATCH:{source_occurrence_id}:{edge_ids}"
                )
            rows.append(SourceScopeSpecification(
                source_occurrence_id=source_occurrence_id,
                graph_record_id=graph_record_id,
                scope_specification_status=EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED,
                source_scope_evidence_mode=SOURCE_CONTEXT_INHERITED_NATAL_CONTEXT,
                source_chart_domain=NATAL_FOUR_PILLAR,
                runtime_scope_subject=ALL_BOUND_SOURCE_PARTICIPANTS,
                required_runtime_participant_layer=NATAL,
                cross_layer_extension_policy=PRESERVE_AS_UNRESOLVED_EXTENSION,
                context_inheritance_edge_ids=edge_ids,
            ))
            continue
        rows.append(SourceScopeSpecification(
            source_occurrence_id=source_occurrence_id,
            graph_record_id=graph_record_id,
            scope_specification_status=NO_R1_RUNTIME_SOURCE_SCOPE_SPECIFICATION,
            source_scope_evidence_mode=None,
            source_chart_domain=None,
            runtime_scope_subject=None,
            required_runtime_participant_layer=None,
            cross_layer_extension_policy=None,
            context_inheritance_edge_ids=(),
        ))

    counts = Counter(row.scope_specification_status for row in rows)
    if counts != Counter({
        EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED: 13,
        NO_R1_RUNTIME_SOURCE_SCOPE_SPECIFICATION: 11,
    }):
        raise SourceScopeSpecificationError(f"SOURCE_SCOPE_CLASS_COUNT_MISMATCH:{dict(counts)}")
    actual_scoped = tuple(row.source_occurrence_id for row in rows if row.scope_specification_status == EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED)
    if set(actual_scoped) != set(EXACT_SCOPED_SOURCE_OCCURRENCE_IDS):
        raise SourceScopeSpecificationError(f"SOURCE_SCOPE_IDENTITY_SET_MISMATCH:{actual_scoped}")
    return tuple(rows)


def project_runtime_scope_compatibility(
    specification: SourceScopeSpecification,
    binding_candidate: Any,
) -> SourceScopeCompatibilityProjection:
    if specification.scope_specification_status != EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED:
        raise SourceScopeSpecificationError(
            f"RUNTIME_SCOPE_REQUESTED_WITHOUT_R1_SPECIFICATION:{specification.source_occurrence_id}"
        )
    if binding_candidate.source_occurrence_id != specification.source_occurrence_id:
        raise SourceScopeSpecificationError("SOURCE_SCOPE_BINDING_SOURCE_OCCURRENCE_MISMATCH")

    participant_rows: list[tuple[str, str]] = []
    for binding in binding_candidate.participant_bindings:
        if not (
            len(binding.runtime_instance_ids)
            == len(binding.participant_layers)
            == len(binding.source_frame_ids)
            == len(binding.position_reference_ids)
        ):
            raise SourceScopeSpecificationError(
                f"SOURCE_SCOPE_PARTICIPANT_BINDING_CARDINALITY_MISMATCH:{binding_candidate.binding_candidate_id}"
            )
        participant_rows.extend(zip(binding.runtime_instance_ids, binding.participant_layers, strict=True))
    if not participant_rows:
        raise SourceScopeSpecificationError(
            f"SOURCE_SCOPE_NO_BOUND_PARTICIPANTS:{binding_candidate.binding_candidate_id}"
        )
    layers = tuple(sorted({layer for _, layer in participant_rows}))
    cross_layer_ids = tuple(sorted({instance_id for instance_id, layer in participant_rows if layer != NATAL}))
    compatibility = DIRECT_SOURCE_SCOPE_MATCH if not cross_layer_ids else CROSS_LAYER_EXTENSION_UNRESOLVED
    return SourceScopeCompatibilityProjection(
        source_occurrence_id=specification.source_occurrence_id,
        binding_candidate_id=binding_candidate.binding_candidate_id,
        source_scope_compatibility=compatibility,
        observed_participant_layers=layers,
        cross_layer_participant_instance_ids=cross_layer_ids,
    )
