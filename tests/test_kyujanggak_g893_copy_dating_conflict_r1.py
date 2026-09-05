from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"docs"/"research"/"KYUJANGGAK-G893-COPY-DATING-CONFLICT-R1.json"

class KyujanggakG893CopyDatingConflictR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data=json.loads(PATH.read_text(encoding="utf-8"))

    def test_institutional_catalog_controls_copy_range_without_inventing_exact_year(self) -> None:
        meta=self.data["institutional_copy_metadata"]
        self.assertEqual(meta["edition"],"甲寅字")
        self.assertEqual(meta["publication_date_surface"],"15世紀 前半(世宗 年間:1418-1450)")
        self.assertFalse(meta["exact_year_stated"])
        self.assertIsNone(self.data["conflict_adjudication"]["exact_year_selected"])

    def test_secondary_specific_year_claims_remain_explicitly_conflicted(self) -> None:
        claims=self.data["specific_year_claims"]
        self.assertEqual([x["claim_year"] for x in claims],[1434,1434,1444])
        self.assertTrue(all(not x["copy_specific_exact_year_authority"] for x in claims))
        adj=self.data["conflict_adjudication"]
        self.assertEqual(adj["1434_secondary_claim_count"],2)
        self.assertEqual(adj["1444_secondary_claim_count"],1)
        self.assertTrue(adj["institutional_catalog_range_contains_1434"])
        self.assertTrue(adj["institutional_catalog_range_contains_1444"])

    def test_kang_bo_1444_is_not_used_to_explain_g893_without_direct_linkage(self) -> None:
        ctrl=self.data["related_separate_work_control"]
        self.assertEqual(ctrl["relationship_to_g893"],"SEPARATE_DERIVED_KOREAN_WORK_NOT_G893")
        self.assertEqual(ctrl["use_to_explain_g893_1444_claim"],"FORBIDDEN_WITHOUT_DIRECT_SOURCE_LINKAGE")
        self.assertEqual(self.data["conflict_adjudication"]["possible_kang_bo_1444_confusion"],"HYPOTHESIS_ONLY_NOT_ADJUDICATED")

    def test_date_conflict_has_no_target_or_runtime_effect(self) -> None:
        b=self.data["epistemic_boundaries"]
        self.assertEqual(b["gapja_type_history_as_exact_surviving_copy_year"],"FORBIDDEN")
        self.assertEqual(b["secondary_1434_majority_as_exact_copy_year"],"FORBIDDEN")
        self.assertEqual(b["single_secondary_1444_bibliography_as_exact_copy_year"],"FORBIDDEN")
        self.assertEqual(b["date_conflict_as_target_folio_or_glyph_evidence"],"FORBIDDEN")
        self.assertEqual(b["algorithm_or_runtime_selection_effect"],"NONE")
        self.assertEqual(self.data["target_control_effect"],"NONE_ALL_SIX_G893_TARGETS_REMAIN_PENDING_DIRECT_IMAGE")

if __name__=="__main__":
    unittest.main()
