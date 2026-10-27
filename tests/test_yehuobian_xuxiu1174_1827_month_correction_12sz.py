import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
C="docs/research/MING-DATONG-YEHUOBIAN-12SZ-XUXIU1174-1827-PREFACE-MONTH-FORWARD-CORRECTION-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
class MonthCorrection12SZ(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/C).read_text(encoding="utf8"))
  cls.old=json.loads((ROOT/cls.r["supersedes_assertion_in"]).read_text(encoding="utf8"))
  cls.state=json.loads((ROOT/S).read_text(encoding="utf8"))
 def test_forward_only_original_preserved_with_explicit_delta(self):
  old=[x for x in self.old["image_read_prefatory_dates"] if x["year"]==1827][0]["reading"]
  self.assertEqual(old,self.r["prior_assertion"])
  self.assertIn("春二月",old)
  self.assertIn("春三月",self.r["corrected_reading"])
  self.assertTrue(self.r["adjudication"]["incorrect_12SY_record_preserved"])
  self.assertEqual(self.r["difference"]["incorrect"],"二")
  self.assertEqual(self.r["difference"]["correct"],"三")
 def test_two_catalogs_corroborate_word_not_physical_glyph_vote(self):
  self.assertEqual({v["ncid"] for v in self.r["cross_checks"]},{"BB23196128","BB18578034"})
  self.assertTrue(all("春三月" in v["passage"] for v in self.r["cross_checks"]))
  self.assertEqual(self.r["adjudication"]["independent_1827_original_target_glyphs_added"],0)
  self.assertEqual(self.r["adjudication"]["new_external_source_added"],0)
 def test_continuity_and_product_not_modified(self):
  a=self.state["historical_audit"]
  self.assertTrue(any(x.startswith("12SZ XUXIU1174") for x in a["current_focus"]))
  self.assertGreaterEqual(a["external_source_registry_total_unique_count"],660)
  self.assertEqual(a["external_source_registry_total_unique_count"],json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json").read_text(encoding="utf-8"))["combined_source_count"])
  self.assertGreaterEqual(len(a["completed_batches"]),487)
  self.assertEqual(self.state["invariants"]["algorithm_reopen_count"],0)
  self.assertEqual(self.state["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
if __name__=="__main__":unittest.main()
