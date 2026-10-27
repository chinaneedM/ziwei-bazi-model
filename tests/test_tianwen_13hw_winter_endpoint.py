import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"scripts/verify-tianwen-13hw-winter-endpoint.py"
S=importlib.util.spec_from_file_location("hw",P);M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
class ReceivedEndpoint(unittest.TestCase):
 def setUp(self): self.e=json.loads(M.E.read_text(encoding="utf8"))
 def test_state_and_source(self): self.assertTrue(M.check(self.e))
 def test_printed_d16_must_not_be_replaced_by_arithmetic(self):
  x=copy.deepcopy(self.e);x["anchor_rows"][2]["literal"]="五分二三六二"
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_cannot_rewrite_earlier_three_source_photo(self):
  x=copy.deepcopy(self.e);x["firewall"]["d16_two_not_attested_in_three_photos"]=False
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_endpoint_slope_is_verified(self):
  x=copy.deepcopy(self.e);x["anchor_rows"][4]["encoded"]=65569
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_no_fabricated_early_print(self):
  x=copy.deepcopy(self.e);x["firewall"]["added_independent_physical_witnesses"]=1
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_separate_sejong_title_and_units(self):
  x=copy.deepcopy(self.e);x["crosswork_title_control"]["edited_title"]="大陽冬至前後二象盈初縮末限"
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_no_exhaustive_claim_for_sparse_anchors(self):
  x=copy.deepcopy(self.e);x["arithmetic"]["full_0_to_88_table_exhaustively_verified"]=True
  with self.assertRaises(AssertionError):M.check(x,False)
