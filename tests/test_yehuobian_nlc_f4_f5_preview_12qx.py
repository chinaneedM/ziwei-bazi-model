"""12QX original f4/f5 mixed-leaf and SHA-verified preview grade regressions."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
filename=ROOT/"scripts/verify_yehuobian_nlc_f4_f5_preview_12qx.py"
spec=importlib.util.spec_from_file_location("tianwen_12qx_test",filename)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class Test12QXF4F5Preview(unittest.TestCase):
    def test_counts_preserve_native_target_backlog(self):
        a=m.verify()
        self.assertEqual(a["source_pages"],1030)
        self.assertEqual(a["body_pages"],1027)
        self.assertEqual(a["montage_only_source_pages"],689)
        self.assertEqual(a["not_target_screened_source_pages"],312)
        self.assertEqual(a["body_not_even_firstpass_screened"],310)
        self.assertEqual(a["native_body_review_backlog"],999)
        self.assertEqual(a["body_full_text_collation_backlog"],1027)
        self.assertFalse(a["global_target_absence_proven"])

    def test_original_1606_f4_mixed_spread_preserved(self):
        a=m.load(m.RECORD)
        f4=a["source_archives"][0]
        self.assertEqual(f4["old_original_juan"],[8,9])
        self.assertEqual(f4["volume_openings"][1]["page"],35)
        self.assertTrue(f4["volume_openings"][1]["prior_volume_on_right_leaf"])
        self.assertEqual(m.verify()["per_fascicle"]["4"]["fourup_only"],56)

    def test_one_holding_no_target_fulltext_proof(self):
        a=m.load(m.RECORD)
        self.assertEqual(a["physical_holding"],"NLC411999003250_ONE_HOLDING")
        self.assertEqual(a["visual_method"]["source_jpegs_rehashed"],119)
        self.assertEqual(a["visual_method"]["contact_jpegs_rehashed"],15)
        self.assertEqual(a["visual_method"]["new_native_target_text_screens"],0)
        self.assertFalse(a["visual_method"]["negative_on_entire_work_proven"])
        self.assertEqual(m.verify()["per_fascicle"]["5"]["native_body_backlog"],63)

    def test_mutations_fail_closed(self):
        base=m.load(m.RECORD)
        changes=[
            lambda x:x["source_archives"][0].__setitem__("status_json_sha256","0"*64),
            lambda x:x["source_archives"][1].__setitem__("source_page_sha_chain","0"*64),
            lambda x:x["source_archives"][0].__setitem__("member_hash_mismatches",1),
            lambda x:x["source_archives"][0]["volume_openings"][1].__setitem__("prior_volume_on_right_leaf",False),
            lambda x:x["visual_method"].__setitem__("new_native_target_text_screens",119),
            lambda x:x["visual_method"].__setitem__("negative_on_entire_work_proven",True),
            lambda x:x["queue_reconciliation"].__setitem__("native_body_review_backlog",880),
            lambda x:x["source_archives"][1].__setitem__("original_images_opened_for_navigation_only",[1,2,63]),
        ]
        for i,fn in enumerate(changes):
            with self.subTest(i=i),tempfile.TemporaryDirectory() as d:
                v=copy.deepcopy(base)
                fn(v)
                loc=Path(d)/"altered.json"
                loc.write_text(json.dumps(v,ensure_ascii=False),encoding="utf-8")
                with self.assertRaises(ValueError):
                    m.verify(loc)

if __name__=="__main__":
    unittest.main()
