from __future__ import annotations

import json
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from fortune_training.bazi_chart import (
    BaziChartFoundation,
    BaziChartRequest,
    bazi_foundation_v1_profile,
)
from fortune_training.bazi_temporal import (
    BaziSex,
    BaziTemporalEngine,
    BaziTemporalRequest,
    bazi_temporal_v1_continuous_profile,
)
from fortune_training.calendar_foundation import (
    BirthInput,
    ChineseCalendarEngine,
    CivilTimeResolver,
    PolicyRegistry,
    SolarTermEngine,
    TimeCalendarFoundation,
)
from fortune_training.calendar_foundation.bazi import BaziTimeResolver
from fortune_training.fusion_chart_acceptance import (
    AcceptanceHarness,
    AcceptanceLocation,
    DefectClass,
    deterministic_resolution_signature,
    require_combined_invariants,
)


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "tests" / "fixtures" / "fusion-chart-capability-golden-r1.json"


class FusionChartCapabilityAcceptanceR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
        cls.registry = PolicyRegistry.from_file(
            ROOT / "config" / "time-calendar-policies.json"
        )
        cls.foundation = TimeCalendarFoundation(cls.registry)
        cls.harness = AcceptanceHarness(ROOT)

    @staticmethod
    def _location(row: dict[str, object]) -> AcceptanceLocation:
        return AcceptanceLocation(
            str(row["place"]),
            float(row["latitude"]),
            float(row["longitude"]),
            str(row["timezone_id"]),
        )

    def test_corpus_governance_never_promotes_reference_to_authority(self) -> None:
        policy = self.corpus["policy"]
        self.assertFalse(policy["reference_implementations_are_authority"])
        self.assertEqual("CLOSED", policy["deterministic_product_state"])
        self.assertEqual(
            "NOT_YET_FORMALIZED",
            policy["ziwei_self_inward_transformation_direction"],
        )
        self.assertEqual(
            {item.value for item in DefectClass},
            set(policy["failure_classifications"]),
        )

    def test_golden_case_corpus(self) -> None:
        for row in self.corpus["cases"]:
            with self.subTest(case_id=row["id"]):
                kind = row["kind"]
                if kind == "STANDARD_COMBINED":
                    birth = self.harness.birth(
                        datetime.fromisoformat(row["local"]),
                        self._location(row),
                    )
                    first = self.harness.resolve_combined(birth, sex=row["sex"])
                    second = self.harness.resolve_combined(birth, sex=row["sex"])
                    self.assertEqual(row["expected_status"], first.status)
                    self.assertEqual(first, second)
                    self.assertEqual(
                        deterministic_resolution_signature(first),
                        deterministic_resolution_signature(second),
                    )
                    require_combined_invariants(first)
                elif kind == "TRUE_SOLAR_CROSS_DAY":
                    birth = BirthInput(
                        datetime.fromisoformat(row["local"]),
                        row["place"],
                        row["latitude"],
                        row["longitude"],
                        row["timezone_id"],
                    )
                    result = self.foundation.resolve(birth)
                    branch = result["branches"][0]
                    self.assertEqual(
                        row["expected_solar_date"],
                        branch["solar_time"]["local_apparent_solar_datetime"][:10],
                    )
                    lunar = branch["ziwei_calendar"]["effective_ziwei_lunar_date"]
                    self.assertEqual(
                        tuple(row["expected_lunar"]),
                        (
                            lunar["year"],
                            lunar["month"],
                            lunar["day"],
                            lunar["is_leap_month"],
                        ),
                    )
                    bazi = branch["bazi_time"]
                    self.assertEqual(
                        tuple(row["expected_bazi"]),
                        tuple(
                            bazi[key]
                            for key in (
                                "year_pillar",
                                "month_pillar",
                                "day_pillar",
                                "hour_pillar",
                            )
                        ),
                    )
                elif kind == "CIVIL_TIME":
                    birth = BirthInput(
                        datetime.fromisoformat(row["local"]),
                        row["place"],
                        row["latitude"],
                        row["longitude"],
                        row["timezone_id"],
                    )
                    result = CivilTimeResolver().resolve(birth)
                    self.assertEqual(row["expected_status"], result.status.value)
                    if "expected_candidate_count" in row:
                        self.assertEqual(row["expected_candidate_count"], len(result.candidates))
                    if "expected_utc_offset_seconds" in row:
                        self.assertEqual(
                            row["expected_utc_offset_seconds"],
                            result.selected_candidate.utc_offset_seconds,
                        )
                        self.assertEqual(
                            row["expected_dst_seconds"],
                            result.selected_candidate.daylight_saving_seconds,
                        )
                elif kind == "LUNAR_DATE":
                    lunar = ChineseCalendarEngine().from_gregorian_date(
                        date.fromisoformat(row["gregorian_date"])
                    )
                    self.assertEqual(
                        tuple(row["expected_lunar"]),
                        (lunar.year, lunar.month, lunar.day, lunar.is_leap_month),
                    )
                elif kind == "LATE_ZI":
                    local = datetime.fromisoformat(row["local"])
                    utc = local.replace(tzinfo=timezone(timedelta(hours=8))).astimezone(
                        timezone.utc
                    )
                    result = BaziTimeResolver().resolve(
                        utc,
                        local,
                        year_boundary_policy="START_OF_SPRING",
                        day_boundary_policy=row["day_boundary_policy"],
                        late_zi_hour_stem_policy=row["late_zi_hour_stem_policy"],
                    )
                    self.assertEqual(row["expected_day_pillar"], result.day_pillar)
                    if "expected_hour_pillar" in row:
                        self.assertEqual(row["expected_hour_pillar"], result.hour_pillar)
                elif kind == "SOLAR_TERM_BOUNDARY":
                    term = SolarTermEngine().term(
                        row["year"], row["longitude_degrees"]
                    ).utc_instant
                    resolver = BaziTimeResolver()
                    before = resolver.resolve(
                        term - timedelta(seconds=1),
                        datetime(row["year"], 2, 4, 20, 0),
                        year_boundary_policy="START_OF_SPRING",
                        day_boundary_policy="MIDNIGHT",
                        late_zi_hour_stem_policy="CLASSICAL_CONTINUOUS",
                    )
                    after = resolver.resolve(
                        term + timedelta(seconds=1),
                        datetime(row["year"], 2, 4, 21, 0),
                        year_boundary_policy="START_OF_SPRING",
                        day_boundary_policy="MIDNIGHT",
                        late_zi_hour_stem_policy="CLASSICAL_CONTINUOUS",
                    )
                    self.assertEqual(row["expected_before_year_pillar"], before.year_pillar)
                    self.assertEqual(row["expected_after_year_pillar"], after.year_pillar)
                    self.assertNotEqual(before.month_pillar, after.month_pillar)
                elif kind == "BAZI_DAYUN":
                    engine = BaziChartFoundation.from_repository(ROOT)
                    profile = bazi_foundation_v1_profile(engine.time_calendar.policy_registry)
                    birth = BirthInput(
                        datetime.fromisoformat(row["local"]),
                        "Beijing",
                        39.9042,
                        116.4074,
                        "Asia/Shanghai",
                    )
                    natal = engine.resolve_typed(BaziChartRequest(birth, profile))
                    self.assertEqual("RESOLVED", natal.status)
                    candidate = natal.candidates[0]
                    self.assertEqual(
                        tuple(row["expected_pillars"]),
                        tuple(item.ganzhi for item in candidate.chart.pillars),
                    )
                    temporal = BaziTemporalEngine().resolve_typed(
                        BaziTemporalRequest(
                            candidate,
                            BaziSex.MALE,
                            bazi_temporal_v1_continuous_profile(),
                            dayun_count=len(row["expected_dayun"]),
                        )
                    )
                    state = temporal.candidates[0].state
                    self.assertEqual(row["expected_direction"], state.direction.direction)
                    self.assertEqual(
                        tuple(row["expected_dayun"]),
                        tuple(item.ganzhi for item in state.dayun_frames),
                    )
                elif kind == "ZIWEI_LIMITS":
                    birth = self.harness.birth(
                        datetime.fromisoformat(row["local"]),
                        AcceptanceLocation("Beijing", 39.9042, 116.4074, "Asia/Shanghai"),
                    )
                    result = self.harness.resolve_combined(birth)
                    require_combined_invariants(result)
                    state = result.ziwei_bundle.temporal_state
                    self.assertEqual(row["expected_daxian_count"], len(state.daxian_frames))
                    self.assertEqual(row["expected_first_daxian_id"], state.daxian_frames[0].frame_id)
                    self.assertEqual(row["expected_last_daxian_id"], state.daxian_frames[-1].frame_id)
                    self.assertEqual(row["expected_first_minor_age"], state.minor_limit_frames[0].nominal_age)
                else:
                    self.fail(f"unsupported golden case kind: {kind}")


if __name__ == "__main__":
    unittest.main()
