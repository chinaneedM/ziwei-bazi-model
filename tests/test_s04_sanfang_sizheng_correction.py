from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from fortune_training.util import object_sha256
from fortune_training.ziwei_chart.registries import PALACE_DESIGNATIONS


ROOT = Path(__file__).resolve().parents[1]
S04_PATH = ROOT / "sources" / "canonical" / "S04_十二宫主题太极与气数位库.txt"
MANIFEST_PATH = ROOT / "sources" / "canonical-manifest.json"
RUNTIME_MANIFEST_PATH = ROOT / "sources" / "canonical-runtime-manifest.json"
SOURCE_POLICY_PATH = ROOT / "config" / "source-policy.json"
RETAINED_MARKER = b"BEGIN_S04_RETAINED_COMPLETE_PAYLOAD\n"
RETAINED_SHA256 = "765caa9944161607b72bd7d7cc641332a65a4d9ac77bba7c9b884de50da7ccc8"
RETAINED_SIZE_BYTES = 1430055
CORRECTION_ID = "S04-SANFANG-SIZHENG-CORRECTION-R1"
FIXED_TABLE_HEADING = "### 12.2 三方四正固定表"
FIXED_TABLE_END = "固定规则：本宫坐守、对宫、三方、夹宫和借照必须分开标记；"


SOURCE_NAME_TO_DESIGNATION_ID = {
    "命宫": "LIFE",
    "兄弟宫": "SIBLINGS",
    "夫妻宫": "SPOUSE",
    "子女宫": "CHILDREN",
    "财帛宫": "WEALTH",
    "疾厄宫": "HEALTH",
    "迁移宫": "TRAVEL",
    "交友宫": "SERVANTS_FRIENDS",
    "奴仆宫": "SERVANTS_FRIENDS",
    "官禄宫": "CAREER",
    "田宅宫": "PROPERTY",
    "福德宫": "FORTUNE",
    "父母宫": "PARENTS",
}


def exact_marker_index(raw: bytes) -> int:
    offsets: list[int] = []
    offset = 0
    for line in raw.splitlines(keepends=True):
        if line == RETAINED_MARKER:
            offsets.append(offset)
        offset += len(line)
    if len(offsets) != 1:
        raise AssertionError(f"expected one exact retained boundary line, found {len(offsets)}")
    return offsets[0]


def retained_fixed_table(text: str) -> str:
    start = text.index(FIXED_TABLE_HEADING)
    end = text.index(FIXED_TABLE_END, start)
    return text[start:end]


class S04SanfangSizhengCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = S04_PATH.read_bytes()
        cls.marker_index = exact_marker_index(cls.raw)
        cls.prefix = cls.raw[: cls.marker_index]
        cls.retained = cls.raw[cls.marker_index + len(RETAINED_MARKER) :]
        cls.prefix_text = cls.prefix.decode("utf-8")
        cls.retained_text = cls.retained.decode("utf-8")
        cls.fixed_table_text = retained_fixed_table(cls.retained_text)

    def test_retained_historical_payload_is_byte_exact(self) -> None:
        self.assertEqual(RETAINED_SIZE_BYTES, len(self.retained))
        self.assertEqual(RETAINED_SHA256, hashlib.sha256(self.retained).hexdigest())
        self.assertIn(
            f"RETAINED_PAYLOAD_SHA256_ASSERTION={RETAINED_SHA256}",
            self.prefix_text,
        )
        self.assertIn(
            f"RETAINED_PAYLOAD_SIZE_BYTES_ASSERTION={RETAINED_SIZE_BYTES}",
            self.prefix_text,
        )

    def test_correction_is_highest_precedence_and_does_not_rewrite_retained_rows(self) -> None:
        self.assertEqual(1, self.prefix_text.count(f"PATCH_ID={CORRECTION_ID}"))
        self.assertIn("PATCH_STATUS=ACTIVE_HIGHEST_PRECEDENCE", self.prefix_text)
        self.assertIn("PATCH_SCOPE=S04-SF-07..S04-SF-12", self.prefix_text)
        self.assertIn(
            "ACTIVE_S04_SANFANG_SIZHENG_RESOLUTION=RETAINED_S04-SF-01..06_PLUS_CORRECTION_S04-SF-CORR-07..12",
            self.prefix_text,
        )
        self.assertIn(
            "| S04-SF-07 | 迁移宫 | 命宫、夫妻宫 | 福德宫 |",
            self.fixed_table_text,
        )
        self.assertIn(
            "| S04-SF-12 | 父母宫 | 子女宫、疾厄宫 | 交友宫 |",
            self.fixed_table_text,
        )

    @staticmethod
    def _parse_markdown_row(line: str) -> tuple[str, tuple[str, str], str, str]:
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) != 4:
            raise AssertionError(f"invalid retained S04-SF row: {line}")
        row_id, theme, trines, opposite = parts
        pair = tuple(item.strip() for item in trines.split("、"))
        if len(pair) != 2:
            raise AssertionError(f"invalid trine pair: {line}")
        return row_id, pair, theme, opposite

    @staticmethod
    def _parse_correction_row(line: str) -> tuple[str, tuple[str, str], str, str]:
        parts = line.split("|")
        if len(parts) != 5:
            raise AssertionError(f"invalid S04 correction row: {line}")
        _row_id, theme, trines, opposite, override = parts
        pair = tuple(item.strip() for item in trines.split("、"))
        if len(pair) != 2 or not override.startswith("OVERRIDES="):
            raise AssertionError(f"invalid S04 correction row: {line}")
        return theme.strip(), pair, opposite.strip(), override.split("=", 1)[1]

    def test_active_all_twelve_rows_normalize_to_z12_geometry(self) -> None:
        expected_ids = {f"S04-SF-{index:02d}" for index in range(1, 13)}
        retained_rows: dict[str, tuple[str, tuple[str, str], str]] = {}
        for line in self.fixed_table_text.splitlines():
            if not line.lstrip().startswith("| S04-SF-"):
                continue
            row_id, trines, theme, opposite = self._parse_markdown_row(line)
            if row_id not in expected_ids:
                continue
            self.assertNotIn(row_id, retained_rows)
            retained_rows[row_id] = (theme, trines, opposite)
        self.assertEqual(expected_ids, set(retained_rows))

        corrections: dict[str, tuple[str, tuple[str, str], str]] = {}
        for line in self.prefix_text.splitlines():
            if not line.startswith("S04-SF-CORR-"):
                continue
            theme, trines, opposite, override = self._parse_correction_row(line)
            self.assertNotIn(override, corrections)
            corrections[override] = (theme, trines, opposite)
        self.assertEqual(
            {f"S04-SF-{index:02d}" for index in range(7, 13)},
            set(corrections),
        )

        active_rows = dict(retained_rows)
        active_rows.update(corrections)
        designation_ordinal = {
            designation_id: index
            for index, (designation_id, _display_name) in enumerate(PALACE_DESIGNATIONS)
        }

        for row_id in sorted(active_rows):
            theme_name, trine_names, opposite_name = active_rows[row_id]
            theme_id = SOURCE_NAME_TO_DESIGNATION_ID[theme_name]
            theme_raw = (-designation_ordinal[theme_id]) % 12
            trine_offsets = {
                ((-designation_ordinal[SOURCE_NAME_TO_DESIGNATION_ID[name]]) - theme_raw) % 12
                for name in trine_names
            }
            opposite_offset = (
                (-designation_ordinal[SOURCE_NAME_TO_DESIGNATION_ID[opposite_name]]) - theme_raw
            ) % 12
            self.assertEqual({4, 8}, trine_offsets, row_id)
            self.assertEqual(6, opposite_offset, row_id)

    def test_manifest_binds_the_corrected_s04_blob(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        s04 = next(row for row in manifest["sources"] if row["source_id"] == "S04")
        self.assertEqual(len(self.raw), s04["bytes"])
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), s04["sha256"])

    def test_source_policy_binds_regenerated_manifest_locks(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        runtime_manifest = json.loads(RUNTIME_MANIFEST_PATH.read_text(encoding="utf-8"))
        source_policy = json.loads(SOURCE_POLICY_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            object_sha256(manifest),
            source_policy["canonical_manifest_sha256"],
        )
        self.assertEqual(
            object_sha256(runtime_manifest),
            source_policy["canonical_runtime_manifest_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
