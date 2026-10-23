import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-solar-d30-action-13ec.py"
sp=importlib.util.spec_from_file_location("v13ec",p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class Test13EC(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L);cls.a=m.load(m.EA);cls.b=m.load(m.EB)
 def runcheck(self,e=None,l=None):return m.check(self.e if e is None else e,self.s,self.l if l is None else l,self.a,self.b)
 def test_positive(self):self.assertTrue(self.runcheck())
 def test_false_d30(self):
  x=copy.deepcopy(self.e);x["bounded_unresolved"]["value"]="0.965038"
  with self.assertRaises(AssertionError):self.runcheck(e=x)
 def test_fake_derived_original(self):
  x=copy.deepcopy(self.e);x["established_source_positive"][2]["value"]="0.964549"
  with self.assertRaises(AssertionError):self.runcheck(e=x)
 def test_stale_action(self):
  x=copy.deepcopy(self.l);z=next(i for i in x["issues"] if i["id"]=="TW-OPEN-0005");z["next_action"]=z["history"][-1]["previous_next_action"]
  with self.assertRaises(AssertionError):self.runcheck(l=x)
 def test_no_evidence_refs(self):
  x=copy.deepcopy(self.l);z=next(i for i in x["issues"] if i["id"]=="TW-OPEN-0005");z["history"][-1]["evidence_refs"]=[]
  with self.assertRaises(AssertionError):self.runcheck(l=x)
 def test_vote_spoof(self):
  x=copy.deepcopy(self.e);x["new_independent_physical_votes"]=1
  with self.assertRaises(AssertionError):self.runcheck(e=x)
if __name__=="__main__":unittest.main()
