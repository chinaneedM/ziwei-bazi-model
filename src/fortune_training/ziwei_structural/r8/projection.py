from __future__ import annotations

from fortune_training.ziwei_structural.r2 import RelativePalaceFrameState, canonical_designation_ids

from .models import AdjacentPalacePairFact
from .profile import (
    ADJACENT_PALACE_SEMANTIC_SCOPE,
    ADJACENT_PALACE_SOURCE_TERM_ID,
    CLOCKWISE_NEIGHBOR_CLOCKWISE_OFFSET,
    CLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL,
    CLOCKWISE_NEIGHBOR_RELATIVE_ROLE,
    COUNTERCLOCKWISE_NEIGHBOR_CLOCKWISE_OFFSET,
    COUNTERCLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL,
    COUNTERCLOCKWISE_NEIGHBOR_RELATIVE_ROLE,
)


class AdjacentPalaceProjectionError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


def _require_frame(by_key, origin_designation_id: str, relative_ordinal: int):
    frame = by_key.get((origin_designation_id, relative_ordinal))
    if frame is None:
        raise AdjacentPalaceProjectionError(
            "MISSING_R2_ADJACENT_FRAME_FACT",
            f"missing R2 ordinal {relative_ordinal} fact for {origin_designation_id}",
        )
    return frame


def project_adjacent_palace_pairs(
    r2_state: RelativePalaceFrameState,
) -> tuple[AdjacentPalacePairFact, ...]:
    by_key = {
        (row.origin_designation_id, row.relative_ordinal): row
        for row in r2_state.frame_facts
    }
    facts: list[AdjacentPalacePairFact] = []
    for origin_designation_id in canonical_designation_ids():
        counterclockwise = _require_frame(
            by_key,
            origin_designation_id,
            COUNTERCLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL,
        )
        clockwise = _require_frame(
            by_key,
            origin_designation_id,
            CLOCKWISE_NEIGHBOR_RELATIVE_ORDINAL,
        )
        if (
            counterclockwise.relative_role_designation_id
            != COUNTERCLOCKWISE_NEIGHBOR_RELATIVE_ROLE
            or counterclockwise.clockwise_offset
            != COUNTERCLOCKWISE_NEIGHBOR_CLOCKWISE_OFFSET
        ):
            raise AdjacentPalaceProjectionError(
                "R2_COUNTERCLOCKWISE_NEIGHBOR_MISMATCH",
                f"{origin_designation_id} ordinal 2 must be SIBLINGS at clockwise offset 11",
            )
        if (
            clockwise.relative_role_designation_id != CLOCKWISE_NEIGHBOR_RELATIVE_ROLE
            or clockwise.clockwise_offset != CLOCKWISE_NEIGHBOR_CLOCKWISE_OFFSET
        ):
            raise AdjacentPalaceProjectionError(
                "R2_CLOCKWISE_NEIGHBOR_MISMATCH",
                f"{origin_designation_id} ordinal 12 must be PARENTS at clockwise offset 1",
            )
        if counterclockwise.origin_address != clockwise.origin_address:
            raise AdjacentPalaceProjectionError(
                "R2_ADJACENT_ORIGIN_ADDRESS_MISMATCH",
                f"R2 adjacent facts disagree on origin address for {origin_designation_id}",
            )
        facts.append(
            AdjacentPalacePairFact(
                source_term_id=ADJACENT_PALACE_SOURCE_TERM_ID,
                origin_designation_id=origin_designation_id,
                origin_address=counterclockwise.origin_address,
                counterclockwise_designation_id=counterclockwise.target_designation_id,
                counterclockwise_address=counterclockwise.target_address,
                counterclockwise_relative_ordinal=counterclockwise.relative_ordinal,
                counterclockwise_clockwise_offset=counterclockwise.clockwise_offset,
                clockwise_designation_id=clockwise.target_designation_id,
                clockwise_address=clockwise.target_address,
                clockwise_relative_ordinal=clockwise.relative_ordinal,
                clockwise_clockwise_offset=clockwise.clockwise_offset,
                semantic_scope=ADJACENT_PALACE_SEMANTIC_SCOPE,
                direct_event_permission=False,
                direct_endpoint_permission=False,
                direct_score_permission=False,
                flank_semantics_permission=False,
            )
        )
    return tuple(facts)
