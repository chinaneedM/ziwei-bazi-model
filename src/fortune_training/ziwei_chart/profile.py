from __future__ import annotations

from dataclasses import dataclass

from fortune_training.calendar_foundation.policies import PolicyRegistry, PolicySelection

from .auxiliary import (
    AUXILIARY_ALGORITHM_ID,
    AUXILIARY_ALGORITHM_VERSION,
    QS_CORE_AUX_RULE_SET_ID,
    QS_CORE_AUX_RULE_SET_VERSION,
)
from .main_stars import MAIN_STAR_ALGORITHM_ID, MAIN_STAR_ALGORITHM_VERSION
from .natal import NATAL_STRUCTURE_ALGORITHM_ID, NATAL_STRUCTURE_ALGORITHM_VERSION


@dataclass(frozen=True)
class ResolvedZiweiCalculationProfile:
    """Immutable rule snapshot required before any Ziwei chart generation begins."""

    profile_id: str
    profile_version: str
    time_calendar_policy_registry_version: str
    time_calendar_policies: PolicySelection
    natal_structure_algorithm_id: str = NATAL_STRUCTURE_ALGORITHM_ID
    natal_structure_algorithm_version: str = NATAL_STRUCTURE_ALGORITHM_VERSION
    main_star_algorithm_id: str = MAIN_STAR_ALGORITHM_ID
    main_star_algorithm_version: str = MAIN_STAR_ALGORITHM_VERSION
    auxiliary_rule_set_id: str | None = None
    auxiliary_rule_set_version: str | None = None
    auxiliary_algorithm_id: str | None = None
    auxiliary_algorithm_version: str | None = None

    def validate(self, policy_registry: PolicyRegistry) -> "ResolvedZiweiCalculationProfile":
        if not self.profile_id.strip():
            raise ValueError("profile_id must not be empty")
        if not self.profile_version.strip():
            raise ValueError("profile_version must not be empty")
        if self.time_calendar_policy_registry_version != policy_registry.version:
            raise ValueError(
                "time/calendar policy registry version mismatch: "
                f"profile={self.time_calendar_policy_registry_version} runtime={policy_registry.version}"
            )
        policy_registry.validate_selection(self.time_calendar_policies)
        if self.natal_structure_algorithm_id != NATAL_STRUCTURE_ALGORITHM_ID:
            raise ValueError("unsupported natal-structure algorithm id")
        if self.natal_structure_algorithm_version != NATAL_STRUCTURE_ALGORITHM_VERSION:
            raise ValueError("unsupported natal-structure algorithm version")
        if self.main_star_algorithm_id != MAIN_STAR_ALGORITHM_ID:
            raise ValueError("unsupported main-star algorithm id")
        if self.main_star_algorithm_version != MAIN_STAR_ALGORITHM_VERSION:
            raise ValueError("unsupported main-star algorithm version")

        aux_values = (
            self.auxiliary_rule_set_id,
            self.auxiliary_rule_set_version,
            self.auxiliary_algorithm_id,
            self.auxiliary_algorithm_version,
        )
        if all(value is None for value in aux_values):
            return self
        if any(value is None for value in aux_values):
            raise ValueError("auxiliary profile binding must be fully specified or fully disabled")
        if self.auxiliary_rule_set_id != QS_CORE_AUX_RULE_SET_ID:
            raise ValueError(f"unsupported auxiliary rule set: {self.auxiliary_rule_set_id}")
        if self.auxiliary_rule_set_version != QS_CORE_AUX_RULE_SET_VERSION:
            raise ValueError("unsupported auxiliary rule-set version")
        if self.auxiliary_algorithm_id != AUXILIARY_ALGORITHM_ID:
            raise ValueError("unsupported auxiliary algorithm id")
        if self.auxiliary_algorithm_version != AUXILIARY_ALGORITHM_VERSION:
            raise ValueError("unsupported auxiliary algorithm version")
        return self
