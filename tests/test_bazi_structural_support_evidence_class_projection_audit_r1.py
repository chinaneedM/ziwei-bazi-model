from __future__ import annotations

import json
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fortune_training.bazi_application.structural_projection import structural_projection
from fortune_training.bazi_application.structural_support_projection import (
    SUPPORT_PROJECTION_ALGORITHM_VERSION,
    SUPPORT_PROJECTION_SCHEMA,
    SUPPORT_PROJECTION_SEMANTIC_SCOPE,
    structural_support_projection,
    validate_structural_support_projection,
)
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
)
from fortune_training.bazi_structural_support import (
    ACTIVE_FLOW_SOLAR_MONTH,
    EXACT_HIDDEN_STEM_MATCH,
    NATAL_MONTH_COMMAND,
    SAME_ELEMENT_HIDDEN_SUPPORT,
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
from fortune_training.calendar_foundation.models import json_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads(
    (
        ROOT
        / "tests"
        / "fixtures"
        / "bazi-structural-support-foundation-r1.json"
    ).read_text(encoding="utf-8")
)


class BaziStructuralSupportEvidenceClassProjectionAuditR1Tests(unittest.TestCase):
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
        cls.structural_profile = bazi_structural_context_r1_profile()
        cls.support_profile = bazi_structural_support_foundation_r1_profile()
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
    def _target(cls, key: str):
        row = FIXTURE["targets"][key]
        target = cls.chart_engine.time_calendar.solar_terms.term(
            row["solar_term_year"], row["solar_longitude_degrees"]
        ).utc_instant
        return target + timedelta(microseconds=row.get("offset_microseconds", 0))

    @classmethod
    def _stack(cls, target, *, natal=None, temporal=None):
        natal = natal or cls.natal
        temporal = temporal or cls.temporal
        flow = cls.flow_engine.resolve_typed(
            BaziFlowRequest(natal, temporal.candidates, target, cls.chart_profile)
        )
        structural = cls.structural_engine.resolve_typed(
            BaziStructuralRequest(natal, flow.candidates, cls.structural_profile)
        )
        support = cls.support_engine.resolve_typed(
            BaziStructuralSupportRequest(
                natal,
                flow.candidates,
                structural.candidates,
                cls.support_profile,
            )
        )
        return flow, structural, support

    def test_four_released_targets_replay_valid_source_bound_support_projections(self) -> None:
        self.assertEqual(4, len(FIXTURE["targets"]))
        for key in FIXTURE["targets"]:
            with self.subTest(key=key):
                flow, structural, support = self._stack(self._target(key))
                self.assertEqual(len(structural.candidates), len(support.candidates))
                for candidate in support.candidates:
                    self.assertEqual(1, len(candidate.source_structural_candidate_indices))
                    self.assertEqual(1, len(candidate.source_flow_candidate_indices))
                    structural_index = candidate.source_structural_candidate_indices[0]
                    flow_index = candidate.source_flow_candidate_indices[0]
                    source_structural = structural.candidates[structural_index]
                    source_flow = flow.candidates[flow_index]
                    projection = structural_support_projection(candidate)
                    self.assertEqual(SUPPORT_PROJECTION_SCHEMA, projection["schema"])
                    self.assertEqual("1.0.0", SUPPORT_PROJECTION_ALGORITHM_VERSION)
                    self.assertEqual(
                        SUPPORT_PROJECTION_SEMANTIC_SCOPE,
                        projection["semantic_scope"],
                    )
                    self.assertTrue(
                        validate_structural_support_projection(
                            projection,
                            source_flow_candidate_index=flow_index,
                            natal_fact_hash=self.natal.hashes.fact_hash,
                            temporal_fact_hash=candidate.context.upstream_temporal_fact_hash,
                            flow_fact_hash=source_flow.hashes.fact_hash,
                            structural_fact_hash=source_structural.hashes.fact_hash,
                            support_fact_hash=candidate.hashes.fact_hash,
                            support_computation_hash=candidate.hashes.computation_hash,
                            flow_monthly_frame=json_value(source_flow.context.monthly_frame),
                            structural_projection=structural_projection(source_structural),
                        )
                    )

    def test_exact_and_same_element_are_distinct_coexisting_evidence_classes(self) -> None:
        _, _, support = self._stack(self._target("pre_dayun"))
        context = support.candidates[0].context
        expected = FIXTURE["evidence_discrimination"]
        exact = next(
            row for row in context.support_evidence_candidates
            if row.visible_stem_instance_id == expected["visible_stem_instance_id"]
            and row.supporting_branch_instance_id
            == expected["exact_supporting_branch_instance_id"]
            and row.evidence_class == EXACT_HIDDEN_STEM_MATCH
        )
        same = next(
            row for row in context.support_evidence_candidates
            if row.visible_stem_instance_id == expected["visible_stem_instance_id"]
            and row.supporting_branch_instance_id
            == expected["same_element_supporting_branch_instance_id"]
            and row.evidence_class == SAME_ELEMENT_HIDDEN_SUPPORT
        )
        self.assertNotEqual(exact.candidate_id, same.candidate_id)
        self.assertTrue(exact.source_exposure_link_ids)
        self.assertFalse(same.source_exposure_link_ids)
        self.assertTrue(
            set(exact.matching_hidden_stem_instance_ids).isdisjoint(
                same.matching_hidden_stem_instance_ids
            )
        )
        self.assertIn(NATAL_MONTH_COMMAND, same.supporting_branch_role_ids)

    def test_every_evidence_candidate_replays_upstream_affinity_and_exposure_lineage(self) -> None:
        for key in FIXTURE["targets"]:
            with self.subTest(key=key):
                _, structural, support = self._stack(self._target(key))
                structural_context = structural.candidates[0].context
                support_context = support.candidates[0].context
                affinity_ids = {
                    row.fact_id for row in self.natal.chart.affinities
                } | {
                    row.fact_id for row in structural_context.dynamic_affinities
                }
                exposure_ids = {
                    row.link_id for row in self.natal.chart.exposures
                } | {
                    row.link_id for row in structural_context.dynamic_exposures
                }
                candidate_ids = set()
                for row in support_context.support_evidence_candidates:
                    self.assertNotIn(row.candidate_id, candidate_ids)
                    candidate_ids.add(row.candidate_id)
                    self.assertIn(row.source_affinity_fact_id, affinity_ids)
                    self.assertEqual(
                        tuple(sorted(row.matching_hidden_stem_instance_ids)),
                        row.matching_hidden_stem_instance_ids,
                    )
                    if row.evidence_class == EXACT_HIDDEN_STEM_MATCH:
                        self.assertTrue(row.source_exposure_link_ids)
                        self.assertTrue(
                            set(row.source_exposure_link_ids).issubset(exposure_ids)
                        )
                        self.assertEqual(
                            tuple(
                                sorted(
                                    f"EXPOSE:{hidden_id}->{row.visible_stem_instance_id}"
                                    for hidden_id in row.matching_hidden_stem_instance_ids
                                )
                            ),
                            row.source_exposure_link_ids,
                        )
                    elif row.evidence_class == SAME_ELEMENT_HIDDEN_SUPPORT:
                        self.assertFalse(row.source_exposure_link_ids)
                    else:
                        self.fail(f"unexpected evidence class: {row.evidence_class}")

    def test_natal_month_command_and_active_flow_month_scopes_remain_independent(self) -> None:
        before = self._stack(self._target("flow_month_before"))[2].candidates[0].context
        exact = self._stack(self._target("flow_month_exact"))[2].candidates[0].context
        self.assertEqual(before.natal_month_command, exact.natal_month_command)
        self.assertNotEqual(before.active_flow_solar_month, exact.active_flow_solar_month)
        self.assertEqual(NATAL_MONTH_COMMAND, exact.natal_month_command.role_id)
        self.assertEqual(ACTIVE_FLOW_SOLAR_MONTH, exact.active_flow_solar_month.role_id)
        for context in (before, exact):
            natal_ids = tuple(
                row.candidate_id
                for row in context.support_evidence_candidates
                if NATAL_MONTH_COMMAND in row.supporting_branch_role_ids
            )
            flow_ids = tuple(
                row.candidate_id
                for row in context.support_evidence_candidates
                if ACTIVE_FLOW_SOLAR_MONTH in row.supporting_branch_role_ids
            )
            self.assertEqual(
                natal_ids,
                context.natal_month_command_support_candidate_ids,
            )
            self.assertEqual(
                flow_ids,
                context.active_flow_solar_month_support_candidate_ids,
            )
            self.assertTrue(set(natal_ids).isdisjoint(flow_ids))

    def test_pre_dayun_multi_candidate_and_semantic_firewalls_never_create_a_root_winner(self) -> None:
        flow, _, support = self._stack(self._target("pre_dayun"))
        self.assertEqual("PRE_DAYUN", flow.candidates[0].context.active_dayun_kind)
        self.assertFalse(
            any(
                "DAYUN" in row.participant_layers
                for row in support.candidates[0].context.support_evidence_candidates
            )
        )
        projection = structural_support_projection(support.candidates[0])
        forbidden = {
            "root",
            "no_root",
            "root_strength",
            "strength",
            "weight",
            "grade",
            "score",
            "rank",
            "winner",
            "pattern",
            "useful_god",
            "prediction",
            "interpretation",
        }

        def walk(value):
            if isinstance(value, dict):
                self.assertTrue(forbidden.isdisjoint(value))
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(projection)

        natal = self._natal(
            datetime(2025, 2, 7, 10, 10),
            uncertainty_seconds=120,
        )
        temporal = self._temporal(natal)
        flow2, structural2, support2 = self._stack(
            datetime(2026, 1, 1, tzinfo=timezone.utc),
            natal=natal,
            temporal=temporal,
        )
        self.assertEqual("MULTI_CANDIDATE", structural2.status)
        self.assertEqual("MULTI_CANDIDATE", support2.status)
        self.assertEqual(len(structural2.candidates), len(support2.candidates))
        self.assertEqual(len(flow2.candidates), len(support2.candidates))
        self.assertEqual(
            len(support2.candidates),
            len(
                {
                    row.context.upstream_structural_fact_hash
                    for row in support2.candidates
                }
            ),
        )


if __name__ == "__main__":
    unittest.main()
