"""Contemporary reproduction services must not be mistaken for early original prints or glyphs."""
import importlib.util
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/MING-DATONG-YEHUOBIAN-12UI-TSUKUBA-NDL-ACQUISITION-MODE-GATES-R1.json"
S="docs/research/MING-DATONG-YEHUOBIAN-12UI-INSTITUTIONAL-ACCESS-SOURCE-SHARD-R1.json"
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
class AcquisitionGate12UI(unittest.TestCase):
 def test_two_material_specific_routes_are_fail_closed(self):
  e=read(E);ts,ndl=e["objects"]; self.assertEqual(ts["item"],"10076865665"); self.assertEqual(ndl["call_number"],"184-65")
  self.assertEqual(e["gates"]["new_ancient_print_target_images"],0); self.assertEqual(e["gates"]["new_independent_glyph_votes"],0)
  self.assertEqual(e["gates"]["requests_sent"],0);self.assertEqual(e["gates"]["forms_submitted"],0);self.assertEqual(e["gates"]["paid_services_purchased"],0)
  self.assertFalse(ts["original_juan20_image_received"]);self.assertFalse(ndl["original_juan20_image_received"])
  self.assertEqual(ts["exact_item_microfilm_status"],"NOT_VERIFIED");self.assertEqual(ts["exact_item_digitization_status"],"NOT_VERIFIED")
  self.assertFalse(ts["official_rules"][0]["specific_item_estimate_obtained"])
  self.assertIs(ts["official_rules"][0]["cut_count_for_item_known"],False)
  self.assertIn("full-page",ts["official_rules"][0]["observations"][0]);self.assertTrue(e["study_only_copy_is_not_physical_print_proof"])
 def test_policy_sources_not_ancient_glyph_authority(self):
  s=read(S)["sources"]; self.assertEqual(len(s),2)
  self.assertTrue(all(x["physical_glyph_authority"] is False and x["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" and x["evidence"]==E for x in s))
  self.assertEqual({x["url"] for x in s},{"https://www.tulips.tsukuba.ac.jp/lib/ja/visitor/waso","https://ndlsearch.ndl.go.jp/en/help/remotecopy"})
  self.assertEqual(read(E)["accounting"]["source_count_after"],683)
 def test_registry_state_and_prior_12uh_still_exist(self):
  s=importlib.util.spec_from_file_location("reg",ROOT/"scripts/verify-historical-source-registry-extensions-r1.py");mod=importlib.util.module_from_spec(s);s.loader.exec_module(mod)
  v=mod.verify(ROOT); state=read("docs/PROJECT-CURRENT-STATE-R1.json")["historical_audit"]
  self.assertEqual(v["combined_source_count"],683); self.assertEqual(v["combined_source_count"],state["external_source_registry_total_unique_count"])
  self.assertEqual(v["extension_source_count"],36);self.assertEqual(v["extension_source_count"],state["external_source_registry_extension_count"])
  self.assertTrue(any(x.startswith("12UI ") for x in state["current_focus"]))
  old=read("docs/research/MING-DATONG-YEHUOBIAN-12UH-NDL1700-TSUKUBA-UNBOUND-PRINT-CATALOG-R1.json")
  self.assertEqual(old["source_gate"]["new_independent_ancient_target_glyph_votes"],0)
if __name__=="__main__":unittest.main()
