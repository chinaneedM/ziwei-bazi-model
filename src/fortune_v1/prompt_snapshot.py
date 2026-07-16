from __future__ import annotations

from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, immutable_copy, sha256_bytes, utc_now


def create_prompt_snapshot(runtime_id: str, prompt_file: str | Path, destination: str | Path,
                           attestation: dict[str, Any] | None = None,
                           expected_sha256: str | None = None,
                           expected_bytes: int | None = None,
                           expected_visible_characters: int | None = None) -> dict[str, Any]:
    source = Path(prompt_file)
    if not source.is_file() or source.stat().st_size == 0:
        raise FortuneError("prompt snapshot source is missing or empty", status="PROMPT_SNAPSHOT_INVALID")
    data = source.read_bytes()
    try:
        text = data.decode("utf-8-sig")
        unicode_status = "UTF8_VALID"
    except UnicodeDecodeError as exc:
        raise FortuneError(f"prompt export is not UTF-8: {exc}", status="PROMPT_SNAPSHOT_INVALID") from exc
    actual_sha256 = sha256_bytes(data)
    actual_bytes = len(data)
    visible_count = sum(1 for char in text if not char.isspace())
    checks = {
        "sha256": expected_sha256 is None or actual_sha256 == expected_sha256,
        "bytes": expected_bytes is None or actual_bytes == expected_bytes,
        "visible_characters": expected_visible_characters is None or visible_count == expected_visible_characters,
    }
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    prompt_target = destination / "main_prompt.txt"
    copy = immutable_copy(source, prompt_target)
    manifest = {
        "schema": "MAIN-PROMPT-AUDIT-SNAPSHOT-V1", "runtime_id": runtime_id,
        "snapshot_sha256": copy["sha256"], "snapshot_bytes": copy["bytes"], "captured_at": utc_now(),
        "authority_statement": "AUDIT_COPY_ONLY_NOT_RUNTIME_AUTHORITY", "runtime_attestation": attestation,
        "expected": {"sha256_raw_bytes": expected_sha256, "size_bytes": expected_bytes,
                     "visible_character_count": expected_visible_characters,
                     "visible_character_count_method": "UNICODE_NON_WHITESPACE_CODEPOINT_COUNT"},
        "actual": {"sha256_raw_bytes": actual_sha256, "size_bytes": actual_bytes,
                   "visible_character_count": visible_count, "unicode_status": unicode_status,
                   "bom": data.startswith(b"\xef\xbb\xbf"), "lf_count": data.count(b"\n"),
                   "crlf_count": data.count(b"\r\n"),
                   "leading_whitespace_codepoints": len(text) - len(text.lstrip()),
                   "trailing_whitespace_codepoints": len(text) - len(text.rstrip())},
        "checks": checks, "status": "PASS" if all(checks.values()) else "PROMPT_EXPORT_MISMATCH",
    }
    atomic_write_json(destination / "snapshot.json", manifest)
    return manifest
