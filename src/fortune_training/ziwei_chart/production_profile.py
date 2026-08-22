from __future__ import annotations

from fortune_training.calendar_foundation.policies import PolicyRegistry

from .auxiliary import (
    AUXILIARY_ALGORITHM_ID,
    AUXILIARY_ALGORITHM_VERSION,
    WENMO_DEFAULT_CORE_AUX_RULE_SET_ID,
    WENMO_DEFAULT_CORE_AUX_RULE_SET_VERSION,
)
from .dignity import DIGNITY_ALGORITHM_ID, DIGNITY_ALGORITHM_VERSION
from .dignity_r4 import (
    OPERATIONAL_R4_DIGNITY_RULE_SET_ID,
    OPERATIONAL_R4_DIGNITY_RULE_SET_VERSION,
)
from .main_stars import MAIN_STAR_ALGORITHM_ID, MAIN_STAR_ALGORITHM_VERSION
from .minor_stars import MINOR_STAR_ALGORITHM_ID
from .minor_stars_r4 import WENMO_DEFAULT_MINOR_R4_RULE_SET_VERSION
from .profile import ResolvedZiweiCalculationProfile
from .rings import (
    RING_ALGORITHM_ID,
    RING_ALGORITHM_VERSION,
    WENMO_DEFAULT_RING_RULE_SET_ID,
    WENMO_DEFAULT_RING_RULE_SET_VERSION,
)
from .roles import (
    QS_ROLE_RULE_SET_ID,
    QS_ROLE_RULE_SET_VERSION,
    ROLE_ALGORITHM_ID,
    ROLE_ALGORITHM_VERSION,
)
from .temporal import (
    S10_CURRENT_TEMPORAL_RULE_SET_ID,
    S10_CURRENT_TEMPORAL_RULE_SET_VERSION,
    TEMPORAL_ALGORITHM_ID,
    TEMPORAL_ALGORITHM_VERSION,
)
from .transformations import (
    S08_TRANSFORMATION_RULE_SET_ID,
    S08_TRANSFORMATION_RULE_SET_VERSION,
    TRANSFORMATION_ALGORITHM_ID,
    TRANSFORMATION_ALGORITHM_VERSION,
)
from .minor_stars import WENMO_DEFAULT_MINOR_RULE_SET_ID


OPERATIONAL_ZIWEI_V1_PROFILE_ID = "OPERATIONAL_ZIWEI_V1_R1"
OPERATIONAL_ZIWEI_V1_PROFILE_VERSION = "1.0.0"


def build_operational_ziwei_v1_profile(
    policy_registry: PolicyRegistry,
) -> ResolvedZiweiCalculationProfile:
    """Build the default production Ziwei V1 immutable profile."""
    profile = ResolvedZiweiCalculationProfile(
        profile_id=OPERATIONAL_ZIWEI_V1_PROFILE_ID,
        profile_version=OPERATIONAL_ZIWEI_V1_PROFILE_VERSION,
        time_calendar_policy_registry_version=policy_registry.version,
        time_calendar_policies=policy_registry.default_selection(),
        main_star_algorithm_id=MAIN_STAR_ALGORITHM_ID,
        main_star_algorithm_version=MAIN_STAR_ALGORITHM_VERSION,
        auxiliary_rule_set_id=WENMO_DEFAULT_CORE_AUX_RULE_SET_ID,
        auxiliary_rule_set_version=WENMO_DEFAULT_CORE_AUX_RULE_SET_VERSION,
        auxiliary_algorithm_id=AUXILIARY_ALGORITHM_ID,
        auxiliary_algorithm_version=AUXILIARY_ALGORITHM_VERSION,
        minor_rule_set_id=WENMO_DEFAULT_MINOR_RULE_SET_ID,
        minor_rule_set_version=WENMO_DEFAULT_MINOR_R4_RULE_SET_VERSION,
        minor_algorithm_id=MINOR_STAR_ALGORITHM_ID,
        minor_algorithm_version=MINOR_STAR_ALGORITHM_VERSION,
        dignity_rule_set_id=OPERATIONAL_R4_DIGNITY_RULE_SET_ID,
        dignity_rule_set_version=OPERATIONAL_R4_DIGNITY_RULE_SET_VERSION,
        dignity_algorithm_id=DIGNITY_ALGORITHM_ID,
        dignity_algorithm_version=DIGNITY_ALGORITHM_VERSION,
        transformation_rule_set_id=S08_TRANSFORMATION_RULE_SET_ID,
        transformation_rule_set_version=S08_TRANSFORMATION_RULE_SET_VERSION,
        transformation_algorithm_id=TRANSFORMATION_ALGORITHM_ID,
        transformation_algorithm_version=TRANSFORMATION_ALGORITHM_VERSION,
        temporal_rule_set_id=S10_CURRENT_TEMPORAL_RULE_SET_ID,
        temporal_rule_set_version=S10_CURRENT_TEMPORAL_RULE_SET_VERSION,
        temporal_algorithm_id=TEMPORAL_ALGORITHM_ID,
        temporal_algorithm_version=TEMPORAL_ALGORITHM_VERSION,
        ring_rule_set_id=WENMO_DEFAULT_RING_RULE_SET_ID,
        ring_rule_set_version=WENMO_DEFAULT_RING_RULE_SET_VERSION,
        ring_algorithm_id=RING_ALGORITHM_ID,
        ring_algorithm_version=RING_ALGORITHM_VERSION,
        role_rule_set_id=QS_ROLE_RULE_SET_ID,
        role_rule_set_version=QS_ROLE_RULE_SET_VERSION,
        role_algorithm_id=ROLE_ALGORITHM_ID,
        role_algorithm_version=ROLE_ALGORITHM_VERSION,
    )
    return profile.validate(policy_registry)
