#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
from pathlib import Path
from typing import Any

POLICY_PATH = Path("config/public-repository-policy.json")
SECRET_PATTERN = re.compile(r"secrets\.([A-Z0-9_]+)")
REPOSITORY_FIELD_PATTERN = re.compile(r"^\s*repository:\s*(.+?)\s*$")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_files(root: Path, configured: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in configured:
        path = root / raw
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(p for p in path.rglob("*") if p.is_file())
    return sorted(set(files))


def relative(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def verify(root: Path, visibility: str) -> dict[str, Any]:
    root = root.resolve()
    policy_path = root / POLICY_PATH
    if not policy_path.is_file():
        raise SystemExit("public repository policy missing")
    policy = read_json(policy_path)
    failures: list[dict[str, str]] = []

    required_visibility = policy.get("required_repository_visibility")
    if visibility != required_visibility:
        failures.append({
            "code": "REPOSITORY_VISIBILITY_NOT_PUBLIC",
            "path": ".",
            "detail": f"actual={visibility} required={required_visibility}",
        })

    forbidden = [str(value) for value in policy.get("forbidden_literals", [])]
    allowed_secrets = set(str(value) for value in policy.get("allowed_answer_secret_names", []))
    scan_files = iter_files(root, list(policy.get("active_scan_roots", [])))
    for path in scan_files:
        rel = relative(root, path)
        if rel == POLICY_PATH.as_posix():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for literal in forbidden:
            if literal and literal in text:
                failures.append({"code": "FORBIDDEN_PRIVATE_REPOSITORY_REFERENCE", "path": rel, "detail": literal})
        for secret in SECRET_PATTERN.findall(text):
            if "ANSWER" in secret and secret not in allowed_secrets:
                failures.append({"code": "FORBIDDEN_ANSWER_SECRET", "path": rel, "detail": secret})
        if rel.startswith(".github/workflows/"):
            for line_number, line in enumerate(text.splitlines(), 1):
                match = REPOSITORY_FIELD_PATTERN.match(line)
                if not match:
                    continue
                value = match.group(1).strip().strip("'\"")
                if value not in {"${{ github.repository }}", "${{github.repository}}"}:
                    failures.append({
                        "code": "CROSS_REPOSITORY_CHECKOUT_FORBIDDEN",
                        "path": rel,
                        "detail": f"line={line_number} repository={value}",
                    })

    vault_root = root / "public-answer-vault"
    allowed_patterns = list(policy.get("allowed_public_answer_patterns", []))
    forbidden_patterns = list(policy.get("plaintext_answer_repository_patterns", []))
    if vault_root.exists():
        for path in vault_root.rglob("*"):
            if not path.is_file():
                continue
            rel = relative(root, path)
            allowed = any(fnmatch.fnmatch(rel, pattern) for pattern in allowed_patterns)
            forbidden_match = any(fnmatch.fnmatch(rel, pattern) for pattern in forbidden_patterns)
            if forbidden_match and not allowed:
                failures.append({"code": "PLAINTEXT_ANSWER_FILE_FORBIDDEN", "path": rel, "detail": "public vault accepts encrypted envelopes only"})
            if path.is_symlink():
                failures.append({"code": "PUBLIC_ANSWER_SYMLINK_FORBIDDEN", "path": rel, "detail": "symlink"})

    result = {
        "schema": "PUBLIC-ONLY-REPOSITORY-VERIFICATION-V1",
        "status": "PASS" if not failures else "FAIL",
        "repository_visibility": visibility,
        "single_repository_runtime": policy.get("single_repository_runtime") is True,
        "scanned_file_count": len(scan_files),
        "failure_count": len(failures),
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--visibility", default=os.environ.get("GITHUB_REPOSITORY_VISIBILITY", "unknown"))
    args = parser.parse_args()
    result = verify(Path(args.root), str(args.visibility).lower())
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
