from __future__ import annotations

from dataclasses import dataclass

from fortune_training.ziwei_chart.release import (
    ZIWEI_CHART_ENGINE_V1_PROFILE_ID,
    ZIWEI_CHART_ENGINE_V1_PROFILE_VERSION,
)
from fortune_training.ziwei_structural.profile import (
    ZIWEI_STRUCTURAL_V2_R1_PROFILE_ID,
    ZIWEI_STRUCTURAL_V2_R1_PROFILE_VERSION,
)


ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID = "ZIWEI-STRUCTURAL-RUNTIME-V2-R2"
ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION = "1.0.0"
RELATIVE_PALACE_FRAME_ALGORITHM_ID = "ZIWEI-RELATIVE-PALACE-FRAME"
RELATIVE_PALACE_FRAME_ALGORITHM_VERSION = "1.0.0"


@dataclass(frozen=True)
class ResolvedRelativePalaceFrameProfile:
    """Immutable R2 profile for interpretation-free relative-palace frames."""

    profile_id: str
    profile_version: str
    natal_profile_id: str
    natal_profile_version: str
    structural_r1_profile_id: str
    structural_r1_profile_version: str
    relative_frame_algorithm_id: str
    relative_frame_algorithm_version: str
    semantic_rule_set_id: str | None = None
    semantic_rule_set_version: str | None = None

    def validate(self) -> "ResolvedRelativePalaceFrameProfile":
        required = {
            "profile_id": self.profile_id,
            "profile_version": self.profile_version,
            "natal_profile_id": self.natal_profile_id,
            "natal_profile_version": self.natal_profile_version,
            "structural_r1_profile_id": self.structural_r1_profile_id,
            "structural_r1_profile_version": self.structural_r1_profile_version,
            "relative_frame_algorithm_id": self.relative_frame_algorithm_id,
            "relative_frame_algorithm_version": self.relative_frame_algorithm_version,
        }
        for label, value in required.items():
            if not value.strip():
                raise ValueError(f"{label} must not be empty")

        if self.profile_id != ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID:
            raise ValueError(f"unsupported R2 profile id: {self.profile_id}")
        if self.profile_version != ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION:
            raise ValueError(f"unsupported R2 profile version: {self.profile_version}")
        if self.natal_profile_id != ZIWEI_CHART_ENGINE_V1_PROFILE_ID:
            raise ValueError(f"unsupported upstream natal profile id: {self.natal_profile_id}")
        if self.natal_profile_version != ZIWEI_CHART_ENGINE_V1_PROFILE_VERSION:
            raise ValueError(
                f"unsupported upstream natal profile version: {self.natal_profile_version}"
            )
        if self.structural_r1_profile_id != ZIWEI_STRUCTURAL_V2_R1_PROFILE_ID:
            raise ValueError(
                f"unsupported upstream structural profile id: {self.structural_r1_profile_id}"
            )
        if self.structural_r1_profile_version != ZIWEI_STRUCTURAL_V2_R1_PROFILE_VERSION:
            raise ValueError(
                "unsupported upstream structural profile version: "
                f"{self.structural_r1_profile_version}"
            )
        if self.relative_frame_algorithm_id != RELATIVE_PALACE_FRAME_ALGORITHM_ID:
            raise ValueError(
                f"unsupported relative-frame algorithm id: {self.relative_frame_algorithm_id}"
            )
        if self.relative_frame_algorithm_version != RELATIVE_PALACE_FRAME_ALGORITHM_VERSION:
            raise ValueError(
                "unsupported relative-frame algorithm version: "
                f"{self.relative_frame_algorithm_version}"
            )

        semantic_values = (self.semantic_rule_set_id, self.semantic_rule_set_version)
        if any(value is not None for value in semantic_values) and any(
            value is None for value in semantic_values
        ):
            raise ValueError(
                "semantic rule-set binding must be fully specified or fully disabled"
            )
        if self.semantic_rule_set_id is not None:
            raise ValueError("named traditional structural semantics are not supported in V2-R2")
        return self


def ziwei_structural_v2_r2_profile() -> ResolvedRelativePalaceFrameProfile:
    return ResolvedRelativePalaceFrameProfile(
        profile_id=ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID,
        profile_version=ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION,
        natal_profile_id=ZIWEI_CHART_ENGINE_V1_PROFILE_ID,
        natal_profile_version=ZIWEI_CHART_ENGINE_V1_PROFILE_VERSION,
        structural_r1_profile_id=ZIWEI_STRUCTURAL_V2_R1_PROFILE_ID,
        structural_r1_profile_version=ZIWEI_STRUCTURAL_V2_R1_PROFILE_VERSION,
        relative_frame_algorithm_id=RELATIVE_PALACE_FRAME_ALGORITHM_ID,
        relative_frame_algorithm_version=RELATIVE_PALACE_FRAME_ALGORITHM_VERSION,
    ).validate()
