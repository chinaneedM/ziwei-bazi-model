from __future__ import annotations

from typing import Any, Mapping

from fortune_training.bazi_structural import BaziStructuralCandidate
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256


STRUCTURAL_PROJECTION_SCHEMA = "BAZI-TARGET-FLOW-STRUCTURAL-PROJECTION-R1"
STRUCTURAL_PROJECTION_ALGORITHM_ID = "BAZI-TARGET-FLOW-STRUCTURAL-PROJECTION-V1"
STRUCTURAL_PROJECTION_ALGORITHM_VERSION = "1.0.0"
STRUCTURAL_SUPPORTED_LAYERS = ("DAYUN", "ANNUAL", "MONTHLY")
STRUCTURAL_EXCLUDED_LAYERS = ("XIAOYUN", "DAILY", "HOURLY")
STRUCTURAL_SEMANTIC_SCOPE = (
    "NEUTRAL_RELATION_OCCURRENCES_ONLY_NO_EFFECT_STRENGTH_OR_TRANSFORMATION_SUCCESS"
)


def _fact_payload(projection: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in projection.items()
        if key not in {"fact_hash", "computation_hash"}
    }


def structural_projection_hashes(
    projection: Mapping[str, Any],
) -> tuple[str, str]:
    fact_hash = object_sha256(_fact_payload(projection))
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "algorithm_id": STRUCTURAL_PROJECTION_ALGORITHM_ID,
            "algorithm_version": STRUCTURAL_PROJECTION_ALGORITHM_VERSION,
            "source_structural_computation_hash": projection.get(
                "source_structural_computation_hash"
            ),
        }
    )
    return fact_hash, computation_hash


def structural_projection(
    candidate: BaziStructuralCandidate,
) -> dict[str, Any]:
    context = candidate.context
    provenance = json_value(context.temporal_participant_provenance)
    active_layers = [
        layer
        for layer in STRUCTURAL_SUPPORTED_LAYERS
        if any(row["layer"] == layer for row in provenance)
    ]
    projection: dict[str, Any] = {
        "schema": STRUCTURAL_PROJECTION_SCHEMA,
        "profile_id": context.profile_id,
        "profile_version": context.profile_version,
        "algorithm_id": STRUCTURAL_PROJECTION_ALGORITHM_ID,
        "algorithm_version": STRUCTURAL_PROJECTION_ALGORITHM_VERSION,
        "source_flow_candidate_indices": list(
            candidate.source_flow_candidate_indices
        ),
        "source_structural_fact_hash": candidate.hashes.fact_hash,
        "source_structural_computation_hash": candidate.hashes.computation_hash,
        "active_layers": active_layers,
        "excluded_layers": list(STRUCTURAL_EXCLUDED_LAYERS),
        "participant_provenance": provenance,
        "relations": json_value(context.dynamic_raw_relations),
        "semantic_scope": STRUCTURAL_SEMANTIC_SCOPE,
    }
    projection["fact_hash"], projection["computation_hash"] = (
        structural_projection_hashes(projection)
    )
    return projection


def validate_structural_projection(
    projection: Mapping[str, Any],
    *,
    source_flow_candidate_index: int,
    flow_fact_hash: str,
    structural_fact_hash: str,
    structural_computation_hash: str,
) -> bool:
    if projection.get("schema") != STRUCTURAL_PROJECTION_SCHEMA:
        return False
    if projection.get("profile_id") != "BAZI-STRUCTURAL-CONTEXT-R1":
        return False
    if projection.get("profile_version") != "1.1.0":
        return False
    if projection.get("algorithm_id") != STRUCTURAL_PROJECTION_ALGORITHM_ID:
        return False
    if projection.get("algorithm_version") != STRUCTURAL_PROJECTION_ALGORITHM_VERSION:
        return False
    if projection.get("source_structural_fact_hash") != structural_fact_hash:
        return False
    if (
        projection.get("source_structural_computation_hash")
        != structural_computation_hash
    ):
        return False
    flow_indices = projection.get("source_flow_candidate_indices")
    if not isinstance(flow_indices, list) or source_flow_candidate_index not in flow_indices:
        return False
    if len(flow_indices) != len(set(flow_indices)):
        return False
    if projection.get("excluded_layers") != list(STRUCTURAL_EXCLUDED_LAYERS):
        return False
    if projection.get("semantic_scope") != STRUCTURAL_SEMANTIC_SCOPE:
        return False

    provenance = projection.get("participant_provenance")
    relations = projection.get("relations")
    if not isinstance(provenance, list) or not isinstance(relations, list):
        return False
    participant_layers: dict[str, str] = {}
    actual_layers: list[str] = []
    for row in provenance:
        if not isinstance(row, dict):
            return False
        layer = row.get("layer")
        instance_id = row.get("instance_id")
        if layer not in STRUCTURAL_SUPPORTED_LAYERS or not isinstance(instance_id, str):
            return False
        if (
            not row.get("source_frame_id")
            or row.get("source_flow_fact_hash") != flow_fact_hash
        ):
            return False
        if instance_id in participant_layers:
            return False
        participant_layers[instance_id] = layer
        if layer not in actual_layers:
            actual_layers.append(layer)
    expected_layers = [
        layer for layer in STRUCTURAL_SUPPORTED_LAYERS if layer in actual_layers
    ]
    if projection.get("active_layers") != expected_layers:
        return False

    forbidden = {
        "effect",
        "severity",
        "strength",
        "winner",
        "transformation_succeeded",
        "prediction",
    }
    for relation in relations:
        if not isinstance(relation, dict) or forbidden.intersection(relation):
            return False
        ids = relation.get("participant_instance_ids")
        layers = relation.get("participant_layers")
        if not isinstance(ids, list) or not isinstance(layers, list):
            return False
        if relation.get("arity") != len(ids):
            return False
        derived_layers = []
        for instance_id in ids:
            layer = participant_layers.get(instance_id, "NATAL")
            if layer not in derived_layers:
                derived_layers.append(layer)
        if set(layers) != set(derived_layers):
            return False
        if not relation.get("rule_set_id") or not relation.get("rule_set_version"):
            return False
        if not relation.get("source_refs"):
            return False
        scope = "CROSS_LAYER" if "NATAL" in layers else "TEMPORAL_ONLY"
        if relation.get("relation_scope") != scope:
            return False

    expected_fact, expected_computation = structural_projection_hashes(projection)
    return (
        projection.get("fact_hash") == expected_fact
        and projection.get("computation_hash") == expected_computation
    )
