import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-utokyo-goryeosa-acquisition-13am.py"
s=importlib.util.spec_from_file_location("g13am",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class TestInquiries(unittest.TestCase):
 def test_integrity(self):self.assertTrue(m.verify())
 def test_no_submission_or_micro_export(self):
  x=m.load(m.E)
  self.assertFalse(x["provider_route"]["actual_submission"])
  self.assertFalse(x["provider_route"]["micro_can_export_USB"])
  self.assertEqual(x["counts"]["omissions_open"],11)
if __name__=="__main__":unittest.main()
