from __future__ import annotations

from fortune_training.ziwei_chart.models import NatalChartState
from fortune_training.ziwei_chart.registries import PALACE_DESIGNATIONS

from .models import RelativePalaceRoleFact


class RelativePalaceFrameError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


def canonical_designation_ids() -> tuple[str, ...]:
    return tuple(designation_id for designation_id, _ in PALACE_DESIGNATIONS)


class RelativePalaceFrameGenerator:
    """Rotate the frozen V1 palace designation order around each natal palace."""

    def generate(self, natal_chart: NatalChartState) -> tuple[RelativePalaceRoleFact, ...]:
        canonical_ids = canonical_designation_ids()
        bindings = natal_chart.structure.designation_bindings
        by_id = {row.designation_id: row for row in bindings}

        if len(bindings) != 12 or set(by_id) != set(canonical_ids):
            raise RelativePalaceFrameError(
                "INVALID_NATAL_DESIGNATION_DOMAIN",
                "natal designation bindings must contain each frozen V1 designation exactly once",
            )

        facts: list[RelativePalaceRoleFact] = []
        for origin_index, origin_designation_id in enumerate(canonical_ids):
            origin = by_id[origin_designation_id]
            for role_offset, relative_role_designation_id in enumerate(canonical_ids):
                target_designation_id = canonical_ids[(origin_index + role_offset) % 12]
                target = by_id[target_designation_id]
                facts.append(
                    RelativePalaceRoleFact(
                        origin_designation_id=origin_designation_id,
                        origin_address=origin.address,
                        relative_ordinal=role_offset + 1,
                        relative_role_designation_id=relative_role_designation_id,
                        target_designation_id=target_designation_id,
                        target_address=target.address,
                        clockwise_offset=(target.address.index - origin.address.index) % 12,
                    )
                )
        return tuple(facts)
