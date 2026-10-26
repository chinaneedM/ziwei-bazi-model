import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"scripts/verify-tianwen-13hv-winter-d16.py"
S=importlib.util.spec_from_file_location("hv",P)
M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
class DirectThreePhotoTest(unittest.TestCase):
 def setUp(self):self.e=json.loads(M.E.read_text(encoding="utf8"))
 def test_sources_and_ledger(self):self.assertTrue(M.check(self.e))
 def test_no_counterfactual_as_print(self):
  e=copy.deepcopy(self.e);e["holdings"][0]["rows"][1]["literal"]="五分二三六二"
  with self.assertRaises(AssertionError):M.check(e,False)
 def test_d16_sha_immutable(self):
  e=copy.deepcopy(self.e);e["holdings"][1]["rows"][1]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):M.check(e,False)
 def test_no_winner_by_three_same_strings(self):
  e=copy.deepcopy(self.e);e["firewall"]["ancestor_of_discrepancy_proven"]=True
  with self.assertRaises(AssertionError):M.check(e,False)
 def test_no_registry_inflation(self):
  e=copy.deepcopy(self.e);e["firewall"]["no_new_registered_sources"]=False
  with self.assertRaises(AssertionError):M.check(e,False)
