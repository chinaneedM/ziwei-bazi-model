from __future__ import annotations

from .models import Placement
from .registries import address


DERIVED_AUXILIARY_ALGORITHM_ID = "ZIWEI-DERIVED-AUXILIARY-V1"
DERIVED_AUXILIARY_ALGORITHM_VERSION = "1.0.0"


class DerivedAuxiliaryGenerationError(ValueError):
    def __init__(self, diagnostic_code: str) -> None:
        super().__init__(diagnostic_code)
        self.diagnostic_code = diagnostic_code


def _placement(entity_id: str, display_name: str, index: int, source_refs: tuple[str, ...]) -> Placement:
    return Placement(
        entity_id=entity_id,
        display_name=display_name,
        address=address(index),
        generator_id=DERIVED_AUXILIARY_ALGORITHM_ID,
        algorithm_version=DERIVED_AUXILIARY_ALGORITHM_VERSION,
        source_refs=source_refs,
    )


class DerivedAuxiliaryGenerator:
    """Generate stars whose anchors are already-generated placement facts."""

    @staticmethod
    def _index_by_entity(placements: tuple[Placement, ...] | list[Placement]) -> dict[str, int]:
        result: dict[str, int] = {}
        for row in placements:
            if row.entity_id in result:
                raise DerivedAuxiliaryGenerationError("DERIVED_AUXILIARY_DUPLICATE_ANCHOR_ENTITY")
            result[row.entity_id] = row.address.index
        return result

    @staticmethod
    def san_tai_ba_zuo(anchor_indices: dict[str, int], lunar_day: int) -> tuple[Placement, Placement]:
        if not 1 <= lunar_day <= 30:
            raise ValueError("lunar_day must be in [1, 30]")
        try:
            zuofu = anchor_indices["STAR.ZUOFU"]
            youbi = anchor_indices["STAR.YOUBI"]
        except KeyError as exc:
            raise DerivedAuxiliaryGenerationError("SAN_TAI_BA_ZUO_MISSING_FU_BI_ANCHOR") from exc
        offset = lunar_day - 1
        return (
            _placement(
                "STAR.SANTAI",
                "三台",
                zuofu + offset,
                ("S01:ZZQS-A-1879", "S01:ZZZA-PR-052"),
            ),
            _placement(
                "STAR.BAZUO",
                "八座",
                youbi - offset,
                ("S01:ZZQS-A-1880", "S01:ZZZA-PR-052"),
            ),
        )

    @staticmethod
    def en_guang_tian_gui(anchor_indices: dict[str, int], lunar_day: int) -> tuple[Placement, Placement]:
        if not 1 <= lunar_day <= 30:
            raise ValueError("lunar_day must be in [1, 30]")
        try:
            wenchang = anchor_indices["STAR.WENCHANG"]
            wenqu = anchor_indices["STAR.WENQU"]
        except KeyError as exc:
            raise DerivedAuxiliaryGenerationError("EN_GUANG_TIAN_GUI_MISSING_CHANG_QU_ANCHOR") from exc
        # 起初一顺数至生日，再退后一格；等价于 anchor + (day - 2).
        offset = lunar_day - 2
        return (
            _placement(
                "STAR.ENGUANG",
                "恩光",
                wenchang + offset,
                ("S01:ZZZA-A-0995", "S01:ZZZA-A-0997", "S01:ZZZA-PR-053"),
            ),
            _placement(
                "STAR.TIANGUI",
                "天贵",
                wenqu + offset,
                ("S01:ZZZA-A-0996", "S01:ZZZA-A-0999", "S01:ZZZA-PR-053"),
            ),
        )

    def generate(self, placements: tuple[Placement, ...] | list[Placement], lunar_day: int) -> tuple[Placement, ...]:
        anchors = self._index_by_entity(placements)
        rows: list[Placement] = []
        rows.extend(self.san_tai_ba_zuo(anchors, lunar_day))
        rows.extend(self.en_guang_tian_gui(anchors, lunar_day))
        return tuple(rows)
