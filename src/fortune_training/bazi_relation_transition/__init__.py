"""Mechanical Bazi Relation Transition Foundation R1."""

from .engine import (
    BaziRelationTransitionEngine,
    BaziRelationTransitionGenerationError,
    BaziRelationTransitionRequest,
)
from .generation import (
    AFTER,
    BEFORE,
    ENTERED,
    EXITED,
    PERSISTING,
    RelationTransitionSnapshotInputs,
    build_relation_transition_context,
    build_snapshot_reference,
)
from .integrity import (
    relation_transition_fact_projection,
    relation_transition_hash_bundle,
    validate_relation_transition_context,
)
from .models import (
    BaziRelationTransitionCandidate,
    BaziRelationTransitionContext,
    BaziRelationTransitionResolution,
    FrameChangeEvidence,
    RawRelationTransitionFact,
    RelationParticipantReference,
    RelationSnapshotReference,
    TransitionHashBundle,
    TransitionIntegrityReport,
)
from .profile import (
    ResolvedBaziRelationTransitionProfile,
    bazi_relation_transition_foundation_r1_profile,
)

__all__ = [
    "AFTER",
    "BEFORE",
    "BaziRelationTransitionCandidate",
    "BaziRelationTransitionContext",
    "BaziRelationTransitionEngine",
    "BaziRelationTransitionGenerationError",
    "BaziRelationTransitionRequest",
    "BaziRelationTransitionResolution",
    "ENTERED",
    "EXITED",
    "FrameChangeEvidence",
    "PERSISTING",
    "RawRelationTransitionFact",
    "RelationParticipantReference",
    "RelationSnapshotReference",
    "RelationTransitionSnapshotInputs",
    "ResolvedBaziRelationTransitionProfile",
    "TransitionHashBundle",
    "TransitionIntegrityReport",
    "bazi_relation_transition_foundation_r1_profile",
    "build_relation_transition_context",
    "build_snapshot_reference",
    "relation_transition_fact_projection",
    "relation_transition_hash_bundle",
    "validate_relation_transition_context",
]

__version__ = "0.1.0"
