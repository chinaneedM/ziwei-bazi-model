from __future__ import annotations

from .registries import CONTROLS, GENERATES, STEM_ELEMENTS, STEM_POLARITY, validate_stem


TEN_GOD_ALGORITHM_ID = "BAZI-TEN-GOD-GENERATOR-V1"
TEN_GOD_ALGORITHM_VERSION = "1.0.0"

TEN_GOD_DISPLAY = {
    "BIJIAN": "比肩",
    "JIECAI": "劫财",
    "SHISHEN": "食神",
    "SHANGGUAN": "伤官",
    "PIANCAI": "偏财",
    "ZHENGCAI": "正财",
    "QISHA": "七杀",
    "ZHENGGUAN": "正官",
    "PIANIN": "偏印",
    "ZHENGIN": "正印",
}


def ten_god_semantic_id(day_master: str, target_stem: str) -> str:
    day_master = validate_stem(day_master)
    target_stem = validate_stem(target_stem)
    day_element = STEM_ELEMENTS[day_master]
    target_element = STEM_ELEMENTS[target_stem]
    same_polarity = STEM_POLARITY[day_master] == STEM_POLARITY[target_stem]

    if target_element == day_element:
        return "BIJIAN" if same_polarity else "JIECAI"
    if GENERATES[target_element] == day_element:
        return "PIANIN" if same_polarity else "ZHENGIN"
    if GENERATES[day_element] == target_element:
        return "SHISHEN" if same_polarity else "SHANGGUAN"
    if CONTROLS[day_element] == target_element:
        return "PIANCAI" if same_polarity else "ZHENGCAI"
    if CONTROLS[target_element] == day_element:
        return "QISHA" if same_polarity else "ZHENGGUAN"
    raise ValueError("unreachable ten-god relationship")


def ten_god(day_master: str, target_stem: str) -> tuple[str, str]:
    semantic_id = ten_god_semantic_id(day_master, target_stem)
    return semantic_id, TEN_GOD_DISPLAY[semantic_id]
