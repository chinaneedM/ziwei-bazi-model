from __future__ import annotations

import unittest
from pathlib import Path

from fortune_training.ziwei_chart.dignity import (
    DIGNITY_SCALE_ID,
    OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_ID,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources" / "canonical-runtime" / "S01" / "segment-0001.txt"
DOC = ROOT / "docs" / "ZIWEI-S01-BRIGHTNESS-AUTHORITY-BOUNDARY-R1.md"


class ZiweiS01BrightnessAuthorityBoundaryR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = SOURCE.read_text(encoding="utf-8")
        cls.doc = DOC.read_text(encoding="utf-8")

    def test_s01_denies_brightness_recalculation_and_reference_overwrite(self) -> None:
        for expected in (
            "BRIGHTNESS_PRIMARY_INPUT=FROZEN_CHART",
            "S01_RECALCULATE_BRIGHTNESS_PERMISSION=NO",
            "SOURCE_BRIGHTNESS_REFERENCE_CAN_OVERWRITE=NO",
            "BRIGHTNESS_REFERENCE_CONFLICT",
            "不得由 S01 选择来源表覆盖原盘",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.source)

    def test_operational_dignity_remains_a_distinct_authority_class(self) -> None:
        self.assertEqual(DIGNITY_SCALE_ID, "ZIWEI-SEVEN-GRADE-DIGNITY-R1")
        self.assertEqual(
            OPERATIONAL_MAIN_STAR_DIGNITY_RULE_SET_ID,
            "OPERATIONAL-ZIWEI-MAIN-STAR-DIGNITY-R1",
        )
        for expected in (
            "MUST NOT",
            "S01 canonical brightness",
            "operational seven-grade `DignityAnnotation`",
            "must remain distinct from the operational dignity annotation",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.doc)


if __name__ == "__main__":
    unittest.main()
