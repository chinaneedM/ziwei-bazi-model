import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-solar-d30-extended-strip-13ed.py"
spec=importlib.util.spec_from_file_location("v13ed",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13ED(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.read(m.E);cls.s=m.read(m.S);cls.l=m.read(m.L);cls.b=m.read(m.B);cls.a=m.read(m.A)
 def go(self,e=None,l=None):return m.check(self.e if e is None else e,self.s,self.l if l is None else l,self.b,self.a)
 def bad(self,fn):
  e=copy.deepcopy(self.e);fn(e)
  with self.assertRaises(AssertionError):self.go(e)
 def test_replay_metadata(self):self.assertTrue(self.go())
 def test_false_numeric_fill(self):self.bad(lambda e:e["finding"].update(full_precision_historical_numeric_assignment="0.96203"))
 def test_false_other_copy_substitution(self):self.bad(lambda e:e["comparison"].update(original_d30_numeric_value="0.965038"))
 def test_native_full_strip_hash_integrity(self):self.bad(lambda e:e["native_rois"][2].update(rgb_sha256="0"*64))
 def test_negative_tail_hash_integrity(self):self.bad(lambda e:e["native_rois"][3].update(rgb_sha256="0"*64))
 def test_false_copyist_attribution(self):self.bad(lambda e:e["finding"].update(missing_or_elided_digits_caused_by_copyist_proven=True))
 def test_false_independent_vote(self):self.bad(lambda e:e["impact"].update(independent_votes_added=1))
 def test_stale_action_fails(self):
  l=copy.deepcopy(self.l);z=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005");z["next_action"]=z["history"][-1]["previous_next_action"]
  with self.assertRaises(AssertionError):self.go(l=l)
 def test_forward_action_reference_required(self):
  l=copy.deepcopy(self.l);z=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005");z["history"][-1]["evidence_refs"]=[]
  with self.assertRaises(AssertionError):self.go(l=l)
if __name__=="__main__":unittest.main()
