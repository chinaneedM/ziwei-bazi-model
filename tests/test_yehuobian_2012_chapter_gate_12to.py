"""12TO: a modern table of contents cannot be promoted to ancient glyph authority."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
class ChapterGate12TO(unittest.TestCase):
    def test_modern_toc_only(self):
        e=load("docs/research/MING-DATONG-YEHUOBIAN-12TO-YANGWANLI-2012-CHAPTER-GATE-R1.json")
        s=load("docs/research/MING-DATONG-YEHUOBIAN-12TO-CHAPTER-CATALOG-SHARD-R1.json")
        self.assertEqual(e["target"],"卷二十／历法／改造漏刻")
        self.assertFalse(e["public_indices"]["dedao"]["target_body_seen"])
        self.assertFalse(e["public_indices"]["dedao"]["note_body_seen"])
        self.assertFalse(e["public_indices"]["zhangyue"]["note_body_seen"])
        self.assertFalse(e["public_indices"]["books_trial"]["unrestricted_target_reader_access_proven"])
        self.assertEqual(e["adjudication"]["new_independent_glyph_votes"],0)
        self.assertEqual(e["adjudication"]["algorithm_reopens"],0)
        self.assertEqual(e["transmission_impact"]["edges_supported"],[])
        self.assertEqual([s["source_id"] for s in s["sources"]],e["source_registry"]["ids"])
        self.assertTrue(all(not x["physical_glyph_authority"] for x in s["sources"]))
    def test_state_and_registry(self):
        m,h=load("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"),load("docs/PROJECT-CURRENT-STATE-R1.json")
        a=h["historical_audit"]
        self.assertEqual(len([x for x in m["shards"] if x["path"]=="docs/research/MING-DATONG-YEHUOBIAN-12TO-CHAPTER-CATALOG-SHARD-R1.json"]),1)
        self.assertGreaterEqual(m["combined_source_count"],676)
        self.assertEqual(m["combined_source_count"],m["root_source_count"]+m["extension_source_count"])
        self.assertEqual(m["extension_source_count"],sum(s["source_count"] for s in m["shards"]))
        self.assertEqual(a["external_source_registry_total_unique_count"],m["combined_source_count"])
        self.assertEqual(a["external_source_registry_extension_count"],m["extension_source_count"])
        self.assertEqual(a["row_count"],222)
        self.assertEqual(a["audited_row_count"],222)
        self.assertEqual(a["repaired_provenance_metadata_defect_count"],45)
        self.assertTrue(any(x.startswith("12TO DIGITAL") for x in a["current_focus"]))
        self.assertEqual(h["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
        self.assertEqual(h["invariants"]["algorithm_reopen_count"],0)
if __name__=="__main__":unittest.main()
