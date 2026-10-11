"""12QW regression: no source-preview promotion to target-glyph proof."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
entry=ROOT/"scripts/verify_yehuobian_nlc_f6_f10_preview_12qw.py"
spec=importlib.util.spec_from_file_location("tianwen_12qw",entry)
model=importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)

class Test12QWF6F10Scope(unittest.TestCase):
    def test_combined_review_coverage_and_unchanged_native_backlog(self):
        s=model.verify()
        self.assertEqual(s["source_pages"],1030)
        self.assertEqual(s["body_pages"],1027)
        self.assertEqual(s["native_screened_source_pages"],29)
        self.assertEqual(s["montage_only_source_pages"],570)
        self.assertEqual(s["not_target_screened_source_pages"],431)
        self.assertEqual(s["body_not_even_firstpass_screened"],429)
        self.assertEqual(s["native_body_review_backlog"],999)
        self.assertEqual(s["body_full_text_collation_backlog"],1027)
        self.assertFalse(s["global_target_absence_proven"])

    def test_f10_existing_native_scoped_pages_preserved(self):
        s=model.verify()
        self.assertEqual(s["per_fascicle"]["10"]["native_screens"],9)
        self.assertEqual(s["per_fascicle"]["10"]["fourup_only"],136)
        self.assertEqual(s["per_fascicle"]["10"]["native_body_backlog"],136)
        self.assertEqual(s["per_fascicle"]["6"]["fourup_only"],116)
        self.assertEqual(s["per_fascicle"]["6"]["native_body_backlog"],116)

    def test_original_volume_19_and_20_mixed_page_boundaries(self):
        q=model.load(model.RECORD)
        f10=q["source_archives"][1]
        self.assertEqual([x["pdf_page"] for x in f10["original_juan_openings"]],[1,81,137])
        self.assertEqual([x["previous_volume_right_leaf"] for x in f10["original_juan_openings"]],[False,True,True])
        self.assertEqual(f10["last_colophon_page"],145)
        self.assertEqual(q["methods"]["new_native_target_text_reviews"],0)
        self.assertEqual(q["methods"]["digest_mismatches"],0)

    def test_source_hash_and_false_absence_mutations_fail_closed(self):
        original=model.load(model.RECORD)
        variants=[
            lambda r:r["source_archives"][0].__setitem__("artifact_metadata_sha256","0"*64),
            lambda r:r["source_archives"][1].__setitem__("page_sha_chain","0"*64),
            lambda r:r["source_archives"][1].__setitem__("contact_count_sha_verified",18),
            lambda r:r["source_archives"][1]["original_juan_openings"][1].__setitem__("previous_volume_right_leaf",False),
            lambda r:r["methods"].__setitem__("whole_work_target_absence_proven",True),
            lambda r:r["methods"].__setitem__("new_native_target_text_reviews",252),
            lambda r:r["grade_rules"].__setitem__("f10_preview_pages","1..145"),
            lambda r:r["queue_reconciliation"]["expected_after"].__setitem__("native_body_review_backlog",747),
        ]
        for i,mutate in enumerate(variants):
            with self.subTest(mutation=i),tempfile.TemporaryDirectory() as d:
                data=copy.deepcopy(original)
                mutate(data)
                f=Path(d)/"variant.json"
                f.write_text(json.dumps(data,ensure_ascii=False),encoding="utf-8")
                with self.assertRaises(ValueError):
                    model.verify(f)

if __name__=="__main__":
    unittest.main()
