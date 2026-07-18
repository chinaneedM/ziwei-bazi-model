#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path

ROUND_DIR = Path(__file__).resolve().parent
PARTS_DIR = ROUND_DIR / 'source-parts'
TARGET = ROUND_DIR / 'materialize_validate.py'
EXPECTED_SHA256 = '1619b74f0d6c324b84b4342fd987413844441b16f451199f4bcd3d8e40458020'


def main() -> int:
    parts = sorted(PARTS_DIR.glob('part*.pyfrag'))
    if parts:
        payload = ''.join(path.read_text(encoding='utf-8') for path in parts)
        digest = hashlib.sha256(payload.encode('utf-8')).hexdigest()
        if digest != EXPECTED_SHA256:
            raise SystemExit(f'R9 source assembly hash mismatch: {digest}')
        TARGET.write_text(payload, encoding='utf-8')
    if not TARGET.exists():
        raise SystemExit('R9 materializer missing and no source parts are available')
    digest = hashlib.sha256(TARGET.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f'R9 materializer hash mismatch: {digest}')
    print(f'R9 materializer ready: {digest}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
