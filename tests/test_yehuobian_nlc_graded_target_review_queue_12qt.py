"""12QT: stage-separated manual manuscript-target review."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
file=ROOT/"scripts/yehuobian_nlc_graded_target_review_queue_12qt.py"
spec=importlib.util.spec_from_file_location("tw12qt",file)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class Test12QTGradedQueue(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=mod.build_rows()
        cls.by={(r["fascicle"],r["pdf_page"]):r for r in cls.rows}

    def test_exact_replay_and_fail_closed_counts(self):
        m=mod.verify_snapshot()
        self.assertEqual(m["source_pages"],1030)
        self.assertEqual(m["body_pages"],1027)
        self.assertEqual(m["native_body_review_backlog"],999)
        self.assertEqual(m["body_not_even_firstpass_screened"],909)
        self.assertEqual(m["body_full_text_collation_backlog"],1027)
        self.assertFalse(m["global_target_absence_proven"])
        self.assertTrue(all(not r["target_absence_proven"] for r in self.rows))

    def test_f7_native_and_fourup_not_collapsed(self):
        for p in range(1,21):
            r=self.by[7,p]
            self.assertEqual(r["target_screen_grade"],"NATIVE_FULL_PAGE_VISUAL_TARGET_SCREEN")
            self.assertFalse(r["requires_native_target_screen"])
            self.assertEqual(len(r["target_image_sha256"]),64)
        for p in range(21,111):
            r=self.by[7,p]
            self.assertEqual(r["target_screen_grade"],"FOURUP_DOWNSAMPLED_TARGET_PREVIEW_ONLY")
            self.assertTrue(r["requires_native_target_screen"])
            self.assertEqual(r["full_resolution_opened_for_navigation_only"],p in (48,68,110))
        self.assertEqual(self.by[7,68]["cross_volume_leaf_ownership"],{"right":13,"left":14})

    def test_old20_endpoints_and_next_f8_queue(self):
        self.assertEqual(self.by[10,136]["target_screen_grade"],"NOT_TARGET_SCREENED")
        for p in range(137,146):
            self.assertEqual(self.by[10,p]["target_screen_grade"],"NATIVE_BOUNDED_HEADING_PASSAGE_SCREEN")
        self.assertFalse(self.by[10,145]["body_search_eligible"])
        self.assertEqual(self.by[10,137]["cross_volume_leaf_ownership"],{"right":19,"left":20})
        self.assertFalse(self.by[1,1]["body_search_eligible"])
        self.assertEqual(mod.summary(self.rows)["per_fascicle"]["8"]["native_body_backlog"],87)

    def test_mutated_qr_source_glyph_or_negative_claim_rejected(self):
        original=mod.load(mod.QR)
        changes=[
            lambda x:x["source"].__setitem__("source_pdf_sha256","0"*64),
            lambda x:x["review"]["screened_pdf_pages"][3].__setitem__("source_derived_page_jpeg_sha256","0"*64),
            lambda x:x["review"]["screened_pdf_pages"][3].__setitem__("proof_target_absent_on_page",True),
            lambda x:x["review"]["screened_pdf_pages"].pop()]
        for change in changes:
            with tempfile.TemporaryDirectory() as d:
                x=copy.deepcopy(original)
                change(x)
                p=Path(d)/"qr.json"
                p.write_text(json.dumps(x,ensure_ascii=False),encoding="utf-8")
                with self.assertRaises(ValueError):mod.build_rows(qr_path=p)

    def test_mutated_qs_preview_negative_claim_rejected(self):
        original=mod.load(mod.QS)
        for key in ("does_not_prove_absence_of_target_on_screened_pages",
                    "does_not_prove_absence_in_whole_work"):
            with tempfile.TemporaryDirectory() as d:
                x=copy.deepcopy(original)
                x["review_scope"][key]=False
                p=Path(d)/"qs.json"
                p.write_text(json.dumps(x,ensure_ascii=False),encoding="utf-8")
                with self.assertRaises(ValueError):mod.build_rows(qs_path=p)

if __name__=="__main__":unittest.main()
