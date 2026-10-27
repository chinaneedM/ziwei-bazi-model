import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"acquire-nlc-goryeosa-group40-13q.py"
s=importlib.util.spec_from_file_location("source13q",p);a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
class OriginalSourceBoundary13Q(unittest.TestCase):
 def test_anchor(self):a.check(a.entry())
 def test_no_fabricated_glyph(self):
  e=copy.deepcopy(a.entry());e["d16_original_glyph"]="五分二三六二"
  with self.assertRaises(AssertionError):a.check(e)
 def test_no_false_early_capture(self):
  e=copy.deepcopy(a.entry());e["source_binary_downloaded_at_checkpoint"]=True
  with self.assertRaises(AssertionError):a.check(e)
 def test_no_copy_multiplication(self):
  e=copy.deepcopy(a.entry());e["adjacent_commons_upload_pages"][0]["independent_numeric_vote"]=True
  with self.assertRaises(AssertionError):a.check(e)
if __name__=="__main__":unittest.main()
