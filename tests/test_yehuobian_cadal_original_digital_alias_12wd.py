import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("wd",ROOT/"scripts/verify-yehuobian-cadal-original-digital-alias-12wd.py")
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class OriginalBinaryScope(unittest.TestCase):
 def setUp(self):
  self.r=json.loads((ROOT/v.REC).read_text())
  self.s=json.loads((ROOT/v.STATE).read_text())
  self.y=(ROOT/v.WF).read_text()
 def bad(self,msg):
  with self.assertRaisesRegex(ValueError,msg):v.validate(self.r,self.s,self.y)
 def test_actual_capture_receipt(self):self.assertEqual(v.verify()["physical_historical_votes"],0)
 def test_original_digest_rejected_if_changed(self):
  self.r["sources"][0]["sha256"]="0"*64;self.bad("old source SHA")
 def test_nonexact_pixels_not_equal(self):
  self.r["image_pages"][0]["exact_grayscale_pixel_identity"]=True;self.bad("no pixel identity")
 def test_not_two_old_print_votes(self):
  self.r["scope"]["new_independent_ancient_print_votes"]=2;self.bad("no historical votes")
 def test_official_source_not_physically_bound(self):
  self.r["scope"]["paper_copy_identity"]="KNOWN";self.bad("physical provenance")
 def test_capture_requires_manual_trigger(self):
  self.y=self.y.replace("if: github.event_name == 'workflow_dispatch'","if: always()");self.bad("manual only expensive capture")
 def test_zip_not_independently_rehashed(self):
  self.r["receipt"]["zip_independently_rehashed"]=True;self.bad("zip SHA reporting scope")
if __name__=="__main__":unittest.main()
