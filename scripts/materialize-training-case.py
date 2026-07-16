#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import binascii
import gzip
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


class MaterializationError(RuntimeError):
    """Raised when a stored training case cannot be reproduced exactly."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(obj: Any) -> bytes:
    """Canonical logical representation used by the training registry."""
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode(
        "utf-8"
    )


def load_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as exc:
        raise MaterializationError(f"cannot read {path}: {exc}") from exc


def load(path: Path) -> Any:
    stored = load_bytes(path)

    if path.name.endswith(".json.gz.b64"):
        try:
            encoded = "".join(stored.decode("ascii").split())
        except UnicodeDecodeError as exc:
            raise MaterializationError(f"{path}: Base64 transport is not ASCII") from exc

        if len(encoded) % 4:
            raise MaterializationError(
                f"{path}: invalid Base64 length {len(encoded)} (not divisible by 4)"
            )

        try:
            compressed = base64.b64decode(encoded, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise MaterializationError(f"{path}: strict Base64 decode failed: {exc}") from exc

        try:
            raw = gzip.decompress(compressed)
        except (gzip.BadGzipFile, EOFError, OSError, zlib_error_types()) as exc:
            raise MaterializationError(f"{path}: gzip integrity check failed: {exc}") from exc
    elif path.name.endswith(".json"):
        raw = stored
    else:
        raise MaterializationError(
            f"{path}: unsupported storage format; use plain .json or .json.gz.b64"
        )

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MaterializationError(f"{path}: materialized payload is not UTF-8: {exc}") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise MaterializationError(f"{path}: materialized payload is not JSON: {exc}") from exc


def zlib_error_types() -> type[BaseException] | tuple[type[BaseException], ...]:
    # gzip.decompress may surface zlib.error, but importing lazily keeps the
    # public surface of this small utility simple.
    import zlib

    return zlib.error


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle")
    parser.add_argument("--output")
    parser.add_argument("--receipt")
    parser.add_argument("--expected-stored-bytes", type=int)
    parser.add_argument("--expected-stored-sha256")
    parser.add_argument("--expected-logical-sha256")
    args = parser.parse_args()

    path = Path(args.bundle)
    receipt: dict[str, Any] = {
        "schema": "TRAINING-CASE-MATERIALIZATION-RECEIPT-V2",
        "path": str(path),
        "status": "FAIL",
    }

    try:
        stored = load_bytes(path)
        receipt["stored_bytes"] = len(stored)
        receipt["stored_sha256"] = sha256_bytes(stored)

        if (
            args.expected_stored_bytes is not None
            and len(stored) != args.expected_stored_bytes
        ):
            raise MaterializationError(
                f"stored byte mismatch: expected {args.expected_stored_bytes}, got {len(stored)}"
            )
        if (
            args.expected_stored_sha256
            and receipt["stored_sha256"] != args.expected_stored_sha256
        ):
            raise MaterializationError(
                "stored SHA-256 mismatch: "
                f"expected {args.expected_stored_sha256}, got {receipt['stored_sha256']}"
            )

        obj = load(path)
        body = canonical_json_bytes(obj)
        receipt["logical_json_bytes"] = len(body)
        receipt["logical_json_sha256"] = sha256_bytes(body)
        if (
            args.expected_logical_sha256
            and receipt["logical_json_sha256"] != args.expected_logical_sha256
        ):
            raise MaterializationError(
                "logical JSON SHA-256 mismatch: "
                f"expected {args.expected_logical_sha256}, got {receipt['logical_json_sha256']}"
            )

        if args.output:
            Path(args.output).write_bytes(body)
        else:
            sys.stdout.buffer.write(body)
        receipt["status"] = "PASS"
        return_code = 0
    except MaterializationError as exc:
        receipt["error"] = str(exc)
        print(str(exc), file=sys.stderr)
        return_code = 1

    if args.receipt:
        Path(args.receipt).parent.mkdir(parents=True, exist_ok=True)
        Path(args.receipt).write_text(
            json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
