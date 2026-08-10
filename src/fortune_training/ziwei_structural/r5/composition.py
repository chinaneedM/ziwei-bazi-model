from __future__ import annotations

from fortune_training.ziwei_structural.r2.frame import canonical_designation_ids
from fortune_training.ziwei_structural.r3.models import BorrowProjectionState
from fortune_training.ziwei_structural.r4.models import NamedStructuralSemanticState

from .models import (
    RESOLVED_MEMBER_OFFSETS,
    RESOLVED_MEMBER_ROLE_BY_OFFSET,
    ResolvedSanfangSizhengFrameFact,
    ResolvedStructuralMemberRef,
)


class ResolvedStructuralCompositionError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


def r3_member_key(origin_designation_id: str, member_offset: int) -> str:
    return f"R3_MEMBER:{origin_designation_id}:{member_offset}"


def physical_source_address(member):
    if member.closure_status == "DIRECT_PHYSICAL":
        return member.target_raw_address
    if member.closure_status == "BORROWED_DIRECT":
        return member.borrowed_from_raw_address
    return None


class ResolvedStructuralComposer:
    """Pure R3 x R4 composition. No second borrow pass and no new semantic rule."""

    def compose(
        self,
        r3_state: BorrowProjectionState,
        r4_state: NamedStructuralSemanticState,
    ) -> tuple[ResolvedSanfangSizhengFrameFact, ...]:
        r3_by_key = {
            (row.evaluation_origin_designation_id, row.member_offset): row
            for row in r3_state.member_facts
        }
        r4_by_origin = {
            row.origin_designation_id: row for row in r4_state.sanfang_sizheng_frames
        }

        frames: list[ResolvedSanfangSizhengFrameFact] = []
        for origin in canonical_designation_ids():
            semantic = r4_by_origin.get(origin)
            if semantic is None:
                raise ResolvedStructuralCompositionError(
                    "MISSING_R4_FRAME",
                    f"R4 has no Sanfang/Sizheng frame for {origin}",
                )
            if semantic.trine_offsets != (4, 8) or semantic.opposition_offset != 6:
                raise ResolvedStructuralCompositionError(
                    "INVALID_R4_FRAME_GEOMETRY",
                    f"R4 frame geometry is not frozen +4/+8/+6 for {origin}",
                )

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

            members: list[ResolvedStructuralMemberRef] = []
            for offset in RESOLVED_MEMBER_OFFSETS:
                r3_member = r3_by_key.get((origin, offset))
                if r3_member is None:
                    raise ResolvedStructuralCompositionError(
                        "MISSING_R3_MEMBER",
                        f"R3 has no member for {origin} offset {offset}",
                    )
                expected_designation, expected_address = expected_targets[offset]
                if (
                    r3_member.target_designation_id != expected_designation
                    or r3_member.target_raw_address != expected_address
                ):
                    raise ResolvedStructuralCompositionError(
                        "R3_R4_TARGET_MISMATCH",
                        f"R3/R4 target mismatch for {origin} offset {offset}",
                    )

                members.append(
                    ResolvedStructuralMemberRef(
                        semantic_role=RESOLVED_MEMBER_ROLE_BY_OFFSET[offset],
                        member_offset=offset,
                        target_designation_id=r3_member.target_designation_id,
                        target_raw_address=r3_member.target_raw_address,
                        closure_status=r3_member.closure_status,
                        borrowed_from_raw_address=r3_member.borrowed_from_raw_address,
                        physical_source_address=physical_source_address(r3_member),
                        structure_physical_key=r3_member.structure_physical_key,
                        r3_member_key=r3_member_key(origin, offset),
                    )
                )

            frames.append(
                ResolvedSanfangSizhengFrameFact(
                    origin_designation_id=semantic.origin_designation_id,
                    origin_address=semantic.origin_address,
                    trine_group_key=semantic.trine_group_key,
                    opposition_axis_key=semantic.opposition_axis_key,
                    members=tuple(members),
                )
            )

        return tuple(frames)
