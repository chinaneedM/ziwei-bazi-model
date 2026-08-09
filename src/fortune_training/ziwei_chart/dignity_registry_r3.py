"""Project-owned operational dependency/minor Dignity registry data for R3.

Generated from the closed 21-export external compatibility calibration set.
External software is provenance only and is not canonical source authority.
"""

# Each graded row is (reachable-branch sequence, parallel one-character grade sequence).
# UNRATED rows list only their reachable branches; unreachable cells do not exist.
_GRADED_ROWS: dict[str, tuple[str, str]] = {
    "STAR.SANTAI": ("子丑寅卯辰巳午未申酉戌亥", "平庙平陷庙平旺庙旺庙旺平"),
    "STAR.BAZUO": ("子丑寅卯辰巳午未申酉戌亥", "陷庙庙平旺庙旺平庙庙平庙"),
    "STAR.ENGUANG": ("子丑寅卯辰巳午未申酉戌亥", "平庙平庙庙平庙旺平陷庙不"),
    "STAR.TIANGUI": ("子丑寅卯辰巳午未申酉戌亥", "庙旺平旺旺平庙旺陷庙旺平"),
    "STAR.TIANGUAN": ("寅卯辰巳午未酉戌亥", "平旺旺旺庙庙平平旺"),
    "STAR.TIANFU_BLESSING": ("子寅卯巳午申酉亥", "平旺平旺平庙庙庙"),
    "STAR.JIEKONG": ("子丑寅卯辰巳午未申酉", "陷不陷平陷庙庙庙庙庙"),
    "STAR.FU_JIEKONG": ("子丑寅卯辰巳午未申酉", "陷不陷平陷庙庙庙庙庙"),
    "STAR.XUNKONG": ("子丑寅卯辰巳午未申酉戌亥", "陷平陷平陷庙庙陷庙庙陷平"),
    "STAR.FU_XUNKONG": ("子丑寅卯辰巳午未申酉戌亥", "陷平陷平陷庙庙陷庙庙陷平"),
    "STAR.TIANKONG": ("子丑寅卯辰巳午未申酉戌亥", "陷平陷平庙庙庙陷旺旺陷平"),
    "STAR.TIANKU": ("子丑寅卯辰巳午未申酉戌亥", "平庙平庙平不陷平庙不平平"),
    "STAR.TIANXU": ("子丑寅卯辰巳午未申酉戌亥", "陷庙旺庙陷旺平陷庙旺陷平"),
    "STAR.HONGLUAN": ("子丑寅卯辰巳午未申酉戌亥", "庙陷旺庙庙旺旺陷庙旺陷庙"),
    "STAR.TIANXI": ("子丑寅卯辰巳午未申酉戌亥", "旺陷庙旺陷庙庙陷旺庙陷旺"),
    "STAR.GUCHEN": ("寅巳申亥", "平陷平陷"),
    "STAR.GUASU": ("丑辰未戌", "平陷不陷"),
    "STAR.DAHAO": ("子丑寅卯辰巳午未申酉戌亥", "旺平陷不平陷旺平陷不平陷"),
    "STAR.POSUI": ("丑巳酉", "陷陷平"),
    "STAR.HUAGAI": ("丑辰未戌", "陷庙陷平"),
    "STAR.XIANCHI": ("子卯午酉", "陷平陷平"),
    "STAR.TIANDE": ("子丑寅卯辰巳午未申酉戌亥", "庙庙平平庙旺旺庙平不庙平"),
    "STAR.NIANJIE": ("子丑寅卯辰巳午未申酉戌亥", "庙得庙庙庙旺庙得利旺庙得"),
    "STAR.TIANCAI": ("子丑寅卯辰巳午未申酉戌亥", "旺平庙旺陷庙旺平庙旺陷庙"),
    "STAR.LONGCHI": ("子丑寅卯辰巳午未申酉戌亥", "旺平平庙庙陷不庙平庙陷旺"),
    "STAR.FENGGE": ("子丑寅卯辰巳午未申酉戌亥", "庙平庙旺陷庙平陷不庙庙旺"),
    "STAR.TIANXING": ("子丑寅卯辰巳午未申酉戌亥", "平陷庙庙平陷平陷陷庙庙陷"),
    "STAR.TIANYAO": ("子丑寅卯辰巳午未申酉戌亥", "陷平旺庙陷平平旺陷庙庙陷"),
    "STAR.JIESHEN": ("子寅辰午申戌", "庙庙庙庙不庙"),
}

_UNRATED_ROWS: dict[str, str] = {
    "STAR.TIANCHU": "子寅巳午申酉亥",
    "STAR.JIESHA": "寅巳申亥",
    "STAR.FEILIAN": "子丑寅卯辰巳午未申酉戌亥",
    "STAR.LONGDE": "子丑寅卯辰巳午未申酉戌亥",
    "STAR.YUEDE": "子丑寅卯辰巳午未申酉戌亥",
    "STAR.TAIFU": "子丑寅卯辰巳午未申酉戌亥",
    "STAR.FENGGAO": "子丑寅卯辰巳午未申酉戌亥",
    "STAR.TIANWU": "寅巳申亥",
    "STAR.TIANYUE_MOON": "寅卯辰巳午未戌亥",
    "STAR.YINSHA": "子寅辰午申戌",
}

OPERATIONAL_DEPENDENCY_MINOR_DIGNITY_RAW_BY_BRANCH: dict[str, dict[str, tuple[str, str | None]]] = {
    entity_id: {branch: ("GRADED", grade) for branch, grade in zip(branches, grades)}
    for entity_id, (branches, grades) in _GRADED_ROWS.items()
}
OPERATIONAL_DEPENDENCY_MINOR_DIGNITY_RAW_BY_BRANCH.update(
    {
        entity_id: {branch: ("UNRATED", None) for branch in branches}
        for entity_id, branches in _UNRATED_ROWS.items()
    }
)
