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
TEMPORAL_ALGORITHM_VERSION = "1.0.1"
WENZHEN_TEMPORAL_ALGORITHM_VERSION = "1.1.0"

CONTINUOUS_PROFILE_ID = "BAZI-TEMPORAL-V1-CONTINUOUS-R1"
WENZHEN_CHINA_COMPATIBILITY_PROFILE_ID = (
    "BAZI-TEMPORAL-WENZHEN-CHINA-COMPATIBILITY-R1"
)

CONTINUOUS_INTERVAL_COORDINATE_POLICY = "ABSOLUTE_UTC_DURATION"
WENZHEN_INTERVAL_COORDINATE_POLICY = (
    "BIRTH_LOCAL_APPARENT_SOLAR_CLOCK_TO_JIE_CHINA_STANDARD_CLOCK"
)
CONTINUOUS_INTERVAL_GRANULARITY_RULE_SET = "MODERN_CONTINUOUS_MICROSECOND"
WENZHEN_INTERVAL_GRANULARITY_RULE_SET = (
    "WENZHEN_UI_HOUR_OBSERVED_INTERNAL_MICROSECOND_R1"
)
CONTINUOUS_CALENDAR_REALIZATION_RULE_SET = "MODERN_CONTINUOUS_RATIO_120X"
WENZHEN_CALENDAR_REALIZATION_RULE_SET = (
    "CALENDAR_MONTH_DISPLACEMENT_THEN_DAY_HOUR_R1"
)
CONTINUOUS_CALENDAR_REALIZATION_SOURCE_CLASS = "ENGINEERING_INTERPOLATION"
WENZHEN_CALENDAR_REALIZATION_SOURCE_CLASS = (
    "THIRD_PARTY_COMPATIBILITY_WITNESS"
)
CONTINUOUS_DAYUN_BOUNDARY_RULE_SET = (
    "PROLEPTIC_GREGORIAN_10Y_UTC_ANNIVERSARY"
)
WENZHEN_DAYUN_BOUNDARY_RULE_SET = (
    "PROLEPTIC_GREGORIAN_10Y_CHINA_STANDARD_ANNIVERSARY"
)


@dataclass(frozen=True)
class ResolvedBaziTemporalProfile:
    """Explicit Dayun temporal conventions; no profile is implied by natal facts."""

    profile_id: str
    profile_version: str
    direction_rule_set_id: str = DIRECTION_RULE_SET_ID
    direction_rule_set_version: str = DIRECTION_RULE_SET_VERSION
    anchor_rule_set_id: str = ANCHOR_RULE_SET_ID
    anchor_rule_set_version: str = ANCHOR_RULE_SET_VERSION
    exact_jie_tie_policy: str = "FAIL_CLOSED"
    interval_coordinate_policy: str = CONTINUOUS_INTERVAL_COORDINATE_POLICY
    interval_granularity_rule_set: str = CONTINUOUS_INTERVAL_GRANULARITY_RULE_SET
    symbolic_age_rule_set_id: str = SYMBOLIC_AGE_RULE_SET_ID
    symbolic_age_rule_set_version: str = SYMBOLIC_AGE_RULE_SET_VERSION
    calendar_realization_rule_set: str = CONTINUOUS_CALENDAR_REALIZATION_RULE_SET
    calendar_realization_source_class: str = CONTINUOUS_CALENDAR_REALIZATION_SOURCE_CLASS
    dayun_sequence_rule_set_id: str = DAYUN_SEQUENCE_RULE_SET_ID
    dayun_sequence_rule_set_version: str = DAYUN_SEQUENCE_RULE_SET_VERSION
    dayun_boundary_rule_set: str = CONTINUOUS_DAYUN_BOUNDARY_RULE_SET
    interval_semantics: str = "START_INCLUSIVE_END_EXCLUSIVE"
    algorithm_id: str = TEMPORAL_ALGORITHM_ID
    algorithm_version: str = TEMPORAL_ALGORITHM_VERSION

    def validate(self) -> "ResolvedBaziTemporalProfile":
        if not self.profile_id.strip() or not self.profile_version.strip():
            raise ValueError("Bazi temporal profile id/version must be non-empty")
        common = {
            "direction_rule_set_id": DIRECTION_RULE_SET_ID,
            "direction_rule_set_version": DIRECTION_RULE_SET_VERSION,
            "anchor_rule_set_id": ANCHOR_RULE_SET_ID,
            "anchor_rule_set_version": ANCHOR_RULE_SET_VERSION,
            "exact_jie_tie_policy": "FAIL_CLOSED",
            "symbolic_age_rule_set_id": SYMBOLIC_AGE_RULE_SET_ID,
            "symbolic_age_rule_set_version": SYMBOLIC_AGE_RULE_SET_VERSION,
            "dayun_sequence_rule_set_id": DAYUN_SEQUENCE_RULE_SET_ID,
            "dayun_sequence_rule_set_version": DAYUN_SEQUENCE_RULE_SET_VERSION,
            "interval_semantics": "START_INCLUSIVE_END_EXCLUSIVE",
            "algorithm_id": TEMPORAL_ALGORITHM_ID,
        }
        profile_specific = {
            CONTINUOUS_PROFILE_ID: {
                "profile_version": "1.0.0",
                "interval_coordinate_policy": CONTINUOUS_INTERVAL_COORDINATE_POLICY,
                "interval_granularity_rule_set": CONTINUOUS_INTERVAL_GRANULARITY_RULE_SET,
                "calendar_realization_rule_set": CONTINUOUS_CALENDAR_REALIZATION_RULE_SET,
                "calendar_realization_source_class": CONTINUOUS_CALENDAR_REALIZATION_SOURCE_CLASS,
                "dayun_boundary_rule_set": CONTINUOUS_DAYUN_BOUNDARY_RULE_SET,
                "algorithm_version": TEMPORAL_ALGORITHM_VERSION,
            },
            WENZHEN_CHINA_COMPATIBILITY_PROFILE_ID: {
                "profile_version": "1.0.0",
                "interval_coordinate_policy": WENZHEN_INTERVAL_COORDINATE_POLICY,
                "interval_granularity_rule_set": WENZHEN_INTERVAL_GRANULARITY_RULE_SET,
                "calendar_realization_rule_set": WENZHEN_CALENDAR_REALIZATION_RULE_SET,
                "calendar_realization_source_class": WENZHEN_CALENDAR_REALIZATION_SOURCE_CLASS,
                "dayun_boundary_rule_set": WENZHEN_DAYUN_BOUNDARY_RULE_SET,
                "algorithm_version": WENZHEN_TEMPORAL_ALGORITHM_VERSION,
            },
        }
        expected = profile_specific.get(self.profile_id)
        if expected is None:
            raise ValueError(f"unsupported Bazi temporal profile: {self.profile_id!r}")
        expected = {**common, **expected}
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
        profile_id=CONTINUOUS_PROFILE_ID,
        profile_version="1.0.0",
    )


def bazi_temporal_wenzhen_china_compatibility_r1_profile() -> ResolvedBaziTemporalProfile:
    """Externally observed Wenzhen China Dayun compatibility behavior.

    This profile is deliberately separate from shared calendar truth.  Its
    mixed-clock interval and calendar-month realization are compatibility
    rules inferred from A7--A11, and its minute/second transition is not
    represented as independently certified Wenzhen UI output.
    """

    return ResolvedBaziTemporalProfile(
        profile_id=WENZHEN_CHINA_COMPATIBILITY_PROFILE_ID,
        profile_version="1.0.0",
        interval_coordinate_policy=WENZHEN_INTERVAL_COORDINATE_POLICY,
        interval_granularity_rule_set=WENZHEN_INTERVAL_GRANULARITY_RULE_SET,
        calendar_realization_rule_set=WENZHEN_CALENDAR_REALIZATION_RULE_SET,
        calendar_realization_source_class=WENZHEN_CALENDAR_REALIZATION_SOURCE_CLASS,
        dayun_boundary_rule_set=WENZHEN_DAYUN_BOUNDARY_RULE_SET,
        algorithm_version=WENZHEN_TEMPORAL_ALGORITHM_VERSION,
    )
