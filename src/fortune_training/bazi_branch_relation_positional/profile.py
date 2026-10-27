from __future__ import annotations

from dataclasses import dataclass


POSITIONAL_PROFILE_ID = "BAZI-BRANCH-RELATION-POSITIONAL-CONTEXT-FOUNDATION-R1"
POSITIONAL_PROFILE_VERSION = "1.0.0"
POSITIONAL_ALGORITHM_ID = "BAZI-BRANCH-RELATION-POSITIONAL-ENGINE-V1"
POSITIONAL_ALGORITHM_VERSION = "1.0.0"
SNAPSHOT_RULE_SET_ID = "BAZI-BRANCH-RELATION-POSITIONAL-SNAPSHOT-R1"
SNAPSHOT_RULE_SET_VERSION = "1.0.0"
PARTICIPANT_POSITION_RULE_SET_ID = "BAZI-BRANCH-PARTICIPANT-POSITION-REFERENCE-R1"
PARTICIPANT_POSITION_RULE_SET_VERSION = "1.0.0"
RELATION_POSITION_RULE_SET_ID = "BAZI-BRANCH-RELATION-POSITIONAL-FACT-R1"
RELATION_POSITION_RULE_SET_VERSION = "1.0.0"
CANDIDATE_LINEAGE_RULE_SET_ID = "BAZI-BRANCH-POSITIONAL-INCIDENCE-LINEAGE-R1"
CANDIDATE_LINEAGE_RULE_SET_VERSION = "1.0.0"


@dataclass(frozen=True)
class ResolvedBaziBranchRelationPositionalProfile:
    """Exact, typed, neutral visible-branch positional context profile."""

    profile_id: str = POSITIONAL_PROFILE_ID
    profile_version: str = POSITIONAL_PROFILE_VERSION
    algorithm_id: str = POSITIONAL_ALGORITHM_ID
    algorithm_version: str = POSITIONAL_ALGORITHM_VERSION
    snapshot_rule_set_id: str = SNAPSHOT_RULE_SET_ID
    snapshot_rule_set_version: str = SNAPSHOT_RULE_SET_VERSION
    participant_position_rule_set_id: str = PARTICIPANT_POSITION_RULE_SET_ID
    participant_position_rule_set_version: str = PARTICIPANT_POSITION_RULE_SET_VERSION
    relation_position_rule_set_id: str = RELATION_POSITION_RULE_SET_ID
    relation_position_rule_set_version: str = RELATION_POSITION_RULE_SET_VERSION
    candidate_lineage_rule_set_id: str = CANDIDATE_LINEAGE_RULE_SET_ID
    candidate_lineage_rule_set_version: str = CANDIDATE_LINEAGE_RULE_SET_VERSION

    def validate(self) -> "ResolvedBaziBranchRelationPositionalProfile":
        expected = ResolvedBaziBranchRelationPositionalProfile()
        if self != expected:
            raise ValueError(f"unsupported Bazi branch positional profile: {self!r}")
        return self


def bazi_branch_relation_positional_context_foundation_r1_profile(
) -> ResolvedBaziBranchRelationPositionalProfile:
    return ResolvedBaziBranchRelationPositionalProfile()
