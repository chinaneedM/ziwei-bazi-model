"""Regression: source contact images are not a manuscript-wide literal negative search."""
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12QM-NLC411999003250-FASC4-5-SCOPED-MANUAL-IMAGE-TRIAGE-R1.json").read_text(encoding="utf-8"))
BASE = json.loads((ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12QL-NLC411999003250-TEN-FASCICLE-BINARY-CAPTURE-RECONCILIATION-R1.json").read_text(encoding="utf-8"))
STATE = json.loads((ROOT / "docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf-8"))

class Test12QMSourceImageScope(unittest.TestCase):
    def test_source_hashes_artifact_ids_and_coverage(self):
        self.assertEqual([r["digital_fascicle"] for r in DATA["checked_artifacts"]], [4, 5])
        self.assertEqual([len(r["contact_sheets_visually_triaged"]) for r in DATA["checked_artifacts"]], [7, 8])
        self.assertEqual([len(r["original_pages_opened"]) for r in DATA["checked_artifacts"]], [4, 3])
        for x in DATA["checked_artifacts"]:
            b = BASE["sources"][x["digital_fascicle"]-1]
            self.assertEqual(x["source_pdf_sha256_from_12ql"], b["source_pdf_sha256"])
            self.assertEqual(x["artifact_id"], b["artifact_id"])
            self.assertEqual(x["workflow_run"], b["workflow_run"])
            self.assertEqual(x["source_pdf_pages"], b["source_pdf_pages"])
            self.assertTrue(x["all_images_and_contact_sha256_verified_against_downloaded_artifact_status_json"])
            covered = []
            for s in x["contact_sheets_visually_triaged"]:
                self.assertEqual(s["level"], "OVERVIEW_ONLY_NOT_TEXT_GLYPH_REVIEW")
                self.assertEqual(len(s["sha256"]), 64)
                covered.extend(range(s["first_page"], min(s["first_page"]+8, b["source_pdf_pages"]+1)))
            self.assertEqual(covered, list(range(1, b["source_pdf_pages"]+1)))
            for pg in x["original_pages_opened"]:
                self.assertEqual(pg["level"], "INDIVIDUAL_DIRECT_IMAGE_VIEW")
                self.assertTrue(1 <= pg["page"] <= b["source_pdf_pages"])
                self.assertEqual(len(pg["jpeg_sha256"]), 64)
            self.assertEqual(x["total_line_by_line_pages_fully_collated"], 0)
            self.assertFalse(x["original_target_heading_folio_found"])

    def test_no_false_negative_or_algorithm_reopen(self):
        scope = DATA["scope"]
        self.assertEqual((scope["contact_sheet_overview_pages"], scope["contact_sheets_visually_triaged"], scope["individual_source_pages_opened"]), (119,15,7))
        self.assertEqual(scope["full_text_pages_collated"], 0)
        for k in ("whole_119_page_absence_claim","whole_1030_page_absence_claim","target_heading_or_passage_located","print_copy_or_edition_identity_newly_established"):
            self.assertFalse(scope[k])
        self.assertFalse(DATA["ocr_performed"])
        self.assertFalse(DATA["automated_target_detection_performed"])
        self.assertEqual(DATA["distinct_antique_copy_count_increment"], 0)
        self.assertEqual(DATA["invariants"]["algorithm_reopens"], 0)
        self.assertEqual(STATE["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
        self.assertEqual(STATE["historical_audit"]["row_count"],222)
        self.assertEqual(STATE["historical_audit"]["audited_row_count"],222)

if __name__ == "__main__":
    unittest.main()
