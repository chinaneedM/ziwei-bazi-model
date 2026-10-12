import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class XuxiuVolume1174Source12ST(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=load("docs/research/MING-DATONG-YEHUOBIAN-12ST-XUXIU-1174-PUBLIC-FACSIMILE-LOCATOR-R1.json")
        cls.sh=load("docs/research/MING-DATONG-YEHUOBIAN-12ST-XUXIU-1174-PUBLIC-SOURCE-SHARD-R1.json")
        cls.m=load("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
        cls.state=load("docs/PROJECT-CURRENT-STATE-R1.json")

    def test_file_pagination_and_no_manuscript_visual_adjudication(self):
        o=self.r["exact_object"]
        f=o["wikimedia_file_description"]
        self.assertEqual(f["modern_series_volume"],1174)
        self.assertEqual(f["content_2_printed_start_page"],115)
        self.assertEqual(f["content_2_pdf_start_page"],118)
        self.assertEqual(f["pdf_page_count"],810)
        self.assertEqual(f["file_size_bytes"],68649578)
        self.assertEqual(f["commons_upstream_sha1"],"fc6a98b070c11372c557e22bb05cdc9859541715")
        self.assertEqual(f["modern_series_publication_year"],2002)
        self.assertIsNone(o["original_file_sha256_observed"])
        self.assertIsNone(o["source_page_sha256_observed"])
        self.assertIsNone(o["exact_article_pdf_page"])
        self.assertFalse(o["target_image_manually_collated"])
        self.assertFalse(o["source_pdf_fetched_this_session"])
        self.assertTrue(all(v is None for v in self.r["four_loci"].values()))
        self.assertEqual(self.r["invariants"]["original_target_glyph_votes_added"],0)

    def test_impression_and_upload_dates_not_conflated(self):
        b=self.r["version_boundaries"]
        self.assertEqual(b["1827_original_printing_equivalence"],"NOT_ESTABLISHED")
        self.assertEqual(b["1869_repaired_printing_catalog_assignment"],"FILE_DESCRIPTION_ONLY_NOT_DIRECT_IMPRESSION_CHECK")
        self.assertEqual(b["2018_upload"],"PUBLIC_DIGITAL_DERIVATIVE_NOT_PHYSICAL_EDITION_DATE")
        self.assertTrue(b["not_same_copy_as_cadal_shlib_or_tokyo_by_name"])
        self.assertTrue(all(v==0 for v in self.r["external_actions"].values()))
        self.assertEqual(self.r["parent_batch"],"12QE_OPEN")

    def test_manifest_shard_hash_and_forward_state(self):
        sources=self.sh["sources"]
        self.assertEqual(len(sources),1)
        self.assertEqual(sources[0]["source_id"],"EXT-XUXIU-SIKU-1174-COMMONS-FACSIMILE-METADATA-12ST")
        self.assertFalse(sources[0]["physical_glyph_authority"])
        self.assertEqual(sources[0]["verification_status"],"BIBLIOGRAPHIC_METADATA_ONLY")
        path="docs/research/MING-DATONG-YEHUOBIAN-12ST-XUXIU-1174-PUBLIC-SOURCE-SHARD-R1.json"
        entries=self.m["shards"]
        self.assertEqual(len({s["path"] for s in entries}),len(entries))
        self.assertEqual(sum(s["path"]==path and s["source_count"]==1 for s in entries),1)
        self.assertGreaterEqual(self.m["extension_source_count"],13)
        self.assertEqual(self.m["extension_source_count"],sum(s["source_count"] for s in entries))
        self.assertEqual(self.m["combined_source_count"],self.m["root_source_count"]+self.m["extension_source_count"])
        a=self.state["historical_audit"]
        self.assertEqual(a["external_source_registry_total_unique_count"],self.m["combined_source_count"])
        self.assertEqual(a["external_source_registry_extension_count"],self.m["extension_source_count"])
        self.assertGreaterEqual(a["row_count"],222)
        self.assertGreaterEqual(a["audited_row_count"],222)
        self.assertEqual(a["row_count"],a["audited_row_count"])
        self.assertGreaterEqual(len(a["completed_batches"]),487)
        self.assertEqual(self.state["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
        self.assertEqual(self.state["invariants"]["algorithm_reopen_count"],0)
        self.assertTrue(any(x.startswith("12ST XUXIU") for x in a["current_focus"]))

if __name__=="__main__":
    unittest.main()
