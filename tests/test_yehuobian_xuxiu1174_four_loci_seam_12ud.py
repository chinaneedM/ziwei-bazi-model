"""12UD direct source image: close four textual loci without claiming the 1827 original."""
import json
import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(path):return json.loads((R/path).read_text(encoding='utf8'))
E='docs/research/MING-DATONG-YEHUOBIAN-12UD-XUXIU1174-FOUR-LOCI-SEAM-CORRECTION-R1.json'
P='docs/research/MING-DATONG-YEHUOBIAN-12UC-XUXIU1174-DIRECT-THREE-LOCI-AND-SEAM-GATE-R1.json'
S='docs/research/MING-DATONG-YEHUOBIAN-12ST-XUXIU-1174-PUBLIC-SOURCE-SHARD-R1.json'
M='docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json'
class SourceFourLoci12UD(unittest.TestCase):
 def test_forward_only_source_image_correction(self):
  e,p,s,m=read(E),read(P),read(S),read(M)
  self.assertEqual(p['four_loci'][3]['direct_reading'],None)
  self.assertEqual(e['trigger']['source_pdf_page_1based_lower'],506)
  self.assertEqual(e['trigger']['source_pdf_page_1based_upper'],507)
  self.assertIn('禁中宮漏循用新',e['trigger']['reading_tail_on_pdf506'])
  self.assertTrue(e['trigger']['reading_head_on_pdf507'].startswith('製不待言'))
  self.assertEqual([x['reading'] for x in e['four_loci']],['宮禁','宮漏','辰初二刻','戌初一刻'])
  self.assertTrue(all(x['visible'] for x in e['four_loci']))
  self.assertEqual(e['source_registry_id'],s['sources'][0]['source_id'])
  self.assertEqual(s['sources'][0]['post_12ud_forward_scoped_correction']['direct_facsimile_loci_count'],4)
  self.assertEqual(m['additional_research_evidence_12ud']['source_count_change'],0)
  self.assertEqual(m['combined_source_count'],678)
 def test_scope_and_no_runtime_reopen(self):
  e=read(E);s=read('docs/PROJECT-CURRENT-STATE-R1.json')
  self.assertFalse(e['facsimile_identity']['original_1827_first_impression_physically_verified'])
  self.assertEqual(e['correction_contract']['ancient_unrepaired_1827_original_witness_vote'],0)
  self.assertFalse(e['correction_contract']['calendar_or_runtime_rule_inference_authorized'])
  self.assertEqual(e['invariants']['source_registry_total'],s['historical_audit']['external_source_registry_total_unique_count'])
  self.assertEqual(s['invariants']['algorithm_reopen_count'],0)
  self.assertEqual(s['invariants']['deterministic_fusion_chart_product_r1'],'CLOSED')
  self.assertTrue(any(x.startswith('12UD ') for x in s['historical_audit']['current_focus']))
if __name__=='__main__':unittest.main()
