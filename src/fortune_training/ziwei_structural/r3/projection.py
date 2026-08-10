from __future__ import annotations

from collections import defaultdict

from fortune_training.util import object_sha256
from fortune_training.ziwei_chart.dignity import MAIN_STAR_ENTITY_IDS
from fortune_training.ziwei_chart.models import NatalChartState, Placement, TransformationActivation
from fortune_training.ziwei_chart.registries import PALACE_DESIGNATIONS, address
from fortune_training.ziwei_structural.r2.models import RelativePalaceFrameState

from .models import BORROW_MEMBER_OFFSETS, BorrowClosureMemberFact


BORROW_PROJECTION_SOURCE_REFS = (
    "S06:ZZTERM_BORROW_CLOSURE",
    "S06:BORROW_RULE_01-05",
)


class BorrowProjectionError(ValueError):
    pass


def _placements_by_address(chart: NatalChartState) -> dict[int, tuple[Placement, ...]]:
    grouped: dict[int, list[Placement]] = defaultdict(list)
    for row in chart.placements:
        grouped[row.address.index].append(row)
    return {
        index: tuple(sorted(rows, key=lambda row: row.entity_id))
        for index, rows in grouped.items()
    }


def _transformations_by_address(
    chart: NatalChartState,
) -> dict[int, tuple[TransformationActivation, ...]]:
    grouped: dict[int, list[TransformationActivation]] = defaultdict(list)
    for row in chart.transformations:
        grouped[row.target_address.index].append(row)
    return {
        index: tuple(sorted(rows, key=lambda row: row.activation_id))
        for index, rows in grouped.items()
    }


def _contains_main_star(rows: tuple[Placement, ...]) -> bool:
    return any(row.entity_id in MAIN_STAR_ENTITY_IDS for row in rows)


def _physical_key(
    *,
    time_layer: str,
    target_index: int,
    physical_source_index: int,
    closure_status: str,
    placements: tuple[Placement, ...],
    transformations: tuple[TransformationActivation, ...],
) -> str:
    digest = object_sha256(
        {
            "time_layer": time_layer,
            "target_raw_address_index": target_index,
            "physical_source_address_index": physical_source_index,
            "closure_status": closure_status,
            "projected_entity_ids": [row.entity_id for row in placements],
            "projected_transformation_ids": [row.activation_id for row in transformations],
        }
    )
    return f"STRUCTURE-PHYSICAL:{digest}"


class BorrowProjectionGenerator:
    """Build S06 borrow-view facts without mutating upstream physical placements."""

    @staticmethod
    def _member_frame_map(relative_state: RelativePalaceFrameState):
        mapping = {}
        for row in relative_state.frame_facts:
            if row.clockwise_offset not in BORROW_MEMBER_OFFSETS:
                continue
            key = (row.origin_designation_id, row.clockwise_offset)
            if key in mapping:
                raise BorrowProjectionError(f"duplicate R2 member geometry: {key}")
            mapping[key] = row
        return mapping

    def generate(
        self,
        natal_chart: NatalChartState,
        relative_state: RelativePalaceFrameState,
        *,
        time_layer: str = "NATAL",
    ) -> tuple[BorrowClosureMemberFact, ...]:
        if time_layer != "NATAL":
            raise BorrowProjectionError(f"unsupported time layer: {time_layer}")

        placements_by_address = _placements_by_address(natal_chart)
        transformations_by_address = _transformations_by_address(natal_chart)
        member_map = self._member_frame_map(relative_state)
        canonical_origin_ids = tuple(row[0] for row in PALACE_DESIGNATIONS)

        facts: list[BorrowClosureMemberFact] = []
        for origin_id in canonical_origin_ids:
            for member_offset in BORROW_MEMBER_OFFSETS:
                try:
                    frame_row = member_map[(origin_id, member_offset)]
                except KeyError as exc:
                    raise BorrowProjectionError(
                        f"missing R2 member geometry: {origin_id}:{member_offset}"
                    ) from exc

                target = frame_row.target_address
                target_placements = placements_by_address.get(target.index, ())
                target_empty = not _contains_main_star(target_placements)

                if not target_empty:
                    closure_status = "DIRECT_PHYSICAL"
                    physical_source = target
                    borrowed_from = None
                    projected_placements = target_placements
                    projected_transformations = transformations_by_address.get(target.index, ())
                    zero_second = False
                else:
                    opposite = address(target.index + 6)
                    source_placements = placements_by_address.get(opposite.index, ())
                    if _contains_main_star(source_placements):
                        closure_status = "BORROWED_DIRECT"
                        physical_source = opposite
                        borrowed_from = opposite
                        projected_placements = source_placements
                        projected_transformations = transformations_by_address.get(opposite.index, ())
                        zero_second = True
                    else:
                        closure_status = "BORROW_SOURCE_EMPTY_OR_UNKNOWN"
                        physical_source = opposite
                        borrowed_from = None
                        projected_placements = ()
                        projected_transformations = ()
                        zero_second = False

                facts.append(
                    BorrowClosureMemberFact(
                        evaluation_origin_designation_id=origin_id,
                        evaluation_origin_address=frame_row.origin_address,
                        time_layer=time_layer,
                        member_offset=member_offset,
                        target_designation_id=frame_row.target_designation_id,
                        target_raw_address=target,
                        target_main_star_empty=target_empty,
                        closure_status=closure_status,
                        borrowed_from_raw_address=borrowed_from,
                        projected_placements=projected_placements,
                        projected_transformations=projected_transformations,
                        structure_physical_key=_physical_key(
                            time_layer=time_layer,
                            target_index=target.index,
                            physical_source_index=physical_source.index,
                            closure_status=closure_status,
                            placements=projected_placements,
                            transformations=projected_transformations,
                        ),
                        zero_second_contribution=zero_second,
                    )
                )

        return tuple(facts)
