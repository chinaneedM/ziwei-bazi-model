import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class KnowledgeWorkbenchTests(unittest.TestCase):
    def test_inventory_covers_locked_sources(self):
        inventory = json.loads((ROOT / "knowledge-workbench/source-inventory.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "sources/canonical-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(inventory["authority"], "DERIVED_INDEX_ONLY")
        self.assertEqual(inventory["source_count"], 20)
        self.assertEqual(
            {row["source_id"]: row["sha256"] for row in inventory["sources"]},
            {row["source_id"]: row["sha256"] for row in manifest["sources"]},
        )

    def test_seed_cards_are_traceable_and_unvalidated(self):
        payload = json.loads((ROOT / "knowledge-workbench/school-method-cards.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(payload["cards"]), 7)
        source_ids = {f"S{number:02d}" for number in range(20)}
        for card in payload["cards"]:
            self.assertEqual(card["status"], "CURATED_UNVALIDATED")
            self.assertEqual(card["validation"]["distinct_case_count"], 0)
            self.assertTrue(card["source_anchors"])
            for anchor in card["source_anchors"]:
                self.assertIn(anchor["source_id"], source_ids)
                self.assertLessEqual(anchor["line_start"], anchor["line_end"])


if __name__ == "__main__":
    unittest.main()
