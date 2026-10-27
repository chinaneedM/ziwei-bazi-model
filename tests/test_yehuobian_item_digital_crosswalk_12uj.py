"""A general library service / digital platform URL is not an item-bound original folio."""
import importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/MING-DATONG-YEHUOBIAN-12UJ-ITEM-DIGITAL-CROSSWALK-PUBLIC-SURFACE-BOUNDARY-R1.json"
S="docs/research/MING-DATONG-YEHUOBIAN-12UJ-ITEM-DIGITAL-CROSSWALK-SOURCE-SHARD-R1.json"
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
class ItemDigitalCrosswalk12UJ(unittest.TestCase):
 def test_public_surfaces_are_not_target_iiif(self):
  e=read(E); ndl,ts=e["exact_item_surfaces"]
  self.assertEqual(ndl["item_bib_id"],"000007607208")
  self.assertEqual(ndl["call_number"],"184-65")
  self.assertIsNone(ndl["observed_public_item_bound_pid"])
  self.assertTrue(ndl["generic_bottom_access_help_present"])
  self.assertFalse(ndl["generic_help_is_item_digitization_proof"])
  self.assertEqual(ndl["item_digitization_status"],"NOT_DETERMINED_FROM_RENDERED_RECORD")
  self.assertEqual(ts["target_item_id"],"10076865665")
  self.assertEqual(ts["observed_opac_result"],"SEARCH_SHELL_ONLY_NO_ITEM_SPECIFIC_DETAIL_IN_RETRIEVED_TEXT")
  self.assertFalse(ts["digital_platform_is_item_attestation"])
  self.assertEqual(ts["item_digitization_status"],"NOT_DETERMINED")
  self.assertTrue(all(v["public_digital_fingerprint_glyphs"] is None for v in e["exact_item_surfaces"]))
 def test_no_impression_or_glyph_leak(self):
  e=read(E);g=e["print_glyph_gate"]
  self.assertTrue(g["old_12uf_4_loci_unchanged"])
  self.assertFalse(g["early_print_original_seen"])
  self.assertFalse(g["original_juan20_leaf_seen"])
  self.assertEqual(g["new_ancient_glyph_votes"],0)
  self.assertTrue(g["guessed_pid_prohibited"] and g["guessed_iiif_id_prohibited"])
  self.assertEqual([g["external_messages_sent"],g["copies_requested"],g["paid_services_used"],g["chart_algorithms_reopened"]],[0,0,0,0])
  self.assertEqual(e["general_provider_rules"]["ndl_rare_material_advance_notice_applies_if_item_in_rare_category"],"PRECONDITION_NOT_CLASSIFIED_FOR_18465")
 def test_source_registry_state_and_prior_record(self):
  s=read(S)["sources"]
  self.assertEqual(len(s),3)
  self.assertTrue(all(x["physical_glyph_authority"] is False and x["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" and x["evidence"]==E for x in s))
  spec=importlib.util.spec_from_file_location("source_registry_12uj",ROOT/"scripts/verify-historical-source-registry-extensions-r1.py")
  mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
  v=mod.verify(ROOT); a=read("docs/PROJECT-CURRENT-STATE-R1.json")["historical_audit"]
  self.assertEqual(v["combined_source_count"],a["external_source_registry_total_unique_count"])
  self.assertEqual(v["extension_source_count"],a["external_source_registry_extension_count"])
  self.assertGreaterEqual(v["combined_source_count"],read(E)["accounting"]["sources_after"])
  self.assertTrue(any(x.startswith("12UJ ") for x in a["current_focus"]))
  self.assertEqual(read("docs/research/MING-DATONG-YEHUOBIAN-12UI-TSUKUBA-NDL-ACQUISITION-MODE-GATES-R1.json")["gates"]["new_independent_glyph_votes"],0)
if __name__=="__main__":unittest.main()
