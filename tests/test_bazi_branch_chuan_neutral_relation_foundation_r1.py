from __future__ import annotations

import unittest
from dataclasses import fields, replace
from itertools import combinations
from pathlib import Path

from fortune_training.bazi_chart import BranchInstance
from fortune_training.bazi_chart.profile import bazi_foundation_v1_profile
from fortune_training.bazi_chart.registries import (
    BRANCH_ELEMENTS,
    EARTHLY_BRANCHES,
    RAW_RELATION_RULE_SET_VERSION,
)
from fortune_training.bazi_chart.relations import (
    RAW_RELATION_ALGORITHM_VERSION,
    generate_raw_relations,
)
from fortune_training.bazi_relation_incidence import (
    bazi_relation_incidence_foundation_r1_profile,
)
from fortune_training.bazi_relation_transition import (
    bazi_relation_transition_foundation_r1_profile,
)
from fortune_training.bazi_structural import bazi_structural_context_r1_profile
from fortune_training.calendar_foundation.models import json_value
from fortune_training.calendar_foundation.policies import PolicyRegistry
from fortune_training.util import object_sha256


CHUAN_PAIRS = {
    frozenset(("子", "未")): "BRANCH.CHUAN.ZI_WEI",
    frozenset(("丑", "午")): "BRANCH.CHUAN.CHOU_WU",
    frozenset(("寅", "巳")): "BRANCH.CHUAN.YIN_SI",
    frozenset(("卯", "辰")): "BRANCH.CHUAN.MAO_CHEN",
    frozenset(("申", "亥")): "BRANCH.CHUAN.SHEN_HAI",
    frozenset(("酉", "戌")): "BRANCH.CHUAN.YOU_XU",
}
ROOT = Path(__file__).resolve().parents[1]


def branch(instance_id: str, position: str, value: str) -> BranchInstance:
    return BranchInstance(instance_id, position, value, BRANCH_ELEMENTS[value])


class BaziBranchChuanNeutralRelationFoundationR1Tests(unittest.TestCase):
    def test_exact_six_unordered_pairs_are_source_faithful_neutral_facts(self):
        for pair, semantic_id in CHUAN_PAIRS.items():
            left, right = sorted(pair, key=EARTHLY_BRANCHES.index)
            participants = (
                branch("LEFT.BRANCH", "YEAR", left),
                branch("RIGHT.BRANCH", "MONTH", right),
            )
            rows = tuple(
                row
                for row in generate_raw_relations((), participants)
                if row.relation_family == "BRANCH_CHUAN"
            )
            self.assertEqual(1, len(rows), pair)
            row = rows[0]
            self.assertEqual(semantic_id, row.semantic_relation_id)
            self.assertEqual(
                ("LEFT.BRANCH", "RIGHT.BRANCH"),
                row.participant_instance_ids,
            )
            self.assertEqual("SYMMETRIC", row.orientation)
            self.assertEqual(2, row.arity)
            self.assertIsNone(row.nominal_transformation_element)
            self.assertEqual(("S14", "YHZP-CH-010"), row.source_refs)
            self.assertNotIn("HARM", row.semantic_relation_id)

    def test_all_sixty_non_pair_directions_do_not_create_chuan(self):
        observed = set()
        for left, right in combinations(EARTHLY_BRANCHES, 2):
            rows = tuple(
                row
                for row in generate_raw_relations(
                    (),
                    (
                        branch("LEFT.BRANCH", "YEAR", left),
                        branch("RIGHT.BRANCH", "MONTH", right),
                    ),
                )
                if row.relation_family == "BRANCH_CHUAN"
            )
            if frozenset((left, right)) in CHUAN_PAIRS:
                self.assertEqual(1, len(rows), (left, right))
                observed.add(frozenset((left, right)))
            else:
                self.assertEqual((), rows, (left, right))
        self.assertEqual(set(CHUAN_PAIRS), observed)

    def test_duplicate_branch_values_preserve_exact_instance_multiplicity(self):
        branches = (
            branch("YEAR.BRANCH", "YEAR", "子"),
            branch("MONTH.BRANCH", "MONTH", "子"),
            branch("DAY.BRANCH", "DAY", "未"),
        )
        rows = tuple(
            row
            for row in generate_raw_relations((), branches)
            if row.relation_family == "BRANCH_CHUAN"
        )
        self.assertEqual(2, len(rows))
        self.assertEqual(
            {
                ("YEAR.BRANCH", "DAY.BRANCH"),
                ("MONTH.BRANCH", "DAY.BRANCH"),
            },
            {row.participant_instance_ids for row in rows},
        )
        self.assertEqual(2, len({row.relation_id for row in rows}))

    def test_order_ids_and_serialized_hash_are_deterministic(self):
        branches = (
            branch("YEAR.BRANCH", "YEAR", "申"),
            branch("MONTH.BRANCH", "MONTH", "亥"),
            branch("DAY.BRANCH", "DAY", "酉"),
            branch("HOUR.BRANCH", "HOUR", "戌"),
        )
        first = generate_raw_relations((), branches)
        second = generate_raw_relations((), branches)
        self.assertEqual(first, second)
        self.assertEqual(
            sorted(row.relation_id for row in first),
            [row.relation_id for row in first],
        )
        self.assertEqual(
            object_sha256(json_value(first)),
            object_sha256(json_value(second)),
        )

    def test_chuan_has_no_classical_effect_or_outcome_fields(self):
        row = next(
            row
            for row in generate_raw_relations(
                (),
                (
                    branch("YEAR.BRANCH", "YEAR", "卯"),
                    branch("MONTH.BRANCH", "MONTH", "辰"),
                ),
            )
            if row.relation_family == "BRANCH_CHUAN"
        )
        prohibited = {
            "harm",
            "activated",
            "effective",
            "severity",
            "strength",
            "priority",
            "good_bad",
            "event",
            "outcome",
            "transformation_target",
            "transformation_success",
        }
        self.assertTrue(prohibited.isdisjoint(field.name for field in fields(row)))

    def test_old_version_identities_cannot_emit_the_new_relation_set(self):
        self.assertEqual("1.1.0", RAW_RELATION_RULE_SET_VERSION)
        self.assertEqual("1.1.0", RAW_RELATION_ALGORITHM_VERSION)

        policy_registry = PolicyRegistry.from_file(
            ROOT / "config" / "time-calendar-policies.json"
        )
        natal_profile = bazi_foundation_v1_profile(policy_registry)
        self.assertEqual("1.1.0", natal_profile.profile_version)
        with self.assertRaises(ValueError):
            replace(
                natal_profile,
                profile_version="1.0.0",
                raw_relation_rule_set_version="1.0.0",
                raw_relation_algorithm_version="1.0.0",
            ).validate(policy_registry)

        profiles = (
            bazi_structural_context_r1_profile(),
            bazi_relation_transition_foundation_r1_profile(),
            bazi_relation_incidence_foundation_r1_profile(),
        )
        for profile in profiles:
            self.assertEqual("1.1.0", profile.profile_version)
            self.assertEqual("1.1.0", profile.algorithm_version)
            with self.assertRaises(ValueError):
                replace(
                    profile,
                    profile_version="1.0.0",
                    algorithm_version="1.0.0",
                ).validate()


if __name__ == "__main__":
    unittest.main()
