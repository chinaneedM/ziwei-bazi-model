from __future__ import annotations

from dataclasses import dataclass


DIRECTION_RULE_SET_ID = "BAZI-DAYUN-DIRECTION-YEAR-STEM-SEX-R1"
DIRECTION_RULE_SET_VERSION = "1.0.0"
ANCHOR_RULE_SET_ID = "BAZI-DAYUN-JIE-ANCHOR-R1"
ANCHOR_RULE_SET_VERSION = "1.0.0"
SYMBOLIC_AGE_RULE_SET_ID = "BAZI-THREE-DAYS-ONE-YEAR-360D-R1"
SYMBOLIC_AGE_RULE_SET_VERSION = "1.0.0"
DAYUN_SEQUENCE_RULE_SET_ID = "BAZI-DAYUN-MONTH-PILLAR-SEQUENCE-R1"
DAYUN_SEQUENCE_RULE_SET_VERSION = "1.0.0"

TEMPORAL_ALGORITHM_ID = "BAZI-DAYUN-TEMPORAL-ENGINE-V1"
TEMPORAL_ALGORITHM_VERSION = "1.0.0"


@dataclass(frozen=True)
class ResolvedBaziTemporalProfile:
    """Explicit Dayun temporal conventions; no profile is implied by natal facts."""

    profile_id: str
    profile_version: str
    direction_rule_set_id: str = DIRECTION_RULE_SET_ID
    direction_rule_set_version: str = DIRECTION_RULE_SET_VERSION
    anchor_rule_set_id: str = ANCHOR_RULE_SET_ID
    anchor_rule_set_version: str = ANCHOR_RULE_SET_VERSION
    interval_coordinate_policy: str = "ABSOLUTE_UTC_DURATION"
    interval_granularity_rule_set: str = "MODERN_CONTINUOUS_MICROSECOND"
    symbolic_age_rule_set_id: str = SYMBOLIC_AGE_RULE_SET_ID
    symbolic_age_rule_set_version: str = SYMBOLIC_AGE_RULE_SET_VERSION
    calendar_realization_rule_set: str = "MODERN_CONTINUOUS_RATIO_120X"
    calendar_realization_source_class: str = "ENGINEERING_INTERPOLATION"
    dayun_sequence_rule_set_id: str = DAYUN_SEQUENCE_RULE_SET_ID
    dayun_sequence_rule_set_version: str = DAYUN_SEQUENCE_RULE_SET_VERSION
    dayun_boundary_rule_set: str = "PROLEPTIC_GREGORIAN_10Y_UTC_ANNIVERSARY"
    interval_semantics: str = "START_INCLUSIVE_END_EXCLUSIVE"
    algorithm_id: str = TEMPORAL_ALGORITHM_ID
    algorithm_version: str = TEMPORAL_ALGORITHM_VERSION

    def validate(self) -> "ResolvedBaziTemporalProfile":
        if not self.profile_id.strip() or not self.profile_version.strip():
            raise ValueError("Bazi temporal profile id/version must be non-empty")
        expected = {
            "direction_rule_set_id": DIRECTION_RULE_SET_ID,
            "direction_rule_set_version": DIRECTION_RULE_SET_VERSION,
            "anchor_rule_set_id": ANCHOR_RULE_SET_ID,
            "anchor_rule_set_version": ANCHOR_RULE_SET_VERSION,
            "interval_coordinate_policy": "ABSOLUTE_UTC_DURATION",
            "interval_granularity_rule_set": "MODERN_CONTINUOUS_MICROSECOND",
            "symbolic_age_rule_set_id": SYMBOLIC_AGE_RULE_SET_ID,
            "symbolic_age_rule_set_version": SYMBOLIC_AGE_RULE_SET_VERSION,
            "calendar_realization_rule_set": "MODERN_CONTINUOUS_RATIO_120X",
            "calendar_realization_source_class": "ENGINEERING_INTERPOLATION",
            "dayun_sequence_rule_set_id": DAYUN_SEQUENCE_RULE_SET_ID,
            "dayun_sequence_rule_set_version": DAYUN_SEQUENCE_RULE_SET_VERSION,
            "dayun_boundary_rule_set": "PROLEPTIC_GREGORIAN_10Y_UTC_ANNIVERSARY",
            "interval_semantics": "START_INCLUSIVE_END_EXCLUSIVE",
            "algorithm_id": TEMPORAL_ALGORITHM_ID,
            "algorithm_version": TEMPORAL_ALGORITHM_VERSION,
        }
        for field, value in expected.items():
            if getattr(self, field) != value:
                raise ValueError(f"unsupported Bazi temporal {field}: {getattr(self, field)!r}")
        return self


def bazi_temporal_v1_continuous_profile() -> ResolvedBaziTemporalProfile:
    """First operational Jiaoyun realization.

    This profile is intentionally named as an engineering interpolation, not a
    claim that continuous microsecond x120 is the unique classical calendar
    realization. Classical lunisolar/anniversary profiles remain separate work.
    """

    return ResolvedBaziTemporalProfile(
        profile_id="BAZI-TEMPORAL-V1-CONTINUOUS-R1",
        profile_version="1.0.0",
    )
