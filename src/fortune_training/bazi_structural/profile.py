from __future__ import annotations

from dataclasses import dataclass


STRUCTURAL_PROFILE_ID = "BAZI-STRUCTURAL-CONTEXT-R1"
STRUCTURAL_PROFILE_VERSION = "1.1.0"
STRUCTURAL_ALGORITHM_ID = "BAZI-STRUCTURAL-CONTEXT-ENGINE-V1"
STRUCTURAL_ALGORITHM_VERSION = "1.1.0"
PARTICIPANT_RULE_SET_ID = "BAZI-ACTIVE-TEMPORAL-PARTICIPANT-R1"
PARTICIPANT_RULE_SET_VERSION = "1.0.0"
RELATION_SCOPE_RULE_SET_ID = "BAZI-DYNAMIC-RELATION-SCOPE-R1"
RELATION_SCOPE_RULE_SET_VERSION = "1.0.0"


@dataclass(frozen=True)
class ResolvedBaziStructuralProfile:
    """Explicit neutral Structural Context R1 calculation profile."""

    profile_id: str = STRUCTURAL_PROFILE_ID
    profile_version: str = STRUCTURAL_PROFILE_VERSION
    algorithm_id: str = STRUCTURAL_ALGORITHM_ID
    algorithm_version: str = STRUCTURAL_ALGORITHM_VERSION
    participant_rule_set_id: str = PARTICIPANT_RULE_SET_ID
    participant_rule_set_version: str = PARTICIPANT_RULE_SET_VERSION
    relation_scope_rule_set_id: str = RELATION_SCOPE_RULE_SET_ID
    relation_scope_rule_set_version: str = RELATION_SCOPE_RULE_SET_VERSION

    def validate(self) -> "ResolvedBaziStructuralProfile":
        expected = ResolvedBaziStructuralProfile()
        if self != expected:
            raise ValueError(f"unsupported Bazi structural profile: {self!r}")
        return self


def bazi_structural_context_r1_profile() -> ResolvedBaziStructuralProfile:
    return ResolvedBaziStructuralProfile()
