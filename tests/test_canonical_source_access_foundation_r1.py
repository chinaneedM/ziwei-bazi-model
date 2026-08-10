from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from fortune_training.cli import build_parser
from fortune_training.source_access import (
    DEFAULT_MAX_SEGMENT_BYTES,
    DERIVED_ACCESS_ROOT,
    _split_complete_lines,
    build_source_access_index,
    write_source_access,
)
from fortune_training.source_access_validator import validate_source_access
from fortune_training.util import TrainingError


PROJECT_ROOT = Path(__file__).resolve().parents[1]
S14_PATH = "sources/canonical/S14_test.txt"


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="",
    )


def _git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()


class SourceAccessFixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        unit = (
            "甲乙，。  \r\n"
            "\r\n"
            "CJK：合冲刑害\n"
            "decomposed: e\u0301\r"
            "fullwidth：ＡＢＣ\n"
        ).encode("utf-8")
        self.payload = unit * 1700 + "末行无换行  ".encode("utf-8")
        self.source_path = root / S14_PATH
        self.source_path.parent.mkdir(parents=True, exist_ok=True)
        self.source_path.write_bytes(self.payload)
        self.source = {
            "source_id": "S14",
            "path": S14_PATH,
            "bytes": len(self.payload),
            "sha256": _sha256(self.payload),
            "runtime_role": "PREDICTION_KNOWLEDGE_ONLY",
        }
        self.manifest_path = root / "sources/canonical-manifest.json"
        _write_json(
            self.manifest_path,
            {
                "schema": "CANONICAL-SOURCE-MANIFEST-V1",
                "source_count": 1,
                "sources": [self.source],
            },
        )
        _git(root, "init", "-q")
        _git(root, "config", "user.email", "source-access-test@example.invalid")
        _git(root, "config", "user.name", "Source Access Test")
        _git(root, "add", "sources/canonical", "sources/canonical-manifest.json")
        _git(root, "commit", "-qm", "fixture canonical identity")
        self.source_commit = _git(root, "rev-parse", "HEAD")

    @property
    def access_root(self) -> Path:
        return self.root / DERIVED_ACCESS_ROOT / "S14"

    @property
    def index_path(self) -> Path:
        return self.access_root / "index.json"

    def materialize(self) -> dict[str, object]:
        return write_source_access(
            self.root,
            source_commit=self.source_commit,
        )

    def load_index(self) -> dict[str, object]:
        return json.loads(self.index_path.read_text(encoding="utf-8"))

    def write_index(self, index: dict[str, object]) -> None:
        _write_json(self.index_path, index)


class CanonicalSourceAccessUnitTests(unittest.TestCase):
    def test_round_trip_preserves_all_bytes_and_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = SourceAccessFixture(Path(temporary))
            index = fixture.materialize()
            report = validate_source_access(fixture.root)
            reconstructed = b"".join(
                (fixture.root / row["path"]).read_bytes()
                for row in index["segments"]
            )
            self.assertEqual(reconstructed, fixture.payload)
            self.assertEqual(report["canonical_bytes"], len(fixture.payload))
            self.assertEqual(report["canonical_sha256"], _sha256(fixture.payload))
            self.assertEqual(report["source_commit"], fixture.source_commit)
            self.assertTrue(report["source_commit_verified"])
            self.assertTrue(report["round_trip_exact"])
            self.assertGreater(index["segment_count"], 1)
            self.assertEqual(index["segments"][0]["byte_start"], 0)
            self.assertEqual(
                index["segments"][-1]["byte_end_exclusive"],
                len(fixture.payload),
            )
            self.assertFalse(fixture.payload.endswith((b"\r", b"\n")))

    def test_materialization_is_deterministic_for_bound_commit(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = SourceAccessFixture(Path(temporary))
            first = fixture.materialize()
            first_files = {
                path.relative_to(fixture.root).as_posix(): path.read_bytes()
                for path in fixture.access_root.rglob("*")
                if path.is_file()
            }
            second = fixture.materialize()
            second_files = {
                path.relative_to(fixture.root).as_posix(): path.read_bytes()
                for path in fixture.access_root.rglob("*")
                if path.is_file()
            }
            self.assertEqual(first, second)
            self.assertEqual(first_files, second_files)

    def test_segment_tamper_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = SourceAccessFixture(Path(temporary))
            index = fixture.materialize()
            segment = fixture.root / index["segments"][0]["path"]
            payload = segment.read_bytes()
            marker = payload.index(b"decomposed")
            segment.write_bytes(payload[:marker] + b"D" + payload[marker + 1 :])
            with self.assertRaisesRegex(TrainingError, "segment metadata or hash"):
                validate_source_access(fixture.root)

    def test_index_tamper_variants_fail_closed(self):
        mutations = {
            "byte range": lambda index: index["segments"][0].__setitem__(
                "byte_start", 1
            ),
            "source SHA": lambda index: index["source"].__setitem__(
                "canonical_sha256", "0" * 64
            ),
            "source identity": lambda index: index["source"].__setitem__(
                "source_id", "S13"
            ),
            "segment order": lambda index: index["segments"].__setitem__(
                slice(0, 2), list(reversed(index["segments"][:2]))
            ),
            "duplicate path": lambda index: index["segments"][1].__setitem__(
                "path", index["segments"][0]["path"]
            ),
            "missing path": lambda index: index["segments"][0].__setitem__(
                "path", "sources/derived-access/S14/segment-9999.txt"
            ),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temporary:
                fixture = SourceAccessFixture(Path(temporary))
                fixture.materialize()
                index = copy.deepcopy(fixture.load_index())
                mutate(index)
                fixture.write_index(index)
                with self.assertRaises(TrainingError):
                    validate_source_access(fixture.root)

    def test_missing_and_unexpected_segment_files_fail_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = SourceAccessFixture(Path(temporary))
            index = fixture.materialize()
            (fixture.root / index["segments"][-1]["path"]).unlink()
            with self.assertRaisesRegex(TrainingError, "missing segment"):
                validate_source_access(fixture.root)
        with tempfile.TemporaryDirectory() as temporary:
            fixture = SourceAccessFixture(Path(temporary))
            fixture.materialize()
            (fixture.access_root / "segment-extra.txt").write_text("extra", encoding="utf-8")
            with self.assertRaisesRegex(TrainingError, "unexpected segment file"):
                validate_source_access(fixture.root)

    def test_stale_canonical_and_manifest_fail_before_or_during_replay(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = SourceAccessFixture(Path(temporary))
            fixture.materialize()
            fixture.source_path.write_bytes(fixture.payload + b"tamper")
            with self.assertRaisesRegex(TrainingError, "canonical source does not match manifest"):
                build_source_access_index(
                    fixture.root,
                    source_id="S14",
                    source_commit=fixture.source_commit,
                )
            with self.assertRaisesRegex(TrainingError, "canonical source does not match manifest"):
                validate_source_access(fixture.root)
        with tempfile.TemporaryDirectory() as temporary:
            fixture = SourceAccessFixture(Path(temporary))
            fixture.materialize()
            manifest = json.loads(fixture.manifest_path.read_text(encoding="utf-8"))
            manifest["sources"][0]["sha256"] = "0" * 64
            _write_json(fixture.manifest_path, manifest)
            with self.assertRaisesRegex(TrainingError, "canonical source does not match manifest"):
                validate_source_access(fixture.root)

    def test_invalid_utf8_and_oversized_line_fail_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = SourceAccessFixture(Path(temporary))
            invalid = b"valid\ninvalid:\xff\n"
            fixture.source_path.write_bytes(invalid)
            fixture.source["bytes"] = len(invalid)
            fixture.source["sha256"] = _sha256(invalid)
            _write_json(
                fixture.manifest_path,
                {
                    "schema": "CANONICAL-SOURCE-MANIFEST-V1",
                    "source_count": 1,
                    "sources": [fixture.source],
                },
            )
            with self.assertRaisesRegex(TrainingError, "strict UTF-8"):
                build_source_access_index(fixture.root, source_id="S14")
        with self.assertRaisesRegex(TrainingError, "line exceeds"):
            _split_complete_lines(
                b"one line is too long\n",
                source_id="S14",
                max_segment_bytes=8,
            )

    def test_source_commit_binding_rejects_uncommitted_identity_drift(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = SourceAccessFixture(Path(temporary))
            replacement = fixture.payload.replace(b"CJK", b"ALT", 1)
            fixture.source_path.write_bytes(replacement)
            fixture.source["bytes"] = len(replacement)
            fixture.source["sha256"] = _sha256(replacement)
            _write_json(
                fixture.manifest_path,
                {
                    "schema": "CANONICAL-SOURCE-MANIFEST-V1",
                    "source_count": 1,
                    "sources": [fixture.source],
                },
            )
            with self.assertRaisesRegex(TrainingError, "source commit canonical bytes"):
                build_source_access_index(
                    fixture.root,
                    source_id="S14",
                    source_commit=fixture.source_commit,
                )

    def test_r1_materializer_rejects_other_sources(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaisesRegex(TrainingError, "S14 only"):
                write_source_access(root, source_id="S13")

    def test_cli_exposes_build_and_independent_validation_paths(self):
        parser = build_parser()
        action = next(item for item in parser._actions if item.dest == "command")
        self.assertIn("canonical-source-access-build", action.choices)
        self.assertIn("canonical-source-access-validate", action.choices)


class CanonicalSourceAccessReleaseTests(unittest.TestCase):
    def test_materialized_s14_is_small_readable_and_exact(self):
        report = validate_source_access(PROJECT_ROOT)
        index_path = PROJECT_ROOT / DERIVED_ACCESS_ROOT / "S14/index.json"
        index = json.loads(index_path.read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["source_id"], "S14")
        self.assertTrue(report["source_commit_verified"])
        self.assertEqual(report["canonical_bytes"], 3354845)
        self.assertEqual(
            report["canonical_sha256"],
            "b225e64fcf7238b27a634e653a6904403d518335aeca59372b32e02f4a560407",
        )
        self.assertLess(index_path.stat().st_size, DEFAULT_MAX_SEGMENT_BYTES)
        self.assertTrue(index["segments"])
        for row in index["segments"]:
            segment_path = PROJECT_ROOT / row["path"]
            payload = segment_path.read_bytes()
            payload.decode("utf-8", errors="strict")
            self.assertLessEqual(len(payload), DEFAULT_MAX_SEGMENT_BYTES)
            self.assertEqual(len(payload), row["bytes"])

    def test_materialized_namespace_contains_s14_only(self):
        source_directories = {
            path.name
            for path in (PROJECT_ROOT / DERIVED_ACCESS_ROOT).iterdir()
            if path.is_dir()
        }
        self.assertEqual(source_directories, {"S14"})


if __name__ == "__main__":
    unittest.main()
