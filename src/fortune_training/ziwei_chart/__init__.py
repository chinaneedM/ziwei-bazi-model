"""Deterministic Ziwei chart foundation consuming the shared Time/Calendar layer."""

from .auxiliary import AuxiliaryContext, QSCoreAuxiliaryGenerator
from .derived_auxiliary import DerivedAuxiliaryGenerator
from .engine import ZiweiChartFoundation, ZiweiChartRequest
from .main_stars import MainStarGenerator
from .models import NatalChartState, NatalStructureState, RoleBinding, Sex
from .natal import NatalStructureGenerator, NatalStructureInput
from .profile import ResolvedZiweiCalculationProfile
from .roles import QSRoleGenerator, WenmoDefaultRoleGenerator

__all__ = [
    "AuxiliaryContext",
    "DerivedAuxiliaryGenerator",
    "MainStarGenerator",
    "NatalChartState",
    "NatalStructureGenerator",
    "NatalStructureInput",
    "NatalStructureState",
    "QSCoreAuxiliaryGenerator",
    "QSRoleGenerator",
    "ResolvedZiweiCalculationProfile",
    "RoleBinding",
    "Sex",
    "WenmoDefaultRoleGenerator",
    "ZiweiChartFoundation",
    "ZiweiChartRequest",
]

__version__ = "0.3.0"
