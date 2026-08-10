from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

import jsonschema

from fortune_training.bazi_chart import BaziChartFoundation, BaziChartRequest, bazi_foundation_v1_profile
from fortune_training.bazi_flow import BaziFlowEngine, BaziFlowRequest
from fortune_training.bazi_relation_transition import BaziRelationTransitionEngine, BaziRelationTransitionRequest, bazi_relation_transition_foundation_r1_profile
from fortune_training.bazi_structural import BaziStructuralEngine, BaziStructuralRequest, bazi_structural_context_r1_profile
from fortune_training.bazi_structural_support import BaziStructuralSupportEngine, BaziStructuralSupportRequest, bazi_structural_support_foundation_r1_profile
from fortune_training.bazi_temporal import BaziSex, BaziTemporalEngine, BaziTemporalRequest, bazi_temporal_v1_continuous_profile
from fortune_training.calendar_foundation import BirthInput


ROOT = Path(__file__).resolve().parents[1]


class BaziRelationTransitionFoundationR1ReleaseTests(unittest.TestCase):
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
        flow_engine = BaziFlowEngine(chart_engine.time_calendar.bazi)
        structural_engine = BaziStructuralEngine()
        support_engine = BaziStructuralSupportEngine()

        def stack(target):
            flow = flow_engine.resolve_typed(BaziFlowRequest(
                natal, temporal.candidates, target, chart_profile
            ))
            structural = structural_engine.resolve_typed(BaziStructuralRequest(
                natal, flow.candidates, bazi_structural_context_r1_profile()
            ))
            support = support_engine.resolve_typed(BaziStructuralSupportRequest(
                natal, flow.candidates, structural.candidates,
                bazi_structural_support_foundation_r1_profile()
            ))
            return flow, structural, support

        cls.before_target = datetime(2026, 10, 9, tzinfo=timezone.utc)
        cls.after_target = datetime(2026, 10, 10, tzinfo=timezone.utc)
        before = stack(cls.before_target)
        after = stack(cls.after_target)
        cls.natal = natal
        cls.before = before
        cls.after = after
        cls.profile = bazi_relation_transition_foundation_r1_profile()
        cls.engine = BaziRelationTransitionEngine()
        cls.request = BaziRelationTransitionRequest(
            natal,
            cls.before_target,
            cls.after_target,
            before[0].candidates,
            before[1].candidates,
            before[2].candidates,
            after[0].candidates,
            after[1].candidates,
            after[2].candidates,
            cls.profile,
        )
        cls.schema = json.loads((
            ROOT / "schemas" / "bazi-relation-transition-foundation-r1.schema.json"
        ).read_text(encoding="utf-8"))

    def test_public_json_validates_against_published_schema(self):
        payload = self.engine.resolve(self.request)
        jsonschema.Draft202012Validator.check_schema(self.schema)
        jsonschema.validate(payload, self.schema)
        self.assertEqual("BAZI-RELATION-TRANSITION-FOUNDATION-RESULT-V1", payload["schema"])
        self.assertEqual("RESOLVED", payload["status"])
        self.assertEqual("PASS", payload["candidates"][0]["integrity"]["status"])

    def test_public_contract_has_exact_neutral_states_and_no_lifecycle_leakage(self):
        payload = self.engine.resolve(self.request)
        context = payload["candidates"][0]["context"]
        self.assertEqual(
            {"PERSISTING"},
            {row["transition_state"] for row in context["transition_facts"]},
        )
        prohibited_keys = {
            "activated", "reactivated", "suppressed", "cancelled", "rescued",
            "released", "effective", "dominant", "strength", "weight",
            "winner", "loser", "transformation_success", "cause", "priority"
        }

        def keys(value):
            if isinstance(value, dict):
                return set(value) | set().union(*(keys(item) for item in value.values()))
            if isinstance(value, list):
                return set().union(*(keys(item) for item in value), set())
            return set()

        self.assertTrue(prohibited_keys.isdisjoint(keys(context)))
        self.assertEqual(
            self.natal.hashes.fact_hash,
            context["before_snapshot"]["upstream_natal_fact_hash"],
        )
        self.assertEqual(
            self.natal.hashes.fact_hash,
            context["after_snapshot"]["upstream_natal_fact_hash"],
        )

    def test_transition_hash_layer_is_independent_and_deterministic(self):
        first = self.engine.resolve_typed(self.request).candidates[0]
        second = self.engine.resolve_typed(self.request).candidates[0]
        self.assertEqual(first.hashes, second.hashes)
        self.assertEqual("BAZI-RELATION-TRANSITION-HASH-V1", first.hashes.algorithm_id)
        upstream_hashes = {
            self.natal.hashes.fact_hash,
            self.before[0].candidates[0].hashes.fact_hash,
            self.before[1].candidates[0].hashes.fact_hash,
            self.before[2].candidates[0].hashes.fact_hash,
            self.after[0].candidates[0].hashes.fact_hash,
            self.after[1].candidates[0].hashes.fact_hash,
            self.after[2].candidates[0].hashes.fact_hash,
        }
        self.assertNotIn(first.hashes.fact_hash, upstream_hashes)


if __name__ == "__main__":
    unittest.main()
