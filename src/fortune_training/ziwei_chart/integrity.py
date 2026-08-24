from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .models import (
    NatalChartState,
    TemporalAuxiliaryActivation,
    TemporalAuxiliaryCandidateSet,
    TransformationActivation,
)
from .registries import sexagenary_for_year
from .temporal import (
    DOUJUN_RULE_ID,
    ANNUAL_AUXILIARY_SOURCE_REFS,
    DAXIAN_AUXILIARY_SOURCE_REFS,
    LEAP_MONTH_POLICY_STATUS,
    MONTH_GANZHI_RULE_ID,
    MONTHLY_RULE_ID,
    MONTHLY_AUXILIARY_SOURCE_REFS,
    REGULAR_MONTH_CALENDAR_SCOPE,
    TemporalNatalContext,
    ZiweiTemporalEngine,
    ZiweiTemporalState,
)
from .temporal_auxiliary import TemporalAuxiliaryGenerator

if TYPE_CHECKING:
    from .profile import ResolvedZiweiCalculationProfile


INTEGRITY_ALGORITHM_ID = "ZIWEI-INTEGRITY-HASH-V1"
INTEGRITY_ALGORITHM_VERSION = "1.0.3"
DIGNITY_GRADES = {"庙", "旺", "得", "利", "平", "不", "陷"}
DIGNITY_STATUSES = {"GRADED", "UNRATED"}


@dataclass(frozen=True)
class IntegrityDiagnostic:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class IntegrityReport:
    status: str
    diagnostics: tuple[IntegrityDiagnostic, ...]
    algorithm_id: str = INTEGRITY_ALGORITHM_ID
    algorithm_version: str = INTEGRITY_ALGORITHM_VERSION


@dataclass(frozen=True)
class HashBundle:
    fact_hash: str
    computation_hash: str
    algorithm_id: str = INTEGRITY_ALGORITHM_ID
    algorithm_version: str = INTEGRITY_ALGORITHM_VERSION


def _address_fact(value) -> dict[str, Any]:
    return {"index": value.index, "branch": value.branch}


def _designation_facts(rows) -> list[dict[str, Any]]:
    return [
        {"designation_id": row.designation_id, "address": _address_fact(row.address)}
        for row in sorted(rows, key=lambda item: item.designation_id)
    ]


def _transformation_fact(row: TransformationActivation) -> dict[str, Any]:
    return {
        "activation_id": row.activation_id,
        "transformation_type": row.transformation_type,
        "target_entity_id": row.target_entity_id,
        "target_address": _address_fact(row.target_address),
        "source_layer": row.source_layer,
        "source_stem": row.source_stem,
        "context_id": row.context_id,
    }


def _temporal_auxiliary_fact(row: TemporalAuxiliaryActivation) -> dict[str, Any]:
    return {
        "activation_id": row.activation_id,
        "entity_id": row.entity_id,
        "target_address": _address_fact(row.target_address),
        "source_layer": row.source_layer,
        "source_stem": row.source_stem,
        "context_id": row.context_id,
    }


def _temporal_auxiliary_candidate_set_fact(
    row: TemporalAuxiliaryCandidateSet,
) -> dict[str, Any]:
    return {
        "candidate_set_id": row.candidate_set_id,
        "source_layer": row.source_layer,
        "source_stem": row.source_stem,
        "context_id": row.context_id,
        "entity_ids": row.entity_ids,
        "selection_status": row.selection_status,
        "method_candidates": [
            {
                "candidate_id": candidate.candidate_id,
                "method_id": candidate.method_id,
                "authority_status": candidate.authority_status,
                "activations": [
                    _temporal_auxiliary_fact(activation)
                    for activation in candidate.activations
                ],
                "fact_hash": candidate.fact_hash,
            }
            for candidate in row.method_candidates
        ],
        "fact_hash": row.fact_hash,
    }


def natal_fact_projection(chart: NatalChartState) -> dict[str, Any]:
    structure = chart.structure
    return {
        "structure": {
            "ziwei_birth_year_stem": structure.ziwei_birth_year_stem,
            "ziwei_birth_year_branch": structure.ziwei_birth_year_branch,
            "raw_lunar_month": structure.raw_lunar_month,
            "natal_month_coordinate": structure.natal_month_coordinate,
            "lunar_birth_day": structure.lunar_birth_day,
            "birth_hour_branch": _address_fact(structure.birth_hour_branch),
            "month_anchor": _address_fact(structure.month_anchor),
            "life_address": _address_fact(structure.life_address),
            "body_address": _address_fact(structure.body_address),
            "designation_bindings": _designation_facts(structure.designation_bindings),
            "address_attributes": [
                {"address": _address_fact(row.address), "stem": row.stem}
                for row in sorted(structure.address_attributes, key=lambda item: item.address.index)
            ],
            "bureau": {
                "element": structure.bureau.element,
                "number": structure.bureau.number,
                "life_palace_ganzhi": structure.bureau.life_palace_ganzhi,
                "nayin_name": structure.bureau.nayin_name,
            },
        },
        "placements": [
            {"entity_id": row.entity_id, "address": _address_fact(row.address)}
            for row in sorted(chart.placements, key=lambda item: item.entity_id)
        ],
        "annotations": [
            {
                "annotation_id": row.annotation_id,
                "annotation_type": row.annotation_type,
                "target_entity_id": row.target_entity_id,
                "target_address": _address_fact(row.target_address),
                "status": row.status,
                "grade": row.grade,
                "scale_id": row.scale_id,
                "scale_version": row.scale_version,
            }
            for row in sorted(chart.annotations, key=lambda item: item.annotation_id)
        ],
        "transformations": [
            _transformation_fact(row)
            for row in sorted(chart.transformations, key=lambda item: item.activation_id)
        ],
        "role_bindings": [
            {
                "role_id": row.role_id,
                "entity_id": row.entity_id,
                "basis_type": row.basis_type,
                "basis_value": row.basis_value,
            }
            for row in sorted(chart.role_bindings, key=lambda item: item.role_id)
        ],
        "rings": [
            {
                "ring_id": ring.ring_id,
                "anchor_address": _address_fact(ring.anchor_address),
                "direction": ring.direction,
                "members": [
                    {
                        "member_id": member.member_id,
                        "address": _address_fact(member.address),
                        "ordinal": member.ordinal,
                    }
                    for member in sorted(ring.members, key=lambda item: item.member_id)
                ],
            }
            for ring in sorted(chart.rings, key=lambda item: item.ring_id)
        ],
    }


def _natal_lineage_projection(chart: NatalChartState) -> dict[str, Any]:
    return {
        "structure_trace": [
            {
                "operation": row.operation,
                "algorithm_id": row.algorithm_id,
                "algorithm_version": row.algorithm_version,
                "source_refs": sorted(row.source_refs),
            }
            for row in chart.structure.trace
        ],
        "placements": [
            {
                "entity_id": row.entity_id,
                "generator_id": row.generator_id,
                "algorithm_version": row.algorithm_version,
                "source_refs": sorted(row.source_refs),
            }
            for row in sorted(chart.placements, key=lambda item: item.entity_id)
        ],
        "annotations": [
            {
                "annotation_id": row.annotation_id,
                "rule_set_id": row.rule_set_id,
                "rule_set_version": row.rule_set_version,
                "generator_id": row.generator_id,
                "algorithm_version": row.algorithm_version,
                "source_refs": sorted(row.source_refs),
            }
            for row in sorted(chart.annotations, key=lambda item: item.annotation_id)
        ],
        "transformations": [
            {
                "activation_id": row.activation_id,
                "assignment_id": row.assignment_id,
                "mechanism_id": row.mechanism_id,
                "generator_id": row.generator_id,
                "algorithm_version": row.algorithm_version,
                "source_refs": sorted(row.source_refs),
            }
            for row in sorted(chart.transformations, key=lambda item: item.activation_id)
        ],
        "roles": [
            {
                "role_id": row.role_id,
                "generator_id": row.generator_id,
                "algorithm_version": row.algorithm_version,
                "source_refs": sorted(row.source_refs),
            }
            for row in sorted(chart.role_bindings, key=lambda item: item.role_id)
        ],
        "rings": [
            {
                "ring_id": ring.ring_id,
                "generator_id": ring.generator_id,
                "algorithm_version": ring.algorithm_version,
                "source_refs": sorted(ring.source_refs),
                "member_source_refs": {
                    member.member_id: sorted(member.source_refs)
                    for member in sorted(ring.members, key=lambda item: item.member_id)
                },
            }
            for ring in sorted(chart.rings, key=lambda item: item.ring_id)
        ],
        "algorithm_versions": dict(sorted(chart.algorithm_versions.items())),
    }


def natal_hash_bundle(chart: NatalChartState, profile: "ResolvedZiweiCalculationProfile") -> HashBundle:
    fact_hash = object_sha256(natal_fact_projection(chart))
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "resolved_profile": json_value(profile),
            "lineage": _natal_lineage_projection(chart),
            "hash_algorithm": f"{INTEGRITY_ALGORITHM_ID}@{INTEGRITY_ALGORITHM_VERSION}",
        }
    )
    return HashBundle(fact_hash=fact_hash, computation_hash=computation_hash)


def temporal_fact_projection(state: ZiweiTemporalState) -> dict[str, Any]:
    return {
        "daxian_direction": state.daxian_direction,
        "first_daxian_nominal_age": state.first_daxian_nominal_age,
        "daxian_frames": [
            {
                "frame_id": frame.frame_id,
                "index": frame.index,
                "nominal_age_start": frame.nominal_age_start,
                "nominal_age_end": frame.nominal_age_end,
                "absolute_year_start": frame.absolute_year_start,
                "absolute_year_end": frame.absolute_year_end,
                "active_address": _address_fact(frame.active_address),
                "active_palace_ganzhi": frame.active_palace_ganzhi,
                "designation_overlay": _designation_facts(frame.designation_overlay),
                "source_stem": frame.source_stem,
                "auxiliary_activations": [
                    _temporal_auxiliary_fact(row)
                    for row in sorted(frame.auxiliary_activations, key=lambda item: item.activation_id)
                ],
                "auxiliary_candidate_sets": [
                    _temporal_auxiliary_candidate_set_fact(row)
                    for row in frame.auxiliary_candidate_sets
                ],
                "transformations": [
                    _transformation_fact(row)
                    for row in sorted(frame.transformations, key=lambda item: item.activation_id)
                ],
            }
            for frame in sorted(state.daxian_frames, key=lambda item: item.index)
        ],
        "annual_frames": [
            {
                "frame_id": frame.frame_id,
                "absolute_year": frame.absolute_year,
                "nominal_age": frame.nominal_age,
                "year_stem": frame.year_stem,
                "year_branch": frame.year_branch,
                "active_address": _address_fact(frame.active_address),
                "active_palace_ganzhi": frame.active_palace_ganzhi,
                "doujun_address": _address_fact(frame.doujun_address),
                "doujun_rule_id": frame.doujun_rule_id,
                "designation_overlay": _designation_facts(frame.designation_overlay),
                "parent_daxian_frame_id": frame.parent_daxian_frame_id,
                "auxiliary_activations": [
                    _temporal_auxiliary_fact(row)
                    for row in sorted(frame.auxiliary_activations, key=lambda item: item.activation_id)
                ],
                "auxiliary_candidate_sets": [
                    _temporal_auxiliary_candidate_set_fact(row)
                    for row in frame.auxiliary_candidate_sets
                ],
                "transformations": [
                    _transformation_fact(row)
                    for row in sorted(frame.transformations, key=lambda item: item.activation_id)
                ],
            }
            for frame in sorted(state.annual_frames, key=lambda item: item.absolute_year)
        ],
        "monthly_frames": [
            {
                "frame_id": frame.frame_id,
                "absolute_year": frame.absolute_year,
                "lunar_month": frame.lunar_month,
                "month_stem": frame.month_stem,
                "month_branch": frame.month_branch,
                "month_ganzhi": frame.month_ganzhi,
                "active_address": _address_fact(frame.active_address),
                "designation_overlay": _designation_facts(frame.designation_overlay),
                "parent_annual_frame_id": frame.parent_annual_frame_id,
                "monthly_rule_id": frame.monthly_rule_id,
                "month_ganzhi_rule_id": frame.month_ganzhi_rule_id,
                "calendar_scope": frame.calendar_scope,
                "leap_month_policy_status": frame.leap_month_policy_status,
                "auxiliary_activations": [
                    _temporal_auxiliary_fact(row)
                    for row in sorted(frame.auxiliary_activations, key=lambda item: item.activation_id)
                ],
                "auxiliary_candidate_sets": [
                    _temporal_auxiliary_candidate_set_fact(row)
                    for row in frame.auxiliary_candidate_sets
                ],
                "transformations": [
                    _transformation_fact(row)
                    for row in sorted(frame.transformations, key=lambda item: item.activation_id)
                ],
            }
            for frame in sorted(state.monthly_frames, key=lambda item: (item.absolute_year, item.lunar_month))
        ],
        "minor_limit_frames": [
            {
                "frame_id": frame.frame_id,
                "nominal_age": frame.nominal_age,
                "active_address": _address_fact(frame.active_address),
            }
            for frame in sorted(state.minor_limit_frames, key=lambda item: item.nominal_age)
        ],
    }


def _temporal_lineage_projection(state: ZiweiTemporalState) -> dict[str, Any]:
    def transformations(rows) -> list[dict[str, Any]]:
        return [
            {
                "activation_id": row.activation_id,
                "assignment_id": row.assignment_id,
                "mechanism_id": row.mechanism_id,
                "generator_id": row.generator_id,
                "algorithm_version": row.algorithm_version,
                "source_refs": sorted(row.source_refs),
            }
            for row in sorted(rows, key=lambda item: item.activation_id)
        ]

    def auxiliaries(rows) -> list[dict[str, Any]]:
        return [
            {
                "activation_id": row.activation_id,
                "rule_id": row.rule_id,
                "generator_id": row.generator_id,
                "algorithm_version": row.algorithm_version,
                "source_refs": sorted(row.source_refs),
            }
            for row in sorted(rows, key=lambda item: item.activation_id)
        ]

    def auxiliary_candidate_sets(rows) -> list[dict[str, Any]]:
        return [
            {
                "candidate_set_id": row.candidate_set_id,
                "source_refs": sorted(row.source_refs),
                "fact_hash": row.fact_hash,
                "computation_hash": row.computation_hash,
                "method_candidates": [
                    {
                        "candidate_id": candidate.candidate_id,
                        "method_id": candidate.method_id,
                        "source_refs": sorted(candidate.source_refs),
                        "fact_hash": candidate.fact_hash,
                        "computation_hash": candidate.computation_hash,
                        "activations": auxiliaries(candidate.activations),
                    }
                    for candidate in row.method_candidates
                ],
            }
            for row in rows
        ]

    return {
        "rule_set_id": state.rule_set_id,
        "rule_set_version": state.rule_set_version,
        "algorithm_id": state.algorithm_id,
        "algorithm_version": state.algorithm_version,
        "daxian": [
            {
                "frame_id": frame.frame_id,
                "source_refs": sorted(frame.source_refs),
                "auxiliary_activations": auxiliaries(frame.auxiliary_activations),
                "auxiliary_candidate_sets": auxiliary_candidate_sets(frame.auxiliary_candidate_sets),
                "transformations": transformations(frame.transformations),
            }
            for frame in sorted(state.daxian_frames, key=lambda item: item.index)
        ],
        "annual": [
            {
                "frame_id": frame.frame_id,
                "source_refs": sorted(frame.source_refs),
                "auxiliary_activations": auxiliaries(frame.auxiliary_activations),
                "auxiliary_candidate_sets": auxiliary_candidate_sets(frame.auxiliary_candidate_sets),
                "transformations": transformations(frame.transformations),
            }
            for frame in sorted(state.annual_frames, key=lambda item: item.absolute_year)
        ],
        "monthly": [
            {
                "frame_id": frame.frame_id,
                "source_refs": sorted(frame.source_refs),
                "auxiliary_activations": auxiliaries(frame.auxiliary_activations),
                "auxiliary_candidate_sets": auxiliary_candidate_sets(frame.auxiliary_candidate_sets),
                "transformations": transformations(frame.transformations),
            }
            for frame in sorted(state.monthly_frames, key=lambda item: (item.absolute_year, item.lunar_month))
        ],
        "minor": [
            {"frame_id": frame.frame_id, "source_refs": sorted(frame.source_refs)}
            for frame in sorted(state.minor_limit_frames, key=lambda item: item.nominal_age)
        ],
    }


def temporal_hash_bundle(state: ZiweiTemporalState, profile: "ResolvedZiweiCalculationProfile") -> HashBundle:
    fact_hash = object_sha256(temporal_fact_projection(state))
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "resolved_profile": json_value(profile),
            "lineage": _temporal_lineage_projection(state),
            "hash_algorithm": f"{INTEGRITY_ALGORITHM_ID}@{INTEGRITY_ALGORITHM_VERSION}",
        }
    )
    return HashBundle(fact_hash=fact_hash, computation_hash=computation_hash)


def _diag(diagnostics: list[IntegrityDiagnostic], code: str, path: str, detail: str) -> None:
    diagnostics.append(IntegrityDiagnostic(code=code, path=path, detail=detail))


def _validate_source_refs(diagnostics: list[IntegrityDiagnostic], refs, path: str) -> None:
    if not refs or any(not str(ref).strip() for ref in refs):
        _diag(diagnostics, "MISSING_PROVENANCE", path, "source_refs must contain stable non-empty identities")


def validate_natal_chart(chart: NatalChartState) -> IntegrityReport:
    diagnostics: list[IntegrityDiagnostic] = []
    structure = chart.structure

    designations = structure.designation_bindings
    if len(designations) != 12 or len({row.designation_id for row in designations}) != 12:
        _diag(diagnostics, "INVALID_DESIGNATION_SET", "structure.designation_bindings", "expected 12 unique designation IDs")
    if len({row.address.index for row in designations}) != 12:
        _diag(diagnostics, "INVALID_DESIGNATION_TOPOLOGY", "structure.designation_bindings", "designations must cover all 12 addresses exactly once")

    attributes = structure.address_attributes
    if len(attributes) != 12 or len({row.address.index for row in attributes}) != 12:
        _diag(diagnostics, "INVALID_ADDRESS_STEM_SET", "structure.address_attributes", "expected exactly one stem for each Z12 address")
    stems = {row.address.index: row.stem for row in attributes}
    life_stem = stems.get(structure.life_address.index)
    expected_life_ganzhi = f"{life_stem}{structure.life_address.branch}" if life_stem else None
    if expected_life_ganzhi != structure.bureau.life_palace_ganzhi:
        _diag(diagnostics, "BUREAU_LINEAGE_MISMATCH", "structure.bureau.life_palace_ganzhi", f"expected {expected_life_ganzhi!r}")

    for index, step in enumerate(structure.trace):
        _validate_source_refs(diagnostics, step.source_refs, f"structure.trace[{index}].source_refs")
        if not step.algorithm_id or not step.algorithm_version:
            _diag(diagnostics, "MISSING_ALGORITHM_IDENTITY", f"structure.trace[{index}]", "algorithm id/version must be non-empty")

    placement_by_entity = {}
    for index, row in enumerate(chart.placements):
        if row.entity_id in placement_by_entity:
            _diag(diagnostics, "DUPLICATE_PLACEMENT_ENTITY", f"placements[{index}]", row.entity_id)
        placement_by_entity[row.entity_id] = row
        _validate_source_refs(diagnostics, row.source_refs, f"placements[{index}].source_refs")
        if not row.generator_id or not row.algorithm_version:
            _diag(diagnostics, "MISSING_ALGORITHM_IDENTITY", f"placements[{index}]", row.entity_id)

    annotation_ids: set[str] = set()
    dignity_targets: set[str] = set()
    for index, row in enumerate(chart.annotations):
        if row.annotation_id in annotation_ids:
            _diag(diagnostics, "DUPLICATE_ANNOTATION_ID", f"annotations[{index}]", row.annotation_id)
        annotation_ids.add(row.annotation_id)
        if row.annotation_type != "DIGNITY":
            _diag(diagnostics, "UNSUPPORTED_ANNOTATION_TYPE", f"annotations[{index}].annotation_type", row.annotation_type)
        if row.target_entity_id in dignity_targets:
            _diag(diagnostics, "DUPLICATE_DIGNITY_TARGET", f"annotations[{index}]", row.target_entity_id)
        dignity_targets.add(row.target_entity_id)
        target = placement_by_entity.get(row.target_entity_id)
        if target is None:
            _diag(diagnostics, "ANNOTATION_TARGET_MISSING", f"annotations[{index}]", row.target_entity_id)
        elif target.address != row.target_address:
            _diag(diagnostics, "ANNOTATION_TARGET_ADDRESS_MISMATCH", f"annotations[{index}].target_address", row.target_entity_id)
        if row.status not in DIGNITY_STATUSES:
            _diag(diagnostics, "INVALID_DIGNITY_STATUS", f"annotations[{index}].status", row.status)
        elif row.status == "GRADED":
            if row.grade not in DIGNITY_GRADES:
                _diag(diagnostics, "INVALID_DIGNITY_GRADE", f"annotations[{index}].grade", str(row.grade))
        elif row.grade is not None:
            _diag(diagnostics, "UNRATED_DIGNITY_MUST_NOT_HAVE_GRADE", f"annotations[{index}].grade", str(row.grade))
        if not row.scale_id or not row.scale_version or not row.rule_set_id or not row.rule_set_version:
            _diag(diagnostics, "MISSING_DIGNITY_IDENTITY", f"annotations[{index}]", row.annotation_id)
        if not row.generator_id or not row.algorithm_version:
            _diag(diagnostics, "MISSING_ALGORITHM_IDENTITY", f"annotations[{index}]", row.annotation_id)
        _validate_source_refs(diagnostics, row.source_refs, f"annotations[{index}].source_refs")

    activation_ids: set[str] = set()
    for index, row in enumerate(chart.transformations):
        if row.activation_id in activation_ids:
            _diag(diagnostics, "DUPLICATE_TRANSFORMATION_ACTIVATION", f"transformations[{index}]", row.activation_id)
        activation_ids.add(row.activation_id)
        target = placement_by_entity.get(row.target_entity_id)
        if target is None:
            _diag(diagnostics, "TRANSFORMATION_TARGET_MISSING", f"transformations[{index}]", row.target_entity_id)
        elif target.address != row.target_address:
            _diag(diagnostics, "TRANSFORMATION_TARGET_ADDRESS_MISMATCH", f"transformations[{index}].target_address", row.target_entity_id)
        if row.transformation_type not in {"化禄", "化权", "化科", "化忌"}:
            _diag(diagnostics, "INVALID_TRANSFORMATION_TYPE", f"transformations[{index}].transformation_type", row.transformation_type)
        _validate_source_refs(diagnostics, row.source_refs, f"transformations[{index}].source_refs")

    role_ids: set[str] = set()
    for index, row in enumerate(chart.role_bindings):
        if row.role_id in role_ids:
            _diag(diagnostics, "DUPLICATE_ROLE_ID", f"role_bindings[{index}]", row.role_id)
        role_ids.add(row.role_id)
        _validate_source_refs(diagnostics, row.source_refs, f"role_bindings[{index}].source_refs")

    ring_ids: set[str] = set()
    for ring_index, ring in enumerate(chart.rings):
        if ring.ring_id in ring_ids:
            _diag(diagnostics, "DUPLICATE_RING_ID", f"rings[{ring_index}]", ring.ring_id)
        ring_ids.add(ring.ring_id)
        _validate_source_refs(diagnostics, ring.source_refs, f"rings[{ring_index}].source_refs")
        if len(ring.members) != 12:
            _diag(diagnostics, "INVALID_RING_CARDINALITY", f"rings[{ring_index}].members", f"expected 12, got {len(ring.members)}")
        if len({member.member_id for member in ring.members}) != len(ring.members):
            _diag(diagnostics, "DUPLICATE_RING_MEMBER_ID", f"rings[{ring_index}].members", ring.ring_id)
        if {member.ordinal for member in ring.members} != set(range(12)):
            _diag(diagnostics, "INVALID_RING_ORDINALS", f"rings[{ring_index}].members", ring.ring_id)
        if len({member.address.index for member in ring.members}) != len(ring.members):
            _diag(diagnostics, "INVALID_RING_TOPOLOGY", f"rings[{ring_index}].members", ring.ring_id)
        ordinal_zero = next((member for member in ring.members if member.ordinal == 0), None)
        if ordinal_zero is None or ordinal_zero.address != ring.anchor_address:
            _diag(diagnostics, "RING_ANCHOR_MISMATCH", f"rings[{ring_index}].anchor_address", ring.ring_id)
        for member_index, member in enumerate(ring.members):
            _validate_source_refs(diagnostics, member.source_refs, f"rings[{ring_index}].members[{member_index}].source_refs")

    if any(not str(value).strip() for value in chart.algorithm_versions.values()):
        _diag(diagnostics, "EMPTY_ALGORITHM_VERSION", "algorithm_versions", "all declared algorithm versions must be non-empty")

    return IntegrityReport(status="PASS" if not diagnostics else "FAIL", diagnostics=tuple(diagnostics))


def validate_temporal_state(
    state: ZiweiTemporalState,
    context: TemporalNatalContext,
) -> IntegrityReport:
    diagnostics: list[IntegrityDiagnostic] = []
    natal_by_entity = {row.entity_id: row for row in context.placements}

    def validate_overlay(rows, path: str) -> None:
        if len(rows) != 12 or len({row.designation_id for row in rows}) != 12:
            _diag(diagnostics, "INVALID_TEMPORAL_DESIGNATION_SET", path, "expected 12 unique designations")
        if len({row.address.index for row in rows}) != 12:
            _diag(diagnostics, "INVALID_TEMPORAL_DESIGNATION_TOPOLOGY", path, "expected all 12 addresses")

    def validate_transformations(rows, path: str) -> None:
        ids: set[str] = set()
        for index, row in enumerate(rows):
            if row.activation_id in ids:
                _diag(diagnostics, "DUPLICATE_TEMPORAL_TRANSFORMATION", f"{path}[{index}]", row.activation_id)
            ids.add(row.activation_id)
            target = natal_by_entity.get(row.target_entity_id)
            if target is None:
                _diag(diagnostics, "TEMPORAL_TRANSFORMATION_TARGET_MISSING", f"{path}[{index}]", row.target_entity_id)
            elif target.address != row.target_address:
                _diag(diagnostics, "TEMPORAL_TRANSFORMATION_MOVED_PHYSICAL_STAR", f"{path}[{index}]", row.target_entity_id)
            _validate_source_refs(diagnostics, row.source_refs, f"{path}[{index}].source_refs")

    def validate_auxiliaries(
        rows,
        *,
        source_stem: str,
        source_layer: str,
        context_id: str,
        temporal_source_refs: tuple[str, ...],
        path: str,
    ) -> None:
        expected = TemporalAuxiliaryGenerator.activate(
            source_stem,
            source_layer=source_layer,
            context_id=context_id,
            temporal_source_refs=temporal_source_refs,
        )
        if tuple(rows) != expected:
            _diag(diagnostics, "TEMPORAL_AUXILIARY_REPLAY_MISMATCH", path, context_id)
        if len(rows) != 5 or len({row.activation_id for row in rows}) != 5:
            _diag(diagnostics, "INVALID_TEMPORAL_AUXILIARY_SET", path, context_id)
        for index, row in enumerate(rows):
            _validate_source_refs(diagnostics, row.source_refs, f"{path}[{index}].source_refs")

    def validate_auxiliary_candidate_sets(
        rows,
        *,
        source_stem: str,
        source_layer: str,
        context_id: str,
        temporal_source_refs: tuple[str, ...],
        path: str,
    ) -> None:
        expected = (
            TemporalAuxiliaryGenerator.kui_yue_candidate_set(
                source_stem,
                source_layer=source_layer,
                context_id=context_id,
                temporal_source_refs=temporal_source_refs,
            ),
        )
        if tuple(rows) != expected:
            _diag(
                diagnostics,
                "TEMPORAL_AUXILIARY_CANDIDATE_REPLAY_MISMATCH",
                path,
                context_id,
            )
        if len(rows) != 1:
            _diag(
                diagnostics,
                "INVALID_TEMPORAL_AUXILIARY_CANDIDATE_SET",
                path,
                context_id,
            )
        for set_index, candidate_set in enumerate(rows):
            set_path = f"{path}[{set_index}]"
            _validate_source_refs(diagnostics, candidate_set.source_refs, f"{set_path}.source_refs")
            for candidate_index, candidate in enumerate(candidate_set.method_candidates):
                candidate_path = f"{set_path}.method_candidates[{candidate_index}]"
                _validate_source_refs(diagnostics, candidate.source_refs, f"{candidate_path}.source_refs")
                for activation_index, activation in enumerate(candidate.activations):
                    _validate_source_refs(
                        diagnostics,
                        activation.source_refs,
                        f"{candidate_path}.activations[{activation_index}].source_refs",
                    )

    daxian_ids = {frame.frame_id for frame in state.daxian_frames}
    if len(daxian_ids) != len(state.daxian_frames):
        _diag(diagnostics, "DUPLICATE_DAXIAN_FRAME_ID", "daxian_frames", "frame IDs must be unique")
    for index, frame in enumerate(state.daxian_frames):
        path = f"daxian_frames[{index}]"
        if frame.nominal_age_end - frame.nominal_age_start != 9:
            _diag(diagnostics, "INVALID_DAXIAN_AGE_INTERVAL", path, frame.frame_id)
        if frame.absolute_year_end - frame.absolute_year_start != 9:
            _diag(diagnostics, "INVALID_DAXIAN_YEAR_INTERVAL", path, frame.frame_id)
        if frame.designation_overlay[0].address != frame.active_address:
            _diag(diagnostics, "DAXIAN_LIFE_OVERLAY_MISMATCH", path, frame.frame_id)
        validate_overlay(frame.designation_overlay, f"{path}.designation_overlay")
        validate_auxiliaries(
            frame.auxiliary_activations,
            source_stem=frame.source_stem,
            source_layer="DAXIAN",
            context_id=frame.frame_id,
            temporal_source_refs=DAXIAN_AUXILIARY_SOURCE_REFS,
            path=f"{path}.auxiliary_activations",
        )
        validate_auxiliary_candidate_sets(
            frame.auxiliary_candidate_sets,
            source_stem=frame.source_stem,
            source_layer="DAXIAN",
            context_id=frame.frame_id,
            temporal_source_refs=DAXIAN_AUXILIARY_SOURCE_REFS,
            path=f"{path}.auxiliary_candidate_sets",
        )
        validate_transformations(frame.transformations, f"{path}.transformations")
        _validate_source_refs(diagnostics, frame.source_refs, f"{path}.source_refs")

    annual_years: set[int] = set()
    birth_year_candidates: set[int] = set()
    for index, frame in enumerate(state.annual_frames):
        path = f"annual_frames[{index}]"
        if frame.absolute_year in annual_years:
            _diag(diagnostics, "DUPLICATE_ANNUAL_YEAR", path, str(frame.absolute_year))
        annual_years.add(frame.absolute_year)
        birth_year_candidates.add(frame.absolute_year - frame.nominal_age + 1)
        expected_stem, expected_branch = sexagenary_for_year(frame.absolute_year)
        if (frame.year_stem, frame.year_branch) != (expected_stem, expected_branch):
            _diag(diagnostics, "ANNUAL_GANZHI_MISMATCH", path, f"expected {expected_stem}{expected_branch}")
        if frame.active_address.branch != frame.year_branch:
            _diag(diagnostics, "ANNUAL_TAISUI_ADDRESS_MISMATCH", path, frame.frame_id)
        expected_doujun = (
            frame.active_address.index
            - (context.natal_month_coordinate - 1)
            + context.birth_hour_branch.index
        ) % 12
        if frame.doujun_address.index != expected_doujun:
            _diag(diagnostics, "ANNUAL_DOUJUN_ADDRESS_MISMATCH", path, frame.frame_id)
        if frame.doujun_rule_id != DOUJUN_RULE_ID:
            _diag(diagnostics, "ANNUAL_DOUJUN_RULE_ID_MISMATCH", path, frame.frame_id)
        if frame.designation_overlay[0].address != frame.active_address:
            _diag(diagnostics, "ANNUAL_LIFE_OVERLAY_MISMATCH", path, frame.frame_id)
        validate_overlay(frame.designation_overlay, f"{path}.designation_overlay")
        validate_auxiliaries(
            frame.auxiliary_activations,
            source_stem=frame.year_stem,
            source_layer="ANNUAL",
            context_id=frame.frame_id,
            temporal_source_refs=ANNUAL_AUXILIARY_SOURCE_REFS,
            path=f"{path}.auxiliary_activations",
        )
        validate_auxiliary_candidate_sets(
            frame.auxiliary_candidate_sets,
            source_stem=frame.year_stem,
            source_layer="ANNUAL",
            context_id=frame.frame_id,
            temporal_source_refs=ANNUAL_AUXILIARY_SOURCE_REFS,
            path=f"{path}.auxiliary_candidate_sets",
        )
        validate_transformations(frame.transformations, f"{path}.transformations")
        if frame.parent_daxian_frame_id is not None:
            if frame.parent_daxian_frame_id not in daxian_ids:
                _diag(diagnostics, "ANNUAL_UNKNOWN_DAXIAN_PARENT", path, frame.parent_daxian_frame_id)
            else:
                parent = next(row for row in state.daxian_frames if row.frame_id == frame.parent_daxian_frame_id)
                if not parent.nominal_age_start <= frame.nominal_age <= parent.nominal_age_end:
                    _diag(diagnostics, "ANNUAL_DAXIAN_PARENT_AGE_MISMATCH", path, frame.parent_daxian_frame_id)
        _validate_source_refs(diagnostics, frame.source_refs, f"{path}.source_refs")
    if len(birth_year_candidates) > 1:
        _diag(diagnostics, "ANNUAL_BIRTH_YEAR_INCONSISTENCY", "annual_frames", str(sorted(birth_year_candidates)))
    elif birth_year_candidates and next(iter(birth_year_candidates)) != context.ziwei_birth_year:
        _diag(diagnostics, "ANNUAL_BIRTH_YEAR_MISMATCH", "annual_frames", f"expected {context.ziwei_birth_year}")

    annual_by_id = {frame.frame_id: frame for frame in state.annual_frames}
    monthly_coordinates: set[tuple[int, int]] = set()
    months_by_year: dict[int, set[int]] = {}
    for index, frame in enumerate(state.monthly_frames):
        path = f"monthly_frames[{index}]"
        coordinate = (frame.absolute_year, frame.lunar_month)
        if coordinate in monthly_coordinates:
            _diag(diagnostics, "DUPLICATE_MONTHLY_COORDINATE", path, str(coordinate))
        monthly_coordinates.add(coordinate)
        months_by_year.setdefault(frame.absolute_year, set()).add(frame.lunar_month)
        parent = annual_by_id.get(frame.parent_annual_frame_id)
        if parent is None:
            _diag(diagnostics, "MONTHLY_UNKNOWN_ANNUAL_PARENT", path, frame.parent_annual_frame_id)
        else:
            if frame.absolute_year != parent.absolute_year:
                _diag(diagnostics, "MONTHLY_ANNUAL_PARENT_YEAR_MISMATCH", path, frame.frame_id)
            expected_active_index = (parent.doujun_address.index + frame.lunar_month - 1) % 12
            if frame.active_address.index != expected_active_index:
                _diag(diagnostics, "MONTHLY_ADDRESS_MISMATCH", path, frame.frame_id)
        try:
            expected_stem, expected_branch = ZiweiTemporalEngine.month_ganzhi(
                parent.year_stem if parent is not None else sexagenary_for_year(frame.absolute_year)[0],
                frame.lunar_month,
            )
        except ValueError:
            _diag(diagnostics, "INVALID_MONTHLY_NUMBER", path, str(frame.lunar_month))
        else:
            if (frame.month_stem, frame.month_branch, frame.month_ganzhi) != (
                expected_stem,
                expected_branch,
                f"{expected_stem}{expected_branch}",
            ):
                _diag(diagnostics, "MONTHLY_GANZHI_MISMATCH", path, frame.frame_id)
        if frame.designation_overlay[0].address != frame.active_address:
            _diag(diagnostics, "MONTHLY_LIFE_OVERLAY_MISMATCH", path, frame.frame_id)
        validate_overlay(frame.designation_overlay, f"{path}.designation_overlay")
        validate_auxiliaries(
            frame.auxiliary_activations,
            source_stem=frame.month_stem,
            source_layer="MONTH",
            context_id=frame.frame_id,
            temporal_source_refs=MONTHLY_AUXILIARY_SOURCE_REFS,
            path=f"{path}.auxiliary_activations",
        )
        validate_auxiliary_candidate_sets(
            frame.auxiliary_candidate_sets,
            source_stem=frame.month_stem,
            source_layer="MONTH",
            context_id=frame.frame_id,
            temporal_source_refs=MONTHLY_AUXILIARY_SOURCE_REFS,
            path=f"{path}.auxiliary_candidate_sets",
        )
        validate_transformations(frame.transformations, f"{path}.transformations")
        if any(row.source_layer != "MONTH" or row.source_stem != frame.month_stem for row in frame.transformations):
            _diag(diagnostics, "MONTHLY_TRANSFORMATION_SOURCE_MISMATCH", path, frame.frame_id)
        if frame.monthly_rule_id != MONTHLY_RULE_ID:
            _diag(diagnostics, "MONTHLY_RULE_ID_MISMATCH", path, frame.frame_id)
        if frame.month_ganzhi_rule_id != MONTH_GANZHI_RULE_ID:
            _diag(diagnostics, "MONTHLY_GANZHI_RULE_ID_MISMATCH", path, frame.frame_id)
        if frame.calendar_scope != REGULAR_MONTH_CALENDAR_SCOPE:
            _diag(diagnostics, "MONTHLY_CALENDAR_SCOPE_MISMATCH", path, frame.frame_id)
        if frame.leap_month_policy_status != LEAP_MONTH_POLICY_STATUS:
            _diag(diagnostics, "MONTHLY_LEAP_POLICY_STATUS_MISMATCH", path, frame.frame_id)
        _validate_source_refs(diagnostics, frame.source_refs, f"{path}.source_refs")
    for year, months in months_by_year.items():
        if months != set(range(1, 13)):
            _diag(diagnostics, "INCOMPLETE_REGULAR_MONTHLY_YEAR", "monthly_frames", f"{year}: {sorted(months)}")
    if not set(months_by_year).issubset(annual_years):
        _diag(diagnostics, "MONTHLY_ANNUAL_COVERAGE_MISMATCH", "monthly_frames", "monthly years must be a subset of annual frames")

    minor_ages: set[int] = set()
    for index, frame in enumerate(state.minor_limit_frames):
        path = f"minor_limit_frames[{index}]"
        if frame.nominal_age in minor_ages:
            _diag(diagnostics, "DUPLICATE_MINOR_LIMIT_AGE", path, str(frame.nominal_age))
        minor_ages.add(frame.nominal_age)
        _validate_source_refs(diagnostics, frame.source_refs, f"{path}.source_refs")

    return IntegrityReport(status="PASS" if not diagnostics else "FAIL", diagnostics=tuple(diagnostics))
