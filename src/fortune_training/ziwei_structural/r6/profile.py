from __future__ import annotations

from dataclasses import dataclass

from fortune_training.ziwei_structural.r2.profile import (
    ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID,
    ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION,
)


ZIWEI_STRUCTURAL_V2_R6_PROFILE_ID = "ZIWEI-STRUCTURAL-RUNTIME-V2-R6"
ZIWEI_STRUCTURAL_V2_R6_PROFILE_VERSION = "1.0.0"
QISHU_POSITION_ALGORITHM_ID = "ZIWEI-QISHU-POSITION-PROJECTION"
QISHU_POSITION_ALGORITHM_VERSION = "1.0.0"
QISHU_SOURCE_ID = "S04"
QISHU_SOURCE_SECTION = "十四、气数位"
QISHU_SOURCE_RUNTIME_PATH = "sources/canonical-runtime/S04/segment-0001.txt"
QISHU_SOURCE_RUNTIME_BLOB_SHA = "8401f1d190e3ee4b87aab86f82216972bea7dde8"
QISHU_RELATIVE_ORDINAL = 9
QISHU_CLOCKWISE_OFFSET = 4


@dataclass(frozen=True)
class ResolvedQiShuPositionProfile:
    profile_id: str
    profile_version: str
    upstream_r2_profile_id: str
    upstream_r2_profile_version: str
    algorithm_id: str
    algorithm_version: str
    source_id: str
    source_section: str
    source_runtime_path: str
    source_runtime_blob_sha: str
    relative_ordinal: int
    clockwise_offset: int
    supported_time_layer: str

    def validate(self) -> "ResolvedQiShuPositionProfile":
        required = {
            "profile_id": self.profile_id,
            "profile_version": self.profile_version,
            "upstream_r2_profile_id": self.upstream_r2_profile_id,
            "upstream_r2_profile_version": self.upstream_r2_profile_version,
            "algorithm_id": self.algorithm_id,
            "algorithm_version": self.algorithm_version,
            "source_id": self.source_id,
            "source_section": self.source_section,
            "source_runtime_path": self.source_runtime_path,
            "source_runtime_blob_sha": self.source_runtime_blob_sha,
            "supported_time_layer": self.supported_time_layer,
        }
        for label, value in required.items():
            if not value.strip():
                raise ValueError(f"{label} must not be empty")
        expected = {
            "profile_id": ZIWEI_STRUCTURAL_V2_R6_PROFILE_ID,
            "profile_version": ZIWEI_STRUCTURAL_V2_R6_PROFILE_VERSION,
            "upstream_r2_profile_id": ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID,
            "upstream_r2_profile_version": ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION,
            "algorithm_id": QISHU_POSITION_ALGORITHM_ID,
            "algorithm_version": QISHU_POSITION_ALGORITHM_VERSION,
            "source_id": QISHU_SOURCE_ID,
            "source_section": QISHU_SOURCE_SECTION,
            "source_runtime_path": QISHU_SOURCE_RUNTIME_PATH,
            "source_runtime_blob_sha": QISHU_SOURCE_RUNTIME_BLOB_SHA,
            "relative_ordinal": QISHU_RELATIVE_ORDINAL,
            "clockwise_offset": QISHU_CLOCKWISE_OFFSET,
            "supported_time_layer": "NATAL",
        }
        for label, value in expected.items():
            if getattr(self, label) != value:
                raise ValueError(f"unsupported R6 {label}: {getattr(self, label)!r}")
        return self


def ziwei_structural_v2_r6_profile() -> ResolvedQiShuPositionProfile:
    return ResolvedQiShuPositionProfile(
        profile_id=ZIWEI_STRUCTURAL_V2_R6_PROFILE_ID,
        profile_version=ZIWEI_STRUCTURAL_V2_R6_PROFILE_VERSION,
        upstream_r2_profile_id=ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID,
        upstream_r2_profile_version=ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION,
        algorithm_id=QISHU_POSITION_ALGORITHM_ID,
        algorithm_version=QISHU_POSITION_ALGORITHM_VERSION,
        source_id=QISHU_SOURCE_ID,
        source_section=QISHU_SOURCE_SECTION,
        source_runtime_path=QISHU_SOURCE_RUNTIME_PATH,
        source_runtime_blob_sha=QISHU_SOURCE_RUNTIME_BLOB_SHA,
        relative_ordinal=QISHU_RELATIVE_ORDINAL,
        clockwise_offset=QISHU_CLOCKWISE_OFFSET,
        supported_time_layer="NATAL",
    ).validate()
