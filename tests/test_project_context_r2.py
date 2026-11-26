from __future__ import annotations
import json
import runpy
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
mod = runpy.run_path(str(ROOT / "scripts/project-context-r2.py"))

class ContextR2Tests(unittest.TestCase):
    def test_current_view_reproduces_canonical_inputs(self):
        result = mod["verify_view"](ROOT)
        self.assertEqual(result["status"], "PASS")

    def test_literal_search_decoded_strings_and_keys(self):
        raw = r'{"sources":[{"\u7a2e":"\u7d2b\u5fae","title":"A B"}]}'
        self.assertEqual(mod["matching_terms"](raw, json.loads(raw), ["紫微", "種", "A B", "a b", "不存在"]), ["紫微", "種", "A B"])

    def test_view_detects_tampering_and_keeps_all_p0(self):
        data = {k: json.loads((ROOT / p).read_bytes()) for k, p in mod["PATHS"].items()}
        bindings = {p: mod["blob_sha"]((ROOT / p).read_bytes()) for p in mod["PATHS"].values()}
        view = mod["project"](data, bindings)
        self.assertEqual(len(view["p0"]), sum(q["priority"] == "P0" and q["status"] != "RESOLVED_WITH_EVIDENCE" for q in data["ledger"]["issues"]))
        data["ledger"]["binding"]["source_focus_count"] += 1
        with self.assertRaises(ValueError):
            mod["project"](data, bindings)

    def test_budget_fails_closed(self):
        with self.assertRaises(ValueError):
            mod["encode"]({"next": "X" * 13000})

    def test_full_registry_search_control(self):
        root = json.loads((ROOT / mod["PATHS"]["root"]).read_bytes())
        term = root["sources"][0]["source_id"]
        result = mod["scan_registry"](ROOT, [term], 1)
        self.assertEqual(result["status"], "PASS")
        self.assertGreaterEqual(result["per_term_matching_files"][term], 1)
        self.assertEqual(result["records"], json.loads((ROOT / mod["PATHS"]["manifest"]).read_bytes())["combined_source_count"])


    def test_request_pins_checkpoint_and_manifest(self):
        sha = "1" * 40
        q = {"schema":"TIANWEN-REGISTRY-QUERY-REQUEST-R2","query_id":"q","checkpoint_id":"cp","manifest_blob_sha":sha,"terms":["紫微"],"limit":5}
        self.assertTrue(mod["validate_request"](q, "cp", sha))
        self.assertFalse(mod["validate_request"](q, "other", sha))
        with self.assertRaises(ValueError):
            mod["validate_request"](q, "cp", "2" * 40)
        with self.assertRaises(ValueError):
            mod["validate_request"]({**q, "terms":[""]}, "cp", sha)

    def test_active_request_real_registry_or_explicit_skip(self):
        result = mod["run_request"](ROOT)
        self.assertIn(result["status"], {"PASS", "STALE_CHECKPOINT", "NO_REQUEST"})
        if result["status"] == "PASS":
            view = json.loads((ROOT / mod["VIEW"]).read_bytes())
            self.assertEqual(result["records"], view["counts"]["total_sources"])
            self.assertEqual(result["files"], view["counts"]["shards"] + 1)
            self.assertEqual(result["checkpoint_id"], view["checkpoint"]["id"])
            q = json.loads((ROOT / mod["REQUEST"]).read_bytes())
            self.assertEqual(set(result["per_term_matching_files"]), set(q["terms"]))
            self.assertEqual(result["registry_manifest_blob_sha"], q["manifest_blob_sha"])

if __name__ == "__main__":
    unittest.main()
