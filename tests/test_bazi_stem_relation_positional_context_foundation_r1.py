from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

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
    NATAL_PILLAR,
    TEMPORAL_FRAME,
    BaziStemRelationPositionalEngine,
    BaziStemRelationPositionalRequest,
    bazi_stem_relation_positional_context_foundation_r1_profile,
    stem_relation_positional_hash_bundle,
    validate_stem_relation_positional_context,
)
from fortune_training.bazi_stem_relation_positional.generation import (
    _pair_positional_fact,
    _position_reference,
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


class BaziStemRelationPositionalContextFoundationR1Tests(unittest.TestCase):
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
        cls.positional_engine = BaziStemRelationPositionalEngine()
        cls.temporal_profile = bazi_temporal_v1_continuous_profile()
        cls.structural_profile = bazi_structural_context_r1_profile()
        cls.support_profile = bazi_structural_support_foundation_r1_profile()
        cls.incidence_profile = bazi_relation_incidence_foundation_r1_profile()
        cls.positional_profile = (
            bazi_stem_relation_positional_context_foundation_r1_profile()
        )
        cls.natal = cls._natal()
        cls.temporal = cls._temporal(cls.natal)
        cls._cache = {}

    @classmethod
    def _natal(cls, uncertainty_seconds: int = 0):
        result = cls.chart_engine.resolve_typed(BaziChartRequest(
            BirthInput(
                datetime(2025, 2, 7, 10, 10),
                "Beijing",
                39.9042,
                116.4074,
                "Asia/Shanghai",
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
    def _stack(cls, target, natal=None, temporal=None):
        natal = natal or cls.natal
        temporal = temporal or cls.temporal
        key = (natal.hashes.computation_hash, target)
        if key in cls._cache:
            return cls._cache[key]
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
        result = (flow, structural, support, incidence)
        cls._cache[key] = result
        return result

    @classmethod
    def _resolution(cls, target, natal=None, temporal=None):
        natal = natal or cls.natal
        stack = cls._stack(target, natal, temporal)
        positional = cls.positional_engine.resolve_typed(
            BaziStemRelationPositionalRequest(
                natal,
                stack[1].candidates,
                stack[3].candidates,
                cls.positional_profile,
            )
        )
        return stack, positional

    @classmethod
    def _manual_fact(cls, left_token, right_token):
        target = datetime(2026, 4, 15, tzinfo=timezone.utc)
        stack = cls._stack(target)
        incidence = stack[3].candidates[0]
        source = next(
            row for row in incidence.context.relation_occurrences
            if row.relation_type == "STEM_FIVE_COMBINATION"
        )
        natal_by_position = {row.position: row for row in cls.natal.chart.stems}
        structural = stack[1].candidates[0]
        temporal_by_position = {
            row.position: row for row in structural.context.active_temporal_stems
        }
        provenance = {
            row.instance_id: row
            for row in structural.context.temporal_participant_provenance
        }

        def reference(token):
            if token in natal_by_position:
                stem = natal_by_position[token]
                return _position_reference(
                    stem,
                    "NATAL",
                    None,
                    cls.natal.hashes.fact_hash,
                    (source.reference_id,),
                    "DAY.STEM",
                )
            stem = temporal_by_position[token]
            source_provenance = provenance[stem.instance_id]
            return _position_reference(
                stem,
                token,
                source_provenance.source_frame_id,
                structural.hashes.fact_hash,
                (source.reference_id,),
                "DAY.STEM",
            )

        positions = (reference(left_token), reference(right_token))
        relation = replace(
            source,
            relation_id=f"TEST.POSITION:{positions[0].participant_instance_id}+{positions[1].participant_instance_id}",
            participant_instance_ids=tuple(
                row.participant_instance_id for row in positions
            ),
        )
        return _pair_positional_fact(
            relation, positions, cls.natal.chart.stems, incidence
        )

    @classmethod
    def _validate(cls, candidate, stack, context=None, **overrides):
        incidence = stack[3].candidates[0]
        structural = stack[1].candidates[0]
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
        return validate_stem_relation_positional_context(
            context or candidate.context,
            cls.natal,
            structural,
            incidence,
            profile=cls.positional_profile,
            hashes=candidate.hashes,
            request_incidence_candidates=stack[3].candidates,
            **values,
        )

    def test_natal_year_month_distance_one_has_no_intervener(self):
        fact = self._manual_fact("YEAR", "MONTH")
        self.assertTrue(fact.natal_linear_order_comparable)
        self.assertEqual((0, 1), fact.natal_pillar_ordinals)
        self.assertEqual(1, fact.natal_ordinal_distance)
        self.assertEqual((), fact.intervening_natal_visible_stem_instance_ids)

    def test_natal_year_day_distance_two_has_month_intervener(self):
        fact = self._manual_fact("YEAR", "DAY")
        self.assertEqual(2, fact.natal_ordinal_distance)
        self.assertEqual(
            ("MONTH.STEM",), fact.intervening_natal_visible_stem_instance_ids
        )

    def test_natal_year_hour_distance_three_has_ordered_interveners(self):
        fact = self._manual_fact("YEAR", "HOUR")
        self.assertEqual(3, fact.natal_ordinal_distance)
        self.assertEqual(
            ("MONTH.STEM", "DAY.STEM"),
            fact.intervening_natal_visible_stem_instance_ids,
        )

    def test_natal_month_hour_distance_two_has_day_intervener(self):
        fact = self._manual_fact("MONTH", "HOUR")
        self.assertEqual(2, fact.natal_ordinal_distance)
        self.assertEqual(
            ("DAY.STEM",), fact.intervening_natal_visible_stem_instance_ids
        )

    def test_day_master_is_exact_day_stem_identity_not_equal_stem_value(self):
        day = next(row for row in self.natal.chart.stems if row.position == "DAY")
        year = next(row for row in self.natal.chart.stems if row.position == "YEAR")
        source_id = "RELATION_OCCURRENCE_REFERENCE:TEST"
        exact = _position_reference(
            day, "NATAL", None, self.natal.hashes.fact_hash, (source_id,), "DAY.STEM"
        )
        equal_value_elsewhere = _position_reference(
            replace(year, stem=day.stem),
            "NATAL",
            None,
            self.natal.hashes.fact_hash,
            (source_id,),
            "DAY.STEM",
        )
        self.assertTrue(exact.is_natal_day_master_participant)
        self.assertFalse(equal_value_elsewhere.is_natal_day_master_participant)

    def test_natal_to_each_temporal_domain_has_no_natal_distance(self):
        for token in ("DAYUN", "ANNUAL", "MONTHLY"):
            with self.subTest(token=token):
                fact = self._manual_fact("YEAR", token)
                self.assertFalse(fact.natal_linear_order_comparable)
                self.assertEqual((NATAL_PILLAR, TEMPORAL_FRAME), fact.position_domain_pair)
                self.assertEqual((), fact.natal_pillar_ordinals)
                self.assertIsNone(fact.natal_ordinal_distance)
                self.assertEqual((), fact.intervening_natal_visible_stem_instance_ids)

    def test_temporal_to_temporal_has_no_natal_linear_distance(self):
        fact = self._manual_fact("ANNUAL", "MONTHLY")
        self.assertEqual((TEMPORAL_FRAME, TEMPORAL_FRAME), fact.position_domain_pair)
        self.assertFalse(fact.natal_linear_order_comparable)
        self.assertIsNone(fact.natal_ordinal_distance)
        self.assertEqual((), fact.intervening_natal_visible_stem_instance_ids)

    def test_pre_dayun_does_not_manufacture_dayun_stem_position(self):
        target = self.temporal.candidates[0].state.jiaoyun.first_transition_utc - timedelta(microseconds=1)
        _, result = self._resolution(target)
        candidate = result.candidates[0]
        self.assertEqual(
            "PRE_DAYUN",
            self._stack(target)[3].candidates[0].context.snapshot.active_dayun_kind,
        )
        self.assertFalse(any(
            row.raw_position_token == "DAYUN"
            for row in candidate.context.participant_position_references
        ))

    def test_released_natal_monthly_relations_are_neutral_and_exact(self):
        target = datetime(2026, 2, 15, tzinfo=timezone.utc)
        stack, result = self._resolution(target)
        candidate = result.candidates[0]
        facts = candidate.context.stem_pair_positional_facts
        self.assertTrue(facts)
        incidence_by_ref = {
            row.reference_id: row
            for row in stack[3].candidates[0].context.relation_occurrences
        }
        for fact in facts:
            self.assertEqual(
                incidence_by_ref[fact.source_relation_reference_id].relation_id,
                fact.source_relation_id,
            )
            self.assertFalse(fact.natal_linear_order_comparable)
            self.assertIsNone(fact.natal_ordinal_distance)

    def test_day_master_relation_marks_only_exact_day_stem(self):
        _, result = self._resolution(datetime(2025, 6, 15, tzinfo=timezone.utc))
        fact = next(
            row for row in result.candidates[0].context.stem_pair_positional_facts
            if "DAY.STEM" in row.participant_instance_ids
        )
        self.assertTrue(fact.contains_natal_day_master_participant)
        self.assertEqual(("DAY.STEM",), fact.natal_day_master_participant_instance_ids)

    def test_shared_participant_does_not_create_competition_or_winner(self):
        _, result = self._resolution(datetime(2026, 2, 15, tzinfo=timezone.utc))
        payload = repr(result.candidates[0].context).lower()
        for prohibited in ("competes", "competition", "winner", "loser", "blocked", "not_engaged"):
            self.assertNotIn(prohibited, payload)

    def test_upstream_ids_and_hashes_are_unchanged(self):
        target = datetime(2026, 2, 15, tzinfo=timezone.utc)
        stack = self._stack(target)
        before = (
            self.natal.hashes,
            tuple(row.hashes for row in stack[0].candidates),
            tuple(row.hashes for row in stack[1].candidates),
            tuple(row.hashes for row in stack[2].candidates),
            tuple(row.hashes for row in stack[3].candidates),
            tuple(
                row.relation_id
                for row in stack[3].candidates[0].context.relation_occurrences
            ),
        )
        self._resolution(target)
        after = (
            self.natal.hashes,
            tuple(row.hashes for row in stack[0].candidates),
            tuple(row.hashes for row in stack[1].candidates),
            tuple(row.hashes for row in stack[2].candidates),
            tuple(row.hashes for row in stack[3].candidates),
            tuple(
                row.relation_id
                for row in stack[3].candidates[0].context.relation_occurrences
            ),
        )
        self.assertEqual(before, after)

    def test_genuine_multi_candidate_lineage_is_preserved(self):
        natal = self._natal(uncertainty_seconds=120)
        temporal = self._temporal(natal)
        stack, result = self._resolution(
            datetime(2026, 1, 1, tzinfo=timezone.utc), natal, temporal
        )
        self.assertEqual("MULTI_CANDIDATE", stack[3].status)
        self.assertEqual("MULTI_CANDIDATE", result.status)
        self.assertEqual(len(stack[3].candidates), len(result.candidates))
        for source, positional in zip(stack[3].candidates, result.candidates, strict=True):
            self.assertEqual(source.source_flow_candidate_indices, positional.source_flow_candidate_indices)
            self.assertEqual(source.source_structural_candidate_indices, positional.source_structural_candidate_indices)
            self.assertEqual(source.source_support_candidate_indices, positional.source_support_candidate_indices)
            self.assertEqual(source.source_temporal_candidate_indices, positional.source_temporal_candidate_indices)
            self.assertEqual(source.source_temporal_seed_ids, positional.source_temporal_seed_ids)
            self.assertEqual(source.lineage_binding_keys, positional.source_incidence_lineage_binding_keys)

    def test_aggregated_upstream_lineage_multiplicity_is_preserved(self):
        target = datetime(2026, 10, 9, tzinfo=timezone.utc)
        flow, structural_resolution, support_resolution, _ = self._stack(target)
        flow_candidate = flow.candidates[0]
        structural = replace(
            structural_resolution.candidates[0],
            source_flow_candidate_indices=(0, 1),
        )
        support = replace(
            support_resolution.candidates[0],
            source_structural_candidate_indices=(0, 1),
            source_flow_candidate_indices=(0, 1),
        )
        flows = (flow_candidate, flow_candidate)
        structurals = (structural, structural)
        supports = (support, support)
        incidence = self.incidence_engine.resolve_typed(
            BaziRelationIncidenceRequest(
                self.natal,
                target,
                flows,
                structurals,
                supports,
                self.incidence_profile,
            )
        )
        result = self.positional_engine.resolve_typed(
            BaziStemRelationPositionalRequest(
                self.natal,
                structurals,
                incidence.candidates,
                self.positional_profile,
            )
        )
        candidate = result.candidates[0]
        self.assertEqual((0, 1), candidate.source_flow_candidate_indices)
        self.assertEqual((0, 1), candidate.source_structural_candidate_indices)
        self.assertEqual((0, 1), candidate.source_support_candidate_indices)
        self.assertEqual(
            incidence.candidates[0].lineage_binding_keys,
            candidate.source_incidence_lineage_binding_keys,
        )

    def test_identical_incidence_candidates_aggregate_without_losing_indices(self):
        target = datetime(2026, 2, 15, tzinfo=timezone.utc)
        stack = self._stack(target)
        incidence = stack[3].candidates[0]
        result = self.positional_engine.resolve_typed(
            BaziStemRelationPositionalRequest(
                self.natal,
                stack[1].candidates,
                (incidence, incidence),
                self.positional_profile,
            )
        )
        self.assertEqual("RESOLVED", result.status)
        self.assertEqual((0, 1), result.candidates[0].source_incidence_candidate_indices)

    def test_tamper_position_ordinal_intervener_day_master_and_source_relation_fails_closed(self):
        target = datetime(2025, 6, 15, tzinfo=timezone.utc)
        stack, result = self._resolution(target)
        candidate = result.candidates[0]
        reference = next(
            row for row in candidate.context.participant_position_references
            if row.participant_instance_id == "DAY.STEM"
        )
        fact = next(
            row for row in candidate.context.stem_pair_positional_facts
            if "DAY.STEM" in row.participant_instance_ids
        )
        tampered_reference = replace(
            reference,
            raw_position_token="YEAR",
            natal_pillar_ordinal=0,
            is_natal_day_master_participant=False,
        )
        tampered_fact = replace(
            fact,
            source_relation_id="TAMPERED.RELATION",
            intervening_natal_visible_stem_instance_ids=("MONTH.STEM",),
            contains_natal_day_master_participant=False,
            natal_day_master_participant_instance_ids=(),
        )
        context = replace(
            candidate.context,
            participant_position_references=tuple(
                tampered_reference if row == reference else row
                for row in candidate.context.participant_position_references
            ),
            stem_pair_positional_facts=tuple(
                tampered_fact if row == fact else row
                for row in candidate.context.stem_pair_positional_facts
            ),
        )
        report = self._validate(candidate, stack, context=context)
        codes = {row.code for row in report.diagnostics}
        self.assertEqual("FAIL", report.status)
        self.assertIn("PARTICIPANT_POSITION_REPLAY_MISMATCH", codes)
        self.assertIn("NATAL_ORDINAL_REPLAY_MISMATCH", codes)
        self.assertIn("INTERVENER_MEMBERSHIP_OR_ORDER_REPLAY_MISMATCH", codes)
        self.assertIn("DAY_MASTER_IDENTITY_REPLAY_MISMATCH", codes)
        self.assertIn("SOURCE_RELATION_REPLAY_MISMATCH", codes)
        self.assertIn("POSITIONAL_HASH_REPLAY_MISMATCH", codes)

    def test_tamper_intervener_order_fails_closed(self):
        target = datetime(2025, 6, 15, tzinfo=timezone.utc)
        stack, result = self._resolution(target)
        candidate = result.candidates[0]
        fact = candidate.context.stem_pair_positional_facts[0]
        tampered = replace(
            fact,
            intervening_natal_visible_stem_instance_ids=(
                "DAY.STEM", "MONTH.STEM"
            ),
        )
        context = replace(
            candidate.context,
            stem_pair_positional_facts=(
                tampered, *candidate.context.stem_pair_positional_facts[1:]
            ),
        )
        report = self._validate(candidate, stack, context=context)
        codes = {row.code for row in report.diagnostics}
        self.assertEqual("FAIL", report.status)
        self.assertIn("INTERVENER_MEMBERSHIP_OR_ORDER_REPLAY_MISMATCH", codes)
        self.assertIn("POSITIONAL_HASH_REPLAY_MISMATCH", codes)

    def test_tamper_lineage_fails_hash_and_integrity_replay(self):
        target = datetime(2026, 2, 15, tzinfo=timezone.utc)
        stack, result = self._resolution(target)
        candidate = result.candidates[0]
        tampered = candidate.source_flow_candidate_indices + (99,)
        report = self._validate(
            candidate,
            stack,
            source_flow_candidate_indices=tampered,
        )
        codes = {row.code for row in report.diagnostics}
        self.assertEqual("FAIL", report.status)
        self.assertIn("LINEAGE_REPLAY_MISMATCH", codes)
        self.assertIn("POSITIONAL_HASH_REPLAY_MISMATCH", codes)
        self.assertNotEqual(
            candidate.hashes.computation_hash,
            stem_relation_positional_hash_bundle(
                candidate.context,
                stack[3].candidates[0],
                candidate.source_incidence_candidate_indices,
                tampered,
                candidate.source_structural_candidate_indices,
                candidate.source_support_candidate_indices,
                candidate.source_temporal_candidate_indices,
                candidate.source_temporal_seed_ids,
                candidate.source_incidence_lineage_binding_keys,
                candidate.lineage_binding_keys,
                self.positional_profile,
            ).computation_hash,
        )

    def test_no_second_raw_relation_generator_dependency(self):
        package = ROOT / "src" / "fortune_training" / "bazi_stem_relation_positional"
        source = "\n".join(
            path.read_text(encoding="utf-8") for path in package.glob("*.py")
        )
        self.assertNotIn("generate_raw_relations", source)
        self.assertNotIn("fortune_training.bazi_chart.relations", source)


if __name__ == "__main__":
    unittest.main()
