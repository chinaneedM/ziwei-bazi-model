from __future__ import annotations

from itertools import combinations

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .models import BaziNatalState, RelationCandidate
from .relations import _STEM_COMBINATIONS


HISTORICAL_RELATION_CANDIDATE_RULE_SET_ID = "BAZI-HISTORICAL-RELATION-CANDIDATES-R1"
HISTORICAL_RELATION_CANDIDATE_RULE_SET_VERSION = "1.0.0"
HISTORICAL_RELATION_CANDIDATE_SELECTION_STATUS = "PRESERVED_NOT_SELECTED"
HISTORICAL_RELATION_CANDIDATE_RUNTIME_RESOLVER_ID = (
    "BAZI-HISTORICAL-RELATION-SOURCE-SCOPED-CANDIDATE-RUNTIME-R1"
)
HISTORICAL_RELATION_CANDIDATE_RUNTIME_RESOLVER_VERSION = "1.0.0"

_FOUR_EARTH_MEMBERS = frozenset(("辰", "戌", "丑", "未"))
_FOUR_EARTH_SOURCE_REFS = (
    "S14:YHZP-CH-008",
    "EXT-CTEXT-SANMING-V1-FOUR-EARTH-BUREAU",
)

_DIRECTIONAL_TRIADS = {
    frozenset(("寅", "卯", "辰")): (
        "BRANCH.DIRECTIONAL_TRIAD.EAST.WOOD",
        "木",
        "EAST",
    ),
    frozenset(("巳", "午", "未")): (
        "BRANCH.DIRECTIONAL_TRIAD.SOUTH.FIRE",
        "火",
        "SOUTH",
    ),
    frozenset(("申", "酉", "戌")): (
        "BRANCH.DIRECTIONAL_TRIAD.WEST.METAL",
        "金",
        "WEST",
    ),
    frozenset(("亥", "子", "丑")): (
        "BRANCH.DIRECTIONAL_TRIAD.NORTH.WATER",
        "水",
        "NORTH",
    ),
}
_DIRECTIONAL_TRIAD_SOURCE_REFS = (
    "EXT-CTEXT-SANMING-V6-DIRECTIONAL-TRIADS",
    "S14:DTCW-REN-COMMENTARY-CANDIDATE",
)

_EARLY_BREAKS = {
    frozenset(("卯", "午")): "BRANCH.BREAK.EARLY.MAO_WU",
    frozenset(("丑", "辰")): "BRANCH.BREAK.EARLY.CHOU_CHEN",
    frozenset(("子", "酉")): "BRANCH.BREAK.EARLY.ZI_YOU",
    frozenset(("未", "戌")): "BRANCH.BREAK.EARLY.WEI_XU",
}
_EARLY_BREAK_SOURCE_REFS = ("EXT-CTEXT-WUXING-JINGJI-V23-BREAK",)

_STEM_HIDDEN_SOURCE_REFS = (
    "EXT-CTEXT-SANMING-V2-ZUOXIA-ZIHUA",
    "EXT-CTEXT-MINGLI-TANYUAN-RELATIONS",
)


def historical_relation_candidate_registry_payload() -> dict[str, object]:
    return {
        "schema": "BAZI-HISTORICAL-RELATION-CANDIDATE-REGISTRY-R1",
        "rule_set_id": HISTORICAL_RELATION_CANDIDATE_RULE_SET_ID,
        "rule_set_version": HISTORICAL_RELATION_CANDIDATE_RULE_SET_VERSION,
        "selection_status": HISTORICAL_RELATION_CANDIDATE_SELECTION_STATUS,
        "families": {
            "four_earth_bureau": {
                "members": ("辰", "戌", "丑", "未"),
                "relation_family": "FOUR_EARTH_BUREAU",
                "semantic_relation_id": "BRANCH.FOUR_EARTH_BUREAU.EARTH",
                "nominal_transformation_element": "土",
                "source_refs": _FOUR_EARTH_SOURCE_REFS,
            },
            "directional_triads": tuple(
                {
                    "members": tuple(sorted(members)),
                    "semantic_relation_id": semantic_id,
                    "nominal_transformation_element": element,
                    "direction": direction,
                    "source_refs": _DIRECTIONAL_TRIAD_SOURCE_REFS,
                }
                for members, (semantic_id, element, direction) in sorted(
                    _DIRECTIONAL_TRIADS.items(),
                    key=lambda item: item[1][0],
                )
            ),
            "early_four_break": tuple(
                {
                    "members": tuple(sorted(members)),
                    "semantic_relation_id": semantic_id,
                    "source_refs": _EARLY_BREAK_SOURCE_REFS,
                }
                for members, semantic_id in sorted(
                    _EARLY_BREAKS.items(),
                    key=lambda item: item[1],
                )
            ),
            "same_pillar_stem_hidden_combination": {
                "mechanical_basis": (
                    "VISIBLE_STEM_AND_HIDDEN_STEM_IN_THE_SAME_PILLAR_MATCH_"
                    "THE_EXISTING_FIVE_STEM_COMBINATION_REGISTRY"
                ),
                "relation_family": "STEM_HIDDEN_COMBINATION",
                "source_refs": _STEM_HIDDEN_SOURCE_REFS,
                "automatic_transformation_permission": False,
            },
        },
    }


def historical_relation_candidate_registry_hash() -> str:
    return object_sha256(historical_relation_candidate_registry_payload())


def _relation_id(semantic_id: str, participants: tuple[str, ...]) -> str:
    return f"{semantic_id}:" + "+".join(participants)


def _candidate(
    *,
    semantic_id: str,
    relation_family: str,
    participants: tuple[str, ...],
    orientation: str,
    nominal_element: str | None,
    source_refs: tuple[str, ...],
) -> RelationCandidate:
    return RelationCandidate(
        relation_id=_relation_id(semantic_id, participants),
        semantic_relation_id=semantic_id,
        relation_family=relation_family,
        participant_instance_ids=participants,
        orientation=orientation,
        arity=len(participants),
        nominal_transformation_element=nominal_element,
        rule_set_id=HISTORICAL_RELATION_CANDIDATE_RULE_SET_ID,
        rule_set_version=HISTORICAL_RELATION_CANDIDATE_RULE_SET_VERSION,
        source_refs=source_refs,
    )


def resolve_bazi_historical_relation_candidates(chart: BaziNatalState) -> dict[str, object]:
    """Materialize source-scoped relation candidates without changing raw core facts."""

    rows: list[RelationCandidate] = []

    for members in combinations(chart.branches, 4):
        if (
            len({member.branch for member in members}) == 4
            and frozenset(member.branch for member in members) == _FOUR_EARTH_MEMBERS
        ):
            participants = tuple(member.instance_id for member in members)
            rows.append(
                _candidate(
                    semantic_id="BRANCH.FOUR_EARTH_BUREAU.EARTH",
                    relation_family="FOUR_EARTH_BUREAU",
                    participants=participants,
                    orientation="GROUP",
                    nominal_element="土",
                    source_refs=_FOUR_EARTH_SOURCE_REFS,
                )
            )

    for members in combinations(chart.branches, 3):
        branch_set = frozenset(member.branch for member in members)
        match = _DIRECTIONAL_TRIADS.get(branch_set)
        if match is None or len({member.branch for member in members}) != 3:
            continue
        semantic_id, element, _direction = match
        participants = tuple(member.instance_id for member in members)
        rows.append(
            _candidate(
                semantic_id=semantic_id,
                relation_family="DIRECTIONAL_TRIAD",
                participants=participants,
                orientation="GROUP",
                nominal_element=element,
                source_refs=_DIRECTIONAL_TRIAD_SOURCE_REFS,
            )
        )

    for left, right in combinations(chart.branches, 2):
        semantic_id = _EARLY_BREAKS.get(frozenset((left.branch, right.branch)))
        if semantic_id is None:
            continue
        rows.append(
            _candidate(
                semantic_id=semantic_id,
                relation_family="BRANCH_BREAK_EARLY_FOUR",
                participants=(left.instance_id, right.instance_id),
                orientation="SYMMETRIC",
                nominal_element=None,
                source_refs=_EARLY_BREAK_SOURCE_REFS,
            )
        )

    branch_by_position = {row.position: row for row in chart.branches}
    hidden_by_branch: dict[str, tuple[object, ...]] = {}
    for branch in chart.branches:
        hidden_by_branch[branch.instance_id] = tuple(
            row for row in chart.hidden_stems if row.branch_instance_id == branch.instance_id
        )

    for visible in chart.stems:
        branch = branch_by_position.get(visible.position)
        if branch is None:
            continue
        for hidden in hidden_by_branch.get(branch.instance_id, ()):
            match = _STEM_COMBINATIONS.get(frozenset((visible.stem, hidden.stem)))
            if match is None:
                continue
            base_semantic_id, target = match
            semantic_id = base_semantic_id.replace(
                "STEM.COMBINATION.",
                "STEM_HIDDEN.COMBINATION.",
                1,
            )
            rows.append(
                _candidate(
                    semantic_id=semantic_id,
                    relation_family="STEM_HIDDEN_COMBINATION",
                    participants=(visible.instance_id, hidden.instance_id),
                    orientation="WITHIN_PILLAR",
                    nominal_element=target,
                    source_refs=_STEM_HIDDEN_SOURCE_REFS,
                )
            )

    unique = {row.relation_id: row for row in rows}
    candidates = tuple(unique[key] for key in sorted(unique))
    payload: dict[str, object] = {
        "schema": "BAZI-HISTORICAL-RELATION-SOURCE-SCOPED-CANDIDATE-RUNTIME-R1",
        "rule_set_id": HISTORICAL_RELATION_CANDIDATE_RULE_SET_ID,
        "rule_set_version": HISTORICAL_RELATION_CANDIDATE_RULE_SET_VERSION,
        "selection_status": HISTORICAL_RELATION_CANDIDATE_SELECTION_STATUS,
        "runtime_resolver_id": HISTORICAL_RELATION_CANDIDATE_RUNTIME_RESOLVER_ID,
        "runtime_resolver_version": HISTORICAL_RELATION_CANDIDATE_RUNTIME_RESOLVER_VERSION,
        "registry_hash": historical_relation_candidate_registry_hash(),
        "upstream_profile_id": chart.profile_id,
        "upstream_profile_version": chart.profile_version,
        "upstream_raw_relation_count": len(chart.raw_relations),
        "candidate_count": len(candidates),
        "candidates": json_value(candidates),
    }
    return {
        **payload,
        "runtime_hash": object_sha256(payload),
    }


def validate_historical_relation_candidate_registry() -> None:
    payload = historical_relation_candidate_registry_payload()
    if payload["selection_status"] != "PRESERVED_NOT_SELECTED":
        raise ValueError("historical Bazi relation candidates must remain unselected")
    if len(_FOUR_EARTH_MEMBERS) != 4:
        raise ValueError("four-earth bureau must contain four distinct branches")
    if len(_DIRECTIONAL_TRIADS) != 4:
        raise ValueError("directional-triad registry must contain four groups")
    if any(len(members) != 3 for members in _DIRECTIONAL_TRIADS):
        raise ValueError("every directional-triad candidate must contain three branches")
    if len(_EARLY_BREAKS) != 4:
        raise ValueError("early break registry must preserve the four-pair source table")
    later_only_pairs = {
        frozenset(("寅", "亥")),
        frozenset(("巳", "申")),
    }
    if later_only_pairs & set(_EARLY_BREAKS):
        raise ValueError("later six-break additions must not leak into the early four-break registry")
    if set(_STEM_COMBINATIONS) != {
        frozenset(("甲", "己")),
        frozenset(("乙", "庚")),
        frozenset(("丙", "辛")),
        frozenset(("丁", "壬")),
        frozenset(("戊", "癸")),
    }:
        raise ValueError("same-pillar candidate must reuse the frozen five-stem combination registry")


validate_historical_relation_candidate_registry()
