import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location("hs",ROOT/"scripts/verify-tianwen-13hs-ndl991069-d16-firstfield.py")
M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
class Exact1909FirstFieldTest(unittest.TestCase):
 def setUp(self): self.e=json.loads(M.E.read_text(encoding="utf8"))
 def test_source_and_issue_handoff(self): self.assertTrue(M.check(self.e))
 def test_no_silent_replacement_of_printed_d16(self):
  x=copy.deepcopy(self.e);x["rows"][4]["printed_literal"]="五分二三六二"
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_no_false_early_original_equivalence(self):
  x=copy.deepcopy(self.e);x["firewall"]["not_ncl03130_original"]=False
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_no_ancient_winner_from_local_progression(self):
  x=copy.deepcopy(self.e);x["firewall"]["ancient_technical_unit"]="少"
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_no_unverified_printed_correction(self):
  x=copy.deepcopy(self.e);x["arithmetic_control"]["candidate_2362_not_original_glyph"]=False
  with self.assertRaises(AssertionError):M.check(x,False)
 def test_no_bad_artifact_source_digest(self):
  x=copy.deepcopy(self.e);x["source"]["source_jpeg_sha256"]="0"*64
  with self.assertRaises(AssertionError):M.check(x,False)
