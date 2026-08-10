from __future__ import annotations

import re
from typing import Any, Iterable

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256
from fortune_training.ziwei_chart.registries import address

from .models import (
    STRUCTURAL_STATE_SCHEMA,
    AddressOffsetFact,
    StructuralHashBundle,
    StructuralIntegrityDiagnostic,
    StructuralIntegrityReport,
    StructuralState,
)
from .profile import ResolvedZiweiStructuralProfile


STRUCTURAL_INTEGRITY_ALGORITHM_ID = "ZIWEI-STRUCTURAL-INTEGRITY-HASH-V2-R1"
STRUCTURAL_INTEGRITY_ALGORITHM_VERSION = "1.0.0"
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")


def _diag(
    diagnostics: list[StructuralIntegrityDiagnostic],
    code: str,
    path: str,
    detail: str,
) -> None:
    diagnostics.append(StructuralIntegrityDiagnostic(code=code, path=path, detail=detail))


def _address_fact(value) -> dict[str, Any]:
    return {"index": value.index, "branch": value.branch}


def _ordered_facts(facts: Iterable[AddressOffsetFact]) -> list[AddressOffsetFact]:
    return sorted(facts, key=lambda row: (row.source.index, row.target.index))


def structural_fact_projection(
    upstream_natal_fact_hash: str,
    facts: Iterable[AddressOffsetFact],
) -> dict[str, Any]:
    return {
        "upstream_natal_fact_hash": upstream_natal_fact_hash,
        "topology_facts": [
            {
                "source": _address_fact(row.source),
                "target": _address_fact(row.target),
                "clockwise_offset": row.clockwise_offset,
            }
            for row in _ordered_facts(facts)
        ],
    }


def structural_hash_bundle(
    upstream_natal_fact_hash: str,
    upstream_natal_computation_hash: str,
    profile: ResolvedZiweiStructuralProfile,
    facts: Iterable[AddressOffsetFact],
) -> StructuralHashBundle:
    fact_hash = object_sha256(structural_fact_projection(upstream_natal_fact_hash, facts))
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "upstream_natal_computation_hash": upstream_natal_computation_hash,
            "resolved_structural_profile": json_value(profile),
            "hash_algorithm": (
                f"{STRUCTURAL_INTEGRITY_ALGORITHM_ID}@"
                f"{STRUCTURAL_INTEGRITY_ALGORITHM_VERSION}"
            ),
        }
    )
    return StructuralHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=STRUCTURAL_INTEGRITY_ALGORITHM_ID,
        algorithm_version=STRUCTURAL_INTEGRITY_ALGORITHM_VERSION,
    )


def validate_structural_components(
    upstream_natal_fact_hash: str,
    upstream_natal_computation_hash: str,
    profile: ResolvedZiweiStructuralProfile,
    facts: tuple[AddressOffsetFact, ...],
) -> StructuralIntegrityReport:
    diagnostics: list[StructuralIntegrityDiagnostic] = []

    try:
        profile.validate()
    except ValueError as exc:
        _diag(diagnostics, "INVALID_STRUCTURAL_PROFILE", "profile", str(exc))

    if not _SHA256_HEX.fullmatch(upstream_natal_fact_hash):
        _diag(
            diagnostics,
            "INVALID_UPSTREAM_NATAL_FACT_HASH",
            "upstream_natal_fact_hash",
            "expected lowercase SHA-256 hex",
        )
    if not _SHA256_HEX.fullmatch(upstream_natal_computation_hash):
        _diag(
            diagnostics,
            "INVALID_UPSTREAM_NATAL_COMPUTATION_HASH",
            "upstream_natal_computation_hash",
            "expected lowercase SHA-256 hex",
        )

    if len(facts) != 144:
        _diag(
            diagnostics,
            "INVALID_TOPOLOGY_FACT_COUNT",
            "topology_facts",
            f"expected 144 facts, got {len(facts)}",
        )

    pairs = [(row.source.index, row.target.index) for row in facts]
    if len(set(pairs)) != len(pairs):
        _diag(
            diagnostics,
            "DUPLICATE_TOPOLOGY_PAIR",
            "topology_facts",
            "source/target pairs must be unique",
        )

    expected_order = sorted(pairs)
    if pairs != expected_order:
        _diag(
            diagnostics,
            "NON_CANONICAL_TOPOLOGY_ORDER",
            "topology_facts",
            "facts must be ordered by source index then target index",
        )

    source_indices = {row.source.index for row in facts}
    target_indices = {row.target.index for row in facts}
    if source_indices != set(range(12)):
        _diag(
            diagnostics,
            "INVALID_SOURCE_ADDRESS_DOMAIN",
            "topology_facts",
            "source addresses must cover all 12 Z12 indices",
        )
    if target_indices != set(range(12)):
        _diag(
            diagnostics,
            "INVALID_TARGET_ADDRESS_DOMAIN",
            "topology_facts",
            "target addresses must cover all 12 Z12 indices",
        )

    targets_by_source: dict[int, set[int]] = {index: set() for index in range(12)}
    for index, row in enumerate(facts):
        for label, value in (("source", row.source), ("target", row.target)):
            canonical = address(value.index)
            if value != canonical:
                _diag(
                    diagnostics,
                    "NON_CANONICAL_Z12_ADDRESS",
                    f"topology_facts[{index}].{label}",
                    f"expected {canonical.index}:{canonical.branch}",
                )
        targets_by_source.setdefault(row.source.index, set()).add(row.target.index)
        expected_offset = (row.target.index - row.source.index) % 12
        if row.clockwise_offset != expected_offset:
            _diag(
                diagnostics,
                "TOPOLOGY_OFFSET_MISMATCH",
                f"topology_facts[{index}].clockwise_offset",
                f"expected {expected_offset}, got {row.clockwise_offset}",
            )
        if row.source.index == row.target.index and row.clockwise_offset != 0:
            _diag(
                diagnostics,
                "IDENTITY_OFFSET_MISMATCH",
                f"topology_facts[{index}]",
                "self relation must have offset 0",
            )

    for source_index in range(12):
        if targets_by_source.get(source_index, set()) != set(range(12)):
            _diag(
                diagnostics,
                "INCOMPLETE_TARGET_COVERAGE",
                f"topology_facts[source={source_index}]",
                "each source must target all 12 addresses exactly once",
            )

    return StructuralIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=STRUCTURAL_INTEGRITY_ALGORITHM_ID,
        algorithm_version=STRUCTURAL_INTEGRITY_ALGORITHM_VERSION,
    )


def validate_structural_state(state: StructuralState) -> StructuralIntegrityReport:
    base = validate_structural_components(
        state.upstream_natal_fact_hash,
        state.upstream_natal_computation_hash,
        state.profile,
        state.topology_facts,
    )
    diagnostics = list(base.diagnostics)

    if state.schema != STRUCTURAL_STATE_SCHEMA:
        _diag(
            diagnostics,
            "INVALID_STRUCTURAL_SCHEMA_ID",
            "schema",
            f"expected {STRUCTURAL_STATE_SCHEMA}",
        )

    if (
        state.integrity.status != "PASS"
        or state.integrity.diagnostics
        or state.integrity.algorithm_id != STRUCTURAL_INTEGRITY_ALGORITHM_ID
        or state.integrity.algorithm_version != STRUCTURAL_INTEGRITY_ALGORITHM_VERSION
    ):
        _diag(
            diagnostics,
            "INVALID_EMBEDDED_INTEGRITY_REPORT",
            "integrity",
            "embedded report must be the canonical PASS report for this runtime",
        )

    expected_hashes = structural_hash_bundle(
        state.upstream_natal_fact_hash,
        state.upstream_natal_computation_hash,
        state.profile,
        state.topology_facts,
    )
    if state.hashes.algorithm_id != STRUCTURAL_INTEGRITY_ALGORITHM_ID:
        _diag(
            diagnostics,
            "INVALID_HASH_ALGORITHM_ID",
            "hashes.algorithm_id",
            state.hashes.algorithm_id,
        )
    if state.hashes.algorithm_version != STRUCTURAL_INTEGRITY_ALGORITHM_VERSION:
        _diag(
            diagnostics,
            "INVALID_HASH_ALGORITHM_VERSION",
            "hashes.algorithm_version",
            state.hashes.algorithm_version,
        )
    if state.hashes.fact_hash != expected_hashes.fact_hash:
        _diag(
            diagnostics,
            "STRUCTURAL_FACT_HASH_MISMATCH",
            "hashes.fact_hash",
            "stored hash does not match canonical structural fact projection",
        )
    if state.hashes.computation_hash != expected_hashes.computation_hash:
        _diag(
            diagnostics,
            "STRUCTURAL_COMPUTATION_HASH_MISMATCH",
            "hashes.computation_hash",
            "stored hash does not match structural computation lineage",
        )

    return StructuralIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=STRUCTURAL_INTEGRITY_ALGORITHM_ID,
        algorithm_version=STRUCTURAL_INTEGRITY_ALGORITHM_VERSION,
    )
