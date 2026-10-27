from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

import jsonschema

from fortune_training.bazi_chart import (
    BaziChartFoundation,
    BaziChartRequest,
    bazi_foundation_v1_profile,
)
from fortune_training.bazi_flow import BaziFlowEngine, BaziFlowRequest
from fortune_training.bazi_temporal import (
    BaziSex,
    BaziTemporalEngine,
    BaziTemporalRequest,
    bazi_temporal_v1_continuous_profile,
)
from fortune_training.calendar_foundation import BirthInput


ROOT = Path(__file__).resolve().parents[1]


class BaziFlowContextR1ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        chart_engine = BaziChartFoundation.from_repository(ROOT)
        cls.profile = bazi_foundation_v1_profile(chart_engine.time_calendar.policy_registry)
        natal = chart_engine.resolve_typed(
            BaziChartRequest(
                BirthInput(
                    reported_local_datetime=datetime(2025, 2, 7, 10, 10),
                    birth_place="Beijing",
                    latitude=39.9042,
                    longitude=116.4074,
                    timezone_id="Asia/Shanghai",
                ),
                cls.profile,
            )
        )
        cls.natal = natal.candidates[0]
        cls.temporal = BaziTemporalEngine().resolve_typed(
            BaziTemporalRequest(
                cls.natal,
                BaziSex.MALE,
                bazi_temporal_v1_continuous_profile(),
                dayun_count=4,
            )
        )
        cls.engine = BaziFlowEngine(chart_engine.time_calendar.bazi)
        cls.request = BaziFlowRequest(
            cls.natal,
            cls.temporal.candidates,
            datetime(2026, 6, 1, tzinfo=timezone.utc),
            cls.profile,
        )
        cls.schema = json.loads(
            (ROOT / "schemas" / "bazi-flow-context-v1.schema.json").read_text(encoding="utf-8")
        )

    def test_public_json_validates_against_published_schema(self):
        payload = self.engine.resolve(self.request)
        jsonschema.Draft202012Validator.check_schema(self.schema)
        jsonschema.validate(payload, self.schema)
        self.assertEqual("BAZI-FLOW-CONTEXT-RESULT-V1", payload["schema"])
        self.assertEqual("RESOLVED", payload["status"])
        self.assertEqual("PASS", payload["candidates"][0]["integrity"]["status"])

    def test_flow_context_does_not_embed_interpretation_or_mutate_upstream(self):
        payload = self.engine.resolve(self.request)
        context = payload["candidates"][0]["context"]
        prohibited = {
            "dynamic_relations", "strength", "pattern", "useful_god", "tiao_hou",
            "shen_sha", "daily_frame", "hourly_frame", "prediction",
        }
        self.assertTrue(prohibited.isdisjoint(context))
        self.assertEqual(self.natal.hashes.fact_hash, context["upstream_natal_fact_hash"])
        self.assertEqual(
            self.temporal.candidates[0].hashes.fact_hash,
            context["upstream_temporal_fact_hash"],
        )


if __name__ == "__main__":
    unittest.main()
