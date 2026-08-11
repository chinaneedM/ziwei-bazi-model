from __future__ import annotations

from dataclasses import dataclass

from fortune_training.calendar_foundation.policies import BaziPolicySelection, PolicyRegistry

from .hidden_stems import (
    AFFINITY_ALGORITHM_ID,
    AFFINITY_ALGORITHM_VERSION,
    HIDDEN_STEM_ALGORITHM_ID,
    HIDDEN_STEM_ALGORITHM_VERSION,
)
from .registries import (
    AFFINITY_RULE_SET_ID,
    AFFINITY_RULE_SET_VERSION,
    HIDDEN_STEM_RULE_SET_ID,
    HIDDEN_STEM_RULE_SET_VERSION,
    RAW_RELATION_RULE_SET_ID,
    RAW_RELATION_RULE_SET_VERSION,
    SEXAGENARY_REGISTRY_ID,
    SEXAGENARY_REGISTRY_VERSION,
    TEN_GOD_RULE_SET_ID,
    TEN_GOD_RULE_SET_VERSION,
)
from .relations import RAW_RELATION_ALGORITHM_ID, RAW_RELATION_ALGORITHM_VERSION
from .ten_gods import TEN_GOD_ALGORITHM_ID, TEN_GOD_ALGORITHM_VERSION


NATAL_ALGORITHM_ID = "BAZI-NATAL-GENERATOR-V1"
NATAL_ALGORITHM_VERSION = "1.1.0"


@dataclass(frozen=True)
class ResolvedBaziCalculationProfile:
    """Immutable rule snapshot required before Bazi natal generation."""

    profile_id: str
    profile_version: str
    time_calendar_policy_registry_version: str
    time_calendar_policies: BaziPolicySelection
    time_coordinate_policy: str = "LOCAL_APPARENT_SOLAR"
    sexagenary_registry_id: str = SEXAGENARY_REGISTRY_ID
    sexagenary_registry_version: str = SEXAGENARY_REGISTRY_VERSION
    hidden_stem_rule_set_id: str = HIDDEN_STEM_RULE_SET_ID
    hidden_stem_rule_set_version: str = HIDDEN_STEM_RULE_SET_VERSION
    ten_god_rule_set_id: str = TEN_GOD_RULE_SET_ID
    ten_god_rule_set_version: str = TEN_GOD_RULE_SET_VERSION
    affinity_rule_set_id: str = AFFINITY_RULE_SET_ID
    affinity_rule_set_version: str = AFFINITY_RULE_SET_VERSION
    raw_relation_rule_set_id: str = RAW_RELATION_RULE_SET_ID
    raw_relation_rule_set_version: str = RAW_RELATION_RULE_SET_VERSION
    natal_algorithm_id: str = NATAL_ALGORITHM_ID
    natal_algorithm_version: str = NATAL_ALGORITHM_VERSION
    hidden_stem_algorithm_id: str = HIDDEN_STEM_ALGORITHM_ID
    hidden_stem_algorithm_version: str = HIDDEN_STEM_ALGORITHM_VERSION
    ten_god_algorithm_id: str = TEN_GOD_ALGORITHM_ID
    ten_god_algorithm_version: str = TEN_GOD_ALGORITHM_VERSION
    affinity_algorithm_id: str = AFFINITY_ALGORITHM_ID
    affinity_algorithm_version: str = AFFINITY_ALGORITHM_VERSION
    raw_relation_algorithm_id: str = RAW_RELATION_ALGORITHM_ID
    raw_relation_algorithm_version: str = RAW_RELATION_ALGORITHM_VERSION

    def validate(self, policy_registry: PolicyRegistry) -> "ResolvedBaziCalculationProfile":
        if not self.profile_id.strip() or not self.profile_version.strip():
            raise ValueError("Bazi profile id/version must be non-empty")
        if self.time_calendar_policy_registry_version != policy_registry.version:
            raise ValueError(
                "time/calendar policy registry version mismatch: "
                f"profile={self.time_calendar_policy_registry_version} runtime={policy_registry.version}"
            )
        policy_registry.validate_bazi_selection(self.time_calendar_policies)
        if self.time_coordinate_policy != "LOCAL_APPARENT_SOLAR":
            raise ValueError(f"unsupported Bazi time coordinate: {self.time_coordinate_policy}")

        expected = {
            "sexagenary_registry_id": SEXAGENARY_REGISTRY_ID,
            "sexagenary_registry_version": SEXAGENARY_REGISTRY_VERSION,
            "hidden_stem_rule_set_id": HIDDEN_STEM_RULE_SET_ID,
            "hidden_stem_rule_set_version": HIDDEN_STEM_RULE_SET_VERSION,
            "ten_god_rule_set_id": TEN_GOD_RULE_SET_ID,
            "ten_god_rule_set_version": TEN_GOD_RULE_SET_VERSION,
            "affinity_rule_set_id": AFFINITY_RULE_SET_ID,
            "affinity_rule_set_version": AFFINITY_RULE_SET_VERSION,
            "raw_relation_rule_set_id": RAW_RELATION_RULE_SET_ID,
            "raw_relation_rule_set_version": RAW_RELATION_RULE_SET_VERSION,
            "natal_algorithm_id": NATAL_ALGORITHM_ID,
            "natal_algorithm_version": NATAL_ALGORITHM_VERSION,
            "hidden_stem_algorithm_id": HIDDEN_STEM_ALGORITHM_ID,
            "hidden_stem_algorithm_version": HIDDEN_STEM_ALGORITHM_VERSION,
            "ten_god_algorithm_id": TEN_GOD_ALGORITHM_ID,
            "ten_god_algorithm_version": TEN_GOD_ALGORITHM_VERSION,
            "affinity_algorithm_id": AFFINITY_ALGORITHM_ID,
            "affinity_algorithm_version": AFFINITY_ALGORITHM_VERSION,
            "raw_relation_algorithm_id": RAW_RELATION_ALGORITHM_ID,
            "raw_relation_algorithm_version": RAW_RELATION_ALGORITHM_VERSION,
        }
        for field, value in expected.items():
            if getattr(self, field) != value:
                raise ValueError(f"unsupported {field}: {getattr(self, field)!r}")
        return self


def bazi_foundation_v1_profile(policy_registry: PolicyRegistry) -> ResolvedBaziCalculationProfile:
    return ResolvedBaziCalculationProfile(
        profile_id="BAZI-FOUNDATION-V1-R1",
        profile_version="1.1.0",
        time_calendar_policy_registry_version=policy_registry.version,
        time_calendar_policies=policy_registry.default_bazi_selection(),
    )
