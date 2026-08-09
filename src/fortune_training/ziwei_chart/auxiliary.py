from __future__ import annotations

from dataclasses import dataclass

from .models import Address, Placement
from .registries import address


AUXILIARY_ALGORITHM_ID = "ZIWEI-CORE-AUXILIARY-V1"
AUXILIARY_ALGORITHM_VERSION = "1.0.0"
QS_CORE_AUX_RULE_SET_ID = "QS_EWITNESS_CORE_AUX_R1"
QS_CORE_AUX_RULE_SET_VERSION = "1.0.0"


@dataclass(frozen=True)
class AuxiliaryContext:
    ziwei_birth_year_stem: str
    ziwei_birth_year_branch: str
    raw_lunar_month: int
    birth_hour_branch: Address


KUI_YUE_BY_STEM = {
    "甲": ("丑", "未"),
    "戊": ("丑", "未"),
    "庚": ("丑", "未"),
    "乙": ("子", "申"),
    "己": ("子", "申"),
    "辛": ("午", "寅"),
    "壬": ("卯", "巳"),
    "癸": ("卯", "巳"),
    "丙": ("亥", "酉"),
    "丁": ("亥", "酉"),
}

LUCUN_BY_STEM = {
    "甲": "寅",
    "乙": "卯",
    "丙": "巳",
    "戊": "巳",
    "丁": "午",
    "己": "午",
    "庚": "申",
    "辛": "酉",
    "壬": "亥",
    "癸": "子",
}

TIANMA_BY_BRANCH = {
    "寅": "申", "午": "申", "戌": "申",
    "申": "寅", "子": "寅", "辰": "寅",
    "巳": "亥", "酉": "亥", "丑": "亥",
    "亥": "巳", "卯": "巳", "未": "巳",
}

BRANCH_TO_INDEX = {
    "子": 0, "丑": 1, "寅": 2, "卯": 3, "辰": 4, "巳": 5,
    "午": 6, "未": 7, "申": 8, "酉": 9, "戌": 10, "亥": 11,
}


def _placement(entity_id: str, display_name: str, index: int, source_refs: tuple[str, ...]) -> Placement:
    return Placement(
        entity_id=entity_id,
        display_name=display_name,
        address=address(index),
        generator_id=AUXILIARY_ALGORITHM_ID,
        algorithm_version=AUXILIARY_ALGORITHM_VERSION,
        source_refs=source_refs,
    )


class QSCoreAuxiliaryGenerator:
    """Strict QS e-witness core auxiliary placement rules with no modern fallback."""

    rule_set_id = QS_CORE_AUX_RULE_SET_ID
    rule_set_version = QS_CORE_AUX_RULE_SET_VERSION

    @staticmethod
    def chang_qu(hour_index: int) -> tuple[Placement, Placement]:
        return (
            _placement(
                "STAR.WENCHANG",
                "文昌",
                10 - hour_index,
                ("S01:ZZQS-A-1784", "S01:ZZZA-PR-017"),
            ),
            _placement(
                "STAR.WENQU",
                "文曲",
                4 + hour_index,
                ("S01:ZZQS-A-1785", "S01:ZZZA-PR-017"),
            ),
        )

    @staticmethod
    def fu_bi(raw_lunar_month: int) -> tuple[Placement, Placement]:
        if not 1 <= raw_lunar_month <= 12:
            raise ValueError("raw_lunar_month must be in [1, 12]")
        offset = raw_lunar_month - 1
        return (
            _placement(
                "STAR.ZUOFU",
                "左辅",
                4 + offset,
                ("S01:ZZQS-A-1791", "S01:ZZQS-A-1793", "S01:ZZZA-PR-016"),
            ),
            _placement(
                "STAR.YOUBI",
                "右弼",
                10 - offset,
                ("S01:ZZQS-A-1792", "S01:ZZQS-A-1794", "S01:ZZZA-PR-016"),
            ),
        )

    @staticmethod
    def kui_yue(year_stem: str) -> tuple[Placement, Placement]:
        try:
            kui_branch, yue_branch = KUI_YUE_BY_STEM[year_stem]
        except KeyError as exc:
            raise ValueError(f"unsupported year stem for Kui/Yue: {year_stem}") from exc
        return (
            _placement(
                "STAR.TIANKUI",
                "天魁",
                BRANCH_TO_INDEX[kui_branch],
                ("S01:ZZQS-A-1800", "S01:ZZQS-A-1801", "S01:ZZZA-PR-019"),
            ),
            _placement(
                "STAR.TIANYUE",
                "天钺",
                BRANCH_TO_INDEX[yue_branch],
                ("S01:ZZQS-A-1800", "S01:ZZQS-A-1801", "S01:ZZZA-PR-019"),
            ),
        )

    @staticmethod
    def tianma(year_branch: str) -> tuple[Placement, ...]:
        try:
            target = TIANMA_BY_BRANCH[year_branch]
        except KeyError as exc:
            raise ValueError(f"unsupported year branch for Tianma: {year_branch}") from exc
        return (
            _placement(
                "STAR.TIANMA",
                "天马",
                BRANCH_TO_INDEX[target],
                ("S01:ZZQS-A-1808", "S01:ZZQS-A-1809"),
            ),
        )

    @staticmethod
    def lucun_yang_tuo(year_stem: str) -> tuple[Placement, Placement, Placement]:
        try:
            lucun_branch = LUCUN_BY_STEM[year_stem]
        except KeyError as exc:
            raise ValueError(f"unsupported year stem for Lucun: {year_stem}") from exc
        lucun_index = BRANCH_TO_INDEX[lucun_branch]
        return (
            _placement(
                "STAR.LUCUN",
                "禄存",
                lucun_index,
                ("S01:ZZQS-A-1816", "S01:ZZQS-A-1817", "S01:ZZZA-PR-020"),
            ),
            _placement(
                "STAR.QINGYANG",
                "擎羊",
                lucun_index + 1,
                ("S01:ZZQS-A-1825", "S01:ZZZA-PR-020"),
            ),
            _placement(
                "STAR.TUOLUO",
                "陀罗",
                lucun_index - 1,
                ("S01:ZZQS-A-1825", "S01:ZZZA-PR-020"),
            ),
        )

    @staticmethod
    def hour_void_robbery(hour_index: int) -> tuple[Placement, Placement]:
        return (
            _placement(
                "AUX.HOUR_VOID",
                "天空",
                11 - hour_index,
                ("S01:ZZQS-A-1847", "S01:ZZQS-A-1848", "S01:ZZZA-PR-018"),
            ),
            _placement(
                "STAR.DIJIE",
                "地劫",
                11 + hour_index,
                ("S01:ZZQS-A-1847", "S01:ZZQS-A-1848", "S01:ZZZA-PR-018"),
            ),
        )

    def generate(self, context: AuxiliaryContext) -> tuple[Placement, ...]:
        hour_index = context.birth_hour_branch.index
        rows: list[Placement] = []
        rows.extend(self.chang_qu(hour_index))
        rows.extend(self.fu_bi(context.raw_lunar_month))
        rows.extend(self.kui_yue(context.ziwei_birth_year_stem))
        rows.extend(self.tianma(context.ziwei_birth_year_branch))
        rows.extend(self.lucun_yang_tuo(context.ziwei_birth_year_stem))
        rows.extend(self.hour_void_robbery(hour_index))
        return tuple(rows)
