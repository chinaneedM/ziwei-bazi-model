"""13ML retained source scope is forward-only across later handoff versions."""
import copy, importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
mod=ROOT/"scripts/verify-tianwen-13ml-g893-folio-seam.py"
spec=importlib.util.spec_from_file_location("v13ml",mod)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class FolioSeamContinuity(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=json.loads(v.E.read_text(encoding="utf-8"))
  cls.s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf-8"))
  cls.l=json.loads((ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf-8"))
 def test_original_evidence_still_passes(self):
  self.assertTrue(v.verify(self.e,self.s,self.l))
 def test_newer_focus_keeps_13ml_archive(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["historical_audit"]["current_focus"].append("13MM new original witness research")
  l["binding"]["source_focus_count"]+=1
  l["binding"]["latest_research_focus_prefix"]="13MM"
  self.assertTrue(v.verify(self.e,s,l))
 def test_deleted_13ml_focus_fails(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["historical_audit"]["current_focus"]=[x for x in s["historical_audit"]["current_focus"] if not x.startswith("13ML ")]
  l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
  with self.assertRaises(AssertionError):v.verify(self.e,s,l)
 def test_latest_prefix_mismatch_fails(self):
  l=copy.deepcopy(self.l);l["binding"]["latest_research_focus_prefix"]="13MC"
  with self.assertRaises(AssertionError):v.verify(self.e,self.s,l)
 def test_original_checkpoint_must_survive(self):
  l=copy.deepcopy(self.l)
  l["checkpoint_log"]=[x for x in l["checkpoint_log"] if x.get("id")!="OMISSIONS-13ML-G893-ORIGINAL-D9-D19-FOLIO-SEAM-20261031"]
  with self.assertRaises(AssertionError):v.verify(self.e,self.s,l)
 def test_numerical_winner_cannot_be_invented(self):
  e=copy.deepcopy(self.e);e["comparison_gate"]["historical_G893_six_cross_original_winners"]=1
  with self.assertRaises(AssertionError):v.verify(e,self.s,self.l)
if __name__=="__main__":unittest.main()
