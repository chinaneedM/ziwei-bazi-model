from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.clean_start import create_group_clean_start, record_group_contamination
from fortune_v1.util import FortuneError


class CleanStartTests(unittest.TestCase):
    def write_json(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    def fixture(self, root: Path) -> tuple[Path, Path]:
        cases = []
        for index in range(1, 3):
            case_id = f"CASE-{index}"
            case_path = root / "cases" / f"{case_id}.json"
            self.write_json(case_path, {
                "case_id": case_id,
                "dataset_type": "DEV",
                "binding": {"main_prompt_runtime_id": "R16", "source_baseline_tag": "S00-S19"},
                "answer_isolation": {"answer_payload_present": False},
                "questions": {"parsed": [{
                    "question_id": "Q1",
                    "options": [
                        {"option_id": "A", "text": "a"},
                        {"option_id": "B", "text": "b"},
                        {"option_id": "C", "text": "c"},
                        {"option_id": "D", "text": "d"},
                    ],
                }]},
            })
            cases.append({"case_id": case_id, "path": str(case_path)})
        group_path = root / "manifest.json"
        self.write_json(group_path, {
            "group_id": "GROUP-1",
            "case_count": 2,
            "question_count_total": 2,
            "status": "READY_FOR_BASELINE_PREDICTION",
            "answer_payload_present": False,
            "runtime_answer_scan": "PASS",
            "cases": cases,
        })
        install_path = root / "install-state.json"
        self.write_json(install_path, {
            "status": "INSTALLED_VALIDATED",
            "code_commit": "abc123",
        })
        return group_path, install_path

    def test_clean_start_creates_exact_allowlist_and_skeletons(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            group, install = self.fixture(root)
            result = create_group_clean_start(group, install, root / "runs", "RUN-1", "SESSION-1")
            self.assertEqual(result["status"], "READY_FOR_CLEAN_GROUP_PREDICTION")
            self.assertFalse(result["retrieval_policy"]["repository_search_allowed"])
            self.assertFalse(result["retrieval_policy"]["history_navigation_allowed"])
            self.assertEqual(len(result["cases"]), 2)
            for row in result["cases"]:
                skeleton = json.loads(Path(row["skeleton_path"]).read_text(encoding="utf-8"))
                self.assertEqual(skeleton["status"], "EMPTY_SKELETON_NOT_VALID_FOR_FREEZE")
                self.assertEqual(len(skeleton["questions"][0]["pairwise_rows"]), 6)
                self.assertIsNone(skeleton["questions"][0]["top1"])

    def test_nonoverwrite_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            group, install = self.fixture(root)
            create_group_clean_start(group, install, root / "runs", "RUN-1", "SESSION-1")
            with self.assertRaises(FortuneError) as caught:
                create_group_clean_start(group, install, root / "runs", "RUN-1", "SESSION-2")
            self.assertEqual(caught.exception.status, "GROUP_RUN_NONOVERWRITE_FAILED")

    def test_answer_bearing_group_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            group, install = self.fixture(root)
            data = json.loads(group.read_text(encoding="utf-8"))
            data["answer_payload_present"] = True
            self.write_json(group, data)
            with self.assertRaises(FortuneError) as caught:
                create_group_clean_start(group, install, root / "runs", "RUN-1", "SESSION-1")
            self.assertEqual(caught.exception.status, "GROUP_ANSWER_ISOLATION_FAILED")

    def test_contamination_receipt_nulls_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            group, install = self.fixture(root)
            result = create_group_clean_start(group, install, root / "runs", "RUN-1", "SESSION-1")
            receipt_path = root / "contamination.json"
            receipt = record_group_contamination(
                result["clean_start_path"], receipt_path, "pull_request", "PR-10"
            )
            self.assertEqual(receipt["status"], "FAIL_CLOSED_CONTAMINATED")
            self.assertIsNone(receipt["public_relative_prediction"])
            self.assertIsNone(receipt["formal_exact_assertion"])
            self.assertEqual(receipt["group_freeze"], "NOT_PERFORMED")


if __name__ == "__main__":
    unittest.main()
