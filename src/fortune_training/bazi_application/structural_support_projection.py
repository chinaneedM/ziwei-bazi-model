from __future__ import annotations

from typing import Any, Mapping

from fortune_training.bazi_structural_support import BaziStructuralSupportCandidate
from fortune_training.bazi_structural_support.profile import (
    SEASONAL_ROLE_RULE_SET_ID,
    SEASONAL_ROLE_RULE_SET_VERSION,
    SUPPORT_EVIDENCE_RULE_SET_ID,
    SUPPORT_EVIDENCE_RULE_SET_VERSION,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256


SUPPORT_PROJECTION_SCHEMA = "BAZI-TARGET-FLOW-STRUCTURAL-SUPPORT-PROJECTION-R1"
SUPPORT_PROJECTION_ALGORITHM_ID = (
    "BAZI-TARGET-FLOW-STRUCTURAL-SUPPORT-PROJECTION-V1"
)
SUPPORT_PROJECTION_ALGORITHM_VERSION = "1.0.0"
SUPPORT_PROJECTION_SEMANTIC_SCOPE = (
    "NEUTRAL_SUPPORT_EVIDENCE_CANDIDATES_ONLY_NO_ROOT_STRENGTH_OR_WEIGHT"
)
LAYER_ORDER = ("NATAL", "DAYUN", "ANNUAL", "MONTHLY")
NATAL_MONTH_COMMAND = "NATAL_MONTH_COMMAND"
ACTIVE_FLOW_SOLAR_MONTH = "ACTIVE_FLOW_SOLAR_MONTH"
EXACT_HIDDEN_STEM_MATCH = "EXACT_HIDDEN_STEM_MATCH"
SAME_ELEMENT_HIDDEN_SUPPORT = "SAME_ELEMENT_HIDDEN_SUPPORT"


def _fact_payload(projection: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in projection.items()
        if key not in {"fact_hash", "computation_hash"}
    }


def structural_support_projection_hashes(
    projection: Mapping[str, Any],
) -> tuple[str, str]:
    fact_hash = object_sha256(_fact_payload(projection))
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "algorithm_id": SUPPORT_PROJECTION_ALGORITHM_ID,
            "algorithm_version": SUPPORT_PROJECTION_ALGORITHM_VERSION,
            "source_support_computation_hash": projection.get(
                "source_support_computation_hash"
            ),
        }
    )
    return fact_hash, computation_hash


def structural_support_projection(
    candidate: BaziStructuralSupportCandidate,
) -> dict[str, Any]:
    context = candidate.context
    projection: dict[str, Any] = {
        "schema": SUPPORT_PROJECTION_SCHEMA,
        "profile_id": context.profile_id,
        "profile_version": context.profile_version,
        "algorithm_id": SUPPORT_PROJECTION_ALGORITHM_ID,
        "algorithm_version": SUPPORT_PROJECTION_ALGORITHM_VERSION,
        "source_structural_candidate_indices": list(
            candidate.source_structural_candidate_indices
        ),
        "source_flow_candidate_indices": list(candidate.source_flow_candidate_indices),
        "source_temporal_candidate_indices": list(
            candidate.source_temporal_candidate_indices
        ),
        "source_temporal_seed_ids": list(candidate.source_temporal_seed_ids),
        "source_support_fact_hash": candidate.hashes.fact_hash,
        "source_support_computation_hash": candidate.hashes.computation_hash,
        "upstream_natal_fact_hash": context.upstream_natal_fact_hash,
        "upstream_temporal_fact_hash": context.upstream_temporal_fact_hash,
        "upstream_flow_fact_hash": context.upstream_flow_fact_hash,
        "upstream_structural_fact_hash": context.upstream_structural_fact_hash,
        "natal_month_command": json_value(context.natal_month_command),
        "active_flow_solar_month": json_value(context.active_flow_solar_month),
        "support_evidence_candidates": json_value(
            context.support_evidence_candidates
        ),
        "natal_month_command_support_candidate_ids": list(
            context.natal_month_command_support_candidate_ids
        ),
        "active_flow_solar_month_support_candidate_ids": list(
            context.active_flow_solar_month_support_candidate_ids
        ),
        "algorithm_versions": dict(context.algorithm_versions),
        "semantic_scope": SUPPORT_PROJECTION_SEMANTIC_SCOPE,
    }
    projection["fact_hash"], projection["computation_hash"] = (
        structural_support_projection_hashes(projection)
    )
    return projection


def _unique_list(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (not nonempty or bool(value))
        and len(value) == len(set(value))
    )


def validate_structural_support_projection(
    projection: Mapping[str, Any],
    *,
    source_flow_candidate_index: int,
    natal_fact_hash: str,
    temporal_fact_hash: str,
    flow_fact_hash: str,
    structural_fact_hash: str,
    support_fact_hash: str,
    support_computation_hash: str,
    flow_monthly_frame: Mapping[str, Any],
    structural_projection: Mapping[str, Any],
) -> bool:
    expected_scalars = {
        "schema": SUPPORT_PROJECTION_SCHEMA,
        "profile_id": "BAZI-STRUCTURAL-SUPPORT-FOUNDATION-R1",
        "profile_version": "1.0.0",
        "algorithm_id": SUPPORT_PROJECTION_ALGORITHM_ID,
        "algorithm_version": SUPPORT_PROJECTION_ALGORITHM_VERSION,
        "source_support_fact_hash": support_fact_hash,
        "source_support_computation_hash": support_computation_hash,
        "upstream_natal_fact_hash": natal_fact_hash,
        "upstream_temporal_fact_hash": temporal_fact_hash,
        "upstream_flow_fact_hash": flow_fact_hash,
        "upstream_structural_fact_hash": structural_fact_hash,
        "semantic_scope": SUPPORT_PROJECTION_SEMANTIC_SCOPE,
    }
    if any(projection.get(key) != value for key, value in expected_scalars.items()):
        return False

    structural_indices = projection.get("source_structural_candidate_indices")
    flow_indices = projection.get("source_flow_candidate_indices")
    temporal_indices = projection.get("source_temporal_candidate_indices")
    seed_ids = projection.get("source_temporal_seed_ids")
    if not all(
        _unique_list(value, nonempty=True)
        for value in (structural_indices, flow_indices, temporal_indices, seed_ids)
    ):
        return False
    if source_flow_candidate_index not in flow_indices:
        return False
    if not all(isinstance(value, int) and value >= 0 for value in structural_indices):
        return False
    if not all(isinstance(value, int) and value >= 0 for value in flow_indices):
        return False
    if not all(isinstance(value, int) and value >= 0 for value in temporal_indices):
        return False
    if not all(
        isinstance(value, str) and value.startswith("BAZI-TEMPORAL-SEED:")
        for value in seed_ids
    ):
        return False

    algorithm_versions = projection.get("algorithm_versions")
    if algorithm_versions != {
        "support": "1.0.0",
        "seasonal_roles": "1.0.0",
        "support_evidence": "1.0.0",
    }:
        return False

    natal_role = projection.get("natal_month_command")
    flow_role = projection.get("active_flow_solar_month")
    evidence = projection.get("support_evidence_candidates")
    natal_scope = projection.get("natal_month_command_support_candidate_ids")
    flow_scope = projection.get("active_flow_solar_month_support_candidate_ids")
    if not isinstance(natal_role, dict) or not isinstance(flow_role, dict):
        return False
    if not isinstance(evidence, list):
        return False
    if not _unique_list(natal_scope) or not _unique_list(flow_scope):
        return False

    forbidden = {
        "root",
        "strength",
        "weight",
        "grade",
        "score",
        "winner",
        "prediction",
        "interpretation",
    }
    if any(
        forbidden.intersection(row)
        for row in (natal_role, flow_role, *evidence)
        if isinstance(row, dict)
    ):
        return False

    if (
        natal_role.get("role_id") != NATAL_MONTH_COMMAND
        or natal_role.get("upstream_natal_fact_hash") != natal_fact_hash
        or natal_role.get("source_branch_instance_id") != "MONTH.BRANCH"
        or natal_role.get("branch")
        != str(natal_role.get("natal_month_ganzhi", ""))[1:2]
        or natal_role.get("reference_id")
        != (
            f"SEASONAL_ROLE:{NATAL_MONTH_COMMAND}:{natal_fact_hash}:"
            "MONTH.BRANCH"
        )
        or natal_role.get("rule_set_id") != SEASONAL_ROLE_RULE_SET_ID
        or natal_role.get("rule_set_version") != SEASONAL_ROLE_RULE_SET_VERSION
        or not natal_role.get("source_refs")
    ):
        return False

    monthly_branch = next(
        (
            row
            for row in structural_projection.get("active_temporal_branches", ())
            if isinstance(row, dict) and row.get("position") == "MONTHLY"
        ),
        None,
    )
    if (
        monthly_branch is None
        or flow_role.get("role_id") != ACTIVE_FLOW_SOLAR_MONTH
        or flow_role.get("upstream_flow_fact_hash") != flow_fact_hash
        or flow_role.get("source_monthly_frame_id")
        != flow_monthly_frame.get("frame_id")
        or flow_role.get("source_temporal_branch_instance_id")
        != monthly_branch.get("instance_id")
        or flow_role.get("active_month_ganzhi") != flow_monthly_frame.get("ganzhi")
        or flow_role.get("branch") != monthly_branch.get("branch")
        or flow_role.get("start_utc") != flow_monthly_frame.get("start_utc")
        or flow_role.get("end_utc") != flow_monthly_frame.get("end_utc")
        or flow_role.get("interval_semantics") != "START_INCLUSIVE_END_EXCLUSIVE"
        or flow_role.get("rule_set_id") != SEASONAL_ROLE_RULE_SET_ID
        or flow_role.get("rule_set_version") != SEASONAL_ROLE_RULE_SET_VERSION
        or not flow_role.get("source_refs")
    ):
        return False
    if flow_role.get("reference_id") != (
        f"SEASONAL_ROLE:{ACTIVE_FLOW_SOLAR_MONTH}:"
        f"{flow_role.get('source_monthly_frame_id')}:"
        f"{flow_role.get('source_temporal_branch_instance_id')}"
    ):
        return False

    affinity_ids = set(
        structural_projection.get("upstream_reference_ids", {}).get(
            "natal_affinity_fact_ids", ()
        )
    ) | {
        row.get("fact_id")
        for row in structural_projection.get("dynamic_affinities", ())
        if isinstance(row, dict)
    }
    exposure_ids = set(
        structural_projection.get("upstream_reference_ids", {}).get(
            "natal_exposure_link_ids", ()
        )
    ) | {
        row.get("link_id")
        for row in structural_projection.get("dynamic_exposures", ())
        if isinstance(row, dict)
    }
    temporal_stem_ids = {
        row.get("instance_id")
        for row in structural_projection.get("active_temporal_stems", ())
        if isinstance(row, dict)
    }
    temporal_branch_ids = {
        row.get("instance_id")
        for row in structural_projection.get("active_temporal_branches", ())
        if isinstance(row, dict)
    }
    temporal_hidden_ids = {
        row.get("instance_id")
        for row in structural_projection.get("temporal_hidden_stems", ())
        if isinstance(row, dict)
    }

    seen_ids: set[str] = set()
    derived_natal_scope: list[str] = []
    derived_flow_scope: list[str] = []
    for row in evidence:
        if not isinstance(row, dict):
            return False
        candidate_id = row.get("candidate_id")
        visible_id = row.get("visible_stem_instance_id")
        branch_id = row.get("supporting_branch_instance_id")
        hidden_ids = row.get("matching_hidden_stem_instance_ids")
        evidence_class = row.get("evidence_class")
        role_ids = row.get("supporting_branch_role_ids")
        participant_layers = row.get("participant_layers")
        exposure_link_ids = row.get("source_exposure_link_ids")
        if (
            not isinstance(candidate_id, str)
            or candidate_id in seen_ids
            or not isinstance(visible_id, str)
            or not isinstance(branch_id, str)
            or not _unique_list(hidden_ids, nonempty=True)
            or hidden_ids != sorted(hidden_ids)
            or not _unique_list(role_ids)
            or not _unique_list(participant_layers, nonempty=True)
            or not _unique_list(exposure_link_ids)
            or row.get("source_affinity_fact_id") not in affinity_ids
            or row.get("source_affinity_fact_id")
            != f"AFFINITY:{visible_id}<->{branch_id}"
            or row.get("rule_set_id") != SUPPORT_EVIDENCE_RULE_SET_ID
            or row.get("rule_set_version") != SUPPORT_EVIDENCE_RULE_SET_VERSION
            or not row.get("source_refs")
        ):
            return False
        if candidate_id != (
            f"SUPPORT:{evidence_class}:{visible_id}<->{branch_id}:"
            + "+".join(hidden_ids)
        ):
            return False
        expected_layers = [
            layer
            for layer in LAYER_ORDER
            if layer
            in {
                row.get("visible_participant_layer"),
                row.get("supporting_branch_participant_layer"),
            }
        ]
        if participant_layers != expected_layers:
            return False
        if visible_id in temporal_stem_ids and row.get(
            "visible_participant_layer"
        ) not in {"DAYUN", "ANNUAL", "MONTHLY"}:
            return False
        if branch_id in temporal_branch_ids and row.get(
            "supporting_branch_participant_layer"
        ) not in {"DAYUN", "ANNUAL", "MONTHLY"}:
            return False
        if any(
            hidden_id in temporal_hidden_ids
            and not hidden_id.startswith(f"{branch_id}.HIDDEN:")
            for hidden_id in hidden_ids
        ):
            return False

        expected_roles = []
        if branch_id == natal_role.get("source_branch_instance_id"):
            expected_roles.append(NATAL_MONTH_COMMAND)
        if branch_id == flow_role.get("source_temporal_branch_instance_id"):
            expected_roles.append(ACTIVE_FLOW_SOLAR_MONTH)
        if role_ids != expected_roles:
            return False
        if evidence_class == EXACT_HIDDEN_STEM_MATCH:
            expected_exposure_ids = sorted(
                f"EXPOSE:{hidden_id}->{visible_id}" for hidden_id in hidden_ids
            )
            if exposure_link_ids != expected_exposure_ids or not set(
                exposure_link_ids
            ).issubset(exposure_ids):
                return False
        elif evidence_class == SAME_ELEMENT_HIDDEN_SUPPORT:
            if exposure_link_ids:
                return False
        else:
            return False

        if NATAL_MONTH_COMMAND in role_ids:
            derived_natal_scope.append(candidate_id)
        if ACTIVE_FLOW_SOLAR_MONTH in role_ids:
            derived_flow_scope.append(candidate_id)
        seen_ids.add(candidate_id)

    if natal_scope != derived_natal_scope or flow_scope != derived_flow_scope:
        return False
    expected_fact, expected_computation = structural_support_projection_hashes(
        projection
    )
    return (
        projection.get("fact_hash") == expected_fact
        and projection.get("computation_hash") == expected_computation
    )
