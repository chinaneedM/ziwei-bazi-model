from __future__ import annotations

from dataclasses import dataclass


INCIDENCE_PROFILE_ID = "BAZI-RELATION-INCIDENCE-FOUNDATION-R1"
INCIDENCE_PROFILE_VERSION = "1.0.0"
INCIDENCE_ALGORITHM_ID = "BAZI-RELATION-INCIDENCE-ENGINE-V1"
INCIDENCE_ALGORITHM_VERSION = "1.0.0"
SNAPSHOT_RULE_SET_ID = "BAZI-RELATION-INCIDENCE-SNAPSHOT-R1"
SNAPSHOT_RULE_SET_VERSION = "1.0.0"
OCCURRENCE_REFERENCE_RULE_SET_ID = "BAZI-RELEASED-RELATION-OCCURRENCE-REFERENCE-R1"
OCCURRENCE_REFERENCE_RULE_SET_VERSION = "1.0.0"
PARTICIPANT_INCIDENCE_RULE_SET_ID = "BAZI-PARTICIPANT-RELATION-INCIDENCE-R1"
PARTICIPANT_INCIDENCE_RULE_SET_VERSION = "1.0.0"
PAIR_TOPOLOGY_RULE_SET_ID = "BAZI-EXACT-RELATION-PAIR-TOPOLOGY-R1"
PAIR_TOPOLOGY_RULE_SET_VERSION = "1.0.0"
SUPPORT_TOUCH_RULE_SET_ID = "BAZI-EXACT-SUPPORT-TOUCH-R1"
SUPPORT_TOUCH_RULE_SET_VERSION = "1.0.0"
CANDIDATE_PAIRING_RULE_SET_ID = "BAZI-INCIDENCE-LINEAGE-PAIRING-R1"
CANDIDATE_PAIRING_RULE_SET_VERSION = "1.0.0"


@dataclass(frozen=True)
class ResolvedBaziRelationIncidenceProfile:
    """Explicit single-snapshot, exact-ID Relation Incidence R1 profile."""

    profile_id: str = INCIDENCE_PROFILE_ID
    profile_version: str = INCIDENCE_PROFILE_VERSION
    algorithm_id: str = INCIDENCE_ALGORITHM_ID
    algorithm_version: str = INCIDENCE_ALGORITHM_VERSION
    snapshot_rule_set_id: str = SNAPSHOT_RULE_SET_ID
    snapshot_rule_set_version: str = SNAPSHOT_RULE_SET_VERSION
    occurrence_reference_rule_set_id: str = OCCURRENCE_REFERENCE_RULE_SET_ID
    occurrence_reference_rule_set_version: str = OCCURRENCE_REFERENCE_RULE_SET_VERSION
    participant_incidence_rule_set_id: str = PARTICIPANT_INCIDENCE_RULE_SET_ID
    participant_incidence_rule_set_version: str = PARTICIPANT_INCIDENCE_RULE_SET_VERSION
    pair_topology_rule_set_id: str = PAIR_TOPOLOGY_RULE_SET_ID
    pair_topology_rule_set_version: str = PAIR_TOPOLOGY_RULE_SET_VERSION
    support_touch_rule_set_id: str = SUPPORT_TOUCH_RULE_SET_ID
    support_touch_rule_set_version: str = SUPPORT_TOUCH_RULE_SET_VERSION
    candidate_pairing_rule_set_id: str = CANDIDATE_PAIRING_RULE_SET_ID
    candidate_pairing_rule_set_version: str = CANDIDATE_PAIRING_RULE_SET_VERSION

    def validate(self) -> "ResolvedBaziRelationIncidenceProfile":
        expected = ResolvedBaziRelationIncidenceProfile()
        if self != expected:
            raise ValueError(f"unsupported Bazi relation incidence profile: {self!r}")
        return self


def bazi_relation_incidence_foundation_r1_profile(
) -> ResolvedBaziRelationIncidenceProfile:
    return ResolvedBaziRelationIncidenceProfile()
