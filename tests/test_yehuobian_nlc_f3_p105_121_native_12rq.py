"""12RQ source pin/window continuity and non-absence regressions."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tw12rq", ROOT/"scripts/verify_yehuobian_nlc_f3_p105_121_native_12rq.py")
GATE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)

class TestF3Native105To121_12RQ(unittest.TestCase):
    def tamper(self, mutate):
        d=copy.deepcopy(GATE.read(GATE.DATA))
        mutate(d)
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"tampered.json"
            path.write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8")
            with self.assertRaises(ValueError):
                GATE.verify(record_path=path)
    def test_firstpass_not_fulltext(self):
        r=GATE.verify()
        self.assertEqual(r["fascicle3_source_page_bounded_firstpass"],"121/121")
        self.assertEqual((r["whole_holding_native_bounded"],r["whole_holding_preview_only"]),(339,689))
        self.assertEqual(r["fulltext_body_pages_still_pending"],1027)
        self.assertFalse(r["old20_target_presence_or_absence_proven"])
    def test_mutated_source_page_sha(self):
        self.tamper(lambda d:d["review"]["original_jpeg_sha256_in_pdf_page_order"].__setitem__(10,"0"*64))
    def test_false_fulltext_complete(self):
        self.tamper(lambda d:d["review"].__setitem__("complete_linewise_collation_performed",True))
    def test_false_whole_book_absence(self):
        self.tamper(lambda d:d["review"].__setitem__("whole_old20_work_target_absence_proven",True))
    def test_false_fascicle_absence(self):
        self.tamper(lambda d:d["review"].__setitem__("fascicle3_target_absence_proven",True))
    def test_false_old_juan_assignment(self):
        self.tamper(lambda d:d["review"].__setitem__("current_p105_121_exclusively_assigned_to_original_juan7",True))
    def test_false_1827_equivalence(self):
        self.tamper(lambda d:d["review"].__setitem__("print1827_30juan_original_leaf_equivalence_proven",True))
    def test_queue_inflation(self):
        self.tamper(lambda d:d["queue"].__setitem__("new_whole_native_bounded_source_pages",340))
    def test_pending_fulltext_cannot_be_closed(self):
        self.tamper(lambda d:d["queue"].__setitem__("whole_holding_fulltext_body_collation_pending",0))
    def test_source_pdf_not_rehashed(self):
        self.tamper(lambda d:d["source"].__setitem__("source_pdf_binary_rehashed_in_12rq",True))
    def test_lineage_cannot_be_inflated(self):
        self.tamper(lambda d:d["queue"].__setitem__("new_direct_stemmatic_copy_edges",1))

if __name__=="__main__":
    unittest.main()
