from __future__ import annotations

import json
import unittest
from collections import Counter
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
from fortune_training.bazi_relation_transition import (
    ENTERED,
    EXITED,
    PERSISTING,
    BaziRelationTransitionEngine,
    BaziRelationTransitionRequest,
    RelationTransitionSnapshotInputs,
    bazi_relation_transition_foundation_r1_profile,
    relation_transition_hash_bundle,
    validate_relation_transition_context,
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
    ROOT / "tests" / "fixtures" / "bazi-relation-transition-foundation-r1.json"
).read_text(encoding="utf-8"))


class BaziRelationTransitionFoundationR1Tests(unittest.TestCase):
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
        cls.transition_engine = BaziRelationTransitionEngine()
        cls.temporal_profile = bazi_temporal_v1_continuous_profile()
        cls.structural_profile = bazi_structural_context_r1_profile()
        cls.support_profile = bazi_structural_support_foundation_r1_profile()
        cls.transition_profile = bazi_relation_transition_foundation_r1_profile()
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
        if len(result.candidates) != 1:
            raise RuntimeError(f"fixture requires one Natal candidate: {result.status}")
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
        key = (natal.hashes.fact_hash, target, tuple(
            row.hashes.fact_hash for row in temporal.candidates
        ))
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
    def _transition_resolution(cls, before_target, after_target, natal=None, temporal=None):
        natal = natal or cls.natal
        temporal = temporal or cls.temporal
        before = cls._stack(before_target, natal, temporal)
        after = cls._stack(after_target, natal, temporal)
        result = cls.transition_engine.resolve_typed(BaziRelationTransitionRequest(
            natal_candidate=natal,
            before_target_utc=before_target,
            after_target_utc=after_target,
            before_flow_candidates=before[0].candidates,
            before_structural_candidates=before[1].candidates,
            before_support_candidates=before[2].candidates,
            after_flow_candidates=after[0].candidates,
            after_structural_candidates=after[1].candidates,
            after_support_candidates=after[2].candidates,
            transition_profile=cls.transition_profile,
        ))
        return before, after, result

    @classmethod
    def _term(cls, key):
        row = FIXTURE["targets"][key]
        return cls.chart_engine.time_calendar.solar_terms.term(
            row["solar_term_year"], row["solar_longitude_degrees"]
        ).utc_instant

    def test_same_frame_snapshot_is_exact_persistence_only(self):
        before_target = datetime.fromisoformat(FIXTURE["targets"]["same_frame_before"])
        after_target = datetime.fromisoformat(FIXTURE["targets"]["same_frame_after"])
        _, _, result = self._transition_resolution(before_target, after_target)
        self.assertEqual("RESOLVED", result.status)
        candidate = result.candidates[0]
        context = candidate.context
        self.assertFalse(context.frame_change_evidence)
        self.assertTrue(context.transition_facts)
        self.assertEqual(
            {PERSISTING}, {row.transition_state for row in context.transition_facts}
        )
        self.assertEqual(
            context.before_snapshot.raw_relation_ids,
            context.after_snapshot.raw_relation_ids,
        )
        self.assertEqual("PASS", candidate.integrity.status)

    def test_exact_jie_reuses_half_open_month_boundary(self):
        exact = self._term("exact_jie")
        _, _, result = self._transition_resolution(
            exact - timedelta(microseconds=1), exact
        )
        context = result.candidates[0].context
        evidence = {row.evidence_type: row for row in context.frame_change_evidence}
        self.assertEqual({"MONTHLY_FRAME_CHANGED"}, set(evidence))
        monthly = evidence["MONTHLY_FRAME_CHANGED"]
        self.assertEqual(2, len(monthly.exited_participant_instance_ids))
        self.assertEqual(2, len(monthly.entered_participant_instance_ids))
        self.assertTrue(set(monthly.exited_participant_instance_ids).isdisjoint(
            monthly.entered_participant_instance_ids
        ))
        states = Counter(row.transition_state for row in context.transition_facts)
        self.assertGreater(states[PERSISTING], 0)
        self.assertGreater(states[ENTERED], 0)
        self.assertGreater(states[EXITED], 0)
        self.assertEqual(exact, context.after_snapshot.target_utc)

    def test_lichun_records_annual_and_monthly_changes_without_priority(self):
        exact = self._term("lichun")
        _, _, result = self._transition_resolution(
            exact - timedelta(microseconds=1), exact
        )
        context = result.candidates[0].context
        self.assertEqual(
            {"ANNUAL_FRAME_CHANGED", "MONTHLY_FRAME_CHANGED"},
            {row.evidence_type for row in context.frame_change_evidence},
        )
        self.assertFalse(any(
            row.evidence_type == "DAYUN_FRAME_CHANGED"
            for row in context.frame_change_evidence
        ))
        self.assertTrue(all(
            not hasattr(row, "priority") and not hasattr(row, "cause")
            for row in context.frame_change_evidence
        ))

    def test_pre_dayun_to_first_dayun_has_no_fake_before_participant(self):
        exact = self.temporal.candidates[0].state.jiaoyun.first_transition_utc
        _, _, result = self._transition_resolution(
            exact - timedelta(microseconds=1), exact
        )
        context = result.candidates[0].context
        self.assertEqual("PRE_DAYUN", context.before_snapshot.active_dayun_kind)
        self.assertEqual("DAYUN", context.after_snapshot.active_dayun_kind)
        evidence = next(
            row for row in context.frame_change_evidence
            if row.evidence_type == "DAYUN_FRAME_CHANGED"
        )
        self.assertEqual((), evidence.exited_participant_instance_ids)
        self.assertEqual(2, len(evidence.entered_participant_instance_ids))
        entered_ids = set(evidence.entered_participant_instance_ids)
        self.assertTrue(any(
            row.transition_state == ENTERED
            and set(row.participant_instance_ids) & entered_ids
            for row in context.transition_facts
        ))

    def test_dayun_to_next_dayun_keeps_occurrence_ids_distinct(self):
        exact = self.temporal.candidates[0].state.dayun_frames[0].end_utc
        _, _, result = self._transition_resolution(
            exact - timedelta(microseconds=1), exact
        )
        context = result.candidates[0].context
        evidence = next(
            row for row in context.frame_change_evidence
            if row.evidence_type == "DAYUN_FRAME_CHANGED"
        )
        self.assertEqual(2, len(evidence.exited_participant_instance_ids))
        self.assertEqual(2, len(evidence.entered_participant_instance_ids))
        self.assertTrue(set(evidence.exited_participant_instance_ids).isdisjoint(
            evidence.entered_participant_instance_ids
        ))
        self.assertNotEqual(
            context.before_snapshot.active_dayun_source_frame_id,
            context.after_snapshot.active_dayun_source_frame_id,
        )

    def test_natal_only_raw_relations_are_byte_stable_and_persist(self):
        before_target = datetime.fromisoformat(FIXTURE["targets"]["same_frame_before"])
        after_target = self._term("lichun")
        original_hashes = self.natal.hashes
        original_relations = self.natal.chart.raw_relations
        _, _, result = self._transition_resolution(before_target, after_target)
        facts = {row.relation_id: row for row in result.candidates[0].context.transition_facts}
        self.assertEqual(
            FIXTURE["natal"]["expected_fact_hash"], self.natal.hashes.fact_hash
        )
        self.assertEqual(
            FIXTURE["natal"]["expected_pillars"],
            [row.ganzhi for row in self.natal.chart.pillars],
        )
        self.assertEqual(
            FIXTURE["natal"]["expected_raw_relation_ids"],
            [row.relation_id for row in self.natal.chart.raw_relations],
        )
        for relation in self.natal.chart.raw_relations:
            fact = facts[relation.relation_id]
            self.assertEqual(PERSISTING, fact.transition_state)
            self.assertEqual("NATAL_ONLY", fact.occurrence_scope)
            self.assertEqual(("NATAL",), fact.participant_layers)
        self.assertEqual(original_hashes, self.natal.hashes)
        self.assertEqual(original_relations, self.natal.chart.raw_relations)

    def test_complete_sanhe_occurrence_enters_then_exact_id_exits(self):
        entry = self._term("sanhe_entry")
        _, _, entry_result = self._transition_resolution(
            entry - timedelta(microseconds=1), entry
        )
        entered = {
            row.relation_id for row in entry_result.candidates[0].context.transition_facts
            if row.relation_type == "BRANCH_SANHE_COMPLETE"
            and row.transition_state == ENTERED
        }
        exit_target = self._term("sanhe_exit")
        _, _, exit_result = self._transition_resolution(
            exit_target - timedelta(microseconds=1), exit_target
        )
        exited = {
            row.relation_id for row in exit_result.candidates[0].context.transition_facts
            if row.relation_type == "BRANCH_SANHE_COMPLETE"
            and row.transition_state == EXITED
        }
        self.assertTrue(entered & exited)
        for result in (entry_result, exit_result):
            sanhe = [
                row for row in result.candidates[0].context.transition_facts
                if row.relation_type == "BRANCH_SANHE_COMPLETE"
            ]
            self.assertTrue(sanhe)
            self.assertTrue(all(not hasattr(row, "transformation_success") for row in sanhe))

    def test_chuan_transition_is_exact_entered_persisting_exited_set_replay(self):
        exact = self._term("lichun")
        _, _, result = self._transition_resolution(
            exact - timedelta(microseconds=1), exact
        )
        rows = [
            row
            for row in result.candidates[0].context.transition_facts
            if row.relation_family == "BRANCH_CHUAN"
        ]
        self.assertTrue(rows)
        self.assertEqual(
            {ENTERED, PERSISTING, EXITED},
            {row.transition_state for row in rows},
        )
        self.assertTrue(all(row.relation_type == "BRANCH_CHUAN" for row in rows))
        self.assertTrue(all(row.arity == 2 for row in rows))
        self.assertTrue(
            all(row.nominal_transformation_element is None for row in rows)
        )
        prohibited = {
            "activated", "effective", "suppressed", "cancelled", "released",
            "severity", "strength", "priority", "outcome", "event",
        }
        self.assertTrue(all(
            prohibited.isdisjoint(row.__dataclass_fields__) for row in rows
        ))

    def test_repeated_characters_across_layers_do_not_collapse_occurrences(self):
        exact = self._term("sanhe_entry")
        _, _, result = self._transition_resolution(
            exact - timedelta(microseconds=1), exact
        )
        facts = result.candidates[0].context.transition_facts
        provenance = [
            item
            for row in facts
            for item in row.before_participant_provenance + row.after_participant_provenance
        ]
        repeated_values = {
            value for value in {row.value for row in provenance}
            if len({row.instance_id for row in provenance if row.value == value}) > 1
        }
        self.assertTrue(repeated_values)
        self.assertEqual(len(facts), len({row.relation_id for row in facts}))
        self.assertEqual(len(facts), len({row.transition_fact_id for row in facts}))

    def test_multi_candidate_lineage_pairs_five_not_cartesian_twenty_five(self):
        natal = self._natal(uncertainty_seconds=120)
        temporal = self._temporal(natal)
        self.assertEqual("MULTI_CANDIDATE", temporal.status)
        before = datetime(2026, 1, 1, tzinfo=timezone.utc)
        after = before + timedelta(days=1)
        _, _, result = self._transition_resolution(before, after, natal, temporal)
        self.assertEqual("MULTI_CANDIDATE", result.status)
        self.assertEqual(len(temporal.candidates), len(result.candidates))
        self.assertNotEqual(
            len(temporal.candidates) ** 2,
            len(result.candidates),
        )
        self.assertEqual(
            len(result.candidates),
            len({row.hashes.computation_hash for row in result.candidates}),
        )
        self.assertTrue(all(len(row.paired_temporal_seed_ids) == 1 for row in result.candidates))

    def test_transition_never_calls_raw_relation_generator(self):
        before_target = datetime.fromisoformat(FIXTURE["targets"]["same_frame_before"])
        after_target = datetime.fromisoformat(FIXTURE["targets"]["same_frame_after"])
        before = self._stack(before_target)
        after = self._stack(after_target)
        request = BaziRelationTransitionRequest(
            self.natal,
            before_target,
            after_target,
            before[0].candidates,
            before[1].candidates,
            before[2].candidates,
            after[0].candidates,
            after[1].candidates,
            after[2].candidates,
            self.transition_profile,
        )
        with patch(
            "fortune_training.bazi_chart.relations.generate_raw_relations",
            side_effect=AssertionError("transition must replay released relation IDs"),
        ):
            result = self.transition_engine.resolve_typed(request)
        self.assertEqual("RESOLVED", result.status)

    def test_integrity_and_hash_replay_detect_transition_tampering(self):
        before_target = datetime.fromisoformat(FIXTURE["targets"]["same_frame_before"])
        after_target = datetime.fromisoformat(FIXTURE["targets"]["same_frame_after"])
        before_stack, after_stack, result = self._transition_resolution(
            before_target, after_target
        )
        candidate = result.candidates[0]
        first = candidate.context.transition_facts[0]
        tampered = replace(
            candidate.context,
            transition_facts=(
                replace(first, transition_state=ENTERED),
                *candidate.context.transition_facts[1:],
            ),
        )
        before = RelationTransitionSnapshotInputs(
            0, 0, 0,
            before_stack[0].candidates[0],
            before_stack[1].candidates[0],
            before_stack[2].candidates[0],
        )
        after = RelationTransitionSnapshotInputs(
            0, 0, 0,
            after_stack[0].candidates[0],
            after_stack[1].candidates[0],
            after_stack[2].candidates[0],
        )
        report = validate_relation_transition_context(
            tampered,
            self.natal,
            before,
            after,
            candidate.paired_temporal_candidate_indices,
            candidate.paired_temporal_seed_ids,
            candidate.lineage_pairing_keys,
            self.transition_profile,
            candidate.hashes,
        )
        codes = {row.code for row in report.diagnostics}
        self.assertEqual("FAIL", report.status)
        self.assertIn("PERSISTING_SET_REPLAY_MISMATCH", codes)
        self.assertIn("ENTERED_SET_REPLAY_MISMATCH", codes)
        self.assertIn("TRANSITION_FACT_REPLAY_MISMATCH", codes)
        self.assertIn("TRANSITION_HASH_REPLAY_MISMATCH", codes)
        self.assertNotEqual(
            candidate.hashes.fact_hash,
            relation_transition_hash_bundle(
                tampered,
                self.natal,
                before,
                after,
                candidate.paired_temporal_candidate_indices,
                candidate.paired_temporal_seed_ids,
                candidate.lineage_pairing_keys,
                self.transition_profile,
            ).fact_hash,
        )

    def test_equal_or_reversed_targets_fail_closed(self):
        target = datetime.fromisoformat(FIXTURE["targets"]["same_frame_before"])
        stack = self._stack(target)
        for before, after in ((target, target), (target + timedelta(seconds=1), target)):
            result = self.transition_engine.resolve_typed(BaziRelationTransitionRequest(
                self.natal,
                before,
                after,
                stack[0].candidates,
                stack[1].candidates,
                stack[2].candidates,
                stack[0].candidates,
                stack[1].candidates,
                stack[2].candidates,
                self.transition_profile,
            ))
            self.assertEqual("FAILED", result.status)
            self.assertTrue(result.diagnostics[0].startswith("INVALID_TARGET_ORDER"))


if __name__ == "__main__":
    unittest.main()
