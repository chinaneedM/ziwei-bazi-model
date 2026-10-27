"""12TH TELDAP source corroborates catalog identity, not a second ancient witness."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))

class TeldapIdentity12TH(unittest.TestCase):
    def test_scope_and_physical_witness_limit(self):
        record=read("docs/research/MING-DATONG-YEHUOBIAN-12TH-TELDAP-NCL02260-INSTITUTIONAL-CROSSCHECK-R1.json")
        shard=read("docs/research/MING-DATONG-YEHUOBIAN-12TH-TELDAP-NCL02260-SOURCE-SHARD-R1.json")
        self.assertEqual(len(shard["sources"]),1)
        src=shard["sources"][0]
        self.assertEqual(src["verification_status"],"BIBLIOGRAPHIC_METADATA_ONLY")
        self.assertIs(src["physical_glyph_authority"],False)
        self.assertEqual(src["source_id"],record["source_identity"]["new_source_id"])
        self.assertEqual(record["institutional_catalog"]["book_number"],"02260")
        self.assertEqual(record["institutional_catalog"]["physical_fascicles"],16)
        self.assertEqual(record["neighboring_object"]["book_number"],"02261")
        self.assertIs(record["neighboring_object"]["same_physical_copy_as_02260"],False)
        self.assertIs(record["institutional_catalog"]["original_data_target_is_item_specific"],False)
        self.assertEqual(record["source_identity"]["new_independent_ancient_copy_count"],0)
        self.assertIs(record["adjudication"]["tel_dap_independently_proves_zhou_original_seal_glyphs"],False)
        self.assertIs(record["adjudication"]["tel_dap_entry_collates_kaizao_louke_original_folio"],False)
        self.assertIs(record["adjudication"]["tel_dap_and_commons_are_independent_physical_copies"],False)
        self.assertEqual(record["adjudication"]["new_unrepaired_1827_physical_target_votes"],0)
        self.assertEqual(record["adjudication"]["new_repaired_1869_physical_target_votes"],0)
        self.assertFalse(record["adjudication"]["algorithm_reopen"])
        self.assertEqual(record["transmission_impact"]["edges_supported"],[])

    def test_live_registry_and_project_invariants(self):
        record=read("docs/research/MING-DATONG-YEHUOBIAN-12TH-TELDAP-NCL02260-INSTITUTIONAL-CROSSCHECK-R1.json")
        manifest=read("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
        state=read("docs/PROJECT-CURRENT-STATE-R1.json")
        self.assertEqual(len([x for x in manifest["shards"] if x["path"]=="docs/research/MING-DATONG-YEHUOBIAN-12TH-TELDAP-NCL02260-SOURCE-SHARD-R1.json"]),1)
        self.assertGreaterEqual(manifest["combined_source_count"],662)
        self.assertEqual(manifest["extension_source_count"],sum(x["source_count"] for x in manifest["shards"]))
        self.assertEqual(manifest["combined_source_count"],manifest["root_source_count"]+manifest["extension_source_count"])
        self.assertEqual(state["historical_audit"]["external_source_registry_total_unique_count"],manifest["combined_source_count"])
        self.assertEqual(record["source_identity"]["new_catalog_source_count"],1)
        self.assertTrue(any(x.startswith("12TH NCL02260 INSTITUTIONAL") for x in state["historical_audit"]["current_focus"]))
        self.assertEqual(state["invariants"]["algorithm_reopen_count"],0)
        self.assertEqual(state["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")

if __name__ == "__main__":
    unittest.main()
