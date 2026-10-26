import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("hl",ROOT/"scripts/verify-tianwen-13hl-ncl03130-source-native-intake.py")
M=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(M)
class NativeNclScope(unittest.TestCase):
 def setUp(self):self.e=json.loads(M.E.read_text(encoding="utf8"))
 def test_exact_scope_and_handoff(self):self.assertTrue(M.check(self.e))
 def test_neighbor_not_target(self):
  e=copy.deepcopy(self.e);e["provider_controls"]["indexed_neighbor_example"]["is_03130_target"]=True
  with self.assertRaises(AssertionError):M.check(e)
 def test_unverified_native_item(self):
  e=copy.deepcopy(self.e);e["provider_controls"]["exact_03130_native_item_url_obtained"]=True
  with self.assertRaises(AssertionError):M.check(e)
 def test_unsent_not_sent(self):
  e=copy.deepcopy(self.e);e["authorization_firewall"]["contact_or_application_submitted"]=True
  with self.assertRaises(AssertionError):M.check(e)
 def test_photo_not_ncl_glyph(self):
  e=copy.deepcopy(self.e);e["source_scope"]["local_original_d14_full_numeral"]="四分六六三〇"
  with self.assertRaises(AssertionError):M.check(e)
