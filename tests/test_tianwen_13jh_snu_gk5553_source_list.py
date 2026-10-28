import hashlib,importlib.util,json,unittest,urllib.error,urllib.request
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/probe-tianwen-13jh-snu-gk5553-source-listed-viewers.py"
spec=importlib.util.spec_from_file_location("t13jh",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class ExactSourceViewer(unittest.TestCase):
 def test_source_identity(self):
  self.assertEqual(v.BOOK,"GK05553_00")
  self.assertEqual(v.TARGET_VOL_TOKENS,("0012","0029"))
 def test_firstparty_exclusive_redirect(self):
  with self.assertRaises(urllib.error.HTTPError):
   v.OfficialOnly().redirect_request(urllib.request.Request(v.CATALOG),None,302,"x",{},"https://wrong.example/api")
 def test_catalog_gate(self):
  self.assertFalse(v.summarize_catalog(b"Other book and faked options")["exact_post_control"])
  self.assertTrue(v.summarize_catalog(b"GK05553_00 fn_mfPdfPopShow('GK05553_00')")["exact_post_control"])
 def test_source_listed_rows_only(self):
  raw=json.dumps({"RESULT":"SUCCESS","volList":[{"BOOK_CD":"GK05553_00","ITEM_CD":"GJB","VOL_NO":"0012"},{"BOOK_CD":"GK05553_00","ITEM_CD":"GJB","VOL_NO":"0029"}]}).encode()
  obj=v.parse_vols(raw)
  self.assertEqual(v.source_listed_targets(obj),["0012","0029"])
 def test_mismatched_copy_blocks_navigation(self):
  raw=json.dumps({"volList":[{"BOOK_CD":"GK05554_00","ITEM_CD":"GJB","VOL_NO":"0012"}]}).encode()
  obj=v.parse_vols(raw)
  self.assertEqual(obj["status"],"INVALID_OR_MIXED_BOOK_ROWS")
  self.assertEqual(v.source_listed_targets(obj),[])
 def test_unlisted_volume_never_followed(self):
  raw=json.dumps({"volList":[{"BOOK_CD":"GK05553_00","ITEM_CD":"GJB","VOL_NO":"0005"}]}).encode()
  self.assertEqual(v.source_listed_targets(v.parse_vols(raw)),[])
 def test_html_toc_not_ancient_folio(self):
  d=v.analyze_viewer(b"""<div class="bookinfo" data-page_no="001a" data-vol_no="0012" data-call_no="5553"></div>
          fn_originalImg('GJB','GK05553_00','0012','001a')""","0012")
  self.assertEqual(len(d["literal_originalimg_calls"]),1)
  self.assertFalse(d["original_printed_juan_verified"])
  self.assertFalse(d["ancient_original_image_acquired"])
 def test_bounded_network(self):
  self.assertEqual(v.MAX_ATTEMPTS,3)
  self.assertLessEqual(v.MAX_BYTES,2000000)
 def test_invalid_or_missing_json_failclosed(self):
  self.assertEqual(v.source_listed_targets(v.parse_vols(b"<html>blocked")) ,[])
if __name__=="__main__":unittest.main()
