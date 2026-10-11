"""Fail-closed regression for old20 12RA original page p23-42 native screening."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / "scripts/verify_yehuobian_nlc_f1_p23_42_native_12ra.py"
spec = importlib.util.spec_from_file_location("tw12ra_native", S)
tw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tw)

class Test12RANativeSourceReview(unittest.TestCase):
    def _mutated(self, updater):
        record = copy.deepcopy(tw.load(tw.RECORD))
        updater(record)
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "ra.json"
            f.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(ValueError):
                tw.verify(record_path=f)

    def test_twenty_native_upgrades_and_no_fulltext_inference(self):
        result = tw.verify()
        self.assertEqual(result["native_screened_source_pages"], 69)
        self.assertEqual(result["native_body_review_backlog"], 959)
        self.assertEqual(result["preview_only_source_pages"], 959)
        self.assertEqual(result["full_text_collation_backlog"], 1027)
        self.assertFalse(result["whole_manuscript_negative_proven"])

    def test_original_jpeg_chain_tampering_fails_closed(self):
        self._mutated(lambda r: r["review"]["page_image_sha256_in_pdf_order"].__setitem__(0, "0" * 64))

    def test_mixed_original_juan_leaf_boundary_cannot_collapse(self):
        self._mutated(lambda r: r["review"]["cross_volume_leaf_ownership"].__setitem__("right_leaf_original_juan", 2))

    def test_visual_screen_cannot_turn_into_absence_proof(self):
        self._mutated(lambda r: r["review"].__setitem__("proof_target_absent_on_any_page", True))

    def test_source_copy_count_cannot_inflate(self):
        self._mutated(lambda r: r["queue_reconciliation"].__setitem__("independent_physical_copy_increment", 1))

if __name__ == "__main__":
    unittest.main()
