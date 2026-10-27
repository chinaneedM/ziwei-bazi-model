"""12RU F5 first20 source SHA pins and scoped evidence tests."""
import copy,importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location("tw12ru",ROOT/"scripts/verify_yehuobian_nlc_f5_p1_20_native_12ru.py")
G=importlib.util.module_from_spec(S);S.loader.exec_module(G)
class TestNlcF5First20(unittest.TestCase):
 def fake(self,fn):
  x=copy.deepcopy(G.read(G.RECORD));fn(x)
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"record.json";p.write_text(json.dumps(x,ensure_ascii=False),encoding="utf-8")
   with self.assertRaisesRegex(ValueError,"12RU_"):G.verify(record_path=p)
 def test_real_original_source(self):
  r=G.verify();self.assertEqual(r["f5_native_bounded"],"20/63")
  self.assertEqual(r["f5_remaining"],43)
  self.assertFalse(r["original_target_presence_or_absence_proven"])
 def test_sha_mutation(self):self.fake(lambda x:x["review"]["image_pins"].__setitem__(1,"0"*64))
 def test_wrong_juan_heading(self):self.fake(lambda x:x["review"].__setitem__("first_page_juan_heading","卷九"))
 def test_false_absence(self):self.fake(lambda x:x["review"].__setitem__("whole_work_target_absence_proven",True))
 def test_false_fulltext(self):self.fake(lambda x:x["review"].__setitem__("fulltext_linewise_collated",True))
 def test_no_extra_copy(self):self.fake(lambda x:x["review"].__setitem__("physical_copy_increment",1))
 def test_global_count(self):self.fake(lambda x:x["queue"].__setitem__("old_global_native_count",400))
 def test_parent_distinction(self):self.fake(lambda x:x.__setitem__("parent_open_batch","12QE_OPEN"))
if __name__=="__main__":unittest.main()
