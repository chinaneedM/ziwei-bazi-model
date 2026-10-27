from __future__ import annotations

import re
from typing import Any, Iterable

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256
from fortune_training.ziwei_chart.models import NatalChartState
from fortune_training.ziwei_chart.registries import PALACE_DESIGNATIONS
from fortune_training.ziwei_structural import StructuralState, validate_structural_state

from .models import (
    RELATIVE_PALACE_FRAME_STATE_SCHEMA,
    RelativeFrameHashBundle,
    RelativeFrameIntegrityDiagnostic,
    RelativeFrameIntegrityReport,
    RelativePalaceFrameState,
    RelativePalaceRoleFact,
)
from .profile import ResolvedRelativePalaceFrameProfile


RELATIVE_FRAME_INTEGRITY_ALGORITHM_ID = "ZIWEI-RELATIVE-PALACE-FRAME-INTEGRITY-HASH-V2-R2"
RELATIVE_FRAME_INTEGRITY_ALGORITHM_VERSION = "1.0.0"
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")
_CANONICAL_IDS = tuple(row[0] for row in PALACE_DESIGNATIONS)
_DESIGNATION_ORDER = {designation_id: index for index, designation_id in enumerate(_CANONICAL_IDS)}


def _diag(
    diagnostics: list[RelativeFrameIntegrityDiagnostic],
    code: str,
    path: str,
    detail: str,
) -> None:
    diagnostics.append(RelativeFrameIntegrityDiagnostic(code=code, path=path, detail=detail))


def _address_fact(value) -> dict[str, Any]:
    return {"index": value.index, "branch": value.branch}


def _ordered_facts(facts: Iterable[RelativePalaceRoleFact]) -> list[RelativePalaceRoleFact]:
    return sorted(
        facts,
        key=lambda row: (
            _DESIGNATION_ORDER.get(row.origin_designation_id, 99),
            row.relative_ordinal,
            row.target_designation_id,
        ),
    )


def relative_frame_fact_projection(
    upstream_structural_fact_hash: str,
    facts: Iterable[RelativePalaceRoleFact],
) -> dict[str, Any]:
    return {
        "upstream_structural_fact_hash": upstream_structural_fact_hash,
        "frame_facts": [
            {
                "origin_designation_id": row.origin_designation_id,
                "origin_address": _address_fact(row.origin_address),
                "relative_ordinal": row.relative_ordinal,
                "relative_role_designation_id": row.relative_role_designation_id,
                "target_designation_id": row.target_designation_id,
                "target_address": _address_fact(row.target_address),
                "clockwise_offset": row.clockwise_offset,
            }
            for row in _ordered_facts(facts)
        ],
    }


def relative_frame_hash_bundle(
    upstream_structural_fact_hash: str,
    upstream_structural_computation_hash: str,
    profile: ResolvedRelativePalaceFrameProfile,
    facts: Iterable[RelativePalaceRoleFact],
) -> RelativeFrameHashBundle:
    fact_hash = object_sha256(relative_frame_fact_projection(upstream_structural_fact_hash, facts))
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "upstream_structural_computation_hash": upstream_structural_computation_hash,
            "resolved_relative_frame_profile": json_value(profile),
            "hash_algorithm": (
                f"{RELATIVE_FRAME_INTEGRITY_ALGORITHM_ID}@"
                f"{RELATIVE_FRAME_INTEGRITY_ALGORITHM_VERSION}"
            ),
        }
    )
    return RelativeFrameHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=RELATIVE_FRAME_INTEGRITY_ALGORITHM_ID,
        algorithm_version=RELATIVE_FRAME_INTEGRITY_ALGORITHM_VERSION,
    )


def validate_relative_frame_components(
    natal_chart: NatalChartState,
    structural_state: StructuralState,
    profile: ResolvedRelativePalaceFrameProfile,
    facts: tuple[RelativePalaceRoleFact, ...],
) -> RelativeFrameIntegrityReport:
    diagnostics: list[RelativeFrameIntegrityDiagnostic] = []

    try:
        profile.validate()
    except ValueError as exc:
        _diag(diagnostics, "INVALID_RELATIVE_FRAME_PROFILE", "profile", str(exc))

    structural_report = validate_structural_state(structural_state)
    if structural_report.status != "PASS":
        first = structural_report.diagnostics[0]
        _diag(
            diagnostics,
            "UPSTREAM_STRUCTURAL_INTEGRITY_FAILED",
            "structural_state",
            f"{first.code}:{first.path}:{first.detail}",
        )

    if (
        structural_state.profile.profile_id != profile.structural_r1_profile_id
        or structural_state.profile.profile_version != profile.structural_r1_profile_version
    ):
        _diag(
            diagnostics,
            "UPSTREAM_STRUCTURAL_PROFILE_MISMATCH",
            "structural_state.profile",
            "R1 state profile does not match the R2 profile binding",
        )

    if (
        natal_chart.profile_id != profile.natal_profile_id
        or natal_chart.profile_version != profile.natal_profile_version
    ):
        _diag(
            diagnostics,
            "UPSTREAM_NATAL_PROFILE_MISMATCH",
            "natal_chart",
            "Natal profile does not match the R2 profile binding",
        )

    if len(facts) != 144:
        _diag(
            diagnostics,
            "INVALID_RELATIVE_FRAME_FACT_COUNT",
            "frame_facts",
            f"expected 144 facts, got {len(facts)}",
        )

    bindings = natal_chart.structure.designation_bindings
    by_id = {row.designation_id: row for row in bindings}
    if len(bindings) != 12 or set(by_id) != set(_CANONICAL_IDS):
        _diag(
            diagnostics,
            "INVALID_NATAL_DESIGNATION_DOMAIN",
            "natal_chart.structure.designation_bindings",
            "expected all 12 frozen V1 palace designations exactly once",
        )

    topology = {
        (row.source.index, row.target.index, row.clockwise_offset)
        for row in structural_state.topology_facts
    }

    keys = [(row.origin_designation_id, row.relative_ordinal) for row in facts]
    if len(set(keys)) != len(keys):
        _diag(
            diagnostics,
            "DUPLICATE_RELATIVE_FRAME_KEY",
            "frame_facts",
            "origin designation / relative ordinal pairs must be unique",
        )

    canonical_keys = [
        (origin_id, ordinal)
        for origin_id in _CANONICAL_IDS
        for ordinal in range(1, 13)
    ]
    if keys != canonical_keys:
        _diag(
            diagnostics,
            "NON_CANONICAL_RELATIVE_FRAME_ORDER",
            "frame_facts",
            "facts must be ordered by frozen origin designation order then ordinal 1..12",
        )

    targets_by_origin: dict[str, set[str]] = {origin_id: set() for origin_id in _CANONICAL_IDS}
    ordinals_by_origin: dict[str, set[int]] = {origin_id: set() for origin_id in _CANONICAL_IDS}

    for index, row in enumerate(facts):
        path = f"frame_facts[{index}]"
        origin_index = _DESIGNATION_ORDER.get(row.origin_designation_id)
        if origin_index is None:
            _diag(
                diagnostics,
                "UNKNOWN_ORIGIN_DESIGNATION",
                f"{path}.origin_designation_id",
                row.origin_designation_id,
            )
            continue

        role_offset = row.relative_ordinal - 1
        if not 0 <= role_offset < 12:
            _diag(
                diagnostics,
                "INVALID_RELATIVE_ORDINAL",
                f"{path}.relative_ordinal",
                str(row.relative_ordinal),
            )
            continue

        expected_role_id = _CANONICAL_IDS[role_offset]
        expected_target_id = _CANONICAL_IDS[(origin_index + role_offset) % 12]
        if row.relative_role_designation_id != expected_role_id:
            _diag(
                diagnostics,
                "RELATIVE_ROLE_MISMATCH",
                f"{path}.relative_role_designation_id",
                f"expected {expected_role_id}, got {row.relative_role_designation_id}",
            )
        if row.target_designation_id != expected_target_id:
            _diag(
                diagnostics,
                "RELATIVE_TARGET_DESIGNATION_MISMATCH",
                f"{path}.target_designation_id",
                f"expected {expected_target_id}, got {row.target_designation_id}",
            )

        origin_binding = by_id.get(row.origin_designation_id)
        target_binding = by_id.get(expected_target_id)
        if origin_binding is not None and row.origin_address != origin_binding.address:
            _diag(
                diagnostics,
                "ORIGIN_ADDRESS_MISMATCH",
                f"{path}.origin_address",
                "origin address does not match upstream V1 designation binding",
            )
        if target_binding is not None and row.target_address != target_binding.address:
            _diag(
                diagnostics,
                "TARGET_ADDRESS_MISMATCH",
                f"{path}.target_address",
                "target address does not match upstream V1 designation binding",
            )

        expected_offset = (row.target_address.index - row.origin_address.index) % 12
        if row.clockwise_offset != expected_offset:
            _diag(
                diagnostics,
                "RELATIVE_OFFSET_TARGET_MISMATCH",
                f"{path}.clockwise_offset",
                f"expected {expected_offset}, got {row.clockwise_offset}",
            )
        expected_geometry_offset = (-role_offset) % 12
        if row.clockwise_offset != expected_geometry_offset:
            _diag(
                diagnostics,
                "RELATIVE_FRAME_GEOMETRY_MISMATCH",
                f"{path}.clockwise_offset",
                (
                    f"ordinal {row.relative_ordinal} requires frozen V1 geometric offset "
                    f"{expected_geometry_offset}, got {row.clockwise_offset}"
                ),
            )
        if (row.origin_address.index, row.target_address.index, row.clockwise_offset) not in topology:
            _diag(
                diagnostics,
                "MISSING_UPSTREAM_TOPOLOGY_FACT",
                path,
                "relative frame edge is absent from upstream R1 neutral topology",
            )

        targets_by_origin.setdefault(row.origin_designation_id, set()).add(row.target_designation_id)
        ordinals_by_origin.setdefault(row.origin_designation_id, set()).add(row.relative_ordinal)

    expected_targets = set(_CANONICAL_IDS)
    expected_ordinals = set(range(1, 13))
    for origin_id in _CANONICAL_IDS:
        if targets_by_origin.get(origin_id, set()) != expected_targets:
            _diag(
                diagnostics,
                "INCOMPLETE_RELATIVE_TARGET_COVERAGE",
                f"frame_facts[origin={origin_id}]",
                "each origin must resolve all 12 natal palace targets exactly once",
            )
        if ordinals_by_origin.get(origin_id, set()) != expected_ordinals:
            _diag(
                diagnostics,
                "INCOMPLETE_RELATIVE_ORDINAL_COVERAGE",
                f"frame_facts[origin={origin_id}]",
                "each origin must cover relative ordinals 1..12 exactly once",
            )

    return RelativeFrameIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=RELATIVE_FRAME_INTEGRITY_ALGORITHM_ID,
        algorithm_version=RELATIVE_FRAME_INTEGRITY_ALGORITHM_VERSION,
    )


def validate_relative_frame_state(
    natal_chart: NatalChartState,
    structural_state: StructuralState,
    state: RelativePalaceFrameState,
) -> RelativeFrameIntegrityReport:
    base = validate_relative_frame_components(
        natal_chart,
        structural_state,
        state.profile,
        state.frame_facts,
    )
    diagnostics = list(base.diagnostics)

    if state.schema != RELATIVE_PALACE_FRAME_STATE_SCHEMA:
        _diag(
            diagnostics,
            "INVALID_RELATIVE_FRAME_SCHEMA_ID",
            "schema",
            f"expected {RELATIVE_PALACE_FRAME_STATE_SCHEMA}",
        )

    if state.upstream_structural_fact_hash != structural_state.hashes.fact_hash:
        _diag(
            diagnostics,
            "UPSTREAM_STRUCTURAL_FACT_HASH_MISMATCH",
            "upstream_structural_fact_hash",
            "state is not bound to the supplied R1 StructuralState FactHash",
        )
    if state.upstream_structural_computation_hash != structural_state.hashes.computation_hash:
        _diag(
            diagnostics,
            "UPSTREAM_STRUCTURAL_COMPUTATION_HASH_MISMATCH",
            "upstream_structural_computation_hash",
            "state is not bound to the supplied R1 StructuralState ComputationHash",
        )

    for label, value in (
        ("upstream_structural_fact_hash", state.upstream_structural_fact_hash),
        ("upstream_structural_computation_hash", state.upstream_structural_computation_hash),
    ):
        if not _SHA256_HEX.fullmatch(value):
            _diag(
                diagnostics,
                "INVALID_UPSTREAM_STRUCTURAL_HASH",
                label,
                "expected lowercase SHA-256 hex",
            )

    if (
        state.integrity.status != "PASS"
        or state.integrity.diagnostics
        or state.integrity.algorithm_id != RELATIVE_FRAME_INTEGRITY_ALGORITHM_ID
        or state.integrity.algorithm_version != RELATIVE_FRAME_INTEGRITY_ALGORITHM_VERSION
    ):
        _diag(
            diagnostics,
            "INVALID_EMBEDDED_RELATIVE_FRAME_INTEGRITY_REPORT",
            "integrity",
            "embedded report must be the canonical PASS report for V2-R2",
        )

    expected_hashes = relative_frame_hash_bundle(
        state.upstream_structural_fact_hash,
        state.upstream_structural_computation_hash,
        state.profile,
        state.frame_facts,
    )
    if state.hashes.algorithm_id != RELATIVE_FRAME_INTEGRITY_ALGORITHM_ID:
        _diag(
            diagnostics,
            "INVALID_RELATIVE_FRAME_HASH_ALGORITHM_ID",
            "hashes.algorithm_id",
            state.hashes.algorithm_id,
        )
    if state.hashes.algorithm_version != RELATIVE_FRAME_INTEGRITY_ALGORITHM_VERSION:
        _diag(
            diagnostics,
            "INVALID_RELATIVE_FRAME_HASH_ALGORITHM_VERSION",
            "hashes.algorithm_version",
            state.hashes.algorithm_version,
        )
    if state.hashes.fact_hash != expected_hashes.fact_hash:
        _diag(
            diagnostics,
            "RELATIVE_FRAME_FACT_HASH_MISMATCH",
            "hashes.fact_hash",
            "stored hash does not match canonical relative-frame fact projection",
        )
    if state.hashes.computation_hash != expected_hashes.computation_hash:
        _diag(
            diagnostics,
            "RELATIVE_FRAME_COMPUTATION_HASH_MISMATCH",
            "hashes.computation_hash",
            "stored hash does not match relative-frame computation lineage",
        )

    return RelativeFrameIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=RELATIVE_FRAME_INTEGRITY_ALGORITHM_ID,
        algorithm_version=RELATIVE_FRAME_INTEGRITY_ALGORITHM_VERSION,
    )
