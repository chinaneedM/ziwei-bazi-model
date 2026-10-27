import importlib.util,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("gx",R/"scripts/verify-tianwen-13gx-null-identity-erratum.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class UnknownIdentity(unittest.TestCase):
 def setUp(self):self.e=json.loads(m.E.read_text(encoding="utf8"))
 def test_source_preserving_null_overlay(self):self.assertTrue(m.check(self.e))
 def test_false_is_not_disproof(self):
  self.e["correction"]["effective_fourfen_chudu_mechanical_identity"]=False
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_true_is_not_proof(self):
  self.e["correction"]["effective_fourfen_chudu_mechanical_identity"]=True
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_nonedge_requires_evidence(self):
  self.e["correction"]["proven_non_edge"]=True
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_old_history_cannot_be_rewritten(self):
  self.e["source_snapshot"]["git_blob_sha"]="0"*40
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_unit_cannot_be_activated(self):
  self.e["correction"]["effective_fourfen_chudu_ancient_unit_identity"]="同一秒"
  with self.assertRaises(AssertionError):m.check(self.e)
if __name__=="__main__":unittest.main()
