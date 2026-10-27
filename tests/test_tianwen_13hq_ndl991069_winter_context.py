import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location("tianwen13hq",ROOT/"scripts/verify-tianwen-13hq-ndl991069-winter-context.py")
M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
class NdlWinterPageContinuity(unittest.TestCase):
 def setUp(self): self.e=json.loads(M.E.read_text(encoding="utf8"))
 def test_header_and_provenance(self):self.assertTrue(M.check(self.e))
 def test_no_false_ancient_numeric_winner(self):
  x=copy.deepcopy(self.e);x["contextual_reading"]["ancient_numerical_winner"]="五分一九九〇"
  with self.assertRaises(AssertionError): M.check(x)
 def test_no_nikh_summer_merge(self):
  x=copy.deepcopy(self.e);x["scope_firewall"]["printed_winter_surplus_deficit_context_does_not_equal_nikh_summer_d14"]=False
  with self.assertRaises(AssertionError): M.check(x)
 def test_pixel_source_region_integrity(self):
  x=copy.deepcopy(self.e);x["image_regions"][1]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError): M.check(x)
 def test_no_missing_old_copy_promotion(self):
  x=copy.deepcopy(self.e);x["scope_firewall"]["NCL03130_original_D14_full"]="四分六六三〇"
  with self.assertRaises(AssertionError): M.check(x)
