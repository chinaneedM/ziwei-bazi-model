"""12TE scholarly-source scope must not impersonate a physical-glyph witness."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))
class YehuobianSecondaryProvenance12TE(unittest.TestCase):
    def test_scholarly_status_and_no_target_votes(self):
        shard=read("docs/research/MING-DATONG-YEHUOBIAN-12TE-MING-PRINT-SCHOLARLY-SOURCE-SHARD-R1.json")
        record=read("docs/research/MING-DATONG-YEHUOBIAN-12TE-MING-PRINT-MISATTRIBUTION-SECONDARY-SCHOLARSHIP-R1.json")
        self.assertEqual(shard["schema"],"MING-DATONG-YEHUOBIAN-12TE-MING-PRINT-SCHOLARLY-SOURCE-SHARD-R1")
        self.assertEqual(len(shard["sources"]),1)
        src=shard["sources"][0]
        self.assertEqual(src["source_id"],"EXT-PKU-CHINESE-CLASSICS-CULTURE-DU2019-YEHUOBIAN-MING-PRINT-QUESTION")
        self.assertEqual(src["verification_status"],"BIBLIOGRAPHIC_METADATA_ONLY")
        self.assertIs(src["physical_glyph_authority"],False)
        adjud=record["adjudication"]
        for key in ("physical_ming_print_existence_negatively_proven","claimed_zhou_manuscript_identity_physically_rechecked","shen_1619_original_target_text_collated","early_manuscript_has_kaizao_louke_target_proven","cadal_xuxiu_photo_identity_resolved","rule_mechanical_source_binding_changed"):
            self.assertIs(adjud[key],False)
        self.assertEqual(adjud["scoped_1827_unrepaired_target_page_votes_added"],0)
        self.assertEqual(adjud["scoped_1869_repair_target_page_votes_added"],0)
        self.assertEqual(record["transmission_impact"]["edges_supported"],[])
    def test_forward_shard_manifest_and_product_invariants(self):
        shard=read("docs/research/MING-DATONG-YEHUOBIAN-12TE-MING-PRINT-SCHOLARLY-SOURCE-SHARD-R1.json")
        manifest=read("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
        state=read("docs/PROJECT-CURRENT-STATE-R1.json")
        self.assertEqual(len([x for x in manifest["shards"] if x["path"]=="docs/research/MING-DATONG-YEHUOBIAN-12TE-MING-PRINT-SCHOLARLY-SOURCE-SHARD-R1.json"]),1)
        self.assertGreaterEqual(manifest["combined_source_count"],661)
        self.assertEqual(manifest["combined_source_count"],manifest["root_source_count"]+manifest["extension_source_count"])
        self.assertEqual(manifest["extension_source_count"],sum(x["source_count"] for x in manifest["shards"]))
        self.assertEqual(state["historical_audit"]["external_source_registry_total_unique_count"],manifest["combined_source_count"])
        self.assertEqual(state["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
        self.assertEqual(state["invariants"]["algorithm_reopen_count"],0)
        self.assertTrue(any(x.startswith("12TE SCHOLARLY MING-PRINT") for x in state["historical_audit"]["current_focus"]))
if __name__=="__main__":
    unittest.main()
