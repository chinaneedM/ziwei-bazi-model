import argparse
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "build_r17_prompt_cutover.py"
SPEC = importlib.util.spec_from_file_location("r17_cutover", SCRIPT_PATH)
cutover = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(cutover)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class R17PromptCutoverTest(unittest.TestCase):
    def build_base(self, root: Path) -> tuple[Path, Path, dict]:
        base = root / "knowledge" / "base"
        base.mkdir(parents=True)
        rows = []
        for index in range(20):
            library_id = f"S{index:02d}"
            filename = f"{library_id}_测试库.txt"
            data = f"LIBRARY_ID={library_id}\nBASE={library_id}\n".encode("utf-8")
            (base / filename).write_bytes(data)
            rows.append({
                "library_id": library_id,
                "canonical_filename": filename,
                "repository_relative_path": f"knowledge/base/{filename}",
                "sha256_raw_file_bytes": sha(data),
                "file_size_bytes": len(data),
            })
        manifest = {
            "knowledge_release_id": "KNOWLEDGE-R16",
            "source_root": "knowledge/base",
            "source_files": rows,
            "s19_binding_sha256": "b" * 64,
        }
        manifest_path = base / "release-manifest-R16.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
        return base, manifest_path, manifest

    def build_snapshot(self, root: Path) -> tuple[Path, Path]:
        prompt = root / "operator-export.txt"
        prompt.write_text(
            f"MAIN_PROMPT_RUNTIME_ID={cutover.R17_RUNTIME_ID}\nactive prompt\n",
            encoding="utf-8",
        )
        normalized_hash = cutover.prompt_metrics(prompt.read_bytes())["sha256_utf8_lf_trailing_lf"]
        output_text = root / "model" / "candidates" / "MODEL-R17" / "main-prompt.txt"
        output_receipt = root / "model" / "candidates" / "MODEL-R17" / "prompt-snapshot.json"
        status = cutover.build_prompt_snapshot(argparse.Namespace(
            input=str(prompt),
            output_text=str(output_text),
            output_receipt=str(output_receipt),
            expected_normalized_sha256=normalized_hash,
        ))
        self.assertEqual(status, 0)
        return output_text, output_receipt

    def stage(self, root: Path, prompt_receipt: Path) -> Path:
        output_relative = Path("knowledge/candidates/KNOWLEDGE-R17")
        status = cutover.stage_knowledge_candidate(argparse.Namespace(
            repository_root=str(root),
            base_dir="knowledge/base",
            base_manifest="knowledge/base/release-manifest-R16.json",
            prompt_receipt=str(prompt_receipt),
            output_dir=output_relative.as_posix(),
            release_id="KNOWLEDGE-R17",
        ))
        self.assertEqual(status, 0)
        return root / output_relative

    def test_two_phase_candidate_preserves_r16_and_changes_only_s19(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, _, parent_manifest = self.build_base(root)
            _, prompt_receipt = self.build_snapshot(root)
            candidate_dir = self.stage(root, prompt_receipt)

            self.assertFalse((candidate_dir / "release-manifest.json").exists())
            stage = json.loads((candidate_dir / "cutover-stage-receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(stage["status"], "PASS_SOURCE_SET_STAGED_NOT_COMMIT_BOUND")

            status = cutover.finalize_knowledge_candidate(argparse.Namespace(
                repository_root=str(root),
                candidate_dir="knowledge/candidates/KNOWLEDGE-R17",
                base_manifest="knowledge/base/release-manifest-R16.json",
                prompt_receipt=str(prompt_receipt),
                source_content_commit="a" * 40,
                repository="owner/repo",
                release_id="KNOWLEDGE-R17",
            ))
            self.assertEqual(status, 0)
            manifest = json.loads((candidate_dir / "release-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["repository_commit_sha"], "a" * 40)
            self.assertEqual(manifest["changed_library_ids"], ["S19"])
            self.assertEqual(manifest["source_file_count"], 20)
            for row, parent in zip(manifest["source_files"][:19], parent_manifest["source_files"][:19]):
                self.assertEqual(row["sha256_raw_file_bytes"], parent["sha256_raw_file_bytes"])
            self.assertNotEqual(
                manifest["source_files"][19]["sha256_raw_file_bytes"],
                parent_manifest["source_files"][19]["sha256_raw_file_bytes"],
            )
            s19 = next(candidate_dir.glob("S19_*.txt")).read_text(encoding="utf-8")
            self.assertTrue(s19.startswith("# R17半自动化仓库运行与提示词—方法解耦唯一活动控制根"))
            self.assertIn("BEGIN_S19_RETAINED_R16_COMPLETE_FILE", s19)
            finalize = json.loads((candidate_dir / "cutover-finalize-receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(finalize["status"], "PASS_MANIFEST_BUILT_PENDING_IMMUTABLE_COMMIT_READBACK")

    def test_snapshot_mismatch_is_review_required_and_blocks_stage(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.build_base(root)
            prompt = root / "operator-export.txt"
            prompt.write_text(
                f"MAIN_PROMPT_RUNTIME_ID={cutover.R17_RUNTIME_ID}\ndifferent\n",
                encoding="utf-8",
            )
            output_text = root / "model" / "candidates" / "MODEL-R17" / "main-prompt.txt"
            output_receipt = root / "model" / "candidates" / "MODEL-R17" / "prompt-snapshot.json"
            status = cutover.build_prompt_snapshot(argparse.Namespace(
                input=str(prompt),
                output_text=str(output_text),
                output_receipt=str(output_receipt),
                expected_normalized_sha256="0" * 64,
            ))
            self.assertEqual(status, 2)
            receipt = json.loads(output_receipt.read_text(encoding="utf-8"))
            self.assertEqual(receipt["status"], "REVIEW_REQUIRED")
            with self.assertRaises(cutover.CutoverError):
                cutover.stage_knowledge_candidate(argparse.Namespace(
                    repository_root=str(root),
                    base_dir="knowledge/base",
                    base_manifest="knowledge/base/release-manifest-R16.json",
                    prompt_receipt=str(output_receipt),
                    output_dir="knowledge/candidates/KNOWLEDGE-R17",
                    release_id="KNOWLEDGE-R17",
                ))

    def test_finalize_rejects_nonimmutable_commit_identifier(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.build_base(root)
            _, prompt_receipt = self.build_snapshot(root)
            self.stage(root, prompt_receipt)
            with self.assertRaises(cutover.CutoverError):
                cutover.finalize_knowledge_candidate(argparse.Namespace(
                    repository_root=str(root),
                    candidate_dir="knowledge/candidates/KNOWLEDGE-R17",
                    base_manifest="knowledge/base/release-manifest-R16.json",
                    prompt_receipt=str(prompt_receipt),
                    source_content_commit="main",
                    repository="owner/repo",
                    release_id="KNOWLEDGE-R17",
                ))


if __name__ == "__main__":
    unittest.main()
