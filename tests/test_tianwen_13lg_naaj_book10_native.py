import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13lg-naaj-book10-native.py"
spec=importlib.util.spec_from_file_location("tw13lg",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class OriginalBook10(unittest.TestCase):
 def setUp(self):self.a=copy.deepcopy(list(v.load()))
 def bad(self):
  with self.assertRaises(AssertionError):v.check(*self.a)
 def test_base(self):self.assertEqual(v.check(*self.a)["confirmed_numeric_original"],"238977.09")
 def test_false_numeral(self):self.a[0]["page_collation"][1]["original_printed_text"]="有閏加二十八萬八九七七○九";self.bad()
 def test_fake_glyph_hash(self):self.a[0]["page_collation"][1]["roi_rgb_sha256"]="0"*64;self.bad()
 def test_false_print_year(self):self.a[0]["archive"]["exact_1739_physical_impression_proved"]=True;self.bad()
 def test_fake_independent_recension(self):self.a[0]["comparison"]["historical_independent_textual_recensions_added"]=1;self.bad()
 def test_restore_legacy_archive(self):self.a[2]["issues"][4]["next_action"]="13LG CURRENT ACTION: no history";self.bad()
 def test_future_focus(self):
  self.a[1]["historical_audit"]["current_focus"].append("13LH future")
  self.a[2]["binding"]["source_focus_count"]+=1;self.a[2]["binding"]["latest_research_focus_prefix"]="13LH"
  self.assertEqual(v.check(*self.a)["status"],"PASS")
if __name__=="__main__":unittest.main()
