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
from fortune_training.bazi_stem_relation_positional import (
    BaziStemRelationPositionalEngine,
    BaziStemRelationPositionalRequest,
    bazi_stem_relation_positional_context_foundation_r1_profile,
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


class BaziStemRelationPositionalContextFoundationR1ReleaseTests(unittest.TestCase):
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
        target = datetime(2026, 2, 15, tzinfo=timezone.utc)
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
        incidence = BaziRelationIncidenceEngine().resolve_typed(
            BaziRelationIncidenceRequest(
                natal,
                target,
                flow.candidates,
                structural.candidates,
                support.candidates,
                bazi_relation_incidence_foundation_r1_profile(),
            )
        )
        cls.natal = natal
        cls.flow = flow
        cls.structural = structural
        cls.support = support
        cls.incidence = incidence
        cls.engine = BaziStemRelationPositionalEngine()
        cls.profile = bazi_stem_relation_positional_context_foundation_r1_profile()
        cls.request = BaziStemRelationPositionalRequest(
            natal, structural.candidates, incidence.candidates, cls.profile
        )
        cls.schema = json.loads((
            ROOT
            / "schemas"
            / "bazi-stem-relation-positional-context-foundation-r1.schema.json"
        ).read_text(encoding="utf-8"))

    def test_public_json_validates_against_published_schema(self):
        payload = self.engine.resolve(self.request)
        jsonschema.Draft202012Validator.check_schema(self.schema)
        jsonschema.validate(payload, self.schema)
        self.assertEqual(
            "BAZI-STEM-RELATION-POSITIONAL-CONTEXT-FOUNDATION-RESULT-V1",
            payload["schema"],
        )
        self.assertEqual("RESOLVED", payload["status"])
        self.assertEqual("PASS", payload["candidates"][0]["integrity"]["status"])

    def test_public_contract_contains_only_neutral_coordinate_facts(self):
        payload = self.engine.resolve(self.request)
        context = payload["candidates"][0]["context"]
        prohibited = {
            "near", "far", "blocked", "unblocked", "intervened", "engaged",
            "not_engaged", "pairing_success", "pairing_failure", "first_claim",
            "priority", "competes", "winner", "loser", "transformed",
            "not_transformed", "activated", "suppressed", "cancelled",
            "released", "strength", "root_grade", "prediction",
        }

        def keys(value):
            if isinstance(value, dict):
                return set(value) | set().union(*(keys(item) for item in value.values()))
            if isinstance(value, list):
                return set().union(*(keys(item) for item in value), set())
            return set()

        self.assertTrue(prohibited.isdisjoint(keys(context)))
        self.assertTrue(context["stem_pair_positional_facts"])
        for row in context["stem_pair_positional_facts"]:
            self.assertFalse(row["natal_linear_order_comparable"])
            self.assertIsNone(row["natal_ordinal_distance"])
            self.assertEqual([], row["intervening_natal_visible_stem_instance_ids"])

    def test_positional_hashes_are_independent_and_deterministic(self):
        first = self.engine.resolve_typed(self.request).candidates[0]
        second = self.engine.resolve_typed(self.request).candidates[0]
        self.assertEqual(first.hashes, second.hashes)
        self.assertEqual(
            "BAZI-STEM-RELATION-POSITIONAL-HASH-V1",
            first.hashes.algorithm_id,
        )
        upstream = {
            self.natal.hashes.fact_hash,
            self.flow.candidates[0].hashes.fact_hash,
            self.structural.candidates[0].hashes.fact_hash,
            self.support.candidates[0].hashes.fact_hash,
            self.incidence.candidates[0].hashes.fact_hash,
        }
        self.assertNotIn(first.hashes.fact_hash, upstream)

    def test_snapshot_binds_complete_upstream_hash_chain(self):
        candidate = self.engine.resolve_typed(self.request).candidates[0]
        snapshot = candidate.context.snapshot
        source = self.incidence.candidates[0]
        self.assertEqual(source.hashes.fact_hash, snapshot.source_incidence_fact_hash)
        self.assertEqual(
            source.hashes.computation_hash,
            snapshot.source_incidence_computation_hash,
        )
        self.assertEqual(self.natal.hashes.fact_hash, snapshot.source_natal_fact_hash)
        self.assertEqual(
            self.structural.candidates[0].hashes.fact_hash,
            snapshot.source_structural_fact_hash,
        )


if __name__ == "__main__":
    unittest.main()
