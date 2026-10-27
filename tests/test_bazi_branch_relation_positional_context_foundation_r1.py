from __future__ import annotations

import json
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.bazi_branch_relation_positional import (
    IN_SCOPE_RELATION_TYPES,
    NATAL_PILLAR,
    NATAL_PILLAR_ORDINALS,
    TEMPORAL_FRAME,
    BaziBranchRelationPositionalEngine,
    BaziBranchRelationPositionalRequest,
    bazi_branch_relation_positional_context_foundation_r1_profile,
    branch_relation_positional_hash_bundle,
    validate_branch_relation_positional_context,
)
from fortune_training.bazi_branch_relation_positional.generation import _position_reference
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
FIXTURE = json.loads((
    ROOT / "tests" / "fixtures" / "bazi-relation-incidence-foundation-r1.json"
).read_text(encoding="utf-8"))


class BaziBranchRelationPositionalContextFoundationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.chart_engine = BaziChartFoundation.from_repository(ROOT)
        cls.chart_profile = bazi_foundation_v1_profile(
            cls.chart_engine.time_calendar.policy_registry
        )
        cls.temporal_engine = BaziTemporalEngine()
        cls.flow_engine = BaziFlowEngine(cls.chart_engine.time_calendar.bazi)
        cls.structural_engine = BaziStructuralEngine()
        cls.support_engine = BaziStructuralSupportEngine()
        cls.incidence_engine = BaziRelationIncidenceEngine()
        cls.positional_engine = BaziBranchRelationPositionalEngine()
        cls.temporal_profile = bazi_temporal_v1_continuous_profile()
        cls.structural_profile = bazi_structural_context_r1_profile()
        cls.support_profile = bazi_structural_support_foundation_r1_profile()
        cls.incidence_profile = bazi_relation_incidence_foundation_r1_profile()
        cls.positional_profile = (
            bazi_branch_relation_positional_context_foundation_r1_profile()
        )
        cls.natal = cls._natal()
        cls.temporal = cls._temporal(cls.natal)
        cls._cache = {}

    @classmethod
    def _natal(cls, uncertainty_seconds: int = 0):
        birth = FIXTURE["birth"]
        result = cls.chart_engine.resolve_typed(BaziChartRequest(
            BirthInput(
                reported_local_datetime=datetime.fromisoformat(
                    birth["reported_local_datetime"]
                ),
                birth_place=birth["birth_place"],
                latitude=birth["latitude"],
                longitude=birth["longitude"],
                timezone_id=birth["timezone_id"],
                uncertainty_seconds=uncertainty_seconds,
            ),
            cls.chart_profile,
        ))
        return result.candidates[0]

    @classmethod
    def _temporal(cls, natal):
        return cls.temporal_engine.resolve_typed(BaziTemporalRequest(
            natal,
            BaziSex.MALE,
            cls.temporal_profile,
            dayun_count=10,
        ))

    @classmethod
    def _target(cls, key):
        if key == "zimao":
            return datetime.fromisoformat("2032-03-15T00:00:00+00:00")
        if key == "multi_candidate":
            return datetime.fromisoformat("2026-01-01T00:00:00+00:00")
        return datetime.fromisoformat(FIXTURE["targets"][key])

    @classmethod
    def _resolution(cls, key, natal=None, temporal=None):
        natal = natal or cls.natal
        temporal = temporal or cls.temporal
        target = cls._target(key)
        cache_key = (key, natal.hashes.computation_hash)
        if cache_key in cls._cache:
            return cls._cache[cache_key]
        flow = cls.flow_engine.resolve_typed(BaziFlowRequest(
            natal, temporal.candidates, target, cls.chart_profile
        ))
        structural = cls.structural_engine.resolve_typed(BaziStructuralRequest(
            natal, flow.candidates, cls.structural_profile
        ))
        support = cls.support_engine.resolve_typed(BaziStructuralSupportRequest(
            natal,
            flow.candidates,
            structural.candidates,
            cls.support_profile,
        ))
        incidence = cls.incidence_engine.resolve_typed(BaziRelationIncidenceRequest(
            natal,
            target,
            flow.candidates,
            structural.candidates,
            support.candidates,
            cls.incidence_profile,
        ))
        positional = cls.positional_engine.resolve_typed(
            BaziBranchRelationPositionalRequest(
                natal,
                structural.candidates,
                incidence.candidates,
                cls.positional_profile,
            )
        )
        result = (flow, structural, support, incidence, positional)
        cls._cache[cache_key] = result
        return result

    def _validate(self, stack, candidate, context=None, **overrides):
        incidence = stack[3].candidates[0]
        values = {
            "source_incidence_candidate_indices": candidate.source_incidence_candidate_indices,
            "source_flow_candidate_indices": candidate.source_flow_candidate_indices,
            "source_structural_candidate_indices": candidate.source_structural_candidate_indices,
            "source_support_candidate_indices": candidate.source_support_candidate_indices,
            "source_temporal_candidate_indices": candidate.source_temporal_candidate_indices,
            "source_temporal_seed_ids": candidate.source_temporal_seed_ids,
            "source_incidence_lineage_binding_keys": candidate.source_incidence_lineage_binding_keys,
            "lineage_binding_keys": candidate.lineage_binding_keys,
        }
        values.update(overrides)
        return validate_branch_relation_positional_context(
            context or candidate.context,
            self.natal,
            stack[1].candidates[0],
            incidence,
            profile=self.positional_profile,
            hashes=candidate.hashes,
            request_incidence_candidates=stack[3].candidates,
            **values,
        )

    def test_natal_year_month_day_hour_map_exactly_to_zero_through_three(self):
        source_ref = ("RELATION_OCCURRENCE_REFERENCE:TEST",)
        for branch in self.natal.chart.branches:
            with self.subTest(position=branch.position):
                row = _position_reference(
                    branch,
                    "NATAL",
                    None,
                    self.natal.hashes.fact_hash,
                    source_ref,
                )
                self.assertEqual(NATAL_PILLAR, row.position_domain)
                self.assertEqual(NATAL_PILLAR_ORDINALS[branch.position], row.natal_pillar_ordinal)
                self.assertIsNone(row.source_frame_id)

    def test_temporal_positions_remain_typed_frames_without_cross_domain_ordinal(self):
        stack = self._resolution("baseline")
        context = stack[4].candidates[0].context
        temporal = [
            row for row in context.participant_position_references
            if row.position_domain == TEMPORAL_FRAME
        ]
        self.assertEqual({"DAYUN", "ANNUAL", "MONTHLY"}, {row.raw_position_token for row in temporal})
        self.assertTrue(all(row.source_frame_id for row in temporal))
        self.assertTrue(all(row.natal_pillar_ordinal is None for row in temporal))
        cross_domain = [
            row for row in context.branch_relation_positional_facts
            if len(set(row.position_domains)) > 1
        ]
        self.assertTrue(cross_domain)
        self.assertTrue(all(not row.all_participants_natal_pillar and not row.natal_pillar_ordinals for row in cross_domain))

    def test_all_seven_released_branch_relation_types_are_covered(self):
        actual = set()
        for key in ("baseline", "self_punishment", "zimao"):
            actual.update(
                row.source_relation_type
                for row in self._resolution(key)[4].candidates[0].context.branch_relation_positional_facts
            )
        self.assertEqual(set(IN_SCOPE_RELATION_TYPES), actual)

    def test_every_positional_fact_is_one_to_one_incidence_replay(self):
        stack = self._resolution("baseline")
        source = {
            row.reference_id: row
            for row in stack[3].candidates[0].context.relation_occurrences
            if row.relation_type in IN_SCOPE_RELATION_TYPES
        }
        facts = {
            row.source_relation_reference_id: row
            for row in stack[4].candidates[0].context.branch_relation_positional_facts
        }
        self.assertEqual(set(source), set(facts))
        for reference_id, fact in facts.items():
            occurrence = source[reference_id]
            self.assertEqual(occurrence.relation_id, fact.source_relation_id)
            self.assertEqual(occurrence.semantic_relation_id, fact.source_semantic_relation_id)
            self.assertEqual(occurrence.participant_instance_ids, fact.participant_instance_ids)
            self.assertEqual(
                tuple(row.participant_layer for row in occurrence.participant_provenance),
                fact.participant_layers,
            )

    def test_complete_sanhe_preserves_exact_ordered_three_participant_occurrence(self):
        stack = self._resolution("sanhe")
        source = next(
            row for row in stack[3].candidates[0].context.relation_occurrences
            if row.relation_type == "BRANCH_SANHE_COMPLETE"
        )
        fact = next(
            row for row in stack[4].candidates[0].context.branch_relation_positional_facts
            if row.source_relation_reference_id == source.reference_id
        )
        self.assertEqual(3, fact.source_arity)
        self.assertEqual(source.participant_instance_ids, fact.participant_instance_ids)
        self.assertEqual(3, len(fact.participant_position_reference_ids))
        self.assertEqual("GROUP", fact.source_orientation)

    def test_directed_punishment_preserves_exact_order_and_orientation(self):
        stack = self._resolution("baseline")
        source = next(
            row for row in stack[3].candidates[0].context.relation_occurrences
            if row.relation_type == "BRANCH_DIRECTIONAL_PUNISHMENT"
        )
        fact = next(
            row for row in stack[4].candidates[0].context.branch_relation_positional_facts
            if row.source_relation_reference_id == source.reference_id
        )
        self.assertEqual("DIRECTED", fact.source_orientation)
        self.assertEqual(source.participant_instance_ids, fact.participant_instance_ids)

    def test_self_punishment_preserves_two_distinct_same_value_instances(self):
        stack = self._resolution("self_punishment")
        source = next(
            row for row in stack[3].candidates[0].context.relation_occurrences
            if row.relation_type == "BRANCH_SELF_PUNISHMENT"
        )
        fact = next(
            row for row in stack[4].candidates[0].context.branch_relation_positional_facts
            if row.source_relation_reference_id == source.reference_id
        )
        self.assertEqual(2, len(set(fact.participant_instance_ids)))
        by_id = {
            row.participant_instance_id: row
            for row in stack[4].candidates[0].context.participant_position_references
        }
        self.assertEqual(1, len({by_id[item].branch for item in fact.participant_instance_ids}))

    def test_chuan_remains_neutral_source_faithful_identity_without_harm_leakage(self):
        context = self._resolution("baseline")[4].candidates[0].context
        rows = [row for row in context.branch_relation_positional_facts if row.source_relation_type == "BRANCH_CHUAN"]
        self.assertTrue(rows)
        self.assertTrue(all(row.source_relation_family == "BRANCH_CHUAN" for row in rows))
        self.assertTrue(all(row.source_semantic_relation_id.startswith("BRANCH.CHUAN.") for row in rows))
        self.assertNotIn("harm", repr(rows).lower())

    def test_cross_layer_exact_provenance_replays_incidence(self):
        stack = self._resolution("baseline")
        source_by_ref = {row.reference_id: row for row in stack[3].candidates[0].context.relation_occurrences}
        fact = next(
            row for row in stack[4].candidates[0].context.branch_relation_positional_facts
            if len(set(row.participant_layers)) > 1
        )
        source = source_by_ref[fact.source_relation_reference_id]
        self.assertEqual(tuple(row.participant_layer for row in source.participant_provenance), fact.participant_layers)
        self.assertEqual(tuple(row.source_frame_id for row in source.participant_provenance), fact.source_frame_ids)
        references = {
            row.participant_instance_id: row
            for row in stack[4].candidates[0].context.participant_position_references
        }
        self.assertEqual(
            tuple(row.source_upstream_fact_hash for row in source.participant_provenance),
            tuple(references[item].source_upstream_fact_hash for item in fact.participant_instance_ids),
        )

    def test_deterministic_hash_order_and_replay(self):
        stack = self._resolution("baseline")
        request = BaziBranchRelationPositionalRequest(
            self.natal,
            stack[1].candidates,
            stack[3].candidates,
            self.positional_profile,
        )
        first = self.positional_engine.resolve_typed(request).candidates[0]
        second = self.positional_engine.resolve_typed(request).candidates[0]
        self.assertEqual(first, second)
        self.assertEqual("PASS", self._validate(stack, first).status)

    def test_identical_incidence_candidates_aggregate_without_losing_indices(self):
        stack = self._resolution("baseline")
        incidence = stack[3].candidates[0]
        result = self.positional_engine.resolve_typed(BaziBranchRelationPositionalRequest(
            self.natal,
            stack[1].candidates,
            (incidence, incidence),
            self.positional_profile,
        ))
        self.assertEqual("RESOLVED", result.status)
        self.assertEqual((0, 1), result.candidates[0].source_incidence_candidate_indices)

    def test_genuine_multi_candidate_lineage_is_preserved_without_fact_hash_collapse(self):
        natal = self._natal(uncertainty_seconds=120)
        temporal = self._temporal(natal)
        stack = self._resolution("multi_candidate", natal, temporal)
        incidence = stack[3]
        positional = stack[4]
        self.assertEqual("MULTI_CANDIDATE", incidence.status)
        self.assertEqual("MULTI_CANDIDATE", positional.status)
        self.assertEqual(len(incidence.candidates), len(positional.candidates))
        for source, candidate in zip(incidence.candidates, positional.candidates, strict=True):
            self.assertEqual(source.source_flow_candidate_indices, candidate.source_flow_candidate_indices)
            self.assertEqual(source.source_structural_candidate_indices, candidate.source_structural_candidate_indices)
            self.assertEqual(source.source_support_candidate_indices, candidate.source_support_candidate_indices)
            self.assertEqual(source.source_temporal_candidate_indices, candidate.source_temporal_candidate_indices)
            self.assertEqual(source.source_temporal_seed_ids, candidate.source_temporal_seed_ids)
            self.assertEqual(source.lineage_binding_keys, candidate.source_incidence_lineage_binding_keys)

    def test_tamper_order_position_and_lineage_fail_closed(self):
        stack = self._resolution("baseline")
        candidate = stack[4].candidates[0]
        fact = candidate.context.branch_relation_positional_facts[0]
        tampered_fact = replace(
            fact,
            participant_instance_ids=tuple(reversed(fact.participant_instance_ids)),
            raw_position_tokens=tuple(reversed(fact.raw_position_tokens)),
        )
        context = replace(
            candidate.context,
            branch_relation_positional_facts=(tampered_fact, *candidate.context.branch_relation_positional_facts[1:]),
        )
        report = self._validate(stack, candidate, context=context)
        self.assertEqual("FAIL", report.status)
        self.assertIn("ORDER_ARITY_ORIENTATION_REPLAY_MISMATCH", {row.code for row in report.diagnostics})
        lineage = candidate.source_flow_candidate_indices + (99,)
        lineage_report = self._validate(stack, candidate, source_flow_candidate_indices=lineage)
        self.assertIn("LINEAGE_REPLAY_MISMATCH", {row.code for row in lineage_report.diagnostics})
        self.assertNotEqual(
            candidate.hashes.computation_hash,
            branch_relation_positional_hash_bundle(
                candidate.context,
                stack[3].candidates[0],
                candidate.source_incidence_candidate_indices,
                lineage,
                candidate.source_structural_candidate_indices,
                candidate.source_support_candidate_indices,
                candidate.source_temporal_candidate_indices,
                candidate.source_temporal_seed_ids,
                candidate.source_incidence_lineage_binding_keys,
                candidate.lineage_binding_keys,
                self.positional_profile,
            ).computation_hash,
        )

    def test_no_raw_generator_or_classical_runtime_dependency(self):
        package = ROOT / "src" / "fortune_training" / "bazi_branch_relation_positional"
        source = "\n".join(path.read_text(encoding="utf-8") for path in package.glob("*.py"))
        self.assertNotIn("generate_raw_relations", source)
        self.assertNotIn("fortune_training.bazi_chart.relations", source)
        prohibited = (
            "classical_relation_interaction_assertion", "operability", "fixpoint",
            "winner_selection", "BRANCH_HARM", "BRANCH_BREAK", "BRANCH_PARTIAL_TRINE",
            "HIDDEN_COMBINATION",
        )
        for token in prohibited:
            self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
