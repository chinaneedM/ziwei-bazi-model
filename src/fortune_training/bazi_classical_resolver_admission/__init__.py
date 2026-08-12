"""Classical source semantic profile and resolver admission sidecar R1."""

from .dependency import (
    PRIMITIVE_OBSERVATION_ATTRIBUTE,
    NeutralDependencyMaterializationError,
    dependency_blocker_ids,
    normalize_neutral_dependency_materialization,
)
from .engine import (
    BaziClassicalResolverAdmissionEngine,
    BaziClassicalResolverAdmissionError,
    BaziClassicalResolverAdmissionRequest,
    project_fragment_admission,
)
from .integrity import (
    admission_hash_bundle,
    match_projection_outer,
    replay_effect_envelope,
    validate_admission_envelope,
)
from .models import *
from .profile import (
    ClassicalInteractionResolverAdmissionProfile,
    ClassicalSourceSemanticProfile,
    bazi_classical_resolver_admission_strict_r1_profile,
    shen_zpzq_ch09_classical_interaction_r1_profile,
)
from .release import (
    AUDIT_ID,
    CONTRACT_PATH,
    REPORT_PATH,
    RUNTIME_SCHEMA_PATH,
    SCHEMA_PATH,
    build_release_contract,
    validate_release_contract,
    write_release_contract,
)

__all__ = [name for name in globals() if not name.startswith("_")]
