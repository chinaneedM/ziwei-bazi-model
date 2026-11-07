import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"docs/research/TIANWEN-13TK-XINGYUNLU-MING-V45-DIRECT-ORIGINAL-LIMIT-LOCATORS-R1.json"
SHARD=ROOT/"docs/research/TIANWEN-13TK-XINGYUNLU-NLC-CBM1408-SOURCE-SHARD-R1.json"

class XingOriginalTargetLocator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(REPORT.read_text(encoding="utf-8"))
        cls.r=json.loads(SHARD.read_text(encoding="utf-8"))["sources"][0]

    def test_sha_bound_two_original_limit_headers_only(self):
        d=self.d
        w=d["witness"]
        self.assertEqual(len(w["source_sha256"]),64)
        self.assertEqual(w["source_bytes"],18807026)
        self.assertEqual(w["pdf_pages"],74)
        self.assertFalse(w["edition_impression_date_bound"])
        self.assertFalse(w["physical_copy_catalog_identity_bound"])
        self.assertEqual({x["page"] for x in w["manually_collated_pages"]},{66,71})
        self.assertEqual({x["target"] for x in w["manually_collated_pages"]},{"三十五限","一百三十二限"})
        for p in w["manually_collated_pages"]:
            self.assertEqual(p["last_four_place_numeric_target"],"NOT_ADJUDICATED")
            self.assertTrue(p["row_header_confirmed"])
            self.assertEqual(len(p["sha256"]),64)
            self.assertEqual(len(p["window_jpeg_sha256"]),64)

    def test_registered_attestation_and_historical_firewall(self):
        r=self.r; d=self.d
        self.assertTrue(r["physical_glyph_authority"])
        self.assertEqual(r["verification_status"],"DIRECT_SOURCE_IMAGE_GLYPH_COLLATED_EDITION_UNBOUND")
        self.assertEqual(r["evidence"],"docs/research/TIANWEN-13TK-XINGYUNLU-MING-V45-DIRECT-ORIGINAL-LIMIT-LOCATORS-R1.json")
        self.assertEqual(r["direct_image_attestation"]["source_sha256"],d["witness"]["source_sha256"])
        self.assertEqual(r["direct_image_attestation"]["source_url"],d["witness"]["source_url"])
        self.assertEqual(r["direct_image_attestation"]["page_sha256"],{str(x["page"]):x["sha256"] for x in d["witness"]["manually_collated_pages"]})
        self.assertEqual(d["historical_comparison"]["new_Xing_source_L35_Ji"],"UNDECIDED_ORIGINAL_LAST_PLACE")
        self.assertEqual(d["historical_comparison"]["new_Xing_source_L132_Chi"],"UNDECIDED_ORIGINAL_LAST_PLACE")
        self.assertEqual(d["adjudication"]["g893_historical_finals"],"0/6")
        self.assertEqual(d["adjudication"]["algorithm_reopens"],0)

if __name__=="__main__":unittest.main()
