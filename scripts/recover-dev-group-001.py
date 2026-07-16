#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import json
import pathlib
import zlib
from dataclasses import dataclass
from typing import Any, Iterable

ROOT = pathlib.Path(__file__).resolve().parents[1]
CASE_ROOT = ROOT / "training-data" / "DEV-GROUP-001" / "cases"
OUT_ROOT = ROOT / "runtime-recovery" / "DEV-GROUP-001"

EXPECTED = {
    "DEV-EXAMPLE-001": "fe390d56c06a776389a6a3844850e1eef57f68cadb3cc553296ed5718f27043e",
    "DEV-EXAMPLE-002": "edcae8dd0651cf7c6754b7b2664b1f0ebabb279d0a33d7bcfa9843fd5aa44b2e",
    "DEV-EXAMPLE-003": "3684944f3c46f2c8280171ea99be7aa9f2791ce8dea9d57d0a3ddc0c1372809a",
    "DEV-EXAMPLE-004": "6fe5074d02d1e60686d487c8b37ef6ac2e14e7f74f1cedaf2c1b1129ed2ad672",
    "DEV-EXAMPLE-005": "5292c94c69263d6aacf934e0078b1d5f2e90a29d0b731df482da6b293a541e45",
}

B64_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_variants(obj: Any, original: bytes | None = None) -> dict[str, bytes]:
    variants = {
        "compact_sorted": json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"),
        "compact_sorted_nl": (json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8"),
        "pretty_sorted": json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8"),
        "pretty_sorted_nl": (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8"),
    }
    if original is not None:
        variants["original"] = original
        variants["original_strip"] = original.strip()
    return variants


def match_logical_hash(obj: Any, target: str, original: bytes | None = None) -> tuple[str | None, dict[str, str]]:
    hashes = {name: sha(body) for name, body in canonical_variants(obj, original).items()}
    for name, digest in hashes.items():
        if digest == target:
            return name, hashes
    return None, hashes


def decode_b64_loose(text: str) -> bytes:
    compact = "".join(text.split())
    compact += "=" * ((4 - len(compact) % 4) % 4)
    return base64.b64decode(compact, validate=False)


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


@dataclass
class InflateResult:
    output: bytes
    eof: bool
    error: str | None
    fail_offset: int | None


def incremental_gzip(data: bytes) -> InflateResult:
    d = zlib.decompressobj(16 + zlib.MAX_WBITS)
    out = bytearray()
    for i, byte in enumerate(data):
        try:
            out.extend(d.decompress(bytes([byte])))
        except Exception as exc:  # noqa: BLE001
            return InflateResult(bytes(out), d.eof, f"{type(exc).__name__}: {exc}", i)
    try:
        out.extend(d.flush())
    except Exception as exc:  # noqa: BLE001
        return InflateResult(bytes(out), d.eof, f"{type(exc).__name__}: {exc}", len(data))
    return InflateResult(bytes(out), d.eof, None, None)


def raw_deflate(data: bytes) -> InflateResult:
    try:
        start = gzip_header_size(data)
    except Exception as exc:  # noqa: BLE001
        return InflateResult(b"", False, f"header: {exc}", 0)
    payload = data[start:-8] if len(data) >= start + 8 else data[start:]
    d = zlib.decompressobj(-zlib.MAX_WBITS)
    out = bytearray()
    for i, byte in enumerate(payload):
        try:
            out.extend(d.decompress(bytes([byte])))
        except Exception as exc:  # noqa: BLE001
            return InflateResult(bytes(out), d.eof, f"{type(exc).__name__}: {exc}", start + i)
    try:
        out.extend(d.flush())
    except Exception as exc:  # noqa: BLE001
        return InflateResult(bytes(out), d.eof, f"{type(exc).__name__}: {exc}", len(data))
    return InflateResult(bytes(out), d.eof, None, None)


def parse_candidate(raw: bytes, case_id: str) -> tuple[Any | None, dict[str, Any]]:
    diag: dict[str, Any] = {"bytes": len(raw), "raw_sha256": sha(raw)}
    try:
        text = raw.decode("utf-8")
        diag["utf8"] = "PASS"
    except UnicodeDecodeError as exc:
        diag["utf8"] = f"FAIL:{exc}"
        return None, diag
    try:
        obj = json.loads(text)
        diag["json"] = "PASS"
    except json.JSONDecodeError as exc:
        diag["json"] = f"FAIL:{exc}"
        diag["prefix"] = text[:160]
        diag["suffix"] = text[-320:]
        return None, diag
    diag["case_id"] = obj.get("case_id")
    iso = obj.get("answer_isolation", {})
    diag["answer_payload_present"] = iso.get("answer_payload_present")
    diag["answer_reference_disclosed"] = iso.get("answer_reference_disclosed")
    diag["question_count"] = obj.get("questions", {}).get("question_count")
    if obj.get("case_id") != case_id:
        diag["identity"] = "FAIL_CASE_ID"
        return None, diag
    if iso.get("answer_payload_present") is not False or iso.get("answer_reference_disclosed") is not False:
        diag["identity"] = "FAIL_ANSWER_ISOLATION"
        return None, diag
    if obj.get("questions", {}).get("question_count") != 5:
        diag["identity"] = "FAIL_QUESTION_COUNT"
        return None, diag
    diag["identity"] = "PASS"
    return obj, diag


def evaluate(raw: bytes, case_id: str) -> tuple[Any | None, dict[str, Any]]:
    obj, diag = parse_candidate(raw, case_id)
    if obj is None:
        return None, diag
    variant, hashes = match_logical_hash(obj, EXPECTED[case_id], raw)
    diag["canonical_hashes"] = hashes
    diag["matching_variant"] = variant
    diag["logical_hash_match"] = variant is not None
    return (obj if variant is not None else None), diag


def candidate_streams(data: bytes) -> Iterable[tuple[str, bytes, InflateResult]]:
    full = incremental_gzip(data)
    yield "gzip_incremental", full.output, full
    raw = raw_deflate(data)
    yield "raw_deflate_incremental", raw.output, raw


def try_direct(case_id: str, text: str) -> tuple[Any | None, dict[str, Any], bytes]:
    data = decode_b64_loose(text)
    report: dict[str, Any] = {
        "decoded_bytes": len(data),
        "decoded_sha256": sha(data),
        "attempts": [],
    }
    for method, raw, infl in candidate_streams(data):
        obj, diag = evaluate(raw, case_id)
        report["attempts"].append({
            "method": method,
            "inflate": {
                "output_bytes": len(infl.output),
                "eof": infl.eof,
                "error": infl.error,
                "fail_offset": infl.fail_offset,
            },
            "candidate": diag,
        })
        if obj is not None:
            report["recovery_method"] = method
            return obj, report, data
    return None, report, data


def try_mutations(case_id: str, text: str, data: bytes, direct_report: dict[str, Any]) -> tuple[Any | None, dict[str, Any]]:
    mutation_report: dict[str, Any] = {"attempted": 0, "best_partial": []}
    fail_offsets = [
        row["inflate"].get("fail_offset")
        for row in direct_report.get("attempts", [])
        if row["inflate"].get("fail_offset") is not None
    ]
    center = min(fail_offsets) if fail_offsets else max(10, len(data) // 2)
    start = max(10, center - 96)
    end = min(max(start + 1, len(data) - 8), center + 96)
    best: list[tuple[int, str]] = []

    def inspect(candidate: bytes, label: str) -> Any | None:
        mutation_report["attempted"] += 1
        result = raw_deflate(candidate)
        score = len(result.output)
        if len(best) < 12 or score > best[0][0]:
            best.append((score, label))
            best.sort()
            del best[:-12]
        obj, _diag = evaluate(result.output, case_id)
        return obj

    # One decoded-byte substitution near the deterministic failure point.
    for pos in range(start, end):
        original = data[pos]
        for value in range(256):
            if value == original:
                continue
            candidate = bytearray(data)
            candidate[pos] = value
            obj = inspect(bytes(candidate), f"byte_replace:{pos}:{original}->{value}")
            if obj is not None:
                mutation_report["recovery_method"] = f"byte_replace:{pos}:{original}->{value}"
                mutation_report["best_partial"] = [{"bytes": n, "mutation": label} for n, label in sorted(best, reverse=True)]
                return obj, mutation_report

    compact = "".join(text.split())
    b64_center = min(len(compact), max(0, center * 4 // 3))
    b64_start = max(0, b64_center - 80)
    b64_end = min(len(compact), b64_center + 80)

    # One Base64-character replacement, insertion, or deletion. This catches a
    # dropped/changed character that shifted all subsequent decoded bits.
    for pos in range(b64_start, b64_end):
        original = compact[pos]
        for char in B64_ALPHABET:
            if char == original:
                continue
            mutated = compact[:pos] + char + compact[pos + 1:]
            try:
                candidate = decode_b64_loose(mutated)
            except Exception:  # noqa: BLE001
                continue
            obj = inspect(candidate, f"b64_replace:{pos}:{original}->{char}")
            if obj is not None:
                mutation_report["recovery_method"] = f"b64_replace:{pos}:{original}->{char}"
                mutation_report["best_partial"] = [{"bytes": n, "mutation": label} for n, label in sorted(best, reverse=True)]
                return obj, mutation_report

        mutated = compact[:pos] + compact[pos + 1:]
        try:
            candidate = decode_b64_loose(mutated)
            obj = inspect(candidate, f"b64_delete:{pos}:{original}")
            if obj is not None:
                mutation_report["recovery_method"] = f"b64_delete:{pos}:{original}"
                mutation_report["best_partial"] = [{"bytes": n, "mutation": label} for n, label in sorted(best, reverse=True)]
                return obj, mutation_report
        except Exception:  # noqa: BLE001
            pass

        for char in B64_ALPHABET:
            mutated = compact[:pos] + char + compact[pos:]
            try:
                candidate = decode_b64_loose(mutated)
            except Exception:  # noqa: BLE001
                continue
            obj = inspect(candidate, f"b64_insert:{pos}:{char}")
            if obj is not None:
                mutation_report["recovery_method"] = f"b64_insert:{pos}:{char}"
                mutation_report["best_partial"] = [{"bytes": n, "mutation": label} for n, label in sorted(best, reverse=True)]
                return obj, mutation_report

    mutation_report["best_partial"] = [{"bytes": n, "mutation": label} for n, label in sorted(best, reverse=True)]
    return None, mutation_report


def write_recovered(case_id: str, obj: Any) -> dict[str, Any]:
    body = (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    path = OUT_ROOT / f"{case_id}.json"
    path.write_bytes(body)
    variant, hashes = match_logical_hash(obj, EXPECTED[case_id])
    return {
        "path": str(path.relative_to(ROOT)),
        "stored_bytes": len(body),
        "stored_sha256": sha(body),
        "logical_sha256": EXPECTED[case_id],
        "logical_hash_variant": variant,
        "canonical_hashes": hashes,
    }


def main() -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    receipt: dict[str, Any] = {
        "schema": "DEV-GROUP-001-MECHANICAL-RECOVERY-V1",
        "group_id": "DEV-GROUP-001",
        "answer_vault_accessed": False,
        "cases": [],
    }

    # Infer the original logical-hash canonicalization from the readable case.
    case5_path = CASE_ROOT / "DEV-EXAMPLE-005.json"
    case5_raw = case5_path.read_bytes()
    case5_obj = json.loads(case5_raw.decode("utf-8"))
    variant5, hashes5 = match_logical_hash(case5_obj, EXPECTED["DEV-EXAMPLE-005"], case5_raw)
    receipt["logical_hash_inference"] = {
        "case_id": "DEV-EXAMPLE-005",
        "matching_variant": variant5,
        "hashes": hashes5,
        "status": "PASS" if variant5 else "FAIL",
    }

    for index in range(1, 5):
        case_id = f"DEV-EXAMPLE-{index:03d}"
        path = CASE_ROOT / f"{case_id}.json.gz.b64"
        text = path.read_text(encoding="utf-8")
        obj, direct_report, decoded = try_direct(case_id, text)
        row: dict[str, Any] = {
            "case_id": case_id,
            "source_path": str(path.relative_to(ROOT)),
            "source_bytes": len(path.read_bytes()),
            "source_sha256": sha(path.read_bytes()),
            "expected_logical_sha256": EXPECTED[case_id],
            "direct": direct_report,
        }
        if obj is None and case_id == "DEV-EXAMPLE-001":
            obj, mutation_report = try_mutations(case_id, text, decoded, direct_report)
            row["mutation_search"] = mutation_report
        if obj is not None:
            row["recovered"] = write_recovered(case_id, obj)
            row["status"] = "PASS_RECOVERED_HASH_MATCHED"
        else:
            row["status"] = "FAIL_NOT_RECOVERED"
        receipt["cases"].append(row)

    recovered = sum(1 for row in receipt["cases"] if row["status"].startswith("PASS"))
    receipt["recovered_case_count"] = recovered
    receipt["expected_recovered_case_count"] = 4
    receipt["status"] = "PASS_ALL_RECOVERED" if recovered == 4 and variant5 else "PARTIAL_OR_FAILED"
    (OUT_ROOT.parent / "recovery-receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
