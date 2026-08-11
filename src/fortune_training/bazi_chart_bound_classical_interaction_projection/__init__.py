"""Chart-bound Classical interaction source-scope, neutral observation, and claim projection R1."""

from .engine import (
    BaziChartBoundClassicalInteractionProjectionEngine,
    BaziChartBoundClassicalInteractionProjectionError,
    BaziChartBoundClassicalInteractionProjectionRequest,
)
from .integrity import projection_hash_bundle, replay_source_binding_hashes, validate_projection_outer_candidate
from .models import *
from .observation import materialize_neutral_observation_bundle, matrix_dependency_primitives
from .profile import (
    ResolvedBaziChartBoundClassicalInteractionProjectionProfile,
    bazi_chart_bound_classical_interaction_projection_foundation_r1_profile,
)
from .projection import project_chart_bound_claims
from .scope import derive_source_scope_specifications, project_runtime_scope_compatibility

from .release import (
    AUDIT_ID,
    REPORT_PATH,
    RUNTIME_SCHEMA_PATH,
    SCHEMA_PATH,
    SCOPE_ARTIFACT_PATH,
    build_source_scope_artifact,
    validate_source_scope_artifact,
    write_source_scope_artifact,
)

__all__ = [name for name in globals() if not name.startswith("_")]
