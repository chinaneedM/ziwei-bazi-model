from __future__ import annotations

import unittest

from fortune_training.ziwei_chart.dignity_historical_candidates import (
    JIELAN_1581_DIGNITY_NORMALIZATION_STATUS,
    JIELAN_1581_DIGNITY_SELECTION_STATUS,
    jielan_1581_dignity_lexeme_registry_payload,
    resolve_jielan_1581_dignity_lexeme_candidate,
)


class Jielan1581DignityLexemeCandidateTest(unittest.TestCase):
    def test_registry_preserves_source_lexemes_without_production_grade_mapping(self) -> None:
        payload = jielan_1581_dignity_lexeme_registry_payload()
        self.assertEqual(25, payload["entity_count"])
        self.assertEqual(300, payload["cell_count"])
        self.assertEqual("PRESERVED_NOT_SELECTED", JIELAN_1581_DIGNITY_SELECTION_STATUS)
        self.assertEqual(
            "SOURCE_LEXEME_ONLY_NO_PRODUCTION_GRADE_COERCION",
            JIELAN_1581_DIGNITY_NORMALIZATION_STATUS,
        )
        self.assertFalse(payload["production_grade_mapping_present"])
        self.assertEqual(
            "PRESENT_REQUIRES_CELL_LEVEL_CROSS_COLLATION",
            payload["parallel_source_status"],
        )

    def test_known_source_conflicts_and_unstated_cell_are_not_silently_resolved(self) -> None:
        payload = jielan_1581_dignity_lexeme_registry_payload()
        conflicts = {
            (row["display_name"], row["branch"], tuple(row["source_lexemes"]))
            for row in payload["cells"]
            if row["source_conflict"]
        }
        self.assertEqual(
            {
                ("紫微", "午", ("庙", "平")),
                ("巨门", "丑", ("局", "陷")),
            },
            conflicts,
        )
        unstated = {
            (row["display_name"], row["branch"])
            for row in payload["cells"]
            if row["attestation_status"] == "UNSTATED_IN_CH70_STAR_VERSE"
        }
        self.assertEqual({("天机", "巳")}, unstated)

    def test_source_explicit_glosses_are_kept_as_lexical_relations(self) -> None:
        payload = jielan_1581_dignity_lexeme_registry_payload()
        glosses = payload["explicit_glosses"]
        self.assertEqual("庙", glosses["旺"]["gloss_target"])
        self.assertEqual("闲", glosses["平"]["gloss_target"])
        self.assertEqual("旺", glosses["得地"]["gloss_target"])
        self.assertEqual("陷", glosses["嗔"]["gloss_target"])
        self.assertEqual("得地", glosses["局"]["gloss_target"])
        self.assertEqual("庙", glosses["庭"]["gloss_target"])

    def test_resolver_can_return_one_entity_without_inventing_missing_values(self) -> None:
        payload = resolve_jielan_1581_dignity_lexeme_candidate(display_name="天机")
        self.assertEqual(12, len(payload["rows"]))
        si = next(row for row in payload["rows"] if row["branch"] == "巳")
        self.assertEqual((), si["source_lexemes"])
        self.assertEqual("UNSTATED_IN_CH70_STAR_VERSE", si["attestation_status"])
        self.assertFalse(si["source_conflict"])
        self.assertFalse(payload["production_grade_mapping_present"])
        self.assertEqual(64, len(payload["registry_hash"]))
        self.assertEqual(64, len(payload["runtime_hash"]))

    def test_resolver_rejects_unknown_entity(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported Jielan dignity entity"):
            resolve_jielan_1581_dignity_lexeme_candidate(display_name="UNKNOWN")


if __name__ == "__main__":
    unittest.main()
