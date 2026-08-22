"""Typed, auditable Bazi chart foundation."""

from .engine import BaziChartCandidate, BaziChartFoundation, BaziChartRequest, BaziTypedResolution
from .integrity import natal_fact_projection, natal_hash_bundle, validate_natal_state
from .models import (
    BaziNatalState,
    BaziTemporalSeed,
    BranchInstance,
    HashBundle,
    HiddenStemExposureLink,
    HiddenStemMembership,
    IntegrityReport,
    PillarState,
    RelationCandidate,
    StemBranchAffinityFact,
    StemInstance,
    TenGodBinding,
)
from .profile import (
    ResolvedBaziCalculationProfile,
    ZI_START_23_PROFILE_ID,
    ZI_START_23_PROFILE_VERSION,
    bazi_foundation_v1_profile,
    bazi_foundation_zi_start_23_r1_profile,
)
from .production_profile import (
    PRODUCTION_BAZI_PROFILE_ID,
    PRODUCTION_BAZI_PROFILE_VERSION,
    build_production_bazi_profile,
)
from .registries import SEXAGENARY_CYCLE, sexagenary_index

__all__ = [
    "BaziChartCandidate",
    "BaziChartFoundation",
    "BaziChartRequest",
    "BaziNatalState",
    "BaziTemporalSeed",
    "BaziTypedResolution",
    "BranchInstance",
    "HashBundle",
    "HiddenStemExposureLink",
    "HiddenStemMembership",
    "IntegrityReport",
    "PillarState",
    "PRODUCTION_BAZI_PROFILE_ID",
    "PRODUCTION_BAZI_PROFILE_VERSION",
    "RelationCandidate",
    "ResolvedBaziCalculationProfile",
    "SEXAGENARY_CYCLE",
    "StemBranchAffinityFact",
    "StemInstance",
    "TenGodBinding",
    "ZI_START_23_PROFILE_ID",
    "ZI_START_23_PROFILE_VERSION",
    "bazi_foundation_v1_profile",
    "bazi_foundation_zi_start_23_r1_profile",
    "build_production_bazi_profile",
    "natal_fact_projection",
    "natal_hash_bundle",
    "sexagenary_index",
    "validate_natal_state",
]

__version__ = "0.1.0"
