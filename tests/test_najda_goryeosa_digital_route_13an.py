import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-najda-goryeosa-digital-route-13an.py"
spec=importlib.util.spec_from_file_location("t13an",p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class TestNAJDA(unittest.TestCase):
 def test_replay(self): self.assertTrue(module.verify())
 def test_book_vs_work(self):
  a=module.load(module.E)["na_japan_holding"]
  self.assertEqual(a["child_book_order"],"0052")
  self.assertEqual(a["work_volume_52_mapping"],"UNKNOWN")
  self.assertIsNone(a["target_work_volume_in_book_0052"])
  self.assertFalse(a["target_work_volume_in_book_0052_proven"])
 def test_plan_not_scan(self):
  a=module.load(module.E)["independent_witness_status"]
  self.assertNotEqual(a["digitization_completed_by_2022"],"YES")
  self.assertIsNone(a["D16_original_glyph"])
if __name__=="__main__":unittest.main()
