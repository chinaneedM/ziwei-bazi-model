"""12QZ first 20 independently viewed original JPEGs and proof-scope firewall."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/"scripts/verify_yehuobian_nlc_f1_first20_native_12qz.py"
spec=importlib.util.spec_from_file_location("tw_12qz_native",path)
qz=importlib.util.module_from_spec(spec)
spec.loader.exec_module(qz)

class Test12QZNativeTwenty(unittest.TestCase):
    def test_twenty_native_screened_reduce_only_native_target_backlog(self):
        result=qz.verify()
        self.assertEqual(result["native_screened_source_pages"],49)
        self.assertEqual(result["montage_only_source_pages"],979)
        self.assertEqual(result["native_body_review_backlog"],979)
        self.assertEqual(result["body_full_text_collation_backlog"],1027)
        self.assertEqual(result["body_not_even_firstpass_screened"],0)
        self.assertEqual(result["not_target_screened_source_pages"],2)
        self.assertFalse(result["global_target_absence_proven"])

    def test_source_pinned_sha_sequence_and_original_volume1_opening(self):
        r=qz.load(qz.RECORD)
        self.assertEqual(r["review"]["page_image_sha256_in_pdf_order"],qz.PIN)
        self.assertEqual(r["source"]["source_original_jpeg_members_rechecked"],20)
        self.assertEqual(r["source"]["image_hash_mismatches"],0)
        self.assertEqual(r["review"]["page_3_original_volume_opening_direct_image_label"],"萬曆二十六年戊戌卷一")
        self.assertEqual(qz.verify()["per_fascicle"]["1"]["native_screens"],20)

    def test_bounded_visual_scan_is_not_negative_proof(self):
        r=qz.load(qz.RECORD)
        self.assertFalse(r["review"]["full_text_transcribed"])
        self.assertFalse(r["review"]["proof_target_absent_on_any_page"])
        self.assertFalse(r["review"]["proof_target_absent_in_manuscript"])
        self.assertEqual(r["review"]["target_original_glyph_positive_attestations"],0)
        self.assertEqual(qz.verify()["per_fascicle"]["1"]["native_body_backlog"],97)

    def test_fail_closed_mutations(self):
        original=qz.load(qz.RECORD)
        mutations=[
            lambda x:x["source"].__setitem__("artifact_status_json_sha256","0"*64),
            lambda x:x["review"]["page_image_sha256_in_pdf_order"].__setitem__(6,"0"*64),
            lambda x:x["review"].__setitem__("page_image_sha256_concatenation_sha256","0"*64),
            lambda x:x["review"].__setitem__("proof_target_absent_on_any_page",True),
            lambda x:x["review"].__setitem__("proof_target_absent_in_manuscript",True),
            lambda x:x["review"].__setitem__("full_text_transcribed",True),
            lambda x:x["queue_reconciliation"].__setitem__("new_native_body_target_review_backlog",0),
            lambda x:x["review"].__setitem__("original_pdf_pages_individually_viewed",19),
        ]
        for i,mutate in enumerate(mutations):
            with self.subTest(mutation=i),tempfile.TemporaryDirectory() as td:
                sample=copy.deepcopy(original)
                mutate(sample)
                f=Path(td)/"modified.json"
                f.write_text(json.dumps(sample,ensure_ascii=False),encoding="utf-8")
                with self.assertRaises(ValueError):
                    qz.verify(f)

if __name__=="__main__":
    unittest.main()
