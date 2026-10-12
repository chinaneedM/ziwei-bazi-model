"""12UE same-source correction and historical source identity regression."""
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def j(p):return json.loads((R/p).read_text(encoding='utf8'))
class Source12UE(unittest.TestCase):
 def test_controlling_readings(self):
  e=j("docs/research/MING-DATONG-YEHUOBIAN-12UE-XUXIU1174-SAME-SOURCE-GLYPH-MISREAD-REPAIR-R1.json")
  tb=j(e["controlling_earlier"]);ud=j(e["superseded_recent"])
  x=next(z["loci"] for z in tb["corrected_direct_image_loci"] if z["id"]=="XUXIU1174_2002")
  self.assertEqual(x,["宮禁","官漏","辰初二刻","戌初三刻"])
  self.assertEqual(e["corrected_same_source_loci"],x)
  self.assertEqual(ud["four_loci"][1]["reading"],"宮漏")
  sh=j("docs/research/MING-DATONG-YEHUOBIAN-12ST-XUXIU-1174-PUBLIC-SOURCE-SHARD-R1.json")
  self.assertEqual(sh["sources"][0]["post_12ue_forward_scoped_correction"]["corrected_source_loci"],x)
 def test_no_inflation(self):
  e=j("docs/research/MING-DATONG-YEHUOBIAN-12UE-XUXIU1174-SAME-SOURCE-GLYPH-MISREAD-REPAIR-R1.json")
  s=j("docs/PROJECT-CURRENT-STATE-R1.json");m=j("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
  self.assertFalse(e["gates"]["original_1827_unrepaired_leaf_seen"])
  self.assertEqual(m["additional_research_evidence_12ue"]["source_count_change"],0)
  self.assertEqual(m["combined_source_count"],678)
  self.assertEqual(s["invariants"]["algorithm_reopen_count"],0)
  self.assertTrue(any(x.startswith("12UE ") for x in s["historical_audit"]["current_focus"]))
if __name__=="__main__":unittest.main()
