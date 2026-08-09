from __future__ import annotations

from .models import RoleBinding


ROLE_ALGORITHM_ID = "ZIWEI-ROLE-BINDINGS-V1"
ROLE_ALGORITHM_VERSION = "1.0.0"
QS_ROLE_RULE_SET_ID = "QS_EWITNESS_ROLE_R1"
QS_ROLE_RULE_SET_VERSION = "1.0.0"
WENMO_DEFAULT_ROLE_RULE_SET_ID = "WENMO_DEFAULT_ROLE_R1"
WENMO_DEFAULT_ROLE_RULE_SET_VERSION = "1.0.0"


class RoleGenerationError(ValueError):
    def __init__(self, diagnostic_code: str) -> None:
        super().__init__(diagnostic_code)
        self.diagnostic_code = diagnostic_code


MINGZHU_BY_LIFE_BRANCH = {
    "子": ("STAR.TANLANG", "贪狼"),
    "丑": ("STAR.JUMEN", "巨门"),
    "寅": ("STAR.LUCUN", "禄存"),
    "卯": ("STAR.WENQU", "文曲"),
    "辰": ("STAR.LIANZHEN", "廉贞"),
    "巳": ("STAR.WUQU", "武曲"),
    "午": ("STAR.POJUN", "破军"),
    "未": ("STAR.WUQU", "武曲"),
    "申": ("STAR.LIANZHEN", "廉贞"),
    "酉": ("STAR.WENQU", "文曲"),
    "戌": ("STAR.LUCUN", "禄存"),
    "亥": ("STAR.JUMEN", "巨门"),
}

SHENZHU_COMMON_BY_YEAR_BRANCH = {
    "丑": ("STAR.TIANXIANG", "天相"),
    "未": ("STAR.TIANXIANG", "天相"),
    "寅": ("STAR.TIANLIANG", "天梁"),
    "申": ("STAR.TIANLIANG", "天梁"),
    "卯": ("STAR.TIANTONG", "天同"),
    "酉": ("STAR.TIANTONG", "天同"),
    "辰": ("STAR.WENCHANG", "文昌"),
    "戌": ("STAR.WENCHANG", "文昌"),
    "巳": ("STAR.TIANJI", "天机"),
    "亥": ("STAR.TIANJI", "天机"),
}

WENMO_SHENZHU_BY_YEAR_BRANCH = {
    **SHENZHU_COMMON_BY_YEAR_BRANCH,
    "子": ("STAR.HUOXING", "火星"),
    "午": ("STAR.HUOXING", "火星"),
}


def _binding(
    role_id: str,
    display_name: str,
    entity_id: str,
    entity_display_name: str,
    basis_type: str,
    basis_value: str,
    source_refs: tuple[str, ...],
) -> RoleBinding:
    return RoleBinding(
        role_id=role_id,
        display_name=display_name,
        entity_id=entity_id,
        entity_display_name=entity_display_name,
        basis_type=basis_type,
        basis_value=basis_value,
        generator_id=ROLE_ALGORITHM_ID,
        algorithm_version=ROLE_ALGORITHM_VERSION,
        source_refs=source_refs,
    )


class QSRoleGenerator:
    """Strict QS role bindings with explicit preservation of the 子午身主 wording ambiguity."""

    rule_set_id = QS_ROLE_RULE_SET_ID
    rule_set_version = QS_ROLE_RULE_SET_VERSION

    @staticmethod
    def mingzhu(life_branch: str) -> RoleBinding:
        try:
            entity_id, name = MINGZHU_BY_LIFE_BRANCH[life_branch]
        except KeyError as exc:
            raise ValueError(f"unsupported Life branch for Mingzhu: {life_branch}") from exc
        return _binding(
            "ROLE.MINGZHU",
            "命主",
            entity_id,
            name,
            "LIFE_PALACE_BRANCH",
            life_branch,
            ("S01:ZZQS-A-1995", "S01:ZZQS-A-1996", "S01:ZZQS-A-1997", "S01:ZZZA-PR-054"),
        )

    @staticmethod
    def shenzhu(birth_year_branch: str) -> RoleBinding:
        if birth_year_branch in {"子", "午"}:
            raise RoleGenerationError("QS_SHENZHU_ZI_WU_TEXTUAL_AMBIGUITY")
        try:
            entity_id, name = SHENZHU_COMMON_BY_YEAR_BRANCH[birth_year_branch]
        except KeyError as exc:
            raise ValueError(f"unsupported birth-year branch for Shenzhu: {birth_year_branch}") from exc
        return _binding(
            "ROLE.SHENZHU",
            "身主",
            entity_id,
            name,
            "ZIWEI_BIRTH_YEAR_BRANCH",
            birth_year_branch,
            ("S01:ZZQS-A-2003", "S01:ZZQS-A-2004", "S01:ZZZA-PR-055"),
        )

    def generate(self, life_branch: str, birth_year_branch: str) -> tuple[RoleBinding, RoleBinding]:
        return (self.mingzhu(life_branch), self.shenzhu(birth_year_branch))


class WenmoDefaultRoleGenerator(QSRoleGenerator):
    """Operational role bindings matching Wenmo's default convention without mutating QS."""

    rule_set_id = WENMO_DEFAULT_ROLE_RULE_SET_ID
    rule_set_version = WENMO_DEFAULT_ROLE_RULE_SET_VERSION

    @staticmethod
    def shenzhu(birth_year_branch: str) -> RoleBinding:
        try:
            entity_id, name = WENMO_SHENZHU_BY_YEAR_BRANCH[birth_year_branch]
        except KeyError as exc:
            raise ValueError(f"unsupported birth-year branch for Wenmo Shenzhu: {birth_year_branch}") from exc
        refs = ["S01:ZZZA-PR-055"]
        if birth_year_branch == "巳":
            refs.append("COMPAT:WENMO-CHARTDIFF-006")
        return _binding(
            "ROLE.SHENZHU",
            "身主",
            entity_id,
            name,
            "ZIWEI_BIRTH_YEAR_BRANCH",
            birth_year_branch,
            tuple(refs),
        )
