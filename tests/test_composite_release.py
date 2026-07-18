import tempfile
import unittest
from pathlib import Path

from fortune_v1.composite_release import materialize_knowledge_release
from fortune_v1.repository_release import LIBRARIES, write_object
from fortune_v1.util import FortuneError, sha256_file


class CompositeKnowledgeReleaseTest(unittest.TestCase):
    def fixture(self, root: Path):
        base = root / "knowledge" / "base"
        candidate = root / "knowledge" / "candidates" / "K-R17"
        base.mkdir(parents=True)
        candidate.mkdir(parents=True)
        overlay = candidate / "S19-overlay.txt"
        overlay.write_bytes(b"R17-OVERLAY\n")
        rows = []
        for lib in LIBRARIES:
            filename = f"{lib}_test.txt"
            base_file = base / filename
            base_file.write_bytes(f"BASE-{lib}\n".encode())
            if lib == "S19":
                expected = overlay.read_bytes() + base_file.read_bytes()
                rows.append({
                    "library_id": lib,
                    "canonical_filename": filename,
                    "repository_relative_path": f"knowledge/candidates/K-R17/materialized/{filename}",
                    "sha256_raw_file_bytes": __import__("hashlib").sha256(expected).hexdigest(),
                    "file_size_bytes": len(expected),
                    "source_materialization": {
                        "mode": "BYTE_PREPEND",
                        "base_repository_relative_path": f"knowledge/base/{filename}",
                        "base_sha256_raw_file_bytes": sha256_file(base_file),
                        "base_file_size_bytes": base_file.stat().st_size,
                        "overlay_repository_relative_path": "knowledge/candidates/K-R17/S19-overlay.txt",
                        "overlay_sha256_raw_file_bytes": sha256_file(overlay),
                        "overlay_file_size_bytes": overlay.stat().st_size,
                    },
                })
            else:
                rows.append({
                    "library_id": lib,
                    "canonical_filename": filename,
                    "repository_relative_path": f"knowledge/base/{filename}",
                    "sha256_raw_file_bytes": sha256_file(base_file),
                    "file_size_bytes": base_file.stat().st_size,
                    "source_materialization": {
                        "mode": "DIRECT_PARENT_REUSE",
                        "parent_repository_relative_path": f"knowledge/base/{filename}",
                    },
                })
        manifest = candidate / "release-manifest.json"
        write_object(manifest, {
            "schema": "FORTUNE-KNOWLEDGE-RELEASE-MANIFEST-V1",
            "knowledge_release_id": "K-R17",
            "release_kind": "COMPOSITE_CANDIDATE",
            "parent_release_id": "K-R16",
            "repository_full_name": "owner/repo",
            "repository_commit_sha": "a" * 40,
            "source_root": "knowledge/candidates/K-R17",
            "source_authority": "GITHUB_REPOSITORY_CONTENT_ADDRESSED_COMPOSITE",
            "source_file_count": 20,
            "source_files": rows,
            "s19_binding_sha256": "b" * 64,
        })
        return manifest, overlay

    def test_materializes_parent_reuse_and_s19_overlay(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, _ = self.fixture(root)
            output = root / "knowledge" / "candidates" / "K-R17-materialized"
            receipt = materialize_knowledge_release(manifest, root, output)
            self.assertEqual(receipt["status"], "PASS")
            self.assertEqual(receipt["source_file_count"], 20)
            self.assertEqual((output / "S00_test.txt").read_bytes(), b"BASE-S00\n")
            self.assertEqual((output / "S19_test.txt").read_bytes(), b"R17-OVERLAY\nBASE-S19\n")
            self.assertEqual(receipt["rows"][19]["mode"], "BYTE_PREPEND")

    def test_tampered_overlay_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, overlay = self.fixture(root)
            overlay.write_bytes(b"TAMPERED\n")
            output = root / "knowledge" / "candidates" / "K-R17-materialized"
            with self.assertRaises(FortuneError) as context:
                materialize_knowledge_release(manifest, root, output)
            self.assertEqual(context.exception.status, "COMPOSITE_SOURCE_SIZE_MISMATCH")


if __name__ == "__main__":
    unittest.main()
