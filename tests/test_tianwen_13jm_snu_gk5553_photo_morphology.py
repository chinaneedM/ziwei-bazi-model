import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13JM-GK5553-8-26-MANUSCRIPT-NEIGHBOR-SIX-ORIGINAL-IMAGE-SCOPE-R1.json"
S=R/'docs/PROJECT-CURRENT-STATE-R1.json'
L=R/'docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json'
class CopyMorphology(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.d=json.loads(E.read_text(encoding='utf-8'));cls.s=json.loads(S.read_text(encoding='utf-8'));cls.l=json.loads(L.read_text(encoding='utf-8'))
 def test_six_originals_authentic_source_chain(self):
  d=self.d
  self.assertEqual(d['source_chain']['source_exact_original_images_artifact'],12809334156)
  self.assertEqual([(p['digital_volume'],p['printed_work_juan']) for p in d['pages']],[('0008',19),('0026',73),('0011',28),('0013',35),('0025',69),('0027',75)])
  self.assertTrue(all(len(p['jpeg_sha256'])==64 and len(p['rgb_sha256'])==64 and len(p['native_rgb_rois'])==2 for p in d['pages']))
 def test_neighborhood_groupings_no_physical_promotion(self):
  a=self.d['source_scoped_adjudication']
  self.assertEqual(a['digital_volumes_handwritten'],['0008','0026','0029'])
  self.assertEqual(a['digital_volumes_printed'],['0011','0012','0013','0025','0027'])
  self.assertIsNone(a['manuscript_copying_date'])
  self.assertEqual(a['independent_physical_witness_votes_added'],0)
  self.assertTrue(all(self.d['firewall'].values()))
 def test_g893_other_targets_not_inferred(self):
  self.assertEqual(self.d['transmission_impact']['edges_supported'],[])
  self.assertEqual(self.d['counts']['algorithm_reopen'],0)
  self.assertEqual(self.d['counts']['source_total'],763)
 def test_state_continuity(self):
  self.assertEqual(self.s['schema_version'],self.l['binding']['reviewed_state_version'])
  self.assertEqual(self.s['historical_audit']['research_omission_guard']['reviewed_state_version'],self.s['schema_version'])
  self.assertEqual(self.l['binding']['source_focus_count'],len(self.s['historical_audit']['current_focus']))
  self.assertEqual(self.l['binding']['latest_research_focus_prefix'],'13JN')
  self.assertTrue(self.s['historical_audit']['current_focus'][-2].startswith('13JM '))
  self.assertTrue(self.s['historical_audit']['current_focus'][-1].startswith('13JN '))
 def test_previous_batch_and_legacy_tokens_preserved(self):
  i=next(x for x in self.l['issues'] if x['id']=='TW-OPEN-0005')
  self.assertEqual((i['status'],i['priority']),('OPEN','P0'))
  self.assertIn(E.relative_to(R).as_posix(),i['source_refs'])
  for word in ('13JM CURRENT ACTION:','13JJ CURRENT ACTION:','13JG CURRENT ACTION:','GK03539_00','G893','GK3467','NLC03130 solar D30','NULL','四分','初度','13EI','RETRACTED'):self.assertIn(word,i['next_action'])
  self.assertTrue(any(x.get('revision_id','').startswith('TW-OPEN-0005-13JM') for x in i['history']))
  self.assertEqual(self.l['checkpoint_log'][-1]['state_version'],self.s['schema_version'])
if __name__=='__main__':unittest.main()
