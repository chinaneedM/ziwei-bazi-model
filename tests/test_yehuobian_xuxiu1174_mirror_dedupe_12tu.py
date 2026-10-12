"""12TU: multiple public mirrors of Xuxiu 1174 are not separate historical witnesses."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

class FacsimileDedupe12TU(unittest.TestCase):
    def test_existing_source_identity(self):
        e=load("docs/research/MING-DATONG-YEHUOBIAN-12TU-XUXIU1174-COMMONS-IA-DEDUPE-R1.json")
        shard=load(e["pre_existing_source_shard"])
        self.assertEqual(e["pre_existing_source_id"],shard["sources"][0]["source_id"])
        self.assertEqual(e["existing_commons"]["pdf_page_start_yehuobian_1based"],118)
        self.assertEqual(e["existing_commons"]["pdf_page_count"],810)
        self.assertEqual(e["existing_commons"]["pdf_bytes"],68649578)
        self.assertEqual(e["existing_commons"]["printed_page_start_yehuobian"],115)
        self.assertEqual(e["witness_identity"]["media_files_byte_identical"],"UNVERIFIED_REQUIRE_SHA256_COMPARISON")
        self.assertFalse(e["witness_identity"]["digitizations_are_independent_ancient_witnesses"])
        self.assertFalse(e["new_ia_route"]["source_registry_record_added"])

    def test_product_gate_and_no_double_count(self):
        e=load("docs/research/MING-DATONG-YEHUOBIAN-12TU-XUXIU1174-COMMONS-IA-DEDUPE-R1.json")
        s=load("docs/PROJECT-CURRENT-STATE-R1.json")
        i=e["invariants"]
        self.assertEqual(i["new_root_or_shard_source_records"],0)
        self.assertEqual(i["external_source_registry_total"],678)
        self.assertLessEqual(i["external_source_registry_total"],s["historical_audit"]["external_source_registry_total_unique_count"])
        self.assertEqual(i["ancient_target_glyph_votes_added"],0)
        self.assertEqual(i["chart_algorithm_reopens"],s["invariants"]["algorithm_reopen_count"])
        self.assertEqual(s["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
        self.assertTrue(any(x.startswith("12TU ") for x in s["historical_audit"]["current_focus"]))

if __name__=="__main__":
    unittest.main()
