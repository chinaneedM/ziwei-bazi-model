"""12QF printed first-fascicle preface dates, no source or impression collapse."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QF-CADAL-FIRST-PREFACE-DIRECT-DATES-R1.json"
SHARD=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QF-CADAL-PREFACE-SOURCE-SHARD-R1.json"
STATE=ROOT/"docs/PROJECT-CURRENT-STATE-R1.json"
MANIFEST=ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
class Yehuobian12QFFrontmatterDateScope(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.shard=json.loads(SHARD.read_text(encoding="utf-8"))
        cls.state=json.loads(STATE.read_text(encoding="utf-8"))
        cls.manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    def test_four_date_layers_are_direct_pages_not_impression_date(self):
        self.assertEqual([(p["year"],p["direct_page"]) for p in self.e["four_separate_date_layers"]],
                         [(1606,7),(1700,10),(1827,5),(1869,5)])
        self.assertIn("同治八年己巳春月重校刊補",self.e["four_separate_date_layers"][-1]["source_text"])
        self.assertEqual(self.e["witness"]["source_pages"],115)
        self.assertEqual(self.e["witness"]["source_sha1"],"ea7e67a4eb47f6ca59bc54d4635f2f26eeef6f2a")
        self.assertFalse(self.e["witness"]["edition_impression_date_bound"])
    def test_source_copy_lineage_to_target_is_still_unproven(self):
        c=self.e["cross_fascicle_scope"]
        self.assertTrue(c["same_catalog_series_listing"])
        self.assertFalse(c["same_physical_copy_proven"])
        self.assertFalse(c["same_printing_or_edition_proven"])
        self.assertEqual(c["volume20_target_impression_1827_or_1869"],"NOT_FORMALLY_IDENTIFIED")
        self.assertFalse(self.e["witness"]["physical_copy_catalog_identity_bound"])
        self.assertFalse(self.e["cross_fascicle_scope"]["read_1869_page_as_evidence_1447_completion"])
    def test_original_pages_hash_scoped_to_source(self):
        row=self.shard["sources"][0]
        self.assertTrue(row["physical_glyph_authority"])
        self.assertEqual(row["verification_status"],"DIRECT_SOURCE_IMAGE_GLYPH_COLLATED_EDITION_UNBOUND")
        lookup={str(x["page"]):x["sha256"] for x in self.e["witness"]["manually_collated_pages"]}
        self.assertEqual(row["direct_image_attestation"]["page_sha256"],
                         {p:lookup[p] for p in ("5","7","10")})
        self.assertEqual(row["direct_image_attestation"]["source_sha256"],
                         self.e["witness"]["source_sha256"])
    def test_source_extension_and_product_gate(self):
        self.assertEqual(self.manifest["root_source_count"],647)
        self.assertEqual(self.manifest["extension_source_count"],7)
        self.assertEqual(self.manifest["combined_source_count"],654)
        self.assertEqual(self.state["historical_audit"]["external_source_registry_total_unique_count"],654)
        self.assertEqual(self.state["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
        self.assertEqual(self.state["invariants"]["algorithm_reopen_count"],0)
if __name__=="__main__":unittest.main()
