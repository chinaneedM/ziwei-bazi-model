import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "materialize-training-runtime-view.py"
spec = importlib.util.spec_from_file_location("runtime_view", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class RuntimeViewMaterializationTests(unittest.TestCase):
    def _case(self, root: Path, *, answer_present: bool = False) -> Path:
        payload = {
            "case_id": "DEV-TEST-001",
            "answer_isolation": {
                "answer_payload_present": answer_present,
                "answer_reference_disclosed": False,
                "status": "PROGRAMMATICALLY_ISOLATED",
            },
            "ziwei": {"text": "宫位一\r\n宫位二\r\n"},
            "questions": {
                "original_text": "问题1\r\nA甲\r\nB乙",
                "parsed": [{"question_id": "Q1", "stem": "问题1", "options": []}],
            },
            "bazi": {"transcription": {"pillars": {"year": "甲子"}}},
        }
        path = root / "case.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def test_materializes_line_readable_answer_free_view(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = module.materialize(self._case(root), root / "views")
            self.assertEqual((out / "ziwei.txt").read_text(encoding="utf-8"), "宫位一\n宫位二\n")
            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema"], "TRAINING-CASE-RUNTIME-VIEW-V1")
            self.assertFalse(manifest["answer_payload_present"])
            self.assertIn("ziwei.txt", manifest["files"])

    def test_rejects_answer_bearing_case(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(ValueError):
                module.materialize(self._case(root, answer_present=True), root / "views")

    def test_rejects_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            case = self._case(root)
            module.materialize(case, root / "views")
            with self.assertRaises(FileExistsError):
                module.materialize(case, root / "views")


if __name__ == "__main__":
    unittest.main()
