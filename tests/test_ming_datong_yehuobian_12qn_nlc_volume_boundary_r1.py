"""12QN original volume headings are bounded source pages, never exclusive PDF-page ownership."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = json.loads((ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12QN-NLC411999003250-VOL11-17-BOUNDARY-FOLIOS-R1.json").read_text(encoding="utf-8"))
Q = json.loads((ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12QL-NLC411999003250-TEN-FASCICLE-BINARY-CAPTURE-RECONCILIATION-R1.json").read_text(encoding="utf-8"))
S = json.loads((ROOT / "docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf-8"))

class TestNLC12QNBoundaries(unittest.TestCase):
    def test_seven_volume_headings_and_three_new_locations(self):
        rows = E["original_volume_heading_checks"]
        self.assertEqual([x["original_volume"] for x in rows], list(range(11, 18)))
        self.assertEqual([(x["fascicle"], x["pdf_page"]) for x in rows],
                         [(6, 1), (7, 1), (7, 48), (7, 68), (8, 1), (9, 1), (9, 84)])
        self.assertEqual([x["original_volume"] for x in rows if not x["already_documented_in_12ql"]], [13, 14, 17])
        self.assertEqual([x["original_volume"] for x in rows if x["shared_spread_with_prior_volume"]], [14, 17])
        for x in rows:
            self.assertEqual(len(x["jpeg_sha256"]), 64)
            self.assertTrue(x["exact_heading"].endswith("卷" + {11:"十一",12:"十二",13:"十三",14:"十四",15:"十五",16:"十六",17:"十七"}[x["original_volume"]]))
            self.assertEqual(x["source_glyph_level"], "DIRECT_MANUAL_IMAGE_VIEW")
            self.assertEqual(x["previous_volume_content_on_right"], x["shared_spread_with_prior_volume"])
            self.assertLessEqual(x["pdf_page"], Q["sources"][x["fascicle"]-1]["source_pdf_pages"])
    def test_artifact_capture_and_invariants(self):
        src = E["source_capture_checks"]
        self.assertEqual([x["source_page_images_verified_against_original_status_json"] for x in src], [116,110,87,141])
        self.assertEqual([x["contact_sheets_verified_against_original_status_json"] for x in src], [15,14,11,18])
        self.assertEqual(sum(x["source_page_images_verified_against_original_status_json"] for x in src), 454)
        self.assertEqual(sum(x["contact_sheets_verified_against_original_status_json"] for x in src), 58)
        for x in src:
            q = Q["sources"][x["fascicle"]-1]
            for k in ("source_pdf_pages", "source_pdf_sha256", "artifact_id", "workflow_run"):
                self.assertEqual(x[k], q[k])
            self.assertEqual(x["derived_page_hash_mismatches"], 0)
            self.assertEqual(x["derived_contact_hash_mismatches"], 0)
        for k in ("full_454_page_transcription", "full_old20_target_search_completed", "original_1447_louke_target_folio_found"):
            self.assertFalse(E["counting"][k])
        self.assertTrue(E["counting"]["zero_ocr"])
        self.assertEqual(E["new_independent_physical_copy_count"], 0)
        self.assertEqual(E["invariants"]["algorithm_reopens"], 0)
        self.assertEqual(E["invariants"]["product_r1"], "CLOSED")
        self.assertEqual(S["invariants"]["deterministic_fusion_chart_product_r1"], "CLOSED")
        self.assertEqual(S["historical_audit"]["row_count"], 222)
        self.assertEqual(S["historical_audit"]["audited_row_count"], 222)
        self.assertEqual([x["pdf_page"] for x in E["adjacent_and_terminal_page_checks"] if x["fascicle"]==7 and "IMMEDIATELY_PRECEDES" in x["scope"]],[47,67])

if __name__ == "__main__":
    unittest.main()
