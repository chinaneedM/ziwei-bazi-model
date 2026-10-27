from __future__ import annotations

from dataclasses import dataclass

from .models import Address, Placement
from .registries import address, branch_index, sexagenary_index


MINOR_STAR_ALGORITHM_ID = "ZIWEI-OPERATIONAL-MINOR-STARS-V1"
MINOR_STAR_ALGORITHM_VERSION = "1.0.0"
WENMO_DEFAULT_MINOR_RULE_SET_ID = "WENMO_DEFAULT_MINOR_R1"
WENMO_DEFAULT_MINOR_RULE_SET_VERSION = "1.0.0"


class MinorStarGenerationError(ValueError):
    def __init__(self, diagnostic_code: str) -> None:
        super().__init__(diagnostic_code)
        self.diagnostic_code = diagnostic_code


@dataclass(frozen=True)
class MinorStarContext:
    ziwei_birth_year_stem: str
    ziwei_birth_year_branch: str
    raw_lunar_month: int
    is_leap_month: bool
    lunar_day: int
    birth_hour_branch: Address
    life_address: Address
    body_address: Address


YANG_STEMS = {"甲", "丙", "戊", "庚", "壬"}

TIANGUAN_TIANFU_BY_STEM = {
    "甲": ("未", "酉"),
    "乙": ("辰", "申"),
    "丙": ("巳", "子"),
    "丁": ("寅", "亥"),
    "戊": ("卯", "卯"),
    "己": ("酉", "寅"),
    "庚": ("亥", "午"),
    "辛": ("酉", "巳"),
    "壬": ("戌", "午"),
    "癸": ("午", "巳"),
}

TIANCHU_BY_STEM = {
    "甲": "巳", "丁": "巳",
    "乙": "午", "戊": "午", "辛": "午",
    "丙": "子",
    "己": "申",
    "庚": "寅",
    "壬": "酉",
    "癸": "亥",
}

JIEKONG_PAIR_BY_STEM = {
    "甲": ("申", "酉"), "己": ("申", "酉"),
    "乙": ("午", "未"), "庚": ("午", "未"),
    "丙": ("辰", "巳"), "辛": ("辰", "巳"),
    "丁": ("寅", "卯"), "壬": ("寅", "卯"),
    "戊": ("子", "丑"), "癸": ("子", "丑"),
}

FEILIAN_BY_BRANCH = {
    "子": "申", "丑": "酉", "寅": "戌",
    "卯": "巳", "辰": "午", "巳": "未",
    "午": "寅", "未": "卯", "申": "辰",
    "酉": "亥", "戌": "子", "亥": "丑",
}

POSUI_BY_BRANCH = {
    "子": "巳", "午": "巳", "卯": "巳", "酉": "巳",
    "寅": "酉", "申": "酉", "巳": "酉", "亥": "酉",
    "辰": "丑", "戌": "丑", "丑": "丑", "未": "丑",
}

JIESHA_BY_BRANCH = {
    "申": "巳", "子": "巳", "辰": "巳",
    "亥": "申", "卯": "申", "未": "申",
    "寅": "亥", "午": "亥", "戌": "亥",
    "巳": "寅", "酉": "寅", "丑": "寅",
}

HUAGAI_BY_BRANCH = {
    "申": "辰", "子": "辰", "辰": "辰",
    "巳": "丑", "酉": "丑", "丑": "丑",
    "寅": "戌", "午": "戌", "戌": "戌",
    "亥": "未", "卯": "未", "未": "未",
}

XIANCHI_BY_BRANCH = {
    "申": "酉", "子": "酉", "辰": "酉",
    "巳": "午", "酉": "午", "丑": "午",
    "寅": "卯", "午": "卯", "戌": "卯",
    "亥": "子", "卯": "子", "未": "子",
}

GUCHEN_GUASU_BY_BRANCH = {
    "亥": ("寅", "戌"), "子": ("寅", "戌"), "丑": ("寅", "戌"),
    "寅": ("巳", "丑"), "卯": ("巳", "丑"), "辰": ("巳", "丑"),
    "巳": ("申", "辰"), "午": ("申", "辰"), "未": ("申", "辰"),
    "申": ("亥", "未"), "酉": ("亥", "未"), "戌": ("亥", "未"),
}

JIESHEN_BY_MONTH = {
    1: "申", 2: "申", 3: "戌", 4: "戌",
    5: "子", 6: "子", 7: "寅", 8: "寅",
    9: "辰", 10: "辰", 11: "午", 12: "午",
}

TIANWU_BY_MONTH = {
    1: "巳", 5: "巳", 9: "巳",
    2: "申", 6: "申", 10: "申",
    3: "寅", 7: "寅", 11: "寅",
    4: "亥", 8: "亥", 12: "亥",
}

TIANYUE_MOON_BY_MONTH = {
    1: "戌", 2: "巳", 3: "辰", 4: "寅",
    5: "未", 6: "卯", 7: "亥", 8: "未",
    9: "寅", 10: "午", 11: "戌", 12: "寅",
}


def _placement(entity_id: str, display_name: str, index: int, source_refs: tuple[str, ...]) -> Placement:
    return Placement(
        entity_id=entity_id,
        display_name=display_name,
        address=address(index),
        generator_id=MINOR_STAR_ALGORITHM_ID,
        algorithm_version=MINOR_STAR_ALGORITHM_VERSION,
        source_refs=source_refs,
    )


def _branch_placement(entity_id: str, display_name: str, branch: str, source_refs: tuple[str, ...]) -> Placement:
    return _placement(entity_id, display_name, branch_index(branch), source_refs)


class WenmoDefaultMinorStarGenerator:
    """Operational small-star profile reconstructed from S01 and frozen Wenmo fixtures.

    This rule set intentionally does not claim to be a strict historical QS profile.
    S01 cells that record unresolved source conflicts are only activated here where
    the external Wenmo fixture selects a concrete operational branch.
    """

    rule_set_id = WENMO_DEFAULT_MINOR_RULE_SET_ID
    rule_set_version = WENMO_DEFAULT_MINOR_RULE_SET_VERSION

    @staticmethod
    def _month_coordinate(context: MinorStarContext) -> int:
        if not 1 <= context.raw_lunar_month <= 12:
            raise ValueError("raw_lunar_month must be in [1, 12]")
        if not context.is_leap_month:
            return context.raw_lunar_month
        # Explicit Wenmo operational binding; independent from the Life/Body policy field.
        return context.raw_lunar_month if context.lunar_day <= 15 else context.raw_lunar_month % 12 + 1

    @staticmethod
    def _refs(route: str, *, external: bool = True) -> tuple[str, ...]:
        refs = [f"S01:{route}"]
        if external:
            refs.append("COMPAT:WENMO-CHARTDIFF-006")
        return tuple(refs)

    @classmethod
    def stem_stars(cls, stem: str) -> tuple[Placement, ...]:
        try:
            tianguan, tianfu = TIANGUAN_TIANFU_BY_STEM[stem]
            tianchu = TIANCHU_BY_STEM[stem]
            jie_pair = JIEKONG_PAIR_BY_STEM[stem]
        except KeyError as exc:
            raise ValueError(f"unsupported stem for operational minor stars: {stem}") from exc
        first, second = jie_pair
        primary, secondary = (first, second) if stem in YANG_STEMS else (second, first)
        return (
            _branch_placement("STAR.TIANGUAN", "天官", tianguan, cls._refs("ZZZA-PR-022")),
            _branch_placement("STAR.TIANFU_BLESSING", "天福", tianfu, cls._refs("ZZZA-PR-022")),
            _branch_placement("STAR.TIANCHU", "天厨", tianchu, cls._refs("ZZZA-PR-023")),
            _branch_placement("STAR.JIEKONG", "截空", primary, cls._refs("ZZZA-PR-024")),
            _branch_placement("STAR.FU_JIEKONG", "副截", secondary, cls._refs("ZZZA-PR-024")),
        )

    @classmethod
    def xunkong(cls, stem: str, branch: str) -> tuple[Placement, Placement]:
        index = sexagenary_index(stem, branch)
        xun_start_branch_index = (index // 10 * 10) % 12
        first_void = address(xun_start_branch_index + 10).branch
        second_void = address(xun_start_branch_index + 11).branch
        primary, secondary = (first_void, second_void) if stem in YANG_STEMS else (second_void, first_void)
        return (
            _branch_placement("STAR.XUNKONG", "旬空", primary, cls._refs("ZZZA-PR-025")),
            _branch_placement("STAR.FU_XUNKONG", "副旬", secondary, cls._refs("ZZZA-PR-025")),
        )

    @classmethod
    def year_branch_stars(cls, year_branch: str, year_stem: str, life_index: int) -> tuple[Placement, ...]:
        y = branch_index(year_branch)
        try:
            guchen, guasu = GUCHEN_GUASU_BY_BRANCH[year_branch]
            jiesha = JIESHA_BY_BRANCH[year_branch]
            feilian = FEILIAN_BY_BRANCH[year_branch]
            posui = POSUI_BY_BRANCH[year_branch]
            huagai = HUAGAI_BY_BRANCH[year_branch]
            xianchi = XIANCHI_BY_BRANCH[year_branch]
        except KeyError as exc:
            raise ValueError(f"unsupported year branch for operational minor stars: {year_branch}") from exc
        dahao = y + 6 + (1 if year_stem in YANG_STEMS else -1)
        return (
            _placement("STAR.TIANKONG", "天空", y + 1, cls._refs("ZZZA-PR-027")),
            _placement("STAR.TIANKU", "天哭", 6 - y, cls._refs("ZZZA-PR-028")),
            _placement("STAR.TIANXU", "天虚", 6 + y, cls._refs("ZZZA-PR-028")),
            _placement("STAR.HONGLUAN", "红鸾", 3 - y, cls._refs("ZZZA-PR-029")),
            _placement("STAR.TIANXI", "天喜", 3 - y + 6, cls._refs("ZZZA-PR-029")),
            _branch_placement("STAR.GUCHEN", "孤辰", guchen, cls._refs("ZZZA-PR-030")),
            _branch_placement("STAR.GUASU", "寡宿", guasu, cls._refs("ZZZA-PR-030")),
            _branch_placement("STAR.JIESHA", "劫煞", jiesha, cls._refs("ZZZA-PR-031")),
            _placement("STAR.DAHAO", "大耗", dahao, cls._refs("ZZZA-PR-032")),
            _branch_placement("STAR.FEILIAN", "蜚廉", feilian, cls._refs("ZZZA-PR-033")),
            _branch_placement("STAR.POSUI", "破碎", posui, cls._refs("ZZZA-PR-034")),
            _branch_placement("STAR.HUAGAI", "华盖", huagai, cls._refs("ZZZA-PR-035")),
            _branch_placement("STAR.XIANCHI", "咸池", xianchi, cls._refs("ZZZA-PR-036")),
            _placement("STAR.LONGDE", "龙德", 7 + y, cls._refs("ZZZA-PR-037")),
            _placement("STAR.YUEDE", "月德", 5 + y, cls._refs("ZZZA-PR-038")),
            # S01 records textual conflicts for TianDe/NianJie. Wenmo-006 selects the table/verse branch.
            _placement("STAR.TIANDE", "天德", 9 + y, cls._refs("ZZZA-PR-039")),
            _placement("STAR.NIANJIE", "年解", 10 - y, cls._refs("ZZZA-PR-040")),
            _placement("STAR.TIANCAI", "天才", life_index + y, cls._refs("ZZZA-PR-041")),
            _placement("STAR.LONGCHI", "龙池", 4 + y, cls._refs("ZZZA-PR-043")),
            _placement("STAR.FENGGE", "凤阁", 10 - y, cls._refs("ZZZA-PR-044")),
        )

    @classmethod
    def hour_stars(cls, hour_index: int) -> tuple[Placement, Placement]:
        if not 0 <= hour_index < 12:
            raise ValueError("hour_index must be in [0, 11]")
        return (
            _placement("STAR.TAIFU", "台辅", 6 + hour_index, cls._refs("ZZQS-A-1899")),
            _placement("STAR.FENGGAO", "封诰", 2 + hour_index, cls._refs("ZZQS-A-1905")),
        )

    @classmethod
    def month_stars(cls, month: int) -> tuple[Placement, ...]:
        if not 1 <= month <= 12:
            raise ValueError("month must be in [1, 12]")
        yinsha = 2 - 2 * (month - 1)
        return (
            _placement("STAR.TIANXING", "天刑", 9 + month - 1, cls._refs("ZZZA-PR-046")),
            _placement("STAR.TIANYAO", "天姚", 1 + month - 1, cls._refs("ZZZA-PR-046")),
            _branch_placement("STAR.JIESHEN", "解神", JIESHEN_BY_MONTH[month], cls._refs("ZZZA-PR-047")),
            _branch_placement("STAR.TIANWU", "天巫", TIANWU_BY_MONTH[month], cls._refs("ZZZA-PR-048")),
            _branch_placement("STAR.TIANYUE_MOON", "天月", TIANYUE_MOON_BY_MONTH[month], cls._refs("ZZZA-PR-049")),
            _placement("STAR.YINSHA", "阴煞", yinsha, cls._refs("ZZZA-PR-050")),
        )

    def generate(self, context: MinorStarContext) -> tuple[Placement, ...]:
        month = self._month_coordinate(context)
        rows: list[Placement] = []
        rows.extend(self.stem_stars(context.ziwei_birth_year_stem))
        rows.extend(self.xunkong(context.ziwei_birth_year_stem, context.ziwei_birth_year_branch))
        rows.extend(
            self.year_branch_stars(
                context.ziwei_birth_year_branch,
                context.ziwei_birth_year_stem,
                context.life_address.index,
            )
        )
        rows.extend(self.hour_stars(context.birth_hour_branch.index))
        rows.extend(self.month_stars(month))
        return tuple(rows)
