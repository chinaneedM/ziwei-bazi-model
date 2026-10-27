"""Two bibliographic print leads are NOT two original four-locus glyph witnesses."""
import json
from pathlib import Path
import unittest
import importlib.util
ROOT=Path(__file__).resolve().parents[1]
EVIDENCE="docs/research/MING-DATONG-YEHUOBIAN-12UH-NDL1700-TSUKUBA-UNBOUND-PRINT-CATALOG-R1.json"
SHARD="docs/research/MING-DATONG-YEHUOBIAN-12UH-EARLY-PRINT-CATALOG-SOURCE-SHARD-R1.json"
def load(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))
class PrintCatalogScope12UH(unittest.TestCase):
    def test_catalogues_are_no_physical_glyph_votes(self):
        e=load(EVIDENCE); sources=load(SHARD)["sources"]
        self.assertEqual(len(e["candidates"]),2)
        self.assertEqual(len(sources),2)
        self.assertEqual({x["verification_status"] for x in sources},{"BIBLIOGRAPHIC_METADATA_ONLY"})
        self.assertTrue(all(x["physical_glyph_authority"] is False for x in sources))
        self.assertTrue(all(x["evidence"]==EVIDENCE for x in sources))
        self.assertEqual(e["source_gate"]["new_independent_ancient_target_glyph_votes"],0)
        self.assertEqual(e["source_gate"]["original_source_images_acquired"],0)
        self.assertFalse(e["source_gate"]["edition_date_inferred_from_preface"])
        self.assertFalse(e["source_gate"]["meiji7_ink_note_used_as_original_print_date"])
        self.assertTrue(all(x["target_4_loci"] is None for x in e["candidates"]))
        self.assertEqual(e["candidates"][0]["catalog_imprint_phrase"],"康煕39序活字印")
        self.assertEqual(e["candidates"][1]["physical_item_id_vol20"],"10076865665")
        self.assertFalse(e["source_gate"]["automatic_chart_algorithm_reopen"])
    def test_registry_counts_and_reading_precedence(self):
        spec=importlib.util.spec_from_file_location("source_verifier_12uh",ROOT/"scripts/verify-historical-source-registry-extensions-r1.py")
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        result=m.verify(ROOT)
        state=load("docs/PROJECT-CURRENT-STATE-R1.json")
        self.assertEqual(result["combined_source_count"],state["historical_audit"]["external_source_registry_total_unique_count"])
        self.assertEqual(result["extension_source_count"],state["historical_audit"]["external_source_registry_extension_count"])
        self.assertEqual(load(EVIDENCE)["accounting"]["sources_after"],681)
        self.assertTrue(any(x.startswith("12UH ") for x in state["historical_audit"]["current_focus"]))
        old=load("docs/research/MING-DATONG-YEHUOBIAN-12UF-SOURCE-READING-CONTROL-AND-IMPRESSION-GATES-R1.json")
        self.assertEqual(old["copy_independence"]["distinct_original_printing_states_positively_verified"],0)
        self.assertEqual(len(old["source_surfaces"]),3)
if __name__=="__main__":
    unittest.main()
