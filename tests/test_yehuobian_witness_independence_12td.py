"""Source-bound guard: same digital readings are not independent old-print votes."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))

class WitnessIndependence12TD(unittest.TestCase):
    def test_four_loci_follow_forward_correction(self):
        record=load("docs/research/MING-DATONG-YEHUOBIAN-12TB-PRINT-IMAGE-MISREAD-CORRECTION-R1.json")
        gate=load("docs/research/MING-DATONG-YEHUOBIAN-12TD-WITNESS-INDEPENDENCE-GATE-R1.json")
        actual={x["id"]:x["loci"] for x in record["corrected_direct_image_loci"]}
        expected={x["id"]:x["loci"] for x in gate["direct_image_four_locus_controls"]}
        self.assertEqual(actual,expected)
        self.assertEqual(actual["CADAL02096915"],actual["XUXIU1174_2002"])
        self.assertEqual({x[-1] for x in actual.values()},{"戌初一刻","戌初三刻"})
        self.assertEqual(record["adjudication"]["earlier_12TA_image_three_distinct_summer_values"],"RETRACTED")
        self.assertEqual([x["corrected"] for x in record["corrections"][:2]],["是時禁中官漏循用新製","戌初三刻"])

    def test_two_digital_derivatives_are_not_two_physical_votes(self):
        r=load("docs/research/MING-DATONG-YEHUOBIAN-12TB-PRINT-IMAGE-MISREAD-CORRECTION-R1.json")
        g=load("docs/research/MING-DATONG-YEHUOBIAN-12TD-WITNESS-INDEPENDENCE-GATE-R1.json")
        reg=r["digital_registration"]
        self.assertGreater(reg["sift_ratio_good_matches"],1000)
        self.assertGreater(reg["homography_inliers"],1000)
        for field in ("source_image_identical_physical_copy_confirmed","source_image_duplicate_underlying_photo_confirmed","underlying_printing_plate_date_confirmed"):
            self.assertIs(reg[field],False)
        self.assertIs(r["adjudication"]["cadal_xuxiu_as_independent_original_print_votes"],False)
        self.assertEqual(r["adjudication"]["authoritative_independent_1827_unrepaired_page_votes"],0)
        self.assertEqual(g["source_authority_gates"]["confirmed_1869_original_target_leaf_votes"],0)
        self.assertTrue(all(x["independent_orig_1827_1869_vote"] is False for x in g["direct_image_four_locus_controls"]))
        self.assertEqual(r["adjudication"]["modern_CText_summer_reading"],"戌初二刻")
        self.assertTrue(r["adjudication"]["no_new_graph_edge"])
        self.assertTrue(r["adjudication"]["no_algorithm_reopen"])

    def test_source_digest_and_state_still_fail_closed(self):
        r=load("docs/research/MING-DATONG-YEHUOBIAN-12TB-PRINT-IMAGE-MISREAD-CORRECTION-R1.json")
        script=(ROOT/"scripts/replay-yehuobian-image-registration-12tc.py").read_text(encoding="utf-8")
        for name in ("cadal","xuxiu"):
            self.assertIn(r["original_images"][name]["jpeg_sha256"],script)
        s=load("docs/PROJECT-CURRENT-STATE-R1.json")
        self.assertTrue(any(x.startswith("12TD FORWARD-ONLY IMAGE-WITNESS") for x in s["historical_audit"]["current_focus"]))
        self.assertEqual(s["invariants"]["algorithm_reopen_count"],0)
        self.assertEqual(s["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")

if __name__=="__main__":
    unittest.main()
