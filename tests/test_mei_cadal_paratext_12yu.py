import unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-mei-cadal-paratext-12yu.py"
sp=importlib.util.spec_from_file_location("tianwen_12yu",p);v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class TestBoundedEditionParatext(unittest.TestCase):
 def setUp(self):self.x=list(v.read())
 def rejected(self):
  with self.assertRaises(ValueError):v.verify(*self.x)
 def test_valid(self):self.assertEqual(v.verify(*self.x)["original_read_paratext_pages"],4)
 def test_hash_tamper(self):self.x[0]["source_internal_printed_page_reviews"][1]["original_png_sha256"]="fake";self.rejected()
 def test_falsely_certified_imprint(self):self.x[0]["chronology_firewall"]["physical_origination_year"]="1781";self.rejected()
 def test_falsely_certified_pavilion(self):self.x[0]["chronology_firewall"]["name_qinding_siku"]="WENYUANGE_PROVEN";self.rejected()
 def test_full_page_claim(self):self.x[0]["scan_scope"]["entire_book_line_by_line_collated"]=True;self.rejected()
 def test_fake_extra_physical_vote(self):self.x[0]["evidence_impact"]["new_independent_ancient_physical_copy_votes"]=1;self.rejected()
 def test_wrong_title(self):self.x[0]["source_internal_printed_page_reviews"][2]["direct_visible"]="原刻梅文鼎大統歷志";self.rejected()
 def test_frozen_chart(self):self.x[0]["evidence_impact"]["new_algorithm_reopens"]=1;self.rejected()
 def test_unresolved_issue(self):next(i for i in self.x[1]["issues"] if i["id"]=="TW-OPEN-0005")["status"]="RESOLVED";self.rejected()
 def test_future_focus(self):self.x[2]["historical_audit"]["current_focus"].append("12YV FUTURE");self.assertEqual(v.verify(*self.x)["status"],"PASS")
 def test_missing_focus(self):self.x[2]["historical_audit"]["current_focus"]=[x for x in self.x[2]["historical_audit"]["current_focus"] if not x.startswith("12YU ")];self.rejected()
if __name__=="__main__":unittest.main()
