from __future__ import annotations

from typing import Any, TYPE_CHECKING

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .hidden_stems import generate_affinities, generate_exposures, generate_hidden_stems
from .models import BaziNatalState, HashBundle, IntegrityDiagnostic, IntegrityReport
from .registries import HIDDEN_STEMS, PILLAR_POSITIONS, sexagenary_index
from .relations import generate_raw_relations
from .ten_gods import ten_god

if TYPE_CHECKING:
    from .profile import ResolvedBaziCalculationProfile


INTEGRITY_ALGORITHM_ID = "BAZI-NATAL-INTEGRITY-V1"
INTEGRITY_ALGORITHM_VERSION = "1.0.0"
HASH_ALGORITHM_ID = "BAZI-NATAL-HASH-V1"
HASH_ALGORITHM_VERSION = "1.0.1"


def _diag(rows: list[IntegrityDiagnostic], code: str, path: str, detail: str) -> None:
    rows.append(IntegrityDiagnostic(code=code, path=path, detail=detail))


def _require_refs(rows: list[IntegrityDiagnostic], refs: tuple[str, ...], path: str) -> None:
    if not refs or any(not str(ref).strip() for ref in refs):
        _diag(rows, "MISSING_PROVENANCE", path, "source_refs must be non-empty")


def validate_natal_state(chart: BaziNatalState) -> IntegrityReport:
    diagnostics: list[IntegrityDiagnostic] = []

    if tuple(row.position for row in chart.pillars) != PILLAR_POSITIONS:
        _diag(diagnostics, "INVALID_PILLAR_ORDER", "pillars", str(tuple(row.position for row in chart.pillars)))
    if len(chart.stems) != 4 or len({row.instance_id for row in chart.stems}) != 4:
        _diag(diagnostics, "INVALID_VISIBLE_STEM_SET", "stems", "expected four unique visible stems")
    if len(chart.branches) != 4 or len({row.instance_id for row in chart.branches}) != 4:
        _diag(diagnostics, "INVALID_BRANCH_SET", "branches", "expected four unique branch instances")

    stems = {row.instance_id: row for row in chart.stems}
    branches = {row.instance_id: row for row in chart.branches}
    for index, pillar in enumerate(chart.pillars):
        try:
            expected_index = sexagenary_index(pillar.ganzhi)
        except ValueError as exc:
            _diag(diagnostics, "INVALID_SEXAGENARY_IDENTITY", f"pillars[{index}].ganzhi", str(exc))
            continue
        if pillar.sexagenary_index != expected_index:
            _diag(diagnostics, "SEXAGENARY_INDEX_MISMATCH", f"pillars[{index}]", pillar.ganzhi)
        stem = stems.get(pillar.stem_instance_id)
        branch = branches.get(pillar.branch_instance_id)
        if stem is None or branch is None:
            _diag(diagnostics, "PILLAR_INSTANCE_LINK_MISSING", f"pillars[{index}]", pillar.ganzhi)
        elif stem.stem + branch.branch != pillar.ganzhi:
            _diag(diagnostics, "PILLAR_INSTANCE_LINK_MISMATCH", f"pillars[{index}]", pillar.ganzhi)

    day_stems = [row for row in chart.stems if row.position == "DAY"]
    if len(day_stems) != 1 or chart.day_master_stem != day_stems[0].stem:
        _diag(diagnostics, "DAY_MASTER_MISMATCH", "day_master_stem", chart.day_master_stem)

    expected_hidden = generate_hidden_stems(chart.branches)
    if chart.hidden_stems != expected_hidden:
        _diag(diagnostics, "HIDDEN_STEM_MEMBERSHIP_MISMATCH", "hidden_stems", "registry replay mismatch")
    for index, row in enumerate(chart.hidden_stems):
        _require_refs(diagnostics, row.source_refs, f"hidden_stems[{index}].source_refs")
        branch = branches.get(row.branch_instance_id)
        if branch is None or row.stem not in HIDDEN_STEMS.get(branch.branch, ()):
            _diag(diagnostics, "INVALID_HIDDEN_STEM_BINDING", f"hidden_stems[{index}]", row.instance_id)

    target_stems = {row.instance_id: row.stem for row in chart.stems}
    target_stems.update({row.instance_id: row.stem for row in chart.hidden_stems})
    seen_ten_gods: set[str] = set()
    for index, row in enumerate(chart.ten_gods):
        _require_refs(diagnostics, row.source_refs, f"ten_gods[{index}].source_refs")
        target = target_stems.get(row.target_instance_id)
        if target is None:
            _diag(diagnostics, "TEN_GOD_TARGET_MISSING", f"ten_gods[{index}]", row.target_instance_id)
            continue
        semantic, display = ten_god(chart.day_master_stem, target)
        if (
            row.target_stem != target
            or row.day_master_stem != chart.day_master_stem
            or row.semantic_role_id != semantic
            or row.display_name != display
        ):
            _diag(diagnostics, "TEN_GOD_BINDING_MISMATCH", f"ten_gods[{index}]", row.binding_id)
        if row.target_instance_id in seen_ten_gods:
            _diag(diagnostics, "DUPLICATE_TEN_GOD_TARGET", f"ten_gods[{index}]", row.target_instance_id)
        seen_ten_gods.add(row.target_instance_id)
    if seen_ten_gods != set(target_stems):
        _diag(diagnostics, "INCOMPLETE_TEN_GOD_BINDINGS", "ten_gods", "every visible/hidden stem needs one binding")

    expected_exposures = generate_exposures(chart.stems, chart.hidden_stems)
    if chart.exposures != expected_exposures:
        _diag(diagnostics, "EXPOSURE_REPLAY_MISMATCH", "exposures", "exposure links do not replay")
    for index, row in enumerate(chart.exposures):
        _require_refs(diagnostics, row.source_refs, f"exposures[{index}].source_refs")

    expected_affinities = generate_affinities(chart.stems, chart.branches, chart.hidden_stems)
    if chart.affinities != expected_affinities:
        _diag(diagnostics, "AFFINITY_REPLAY_MISMATCH", "affinities", "affinity facts do not replay")
    if len(chart.affinities) != 16:
        _diag(diagnostics, "AFFINITY_CARDINALITY_MISMATCH", "affinities", str(len(chart.affinities)))
    for index, row in enumerate(chart.affinities):
        _require_refs(diagnostics, row.source_refs, f"affinities[{index}].source_refs")

    expected_relations = generate_raw_relations(chart.stems, chart.branches)
    if chart.raw_relations != expected_relations:
        _diag(diagnostics, "RAW_RELATION_REPLAY_MISMATCH", "raw_relations", "relation graph does not replay")
    all_instance_ids = set(stems) | set(branches)
    for index, row in enumerate(chart.raw_relations):
        _require_refs(diagnostics, row.source_refs, f"raw_relations[{index}].source_refs")
        if row.arity != len(row.participant_instance_ids):
            _diag(diagnostics, "RELATION_ARITY_MISMATCH", f"raw_relations[{index}]", row.relation_id)
        if any(participant not in all_instance_ids for participant in row.participant_instance_ids):
            _diag(diagnostics, "RELATION_PARTICIPANT_MISSING", f"raw_relations[{index}]", row.relation_id)

    for index, row in enumerate(chart.trace):
        _require_refs(diagnostics, row.source_refs, f"trace[{index}].source_refs")
        if not row.algorithm_id or not row.algorithm_version:
            _diag(diagnostics, "MISSING_ALGORITHM_IDENTITY", f"trace[{index}]", row.operation)

    return IntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=INTEGRITY_ALGORITHM_ID,
        algorithm_version=INTEGRITY_ALGORITHM_VERSION,
    )


def natal_fact_projection(chart: BaziNatalState) -> dict[str, Any]:
    return {
        "pillars": [
            {
                "position": row.position,
                "ganzhi": row.ganzhi,
                "sexagenary_index": row.sexagenary_index,
                "stem_instance_id": row.stem_instance_id,
                "branch_instance_id": row.branch_instance_id,
            }
            for row in chart.pillars
        ],
        "stems": [
            {
                "instance_id": row.instance_id,
                "position": row.position,
                "stem": row.stem,
                "element": row.element,
                "polarity": row.polarity,
            }
            for row in chart.stems
        ],
        "branches": [
            {
                "instance_id": row.instance_id,
                "position": row.position,
                "branch": row.branch,
                "element_affiliation": row.element_affiliation,
            }
            for row in chart.branches
        ],
        # Hidden-stem membership is a fact; registry/display order is lineage.
        "hidden_stems": [
            {
                "instance_id": row.instance_id,
                "branch_instance_id": row.branch_instance_id,
                "stem": row.stem,
                "element": row.element,
            }
            for row in sorted(chart.hidden_stems, key=lambda item: item.instance_id)
        ],
        "ten_gods": [
            {
                "target_instance_id": row.target_instance_id,
                "target_stem": row.target_stem,
                "day_master_stem": row.day_master_stem,
                "semantic_role_id": row.semantic_role_id,
            }
            for row in sorted(chart.ten_gods, key=lambda item: item.target_instance_id)
        ],
        "exposures": [
            {
                "hidden_stem_instance_id": row.hidden_stem_instance_id,
                "visible_stem_instance_id": row.visible_stem_instance_id,
                "stem": row.stem,
                "match_kind": row.match_kind,
            }
            for row in chart.exposures
        ],
        "affinities": [
            {
                "visible_stem_instance_id": row.visible_stem_instance_id,
                "branch_instance_id": row.branch_instance_id,
                "exact_hidden_stem_instance_ids": list(row.exact_hidden_stem_instance_ids),
                "same_element_hidden_stem_instance_ids": list(row.same_element_hidden_stem_instance_ids),
            }
            for row in chart.affinities
        ],
        "raw_relations": [
            {
                "semantic_relation_id": row.semantic_relation_id,
                "relation_family": row.relation_family,
                "participant_instance_ids": list(row.participant_instance_ids),
                "orientation": row.orientation,
                "arity": row.arity,
                "nominal_transformation_element": row.nominal_transformation_element,
            }
            for row in chart.raw_relations
        ],
        "day_master_stem": chart.day_master_stem,
    }


def _lineage_projection(chart: BaziNatalState) -> dict[str, Any]:
    return {
        "profile_id": chart.profile_id,
        "profile_version": chart.profile_version,
        "algorithm_versions": dict(sorted(chart.algorithm_versions.items())),
        "trace": [
            {
                "operation": row.operation,
                "algorithm_id": row.algorithm_id,
                "algorithm_version": row.algorithm_version,
                "source_refs": sorted(row.source_refs),
            }
            for row in chart.trace
        ],
        "hidden_stem_registry_order": [
            {
                "instance_id": row.instance_id,
                "registry_ordinal": row.registry_ordinal,
                "rule_set_id": row.rule_set_id,
                "rule_set_version": row.rule_set_version,
            }
            for row in chart.hidden_stems
        ],
        "hidden_stem_sources": sorted({ref for row in chart.hidden_stems for ref in row.source_refs}),
        "ten_god_sources": sorted({ref for row in chart.ten_gods for ref in row.source_refs}),
        "relation_sources": sorted({ref for row in chart.raw_relations for ref in row.source_refs}),
    }


def natal_hash_bundle(
    chart: BaziNatalState,
    profile: "ResolvedBaziCalculationProfile",
) -> HashBundle:
    fact_hash = object_sha256(natal_fact_projection(chart))
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "resolved_profile": json_value(profile),
            "lineage": _lineage_projection(chart),
            "hash_algorithm": f"{HASH_ALGORITHM_ID}@{HASH_ALGORITHM_VERSION}",
        }
    )
    return HashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=HASH_ALGORITHM_ID,
        algorithm_version=HASH_ALGORITHM_VERSION,
    )
