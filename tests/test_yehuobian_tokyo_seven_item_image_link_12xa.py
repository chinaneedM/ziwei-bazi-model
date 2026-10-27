import copy,importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("xa",ROOT/"scripts/verify-yehuobian-tokyo-seven-item-image-link-12xa.py")
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class ImageButtonBoundaries(unittest.TestCase):
 def setUp(self):
  self.r=m.jread(m.REC);self.w=m.jread(m.WZ);self.s=m.jread(m.STATE);self.man=m.jread(m.MANIFEST)
 def bad(self,needle):
  with self.assertRaisesRegex(ValueError,needle):m.validate(self.r,self.w,self.s,self.man)
 def test_live_evidence_ledger(self):self.assertEqual(m.verify()["historical_print_glyph_votes"],0)
 def test_fake_print_vote(self):
  self.r["scope"]["new_ancient_print_impression_votes"]=1;self.bad("source promotion")
 def test_missing_original_leaf_false_positive(self):
  self.r["physical_target_controls"]["9927"]["source_original_juan20_folio_obtained"]=True;self.bad("still missing")
 def test_image_button_misattributed_to_1827(self):
  self.r["item_controls"][0]["has_explicit_pdflink_image_control"]=True;self.bad("restricted to 1959")
 def test_1959_control_reassigned_to_1869(self):
  self.r["modern_image_control"]["only_catalog_item_with_visible_image_icon"]="90972";self.bad("modern separate")
 def test_cadal_copy_identity_assumed(self):
  self.r["scope"]["source_metadata_print_date_not_original_folio_print_date_proof"]=False;self.bad("negative proof scope")
 def test_imabori_missing_juan_cannot_prove_20_present(self):
  self.r["physical_target_controls"]["103841"]["juan20_complete_or_available_proven"]=True;self.bad("volume20 unknown")
 def test_modern_link_no_longer_exact_source(self):
  self.r["modern_image_control"]["provider_source_emitted_href"]="javascript:pdflink('/other/juan20.pdf')";self.bad("link exact")
 def test_original_bytes_sha_stable(self):
  self.r["item_controls"][3]["raw_original_html_sha256"]="0"*64;self.bad("identities")
 def test_no_original_image_proven_on_other_sites(self):
  self.r["scope"]["lack_of_button_in_seven_pages_not_proof_no_digitization_elsewhere"]=False;self.bad("negative proof")
 def test_source_registry_not_duplicate_seven_times(self):
  self.r["scope"]["new_registry_source_entries"]=7;self.bad("source promotion")
 def test_no_new_genealogy_edge_from_metadata(self):
  self.r["transmission_impact"]["edges_supported"]=["9927 -> 90972"];self.bad("genealogy promotion")
if __name__=="__main__":unittest.main()
