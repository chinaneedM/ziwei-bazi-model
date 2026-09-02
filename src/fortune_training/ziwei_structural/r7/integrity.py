from __future__ import annotations

import re
from typing import Any, Iterable

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256
from fortune_training.ziwei_structural.r2 import RelativePalaceFrameState, canonical_designation_ids

from .models import (
    ONE_SIX_COMMON_ROOT_STATE_SCHEMA,
    OneSixCommonRootFact,
    OneSixCommonRootState,
    OneSixHashBundle,
    OneSixIntegrityDiagnostic,
    OneSixIntegrityReport,
)
from .profile import (
    ONE_SIX_CLOCKWISE_OFFSET,
    ONE_SIX_RELATIVE_ORDINAL,
    ONE_SIX_SEMANTIC_SCOPE,
    ONE_SIX_SOURCE_TECHNIQUE_ID,
    ResolvedOneSixCommonRootProfile,
)
from .projection import OneSixProjectionError, project_one_six_common_roots


ONE_SIX_INTEGRITY_ALGORITHM_ID = "ZIWEI-ONE-SIX-COMMON-ROOT-INTEGRITY-HASH-V2-R7"
ONE_SIX_INTEGRITY_ALGORITHM_VERSION = "1.0.0"
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")


def _diag(
    diagnostics: list[OneSixIntegrityDiagnostic],
    code: str,
    path: str,
    detail: str,
) -> None:
    diagnostics.append(OneSixIntegrityDiagnostic(code=code, path=path, detail=detail))


def _address_fact(value) -> dict[str, Any]:
    return {"index": value.index, "branch": value.branch}


def one_six_fact_projection(
    upstream_r2_fact_hash: str,
    facts: Iterable[OneSixCommonRootFact],
) -> dict[str, Any]:
    return {
        "upstream_r2_fact_hash": upstream_r2_fact_hash,
        "one_six_facts": [
            {
                "source_technique_id": row.source_technique_id,
                "origin_designation_id": row.origin_designation_id,
                "origin_address": _address_fact(row.origin_address),
                "relative_role_designation_id": row.relative_role_designation_id,
                "target_designation_id": row.target_designation_id,
                "target_address": _address_fact(row.target_address),
                "relative_ordinal": row.relative_ordinal,
                "clockwise_offset": row.clockwise_offset,
                "semantic_scope": row.semantic_scope,
                "direct_event_permission": row.direct_event_permission,
                "direct_endpoint_permission": row.direct_endpoint_permission,
            }
            for row in facts
        ],
    }


def one_six_hash_bundle(
    upstream_r2_fact_hash: str,
    upstream_r2_computation_hash: str,
    profile: ResolvedOneSixCommonRootProfile,
    time_layer: str,
    facts: Iterable[OneSixCommonRootFact],
) -> OneSixHashBundle:
    fact_hash = object_sha256(one_six_fact_projection(upstream_r2_fact_hash, facts))
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "upstream_r2_computation_hash": upstream_r2_computation_hash,
            "resolved_one_six_profile": json_value(profile),
            "time_layer": time_layer,
            "hash_algorithm": (
                f"{ONE_SIX_INTEGRITY_ALGORITHM_ID}@{ONE_SIX_INTEGRITY_ALGORITHM_VERSION}"
            ),
        }
    )
    return OneSixHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=ONE_SIX_INTEGRITY_ALGORITHM_ID,
        algorithm_version=ONE_SIX_INTEGRITY_ALGORITHM_VERSION,
    )


def validate_one_six_components(
    r2_state: RelativePalaceFrameState,
    profile: ResolvedOneSixCommonRootProfile,
    time_layer: str,
    facts: tuple[OneSixCommonRootFact, ...],
) -> OneSixIntegrityReport:
    diagnostics: list[OneSixIntegrityDiagnostic] = []
    try:
        profile.validate()
    except ValueError as exc:
        _diag(diagnostics, "INVALID_ONE_SIX_PROFILE", "profile", str(exc))

    if (
        r2_state.profile.profile_id != profile.upstream_r2_profile_id
        or r2_state.profile.profile_version != profile.upstream_r2_profile_version
    ):
        _diag(
            diagnostics,
            "UPSTREAM_R2_PROFILE_MISMATCH",
            "r2_state.profile",
            "R2 state profile does not match the R7 profile binding",
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
            "UNSUPPORTED_ONE_SIX_TIME_LAYER",
            "time_layer",
            f"expected {profile.supported_time_layer}, got {time_layer}",
        )

    canonical_origins = canonical_designation_ids()
    if len(facts) != 12:
        _diag(
            diagnostics,
            "INVALID_ONE_SIX_FACT_COUNT",
            "one_six_facts",
            f"expected 12, got {len(facts)}",
        )
    if tuple(row.origin_designation_id for row in facts) != canonical_origins:
        _diag(
            diagnostics,
            "NON_CANONICAL_ONE_SIX_ORIGIN_ORDER",
            "one_six_facts",
            "facts must follow the frozen V1 palace designation order exactly once",
        )
    for index, row in enumerate(facts):
        path = f"one_six_facts[{index}]"
        if row.source_technique_id != ONE_SIX_SOURCE_TECHNIQUE_ID:
            _diag(
                diagnostics,
                "INVALID_ONE_SIX_SOURCE_TECHNIQUE",
                f"{path}.source_technique_id",
                f"expected {ONE_SIX_SOURCE_TECHNIQUE_ID}",
            )
        if row.relative_role_designation_id != "HEALTH":
            _diag(
                diagnostics,
                "INVALID_ONE_SIX_RELATIVE_ROLE",
                f"{path}.relative_role_designation_id",
                "relative ordinal 6 must carry HEALTH",
            )
        if row.relative_ordinal != ONE_SIX_RELATIVE_ORDINAL:
            _diag(
                diagnostics,
                "INVALID_ONE_SIX_RELATIVE_ORDINAL",
                f"{path}.relative_ordinal",
                f"expected {ONE_SIX_RELATIVE_ORDINAL}, got {row.relative_ordinal}",
            )
        if row.clockwise_offset != ONE_SIX_CLOCKWISE_OFFSET:
            _diag(
                diagnostics,
                "INVALID_ONE_SIX_CLOCKWISE_OFFSET",
                f"{path}.clockwise_offset",
                f"expected {ONE_SIX_CLOCKWISE_OFFSET}, got {row.clockwise_offset}",
            )
        if row.semantic_scope != ONE_SIX_SEMANTIC_SCOPE:
            _diag(
                diagnostics,
                "INVALID_ONE_SIX_SEMANTIC_SCOPE",
                f"{path}.semantic_scope",
                f"expected {ONE_SIX_SEMANTIC_SCOPE}",
            )
        if row.direct_event_permission or row.direct_endpoint_permission:
            _diag(
                diagnostics,
                "ILLEGAL_ONE_SIX_RESULT_PERMISSION",
                path,
                "one-six identity must not directly prove an event or endpoint",
            )

    try:
        expected_facts = project_one_six_common_roots(r2_state)
    except OneSixProjectionError as exc:
        _diag(diagnostics, exc.diagnostic_code, "r2_state.frame_facts", str(exc))
    else:
        if facts != expected_facts:
            _diag(
                diagnostics,
                "ONE_SIX_FACT_PROJECTION_MISMATCH",
                "one_six_facts",
                "facts do not equal the canonical S04 projection over R2 ordinal 6",
            )

    return OneSixIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=ONE_SIX_INTEGRITY_ALGORITHM_ID,
        algorithm_version=ONE_SIX_INTEGRITY_ALGORITHM_VERSION,
    )


def validate_one_six_state(
    r2_state: RelativePalaceFrameState,
    state: OneSixCommonRootState,
) -> OneSixIntegrityReport:
    base = validate_one_six_components(
        r2_state,
        state.profile,
        state.time_layer,
        state.one_six_facts,
    )
    diagnostics = list(base.diagnostics)
    if state.schema != ONE_SIX_COMMON_ROOT_STATE_SCHEMA:
        _diag(
            diagnostics,
            "INVALID_ONE_SIX_SCHEMA_ID",
            "schema",
            f"expected {ONE_SIX_COMMON_ROOT_STATE_SCHEMA}",
        )
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
        or state.integrity.algorithm_id != ONE_SIX_INTEGRITY_ALGORITHM_ID
        or state.integrity.algorithm_version != ONE_SIX_INTEGRITY_ALGORITHM_VERSION
    ):
        _diag(
            diagnostics,
            "INVALID_EMBEDDED_ONE_SIX_INTEGRITY_REPORT",
            "integrity",
            "embedded report must be the canonical PASS report for V2-R7",
        )
    expected_hashes = one_six_hash_bundle(
        state.upstream_r2_fact_hash,
        state.upstream_r2_computation_hash,
        state.profile,
        state.time_layer,
        state.one_six_facts,
    )
    if state.hashes != expected_hashes:
        _diag(
            diagnostics,
            "ONE_SIX_HASH_BUNDLE_MISMATCH",
            "hashes",
            "stored hashes do not match canonical R7 fact/computation projections",
        )
    return OneSixIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=ONE_SIX_INTEGRITY_ALGORITHM_ID,
        algorithm_version=ONE_SIX_INTEGRITY_ALGORITHM_VERSION,
    )
