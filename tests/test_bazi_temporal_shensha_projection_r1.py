from __future__ import annotations

import copy
import unittest

from fortune_training.bazi_application.shensha import classical_shensha_for_pillars
from fortune_training.bazi_application.temporal_shensha import (
    TEMPORAL_SHENSHA_PROFILE_ID,
    temporal_shensha_target_projection,
    validate_temporal_shensha_target_projection,
)


class BaziTemporalShenshaProjectionR1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = classical_shensha_for_pillars(
            {
                "YEAR": "甲戌",
                "MONTH": "己巳",
                "DAY": "癸卯",
                "HOUR": "己未",
            }
        )
        self.xiaoyun = [
            {
                "profile_id": "XIAOYUN-A",
                "direction": "FORWARD",
                "active_frame": {"frame_id": "XY:A", "ganzhi": "乙巳"},
                "activation_status": "OPERATIONAL_CIVIL_NOMINAL_AGE_MATCH",
            },
            {
                "profile_id": "XIAOYUN-B",
                "direction": "REVERSE",
                "active_frame": None,
                "activation_status": "OUTSIDE_MATERIALIZED_XIAOYUN_RANGE",
            },
        ]

    def project(self, *, annual: str = "甲午", daily: str = "甲午", dayun_kind: str = "DAYUN") -> dict:
        return temporal_shensha_target_projection(
            self.source,
            dayun_kind=dayun_kind,
            dayun_frame={"frame_id": "DU:1", "ganzhi": "丁未"},
            xiaoyun_candidates=self.xiaoyun,
            annual_frame={"frame_id": "Y:1", "ganzhi": annual},
            monthly_frame={"frame_id": "M:1", "ganzhi": "庚子"},
            daily_frame={"frame_id": "D:1", "ganzhi": daily},
            hourly_frame={"frame_id": "H:1", "ganzhi": "丁未"},
        )

    def source_candidate_id(self, shensha_id: str, *, match_scope: str | None = None) -> str:
        rows = [
            row for row in self.source["candidates"]
            if row["shensha_id"] == shensha_id
            and (match_scope is None or row["match_scope"] == match_scope)
        ]
        self.assertEqual(1, len(rows))
        return rows[0]["candidate_id"]

    @staticmethod
    def match_ids(slot: dict) -> set[str]:
        return {row["source_candidate_id"] for row in slot["matches"]}

    def test_projection_is_engineering_target_match_not_classical_temporal_adjudication(self) -> None:
        result = self.project()
        self.assertEqual(TEMPORAL_SHENSHA_PROFILE_ID, result["profile_id"])
        self.assertEqual("1.0.0", result["profile_version"])
        self.assertEqual("1.6.0", result["source_shensha_profile_version"])
        self.assertEqual(
            "ENGINEERING_TARGET_MATCH_NOT_CLASSICAL_TEMPORAL_APPLICABILITY",
            result["projection_policy"],
        )
        self.assertEqual("SOURCE_CANDIDATES_PRESERVED_NO_WINNER", result["selection_semantics"])
        self.assertEqual(
            "TARGET_IDENTITY_MATCH_ONLY_NO_AUSPICIOUSNESS_OR_TEMPORAL_RULE_ADJUDICATION",
            result["semantic_scope"],
        )
        for layer in ("dayun", "annual", "monthly", "daily", "hourly"):
            for row in result[layer]["matches"]:
                self.assertEqual("NOT_CLASSICALLY_ARBITRATED", row["temporal_applicability_status"])
                self.assertTrue(row["source_refs"])

    def test_simple_source_targets_project_but_structural_rules_are_explicitly_excluded(self) -> None:
        result = self.project()
        self.assertEqual(29, len(result["eligible_source_candidates"]))
        self.assertEqual(6, len(result["excluded_source_candidates"]))
        self.assertEqual(26, result["dayun"]["evaluated_candidate_count"])
        self.assertEqual(29, result["daily"]["evaluated_candidate_count"])

        excluded_ids = {row["shensha_id"] for row in result["excluded_source_candidates"]}
        self.assertEqual({"SANQI", "JIALU", "YUANCHENG"}, excluded_ids)
        all_match_ids = {
            row["shensha_id"]
            for layer in ("dayun", "annual", "monthly", "daily", "hourly")
            for row in result[layer]["matches"]
        }
        self.assertTrue({"SANQI", "JIALU", "YUANCHENG"}.isdisjoint(all_match_ids))

        tianguan_id = self.source_candidate_id("TIANGUAN")
        self.assertIn(tianguan_id, self.match_ids(result["dayun"]))
        tianguan_match = next(
            row for row in result["dayun"]["matches"]
            if row["source_candidate_id"] == tianguan_id
        )
        self.assertEqual("未", tianguan_match["matched_value"])
        self.assertEqual("YEAR_STEM", tianguan_match["anchor_basis"])

    def test_only_day_source_scope_never_leaks_to_non_daily_temporal_layers(self) -> None:
        result = self.project(annual="甲午", daily="甲午")
        tianshe_id = self.source_candidate_id("TIANSHE")
        self.assertNotIn(tianshe_id, self.match_ids(result["annual"]))
        self.assertIn(tianshe_id, self.match_ids(result["daily"]))

        yuede_projection = self.project(annual="庚子", daily="庚子")
        yuede_id = self.source_candidate_id("YUEDE")
        self.assertNotIn(yuede_id, self.match_ids(yuede_projection["annual"]))
        self.assertIn(yuede_id, self.match_ids(yuede_projection["daily"]))

        daily_only_yuedehe = self.source_candidate_id("YUEDEHE", match_scope="ONLY_DAY")
        all_pillars_yuedehe = self.source_candidate_id("YUEDEHE", match_scope="ALL_PILLARS")
        self.assertNotIn(daily_only_yuedehe, self.match_ids(yuede_projection["annual"]))
        self.assertIn(daily_only_yuedehe, self.match_ids(yuede_projection["daily"]))
        self.assertIn(all_pillars_yuedehe, self.match_ids(yuede_projection["annual"]))
        self.assertIn(all_pillars_yuedehe, self.match_ids(yuede_projection["daily"]))

    def test_xiaoyun_candidates_and_pre_dayun_status_remain_unmerged(self) -> None:
        result = self.project(dayun_kind="PRE_DAYUN")
        self.assertEqual("PRE_DAYUN_NO_GANZHI_PROJECTION", result["dayun"]["status"])
        self.assertIsNone(result["dayun"]["ganzhi"])
        self.assertEqual(2, len(result["xiaoyun_candidates"]))
        self.assertEqual("RESOLVED", result["xiaoyun_candidates"][0]["status"])
        self.assertEqual(
            "OUTSIDE_MATERIALIZED_XIAOYUN_RANGE",
            result["xiaoyun_candidates"][1]["status"],
        )
        self.assertEqual("XIAOYUN-A", result["xiaoyun_candidates"][0]["profile_id"])
        self.assertEqual("XIAOYUN-B", result["xiaoyun_candidates"][1]["profile_id"])

    def test_projection_hashes_are_deterministic_and_tamper_replay_fails(self) -> None:
        first = self.project()
        second = self.project()
        self.assertEqual(first, second)
        self.assertEqual(64, len(first["fact_hash"]))
        self.assertEqual(64, len(first["computation_hash"]))
        self.assertTrue(
            validate_temporal_shensha_target_projection(
                first,
                self.source,
                dayun_kind="DAYUN",
                dayun_frame={"frame_id": "DU:1", "ganzhi": "丁未"},
                xiaoyun_candidates=self.xiaoyun,
                annual_frame={"frame_id": "Y:1", "ganzhi": "甲午"},
                monthly_frame={"frame_id": "M:1", "ganzhi": "庚子"},
                daily_frame={"frame_id": "D:1", "ganzhi": "甲午"},
                hourly_frame={"frame_id": "H:1", "ganzhi": "丁未"},
            )
        )
        tampered = copy.deepcopy(first)
        tampered["dayun"]["matches"][0]["matched_value"] = "子"
        self.assertFalse(
            validate_temporal_shensha_target_projection(
                tampered,
                self.source,
                dayun_kind="DAYUN",
                dayun_frame={"frame_id": "DU:1", "ganzhi": "丁未"},
                xiaoyun_candidates=self.xiaoyun,
                annual_frame={"frame_id": "Y:1", "ganzhi": "甲午"},
                monthly_frame={"frame_id": "M:1", "ganzhi": "庚子"},
                daily_frame={"frame_id": "D:1", "ganzhi": "甲午"},
                hourly_frame={"frame_id": "H:1", "ganzhi": "丁未"},
            )
        )


if __name__ == "__main__":
    unittest.main()
