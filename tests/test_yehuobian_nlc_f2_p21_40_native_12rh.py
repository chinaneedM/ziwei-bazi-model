"""12RH regression: original-size source scope, exact JPEG hashes, zero negative proofs."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("tw12rh", ROOT / "scripts/verify_yehuobian_nlc_f2_p21_40_native_12rh.py")
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


class TestNlcOld20Fascicle2Native12RH(unittest.TestCase):
    def mutate(self, fn):
        rec = copy.deepcopy(GATE.load(GATE.RECORD))
        fn(rec)
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / "mutated.json"
            dest.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(ValueError):
                GATE.verify(record_path=dest)

    def test_exact_source_page_window(self):
        a = GATE.verify()
        self.assertEqual(a["fascicle2_native_pages"], 40)
        self.assertEqual(a["fascicle2_remaining_native_target_pages"], 32)
        self.assertEqual(a["all_native_bounded_pages"], 186)
        self.assertEqual(a["all_preview_only_remaining"], 842)
        self.assertEqual(a["full_text_body_collation_remaining"], 1027)
        self.assertFalse(a["new_target_glyph_or_text_absence_proof"])

    def test_original_jpeg_hash_mutation(self):
        self.mutate(lambda x: x["review"]["original_jpeg_sha256_ordered"].__setitem__(11, "0" * 64))

    def test_ordered_chain_mutation(self):
        self.mutate(lambda x: x["review"].__setitem__("ordered_hash_chain_sha256", "0" * 64))

    def test_crossbatch_chain_mutation(self):
        self.mutate(lambda x: x["review"].__setitem__("fascicle2_p1_40_combined_chain_sha256", "0" * 64))

    def test_cannot_misbind_different_fascicle(self):
        self.mutate(lambda x: x["source"].__setitem__("digital_fascicle", 3))

    def test_pdf_binary_not_rehashed(self):
        self.mutate(lambda x: x["source"].__setitem__("source_pdf_binary_rehashed", True))

    def test_visual_screen_not_complete_transcription(self):
        self.mutate(lambda x: x["review"].__setitem__("complete_text_transcription_performed", True))

    def test_no_whole_volume_absence_proof(self):
        self.mutate(lambda x: x["review"].__setitem__("whole_volume_absence_proven", True))

    def test_no_manuscript_absence_proof(self):
        self.mutate(lambda x: x["review"].__setitem__("whole_manuscript_absence_proven", True))

    def test_source_count_cannot_inflate(self):
        self.mutate(lambda x: x["queue"].__setitem__("independent_physical_witness_increment", 1))

    def test_unreviewed_f2_pages_cannot_disappear(self):
        self.mutate(lambda x: x["queue"].__setitem__("fascicle2_native_body_pending", 0))


if __name__ == "__main__":
    unittest.main()
