"""12QS: preserve the distinction between a four-up image preview and source collation."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/verify_yehuobian_nlc_f7_montage_scope_12qs.py"
spec = importlib.util.spec_from_file_location("nlc_montage_12qs", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class Test12QSScopedMontageReview(unittest.TestCase):
    def test_controlled_90_page_scope(self):
        summary = mod.verify_scope()
        self.assertEqual(summary["f7_fourup_source_pages_this_batch"], 90)
        self.assertEqual(summary["f7_cross_volume_page"], 68)
        self.assertEqual(summary["firstpass_source_pages_including_prior_scans"], 119)

    def test_no_upgrade_of_999_full_resolution_pages(self):
        summary = mod.verify_scope()
        self.assertEqual(summary["still_requires_individual_native_pages"], 999)
        self.assertFalse(summary["absence_proven"])
        self.assertEqual(summary["new_independent_physical_witnesses"], 0)

    def test_12qr_inherited_and_12qoverified_hashes(self):
        q = mod.load(mod.QS)
        old = mod.load(mod.QR)
        self.assertEqual(q["source"]["artifact_zip_sha256"], old["source"]["artifact_zip_sha256"])
        self.assertEqual(q["source"]["artifact_status_json_sha256"],
                         old["source"]["artifact_status_sha256"])
        openings = {x["volume"]: x for x in mod.load(mod.QO)["original_juan_openings"]}
        self.assertEqual(q["review_scope"]["original_full_image_anchor_sha256"]["48"],
                         openings[13]["page_jpeg_sha256"])
        self.assertEqual(q["review_scope"]["original_full_image_anchor_sha256"]["68"],
                         openings[14]["page_jpeg_sha256"])
        self.assertTrue(openings[14]["right_leaf_has_previous_volume"])

    def test_source_digest_and_firstpass_coverage_not_global_negative(self):
        q = mod.load(mod.QS)
        self.assertRegex(q["review_scope"]["page_sequence_hash_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(sum(q["leaf_aware_navigation"][key] for key in (
            "f7_pages_21_to_47_volume12",
            "f7_pages_48_to_67_volume13",
            "f7_page_68_mixed_original_volume13_right_volume14_left",
            "f7_pages_69_to_110_volume14")), 90)
        self.assertTrue(q["review_scope"]["does_not_prove_absence_in_whole_work"])
        self.assertTrue(q["review_scope"]["does_not_prove_absence_of_target_on_screened_pages"])

    def test_mutated_source_and_visual_scope_fail_closed(self):
        original = mod.load(mod.QS)
        def probe(change):
            with tempfile.TemporaryDirectory() as tmp:
                copied = copy.deepcopy(original)
                change(copied)
                path = Path(tmp) / "modified.json"
                path.write_text(json.dumps(copied, ensure_ascii=False), encoding="utf-8")
                with self.assertRaises(ValueError):
                    mod.verify_scope(path)
        probe(lambda x: x["source"].__setitem__("source_pdf_sha256", "0" * 64))
        probe(lambda x: x["review_scope"].__setitem__("ocr_used", True))
        probe(lambda x: x["review_scope"].__setitem__("does_not_prove_absence_in_whole_work", False))
        probe(lambda x: x["review_scope"].__setitem__("individually_reopened_full_resolution_source_pages",[48,110]))
        probe(lambda x: x["queue_reconciliation"].__setitem__("still_requires_individual_native_source_page_target_review",909))
        probe(lambda x: x["review_scope"]["original_full_image_anchor_sha256"].__setitem__("68", "0"*64))


if __name__ == "__main__":
    unittest.main()
