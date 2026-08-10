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
from fortune_training.bazi_relation_incidence import (
    BaziRelationIncidenceEngine,
    BaziRelationIncidenceRequest,
    bazi_relation_incidence_foundation_r1_profile,
)
from fortune_training.bazi_structural import (
    BaziStructuralEngine,
    BaziStructuralRequest,
    bazi_structural_context_r1_profile,
)
from fortune_training.bazi_structural_support import (
    BaziStructuralSupportEngine,
    BaziStructuralSupportRequest,
    bazi_structural_support_foundation_r1_profile,
)
from fortune_training.bazi_temporal import (
    BaziSex,
    BaziTemporalEngine,
    BaziTemporalRequest,
    bazi_temporal_v1_continuous_profile,
)
from fortune_training.calendar_foundation import BirthInput


ROOT = Path(__file__).resolve().parents[1]


class BaziRelationIncidenceFoundationR1ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        chart_engine = BaziChartFoundation.from_repository(ROOT)
        chart_profile = bazi_foundation_v1_profile(
            chart_engine.time_calendar.policy_registry
        )
        natal = chart_engine.resolve_typed(BaziChartRequest(
            BirthInput(
                datetime(2025, 2, 7, 10, 10),
                "Beijing",
                39.9042,
                116.4074,
                "Asia/Shanghai",
            ),
            chart_profile,
        )).candidates[0]
        temporal = BaziTemporalEngine().resolve_typed(BaziTemporalRequest(
            natal,
            BaziSex.MALE,
            bazi_temporal_v1_continuous_profile(),
            dayun_count=4,
        ))
        target = datetime(2026, 10, 9, tzinfo=timezone.utc)
        flow = BaziFlowEngine(chart_engine.time_calendar.bazi).resolve_typed(
            BaziFlowRequest(natal, temporal.candidates, target, chart_profile)
        )
        structural = BaziStructuralEngine().resolve_typed(BaziStructuralRequest(
            natal, flow.candidates, bazi_structural_context_r1_profile()
        ))
        support = BaziStructuralSupportEngine().resolve_typed(
            BaziStructuralSupportRequest(
                natal,
                flow.candidates,
                structural.candidates,
                bazi_structural_support_foundation_r1_profile(),
            )
        )
        cls.natal = natal
        cls.flow = flow
        cls.structural = structural
        cls.support = support
        cls.target = target
        cls.profile = bazi_relation_incidence_foundation_r1_profile()
        cls.engine = BaziRelationIncidenceEngine()
        cls.request = BaziRelationIncidenceRequest(
            natal,
            target,
            flow.candidates,
            structural.candidates,
            support.candidates,
            cls.profile,
        )
        cls.schema = json.loads((
            ROOT / "schemas" / "bazi-relation-incidence-foundation-r1.schema.json"
        ).read_text(encoding="utf-8"))

    def test_public_json_validates_against_published_schema(self):
        payload = self.engine.resolve(self.request)
        jsonschema.Draft202012Validator.check_schema(self.schema)
        jsonschema.validate(payload, self.schema)
        self.assertEqual(
            "BAZI-RELATION-INCIDENCE-FOUNDATION-RESULT-V1",
            payload["schema"],
        )
        self.assertEqual("RESOLVED", payload["status"])
        self.assertEqual("PASS", payload["candidates"][0]["integrity"]["status"])

    def test_public_contract_is_exact_id_topology_without_interpretive_leakage(self):
        payload = self.engine.resolve(self.request)
        context = payload["candidates"][0]["context"]
        self.assertEqual(
            {"SHARED_PARTICIPANT", "DISJOINT"},
            {row["topology_kind"] for row in context["relation_pair_topology_facts"]},
        )
        self.assertTrue(all(
            row["relation_count"] == len(row["relation_ids"])
            for row in context["participant_incidence_facts"]
        ))
        prohibited_keys = {
            "activated", "reactivated", "suppressed", "cancelled", "rescued",
            "released", "conflicting", "competing", "interacting", "binding",
            "effective", "dominant", "strength", "pressure", "weight",
            "priority", "winner", "loser", "transformation_success",
            "transformation_succeeded", "cause"
        }

        def keys(value):
            if isinstance(value, dict):
                return set(value) | set().union(*(keys(item) for item in value.values()))
            if isinstance(value, list):
                return set().union(*(keys(item) for item in value), set())
            return set()

        self.assertTrue(prohibited_keys.isdisjoint(keys(context)))

    def test_snapshot_replays_released_relation_universe_and_hash_is_independent(self):
        first = self.engine.resolve_typed(self.request).candidates[0]
        second = self.engine.resolve_typed(self.request).candidates[0]
        self.assertEqual(first.hashes, second.hashes)
        self.assertEqual("BAZI-RELATION-INCIDENCE-HASH-V1", first.hashes.algorithm_id)
        expected_ids = tuple(sorted(
            [row.relation_id for row in self.natal.chart.raw_relations]
            + [
                row.relation_id
                for row in self.structural.candidates[0].context.dynamic_raw_relations
            ]
        ))
        self.assertEqual(expected_ids, first.context.snapshot.raw_relation_ids)
        upstream_hashes = {
            self.natal.hashes.fact_hash,
            self.flow.candidates[0].hashes.fact_hash,
            self.structural.candidates[0].hashes.fact_hash,
            self.support.candidates[0].hashes.fact_hash,
        }
        self.assertNotIn(first.hashes.fact_hash, upstream_hashes)


if __name__ == "__main__":
    unittest.main()
