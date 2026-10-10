"""12QR: 20 SHA-bound visual screens must not silently become text absence proof."""
from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "scripts/yehuobian_nlc_target_review_overlay_12qr.py"
spec = importlib.util.spec_from_file_location("nlc_review_12qr", P)
qr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qr)


class Test12QRDirectTwentyImageScreens(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report, cls.pages = qr.reconcile()
        cls.by_page = {(p["fascicle"], p["pdf_page"]): p for p in cls.pages}

    def test_source_bound_replay_and_remaining_queue(self):
        self.assertEqual(self.report["source_pages"], 1030)
        self.assertEqual(self.report["prior_bounded_target_checked_source_pages"], 9)
        self.assertEqual(self.report["new_direct_screened_source_pages"], 20)
        self.assertEqual(self.report["body_candidate_remaining_unreviewed"], 999)
        self.assertEqual(self.report["old20_target_original_folio"], "UNLOCATED")
        self.assertFalse(self.report["whole_manuscript_absence_proven"])
        self.assertFalse(self.report["all_manuscript_pages_line_by_line_collated"])

    def test_first_twenty_original_volume12_screens_and_next_page(self):
        for i in range(1,21):
            row = self.by_page[7,i]
            self.assertEqual(row["original_volume_candidates"], [12])
            self.assertEqual(row["target_review_status"],
                             "12QR_DIRECT_VISUAL_SCREEN_NO_POSITIVE_ATTESTATION")
            self.assertFalse(row["entire_manuscript_target_absence_proven"])
            self.assertFalse(row["needs_target_image_review"])
            self.assertEqual(len(row["page_jpeg_sha256_if_known"]), 64)
            self.assertEqual(row["physical_witness_increment"],0)
        self.assertTrue(self.by_page[7,21]["needs_target_image_review"])
        self.assertEqual(self.by_page[7,68]["original_volume_candidates"], [13,14])
        self.assertEqual(self.by_page[10,137]["target_review_status"],
                         "PRIOR_NINE_PAGE_BOUNDED_CHECK")

    def test_hash_bound_acquisition_provenance(self):
        ledger = json.loads(qr.QR_LEDGER.read_text(encoding="utf-8"))
        src = ledger["source"]
        self.assertEqual(src["artifact_status_sha256"],
                         "fe20b671dee5f97b69933dc27655c3780861954eb32d05a14a945687c526004d")
        self.assertEqual(src["artifact_zip_sha256"],
                         "31eb8bf2d27d6a562a676da3eba034e74db173282f5004e5c234547167052f14")
        self.assertEqual(src["artifact_members_verified"]["hash_mismatches"], 0)
        self.assertFalse(src["source_pdf_rehashed_this_batch"])
        self.assertEqual(ledger["review"]["page_1_heading_context"], "萬曆三十七年己酉卷十二")
        self.assertFalse(ledger["review"]["any_page_proven_target_absent"])
        self.assertEqual(len(ledger["review"]["screened_pdf_pages"]), 20)

    def test_mutations_of_source_identity_and_scope_fail_closed(self):
        original = json.loads(qr.QR_LEDGER.read_text(encoding="utf-8"))
        def altered(setter):
            with tempfile.TemporaryDirectory() as d:
                p = Path(d)/"altered.json"
                new = copy.deepcopy(original)
                setter(new)
                p.write_text(json.dumps(new,ensure_ascii=False),encoding="utf-8")
                with self.assertRaises(ValueError):
                    qr.reconcile(p)
        altered(lambda j:j["source"].__setitem__("source_pdf_sha256","0"*64))
        altered(lambda j:j["review"].__setitem__("whole_manuscript_absence_proven",True))
        altered(lambda j:j["review"]["screened_pdf_pages"][0].__setitem__("proof_target_absent_on_page",True))
        altered(lambda j:j["review"]["screened_pdf_pages"][0].__setitem__("pdf_page",21))
        altered(lambda j:j["review"]["screened_pdf_pages"][0].__setitem__("source_derived_page_jpeg_sha256","0"*64))

    def test_no_false_negative_even_on_previous_review_pages(self):
        for p in self.pages:
            self.assertFalse(p["entire_manuscript_target_absence_proven"])
        self.assertEqual(self.by_page[10,145]["page_scope"],
                         "END_COLOPHON_CONTEXT_NOT_CERTIFIED_VOLUME_TEXT")
        self.assertFalse(self.by_page[10,145]["body_search_eligible"])


if __name__ == "__main__":
    unittest.main()
