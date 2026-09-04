from __future__ import annotations

from fortune_training.util import object_sha256


JIELAN_1581_RULE_SET_ID = "ZIWEI-JIELAN-1581-HISTORICAL-CANDIDATES-R1"
JIELAN_1581_RULE_SET_VERSION = "1.0.0"
JIELAN_1581_SELECTION_STATUS = "PRESERVED_NOT_SELECTED"
JIELAN_1581_SOURCE_ID = "EXT-ZIWEI-JIELAN-1581"

# 《新刻纂集紫微斗数捷览》卷一·安禄权科忌四化诀.
# Order is 禄、权、科、忌.
JIELAN_1581_FOUR_TRANSFORMATIONS = {
    "甲": ("廉贞", "破军", "武曲", "太阳"),
    "乙": ("天机", "天梁", "紫微", "太阴"),
    "丙": ("天同", "天机", "文昌", "廉贞"),
    "丁": ("太阴", "天同", "天机", "巨门"),
    "戊": ("贪狼", "太阴", "右弼", "天机"),
    "己": ("武曲", "贪狼", "天梁", "文曲"),
    "庚": ("太阳", "武曲", "太阴", "天同"),
    "辛": ("巨门", "太阳", "文曲", "文昌"),
    "壬": ("天梁", "紫微", "左辅", "武曲"),
    "癸": ("破军", "巨门", "太阴", "贪狼"),
}
JIELAN_1581_FOUR_TRANSFORMATION_SOURCE_REFS = (
    f"{JIELAN_1581_SOURCE_ID}:CH23",
)

# 《捷览》卷一·安天魁天钺诀.
# This differs from the current QS/received-Fullbook family at 庚:
# Jielan groups 庚辛 at 午/寅, while the current QS family groups 庚 with 甲戊 at 丑/未.
JIELAN_1581_KUI_YUE_BY_STEM = {
    "甲": ("丑", "未"),
    "戊": ("丑", "未"),
    "乙": ("子", "申"),
    "己": ("子", "申"),
    "丙": ("亥", "酉"),
    "丁": ("亥", "酉"),
    "壬": ("卯", "巳"),
    "癸": ("卯", "巳"),
    "庚": ("午", "寅"),
    "辛": ("午", "寅"),
}
JIELAN_1581_KUI_YUE_SOURCE_REFS = (
    f"{JIELAN_1581_SOURCE_ID}:CH25",
)

# 《捷览》卷一·安火铃星诀. Values are the 子时 starting branches.
# Both stars then count forward by birth-hour ordinal.
JIELAN_1581_FIRE_BELL_START_BY_YEAR_BRANCH = {
    "申": ("寅", "戌"),
    "子": ("寅", "戌"),
    "辰": ("寅", "戌"),
    "寅": ("丑", "卯"),
    "午": ("丑", "卯"),
    "戌": ("丑", "卯"),
    "亥": ("酉", "戌"),
    "卯": ("酉", "戌"),
    "未": ("酉", "戌"),
    "巳": ("戌", "卯"),
    "酉": ("戌", "卯"),
    "丑": ("戌", "卯"),
}
JIELAN_1581_FIRE_BELL_SOURCE_REFS = (
    f"{JIELAN_1581_SOURCE_ID}:CH27",
)

# 《捷览》卷一·安天殇天使诀. In repository Z12 branch-index orientation,
# its worked example 命寅 -> 天殇未 / 天使酉 is +5 / +7.
JIELAN_1581_TIANSHANG_TIANSHI_OFFSETS = {
    "STAR.TIANSHANG": 5,
    "STAR.TIANSHI": 7,
}
JIELAN_1581_TIANSHANG_TIANSHI_SOURCE_REFS = (
    f"{JIELAN_1581_SOURCE_ID}:CH24",
)

# 《捷览》卷一·定五局长生例.
JIELAN_1581_CHANGSHENG_ANCHOR_BY_ELEMENT = {
    "金": "巳",
    "木": "亥",
    "火": "寅",
    "水": "申",
    "土": "申",
}
JIELAN_1581_CHANGSHENG_DIRECTION_RULE = {
    "YANG_MALE": "FORWARD",
    "YIN_FEMALE": "FORWARD",
    "YIN_MALE": "REVERSE",
    "YANG_FEMALE": "REVERSE",
}
JIELAN_1581_CHANGSHENG_SOURCE_REFS = (
    f"{JIELAN_1581_SOURCE_ID}:CH19",
)

# The 1581 text contains a historical dignity table, but several cells/phrases
# require edition collation before conversion into a closed 7-grade runtime table.
# Keep the source family registered without silently normalizing it.
JIELAN_1581_DIGNITY_SOURCE_STATUS = "SOURCE_TABLE_PRESENT_NORMALIZATION_PENDING"
JIELAN_1581_DIGNITY_SOURCE_REFS = (
    f"{JIELAN_1581_SOURCE_ID}:CH69",
    f"{JIELAN_1581_SOURCE_ID}:CH70",
)


def historical_candidate_payload() -> dict[str, object]:
    return {
        "rule_set_id": JIELAN_1581_RULE_SET_ID,
        "rule_set_version": JIELAN_1581_RULE_SET_VERSION,
        "selection_status": JIELAN_1581_SELECTION_STATUS,
        "source_id": JIELAN_1581_SOURCE_ID,
        "four_transformations": JIELAN_1581_FOUR_TRANSFORMATIONS,
        "kui_yue_by_stem": JIELAN_1581_KUI_YUE_BY_STEM,
        "fire_bell_start_by_year_branch": JIELAN_1581_FIRE_BELL_START_BY_YEAR_BRANCH,
        "tianshang_tianshi_offsets": JIELAN_1581_TIANSHANG_TIANSHI_OFFSETS,
        "changsheng_anchor_by_element": JIELAN_1581_CHANGSHENG_ANCHOR_BY_ELEMENT,
        "changsheng_direction_rule": JIELAN_1581_CHANGSHENG_DIRECTION_RULE,
        "dignity_source_status": JIELAN_1581_DIGNITY_SOURCE_STATUS,
    }


def historical_candidate_hash() -> str:
    return object_sha256(historical_candidate_payload())


def validate_historical_candidate_registry() -> None:
    if tuple(JIELAN_1581_FOUR_TRANSFORMATIONS) != tuple("甲乙丙丁戊己庚辛壬癸"):
        raise ValueError("Jielan 1581 Four-Transformation table must cover all ten stems in order")
    if set(JIELAN_1581_KUI_YUE_BY_STEM) != set("甲乙丙丁戊己庚辛壬癸"):
        raise ValueError("Jielan 1581 Kui/Yue table must cover all ten stems")
    if set(JIELAN_1581_FIRE_BELL_START_BY_YEAR_BRANCH) != set("子丑寅卯辰巳午未申酉戌亥"):
        raise ValueError("Jielan 1581 Fire/Bell table must cover all twelve year branches")
    if set(JIELAN_1581_CHANGSHENG_ANCHOR_BY_ELEMENT) != {"金", "木", "火", "水", "土"}:
        raise ValueError("Jielan 1581 Changsheng anchors must cover five bureau elements")
    if JIELAN_1581_SELECTION_STATUS != "PRESERVED_NOT_SELECTED":
        raise ValueError("historical candidate registry must not become production-selected implicitly")
    if JIELAN_1581_DIGNITY_SOURCE_STATUS != "SOURCE_TABLE_PRESENT_NORMALIZATION_PENDING":
        raise ValueError("Jielan dignity must remain unnormalized until edition collation closes")


validate_historical_candidate_registry()
