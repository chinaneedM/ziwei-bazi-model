from __future__ import annotations

from .profile import bazi_foundation_v1_profile


# The production selector preserves the calculation-profile identity already
# bound into released Bazi V1 computation hashes.  It must not mint a second
# default profile merely to give product callers a descriptive entry point.
PRODUCTION_BAZI_PROFILE_ID = "BAZI-FOUNDATION-V1-R1"
PRODUCTION_BAZI_PROFILE_VERSION = "1.1.0"

build_production_bazi_profile = bazi_foundation_v1_profile


__all__ = [
    "PRODUCTION_BAZI_PROFILE_ID",
    "PRODUCTION_BAZI_PROFILE_VERSION",
    "build_production_bazi_profile",
]
