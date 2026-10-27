"""Neutral active Bazi Structural Context R1."""

from .engine import (
    BaziStructuralEngine,
    BaziStructuralGenerationError,
    BaziStructuralRequest,
)
from .generation import build_structural_context, materialize_temporal_participants
from .integrity import (
    structural_fact_projection,
    structural_hash_bundle,
    validate_structural_context,
)
from .models import (
    BaziStructuralCandidate,
    BaziStructuralContext,
    BaziStructuralResolution,
    DynamicRelationOccurrence,
    StructuralHashBundle,
    StructuralIntegrityReport,
    TemporalParticipantProvenance,
)
from .profile import (
    ResolvedBaziStructuralProfile,
    bazi_structural_context_r1_profile,
)

__all__ = [
    "BaziStructuralCandidate",
    "BaziStructuralContext",
    "BaziStructuralEngine",
    "BaziStructuralGenerationError",
    "BaziStructuralRequest",
    "BaziStructuralResolution",
    "DynamicRelationOccurrence",
    "ResolvedBaziStructuralProfile",
    "StructuralHashBundle",
    "StructuralIntegrityReport",
    "TemporalParticipantProvenance",
    "bazi_structural_context_r1_profile",
    "build_structural_context",
    "materialize_temporal_participants",
    "structural_fact_projection",
    "structural_hash_bundle",
    "validate_structural_context",
]

__version__ = "0.1.0"
