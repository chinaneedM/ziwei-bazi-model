"""Deterministic Ziwei chart foundation consuming the shared Time/Calendar layer."""

from .auxiliary import AuxiliaryContext, QSCoreAuxiliaryGenerator
from .derived_auxiliary import DerivedAuxiliaryGenerator
from .dignity import (
    DignityRegistrySummary,
    OperationalMainStarDignityGenerator,
)
from .engine import ZiweiChartFoundation, ZiweiChartRequest
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
    "OperationalMainStarDignityGenerator",
    "PalaceViewCell",
    "PlainTextZiweiRenderer",
    "PresentationProfile",
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
    "WenmoDefaultRingGenerator",
    "WenmoDefaultRoleGenerator",
    "ZiweiChartFoundation",
    "ZiweiChartRequest",
    "ZiweiTemporalEngine",
    "ZiweiTemporalState",
    "ZiweiViewProjectionCompiler",
    "natal_hash_bundle",
    "temporal_hash_bundle",
    "validate_natal_chart",
    "validate_temporal_state",
]

__version__ = "0.10.0"
