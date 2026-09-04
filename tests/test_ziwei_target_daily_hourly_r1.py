from __future__ import annotations

import unittest
from datetime import date, datetime, timezone
from types import SimpleNamespace

from fortune_training.calendar_foundation import (
    BaziTimeResolver,
    five_rats_hour_pillar,
    sexagenary_day_pillar,
)
from fortune_training.ziwei_chart import ZiweiTargetTemporalEngine
from fortune_training.ziwei_chart.temporal_auxiliary import TemporalAuxiliaryGenerator


class ZiweiTargetDailyHourlyR1Tests(unittest.TestCase):
    def test_kui_yue_methods_are_preserved_without_result_deduplication(self) -> None:
        for stem in "甲乙丙丁戊己庚辛壬癸":
            with self.subTest(stem=stem):
                candidate_set = TemporalAuxiliaryGenerator.kui_yue_candidate_set(
                    stem,
                    source_layer="ANNUAL",
                    context_id=f"ANNUAL:{stem}",
                    temporal_source_refs=("S10:TEST-CONTEXT",),
                )
                self.assertEqual("CANDIDATES_PRESERVED_NO_SELECTION", candidate_set.selection_status)
                self.assertEqual(("STAR.TIANKUI", "STAR.TIANYUE"), candidate_set.entity_ids)
                self.assertEqual(2, len(candidate_set.method_candidates))
                strict, wenmo = candidate_set.method_candidates
                self.assertEqual("S01-QS-STRICT-KUI-YUE-R1", strict.method_id)
                self.assertEqual("COMPAT-WENMO-KUI-YUE-R1", wenmo.method_id)
                self.assertNotEqual(strict.candidate_id, wenmo.candidate_id)
                self.assertEqual(4, len({row.activation_id for method in candidate_set.method_candidates for row in method.activations}))
                self.assertTrue(all(len(value) == 64 for value in (
                    candidate_set.fact_hash,
                    candidate_set.computation_hash,
                    strict.fact_hash,
                    strict.computation_hash,
                    wenmo.fact_hash,
                    wenmo.computation_hash,
                )))
                strict_branches = tuple(row.target_address.branch for row in strict.activations)
                wenmo_branches = tuple(row.target_address.branch for row in wenmo.activations)
                if stem == "辛":
                    self.assertEqual(("午", "寅"), strict_branches)
                    self.assertEqual(("寅", "午"), wenmo_branches)
                else:
                    self.assertEqual(strict_branches, wenmo_branches)

    def test_s10_flow_chang_qu_table_is_exact_for_all_ten_stems(self) -> None:
        expected = {
            "甲": ("巳", "酉"), "乙": ("午", "申"), "丙": ("申", "午"),
            "丁": ("酉", "巳"), "戊": ("申", "午"), "己": ("酉", "巳"),
            "庚": ("亥", "卯"), "辛": ("子", "寅"), "壬": ("寅", "子"),
            "癸": ("卯", "亥"),
        }
        for stem, branches in expected.items():
            with self.subTest(stem=stem):
                rows = TemporalAuxiliaryGenerator.activate(
                    stem,
                    source_layer="ANNUAL",
                    context_id=f"ANNUAL:{stem}",
                    temporal_source_refs=("S10:TEST-CONTEXT",),
                )
                self.assertEqual(5, len(rows))
                self.assertEqual(branches, tuple(row.target_address.branch for row in rows[-2:]))
                self.assertEqual(("STAR.WENCHANG", "STAR.WENQU"), tuple(row.entity_id for row in rows[-2:]))
                self.assertEqual(
                    {"S10-STEM-FLOW-WENCHANG-WENQU-R1"},
                    {row.rule_id for row in rows[-2:]},
                )
                self.assertTrue(all("S10:ZZZA-A-1103" in row.source_refs for row in rows[-2:]))
                self.assertNotIn(rows[-2].target_address.branch, "丑辰未戌")
                self.assertNotIn(rows[-1].target_address.branch, "丑辰未戌")

    def test_shared_sexagenary_primitives_preserve_bazi_outputs(self) -> None:
        resolver = BaziTimeResolver()
        local = datetime(2026, 8, 18, 23, 30)
        effective = date(2026, 8, 19)
        self.assertEqual(sexagenary_day_pillar(effective), "乙丑")
        self.assertEqual(five_rats_hour_pillar(local, effective), "丙子")

    def test_ziwei_boundary_is_an_explicit_engine_input(self) -> None:
        engine = ZiweiTargetTemporalEngine()
        local = datetime(2026, 8, 18, 23, 30)
        self.assertEqual(date(2026, 8, 18), engine.effective_gregorian_date(local, "MIDNIGHT"))
        self.assertEqual(date(2026, 8, 19), engine.effective_gregorian_date(local, "ZI_START_23"))

    def test_hourly_method_preserves_case_scoped_active_address_candidates(self) -> None:
        rows = ZiweiTargetTemporalEngine().hourly_method_candidates(
            target_utc=datetime(2026, 11, 15, 5, 15, tzinfo=timezone.utc),
            local_apparent_solar_datetime=datetime(2026, 11, 15, 13, 1),
            ziwei_day_boundary_policy="ZI_START_23",
            profile=SimpleNamespace(
                transformation_rule_set_id=None,
                transformation_rule_set_version=None,
            ),
            placements=(),
        )
        self.assertEqual(2, len(rows))
        self.assertEqual({"未", "午"}, {row.hour_branch for row in rows})
        self.assertEqual([row.hour_branch for row in rows], [row.active_address.branch for row in rows])
        self.assertTrue(all(len(row.designation_overlay) == 12 for row in rows))
        self.assertTrue(all(row.designation_overlay[0].address == row.active_address for row in rows))
        self.assertTrue(all(row.frame_status == "CASE_METHOD_ACTIVE_ADDRESS_CANDIDATE_NO_COMPLETE_CHART" for row in rows))
        self.assertTrue(all(row.active_address_rule_id == "S10-CASE-HOUR-BRANCH-ACTIVE-ADDRESS-CANDIDATE-R1" for row in rows))
        self.assertTrue(all("S10:ZZTERM-P-0316" in row.active_address_source_refs for row in rows))
        self.assertTrue(all(row.auxiliary_status == "CASE_METHOD_SOURCE_RULE_RESOLVED" for row in rows))
        self.assertTrue(all(len(row.auxiliary_activations) == 5 for row in rows))
        self.assertTrue(all(
            [item.display_name for item in row.auxiliary_activations] == ["禄存", "擎羊", "陀罗", "文昌", "文曲"]
            for row in rows
        ))
        self.assertTrue(all(
            {item.source_stem for item in row.auxiliary_activations} == {row.hour_ganzhi[0]}
            for row in rows
        ))
        self.assertTrue(all(row.authority_status == "CASE_METHOD_ONLY_NOT_GLOBAL_RULE" for row in rows))
        self.assertTrue(all("S01:ZZZA-CF-001" in row.source_refs for row in rows))
        self.assertEqual("ZHONGZHOU_LUOYANG_MEAN_SOLAR_TIME", rows[0].time_standard)
        self.assertEqual(datetime(2026, 11, 15, 12, 44, 44), rows[0].source_local_datetime)
        self.assertTrue(all(row.transformation_status == "CASE_METHOD_PROFILE_TRANSFORMATIONS_DISABLED" for row in rows))
        self.assertTrue(all(row.transformations == () for row in rows))


if __name__ == "__main__":
    unittest.main()
