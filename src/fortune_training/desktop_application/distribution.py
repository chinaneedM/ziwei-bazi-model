from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

DESKTOP_DISTRIBUTION_SCHEMA = "ZIWEI-BAZI-WINDOWS-PORTABLE-DISTRIBUTION-R1"
DESKTOP_BUILD_METADATA_SCHEMA = "ZIWEI-BAZI-WINDOWS-PORTABLE-BUILD-METADATA-R1"
DESKTOP_APPLICATION_ID = "FORTUNE-CHART-WINDOWS-PORTABLE-R1"
DESKTOP_APPLICATION_VERSION = "0.2.0"

REQUIRED_RUNTIME_REPOSITORY_FILES: tuple[str, ...] = (
    "config/time-calendar-policies.json",
)

FORBIDDEN_REPOSITORY_DATA_PREFIXES: tuple[str, ...] = (
    "training/",
    "answers/",
    "answer-vault/",
    "answer_vault/",
    "model-learning/",
    "sources/canonical/",
    "sources/canonical-manifest.json",
)

_SOURCE_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


def repository_data_manifest() -> dict[str, object]:
    return {
        "schema": DESKTOP_DISTRIBUTION_SCHEMA,
        "application_id": DESKTOP_APPLICATION_ID,
        "application_version": DESKTOP_APPLICATION_VERSION,
        "runtime_repository_files": list(REQUIRED_RUNTIME_REPOSITORY_FILES),
        "forbidden_repository_data_prefixes": list(FORBIDDEN_REPOSITORY_DATA_PREFIXES),
        "distribution_shape": "WINDOWS_PYINSTALLER_ONEDIR_PORTABLE",
        "bind_policy": "LOOPBACK_ONLY",
        "automatic_git_pull": False,
        "prediction_training_runtime": False,
    }


def build_metadata(source_commit: str) -> dict[str, object]:
    normalized = source_commit.strip().lower()
    if not _SOURCE_COMMIT_RE.fullmatch(normalized):
        raise ValueError("source_commit must be a full 40-character lowercase/uppercase Git SHA")
    return {
        "schema": DESKTOP_BUILD_METADATA_SCHEMA,
        "application_id": DESKTOP_APPLICATION_ID,
        "application_version": DESKTOP_APPLICATION_VERSION,
        "source_commit": normalized,
        "distribution_shape": "WINDOWS_PYINSTALLER_ONEDIR_PORTABLE",
    }


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Emit deterministic Windows desktop build metadata")
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--metadata-out", type=Path, required=True)
    parser.add_argument("--manifest-out", type=Path, required=True)
    args = parser.parse_args(argv)

    _write_json(args.metadata_out, build_metadata(args.source_commit))
    _write_json(args.manifest_out, repository_data_manifest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
