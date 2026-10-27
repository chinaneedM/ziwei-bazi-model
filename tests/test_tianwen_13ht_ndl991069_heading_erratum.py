import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"scripts/verify-tianwen-13ht-ndl991069-heading-erratum.py"
S=importlib.util.spec_from_file_location("ht",P)
M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
class Ndl1909HeadingErratum(unittest.TestCase):
 def setUp(self):self.e=json.loads(M.E.read_text(encoding="utf8"))
 def test_forward_only_handoff_and_prior_immutable(self):self.assertTrue(M.check(self.e))
 def test_cannot_keep_old_heading_as_authority(self):
  x=copy.deepcopy(self.e);x["corrected_direct_source_reading"]=M.OLD
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_cannot_misread_terminal_as_qi(self):
  x=copy.deepcopy(self.e);x["corrected_pairwise_atoms"][1]["direct"]="二氣"
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_cannot_invent_independent_physical_witness(self):
  x=copy.deepcopy(self.e);x["firewall"]["new_physical_witnesses"]=1
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_cannot_replace_day16_print_with_arithmetic_guess(self):
  x=copy.deepcopy(self.e);x["institutional_text_crosscheck"]["winter_day16_literal_in_official_text"]="五分二三六二"
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_pixel_binding_cannot_change_without_new_evidence(self):
  x=copy.deepcopy(self.e);x["source_roi"]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):M.check(x,False)
