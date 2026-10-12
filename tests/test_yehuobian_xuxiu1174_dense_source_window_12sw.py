import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD="docs/research/MING-DATONG-YEHUOBIAN-12SW-XUXIU1174-SOURCE-OBJECT-VERIFICATION-AND-VOL20-BOUND-R1.json"
WORKFLOW=".github/workflows/probe-xuxiu1174-volume20-dense-leaves-12sw.yml"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"

class Xuxiu1174DenseOriginalSource12SW(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads((ROOT/RECORD).read_text(encoding="utf-8"))
        cls.s=json.loads((ROOT/STATE).read_text(encoding="utf-8"))
        cls.w=(ROOT/WORKFLOW).read_text(encoding="utf-8")

    def test_verified_source_identity_and_sample_attestations(self):
        x=self.d["exact_source_proof"]
        self.assertEqual(x["run_status"],"COMPLETED_SUCCESS")
        self.assertEqual(x["source_pdf_bytes"],68649578)
        self.assertEqual(x["source_pdf_pages"],810)
        self.assertEqual(x["jpeg_sample_pages"],65)
        self.assertEqual(x["contact_sheets"],9)
        self.assertEqual(len(x["source_sha256"]),64)
        pages={p["pdf_page_1based"]:p for p in self.d["visually_reviewed_samples"]}
        self.assertEqual(set(pages),{118,490,502,514})
        self.assertIn("卷二〇",pages[502]["reading"])
        self.assertEqual(self.d["invariants"]["source_glyph_votes_added"],0)

    def test_dense_gate_and_fail_closed_artifact(self):
        self.assertIn("range(486,519)",self.w)
        self.assertIn('SOURCE_IDENTITY_OR_PAGE_COUNT_MISMATCH_FAIL_CLOSED',self.w)
        self.assertIn(self.d["exact_source_proof"]["source_sha256"],self.w)
        self.assertIn("pdftoppm",self.w)
        self.assertIn("upload-artifact@v4",self.w)
        self.assertNotIn("tesseract",self.w.lower())
        self.assertTrue(any("no target glyph" in q.lower() for q in self.d["limits"]))

    def test_state_forward_only_no_automatic_algorithm_reopen(self):
        a=self.s["historical_audit"]
        self.assertTrue(any(t.startswith("12SW XUXIU1174") for t in a["current_focus"]))
        self.assertGreaterEqual(len(a["completed_batches"]),487)
        self.assertGreaterEqual(a["external_source_registry_total_unique_count"],660)
        self.assertEqual(a["external_source_registry_total_unique_count"],json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json").read_text(encoding="utf-8"))["combined_source_count"])
        self.assertEqual(self.s["invariants"]["algorithm_reopen_count"],0)
        self.assertEqual(self.s["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")

if __name__=="__main__":
    unittest.main()
