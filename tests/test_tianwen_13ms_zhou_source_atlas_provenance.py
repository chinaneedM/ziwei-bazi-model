"""13MS false physical identity and legacy hash equality are forbidden."""
import copy,importlib.util,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P=R/"scripts/verify-tianwen-13ms-zhou-source-atlas-provenance.py"
sp=importlib.util.spec_from_file_location("gate13ms",P);v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class ScopeGate(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.a=[json.loads(z.read_text(encoding="utf-8")) for z in (v.E,v.S,v.L,v.P)]
 def test_source_provenance_positive(self):self.assertEqual(v.check(*self.a)["status"],"PASS")
 def test_fake_same_cropped_pixels_rejected(self):
  a=copy.deepcopy(self.a);a[0]["pixel_replay_conflict"]["hashes_equal"]=True
  with self.assertRaises(AssertionError):v.check(*a)
 def test_fake_edition_certification_rejected(self):
  a=copy.deepcopy(self.a);a[0]["calendrical_dates_separated"]["specific_surviving_copy_impression_date"]="1569"
  with self.assertRaises(AssertionError):v.check(*a)
 def test_fake_historical_numeric_winner_rejected(self):
  a=copy.deepcopy(self.a);a[0]["no_promotion"]["g893_six_historical_winners"]=1
  with self.assertRaises(AssertionError):v.check(*a)
 def test_fake_full_original_register_rejected(self):
  a=copy.deepcopy(self.a);a[0]["original_acquisition"]["new_physical_copy_count"]=1
  with self.assertRaises(AssertionError):v.check(*a)
 def test_successor_version_forward_only(self):
  a=copy.deepcopy(self.a);a[1]["schema_version"]="1.982.0";a[1]["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.982.0";a[1]["historical_audit"]["current_focus"].append("13MT successor");a[2]["binding"]["reviewed_state_version"]="1.982.0";a[2]["binding"]["source_focus_count"]+=1
  self.assertEqual(v.check(*a)["status"],"PASS")
if __name__=="__main__":unittest.main()
