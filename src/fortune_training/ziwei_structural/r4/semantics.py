from __future__ import annotations

from fortune_training.ziwei_structural.r2.frame import canonical_designation_ids
from fortune_training.ziwei_structural.r2.models import RelativePalaceFrameState

from .models import OppositionAxisFact, SanfangSizhengFrameFact, TrineGroupFact


class NamedStructuralSemanticError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


def _semantic_key(prefix: str, designation_ids: tuple[str, ...]) -> str:
    return f"{prefix}:" + "|".join(designation_ids)


class NamedStructuralSemanticCompiler:
    """Compile source-bound Sanfang/Sizheng names over validated R2 geometry."""

    def compile(
        self,
        frame_state: RelativePalaceFrameState,
    ) -> tuple[
        tuple[OppositionAxisFact, ...],
        tuple[TrineGroupFact, ...],
        tuple[SanfangSizhengFrameFact, ...],
    ]:
        canonical_ids = canonical_designation_ids()
        order = {designation_id: index for index, designation_id in enumerate(canonical_ids)}
        rows_by_origin: dict[str, dict[int, object]] = {designation_id: {} for designation_id in canonical_ids}

        for fact in frame_state.frame_facts:
            if fact.origin_designation_id not in rows_by_origin:
                raise NamedStructuralSemanticError(
                    "UNKNOWN_R2_ORIGIN",
                    f"unknown R2 origin designation: {fact.origin_designation_id}",
                )
            offset_rows = rows_by_origin[fact.origin_designation_id]
            if fact.clockwise_offset in offset_rows:
                raise NamedStructuralSemanticError(
                    "DUPLICATE_R2_OFFSET",
                    f"origin {fact.origin_designation_id} repeats offset {fact.clockwise_offset}",
                )
            offset_rows[fact.clockwise_offset] = fact

        required_offsets = {0, 4, 6, 8}
        for origin_designation_id, offset_rows in rows_by_origin.items():
            missing = required_offsets - set(offset_rows)
            if missing:
                raise NamedStructuralSemanticError(
                    "MISSING_R2_SEMANTIC_OFFSETS",
                    f"origin {origin_designation_id} is missing offsets {sorted(missing)}",
                )

        axes_by_members: dict[tuple[str, str], OppositionAxisFact] = {}
        groups_by_members: dict[tuple[str, str, str], TrineGroupFact] = {}
        frames: list[SanfangSizhengFrameFact] = []

        for origin_designation_id in canonical_ids:
            offset_rows = rows_by_origin[origin_designation_id]
            origin = offset_rows[0]
            opposition = offset_rows[6]
            trine_four = offset_rows[4]
            trine_eight = offset_rows[8]

            axis_members = tuple(
                sorted(
                    (origin_designation_id, opposition.target_designation_id),
                    key=order.__getitem__,
                )
            )
            if axis_members not in axes_by_members:
                address_by_id = {
                    origin_designation_id: origin.origin_address,
                    opposition.target_designation_id: opposition.target_address,
                }
                axes_by_members[axis_members] = OppositionAxisFact(
                    axis_key=_semantic_key("OPPOSITION_AXIS", axis_members),
                    member_designation_ids=axis_members,
                    member_addresses=tuple(address_by_id[designation_id] for designation_id in axis_members),
                )

            trine_members = tuple(
                sorted(
                    (
                        origin_designation_id,
                        trine_four.target_designation_id,
                        trine_eight.target_designation_id,
                    ),
                    key=order.__getitem__,
                )
            )
            if trine_members not in groups_by_members:
                address_by_id = {
                    origin_designation_id: origin.origin_address,
                    trine_four.target_designation_id: trine_four.target_address,
                    trine_eight.target_designation_id: trine_eight.target_address,
                }
                groups_by_members[trine_members] = TrineGroupFact(
                    group_key=_semantic_key("TRINE_GROUP", trine_members),
                    member_designation_ids=trine_members,
                    member_addresses=tuple(address_by_id[designation_id] for designation_id in trine_members),
                )

            axis = axes_by_members[axis_members]
            group = groups_by_members[trine_members]
            frames.append(
                SanfangSizhengFrameFact(
                    origin_designation_id=origin_designation_id,
                    origin_address=origin.origin_address,
                    trine_group_key=group.group_key,
                    trine_partner_designation_ids=(
                        trine_four.target_designation_id,
                        trine_eight.target_designation_id,
                    ),
                    trine_partner_addresses=(
                        trine_four.target_address,
                        trine_eight.target_address,
                    ),
                    trine_offsets=(4, 8),
                    opposition_axis_key=axis.axis_key,
                    opposition_designation_id=opposition.target_designation_id,
                    opposition_address=opposition.target_address,
                    opposition_offset=6,
                )
            )

        axes = tuple(
            axes_by_members[key]
            for key in sorted(axes_by_members, key=lambda row: tuple(order[item] for item in row))
        )
        groups = tuple(
            groups_by_members[key]
            for key in sorted(groups_by_members, key=lambda row: tuple(order[item] for item in row))
        )
        return axes, groups, tuple(frames)
