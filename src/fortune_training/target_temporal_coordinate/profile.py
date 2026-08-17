from __future__ import annotations

from fortune_training.calendar_foundation import CivilTimeResolver, SolarTimeEngine

from .models import TargetTemporalProfile


TARGET_COORDINATE_ALGORITHM_ID = "TARGET-TEMPORAL-COORDINATE-ENGINE-R1"
TARGET_COORDINATE_ALGORITHM_VERSION = "1.0.0"
TARGET_COORDINATE_PROFILE_ID = "TARGET-TEMPORAL-COORDINATE-R1"
TARGET_COORDINATE_PROFILE_VERSION = "1.0.0"


def target_temporal_coordinate_r1_profile() -> TargetTemporalProfile:
    return TargetTemporalProfile(
        profile_id=TARGET_COORDINATE_PROFILE_ID,
        profile_version=TARGET_COORDINATE_PROFILE_VERSION,
        civil_ambiguous_time_policy="REJECT",
        coordinate_algorithm_id=TARGET_COORDINATE_ALGORITHM_ID,
        coordinate_algorithm_version=TARGET_COORDINATE_ALGORITHM_VERSION,
        civil_algorithm_id=CivilTimeResolver.algorithm_id,
        solar_algorithm_id=SolarTimeEngine.algorithm_id,
    )


def validate_target_temporal_profile(profile: TargetTemporalProfile) -> TargetTemporalProfile:
    expected = target_temporal_coordinate_r1_profile()
    if profile != expected:
        raise ValueError(f"unsupported target temporal profile: {profile!r}")
    return profile
