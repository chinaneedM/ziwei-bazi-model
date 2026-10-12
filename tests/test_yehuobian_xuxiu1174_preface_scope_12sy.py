import unittest,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/MING-DATONG-YEHUOBIAN-12SY-XUXIU1174-PREFACE-DATE-SCOPE-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
class PrefaceScope12SY(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/P).read_text(encoding="utf-8"))
  cls.s=json.loads((ROOT/S).read_text(encoding="utf-8"))
 def test_dates_distinct_from_impression(self):
  d=self.r
  self.assertEqual([x["year"] for x in d["image_read_prefatory_dates"]],[1606,1827,1869])
  self.assertEqual([x["kind"] for x in d["image_read_prefatory_dates"]],["AUTHORIAL_PREFACE_SIGNATURE","YAO_PREFACE_SIGNATURE","REVISED_PRINT_EDITORIAL_INSCRIPTION"])
  self.assertTrue(d["edition_date_firewall"]["dated_1827_preface_not_untouched_1827_leaf"])
  self.assertTrue(d["edition_date_firewall"]["dated_1869_reprint_statement_not_proof_target_leaf_recut"])
  self.assertEqual(d["edition_date_firewall"]["independent_1827_original_glyph_votes"],0)
 def test_exact_image_hashes(self):
  p={x["pdf_page"]:x["jpeg_sha256"] for x in self.r["pages"]}
  self.assertEqual(p[119],"f76a74aff8c11113ae9ec7f55d2db7286d114d82032291835751f294312312ae")
  self.assertEqual(p[506],"ece3094a332ca5f329a1c21f27f3e65a3412a2ad252452cae5a17fe50fd0ac11")
 def test_handoff_and_product_remain_stable(self):
  a=self.s["historical_audit"]
  self.assertTrue(any(x.startswith("12SY XUXIU1174") for x in a["current_focus"]))
  self.assertGreaterEqual(a["external_source_registry_total_unique_count"],660)
  self.assertEqual(a["external_source_registry_total_unique_count"],json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json").read_text(encoding="utf-8"))["combined_source_count"])
  self.assertEqual(len(a["completed_batches"]),487)
  self.assertEqual(self.s["invariants"]["algorithm_reopen_count"],0)
  self.assertEqual(self.s["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
if __name__=="__main__":unittest.main()
