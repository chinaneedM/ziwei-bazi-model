import importlib.util, unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-agawa-digital-work-identity-13aj.py"
spec=importlib.util.spec_from_file_location("ag13aj",p)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class TestAgawaDigitalIdentity(unittest.TestCase):
 def test_full(self):self.assertTrue(mod.verify())
 def test_no_negative_holding_proof(self):
  c=mod.load(mod.E)["collection"];self.assertFalse(c["negative_catalog_inference_authorized"])
 def test_preface_is_not_print_date(self):
  c=mod.load(mod.E)["controlled_item"];self.assertFalse(c["edition_date_from_preface_proven"])
 def test_snapshot_count_gates_only_lower_bound(self):
  m=mod.load(mod.M);e=mod.load(mod.E)
  self.assertGreaterEqual(m["combined_source_count"],e["comparison"]["registry_total_after"])
 def test_no_title_similarity_numeric_voting(self):
  x=mod.load(mod.E);self.assertFalse(x["controlled_item"]["source_item_original_Goryeosa_vol52"])
  self.assertEqual(x["comparison"]["independent_numeric_votes_added"],0)
if __name__=="__main__":unittest.main()
