from __future__ import annotations

from datetime import timezone
from typing import Any

from fortune_training.bazi_chart import BaziChartCandidate
from fortune_training.bazi_flow import BaziFlowCandidate
from fortune_training.bazi_structural import BaziStructuralCandidate
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .generation import (
    ACTIVE_FLOW_SOLAR_MONTH,
    EXACT_HIDDEN_STEM_MATCH,
    NATAL_MONTH_COMMAND,
    SAME_ELEMENT_HIDDEN_SUPPORT,
    build_structural_support_context,
)
from .models import (
    BaziStructuralSupportContext,
    SupportHashBundle,
    SupportIntegrityDiagnostic,
    SupportIntegrityReport,
)
from .profile import ResolvedBaziStructuralSupportProfile


INTEGRITY_ALGORITHM_ID = "BAZI-STRUCTURAL-SUPPORT-INTEGRITY-V1"
INTEGRITY_ALGORITHM_VERSION = "1.0.0"
HASH_ALGORITHM_ID = "BAZI-STRUCTURAL-SUPPORT-HASH-V1"
HASH_ALGORITHM_VERSION = "1.0.0"


def _diag(rows, code: str, path: str, detail: str) -> None:
    rows.append(SupportIntegrityDiagnostic(code=code, path=path, detail=detail))


def _instant_fact(value) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("support fact instant must be timezone-aware")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds")


def _natal_role_fact(row) -> dict[str, Any]:
    return {
        "reference_id": row.reference_id,
        "role_id": row.role_id,
        "upstream_natal_fact_hash": row.upstream_natal_fact_hash,
        "source_branch_instance_id": row.source_branch_instance_id,
        "natal_month_ganzhi": row.natal_month_ganzhi,
        "branch": row.branch,
        "natal_profile_id": row.natal_profile_id,
        "natal_profile_version": row.natal_profile_version,
        "source_temporal_seed_ids": sorted(row.source_temporal_seed_ids),
        "time_calendar_policy_registry_versions": sorted(
            row.time_calendar_policy_registry_versions
        ),
    }


def _flow_role_fact(row) -> dict[str, Any]:
    return {
        "reference_id": row.reference_id,
        "role_id": row.role_id,
        "upstream_flow_fact_hash": row.upstream_flow_fact_hash,
        "source_monthly_frame_id": row.source_monthly_frame_id,
        "source_temporal_branch_instance_id": row.source_temporal_branch_instance_id,
        "active_month_ganzhi": row.active_month_ganzhi,
        "branch": row.branch,
        "start_jie_name": row.start_jie_name,
        "start_jie_chinese_name": row.start_jie_chinese_name,
        "start_jie_longitude_degrees": row.start_jie_longitude_degrees,
        "start_utc": _instant_fact(row.start_utc),
        "end_jie_name": row.end_jie_name,
        "end_jie_chinese_name": row.end_jie_chinese_name,
        "end_jie_longitude_degrees": row.end_jie_longitude_degrees,
        "end_utc": _instant_fact(row.end_utc),
        "interval_semantics": row.interval_semantics,
    }


def _evidence_fact(row) -> dict[str, Any]:
    return {
        "candidate_id": row.candidate_id,
        "visible_stem_instance_id": row.visible_stem_instance_id,
        "supporting_branch_instance_id": row.supporting_branch_instance_id,
        "matching_hidden_stem_instance_ids": sorted(
            row.matching_hidden_stem_instance_ids
        ),
        "evidence_class": row.evidence_class,
        "visible_participant_layer": row.visible_participant_layer,
        "supporting_branch_participant_layer": row.supporting_branch_participant_layer,
        "participant_layers": list(row.participant_layers),
        "supporting_branch_role_ids": list(row.supporting_branch_role_ids),
        "source_affinity_fact_id": row.source_affinity_fact_id,
        "source_exposure_link_ids": sorted(row.source_exposure_link_ids),
    }


def structural_support_fact_projection(
    context: BaziStructuralSupportContext,
) -> dict[str, Any]:
    return {
        "upstream_natal_fact_hash": context.upstream_natal_fact_hash,
        "upstream_temporal_fact_hash": context.upstream_temporal_fact_hash,
        "upstream_flow_fact_hash": context.upstream_flow_fact_hash,
        "upstream_structural_fact_hash": context.upstream_structural_fact_hash,
        "natal_month_command": _natal_role_fact(context.natal_month_command),
        "active_flow_solar_month": _flow_role_fact(context.active_flow_solar_month),
        "support_evidence_candidates": [
            _evidence_fact(row) for row in context.support_evidence_candidates
        ],
        "natal_month_command_support_candidate_ids": sorted(
            context.natal_month_command_support_candidate_ids
        ),
        "active_flow_solar_month_support_candidate_ids": sorted(
            context.active_flow_solar_month_support_candidate_ids
        ),
    }


def structural_support_hash_bundle(
    context: BaziStructuralSupportContext,
    natal: BaziChartCandidate,
    flow: BaziFlowCandidate,
    structural: BaziStructuralCandidate,
    profile: ResolvedBaziStructuralSupportProfile,
) -> SupportHashBundle:
    fact_hash = object_sha256(structural_support_fact_projection(context))
    generated_rows = (
        context.natal_month_command,
        context.active_flow_solar_month,
    ) + context.support_evidence_candidates
    computation_hash = object_sha256({
        "fact_hash": fact_hash,
        "upstream_natal_computation_hash": natal.hashes.computation_hash,
        "upstream_flow_computation_hash": flow.hashes.computation_hash,
        "upstream_structural_computation_hash": structural.hashes.computation_hash,
        "resolved_support_profile": json_value(profile),
        "algorithm_versions": dict(sorted(context.algorithm_versions.items())),
        "rule_and_source_lineage": [
            {
                "rule_set_id": row.rule_set_id,
                "rule_set_version": row.rule_set_version,
                "source_refs": sorted(row.source_refs),
            }
            for row in generated_rows
        ],
        "hash_algorithm": f"{HASH_ALGORITHM_ID}@{HASH_ALGORITHM_VERSION}",
    })
    return SupportHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=HASH_ALGORITHM_ID,
        algorithm_version=HASH_ALGORITHM_VERSION,
    )


def validate_structural_support_context(
    context: BaziStructuralSupportContext,
    natal: BaziChartCandidate,
    flow: BaziFlowCandidate,
    structural: BaziStructuralCandidate,
    profile: ResolvedBaziStructuralSupportProfile,
    hashes: SupportHashBundle | None = None,
) -> SupportIntegrityReport:
    diagnostics: list[SupportIntegrityDiagnostic] = []
    try:
        profile.validate()
    except ValueError as exc:
        _diag(diagnostics, "PROFILE_INVALID", "profile", str(exc))

    upstream_checks = (
        ("UPSTREAM_NATAL_HASH_MISMATCH", "upstream_natal_fact_hash", natal.hashes.fact_hash),
        (
            "UPSTREAM_TEMPORAL_HASH_MISMATCH",
            "upstream_temporal_fact_hash",
            structural.context.upstream_temporal_fact_hash,
        ),
        ("UPSTREAM_FLOW_HASH_MISMATCH", "upstream_flow_fact_hash", flow.hashes.fact_hash),
        (
            "UPSTREAM_STRUCTURAL_HASH_MISMATCH",
            "upstream_structural_fact_hash",
            structural.hashes.fact_hash,
        ),
    )
    for code, field, expected_value in upstream_checks:
        if getattr(context, field) != expected_value:
            _diag(diagnostics, code, field, getattr(context, field))
    if structural.context.upstream_natal_fact_hash != natal.hashes.fact_hash:
        _diag(
            diagnostics,
            "STRUCTURAL_NATAL_LINEAGE_MISMATCH",
            "upstream_structural_fact_hash",
            structural.context.upstream_natal_fact_hash,
        )
    if structural.context.upstream_flow_fact_hash != flow.hashes.fact_hash:
        _diag(
            diagnostics,
            "STRUCTURAL_FLOW_LINEAGE_MISMATCH",
            "upstream_structural_fact_hash",
            structural.context.upstream_flow_fact_hash,
        )
    if (context.profile_id, context.profile_version) != (
        profile.profile_id,
        profile.profile_version,
    ):
        _diag(
            diagnostics,
            "SUPPORT_PROFILE_BINDING_MISMATCH",
            "profile_id",
            context.profile_id,
        )

    try:
        expected = build_structural_support_context(natal, flow, structural, profile)
    except (ValueError, StopIteration) as exc:
        _diag(diagnostics, "SUPPORT_REPLAY_FAILED", "context", str(exc))
        expected = None
    if expected is not None:
        replay_checks = (
            ("NATAL_MONTH_COMMAND_REPLAY_MISMATCH", "natal_month_command"),
            ("ACTIVE_FLOW_MONTH_REPLAY_MISMATCH", "active_flow_solar_month"),
            ("SUPPORT_EVIDENCE_REPLAY_MISMATCH", "support_evidence_candidates"),
            (
                "MONTH_COMMAND_SUPPORT_SET_MISMATCH",
                "natal_month_command_support_candidate_ids",
            ),
            (
                "FLOW_MONTH_SUPPORT_SET_MISMATCH",
                "active_flow_solar_month_support_candidate_ids",
            ),
            ("SUPPORT_ALGORITHM_VERSION_MISMATCH", "algorithm_versions"),
        )
        for code, field in replay_checks:
            if getattr(context, field) != getattr(expected, field):
                _diag(diagnostics, code, field, "deterministic support replay mismatch")

    month_pillar = next(
        (row for row in natal.chart.pillars if row.position == "MONTH"), None
    )
    month_branch = next(
        (row for row in natal.chart.branches if row.position == "MONTH"), None
    )
    natal_role = context.natal_month_command
    if (
        month_pillar is None
        or month_branch is None
        or natal_role.role_id != NATAL_MONTH_COMMAND
        or natal_role.source_branch_instance_id != month_branch.instance_id
        or natal_role.natal_month_ganzhi != month_pillar.ganzhi
        or natal_role.branch != month_branch.branch
    ):
        _diag(
            diagnostics,
            "NATAL_MONTH_COMMAND_BINDING_INVALID",
            "natal_month_command",
            natal_role.reference_id,
        )

    monthly_frame = flow.context.monthly_frame
    flow_role = context.active_flow_solar_month
    monthly_branch = next(
        (
            row for row in structural.context.active_temporal_branches
            if row.position == "MONTHLY"
        ),
        None,
    )
    if (
        monthly_branch is None
        or flow_role.role_id != ACTIVE_FLOW_SOLAR_MONTH
        or flow_role.source_monthly_frame_id != monthly_frame.frame_id
        or flow_role.source_temporal_branch_instance_id != monthly_branch.instance_id
        or flow_role.active_month_ganzhi != monthly_frame.ganzhi
        or flow_role.branch != monthly_branch.branch
        or not (flow_role.start_utc <= flow.context.target_utc < flow_role.end_utc)
    ):
        _diag(
            diagnostics,
            "ACTIVE_FLOW_MONTH_BINDING_INVALID",
            "active_flow_solar_month",
            flow_role.reference_id,
        )
    if natal_role.role_id == flow_role.role_id:
        _diag(
            diagnostics,
            "SEASONAL_ROLES_ALIASED",
            "seasonal_roles",
            natal_role.role_id,
        )

    stems = natal.chart.stems + structural.context.active_temporal_stems
    branches = natal.chart.branches + structural.context.active_temporal_branches
    hidden = natal.chart.hidden_stems + structural.context.temporal_hidden_stems
    affinities = natal.chart.affinities + structural.context.dynamic_affinities
    exposures = natal.chart.exposures + structural.context.dynamic_exposures
    stem_by_id = {row.instance_id: row for row in stems}
    branch_by_id = {row.instance_id: row for row in branches}
    hidden_by_id = {row.instance_id: row for row in hidden}
    affinity_by_id = {row.fact_id: row for row in affinities}
    exposure_ids = {row.link_id for row in exposures}
    seen_candidate_ids: set[str] = set()
    for index, row in enumerate(context.support_evidence_candidates):
        path = f"support_evidence_candidates[{index}]"
        if row.candidate_id in seen_candidate_ids:
            _diag(diagnostics, "DUPLICATE_SUPPORT_CANDIDATE", path, row.candidate_id)
        seen_candidate_ids.add(row.candidate_id)
        visible = stem_by_id.get(row.visible_stem_instance_id)
        branch = branch_by_id.get(row.supporting_branch_instance_id)
        affinity = affinity_by_id.get(row.source_affinity_fact_id)
        matching = [hidden_by_id.get(hidden_id) for hidden_id in row.matching_hidden_stem_instance_ids]
        if visible is None or branch is None or any(item is None for item in matching):
            _diag(diagnostics, "SUPPORT_PARTICIPANT_MISSING", path, row.candidate_id)
            continue
        if affinity is None:
            _diag(diagnostics, "SOURCE_AFFINITY_MISSING", path, row.source_affinity_fact_id)
            continue
        if (
            affinity.visible_stem_instance_id != visible.instance_id
            or affinity.branch_instance_id != branch.instance_id
        ):
            _diag(diagnostics, "SOURCE_AFFINITY_PARTICIPANT_MISMATCH", path, row.source_affinity_fact_id)
        if not set(row.source_exposure_link_ids) <= exposure_ids:
            _diag(diagnostics, "SOURCE_EXPOSURE_MISSING", path, row.candidate_id)
        if row.evidence_class == EXACT_HIDDEN_STEM_MATCH:
            if any(item.stem != visible.stem for item in matching):
                _diag(diagnostics, "EXACT_SUPPORT_MISLABELED", path, row.candidate_id)
            if not row.source_exposure_link_ids:
                _diag(diagnostics, "EXACT_SUPPORT_EXPOSURE_MISSING", path, row.candidate_id)
        elif row.evidence_class == SAME_ELEMENT_HIDDEN_SUPPORT:
            if any(
                item.element != visible.element or item.stem == visible.stem
                for item in matching
            ):
                _diag(diagnostics, "SAME_ELEMENT_SUPPORT_MISLABELED", path, row.candidate_id)
            if row.source_exposure_link_ids:
                _diag(diagnostics, "SAME_ELEMENT_SUPPORT_HAS_EXACT_EXPOSURE", path, row.candidate_id)
        else:
            _diag(diagnostics, "SUPPORT_EVIDENCE_CLASS_INVALID", path, row.evidence_class)
        for prohibited_field in (
            "weight",
            "strength",
            "root_grade",
            "registry_ordinal",
        ):
            if hasattr(row, prohibited_field):
                _diag(
                    diagnostics,
                    "PROHIBITED_SUPPORT_GRADE_PRESENT",
                    path,
                    prohibited_field,
                )

    if flow.context.active_dayun_kind == "PRE_DAYUN" and any(
        "DAYUN" in row.participant_layers
        for row in context.support_evidence_candidates
    ):
        _diag(
            diagnostics,
            "PRE_DAYUN_FAKE_SUPPORT_CANDIDATE",
            "support_evidence_candidates",
            "PRE_DAYUN cannot produce a Dayun support occurrence",
        )

    if hashes is not None:
        expected_hashes = structural_support_hash_bundle(
            context, natal, flow, structural, profile
        )
        if hashes != expected_hashes:
            _diag(
                diagnostics,
                "SUPPORT_HASH_REPLAY_MISMATCH",
                "hashes",
                hashes.fact_hash,
            )

    return SupportIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=INTEGRITY_ALGORITHM_ID,
        algorithm_version=INTEGRITY_ALGORITHM_VERSION,
    )
