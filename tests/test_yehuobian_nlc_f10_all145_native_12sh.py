"""12SH bounded archive-source page identity, full chain and no-absence-proof firewall."""
import json,tempfile,unittest
from pathlib import Path
from scripts.verify_yehuobian_nlc_f10_all145_native_12sh import PACK,RECORD,verify
class F10WholeNative12SH(unittest.TestCase):
 def test_valid(self):
  self.assertEqual((verify()["native_source_pages"],verify()["native_body_bounded"]),(1028,1027))
 def mutate(self,fn):
  d=json.loads(RECORD.read_text(encoding="utf-8"));fn(d)
  with tempfile.TemporaryDirectory() as f:
   p=Path(f)/"fake.json";p.write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8")
   with self.assertRaises(ValueError):verify(record_path=p)
 def test_bad_hash_bytes(self):
  with tempfile.TemporaryDirectory() as f:
   p=Path(f)/"bad-pins.txt";data=PACK.read_text(encoding="ascii").strip()
   p.write_text(("A" if data[0]!="A" else "B")+data[1:],encoding="ascii")
   with self.assertRaises(ValueError):verify(pack_path=p)
 def test_page_window_skip(self):
  self.mutate(lambda d:d["review"]["montage_page_windows"].pop())
 def test_archive_identity(self):
  self.mutate(lambda d:d["source"].__setitem__("archived_artifact_id",1))
 def test_fake_target_absence(self):
  self.mutate(lambda d:d["review"].__setitem__("whole_old20_work_target_absence_proven",True))
 def test_fake_target_positive(self):
  self.mutate(lambda d:d["review"].__setitem__("any_original_old20_gaizao_louke_target_folio_positive_attestation",True))
 def test_folio_crosswalk(self):
  self.mutate(lambda d:d["review"].__setitem__("p81_left_leaf_new_volume",20))
 def test_fulltext_authority(self):
  self.mutate(lambda d:d["review"].__setitem__("fulltext_line_by_line_collated",True))
 def test_double_count(self):
  self.mutate(lambda d:d["grade_union"].__setitem__("global_native_source_pages_after",1030))
if __name__=="__main__":unittest.main()
