"""12UM: fail closed between Kyoto front matter and juan 20 original leaves."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12UM-KYOTO-DUAL-ITEM-ACQUISITION-GATE-R1.json"
QUEUE = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12UK-ORIGINAL-LEAF-INTAKE-QUEUE-R1.json"
STATE = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"

class KyotoScope12UM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(NOTE.read_text(encoding="utf-8"))
        cls.queue = json.loads(QUEUE.read_text(encoding="utf-8"))
        cls.state = json.loads(STATE.read_text(encoding="utf-8"))

    def test_source_scoped_kyoto_roles_are_separate(self):
        a, b = self.record["distinct_request_items"]
        self.assertEqual([a["role"], b["role"]], ["PREFACE_FRONTMATTER", "JUAN20_TARGET"])
        self.assertEqual(a["source_issued_call_number"], "B||VIb||9-1 188987")
        self.assertEqual(b["source_issued_call_number"], "B||VIb||9-1 188987L")
        self.assertNotEqual(a["source_issued_call_number"], b["source_issued_call_number"])
        self.assertIn("JUAN20_FOUR_LOCUS_GLYPH_VOTE", a["not_usable_for"])
        self.assertIn("KYOTO_FRONTMATTER_DIRECT_GLYPH_READ_WITHOUT_188987_IMAGE", b["not_usable_for"])
        self.assertEqual(b["holding_scope"], "卷19-20")

    def test_12uk_original_queue_remains_historical_six_candidate_snapshot(self):
        self.assertEqual(len(self.queue["candidates"]), 6)
        ids = {x["object_identifier"] for x in self.queue["candidates"]}
        self.assertIn("B||VIb||9-1 188987L", ids)
        self.assertNotIn("B||VIb||9-1 188987", ids)
        self.assertTrue(all(x["historical_vote"] is False for x in self.queue["candidates"]))

    def test_general_archive_access_does_not_pretend_item_iiif(self):
        self.assertTrue(all(x["item_specific_image_or_manifest"] == "NOT_IDENTIFIED_FROM_INSPECTED_PUBLIC_SOURCES"
                            for x in self.record["institutional_access"]
                            if "item_specific_image_or_manifest" in x))
        self.assertTrue(all(x.get("item_copy_eligibility", "").startswith("UNVERIFIED")
                            for x in self.record["institutional_access"]
                            if "item_copy_eligibility" in x))
        self.assertFalse(self.record["acquisition"]["negative_catalog_existence_asserted"])

    def test_no_unobtained_images_payments_or_historical_votes(self):
        a = self.record["acquisition"]
        self.assertTrue(all(a[x] is False for x in (
            "image_or_iiif_manifest_obtained", "item_specific_copy_permission",
            "outreach_sent", "paid_order_placed")))
        self.assertEqual(a["files_or_glyph_votes_acquired"], 0)
        d = self.record["decision"]
        self.assertFalse(d["algorithm_reopen_authorized"])
        self.assertFalse(d["graph_edge_promotion_authorized"])

    def test_regnal_mismatch_is_catalog_only(self):
        self.assertEqual(self.record["catalog"]["catalog_year_statement"], "康熙30年[1700]")
        self.assertEqual(self.record["catalog"]["exact_catalog_error_cause"], "UNRESOLVED")
        self.assertEqual(self.record["catalog"]["historical_impression_date_from_catalog"], "NOT_ATTESTED")

    def test_latest_project_status_persists(self):
        st = self.state
        h = st["historical_audit"]
        self.assertTrue(any(x.startswith("12UM ") for x in h["current_focus"]))
        self.assertEqual(h["external_source_registry_total_unique_count"], 687)
        self.assertEqual(len(h["completed_batches"]), 487)
        self.assertEqual(st["invariants"]["deterministic_fusion_chart_product_r1"], "CLOSED")
        self.assertEqual(st["invariants"]["algorithm_reopen_count"], 0)
        self.assertEqual(self.record["accounting"]["original_kyoto_folios"], 0)

if __name__ == "__main__":
    unittest.main()
