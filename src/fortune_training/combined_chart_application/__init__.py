"""Thin local composition shell for independent Ziwei and Bazi application bundles."""

from .models import (
    CombinedApplicationIntegrityReport,
    CombinedChartApplicationRequest,
    CombinedChartApplicationResolution,
    CombinedSubsystemError,
)
from .profile import (
    COMBINED_MANIFEST_SCHEMA,
    COMBINED_PROFILE_ID,
    COMBINED_PROFILE_VERSION,
    CombinedChartApplicationProfile,
    combined_chart_application_v1_profile,
)
from .service import (
    COMBINED_EXPORT_SCHEMA,
    COMBINED_RESOLUTION_SCHEMA,
    CombinedApplicationResolutionError,
    CombinedChartService,
    combined_manifest_hash,
    combined_manifest_payload,
    validate_combined_resolution,
)

__all__ = [
    "COMBINED_EXPORT_SCHEMA",
    "COMBINED_MANIFEST_SCHEMA",
    "COMBINED_PROFILE_ID",
    "COMBINED_PROFILE_VERSION",
    "COMBINED_RESOLUTION_SCHEMA",
    "CombinedApplicationIntegrityReport",
    "CombinedApplicationResolutionError",
    "CombinedChartApplicationProfile",
    "CombinedChartApplicationRequest",
    "CombinedChartApplicationResolution",
    "CombinedChartService",
    "CombinedSubsystemError",
    "combined_chart_application_v1_profile",
    "combined_manifest_hash",
    "combined_manifest_payload",
    "validate_combined_resolution",
]

__version__ = "0.1.0"
