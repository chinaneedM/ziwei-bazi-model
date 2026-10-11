import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class KyotoAccessAndAlternatives12SR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = read("docs/research/MING-DATONG-YEHUOBIAN-12SR-KYOTO-ACCESS-AND-ALTERNATIVE-COPY-TRIAGE-R1.json")
        cls.s = read("docs/PROJECT-CURRENT-STATE-R1.json")
        cls.sp = read("docs/research/MING-DATONG-YEHUOBIAN-12SP-FOUR-COPY-LEAF-ACQUISITION-PACKET-R1.json")

    def test_firstparty_institution_contact_not_copy_approval(self):
        k = self.r["kyoto"]
        self.assertEqual(k["official_contact"], "letlib@mail2.adm.kyoto-u.ac.jp")
        self.assertEqual(len(k["official_directories"]), 2)
        p = k["official_visitor_policy"]
        self.assertTrue(p["external_users_prior_contact"])
        self.assertTrue(p["unaffiliated_visitors_holding_inquiry_form_before_visit"])
        self.assertTrue(p["rare_book_reading_advance_application_and_department_permission"])
        self.assertTrue(p["chinese_stitched_or_fragile_books_may_not_be_eligible_for_normal_photocopy"])
        self.assertEqual(p["remote_image_delivery_for_these_items"], "UNCONFIRMED")
        self.assertEqual(p["right_to_republish_target_images"], "NOT_GRANTED")
        self.assertEqual({(v["ncid"], v["item"]) for v in k["target_physical_items"]},
                         {("BB18578034", "188987L"), ("BB05477307", "200023037620")})

    def test_alternative_copy_is_not_a_glyph_or_absence_claim(self):
        r = self.r
        alternatives = {x["ncid"]: x for x in r["alternative_holdings"]}
        self.assertEqual(set(alternatives), {"BC08398372", "BB10385966"})
        self.assertEqual(alternatives["BC08398372"]["copy_item"], "6411758714")
        self.assertEqual(alternatives["BB10385966"]["copy_item"], "0181427762")
        self.assertTrue(all(x["target_page_observed"] is False for x in alternatives.values()))
        for key in ("newly_observed_physical_target_leaf_count", "independent_target_glyph_votes_added"):
            self.assertEqual(r["access_not_glyph_guard"][key], 0)
        self.assertTrue(r["access_not_glyph_guard"]["no_article_absence_inferred"])
        self.assertTrue(r["access_not_glyph_guard"]["bibliographic_distinct_holdings_not_independent_textual_stemma"])
        self.assertTrue(all(v == 0 for v in r["external_actions"].values()))
        self.assertTrue(all(v == 0 for v in self.sp["external_actions"].values()))

    def test_supplement_only_preserves_closed_product_and_forward_state(self):
        h = self.s["historical_audit"]
        i = self.r["invariants"]
        self.assertEqual(self.r["parent_batch"], "12QE_OPEN")
        self.assertEqual(i["formal_batch_delta"], 0)
        self.assertEqual(i["source_registry_delta"], 0)
        self.assertEqual(i["graph_delta"], 0)
        self.assertTrue(h["latest_batch_doc"].endswith("-QD.md"))
        self.assertGreaterEqual(len(h["completed_batches"]), 487)
        self.assertEqual(h["row_count"], 222)
        self.assertEqual(h["audited_row_count"], 222)
        self.assertEqual(h["external_source_registry_total_unique_count"], 658)
        self.assertEqual(self.s["invariants"]["deterministic_fusion_chart_product_r1"], "CLOSED")
        self.assertEqual(self.s["invariants"]["algorithm_reopen_count"], 0)
        self.assertTrue(any(x.startswith("12SR KYOTO") for x in h["current_focus"]))

if __name__ == "__main__":
    unittest.main()
