import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'scripts'/'verify-tianwen-13fb-nikh-thumb-cert.py'
s=importlib.util.spec_from_file_location('v13fb',p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Test13FB(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=v.get(v.P);cls.s=v.get(v.C);cls.l=v.get(v.L);cls.m=v.get(v.M)
 def good(self,e=None):return v.check(self.e if e is None else e,self.s,self.l,self.m)
 def deny(self,fn):
  x=copy.deepcopy(self.e);fn(x)
  with self.assertRaises(AssertionError):self.good(x)
 def test_pass(self):self.assertTrue(self.good())
 def test_fake_highres(self):self.deny(lambda x:x['native_viewer'].update(full_resolution_original_image_acquired=True))
 def test_fake_folio(self):self.deny(lambda x:x['native_viewer'].update(source_original_leaf_number=52))
 def test_fake_missing_original(self):self.deny(lambda x:x['bounded_thumbnail_requests'][1].update(status='ABSENT_FROM_MANUSCRIPT'))
 def test_forged_thumb_sha(self):self.deny(lambda x:x['bounded_thumbnail_requests'][0].update(sha256='0'*64))
 def test_image_list_mutation(self):self.deny(lambda x:x['native_viewer'].update(source_emitted_image_count=24))
 def test_false_ancient_glyph(self):self.deny(lambda x:x['impact'].update(original_historic_glyph_votes_added=1))
 def test_false_stemma(self):self.deny(lambda x:x['impact'].update(genealogy_edges_added=1))
 def test_false_numeric(self):self.deny(lambda x:x['numerical_and_philological_firewall'].update(precise_historic_numeric_D5=5.5172))
 def test_13ei_revival(self):self.deny(lambda x:x['numerical_and_philological_firewall'].update(old_13EI_false_source_claim='APPROVED'))
 def test_algorithm_reopen(self):self.deny(lambda x:x['impact'].update(algorithm_reopens=1))
if __name__=='__main__':unittest.main()
