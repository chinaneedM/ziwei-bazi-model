from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

import jsonschema

from fortune_training.bazi_branch_relation_positional import (
    BaziBranchRelationPositionalEngine,
    BaziBranchRelationPositionalRequest,
    bazi_branch_relation_positional_context_foundation_r1_profile,
)
from fortune_training.bazi_chart import BaziChartFoundation, BaziChartRequest, bazi_foundation_v1_profile
from fortune_training.bazi_flow import BaziFlowEngine, BaziFlowRequest
from fortune_training.bazi_relation_incidence import BaziRelationIncidenceEngine, BaziRelationIncidenceRequest, bazi_relation_incidence_foundation_r1_profile
from fortune_training.bazi_structural import BaziStructuralEngine, BaziStructuralRequest, bazi_structural_context_r1_profile
from fortune_training.bazi_structural_support import BaziStructuralSupportEngine, BaziStructuralSupportRequest, bazi_structural_support_foundation_r1_profile
from fortune_training.bazi_temporal import BaziSex, BaziTemporalEngine, BaziTemporalRequest, bazi_temporal_v1_continuous_profile
from fortune_training.calendar_foundation import BirthInput


ROOT = Path(__file__).resolve().parents[1]


class BaziBranchRelationPositionalContextFoundationR1ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture = json.loads((ROOT / "tests" / "fixtures" / "bazi-relation-incidence-foundation-r1.json").read_text(encoding="utf-8"))
        birth = fixture["birth"]
        chart_engine = BaziChartFoundation.from_repository(ROOT)
        chart_profile = bazi_foundation_v1_profile(chart_engine.time_calendar.policy_registry)
        natal = chart_engine.resolve_typed(BaziChartRequest(
            BirthInput(
                datetime.fromisoformat(birth["reported_local_datetime"]), birth["birth_place"],
                birth["latitude"], birth["longitude"], birth["timezone_id"],
            ),
            chart_profile,
        )).candidates[0]
        temporal = BaziTemporalEngine().resolve_typed(BaziTemporalRequest(
            natal, BaziSex.MALE, bazi_temporal_v1_continuous_profile(), dayun_count=4
        ))
        target = datetime(2026, 10, 9, tzinfo=timezone.utc)
        flow = BaziFlowEngine(chart_engine.time_calendar.bazi).resolve_typed(BaziFlowRequest(natal, temporal.candidates, target, chart_profile))
        structural = BaziStructuralEngine().resolve_typed(BaziStructuralRequest(natal, flow.candidates, bazi_structural_context_r1_profile()))
        support = BaziStructuralSupportEngine().resolve_typed(BaziStructuralSupportRequest(
            natal, flow.candidates, structural.candidates, bazi_structural_support_foundation_r1_profile()
        ))
        incidence = BaziRelationIncidenceEngine().resolve_typed(BaziRelationIncidenceRequest(
            natal, target, flow.candidates, structural.candidates, support.candidates,
            bazi_relation_incidence_foundation_r1_profile(),
        ))
        cls.natal = natal
        cls.flow = flow
        cls.structural = structural
        cls.support = support
        cls.incidence = incidence
        cls.engine = BaziBranchRelationPositionalEngine()
        cls.profile = bazi_branch_relation_positional_context_foundation_r1_profile()
        cls.request = BaziBranchRelationPositionalRequest(natal, structural.candidates, incidence.candidates, cls.profile)
        cls.schema = json.loads((ROOT / "schemas" / "bazi-branch-relation-positional-context-foundation-r1.schema.json").read_text(encoding="utf-8"))

    def test_public_json_validates_against_closed_published_schema(self):
        payload = self.engine.resolve(self.request)
        jsonschema.Draft202012Validator.check_schema(self.schema)
        jsonschema.validate(payload, self.schema)
        self.assertEqual("BAZI-BRANCH-RELATION-POSITIONAL-CONTEXT-FOUNDATION-RESULT-V1", payload["schema"])
        self.assertEqual("RESOLVED", payload["status"])
        self.assertEqual("PASS", payload["candidates"][0]["integrity"]["status"])

    def test_public_contract_contains_only_neutral_coordinate_facts(self):
        context = self.engine.resolve(self.request)["candidates"][0]["context"]
        prohibited = {
            "near", "far", "adjacent", "remote", "blocked", "blocking",
            "intervening_effect", "engaged", "operable", "precedence", "priority",
            "winner", "loser", "allocation", "activated", "suppressed", "released",
            "strength", "severity", "classical_order", "source_interaction_pattern",
            "classical_assertion_binding", "final_relation_outcome", "prediction",
        }

        def keys(value):
            if isinstance(value, dict):
                return set(value) | set().union(*(keys(item) for item in value.values()))
            if isinstance(value, list):
                return set().union(*(keys(item) for item in value), set())
            return set()

        self.assertTrue(prohibited.isdisjoint(keys(context)))
        self.assertTrue(context["branch_relation_positional_facts"])
        self.assertTrue(any(row["source_arity"] == 3 for row in context["branch_relation_positional_facts"]))
        for row in context["participant_position_references"]:
            if row["position_domain"] == "TEMPORAL_FRAME":
                self.assertIsNone(row["natal_pillar_ordinal"])

    def test_hashes_are_independent_deterministic_and_bind_complete_upstream_chain(self):
        first = self.engine.resolve_typed(self.request).candidates[0]
        second = self.engine.resolve_typed(self.request).candidates[0]
        self.assertEqual(first.hashes, second.hashes)
        self.assertEqual("BAZI-BRANCH-RELATION-POSITIONAL-HASH-V1", first.hashes.algorithm_id)
        snapshot = first.context.snapshot
        self.assertEqual(self.incidence.candidates[0].hashes.fact_hash, snapshot.source_incidence_fact_hash)
        self.assertEqual(self.incidence.candidates[0].hashes.computation_hash, snapshot.source_incidence_computation_hash)
        self.assertEqual(self.natal.hashes.fact_hash, snapshot.source_natal_fact_hash)
        self.assertEqual(self.structural.candidates[0].hashes.fact_hash, snapshot.source_structural_fact_hash)
        self.assertNotIn(first.hashes.fact_hash, {
            self.natal.hashes.fact_hash, self.flow.candidates[0].hashes.fact_hash,
            self.structural.candidates[0].hashes.fact_hash, self.support.candidates[0].hashes.fact_hash,
            self.incidence.candidates[0].hashes.fact_hash,
        })


if __name__ == "__main__":
    unittest.main()
