from __future__ import annotations

import json
import subprocess
import sys
import unittest
from datetime import datetime
from pathlib import Path

import jsonschema

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
from fortune_training.calendar_foundation import BirthInput


ROOT = Path(__file__).resolve().parents[1]


class BaziTemporalV1ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.chart_engine = BaziChartFoundation.from_repository(ROOT)
        chart_profile = bazi_foundation_v1_profile(cls.chart_engine.time_calendar.policy_registry)
        natal = cls.chart_engine.resolve_typed(
            BaziChartRequest(
                birth=BirthInput(
                    reported_local_datetime=datetime(2025, 2, 7, 10, 10),
                    birth_place="Beijing",
                    latitude=39.9042,
                    longitude=116.4074,
                    timezone_id="Asia/Shanghai",
                ),
                profile=chart_profile,
            )
        )
        if len(natal.candidates) != 1:
            raise RuntimeError(f"release fixture requires one natal candidate: {natal.status}")
        cls.candidate = natal.candidates[0]
        cls.profile = bazi_temporal_v1_continuous_profile()
        cls.engine = BaziTemporalEngine()
        cls.request = BaziTemporalRequest(
            candidate=cls.candidate,
            sex=BaziSex.MALE,
            profile=cls.profile,
            dayun_count=8,
        )
        cls.schema = json.loads(
            (ROOT / "schemas" / "bazi-temporal-v1.schema.json").read_text(encoding="utf-8")
        )

    def test_public_json_resolution_validates_against_schema(self):
        result = self.engine.resolve(self.request)
        jsonschema.Draft202012Validator.check_schema(self.schema)
        jsonschema.validate(result, self.schema)
        self.assertEqual("BAZI-TEMPORAL-RESULT-V1", result["schema"])
        self.assertEqual("BAZI-TEMPORAL-TYPED-RESOLUTION-V1", result["typed_schema"])
        self.assertEqual("RESOLVED", result["status"])
        self.assertEqual(1, len(result["candidates"]))
        self.assertEqual(8, len(result["candidates"][0]["state"]["dayun_frames"]))

    def test_json_and_typed_contract_share_hashes_and_boundaries(self):
        typed = self.engine.resolve_typed(self.request)
        exported = self.engine.resolve(self.request)
        self.assertEqual(typed.candidates[0].hashes.fact_hash, exported["candidates"][0]["hashes"]["fact_hash"])
        self.assertEqual(
            typed.candidates[0].state.jiaoyun.first_transition_utc.isoformat().replace("+00:00", "Z"),
            exported["candidates"][0]["state"]["jiaoyun"]["first_transition_utc"],
        )
        self.assertEqual(
            [frame.ganzhi for frame in typed.candidates[0].state.dayun_frames],
            [frame["ganzhi"] for frame in exported["candidates"][0]["state"]["dayun_frames"]],
        )

    def test_release_export_contains_no_annual_monthly_or_interpretation_state(self):
        state = self.engine.resolve(self.request)["candidates"][0]["state"]
        prohibited = {
            "annual_frames",
            "monthly_frames",
            "strength",
            "pattern",
            "useful_god",
            "shen_sha",
            "dynamic_relations",
        }
        self.assertTrue(prohibited.isdisjoint(state))

    def test_operational_realization_is_explicitly_non_classical_default_claim(self):
        result = self.engine.resolve(self.request)
        profile = result["calculation_profile"]
        self.assertEqual("MODERN_CONTINUOUS_RATIO_120X", profile["calendar_realization_rule_set"])
        self.assertEqual("ENGINEERING_INTERPOLATION", profile["calendar_realization_source_class"])
        self.assertEqual("FAIL_CLOSED", profile["exact_jie_tie_policy"])

    def test_example_script_emits_schema_valid_temporal_result(self):
        process = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "bazi-temporal-example.py")],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(process.stdout)
        jsonschema.validate(payload, self.schema)
        self.assertEqual("REVERSE", payload["candidates"][0]["state"]["direction"]["direction"])
        self.assertEqual("丁丑", payload["candidates"][0]["state"]["dayun_frames"][0]["ganzhi"])


if __name__ == "__main__":
    unittest.main()
