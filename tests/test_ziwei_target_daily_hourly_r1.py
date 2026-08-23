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

    def test_hourly_method_never_promotes_case_evidence_to_active_frame(self) -> None:
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
        self.assertTrue(all(row.active_address is None for row in rows))
        self.assertTrue(all(row.authority_status == "CASE_METHOD_ONLY_NOT_GLOBAL_RULE" for row in rows))
        self.assertTrue(all("S01:ZZZA-CF-001" in row.source_refs for row in rows))
        self.assertEqual("ZHONGZHOU_LUOYANG_MEAN_SOLAR_TIME", rows[0].time_standard)
        self.assertEqual(datetime(2026, 11, 15, 12, 44, 44), rows[0].source_local_datetime)
        self.assertTrue(all(row.transformation_status == "CASE_METHOD_PROFILE_TRANSFORMATIONS_DISABLED" for row in rows))
        self.assertTrue(all(row.transformations == () for row in rows))


if __name__ == "__main__":
    unittest.main()
