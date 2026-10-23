import copy,importlib.util,unittest
from pathlib import Path
f=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-solar-d27-d30-original-13eb.py"
sp=importlib.util.spec_from_file_location("t13eb",f);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class Test13EB(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L);cls.p=m.load(m.P)
 def go(self,e=None,s=None,l=None):return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l,self.p)
 def bad(self,fn):
  e=copy.deepcopy(self.e);fn(e)
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_positive(self):self.assertTrue(self.go())
 def test_d27_wrong_glyph(self):self.bad(lambda e:e["rows"][0].update(literal="初度九十六四〇六二"))
 def test_d27_wrong_numeric(self):self.bad(lambda e:e["rows"][0].update(value="0.964549"))
 def test_d27_wrong_source_sha(self):self.bad(lambda e:e["rows"][0].update(field_rgb_sha256="0"*64))
 def test_d30_false_numeric(self):self.bad(lambda e:e["rows"][1].update(value="0.965038"))
 def test_d30_false_literal(self):self.bad(lambda e:e["rows"][1].update(literal="初度九十六五〇三八"))
 def test_d30_wrong_roi(self):self.bad(lambda e:e["rows"][1].update(field_bbox=[0,0,1,1]))
 def test_fake_independent_vote(self):self.bad(lambda e:e["scope"].update(independent_votes_added=1))
 def test_fake_global_law(self):self.bad(lambda e:e["cross"].update(global_day_offset_established=True))
 def test_future_focus(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["schema_version"]="FUTURE";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="FUTURE"
  s["historical_audit"]["current_focus"].append("13EC NEXT")
  l["binding"].update(reviewed_state_version="FUTURE",latest_research_focus_prefix="13EC",source_focus_count=len(s["historical_audit"]["current_focus"]))
  l["checkpoint_log"].append({"state_version":"FUTURE","reviewed_issue_ids":[x["id"] for x in l["issues"]]})
  self.assertTrue(self.go(s=s,l=l))
if __name__=="__main__":unittest.main()
