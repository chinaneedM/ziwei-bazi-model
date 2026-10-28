import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13JJ-SNU-GK5553-ORIGINAL-12-29-PHOTO-COLLATION-R1.json"
S=R/"docs/PROJECT-CURRENT-STATE-R1.json"
L=R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
class PhotoScope(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=json.loads(E.read_text(encoding='utf-8'));cls.s=json.loads(S.read_text(encoding='utf-8'));cls.l=json.loads(L.read_text(encoding='utf-8'))
 def test_five_bounded_originals(self):
  self.assertEqual([(x['digital_volume'],x['page_no'],x['work_juan']) for x in self.e['original_pages']],[('0012','002a',31),('0012','075a',33),('0029','001a',81),('0029','038a',82),('0029','081a',83)])
  self.assertTrue(all(len(x['source_jpeg_sha256'])==64 and len(x['source_heading_rgb_roi_sha256'])==64 for x in self.e['original_pages']))
 def test_physical_firewall(self):
  c=self.e['evidence_scope'];self.assertEqual(c['khs_book_replacements'],[8,12,26]);self.assertEqual(c['snu_book_replacements'],[8,26,29]);self.assertTrue(c['digital_volume_number_not_proven_physical_book_number'])
  self.assertEqual(self.e['impact']['independent_physical_witness_votes_added'],0)
 def test_altered_algorithm_disallowed(self):
  self.assertEqual(self.e['impact']['algorithm_reopens'],0);self.assertEqual(self.e['transmission_impact']['edges_supported'],[])
 def test_sync(self):
  self.assertEqual(self.s['schema_version'],self.l['binding']['reviewed_state_version'])
  self.assertEqual(self.s['historical_audit']['research_omission_guard']['reviewed_state_version'],self.s['schema_version'])
  self.assertEqual(self.l['binding']['source_focus_count'],len(self.s['historical_audit']['current_focus']))
  self.assertIn('13JJ ',self.s['historical_audit']['current_focus'][-1][:5])
 def test_living_issue(self):
  issue=next(x for x in self.l['issues'] if x['id']=='TW-OPEN-0005')
  self.assertEqual((issue['priority'],issue['status']),('P0','OPEN'));self.assertIn(E.relative_to(R).as_posix(),issue['source_refs'])
  self.assertTrue(issue['next_action'].startswith('13JJ CURRENT ACTION:'))
  for word in ('13JG CURRENT ACTION:','GK03539_00','G893','GK3467','NULL','四分','初度','RETRACTED'):self.assertIn(word,issue['next_action'])
  self.assertEqual(self.l['checkpoint_log'][-1]['state_version'],self.s['schema_version'])
if __name__=='__main__':unittest.main()
