from __future__ import annotations

from .production_profile import (
    PRODUCTION_ZIWEI_PROFILE_ID,
    PRODUCTION_ZIWEI_PROFILE_VERSION,
    build_production_ziwei_profile,
)


# Frozen V1 names remain public compatibility aliases. The implementation lives
# only in production_profile so release and product callers cannot drift apart.
ZIWEI_CHART_ENGINE_V1_PROFILE_ID = PRODUCTION_ZIWEI_PROFILE_ID
ZIWEI_CHART_ENGINE_V1_PROFILE_VERSION = PRODUCTION_ZIWEI_PROFILE_VERSION
ziwei_chart_engine_v1_profile = build_production_ziwei_profile
