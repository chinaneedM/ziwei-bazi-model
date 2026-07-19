import base64
import gzip
import hashlib
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
                    "sha256_raw_file_bytes": hashlib.sha256(expected).hexdigest(),
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

    def gzip_fixture(self, root: Path):
        base = root / "knowledge" / "base"
        candidate = root / "knowledge" / "candidates" / "K-R17-GZIP"
        base.mkdir(parents=True)
        candidate.mkdir(parents=True)
        decoded_overlay = b"R17-CANONICAL-OVERLAY\n"
        container = candidate / "S19-overlay.utf8.gz.b64"
        container.write_bytes(base64.b64encode(gzip.compress(decoded_overlay, mtime=0)))
        rows = []
        for lib in LIBRARIES:
            filename = f"{lib}_test.txt"
            base_file = base / filename
            base_file.write_bytes(f"BASE-{lib}\n".encode())
            if lib == "S19":
                expected = decoded_overlay + base_file.read_bytes()
                rows.append({
                    "library_id": lib,
                    "canonical_filename": filename,
                    "repository_relative_path": f"knowledge/candidates/K-R17-GZIP/materialized/{filename}",
                    "sha256_raw_file_bytes": hashlib.sha256(expected).hexdigest(),
                    "file_size_bytes": len(expected),
                    "source_materialization": {
                        "mode": "GZIP_BASE64_PREPEND",
                        "base_repository_relative_path": f"knowledge/base/{filename}",
                        "base_sha256_raw_file_bytes": sha256_file(base_file),
                        "base_file_size_bytes": base_file.stat().st_size,
                        "overlay_container_repository_relative_path": "knowledge/candidates/K-R17-GZIP/S19-overlay.utf8.gz.b64",
                        "overlay_container_sha256_raw_file_bytes": sha256_file(container),
                        "overlay_container_file_size_bytes": container.stat().st_size,
                        "overlay_sha256_raw_file_bytes": hashlib.sha256(decoded_overlay).hexdigest(),
                        "overlay_file_size_bytes": len(decoded_overlay),
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
        manifest = candidate / "release-manifest-v2.json"
        write_object(manifest, {
            "schema": "FORTUNE-KNOWLEDGE-RELEASE-MANIFEST-V1",
            "knowledge_release_id": "K-R17-GZIP",
            "release_kind": "COMPOSITE_CANDIDATE",
            "parent_release_id": "K-R16",
            "repository_full_name": "owner/repo",
            "repository_commit_sha": "c" * 40,
            "source_root": "knowledge/candidates/K-R17-GZIP",
            "source_authority": "GITHUB_REPOSITORY_CONTENT_ADDRESSED_COMPOSITE",
            "source_file_count": 20,
            "source_files": rows,
            "s19_binding_sha256": "d" * 64,
        })
        return manifest, container, decoded_overlay

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

    def test_materializes_canonical_gzip_base64_overlay(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, _, decoded_overlay = self.gzip_fixture(root)
            output = root / "knowledge" / "candidates" / "K-R17-GZIP-materialized"
            receipt = materialize_knowledge_release(manifest, root, output)
            self.assertEqual(receipt["status"], "PASS")
            self.assertEqual(
                (output / "S19_test.txt").read_bytes(),
                decoded_overlay + b"BASE-S19\n",
            )
            self.assertEqual(receipt["rows"][19]["mode"], "GZIP_BASE64_PREPEND")
            self.assertEqual(
                receipt["rows"][19]["decoded_overlay_sha256"],
                hashlib.sha256(decoded_overlay).hexdigest(),
            )

    def test_tampered_gzip_base64_container_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, container, _ = self.gzip_fixture(root)
            tampered = bytearray(container.read_bytes())
            tampered[-1] ^= 1
            container.write_bytes(bytes(tampered))
            output = root / "knowledge" / "candidates" / "K-R17-GZIP-materialized"
            with self.assertRaises(FortuneError) as context:
                materialize_knowledge_release(manifest, root, output)
            self.assertIn(
                context.exception.status,
                {"COMPOSITE_SOURCE_HASH_MISMATCH", "COMPOSITE_OVERLAY_DECODE_INVALID"},
            )


if __name__ == "__main__":
    unittest.main()
