from __future__ import annotations

import re
from typing import Any, Iterable

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256
from fortune_training.ziwei_structural.r2.frame import canonical_designation_ids
from fortune_training.ziwei_structural.r2.models import RelativePalaceFrameState

from .models import (
    NAMED_STRUCTURAL_SEMANTIC_STATE_SCHEMA,
    NamedSemanticHashBundle,
    NamedSemanticIntegrityDiagnostic,
    NamedSemanticIntegrityReport,
    NamedStructuralSemanticState,
    OppositionAxisFact,
    SanfangSizhengFrameFact,
    TrineGroupFact,
)
from .profile import ResolvedNamedStructuralSemanticProfile


NAMED_SEMANTIC_INTEGRITY_ALGORITHM_ID = (
    "ZIWEI-NAMED-STRUCTURAL-SEMANTICS-INTEGRITY-HASH-V2-R4"
)
NAMED_SEMANTIC_INTEGRITY_ALGORITHM_VERSION = "1.0.0"
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")
_CANONICAL_IDS = canonical_designation_ids()
_ORDER = {designation_id: index for index, designation_id in enumerate(_CANONICAL_IDS)}


def _diag(
    diagnostics: list[NamedSemanticIntegrityDiagnostic],
    code: str,
    path: str,
    detail: str,
) -> None:
    diagnostics.append(NamedSemanticIntegrityDiagnostic(code=code, path=path, detail=detail))


def _address_fact(value) -> dict[str, Any]:
    return {"index": value.index, "branch": value.branch}


def _ordered_ids(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted(values, key=lambda item: _ORDER.get(item, 99)))


def _expected_key(prefix: str, values: Iterable[str]) -> str:
    return f"{prefix}:" + "|".join(_ordered_ids(values))


def _ordered_axes(facts: Iterable[OppositionAxisFact]) -> list[OppositionAxisFact]:
    return sorted(facts, key=lambda row: tuple(_ORDER.get(item, 99) for item in row.member_designation_ids))


def _ordered_groups(facts: Iterable[TrineGroupFact]) -> list[TrineGroupFact]:
    return sorted(facts, key=lambda row: tuple(_ORDER.get(item, 99) for item in row.member_designation_ids))


def _ordered_frames(facts: Iterable[SanfangSizhengFrameFact]) -> list[SanfangSizhengFrameFact]:
    return sorted(facts, key=lambda row: _ORDER.get(row.origin_designation_id, 99))


def named_semantic_fact_projection(
    upstream_r2_fact_hash: str,
    opposition_axes: Iterable[OppositionAxisFact],
    trine_groups: Iterable[TrineGroupFact],
    frames: Iterable[SanfangSizhengFrameFact],
) -> dict[str, Any]:
    return {
        "upstream_r2_fact_hash": upstream_r2_fact_hash,
        "opposition_axes": [
            {
                "axis_key": row.axis_key,
                "member_designation_ids": list(row.member_designation_ids),
                "member_addresses": [_address_fact(value) for value in row.member_addresses],
            }
            for row in _ordered_axes(opposition_axes)
        ],
        "trine_groups": [
            {
                "group_key": row.group_key,
                "member_designation_ids": list(row.member_designation_ids),
                "member_addresses": [_address_fact(value) for value in row.member_addresses],
            }
            for row in _ordered_groups(trine_groups)
        ],
        "sanfang_sizheng_frames": [
            {
                "origin_designation_id": row.origin_designation_id,
                "origin_address": _address_fact(row.origin_address),
                "trine_group_key": row.trine_group_key,
                "trine_partner_designation_ids": list(row.trine_partner_designation_ids),
                "trine_partner_addresses": [
                    _address_fact(value) for value in row.trine_partner_addresses
                ],
                "trine_offsets": list(row.trine_offsets),
                "opposition_axis_key": row.opposition_axis_key,
                "opposition_designation_id": row.opposition_designation_id,
                "opposition_address": _address_fact(row.opposition_address),
                "opposition_offset": row.opposition_offset,
            }
            for row in _ordered_frames(frames)
        ],
    }


def named_semantic_hash_bundle(
    upstream_r2_fact_hash: str,
    upstream_r2_computation_hash: str,
    profile: ResolvedNamedStructuralSemanticProfile,
    opposition_axes: Iterable[OppositionAxisFact],
    trine_groups: Iterable[TrineGroupFact],
    frames: Iterable[SanfangSizhengFrameFact],
) -> NamedSemanticHashBundle:
    fact_hash = object_sha256(
        named_semantic_fact_projection(
            upstream_r2_fact_hash,
            opposition_axes,
            trine_groups,
            frames,
        )
    )
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "upstream_r2_computation_hash": upstream_r2_computation_hash,
            "resolved_named_semantic_profile": json_value(profile),
            "semantic_source_lineage": {
                "canonical_source_id": profile.canonical_source_id,
                "canonical_source_sha256": profile.canonical_source_sha256,
                "canonical_manifest_object_sha256": profile.canonical_manifest_object_sha256,
                "semantic_rule_set_id": profile.semantic_rule_set_id,
                "semantic_rule_set_version": profile.semantic_rule_set_version,
            },
            "hash_algorithm": (
                f"{NAMED_SEMANTIC_INTEGRITY_ALGORITHM_ID}@"
                f"{NAMED_SEMANTIC_INTEGRITY_ALGORITHM_VERSION}"
            ),
        }
    )
    return NamedSemanticHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=NAMED_SEMANTIC_INTEGRITY_ALGORITHM_ID,
        algorithm_version=NAMED_SEMANTIC_INTEGRITY_ALGORITHM_VERSION,
    )


def validate_named_semantic_components(
    frame_state: RelativePalaceFrameState,
    profile: ResolvedNamedStructuralSemanticProfile,
    opposition_axes: tuple[OppositionAxisFact, ...],
    trine_groups: tuple[TrineGroupFact, ...],
    frames: tuple[SanfangSizhengFrameFact, ...],
) -> NamedSemanticIntegrityReport:
    diagnostics: list[NamedSemanticIntegrityDiagnostic] = []

    try:
        profile.validate()
    except ValueError as exc:
        _diag(diagnostics, "INVALID_R4_PROFILE", "profile", str(exc))

    if frame_state.integrity.status != "PASS":
        _diag(
            diagnostics,
            "UPSTREAM_R2_INTEGRITY_FAILED",
            "frame_state.integrity",
            "R2 frame state must carry PASS integrity",
        )
    if (
        frame_state.profile.profile_id != profile.upstream_r2_profile_id
        or frame_state.profile.profile_version != profile.upstream_r2_profile_version
    ):
        _diag(
            diagnostics,
            "UPSTREAM_R2_PROFILE_MISMATCH",
            "frame_state.profile",
            "R2 profile does not match the R4 binding",
        )
    if frame_state.profile.semantic_rule_set_id is not None:
        _diag(
            diagnostics,
            "R2_SEMANTIC_LAYER_MUTATED",
            "frame_state.profile.semantic_rule_set_id",
            "R2 must remain interpretation-free; R4 owns named semantics",
        )
    if not _SHA256_HEX.fullmatch(frame_state.hashes.fact_hash):
        _diag(diagnostics, "INVALID_UPSTREAM_R2_FACT_HASH", "frame_state.hashes.fact_hash", "invalid SHA256")
    if not _SHA256_HEX.fullmatch(frame_state.hashes.computation_hash):
        _diag(
            diagnostics,
            "INVALID_UPSTREAM_R2_COMPUTATION_HASH",
            "frame_state.hashes.computation_hash",
            "invalid SHA256",
        )

    r2_rows: dict[str, dict[int, Any]] = {designation_id: {} for designation_id in _CANONICAL_IDS}
    for row in frame_state.frame_facts:
        if row.origin_designation_id in r2_rows:
            r2_rows[row.origin_designation_id][row.clockwise_offset] = row
    if len(frame_state.frame_facts) != 144 or any(len(rows) != 12 for rows in r2_rows.values()):
        _diag(
            diagnostics,
            "INVALID_UPSTREAM_R2_DOMAIN",
            "frame_state.frame_facts",
            "R4 requires the complete 12x12 R2 frame domain",
        )

    address_by_id: dict[str, Any] = {}
    for designation_id, rows in r2_rows.items():
        if 0 in rows:
            address_by_id[designation_id] = rows[0].origin_address

    if len(opposition_axes) != 6:
        _diag(diagnostics, "INVALID_OPPOSITION_AXIS_COUNT", "opposition_axes", "expected exactly 6 axes")
    axis_keys: set[str] = set()
    axis_membership: dict[str, int] = {designation_id: 0 for designation_id in _CANONICAL_IDS}
    axes_by_key: dict[str, OppositionAxisFact] = {}
    for index, axis in enumerate(opposition_axes):
        path = f"opposition_axes[{index}]"
        if axis.axis_key in axis_keys:
            _diag(diagnostics, "DUPLICATE_OPPOSITION_AXIS_KEY", path, axis.axis_key)
        axis_keys.add(axis.axis_key)
        axes_by_key[axis.axis_key] = axis
        members = axis.member_designation_ids
        if len(set(members)) != 2 or any(item not in _ORDER for item in members):
            _diag(diagnostics, "INVALID_OPPOSITION_AXIS_MEMBERS", path, repr(members))
            continue
        expected_members = _ordered_ids(members)
        if members != expected_members:
            _diag(diagnostics, "NONCANONICAL_OPPOSITION_AXIS_ORDER", path, repr(members))
        if axis.axis_key != _expected_key("OPPOSITION_AXIS", members):
            _diag(diagnostics, "INVALID_OPPOSITION_AXIS_KEY", path, axis.axis_key)
        for designation_id in members:
            axis_membership[designation_id] += 1
        if len(axis.member_addresses) != 2:
            _diag(diagnostics, "INVALID_OPPOSITION_AXIS_ADDRESSES", path, "expected two addresses")
            continue
        for designation_id, address in zip(members, axis.member_addresses):
            if address_by_id.get(designation_id) != address:
                _diag(diagnostics, "OPPOSITION_AXIS_ADDRESS_MISMATCH", path, designation_id)
        first, second = members
        if 6 not in r2_rows.get(first, {}) or r2_rows[first][6].target_designation_id != second:
            _diag(diagnostics, "OPPOSITION_AXIS_NOT_PLUS_6", path, f"{first}->{second}")
        if 6 not in r2_rows.get(second, {}) or r2_rows[second][6].target_designation_id != first:
            _diag(diagnostics, "OPPOSITION_AXIS_NOT_INVOLUTION", path, f"{second}->{first}")
    for designation_id, count in axis_membership.items():
        if count != 1:
            _diag(
                diagnostics,
                "OPPOSITION_AXIS_COVERAGE_MISMATCH",
                "opposition_axes",
                f"{designation_id} appears {count} times",
            )

    if len(trine_groups) != 4:
        _diag(diagnostics, "INVALID_TRINE_GROUP_COUNT", "trine_groups", "expected exactly 4 groups")
    group_keys: set[str] = set()
    group_membership: dict[str, int] = {designation_id: 0 for designation_id in _CANONICAL_IDS}
    groups_by_key: dict[str, TrineGroupFact] = {}
    for index, group in enumerate(trine_groups):
        path = f"trine_groups[{index}]"
        if group.group_key in group_keys:
            _diag(diagnostics, "DUPLICATE_TRINE_GROUP_KEY", path, group.group_key)
        group_keys.add(group.group_key)
        groups_by_key[group.group_key] = group
        members = group.member_designation_ids
        if len(set(members)) != 3 or any(item not in _ORDER for item in members):
            _diag(diagnostics, "INVALID_TRINE_GROUP_MEMBERS", path, repr(members))
            continue
        if members != _ordered_ids(members):
            _diag(diagnostics, "NONCANONICAL_TRINE_GROUP_ORDER", path, repr(members))
        if group.group_key != _expected_key("TRINE_GROUP", members):
            _diag(diagnostics, "INVALID_TRINE_GROUP_KEY", path, group.group_key)
        for designation_id in members:
            group_membership[designation_id] += 1
        if len(group.member_addresses) != 3:
            _diag(diagnostics, "INVALID_TRINE_GROUP_ADDRESSES", path, "expected three addresses")
            continue
        for designation_id, address in zip(members, group.member_addresses):
            if address_by_id.get(designation_id) != address:
                _diag(diagnostics, "TRINE_GROUP_ADDRESS_MISMATCH", path, designation_id)
        member_set = set(members)
        for designation_id in members:
            rows = r2_rows.get(designation_id, {})
            if not {0, 4, 8}.issubset(rows):
                _diag(diagnostics, "TRINE_GROUP_MISSING_R2_OFFSETS", path, designation_id)
                continue
            orbit = {
                rows[0].target_designation_id,
                rows[4].target_designation_id,
                rows[8].target_designation_id,
            }
            if orbit != member_set:
                _diag(diagnostics, "TRINE_GROUP_NOT_Z12_ORBIT", path, designation_id)
    for designation_id, count in group_membership.items():
        if count != 1:
            _diag(
                diagnostics,
                "TRINE_GROUP_COVERAGE_MISMATCH",
                "trine_groups",
                f"{designation_id} appears {count} times",
            )

    if len(frames) != 12:
        _diag(diagnostics, "INVALID_SANFANG_SIZHENG_FRAME_COUNT", "sanfang_sizheng_frames", "expected 12 frames")
    frame_origins: set[str] = set()
    for index, frame in enumerate(frames):
        path = f"sanfang_sizheng_frames[{index}]"
        origin = frame.origin_designation_id
        if origin in frame_origins:
            _diag(diagnostics, "DUPLICATE_SANFANG_SIZHENG_ORIGIN", path, origin)
        frame_origins.add(origin)
        if origin not in r2_rows or not {0, 4, 6, 8}.issubset(r2_rows[origin]):
            _diag(diagnostics, "INVALID_SANFANG_SIZHENG_ORIGIN", path, origin)
            continue
        rows = r2_rows[origin]
        expected_trines = (rows[4].target_designation_id, rows[8].target_designation_id)
        expected_trine_addresses = (rows[4].target_address, rows[8].target_address)
        if frame.origin_address != rows[0].origin_address:
            _diag(diagnostics, "SANFANG_SIZHENG_ORIGIN_ADDRESS_MISMATCH", path, origin)
        if frame.trine_partner_designation_ids != expected_trines:
            _diag(diagnostics, "SANFANG_SIZHENG_TRINE_TARGET_MISMATCH", path, repr(frame.trine_partner_designation_ids))
        if frame.trine_partner_addresses != expected_trine_addresses:
            _diag(diagnostics, "SANFANG_SIZHENG_TRINE_ADDRESS_MISMATCH", path, origin)
        if frame.trine_offsets != (4, 8):
            _diag(diagnostics, "SANFANG_SIZHENG_TRINE_OFFSET_MISMATCH", path, repr(frame.trine_offsets))
        if frame.opposition_designation_id != rows[6].target_designation_id:
            _diag(diagnostics, "SANFANG_SIZHENG_OPPOSITION_TARGET_MISMATCH", path, frame.opposition_designation_id)
        if frame.opposition_address != rows[6].target_address or frame.opposition_offset != 6:
            _diag(diagnostics, "SANFANG_SIZHENG_OPPOSITION_GEOMETRY_MISMATCH", path, origin)
        group = groups_by_key.get(frame.trine_group_key)
        if group is None or origin not in group.member_designation_ids or not set(expected_trines).issubset(group.member_designation_ids):
            _diag(diagnostics, "SANFANG_SIZHENG_TRINE_GROUP_REFERENCE_MISMATCH", path, frame.trine_group_key)
        axis = axes_by_key.get(frame.opposition_axis_key)
        if axis is None or set(axis.member_designation_ids) != {origin, rows[6].target_designation_id}:
            _diag(diagnostics, "SANFANG_SIZHENG_AXIS_REFERENCE_MISMATCH", path, frame.opposition_axis_key)
        members = {origin, *expected_trines, rows[6].target_designation_id}
        if len(members) != 4:
            _diag(diagnostics, "SANFANG_SIZHENG_MEMBER_COLLISION", path, repr(members))
    if frame_origins != set(_CANONICAL_IDS):
        _diag(diagnostics, "SANFANG_SIZHENG_ORIGIN_COVERAGE_MISMATCH", "sanfang_sizheng_frames", repr(sorted(frame_origins)))

    status = "PASS" if not diagnostics else "FAIL"
    return NamedSemanticIntegrityReport(
        status=status,
        diagnostics=tuple(diagnostics),
        algorithm_id=NAMED_SEMANTIC_INTEGRITY_ALGORITHM_ID,
        algorithm_version=NAMED_SEMANTIC_INTEGRITY_ALGORITHM_VERSION,
    )


def validate_named_semantic_state(
    frame_state: RelativePalaceFrameState,
    state: NamedStructuralSemanticState,
) -> NamedSemanticIntegrityReport:
    report = validate_named_semantic_components(
        frame_state,
        state.profile,
        state.opposition_axes,
        state.trine_groups,
        state.sanfang_sizheng_frames,
    )
    diagnostics = list(report.diagnostics)

    if state.schema != NAMED_STRUCTURAL_SEMANTIC_STATE_SCHEMA:
        _diag(diagnostics, "INVALID_R4_SCHEMA", "schema", state.schema)
    if state.upstream_r2_fact_hash != frame_state.hashes.fact_hash:
        _diag(diagnostics, "UPSTREAM_R2_FACT_HASH_MISMATCH", "upstream_r2_fact_hash", "state is not bound to supplied R2 FactHash")
    if state.upstream_r2_computation_hash != frame_state.hashes.computation_hash:
        _diag(
            diagnostics,
            "UPSTREAM_R2_COMPUTATION_HASH_MISMATCH",
            "upstream_r2_computation_hash",
            "state is not bound to supplied R2 ComputationHash",
        )

    expected_hashes = named_semantic_hash_bundle(
        frame_state.hashes.fact_hash,
        frame_state.hashes.computation_hash,
        state.profile,
        state.opposition_axes,
        state.trine_groups,
        state.sanfang_sizheng_frames,
    )
    if state.hashes != expected_hashes:
        _diag(diagnostics, "R4_HASH_MISMATCH", "hashes", "stored R4 hashes do not reproduce")

    status = "PASS" if not diagnostics else "FAIL"
    return NamedSemanticIntegrityReport(
        status=status,
        diagnostics=tuple(diagnostics),
        algorithm_id=NAMED_SEMANTIC_INTEGRITY_ALGORITHM_ID,
        algorithm_version=NAMED_SEMANTIC_INTEGRITY_ALGORITHM_VERSION,
    )
