"""Typed Bazi Dayun temporal runtime."""

from .engine import BaziTemporalEngine, BaziTemporalGenerationError, BaziTemporalRequest
from .integrity import temporal_fact_projection, temporal_hash_bundle, validate_dayun_state
from .models import (
    BaziDayunState,
    BaziSex,
    BaziTemporalCandidate,
    BaziTemporalResolution,
    DayunDirectionResolution,
    DayunFrame,
    JiaoyunResolution,
    PreDayunFrame,
    SymbolicLuckAge,
    TemporalHashBundle,
    TemporalIntegrityReport,
)
from .profile import ResolvedBaziTemporalProfile, bazi_temporal_v1_continuous_profile

__all__ = [
    "BaziDayunState",
    "BaziSex",
    "BaziTemporalCandidate",
    "BaziTemporalEngine",
    "BaziTemporalGenerationError",
    "BaziTemporalRequest",
    "BaziTemporalResolution",
    "DayunDirectionResolution",
    "DayunFrame",
    "JiaoyunResolution",
    "PreDayunFrame",
    "ResolvedBaziTemporalProfile",
    "SymbolicLuckAge",
    "TemporalHashBundle",
    "TemporalIntegrityReport",
    "bazi_temporal_v1_continuous_profile",
    "temporal_fact_projection",
    "temporal_hash_bundle",
    "validate_dayun_state",
]

__version__ = "0.1.0"
