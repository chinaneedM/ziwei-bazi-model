from __future__ import annotations

from dataclasses import dataclass

from fortune_training.calendar_foundation.policies import PolicyRegistry, PolicySelection

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
        return self
