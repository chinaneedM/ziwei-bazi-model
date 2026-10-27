import importlib.util, unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-cadal-source-recovery-12zb.py"
s=importlib.util.spec_from_file_location("tianwen12zb",p)
v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class RegisteredGoryeosaOriginalRecovery(unittest.TestCase):
 def setUp(self):self.x=list(v.load())
 def bad(self):
  with self.assertRaises(ValueError):v.verify(*self.x)
 def test_valid(self):self.assertEqual(v.verify(*self.x)["historical_witnesses_added"],0)
 def test_do_not_substitute_page(self):self.x[0]["previous_source"]["scan_page"]=40;self.bad()
 def test_do_not_promote_historical_year(self):self.x[1]["copy_level_date_status"]="1451_PRINT_PROVEN";self.bad()
 def test_do_not_invent_source_vote(self):self.x[0]["classification"]["independent_stemmatic_original_voting_granted"]=1;self.bad()
 def test_do_not_guess_nikh_copy(self):self.x[0]["official_image_route"]["exact_nikh_d16_link_bound_to_specific_book_code"]=True;self.bad()
 def test_do_not_conflate_missing_leaf_with_available_scan(self):self.x[0]["official_image_route"]["catalog_candidates"][0]["exact_target_folio_not_read"]=False;self.bad()
 def test_do_not_silently_change_source_glpyh(self):self.x[1]["controls"][0]["direct_surface"]="五分二三六二";self.bad()
 def test_do_not_undo_12za(self):self.x[3]["new_hanja_literal_candidate"]["decimal_lexical_five_place"]="8424.6408";self.bad()
 def test_forward_foci(self):
  self.x[4]["historical_audit"]["current_focus"].append("12ZC future")
  self.x[5]["binding"]["source_focus_count"]+=1
  self.x[5]["binding"]["latest_research_focus_prefix"]="12ZC"
  self.assertEqual(v.verify(*self.x)["status"],"PASS")
if __name__=="__main__":unittest.main()
