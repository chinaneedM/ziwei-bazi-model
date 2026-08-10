from __future__ import annotations

from fortune_training.bazi_chart import (
    BaziChartCandidate,
    BranchInstance,
    StemInstance,
    TenGodBinding,
)
from fortune_training.bazi_chart.hidden_stems import (
    AFFINITY_ALGORITHM_VERSION,
    HIDDEN_STEM_ALGORITHM_VERSION,
    generate_affinities,
    generate_exposures,
    generate_hidden_stems,
)
from fortune_training.bazi_chart.registries import (
    BRANCH_ELEMENTS,
    STEM_ELEMENTS,
    STEM_POLARITY,
    TEN_GOD_RULE_SET_ID,
    TEN_GOD_RULE_SET_VERSION,
)
from fortune_training.bazi_chart.relations import (
    RAW_RELATION_ALGORITHM_VERSION,
    generate_raw_relations,
)
from fortune_training.bazi_chart.ten_gods import TEN_GOD_ALGORITHM_VERSION, ten_god
from fortune_training.bazi_flow import BaziFlowCandidate

from .models import (
    BaziStructuralContext,
    DynamicRelationOccurrence,
    TemporalParticipantProvenance,
)
from .profile import (
    PARTICIPANT_RULE_SET_VERSION,
    RELATION_SCOPE_RULE_SET_VERSION,
    ResolvedBaziStructuralProfile,
)


LAYER_ORDER = ("NATAL", "DAYUN", "ANNUAL", "MONTHLY")


def _visible_pair(
    layer: str,
    frame_id: str,
    ganzhi: str,
    flow_fact_hash: str,
) -> tuple[
    StemInstance,
    BranchInstance,
    tuple[TemporalParticipantProvenance, TemporalParticipantProvenance],
]:
    # All released active frame IDs are already layer-namespaced. Reusing that
    # identity avoids inventing a parallel occurrence namespace.
    stem_id = f"{frame_id}.STEM"
    branch_id = f"{frame_id}.BRANCH"
    stem = StemInstance(
        instance_id=stem_id,
        position=layer,
        stem=ganzhi[0],
        element=STEM_ELEMENTS[ganzhi[0]],
        polarity=STEM_POLARITY[ganzhi[0]],
    )
    branch = BranchInstance(
        instance_id=branch_id,
        position=layer,
        branch=ganzhi[1],
        element_affiliation=BRANCH_ELEMENTS[ganzhi[1]],
    )
    provenance = (
        TemporalParticipantProvenance(
            instance_id=stem_id,
            layer=layer,
            source_frame_id=frame_id,
            source_flow_fact_hash=flow_fact_hash,
            source_ganzhi=ganzhi,
        ),
        TemporalParticipantProvenance(
            instance_id=branch_id,
            layer=layer,
            source_frame_id=frame_id,
            source_flow_fact_hash=flow_fact_hash,
            source_ganzhi=ganzhi,
        ),
    )
    return stem, branch, provenance


def materialize_temporal_participants(
    flow: BaziFlowCandidate,
) -> tuple[
    tuple[StemInstance, ...],
    tuple[BranchInstance, ...],
    tuple[TemporalParticipantProvenance, ...],
]:
    context = flow.context
    frames: list[tuple[str, str, str]] = []
    if context.active_dayun_kind == "DAYUN":
        frames.append(
            (
                "DAYUN",
                context.active_dayun_frame.frame_id,
                context.active_dayun_frame.ganzhi,
            )
        )
    frames.extend(
        (
            ("ANNUAL", context.annual_frame.frame_id, context.annual_frame.ganzhi),
            ("MONTHLY", context.monthly_frame.frame_id, context.monthly_frame.ganzhi),
        )
    )

    stems: list[StemInstance] = []
    branches: list[BranchInstance] = []
    provenance: list[TemporalParticipantProvenance] = []
    for layer, frame_id, ganzhi in frames:
        stem, branch, pair_provenance = _visible_pair(
            layer,
            frame_id,
            ganzhi,
            flow.hashes.fact_hash,
        )
        stems.append(stem)
        branches.append(branch)
        provenance.extend(pair_provenance)
    return tuple(stems), tuple(branches), tuple(provenance)


def _temporal_ten_gods(day_master: str, stems, hidden_stems) -> tuple[TenGodBinding, ...]:
    rows: list[TenGodBinding] = []
    targets = tuple((row.instance_id, row.stem) for row in stems) + tuple(
        (row.instance_id, row.stem) for row in hidden_stems
    )
    for target_id, target_stem in targets:
        semantic_id, display = ten_god(day_master, target_stem)
        rows.append(
            TenGodBinding(
                binding_id=f"TEN_GOD:{target_id}",
                target_instance_id=target_id,
                target_stem=target_stem,
                day_master_stem=day_master,
                semantic_role_id=semantic_id,
                display_name=display,
                rule_set_id=TEN_GOD_RULE_SET_ID,
                rule_set_version=TEN_GOD_RULE_SET_VERSION,
                source_refs=("S11",),
            )
        )
    return tuple(rows)


def _dynamic_relation_occurrences(relations, layer_by_instance):
    rows: list[DynamicRelationOccurrence] = []
    for relation in relations:
        participant_layers = tuple(
            layer for layer in LAYER_ORDER if layer in {
                layer_by_instance[instance_id]
                for instance_id in relation.participant_instance_ids
            }
        )
        if participant_layers == ("NATAL",):
            continue
        scope = "CROSS_LAYER" if "NATAL" in participant_layers else "TEMPORAL_ONLY"
        rows.append(
            DynamicRelationOccurrence(
                relation_id=relation.relation_id,
                semantic_relation_id=relation.semantic_relation_id,
                relation_family=relation.relation_family,
                participant_instance_ids=relation.participant_instance_ids,
                participant_layers=participant_layers,
                relation_scope=scope,
                orientation=relation.orientation,
                arity=relation.arity,
                nominal_transformation_element=relation.nominal_transformation_element,
                rule_set_id=relation.rule_set_id,
                rule_set_version=relation.rule_set_version,
                source_refs=relation.source_refs,
            )
        )
    return tuple(rows)


def build_structural_context(
    natal: BaziChartCandidate,
    flow: BaziFlowCandidate,
    profile: ResolvedBaziStructuralProfile,
) -> BaziStructuralContext:
    profile.validate()
    chart = natal.chart
    temporal_stems, temporal_branches, provenance = materialize_temporal_participants(flow)
    temporal_hidden = generate_hidden_stems(temporal_branches)
    temporal_ten_gods = _temporal_ten_gods(
        chart.day_master_stem,
        temporal_stems,
        temporal_hidden,
    )

    combined_stems = chart.stems + temporal_stems
    combined_branches = chart.branches + temporal_branches
    combined_hidden = chart.hidden_stems + temporal_hidden
    temporal_visible_ids = {
        row.instance_id for row in temporal_stems + temporal_branches
    }
    temporal_hidden_ids = {row.instance_id for row in temporal_hidden}

    dynamic_exposures = tuple(
        row
        for row in generate_exposures(combined_stems, combined_hidden)
        if row.visible_stem_instance_id in temporal_visible_ids
        or row.hidden_stem_instance_id in temporal_hidden_ids
    )
    dynamic_affinities = tuple(
        row
        for row in generate_affinities(combined_stems, combined_branches, combined_hidden)
        if row.visible_stem_instance_id in temporal_visible_ids
        or row.branch_instance_id in temporal_visible_ids
    )

    layer_by_instance = {
        **{row.instance_id: "NATAL" for row in chart.stems + chart.branches},
        **{row.instance_id: row.layer for row in provenance},
    }
    dynamic_relations = _dynamic_relation_occurrences(
        generate_raw_relations(combined_stems, combined_branches),
        layer_by_instance,
    )

    return BaziStructuralContext(
        upstream_natal_fact_hash=natal.hashes.fact_hash,
        upstream_temporal_fact_hash=flow.context.upstream_temporal_fact_hash,
        upstream_flow_fact_hash=flow.hashes.fact_hash,
        natal_day_master_stem=chart.day_master_stem,
        natal_stem_instance_ids=tuple(row.instance_id for row in chart.stems),
        natal_branch_instance_ids=tuple(row.instance_id for row in chart.branches),
        active_temporal_stems=temporal_stems,
        active_temporal_branches=temporal_branches,
        temporal_participant_provenance=provenance,
        temporal_hidden_stems=temporal_hidden,
        temporal_ten_gods=temporal_ten_gods,
        upstream_natal_exposure_link_ids=tuple(sorted(row.link_id for row in chart.exposures)),
        dynamic_exposures=dynamic_exposures,
        upstream_natal_affinity_fact_ids=tuple(sorted(row.fact_id for row in chart.affinities)),
        dynamic_affinities=dynamic_affinities,
        upstream_natal_raw_relation_ids=tuple(sorted(row.relation_id for row in chart.raw_relations)),
        dynamic_raw_relations=dynamic_relations,
        profile_id=profile.profile_id,
        profile_version=profile.profile_version,
        algorithm_versions={
            "structural": profile.algorithm_version,
            "participant_materialization": PARTICIPANT_RULE_SET_VERSION,
            "hidden_stems": HIDDEN_STEM_ALGORITHM_VERSION,
            "ten_gods": TEN_GOD_ALGORITHM_VERSION,
            "affinity": AFFINITY_ALGORITHM_VERSION,
            "raw_relations": RAW_RELATION_ALGORITHM_VERSION,
            "relation_scope": RELATION_SCOPE_RULE_SET_VERSION,
        },
    )
