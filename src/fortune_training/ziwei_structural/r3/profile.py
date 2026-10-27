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
from fortune_training.ziwei_structural.r2.profile import (
    ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID,
    ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION,
)


ZIWEI_STRUCTURAL_V2_R3_PROFILE_ID = "ZIWEI-STRUCTURAL-RUNTIME-V2-R3"
ZIWEI_STRUCTURAL_V2_R3_PROFILE_VERSION = "1.0.0"
BORROW_PROJECTION_RULE_SET_ID = "S06-BORROW-CLOSURE-R1"
BORROW_PROJECTION_RULE_SET_VERSION = "1.0.0"
BORROW_PROJECTION_ALGORITHM_ID = "ZIWEI-BORROW-PROJECTION-V2-R3"
BORROW_PROJECTION_ALGORITHM_VERSION = "1.0.0"


@dataclass(frozen=True)
class ResolvedBorrowProjectionProfile:
    profile_id: str
    profile_version: str
    natal_profile_id: str
    natal_profile_version: str
    structural_r1_profile_id: str
    structural_r1_profile_version: str
    structural_r2_profile_id: str
    structural_r2_profile_version: str
    rule_set_id: str
    rule_set_version: str
    algorithm_id: str
    algorithm_version: str
    supported_time_layer: str = "NATAL"

    def validate(self) -> "ResolvedBorrowProjectionProfile":
        required = {
            "profile_id": self.profile_id,
            "profile_version": self.profile_version,
            "natal_profile_id": self.natal_profile_id,
            "natal_profile_version": self.natal_profile_version,
            "structural_r1_profile_id": self.structural_r1_profile_id,
            "structural_r1_profile_version": self.structural_r1_profile_version,
            "structural_r2_profile_id": self.structural_r2_profile_id,
            "structural_r2_profile_version": self.structural_r2_profile_version,
            "rule_set_id": self.rule_set_id,
            "rule_set_version": self.rule_set_version,
            "algorithm_id": self.algorithm_id,
            "algorithm_version": self.algorithm_version,
            "supported_time_layer": self.supported_time_layer,
        }
        for label, value in required.items():
            if not value.strip():
                raise ValueError(f"{label} must not be empty")

        expected = {
            "profile_id": ZIWEI_STRUCTURAL_V2_R3_PROFILE_ID,
            "profile_version": ZIWEI_STRUCTURAL_V2_R3_PROFILE_VERSION,
            "natal_profile_id": ZIWEI_CHART_ENGINE_V1_PROFILE_ID,
            "natal_profile_version": ZIWEI_CHART_ENGINE_V1_PROFILE_VERSION,
            "structural_r1_profile_id": ZIWEI_STRUCTURAL_V2_R1_PROFILE_ID,
            "structural_r1_profile_version": ZIWEI_STRUCTURAL_V2_R1_PROFILE_VERSION,
            "structural_r2_profile_id": ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID,
            "structural_r2_profile_version": ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION,
            "rule_set_id": BORROW_PROJECTION_RULE_SET_ID,
            "rule_set_version": BORROW_PROJECTION_RULE_SET_VERSION,
            "algorithm_id": BORROW_PROJECTION_ALGORITHM_ID,
            "algorithm_version": BORROW_PROJECTION_ALGORITHM_VERSION,
            "supported_time_layer": "NATAL",
        }
        for label, expected_value in expected.items():
            actual = getattr(self, label)
            if actual != expected_value:
                raise ValueError(f"unsupported {label}: {actual}")
        return self


def ziwei_structural_v2_r3_profile() -> ResolvedBorrowProjectionProfile:
    return ResolvedBorrowProjectionProfile(
        profile_id=ZIWEI_STRUCTURAL_V2_R3_PROFILE_ID,
        profile_version=ZIWEI_STRUCTURAL_V2_R3_PROFILE_VERSION,
        natal_profile_id=ZIWEI_CHART_ENGINE_V1_PROFILE_ID,
        natal_profile_version=ZIWEI_CHART_ENGINE_V1_PROFILE_VERSION,
        structural_r1_profile_id=ZIWEI_STRUCTURAL_V2_R1_PROFILE_ID,
        structural_r1_profile_version=ZIWEI_STRUCTURAL_V2_R1_PROFILE_VERSION,
        structural_r2_profile_id=ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID,
        structural_r2_profile_version=ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION,
        rule_set_id=BORROW_PROJECTION_RULE_SET_ID,
        rule_set_version=BORROW_PROJECTION_RULE_SET_VERSION,
        algorithm_id=BORROW_PROJECTION_ALGORITHM_ID,
        algorithm_version=BORROW_PROJECTION_ALGORITHM_VERSION,
    ).validate()
