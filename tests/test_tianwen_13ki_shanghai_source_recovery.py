import copy, importlib.util, unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13ki-shanghai-source-recovery.py"
spec=importlib.util.spec_from_file_location("tw13ki_verify",p)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

class ShanghaiRecoveryGate(unittest.TestCase):
 def setUp(self):self.data=copy.deepcopy(list(v.load()))
 def rejects(self):
  with self.assertRaises(ValueError):v.verify(*self.data)
 def test_confirm_acquisition_scope(self):self.assertEqual(v.verify(*self.data)["status"],"PASS")
 def test_false_original_glyph(self):self.data[0]["critical_readings_not_awarded"]["huang_益加損減_original_glyph_proven"]=True;self.rejects()
 def test_false_physical_copy(self):self.data[0]["historical_scope"]["new_independent_physical_copy_votes"]=1;self.rejects()
 def test_false_registry_authority(self):self.data[1]["sources"][0]["physical_glyph_authority"]=True;self.rejects()
 def test_source_hash_replacement(self):self.data[0]["digital_source"]["sha256"]="0"*64;self.rejects()
 def test_future_append_only(self):
  self.data[2]["historical_audit"]["current_focus"].append("13KJ FUTURE WORK")
  self.data[3]["binding"]["source_focus_count"]+=1
  self.data[3]["binding"]["latest_research_focus_prefix"]="13KJ"
  i=next(x for x in self.data[3]["issues"] if x["id"]=="TW-OPEN-0005")
  i["next_action"]="13KJ CURRENT ACTION: "+i["next_action"]
  self.assertEqual(v.verify(*self.data)["status"],"PASS")
if __name__=="__main__":unittest.main()
