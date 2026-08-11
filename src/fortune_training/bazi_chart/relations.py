from __future__ import annotations

from itertools import combinations, permutations

from .models import BranchInstance, RelationCandidate, StemInstance
from .registries import RAW_RELATION_RULE_SET_ID, RAW_RELATION_RULE_SET_VERSION


RAW_RELATION_ALGORITHM_ID = "BAZI-RAW-RELATION-GENERATOR-V1"
RAW_RELATION_ALGORITHM_VERSION = "1.1.0"

_STEM_COMBINATIONS = {
    frozenset(("甲", "己")): ("STEM.COMBINATION.JIA_JI", "土"),
    frozenset(("乙", "庚")): ("STEM.COMBINATION.YI_GENG", "金"),
    frozenset(("丙", "辛")): ("STEM.COMBINATION.BING_XIN", "水"),
    frozenset(("丁", "壬")): ("STEM.COMBINATION.DING_REN", "木"),
    frozenset(("戊", "癸")): ("STEM.COMBINATION.WU_GUI", "火"),
}

_BRANCH_SIX_HARMONY = {
    frozenset(("子", "丑")): "BRANCH.HARMONY.SIX.ZI_CHOU",
    frozenset(("寅", "亥")): "BRANCH.HARMONY.SIX.YIN_HAI",
    frozenset(("卯", "戌")): "BRANCH.HARMONY.SIX.MAO_XU",
    frozenset(("辰", "酉")): "BRANCH.HARMONY.SIX.CHEN_YOU",
    frozenset(("巳", "申")): "BRANCH.HARMONY.SIX.SI_SHEN",
    frozenset(("午", "未")): "BRANCH.HARMONY.SIX.WU_WEI",
}

_BRANCH_CLASH = {
    frozenset(("子", "午")): "BRANCH.CLASH.ZI_WU",
    frozenset(("丑", "未")): "BRANCH.CLASH.CHOU_WEI",
    frozenset(("寅", "申")): "BRANCH.CLASH.YIN_SHEN",
    frozenset(("卯", "酉")): "BRANCH.CLASH.MAO_YOU",
    frozenset(("辰", "戌")): "BRANCH.CLASH.CHEN_XU",
    frozenset(("巳", "亥")): "BRANCH.CLASH.SI_HAI",
}

# Source-faithful YHZP-CH-010 / 论十二支相穿 membership.  相穿为害 is
# preserved by the source identity, but this registry publishes only the
# neutral CHUAN occurrence fact and no Classical effect semantics.
_BRANCH_CHUAN = {
    frozenset(("子", "未")): "BRANCH.CHUAN.ZI_WEI",
    frozenset(("丑", "午")): "BRANCH.CHUAN.CHOU_WU",
    frozenset(("寅", "巳")): "BRANCH.CHUAN.YIN_SI",
    frozenset(("卯", "辰")): "BRANCH.CHUAN.MAO_CHEN",
    frozenset(("申", "亥")): "BRANCH.CHUAN.SHEN_HAI",
    frozenset(("酉", "戌")): "BRANCH.CHUAN.YOU_XU",
}

_BRANCH_TRINES = {
    frozenset(("申", "子", "辰")): ("BRANCH.TRINE.WATER", "水"),
    frozenset(("亥", "卯", "未")): ("BRANCH.TRINE.WOOD", "木"),
    frozenset(("寅", "午", "戌")): ("BRANCH.TRINE.FIRE", "火"),
    frozenset(("巳", "酉", "丑")): ("BRANCH.TRINE.METAL", "金"),
}

_DIRECTED_PUNISHMENTS = {
    ("寅", "巳"): "BRANCH.PUNISHMENT.YIN_TO_SI",
    ("巳", "申"): "BRANCH.PUNISHMENT.SI_TO_SHEN",
    ("申", "寅"): "BRANCH.PUNISHMENT.SHEN_TO_YIN",
    ("丑", "戌"): "BRANCH.PUNISHMENT.CHOU_TO_XU",
    ("戌", "未"): "BRANCH.PUNISHMENT.XU_TO_WEI",
    ("未", "丑"): "BRANCH.PUNISHMENT.WEI_TO_CHOU",
}
_SELF_PUNISHMENT_BRANCHES = {"辰", "午", "酉", "亥"}


def _relation_id(semantic_id: str, participants: tuple[str, ...]) -> str:
    return f"{semantic_id}:" + "+".join(participants)


def generate_raw_relations(
    stems: tuple[StemInstance, ...],
    branches: tuple[BranchInstance, ...],
) -> tuple[RelationCandidate, ...]:
    rows: list[RelationCandidate] = []

    for left, right in combinations(stems, 2):
        match = _STEM_COMBINATIONS.get(frozenset((left.stem, right.stem)))
        if match is None:
            continue
        semantic_id, target = match
        participants = (left.instance_id, right.instance_id)
        rows.append(
            RelationCandidate(
                relation_id=_relation_id(semantic_id, participants),
                semantic_relation_id=semantic_id,
                relation_family="STEM_COMBINATION",
                participant_instance_ids=participants,
                orientation="SYMMETRIC",
                arity=2,
                nominal_transformation_element=target,
                rule_set_id=RAW_RELATION_RULE_SET_ID,
                rule_set_version=RAW_RELATION_RULE_SET_VERSION,
                source_refs=("S14",),
            )
        )

    for left, right in combinations(branches, 2):
        pair = frozenset((left.branch, right.branch))
        for family, registry in (
            ("BRANCH_SIX_HARMONY", _BRANCH_SIX_HARMONY),
            ("BRANCH_CLASH", _BRANCH_CLASH),
            ("BRANCH_CHUAN", _BRANCH_CHUAN),
        ):
            semantic_id = registry.get(pair)
            if semantic_id is None:
                continue
            participants = (left.instance_id, right.instance_id)
            rows.append(
                RelationCandidate(
                    relation_id=_relation_id(semantic_id, participants),
                    semantic_relation_id=semantic_id,
                    relation_family=family,
                    participant_instance_ids=participants,
                    orientation="SYMMETRIC",
                    arity=2,
                    nominal_transformation_element=None,
                    rule_set_id=RAW_RELATION_RULE_SET_ID,
                    rule_set_version=RAW_RELATION_RULE_SET_VERSION,
                    source_refs=(
                        ("S14", "YHZP-CH-010")
                        if family == "BRANCH_CHUAN"
                        else ("S14",)
                    ),
                )
            )

        if left.branch != right.branch and pair == frozenset(("子", "卯")):
            semantic_id = "BRANCH.PUNISHMENT.ZI_MAO"
            participants = (left.instance_id, right.instance_id)
            rows.append(
                RelationCandidate(
                    relation_id=_relation_id(semantic_id, participants),
                    semantic_relation_id=semantic_id,
                    relation_family="BRANCH_PUNISHMENT",
                    participant_instance_ids=participants,
                    orientation="SYMMETRIC",
                    arity=2,
                    nominal_transformation_element=None,
                    rule_set_id=RAW_RELATION_RULE_SET_ID,
                    rule_set_version=RAW_RELATION_RULE_SET_VERSION,
                    source_refs=("S14",),
                )
            )

        if left.branch == right.branch and left.branch in _SELF_PUNISHMENT_BRANCHES:
            semantic_id = f"BRANCH.PUNISHMENT.SELF.{left.branch}"
            participants = (left.instance_id, right.instance_id)
            rows.append(
                RelationCandidate(
                    relation_id=_relation_id(semantic_id, participants),
                    semantic_relation_id=semantic_id,
                    relation_family="BRANCH_PUNISHMENT",
                    participant_instance_ids=participants,
                    orientation="SELF",
                    arity=2,
                    nominal_transformation_element=None,
                    rule_set_id=RAW_RELATION_RULE_SET_ID,
                    rule_set_version=RAW_RELATION_RULE_SET_VERSION,
                    source_refs=("S14",),
                )
            )

    for source, target in permutations(branches, 2):
        semantic_id = _DIRECTED_PUNISHMENTS.get((source.branch, target.branch))
        if semantic_id is None:
            continue
        participants = (source.instance_id, target.instance_id)
        rows.append(
            RelationCandidate(
                relation_id=_relation_id(semantic_id, participants),
                semantic_relation_id=semantic_id,
                relation_family="BRANCH_PUNISHMENT",
                participant_instance_ids=participants,
                orientation="DIRECTED",
                arity=2,
                nominal_transformation_element=None,
                rule_set_id=RAW_RELATION_RULE_SET_ID,
                rule_set_version=RAW_RELATION_RULE_SET_VERSION,
                source_refs=("S14",),
            )
        )

    for members in combinations(branches, 3):
        match = _BRANCH_TRINES.get(frozenset(member.branch for member in members))
        if match is None or len({member.branch for member in members}) != 3:
            continue
        semantic_id, target = match
        participants = tuple(member.instance_id for member in members)
        rows.append(
            RelationCandidate(
                relation_id=_relation_id(semantic_id, participants),
                semantic_relation_id=semantic_id,
                relation_family="BRANCH_TRINE",
                participant_instance_ids=participants,
                orientation="GROUP",
                arity=3,
                nominal_transformation_element=target,
                rule_set_id=RAW_RELATION_RULE_SET_ID,
                rule_set_version=RAW_RELATION_RULE_SET_VERSION,
                source_refs=("S14",),
            )
        )

    unique = {row.relation_id: row for row in rows}
    return tuple(unique[key] for key in sorted(unique))
