"""Single-snapshot Bazi Relation Incidence Foundation R1."""

from .engine import (
    BaziRelationIncidenceEngine,
    BaziRelationIncidenceGenerationError,
    BaziRelationIncidenceRequest,
)
from .generation import (
    DISJOINT,
    SHARED_PARTICIPANT,
    RelationIncidenceSnapshotInputs,
    build_incidence_snapshot,
    build_relation_incidence_context,
)
from .integrity import (
    relation_incidence_fact_projection,
    relation_incidence_hash_bundle,
    validate_relation_incidence_context,
)
from .models import (
    BaziRelationIncidenceCandidate,
    BaziRelationIncidenceContext,
    BaziRelationIncidenceResolution,
    IncidenceHashBundle,
    IncidenceIntegrityReport,
    IncidenceParticipantReference,
    ParticipantRelationIncidenceFact,
    RelationIncidenceSnapshot,
    RelationOccurrenceReference,
    RelationPairTopologyFact,
)
from .profile import (
    ResolvedBaziRelationIncidenceProfile,
    bazi_relation_incidence_foundation_r1_profile,
)

__all__ = [
    "BaziRelationIncidenceCandidate",
    "BaziRelationIncidenceContext",
    "BaziRelationIncidenceEngine",
    "BaziRelationIncidenceGenerationError",
    "BaziRelationIncidenceRequest",
    "BaziRelationIncidenceResolution",
    "DISJOINT",
    "IncidenceHashBundle",
    "IncidenceIntegrityReport",
    "IncidenceParticipantReference",
    "ParticipantRelationIncidenceFact",
    "RelationIncidenceSnapshot",
    "RelationIncidenceSnapshotInputs",
    "RelationOccurrenceReference",
    "RelationPairTopologyFact",
    "ResolvedBaziRelationIncidenceProfile",
    "SHARED_PARTICIPANT",
    "bazi_relation_incidence_foundation_r1_profile",
    "build_incidence_snapshot",
    "build_relation_incidence_context",
    "relation_incidence_fact_projection",
    "relation_incidence_hash_bundle",
    "validate_relation_incidence_context",
]

__version__ = "0.1.0"
