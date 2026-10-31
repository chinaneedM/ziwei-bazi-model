"""13MR regression: source-local operation cannot be promoted into cross-source equivalence."""
import copy,importlib.util,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P=R/"scripts/verify-tianwen-13mr-zhou-operator-scope.py"
sp=importlib.util.spec_from_file_location("gate13mr",P)
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class OriginalOperatorScope(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=[json.loads(x.read_text(encoding="utf-8")) for x in (v.E,v.S,v.L,v.P)]
 def test_original_operator_metadata_only(self):
  self.assertEqual(v.check(*self.data)["pixel_replay"],"NOT_EXECUTED_WITHOUT_SOURCE_BYTES")
 def test_fake_field_equivalence_rejected(self):
  items=copy.deepcopy(self.data);items[0]["comparison"]["cross_source_field_unit_radix_epoch_identity"]="PROVEN"
  with self.assertRaises(AssertionError):v.check(*items)
 def test_fake_new_hash_rejected(self):
  items=copy.deepcopy(self.data);items[0]["source"]["new_source_pixel_sha_computed_this_batch"]=True
  with self.assertRaises(AssertionError):v.check(*items)
 def test_false_d15_equal_string_rejected(self):
  items=copy.deepcopy(self.data);items[0]["comparison"]["same_printed_strings"]=True
  with self.assertRaises(AssertionError):v.check(*items)
 def test_historical_winner_promotion_rejected(self):
  items=copy.deepcopy(self.data);items[0]["guard"]["g893_final_historical_winners"]=1
  with self.assertRaises(AssertionError):v.check(*items)
 def test_state_forward_successor_safe(self):
  items=copy.deepcopy(self.data)
  items[1]["schema_version"]="1.981.0";items[1]["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.981.0";items[1]["historical_audit"]["current_focus"].append("13MS successor")
  items[2]["binding"]["reviewed_state_version"]="1.981.0";items[2]["binding"]["source_focus_count"]+=1
  self.assertEqual(v.check(*items)["status"],"PASS")
if __name__=="__main__":unittest.main()
