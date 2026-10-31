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
 def test_legacy_nonrevision_event_allowed(self):
  l=copy.deepcopy(self.l)
  i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  i["history"].insert(0,{"event":"HISTORICAL_ADMISSION"})
  self.assertEqual(v.check(self.e,self.s,l)["status"],"PASS")
 def test_missing_exact_13mo_revision_rejected(self):
  l=copy.deepcopy(self.l)
  i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  i["history"]=[x for x in i["history"] if x.get("revision_id")!="TW-OPEN-0005-13MO-PAIRED-SOURCE-COMPARISON-20261031"]
  with self.assertRaises(AssertionError):v.check(self.e,self.s,l)
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
 def test_successor_state_allowed(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["schema_version"]="1.978.0"
  s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.978.0"
  s["historical_audit"]["current_focus"].append("13MP successor, preserves 13MO source proof")
  l["binding"]["reviewed_state_version"]="1.978.0"
  l["binding"]["source_focus_count"]+=1
  l["binding"]["latest_research_focus_prefix"]="13MP"
  self.assertEqual(v.check(self.e,s,l)["status"],"PASS")
 def test_false_missing_predecessor_rejected(self):
  s=copy.deepcopy(self.s)
  s["historical_audit"]["current_focus"]=[x for x in s["historical_audit"]["current_focus"] if not x.startswith("13MO ")]
  with self.assertRaises(AssertionError):v.check(self.e,s,self.l)
if __name__=="__main__":unittest.main()
