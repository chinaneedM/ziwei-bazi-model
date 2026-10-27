import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-naj-summer-three-holding-13dg.py"
s=importlib.util.spec_from_file_location("tw13dg",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Test13DG(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.load(m.E);cls.w=m.load(m.W);cls.p=m.load(m.P);cls.s=m.load(m.S);cls.l=m.load(m.L)
 def check(self,e=None,l=None):return m.check(self.e if e is None else e,self.w,self.p,self.s,self.l if l is None else l)
 def fail(self,f):
  e=copy.deepcopy(self.e);f(e)
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_positive(self):self.assertTrue(self.check())
 def test_wrong_original_sha(self):self.fail(lambda e:e["naj_physical_witness"].update(source_jpeg_sha256="0"*64))
 def test_wrong_d29_read(self):self.fail(lambda e:e["naj_direct_rows"][1].update(glyph="初度九十六四五四九"))
 def test_wrong_roi(self):self.fail(lambda e:e["naj_direct_rows"][1].update(roi_sha256="0"*64))
 def test_false_live_success(self):self.fail(lambda e:e["naj_physical_witness"]["current_live_reacquisition"].update(http_status=200))
 def test_false_stemma_independence(self):self.fail(lambda e:e["three_holding_comparison"].update(established_stemmatically_independent_votes_added=3))
 def test_false_chart_fix(self):self.fail(lambda e:e["impact"].update(algorithm_reopens=1))
 def test_false_candidate(self):self.fail(lambda e:e["three_holding_comparison"].update(candidate_0_964549_attested_as_original_in_any_of_these_loci=True))
 def test_ledger(self):
  l=copy.deepcopy(self.l);l["binding"]["source_focus_count"]-=1
  with self.assertRaises(AssertionError):self.check(l=l)
if __name__=="__main__":unittest.main()
