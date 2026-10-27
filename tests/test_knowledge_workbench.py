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

    def test_phase2_cards_cover_all_batches_and_sources(self):
        seed = json.loads(
            (ROOT / "knowledge-workbench/school-method-cards.json").read_text(encoding="utf-8")
        )
        phase2 = json.loads(
            (ROOT / "knowledge-workbench/phase2-executable-cards.json").read_text(encoding="utf-8")
        )
        manifest = json.loads(
            (ROOT / "sources/canonical-manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(phase2["card_count"], len(phase2["cards"]))
        self.assertEqual(len(seed["cards"]) + len(phase2["cards"]), 23)
        self.assertEqual(
            {card["batch"] for card in phase2["cards"]},
            {
                "A_ZIWEI_STATIC",
                "B_ZIWEI_DYNAMIC_SCHOOLS",
                "C_BAZI_SYSTEM",
                "D_FUSION_REALITY_GOVERNANCE",
            },
        )
        source_paths = {row["source_id"]: ROOT / row["path"] for row in manifest["sources"]}
        covered_sources = set()
        for card in phase2["cards"]:
            self.assertEqual(card["status"], "CURATED_UNVALIDATED")
            self.assertTrue(card["proof_ceiling"])
            self.assertTrue(card["school_attribution"])
            self.assertTrue(card["conflicts"])
            for anchor in card["source_anchors"]:
                source_id = anchor["source_id"]
                covered_sources.add(source_id)
                line_count = len(source_paths[source_id].read_text(encoding="utf-8").splitlines())
                self.assertGreaterEqual(anchor["line_start"], 1)
                self.assertLessEqual(anchor["line_start"], anchor["line_end"])
                self.assertLessEqual(anchor["line_end"], line_count)
            for illustration in card["illustrations"]:
                self.assertEqual(illustration["role"], "METHOD_DEMONSTRATION_ONLY")
                self.assertIn(illustration["source_id"], source_paths)
        self.assertEqual(covered_sources, set(source_paths))


if __name__ == "__main__":
    unittest.main()
