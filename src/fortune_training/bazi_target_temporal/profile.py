from __future__ import annotations

from dataclasses import dataclass

from fortune_training.calendar_foundation.timezone import AMBIGUOUS_TIME_POLICIES, CivilTimeResolver
from fortune_training.calendar_foundation.solar import SolarTimeEngine


TARGET_TEMPORAL_PROFILE_ID = "BAZI-TARGET-TEMPORAL-COORDINATE-FOUNDATION-R1"
TARGET_TEMPORAL_PROFILE_VERSION = "1.0.0"
TARGET_TEMPORAL_ALGORITHM_ID = "BAZI-TARGET-TEMPORAL-COORDINATE-RESOLVER-R1"
TARGET_TEMPORAL_ALGORITHM_VERSION = "1.0.0"
SAMPLING_LINEAGE_ID = "TIME-CALENDAR-FOUNDATION-V1._sample_wall_times"


@dataclass(frozen=True)
class ResolvedTargetTemporalCoordinateProfile:
    profile_id: str = TARGET_TEMPORAL_PROFILE_ID
    profile_version: str = TARGET_TEMPORAL_PROFILE_VERSION
    ambiguous_time_policy: str = "REJECT"
    target_temporal_algorithm_id: str = TARGET_TEMPORAL_ALGORITHM_ID
    target_temporal_algorithm_version: str = TARGET_TEMPORAL_ALGORITHM_VERSION
    civil_time_algorithm_id: str = CivilTimeResolver.algorithm_id
    solar_time_algorithm_id: str = SolarTimeEngine.algorithm_id
    sampling_lineage_id: str = SAMPLING_LINEAGE_ID

    def validate(self) -> "ResolvedTargetTemporalCoordinateProfile":
        if self.profile_id != TARGET_TEMPORAL_PROFILE_ID:
            raise ValueError(f"unsupported target temporal profile: {self.profile_id}")
        if self.profile_version != TARGET_TEMPORAL_PROFILE_VERSION:
            raise ValueError(f"unsupported target temporal profile version: {self.profile_version}")
        if self.ambiguous_time_policy not in AMBIGUOUS_TIME_POLICIES:
            raise ValueError(f"unsupported ambiguous time policy: {self.ambiguous_time_policy}")
        if self.target_temporal_algorithm_id != TARGET_TEMPORAL_ALGORITHM_ID:
            raise ValueError("unsupported target temporal algorithm id")
        if self.target_temporal_algorithm_version != TARGET_TEMPORAL_ALGORITHM_VERSION:
            raise ValueError("unsupported target temporal algorithm version")
        if self.civil_time_algorithm_id != CivilTimeResolver.algorithm_id:
            raise ValueError("unsupported civil time algorithm id")
        if self.solar_time_algorithm_id != SolarTimeEngine.algorithm_id:
            raise ValueError("unsupported solar time algorithm id")
        if self.sampling_lineage_id != SAMPLING_LINEAGE_ID:
            raise ValueError("unsupported sampling lineage id")
        return self


def bazi_target_temporal_coordinate_r1_profile() -> ResolvedTargetTemporalCoordinateProfile:
    return ResolvedTargetTemporalCoordinateProfile()
