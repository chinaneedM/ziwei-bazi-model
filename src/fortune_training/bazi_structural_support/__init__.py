"""Non-interpretive Bazi Structural Support Foundation R1."""

from .engine import (
    BaziStructuralSupportEngine,
    BaziStructuralSupportGenerationError,
    BaziStructuralSupportRequest,
)
from .generation import (
    ACTIVE_FLOW_SOLAR_MONTH,
    EXACT_HIDDEN_STEM_MATCH,
    NATAL_MONTH_COMMAND,
    SAME_ELEMENT_HIDDEN_SUPPORT,
    build_structural_support_context,
)
from .integrity import (
    structural_support_fact_projection,
    structural_support_hash_bundle,
    validate_structural_support_context,
)
from .models import (
    ActiveFlowSolarMonthReference,
    BaziStructuralSupportCandidate,
    BaziStructuralSupportContext,
    BaziStructuralSupportResolution,
    NatalMonthCommandReference,
    SupportEvidenceCandidate,
    SupportHashBundle,
    SupportIntegrityReport,
)
from .profile import (
    ResolvedBaziStructuralSupportProfile,
    bazi_structural_support_foundation_r1_profile,
)

__all__ = [
    "ACTIVE_FLOW_SOLAR_MONTH",
    "ActiveFlowSolarMonthReference",
    "BaziStructuralSupportCandidate",
    "BaziStructuralSupportContext",
    "BaziStructuralSupportEngine",
    "BaziStructuralSupportGenerationError",
    "BaziStructuralSupportRequest",
    "BaziStructuralSupportResolution",
    "EXACT_HIDDEN_STEM_MATCH",
    "NATAL_MONTH_COMMAND",
    "NatalMonthCommandReference",
    "ResolvedBaziStructuralSupportProfile",
    "SAME_ELEMENT_HIDDEN_SUPPORT",
    "SupportEvidenceCandidate",
    "SupportHashBundle",
    "SupportIntegrityReport",
    "bazi_structural_support_foundation_r1_profile",
    "build_structural_support_context",
    "structural_support_fact_projection",
    "structural_support_hash_bundle",
    "validate_structural_support_context",
]

__version__ = "0.1.0"
