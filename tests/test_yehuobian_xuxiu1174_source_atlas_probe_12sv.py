import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
RECORD="docs/research/MING-DATONG-YEHUOBIAN-12SV-XUXIU1174-BONDED-SOURCE-ATLAS-TRIGGER-R1.json"
WORKFLOW=".github/workflows/probe-xuxiu1174-original-pages-12sv.yml"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"

class Xuxiu1174BoundedSourceGate12SV(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rec=json.loads((ROOT/RECORD).read_text(encoding="utf8"))
        cls.state=json.loads((ROOT/STATE).read_text(encoding="utf8"))
        cls.workflow=(ROOT/WORKFLOW).read_text(encoding="utf8")

    def test_exact_known_identity_fails_closed(self):
        obj=self.rec["target_object"]
        self.assertEqual(obj["expected_bytes"],68649578)
        self.assertEqual(obj["expected_sha1"],"fc6a98b070c11372c557e22bb05cdc9859541715")
        self.assertEqual(obj["expected_pdf_pages"],810)
        self.assertEqual(obj["part2_first_pdf_page_1based"],obj["part2_first_printed_page"]+3)
        self.assertEqual(obj["filename"],"續修四庫全書第1174冊.pdf")
        self.assertIn('SOURCE_IDENTITY_MISMATCH_FAIL_CLOSED',self.workflow)
        self.assertIn('SOURCE_PAGINATION_MISMATCH_FAIL_CLOSED',self.workflow)
        self.assertIn('pdfinfo',self.workflow)
        self.assertIn('sha256',self.workflow)

    def test_public_gated_route_and_no_ocr(self):
        self.assertIn('Special:Redirect/file',self.workflow)
        self.assertIn('name="續修四庫全書第1174冊.pdf"',self.workflow)
        self.assertIn('pdftoppm',self.workflow)
        self.assertIn('upload-artifact@v4',self.workflow)
        self.assertIn('if: always()',self.workflow)
        self.assertNotIn('tesseract',self.workflow.lower())
        self.assertFalse(self.rec["current_observation"]["original_pdf_binary_obtained_by_this_commit"])
        self.assertEqual(self.rec["current_observation"]["original_four_locus_votes"],0)
        self.assertTrue(self.rec["method"]["image_processing"].endswith("NO OCR"))

    def test_handoff_and_formal_batch_invariants(self):
        a=self.state["historical_audit"]
        self.assertTrue(any(s.startswith("12SV XUXIU1174") for s in a["current_focus"]))
        self.assertEqual(a["row_count"],222)
        self.assertEqual(a["audited_row_count"],222)
        self.assertEqual(a["external_source_registry_total_unique_count"],660)
        self.assertGreaterEqual(len(a["completed_batches"]),487)
        self.assertEqual(self.state["invariants"]["algorithm_reopen_count"],0)
        self.assertEqual(self.state["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
        self.assertEqual(self.rec["invariants"]["formal_batches"],487)
        self.assertEqual(self.rec["invariants"]["new_source_or_glyph_vote"],0)

if __name__=="__main__":
    unittest.main()
