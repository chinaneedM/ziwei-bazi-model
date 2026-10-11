"""12QV: f9 141-page preview cannot be promoted to native original-target proof."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
target=ROOT/"scripts/verify_yehuobian_nlc_f9_montage_scope_12qv.py"
spec=importlib.util.spec_from_file_location("nlc_f9_12qv",target)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class Test12QVF9PreviewBoundaries(unittest.TestCase):
    def test_f9_previews_do_not_reduce_native_review(self):
        s=mod.verify()
        self.assertEqual(s["source_pages"],1030)
        self.assertEqual(s["body_pages"],1027)
        self.assertEqual(s["native_screened_source_pages"],29)
        self.assertEqual(s["montage_only_source_pages"],318)
        self.assertEqual(s["body_not_even_firstpass_screened"],681)
        self.assertEqual(s["native_body_review_backlog"],999)
        self.assertEqual(s["body_full_text_collation_backlog"],1027)
        self.assertFalse(s["global_target_absence_proven"])

    def test_f9_original_volume_mixed_right_left_leaf(self):
        item=mod.load(mod.QV)
        self.assertEqual(item["navigation"]["p84_right_leaf_original_volume"],16)
        self.assertEqual(item["navigation"]["p84_left_leaf_original_volume"],17)
        self.assertEqual(item["manual_review"]["native_images_opened_for_navigation_only"],[1,84,141])
        self.assertEqual(mod.verify()["per_fascicle"]["9"]["fourup_only"],141)
        self.assertEqual(mod.verify()["per_fascicle"]["9"]["native_body_backlog"],141)

    def test_source_hash_identity_and_absence_boundaries(self):
        item=mod.load(mod.QV)
        self.assertEqual(item["source"]["source_jpeg_count"],141)
        self.assertEqual(item["source"]["contact_sheet_count"],18)
        self.assertEqual(item["source"]["hash_mismatches"],0)
        self.assertFalse(item["source"]["pdf_binary_rehashed_this_round"])
        self.assertEqual(item["manual_review"]["positive_target_glyph_attestations"],0)
        self.assertFalse(item["manual_review"]["absence_in_entire_work_proven"])

    def test_mutation_guards(self):
        base=mod.load(mod.QV)
        mutators=[
            lambda x:x["source"].__setitem__("page_sha_chain","0"*64),
            lambda x:x["source"].__setitem__("status_json_sha256","0"*64),
            lambda x:x["source"].__setitem__("hash_mismatches",1),
            lambda x:x["manual_review"].__setitem__("absence_in_entire_work_proven",True),
            lambda x:x["manual_review"].__setitem__("native_images_opened_for_navigation_only",[1,141]),
            lambda x:x["navigation"].__setitem__("p84_right_leaf_original_volume",17),
            lambda x:x["queue_after"].__setitem__("native_body_target_review_backlog",858),
        ]
        for i,fn in enumerate(mutators):
            with self.subTest(i=i),tempfile.TemporaryDirectory() as d:
                entry=copy.deepcopy(base)
                fn(entry)
                p=Path(d)/"mutated.json"
                p.write_text(json.dumps(entry,ensure_ascii=False),encoding="utf-8")
                with self.assertRaises(ValueError):
                    mod.verify(p)

if __name__=="__main__":
    unittest.main()
