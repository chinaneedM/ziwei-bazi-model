#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import json
import pathlib
import zlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CASE_ROOT = ROOT / "training-data" / "DEV-GROUP-001" / "cases"
OUT_ROOT = ROOT / "runtime-recovery-v2" / "DEV-GROUP-001"

EXPECTED_LOGICAL = {
    "DEV-EXAMPLE-001": "fe390d56c06a776389a6a3844850e1eef57f68cadb3cc553296ed5718f27043e",
    "DEV-EXAMPLE-002": "edcae8dd0651cf7c6754b7b2664b1f0ebabb279d0a33d7bcfa9843fd5aa44b2e",
    "DEV-EXAMPLE-003": "3684944f3c46f2c8280171ea99be7aa9f2791ce8dea9d57d0a3ddc0c1372809a",
    "DEV-EXAMPLE-004": "6fe5074d02d1e60686d487c8b37ef6ac2e14e7f74f1cedaf2c1b1129ed2ad672",
}
EXPECTED_SOURCE_BYTES = {
    "DEV-EXAMPLE-001": 8025,
    "DEV-EXAMPLE-002": 8805,
    "DEV-EXAMPLE-003": 8749,
    "DEV-EXAMPLE-004": 8165,
}
B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact_b64(text: str) -> str:
    return "".join(text.split())


def decode_b64(text: str) -> bytes:
    s = compact_b64(text)
    s += "=" * ((4 - len(s) % 4) % 4)
    return base64.b64decode(s, validate=False)


def gzip_header_size(data: bytes) -> int:
    if len(data) < 10 or data[:2] != b"\x1f\x8b":
        raise ValueError("not gzip")
    flags = data[3]
    pos = 10
    if flags & 4:
        xlen = int.from_bytes(data[pos:pos + 2], "little")
        pos += 2 + xlen
    if flags & 8:
        pos = data.index(0, pos) + 1
    if flags & 16:
        pos = data.index(0, pos) + 1
    if flags & 2:
        pos += 2
    return pos


def raw_inflate(data: bytes) -> bytes | None:
    try:
        start = gzip_header_size(data)
        payload = data[start:-8] if len(data) >= start + 8 else data[start:]
        return zlib.decompress(payload, -zlib.MAX_WBITS)
    except Exception:
        return None


def logical_body(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def accept(raw: bytes | None, case_id: str) -> Any | None:
    if raw is None:
        return None
    try:
        obj = json.loads(raw.decode("utf-8"))
    except Exception:
        return None
    iso = obj.get("answer_isolation", {})
    if obj.get("case_id") != case_id:
        return None
    if iso.get("answer_payload_present") is not False:
        return None
    if iso.get("answer_reference_disclosed") is not False:
        return None
    if obj.get("questions", {}).get("question_count") != 5:
        return None
    if sha(logical_body(obj)) != EXPECTED_LOGICAL[case_id]:
        return None
    return obj


def first_invalid_utf8(raw: bytes) -> int | None:
    try:
        raw.decode("utf-8")
        return None
    except UnicodeDecodeError as exc:
        return exc.start


def map_output_to_compressed(data: bytes, output_index: int) -> int:
    start = gzip_header_size(data)
    payload = data[start:-8] if len(data) >= start + 8 else data[start:]
    d = zlib.decompressobj(-zlib.MAX_WBITS)
    produced = 0
    for i, byte in enumerate(payload):
        chunk = d.decompress(bytes([byte]))
        produced += len(chunk)
        if produced > output_index:
            return start + i
    return start + max(0, len(payload) // 2)


def write_case(case_id: str, obj: Any) -> dict[str, Any]:
    body = logical_body(obj)
    path = OUT_ROOT / f"{case_id}.json"
    path.write_bytes(body)
    return {
        "path": str(path.relative_to(ROOT)),
        "bytes": len(body),
        "sha256": sha(body),
        "expected_logical_sha256": EXPECTED_LOGICAL[case_id],
        "logical_hash_match": sha(body) == EXPECTED_LOGICAL[case_id],
    }


def recover_local_substitution(case_id: str, text: str) -> tuple[Any | None, dict[str, Any]]:
    data = decode_b64(text)
    raw = raw_inflate(data)
    report: dict[str, Any] = {
        "decoded_bytes": len(data),
        "decoded_sha256": sha(data),
        "inflated_bytes": len(raw) if raw is not None else None,
        "first_invalid_utf8": first_invalid_utf8(raw) if raw is not None else None,
        "attempted_decoded_byte_replacements": 0,
        "attempted_base64_replacements": 0,
    }
    if raw is None:
        return None, report
    bad = first_invalid_utf8(raw)
    if bad is None:
        return None, report
    center = map_output_to_compressed(data, bad)
    report["mapped_compressed_offset"] = center

    # A single corrupted decoded byte usually begins affecting output at or just
    # before the first malformed UTF-8 sequence. Search a bounded deterministic
    # window and accept only the pre-registered logical SHA-256.
    lo = max(10, center - 192)
    hi = min(len(data) - 8, center + 96)
    for pos in range(lo, hi):
        original = data[pos]
        for value in range(256):
            if value == original:
                continue
            report["attempted_decoded_byte_replacements"] += 1
            candidate = bytearray(data)
            candidate[pos] = value
            obj = accept(raw_inflate(bytes(candidate)), case_id)
            if obj is not None:
                report["method"] = f"decoded_byte_replace:{pos}:{original}->{value}"
                return obj, report

    # One changed Base64 character can alter two adjacent decoded bytes. Search
    # the corresponding source-text window as a separate representation layer.
    compact = compact_b64(text)
    b64_center = min(len(compact), center * 4 // 3)
    lo = max(0, b64_center - 320)
    hi = min(len(compact), b64_center + 240)
    for pos in range(lo, hi):
        original = compact[pos]
        for char in B64:
            if char == original:
                continue
            report["attempted_base64_replacements"] += 1
            mutated = compact[:pos] + char + compact[pos + 1:]
            try:
                candidate = decode_b64(mutated)
            except Exception:
                continue
            obj = accept(raw_inflate(candidate), case_id)
            if obj is not None:
                report["method"] = f"base64_char_replace:{pos}:{original}->{char}"
                return obj, report
    return None, report


def recover_case4_deletion(text: str) -> tuple[Any | None, dict[str, Any]]:
    case_id = "DEV-EXAMPLE-004"
    compact = compact_b64(text)
    expected_file_bytes = EXPECTED_SOURCE_BYTES[case_id]
    report: dict[str, Any] = {
        "source_file_bytes": len(text.encode("utf-8")),
        "compact_chars": len(compact),
        "expected_source_file_bytes": expected_file_bytes,
        "attempted_deletions": 0,
    }

    # The registry says the stored object should be 8,165 bytes while the
    # committed object is 8,720 bytes. Try the exact observed excess and the
    # newline-adjusted neighbours at every insertion boundary.
    observed_excess = len(text.encode("utf-8")) - expected_file_bytes
    lengths = sorted({observed_excess - 1, observed_excess, observed_excess + 1, 554, 555, 556})
    lengths = [n for n in lengths if n > 0 and n < len(compact)]
    report["deletion_lengths"] = lengths
    for delete_len in lengths:
        for pos in range(0, len(compact) - delete_len + 1):
            report["attempted_deletions"] += 1
            mutated = compact[:pos] + compact[pos + delete_len:]
            try:
                candidate = decode_b64(mutated)
            except Exception:
                continue
            obj = accept(raw_inflate(candidate), case_id)
            if obj is not None:
                report["method"] = f"base64_window_delete:{pos}:{delete_len}"
                return obj, report
    return None, report


def main() -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    receipt: dict[str, Any] = {
        "schema": "DEV-GROUP-001-LOCALIZED-RECOVERY-V2",
        "group_id": "DEV-GROUP-001",
        "answer_vault_accessed": False,
        "acceptance_rule": "VALID_JSON_AND_NO_ANSWER_PAYLOAD_AND_REGISTERED_LOGICAL_SHA256_MATCH",
        "cases": [],
    }

    for case_id in ("DEV-EXAMPLE-002", "DEV-EXAMPLE-003"):
        path = CASE_ROOT / f"{case_id}.json.gz.b64"
        obj, report = recover_local_substitution(case_id, path.read_text(encoding="utf-8"))
        row: dict[str, Any] = {"case_id": case_id, "search": report}
        if obj is not None:
            row["recovered"] = write_case(case_id, obj)
            row["status"] = "PASS_RECOVERED"
        else:
            row["status"] = "FAIL_NOT_RECOVERED"
        receipt["cases"].append(row)

    path4 = CASE_ROOT / "DEV-EXAMPLE-004.json.gz.b64"
    obj4, report4 = recover_case4_deletion(path4.read_text(encoding="utf-8"))
    row4: dict[str, Any] = {"case_id": "DEV-EXAMPLE-004", "search": report4}
    if obj4 is not None:
        row4["recovered"] = write_case("DEV-EXAMPLE-004", obj4)
        row4["status"] = "PASS_RECOVERED"
    else:
        row4["status"] = "FAIL_NOT_RECOVERED"
    receipt["cases"].append(row4)

    passed = sum(1 for row in receipt["cases"] if row["status"] == "PASS_RECOVERED")
    receipt["recovered_case_count"] = passed
    receipt["status"] = "PASS_ALL_TARGETS" if passed == 3 else "PARTIAL_OR_FAILED"
    out = OUT_ROOT.parent / "recovery-v2-receipt.json"
    out.write_text(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
