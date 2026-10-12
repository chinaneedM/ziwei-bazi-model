import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD="docs/research/MING-DATONG-YEHUOBIAN-12SX-XUXIU1174-DIRECT-FOUR-LOCUS-FACSIMILE-COLLATION-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
PARENT="docs/research/MING-DATONG-YEHUOBIAN-12SW-XUXIU1174-SOURCE-OBJECT-VERIFICATION-AND-VOL20-BOUND-R1.json"

class Xuxiu1174DirectFourLoci12SX(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads((ROOT/RECORD).read_text(encoding="utf-8"))
        cls.s=json.loads((ROOT/STATE).read_text(encoding="utf-8"))
        cls.p=json.loads((ROOT/PARENT).read_text(encoding="utf-8"))

    def test_exact_file_identity_and_bound_original_page(self):
        src=self.d["source_object"]
        self.assertEqual(src["verified_full_pdf_sha256"],self.p["exact_source_proof"]["source_sha256"])
        self.assertEqual(src["file_bytes"],68649578)
        self.assertEqual(src["source_page_count"],810)
        self.assertFalse(src["original_1827_unrepaired_impression_verified"])
        t=self.d["target_passage"]
        self.assertEqual(t["title_seen_directly_pdf_page_1based"],506)
        self.assertEqual(t["continuation_pdf_page_1based"],507)
        self.assertEqual(t["printed_page_of_primary_loci"]+3,t["primary_locus_pdf_page_1based"])
        self.assertEqual(len(t["page_506_rendered_jpeg_sha256"]),64)
        self.assertEqual(len(t["page_507_rendered_jpeg_sha256"]),64)

    def test_mixed_four_loci_are_edition_scoped(self):
        a=self.d["directly_read_four_loci"]
        self.assertEqual(len(a),4)
        self.assertEqual([p["reading"] for p in a],["宮禁","官漏","辰初二刻","戌初二刻"])
        self.assertEqual(len({p["id"] for p in a}),4)
        self.assertTrue(all(p["pdf_page_1based"]==506 for p in a))
        self.assertTrue(all(p["reading"] in p["phrase"] for p in a))
        c=self.d["registered_prior_witness_comparison"]
        self.assertEqual(c["xuxiu_1174_facsimile"],[p["reading"] for p in a])
        self.assertEqual(c["shanghai_GJ2312912_scanned"],["宮禁","宮漏","辰初一刻","戌初一刻"])
        self.assertEqual(c["ctext_received_text"],["官禁","官漏","辰初二刻","戌初二刻"])
        self.assertFalse(c["ctext_and_xuxiu_identical_across_four_loci"])
        self.assertFalse(c["shanghai_and_xuxiu_identical_across_four_loci"])

    def test_no_false_physical_vote_or_chart_reopen(self):
        x=self.d["adjudication"]
        self.assertTrue(x["facsimile_target_passage_verified"])
        self.assertEqual(x["facsimile_four_loci_read_count"],4)
        self.assertEqual(x["verified_new_independent_1827_unrepaired_physical_copy_votes"],0)
        self.assertEqual(x["source_manifest_new_source_count"],0)
        self.assertFalse(x["algorithm_reopen_authorized"])
        self.assertFalse(x["machine_candidate_collapse_authorized"])
        self.assertEqual(self.d["transmission_impact"]["edges_supported"],[])
        s=self.s["historical_audit"]
        self.assertTrue(any(z.startswith("12SX XUXIU1174") for z in s["current_focus"]))
        self.assertEqual(s["external_source_registry_total_unique_count"],660)
        self.assertEqual(s["audited_row_count"],222)
        self.assertGreaterEqual(len(s["completed_batches"]),487)
        self.assertEqual(self.s["invariants"]["algorithm_reopen_count"],0)
        self.assertEqual(self.s["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")

if __name__=="__main__":
    unittest.main()
