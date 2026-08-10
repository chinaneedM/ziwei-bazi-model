from __future__ import annotations

import re
from typing import Any, Iterable

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256
from fortune_training.ziwei_chart.integrity import validate_natal_chart
from fortune_training.ziwei_chart.models import NatalChartState
from fortune_training.ziwei_chart.registries import PALACE_DESIGNATIONS
from fortune_training.ziwei_structural import StructuralState, validate_structural_state
from fortune_training.ziwei_structural.r2 import (
    RelativePalaceFrameState,
    validate_relative_frame_state,
)

from .models import (
    BORROW_MEMBER_OFFSETS,
    BORROW_PROJECTION_STATE_SCHEMA,
    BorrowClosureMemberFact,
    BorrowProjectionHashBundle,
    BorrowProjectionIntegrityDiagnostic,
    BorrowProjectionIntegrityReport,
    BorrowProjectionState,
)
from .profile import ResolvedBorrowProjectionProfile
from .projection import BORROW_PROJECTION_SOURCE_REFS, BorrowProjectionGenerator


BORROW_PROJECTION_INTEGRITY_ALGORITHM_ID = "ZIWEI-BORROW-PROJECTION-INTEGRITY-HASH-V2-R3"
BORROW_PROJECTION_INTEGRITY_ALGORITHM_VERSION = "1.0.0"
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")
_CANONICAL_IDS = tuple(row[0] for row in PALACE_DESIGNATIONS)
_ORIGIN_ORDER = {designation_id: index for index, designation_id in enumerate(_CANONICAL_IDS)}
_OFFSET_ORDER = {offset: index for index, offset in enumerate(BORROW_MEMBER_OFFSETS)}


def _diag(
    diagnostics: list[BorrowProjectionIntegrityDiagnostic],
    code: str,
    path: str,
    detail: str,
) -> None:
    diagnostics.append(BorrowProjectionIntegrityDiagnostic(code=code, path=path, detail=detail))


def _address_fact(value) -> dict[str, Any] | None:
    if value is None:
        return None
    return {"index": value.index, "branch": value.branch}


def _ordered_facts(facts: Iterable[BorrowClosureMemberFact]) -> list[BorrowClosureMemberFact]:
    return sorted(
        facts,
        key=lambda row: (
            _ORIGIN_ORDER.get(row.evaluation_origin_designation_id, 99),
            _OFFSET_ORDER.get(row.member_offset, 99),
        ),
    )


def _placement_fact(row) -> dict[str, Any]:
    return {
        "entity_id": row.entity_id,
        "address": _address_fact(row.address),
    }


def _transformation_fact(row) -> dict[str, Any]:
    return {
        "activation_id": row.activation_id,
        "transformation_type": row.transformation_type,
        "target_entity_id": row.target_entity_id,
        "target_address": _address_fact(row.target_address),
        "source_layer": row.source_layer,
        "source_stem": row.source_stem,
        "context_id": row.context_id,
        "assignment_id": row.assignment_id,
        "mechanism_id": row.mechanism_id,
    }


def borrow_projection_fact_projection(
    upstream_relative_frame_fact_hash: str,
    time_layer: str,
    facts: Iterable[BorrowClosureMemberFact],
) -> dict[str, Any]:
    return {
        "upstream_relative_frame_fact_hash": upstream_relative_frame_fact_hash,
        "time_layer": time_layer,
        "member_facts": [
            {
                "evaluation_origin_designation_id": row.evaluation_origin_designation_id,
                "evaluation_origin_address": _address_fact(row.evaluation_origin_address),
                "member_offset": row.member_offset,
                "target_designation_id": row.target_designation_id,
                "target_raw_address": _address_fact(row.target_raw_address),
                "target_main_star_empty": row.target_main_star_empty,
                "closure_status": row.closure_status,
                "borrowed_from_raw_address": _address_fact(row.borrowed_from_raw_address),
                "projected_placements": [_placement_fact(item) for item in row.projected_placements],
                "projected_transformations": [
                    _transformation_fact(item) for item in row.projected_transformations
                ],
                "structure_physical_key": row.structure_physical_key,
                "zero_second_contribution": row.zero_second_contribution,
            }
            for row in _ordered_facts(facts)
        ],
    }


def borrow_projection_hash_bundle(
    upstream_relative_frame_fact_hash: str,
    upstream_relative_frame_computation_hash: str,
    profile: ResolvedBorrowProjectionProfile,
    time_layer: str,
    facts: Iterable[BorrowClosureMemberFact],
) -> BorrowProjectionHashBundle:
    fact_hash = object_sha256(
        borrow_projection_fact_projection(upstream_relative_frame_fact_hash, time_layer, facts)
    )
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "upstream_relative_frame_computation_hash": upstream_relative_frame_computation_hash,
            "resolved_borrow_projection_profile": json_value(profile),
            "source_refs": list(BORROW_PROJECTION_SOURCE_REFS),
            "hash_algorithm": (
                f"{BORROW_PROJECTION_INTEGRITY_ALGORITHM_ID}@"
                f"{BORROW_PROJECTION_INTEGRITY_ALGORITHM_VERSION}"
            ),
        }
    )
    return BorrowProjectionHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=BORROW_PROJECTION_INTEGRITY_ALGORITHM_ID,
        algorithm_version=BORROW_PROJECTION_INTEGRITY_ALGORITHM_VERSION,
    )


def validate_borrow_projection_components(
    natal_chart: NatalChartState,
    structural_state: StructuralState,
    relative_state: RelativePalaceFrameState,
    profile: ResolvedBorrowProjectionProfile,
    time_layer: str,
    facts: tuple[BorrowClosureMemberFact, ...],
) -> BorrowProjectionIntegrityReport:
    diagnostics: list[BorrowProjectionIntegrityDiagnostic] = []

    try:
        profile.validate()
    except ValueError as exc:
        _diag(diagnostics, "INVALID_BORROW_PROJECTION_PROFILE", "profile", str(exc))

    if time_layer != profile.supported_time_layer or time_layer != "NATAL":
        _diag(
            diagnostics,
            "UNSUPPORTED_BORROW_TIME_LAYER",
            "time_layer",
            f"R3 currently supports NATAL only, got {time_layer}",
        )

    natal_report = validate_natal_chart(natal_chart)
    if natal_report.status != "PASS":
        first = natal_report.diagnostics[0]
        _diag(
            diagnostics,
            "UPSTREAM_NATAL_INTEGRITY_FAILED",
            "natal_chart",
            f"{first.code}:{first.path}:{first.detail}",
        )

    structural_report = validate_structural_state(structural_state)
    if structural_report.status != "PASS":
        first = structural_report.diagnostics[0]
        _diag(
            diagnostics,
            "UPSTREAM_STRUCTURAL_INTEGRITY_FAILED",
            "structural_state",
            f"{first.code}:{first.path}:{first.detail}",
        )

    relative_report = validate_relative_frame_state(natal_chart, structural_state, relative_state)
    if relative_report.status != "PASS":
        first = relative_report.diagnostics[0]
        _diag(
            diagnostics,
            "UPSTREAM_RELATIVE_FRAME_INTEGRITY_FAILED",
            "relative_state",
            f"{first.code}:{first.path}:{first.detail}",
        )

    if (
        natal_chart.profile_id != profile.natal_profile_id
        or natal_chart.profile_version != profile.natal_profile_version
    ):
        _diag(
            diagnostics,
            "UPSTREAM_NATAL_PROFILE_MISMATCH",
            "natal_chart",
            "Natal profile does not match R3 binding",
        )
    if (
        structural_state.profile.profile_id != profile.structural_r1_profile_id
        or structural_state.profile.profile_version != profile.structural_r1_profile_version
    ):
        _diag(
            diagnostics,
            "UPSTREAM_STRUCTURAL_R1_PROFILE_MISMATCH",
            "structural_state.profile",
            "R1 profile does not match R3 binding",
        )
    if (
        relative_state.profile.profile_id != profile.structural_r2_profile_id
        or relative_state.profile.profile_version != profile.structural_r2_profile_version
    ):
        _diag(
            diagnostics,
            "UPSTREAM_STRUCTURAL_R2_PROFILE_MISMATCH",
            "relative_state.profile",
            "R2 profile does not match R3 binding",
        )
    if (
        relative_state.upstream_structural_fact_hash != structural_state.hashes.fact_hash
        or relative_state.upstream_structural_computation_hash
        != structural_state.hashes.computation_hash
    ):
        _diag(
            diagnostics,
            "CROSS_STATE_R1_R2_BINDING_MISMATCH",
            "relative_state",
            "R2 state is not bound to the supplied R1 state",
        )

    if len(facts) != 48:
        _diag(
            diagnostics,
            "INVALID_BORROW_MEMBER_FACT_COUNT",
            "member_facts",
            f"expected 48 facts, got {len(facts)}",
        )

    expected_keys = [
        (origin_id, offset)
        for origin_id in _CANONICAL_IDS
        for offset in BORROW_MEMBER_OFFSETS
    ]
    actual_keys = [
        (row.evaluation_origin_designation_id, row.member_offset)
        for row in facts
    ]
    if actual_keys != expected_keys:
        _diag(
            diagnostics,
            "NON_CANONICAL_BORROW_MEMBER_ORDER",
            "member_facts",
            "facts must be ordered by frozen origin designation order then offsets 0,4,6,8",
        )
    if len(set(actual_keys)) != len(actual_keys):
        _diag(
            diagnostics,
            "DUPLICATE_BORROW_MEMBER_KEY",
            "member_facts",
            "origin designation/member offset pairs must be unique",
        )

    expected_facts: tuple[BorrowClosureMemberFact, ...] = ()
    if not diagnostics:
        try:
            expected_facts = BorrowProjectionGenerator().generate(
                natal_chart,
                relative_state,
                time_layer=time_layer,
            )
        except ValueError as exc:
            _diag(diagnostics, "BORROW_EXPECTED_GENERATION_FAILED", "member_facts", str(exc))

    if expected_facts:
        if len(expected_facts) != len(facts):
            _diag(
                diagnostics,
                "BORROW_EXPECTED_FACT_COUNT_MISMATCH",
                "member_facts",
                "generated canonical fact count differs from supplied facts",
            )
        for index, (actual, expected) in enumerate(zip(facts, expected_facts)):
            path = f"member_facts[{index}]"
            fields = (
                ("evaluation_origin_designation_id", "BORROW_ORIGIN_DESIGNATION_MISMATCH"),
                ("evaluation_origin_address", "BORROW_ORIGIN_ADDRESS_MISMATCH"),
                ("time_layer", "BORROW_TIME_LAYER_MISMATCH"),
                ("member_offset", "BORROW_MEMBER_OFFSET_MISMATCH"),
                ("target_designation_id", "BORROW_TARGET_DESIGNATION_MISMATCH"),
                ("target_raw_address", "BORROW_TARGET_ADDRESS_MISMATCH"),
                ("target_main_star_empty", "BORROW_EMPTY_STATUS_MISMATCH"),
                ("closure_status", "BORROW_CLOSURE_STATUS_MISMATCH"),
                ("borrowed_from_raw_address", "BORROW_SOURCE_ADDRESS_MISMATCH"),
                ("projected_placements", "BORROW_PROJECTED_PLACEMENTS_MISMATCH"),
                ("projected_transformations", "BORROW_PROJECTED_TRANSFORMATIONS_MISMATCH"),
                ("structure_physical_key", "BORROW_STRUCTURE_PHYSICAL_KEY_MISMATCH"),
                ("zero_second_contribution", "BORROW_ZERO_SECOND_CONTRIBUTION_MISMATCH"),
            )
            for field_name, code in fields:
                if getattr(actual, field_name) != getattr(expected, field_name):
                    _diag(
                        diagnostics,
                        code,
                        f"{path}.{field_name}",
                        "supplied fact does not match canonical one-step S06 borrow projection",
                    )

    return BorrowProjectionIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=BORROW_PROJECTION_INTEGRITY_ALGORITHM_ID,
        algorithm_version=BORROW_PROJECTION_INTEGRITY_ALGORITHM_VERSION,
    )


def validate_borrow_projection_state(
    natal_chart: NatalChartState,
    structural_state: StructuralState,
    relative_state: RelativePalaceFrameState,
    state: BorrowProjectionState,
) -> BorrowProjectionIntegrityReport:
    base = validate_borrow_projection_components(
        natal_chart,
        structural_state,
        relative_state,
        state.profile,
        state.time_layer,
        state.member_facts,
    )
    diagnostics = list(base.diagnostics)

    if state.schema != BORROW_PROJECTION_STATE_SCHEMA:
        _diag(
            diagnostics,
            "INVALID_BORROW_PROJECTION_SCHEMA_ID",
            "schema",
            f"expected {BORROW_PROJECTION_STATE_SCHEMA}",
        )
    if state.upstream_relative_frame_fact_hash != relative_state.hashes.fact_hash:
        _diag(
            diagnostics,
            "UPSTREAM_R2_FACT_HASH_MISMATCH",
            "upstream_relative_frame_fact_hash",
            "state is not bound to supplied R2 FactHash",
        )
    if state.upstream_relative_frame_computation_hash != relative_state.hashes.computation_hash:
        _diag(
            diagnostics,
            "UPSTREAM_R2_COMPUTATION_HASH_MISMATCH",
            "upstream_relative_frame_computation_hash",
            "state is not bound to supplied R2 ComputationHash",
        )

    for label, value in (
        ("upstream_relative_frame_fact_hash", state.upstream_relative_frame_fact_hash),
        ("upstream_relative_frame_computation_hash", state.upstream_relative_frame_computation_hash),
    ):
        if not _SHA256_HEX.fullmatch(value):
            _diag(diagnostics, "INVALID_UPSTREAM_R2_HASH", label, "expected lowercase SHA-256 hex")

    if (
        state.integrity.status != "PASS"
        or state.integrity.diagnostics
        or state.integrity.algorithm_id != BORROW_PROJECTION_INTEGRITY_ALGORITHM_ID
        or state.integrity.algorithm_version != BORROW_PROJECTION_INTEGRITY_ALGORITHM_VERSION
    ):
        _diag(
            diagnostics,
            "INVALID_EMBEDDED_BORROW_INTEGRITY_REPORT",
            "integrity",
            "embedded report must be canonical PASS report for V2-R3",
        )

    expected_hashes = borrow_projection_hash_bundle(
        state.upstream_relative_frame_fact_hash,
        state.upstream_relative_frame_computation_hash,
        state.profile,
        state.time_layer,
        state.member_facts,
    )
    if state.hashes.algorithm_id != BORROW_PROJECTION_INTEGRITY_ALGORITHM_ID:
        _diag(
            diagnostics,
            "INVALID_BORROW_HASH_ALGORITHM_ID",
            "hashes.algorithm_id",
            state.hashes.algorithm_id,
        )
    if state.hashes.algorithm_version != BORROW_PROJECTION_INTEGRITY_ALGORITHM_VERSION:
        _diag(
            diagnostics,
            "INVALID_BORROW_HASH_ALGORITHM_VERSION",
            "hashes.algorithm_version",
            state.hashes.algorithm_version,
        )
    if state.hashes.fact_hash != expected_hashes.fact_hash:
        _diag(
            diagnostics,
            "BORROW_FACT_HASH_MISMATCH",
            "hashes.fact_hash",
            "stored hash does not match canonical borrow fact projection",
        )
    if state.hashes.computation_hash != expected_hashes.computation_hash:
        _diag(
            diagnostics,
            "BORROW_COMPUTATION_HASH_MISMATCH",
            "hashes.computation_hash",
            "stored hash does not match borrow computation lineage",
        )

    return BorrowProjectionIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=BORROW_PROJECTION_INTEGRITY_ALGORITHM_ID,
        algorithm_version=BORROW_PROJECTION_INTEGRITY_ALGORITHM_VERSION,
    )
