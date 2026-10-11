"""12RD bounded native source images do not establish target absence or complete text."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts/verify_yehuobian_nlc_f1_p89_119_native_12rd.py"
SPEC=importlib.util.spec_from_file_location("tianwen12rd_gate",SCRIPT)
GATE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)

class Test12RD(unittest.TestCase):
    def mutate(self,callback):
        data=copy.deepcopy(GATE.load(GATE.RECORD))
        callback(data)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"edited.json"
            path.write_text(json.dumps(data,ensure_ascii=False),encoding="utf-8")
            with self.assertRaises(ValueError):
                GATE.verify(record_path=path)
    def test_first_fascicle_body_native_screened_not_full_text(self):
        result=GATE.verify()
        self.assertEqual(result["fascicle1_native_body_target_screened"],117)
        self.assertEqual(result["fascicle1_native_target_screen_pending"],0)
        self.assertEqual(result["whole_source_native_body_review_backlog"],882)
        self.assertEqual(result["whole_source_full_text_body_backlog"],1027)
        self.assertFalse(result["whole_manuscript_absence_proven"])
    def test_member_sha_mutation_fails(self):
        self.mutate(lambda x:x["review"]["page_jpeg_sha256_in_pdf_order"].__setitem__(5,"0"*64))
    def test_sequence_chain_mutation_fails(self):
        self.mutate(lambda x:x["review"].__setitem__("sha256_concatenated_page_hashes","0"*64))
    def test_frontmatter_is_not_target_body(self):
        self.mutate(lambda x:x["review"].__setitem__("frontmatter_prelim_pages_not_target_screened",[]))
    def test_full_text_not_promoted(self):
        self.mutate(lambda x:x["review"].__setitem__("complete_text_transcription_performed",True))
    def test_false_target_absence_not_promoted(self):
        self.mutate(lambda x:x["review"].__setitem__("any_page_target_absence_proven",True))
    def test_one_holding_not_multiplied(self):
        self.mutate(lambda x:x["queue"].__setitem__("new_independent_physical_copy_count",1))
    def test_original_pdf_not_claimed_rehashed(self):
        self.mutate(lambda x:x["source"].__setitem__("source_pdf_binary_rehashed",True))
    def test_pending_queue_cannot_silently_close(self):
        self.mutate(lambda x:x["queue"].__setitem__("new_native_body_target_backlog",0))
    def test_first_fascicle_complete_does_not_close_whole_work(self):
        self.mutate(lambda x:x["queue"].__setitem__("whole_manuscript_full_text_body_collation_backlog",0))

if __name__=="__main__":
    unittest.main()
