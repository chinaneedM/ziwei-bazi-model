from __future__ import annotations

from typing import Any

from .models import NeutralDependencyMaterializationEvidence
from .profile import SUPPORTED_NEUTRAL_PRIMITIVES


PRIMITIVE_OBSERVATION_ATTRIBUTE = {
    "EXACT_RAW_RELATION_OCCURRENCE_IDENTITY": "relation_identity_observations",
    "EXACT_PARTICIPANT_INSTANCE_IDENTITY": "participant_identity_observations",
    "RELATION_INCIDENCE_DEGREE": "participant_incidence_observations",
    "RELATION_PAIR_TOPOLOGY": "relation_pair_topology_observations",
    "EXACT_TEMPORAL_LAYER_FRAME": "temporal_layer_frame_observations",
}


class NeutralDependencyMaterializationError(ValueError):
    pass


def _observation_id(row: Any) -> str:
    value = getattr(row, "observation_id", None)
    if not isinstance(value, str) or not value:
        raise NeutralDependencyMaterializationError("NEUTRAL_OBSERVATION_ID_INVALID")
    return value


def normalize_neutral_dependency_materialization(
    neutral_observation_bundle: Any,
) -> tuple[NeutralDependencyMaterializationEvidence, ...]:
    required = tuple(neutral_observation_bundle.required_neutral_primitives)
    if len(required) != len(set(required)):
        raise NeutralDependencyMaterializationError("REQUIRED_NEUTRAL_PRIMITIVE_DUPLICATE")
    unsupported = tuple(sorted(set(required) - set(SUPPORTED_NEUTRAL_PRIMITIVES)))
    if unsupported:
        raise NeutralDependencyMaterializationError(
            f"UNSUPPORTED_OR_TRANSITION_NEUTRAL_PRIMITIVE:{unsupported}"
        )

    rows: list[NeutralDependencyMaterializationEvidence] = []
    required_set = set(required)
    for primitive in SUPPORTED_NEUTRAL_PRIMITIVES:
        observations = tuple(getattr(neutral_observation_bundle, PRIMITIVE_OBSERVATION_ATTRIBUTE[primitive]))
        observation_ids = tuple(_observation_id(row) for row in observations)
        if len(observation_ids) != len(set(observation_ids)):
            raise NeutralDependencyMaterializationError(
                f"NEUTRAL_OBSERVATION_ID_DUPLICATE:{primitive}"
            )
        if primitive in required_set:
            status = "EXACTLY_MATERIALIZED" if observation_ids else "MISSING_REQUIRED_MATERIALIZATION"
            rows.append(NeutralDependencyMaterializationEvidence(
                primitive=primitive,
                observation_ids=observation_ids,
                materialization_status=status,
            ))
        elif observation_ids:
            rows.append(NeutralDependencyMaterializationEvidence(
                primitive=primitive,
                observation_ids=observation_ids,
                materialization_status="UNEXPECTED_MATERIALIZATION",
            ))
    return tuple(rows)


def dependency_blocker_ids(
    materialization: tuple[NeutralDependencyMaterializationEvidence, ...],
) -> tuple[str, ...]:
    blockers: list[str] = []
    for row in materialization:
        if row.materialization_status == "MISSING_REQUIRED_MATERIALIZATION":
            blockers.append(f"MATERIALIZED_DEPENDENCY_MISSING:{row.primitive}")
        elif row.materialization_status == "UNEXPECTED_MATERIALIZATION":
            blockers.append(f"UNEXPECTED_MATERIALIZED_DEPENDENCY:{row.primitive}")
        elif row.materialization_status != "EXACTLY_MATERIALIZED":
            raise NeutralDependencyMaterializationError(
                f"UNKNOWN_DEPENDENCY_MATERIALIZATION_STATUS:{row.materialization_status}"
            )
    return tuple(blockers)
