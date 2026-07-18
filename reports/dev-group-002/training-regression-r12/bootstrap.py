#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import zlib
from pathlib import Path

ROUND_DIR = Path(__file__).resolve().parent
PAYLOAD_DIR = ROUND_DIR / 'payload'
TARGET = ROUND_DIR / 'materialize_validate.py'
EXPECTED_SHA256 = '7646fbc143db4767e78fceead894bb86f4b00a7796014063336a584e992a3ef9'


def main() -> int:
    text_parts = [PAYLOAD_DIR / f'part{i:02}.txt' for i in range(5)]
    hex_tail = PAYLOAD_DIR / 'part05.hex'
    if all(path.exists() for path in text_parts) and hex_tail.exists():
        encoded = ''.join(path.read_text(encoding='utf-8') for path in text_parts)
        encoded += bytes.fromhex(hex_tail.read_text(encoding='utf-8').strip()).decode('ascii')
        payload = zlib.decompress(base64.b64decode(encoded))
        digest = hashlib.sha256(payload).hexdigest()
        if digest != EXPECTED_SHA256:
            raise SystemExit(f'R12 payload hash mismatch: {digest}')
        TARGET.write_bytes(payload)
    if not TARGET.exists():
        raise SystemExit('R12 materializer missing and payload is incomplete')
    digest = hashlib.sha256(TARGET.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f'R12 materializer hash mismatch: {digest}')
    print(f'R12 materializer ready: {digest}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
