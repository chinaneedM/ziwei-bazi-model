"""Project-owned operational Dignity rows added by R4.

The three 12-branch rows are mechanically closed from the 21-chart R3
calibration set plus the two minimal closure exports.  Wenmo is provenance and
compatibility evidence only, not canonical source authority.
"""

# Branch order is the project Z12 order: 子丑寅卯辰巳午未申酉戌亥.
_GRADED_ROWS: dict[str, tuple[str, str]] = {
    "STAR.TIANSHOU": ("子丑寅卯辰巳午未申酉戌亥", "平庙旺陷庙平平旺旺平庙旺"),
    "STAR.TIANSHANG": ("子丑寅卯辰巳午未申酉戌亥", "陷平平陷平平陷陷平平平旺"),
    "STAR.TIANSHI": ("子丑寅卯辰巳午未申酉戌亥", "陷陷平平陷平平平平陷陷旺"),
}

OPERATIONAL_R4_ADDED_DIGNITY_RAW_BY_BRANCH: dict[str, dict[str, tuple[str, str | None]]] = {
    entity_id: {branch: ("GRADED", grade) for branch, grade in zip(branches, grades)}
    for entity_id, (branches, grades) in _GRADED_ROWS.items()
}
