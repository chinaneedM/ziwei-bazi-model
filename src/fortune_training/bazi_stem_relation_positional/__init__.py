"""Bazi Stem Relation Positional Context Foundation R1."""

from .engine import (
    BaziStemRelationPositionalEngine,
    BaziStemRelationPositionalGenerationError,
    BaziStemRelationPositionalRequest,
)
from .generation import (
    NATAL_PILLAR,
    NATAL_PILLAR_ORDINALS,
    TEMPORAL_FRAME,
    build_stem_relation_positional_context,
)
from .integrity import (
    stem_relation_positional_fact_projection,
    stem_relation_positional_hash_bundle,
    validate_stem_relation_positional_context,
)
from .models import (
    BaziStemRelationPositionalCandidate,
    BaziStemRelationPositionalContext,
    BaziStemRelationPositionalResolution,
    PositionalHashBundle,
    PositionalIntegrityReport,
    StemPairPositionalFact,
    StemParticipantPositionReference,
    StemRelationPositionalSnapshot,
)
from .profile import (
    ResolvedBaziStemRelationPositionalProfile,
    bazi_stem_relation_positional_context_foundation_r1_profile,
)

__all__ = [
    "BaziStemRelationPositionalCandidate",
    "BaziStemRelationPositionalContext",
    "BaziStemRelationPositionalEngine",
    "BaziStemRelationPositionalGenerationError",
    "BaziStemRelationPositionalRequest",
    "BaziStemRelationPositionalResolution",
    "NATAL_PILLAR",
    "NATAL_PILLAR_ORDINALS",
    "PositionalHashBundle",
    "PositionalIntegrityReport",
    "ResolvedBaziStemRelationPositionalProfile",
    "StemPairPositionalFact",
    "StemParticipantPositionReference",
    "StemRelationPositionalSnapshot",
    "TEMPORAL_FRAME",
    "bazi_stem_relation_positional_context_foundation_r1_profile",
    "build_stem_relation_positional_context",
    "stem_relation_positional_fact_projection",
    "stem_relation_positional_hash_bundle",
    "validate_stem_relation_positional_context",
]

__version__ = "0.1.0"
