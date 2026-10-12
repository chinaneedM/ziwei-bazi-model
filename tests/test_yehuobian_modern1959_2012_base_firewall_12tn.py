"""12TN: do not merge 1959 Yao-print edition with 2012 IHP-manuscript-described text."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = "docs/research/MING-DATONG-YEHUOBIAN-12TN-MODERN-1959-2012-BASE-TEXT-FIREWALL-R1.json"
S = "docs/research/MING-DATONG-YEHUOBIAN-12TN-MODERN-1959-2012-SOURCE-SHARD-R1.json"
M = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
H = "docs/PROJECT-CURRENT-STATE-R1.json"

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class ModernEditedBaseFirewall12TN(unittest.TestCase):
    def test_source_base_and_physical_identity_scope(self):
        e, s = load(E), load(S)
        b = e["bibliography"]
        self.assertEqual(b["zhonghua_1959"]["catalog_id"], "000001008336")
        self.assertEqual(b["shanghai_2012"]["isbn"], "9787532563593")
        self.assertEqual(b["shanghai_2012"]["ndlcinii_ncid"], "BB11939247")
        self.assertEqual(b["taipei_1976"]["ncid"], "BA59231697")
        self.assertEqual([b[n]["volumes"] for n in ("zhonghua_1959", "shanghai_2012", "taipei_1976")], [3, 3, 5])
        a = e["adjudication"]
        for name in ("zhonghua1959_and_shanghai2012_identical_base_unproved",
                     "shanghai2012_and_taipei1976_same_original_exemplar_unproved",
                     "shanghai2012_and_IHP_barcode174009_identity_unproved"):
            self.assertTrue(a[name])
        self.assertFalse(b["shanghai_2012"]["actual_editorial_foreword_and_target_glyph_directly_checked"])
        self.assertEqual(a["new_historical_glyph_votes"], 0)
        self.assertEqual(a["algorithm_reopens"], 0)
        self.assertEqual(a["graph_edges_added"], 0)
        self.assertEqual(e["transmission_impact"]["edges_supported"], [])
        self.assertEqual(len(s["sources"]), 3)
        self.assertEqual([r["source_id"] for r in s["sources"]], e["source_registry"]["source_ids"])
        self.assertTrue(all(r["physical_glyph_authority"] is False and
                            r["verification_status"] == "BIBLIOGRAPHIC_METADATA_ONLY" and
                            r["evidence"] == E for r in s["sources"]))

    def test_registry_state_forward_only(self):
        m, h = load(M), load(H)
        a = h["historical_audit"]
        shards = [s for s in m["shards"] if s["path"] == S]
        self.assertEqual(len(shards), 1)
        self.assertEqual(shards[0]["source_count"], 3)
        self.assertGreaterEqual(m["combined_source_count"], 674)
        self.assertEqual(m["combined_source_count"], m["root_source_count"] + m["extension_source_count"])
        self.assertEqual(m["extension_source_count"], sum(v["source_count"] for v in m["shards"]))
        self.assertEqual(a["external_source_registry_total_unique_count"], m["combined_source_count"])
        self.assertEqual(a["external_source_registry_extension_count"], m["extension_source_count"])
        self.assertEqual(a["row_count"], 222)
        self.assertEqual(a["audited_row_count"], 222)
        self.assertEqual(a["repaired_provenance_metadata_defect_count"], 45)
        self.assertGreaterEqual(len(a["completed_batches"]), 487)
        self.assertTrue(any(v.startswith("12TN MODERN") for v in a["current_focus"]))
        self.assertEqual(h["invariants"]["deterministic_fusion_chart_product_r1"], "CLOSED")
        self.assertEqual(h["invariants"]["algorithm_reopen_count"], 0)
        self.assertEqual(h["invariants"]["candidate_collapse_count"], 0)

if __name__ == "__main__":
    unittest.main()
