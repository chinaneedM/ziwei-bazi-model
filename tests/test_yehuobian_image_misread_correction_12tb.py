import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12TB-PRINT-IMAGE-MISREAD-CORRECTION-R1.json"
TA="docs/research/MING-DATONG-YEHUOBIAN-12TA-CROSS-IMAGE-THREE-KE-FOUR-LOCUS-MATRIX-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
def load(path):return json.loads((ROOT/path).read_text(encoding="utf8"))
class OriginalPrintImageRecheck12TB(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=load(REC);cls.ta=load(TA);cls.st=load(STATE)
 def test_archived_misreads_are_preserved_and_corrected_forward_only(self):
  self.assertEqual(self.ta["witnessed_readings"][1]["loci"][1],"宮漏")
  self.assertEqual(self.ta["witnessed_readings"][2]["loci"][3],"戌初二刻")
  direct={x["id"]:x["loci"] for x in self.r["corrected_direct_image_loci"]}
  self.assertEqual(direct["CADAL02096915"],direct["XUXIU1174_2002"])
  self.assertEqual(direct["CADAL02096915"],["宮禁","官漏","辰初二刻","戌初三刻"])
  self.assertEqual(len(self.r["corrections"]),3)
 def test_image_sha_and_no_stemmatic_claim(self):
  a=self.r["original_images"]
  self.assertEqual(a["cadal"]["jpeg_sha256"],"5e4f288f257a83b8f851c53c791dd2d2df52e18bd66276256ef6b64e546894a6")
  self.assertEqual(a["xuxiu"]["jpeg_sha256"],"ece3094a332ca5f329a1c21f27f3e65a3412a2ad252452cae5a17fe50fd0ac11")
  self.assertGreaterEqual(self.r["digital_registration"]["homography_inliers"],1800)
  self.assertFalse(self.r["digital_registration"]["source_image_identical_physical_copy_confirmed"])
  self.assertFalse(self.r["adjudication"]["cadal_xuxiu_as_independent_original_print_votes"])
  self.assertEqual(self.r["adjudication"]["printed_image_summer_readings"],["戌初一刻","戌初三刻"])
 def test_handoff_remains_forward_only(self):
  s=self.st
  self.assertTrue(any(x.startswith("12TB CADAL/1174") for x in s["historical_audit"]["current_focus"]))
  self.assertGreaterEqual(s["historical_audit"]["external_source_registry_total_unique_count"],660)
  self.assertEqual(s["historical_audit"]["external_source_registry_total_unique_count"],json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json").read_text(encoding="utf-8"))["combined_source_count"])
  self.assertEqual(len(s["historical_audit"]["completed_batches"]),487)
  self.assertEqual(s["invariants"]["algorithm_reopen_count"],0)
  self.assertEqual(s["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
if __name__=="__main__":unittest.main()
