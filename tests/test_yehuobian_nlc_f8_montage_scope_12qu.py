"""12QU eight-up source-image preview remains a weaker grade than native review."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/"scripts/verify_yehuobian_nlc_f8_montage_scope_12qu.py"
spec=importlib.util.spec_from_file_location("tw12qu",path)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class Test12QUF8SourceScope(unittest.TestCase):
    def test_queue_counts_preserve_native_backlog(self):
        result=module.verify()
        self.assertEqual(result["source_pages"],1030)
        self.assertEqual(result["body_pages"],1027)
        self.assertEqual(result["montage_only_source_pages"],177)
        self.assertEqual(result["not_target_screened_source_pages"],824)
        self.assertEqual(result["body_not_even_firstpass_screened"],822)
        self.assertEqual(result["native_body_review_backlog"],999)
        self.assertEqual(result["body_full_text_collation_backlog"],1027)
        self.assertFalse(result["global_target_absence_proven"])

    def test_f8_87_pages_remain_native_target_pending(self):
        record=module.load(module.DOC)
        self.assertEqual(record["visual_review"]["native_pages_opened_for_navigation_only"],[1,87])
        self.assertEqual(record["visual_review"]["new_native_target_passage_reviews"],0)
        self.assertEqual(module.verify()["per_fascicle"]["8"]["native_body_backlog"],87)
        self.assertEqual(module.verify()["per_fascicle"]["8"]["fourup_only"],87)

    def test_source_digests_and_existing_original_opening(self):
        record=module.load(module.DOC)
        qo=module.load(module.QO)
        label=next(row for row in qo["original_juan_openings"] if row["volume"]==15)
        self.assertEqual(record["original_page_navigation"]["p1_source_sha256"],label["page_jpeg_sha256"])
        self.assertEqual(record["source"]["image_integrity"]["hash_mismatches"],0)
        self.assertFalse(record["source"]["source_pdf_rehashed_this_batch"])

    def test_mutations_reject_unearned_native_or_absence_claim(self):
        base=module.load(module.DOC)
        probes=[
            lambda x:x["source"].__setitem__("page_sha_sequence_sha256","0"*64),
            lambda x:x["source"].__setitem__("artifact_status_json_sha256","0"*64),
            lambda x:x["source"]["image_integrity"].__setitem__("hash_mismatches",1),
            lambda x:x["visual_review"].__setitem__("native_pages_opened_for_navigation_only",list(range(1,88))),
            lambda x:x["visual_review"].__setitem__("does_not_prove_work_absence",False),
            lambda x:x["queue_reconciliation"]["expected_new_summary"].__setitem__("native_body_review_backlog",912),
            lambda x:x["original_page_navigation"].__setitem__("p87_source_sha256","0"*64),
        ]
        for i,mutate in enumerate(probes):
            with self.subTest(mutation=i),tempfile.TemporaryDirectory() as d:
                candidate=copy.deepcopy(base)
                mutate(candidate)
                p=Path(d)/"mutation.json"
                p.write_text(json.dumps(candidate,ensure_ascii=False),encoding="utf-8")
                with self.assertRaises(ValueError):
                    module.verify(p)

if __name__=="__main__":
    unittest.main()
