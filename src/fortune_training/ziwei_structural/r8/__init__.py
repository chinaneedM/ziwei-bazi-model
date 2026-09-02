"""Ziwei Structural Runtime V2-R8 bilateral adjacent-palace geometry."""

from .engine import AdjacentPalaceGenerationError, ZiweiAdjacentPalaceRuntime
from .integrity import (
    ADJACENT_PALACE_INTEGRITY_ALGORITHM_ID,
    ADJACENT_PALACE_INTEGRITY_ALGORITHM_VERSION,
    adjacent_palace_fact_projection,
    adjacent_palace_hash_bundle,
    validate_adjacent_palace_components,
    validate_adjacent_palace_state,
)
from .models import (
    ADJACENT_PALACE_PAIR_STATE_SCHEMA,
    AdjacentPalaceHashBundle,
    AdjacentPalaceIntegrityDiagnostic,
    AdjacentPalaceIntegrityReport,
    AdjacentPalacePairFact,
    AdjacentPalacePairState,
)
from .profile import (
    ADJACENT_PALACE_PAIR_ALGORITHM_ID,
    ADJACENT_PALACE_PAIR_ALGORITHM_VERSION,
    ADJACENT_PALACE_SEMANTIC_SCOPE,
    ADJACENT_PALACE_SOURCE_FAMILY_ID,
    ADJACENT_PALACE_SOURCE_ID,
    ADJACENT_PALACE_SOURCE_PARAGRAPH_ID,
    ADJACENT_PALACE_SOURCE_RELATION_ID,
    ADJACENT_PALACE_SOURCE_RUNTIME_BLOB_SHA,
    ADJACENT_PALACE_SOURCE_RUNTIME_PATH,
    ADJACENT_PALACE_SOURCE_SECTION,
    ADJACENT_PALACE_SOURCE_SEGMENT_IDS,
    ADJACENT_PALACE_SOURCE_TERM_ID,
    CLOCKWISE_NEIGHBOR_CLOCKWISE_OFFSET,
    CLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL,
    COUNTERCLOCKWISE_NEIGHBOR_CLOCKWISE_OFFSET,
    COUNTERCLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL,
    ResolvedAdjacentPalacePairProfile,
    ZIWEI_STRUCTURAL_V2_R8_PROFILE_ID,
    ZIWEI_STRUCTURAL_V2_R8_PROFILE_VERSION,
    ziwei_structural_v2_r8_profile,
)
from .projection import AdjacentPalaceProjectionError, project_adjacent_palace_pairs


__all__ = [
    "ADJACENT_PALACE_INTEGRITY_ALGORITHM_ID",
    "ADJACENT_PALACE_INTEGRITY_ALGORITHM_VERSION",
    "ADJACENT_PALACE_PAIR_ALGORITHM_ID",
    "ADJACENT_PALACE_PAIR_ALGORITHM_VERSION",
    "ADJACENT_PALACE_PAIR_STATE_SCHEMA",
    "ADJACENT_PALACE_SEMANTIC_SCOPE",
    "ADJACENT_PALACE_SOURCE_FAMILY_ID",
    "ADJACENT_PALACE_SOURCE_ID",
    "ADJACENT_PALACE_SOURCE_PARAGRAPH_ID",
    "ADJACENT_PALACE_SOURCE_RELATION_ID",
    "ADJACENT_PALACE_SOURCE_RUNTIME_BLOB_SHA",
    "ADJACENT_PALACE_SOURCE_RUNTIME_PATH",
    "ADJACENT_PALACE_SOURCE_SECTION",
    "ADJACENT_PALACE_SOURCE_SEGMENT_IDS",
    "ADJACENT_PALACE_SOURCE_TERM_ID",
    "AdjacentPalaceGenerationError",
    "AdjacentPalaceHashBundle",
    "AdjacentPalaceIntegrityDiagnostic",
    "AdjacentPalaceIntegrityReport",
    "AdjacentPalacePairFact",
    "AdjacentPalacePairState",
    "AdjacentPalaceProjectionError",
    "CLOCKWISE_NEIGHBOR_CLOCKWISE_OFFSET",
    "CLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL",
    "COUNTERCLOCKWISE_NEIGHBOR_CLOCKWISE_OFFSET",
    "COUNTERCLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL",
    "ResolvedAdjacentPalacePairProfile",
    "ZIWEI_STRUCTURAL_V2_R8_PROFILE_ID",
    "ZIWEI_STRUCTURAL_V2_R8_PROFILE_VERSION",
    "ZiweiAdjacentPalaceRuntime",
    "adjacent_palace_fact_projection",
    "adjacent_palace_hash_bundle",
    "project_adjacent_palace_pairs",
    "validate_adjacent_palace_components",
    "validate_adjacent_palace_state",
    "ziwei_structural_v2_r8_profile",
]

__version__ = "2.0.0-r8"
