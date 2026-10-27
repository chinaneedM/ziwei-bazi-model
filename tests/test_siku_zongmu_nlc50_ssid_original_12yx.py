import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-siku-zongmu-nlc50-ssid-original-12yx.py"
s=importlib.util.spec_from_file_location("siku12yx",p)
v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class OriginalDualRubric(unittest.TestCase):
 def setUp(self):self.a=v.read()
 def reject(self):
  with self.assertRaises(ValueError):v.check(*self.a)
 def test_valid(self):self.assertEqual(v.check(*self.a)["printed_folio_loci"],4)
 def test_no_title_homograph_collapse(self):self.a[0]["direct_original_glyphs"][2]["exact_printed"]="大統歷志十七卷";self.reject()
 def test_wrong_printing_date(self):self.a[0]["source_acquisition"]["scans"][1]["historical_impression_date"]="1739";self.reject()
 def test_wrong_source_hash(self):self.a[0]["source_acquisition"]["scans"][1]["sha256"]="0"*64;self.reject()
 def test_fake_edition_independence(self):self.a[0]["title_variant"]["independently_certified_distinct_historical_physical_impressions"]=True;self.reject()
 def test_false_stemma(self):self.a[0]["title_variant"]["genealogical_copy_direction"]="NLC_FROM_SSID";self.reject()
 def test_wrong_page(self):self.a[0]["direct_original_glyphs"][2]["viewer_page"]=92;self.reject()
 def test_fake_algorithm(self):self.a[0]["evidence_impact"]["algorithm_reopen_count"]=1;self.reject()
 def test_new_future_batch_allowed(self):
  self.a[2]["historical_audit"]["current_focus"].append("12YY future")
  self.a[1]["binding"]["source_focus_count"]+=1
  self.a[1]["binding"]["latest_research_focus_prefix"]="12YY"
  self.assertEqual(v.check(*self.a)["result"],"PASS")
if __name__=="__main__":unittest.main()
