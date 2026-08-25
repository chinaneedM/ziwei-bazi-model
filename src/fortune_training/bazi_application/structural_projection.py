from __future__ import annotations

from typing import Any, Mapping

from fortune_training.bazi_structural import BaziStructuralCandidate
from fortune_training.bazi_chart.registries import (
    BRANCH_ELEMENTS,
    HIDDEN_STEMS,
    STEM_ELEMENTS,
    STEM_POLARITY,
)
from fortune_training.bazi_chart.ten_gods import ten_god
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256


STRUCTURAL_PROJECTION_SCHEMA = "BAZI-TARGET-FLOW-STRUCTURAL-PROJECTION-R1"
STRUCTURAL_PROJECTION_ALGORITHM_ID = "BAZI-TARGET-FLOW-STRUCTURAL-PROJECTION-V1"
STRUCTURAL_PROJECTION_ALGORITHM_VERSION = "1.1.0"
STRUCTURAL_SUPPORTED_LAYERS = ("DAYUN", "ANNUAL", "MONTHLY")
STRUCTURAL_EXCLUDED_LAYERS = ("XIAOYUN", "DAILY", "HOURLY")
STRUCTURAL_SEMANTIC_SCOPE = (
    "NEUTRAL_STRUCTURAL_OCCURRENCES_ONLY_NO_EFFECT_STRENGTH_OR_TRANSFORMATION_SUCCESS"
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
        "natal_day_master_stem": context.natal_day_master_stem,
        "active_layers": active_layers,
        "excluded_layers": list(STRUCTURAL_EXCLUDED_LAYERS),
        "active_temporal_stems": json_value(context.active_temporal_stems),
        "active_temporal_branches": json_value(context.active_temporal_branches),
        "participant_provenance": provenance,
        "temporal_hidden_stems": json_value(context.temporal_hidden_stems),
        "temporal_ten_gods": json_value(context.temporal_ten_gods),
        "dynamic_exposures": json_value(context.dynamic_exposures),
        "dynamic_affinities": json_value(context.dynamic_affinities),
        "relations": json_value(context.dynamic_raw_relations),
        "upstream_reference_ids": {
            "natal_exposure_link_ids": list(
                context.upstream_natal_exposure_link_ids
            ),
            "natal_affinity_fact_ids": list(
                context.upstream_natal_affinity_fact_ids
            ),
            "natal_raw_relation_ids": list(
                context.upstream_natal_raw_relation_ids
            ),
        },
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
    stems = projection.get("active_temporal_stems")
    branches = projection.get("active_temporal_branches")
    hidden_stems = projection.get("temporal_hidden_stems")
    ten_gods = projection.get("temporal_ten_gods")
    exposures = projection.get("dynamic_exposures")
    affinities = projection.get("dynamic_affinities")
    relations = projection.get("relations")
    references = projection.get("upstream_reference_ids")
    if not all(
        isinstance(value, list)
        for value in (
            provenance,
            stems,
            branches,
            hidden_stems,
            ten_gods,
            exposures,
            affinities,
            relations,
        )
    ) or not isinstance(references, dict):
        return False
    forbidden = {
        "effect",
        "severity",
        "strength",
        "winner",
        "transformation_succeeded",
        "prediction",
    }
    if any(
        forbidden.intersection(row)
        for rows in (
            provenance,
            stems,
            branches,
            hidden_stems,
            ten_gods,
            exposures,
            affinities,
            relations,
        )
        for row in rows
        if isinstance(row, dict)
    ):
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

    if len(stems) != len(branches) or len(provenance) != 2 * len(stems):
        return False
    stem_by_id: dict[str, Mapping[str, Any]] = {}
    branch_by_id: dict[str, Mapping[str, Any]] = {}
    for stem in stems:
        if not isinstance(stem, dict):
            return False
        instance_id = stem.get("instance_id")
        source = next(
            (row for row in provenance if row.get("instance_id") == instance_id),
            None,
        )
        if (
            not isinstance(instance_id, str)
            or instance_id in stem_by_id
            or source is None
            or stem.get("position") != source.get("layer")
            or instance_id != f"{source.get('source_frame_id')}.STEM"
            or stem.get("stem") != str(source.get("source_ganzhi", ""))[:1]
            or stem.get("element") != STEM_ELEMENTS.get(stem.get("stem"))
            or stem.get("polarity") != STEM_POLARITY.get(stem.get("stem"))
        ):
            return False
        stem_by_id[instance_id] = stem
    for branch in branches:
        if not isinstance(branch, dict):
            return False
        instance_id = branch.get("instance_id")
        source = next(
            (row for row in provenance if row.get("instance_id") == instance_id),
            None,
        )
        if (
            not isinstance(instance_id, str)
            or instance_id in branch_by_id
            or source is None
            or branch.get("position") != source.get("layer")
            or instance_id != f"{source.get('source_frame_id')}.BRANCH"
            or branch.get("branch") != str(source.get("source_ganzhi", ""))[1:2]
            or branch.get("element_affiliation")
            != BRANCH_ELEMENTS.get(branch.get("branch"))
        ):
            return False
        branch_by_id[instance_id] = branch
    if set(participant_layers) != (set(stem_by_id) | set(branch_by_id)):
        return False
    if any(
        sum(row.get("position") == layer for row in stems) != 1
        or sum(row.get("position") == layer for row in branches) != 1
        for layer in expected_layers
    ):
        return False

    hidden_by_id: dict[str, Mapping[str, Any]] = {}
    for hidden in hidden_stems:
        if not isinstance(hidden, dict):
            return False
        instance_id = hidden.get("instance_id")
        branch = branch_by_id.get(str(hidden.get("branch_instance_id")))
        if (
            branch is None
            or not isinstance(instance_id, str)
            or instance_id in hidden_by_id
        ):
            return False
        registry = HIDDEN_STEMS.get(str(branch.get("branch")), ())
        ordinal = hidden.get("registry_ordinal")
        if (
            hidden.get("branch_position") != branch.get("position")
            or instance_id
            != f"{hidden.get('branch_instance_id')}.HIDDEN:{hidden.get('stem')}"
            or not isinstance(ordinal, int)
            or not 0 <= ordinal < len(registry)
            or hidden.get("stem") != registry[ordinal]
            or hidden.get("element") != STEM_ELEMENTS.get(hidden.get("stem"))
            or not hidden.get("rule_set_id")
            or not hidden.get("rule_set_version")
            or not hidden.get("source_refs")
        ):
            return False
        hidden_by_id[instance_id] = hidden

    expected_ten_god_targets = set(stem_by_id) | set(hidden_by_id)
    seen_ten_god_targets: set[str] = set()
    day_master = projection.get("natal_day_master_stem")
    for binding in ten_gods:
        if not isinstance(binding, dict):
            return False
        target_id = binding.get("target_instance_id")
        target = stem_by_id.get(str(target_id)) or hidden_by_id.get(str(target_id))
        if target is None or target_id in seen_ten_god_targets:
            return False
        try:
            semantic_id, display_name = ten_god(
                str(day_master), str(target.get("stem"))
            )
        except (KeyError, ValueError):
            return False
        if (
            binding.get("binding_id") != f"TEN_GOD:{target_id}"
            or binding.get("target_stem") != target.get("stem")
            or binding.get("day_master_stem") != day_master
            or binding.get("semantic_role_id") != semantic_id
            or binding.get("display_name") != display_name
            or not binding.get("rule_set_id")
            or not binding.get("rule_set_version")
            or not binding.get("source_refs")
        ):
            return False
        seen_ten_god_targets.add(str(target_id))
    if seen_ten_god_targets != expected_ten_god_targets:
        return False

    temporal_hidden_ids = set(hidden_by_id)
    seen_exposure_ids: set[str] = set()
    for exposure in exposures:
        if not isinstance(exposure, dict) or not exposure.get("source_refs"):
            return False
        link_id = exposure.get("link_id")
        hidden_id = exposure.get("hidden_stem_instance_id")
        visible_id = exposure.get("visible_stem_instance_id")
        if not (
            visible_id in stem_by_id or hidden_id in temporal_hidden_ids
        ) or (
            not isinstance(link_id, str)
            or link_id in seen_exposure_ids
            or link_id != f"EXPOSE:{hidden_id}->{visible_id}"
            or exposure.get("match_kind") != "EXACT_STEM"
        ):
            return False
        temporal_hidden = hidden_by_id.get(str(hidden_id))
        temporal_visible = stem_by_id.get(str(visible_id))
        if (
            temporal_hidden is not None
            and exposure.get("stem") != temporal_hidden.get("stem")
        ):
            return False
        if (
            temporal_visible is not None
            and exposure.get("stem") != temporal_visible.get("stem")
        ):
            return False
        seen_exposure_ids.add(link_id)

    seen_affinity_ids: set[str] = set()
    for affinity in affinities:
        if not isinstance(affinity, dict) or not affinity.get("source_refs"):
            return False
        fact_id = affinity.get("fact_id")
        visible_id = affinity.get("visible_stem_instance_id")
        branch_id = affinity.get("branch_instance_id")
        exact_ids = affinity.get("exact_hidden_stem_instance_ids")
        same_element_ids = affinity.get("same_element_hidden_stem_instance_ids")
        if not (
            visible_id in stem_by_id or branch_id in branch_by_id
        ) or (
            not isinstance(fact_id, str)
            or fact_id in seen_affinity_ids
            or fact_id != f"AFFINITY:{visible_id}<->{branch_id}"
            or not isinstance(exact_ids, list)
            or not isinstance(same_element_ids, list)
            or len(exact_ids) != len(set(exact_ids))
            or len(same_element_ids) != len(set(same_element_ids))
            or exact_ids != sorted(exact_ids)
            or same_element_ids != sorted(same_element_ids)
            or not affinity.get("rule_set_id")
            or not affinity.get("rule_set_version")
        ):
            return False
        temporal_branch = branch_by_id.get(str(branch_id))
        temporal_visible = stem_by_id.get(str(visible_id))
        if temporal_branch is not None:
            branch_hidden = {
                instance_id: hidden
                for instance_id, hidden in hidden_by_id.items()
                if hidden.get("branch_instance_id") == branch_id
            }
            if not set(exact_ids).issubset(branch_hidden) or not set(
                same_element_ids
            ).issubset(branch_hidden):
                return False
            if temporal_visible is not None:
                expected_exact = sorted(
                    instance_id
                    for instance_id, hidden in branch_hidden.items()
                    if hidden.get("stem") == temporal_visible.get("stem")
                )
                expected_same_element = sorted(
                    instance_id
                    for instance_id, hidden in branch_hidden.items()
                    if hidden.get("element") == temporal_visible.get("element")
                )
                if (
                    exact_ids != expected_exact
                    or same_element_ids != expected_same_element
                ):
                    return False
        seen_affinity_ids.add(fact_id)

    expected_reference_keys = {
        "natal_exposure_link_ids",
        "natal_affinity_fact_ids",
        "natal_raw_relation_ids",
    }
    if set(references) != expected_reference_keys or any(
        not isinstance(references[key], list)
        or len(references[key]) != len(set(references[key]))
        for key in expected_reference_keys
    ):
        return False

    seen_relation_ids: set[str] = set()
    for relation in relations:
        if not isinstance(relation, dict) or forbidden.intersection(relation):
            return False
        relation_id = relation.get("relation_id")
        ids = relation.get("participant_instance_ids")
        layers = relation.get("participant_layers")
        if (
            not isinstance(relation_id, str)
            or relation_id in seen_relation_ids
            or not isinstance(ids, list)
            or len(ids) != len(set(ids))
            or not isinstance(layers, list)
        ):
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
        seen_relation_ids.add(relation_id)

    expected_fact, expected_computation = structural_projection_hashes(projection)
    return (
        projection.get("fact_hash") == expected_fact
        and projection.get("computation_hash") == expected_computation
    )
