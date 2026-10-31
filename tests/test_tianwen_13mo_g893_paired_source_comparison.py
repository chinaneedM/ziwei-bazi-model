"""13MO paired original lane guard: reject history promotion and digit drift."""
import copy,importlib.util,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P=R/"scripts/verify-tianwen-13mo-g893-paired-source-comparison.py"
spec=importlib.util.spec_from_file_location("gate13mo",P)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class PairedLaneGate(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=json.loads(v.E.read_text(encoding="utf-8"))
  cls.s=json.loads(v.S.read_text(encoding="utf-8"))
  cls.l=json.loads(v.L.read_text(encoding="utf-8"))
 def test_source_pair_pass(self):
  self.assertEqual(v.check(self.e,self.s,self.l)["status"],"PASS")
 def test_short_d16_tamper(self):
  e=copy.deepcopy(self.e);e["paired_column_transcriptions"][1]["short"]="5.1362"
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
 def test_long_d16_tamper(self):
  e=copy.deepcopy(self.e);e["paired_column_transcriptions"][1]["long"]="429.6072"
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
 def test_false_copy_independence(self):
  e=copy.deepcopy(self.e);e["limits"]["zhous_1569_physical_impression_catalog_independence_bound"]=True
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
 def test_false_six_winner(self):
  e=copy.deepcopy(self.e);e["limits"]["historical_cross_original_six_target_winners"]=1
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
 def test_false_field_identity(self):
  e=copy.deepcopy(self.e);e["limits"]["full_field_header_unit_radix_day_anchor_identity_bound"]=True
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
if __name__=="__main__":unittest.main()
