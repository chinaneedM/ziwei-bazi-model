from __future__ import annotations

from fortune_training.bazi_chart import BaziChartCandidate
from fortune_training.bazi_flow import BaziFlowCandidate
from fortune_training.bazi_structural import BaziStructuralCandidate

from .models import (
    ActiveFlowSolarMonthReference,
    BaziStructuralSupportContext,
    NatalMonthCommandReference,
    SupportEvidenceCandidate,
)
from .profile import (
    ResolvedBaziStructuralSupportProfile,
    SEASONAL_ROLE_RULE_SET_ID,
    SEASONAL_ROLE_RULE_SET_VERSION,
    SUPPORT_EVIDENCE_RULE_SET_ID,
    SUPPORT_EVIDENCE_RULE_SET_VERSION,
)


NATAL_MONTH_COMMAND = "NATAL_MONTH_COMMAND"
ACTIVE_FLOW_SOLAR_MONTH = "ACTIVE_FLOW_SOLAR_MONTH"
EXACT_HIDDEN_STEM_MATCH = "EXACT_HIDDEN_STEM_MATCH"
SAME_ELEMENT_HIDDEN_SUPPORT = "SAME_ELEMENT_HIDDEN_SUPPORT"
LAYER_ORDER = ("NATAL", "DAYUN", "ANNUAL", "MONTHLY")


def _participant_layer(position: str) -> str:
    return "NATAL" if position in {"YEAR", "MONTH", "DAY", "HOUR"} else position


def _participant_layers(visible_layer: str, branch_layer: str) -> tuple[str, ...]:
    active = {visible_layer, branch_layer}
    return tuple(layer for layer in LAYER_ORDER if layer in active)


def _natal_month_command(natal: BaziChartCandidate) -> NatalMonthCommandReference:
    pillar = next(row for row in natal.chart.pillars if row.position == "MONTH")
    branch = next(
        row for row in natal.chart.branches
        if row.instance_id == pillar.branch_instance_id
    )
    seed_ids = tuple(sorted(seed.seed_id for seed in natal.temporal_seeds))
    policy_versions = tuple(sorted({
        seed.time_calendar_policy_registry_version for seed in natal.temporal_seeds
    }))
    return NatalMonthCommandReference(
        reference_id=(
            f"SEASONAL_ROLE:{NATAL_MONTH_COMMAND}:"
            f"{natal.hashes.fact_hash}:{branch.instance_id}"
        ),
        role_id=NATAL_MONTH_COMMAND,
        upstream_natal_fact_hash=natal.hashes.fact_hash,
        source_branch_instance_id=branch.instance_id,
        natal_month_ganzhi=pillar.ganzhi,
        branch=branch.branch,
        natal_profile_id=natal.chart.profile_id,
        natal_profile_version=natal.chart.profile_version,
        source_temporal_seed_ids=seed_ids,
        time_calendar_policy_registry_versions=policy_versions,
        rule_set_id=SEASONAL_ROLE_RULE_SET_ID,
        rule_set_version=SEASONAL_ROLE_RULE_SET_VERSION,
        source_refs=("BAZI-CHART-FOUNDATION-V1", "TIME-CALENDAR-FOUNDATION-R1"),
    )


def _active_flow_solar_month(
    flow: BaziFlowCandidate,
    structural: BaziStructuralCandidate,
) -> ActiveFlowSolarMonthReference:
    frame = flow.context.monthly_frame
    branch_id = f"{frame.frame_id}.BRANCH"
    branch = next(
        row for row in structural.context.active_temporal_branches
        if row.instance_id == branch_id and row.position == "MONTHLY"
    )
    provenance = next(
        row for row in structural.context.temporal_participant_provenance
        if row.instance_id == branch_id
    )
    if provenance.source_frame_id != frame.frame_id:
        raise ValueError("Structural MONTHLY branch does not bind the active MonthlyFrame")
    return ActiveFlowSolarMonthReference(
        reference_id=(
            f"SEASONAL_ROLE:{ACTIVE_FLOW_SOLAR_MONTH}:"
            f"{frame.frame_id}:{branch_id}"
        ),
        role_id=ACTIVE_FLOW_SOLAR_MONTH,
        upstream_flow_fact_hash=flow.hashes.fact_hash,
        source_monthly_frame_id=frame.frame_id,
        source_temporal_branch_instance_id=branch_id,
        active_month_ganzhi=frame.ganzhi,
        branch=branch.branch,
        start_jie_name=frame.start_jie_name,
        start_jie_chinese_name=frame.start_jie_chinese_name,
        start_jie_longitude_degrees=frame.start_jie_longitude_degrees,
        start_utc=frame.start_utc,
        end_jie_name=frame.end_jie_name,
        end_jie_chinese_name=frame.end_jie_chinese_name,
        end_jie_longitude_degrees=frame.end_jie_longitude_degrees,
        end_utc=frame.end_utc,
        interval_semantics=frame.interval_semantics,
        rule_set_id=SEASONAL_ROLE_RULE_SET_ID,
        rule_set_version=SEASONAL_ROLE_RULE_SET_VERSION,
        source_refs=("BAZI-TEMPORAL-FLOW-CONTEXT-R1", "BAZI-STRUCTURAL-CONTEXT-R1"),
    )


def _candidate_id(
    evidence_class: str,
    visible_id: str,
    branch_id: str,
    hidden_ids: tuple[str, ...],
) -> str:
    return (
        f"SUPPORT:{evidence_class}:{visible_id}<->{branch_id}:"
        + "+".join(hidden_ids)
    )


def _support_candidates(
    natal: BaziChartCandidate,
    structural: BaziStructuralCandidate,
    natal_role: NatalMonthCommandReference,
    flow_role: ActiveFlowSolarMonthReference,
) -> tuple[SupportEvidenceCandidate, ...]:
    chart = natal.chart
    context = structural.context
    stems = chart.stems + context.active_temporal_stems
    branches = chart.branches + context.active_temporal_branches
    affinities = chart.affinities + context.dynamic_affinities
    exposures = chart.exposures + context.dynamic_exposures
    stem_by_id = {row.instance_id: row for row in stems}
    branch_by_id = {row.instance_id: row for row in branches}
    exposure_by_pair = {
        (row.visible_stem_instance_id, row.hidden_stem_instance_id): row.link_id
        for row in exposures
    }

    rows: list[SupportEvidenceCandidate] = []
    for affinity in affinities:
        visible = stem_by_id[affinity.visible_stem_instance_id]
        branch = branch_by_id[affinity.branch_instance_id]
        visible_layer = _participant_layer(visible.position)
        branch_layer = _participant_layer(branch.position)
        role_ids = tuple(
            role_id
            for role_id, instance_id in (
                (NATAL_MONTH_COMMAND, natal_role.source_branch_instance_id),
                (ACTIVE_FLOW_SOLAR_MONTH, flow_role.source_temporal_branch_instance_id),
            )
            if branch.instance_id == instance_id
        )
        common = {
            "visible_stem_instance_id": visible.instance_id,
            "supporting_branch_instance_id": branch.instance_id,
            "visible_participant_layer": visible_layer,
            "supporting_branch_participant_layer": branch_layer,
            "participant_layers": _participant_layers(visible_layer, branch_layer),
            "supporting_branch_role_ids": role_ids,
            "source_affinity_fact_id": affinity.fact_id,
            "rule_set_id": SUPPORT_EVIDENCE_RULE_SET_ID,
            "rule_set_version": SUPPORT_EVIDENCE_RULE_SET_VERSION,
            "source_refs": tuple(dict.fromkeys(
                affinity.source_refs + ("BAZI-STRUCTURAL-CONTEXT-R1",)
            )),
        }

        exact_ids = tuple(sorted(affinity.exact_hidden_stem_instance_ids))
        if exact_ids:
            exposure_ids = tuple(sorted(
                exposure_by_pair[(visible.instance_id, hidden_id)]
                for hidden_id in exact_ids
            ))
            rows.append(SupportEvidenceCandidate(
                candidate_id=_candidate_id(
                    EXACT_HIDDEN_STEM_MATCH,
                    visible.instance_id,
                    branch.instance_id,
                    exact_ids,
                ),
                matching_hidden_stem_instance_ids=exact_ids,
                evidence_class=EXACT_HIDDEN_STEM_MATCH,
                source_exposure_link_ids=exposure_ids,
                **common,
            ))

        same_element_only = tuple(sorted(
            set(affinity.same_element_hidden_stem_instance_ids) - set(exact_ids)
        ))
        if same_element_only:
            rows.append(SupportEvidenceCandidate(
                candidate_id=_candidate_id(
                    SAME_ELEMENT_HIDDEN_SUPPORT,
                    visible.instance_id,
                    branch.instance_id,
                    same_element_only,
                ),
                matching_hidden_stem_instance_ids=same_element_only,
                evidence_class=SAME_ELEMENT_HIDDEN_SUPPORT,
                source_exposure_link_ids=(),
                **common,
            ))
    return tuple(sorted(rows, key=lambda row: row.candidate_id))


def build_structural_support_context(
    natal: BaziChartCandidate,
    flow: BaziFlowCandidate,
    structural: BaziStructuralCandidate,
    profile: ResolvedBaziStructuralSupportProfile,
) -> BaziStructuralSupportContext:
    profile.validate()
    if structural.context.upstream_natal_fact_hash != natal.hashes.fact_hash:
        raise ValueError("Structural candidate does not descend from supplied Natal candidate")
    if structural.context.upstream_flow_fact_hash != flow.hashes.fact_hash:
        raise ValueError("Structural candidate does not descend from supplied Flow candidate")
    natal_role = _natal_month_command(natal)
    flow_role = _active_flow_solar_month(flow, structural)
    candidates = _support_candidates(natal, structural, natal_role, flow_role)
    return BaziStructuralSupportContext(
        upstream_natal_fact_hash=natal.hashes.fact_hash,
        upstream_temporal_fact_hash=structural.context.upstream_temporal_fact_hash,
        upstream_flow_fact_hash=flow.hashes.fact_hash,
        upstream_structural_fact_hash=structural.hashes.fact_hash,
        natal_month_command=natal_role,
        active_flow_solar_month=flow_role,
        support_evidence_candidates=candidates,
        natal_month_command_support_candidate_ids=tuple(
            row.candidate_id for row in candidates
            if NATAL_MONTH_COMMAND in row.supporting_branch_role_ids
        ),
        active_flow_solar_month_support_candidate_ids=tuple(
            row.candidate_id for row in candidates
            if ACTIVE_FLOW_SOLAR_MONTH in row.supporting_branch_role_ids
        ),
        profile_id=profile.profile_id,
        profile_version=profile.profile_version,
        algorithm_versions={
            "support": profile.algorithm_version,
            "seasonal_roles": profile.seasonal_role_rule_set_version,
            "support_evidence": profile.support_evidence_rule_set_version,
        },
    )
