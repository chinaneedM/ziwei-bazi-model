import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = "docs/research/MING-DATONG-YEHUOBIAN-12SU-XUXIU1174-COMMONS-TITLE-IDENTITY-CORRECTION-R1.json"
SHARD = "docs/research/MING-DATONG-YEHUOBIAN-12ST-XUXIU-1174-PUBLIC-SOURCE-SHARD-R1.json"
ARCHIVE = "docs/research/MING-DATONG-YEHUOBIAN-12ST-XUXIU-1174-PUBLIC-FACSIMILE-LOCATOR-R1.json"
MANIFEST = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
STATE = "docs/PROJECT-CURRENT-STATE-R1.json"

def load(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))
def blobsha(p):
    raw=(ROOT / p).read_bytes()
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()

class XuxiuTraditionalFileTitle12SU(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record=load(RECORD)
        cls.sh=load(SHARD)
        cls.archive=load(ARCHIVE)
        cls.manifest=load(MANIFEST)
        cls.state=load(STATE)

    def test_original_archived_and_corrected_canonical_routes_are_separate(self):
        old=self.record["correction"]["previous_url"]
        new=self.record["correction"]["corrected_url"]
        self.assertEqual(self.archive["exact_object"]["public_file_page"],old)
        self.assertNotEqual(old,new)
        self.assertIn("%E4%BF%AE%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8",new)
        self.assertIn("%E4%BF%AE%E5%9B%9B%E5%BA%93%E5%85%A8%E4%B9%A6",old)
        self.assertEqual(self.sh["sources"][0]["url"],new)
        self.assertEqual(self.sh["sources"][0]["locator_correction"]["forward_record"],RECORD)
        self.assertTrue(self.record["correction"]["live_page_summary_probed"])

    def test_correct_manifest_points_to_exact_changed_blob_and_no_new_source(self):
        specs=[x for x in self.manifest["shards"] if x["path"]==SHARD]
        self.assertEqual(len(specs),1)
        self.assertEqual(specs[0]["blob_sha"],blobsha(SHARD))
        # 12SU SHA is a historical checkpoint, not the latest mutable shard SHA.
        # Follow explicit forward-only 12UC -> 12UD revision links instead.
        uc=self.manifest["additional_research_evidence_12uc"]
        ud=self.manifest["additional_research_evidence_12ud"]
        self.assertEqual(uc["previous_12st_blob_sha"],self.record["source_shard_updated_blob_sha"])
        self.assertEqual(ud["source_registry_shard_sha_before"],uc["new_12uc_blob_sha"])
        self.assertEqual(specs[0]["blob_sha"],ud["source_registry_shard_sha_after"])
        self.assertEqual(self.record["source_shard_previous_blob_sha"],"8ff2ef2d4ce506b53dfe2ed52283f78597e54e1b")
        self.assertEqual(len(self.sh["sources"]),1)
        self.assertFalse(self.sh["sources"][0]["physical_glyph_authority"])
        self.assertEqual(self.sh["sources"][0]["verification_status"],"BIBLIOGRAPHIC_METADATA_ONLY")
        self.assertEqual(self.manifest["extension_source_count"],sum(x["source_count"] for x in self.manifest["shards"]))
        self.assertEqual(self.manifest["combined_source_count"],self.manifest["root_source_count"]+self.manifest["extension_source_count"])
        self.assertGreaterEqual(self.manifest["combined_source_count"],660)
        self.assertEqual(self.state["historical_audit"]["external_source_registry_total_unique_count"],self.manifest["combined_source_count"])
        self.assertEqual(self.state["historical_audit"]["external_source_registry_extension_count"],self.manifest["extension_source_count"])

    def test_no_unverified_target_glyph_and_no_chart_algorithm_reopen(self):
        p=self.record["independently_checked_live_page"]
        self.assertEqual(p["total_pdf_pages"],810)
        self.assertEqual(p["part2_pdf_page_1based"],p["part2_print_page"]+3)
        self.assertFalse(self.record["correction"]["source_pdf_binary_fetched"])
        self.assertIsNone(p["direct_full_pdf_sha256"])
        self.assertIsNone(p["target_article_pdf_page"])
        self.assertTrue(all(v is None for v in p["four_locus_readings"].values()))
        self.assertTrue(all(x==0 for x in self.record["external_actions"].values()))
        self.assertEqual(self.record["scope_guard"]["transmission_edges_added"],0)
        self.assertEqual(self.state["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
        self.assertEqual(self.state["invariants"]["algorithm_reopen_count"],0)
        self.assertGreaterEqual(self.state["historical_audit"]["row_count"],222)
        self.assertGreaterEqual(len(self.state["historical_audit"]["completed_batches"]),487)
        self.assertTrue(any(x.startswith("12SU XUXIU") for x in self.state["historical_audit"]["current_focus"]))

if __name__=="__main__":
    unittest.main()
