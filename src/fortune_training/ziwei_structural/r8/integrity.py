from __future__ import annotations

import re
from typing import Any, Iterable

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256
from fortune_training.ziwei_structural.r2 import RelativePalaceFrameState, canonical_designation_ids

from .models import (
    ADJACENT_PALACE_PAIR_STATE_SCHEMA,
    AdjacentPalaceHashBundle,
    AdjacentPalaceIntegrityDiagnostic,
    AdjacentPalaceIntegrityReport,
    AdjacentPalacePairFact,
    AdjacentPalacePairState,
)
from .profile import (
    ADJACENT_PALACE_SEMANTIC_SCOPE,
    ADJACENT_PALACE_SOURCE_TERM_ID,
    CLOCKWISE_NEIGHBOR_CLOCKWISE_OFFSET,
    CLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL,
    COUNTERCLOCKWISE_NEIGHBOR_CLOCKWISE_OFFSET,
    COUNTERCLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL,
    ResolvedAdjacentPalacePairProfile,
)
from .projection import AdjacentPalaceProjectionError, project_adjacent_palace_pairs


ADJACENT_PALACE_INTEGRITY_ALGORITHM_ID = "ZIWEI-ADJACENT-PALACE-INTEGRITY-HASH-V2-R8"
ADJACENT_PALACE_INTEGRITY_ALGORITHM_VERSION = "1.0.0"
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")


def _diag(
    diagnostics: list[AdjacentPalaceIntegrityDiagnostic],
    code: str,
    path: str,
    detail: str,
) -> None:
    diagnostics.append(AdjacentPalaceIntegrityDiagnostic(code=code, path=path, detail=detail))


def _address_fact(value) -> dict[str, Any]:
    return {"index": value.index, "branch": value.branch}


def adjacent_palace_fact_projection(
    upstream_r2_fact_hash: str,
    facts: Iterable[AdjacentPalacePairFact],
) -> dict[str, Any]:
    return {
        "upstream_r2_fact_hash": upstream_r2_fact_hash,
        "adjacent_palace_pairs": [
            {
                "source_term_id": row.source_term_id,
                "origin_designation_id": row.origin_designation_id,
                "origin_address": _address_fact(row.origin_address),
                "counterclockwise_designation_id": row.counterclockwise_designation_id,
                "counterclockwise_address": _address_fact(row.counterclockwise_address),
                "counterclockwise_relative_ordinal": row.counterclockwise_relative_ordinal,
                "counterclockwise_clockwise_offset": row.counterclockwise_clockwise_offset,
                "clockwise_designation_id": row.clockwise_designation_id,
                "clockwise_address": _address_fact(row.clockwise_address),
                "clockwise_relative_ordinal": row.clockwise_relative_ordinal,
                "clockwise_clockwise_offset": row.clockwise_clockwise_offset,
                "semantic_scope": row.semantic_scope,
                "direct_event_permission": row.direct_event_permission,
                "direct_endpoint_permission": row.direct_endpoint_permission,
                "direct_score_permission": row.direct_score_permission,
                "flank_semantics_permission": row.flank_semantics_permission,
            }
            for row in facts
        ],
    }


def adjacent_palace_hash_bundle(
    upstream_r2_fact_hash: str,
    upstream_r2_computation_hash: str,
    profile: ResolvedAdjacentPalacePairProfile,
    time_layer: str,
    facts: Iterable[AdjacentPalacePairFact],
) -> AdjacentPalaceHashBundle:
    facts = tuple(facts)
    fact_hash = object_sha256(adjacent_palace_fact_projection(upstream_r2_fact_hash, facts))
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "upstream_r2_computation_hash": upstream_r2_computation_hash,
            "resolved_adjacent_palace_profile": json_value(profile),
            "time_layer": time_layer,
            "integrity_algorithm_id": ADJACENT_PALACE_INTEGRITY_ALGORITHM_ID,
            "integrity_algorithm_version": ADJACENT_PALACE_INTEGRITY_ALGORITHM_VERSION,
        }
    )
    return AdjacentPalaceHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=ADJACENT_PALACE_INTEGRITY_ALGORITHM_ID,
        algorithm_version=ADJACENT_PALACE_INTEGRITY_ALGORITHM_VERSION,
    )


def validate_adjacent_palace_components(
    r2_state: RelativePalaceFrameState,
    profile: ResolvedAdjacentPalacePairProfile,
    time_layer: str,
    facts: tuple[AdjacentPalacePairFact, ...],
) -> AdjacentPalaceIntegrityReport:
    diagnostics: list[AdjacentPalaceIntegrityDiagnostic] = []
    try:
        profile.validate()
    except ValueError as exc:
        _diag(diagnostics, "INVALID_ADJACENT_PALACE_PROFILE", "profile", str(exc))
    if (
        r2_state.profile.profile_id != profile.upstream_r2_profile_id
        or r2_state.profile.profile_version != profile.upstream_r2_profile_version
    ):
        _diag(
            diagnostics,
            "UPSTREAM_R2_PROFILE_MISMATCH",
            "r2_state.profile",
            "R2 state profile does not match the R8 profile binding",
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
            "UNSUPPORTED_ADJACENT_PALACE_TIME_LAYER",
            "time_layer",
            f"expected {profile.supported_time_layer}, got {time_layer}",
        )
    canonical_origins = canonical_designation_ids()
    if len(facts) != 12:
        _diag(
            diagnostics,
            "INVALID_ADJACENT_PALACE_FACT_COUNT",
            "adjacent_palace_pairs",
            f"expected 12, got {len(facts)}",
        )
    if tuple(row.origin_designation_id for row in facts) != canonical_origins:
        _diag(
            diagnostics,
            "NON_CANONICAL_ADJACENT_PALACE_ORIGIN_ORDER",
            "adjacent_palace_pairs",
            "facts must follow the frozen V1 palace designation order exactly once",
        )
    for index, row in enumerate(facts):
        path = f"adjacent_palace_pairs[{index}]"
        if row.source_term_id != ADJACENT_PALACE_SOURCE_TERM_ID:
            _diag(diagnostics, "INVALID_ADJACENT_PALACE_SOURCE_TERM", f"{path}.source_term_id", "unexpected source term")
        if (
            row.counterclockwise_relative_ordinal != COUNTERCLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL
            or row.counterclockwise_clockwise_offset != COUNTERCLOCKWISE_NEIGHBOR_CLOCKWISE_OFFSET
        ):
            _diag(diagnostics, "INVALID_COUNTERCLOCKWISE_NEIGHBOR_GEOMETRY", path, "expected ordinal 2 / clockwise offset 11")
        if (
            row.clockwise_relative_ordinal != CLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL
            or row.clockwise_clockwise_offset != CLOCKWISE_NEIGHBOR_CLOCKWISE_OFFSET
        ):
            _diag(diagnostics, "INVALID_CLOCKWISE_NEIGHBOR_GEOMETRY", path, "expected ordinal 12 / clockwise offset 1")
        if row.semantic_scope != ADJACENT_PALACE_SEMANTIC_SCOPE:
            _diag(diagnostics, "INVALID_ADJACENT_PALACE_SEMANTIC_SCOPE", f"{path}.semantic_scope", "unexpected semantic scope")
        if (
            row.direct_event_permission
            or row.direct_endpoint_permission
            or row.direct_score_permission
            or row.flank_semantics_permission
        ):
            _diag(
                diagnostics,
                "ILLEGAL_ADJACENT_PALACE_RESULT_PERMISSION",
                path,
                "adjacent geometry must not directly prove flank semantics, event, endpoint or score",
            )
        if row.counterclockwise_address == row.clockwise_address:
            _diag(diagnostics, "COLLAPSED_ADJACENT_PALACE_PAIR", path, "two neighbor addresses must be distinct")
    try:
        expected_facts = project_adjacent_palace_pairs(r2_state)
    except AdjacentPalaceProjectionError as exc:
        _diag(diagnostics, exc.diagnostic_code, "r2_state.frame_facts", str(exc))
    else:
        if facts != expected_facts:
            _diag(
                diagnostics,
                "ADJACENT_PALACE_FACT_PROJECTION_MISMATCH",
                "adjacent_palace_pairs",
                "facts do not equal the canonical S04 neighbor projection over R2",
            )
    return AdjacentPalaceIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=ADJACENT_PALACE_INTEGRITY_ALGORITHM_ID,
        algorithm_version=ADJACENT_PALACE_INTEGRITY_ALGORITHM_VERSION,
    )


def validate_adjacent_palace_state(
    r2_state: RelativePalaceFrameState,
    state: AdjacentPalacePairState,
) -> AdjacentPalaceIntegrityReport:
    base = validate_adjacent_palace_components(
        r2_state,
        state.profile,
        state.time_layer,
        state.adjacent_palace_pairs,
    )
    diagnostics = list(base.diagnostics)
    if state.schema != ADJACENT_PALACE_PAIR_STATE_SCHEMA:
        _diag(diagnostics, "INVALID_ADJACENT_PALACE_SCHEMA_ID", "schema", f"expected {ADJACENT_PALACE_PAIR_STATE_SCHEMA}")
    if state.upstream_r2_fact_hash != r2_state.hashes.fact_hash:
        _diag(diagnostics, "UPSTREAM_R2_FACT_HASH_MISMATCH", "upstream_r2_fact_hash", "state is not bound to supplied R2 FactHash")
    if state.upstream_r2_computation_hash != r2_state.hashes.computation_hash:
        _diag(diagnostics, "UPSTREAM_R2_COMPUTATION_HASH_MISMATCH", "upstream_r2_computation_hash", "state is not bound to supplied R2 ComputationHash")
    for label, value in (
        ("upstream_r2_fact_hash", state.upstream_r2_fact_hash),
        ("upstream_r2_computation_hash", state.upstream_r2_computation_hash),
    ):
        if not _SHA256_HEX.fullmatch(value):
            _diag(diagnostics, "INVALID_UPSTREAM_R2_HASH", label, "expected lowercase SHA-256 hex")
    if (
        state.integrity.status != "PASS"
        or state.integrity.diagnostics
        or state.integrity.algorithm_id != ADJACENT_PALACE_INTEGRITY_ALGORITHM_ID
        or state.integrity.algorithm_version != ADJACENT_PALACE_INTEGRITY_ALGORITHM_VERSION
    ):
        _diag(
            diagnostics,
            "INVALID_EMBEDDED_ADJACENT_PALACE_INTEGRITY_REPORT",
            "integrity",
            "embedded report must be the canonical PASS report for V2-R8",
        )
    expected_hashes = adjacent_palace_hash_bundle(
        state.upstream_r2_fact_hash,
        state.upstream_r2_computation_hash,
        state.profile,
        state.time_layer,
        state.adjacent_palace_pairs,
    )
    if state.hashes != expected_hashes:
        _diag(
            diagnostics,
            "ADJACENT_PALACE_HASH_BUNDLE_MISMATCH",
            "hashes",
            "stored hashes do not match canonical R8 fact/computation projections",
        )
    return AdjacentPalaceIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=ADJACENT_PALACE_INTEGRITY_ALGORITHM_ID,
        algorithm_version=ADJACENT_PALACE_INTEGRITY_ALGORITHM_VERSION,
    )
