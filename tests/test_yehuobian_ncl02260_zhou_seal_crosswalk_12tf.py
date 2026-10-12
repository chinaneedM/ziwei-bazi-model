"""12TF: old manuscript identity and ownership metadata are not original target folio witnesses."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class NclCopyCrosswalk12TF(unittest.TestCase):
    def test_two_physical_holding_ids_not_collapsed(self):
        record=load("docs/research/MING-DATONG-YEHUOBIAN-12TF-NCL02260-ZHOU-SEAL-CROSSWALK-R1.json")
        base=load("docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json")
        entries={s["source_id"]:s for s in base["sources"]}
        a=record["target_copy_catalog_proxy"];b=record["distinct_copy_control"]
        self.assertNotEqual(a["source_id"],b["source_id"])
        self.assertIn(a["source_id"],entries);self.assertIn(b["source_id"],entries)
        self.assertEqual(a["shelfmark"],"204.26 02260")
        self.assertEqual(b["shelfmark"],"204.26 02261")
        self.assertNotEqual(a["layout_lines"],b["layout_lines"])
        self.assertNotEqual(a["physical_fascicles"],b["physical_fascicles"])
        self.assertTrue(a["do_not_count_pdf_parts_as_independent_manuscript_copies"])
        self.assertTrue(b["do_not_reclassify_as_ncl02260"])
        self.assertTrue(all(e["physical_glyph_authority"] is False for e in (entries[a["source_id"]],entries[b["source_id"]])))
        self.assertIn("周印/星詒",a["catalog_transcribed_marks"])
        self.assertIn("祥符周/氏瑞瓜/堂圖書",a["catalog_transcribed_marks"])

    def test_1619_and_original_leaf_claims_stay_unproven(self):
        r=load("docs/research/MING-DATONG-YEHUOBIAN-12TF-NCL02260-ZHOU-SEAL-CROSSWALK-R1.json")
        adjud=r["adjudication"]
        for key in ("li_ciming_read_exact_ncl02260_physical_copy_proven",
                    "seal_original_physical_glyph_directly_seen",
                    "shen_1619_exact_manuscript_text_directly_collated",
                    "original_kaizao_louke_passage_present_in_ncl02260_proven",
                    "catalog_preface_sexagenary_variants_resolved",
                    "cadal_xuxiu_photo_lineage_resolved"):
            self.assertIs(adjud[key],False)
        self.assertNotEqual(r["target_copy_catalog_proxy"]["catalog_preface_sexagenary_wording"],r["distinct_copy_control"]["catalog_preface_sexagenary_wording"])
        self.assertEqual(adjud["new_direct_original_1827_votes"],0)
        self.assertEqual(adjud["new_direct_1869_revised_print_votes"],0)
        self.assertEqual(r["transmission_impact"]["edges_supported"],[])
        self.assertEqual(r["transmission_impact"]["nodes_added_or_strengthened"],[])

    def test_reuse_sources_not_count_new_ones(self):
        r=load("docs/research/MING-DATONG-YEHUOBIAN-12TF-NCL02260-ZHOU-SEAL-CROSSWALK-R1.json")
        state=load("docs/PROJECT-CURRENT-STATE-R1.json")
        manifest=load("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
        self.assertTrue(r["registry_reuse"]["no_new_source"])
        self.assertEqual(r["registry_reuse"]["source_union"],661)
        self.assertGreaterEqual(manifest["combined_source_count"],661)
        self.assertEqual(manifest["combined_source_count"],manifest["root_source_count"]+manifest["extension_source_count"])
        self.assertEqual(manifest["extension_source_count"],sum(x["source_count"] for x in manifest["shards"]))
        self.assertEqual(state["historical_audit"]["external_source_registry_total_unique_count"],manifest["combined_source_count"])
        self.assertEqual(state["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
        self.assertEqual(state["invariants"]["algorithm_reopen_count"],0)
        self.assertTrue(any(x.startswith("12TF NCL02260 ZHOU SEAL") for x in state["historical_audit"]["current_focus"]))
if __name__=="__main__":
    unittest.main()
