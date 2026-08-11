from __future__ import annotations

from dataclasses import dataclass


TRANSITION_PROFILE_ID = "BAZI-RELATION-TRANSITION-FOUNDATION-R1"
TRANSITION_PROFILE_VERSION = "1.1.0"
TRANSITION_ALGORITHM_ID = "BAZI-RELATION-TRANSITION-ENGINE-V1"
TRANSITION_ALGORITHM_VERSION = "1.1.0"
SNAPSHOT_RULE_SET_ID = "BAZI-RAW-RELATION-SNAPSHOT-R1"
SNAPSHOT_RULE_SET_VERSION = "1.0.0"
SET_REPLAY_RULE_SET_ID = "BAZI-EXACT-RELATION-ID-SET-TRANSITION-R1"
SET_REPLAY_RULE_SET_VERSION = "1.0.0"
FRAME_DIFFERENCE_RULE_SET_ID = "BAZI-NEUTRAL-FRAME-DIFFERENCE-R1"
FRAME_DIFFERENCE_RULE_SET_VERSION = "1.0.0"
CANDIDATE_PAIRING_RULE_SET_ID = "BAZI-TRANSITION-LINEAGE-PAIRING-R1"
CANDIDATE_PAIRING_RULE_SET_VERSION = "1.0.0"


@dataclass(frozen=True)
class ResolvedBaziRelationTransitionProfile:
    """Explicit, mechanical Relation Transition Foundation R1 profile."""

    profile_id: str = TRANSITION_PROFILE_ID
    profile_version: str = TRANSITION_PROFILE_VERSION
    algorithm_id: str = TRANSITION_ALGORITHM_ID
    algorithm_version: str = TRANSITION_ALGORITHM_VERSION
    snapshot_rule_set_id: str = SNAPSHOT_RULE_SET_ID
    snapshot_rule_set_version: str = SNAPSHOT_RULE_SET_VERSION
    set_replay_rule_set_id: str = SET_REPLAY_RULE_SET_ID
    set_replay_rule_set_version: str = SET_REPLAY_RULE_SET_VERSION
    frame_difference_rule_set_id: str = FRAME_DIFFERENCE_RULE_SET_ID
    frame_difference_rule_set_version: str = FRAME_DIFFERENCE_RULE_SET_VERSION
    candidate_pairing_rule_set_id: str = CANDIDATE_PAIRING_RULE_SET_ID
    candidate_pairing_rule_set_version: str = CANDIDATE_PAIRING_RULE_SET_VERSION

    def validate(self) -> "ResolvedBaziRelationTransitionProfile":
        expected = ResolvedBaziRelationTransitionProfile()
        if self != expected:
            raise ValueError(f"unsupported Bazi relation transition profile: {self!r}")
        return self


def bazi_relation_transition_foundation_r1_profile(
) -> ResolvedBaziRelationTransitionProfile:
    return ResolvedBaziRelationTransitionProfile()
