"""Deterministic Ziwei chart foundation consuming the shared Time/Calendar layer."""

from .auxiliary import AuxiliaryContext, QSCoreAuxiliaryGenerator
from .derived_auxiliary import DerivedAuxiliaryGenerator
from .engine import ZiweiChartFoundation, ZiweiChartRequest
from .main_stars import MainStarGenerator
from .minor_stars import MinorStarContext, WenmoDefaultMinorStarGenerator
from .models import (
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
from .transformations import TransformationGenerator

__all__ = [
    "AuxiliaryContext",
    "DerivedAuxiliaryGenerator",
    "MainStarGenerator",
    "MinorStarContext",
    "NatalChartState",
    "NatalStructureGenerator",
    "NatalStructureInput",
    "NatalStructureState",
    "QSCoreAuxiliaryGenerator",
    "QSRoleGenerator",
    "ResolvedZiweiCalculationProfile",
    "RingInstance",
    "RingMemberBinding",
    "RoleBinding",
    "Sex",
    "TransformationActivation",
    "TransformationGenerator",
    "WenmoDefaultMinorStarGenerator",
    "WenmoDefaultRingGenerator",
    "WenmoDefaultRoleGenerator",
    "ZiweiChartFoundation",
    "ZiweiChartRequest",
]

__version__ = "0.6.0"
