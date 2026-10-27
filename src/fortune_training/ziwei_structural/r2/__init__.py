"""Ziwei Structural Runtime V2-R2 relative-palace frame core."""

from .engine import RelativeFrameGenerationError, ZiweiRelativePalaceFrameRuntime
from .frame import (
    RelativePalaceFrameError,
    RelativePalaceFrameGenerator,
    canonical_designation_ids,
)
from .integrity import (
    RELATIVE_FRAME_INTEGRITY_ALGORITHM_ID,
    RELATIVE_FRAME_INTEGRITY_ALGORITHM_VERSION,
    relative_frame_fact_projection,
    relative_frame_hash_bundle,
    validate_relative_frame_components,
    validate_relative_frame_state,
)
from .models import (
    RELATIVE_PALACE_FRAME_STATE_SCHEMA,
    RelativeFrameHashBundle,
    RelativeFrameIntegrityDiagnostic,
    RelativeFrameIntegrityReport,
    RelativePalaceFrameState,
    RelativePalaceRoleFact,
)
from .profile import (
    RELATIVE_PALACE_FRAME_ALGORITHM_ID,
    RELATIVE_PALACE_FRAME_ALGORITHM_VERSION,
    ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID,
    ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION,
    ResolvedRelativePalaceFrameProfile,
    ziwei_structural_v2_r2_profile,
)


__all__ = [
    "RELATIVE_FRAME_INTEGRITY_ALGORITHM_ID",
    "RELATIVE_FRAME_INTEGRITY_ALGORITHM_VERSION",
    "RELATIVE_PALACE_FRAME_ALGORITHM_ID",
    "RELATIVE_PALACE_FRAME_ALGORITHM_VERSION",
    "RELATIVE_PALACE_FRAME_STATE_SCHEMA",
    "RelativeFrameGenerationError",
    "RelativeFrameHashBundle",
    "RelativeFrameIntegrityDiagnostic",
    "RelativeFrameIntegrityReport",
    "RelativePalaceFrameError",
    "RelativePalaceFrameGenerator",
    "RelativePalaceFrameState",
    "RelativePalaceRoleFact",
    "ResolvedRelativePalaceFrameProfile",
    "ZIWEI_STRUCTURAL_V2_R2_PROFILE_ID",
    "ZIWEI_STRUCTURAL_V2_R2_PROFILE_VERSION",
    "ZiweiRelativePalaceFrameRuntime",
    "canonical_designation_ids",
    "relative_frame_fact_projection",
    "relative_frame_hash_bundle",
    "validate_relative_frame_components",
    "validate_relative_frame_state",
    "ziwei_structural_v2_r2_profile",
]

__version__ = "2.0.0-r2"
