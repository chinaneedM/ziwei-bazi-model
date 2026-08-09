from __future__ import annotations

import math

from .models import Placement
from .registries import address


MAIN_STAR_ALGORITHM_ID = "ZIWEI-FOURTEEN-MAIN-STARS-V1"
MAIN_STAR_ALGORITHM_VERSION = "1.0.0"

ZIWEI_SOURCE_REFS = ("S01:ZZZA-PR-012", "S01:ZZZA-PR-014")
TIANFU_SOURCE_REFS = ("S01:ZZZA-PR-013", "S01:ZZZA-PR-015")

ZIWEI_GROUP = (
    ("STAR.ZIWEI", "紫微", 0),
    ("STAR.TIANJI", "天机", -1),
    ("STAR.TAIYANG", "太阳", -3),
    ("STAR.WUQU", "武曲", -4),
    ("STAR.TIANTONG", "天同", -5),
    ("STAR.LIANZHEN", "廉贞", -7),
)

TIANFU_GROUP = (
    ("STAR.TIANFU", "天府", 0),
    ("STAR.TAIYIN", "太阴", 1),
    ("STAR.TANLANG", "贪狼", 2),
    ("STAR.JUMEN", "巨门", 3),
    ("STAR.TIANXIANG", "天相", 4),
    ("STAR.TIANLIANG", "天梁", 5),
    ("STAR.QISHA", "七杀", 6),
    ("STAR.POJUN", "破军", 10),
)


class MainStarGenerator:
    @staticmethod
    def ziwei_anchor(lunar_day: int, bureau_number: int) -> int:
        if not 1 <= lunar_day <= 30:
            raise ValueError("lunar_day must be in [1, 30]")
        if bureau_number not in {2, 3, 4, 5, 6}:
            raise ValueError("bureau_number must be one of 2, 3, 4, 5, 6")
        quotient = math.ceil(lunar_day / bureau_number)
        complement = quotient * bureau_number - lunar_day
        offset = (quotient - 1) + ((-1) ** complement) * complement
        return (2 + offset) % 12

    @staticmethod
    def tianfu_anchor(ziwei_index: int) -> int:
        # Reflection of the Ziwei anchor across the 寅申 diameter in Z12.
        return (4 - ziwei_index) % 12

    def generate_from_ziwei_anchor(self, ziwei_index: int) -> tuple[Placement, ...]:
        ziwei = ziwei_index % 12
        tianfu = self.tianfu_anchor(ziwei)
        rows: list[Placement] = []
        for entity_id, display_name, offset in ZIWEI_GROUP:
            rows.append(
                Placement(
                    entity_id=entity_id,
                    display_name=display_name,
                    address=address(ziwei + offset),
                    generator_id=MAIN_STAR_ALGORITHM_ID,
                    algorithm_version=MAIN_STAR_ALGORITHM_VERSION,
                    source_refs=ZIWEI_SOURCE_REFS,
                )
            )
        for entity_id, display_name, offset in TIANFU_GROUP:
            rows.append(
                Placement(
                    entity_id=entity_id,
                    display_name=display_name,
                    address=address(tianfu + offset),
                    generator_id=MAIN_STAR_ALGORITHM_ID,
                    algorithm_version=MAIN_STAR_ALGORITHM_VERSION,
                    source_refs=TIANFU_SOURCE_REFS,
                )
            )
        return tuple(rows)

    def generate(self, lunar_day: int, bureau_number: int) -> tuple[Placement, ...]:
        return self.generate_from_ziwei_anchor(self.ziwei_anchor(lunar_day, bureau_number))
