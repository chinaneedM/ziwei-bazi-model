from __future__ import annotations

from dataclasses import dataclass

from fortune_training.calendar_foundation.policies import PolicyRegistry, PolicySelection

from .auxiliary import (
    AUXILIARY_ALGORITHM_ID,
    AUXILIARY_ALGORITHM_VERSION,
    QS_CORE_AUX_RULE_SET_ID,
    QS_CORE_AUX_RULE_SET_VERSION,
    WENMO_DEFAULT_CORE_AUX_RULE_SET_ID,
    WENMO_DEFAULT_CORE_AUX_RULE_SET_VERSION,
)
from .main_stars import MAIN_STAR_ALGORITHM_ID, MAIN_STAR_ALGORITHM_VERSION
from .natal import NATAL_STRUCTURE_ALGORITHM_ID, NATAL_STRUCTURE_ALGORITHM_VERSION
from .roles import (
    QS_ROLE_RULE_SET_ID,
    QS_ROLE_RULE_SET_VERSION,
    ROLE_ALGORITHM_ID,
    ROLE_ALGORITHM_VERSION,
    WENMO_DEFAULT_ROLE_RULE_SET_ID,
    WENMO_DEFAULT_ROLE_RULE_SET_VERSION,
)


@dataclass(frozen=True)
class ResolvedZiweiCalculationProfile:
    """Immutable rule snapshot required before any Ziwei chart generation begins."""

    profile_id: str
    profile_version: str
    time_calendar_policy_registry_version: str
    time_calendar_policies: PolicySelection
    ziwei_day_boundary_policy: str = "MIDNIGHT"
    natal_structure_algorithm_id: str = NATAL_STRUCTURE_ALGORITHM_ID
    natal_structure_algorithm_version: str = NATAL_STRUCTURE_ALGORITHM_VERSION
    main_star_algorithm_id: str = MAIN_STAR_ALGORITHM_ID
    main_star_algorithm_version: str = MAIN_STAR_ALGORITHM_VERSION
    auxiliary_rule_set_id: str | None = None
    auxiliary_rule_set_version: str | None = None
    auxiliary_algorithm_id: str | None = None
    auxiliary_algorithm_version: str | None = None
    role_rule_set_id: str | None = None
    role_rule_set_version: str | None = None
    role_algorithm_id: str | None = None
    role_algorithm_version: str | None = None

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
        if self.ziwei_day_boundary_policy not in {"MIDNIGHT", "ZI_START_23"}:
            raise ValueError(f"unsupported Ziwei day-boundary policy: {self.ziwei_day_boundary_policy}")
        if (
            self.ziwei_day_boundary_policy == "ZI_START_23"
            and self.time_calendar_policies.ziwei_calendar_date_policy != "LOCAL_SOLAR_DATE_INDEXED"
        ):
            raise ValueError("ZI_START_23 currently requires LOCAL_SOLAR_DATE_INDEXED")
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
        if any(value is not None for value in aux_values):
            if any(value is None for value in aux_values):
                raise ValueError("auxiliary profile binding must be fully specified or fully disabled")
            supported_rule_sets = {
                QS_CORE_AUX_RULE_SET_ID: QS_CORE_AUX_RULE_SET_VERSION,
                WENMO_DEFAULT_CORE_AUX_RULE_SET_ID: WENMO_DEFAULT_CORE_AUX_RULE_SET_VERSION,
            }
            try:
                expected_rule_set_version = supported_rule_sets[self.auxiliary_rule_set_id]
            except KeyError as exc:
                raise ValueError(f"unsupported auxiliary rule set: {self.auxiliary_rule_set_id}") from exc
            if self.auxiliary_rule_set_version != expected_rule_set_version:
                raise ValueError("unsupported auxiliary rule-set version")
            if self.auxiliary_algorithm_id != AUXILIARY_ALGORITHM_ID:
                raise ValueError("unsupported auxiliary algorithm id")
            if self.auxiliary_algorithm_version != AUXILIARY_ALGORITHM_VERSION:
                raise ValueError("unsupported auxiliary algorithm version")

        role_values = (
            self.role_rule_set_id,
            self.role_rule_set_version,
            self.role_algorithm_id,
            self.role_algorithm_version,
        )
        if any(value is not None for value in role_values):
            if any(value is None for value in role_values):
                raise ValueError("role profile binding must be fully specified or fully disabled")
            supported_role_sets = {
                QS_ROLE_RULE_SET_ID: QS_ROLE_RULE_SET_VERSION,
                WENMO_DEFAULT_ROLE_RULE_SET_ID: WENMO_DEFAULT_ROLE_RULE_SET_VERSION,
            }
            try:
                expected_role_version = supported_role_sets[self.role_rule_set_id]
            except KeyError as exc:
                raise ValueError(f"unsupported role rule set: {self.role_rule_set_id}") from exc
            if self.role_rule_set_version != expected_role_version:
                raise ValueError("unsupported role rule-set version")
            if self.role_algorithm_id != ROLE_ALGORITHM_ID:
                raise ValueError("unsupported role algorithm id")
            if self.role_algorithm_version != ROLE_ALGORITHM_VERSION:
                raise ValueError("unsupported role algorithm version")
        return self
