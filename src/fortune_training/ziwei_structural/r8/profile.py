from __future__ import annotations

from dataclasses import dataclass

from fortune_training.ziwei_structural.r2.profile import (
    ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID,
    ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION,
)


ZIWEI_STRUCTURAL_V2_R8_PROFILE_ID = "ZIWEI-STRUCTURAL-RUNTIME-V2-R8"
ZIWEI_STRUCTURAL_V2_R8_PROFILE_VERSION = "1.0.0"
ADJACENT_PALACE_PAIR_ALGORITHM_ID = "ZIWEI-ADJACENT-PALACE-PAIR-PROJECTION"
ADJACENT_PALACE_PAIR_ALGORITHM_VERSION = "1.0.0"
ADJACENT_PALACE_SOURCE_ID = "S04"
ADJACENT_PALACE_SOURCE_FAMILY_ID = "S05-SRC-ZZTERM-METHOD"
ADJACENT_PALACE_SOURCE_SECTION = "紫微斗数基础术语数据库：十五、邻宫"
ADJACENT_PALACE_SOURCE_RUNTIME_PATH = "sources/canonical-runtime/S04/segment-0001.txt"
ADJACENT_PALACE_SOURCE_RUNTIME_BLOB_SHA = "8401f1d190e3ee4b87aab86f82216972bea7dde8"
ADJACENT_PALACE_SOURCE_PARAGRAPH_ID = "ZZTERM-P-0018"
ADJACENT_PALACE_SOURCE_SEGMENT_IDS = ("ZZTERM-L-0057", "ZZTERM-L-0058")
ADJACENT_PALACE_SOURCE_RELATION_ID = "ZZTERM-R-0057-0058"
ADJACENT_PALACE_SOURCE_TERM_ID = "ZZTERM-PAL-04"
COUNTERCLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL = 2
COUNTERCLOCKWISE_NEIGHBOR_CLOCKWISE_OFFSET = 11
COUNTERCLOCKWISE_NEIGHBOR_RELATIVE_ROLE = "SIBLINGS"
CLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL = 12
CLOCKWISE_NEIGHBOR_CLOCKWISE_OFFSET = 1
CLOCKWISE_NEIGHBOR_RELATIVE_ROLE = "PARENTS"
ADJACENT_PALACE_SEMANTIC_SCOPE = "BILATERAL_ADJACENT_PALACE_GEOMETRY_ONLY"


@dataclass(frozen=True)
class ResolvedAdjacentPalacePairProfile:
    profile_id: str
    profile_version: str
    upstream_r2_profile_id: str
    upstream_r2_profile_version: str
    algorithm_id: str
    algorithm_version: str
    source_id: str
    source_family_id: str
    source_section: str
    source_runtime_path: str
    source_runtime_blob_sha: str
    source_paragraph_id: str
    source_segment_ids: tuple[str, ...]
    source_relation_id: str
    source_term_id: str
    counterclockwise_relative_ordinal: int
    counterclockwise_clockwise_offset: int
    counterclockwise_relative_role: str
    clockwise_relative_ordinal: int
    clockwise_clockwise_offset: int
    clockwise_relative_role: str
    semantic_scope: str
    direct_event_permission: bool
    direct_endpoint_permission: bool
    direct_score_permission: bool
    flank_semantics_permission: bool
    supported_time_layer: str

    def validate(self) -> "ResolvedAdjacentPalacePairProfile":
        required = {
            "profile_id": self.profile_id,
            "profile_version": self.profile_version,
            "upstream_r2_profile_id": self.upstream_r2_profile_id,
            "upstream_r2_profile_version": self.upstream_r2_profile_version,
            "algorithm_id": self.algorithm_id,
            "algorithm_version": self.algorithm_version,
            "source_id": self.source_id,
            "source_family_id": self.source_family_id,
            "source_section": self.source_section,
            "source_runtime_path": self.source_runtime_path,
            "source_runtime_blob_sha": self.source_runtime_blob_sha,
            "source_paragraph_id": self.source_paragraph_id,
            "source_relation_id": self.source_relation_id,
            "source_term_id": self.source_term_id,
            "counterclockwise_relative_role": self.counterclockwise_relative_role,
            "clockwise_relative_role": self.clockwise_relative_role,
            "semantic_scope": self.semantic_scope,
            "supported_time_layer": self.supported_time_layer,
        }
        for label, value in required.items():
            if not value.strip():
                raise ValueError(f"{label} must not be empty")
        expected = {
            "profile_id": ZIWEI_STRUCTURAL_V2_R8_PROFILE_ID,
            "profile_version": ZIWEI_STRUCTURAL_V2_R8_PROFILE_VERSION,
            "upstream_r2_profile_id": ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID,
            "upstream_r2_profile_version": ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION,
            "algorithm_id": ADJACENT_PALACE_PAIR_ALGORITHM_ID,
            "algorithm_version": ADJACENT_PALACE_PAIR_ALGORITHM_VERSION,
            "source_id": ADJACENT_PALACE_SOURCE_ID,
            "source_family_id": ADJACENT_PALACE_SOURCE_FAMILY_ID,
            "source_section": ADJACENT_PALACE_SOURCE_SECTION,
            "source_runtime_path": ADJACENT_PALACE_SOURCE_RUNTIME_PATH,
            "source_runtime_blob_sha": ADJACENT_PALACE_SOURCE_RUNTIME_BLOB_SHA,
            "source_paragraph_id": ADJACENT_PALACE_SOURCE_PARAGRAPH_ID,
            "source_segment_ids": ADJACENT_PALACE_SOURCE_SEGMENT_IDS,
            "source_relation_id": ADJACENT_PALACE_SOURCE_RELATION_ID,
            "source_term_id": ADJACENT_PALACE_SOURCE_TERM_ID,
            "counterclockwise_relative_ordinal": COUNTERCLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL,
            "counterclockwise_clockwise_offset": COUNTERCLOCKWISE_NEIGHBOR_CLOCKWISE_OFFSET,
            "counterclockwise_relative_role": COUNTERCLOCKWISE_NEIGHBOR_RELATIVE_ROLE,
            "clockwise_relative_ordinal": CLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL,
            "clockwise_clockwise_offset": CLOCKWISE_NEIGHBOR_CLOCKWISE_OFFSET,
            "clockwise_relative_role": CLOCKWISE_NEIGHBOR_RELATIVE_ROLE,
            "semantic_scope": ADJACENT_PALACE_SEMANTIC_SCOPE,
            "direct_event_permission": False,
            "direct_endpoint_permission": False,
            "direct_score_permission": False,
            "flank_semantics_permission": False,
            "supported_time_layer": "NATAL",
        }
        for label, value in expected.items():
            if getattr(self, label) != value:
                raise ValueError(f"unsupported R8 {label}: {getattr(self, label)!r}")
        return self


def ziwei_structural_v2_r8_profile() -> ResolvedAdjacentPalacePairProfile:
    return ResolvedAdjacentPalacePairProfile(
        profile_id=ZIWEI_STRUCTURAL_V2_R8_PROFILE_ID,
        profile_version=ZIWEI_STRUCTURAL_V2_R8_PROFILE_VERSION,
        upstream_r2_profile_id=ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID,
        upstream_r2_profile_version=ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION,
        algorithm_id=ADJACENT_PALACE_PAIR_ALGORITHM_ID,
        algorithm_version=ADJACENT_PALACE_PAIR_ALGORITHM_VERSION,
        source_id=ADJACENT_PALACE_SOURCE_ID,
        source_family_id=ADJACENT_PALACE_SOURCE_FAMILY_ID,
        source_section=ADJACENT_PALACE_SOURCE_SECTION,
        source_runtime_path=ADJACENT_PALACE_SOURCE_RUNTIME_PATH,
        source_runtime_blob_sha=ADJACENT_PALACE_SOURCE_RUNTIME_BLOB_SHA,
        source_paragraph_id=ADJACENT_PALACE_SOURCE_PARAGRAPH_ID,
        source_segment_ids=ADJACENT_PALACE_SOURCE_SEGMENT_IDS,
        source_relation_id=ADJACENT_PALACE_SOURCE_RELATION_ID,
        source_term_id=ADJACENT_PALACE_SOURCE_TERM_ID,
        counterclockwise_relative_ordinal=COUNTERCLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL,
        counterclockwise_clockwise_offset=COUNTERCLOCKWISE_NEIGHBOR_CLOCKWISE_OFFSET,
        counterclockwise_relative_role=COUNTERCLOCKWISE_NEIGHBOR_RELATIVE_ROLE,
        clockwise_relative_ordinal=CLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL,
        clockwise_clockwise_offset=CLOCKWISE_NEIGHBOR_CLOCKWISE_OFFSET,
        clockwise_relative_role=CLOCKWISE_NEIGHBOR_RELATIVE_ROLE,
        semantic_scope=ADJACENT_PALACE_SEMANTIC_SCOPE,
        direct_event_permission=False,
        direct_endpoint_permission=False,
        direct_score_permission=False,
        flank_semantics_permission=False,
        supported_time_layer="NATAL",
    ).validate()
