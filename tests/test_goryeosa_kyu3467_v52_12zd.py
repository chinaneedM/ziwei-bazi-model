import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-kyu3467-v52-12zd.py"
s=importlib.util.spec_from_file_location("tw12zd",p)
v=importlib.util.module_from_spec(s)
s.loader.exec_module(v)
class Goryeosa3467Scope(unittest.TestCase):
 def setUp(self): self.x=list(v.load())
 def bad(self):
  with self.assertRaises(ValueError): v.verify(*self.x)
 def test_valid(self): self.assertEqual(v.verify(*self.x)["new_original_folios"],0)
 def test_do_not_date_print_from_1451(self): self.x[0]["new_leads"][0]["print_year"]=1451;self.bad()
 def test_do_not_phantom_folio(self): self.x[0]["new_leads"][0]["original_target_folio_bound"]=True;self.bad()
 def test_exact_book_volume_link(self): self.x[0]["new_leads"][0]["work_volume"]=53;self.bad()
 def test_5553_replaced_volume_map(self): self.x[0]["new_leads"][1]["known_manuscript_replacements"][0]["work_volumes"]=[19,20,52];self.bad()
 def test_5553_local_repair_not_excluded(self): self.x[0]["new_leads"][1]["unknown_local_repair_possible"]=False;self.bad()
 def test_5553_target_not_yet_printed_glyph(self): self.x[0]["new_leads"][1]["printed_target_glyph_bound"]=True;self.bad()
 def test_mf_not_work_vol_mapping(self): self.x[0]["new_leads"][2]["target_microfilm_group_identified"]=True;self.bad()
 def test_3467_split_unknown(self): self.x[0]["digital_catalog_scope"]["exact_match_of_fascicle_6_to_split_catalog_item"]="奎3467의2";self.bad()
 def test_no_research_closed(self): self.x[3]["issues"][4]["status"]="RESOLVED_WITH_EVIDENCE";self.bad()
 def test_no_phantom_source(self): self.x[0]["risk_controls"]["source_witness_count_new"]=1;self.bad()
 def test_preserve_reviewed_version(self): self.x[3]["binding"]["reviewed_state_version"]="1.641.0";self.bad()
if __name__=="__main__":unittest.main()
