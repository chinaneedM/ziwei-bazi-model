import importlib.util, unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-agawa-old-catalog-nanki-g23-control-13ah.py"
spec=importlib.util.spec_from_file_location("ag13ah",p)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class TestAgawaArchiveCounterexample(unittest.TestCase):
 def test_registry_gate(self):self.assertTrue(mod.verify())
 def test_Nanki_stamp_cannot_promote_other_G23(self):
  e=mod.load(mod.E);self.assertFalse(e["utokyo_g23_nanki_control"]["prefix_proves_either_target_ownership"])
  self.assertTrue(all(x["Agawa_provenance"]=="UNVERIFIED" for x in e["target_work52_items"]))
 def test_kyushu_same_copy_as_CiNii(self):
  e=mod.load(mod.E);self.assertTrue(e["kyushu_firstparty"]["same_item_as_CiNii_record"])
  self.assertFalse(e["kyushu_firstparty"]["digitized_fulltext_claim"])
 def test_no_historical_numerical_witness(self):
  self.assertEqual(mod.load(mod.E)["comparison"]["new_historical_numeric_votes"],0)
if __name__=="__main__":unittest.main()
