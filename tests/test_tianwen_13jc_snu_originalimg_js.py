import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"probe-tianwen-13jc-snu-booksearch-originalimg.py"
spec=importlib.util.spec_from_file_location("t13jc",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class BoundJS(unittest.TestCase):
 def test_exact_source_uri(self):self.assertEqual(v.URL,"https://kyudb.snu.ac.kr/js/book/bookSearch.js")
 def test_positive_function_signature(self):
  a=v.inspect(b"function fn_originalImg(item_cd, book_cd, vol_no, page_no) { return 1; }")
  self.assertEqual(a["function_signature"],"function fn_originalImg(item_cd, book_cd, vol_no, page_no)")
  self.assertFalse(a["printed_folio_content_acquired"])
 def test_no_function_in_comments(self):
  a=v.inspect(b"// not a defined function but fn_originalImg is mentioned")
  self.assertFalse(a["function_definition_observed"])
 def test_no_fake_photo_from_script(self):self.assertEqual(v.inspect(b"imgViewer")["new_physical_witness_votes"],0)
 def test_sha_replay(self):
  import hashlib
  b=b"function fn_originalImg(x){}"
  self.assertEqual(v.inspect(b)["sha256"],hashlib.sha256(b).hexdigest())
if __name__=="__main__":unittest.main()
