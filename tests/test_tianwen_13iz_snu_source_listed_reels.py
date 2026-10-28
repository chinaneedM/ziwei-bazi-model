import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"probe-tianwen-13iz-snu-source-listed-reels.py"
s=importlib.util.spec_from_file_location("v13iz",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class PublicProvider(unittest.TestCase):
 def test_explicit_source_button(self):
  x=v.summarize("GK05553_00",b"fn_mfPdfPopShow('GK05553_00') M/F74-102-17-4(GK5553/v25-31)")
  self.assertTrue(x["exact_provider_microfilm_button"])
  self.assertFalse(x["physical_book29_original_folio_proven"])
 def test_wrong_book_button(self):self.assertFalse(v.summarize("GK05553_00",b"fn_mfPdfPopShow('GK05554_00')")["exact_provider_microfilm_button"])
 def test_reel_label_not_leaf(self):
  x=v.summarize("GK05553_00",b"M/F74-102-17-4(GK5553/v25-31)")
  self.assertFalse(x["physical_book12_original_folio_proven"]);self.assertFalse(x["physical_book29_original_folio_proven"])
 def test_json_source_bound(self):
  b=b'{"RESULT":"SUCCESS","volList":[{"BOOK_CD":"GK05553_00","VOL_NO":"0001","IS_PDF":"Y"}]}'
  self.assertEqual(v.parse_volumes(b,"GK05553_00")["status"],"PROVIDER_LIST_BOUND")
 def test_wrong_book_rejected(self):
  b=b'{"RESULT":"SUCCESS","volList":[{"BOOK_CD":"GK05554_00","VOL_NO":"0001"}]}'
  self.assertEqual(v.parse_volumes(b,"GK05553_00")["status"],"UNTRUSTED_OR_MIXED_OBJECT")
 def test_reject_html(self):self.assertEqual(v.parse_volumes(b"<html>error</html>","GK05553_00")["status"],"NON_JSON")
 def test_empty_list_no_folio(self):
  self.assertEqual(v.parse_volumes(b'{"RESULT":"ERROR","volList":[]}',"GK05553_00")["volList_count"],0)
 def test_no_inferred_juan(self):
  x=v.parse_volumes(b'{"RESULT":"SUCCESS","volList":[{"BOOK_CD":"GK05553_00","VOL_NO":"0029"}]}',"GK05553_00")
  self.assertTrue(x["no_folio_to_reel_crosswalk"])
if __name__=="__main__":unittest.main()
