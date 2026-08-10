from __future__ import annotations

import hashlib
import json
from pathlib import Path

from fortune_training.canonical_runtime import validate_canonical_runtime, write_canonical_runtime
from fortune_training.util import object_sha256
from fortune_training.verify import build_source_manifest


ROOT = Path(__file__).resolve().parents[1]
S04_PATH = ROOT / "sources" / "canonical" / "S04_十二宫主题太极与气数位库.txt"
CANONICAL_MANIFEST_PATH = ROOT / "sources" / "canonical-manifest.json"
SOURCE_POLICY_PATH = ROOT / "config" / "source-policy.json"

EXPECTED_CURRENT_S04_SHA256 = "7586cc1b8c71047c15382045adc46533db2ffd3e06d4354a2c56851ee2c7492b"
EXPECTED_CURRENT_S04_SIZE_BYTES = 1434396
RETAINED_SHA256 = "765caa9944161607b72bd7d7cc641332a65a4d9ac77bba7c9b884de50da7ccc8"
RETAINED_SIZE_BYTES = 1430055
RETAINED_MARKER = b"BEGIN_S04_RETAINED_COMPLETE_PAYLOAD\n"
CORRECTION_ID = "S04-SANFANG-SIZHENG-CORRECTION-R1"

CORRECTION_BLOCK = """# S04 三方四正内部一致性最高优先级修正（Issue #194）

```text
PATCH_ID=S04-SANFANG-SIZHENG-CORRECTION-R1
PATCH_STATUS=ACTIVE_HIGHEST_PRECEDENCE
PATCH_SCOPE=S04-SF-07..S04-SF-12
PATCH_REASON=RETAINED_ROWS_CONFLICT_WITH_S04_OPPOSITION_TABLE_AND_Z12_GEOMETRY
PATCH_RETAINED_PAYLOAD_MUTATION=FORBIDDEN
RETAINED_PAYLOAD_SHA256_ASSERTION=765caa9944161607b72bd7d7cc641332a65a4d9ac77bba7c9b884de50da7ccc8
RETAINED_PAYLOAD_SIZE_BYTES_ASSERTION=1430055
ACTIVE_S04_SANFANG_SIZHENG_INVARIANT=OPPOSITION:+6;TRINE_SET:+4,+8
ACTIVE_S04_SANFANG_SIZHENG_RESOLUTION=RETAINED_S04-SF-01..06_PLUS_CORRECTION_S04-SF-CORR-07..12
LOWER_CONFLICTING_S04_SF_07_TO_12=HISTORICAL_AUDIT_ONLY
S04-SF-CORR-07|迁移宫|夫妻宫、福德宫|命宫|OVERRIDES=S04-SF-07
S04-SF-CORR-08|交友宫|子女宫、父母宫|兄弟宫|OVERRIDES=S04-SF-08
S04-SF-CORR-09|官禄宫|命宫、财帛宫|夫妻宫|OVERRIDES=S04-SF-09
S04-SF-CORR-10|田宅宫|兄弟宫、疾厄宫|子女宫|OVERRIDES=S04-SF-10
S04-SF-CORR-11|福德宫|夫妻宫、迁移宫|财帛宫|OVERRIDES=S04-SF-11
S04-SF-CORR-12|父母宫|子女宫、交友宫|疾厄宫|OVERRIDES=S04-SF-12
```

"""


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    raw = S04_PATH.read_bytes()
    if len(raw) != EXPECTED_CURRENT_S04_SIZE_BYTES:
        raise SystemExit(
            f"refusing S04 correction: expected {EXPECTED_CURRENT_S04_SIZE_BYTES} bytes, got {len(raw)}"
        )
    current_sha = sha256_bytes(raw)
    if current_sha != EXPECTED_CURRENT_S04_SHA256:
        raise SystemExit(
            f"refusing S04 correction: expected SHA {EXPECTED_CURRENT_S04_SHA256}, got {current_sha}"
        )
    if raw.count(RETAINED_MARKER) != 1:
        raise SystemExit("refusing S04 correction: retained payload marker is not unique")
    marker_index = raw.index(RETAINED_MARKER)
    retained = raw[marker_index + len(RETAINED_MARKER) :]
    if len(retained) != RETAINED_SIZE_BYTES or sha256_bytes(retained) != RETAINED_SHA256:
        raise SystemExit("refusing S04 correction: retained historical payload identity mismatch")
    if CORRECTION_ID.encode("utf-8") in raw[:marker_index]:
        raise SystemExit("refusing S04 correction: correction already present")

    corrected = raw[:marker_index] + CORRECTION_BLOCK.encode("utf-8") + raw[marker_index:]
    corrected_marker_index = corrected.index(RETAINED_MARKER)
    corrected_retained = corrected[corrected_marker_index + len(RETAINED_MARKER) :]
    if corrected_retained != retained:
        raise SystemExit("refusing S04 correction: retained historical payload changed")
    S04_PATH.write_bytes(corrected)

    canonical_manifest = build_source_manifest(ROOT)
    write_json(CANONICAL_MANIFEST_PATH, canonical_manifest)

    runtime_manifest = write_canonical_runtime(ROOT)
    validated_runtime_manifest = validate_canonical_runtime(ROOT)
    if runtime_manifest != validated_runtime_manifest:
        raise SystemExit("canonical runtime write/check mismatch")

    source_policy = json.loads(SOURCE_POLICY_PATH.read_text(encoding="utf-8"))
    source_policy["canonical_manifest_sha256"] = object_sha256(canonical_manifest)
    source_policy["canonical_runtime_manifest_sha256"] = object_sha256(runtime_manifest)
    write_json(SOURCE_POLICY_PATH, source_policy)

    new_raw = S04_PATH.read_bytes()
    new_marker_index = new_raw.index(RETAINED_MARKER)
    new_retained = new_raw[new_marker_index + len(RETAINED_MARKER) :]
    if len(new_retained) != RETAINED_SIZE_BYTES or sha256_bytes(new_retained) != RETAINED_SHA256:
        raise SystemExit("post-write retained payload verification failed")

    s04_entry = next(row for row in canonical_manifest["sources"] if row["source_id"] == "S04")
    print(f"NEW_S04_BYTES={s04_entry['bytes']}")
    print(f"NEW_S04_SHA256={s04_entry['sha256']}")
    print(f"RETAINED_PAYLOAD_BYTES={len(new_retained)}")
    print(f"RETAINED_PAYLOAD_SHA256={sha256_bytes(new_retained)}")
    print(f"CANONICAL_MANIFEST_OBJECT_SHA256={object_sha256(canonical_manifest)}")
    print(f"CANONICAL_RUNTIME_MANIFEST_OBJECT_SHA256={object_sha256(runtime_manifest)}")


if __name__ == "__main__":
    main()
