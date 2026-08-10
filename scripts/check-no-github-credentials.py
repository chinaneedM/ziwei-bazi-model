#!/usr/bin/env python3
"""Fail if tracked repository content resembles persisted GitHub credentials."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_PATHS = {
    ".git-credentials",
    ".netrc",
    ".config/gh/hosts.yml",
    "gh/hosts.yml",
}
TOKEN_PATTERNS = (
    re.compile(rb"gh[pousr]_[A-Za-z0-9]{36,}"),
    re.compile(rb"github_pat_[A-Za-z0-9_]{80,}"),
)


def tracked_paths() -> list[Path]:
    result = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "ls-files",
            "-z",
            "--cached",
            "--others",
            "--exclude-standard",
        ],
        check=True,
        capture_output=True,
    )
    return [ROOT / item.decode("utf-8") for item in result.stdout.split(b"\0") if item]


def main() -> int:
    failures: list[str] = []
    for path in tracked_paths():
        relative = path.relative_to(ROOT).as_posix()
        if relative in FORBIDDEN_PATHS or relative.endswith("/.config/gh/hosts.yml"):
            failures.append(f"forbidden credential path: {relative}")
            continue
        if not path.is_file():
            continue
        payload = path.read_bytes()
        if any(pattern.search(payload) for pattern in TOKEN_PATTERNS):
            failures.append(f"token-shaped content: {relative}")
    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1
    print("GITHUB_CREDENTIAL_PERSISTENCE=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
