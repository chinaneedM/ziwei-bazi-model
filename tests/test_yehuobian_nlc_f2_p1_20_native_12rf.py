"""12RF tests: native visual target screening remains source-bound, non-negative."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tianwen12rf",ROOT/"scripts/verify_yehuobian_nlc_f2_p1_20_native_12rf.py")
GATE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)

class TestNlcFascicle2Native12RF(unittest.TestCase):
    def mutate(self,change):
        x=copy.deepcopy(GATE.load(GATE.RECORD))
        change(x)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"mutant.json"
            p.write_text(json.dumps(x,ensure_ascii=False),encoding="utf-8")
            with self.assertRaises(ValueError):
                GATE.verify(record_path=p)
    def test_real_source_scoped_20_pages(self):
        x=GATE.verify()
        self.assertEqual(x["fascicle2_native_target_screen_pages"],20)
        self.assertEqual(x["fascicle2_remaining_native_target_screen_pages"],52)
        self.assertEqual(x["whole_source_native_body_backlog"],862)
        self.assertEqual(x["whole_manuscript_full_text_body_collation_backlog"],1027)
        self.assertFalse(x["whole_text_absence_proven"])
    def test_page_hash_mutation(self):
        self.mutate(lambda x:x["review"]["source_page_sha256_in_pdf_order"].__setitem__(2,"0"*64))
    def test_page_sequence_digest_mutation(self):
        self.mutate(lambda x:x["review"].__setitem__("sha256_concatenated_page_hashes","0"*64))
    def test_f1_source_is_not_f2(self):
        self.mutate(lambda x:x["source"].__setitem__("digital_fascicle",1))
    def test_unverified_source_pdf_hash_claim(self):
        self.mutate(lambda x:x["source"].__setitem__("source_pdf_binary_rehashed",True))
    def test_misclaim_whole_absence(self):
        self.mutate(lambda x:x["review"].__setitem__("whole_manuscript_absence_proven",True))
    def test_misclaim_page_absence(self):
        self.mutate(lambda x:x["review"].__setitem__("page_target_absence_proven",True))
    def test_false_full_transcript(self):
        self.mutate(lambda x:x["review"].__setitem__("complete_text_transcription_performed",True))
    def test_queue_cannot_silently_complete(self):
        self.mutate(lambda x:x["queue"].__setitem__("whole_source_full_text_body_collation_backlog",0))
    def test_single_physical_holding(self):
        self.mutate(lambda x:x["queue"].__setitem__("new_independent_physical_copy_count",1))

if __name__=="__main__":
    unittest.main()
