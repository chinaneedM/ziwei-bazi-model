import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("columbia12vu",ROOT/"scripts/verify-yehuobian-columbia-catalog-gate-12vu.py")
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class ColumbiaGate(unittest.TestCase):
 def setUp(self):
  self.r=json.loads((ROOT/v.RECORD).read_text());self.s=json.loads((ROOT/v.SHARD).read_text());self.m=json.loads((ROOT/v.MANIFEST).read_text());self.state=json.loads((ROOT/v.STATE).read_text())
 def bad(self,label):
  with self.assertRaisesRegex(ValueError,label):v.validate(self.r,self.s,self.m,self.state)
 def test_actual_snapshot(self):self.assertEqual(v.verify()["verified_clio_items"],0)
 def test_citation_year_scope(self):self.r["source_claim"]["cited_year"]=1869;self.bad("academic bibliography")
 def test_bibliographic_author_literal_preserved(self):self.r["source_claim"]["cited_author_literal"]="沈德符";self.bad("quotation scope")
 def test_unverified_clio_id(self):self.r["source_claim"]["source_issued_clio_id"]="guess123";self.bad("physical item")
 def test_invented_firstparty_clio(self):self.r["institutional_controls"]["first_party_specific_yehuobian_item_found"]=True;self.bad("invented institutional")
 def test_invented_folio(self):self.r["institutional_controls"]["target_folio"]="卷20第5葉";self.bad("invented firstparty")
 def test_ninth_actionable_candidate_not_authorized(self):self.r["acquisition_classification"]["new_source_issued_physical_item_candidates"]=1;self.bad("nine-item")
 def test_unearned_target_image(self):self.r["acquisition_classification"]["no_original_target_juan20_image"]=False;self.bad("historical evidence")
 def test_no_received_text_glyph_vote(self):self.r["four_locus_gate"]["GONGJIN"]="官禁";self.bad("unattested")
 def test_source_class_cannot_vote(self):self.s["sources"][0]["physical_glyph_authority"]=True;self.bad("bibliography used")
 def test_general_library_route_not_permission(self):self.r["institutional_controls"]["general_repro_request_not_item_eligibility"]=False;self.bad("institutional scope")
 def test_future_registry_growth_allowed(self):
  self.m["combined_source_count"]+=1;self.m["extension_source_count"]+=1;self.state["historical_audit"]["external_source_registry_total_unique_count"]+=1
  self.assertEqual(v.validate(self.r,self.s,self.m,self.state)["status"],"PASS")
 def test_graph_not_promoted(self):self.r["transmission_impact"]["edges_supported"].append("false");self.bad("unproven genealogy")
if __name__=="__main__":unittest.main()
