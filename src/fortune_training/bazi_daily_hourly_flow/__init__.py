"""Deterministic Bazi Daily/Hourly target-coordinate sidecar."""

from .engine import BaziDailyHourlyFlowEngine, BaziDailyHourlyFlowGenerationError
from .integrity import (
    daily_hourly_fact_projection,
    daily_hourly_hash_bundle,
    validate_daily_hourly_context,
)
from .models import (
    BaziDailyHourlyFlowCandidate,
    BaziDailyHourlyFlowContext,
    BaziDailyHourlyFlowRequest,
    BaziDailyHourlyFlowResolution,
    DailyFrame,
    DailyHourlyHashBundle,
    DailyHourlyIntegrityDiagnostic,
    DailyHourlyIntegrityReport,
    HourlyFrame,
)

__all__ = [
    "BaziDailyHourlyFlowCandidate",
    "BaziDailyHourlyFlowContext",
    "BaziDailyHourlyFlowEngine",
    "BaziDailyHourlyFlowGenerationError",
    "BaziDailyHourlyFlowRequest",
    "BaziDailyHourlyFlowResolution",
    "DailyFrame",
    "DailyHourlyHashBundle",
    "DailyHourlyIntegrityDiagnostic",
    "DailyHourlyIntegrityReport",
    "HourlyFrame",
    "daily_hourly_fact_projection",
    "daily_hourly_hash_bundle",
    "validate_daily_hourly_context",
]

__version__ = "0.1.0"
