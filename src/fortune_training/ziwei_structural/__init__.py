"""Ziwei Structural Runtime V2-R1 neutral topology layer."""

from .engine import StructuralGenerationError, ZiweiStructuralRuntime
from .integrity import (
    STRUCTURAL_INTEGRITY_ALGORITHM_ID,
    STRUCTURAL_INTEGRITY_ALGORITHM_VERSION,
    structural_fact_projection,
    structural_hash_bundle,
    validate_structural_components,
    validate_structural_state,
)
from .models import (
    STRUCTURAL_STATE_SCHEMA,
    AddressOffsetFact,
    StructuralHashBundle,
    StructuralIntegrityDiagnostic,
    StructuralIntegrityReport,
    StructuralState,
)
from .profile import (
    NEUTRAL_Z12_TOPOLOGY_ALGORITHM_ID,
    NEUTRAL_Z12_TOPOLOGY_ALGORITHM_VERSION,
    ZIWEI_STRUCTURAL_V2_R1_PROFILE_ID,
    ZIWEI_STRUCTURAL_V2_R1_PROFILE_VERSION,
    ResolvedZiweiStructuralProfile,
    ziwei_structural_v2_r1_profile,
)
from .topology import (
    NeutralZ12Topology,
    StructuralTopologyError,
    canonical_addresses,
    clockwise_offset,
    shift,
)


__all__ = [
    "AddressOffsetFact",
    "NEUTRAL_Z12_TOPOLOGY_ALGORITHM_ID",
    "NEUTRAL_Z12_TOPOLOGY_ALGORITHM_VERSION",
    "NeutralZ12Topology",
    "ResolvedZiweiStructuralProfile",
    "STRUCTURAL_INTEGRITY_ALGORITHM_ID",
    "STRUCTURAL_INTEGRITY_ALGORITHM_VERSION",
    "STRUCTURAL_STATE_SCHEMA",
    "StructuralGenerationError",
    "StructuralHashBundle",
    "StructuralIntegrityDiagnostic",
    "StructuralIntegrityReport",
    "StructuralState",
    "StructuralTopologyError",
    "ZIWEI_STRUCTURAL_V2_R1_PROFILE_ID",
    "ZIWEI_STRUCTURAL_V2_R1_PROFILE_VERSION",
    "ZiweiStructuralRuntime",
    "canonical_addresses",
    "clockwise_offset",
    "shift",
    "structural_fact_projection",
    "structural_hash_bundle",
    "validate_structural_components",
    "validate_structural_state",
    "ziwei_structural_v2_r1_profile",
]

__version__ = "2.0.0-r1"
