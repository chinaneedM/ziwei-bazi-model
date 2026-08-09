from __future__ import annotations

from .models import Address, FiveElementBureau


EARTHLY_BRANCHES = ("子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥")
HEAVENLY_STEMS = ("甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸")

PALACE_DESIGNATIONS = (
    ("LIFE", "命"),
    ("SIBLINGS", "兄弟"),
    ("SPOUSE", "夫妻"),
    ("CHILDREN", "子女"),
    ("WEALTH", "财帛"),
    ("HEALTH", "疾厄"),
    ("TRAVEL", "迁移"),
    ("SERVANTS_FRIENDS", "奴仆"),
    ("CAREER", "官禄"),
    ("PROPERTY", "田宅"),
    ("FORTUNE", "福德"),
    ("PARENTS", "父母"),
)

BUREAU_NUMBER_BY_ELEMENT = {"水": 2, "木": 3, "金": 4, "土": 5, "火": 6}

# The 30 NaYin pairs in sexagenary-cycle order. Each entry covers two consecutive Ganzhi.
NAYIN_PAIRS = (
    ("海中金", "金"),
    ("炉中火", "火"),
    ("大林木", "木"),
    ("路旁土", "土"),
    ("剑锋金", "金"),
    ("山头火", "火"),
    ("涧下水", "水"),
    ("城头土", "土"),
    ("白蜡金", "金"),
    ("杨柳木", "木"),
    ("泉中水", "水"),
    ("屋上土", "土"),
    ("霹雳火", "火"),
    ("松柏木", "木"),
    ("长流水", "水"),
    ("沙中金", "金"),
    ("山下火", "火"),
    ("平地木", "木"),
    ("壁上土", "土"),
    ("金箔金", "金"),
    ("覆灯火", "火"),
    ("天河水", "水"),
    ("大驿土", "土"),
    ("钗钏金", "金"),
    ("桑柘木", "木"),
    ("大溪水", "水"),
    ("沙中土", "土"),
    ("天上火", "火"),
    ("石榴木", "木"),
    ("大海水", "水"),
)

YEAR_STEM_TO_YIN_START_STEM = {
    "甲": "丙",
    "己": "丙",
    "乙": "戊",
    "庚": "戊",
    "丙": "庚",
    "辛": "庚",
    "丁": "壬",
    "壬": "壬",
    "戊": "甲",
    "癸": "甲",
}


def address(index: int) -> Address:
    normalized = index % 12
    return Address(normalized, EARTHLY_BRANCHES[normalized])


def branch_index(branch: str) -> int:
    try:
        return EARTHLY_BRANCHES.index(branch)
    except ValueError as exc:
        raise ValueError(f"unknown earthly branch: {branch}") from exc


def stem_index(stem: str) -> int:
    try:
        return HEAVENLY_STEMS.index(stem)
    except ValueError as exc:
        raise ValueError(f"unknown heavenly stem: {stem}") from exc


def sexagenary_for_year(year: int) -> tuple[str, str]:
    # 4 CE is 甲子; this arithmetic is valid for the modern positive-year range
    # consumed by the current Time/Calendar Foundation.
    offset = year - 4
    return HEAVENLY_STEMS[offset % 10], EARTHLY_BRANCHES[offset % 12]


def sexagenary_index(stem: str, branch: str) -> int:
    s = stem_index(stem)
    b = branch_index(branch)
    for index in range(60):
        if index % 10 == s and index % 12 == b:
            return index
    raise ValueError(f"invalid sexagenary combination: {stem}{branch}")


def nayin_for_ganzhi(stem: str, branch: str) -> tuple[str, str]:
    index = sexagenary_index(stem, branch)
    return NAYIN_PAIRS[index // 2]


def bureau_for_ganzhi(stem: str, branch: str) -> FiveElementBureau:
    nayin_name, element = nayin_for_ganzhi(stem, branch)
    return FiveElementBureau(
        element=element,
        number=BUREAU_NUMBER_BY_ELEMENT[element],
        life_palace_ganzhi=f"{stem}{branch}",
        nayin_name=nayin_name,
    )
