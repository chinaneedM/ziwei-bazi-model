"""Capability/performance acceptance utilities for the closed fusion chart product."""

from .harness import AcceptanceHarness, AcceptanceLocation, DEFAULT_ACCEPTANCE_LOCATIONS
from .invariants import (
    combined_invariant_violations,
    deterministic_resolution_signature,
    require_combined_invariants,
)
from .reference_diff import ReferenceDifference, compare_reference_snapshot
from .taxonomy import DefectClass, DefectRecord

__all__ = [
    "AcceptanceHarness",
    "AcceptanceLocation",
    "DEFAULT_ACCEPTANCE_LOCATIONS",
    "DefectClass",
    "DefectRecord",
    "ReferenceDifference",
    "combined_invariant_violations",
    "compare_reference_snapshot",
    "deterministic_resolution_signature",
    "require_combined_invariants",
]
