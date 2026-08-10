from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping


@dataclass(frozen=True)
class NatalMonthCommandReference:
    reference_id: str
    role_id: str
    upstream_natal_fact_hash: str
    source_branch_instance_id: str
    natal_month_ganzhi: str
    branch: str
    natal_profile_id: str
    natal_profile_version: str
    source_temporal_seed_ids: tuple[str, ...]
    time_calendar_policy_registry_versions: tuple[str, ...]
    rule_set_id: str
    rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class ActiveFlowSolarMonthReference:
    reference_id: str
    role_id: str
    upstream_flow_fact_hash: str
    source_monthly_frame_id: str
    source_temporal_branch_instance_id: str
    active_month_ganzhi: str
    branch: str
    start_jie_name: str
    start_jie_chinese_name: str
    start_jie_longitude_degrees: int
    start_utc: datetime
    end_jie_name: str
    end_jie_chinese_name: str
    end_jie_longitude_degrees: int
    end_utc: datetime
    interval_semantics: str
    rule_set_id: str
    rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class SupportEvidenceCandidate:
    candidate_id: str
    visible_stem_instance_id: str
    supporting_branch_instance_id: str
    matching_hidden_stem_instance_ids: tuple[str, ...]
    evidence_class: str
    visible_participant_layer: str
    supporting_branch_participant_layer: str
    participant_layers: tuple[str, ...]
    supporting_branch_role_ids: tuple[str, ...]
    source_affinity_fact_id: str
    source_exposure_link_ids: tuple[str, ...]
    rule_set_id: str
    rule_set_version: str
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class BaziStructuralSupportContext:
    upstream_natal_fact_hash: str
    upstream_temporal_fact_hash: str
    upstream_flow_fact_hash: str
    upstream_structural_fact_hash: str
    natal_month_command: NatalMonthCommandReference
    active_flow_solar_month: ActiveFlowSolarMonthReference
    support_evidence_candidates: tuple[SupportEvidenceCandidate, ...]
    natal_month_command_support_candidate_ids: tuple[str, ...]
    active_flow_solar_month_support_candidate_ids: tuple[str, ...]
    profile_id: str
    profile_version: str
    algorithm_versions: Mapping[str, str]


@dataclass(frozen=True)
class SupportIntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class SupportIntegrityReport:
    status: str
    diagnostics: tuple[SupportIntegrityDiagnostic, ...]
    algorithm_id: str = "BAZI-STRUCTURAL-SUPPORT-INTEGRITY-V1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class SupportHashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = "BAZI-STRUCTURAL-SUPPORT-HASH-V1"
    algorithm_version: str = "1.0.0"


@dataclass(frozen=True)
class BaziStructuralSupportCandidate:
    source_structural_candidate_indices: tuple[int, ...]
    source_flow_candidate_indices: tuple[int, ...]
    source_temporal_candidate_indices: tuple[int, ...]
    source_temporal_seed_ids: tuple[str, ...]
    context: BaziStructuralSupportContext
    integrity: SupportIntegrityReport
    hashes: SupportHashBundle


@dataclass(frozen=True)
class BaziStructuralSupportResolution:
    schema: str
    status: str
    candidates: tuple[BaziStructuralSupportCandidate, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]
