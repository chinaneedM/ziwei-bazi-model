from __future__ import annotations

import re
from typing import Any, Iterable

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256
from fortune_training.ziwei_structural.r2 import RelativePalaceFrameState

from .models import (
    QISHU_POSITION_STATE_SCHEMA,
    QiShuHashBundle,
    QiShuIntegrityDiagnostic,
    QiShuIntegrityReport,
    QiShuPositionFact,
    QiShuPositionState,
)
from .profile import (
    QISHU_CLOCKWISE_OFFSET,
    QISHU_RELATIVE_ORDINAL,
    ResolvedQiShuPositionProfile,
)
from .projection import QISHU_MAPPING_SPECS, QiShuProjectionError, project_qishu_positions


QISHU_INTEGRITY_ALGORITHM_ID = "ZIWEI-QISHU-POSITION-INTEGRITY-HASH-V2-R6"
QISHU_INTEGRITY_ALGORITHM_VERSION = "1.0.0"
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")


def _diag(diagnostics: list[QiShuIntegrityDiagnostic], code: str, path: str, detail: str) -> None:
    diagnostics.append(QiShuIntegrityDiagnostic(code=code, path=path, detail=detail))


def _address_fact(value) -> dict[str, Any]:
    return {"index": value.index, "branch": value.branch}


def qishu_fact_projection(
    upstream_r2_fact_hash: str,
    facts: Iterable[QiShuPositionFact],
) -> dict[str, Any]:
    return {
        "upstream_r2_fact_hash": upstream_r2_fact_hash,
        "qishu_facts": [
            {
                "source_mapping_id": row.source_mapping_id,
                "origin_designation_id": row.origin_designation_id,
                "origin_address": _address_fact(row.origin_address),
                "target_designation_id": row.target_designation_id,
                "target_address": _address_fact(row.target_address),
                "relative_ordinal": row.relative_ordinal,
                "clockwise_offset": row.clockwise_offset,
                "fixed_support_meaning": row.fixed_support_meaning,
            }
            for row in facts
        ],
    }


def qishu_hash_bundle(
    upstream_r2_fact_hash: str,
    upstream_r2_computation_hash: str,
    profile: ResolvedQiShuPositionProfile,
    time_layer: str,
    facts: Iterable[QiShuPositionFact],
) -> QiShuHashBundle:
    fact_hash = object_sha256(qishu_fact_projection(upstream_r2_fact_hash, facts))
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "upstream_r2_computation_hash": upstream_r2_computation_hash,
            "resolved_qishu_profile": json_value(profile),
            "time_layer": time_layer,
            "hash_algorithm": f"{QISHU_INTEGRITY_ALGORITHM_ID}@{QISHU_INTEGRITY_ALGORITHM_VERSION}",
        }
    )
    return QiShuHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=QISHU_INTEGRITY_ALGORITHM_ID,
        algorithm_version=QISHU_INTEGRITY_ALGORITHM_VERSION,
    )


def validate_qishu_components(
    r2_state: RelativePalaceFrameState,
    profile: ResolvedQiShuPositionProfile,
    time_layer: str,
    facts: tuple[QiShuPositionFact, ...],
) -> QiShuIntegrityReport:
    diagnostics: list[QiShuIntegrityDiagnostic] = []
    try:
        profile.validate()
    except ValueError as exc:
        _diag(diagnostics, "INVALID_QISHU_PROFILE", "profile", str(exc))

    if (
        r2_state.profile.profile_id != profile.upstream_r2_profile_id
        or r2_state.profile.profile_version != profile.upstream_r2_profile_version
    ):
        _diag(
            diagnostics,
            "UPSTREAM_R2_PROFILE_MISMATCH",
            "r2_state.profile",
            "R2 state profile does not match the R6 profile binding",
        )
    if r2_state.integrity.status != "PASS" or r2_state.integrity.diagnostics:
        _diag(
            diagnostics,
            "UPSTREAM_R2_INTEGRITY_NOT_PASS",
            "r2_state.integrity",
            "R2 state must carry a canonical PASS integrity report",
        )
    if time_layer != profile.supported_time_layer:
        _diag(
            diagnostics,
            "UNSUPPORTED_QISHU_TIME_LAYER",
            "time_layer",
            f"expected {profile.supported_time_layer}, got {time_layer}",
        )

    expected_ids = tuple(spec.source_mapping_id for spec in QISHU_MAPPING_SPECS)
    if len(facts) != 12:
        _diag(diagnostics, "INVALID_QISHU_FACT_COUNT", "qishu_facts", f"expected 12, got {len(facts)}")
    if tuple(row.source_mapping_id for row in facts) != expected_ids:
        _diag(
            diagnostics,
            "NON_CANONICAL_QISHU_MAPPING_ORDER",
            "qishu_facts",
            "facts must follow S04-QS-01..12 exactly once in frozen order",
        )
    for index, row in enumerate(facts):
        if row.relative_ordinal != QISHU_RELATIVE_ORDINAL:
            _diag(
                diagnostics,
                "INVALID_QISHU_RELATIVE_ORDINAL",
                f"qishu_facts[{index}].relative_ordinal",
                f"expected {QISHU_RELATIVE_ORDINAL}, got {row.relative_ordinal}",
            )
        if row.clockwise_offset != QISHU_CLOCKWISE_OFFSET:
            _diag(
                diagnostics,
                "INVALID_QISHU_CLOCKWISE_OFFSET",
                f"qishu_facts[{index}].clockwise_offset",
                f"expected {QISHU_CLOCKWISE_OFFSET}, got {row.clockwise_offset}",
            )

    try:
        expected_facts = project_qishu_positions(r2_state)
    except QiShuProjectionError as exc:
        _diag(diagnostics, exc.diagnostic_code, "r2_state.frame_facts", str(exc))
    else:
        if facts != expected_facts:
            _diag(
                diagnostics,
                "QISHU_FACT_PROJECTION_MISMATCH",
                "qishu_facts",
                "facts do not equal the canonical S04 projection over R2 ordinal 9",
            )

    return QiShuIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=QISHU_INTEGRITY_ALGORITHM_ID,
        algorithm_version=QISHU_INTEGRITY_ALGORITHM_VERSION,
    )


def validate_qishu_state(
    r2_state: RelativePalaceFrameState,
    state: QiShuPositionState,
) -> QiShuIntegrityReport:
    base = validate_qishu_components(r2_state, state.profile, state.time_layer, state.qishu_facts)
    diagnostics = list(base.diagnostics)
    if state.schema != QISHU_POSITION_STATE_SCHEMA:
        _diag(diagnostics, "INVALID_QISHU_SCHEMA_ID", "schema", f"expected {QISHU_POSITION_STATE_SCHEMA}")
    if state.upstream_r2_fact_hash != r2_state.hashes.fact_hash:
        _diag(
            diagnostics,
            "UPSTREAM_R2_FACT_HASH_MISMATCH",
            "upstream_r2_fact_hash",
            "state is not bound to supplied R2 FactHash",
        )
    if state.upstream_r2_computation_hash != r2_state.hashes.computation_hash:
        _diag(
            diagnostics,
            "UPSTREAM_R2_COMPUTATION_HASH_MISMATCH",
            "upstream_r2_computation_hash",
            "state is not bound to supplied R2 ComputationHash",
        )
    for label, value in (
        ("upstream_r2_fact_hash", state.upstream_r2_fact_hash),
        ("upstream_r2_computation_hash", state.upstream_r2_computation_hash),
    ):
        if not _SHA256_HEX.fullmatch(value):
            _diag(diagnostics, "INVALID_UPSTREAM_R2_HASH", label, "expected lowercase SHA-256 hex")
    if (
        state.integrity.status != "PASS"
        or state.integrity.diagnostics
        or state.integrity.algorithm_id != QISHU_INTEGRITY_ALGORITHM_ID
        or state.integrity.algorithm_version != QISHU_INTEGRITY_ALGORITHM_VERSION
    ):
        _diag(
            diagnostics,
            "INVALID_EMBEDDED_QISHU_INTEGRITY_REPORT",
            "integrity",
            "embedded report must be the canonical PASS report for V2-R6",
        )
    expected_hashes = qishu_hash_bundle(
        state.upstream_r2_fact_hash,
        state.upstream_r2_computation_hash,
        state.profile,
        state.time_layer,
        state.qishu_facts,
    )
    if state.hashes != expected_hashes:
        _diag(
            diagnostics,
            "QISHU_HASH_BUNDLE_MISMATCH",
            "hashes",
            "stored hashes do not match canonical R6 fact/computation projections",
        )
    return QiShuIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=QISHU_INTEGRITY_ALGORITHM_ID,
        algorithm_version=QISHU_INTEGRITY_ALGORITHM_VERSION,
    )
