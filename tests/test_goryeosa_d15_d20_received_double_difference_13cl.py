import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-d15-d20-received-double-difference-13cl.py"
spec=importlib.util.spec_from_file_location("research13cl",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13CL(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=m.load(m.E);cls.s=m.load(m.STATE);cls.l=m.load(m.LEDGER);cls.reg=m.load(m.REGISTRY)
  cls.old={k:m.load(v["path"]) for k,v in cls.e["exact_original_record_bindings"].items()}
 def check(self,e=None,s=None,l=None):
  return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l,self.reg,self.old)
 def test_pass(self):self.assertTrue(self.check())
 def test_silent_original_emendation(self):
  e=copy.deepcopy(self.e);e["received_rows"][1]["short"]="5.2362"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_fake_daily_short_increment(self):
  e=copy.deepcopy(self.e);e["local_received_arithmetic"]["short_edges"][1]["difference"]="0.0186"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_fake_cumulative(self):
  e=copy.deepcopy(self.e);e["received_rows"][2]["c"]="8000.0000"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_unit_promotion(self):
  e=copy.deepcopy(self.e);e["source_column_identity"]["historical_shao_wei_to_decimal_unit_bridge"]="PROVEN"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_fake_original_blob(self):
  e=copy.deepcopy(self.e);e["exact_original_record_bindings"]["13CI"]["sha"]="a"*40
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_krdb_tail_silence(self):
  e=copy.deepcopy(self.e);e["received_rows"][3]["institutional_received_c_glyph"]="八千四百二十四六四〇八"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_forward_only_future_add(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["schema_version"]="1.900.0";s["historical_audit"]["current_focus"].append("13ZZ later")
  l["binding"]["reviewed_state_version"]="1.900.0";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13ZZ"
  self.assertTrue(self.check(s=s,l=l))
if __name__=="__main__":unittest.main()
