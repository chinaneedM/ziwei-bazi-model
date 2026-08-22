"""Deterministic Ziwei and Bazi composition with shared time lineage."""

from .fusion_time import (
    SHARED_TIME_CREDENTIAL_SCHEMA,
    SHARED_TIME_LINEAGE_SCHEMA,
    build_candidate_lineage,
    build_shared_time_credential,
    validate_candidate_lineage,
    validate_shared_policy_contract,
    validate_subsystem_time_binding,
    validate_shared_time_credential,
)

from .flow_integrity import (
    combined_target_flow_bundle_hash,
    combined_target_flow_source_fact_hash,
    combined_target_flow_view_hash,
    validate_combined_target_flow_resolution,
)
from .flow_models import (
    COMBINED_TARGET_FLOW_SCHEMA,
    CombinedTargetFlowIntegrityReport,
    CombinedTargetFlowRequest,
    CombinedTargetFlowResolution,
)
from .flow_replay import validate_combined_target_flow_full_replay
from .flow_service import (
    CombinedTargetFlowResolutionError,
    CombinedTargetFlowService,
)
from .models import (
    CombinedApplicationIntegrityReport,
    CombinedChartApplicationRequest,
    CombinedChartApplicationResolution,
    CombinedSubsystemError,
)
from .profile import (
    COMBINED_MANIFEST_SCHEMA,
    COMBINED_PROFILE_ID,
    COMBINED_PROFILE_VERSION,
    CombinedChartApplicationProfile,
    combined_chart_application_v1_profile,
)
from .service import (
    COMBINED_EXPORT_SCHEMA,
    COMBINED_RESOLUTION_SCHEMA,
    CombinedApplicationResolutionError,
    CombinedChartService,
    combined_manifest_hash,
    combined_manifest_payload,
    validate_combined_resolution,
)
from .shared_time_integrity import (
    shared_selector_candidate_hash,
    shared_selector_hash_bundle,
    validate_shared_ziwei_selector_projection,
)
from .shared_time_models import (
    SHARED_ZIWEI_SELECTOR_PROJECTION_ALGORITHM_ID,
    SHARED_ZIWEI_SELECTOR_PROJECTION_ALGORITHM_VERSION,
    SHARED_ZIWEI_SELECTOR_PROJECTION_SCHEMA,
    SharedZiweiHourlyMethodCandidate,
    SharedZiweiSelectorProjectionCandidate,
    SharedZiweiSelectorProjectionHashBundle,
    SharedZiweiSelectorProjectionIntegrityReport,
    SharedZiweiSelectorProjectionResolution,
)
from .shared_time_replay import validate_shared_ziwei_selector_full_replay
from .shared_time_service import (
    SharedZiweiSelectorProjectionError,
    SharedZiweiSelectorProjectionService,
)

__all__ = [
    "COMBINED_EXPORT_SCHEMA",
    "COMBINED_MANIFEST_SCHEMA",
    "COMBINED_PROFILE_ID",
    "COMBINED_PROFILE_VERSION",
    "COMBINED_RESOLUTION_SCHEMA",
    "COMBINED_TARGET_FLOW_SCHEMA",
    "SHARED_ZIWEI_SELECTOR_PROJECTION_ALGORITHM_ID",
    "SHARED_ZIWEI_SELECTOR_PROJECTION_ALGORITHM_VERSION",
    "SHARED_ZIWEI_SELECTOR_PROJECTION_SCHEMA",
    "SHARED_TIME_CREDENTIAL_SCHEMA",
    "SHARED_TIME_LINEAGE_SCHEMA",
    "CombinedApplicationIntegrityReport",
    "CombinedApplicationResolutionError",
    "CombinedChartApplicationProfile",
    "CombinedChartApplicationRequest",
    "CombinedChartApplicationResolution",
    "CombinedChartService",
    "CombinedSubsystemError",
    "CombinedTargetFlowIntegrityReport",
    "CombinedTargetFlowRequest",
    "CombinedTargetFlowResolution",
    "CombinedTargetFlowResolutionError",
    "CombinedTargetFlowService",
    "SharedZiweiSelectorProjectionCandidate",
    "SharedZiweiHourlyMethodCandidate",
    "SharedZiweiSelectorProjectionError",
    "SharedZiweiSelectorProjectionHashBundle",
    "SharedZiweiSelectorProjectionIntegrityReport",
    "SharedZiweiSelectorProjectionResolution",
    "SharedZiweiSelectorProjectionService",
    "build_candidate_lineage",
    "build_shared_time_credential",
    "combined_chart_application_v1_profile",
    "combined_manifest_hash",
    "combined_manifest_payload",
    "combined_target_flow_bundle_hash",
    "combined_target_flow_source_fact_hash",
    "combined_target_flow_view_hash",
    "shared_selector_candidate_hash",
    "shared_selector_hash_bundle",
    "validate_combined_resolution",
    "validate_candidate_lineage",
    "validate_combined_target_flow_full_replay",
    "validate_combined_target_flow_resolution",
    "validate_shared_ziwei_selector_full_replay",
    "validate_shared_ziwei_selector_projection",
    "validate_shared_policy_contract",
    "validate_subsystem_time_binding",
    "validate_shared_time_credential",
]

__version__ = "0.3.0"
