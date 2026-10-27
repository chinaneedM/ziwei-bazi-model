"""12QY regression: all first-pass body previews != full-text original targets."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
script=ROOT/"scripts/verify_yehuobian_nlc_f1_f3_firstpass_12qy.py"
spec=importlib.util.spec_from_file_location("tw_12qy",script)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class Test12QYNativeGradeFirewall(unittest.TestCase):
    def test_every_1027_body_page_firstpass_is_not_a_text_negative(self):
        s=m.verify()
        self.assertEqual(s["source_pages"],1030)
        self.assertEqual(s["body_pages"],1027)
        self.assertEqual(s["native_screened_source_pages"],29)
        self.assertEqual(s["montage_only_source_pages"],999)
        self.assertEqual(s["not_target_screened_source_pages"],2)
        self.assertEqual(s["body_not_even_firstpass_screened"],0)
        self.assertEqual(s["native_body_review_backlog"],999)
        self.assertEqual(s["body_full_text_collation_backlog"],1027)
        self.assertFalse(s["global_target_absence_proven"])

    def test_f1_two_prelims_not_promoted_to_body_and_source_grade(self):
        r=m.load(m.RECORD)
        f1=r["sources"][0]
        self.assertEqual(f1["non_body_prelim_pages"],[1,2])
        self.assertEqual(f1["body_preview_pages"],117)
        self.assertEqual(f1["verified_contacts"],15)
        self.assertEqual(m.verify()["per_fascicle"]["1"]["fourup_only"],117)
        self.assertEqual(m.verify()["per_fascicle"]["1"]["native_body_backlog"],117)

    def test_original_f1_f3_volume_boundary_or_year_caveats(self):
        r=m.load(m.RECORD)
        n=r["original_volume_navigation"]
        self.assertEqual([n["f1_old2_mixed_right_old1_left_old2"],n["f1_old3_start"],n["f1_old4_mixed_right_old3_left_old4"]],[35,62,88])
        self.assertEqual(n["f3_old7_mixed_right_old6_left_old7"],83)
        self.assertTrue(n["f3_old6_first_line_clipped"])
        self.assertTrue(n["unreadable_year_from_f3_p1_not_treated_as_physical_glyph"])
        self.assertEqual(m.verify()["per_fascicle"]["3"]["fourup_only"],121)

    def test_40_individual_contacts_member_hashes_no_extra_witness(self):
        r=m.load(m.RECORD)
        self.assertEqual(r["review_scope"]["member_hashes_rechecked_total"],352)
        self.assertEqual(r["review_scope"]["hash_mismatches"],0)
        self.assertTrue(r["review_scope"]["all_40_contacts_individually_visually_viewed"])
        self.assertEqual(r["queue_reconciliation"]["independent_physical_copy_increment"],0)

    def test_mutations_fail_closed(self):
        base=m.load(m.RECORD)
        mutators=[
            lambda r:r["sources"][0].__setitem__("status_sha256","0"*64),
            lambda r:r["sources"][2].__setitem__("page_sha_chain","0"*64),
            lambda r:r["sources"][1]["page_sha_pins"].__setitem__("1","0"*64),
            lambda r:r["sources"][0].__setitem__("non_body_prelim_pages",[]),
            lambda r:r["original_volume_navigation"].__setitem__("f3_old6_first_line_clipped",False),
            lambda r:r["review_scope"].__setitem__("negative_entire_work_proven",True),
            lambda r:r["review_scope"].__setitem__("target_native_reviews_added",310),
            lambda r:r["queue_reconciliation"].__setitem__("native_body_target_review_backlog",689),
        ]
        for i,mutate in enumerate(mutators):
            with self.subTest(i=i),tempfile.TemporaryDirectory() as d:
                v=copy.deepcopy(base)
                mutate(v)
                file=Path(d)/"mutated.json"
                file.write_text(json.dumps(v,ensure_ascii=False),encoding="utf-8")
                with self.assertRaises(ValueError):
                    m.verify(file)

if __name__=="__main__":
    unittest.main()
