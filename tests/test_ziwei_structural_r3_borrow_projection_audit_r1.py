from __future__ import annotations

import json
import unittest
from pathlib import Path

from fortune_training.ziwei_structural.r3 import BORROW_MEMBER_OFFSETS
from fortune_training.ziwei_structural.r3.projection import (
    BORROW_PROJECTION_SOURCE_REFS,
    FOURTEEN_MAIN_STAR_ENTITY_IDS,
)

ROOT = Path(__file__).resolve().parents[1]


class ZiweiStructuralR3BorrowProjectionAuditR1Tests(unittest.TestCase):
    def test_s06_preserves_three_school_specific_borrow_mechanics(self) -> None:
        text = (ROOT / "sources/canonical-runtime/S06/segment-0039.txt").read_text(
            encoding="utf-8"
        )
        for token in (
            "ZZTERM-L-0212",
            "ZZTERM-L-0219",
            "ZZTERM-L-0226",
            "BORROW_RULE_01=",
            "BORROW_RULE_02=",
            "BORROW_RULE_03=",
        ):
            self.assertIn(token, text)
        self.assertIn("本宫无十四正曜时才成立空宫借星", text)
        self.assertIn("借入对宫全部星曜", text)
        self.assertIn("必须先向其自身对宫完成借星", text)

    def test_released_r3_geometry_and_source_refs_remain_frozen(self) -> None:
        self.assertEqual((0, 4, 6, 8), BORROW_MEMBER_OFFSETS)
        self.assertEqual(14, len(FOURTEEN_MAIN_STAR_ENTITY_IDS))
        self.assertEqual(
            ("S06:ZZTERM_BORROW_CLOSURE", "S06:BORROW_RULE_01-05"),
            BORROW_PROJECTION_SOURCE_REFS,
        )

    def test_modern_closure_is_not_promoted_to_classical_doctrine(self) -> None:
        evidence = json.loads(
            (
                ROOT
                / "docs/research/evidence/batch-12mt/borrow-projection-replay.json"
            ).read_text(encoding="utf-8")
        )
        firewall = evidence["controls"]["engineering_firewall"]
        self.assertTrue(firewall["immutable_projection"])
        self.assertFalse(firewall["recursive_projection"])
        self.assertTrue(firewall["zero_second_contribution"])
        self.assertTrue(firewall["physical_dedup_key"])
        self.assertFalse(firewall["engineering_details_claimed_as_classical_doctrine"])

    def test_provenance_granularity_gap_fails_closed_without_fabrication(self) -> None:
        evidence = json.loads(
            (
                ROOT
                / "docs/research/evidence/batch-12mt/borrow-projection-replay.json"
            ).read_text(encoding="utf-8")
        )
        boundary = evidence["controls"]["provenance_boundary"]
        self.assertFalse(boundary["per_member_source_root_atom_ids_serialized"])
        self.assertFalse(boundary["fabricated_source_root_mapping_authorized"])
        self.assertFalse(evidence["runtime_change"])
        self.assertFalse(evidence["algorithm_reopen"])


if __name__ == "__main__":
    unittest.main()
