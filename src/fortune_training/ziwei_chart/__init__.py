"""Deterministic Ziwei Chart Engine V1 consuming the shared Time/Calendar layer."""

from .auxiliary import AuxiliaryContext, QSCoreAuxiliaryGenerator
from .derived_auxiliary import DerivedAuxiliaryGenerator
from .dignity import (
    DignityRegistryCell,
    DignityRegistrySummary,
    OperationalMainStarDignityGenerator,
    OperationalZiweiDignityGenerator,
)
from .dignity_r3 import OperationalFullZiweiDignityGenerator
from .dignity_r4 import OperationalZiweiDignityR4Generator
from .engine import (
    ZiweiChartCandidate,
    ZiweiChartFoundation,
    ZiweiChartRequest,
    ZiweiTypedResolution,
)
from .integrity import (
    HashBundle,
    IntegrityDiagnostic,
    IntegrityReport,
    natal_hash_bundle,
    temporal_hash_bundle,
    validate_natal_chart,
    validate_temporal_state,
)
from .main_stars import MainStarGenerator
from .minor_stars import MinorStarContext, WenmoDefaultMinorStarGenerator
from .minor_stars_r4 import WenmoDefaultMinorStarR4Generator
from .models import (
    DignityAnnotation,
    NatalChartState,
    NatalStructureState,
    RingInstance,
    RingMemberBinding,
    RoleBinding,
    Sex,
    TransformationActivation,
)
from .natal import NatalStructureGenerator, NatalStructureInput
from .profile import ResolvedZiweiCalculationProfile
from .production_profile import (
    OPERATIONAL_ZIWEI_V1_PROFILE_ID,
    OPERATIONAL_ZIWEI_V1_PROFILE_VERSION,
    PRODUCTION_ZIWEI_PROFILE_ID,
    PRODUCTION_ZIWEI_PROFILE_VERSION,
    build_operational_ziwei_v1_profile,
    build_production_ziwei_profile,
)
from .release import (
    ZIWEI_CHART_ENGINE_V1_PROFILE_ID,
    ZIWEI_CHART_ENGINE_V1_PROFILE_VERSION,
    ziwei_chart_engine_v1_profile,
)
from .rings import WenmoDefaultRingGenerator
from .roles import QSRoleGenerator, WenmoDefaultRoleGenerator
from .temporal import (
    AnnualFrame,
    DaxianFrame,
    MinorLimitFrame,
    TemporalNatalContext,
    ZiweiTemporalEngine,
    ZiweiTemporalState,
)
from .transformations import TransformationGenerator
from .view import (
    ChartViewModel,
    LexemeOverride,
    PalaceViewCell,
    PlainTextZiweiRenderer,
    PresentationProfile,
    ViewProjectionError,
    ZiweiViewProjectionCompiler,
)

__all__ = [
    "AnnualFrame",
    "AuxiliaryContext",
    "ChartViewModel",
    "DaxianFrame",
    "DerivedAuxiliaryGenerator",
    "DignityAnnotation",
    "DignityRegistryCell",
    "DignityRegistrySummary",
    "HashBundle",
    "IntegrityDiagnostic",
    "IntegrityReport",
    "LexemeOverride",
    "MainStarGenerator",
    "MinorLimitFrame",
    "MinorStarContext",
    "NatalChartState",
    "NatalStructureGenerator",
    "NatalStructureInput",
    "NatalStructureState",
    "OperationalFullZiweiDignityGenerator",
    "OperationalMainStarDignityGenerator",
    "OperationalZiweiDignityGenerator",
    "OperationalZiweiDignityR4Generator",
    "PalaceViewCell",
    "PlainTextZiweiRenderer",
    "PresentationProfile",
    "PRODUCTION_ZIWEI_PROFILE_ID",
    "PRODUCTION_ZIWEI_PROFILE_VERSION",
    "QSCoreAuxiliaryGenerator",
    "QSRoleGenerator",
    "ResolvedZiweiCalculationProfile",
    "RingInstance",
    "RingMemberBinding",
    "RoleBinding",
    "Sex",
    "TemporalNatalContext",
    "TransformationActivation",
    "TransformationGenerator",
    "ViewProjectionError",
    "WenmoDefaultMinorStarGenerator",
    "WenmoDefaultMinorStarR4Generator",
    "WenmoDefaultRingGenerator",
    "WenmoDefaultRoleGenerator",
    "ZIWEI_CHART_ENGINE_V1_PROFILE_ID",
    "ZIWEI_CHART_ENGINE_V1_PROFILE_VERSION",
    "ZiweiChartCandidate",
    "ZiweiChartFoundation",
    "ZiweiChartRequest",
    "ZiweiTemporalEngine",
    "ZiweiTemporalState",
    "ZiweiTypedResolution",
    "ZiweiViewProjectionCompiler",
    "OPERATIONAL_ZIWEI_V1_PROFILE_ID",
    "OPERATIONAL_ZIWEI_V1_PROFILE_VERSION",
    "build_operational_ziwei_v1_profile",
    "build_production_ziwei_profile",
    "natal_hash_bundle",
    "temporal_hash_bundle",
    "validate_natal_chart",
    "validate_temporal_state",
    "ziwei_chart_engine_v1_profile",
]

__version__ = "1.0.0"
