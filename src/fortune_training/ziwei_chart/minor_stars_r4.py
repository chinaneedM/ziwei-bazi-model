from __future__ import annotations

from .minor_stars import (
    MINOR_STAR_ALGORITHM_ID,
    MINOR_STAR_ALGORITHM_VERSION,
    WENMO_DEFAULT_MINOR_RULE_SET_ID,
    MinorStarContext,
    WenmoDefaultMinorStarGenerator,
    _placement,
)
from .models import Placement
from .registries import branch_index


# Same operational rule-set family, new immutable content version.  The legacy
# v1.0.0 generator remains untouched in minor_stars.py for R3 profile replay.
WENMO_DEFAULT_MINOR_R4_RULE_SET_ID = WENMO_DEFAULT_MINOR_RULE_SET_ID
WENMO_DEFAULT_MINOR_R4_RULE_SET_VERSION = "2.0.0"

R4_ADDED_MINOR_ENTITY_IDS = frozenset(
    {
        "STAR.TIANSHOU",
        "STAR.TIANSHANG",
        "STAR.TIANSHI",
    }
)


class WenmoDefaultMinorStarR4Generator(WenmoDefaultMinorStarGenerator):
    """Wenmo-default V1 operational minor content extended by 天寿/天伤/天使.

    Placement identity is profile-bound and deliberately separate from historical
    source truth.  The alternate yin/yang-sex 天伤/天使 family remains preserved in
    source material; this runtime version selects the fixed 交友/疾厄 convention
    established by the compatibility discriminator.
    """

    rule_set_id = WENMO_DEFAULT_MINOR_R4_RULE_SET_ID
    rule_set_version = WENMO_DEFAULT_MINOR_R4_RULE_SET_VERSION
    algorithm_id = MINOR_STAR_ALGORITHM_ID
    algorithm_version = MINOR_STAR_ALGORITHM_VERSION

    @staticmethod
    def r4_stars(context: MinorStarContext) -> tuple[Placement, Placement, Placement]:
        year_branch_offset = branch_index(context.ziwei_birth_year_branch)
        return (
            _placement(
                "STAR.TIANSHOU",
                "天寿",
                context.body_address.index + year_branch_offset,
                (
                    "S01:ZZZA-PR-042",
                    "COMPAT:WENMO-TIANSHOU-BODY-BASIS:1992-06-10T14:00",
                ),
            ),
            _placement(
                "STAR.TIANSHANG",
                "天伤",
                context.life_address.index + 5,
                (
                    "S01:ZZQS-A-1855",
                    "COMPAT:WENMO-TIANSHANG-TIANSHI-FIXED:1975-05-20T12:00",
                ),
            ),
            _placement(
                "STAR.TIANSHI",
                "天使",
                context.life_address.index + 7,
                (
                    "S01:ZZQS-A-1855",
                    "COMPAT:WENMO-TIANSHANG-TIANSHI-FIXED:1975-05-20T12:00",
                ),
            ),
        )

    def generate(self, context: MinorStarContext) -> tuple[Placement, ...]:
        rows = list(super().generate(context))
        rows.extend(self.r4_stars(context))
        return tuple(rows)
