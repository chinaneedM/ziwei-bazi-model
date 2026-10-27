from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

import jsonschema

from fortune_training.bazi_chart import BaziChartFoundation, BaziChartRequest, bazi_foundation_v1_profile
from fortune_training.bazi_flow import BaziFlowEngine, BaziFlowRequest
from fortune_training.bazi_structural import BaziStructuralEngine, BaziStructuralRequest, bazi_structural_context_r1_profile
from fortune_training.bazi_structural_support import BaziStructuralSupportEngine, BaziStructuralSupportRequest, bazi_structural_support_foundation_r1_profile
from fortune_training.bazi_temporal import BaziSex, BaziTemporalEngine, BaziTemporalRequest, bazi_temporal_v1_continuous_profile
from fortune_training.calendar_foundation import BirthInput


ROOT = Path(__file__).resolve().parents[1]


class BaziStructuralSupportFoundationR1ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        chart_engine = BaziChartFoundation.from_repository(ROOT)
        chart_profile = bazi_foundation_v1_profile(chart_engine.time_calendar.policy_registry)
        natal = chart_engine.resolve_typed(BaziChartRequest(BirthInput(
            datetime(2025, 2, 7, 10, 10), "Beijing", 39.9042, 116.4074, "Asia/Shanghai"
        ), chart_profile)).candidates[0]
        temporal = BaziTemporalEngine().resolve_typed(BaziTemporalRequest(
            natal, BaziSex.MALE, bazi_temporal_v1_continuous_profile(), dayun_count=4
        ))
        flow = BaziFlowEngine(chart_engine.time_calendar.bazi).resolve_typed(BaziFlowRequest(
            natal, temporal.candidates, datetime(2026, 10, 9, tzinfo=timezone.utc), chart_profile
        ))
        structural = BaziStructuralEngine().resolve_typed(BaziStructuralRequest(
            natal, flow.candidates, bazi_structural_context_r1_profile()
        ))
        cls.natal = natal
        cls.flow = flow
        cls.structural = structural
        cls.profile = bazi_structural_support_foundation_r1_profile()
        cls.engine = BaziStructuralSupportEngine()
        cls.request = BaziStructuralSupportRequest(
            natal, flow.candidates, structural.candidates, cls.profile
        )
        cls.schema = json.loads((
            ROOT / "schemas" / "bazi-structural-support-foundation-r1.schema.json"
        ).read_text(encoding="utf-8"))

    def test_public_json_validates_against_published_schema(self):
        payload = self.engine.resolve(self.request)
        jsonschema.Draft202012Validator.check_schema(self.schema)
        jsonschema.validate(payload, self.schema)
        self.assertEqual("BAZI-STRUCTURAL-SUPPORT-FOUNDATION-RESULT-V1", payload["schema"])
        self.assertEqual("RESOLVED", payload["status"])
        self.assertEqual("PASS", payload["candidates"][0]["integrity"]["status"])

    def test_public_contract_keeps_roles_typed_and_excludes_interpretive_non_goals(self):
        payload = self.engine.resolve(self.request)
        context = payload["candidates"][0]["context"]
        self.assertEqual("NATAL_MONTH_COMMAND", context["natal_month_command"]["role_id"])
        self.assertEqual("ACTIVE_FLOW_SOLAR_MONTH", context["active_flow_solar_month"]["role_id"])
        self.assertEqual(self.natal.hashes.fact_hash, context["upstream_natal_fact_hash"])
        self.assertEqual(self.flow.candidates[0].hashes.fact_hash, context["upstream_flow_fact_hash"])
        self.assertEqual(self.structural.candidates[0].hashes.fact_hash, context["upstream_structural_fact_hash"])
        prohibited = {
            "root", "no_root", "root_strength", "strong_root", "weak_root",
            "hidden_stem_weight", "seasonal_score", "day_master_strength",
            "pattern", "useful_god", "tiao_hou", "transformation_success",
            "suppression", "reactivation", "shen_sha", "prediction", "ui"
        }
        self.assertTrue(prohibited.isdisjoint(context))
        self.assertTrue(all(
            prohibited.isdisjoint(row)
            for row in context["support_evidence_candidates"]
        ))

    def test_support_hash_layer_is_independent_and_deterministic(self):
        first = self.engine.resolve_typed(self.request).candidates[0]
        second = self.engine.resolve_typed(self.request).candidates[0]
        self.assertEqual(first.hashes, second.hashes)
        self.assertEqual("BAZI-STRUCTURAL-SUPPORT-HASH-V1", first.hashes.algorithm_id)
        self.assertNotEqual(first.hashes.fact_hash, self.natal.hashes.fact_hash)
        self.assertNotEqual(first.hashes.fact_hash, self.flow.candidates[0].hashes.fact_hash)
        self.assertNotEqual(first.hashes.fact_hash, self.structural.candidates[0].hashes.fact_hash)


if __name__ == "__main__":
    unittest.main()
