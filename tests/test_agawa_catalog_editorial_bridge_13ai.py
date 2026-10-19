import importlib.util, unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-agawa-catalog-editorial-bridge-13ai.py"
spec=importlib.util.spec_from_file_location("agawa13ai",p)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class TestAgawaEditorialBridge(unittest.TestCase):
 def test_full_gate(self): self.assertTrue(mod.verify())
 def test_opac_is_not_physical_copy(self):
  e=mod.load(mod.E); self.assertFalse(e["prior_related_bibliographic_work"]["utokyo_separate_physical_copy_proven"])
 def test_supplement_not_direct_copy(self):
  e=mod.load(mod.E);self.assertTrue(e["utokyo_librarian_referral"]["librarian_describes_supplement_to_prior_catalog"])
  self.assertFalse(e["utokyo_librarian_referral"]["exact_entry_by_entry_derivation_proven"])
 def test_no_target_numerical_voting(self):
  e=mod.load(mod.E);self.assertEqual(e["boundaries"]["cross_original_numeric_votes"],0)
  self.assertTrue(all(x["D16_original"] is None for x in e["unrelated_target_holdings"]))
if __name__=="__main__":unittest.main()
