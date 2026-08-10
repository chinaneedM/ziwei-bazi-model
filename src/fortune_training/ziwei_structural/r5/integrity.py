from __future__ import annotations

import re
from typing import Any, Iterable

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256
from fortune_training.ziwei_structural.r2.frame import canonical_designation_ids
from fortune_training.ziwei_structural.r3 import (
    BORROW_PROJECTION_INTEGRITY_ALGORITHM_ID,
    BORROW_PROJECTION_INTEGRITY_ALGORITHM_VERSION,
    BorrowProjectionState,
    borrow_projection_hash_bundle,
)
from fortune_training.ziwei_structural.r4 import (
    NAMED_SEMANTIC_INTEGRITY_ALGORITHM_ID,
    NAMED_SEMANTIC_INTEGRITY_ALGORITHM_VERSION,
    NamedStructuralSemanticState,
    named_semantic_hash_bundle,
)

from .composition import ResolvedStructuralComposer, physical_source_address, r3_member_key
from .models import (
    RESOLVED_MEMBER_OFFSETS,
    RESOLVED_MEMBER_ROLE_BY_OFFSET,
    RESOLVED_STRUCTURAL_VIEW_STATE_SCHEMA,
    ResolvedSanfangSizhengFrameFact,
    ResolvedStructuralHashBundle,
    ResolvedStructuralIntegrityDiagnostic,
    ResolvedStructuralIntegrityReport,
    ResolvedSanfangSizhengViewState,
)
from .profile import ResolvedStructuralCompositionProfile


RESOLVED_STRUCTURAL_INTEGRITY_ALGORITHM_ID = (
    "ZIWEI-RESOLVED-STRUCTURAL-INTEGRITY-HASH-V2-R5"
)
RESOLVED_STRUCTURAL_INTEGRITY_ALGORITHM_VERSION = "1.0.0"
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")
_CANONICAL_IDS = canonical_designation_ids()
_ORIGIN_ORDER = {designation_id: index for index, designation_id in enumerate(_CANONICAL_IDS)}
_OFFSET_ORDER = {offset: index for index, offset in enumerate(RESOLVED_MEMBER_OFFSETS)}


def _diag(
    diagnostics: list[ResolvedStructuralIntegrityDiagnostic],
    code: str,
    path: str,
    detail: str,
) -> None:
    diagnostics.append(ResolvedStructuralIntegrityDiagnostic(code=code, path=path, detail=detail))


def _address_fact(value) -> dict[str, Any] | None:
    if value is None:
        return None
    return {"index": value.index, "branch": value.branch}


def _ordered_frames(
    frames: Iterable[ResolvedSanfangSizhengFrameFact],
) -> list[ResolvedSanfangSizhengFrameFact]:
    return sorted(frames, key=lambda row: _ORIGIN_ORDER.get(row.origin_designation_id, 99))


def _ordered_members(frame: ResolvedSanfangSizhengFrameFact):
    return sorted(frame.members, key=lambda row: _OFFSET_ORDER.get(row.member_offset, 99))


def resolved_structural_fact_projection(
    upstream_r3_fact_hash: str,
    upstream_r4_fact_hash: str,
    time_layer: str,
    frames: Iterable[ResolvedSanfangSizhengFrameFact],
) -> dict[str, Any]:
    return {
        "upstream_r3_fact_hash": upstream_r3_fact_hash,
        "upstream_r4_fact_hash": upstream_r4_fact_hash,
        "time_layer": time_layer,
        "frames": [
            {
                "origin_designation_id": frame.origin_designation_id,
                "origin_address": _address_fact(frame.origin_address),
                "trine_group_key": frame.trine_group_key,
                "opposition_axis_key": frame.opposition_axis_key,
                "members": [
                    {
                        "semantic_role": member.semantic_role,
                        "member_offset": member.member_offset,
                        "target_designation_id": member.target_designation_id,
                        "target_raw_address": _address_fact(member.target_raw_address),
                        "closure_status": member.closure_status,
                        "borrowed_from_raw_address": _address_fact(
                            member.borrowed_from_raw_address
                        ),
                        "physical_source_address": _address_fact(member.physical_source_address),
                        "structure_physical_key": member.structure_physical_key,
                        "r3_member_key": member.r3_member_key,
                    }
                    for member in _ordered_members(frame)
                ],
            }
            for frame in _ordered_frames(frames)
        ],
    }


def resolved_structural_hash_bundle(
    upstream_r3_fact_hash: str,
    upstream_r3_computation_hash: str,
    upstream_r4_fact_hash: str,
    upstream_r4_computation_hash: str,
    profile: ResolvedStructuralCompositionProfile,
    time_layer: str,
    frames: Iterable[ResolvedSanfangSizhengFrameFact],
) -> ResolvedStructuralHashBundle:
    fact_hash = object_sha256(
        resolved_structural_fact_projection(
            upstream_r3_fact_hash,
            upstream_r4_fact_hash,
            time_layer,
            frames,
        )
    )
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "upstream_r3_computation_hash": upstream_r3_computation_hash,
            "upstream_r4_computation_hash": upstream_r4_computation_hash,
            "resolved_r5_profile": json_value(profile),
            "hash_algorithm": (
                f"{RESOLVED_STRUCTURAL_INTEGRITY_ALGORITHM_ID}@"
                f"{RESOLVED_STRUCTURAL_INTEGRITY_ALGORITHM_VERSION}"
            ),
        }
    )
    return ResolvedStructuralHashBundle(
        fact_hash=fact_hash,
        computation_hash=computation_hash,
        algorithm_id=RESOLVED_STRUCTURAL_INTEGRITY_ALGORITHM_ID,
        algorithm_version=RESOLVED_STRUCTURAL_INTEGRITY_ALGORITHM_VERSION,
    )


def _validate_upstream_states(
    r3_state: BorrowProjectionState,
    r4_state: NamedStructuralSemanticState,
    profile: ResolvedStructuralCompositionProfile,
    diagnostics: list[ResolvedStructuralIntegrityDiagnostic],
) -> None:
    try:
        profile.validate()
    except ValueError as exc:
        _diag(diagnostics, "INVALID_R5_PROFILE", "profile", str(exc))

    try:
        r3_state.profile.validate()
    except ValueError as exc:
        _diag(diagnostics, "UPSTREAM_R3_PROFILE_INVALID", "r3_state.profile", str(exc))
    try:
        r4_state.profile.validate()
    except ValueError as exc:
        _diag(diagnostics, "UPSTREAM_R4_PROFILE_INVALID", "r4_state.profile", str(exc))

    if (
        r3_state.profile.profile_id != profile.upstream_r3_profile_id
        or r3_state.profile.profile_version != profile.upstream_r3_profile_version
    ):
        _diag(
            diagnostics,
            "UPSTREAM_R3_PROFILE_MISMATCH",
            "r3_state.profile",
            "R3 profile does not match R5 binding",
        )
    if (
        r4_state.profile.profile_id != profile.upstream_r4_profile_id
        or r4_state.profile.profile_version != profile.upstream_r4_profile_version
    ):
        _diag(
            diagnostics,
            "UPSTREAM_R4_PROFILE_MISMATCH",
            "r4_state.profile",
            "R4 profile does not match R5 binding",
        )

    if r3_state.time_layer != "NATAL" or r3_state.time_layer != profile.supported_time_layer:
        _diag(
            diagnostics,
            "UNSUPPORTED_R5_TIME_LAYER",
            "r3_state.time_layer",
            f"R5 currently supports NATAL only, got {r3_state.time_layer}",
        )

    if (
        r3_state.integrity.status != "PASS"
        or r3_state.integrity.diagnostics
        or r3_state.integrity.algorithm_id != BORROW_PROJECTION_INTEGRITY_ALGORITHM_ID
        or r3_state.integrity.algorithm_version
        != BORROW_PROJECTION_INTEGRITY_ALGORITHM_VERSION
    ):
        _diag(
            diagnostics,
            "UPSTREAM_R3_INTEGRITY_LINEAGE_INVALID",
            "r3_state.integrity",
            "R3 must carry the frozen canonical PASS integrity report",
        )
    if (
        r4_state.integrity.status != "PASS"
        or r4_state.integrity.diagnostics
        or r4_state.integrity.algorithm_id != NAMED_SEMANTIC_INTEGRITY_ALGORITHM_ID
        or r4_state.integrity.algorithm_version != NAMED_SEMANTIC_INTEGRITY_ALGORITHM_VERSION
    ):
        _diag(
            diagnostics,
            "UPSTREAM_R4_INTEGRITY_LINEAGE_INVALID",
            "r4_state.integrity",
            "R4 must carry the frozen canonical PASS integrity report",
        )

    expected_r3_hashes = borrow_projection_hash_bundle(
        r3_state.upstream_relative_frame_fact_hash,
        r3_state.upstream_relative_frame_computation_hash,
        r3_state.profile,
        r3_state.time_layer,
        r3_state.member_facts,
    )
    if r3_state.hashes != expected_r3_hashes:
        _diag(
            diagnostics,
            "UPSTREAM_R3_HASH_MISMATCH",
            "r3_state.hashes",
            "R3 facts/profile/upstream lineage do not reproduce stored hashes",
        )

    expected_r4_hashes = named_semantic_hash_bundle(
        r4_state.upstream_r2_fact_hash,
        r4_state.upstream_r2_computation_hash,
        r4_state.profile,
        r4_state.opposition_axes,
        r4_state.trine_groups,
        r4_state.sanfang_sizheng_frames,
    )
    if r4_state.hashes != expected_r4_hashes:
        _diag(
            diagnostics,
            "UPSTREAM_R4_HASH_MISMATCH",
            "r4_state.hashes",
            "R4 facts/profile/upstream lineage do not reproduce stored hashes",
        )

    if r3_state.upstream_relative_frame_fact_hash != r4_state.upstream_r2_fact_hash:
        _diag(
            diagnostics,
            "CROSS_R3_R4_R2_FACT_HASH_MISMATCH",
            "upstream_r2_fact_hash",
            "R3 and R4 do not descend from the same R2 FactHash",
        )
    if (
        r3_state.upstream_relative_frame_computation_hash
        != r4_state.upstream_r2_computation_hash
    ):
        _diag(
            diagnostics,
            "CROSS_R3_R4_R2_COMPUTATION_HASH_MISMATCH",
            "upstream_r2_computation_hash",
            "R3 and R4 do not descend from the same R2 ComputationHash",
        )


def validate_resolved_structural_components(
    r3_state: BorrowProjectionState,
    r4_state: NamedStructuralSemanticState,
    profile: ResolvedStructuralCompositionProfile,
    time_layer: str,
    frames: tuple[ResolvedSanfangSizhengFrameFact, ...],
) -> ResolvedStructuralIntegrityReport:
    diagnostics: list[ResolvedStructuralIntegrityDiagnostic] = []
    _validate_upstream_states(r3_state, r4_state, profile, diagnostics)

    if time_layer != "NATAL" or time_layer != profile.supported_time_layer:
        _diag(
            diagnostics,
            "UNSUPPORTED_R5_TIME_LAYER",
            "time_layer",
            f"R5 currently supports NATAL only, got {time_layer}",
        )
    if time_layer != r3_state.time_layer:
        _diag(
            diagnostics,
            "R3_R5_TIME_LAYER_MISMATCH",
            "time_layer",
            "R5 time layer must equal R3 time layer",
        )

    if len(frames) != 12:
        _diag(
            diagnostics,
            "INVALID_RESOLVED_FRAME_COUNT",
            "frames",
            f"expected 12 frames, got {len(frames)}",
        )

    actual_origins = [frame.origin_designation_id for frame in frames]
    if actual_origins != list(_CANONICAL_IDS):
        _diag(
            diagnostics,
            "NONCANONICAL_RESOLVED_FRAME_ORDER",
            "frames",
            "frames must follow frozen natal designation order",
        )
    if len(set(actual_origins)) != len(actual_origins):
        _diag(diagnostics, "DUPLICATE_RESOLVED_FRAME_ORIGIN", "frames", "origins must be unique")

    r3_by_key = {
        (row.evaluation_origin_designation_id, row.member_offset): row
        for row in r3_state.member_facts
    }
    r4_frames = {
        row.origin_designation_id: row for row in r4_state.sanfang_sizheng_frames
    }
    r4_axes = {row.axis_key: row for row in r4_state.opposition_axes}
    r4_groups = {row.group_key: row for row in r4_state.trine_groups}

    for frame_index, frame in enumerate(frames):
        path = f"frames[{frame_index}]"
        semantic = r4_frames.get(frame.origin_designation_id)
        if semantic is None:
            _diag(diagnostics, "MISSING_R4_FRAME_REFERENCE", path, frame.origin_designation_id)
            continue
        if frame.origin_address != semantic.origin_address:
            _diag(diagnostics, "RESOLVED_ORIGIN_ADDRESS_MISMATCH", path, frame.origin_designation_id)
        if frame.trine_group_key != semantic.trine_group_key:
            _diag(diagnostics, "RESOLVED_TRINE_GROUP_KEY_MISMATCH", path, frame.trine_group_key)
        if frame.opposition_axis_key != semantic.opposition_axis_key:
            _diag(diagnostics, "RESOLVED_OPPOSITION_AXIS_KEY_MISMATCH", path, frame.opposition_axis_key)

        group = r4_groups.get(frame.trine_group_key)
        axis = r4_axes.get(frame.opposition_axis_key)
        expected_group_members = {
            semantic.origin_designation_id,
            *semantic.trine_partner_designation_ids,
        }
        if group is None or set(group.member_designation_ids) != expected_group_members:
            _diag(diagnostics, "RESOLVED_TRINE_GROUP_REFERENCE_INVALID", path, frame.trine_group_key)
        if axis is None or set(axis.member_designation_ids) != {
            semantic.origin_designation_id,
            semantic.opposition_designation_id,
        }:
            _diag(
                diagnostics,
                "RESOLVED_OPPOSITION_AXIS_REFERENCE_INVALID",
                path,
                frame.opposition_axis_key,
            )

        if len(frame.members) != 4:
            _diag(diagnostics, "INVALID_RESOLVED_MEMBER_COUNT", f"{path}.members", "expected 4")
            continue
        offsets = [member.member_offset for member in frame.members]
        if offsets != list(RESOLVED_MEMBER_OFFSETS):
            _diag(
                diagnostics,
                "NONCANONICAL_RESOLVED_MEMBER_ORDER",
                f"{path}.members",
                f"expected {RESOLVED_MEMBER_OFFSETS}, got {tuple(offsets)}",
            )
        if len(set(offsets)) != len(offsets):
            _diag(diagnostics, "DUPLICATE_RESOLVED_MEMBER_OFFSET", f"{path}.members", repr(offsets))

        expected_targets = {
            0: (semantic.origin_designation_id, semantic.origin_address),
            4: (
                semantic.trine_partner_designation_ids[0],
                semantic.trine_partner_addresses[0],
            ),
            6: (semantic.opposition_designation_id, semantic.opposition_address),
            8: (
                semantic.trine_partner_designation_ids[1],
                semantic.trine_partner_addresses[1],
            ),
        }
        for member_index, member in enumerate(frame.members):
            member_path = f"{path}.members[{member_index}]"
            expected_role = RESOLVED_MEMBER_ROLE_BY_OFFSET.get(member.member_offset)
            if member.semantic_role != expected_role:
                _diag(
                    diagnostics,
                    "RESOLVED_ROLE_OFFSET_MISMATCH",
                    member_path,
                    f"{member.semantic_role}/{member.member_offset}",
                )
                continue
            expected_target = expected_targets.get(member.member_offset)
            if expected_target is None or (
                member.target_designation_id,
                member.target_raw_address,
            ) != expected_target:
                _diag(diagnostics, "RESOLVED_R4_TARGET_MISMATCH", member_path, member.target_designation_id)

            r3_member = r3_by_key.get((frame.origin_designation_id, member.member_offset))
            if r3_member is None:
                _diag(diagnostics, "MISSING_R3_MEMBER_REFERENCE", member_path, member.r3_member_key)
                continue
            if member.r3_member_key != r3_member_key(
                frame.origin_designation_id, member.member_offset
            ):
                _diag(diagnostics, "INVALID_R3_MEMBER_KEY", member_path, member.r3_member_key)
            fields = (
                ("target_designation_id", member.target_designation_id, r3_member.target_designation_id),
                ("target_raw_address", member.target_raw_address, r3_member.target_raw_address),
                ("closure_status", member.closure_status, r3_member.closure_status),
                (
                    "borrowed_from_raw_address",
                    member.borrowed_from_raw_address,
                    r3_member.borrowed_from_raw_address,
                ),
                (
                    "structure_physical_key",
                    member.structure_physical_key,
                    r3_member.structure_physical_key,
                ),
                (
                    "physical_source_address",
                    member.physical_source_address,
                    physical_source_address(r3_member),
                ),
            )
            for field_name, actual, expected in fields:
                if actual != expected:
                    _diag(
                        diagnostics,
                        "RESOLVED_R3_REFERENCE_MISMATCH",
                        f"{member_path}.{field_name}",
                        "R5 must preserve the referenced R3 physical resolution exactly",
                    )

    expected_frames: tuple[ResolvedSanfangSizhengFrameFact, ...] = ()
    if not diagnostics:
        try:
            expected_frames = ResolvedStructuralComposer().compose(r3_state, r4_state)
        except ValueError as exc:
            _diag(diagnostics, "RESOLVED_EXPECTED_COMPOSITION_FAILED", "frames", str(exc))
    if expected_frames and frames != expected_frames:
        _diag(
            diagnostics,
            "RESOLVED_COMPOSITION_MISMATCH",
            "frames",
            "supplied R5 frames do not equal canonical R3 x R4 composition",
        )

    return ResolvedStructuralIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=RESOLVED_STRUCTURAL_INTEGRITY_ALGORITHM_ID,
        algorithm_version=RESOLVED_STRUCTURAL_INTEGRITY_ALGORITHM_VERSION,
    )


def validate_resolved_structural_state(
    r3_state: BorrowProjectionState,
    r4_state: NamedStructuralSemanticState,
    state: ResolvedSanfangSizhengViewState,
) -> ResolvedStructuralIntegrityReport:
    base = validate_resolved_structural_components(
        r3_state,
        r4_state,
        state.profile,
        state.time_layer,
        state.frames,
    )
    diagnostics = list(base.diagnostics)

    if state.schema != RESOLVED_STRUCTURAL_VIEW_STATE_SCHEMA:
        _diag(
            diagnostics,
            "INVALID_R5_SCHEMA_ID",
            "schema",
            f"expected {RESOLVED_STRUCTURAL_VIEW_STATE_SCHEMA}",
        )

    bindings = (
        ("upstream_r3_fact_hash", state.upstream_r3_fact_hash, r3_state.hashes.fact_hash),
        (
            "upstream_r3_computation_hash",
            state.upstream_r3_computation_hash,
            r3_state.hashes.computation_hash,
        ),
        ("upstream_r4_fact_hash", state.upstream_r4_fact_hash, r4_state.hashes.fact_hash),
        (
            "upstream_r4_computation_hash",
            state.upstream_r4_computation_hash,
            r4_state.hashes.computation_hash,
        ),
    )
    for label, actual, expected in bindings:
        if actual != expected:
            _diag(diagnostics, "UPSTREAM_R5_BINDING_MISMATCH", label, "state is bound to a different upstream")
        if not _SHA256_HEX.fullmatch(actual):
            _diag(diagnostics, "INVALID_UPSTREAM_R5_HASH", label, "expected lowercase SHA-256 hex")

    if (
        state.integrity.status != "PASS"
        or state.integrity.diagnostics
        or state.integrity.algorithm_id != RESOLVED_STRUCTURAL_INTEGRITY_ALGORITHM_ID
        or state.integrity.algorithm_version != RESOLVED_STRUCTURAL_INTEGRITY_ALGORITHM_VERSION
    ):
        _diag(
            diagnostics,
            "INVALID_EMBEDDED_R5_INTEGRITY_REPORT",
            "integrity",
            "embedded report must be canonical PASS report for V2-R5",
        )

    expected_hashes = resolved_structural_hash_bundle(
        state.upstream_r3_fact_hash,
        state.upstream_r3_computation_hash,
        state.upstream_r4_fact_hash,
        state.upstream_r4_computation_hash,
        state.profile,
        state.time_layer,
        state.frames,
    )
    if state.hashes != expected_hashes:
        _diag(
            diagnostics,
            "R5_HASH_MISMATCH",
            "hashes",
            "stored R5 hashes do not reproduce from canonical composition",
        )

    return ResolvedStructuralIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=RESOLVED_STRUCTURAL_INTEGRITY_ALGORITHM_ID,
        algorithm_version=RESOLVED_STRUCTURAL_INTEGRITY_ALGORITHM_VERSION,
    )
