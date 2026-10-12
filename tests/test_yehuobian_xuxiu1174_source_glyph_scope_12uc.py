"""12UC: physical source image establishes only three 2002 facsimile glyphs, not 1827 edition genealogy."""
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(s):return json.loads((R/s).read_text(encoding="utf8"))
E="docs/research/MING-DATONG-YEHUOBIAN-12UC-XUXIU1174-DIRECT-THREE-LOCI-AND-SEAM-GATE-R1.json"
S="docs/research/MING-DATONG-YEHUOBIAN-12ST-XUXIU-1174-PUBLIC-SOURCE-SHARD-R1.json"
M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
class ExactImageScope(unittest.TestCase):
 def test_direct_source_and_loci(self):
  e=load(E);s=load(S);m=load(M)
  self.assertEqual(e["source_identity"]["source_sha256"],"bee08d95d6b141a978f4d7fb068b97b74cf8ee25b46c6273110b2891a0faf953")
  self.assertEqual(e["source_identity"]["pdf_page_count"],810)
  self.assertEqual(e["direct_location"]["section_title_pdf_page_1based"],506)
  self.assertEqual(e["direct_location"]["section_title_printed_volume_page"],503)
  self.assertEqual([x["direct_reading"] for x in e["four_loci"]],["宮禁","辰初二刻","戌初一刻",None])
  self.assertTrue(all(x["vote_for_unrepaired_1827_original"] is False for x in e["four_loci"]))
  self.assertEqual(e["four_loci"][3]["scope"],"P506_P507_BOUNDARY_GLYPH_SEQUENCE_UNRESOLVED")
  self.assertEqual(e["source_registry_id"],s["sources"][0]["source_id"])
  self.assertEqual(s["sources"][0]["post_12uc_forward_scoped_correction"]["direct_facsimile_loci_count"],3)
  self.assertEqual(m["combined_source_count"],678)
  self.assertEqual(m["additional_research_evidence_12uc"]["source_count_change"],0)
  self.assertEqual(m["additional_research_evidence_12uc"]["unresolved_seam_loci"],1)
 def test_product_and_lineage_firewall(self):
  e=load(E);state=load("docs/PROJECT-CURRENT-STATE-R1.json")
  self.assertEqual(e["invariants"]["ancient_1827_original_glyph_votes"],0)
  self.assertEqual(e["invariants"]["graph_nodes"],250)
  self.assertEqual(e["invariants"]["graph_edges"],237)
  self.assertEqual(e["invariants"]["chart_algorithm_reopens"],0)
  self.assertEqual(state["historical_audit"]["external_source_registry_total_unique_count"],678)
  self.assertEqual(state["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
  self.assertEqual(state["invariants"]["algorithm_reopen_count"],0)
  self.assertTrue(state["historical_audit"]["current_focus"][-1].startswith("12UC "))
if __name__=="__main__":unittest.main()
