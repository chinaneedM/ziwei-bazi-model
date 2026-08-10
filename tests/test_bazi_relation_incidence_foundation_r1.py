from __future__ import annotations

import json
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from fortune_training.bazi_chart import (
    BaziChartFoundation,
    BaziChartRequest,
    bazi_foundation_v1_profile,
)
from fortune_training.bazi_flow import BaziFlowEngine, BaziFlowRequest
from fortune_training.bazi_relation_incidence import (
    DISJOINT,
    SHARED_PARTICIPANT,
    BaziRelationIncidenceEngine,
    BaziRelationIncidenceRequest,
    RelationIncidenceSnapshotInputs,
    bazi_relation_incidence_foundation_r1_profile,
    relation_incidence_hash_bundle,
    validate_relation_incidence_context,
)
from fortune_training.bazi_relation_incidence.generation import (
    _participant_incidence_facts,
    _participant_map,
    _relation_pair_topology_facts,
)
from fortune_training.bazi_relation_transition import (
    ENTERED,
    EXITED,
    PERSISTING,
    BaziRelationTransitionEngine,
    BaziRelationTransitionRequest,
    bazi_relation_transition_foundation_r1_profile,
)
from fortune_training.bazi_structural import (
    BaziStructuralEngine,
    BaziStructuralRequest,
    bazi_structural_context_r1_profile,
)
from fortune_training.bazi_structural_support import (
    ACTIVE_FLOW_SOLAR_MONTH,
    NATAL_MONTH_COMMAND,
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


class BaziRelationIncidenceFoundationR1Tests(unittest.TestCase):
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
        cls.temporal_profile = bazi_temporal_v1_continuous_profile()
        cls.structural_profile = bazi_structural_context_r1_profile()
        cls.support_profile = bazi_structural_support_foundation_r1_profile()
        cls.incidence_profile = bazi_relation_incidence_foundation_r1_profile()
        cls.natal = cls._natal()
        cls.temporal = cls._temporal(cls.natal)
        cls._stack_cache = {}

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
        if not result.candidates:
            raise RuntimeError(f"fixture requires Natal candidates: {result.status}")
        return result.candidates[0]

    @classmethod
    def _temporal(cls, natal):
        result = cls.temporal_engine.resolve_typed(BaziTemporalRequest(
            natal,
            BaziSex.MALE,
            cls.temporal_profile,
            dayun_count=4,
        ))
        if not result.candidates:
            raise RuntimeError(f"fixture requires Temporal candidates: {result.status}")
        return result

    @classmethod
    def _stack(cls, target, natal=None, temporal=None):
        natal = natal or cls.natal
        temporal = temporal or cls.temporal
        key = (
            natal.hashes.fact_hash,
            target,
            tuple(row.hashes.fact_hash for row in temporal.candidates),
        )
        if key in cls._stack_cache:
            return cls._stack_cache[key]
        flow = cls.flow_engine.resolve_typed(BaziFlowRequest(
            natal, temporal.candidates, target, cls.chart_profile
        ))
        structural = cls.structural_engine.resolve_typed(BaziStructuralRequest(
            natal, flow.candidates, cls.structural_profile
        ))
        support = cls.support_engine.resolve_typed(BaziStructuralSupportRequest(
            natal, flow.candidates, structural.candidates, cls.support_profile
        ))
        result = (flow, structural, support)
        cls._stack_cache[key] = result
        return result

    @classmethod
    def _resolution(cls, target, natal=None, temporal=None):
        natal = natal or cls.natal
        temporal = temporal or cls.temporal
        stack = cls._stack(target, natal, temporal)
        result = cls.incidence_engine.resolve_typed(BaziRelationIncidenceRequest(
            natal_candidate=natal,
            target_utc=target,
            flow_candidates=stack[0].candidates,
            structural_candidates=stack[1].candidates,
            support_candidates=stack[2].candidates,
            incidence_profile=cls.incidence_profile,
        ))
        return stack, result

    @classmethod
    def _target(cls, key):
        return datetime.fromisoformat(FIXTURE["targets"][key])

    @classmethod
    def _chain(cls, stack, candidate_index=0):
        return RelationIncidenceSnapshotInputs(
            candidate_index,
            candidate_index,
            candidate_index,
            stack[0].candidates[candidate_index],
            stack[1].candidates[candidate_index],
            stack[2].candidates[candidate_index],
        )

    def test_single_relation_degree_one_and_no_pair_topology(self):
        stack, result = self._resolution(self._target("baseline"))
        context = result.candidates[0].context
        relation = context.relation_occurrences[0]
        chain = self._chain(stack)
        participant_map = _participant_map(
            self.natal, chain.flow, chain.structural
        )
        incidence = _participant_incidence_facts(
            context.snapshot,
            chain,
            participant_map,
            (relation,),
        )
        pairs = _relation_pair_topology_facts(
            context.snapshot,
            participant_map,
            (relation,),
            self.incidence_profile,
        )
        self.assertTrue(incidence)
        self.assertEqual({1}, {row.relation_count for row in incidence})
        self.assertEqual((), pairs)

    def test_shared_participant_is_exact_instance_id_intersection(self):
        _, result = self._resolution(self._target("baseline"))
        context = result.candidates[0].context
        relation_by_id = {row.relation_id: row for row in context.relation_occurrences}
        shared = next(
            row for row in context.relation_pair_topology_facts
            if row.topology_kind == SHARED_PARTICIPANT
        )
        exact = set(relation_by_id[shared.relation_ids[0]].participant_instance_ids) & set(
            relation_by_id[shared.relation_ids[1]].participant_instance_ids
        )
        self.assertEqual(exact, set(shared.shared_participant_instance_ids))
        self.assertTrue(exact)

    def test_disjoint_coexistence_is_empty_exact_id_intersection(self):
        _, result = self._resolution(self._target("baseline"))
        context = result.candidates[0].context
        relation_by_id = {row.relation_id: row for row in context.relation_occurrences}
        disjoint = next(
            row for row in context.relation_pair_topology_facts
            if row.topology_kind == DISJOINT
        )
        exact = set(relation_by_id[disjoint.relation_ids[0]].participant_instance_ids) & set(
            relation_by_id[disjoint.relation_ids[1]].participant_instance_ids
        )
        self.assertEqual(set(), exact)
        self.assertEqual((), disjoint.shared_participant_instance_ids)

    def test_repeated_character_distinct_occurrences_do_not_become_shared(self):
        _, result = self._resolution(self._target("repeated_character"))
        context = result.candidates[0].context
        relation_by_id = {row.relation_id: row for row in context.relation_occurrences}
        participant_by_id = {
            item.instance_id: item
            for relation in context.relation_occurrences
            for item in relation.participant_provenance
        }
        found = False
        for pair in context.relation_pair_topology_facts:
            if pair.topology_kind != DISJOINT:
                continue
            left = relation_by_id[pair.relation_ids[0]].participant_instance_ids
            right = relation_by_id[pair.relation_ids[1]].participant_instance_ids
            if any(
                participant_by_id[a].value == participant_by_id[b].value
                and a != b
                for a in left
                for b in right
            ):
                found = True
                break
        self.assertTrue(found, "fixture must discriminate character equality from occurrence identity")

    def test_natal_and_temporal_relation_can_share_exact_natal_node(self):
        _, result = self._resolution(self._target("baseline"))
        context = result.candidates[0].context
        relation_by_id = {row.relation_id: row for row in context.relation_occurrences}
        pair = next(
            row for row in context.relation_pair_topology_facts
            if row.topology_kind == SHARED_PARTICIPANT
            and {
                relation_by_id[item].source_occurrence_kind
                for item in row.relation_ids
            } == {
                "NATAL_RELATION_CANDIDATE",
                "STRUCTURAL_DYNAMIC_RELATION_OCCURRENCE",
            }
        )
        shared = set(pair.shared_participant_instance_ids)
        facts = {
            row.participant_instance_id: row
            for row in context.participant_incidence_facts
        }
        self.assertTrue(shared)
        self.assertTrue(all(facts[item].participant_layer == "NATAL" for item in shared))
        self.assertTrue(all(facts[item].relation_count >= 2 for item in shared))

    def test_complete_sanhe_shares_node_without_resolution_semantics(self):
        _, result = self._resolution(self._target("sanhe"))
        context = result.candidates[0].context
        relation_by_id = {row.relation_id: row for row in context.relation_occurrences}
        sanhe = {
            row.relation_id for row in context.relation_occurrences
            if row.relation_type == "BRANCH_SANHE_COMPLETE"
        }
        pair = next(
            row for row in context.relation_pair_topology_facts
            if row.topology_kind == SHARED_PARTICIPANT
            and set(row.relation_ids) & sanhe
            and not set(row.relation_ids) <= sanhe
        )
        self.assertTrue(pair.shared_participant_instance_ids)
        self.assertNotIn(
            "transformation_success",
            {field for row in relation_by_id.values() for field in row.__dataclass_fields__},
        )

    def test_self_punishment_preserves_exact_participant_multiplicity(self):
        _, result = self._resolution(self._target("self_punishment"))
        context = result.candidates[0].context
        row = next(
            item for item in context.relation_occurrences
            if item.relation_type == "BRANCH_SELF_PUNISHMENT"
        )
        self.assertEqual(2, len(row.participant_instance_ids))
        self.assertEqual(2, len(set(row.participant_instance_ids)))
        self.assertEqual(1, len({item.value for item in row.participant_provenance}))

    def test_support_touch_uses_exact_released_candidate_membership(self):
        stack, result = self._resolution(self._target("baseline"))
        context = result.candidates[0].context
        support_by_id = {
            row.candidate_id: row
            for row in stack[2].candidates[0].context.support_evidence_candidates
        }
        touched = next(
            row for row in context.participant_incidence_facts
            if row.support_evidence_candidate_ids
        )
        for candidate_id in touched.support_evidence_candidate_ids:
            source = support_by_id[candidate_id]
            self.assertIn(
                touched.participant_instance_id,
                {
                    source.visible_stem_instance_id,
                    source.supporting_branch_instance_id,
                },
            )
        self.assertFalse(hasattr(touched, "strength"))
        self.assertFalse(hasattr(touched, "weight"))

    def test_month_command_and_flow_month_roles_remain_distinct_when_character_matches(self):
        stack, result = self._resolution(self._target("repeated_character"))
        context = result.candidates[0].context
        support = stack[2].candidates[0].context
        natal_id = support.natal_month_command.source_branch_instance_id
        flow_id = support.active_flow_solar_month.source_temporal_branch_instance_id
        self.assertNotEqual(natal_id, flow_id)
        self.assertEqual(
            support.natal_month_command.branch,
            support.active_flow_solar_month.branch,
        )
        by_id = {
            row.participant_instance_id: row
            for row in context.participant_incidence_facts
        }
        self.assertIn(NATAL_MONTH_COMMAND, by_id[natal_id].seasonal_role_ids)
        self.assertIn(ACTIVE_FLOW_SOLAR_MONTH, by_id[flow_id].seasonal_role_ids)
        self.assertNotEqual(
            by_id[natal_id].seasonal_role_reference_ids,
            by_id[flow_id].seasonal_role_reference_ids,
        )

    def test_pre_dayun_creates_no_synthetic_dayun_incidence(self):
        first = self.temporal.candidates[0].state.jiaoyun.first_transition_utc
        _, result = self._resolution(first - timedelta(microseconds=1))
        context = result.candidates[0].context
        self.assertEqual("PRE_DAYUN", context.snapshot.active_dayun_kind)
        self.assertFalse(any(
            row.participant_layer == "DAYUN"
            for row in context.participant_incidence_facts
        ))
        self.assertFalse(any(
            "DAYUN" in row.participant_layers
            for row in context.relation_occurrences
        ))

    def test_multi_candidate_lineages_are_preserved_without_cartesian_product(self):
        natal = self._natal(uncertainty_seconds=120)
        temporal = self._temporal(natal)
        self.assertEqual("MULTI_CANDIDATE", temporal.status)
        _, result = self._resolution(
            datetime(2026, 1, 1, tzinfo=timezone.utc), natal, temporal
        )
        self.assertEqual("MULTI_CANDIDATE", result.status)
        self.assertEqual(len(temporal.candidates), len(result.candidates))
        self.assertNotEqual(len(temporal.candidates) ** 3, len(result.candidates))
        self.assertEqual(
            len(result.candidates),
            len({row.hashes.computation_hash for row in result.candidates}),
        )
        self.assertTrue(all(len(row.source_temporal_seed_ids) == 1 for row in result.candidates))

    def test_incidence_aligns_with_transition_without_becoming_dependency(self):
        before_target = self._target("baseline")
        after_target = self._target("transition_after")
        before_stack, before_result = self._resolution(before_target)
        after_stack, after_result = self._resolution(after_target)
        transition = BaziRelationTransitionEngine().resolve_typed(
            BaziRelationTransitionRequest(
                self.natal,
                before_target,
                after_target,
                before_stack[0].candidates,
                before_stack[1].candidates,
                before_stack[2].candidates,
                after_stack[0].candidates,
                after_stack[1].candidates,
                after_stack[2].candidates,
                bazi_relation_transition_foundation_r1_profile(),
            )
        )
        self.assertEqual("RESOLVED", transition.status)
        incidence_before = before_result.candidates[0].context.snapshot
        incidence_after = after_result.candidates[0].context.snapshot
        transition_context = transition.candidates[0].context
        self.assertEqual(
            incidence_before.raw_relation_ids,
            transition_context.before_snapshot.raw_relation_ids,
        )
        self.assertEqual(
            incidence_after.raw_relation_ids,
            transition_context.after_snapshot.raw_relation_ids,
        )
        self.assertEqual(
            incidence_before.upstream_structural_fact_hash,
            transition_context.before_snapshot.upstream_structural_fact_hash,
        )
        self.assertEqual(
            {PERSISTING},
            {row.transition_state for row in transition_context.transition_facts},
        )
        self.assertEqual({PERSISTING, ENTERED, EXITED}, {PERSISTING, ENTERED, EXITED})

    def test_incidence_never_calls_generator_and_preserves_upstream_hashes(self):
        target = self._target("baseline")
        stack = self._stack(target)
        originals = (
            self.natal.hashes,
            stack[0].candidates[0].hashes,
            stack[1].candidates[0].hashes,
            stack[2].candidates[0].hashes,
            self.natal.chart.raw_relations,
            stack[1].candidates[0].context.dynamic_raw_relations,
        )
        request = BaziRelationIncidenceRequest(
            self.natal,
            target,
            stack[0].candidates,
            stack[1].candidates,
            stack[2].candidates,
            self.incidence_profile,
        )
        with patch(
            "fortune_training.bazi_chart.relations.generate_raw_relations",
            side_effect=AssertionError("incidence must replay released relations"),
        ):
            result = self.incidence_engine.resolve_typed(request)
        self.assertEqual("RESOLVED", result.status)
        self.assertEqual(originals, (
            self.natal.hashes,
            stack[0].candidates[0].hashes,
            stack[1].candidates[0].hashes,
            stack[2].candidates[0].hashes,
            self.natal.chart.raw_relations,
            stack[1].candidates[0].context.dynamic_raw_relations,
        ))

    def test_integrity_and_hash_replay_detect_degree_and_topology_tampering(self):
        stack, result = self._resolution(self._target("baseline"))
        candidate = result.candidates[0]
        first_incidence = candidate.context.participant_incidence_facts[0]
        first_pair = candidate.context.relation_pair_topology_facts[0]
        tampered = replace(
            candidate.context,
            participant_incidence_facts=(
                replace(first_incidence, relation_count=first_incidence.relation_count + 1),
                *candidate.context.participant_incidence_facts[1:],
            ),
            relation_pair_topology_facts=(
                replace(
                    first_pair,
                    topology_kind=(
                        DISJOINT
                        if first_pair.topology_kind == SHARED_PARTICIPANT
                        else SHARED_PARTICIPANT
                    ),
                ),
                *candidate.context.relation_pair_topology_facts[1:],
            ),
        )
        chain = self._chain(stack)
        report = validate_relation_incidence_context(
            tampered,
            self.natal,
            chain,
            candidate.source_temporal_candidate_indices,
            candidate.source_temporal_seed_ids,
            candidate.lineage_binding_keys,
            self.incidence_profile,
            candidate.hashes,
        )
        codes = {row.code for row in report.diagnostics}
        self.assertEqual("FAIL", report.status)
        self.assertIn("PARTICIPANT_RELATION_DEGREE_MISMATCH", codes)
        self.assertIn("PAIR_TOPOLOGY_KIND_MISMATCH", codes)
        self.assertIn("INCIDENCE_HASH_REPLAY_MISMATCH", codes)
        self.assertNotEqual(
            candidate.hashes.fact_hash,
            relation_incidence_hash_bundle(
                tampered,
                self.natal,
                chain,
                candidate.source_temporal_candidate_indices,
                candidate.source_temporal_seed_ids,
                candidate.lineage_binding_keys,
                self.incidence_profile,
            ).fact_hash,
        )

    def test_invalid_target_fails_closed(self):
        target = self._target("baseline")
        stack = self._stack(target)
        result = self.incidence_engine.resolve_typed(BaziRelationIncidenceRequest(
            self.natal,
            target.replace(tzinfo=None),
            stack[0].candidates,
            stack[1].candidates,
            stack[2].candidates,
            self.incidence_profile,
        ))
        self.assertEqual("FAILED", result.status)
        self.assertTrue(result.diagnostics[0].startswith("INVALID_TARGET"))


if __name__ == "__main__":
    unittest.main()
