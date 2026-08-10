from __future__ import annotations

from .models import (
    BranchInstance,
    HiddenStemExposureLink,
    HiddenStemMembership,
    StemBranchAffinityFact,
    StemInstance,
)
from .registries import (
    AFFINITY_RULE_SET_ID,
    AFFINITY_RULE_SET_VERSION,
    HIDDEN_STEMS,
    HIDDEN_STEM_RULE_SET_ID,
    HIDDEN_STEM_RULE_SET_VERSION,
    STEM_ELEMENTS,
)


HIDDEN_STEM_ALGORITHM_ID = "BAZI-HIDDEN-STEM-MEMBERSHIP-V1"
HIDDEN_STEM_ALGORITHM_VERSION = "1.0.1"
AFFINITY_ALGORITHM_ID = "BAZI-STEM-BRANCH-AFFINITY-V1"
AFFINITY_ALGORITHM_VERSION = "1.0.0"


def generate_hidden_stems(branches: tuple[BranchInstance, ...]) -> tuple[HiddenStemMembership, ...]:
    rows: list[HiddenStemMembership] = []
    for branch in branches:
        for ordinal, stem in enumerate(HIDDEN_STEMS[branch.branch]):
            rows.append(
                HiddenStemMembership(
                    instance_id=f"{branch.instance_id}.HIDDEN:{stem}",
                    branch_instance_id=branch.instance_id,
                    branch_position=branch.position,
                    stem=stem,
                    element=STEM_ELEMENTS[stem],
                    registry_ordinal=ordinal,
                    rule_set_id=HIDDEN_STEM_RULE_SET_ID,
                    rule_set_version=HIDDEN_STEM_RULE_SET_VERSION,
                    source_refs=("S11",),
                )
            )
    return tuple(rows)


def generate_exposures(
    visible_stems: tuple[StemInstance, ...],
    hidden_stems: tuple[HiddenStemMembership, ...],
) -> tuple[HiddenStemExposureLink, ...]:
    rows: list[HiddenStemExposureLink] = []
    for hidden in hidden_stems:
        for visible in visible_stems:
            if hidden.stem == visible.stem:
                rows.append(
                    HiddenStemExposureLink(
                        link_id=f"EXPOSE:{hidden.instance_id}->{visible.instance_id}",
                        hidden_stem_instance_id=hidden.instance_id,
                        visible_stem_instance_id=visible.instance_id,
                        stem=hidden.stem,
                        match_kind="EXACT_STEM",
                        source_refs=("S11",),
                    )
                )
    return tuple(sorted(rows, key=lambda row: row.link_id))


def generate_affinities(
    visible_stems: tuple[StemInstance, ...],
    branches: tuple[BranchInstance, ...],
    hidden_stems: tuple[HiddenStemMembership, ...],
) -> tuple[StemBranchAffinityFact, ...]:
    hidden_by_branch: dict[str, tuple[HiddenStemMembership, ...]] = {}
    for branch in branches:
        hidden_by_branch[branch.instance_id] = tuple(
            row for row in hidden_stems if row.branch_instance_id == branch.instance_id
        )

    rows: list[StemBranchAffinityFact] = []
    for visible in visible_stems:
        for branch in branches:
            hidden = hidden_by_branch[branch.instance_id]
            exact = tuple(sorted(row.instance_id for row in hidden if row.stem == visible.stem))
            same_element = tuple(sorted(row.instance_id for row in hidden if row.element == visible.element))
            rows.append(
                StemBranchAffinityFact(
                    fact_id=f"AFFINITY:{visible.instance_id}<->{branch.instance_id}",
                    visible_stem_instance_id=visible.instance_id,
                    branch_instance_id=branch.instance_id,
                    exact_hidden_stem_instance_ids=exact,
                    same_element_hidden_stem_instance_ids=same_element,
                    rule_set_id=AFFINITY_RULE_SET_ID,
                    rule_set_version=AFFINITY_RULE_SET_VERSION,
                    source_refs=("S11",),
                )
            )
    return tuple(rows)
