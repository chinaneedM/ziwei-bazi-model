from __future__ import annotations

from dataclasses import dataclass

from fortune_training.ziwei_structural.r3.profile import (
    ZIWEI_STRUCTURAL_V2_R3_PROFILE_ID,
    ZIWEI_STRUCTURAL_V2_R3_PROFILE_VERSION,
)
from fortune_training.ziwei_structural.r4.profile import (
    ZIWEI_STRUCTURAL_V2_R4_PROFILE_ID,
    ZIWEI_STRUCTURAL_V2_R4_PROFILE_VERSION,
)


ZIWEI_STRUCTURAL_V2_R5_PROFILE_ID = "ZIWEI-STRUCTURAL-RUNTIME-V2-R5"
ZIWEI_STRUCTURAL_V2_R5_PROFILE_VERSION = "1.0.0"
RESOLVED_STRUCTURAL_COMPOSITION_ALGORITHM_ID = "ZIWEI-BORROW-RESOLVED-SANFANG-SIZHENG"
RESOLVED_STRUCTURAL_COMPOSITION_ALGORITHM_VERSION = "1.0.0"


@dataclass(frozen=True)
class ResolvedStructuralCompositionProfile:
    profile_id: str
    profile_version: str
    upstream_r3_profile_id: str
    upstream_r3_profile_version: str
    upstream_r4_profile_id: str
    upstream_r4_profile_version: str
    composition_algorithm_id: str
    composition_algorithm_version: str
    supported_time_layer: str = "NATAL"

    def validate(self) -> "ResolvedStructuralCompositionProfile":
        values = {
            "profile_id": self.profile_id,
            "profile_version": self.profile_version,
            "upstream_r3_profile_id": self.upstream_r3_profile_id,
            "upstream_r3_profile_version": self.upstream_r3_profile_version,
            "upstream_r4_profile_id": self.upstream_r4_profile_id,
            "upstream_r4_profile_version": self.upstream_r4_profile_version,
            "composition_algorithm_id": self.composition_algorithm_id,
            "composition_algorithm_version": self.composition_algorithm_version,
            "supported_time_layer": self.supported_time_layer,
        }
        for label, value in values.items():
            if not value.strip():
                raise ValueError(f"{label} must not be empty")

        expected = {
            "profile_id": ZIWEI_STRUCTURAL_V2_R5_PROFILE_ID,
            "profile_version": ZIWEI_STRUCTURAL_V2_R5_PROFILE_VERSION,
            "upstream_r3_profile_id": ZIWEI_STRUCTURAL_V2_R3_PROFILE_ID,
            "upstream_r3_profile_version": ZIWEI_STRUCTURAL_V2_R3_PROFILE_VERSION,
            "upstream_r4_profile_id": ZIWEI_STRUCTURAL_V2_R4_PROFILE_ID,
            "upstream_r4_profile_version": ZIWEI_STRUCTURAL_V2_R4_PROFILE_VERSION,
            "composition_algorithm_id": RESOLVED_STRUCTURAL_COMPOSITION_ALGORITHM_ID,
            "composition_algorithm_version": RESOLVED_STRUCTURAL_COMPOSITION_ALGORITHM_VERSION,
            "supported_time_layer": "NATAL",
        }
        for label, expected_value in expected.items():
            actual = getattr(self, label)
            if actual != expected_value:
                raise ValueError(f"unsupported {label}: {actual}")
        return self


def ziwei_structural_v2_r5_profile() -> ResolvedStructuralCompositionProfile:
    return ResolvedStructuralCompositionProfile(
        profile_id=ZIWEI_STRUCTURAL_V2_R5_PROFILE_ID,
        profile_version=ZIWEI_STRUCTURAL_V2_R5_PROFILE_VERSION,
        upstream_r3_profile_id=ZIWEI_STRUCTURAL_V2_R3_PROFILE_ID,
        upstream_r3_profile_version=ZIWEI_STRUCTURAL_V2_R3_PROFILE_VERSION,
        upstream_r4_profile_id=ZIWEI_STRUCTURAL_V2_R4_PROFILE_ID,
        upstream_r4_profile_version=ZIWEI_STRUCTURAL_V2_R4_PROFILE_VERSION,
        composition_algorithm_id=RESOLVED_STRUCTURAL_COMPOSITION_ALGORITHM_ID,
        composition_algorithm_version=RESOLVED_STRUCTURAL_COMPOSITION_ALGORITHM_VERSION,
    ).validate()
