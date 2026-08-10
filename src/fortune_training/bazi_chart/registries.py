from __future__ import annotations


HEAVENLY_STEMS = tuple("甲乙丙丁戊己庚辛壬癸")
EARTHLY_BRANCHES = tuple("子丑寅卯辰巳午未申酉戌亥")
PILLAR_POSITIONS = ("YEAR", "MONTH", "DAY", "HOUR")

STEM_ELEMENTS = {
    "甲": "木",
    "乙": "木",
    "丙": "火",
    "丁": "火",
    "戊": "土",
    "己": "土",
    "庚": "金",
    "辛": "金",
    "壬": "水",
    "癸": "水",
}
STEM_POLARITY = {
    "甲": "YANG",
    "乙": "YIN",
    "丙": "YANG",
    "丁": "YIN",
    "戊": "YANG",
    "己": "YIN",
    "庚": "YANG",
    "辛": "YIN",
    "壬": "YANG",
    "癸": "YIN",
}
BRANCH_ELEMENTS = {
    "子": "水",
    "丑": "土",
    "寅": "木",
    "卯": "木",
    "辰": "土",
    "巳": "火",
    "午": "火",
    "未": "土",
    "申": "金",
    "酉": "金",
    "戌": "土",
    "亥": "水",
}

# Membership/order only. Registry order is not a root-strength scale.
HIDDEN_STEMS = {
    "子": ("癸",),
    "丑": ("己", "癸", "辛"),
    "寅": ("甲", "丙", "戊"),
    "卯": ("乙",),
    "辰": ("戊", "乙", "癸"),
    "巳": ("丙", "戊", "庚"),
    "午": ("丁", "己"),
    "未": ("己", "丁", "乙"),
    "申": ("庚", "壬", "戊"),
    "酉": ("辛",),
    "戌": ("戊", "辛", "丁"),
    "亥": ("壬", "甲"),
}

GENERATES = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
CONTROLS = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

SEXAGENARY_CYCLE = tuple(
    HEAVENLY_STEMS[index % 10] + EARTHLY_BRANCHES[index % 12]
    for index in range(60)
)
SEXAGENARY_INDEX = {ganzhi: index for index, ganzhi in enumerate(SEXAGENARY_CYCLE)}

SEXAGENARY_REGISTRY_ID = "BAZI-SEXAGENARY-REGISTRY-R1"
SEXAGENARY_REGISTRY_VERSION = "1.0.0"
HIDDEN_STEM_RULE_SET_ID = "S11-STANDARD-HIDDEN-STEM-MEMBERSHIP-R1"
HIDDEN_STEM_RULE_SET_VERSION = "1.0.0"
TEN_GOD_RULE_SET_ID = "S11-TEN-GOD-RELATION-R1"
TEN_GOD_RULE_SET_VERSION = "1.0.0"
AFFINITY_RULE_SET_ID = "BAZI-STEM-BRANCH-AFFINITY-R1"
AFFINITY_RULE_SET_VERSION = "1.0.0"
RAW_RELATION_RULE_SET_ID = "BAZI-RAW-RELATION-CLASSICAL-CORE-R1"
RAW_RELATION_RULE_SET_VERSION = "1.0.0"


def sexagenary_index(ganzhi: str) -> int:
    try:
        return SEXAGENARY_INDEX[ganzhi]
    except KeyError as exc:
        raise ValueError(f"invalid sexagenary identity: {ganzhi!r}") from exc


def validate_stem(stem: str) -> str:
    if stem not in STEM_ELEMENTS:
        raise ValueError(f"invalid heavenly stem: {stem!r}")
    return stem


def validate_branch(branch: str) -> str:
    if branch not in BRANCH_ELEMENTS:
        raise ValueError(f"invalid earthly branch: {branch!r}")
    return branch
