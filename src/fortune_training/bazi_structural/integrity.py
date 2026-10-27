from __future__ import annotations

from typing import Any

from fortune_training.bazi_chart import BaziChartCandidate
from fortune_training.bazi_chart.registries import BRANCH_ELEMENTS, STEM_ELEMENTS, STEM_POLARITY
from fortune_training.bazi_flow import BaziFlowCandidate
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .generation import build_structural_context
from .models import (
    BaziStructuralContext,
    StructuralHashBundle,
    StructuralIntegrityDiagnostic,
    StructuralIntegrityReport,
)
from .profile import ResolvedBaziStructuralProfile


INTEGRITY_ALGORITHM_ID = "BAZI-STRUCTURAL-INTEGRITY-V1"
INTEGRITY_ALGORITHM_VERSION = "1.0.0"
HASH_ALGORITHM_ID = "BAZI-STRUCTURAL-HASH-V1"
HASH_ALGORITHM_VERSION = "1.0.0"


def _diag(rows, code: str, path: str, detail: str) -> None:
    rows.append(StructuralIntegrityDiagnostic(code=code, path=path, detail=detail))


def structural_fact_projection(context: BaziStructuralContext) -> dict[str, Any]:
    return {
        "upstream_natal_fact_hash": context.upstream_natal_fact_hash,
        "upstream_temporal_fact_hash": context.upstream_temporal_fact_hash,
        "upstream_flow_fact_hash": context.upstream_flow_fact_hash,
        "natal_day_master_stem": context.natal_day_master_stem,
        "natal_stem_instance_ids": sorted(context.natal_stem_instance_ids),
        "natal_branch_instance_ids": sorted(context.natal_branch_instance_ids),
        "active_temporal_stems": [
            {
                "instance_id": row.instance_id,
                "position": row.position,
                "stem": row.stem,
                "element": row.element,
                "polarity": row.polarity,
            }
            for row in context.active_temporal_stems
        ],
        "active_temporal_branches": [
            {
                "instance_id": row.instance_id,
                "position": row.position,
                "branch": row.branch,
                "element_affiliation": row.element_affiliation,
            }
            for row in context.active_temporal_branches
        ],
        "temporal_participant_provenance": [
            {
                "instance_id": row.instance_id,
                "layer": row.layer,
                "source_frame_id": row.source_frame_id,
                "source_flow_fact_hash": row.source_flow_fact_hash,
                "source_ganzhi": row.source_ganzhi,
            }
            for row in context.temporal_participant_provenance
        ],
        "temporal_hidden_stems": [
            {
                "instance_id": row.instance_id,
                "branch_instance_id": row.branch_instance_id,
                "branch_position": row.branch_position,
                "stem": row.stem,
                "element": row.element,
                "registry_ordinal": row.registry_ordinal,
            }
            for row in context.temporal_hidden_stems
        ],
        "temporal_ten_gods": [
            {
                "binding_id": row.binding_id,
                "target_instance_id": row.target_instance_id,
                "target_stem": row.target_stem,
                "day_master_stem": row.day_master_stem,
                "semantic_role_id": row.semantic_role_id,
                "display_name": row.display_name,
            }
            for row in context.temporal_ten_gods
        ],
        "upstream_natal_exposure_link_ids": sorted(context.upstream_natal_exposure_link_ids),
        "dynamic_exposures": [
            {
                "link_id": row.link_id,
                "hidden_stem_instance_id": row.hidden_stem_instance_id,
                "visible_stem_instance_id": row.visible_stem_instance_id,
                "stem": row.stem,
                "match_kind": row.match_kind,
            }
            for row in context.dynamic_exposures
        ],
        "upstream_natal_affinity_fact_ids": sorted(context.upstream_natal_affinity_fact_ids),
        "dynamic_affinities": [
            {
                "fact_id": row.fact_id,
                "visible_stem_instance_id": row.visible_stem_instance_id,
                "branch_instance_id": row.branch_instance_id,
                "exact_hidden_stem_instance_ids": sorted(row.exact_hidden_stem_instance_ids),
                "same_element_hidden_stem_instance_ids": sorted(row.same_element_hidden_stem_instance_ids),
            }
            for row in context.dynamic_affinities
        ],
        "upstream_natal_raw_relation_ids": sorted(context.upstream_natal_raw_relation_ids),
        "dynamic_raw_relations": [
            {
                "relation_id": row.relation_id,
                "semantic_relation_id": row.semantic_relation_id,
                "relation_family": row.relation_family,
                "participant_instance_ids": list(row.participant_instance_ids),
                "participant_layers": list(row.participant_layers),
                "relation_scope": row.relation_scope,
                "orientation": row.orientation,
                "arity": row.arity,
                "nominal_transformation_element": row.nominal_transformation_element,
            }
            for row in context.dynamic_raw_relations
        ],
    }


def structural_hash_bundle(
    context: BaziStructuralContext,
    natal: BaziChartCandidate,
    flow: BaziFlowCandidate,
    profile: ResolvedBaziStructuralProfile,
) -> StructuralHashBundle:
    fact_hash = object_sha256(structural_fact_projection(context))
    generated_rows = (
        context.temporal_hidden_stems
        + context.temporal_ten_gods
        + context.dynamic_exposures
        + context.dynamic_affinities
        + context.dynamic_raw_relations
    )
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "upstream_natal_computation_hash": natal.hashes.computation_hash,
            "upstream_flow_computation_hash": flow.hashes.computation_hash,
            "resolved_structural_profile": json_value(profile),
            "algorithm_versions": dict(sorted(context.algorithm_versions.items())),
            "registry_and_source_lineage": [
                {
                    "rule_set_id": getattr(row, "rule_set_id", None),
                    "rule_set_version": getattr(row, "rule_set_version", None),
                    "source_refs": sorted(getattr(row, "source_refs", ())),
                }
                for row in generated_rows
            ],
            "hash_algorithm": f"{HASH_ALGORITHM_ID}@{HASH_ALGORITHM_VERSION}",
        }
    )
    return StructuralHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=HASH_ALGORITHM_ID,
        algorithm_version=HASH_ALGORITHM_VERSION,
    )


def validate_structural_context(
    context: BaziStructuralContext,
    natal: BaziChartCandidate,
    flow: BaziFlowCandidate,
    profile: ResolvedBaziStructuralProfile,
    hashes: StructuralHashBundle | None = None,
) -> StructuralIntegrityReport:
    diagnostics: list[StructuralIntegrityDiagnostic] = []
    try:
        profile.validate()
    except ValueError as exc:
        _diag(diagnostics, "PROFILE_INVALID", "profile", str(exc))

    if context.upstream_natal_fact_hash != natal.hashes.fact_hash:
        _diag(diagnostics, "UPSTREAM_NATAL_HASH_MISMATCH", "upstream_natal_fact_hash", context.upstream_natal_fact_hash)
    if context.upstream_temporal_fact_hash != flow.context.upstream_temporal_fact_hash:
        _diag(diagnostics, "UPSTREAM_TEMPORAL_HASH_MISMATCH", "upstream_temporal_fact_hash", context.upstream_temporal_fact_hash)
    if context.upstream_flow_fact_hash != flow.hashes.fact_hash:
        _diag(diagnostics, "UPSTREAM_FLOW_HASH_MISMATCH", "upstream_flow_fact_hash", context.upstream_flow_fact_hash)
    if (context.profile_id, context.profile_version) != (profile.profile_id, profile.profile_version):
        _diag(diagnostics, "STRUCTURAL_PROFILE_BINDING_MISMATCH", "profile_id", context.profile_id)

    expected = build_structural_context(natal, flow, profile)
    if context.natal_day_master_stem != natal.chart.day_master_stem:
        _diag(diagnostics, "NATAL_DAY_MASTER_MISMATCH", "natal_day_master_stem", context.natal_day_master_stem)
    if context.natal_stem_instance_ids != expected.natal_stem_instance_ids:
        _diag(diagnostics, "NATAL_STEM_REFS_MISMATCH", "natal_stem_instance_ids", "Natal participant references changed")
    if context.natal_branch_instance_ids != expected.natal_branch_instance_ids:
        _diag(diagnostics, "NATAL_BRANCH_REFS_MISMATCH", "natal_branch_instance_ids", "Natal participant references changed")
    if dict(context.algorithm_versions) != dict(expected.algorithm_versions):
        _diag(diagnostics, "STRUCTURAL_ALGORITHM_VERSION_MISMATCH", "algorithm_versions", str(dict(context.algorithm_versions)))
    if (
        context.active_temporal_stems,
        context.active_temporal_branches,
        context.temporal_participant_provenance,
    ) != (
        expected.active_temporal_stems,
        expected.active_temporal_branches,
        expected.temporal_participant_provenance,
    ):
        _diag(diagnostics, "TEMPORAL_PARTICIPANT_REPLAY_MISMATCH", "active_temporal_participants", "active Flow frames do not replay")
    if flow.context.active_dayun_kind == "PRE_DAYUN" and any(
        row.layer == "DAYUN" for row in context.temporal_participant_provenance
    ):
        _diag(diagnostics, "PRE_DAYUN_FAKE_PARTICIPANT", "temporal_participant_provenance", "PRE_DAYUN cannot materialize Ganzhi")

    for index, row in enumerate(context.active_temporal_stems):
        if row.element != STEM_ELEMENTS.get(row.stem) or row.polarity != STEM_POLARITY.get(row.stem):
            _diag(diagnostics, "TEMPORAL_STEM_REGISTRY_MISMATCH", f"active_temporal_stems[{index}]", row.instance_id)
    for index, row in enumerate(context.active_temporal_branches):
        if row.element_affiliation != BRANCH_ELEMENTS.get(row.branch):
            _diag(diagnostics, "TEMPORAL_BRANCH_REGISTRY_MISMATCH", f"active_temporal_branches[{index}]", row.instance_id)

    checks = (
        ("TEMPORAL_HIDDEN_STEM_REPLAY_MISMATCH", "temporal_hidden_stems"),
        ("TEMPORAL_TEN_GOD_REPLAY_MISMATCH", "temporal_ten_gods"),
        ("DYNAMIC_EXPOSURE_REPLAY_MISMATCH", "dynamic_exposures"),
        ("DYNAMIC_AFFINITY_REPLAY_MISMATCH", "dynamic_affinities"),
        ("DYNAMIC_RELATION_REPLAY_MISMATCH", "dynamic_raw_relations"),
    )
    for code, field in checks:
        if getattr(context, field) != getattr(expected, field):
            _diag(diagnostics, code, field, "shared primitive replay mismatch")

    upstream_checks = (
        ("UPSTREAM_NATAL_EXPOSURE_REFS_MISMATCH", "upstream_natal_exposure_link_ids"),
        ("UPSTREAM_NATAL_AFFINITY_REFS_MISMATCH", "upstream_natal_affinity_fact_ids"),
        ("UPSTREAM_NATAL_RELATION_REFS_MISMATCH", "upstream_natal_raw_relation_ids"),
    )
    for code, field in upstream_checks:
        if getattr(context, field) != getattr(expected, field):
            _diag(diagnostics, code, field, "Natal upstream reference mismatch")

    natal_ids = set(context.natal_stem_instance_ids + context.natal_branch_instance_ids)
    temporal_ids = {
        row.instance_id
        for row in context.active_temporal_stems + context.active_temporal_branches
    }
    known_ids = natal_ids | temporal_ids
    seen_relation_ids: set[str] = set()
    for index, row in enumerate(context.dynamic_raw_relations):
        path = f"dynamic_raw_relations[{index}]"
        participants = set(row.participant_instance_ids)
        if not participants <= known_ids:
            _diag(diagnostics, "RELATION_PARTICIPANT_MISSING", path, row.relation_id)
        if participants <= natal_ids:
            _diag(diagnostics, "NATAL_ONLY_RELATION_DUPLICATED", path, row.relation_id)
        if row.arity != len(row.participant_instance_ids) or row.arity not in (2, 3):
            _diag(diagnostics, "RELATION_ARITY_INVALID", path, str(row.arity))
        if row.orientation not in {"SYMMETRIC", "DIRECTED", "SELF", "GROUP"}:
            _diag(diagnostics, "RELATION_ORIENTATION_INVALID", path, row.orientation)
        if row.relation_id in seen_relation_ids:
            _diag(diagnostics, "DUPLICATE_DYNAMIC_RELATION", path, row.relation_id)
        seen_relation_ids.add(row.relation_id)

    if hashes is not None:
        expected_hashes = structural_hash_bundle(context, natal, flow, profile)
        if hashes != expected_hashes:
            _diag(diagnostics, "STRUCTURAL_HASH_REPLAY_MISMATCH", "hashes", hashes.fact_hash)

    return StructuralIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=INTEGRITY_ALGORITHM_ID,
        algorithm_version=INTEGRITY_ALGORITHM_VERSION,
    )
