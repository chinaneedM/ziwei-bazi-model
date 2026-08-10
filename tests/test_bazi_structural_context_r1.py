from __future__ import annotations

import json
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
from fortune_training.bazi_structural import (
    BaziStructuralEngine,
    BaziStructuralRequest,
    bazi_structural_context_r1_profile,
    structural_hash_bundle,
    validate_structural_context,
)
from fortune_training.bazi_temporal import (
    BaziSex,
    BaziTemporalEngine,
    BaziTemporalRequest,
    bazi_temporal_v1_continuous_profile,
)
from fortune_training.calendar_foundation import BirthInput


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads(
    (ROOT / "tests" / "fixtures" / "bazi-structural-context-r1.json").read_text(
        encoding="utf-8"
    )
)


class BaziStructuralContextR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.chart_engine = BaziChartFoundation.from_repository(ROOT)
        cls.chart_profile = bazi_foundation_v1_profile(
            cls.chart_engine.time_calendar.policy_registry
        )
        cls.temporal_engine = BaziTemporalEngine()
        cls.flow_engine = BaziFlowEngine(cls.chart_engine.time_calendar.bazi)
        cls.structural_engine = BaziStructuralEngine()
        cls.structural_profile = bazi_structural_context_r1_profile()
        cls.natal = cls._natal(datetime(2025, 2, 7, 10, 10))
        cls.temporal = cls._temporal(cls.natal)

    @classmethod
    def _natal(cls, local: datetime, **kwargs):
        result = cls.chart_engine.resolve_typed(
            BaziChartRequest(
                BirthInput(
                    reported_local_datetime=local,
                    birth_place="Beijing",
                    latitude=39.9042,
                    longitude=116.4074,
                    timezone_id="Asia/Shanghai",
                    **kwargs,
                ),
                cls.chart_profile,
            )
        )
        if len(result.candidates) != 1:
            raise RuntimeError(f"fixture requires one Natal candidate: {result.status}")
        return result.candidates[0]

    @classmethod
    def _temporal(cls, natal):
        result = cls.temporal_engine.resolve_typed(
            BaziTemporalRequest(
                natal,
                BaziSex.MALE,
                bazi_temporal_v1_continuous_profile(),
                dayun_count=4,
            )
        )
        if not result.candidates:
            raise RuntimeError(f"fixture requires Temporal candidates: {result.status}")
        return result

    @classmethod
    def _flow(cls, target, natal=None, temporal=None):
        natal = natal or cls.natal
        temporal = temporal or cls.temporal
        return cls.flow_engine.resolve_typed(
            BaziFlowRequest(
                natal,
                temporal.candidates,
                target,
                cls.chart_profile,
            )
        )

    @classmethod
    def _resolve(cls, target, natal=None, temporal=None):
        natal = natal or cls.natal
        flow = cls._flow(target, natal=natal, temporal=temporal)
        return cls.structural_engine.resolve_typed(
            BaziStructuralRequest(natal, flow.candidates, cls.structural_profile)
        )

    @classmethod
    def _fixture_target(cls, key):
        row = FIXTURE["targets"][key]
        return cls.chart_engine.time_calendar.solar_terms.term(
            row["solar_term_year"], row["solar_longitude_degrees"]
        ).utc_instant

    def test_natal_hash_and_raw_relation_ids_are_byte_stable(self):
        expected = FIXTURE["natal"]
        self.assertEqual(expected["expected_fact_hash"], self.natal.hashes.fact_hash)
        self.assertEqual(
            expected["expected_pillars"],
            [row.ganzhi for row in self.natal.chart.pillars],
        )
        self.assertEqual(
            expected["expected_raw_relation_ids"],
            [row.relation_id for row in self.natal.chart.raw_relations],
        )
        original_hashes = self.natal.hashes
        original_relations = self.natal.chart.raw_relations
        self._resolve(self._fixture_target("mixed_layer_fire_trine"))
        self.assertEqual(original_hashes, self.natal.hashes)
        self.assertEqual(original_relations, self.natal.chart.raw_relations)

    def test_cross_layer_clash_is_neutral_occurrence(self):
        expected = FIXTURE["targets"]["cross_layer_clash"]
        context = self._resolve(
            self._fixture_target("cross_layer_clash")
        ).candidates[0].context
        rows = [
            row for row in context.dynamic_raw_relations
            if row.semantic_relation_id == expected["semantic_relation_id"]
        ]
        self.assertEqual(2, len(rows))
        self.assertTrue(all(row.relation_scope == "CROSS_LAYER" for row in rows))
        self.assertTrue(all(row.participant_layers == ("NATAL", "MONTHLY") for row in rows))
        self.assertTrue(all(row.nominal_transformation_element is None for row in rows))

    def test_temporal_to_temporal_stem_combination_retains_nominal_target_only(self):
        expected = FIXTURE["targets"]["temporal_stem_combination"]
        context = self._resolve(
            self._fixture_target("temporal_stem_combination")
        ).candidates[0].context
        rows = [
            row for row in context.dynamic_raw_relations
            if row.semantic_relation_id == expected["semantic_relation_id"]
            and row.participant_layers == ("ANNUAL", "MONTHLY")
        ]
        self.assertEqual(1, len(rows))
        self.assertEqual("TEMPORAL_ONLY", rows[0].relation_scope)
        self.assertEqual(expected["nominal_transformation_element"], rows[0].nominal_transformation_element)
        self.assertFalse(hasattr(rows[0], "transformation_succeeded"))

    def test_three_member_relation_spans_natal_annual_monthly(self):
        expected = FIXTURE["targets"]["mixed_layer_fire_trine"]
        context = self._resolve(
            self._fixture_target("mixed_layer_fire_trine")
        ).candidates[0].context
        rows = [
            row for row in context.dynamic_raw_relations
            if row.semantic_relation_id == expected["semantic_relation_id"]
        ]
        self.assertEqual(1, len(rows))
        self.assertEqual(("NATAL", "ANNUAL", "MONTHLY"), rows[0].participant_layers)
        self.assertEqual("CROSS_LAYER", rows[0].relation_scope)
        self.assertEqual(3, rows[0].arity)

    def test_same_character_in_different_layers_has_distinct_frame_bound_identity(self):
        context = self._resolve(
            self._fixture_target("repeated_occurrence")
        ).candidates[0].context
        natal_si = {row.instance_id for row in self.natal.chart.branches if row.branch == "巳"}
        temporal_si = {
            row.instance_id for row in context.active_temporal_branches if row.branch == "巳"
        }
        self.assertTrue(natal_si)
        self.assertTrue(temporal_si)
        self.assertTrue(natal_si.isdisjoint(temporal_si))
        self.assertEqual(
            len(context.temporal_participant_provenance),
            len(context.active_temporal_stems) + len(context.active_temporal_branches),
        )

    def test_pre_dayun_has_annual_monthly_but_no_fabricated_dayun(self):
        target = self._fixture_target("temporal_stem_combination")
        flow_context = self._flow(target).candidates[0].context
        self.assertEqual("PRE_DAYUN", flow_context.active_dayun_kind)
        context = self._resolve(target).candidates[0].context
        self.assertEqual(("ANNUAL", "MONTHLY"), tuple(row.position for row in context.active_temporal_stems))
        self.assertFalse(any(row.layer == "DAYUN" for row in context.temporal_participant_provenance))
        self.assertEqual(2, len(context.active_temporal_branches))

    def test_boundary_replay_changes_only_source_frame_layers(self):
        transition = self.temporal.candidates[0].state.jiaoyun.first_transition_utc
        before = self._resolve(transition - timedelta(microseconds=1)).candidates[0].context
        exact = self._resolve(transition).candidates[0].context
        before_by_layer = {row.position: row for row in before.active_temporal_stems}
        exact_by_layer = {row.position: row for row in exact.active_temporal_stems}
        self.assertNotIn("DAYUN", before_by_layer)
        self.assertIn("DAYUN", exact_by_layer)
        self.assertEqual(before_by_layer["ANNUAL"], exact_by_layer["ANNUAL"])
        self.assertEqual(before_by_layer["MONTHLY"], exact_by_layer["MONTHLY"])

        jie = self.chart_engine.time_calendar.solar_terms.term(2026, 105).utc_instant
        before = self._resolve(jie - timedelta(microseconds=1)).candidates[0].context
        exact = self._resolve(jie).candidates[0].context
        self.assertEqual(before.active_temporal_stems[0:2], exact.active_temporal_stems[0:2])
        self.assertNotEqual(before.active_temporal_stems[-1], exact.active_temporal_stems[-1])

        spring = self.chart_engine.time_calendar.solar_terms.term(2027, 315).utc_instant
        before = self._resolve(spring - timedelta(microseconds=1)).candidates[0].context
        exact = self._resolve(spring).candidates[0].context
        self.assertEqual(before.active_temporal_stems[0], exact.active_temporal_stems[0])
        self.assertNotEqual(before.active_temporal_stems[1:], exact.active_temporal_stems[1:])

    def test_temporal_hidden_ten_god_exposure_and_affinity_replay(self):
        row = self._resolve(self._fixture_target("mixed_layer_fire_trine")).candidates[0]
        context = row.context
        self.assertTrue(context.temporal_hidden_stems)
        self.assertEqual(
            len(context.active_temporal_stems) + len(context.temporal_hidden_stems),
            len(context.temporal_ten_gods),
        )
        self.assertTrue(context.dynamic_exposures)
        self.assertTrue(context.dynamic_affinities)
        self.assertEqual("PASS", validate_structural_context(
            context, self.natal, self._flow(self._fixture_target("mixed_layer_fire_trine")).candidates[0],
            self.structural_profile, row.hashes,
        ).status)

    def test_multi_flow_candidates_preserve_lineage_and_do_not_collapse(self):
        natal = self._natal(datetime(2025, 2, 7, 10, 10), uncertainty_seconds=120)
        temporal = self._temporal(natal)
        self.assertEqual("MULTI_CANDIDATE", temporal.status)
        flow = self._flow(datetime(2026, 1, 1, tzinfo=timezone.utc), natal, temporal)
        result = self.structural_engine.resolve_typed(
            BaziStructuralRequest(natal, flow.candidates, self.structural_profile)
        )
        self.assertEqual("MULTI_CANDIDATE", result.status)
        self.assertEqual(len(flow.candidates), len(result.candidates))
        self.assertEqual(
            len(result.candidates),
            len({row.context.upstream_flow_fact_hash for row in result.candidates}),
        )

    def test_only_identical_complete_structural_payload_deduplicates(self):
        flow = self._flow(datetime(2026, 6, 1, tzinfo=timezone.utc)).candidates[0]
        result = self.structural_engine.resolve_typed(
            BaziStructuralRequest(self.natal, (flow, flow), self.structural_profile)
        )
        self.assertEqual("RESOLVED", result.status)
        self.assertEqual(1, len(result.candidates))
        self.assertEqual((0, 1), result.candidates[0].source_flow_candidate_indices)

    def test_integrity_and_hashes_detect_tampering(self):
        flow = self._flow(self._fixture_target("mixed_layer_fire_trine")).candidates[0]
        row = self.structural_engine.resolve_typed(
            BaziStructuralRequest(self.natal, (flow,), self.structural_profile)
        ).candidates[0]
        tampered = replace(
            row.context,
            active_temporal_stems=tuple(reversed(row.context.active_temporal_stems)),
        )
        report = validate_structural_context(
            tampered, self.natal, flow, self.structural_profile, row.hashes
        )
        codes = {item.code for item in report.diagnostics}
        self.assertEqual("FAIL", report.status)
        self.assertIn("TEMPORAL_PARTICIPANT_REPLAY_MISMATCH", codes)
        self.assertIn("STRUCTURAL_HASH_REPLAY_MISMATCH", codes)
        self.assertNotEqual(
            row.hashes.fact_hash,
            structural_hash_bundle(
                tampered, self.natal, flow, self.structural_profile
            ).fact_hash,
        )


if __name__ == "__main__":
    unittest.main()
