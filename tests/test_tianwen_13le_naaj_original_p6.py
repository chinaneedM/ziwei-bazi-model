import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13le-naaj-original-p6.py"
sp=importlib.util.spec_from_file_location("tw13le",p);v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class OriginalPrint(unittest.TestCase):
 def setUp(self):self.a=copy.deepcopy(list(v.load()))
 def failcheck(self):
  with self.assertRaises(ValueError):v.check(*self.a)
 def test_base(self):self.assertEqual(v.check(*self.a)["original_naaj_2810038_pdf_page6"],"238977.09")
 def test_counterfeit_numeral(self):self.a[0]["page_collation"][0]["original_native_printed_reading"]="有閏加二十八萬八九七七○九";self.failcheck()
 def test_hijacked_roi_hash(self):self.a[0]["page_collation"][0]["roi_rgb_sha256"]="0"*64;self.failcheck()
 def test_invented_print_date(self):self.a[0]["archive_holding"]["physical_1739_impression_directly_verified"]=True;self.failcheck()
 def test_invented_independent_recension(self):self.a[0]["comparison"]["independent_textual_recension_votes_new"]=1;self.failcheck()
 def test_wrong_operator(self):self.a[0]["page_collation"][1]["original_native_printed_reading"]="推遲疾限各置遲疾歷";self.failcheck()
 def test_forward_13lf(self):
  self.a[1]["historical_audit"]["current_focus"].append("13LF later physical copy source route")
  self.a[2]["binding"]["source_focus_count"]+=1
  self.a[2]["binding"]["latest_research_focus_prefix"]="13LF"
  next(i for i in self.a[2]["issues"] if i["id"]=="TW-OPEN-0005")["next_action"]="13LF CURRENT ACTION: later evidence"
  self.assertEqual(v.check(*self.a)["status"],"PASS")
if __name__=="__main__":unittest.main()
