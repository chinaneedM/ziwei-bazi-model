"""Deterministic Ziwei chart foundation consuming the shared Time/Calendar layer."""

from .auxiliary import AuxiliaryContext, QSCoreAuxiliaryGenerator
from .engine import ZiweiChartFoundation, ZiweiChartRequest
from .main_stars import MainStarGenerator
from .models import NatalChartState, NatalStructureState, Sex
from .natal import NatalStructureGenerator, NatalStructureInput
from .profile import ResolvedZiweiCalculationProfile

__all__ = [
    "AuxiliaryContext",
    "MainStarGenerator",
    "NatalChartState",
    "NatalStructureGenerator",
    "NatalStructureInput",
    "NatalStructureState",
    "QSCoreAuxiliaryGenerator",
    "ResolvedZiweiCalculationProfile",
    "Sex",
    "ZiweiChartFoundation",
    "ZiweiChartRequest",
]

__version__ = "0.2.0"
