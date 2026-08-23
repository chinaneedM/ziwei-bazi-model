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


class ZiweiTargetDailyHourlyR1Tests(unittest.TestCase):
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
        self.assertTrue(all(len(row.auxiliary_activations) == 3 for row in rows))
        self.assertTrue(all(
            [item.display_name for item in row.auxiliary_activations] == ["禄存", "擎羊", "陀罗"]
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
