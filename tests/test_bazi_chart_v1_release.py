from __future__ import annotations

import json
import subprocess
import sys
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

import jsonschema

from fortune_training.bazi_chart import (
    BaziChartFoundation,
    BaziChartRequest,
    bazi_foundation_v1_profile,
)
from fortune_training.calendar_foundation import BirthInput


ROOT = Path(__file__).resolve().parents[1]


class BaziChartV1ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = BaziChartFoundation.from_repository(ROOT)
        cls.profile = bazi_foundation_v1_profile(cls.engine.time_calendar.policy_registry)
        cls.birth = BirthInput(
            reported_local_datetime=datetime(1990, 6, 15, 12, 0),
            birth_place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id="Asia/Shanghai",
        )
        cls.request = BaziChartRequest(birth=cls.birth, profile=cls.profile)
        cls.schema = json.loads(
            (ROOT / "schemas" / "bazi-chart-foundation-v1.schema.json").read_text(encoding="utf-8")
        )

    def test_public_json_resolution_validates_against_published_schema(self):
        result = self.engine.resolve(self.request)
        jsonschema.Draft202012Validator.check_schema(self.schema)
        jsonschema.validate(result, self.schema)
        self.assertEqual("BAZI-CHART-FOUNDATION-RESULT-V1", result["schema"])
        self.assertEqual(1, len(result["charts"]))
        self.assertEqual(1, len(result["temporal_seeds"]))
        self.assertEqual(1, len(result["hashes"]))
        self.assertEqual(1, len(result["integrity_reports"]))

    def test_schema_tracks_all_registered_civil_ambiguity_policy_names(self):
        for policy_name in ("REJECT", "EARLIER_OFFSET", "LATER_OFFSET"):
            policies = replace(
                self.profile.time_calendar_policies,
                civil_ambiguous_time_policy=policy_name,
            )
            profile = replace(self.profile, time_calendar_policies=policies)
            result = self.engine.resolve(BaziChartRequest(birth=self.birth, profile=profile))
            jsonschema.validate(result, self.schema)
            self.assertEqual(policy_name, result["calculation_profile"]["time_calendar_policies"]["civil_ambiguous_time_policy"])

    def test_json_and_typed_contract_reference_same_natal_facts(self):
        typed = self.engine.resolve_typed(self.request)
        exported = self.engine.resolve(self.request)
        self.assertEqual(
            [row.ganzhi for row in typed.candidates[0].chart.pillars],
            [row["ganzhi"] for row in exported["charts"][0]["pillars"]],
        )
        self.assertEqual(typed.candidates[0].hashes.fact_hash, exported["hashes"][0]["fact_hash"])
        self.assertEqual(
            len(typed.candidates[0].temporal_seeds),
            len(exported["temporal_seeds"][0]),
        )

    def test_natal_export_contains_no_interpretive_fields(self):
        chart = self.engine.resolve(self.request)["charts"][0]
        prohibited = {
            "strength",
            "body_strength",
            "pattern",
            "useful_god",
            "favorable_elements",
            "unfavorable_elements",
            "root_strength",
            "shen_sha",
            "dayun",
        }
        self.assertTrue(prohibited.isdisjoint(chart))

    def test_example_script_emits_valid_foundation_json(self):
        process = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "bazi-chart-example.py")],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(process.stdout)
        jsonschema.validate(payload, self.schema)
        self.assertEqual("BAZI-CHART-FOUNDATION-RESULT-V1", payload["schema"])
        self.assertEqual(
            ["庚午", "壬午", "辛亥", "癸巳"],
            [row["ganzhi"] for row in payload["charts"][0]["pillars"]],
        )

    def test_profile_is_frozen_to_bazi_only_time_policy_view(self):
        profile = self.profile
        self.assertEqual("LOCAL_APPARENT_SOLAR", profile.time_coordinate_policy)
        self.assertFalse(hasattr(profile.time_calendar_policies, "ziwei_calendar_date_policy"))
        self.assertFalse(hasattr(profile.time_calendar_policies, "ziwei_life_body_leap_month_policy"))


if __name__ == "__main__":
    unittest.main()
