"""12RT fourth digital fascicle original JPEG and dedup consistency."""
import copy, importlib.util, json, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tw12rt",ROOT/"scripts/verify_yehuobian_nlc_f4_p21_56_native_12rt.py")
GATE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)
class TestF4P21To56_12RT(unittest.TestCase):
 def tamper(self,fun):
  d=copy.deepcopy(GATE.read(GATE.RECORD));fun(d)
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"fake.json";p.write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8")
   with self.assertRaisesRegex(ValueError,"12RT_"):GATE.verify(record_path=p)
 def test_real_56_page_scoped_source_union(self):
  r=GATE.verify();self.assertEqual(r["f4_native_firstpass"],"56/56")
  self.assertEqual(r["prior_overlap"],[1,19,27,56])
  self.assertEqual(r["full_body_text_pages_pending"],1027)
  self.assertTrue(r["global_count_deferred"])
 def test_source_pin_mutation(self):self.tamper(lambda d:d["review"]["source_jpeg_shas"].__setitem__(6,"0"*64))
 def test_old_header_invention(self):self.tamper(lambda d:d["review"].__setitem__("new_old_juan9_title_direct_attestation",True))
 def test_false_absence(self):self.tamper(lambda d:d["review"].__setitem__("whole_old20_work_target_absence_proven",True))
 def test_fulltext_inflation(self):self.tamper(lambda d:d["review"].__setitem__("fulltext_collated",True))
 def test_global_count_inflation(self):self.tamper(lambda d:d["queue"].__setitem__("new_global_native_count",395))
 def test_wrong_previous_source_pages(self):self.tamper(lambda d:d["identity_dedup"].__setitem__("previous12qm_source_pages",[1,19,56]))
 def test_wrong_target_parent(self):self.tamper(lambda d:d.__setitem__("parent_open_batch","12QE_OPEN"))
 def test_wrong_manifest_sha(self):self.tamper(lambda d:d["source"].__setitem__("manifest_sha256","0"*64))
if __name__=="__main__":unittest.main()
