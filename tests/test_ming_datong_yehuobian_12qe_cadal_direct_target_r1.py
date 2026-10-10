"""Scope regression for printed CADAL fascicle 16 direct-page collation."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QE-CADAL02096915-V20-DIRECT-TARGET-GLYPH-R1.json"
MANIFEST=ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
SHARD=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QE-CADAL02096915-SOURCE-SHARD-R1.json"
class CADAL12QEDirectTargetImageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.shard=json.loads(SHARD.read_text(encoding="utf-8"))
        cls.manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    def test_direct_page_locator_and_exact_numeric_reading(self):
        w=self.e["witness"]
        self.assertEqual(w["source_pages"],135)
        self.assertEqual(w["source_sha1"],"69d9b157cc060b5cd760c953fedcd5eae282d8e9")
        self.assertEqual([p["page"] for p in w["manually_collated_pages"]],[65,66,120,121,122])
        self.assertEqual(self.e["target"]["target_pages"],[121,122])
        fields={x["field"]:x["reading"] for x in self.e["target"]["field_collation"]}
        self.assertEqual(fields["BEIJING_WINTER_SUNRISE"],"辰初二刻")
        self.assertEqual(fields["BEIJING_SUMMER_SUNSET"],"戌初三刻")
        self.assertIn("宮漏",fields["PALACE_CLOCK_ADOPTION"])
    def test_one_source_not_four_independent_physical_witnesses(self):
        self.assertEqual(self.e["comparison"]["distinct_digital_witness_count_this_batch"],1)
        self.assertEqual(self.e["comparison"]["independent_stemmatic_lineage_count_proven"],0)
        self.assertEqual({(x["winter"],x["summer"]) for x in self.e["comparison"]["rows"]},
                         {("辰初二刻","戌初三刻"),("辰初一刻","戌初一刻"),("辰初二刻","戌初一刻"),("辰初二刻","戌初二刻")})
        self.assertFalse(self.e["witness"]["edition_impression_date_bound"])
        self.assertFalse(self.e["witness"]["physical_copy_catalog_identity_bound"])
        self.assertTrue(all(v is False for v in self.e["scope_firewall"].values()))
    def test_extension_is_digest_bound_and_never_reopens_algorithm(self):
        self.assertEqual(self.manifest["combined_source_count"],654)
        self.assertEqual(self.manifest["extension_source_count"],7)
        row=self.shard["sources"][0]
        self.assertTrue(row["physical_glyph_authority"])
        self.assertEqual(row["verification_status"],"DIRECT_SOURCE_IMAGE_GLYPH_COLLATED_EDITION_UNBOUND")
        self.assertEqual(row["direct_image_attestation"]["source_sha256"],self.e["witness"]["source_sha256"])
        pages={str(x["page"]):x["sha256"] for x in self.e["witness"]["manually_collated_pages"]}
        self.assertEqual(row["direct_image_attestation"]["page_sha256"],
                         {p:pages[p] for p in ("66","121","122")})
        self.assertEqual(self.e["invariants"]["algorithm_reopens"],0)
        self.assertEqual(self.e["invariants"]["deterministic_product_r1"],"CLOSED")
if __name__=="__main__":unittest.main()
