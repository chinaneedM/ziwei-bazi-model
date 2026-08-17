"""Explicit target spatial/civil coordinate foundation for Bazi flow queries."""

from .engine import TargetTemporalCoordinateEngine
from .integrity import target_coordinate_hash_bundle, validate_target_coordinate
from .models import (
    TargetTemporalCoordinate,
    TargetTemporalCoordinateResolution,
    TargetTemporalHashBundle,
    TargetTemporalInput,
    TargetTemporalIntegrityDiagnostic,
    TargetTemporalIntegrityReport,
    TargetTemporalProfile,
    TargetTemporalResolvedCandidate,
    TargetTemporalUnresolvedSample,
)
from .profile import (
    TARGET_COORDINATE_ALGORITHM_ID,
    TARGET_COORDINATE_ALGORITHM_VERSION,
    TARGET_COORDINATE_PROFILE_ID,
    TARGET_COORDINATE_PROFILE_VERSION,
    target_temporal_coordinate_r1_profile,
    validate_target_temporal_profile,
)

__all__ = [
    "TARGET_COORDINATE_ALGORITHM_ID",
    "TARGET_COORDINATE_ALGORITHM_VERSION",
    "TARGET_COORDINATE_PROFILE_ID",
    "TARGET_COORDINATE_PROFILE_VERSION",
    "TargetTemporalCoordinate",
    "TargetTemporalCoordinateEngine",
    "TargetTemporalCoordinateResolution",
    "TargetTemporalHashBundle",
    "TargetTemporalInput",
    "TargetTemporalIntegrityDiagnostic",
    "TargetTemporalIntegrityReport",
    "TargetTemporalProfile",
    "TargetTemporalResolvedCandidate",
    "TargetTemporalUnresolvedSample",
    "target_coordinate_hash_bundle",
    "target_temporal_coordinate_r1_profile",
    "validate_target_coordinate",
    "validate_target_temporal_profile",
]

__version__ = "1.0.0"
