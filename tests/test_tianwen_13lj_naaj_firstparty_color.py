import copy,importlib.util,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'scripts/verify-tianwen-13lj-naaj-firstparty-color.py'
spec=importlib.util.spec_from_file_location('tw13lj',P);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class ColorEvidenceScope(unittest.TestCase):
 def setUp(self):self.data=copy.deepcopy(list(v.load()))
 def reject(self):
  with self.assertRaises(AssertionError):v.check(*self.data)
 def test_verified_source(self):self.assertEqual(v.check(*self.data)['native_numeric_regions'],2)
 def test_catalog_only_upgrade(self):self.data[0]['manual_numeric_collations']=[];self.reject()
 def test_claim_downloaded_jp2(self):self.data[0]['interpretation']['original_jp2_downloaded']=True;self.reject()
 def test_claim_raw(self):self.data[0]['interpretation']['unprocessed_optical_RAW_proven']=True;self.reject()
 def test_claim_lossless(self):self.data[0]['interpretation']['jpeg2000_lossless_proven']=True;self.reject()
 def test_claim_ancient_date(self):self.data[0]['interpretation']['dated_1739_impression_proven']=True;self.reject()
 def test_claim_woodblock(self):self.data[0]['interpretation']['same_woodblock_proven']=True;self.reject()
 def test_false_jbig2_substitution(self):self.data[0]['interpretation']['jbig2_wrong_symbol_substitution_proven']=True;self.reject()
 def test_count_same_copy_twice(self):self.data[0]['interpretation']['independent_historical_recensions_added']=2;self.reject()
 def test_siku_erasure(self):self.data[0]['interpretation']['siku_original_literal_retained']='238977.09';self.reject()
 def test_change_native_coordinate(self):self.data[1]['sources'][0]['pages'][1]['roi_xyxy'][0]+=1;self.reject()
 def test_promote_acquisition_review(self):self.data[1]['sources'][0]['pages'][1]['human_reading']='COMPLETE';self.reject()
 def test_wrong_source_rgb(self):self.data[0]['manual_numeric_collations'][0]['roi_rgb_sha256']='0'*64;self.reject()
 def test_stale_mask_claim(self):self.data[0]['manual_numeric_collations'][0]['source_medium']='PDF_JBIG2';self.reject()
 def test_false_numeric(self):self.data[0]['manual_numeric_collations'][0]['numeric']='288977.09';self.reject()
 def test_forward_compatible(self):
  e,a,s,l=self.data;s['historical_audit']['current_focus'].append('13LK next source review')
  l['binding']['source_focus_count']+=1;l['binding']['latest_research_focus_prefix']='13LK'
  issue=next(x for x in l['issues'] if x['id']=='TW-OPEN-0005');issue['next_action']='13LK CURRENT ACTION: next\n'+issue['next_action']
  self.assertEqual(v.check(*self.data)['status'],'PASS')
if __name__=='__main__':unittest.main()
