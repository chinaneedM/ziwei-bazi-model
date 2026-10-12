"""12TQ: the 1959 scan is a date-identity investigation, not an ancient glyph."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/MING-DATONG-YEHUOBIAN-12TQ-NLC511-1959-PHYSICAL-IMPRINT-IMAGE-ATLAS-GATE-R1.json"
W=".github/workflows/probe-yehuobian-nlc511-1959-imprint-12tq.yml"
H="docs/PROJECT-CURRENT-STATE-R1.json"
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
class NLC511Modern1959SourceGate12TQ(unittest.TestCase):
    def test_gate_identity_and_non_promotion(self):
        x=read(E)
        src=x["source"]
        self.assertEqual(x["existing_registered_source_id"],"EXT-WIKIMEDIA-NLC511-1959-ZHONGHUA-YEHUOBIAN-3V-12QE")
        self.assertEqual(src["commons_file_sha1"],"6b1b516ccbc6bc9423fb9f31d6d1de2ab8ae0f9f")
        self.assertEqual(src["commons_file_size_bytes"],13756274)
        self.assertEqual(src["commons_pdf_page_count"],366)
        self.assertFalse(src["actual_colophon_leaf_read"])
        self.assertEqual(x["adjudication"]["new_registry_source_count"],0)
        self.assertEqual(x["adjudication"]["algorithm_reopens"],0)
        self.assertFalse(x["workflow"]["source_probe_success_unobserved_until_exact_head_job_runs"] is False)
        self.assertEqual(x["transmission_impact"]["edges_supported"],[])
        content=(ROOT/W).read_text(encoding="utf-8")
        self.assertIn("6b1b516ccbc6bc9423fb9f31d6d1de2ab8ae0f9f",content)
        self.assertIn("13756274",content)
        self.assertIn("pages=list(range(1,33))+list(range(350,367))",content)
        self.assertIn("ocr_used",content)
        self.assertIn("ancient_glyph_votes_added",content)
        self.assertIn("SOURCE_FETCH_BOUNDARY",content)
        self.assertIn("FULL_SOURCE_IDENTITY_OR_PAGE_COUNT_MISMATCH",content)
    def test_handoff_preserves_product_and_counts(self):
        h=read(H);a=h["historical_audit"]
        self.assertEqual(a["row_count"],222)
        self.assertEqual(a["audited_row_count"],222)
        self.assertEqual(a["repaired_provenance_metadata_defect_count"],45)
        self.assertGreaterEqual(a["external_source_registry_total_unique_count"],678)
        self.assertGreaterEqual(len(a["completed_batches"]),487)
        self.assertTrue(any(f.startswith("12TQ NLC511") for f in a["current_focus"]))
        self.assertEqual(h["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
        self.assertEqual(h["invariants"]["algorithm_reopen_count"],0)
        self.assertEqual(h["invariants"]["candidate_collapse_count"],0)
if __name__=="__main__":unittest.main()
