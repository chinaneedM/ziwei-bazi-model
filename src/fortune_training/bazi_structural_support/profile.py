from __future__ import annotations

from dataclasses import dataclass


SUPPORT_PROFILE_ID = "BAZI-STRUCTURAL-SUPPORT-FOUNDATION-R1"
SUPPORT_PROFILE_VERSION = "1.0.0"
SUPPORT_ALGORITHM_ID = "BAZI-STRUCTURAL-SUPPORT-ENGINE-V1"
SUPPORT_ALGORITHM_VERSION = "1.0.0"
SEASONAL_ROLE_RULE_SET_ID = "BAZI-SEASONAL-REFERENCE-ROLE-R1"
SEASONAL_ROLE_RULE_SET_VERSION = "1.0.0"
SUPPORT_EVIDENCE_RULE_SET_ID = "BAZI-ROOT-SUPPORT-EVIDENCE-CANDIDATE-R1"
SUPPORT_EVIDENCE_RULE_SET_VERSION = "1.0.0"


@dataclass(frozen=True)
class ResolvedBaziStructuralSupportProfile:
    """Explicit non-interpretive Structural Support Foundation R1 profile."""

    profile_id: str = SUPPORT_PROFILE_ID
    profile_version: str = SUPPORT_PROFILE_VERSION
    algorithm_id: str = SUPPORT_ALGORITHM_ID
    algorithm_version: str = SUPPORT_ALGORITHM_VERSION
    seasonal_role_rule_set_id: str = SEASONAL_ROLE_RULE_SET_ID
    seasonal_role_rule_set_version: str = SEASONAL_ROLE_RULE_SET_VERSION
    support_evidence_rule_set_id: str = SUPPORT_EVIDENCE_RULE_SET_ID
    support_evidence_rule_set_version: str = SUPPORT_EVIDENCE_RULE_SET_VERSION

    def validate(self) -> "ResolvedBaziStructuralSupportProfile":
        expected = ResolvedBaziStructuralSupportProfile()
        if self != expected:
            raise ValueError(f"unsupported Bazi structural support profile: {self!r}")
        return self


def bazi_structural_support_foundation_r1_profile() -> ResolvedBaziStructuralSupportProfile:
    return ResolvedBaziStructuralSupportProfile()
