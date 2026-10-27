"""Deterministic target-time Annual/Monthly and active-Dayun context."""

from .engine import BaziFlowEngine, BaziFlowGenerationError, BaziFlowRequest
from .integrity import flow_fact_projection, flow_hash_bundle, validate_flow_context
from .models import (
    AnnualFrame,
    BaziFlowCandidate,
    BaziFlowContext,
    BaziFlowResolution,
    FlowHashBundle,
    FlowIntegrityReport,
    MonthlyFrame,
)

__all__ = [
    "AnnualFrame",
    "BaziFlowCandidate",
    "BaziFlowContext",
    "BaziFlowEngine",
    "BaziFlowGenerationError",
    "BaziFlowRequest",
    "BaziFlowResolution",
    "FlowHashBundle",
    "FlowIntegrityReport",
    "MonthlyFrame",
    "flow_fact_projection",
    "flow_hash_bundle",
    "validate_flow_context",
]

__version__ = "0.1.0"
