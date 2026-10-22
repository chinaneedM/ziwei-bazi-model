import copy, importlib.util, unittest
from pathlib import Path
f=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-nlc416-summer-d28-native-13dd.py"
spec=importlib.util.spec_from_file_location("tw13dd",f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13DD(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L)
 def go(self,e=None,l=None):return m.check(self.e if e is None else e,self.s,self.l if l is None else l)
 def mutate(self,fn):
  e=copy.deepcopy(self.e);fn(e)
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_positive(self):self.assertTrue(self.go())
 def test_glyph_alteration(self):self.mutate(lambda e:e["source_native_rois"][5].update(literal="初度九十六四五四九"))
 def test_source_sha_alteration(self):self.mutate(lambda e:e["acquisition"].update(source_sha256="0"*64))
 def test_roi_sha_alteration(self):self.mutate(lambda e:e["source_native_rois"][5].update(rgb_sha256="0"*64))
 def test_wrong_d28_number(self):self.mutate(lambda e:e["source_native_rois"][5].update(value="0.964549"))
 def test_preferred_candidate_promoted(self):self.mutate(lambda e:e["independent_decimal_replay"].update(ultimate_source_emendation_authorized=True))
 def test_ancient_vote_inflation(self):self.mutate(lambda e:e["adjudication"].update(new_independent_early_historical_witnesses=1))
 def test_winter_summer_conflated(self):self.mutate(lambda e:e["adjudication"].update(winter_D16_difference_5_1362_vs_5_2362="CLOSED"))
 def test_ledger_binding(self):
  l=copy.deepcopy(self.l);l["binding"]["source_focus_count"]-=1
  with self.assertRaises(AssertionError):self.go(l=l)
if __name__=="__main__":unittest.main()
