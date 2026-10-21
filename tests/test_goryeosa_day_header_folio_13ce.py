import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-day-header-folio-13ce.py"
sp=importlib.util.spec_from_file_location("topo13ce",p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class T13CE(unittest.TestCase):
 def setUp(self):self.e=m.load(m.E);self.s=m.load(m.S);self.l=m.load(m.L)
 def chk(self,e=None,s=None,l=None):return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l)
 def test_positive(self):self.assertTrue(self.chk())
 def test_day_forgery(self):
  a=copy.deepcopy(self.e);a["original_headings"][0]["literal"]="十六日"
  with self.assertRaises(AssertionError):self.chk(e=a)
 def test_roi_forgery(self):
  a=copy.deepcopy(self.e);a["original_headings"][5]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.chk(e=a)
 def test_folio_forgery(self):
  a=copy.deepcopy(self.e);a["original_headings"][5]["leaf"]="RIGHT"
  with self.assertRaises(AssertionError):self.chk(e=a)
 def test_unbound_cannot_be_claimed(self):
  a=copy.deepcopy(self.e);a["unresolved"]["WASEDA_D16_independent_yingsuoji"]="7570.6624"
  with self.assertRaises(AssertionError):self.chk(e=a)
 def test_future_state(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l);s["schema_version"]="1.999.0";s["historical_audit"]["current_focus"].append("13CF future");l["binding"]["reviewed_state_version"]="1.999.0";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);self.assertTrue(self.chk(s=s,l=l))
if __name__=="__main__":unittest.main()
