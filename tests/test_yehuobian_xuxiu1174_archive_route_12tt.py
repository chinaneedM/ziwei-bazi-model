"""12TT: online vol1174 file listing cannot count as ancient text or pure 1827 printing."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12TT-XUXIU1174-INTERNET-ARCHIVE-ROUTE-R1.json"
STATE = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"

class Xuxiu1174AcquisitionScope12TT(unittest.TestCase):
    def test_exact_route_and_two_print_layers(self):
        e = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.assertEqual(e["candidate_witness"]["volume"], 1174)
        self.assertEqual(e["candidate_witness"]["imprint_base_date"], "1827-DAOGUANG7_AS_CATALOGUED")
        self.assertEqual(e["candidate_witness"]["revision_date"], "1869-TONGZHI8_AS_CATALOGUED")
        self.assertFalse(e["candidate_witness"]["edition_physically_collated"])
        self.assertIsNone(e["candidate_witness"]["target_original_leaf"])
        routes = e["evidence_routes"]
        self.assertTrue(any(x.get("file_label")=="续修四库全书.1174.子部.杂家类.pdf" and x["role"]=="FIRST_PARTY_DIGITAL_REPOSITORY_FILE_LIST" for x in routes))
        self.assertTrue(any(x["role"]=="DIRECT_INSTITUTIONAL_RESOURCE_ROUTER" and x["institution"]=="University of Toronto Libraries" for x in routes))
        self.assertIn("BYTES_NOT_OBTAINED", e["retrieval_result"])

    def test_no_historical_vote_or_reopen(self):
        e = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        s = json.loads(STATE.read_text(encoding="utf-8"))
        i = e["invariants"]
        self.assertEqual(i["ancient_target_glyph_votes_added"], 0)
        self.assertEqual(i["chart_algorithm_reopens"], 0)
        self.assertFalse(i["original_1827_unrevised_leaf_seen"])
        self.assertFalse(i["original_1869_revised_leaf_seen"])
        self.assertEqual(i["new_external_source_registry_entries"], 0)
        self.assertEqual(i["source_registry_total"],678)
        self.assertLessEqual(i["source_registry_total"],s["historical_audit"]["external_source_registry_total_unique_count"])
        self.assertEqual(i["graph_nodes"], 250)
        self.assertEqual(i["graph_edges"], 237)
        self.assertEqual(s["invariants"]["deterministic_fusion_chart_product_r1"], "CLOSED")
        self.assertEqual(s["invariants"]["algorithm_reopen_count"], 0)
        self.assertTrue(any(x.startswith("12TT ") for x in s["historical_audit"]["current_focus"]))

if __name__ == "__main__":
    unittest.main()
