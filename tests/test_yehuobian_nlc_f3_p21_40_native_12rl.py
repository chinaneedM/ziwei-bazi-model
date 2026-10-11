"""12RL: regression rejects false source identity, mismatched JPEG hashes and absence claims."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tw12rl", ROOT/"scripts/verify_yehuobian_nlc_f3_p21_40_native_12rl.py")
GATE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)

class TestNlcFascicle3Native12RL(unittest.TestCase):
    def modify(self, func):
        data=copy.deepcopy(GATE.read(GATE.RECORD))
        func(data)
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/"altered.json"
            target.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(ValueError):
                GATE.verify(record_path=target)
    def test_true_20_pages_and_full_backlog(self):
        r=GATE.verify()
        self.assertEqual((r["f3_native_bounded_pages"],r["f3_remaining"]),(40,81))
        self.assertEqual((r["whole_native_bounded_pages"],r["whole_preview_only_pages"]),(258,770))
        self.assertEqual(r["whole_fulltext_body_pending"],1027)
        self.assertFalse(r["new_target_glyph_attested"])
        self.assertFalse(r["target_absence_proven"])
    def test_one_original_jpeg_hash_mutated(self):
        self.modify(lambda r:r["review"]["original_jpeg_sha256_in_pdf_order"].__setitem__(9,"0"*64))
    def test_wrong_sha_chain(self):
        self.modify(lambda r:r["review"].__setitem__("ordered_page_sha256_concatenation_chain","0"*64))
    def test_wrong_archive_id(self):
        self.modify(lambda r:r["source"].__setitem__("artifact_id",0))
    def test_pdf_not_rehashed(self):
        self.modify(lambda r:r["source"].__setitem__("source_pdf_binary_rehashed_in_12rl",True))
    def test_false_original_juan_change(self):
        self.modify(lambda r:r["review"].__setitem__("original_juan6_7_boundary_directly_identified_in_window",True))
    def test_fake_page_absence_proof(self):
        self.modify(lambda r:r["review"].__setitem__("any_scoped_page_target_absence_proven",True))
    def test_fake_fulltext_transcription(self):
        self.modify(lambda r:r["review"].__setitem__("full_text_page_by_page_collation_performed",True))
    def test_fake_new_source_witness(self):
        self.modify(lambda r:r["queue"].__setitem__("independent_copy_increment",1))
    def test_false_fulltext_complete(self):
        self.modify(lambda r:r["queue"].__setitem__("whole_holding_full_text_collation_pending",0))
    def test_missing_preview_backlog(self):
        self.modify(lambda r:r["queue"].__setitem__("new_preview_only_body_pages",0))

if __name__=="__main__":
    unittest.main()
