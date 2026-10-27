from __future__ import annotations

from dataclasses import dataclass

from fortune_training.ziwei_structural.r2.profile import (
    ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID,
    ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION,
)


ZIWEI_STRUCTURAL_V2_R4_PROFILE_ID = "ZIWEI-STRUCTURAL-RUNTIME-V2-R4"
ZIWEI_STRUCTURAL_V2_R4_PROFILE_VERSION = "1.0.0"
NAMED_STRUCTURAL_SEMANTIC_ALGORITHM_ID = "ZIWEI-NAMED-SANFANG-SIZHENG"
NAMED_STRUCTURAL_SEMANTIC_ALGORITHM_VERSION = "1.0.0"
S04_CANONICAL_SOURCE_ID = "S04"
S04_CANONICAL_SOURCE_SHA256 = "f7720ee4a11ce36155007cc3846620bcebdeaf5d98447c4abe427b37348e6c4f"
S04_CANONICAL_MANIFEST_OBJECT_SHA256 = (
    "da7b511bb5734c09febccbe0ed54170490c27a6c0249df79e87c496f10d3e5e6"
)
S04_SANFANG_SIZHENG_RULE_SET_ID = "S04-SANFANG-SIZHENG-CORRECTION-R1"
S04_SANFANG_SIZHENG_RULE_SET_VERSION = "1.0.0"


@dataclass(frozen=True)
class ResolvedNamedStructuralSemanticProfile:
    """Immutable R4 profile for source-bound named Sanfang/Sizheng semantics."""

    profile_id: str
    profile_version: str
    upstream_r2_profile_id: str
    upstream_r2_profile_version: str
    semantic_algorithm_id: str
    semantic_algorithm_version: str
    canonical_source_id: str
    canonical_source_sha256: str
    canonical_manifest_object_sha256: str
    semantic_rule_set_id: str
    semantic_rule_set_version: str

    def validate(self) -> "ResolvedNamedStructuralSemanticProfile":
        values = {
            "profile_id": self.profile_id,
            "profile_version": self.profile_version,
            "upstream_r2_profile_id": self.upstream_r2_profile_id,
            "upstream_r2_profile_version": self.upstream_r2_profile_version,
            "semantic_algorithm_id": self.semantic_algorithm_id,
            "semantic_algorithm_version": self.semantic_algorithm_version,
            "canonical_source_id": self.canonical_source_id,
            "canonical_source_sha256": self.canonical_source_sha256,
            "canonical_manifest_object_sha256": self.canonical_manifest_object_sha256,
            "semantic_rule_set_id": self.semantic_rule_set_id,
            "semantic_rule_set_version": self.semantic_rule_set_version,
        }
        for label, value in values.items():
            if not value.strip():
                raise ValueError(f"{label} must not be empty")

        expected = {
            "profile_id": ZIWEI_STRUCTURAL_V2_R4_PROFILE_ID,
            "profile_version": ZIWEI_STRUCTURAL_V2_R4_PROFILE_VERSION,
            "upstream_r2_profile_id": ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID,
            "upstream_r2_profile_version": ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION,
            "semantic_algorithm_id": NAMED_STRUCTURAL_SEMANTIC_ALGORITHM_ID,
            "semantic_algorithm_version": NAMED_STRUCTURAL_SEMANTIC_ALGORITHM_VERSION,
            "canonical_source_id": S04_CANONICAL_SOURCE_ID,
            "canonical_source_sha256": S04_CANONICAL_SOURCE_SHA256,
            "canonical_manifest_object_sha256": S04_CANONICAL_MANIFEST_OBJECT_SHA256,
            "semantic_rule_set_id": S04_SANFANG_SIZHENG_RULE_SET_ID,
            "semantic_rule_set_version": S04_SANFANG_SIZHENG_RULE_SET_VERSION,
        }
        for label, expected_value in expected.items():
            actual = getattr(self, label)
            if actual != expected_value:
                raise ValueError(f"unsupported {label}: {actual}")
        return self


def ziwei_structural_v2_r4_profile() -> ResolvedNamedStructuralSemanticProfile:
    return ResolvedNamedStructuralSemanticProfile(
        profile_id=ZIWEI_STRUCTURAL_V2_R4_PROFILE_ID,
        profile_version=ZIWEI_STRUCTURAL_V2_R4_PROFILE_VERSION,
        upstream_r2_profile_id=ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID,
        upstream_r2_profile_version=ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION,
        semantic_algorithm_id=NAMED_STRUCTURAL_SEMANTIC_ALGORITHM_ID,
        semantic_algorithm_version=NAMED_STRUCTURAL_SEMANTIC_ALGORITHM_VERSION,
        canonical_source_id=S04_CANONICAL_SOURCE_ID,
        canonical_source_sha256=S04_CANONICAL_SOURCE_SHA256,
        canonical_manifest_object_sha256=S04_CANONICAL_MANIFEST_OBJECT_SHA256,
        semantic_rule_set_id=S04_SANFANG_SIZHENG_RULE_SET_ID,
        semantic_rule_set_version=S04_SANFANG_SIZHENG_RULE_SET_VERSION,
    ).validate()
