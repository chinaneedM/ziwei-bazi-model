from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources" / "canonical-runtime" / "S01" / "segment-0001.txt"
DOC = ROOT / "docs" / "ZIWEI-LAIYIN-RUNTIME-DENIAL-R1.md"


class ZiweiLaiyinRuntimeDenialR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = SOURCE.read_text(encoding="utf-8")
        cls.doc = DOC.read_text(encoding="utf-8")

    def test_canonical_runtime_permission_is_explicitly_denied(self) -> None:
        for expected in (
            "### 20.1 来因宫",
            "LAIYIN_RAW_INPUT_PRESERVE=YES",
            "LAIYIN_RUNTIME_PERMISSION=NO",
            "LAIYIN_EVIDENCE_PERMISSION=NO",
            "不建立运行宫位",
            "不建立证据节点",
            "不得作为冲突解决依据",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.source)

    def test_product_guard_does_not_promote_compatibility_to_runtime_authority(self) -> None:
        for expected in (
            "MUST NOT add a computed Laiyin palace field",
            "compatibility fixtures alone are insufficient",
            "must not alter Life Palace, Body Palace",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.doc)


if __name__ == "__main__":
    unittest.main()
