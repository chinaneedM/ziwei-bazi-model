from __future__ import annotations

from dataclasses import dataclass


POSITIONAL_PROFILE_ID = "BAZI-STEM-RELATION-POSITIONAL-CONTEXT-FOUNDATION-R1"
POSITIONAL_PROFILE_VERSION = "1.0.0"
POSITIONAL_ALGORITHM_ID = "BAZI-STEM-RELATION-POSITIONAL-ENGINE-V1"
POSITIONAL_ALGORITHM_VERSION = "1.0.0"
SNAPSHOT_RULE_SET_ID = "BAZI-STEM-RELATION-POSITIONAL-SNAPSHOT-R1"
SNAPSHOT_RULE_SET_VERSION = "1.0.0"
PARTICIPANT_POSITION_RULE_SET_ID = "BAZI-STEM-PARTICIPANT-POSITION-REFERENCE-R1"
PARTICIPANT_POSITION_RULE_SET_VERSION = "1.0.0"
PAIR_POSITION_RULE_SET_ID = "BAZI-STEM-PAIR-POSITIONAL-FACT-R1"
PAIR_POSITION_RULE_SET_VERSION = "1.0.0"
CANDIDATE_LINEAGE_RULE_SET_ID = "BAZI-POSITIONAL-INCIDENCE-LINEAGE-R1"
CANDIDATE_LINEAGE_RULE_SET_VERSION = "1.0.0"


@dataclass(frozen=True)
class ResolvedBaziStemRelationPositionalProfile:
    """Exact, neutral visible-stem positional context profile."""

    profile_id: str = POSITIONAL_PROFILE_ID
    profile_version: str = POSITIONAL_PROFILE_VERSION
    algorithm_id: str = POSITIONAL_ALGORITHM_ID
    algorithm_version: str = POSITIONAL_ALGORITHM_VERSION
    snapshot_rule_set_id: str = SNAPSHOT_RULE_SET_ID
    snapshot_rule_set_version: str = SNAPSHOT_RULE_SET_VERSION
    participant_position_rule_set_id: str = PARTICIPANT_POSITION_RULE_SET_ID
    participant_position_rule_set_version: str = PARTICIPANT_POSITION_RULE_SET_VERSION
    pair_position_rule_set_id: str = PAIR_POSITION_RULE_SET_ID
    pair_position_rule_set_version: str = PAIR_POSITION_RULE_SET_VERSION
    candidate_lineage_rule_set_id: str = CANDIDATE_LINEAGE_RULE_SET_ID
    candidate_lineage_rule_set_version: str = CANDIDATE_LINEAGE_RULE_SET_VERSION

    def validate(self) -> "ResolvedBaziStemRelationPositionalProfile":
        expected = ResolvedBaziStemRelationPositionalProfile()
        if self != expected:
            raise ValueError(f"unsupported Bazi stem positional profile: {self!r}")
        return self


def bazi_stem_relation_positional_context_foundation_r1_profile(
) -> ResolvedBaziStemRelationPositionalProfile:
    return ResolvedBaziStemRelationPositionalProfile()
