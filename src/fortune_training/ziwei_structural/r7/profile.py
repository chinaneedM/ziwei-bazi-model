from __future__ import annotations

from dataclasses import dataclass

from fortune_training.ziwei_structural.r2.profile import (
    ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID,
    ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION,
)


ZIWEI_STRUCTURAL_V2_R7_PROFILE_ID = "ZIWEI-STRUCTURAL-RUNTIME-V2-R7"
ZIWEI_STRUCTURAL_V2_R7_PROFILE_VERSION = "1.0.0"
ONE_SIX_COMMON_ROOT_ALGORITHM_ID = "ZIWEI-ONE-SIX-COMMON-ROOT-PROJECTION"
ONE_SIX_COMMON_ROOT_ALGORITHM_VERSION = "1.0.0"
ONE_SIX_SOURCE_ID = "S04"
ONE_SIX_SOURCE_TECHNIQUE_ID = "HL_ONE_SIX_COMMON_ROOT"
ONE_SIX_SOURCE_SECTION = "河洛技法索引：HL_ONE_SIX_COMMON_ROOT"
ONE_SIX_SOURCE_RUNTIME_PATH = "sources/canonical-runtime/S04/segment-0001.txt"
ONE_SIX_SOURCE_RUNTIME_BLOB_SHA = "8401f1d190e3ee4b87aab86f82216972bea7dde8"
ONE_SIX_SOURCE_CLAUSE_IDS = (
    "HL-C-0008-04",
    "HL-C-0008-05",
    "HL-C-0314-04",
    "HL-C-0314-05",
    "HL-C-0314-06",
)
ONE_SIX_RELATIVE_ORDINAL = 6
ONE_SIX_CLOCKWISE_OFFSET = 7
ONE_SIX_SEMANTIC_SCOPE = "DIRECTED_RELATIVE_SIXTH_PALACE_IDENTITY_ONLY"


@dataclass(frozen=True)
class ResolvedOneSixCommonRootProfile:
    profile_id: str
    profile_version: str
    upstream_r2_profile_id: str
    upstream_r2_profile_version: str
    algorithm_id: str
    algorithm_version: str
    source_id: str
    source_technique_id: str
    source_section: str
    source_runtime_path: str
    source_runtime_blob_sha: str
    source_clause_ids: tuple[str, ...]
    relative_ordinal: int
    clockwise_offset: int
    semantic_scope: str
    direct_event_permission: bool
    direct_endpoint_permission: bool
    supported_time_layer: str

    def validate(self) -> "ResolvedOneSixCommonRootProfile":
        required = {
            "profile_id": self.profile_id,
            "profile_version": self.profile_version,
            "upstream_r2_profile_id": self.upstream_r2_profile_id,
            "upstream_r2_profile_version": self.upstream_r2_profile_version,
            "algorithm_id": self.algorithm_id,
            "algorithm_version": self.algorithm_version,
            "source_id": self.source_id,
            "source_technique_id": self.source_technique_id,
            "source_section": self.source_section,
            "source_runtime_path": self.source_runtime_path,
            "source_runtime_blob_sha": self.source_runtime_blob_sha,
            "semantic_scope": self.semantic_scope,
            "supported_time_layer": self.supported_time_layer,
        }
        for label, value in required.items():
            if not value.strip():
                raise ValueError(f"{label} must not be empty")
        expected = {
            "profile_id": ZIWEI_STRUCTURAL_V2_R7_PROFILE_ID,
            "profile_version": ZIWEI_STRUCTURAL_V2_R7_PROFILE_VERSION,
            "upstream_r2_profile_id": ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID,
            "upstream_r2_profile_version": ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION,
            "algorithm_id": ONE_SIX_COMMON_ROOT_ALGORITHM_ID,
            "algorithm_version": ONE_SIX_COMMON_ROOT_ALGORITHM_VERSION,
            "source_id": ONE_SIX_SOURCE_ID,
            "source_technique_id": ONE_SIX_SOURCE_TECHNIQUE_ID,
            "source_section": ONE_SIX_SOURCE_SECTION,
            "source_runtime_path": ONE_SIX_SOURCE_RUNTIME_PATH,
            "source_runtime_blob_sha": ONE_SIX_SOURCE_RUNTIME_BLOB_SHA,
            "source_clause_ids": ONE_SIX_SOURCE_CLAUSE_IDS,
            "relative_ordinal": ONE_SIX_RELATIVE_ORDINAL,
            "clockwise_offset": ONE_SIX_CLOCKWISE_OFFSET,
            "semantic_scope": ONE_SIX_SEMANTIC_SCOPE,
            "direct_event_permission": False,
            "direct_endpoint_permission": False,
            "supported_time_layer": "NATAL",
        }
        for label, value in expected.items():
            if getattr(self, label) != value:
                raise ValueError(f"unsupported R7 {label}: {getattr(self, label)!r}")
        return self


def ziwei_structural_v2_r7_profile() -> ResolvedOneSixCommonRootProfile:
    return ResolvedOneSixCommonRootProfile(
        profile_id=ZIWEI_STRUCTURAL_V2_R7_PROFILE_ID,
        profile_version=ZIWEI_STRUCTURAL_V2_R7_PROFILE_VERSION,
        upstream_r2_profile_id=ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID,
        upstream_r2_profile_version=ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION,
        algorithm_id=ONE_SIX_COMMON_ROOT_ALGORITHM_ID,
        algorithm_version=ONE_SIX_COMMON_ROOT_ALGORITHM_VERSION,
        source_id=ONE_SIX_SOURCE_ID,
        source_technique_id=ONE_SIX_SOURCE_TECHNIQUE_ID,
        source_section=ONE_SIX_SOURCE_SECTION,
        source_runtime_path=ONE_SIX_SOURCE_RUNTIME_PATH,
        source_runtime_blob_sha=ONE_SIX_SOURCE_RUNTIME_BLOB_SHA,
        source_clause_ids=ONE_SIX_SOURCE_CLAUSE_IDS,
        relative_ordinal=ONE_SIX_RELATIVE_ORDINAL,
        clockwise_offset=ONE_SIX_CLOCKWISE_OFFSET,
        semantic_scope=ONE_SIX_SEMANTIC_SCOPE,
        direct_event_permission=False,
        direct_endpoint_permission=False,
        supported_time_layer="NATAL",
    ).validate()
