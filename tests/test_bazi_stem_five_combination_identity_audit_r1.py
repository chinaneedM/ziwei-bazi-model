from __future__ import annotations

import json
import unittest
from itertools import combinations, product
from pathlib import Path
from types import SimpleNamespace

from fortune_training.bazi_chart.models import StemInstance
from fortune_training.bazi_chart.registries import HEAVENLY_STEMS, STEM_ELEMENTS, STEM_POLARITY
from fortune_training.bazi_chart.relations import generate_raw_relations
from fortune_training.bazi_facts import STEM_COMBINATIONS
from fortune_training.combined_chart_application.bazi_stem_relation_local_app import _stem_relation_rows


ROOT = Path(__file__).resolve().parents[1]
ORACLE = json.loads((ROOT / "tests/fixtures/bazi-stem-five-combination-physical-oracle-r1.json").read_text(encoding="utf-8"))
PAIRS = {frozenset(row["members"]): row["semantic_id"] for row in ORACLE["pairs"]}
POSITIONS = ("YEAR", "MONTH", "DAY", "HOUR")


def stems_for(values):
    return tuple(
        StemInstance(f"AUDIT:{position}", position, stem, STEM_ELEMENTS[stem], STEM_POLARITY[stem])
        for position, stem in zip(POSITIONS, values)
    )


class BaziStemFiveCombinationIdentityAuditR1Tests(unittest.TestCase):
    def test_100_ordered_stem_pairs_match_direct_physical_identity_table(self):
        for left, right in product(HEAVENLY_STEMS, repeat=2):
            rows = generate_raw_relations(stems_for((left, right)), ())
            expected = PAIRS.get(frozenset((left, right)))
            with self.subTest(left=left, right=right):
                self.assertEqual(0 if expected is None else 1, len(rows))
                if rows:
                    self.assertEqual(expected, rows[0].semantic_relation_id)
                    self.assertEqual("SYMMETRIC", rows[0].orientation)
                    self.assertEqual(2, rows[0].arity)

    def test_all_10000_four_stem_grids_preserve_exact_instance_occurrences(self):
        total_occurrences = 0
        for values in product(HEAVENLY_STEMS, repeat=4):
            stems = stems_for(values)
            expected = {
                (PAIRS[frozenset((a.stem, b.stem))], (a.instance_id, b.instance_id))
                for a, b in combinations(stems, 2)
                if frozenset((a.stem, b.stem)) in PAIRS
            }
            raw = generate_raw_relations(stems, ())
            actual = {(row.semantic_relation_id, row.participant_instance_ids) for row in raw}
            self.assertEqual(expected, actual, values)
            self.assertEqual(len(expected), len(raw), values)
            projected = _stem_relation_rows(SimpleNamespace(stems=stems, raw_relations=raw))
            self.assertEqual(len(raw), len(projected), values)
            for row, view in zip(raw, projected):
                self.assertEqual(row.semantic_relation_id, view["semantic_relation_id"])
                self.assertEqual(row.participant_instance_ids, tuple(p["instance_id"] for p in view["participants"]))
                self.assertEqual([values[POSITIONS.index(p["position"])] for p in view["participants"]], [p["stem"] for p in view["participants"]])
            total_occurrences += len(raw)
        self.assertEqual(6000, total_occurrences)

    def test_repeated_members_preserve_four_distinct_relations_without_winner(self):
        raw = generate_raw_relations(stems_for(("甲", "己", "甲", "己")), ())
        self.assertEqual(4, len(raw))
        self.assertEqual(4, len({row.relation_id for row in raw}))
        self.assertEqual({"STEM.COMBINATION.JIA_JI"}, {row.semantic_relation_id for row in raw})
        self.assertEqual({("AUDIT:YEAR", "AUDIT:MONTH"), ("AUDIT:YEAR", "AUDIT:HOUR"), ("AUDIT:MONTH", "AUDIT:DAY"), ("AUDIT:DAY", "AUDIT:HOUR")}, {row.participant_instance_ids for row in raw})

    def test_neutral_presentation_omits_nominal_targets_and_outcome_fields(self):
        allowed = {"relation_id", "semantic_relation_id", "relation_family", "orientation", "arity", "participants", "rule_set_id", "rule_set_version", "source_refs"}
        seen = set()
        for pair in ORACLE["pairs"]:
            stems = stems_for(pair["members"])
            raw = generate_raw_relations(stems, ())
            self.assertIsNotNone(raw[0].nominal_transformation_element)
            view = _stem_relation_rows(SimpleNamespace(stems=stems, raw_relations=raw))[0]
            self.assertEqual(allowed, set(view))
            seen.add(view["semantic_relation_id"])
        self.assertEqual(set(PAIRS.values()), seen)

    def test_legacy_fact_registry_has_the_same_five_member_identities(self):
        self.assertEqual(set(PAIRS), set(STEM_COMBINATIONS))


if __name__ == "__main__":
    unittest.main()
