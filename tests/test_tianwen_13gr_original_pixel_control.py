import importlib.util,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("gr",R/"scripts/verify-tianwen-13gr-original-pixel-control.py");m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SameImage(unittest.TestCase):
 def setUp(self):self.e=json.loads(m.E.read_text(encoding="utf8"))
 def test_original_pixel_nested_sha(self):self.assertTrue(m.check(self.e))
 def test_false_complete_D14(self):
  self.e["status"]["D14_complete_source_specific_fourfen"]="四分六六三〇"
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_wrong_date_box(self):
  self.e["d14_nested_existing_source_rois"][0]["source_xyxy"][0]+=1
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_previous_positive_control_not_new_witness(self):
  self.e["status"]["new_independent_witnesses"]=1
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_original_source_digest_preserved(self):
  self.e["source"]["pdf_sha256"]="0"*64
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_unarchived_photo_not_claimed_permanent(self):
  self.e["full_three_day_source_context"]["repository_blob_archived"]=True
  with self.assertRaises(AssertionError):m.check(self.e)
if __name__=="__main__":unittest.main()
