from __future__ import annotations

import unittest

from fortune_training.bazi_application.shensha import classical_shensha_for_pillars
from fortune_training.bazi_application.temporal_shensha import (
    SIMPLE_TARGET_KINDS,
    TEMPORAL_LAYERS,
    TEMPORAL_SHENSHA_PROFILE_ID,
    TEMPORAL_SHENSHA_PROFILE_VERSION,
    temporal_shensha_target_projection,
)
from fortune_training.bazi_chart.registries import (
    EARTHLY_BRANCHES,
    HEAVENLY_STEMS,
    SEXAGENARY_CYCLE,
)


class BaziTemporalShenshaSourceScopeProjectionAuditR1Tests(unittest.TestCase):
    @staticmethod
    def source() -> dict:
        return classical_shensha_for_pillars(
            {"YEAR": "甲戌", "MONTH": "己巳", "DAY": "癸卯", "HOUR": "己未"}
        )

    @staticmethod
    def _allowed(candidate: dict, layer: str) -> bool:
        if candidate["target_kind"] not in SIMPLE_TARGET_KINDS:
            return False
        if candidate["match_scope"] == "ALL_PILLARS":
            return layer in TEMPORAL_LAYERS
        if candidate["match_scope"] == "ONLY_DAY":
            return layer == "DAILY"
        return False

    @staticmethod
    def _target(ganzhi: str, kind: str) -> str:
        if kind == "STEM":
            return ganzhi[0]
        if kind == "BRANCH":
            return ganzhi[1]
        if kind == "GANZHI":
            return ganzhi
        raise AssertionError(f"unexpected target kind: {kind}")

    def _project(self, source: dict, ganzhi: str, *, dayun_kind: str = "DAYUN") -> dict:
        frames = {
            layer: {"frame_id": f"AUDIT:{layer}:{ganzhi}", "ganzhi": ganzhi}
            for layer in ("DAYUN", "XIAOYUN_A", "XIAOYUN_B", "ANNUAL", "MONTHLY", "DAILY", "HOURLY")
        }
        return temporal_shensha_target_projection(
            source,
            dayun_kind=dayun_kind,
            dayun_frame=frames["DAYUN"],
            xiaoyun_candidates=[
                {"profile_id": "AUDIT:XIAOYUN:A", "direction": "FORWARD", "active_frame": frames["XIAOYUN_A"]},
                {"profile_id": "AUDIT:XIAOYUN:B", "direction": "REVERSE", "active_frame": frames["XIAOYUN_B"]},
            ],
            annual_frame=frames["ANNUAL"],
            monthly_frame=frames["MONTHLY"],
            daily_frame=frames["DAILY"],
            hourly_frame=frames["HOURLY"],
        )

    def test_live_source_catalog_partition_and_profile_are_frozen(self) -> None:
        source = self.source()
        self.assertEqual("BAZI-CLASSICAL-SHENSHA-FACTS-R1", source["profile_id"])
        self.assertEqual("1.7.1", source["profile_version"])
        self.assertEqual(38, len(source["candidates"]))
        projection = self._project(source, "甲子")
        self.assertEqual(TEMPORAL_SHENSHA_PROFILE_ID, projection["profile_id"])
        self.assertEqual("1.0.0", TEMPORAL_SHENSHA_PROFILE_VERSION)
        self.assertEqual(32, len(projection["eligible_source_candidates"]))
        self.assertEqual(6, len(projection["excluded_source_candidates"]))
        source_ids = {row["candidate_id"] for row in source["candidates"]}
        partition_ids = {
            row["candidate_id"] for row in projection["eligible_source_candidates"]
        } | {
            row["candidate_id"] for row in projection["excluded_source_candidates"]
        }
        self.assertEqual(source_ids, partition_ids)

    def test_all_60_legal_targets_and_420_slots_exactly_replay_source_candidate_semantics(self) -> None:
        source = self.source()
        by_id = {row["candidate_id"]: row for row in source["candidates"]}
        evaluated_total = 0
        slot_total = 0
        for ganzhi in SEXAGENARY_CYCLE:
            projection = self._project(source, ganzhi)
            slots = [
                ("DAYUN", projection["dayun"]),
                ("XIAOYUN", projection["xiaoyun_candidates"][0]),
                ("XIAOYUN", projection["xiaoyun_candidates"][1]),
                ("ANNUAL", projection["annual"]),
                ("MONTHLY", projection["monthly"]),
                ("DAILY", projection["daily"]),
                ("HOURLY", projection["hourly"]),
            ]
            for layer, slot in slots:
                self.assertEqual("RESOLVED", slot["status"])
                expected_ids = []
                evaluated = 0
                for candidate in source["candidates"]:
                    if not self._allowed(candidate, layer):
                        continue
                    evaluated += 1
                    value = self._target(ganzhi, candidate["target_kind"])
                    if value in candidate["target_values"]:
                        expected_ids.append(candidate["candidate_id"])
                self.assertEqual(evaluated, slot["evaluated_candidate_count"])
                self.assertEqual(expected_ids, [row["source_candidate_id"] for row in slot["matches"]])
                for row in slot["matches"]:
                    original = by_id[row["source_candidate_id"]]
                    self.assertEqual(original["shensha_id"], row["shensha_id"])
                    self.assertEqual(original["anchor_basis"], row["anchor_basis"])
                    self.assertEqual(original["anchor_value"], row["anchor_value"])
                    self.assertEqual(original["target_kind"], row["target_kind"])
                    self.assertEqual(original["target_values"], row["target_values"])
                    self.assertEqual(original["match_scope"], row["source_match_scope"])
                    self.assertEqual(original["selection_status"], row["source_selection_status"])
                    self.assertEqual(original["qualification_status"], row["source_qualification_status"])
                    self.assertEqual(original["source_refs"], row["source_refs"])
                    self.assertEqual("NOT_CLASSICALLY_ARBITRATED", row["temporal_applicability_status"])
                evaluated_total += evaluated
                slot_total += 1
        self.assertEqual(420, slot_total)
        self.assertEqual(12000, evaluated_total)

    def test_only_day_and_structural_source_scopes_never_leak(self) -> None:
        source = self.source()
        structural_ids = {
            row["candidate_id"] for row in source["candidates"]
            if row["target_kind"] not in SIMPLE_TARGET_KINDS
        }
        only_day_ids = {
            row["candidate_id"] for row in source["candidates"]
            if row["match_scope"] == "ONLY_DAY"
        }
        self.assertEqual(6, len(structural_ids))
        self.assertEqual(4, len(only_day_ids))
        for ganzhi in SEXAGENARY_CYCLE:
            projection = self._project(source, ganzhi)
            for slot in [
                projection["dayun"],
                *projection["xiaoyun_candidates"],
                projection["annual"],
                projection["monthly"],
                projection["hourly"],
            ]:
                ids = {row["source_candidate_id"] for row in slot["matches"]}
                self.assertTrue(ids.isdisjoint(only_day_ids))
                self.assertTrue(ids.isdisjoint(structural_ids))
            daily_ids = {row["source_candidate_id"] for row in projection["daily"]["matches"]}
            self.assertTrue(daily_ids.isdisjoint(structural_ids))

    def test_candidate_and_temporal_semantic_firewalls_remain_explicit(self) -> None:
        source = self.source()
        projection = self._project(source, "庚子")
        self.assertEqual(
            "ENGINEERING_TARGET_MATCH_NOT_CLASSICAL_TEMPORAL_APPLICABILITY",
            projection["projection_policy"],
        )
        self.assertEqual("SOURCE_CANDIDATES_PRESERVED_NO_WINNER", projection["selection_semantics"])
        self.assertEqual(
            "TARGET_IDENTITY_MATCH_ONLY_NO_AUSPICIOUSNESS_OR_TEMPORAL_RULE_ADJUDICATION",
            projection["semantic_scope"],
        )
        tiande = [row for row in source["candidates"] if row["shensha_id"] == "TIANDE"]
        self.assertEqual(2, len(tiande))
        self.assertEqual({"ALL_PILLARS", "ONLY_DAY"}, {row["match_scope"] for row in tiande})
        self.assertTrue(all(row["selection_status"] == "CANDIDATE_NOT_ARBITRATED" for row in tiande))
        yuancheng = next(row for row in source["candidates"] if row["shensha_id"] == "YUANCHENG")
        self.assertIn("S11:YHZP-CH-015", yuancheng["source_refs"])
        self.assertNotIn("S12:YHZP-CH-016", yuancheng["source_refs"])

    def test_pre_dayun_and_all_60_illegal_ganzhi_fail_closed(self) -> None:
        source = self.source()
        projection = self._project(source, "甲子", dayun_kind="PRE_DAYUN")
        self.assertEqual("PRE_DAYUN_NO_GANZHI_PROJECTION", projection["dayun"]["status"])
        self.assertIsNone(projection["dayun"]["ganzhi"])
        self.assertEqual(2, len(projection["xiaoyun_candidates"]))
        illegal = {
            stem + branch
            for stem in HEAVENLY_STEMS
            for branch in EARTHLY_BRANCHES
        } - set(SEXAGENARY_CYCLE)
        self.assertEqual(60, len(illegal))
        for ganzhi in illegal:
            with self.assertRaises(ValueError):
                self._project(source, ganzhi)


if __name__ == "__main__":
    unittest.main()
