from __future__ import annotations

from fortune_training.ziwei_structural.r2 import RelativePalaceFrameState, canonical_designation_ids

from .models import OneSixCommonRootFact
from .profile import (
    ONE_SIX_CLOCKWISE_OFFSET,
    ONE_SIX_RELATIVE_ORDINAL,
    ONE_SIX_SEMANTIC_SCOPE,
    ONE_SIX_SOURCE_TECHNIQUE_ID,
)


class OneSixProjectionError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


def project_one_six_common_roots(
    r2_state: RelativePalaceFrameState,
) -> tuple[OneSixCommonRootFact, ...]:
    by_key = {
        (row.origin_designation_id, row.relative_ordinal): row
        for row in r2_state.frame_facts
    }
    facts: list[OneSixCommonRootFact] = []
    for origin_designation_id in canonical_designation_ids():
        frame = by_key.get((origin_designation_id, ONE_SIX_RELATIVE_ORDINAL))
        if frame is None:
            raise OneSixProjectionError(
                "MISSING_R2_ONE_SIX_FRAME_FACT",
                f"missing R2 ordinal {ONE_SIX_RELATIVE_ORDINAL} fact for {origin_designation_id}",
            )
        if frame.relative_role_designation_id != "HEALTH":
            raise OneSixProjectionError(
                "R2_ONE_SIX_ROLE_MISMATCH",
                f"{origin_designation_id} ordinal 6 must carry HEALTH relative role",
            )
        if frame.clockwise_offset != ONE_SIX_CLOCKWISE_OFFSET:
            raise OneSixProjectionError(
                "R2_ONE_SIX_GEOMETRY_MISMATCH",
                f"{origin_designation_id} expected clockwise offset 7, got {frame.clockwise_offset}",
            )
        facts.append(
            OneSixCommonRootFact(
                source_technique_id=ONE_SIX_SOURCE_TECHNIQUE_ID,
                origin_designation_id=frame.origin_designation_id,
                origin_address=frame.origin_address,
                relative_role_designation_id=frame.relative_role_designation_id,
                target_designation_id=frame.target_designation_id,
                target_address=frame.target_address,
                relative_ordinal=frame.relative_ordinal,
                clockwise_offset=frame.clockwise_offset,
                semantic_scope=ONE_SIX_SEMANTIC_SCOPE,
                direct_event_permission=False,
                direct_endpoint_permission=False,
            )
        )
    return tuple(facts)
