import json
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
STATE = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"

def monotone_counts(manifest, state, required_path, minimum):
    shards = manifest["shards"]
    if len({x["path"] for x in shards}) != len(shards):
        return False
    if sum(x["path"] == required_path and x["source_count"] == 1 for x in shards) != 1:
        return False
    return (
        manifest["extension_source_count"] >= minimum
        and manifest["extension_source_count"] == sum(x["source_count"] for x in shards)
        and manifest["combined_source_count"] == manifest["root_source_count"] + manifest["extension_source_count"]
        and state["historical_audit"]["external_source_registry_extension_count"] == manifest["extension_source_count"]
        and state["historical_audit"]["external_source_registry_total_unique_count"] == manifest["combined_source_count"]
    )

class HistoricalShardMonotonicity12SQ(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.s = json.loads(STATE.read_text(encoding="utf-8"))
        cls.paths = {
          "12SN": "docs/research/MING-DATONG-YEHUOBIAN-12SN-IOC-REPRODUCTION-SERVICE-SOURCE-SHARD-R1.json",
          "12SO": "docs/research/MING-DATONG-YEHUOBIAN-12SO-TOKYO-2005-DIGITIZATION-SOURCE-SHARD-R1.json",
        }

    def test_live_manifest_satisfies_both_incremental_checkpoint_gates(self):
        self.assertTrue(monotone_counts(self.m, self.s, self.paths["12SN"], 10))
        self.assertTrue(monotone_counts(self.m, self.s, self.paths["12SO"], 11))

    def test_valid_later_shard_append_is_accepted_by_both_old_gates(self):
        m = deepcopy(self.m)
        s = deepcopy(self.s)
        m["shards"].append({"path": "docs/research/TEST-SIMULATED-FUTURE-SHARD-R1.json",
                           "schema": "SYNTHETIC-NOT-COMMITTED", "source_count": 1,
                           "blob_sha": "0"*40})
        m["extension_source_count"] += 1
        m["combined_source_count"] += 1
        s["historical_audit"]["external_source_registry_extension_count"] += 1
        s["historical_audit"]["external_source_registry_total_unique_count"] += 1
        self.assertTrue(monotone_counts(m, s, self.paths["12SN"], 10))
        self.assertTrue(monotone_counts(m, s, self.paths["12SO"], 11))

    def test_drift_and_duplicate_shards_fail_closed(self):
        m = deepcopy(self.m)
        m["combined_source_count"] += 1
        self.assertFalse(monotone_counts(m, self.s, self.paths["12SN"], 10))
        m = deepcopy(self.m)
        m["shards"].append(deepcopy(m["shards"][-1]))
        self.assertFalse(monotone_counts(m, self.s, self.paths["12SO"], 11))
        m = deepcopy(self.m)
        m["shards"] = [x for x in m["shards"] if x["path"] != self.paths["12SN"]]
        self.assertFalse(monotone_counts(m, self.s, self.paths["12SN"], 10))

if __name__ == "__main__":
    unittest.main()
