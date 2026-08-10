from __future__ import annotations

from dataclasses import dataclass

from fortune_training.ziwei_chart.release import (
    ZIWEI_CHART_ENGINE_V1_PROFILE_ID,
    ZIWEI_CHART_ENGINE_V1_PROFILE_VERSION,
)


ZIWEI_STRUCTURAL_V2_R1_PROFILE_ID = "ZIWEI-STRUCTURAL-RUNTIME-V2-R1"
ZIWEI_STRUCTURAL_V2_R1_PROFILE_VERSION = "1.0.0"
NEUTRAL_Z12_TOPOLOGY_ALGORITHM_ID = "NEUTRAL-Z12-TOPOLOGY"
NEUTRAL_Z12_TOPOLOGY_ALGORITHM_VERSION = "1.0.0"


@dataclass(frozen=True)
class ResolvedZiweiStructuralProfile:
    """Independent immutable rule snapshot for Structural Runtime V2.

    R1 deliberately binds only neutral Z12 topology. Traditional named structural
    semantics remain outside this profile until their current-Git source and
    profile bindings are closed.
    """

    profile_id: str
    profile_version: str
    natal_profile_id: str
    natal_profile_version: str
    topology_algorithm_id: str
    topology_algorithm_version: str
    semantic_rule_set_id: str | None = None
    semantic_rule_set_version: str | None = None

    def validate(self) -> "ResolvedZiweiStructuralProfile":
        required = {
            "profile_id": self.profile_id,
            "profile_version": self.profile_version,
            "natal_profile_id": self.natal_profile_id,
            "natal_profile_version": self.natal_profile_version,
            "topology_algorithm_id": self.topology_algorithm_id,
            "topology_algorithm_version": self.topology_algorithm_version,
        }
        for label, value in required.items():
            if not value.strip():
                raise ValueError(f"{label} must not be empty")

        if self.profile_id != ZIWEI_STRUCTURAL_V2_R1_PROFILE_ID:
            raise ValueError(f"unsupported structural profile id: {self.profile_id}")
        if self.profile_version != ZIWEI_STRUCTURAL_V2_R1_PROFILE_VERSION:
            raise ValueError(f"unsupported structural profile version: {self.profile_version}")
        if self.natal_profile_id != ZIWEI_CHART_ENGINE_V1_PROFILE_ID:
            raise ValueError(f"unsupported upstream natal profile id: {self.natal_profile_id}")
        if self.natal_profile_version != ZIWEI_CHART_ENGINE_V1_PROFILE_VERSION:
            raise ValueError(
                f"unsupported upstream natal profile version: {self.natal_profile_version}"
            )
        if self.topology_algorithm_id != NEUTRAL_Z12_TOPOLOGY_ALGORITHM_ID:
            raise ValueError(f"unsupported topology algorithm id: {self.topology_algorithm_id}")
        if self.topology_algorithm_version != NEUTRAL_Z12_TOPOLOGY_ALGORITHM_VERSION:
            raise ValueError(
                f"unsupported topology algorithm version: {self.topology_algorithm_version}"
            )
        semantic_values = (self.semantic_rule_set_id, self.semantic_rule_set_version)
        if any(value is not None for value in semantic_values) and any(
            value is None for value in semantic_values
        ):
            raise ValueError(
                "semantic structural rule-set binding must be fully specified or fully disabled"
            )
        if self.semantic_rule_set_id is not None:
            raise ValueError("named structural semantic rule sets are not supported in V2-R1")
        return self


def ziwei_structural_v2_r1_profile() -> ResolvedZiweiStructuralProfile:
    return ResolvedZiweiStructuralProfile(
        profile_id=ZIWEI_STRUCTURAL_V2_R1_PROFILE_ID,
        profile_version=ZIWEI_STRUCTURAL_V2_R1_PROFILE_VERSION,
        natal_profile_id=ZIWEI_CHART_ENGINE_V1_PROFILE_ID,
        natal_profile_version=ZIWEI_CHART_ENGINE_V1_PROFILE_VERSION,
        topology_algorithm_id=NEUTRAL_Z12_TOPOLOGY_ALGORITHM_ID,
        topology_algorithm_version=NEUTRAL_Z12_TOPOLOGY_ALGORITHM_VERSION,
    ).validate()
