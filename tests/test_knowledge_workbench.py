import json
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
WORKBENCH = ROOT / "knowledge-workbench"


def load(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


class KnowledgeWorkbenchTests(unittest.TestCase):
    def test_inventory_covers_locked_sources(self):
        inventory = load("knowledge-workbench/source-inventory.json")
        manifest = load("sources/canonical-manifest.json")
        self.assertEqual(inventory["authority"], "DERIVED_INDEX_ONLY")
        self.assertEqual(inventory["source_count"], 20)
        self.assertEqual(
            {row["source_id"]: row["sha256"] for row in inventory["sources"]},
            {row["source_id"]: row["sha256"] for row in manifest["sources"]},
        )

    def test_every_knowledge_card_validates_against_v2_schema(self):
        validator = Draft202012Validator(load("knowledge-workbench/knowledge-card.schema.json"))
        collections = [
            load("knowledge-workbench/school-method-cards.json"),
            load("knowledge-workbench/batch-a-static-cards.json"),
        ]
        cards = [card for collection in collections for card in collection["cards"]]
        self.assertGreaterEqual(len(cards), 22)
        for card in cards:
            validator.validate(card)

    def test_cards_are_traceable_unvalidated_and_examples_are_not_evidence(self):
        manifest = load("sources/canonical-manifest.json")
        source_paths = {row["source_id"]: ROOT / row["path"] for row in manifest["sources"]}
        collections = [
            load("knowledge-workbench/school-method-cards.json"),
            load("knowledge-workbench/batch-a-static-cards.json"),
        ]
        for collection in collections:
            for card in collection["cards"]:
                self.assertEqual(card["status"], "CURATED_UNVALIDATED")
                self.assertEqual(card["source_case_role"], "USAGE_DEMONSTRATION_ONLY_NOT_INDEPENDENT_VALIDATION")
                self.assertEqual(card["validation"]["distinct_case_count"], 0)
                self.assertEqual(card["validation"]["support_count"], 0)
                self.assertEqual(card["validation"]["counterexample_count"], 0)
                for anchor in card["source_anchors"]:
                    lines = source_paths[anchor["source_id"]].read_text(encoding="utf-8").splitlines()
                    self.assertLessEqual(anchor["line_start"], anchor["line_end"])
                    self.assertLessEqual(anchor["line_end"], len(lines))

    def test_batch_a_conflicts_and_coverage_map_every_card(self):
        cards = load("knowledge-workbench/batch-a-static-cards.json")["cards"]
        card_ids = {card["card_id"] for card in cards}
        conflict = load("knowledge-workbench/batch-a-conflict-matrix.json")
        coverage = load("knowledge-workbench/batch-a-case-coverage.json")
        self.assertEqual(len(cards), 16)
        self.assertEqual(len(conflict["rows"]), 10)
        self.assertTrue(all(set(row["card_ids"]).issubset(card_ids) for row in conflict["rows"]))
        self.assertFalse(coverage["answer_data_used"])
        self.assertEqual({row["card_id"] for row in coverage["mappings"]}, card_ids)
        for row in coverage["mappings"]:
            self.assertEqual(row["eligible_case_count"], len(row["eligible_case_ids"]))
            self.assertEqual(row["eligible_question_count"], len(row["eligible_question_refs"]))
            self.assertEqual(row["validation_status"], "COVERAGE_ONLY_NOT_OUTCOME_VALIDATION")

    def test_user_and_ai_hypotheses_have_equal_controls(self):
        registry = load("knowledge-workbench/research-hypotheses.json")
        policy = registry["origin_policy"]
        self.assertEqual(policy["allowed_origins"], ["USER_HYPOTHESIS", "AI_HYPOTHESIS"])
        self.assertTrue(policy["equal_validation_threshold"])
        self.assertFalse(policy["identity_grants_extra_weight"])
        self.assertFalse(policy["direct_promotion_to_truth_allowed"])
        self.assertEqual(
            set(registry["required_controls"]),
            {
                "BASELINE_RATE", "SELECTION_BIAS", "CONFIRMATION_BIAS",
                "REGION_ERA_DIFFERENCE", "ALTERNATIVE_EXPLANATION",
                "COUNTERFACTUAL", "NEGATIVE_EXAMPLE", "ANSWER_DISPUTE",
                "CONFIDENCE_CALIBRATION",
            },
        )

    def test_generated_batch_a_artifacts_are_current(self):
        result = subprocess.run(
            [sys.executable, "tools/build_knowledge_batch_a.py", "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)


if __name__ == "__main__":
    unittest.main()
