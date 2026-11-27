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


    def test_ledger_dependency_inventory_for_storage_migration(self):
        """Read-only exact-HEAD static inventory; no storage or validation changes."""
        import subprocess

        revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                  capture_output=True, text=True)
        if revision.returncode:
            self.skipTest("dependency inventory requires a Git checkout")
        head = revision.stdout.strip()

        def grep_paths(terms):
            args = ["git", "grep", "-I", "-l", "-F"]
            for term in terms:
                args.extend(["-e", term])
            args.extend([head, "--"])
            proc = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
            self.assertIn(proc.returncode, (0, 1), proc.stderr)
            prefix = head + ":"
            return sorted(line[len(prefix):] for line in proc.stdout.splitlines()
                          if line.startswith(prefix))

        groups = {
            "ledger_path_or_schema": [
                "RESEARCH-OMISSION-RISK-LEDGER-R1.json",
                "TIANWEN-RESEARCH-OMISSION-RISK-LEDGER-R1",
            ],
            "ledger_fields": ["checkpoint_log", "reviewed_state_version",
                              "source_focus_count", "record_statuses("],
            "verifier_entrypoint": ["verify-research-omission-risk-ledger-r1.py"],
        }
        report = {"head": head, "scope": "ALL_TRACKED_TEXT_STATIC_LITERAL_REFERENCES"}
        for key, terms in groups.items():
            paths = grep_paths(terms)
            # Evidence documents and JSON data beneath docs/ are not executable
            # readers; retain counts and identify every other matching file.
            evidence = [p for p in paths if p.startswith("docs/") and
                        Path(p).suffix.lower() in {".json", ".md", ".txt"}]
            executable_or_config = [p for p in paths if p not in evidence]
            report[key] = {
                "total": len(paths), "docs_data_count": len(evidence),
                "other_paths": executable_or_config,
            }
        direct = report["ledger_path_or_schema"]["other_paths"]
        self.assertIn("scripts/project-context-r2.py", direct)
        self.assertIn("scripts/verify-research-omission-risk-ledger-r1.py", direct)
        self.assertIn(".github/workflows/verify-research-omission-continuity.yml", direct)
        print("TIANWEN_LEDGER_DEPENDENCY_INVENTORY " +
              json.dumps(report, ensure_ascii=False, separators=(",", ":")), flush=True)


    def test_pending_r8_admission_replays_existing_full_gates(self):
        """Verify the exact bounded candidate in an isolated local checkout overlay."""
        import os
        import subprocess
        import tempfile

        prep = runpy.run_path(str(ROOT / "scripts/prepare-tianwen-r8-admission.py"))
        current = json.loads((ROOT / mod["PATHS"]["state"]).read_bytes())
        manifest = json.loads((ROOT / mod["PATHS"]["manifest"]).read_bytes())
        if any(x["path"] == prep["SHARD"] for x in manifest["shards"]):
            self.assertGreaterEqual(tuple(map(int, current["schema_version"].split("."))), (1, 1588, 0))
            return  # The exact pending transaction no longer applies.
        # If it is still pending, all pins must hold; no silent rebase.
        replacements = prep["prepare"](ROOT)
        original_ledger = (ROOT / mod["PATHS"]["ledger"]).read_bytes()
        tracked = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                                 capture_output=True, check=True).stdout.split(b"\0")
        with tempfile.TemporaryDirectory(prefix="tianwen-r8-", dir=ROOT.parent) as temp:
            candidate = Path(temp)
            # Hardlink the tracked inputs only; never write a linked original.
            # Replace changed paths by unlinking the local link first.
            for entry in tracked:
                if not entry:
                    continue
                path = os.fsdecode(entry)
                source = ROOT / path
                if source.is_symlink():
                    self.fail("unexpected symlink in pinned checkout: " + path)
                target = candidate / path
                target.parent.mkdir(parents=True, exist_ok=True)
                os.link(source, target)
            for path, raw in replacements.items():
                target = candidate / path
                target.unlink()
                target.write_bytes(raw)
            reports = {}
            for script, extra in [
                ("scripts/verify-project-continuity-state-r1.py", []),
                ("scripts/verify-historical-source-registry-extensions-r1.py", []),
                ("scripts/verify-research-omission-risk-ledger-r1.py", []),
                ("scripts/project-context-r2.py", ["verify"]),
                ("scripts/project-context-r2.py", ["request"]),
            ]:
                proc = subprocess.run(["python", str(candidate / script), *extra],
                                      cwd=candidate, capture_output=True, text=True, timeout=60)
                self.assertEqual(proc.returncode, 0, proc.stdout[-2000:] + proc.stderr[-3000:])
                result = json.loads(proc.stdout.strip().splitlines()[-1])
                expected = "STALE_CHECKPOINT" if extra == ["request"] else "PASS"
                self.assertEqual(result["status"], expected)
                reports[script + " " + " ".join(extra)] = result["status"]
            self.assertEqual((ROOT / mod["PATHS"]["ledger"]).read_bytes(), original_ledger)
            candidate_ledger = json.loads((candidate / mod["PATHS"]["ledger"]).read_bytes())
            self.assertEqual(len(candidate_ledger["issues"]), 59)
            self.assertEqual(len(candidate_ledger["checkpoint_log"]), 1019)
            self.assertEqual(candidate_ledger["checkpoint_log"][:-1], json.loads(original_ledger)["checkpoint_log"])
            print("TIANWEN_R8_PREPARED_REPLAY " + json.dumps({
                "status": "PASS_PREPARED_NOT_PUBLISHED",
                "gates": reports,
                "replacement_bytes": {p: len(raw) for p, raw in replacements.items()},
                "candidate_blob_sha": {p: prep["blob_sha"](raw) for p, raw in replacements.items()},
            }, ensure_ascii=False, separators=(",", ":")), flush=True)

if __name__ == "__main__":
    unittest.main()
