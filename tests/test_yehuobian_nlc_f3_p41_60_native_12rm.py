"""12RM original F3 p41–60 source provenance and evidence scope negative tests."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tw12rm",ROOT/"scripts/verify_yehuobian_nlc_f3_p41_60_native_12rm.py")
GATE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)

class TestNlcF3P41To60Native12RM(unittest.TestCase):
    def mutate(self, action):
        data=copy.deepcopy(GATE.read(GATE.RECORD))
        action(data)
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"altered.json"
            path.write_text(json.dumps(data,ensure_ascii=False),encoding="utf-8")
            with self.assertRaises(ValueError):
                GATE.verify(record_path=path)
    def test_real_source_window_and_queue(self):
        r=GATE.verify()
        self.assertEqual((r["f3_native_bounded_reviewed"],r["f3_native_backlog"]),(60,61))
        self.assertEqual((r["all_native_source_pages"],r["preview_only_source_pages"]),(278,750))
        self.assertEqual(r["untranscribed_fulltext_body_pages"],1027)
        self.assertFalse(r["new_original_target_glyph_or_negative_proof"])
    def test_forged_jpeg(self):
        self.mutate(lambda x:x["review"]["original_image_sha256_ordered"].__setitem__(3,"0"*64))
    def test_wrong_hash_chain(self):
        self.mutate(lambda x:x["review"].__setitem__("window_20_page_hash_chain_sha256","0"*64))
    def test_wrong_source_manifest(self):
        self.mutate(lambda x:x["source"].__setitem__("artifact_id",1))
    def test_no_unproved_original_pdf_binary_sha(self):
        self.mutate(lambda x:x["source"].__setitem__("source_pdf_binary_rehashed",True))
    def test_no_juan_boundary_promotion(self):
        self.mutate(lambda x:x["review"].__setitem__("original_juan6_7_transition_directly_verified",True))
    def test_no_fulltext_promotion(self):
        self.mutate(lambda x:x["review"].__setitem__("full_text_transcribed",True))
    def test_no_any_page_negative_proof(self):
        self.mutate(lambda x:x["review"].__setitem__("proof_target_absent_on_any_page",True))
    def test_no_work_absence_proof(self):
        self.mutate(lambda x:x["review"].__setitem__("proof_target_absent_from_old20_work",True))
    def test_f3_pending_pages_not_zero(self):
        self.mutate(lambda x:x["queue"].__setitem__("fascicle3_remaining_native_target_pages",0))
    def test_sources_cannot_duplicate(self):
        self.mutate(lambda x:x["queue"].__setitem__("new_independent_physical_holding",1))

if __name__=="__main__":
    unittest.main()
