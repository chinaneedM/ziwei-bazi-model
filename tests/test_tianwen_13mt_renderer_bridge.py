"""13MT pin renderer profiles, reject spoofed original variant and history rewrite."""
import copy,importlib.util,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("g13mt",R/"scripts/verify-tianwen-13mt-renderer-bridge.py")
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class VersionScopedDigest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.items=[json.loads(q.read_text(encoding="utf-8")) for q in (v.E,v.S,v.L,v.P,v.A)]
 def test_both_renderer_profiles(self):self.assertEqual(v.check(*self.items)["status"],"PASS")
 def test_false_same_source_byte_change(self):
  a=copy.deepcopy(self.items);a[0]["adjudication"]["source_pdf_byte_drift"]=True
  with self.assertRaises(AssertionError):v.check(*a)
 def test_false_physical_print_variation(self):
  a=copy.deepcopy(self.items);a[0]["adjudication"]["independent_printing_different"]=True
  with self.assertRaises(AssertionError):v.check(*a)
 def test_spoofed_old_roi_rejected(self):
  a=copy.deepcopy(self.items);a[0]["pinned_renderer_profiles"][0]["roi_rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):v.check(*a)
 def test_closed_historical_winner_forbidden(self):
  a=copy.deepcopy(self.items);a[0]["nonpromotion"]["g893_cross_original_historical_winners"]=1
  with self.assertRaises(AssertionError):v.check(*a)
 def test_forward_only_next_batch_supported(self):
  a=copy.deepcopy(self.items)
  a[1]["schema_version"]="1.983.0";a[1]["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.983.0";a[1]["historical_audit"]["current_focus"].append("13MU successor")
  a[2]["binding"]["reviewed_state_version"]="1.983.0";a[2]["binding"]["source_focus_count"]+=1
  self.assertEqual(v.check(*a)["status"],"PASS")
if __name__=="__main__":unittest.main()
