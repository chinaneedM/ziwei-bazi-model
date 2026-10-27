"""12SG verify whole F9 source-JPEG chain, exact page 84 and fail-closed evidence grades."""
import json,tempfile,unittest
from pathlib import Path
from scripts.verify_yehuobian_nlc_f9_all141_native_12sg import RECORD,verify
class F9All141Native12SG(unittest.TestCase):
 def test_pass(self):
  self.assertEqual((verify()["f9_original_native_pages"],verify()["global_native_source_pages"]),(141,892))
 def corrupt(self,fn):
  d=json.loads(RECORD.read_text(encoding="utf-8"))
  fn(d)
  with tempfile.TemporaryDirectory() as root:
   p=Path(root)/"changed.json";p.write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8")
   with self.assertRaises(ValueError):verify(p)
 def test_source_page_changed(self):
  self.corrupt(lambda d:d["review"]["source_jpeg_sha256_by_pdf_page_81_141"].__setitem__(3,"0"*64))
 def test_source_page_reorder(self):
  self.corrupt(lambda d:d["review"]["source_jpeg_sha256_by_pdf_page_81_141"].reverse())
 def test_false_target_absence(self):
  self.corrupt(lambda d:d["review"].__setitem__("whole_old20_target_absence_proven",True))
 def test_false_target_positive(self):
  self.corrupt(lambda d:d["review"].__setitem__("positive_old20_gaizao_louke_original_target_folio_attested",True))
 def test_cross_leaf_falsification(self):
  self.corrupt(lambda d:d["review"].__setitem__("p84_right_leaf_original_volume",17))
 def test_montage_skip(self):
  self.corrupt(lambda d:d["review"]["montage_windows"].pop())
 def test_duplicate_physical_witness(self):
  self.corrupt(lambda d:d["grade_union"].__setitem__("independent_physical_witness_increment",1))
 def test_archive_identity(self):
  self.corrupt(lambda d:d["source"].__setitem__("artifact_zip_sha256","0"*64))
if __name__=="__main__":unittest.main()
