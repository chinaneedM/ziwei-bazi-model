"""Deterministic target civil/UTC/local-apparent-solar coordinate foundation."""

from .engine import TargetTemporalCoordinateFoundation
from .integrity import (
    target_hash_bundle,
    validate_target_temporal_resolution,
)
from .models import (
    TargetTemporalCoordinateCandidate,
    TargetTemporalCoordinateResolution,
    TargetTemporalHashBundle,
    TargetTemporalInput,
    TargetTemporalIntegrityDiagnostic,
    TargetTemporalIntegrityReport,
    TargetTemporalUnresolvedSample,
)
from .profile import (
    ResolvedTargetTemporalCoordinateProfile,
    bazi_target_temporal_coordinate_r1_profile,
)

__all__ = [
    "ResolvedTargetTemporalCoordinateProfile",
    "TargetTemporalCoordinateCandidate",
    "TargetTemporalCoordinateFoundation",
    "TargetTemporalCoordinateResolution",
    "TargetTemporalHashBundle",
    "TargetTemporalInput",
    "TargetTemporalIntegrityDiagnostic",
    "TargetTemporalIntegrityReport",
    "TargetTemporalUnresolvedSample",
    "bazi_target_temporal_coordinate_r1_profile",
    "target_hash_bundle",
    "validate_target_temporal_resolution",
]
