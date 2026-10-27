from __future__ import annotations

import json
import unittest
from datetime import datetime
from pathlib import Path

from fortune_training.bazi_application.structural_projection import (
    STRUCTURAL_EXCLUDED_LAYERS,
    STRUCTURAL_PROJECTION_ALGORITHM_VERSION,
    STRUCTURAL_SEMANTIC_SCOPE,
    STRUCTURAL_SUPPORTED_LAYERS,
    structural_projection,
    validate_structural_projection,
)
from fortune_training.bazi_chart import (
    BaziChartFoundation,
    BaziChartRequest,
    bazi_foundation_v1_profile,
)
from fortune_training.bazi_chart.hidden_stems import (
    AFFINITY_ALGORITHM_VERSION,
    HIDDEN_STEM_ALGORITHM_VERSION,
    generate_hidden_stems,
)
from fortune_training.bazi_chart.historical_relation_candidates import (
    HISTORICAL_RELATION_CANDIDATE_RULE_SET_ID,
    HISTORICAL_RELATION_CANDIDATE_SELECTION_STATUS,
)
from fortune_training.bazi_chart.registries import RAW_RELATION_RULE_SET_ID
from fortune_training.bazi_chart.relations import RAW_RELATION_ALGORITHM_VERSION
from fortune_training.bazi_chart.ten_gods import TEN_GOD_ALGORITHM_VERSION, ten_god
from fortune_training.bazi_flow import BaziFlowEngine, BaziFlowRequest
from fortune_training.bazi_structural import (
    BaziStructuralEngine,
    BaziStructuralRequest,
    bazi_structural_context_r1_profile,
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


class BaziStructuralContextSourcePreservingProjectionAuditR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.chart_engine = BaziChartFoundation.from_repository(ROOT)
        cls.chart_profile = bazi_foundation_v1_profile(
            cls.chart_engine.time_calendar.policy_registry
        )
        cls.natal = cls.chart_engine.resolve_typed(
            BaziChartRequest(
                BirthInput(
                    datetime(2025, 2, 7, 10, 10),
                    "Beijing",
                    39.9042,
                    116.4074,
                    "Asia/Shanghai",
                ),
                cls.chart_profile,
            )
        ).candidates[0]
        cls.temporal = BaziTemporalEngine().resolve_typed(
            BaziTemporalRequest(
                cls.natal,
                BaziSex.MALE,
                bazi_temporal_v1_continuous_profile(),
                dayun_count=4,
            )
        )
        cls.flow_engine = BaziFlowEngine(cls.chart_engine.time_calendar.bazi)
        cls.structural_engine = BaziStructuralEngine()
        cls.structural_profile = bazi_structural_context_r1_profile()

    @classmethod
    def target(cls, key: str):
        row = FIXTURE["targets"][key]
        return cls.chart_engine.time_calendar.solar_terms.term(
            row["solar_term_year"], row["solar_longitude_degrees"]
        ).utc_instant

    @classmethod
    def resolve_target(cls, target):
        flow = cls.flow_engine.resolve_typed(
            BaziFlowRequest(
                cls.natal,
                cls.temporal.candidates,
                target,
                cls.chart_profile,
            )
        )
        structural = cls.structural_engine.resolve_typed(
            BaziStructuralRequest(
                cls.natal,
                flow.candidates,
                cls.structural_profile,
            )
        )
        return flow, structural

    @classmethod
    def resolve(cls, key: str):
        return cls.resolve_target(cls.target(key))

    def test_four_fixture_targets_replay_valid_source_bound_projections(self) -> None:
        self.assertEqual(4, len(FIXTURE["targets"]))
        for key in FIXTURE["targets"]:
            with self.subTest(key=key):
                flow, structural = self.resolve(key)
                self.assertEqual(1, len(structural.candidates))
                candidate = structural.candidates[0]
                projection = structural_projection(candidate)
                source_index = candidate.source_flow_candidate_indices[0]
                self.assertTrue(
                    validate_structural_projection(
                        projection,
                        source_flow_candidate_index=source_index,
                        flow_fact_hash=flow.candidates[source_index].hashes.fact_hash,
                        structural_fact_hash=candidate.hashes.fact_hash,
                        structural_computation_hash=candidate.hashes.computation_hash,
                    )
                )
                self.assertEqual(candidate.hashes.fact_hash, projection["source_structural_fact_hash"])
                self.assertEqual(
                    candidate.hashes.computation_hash,
                    projection["source_structural_computation_hash"],
                )

    def test_shared_hidden_stem_and_ten_god_primitives_are_reused_exactly(self) -> None:
        _, structural = self.resolve("mixed_layer_fire_trine")
        context = structural.candidates[0].context
        self.assertEqual(
            generate_hidden_stems(context.active_temporal_branches),
            context.temporal_hidden_stems,
        )
        targets = {
            row.instance_id: row.stem for row in context.active_temporal_stems
        }
        targets.update({
            row.instance_id: row.stem for row in context.temporal_hidden_stems
        })
        self.assertEqual(set(targets), {
            row.target_instance_id for row in context.temporal_ten_gods
        })
        for binding in context.temporal_ten_gods:
            semantic_id, display_name = ten_god(
                context.natal_day_master_stem,
                targets[binding.target_instance_id],
            )
            self.assertEqual(context.natal_day_master_stem, binding.day_master_stem)
            self.assertEqual(semantic_id, binding.semantic_role_id)
            self.assertEqual(display_name, binding.display_name)
        self.assertEqual(HIDDEN_STEM_ALGORITHM_VERSION, context.algorithm_versions["hidden_stems"])
        self.assertEqual(TEN_GOD_ALGORITHM_VERSION, context.algorithm_versions["ten_gods"])
        self.assertEqual(AFFINITY_ALGORITHM_VERSION, context.algorithm_versions["affinity"])
        self.assertEqual(RAW_RELATION_ALGORITHM_VERSION, context.algorithm_versions["raw_relations"])

    def test_released_raw_core_and_historical_relation_sidecar_never_merge(self) -> None:
        _, structural = self.resolve("mixed_layer_fire_trine")
        relations = structural.candidates[0].context.dynamic_raw_relations
        self.assertTrue(relations)
        self.assertEqual(
            {RAW_RELATION_RULE_SET_ID},
            {row.rule_set_id for row in relations},
        )
        self.assertNotIn(
            HISTORICAL_RELATION_CANDIDATE_RULE_SET_ID,
            {row.rule_set_id for row in relations},
        )
        self.assertEqual(
            "PRESERVED_NOT_SELECTED",
            HISTORICAL_RELATION_CANDIDATE_SELECTION_STATUS,
        )

    def test_layer_boundary_and_pre_dayun_absence_are_preserved(self) -> None:
        from datetime import timedelta

        transition = self.temporal.candidates[0].state.jiaoyun.first_transition_utc
        flow_before, structural_before = self.resolve_target(
            transition - timedelta(microseconds=1)
        )
        self.assertEqual("PRE_DAYUN", flow_before.candidates[0].context.active_dayun_kind)
        before_projection = structural_projection(structural_before.candidates[0])
        self.assertEqual(["ANNUAL", "MONTHLY"], before_projection["active_layers"])
        self.assertEqual(list(STRUCTURAL_EXCLUDED_LAYERS), before_projection["excluded_layers"])
        self.assertFalse(any(
            row["layer"] == "DAYUN"
            for row in before_projection["participant_provenance"]
        ))

        flow_after, structural_after = self.resolve_target(transition)
        self.assertEqual("DAYUN", flow_after.candidates[0].context.active_dayun_kind)
        after_projection = structural_projection(structural_after.candidates[0])
        self.assertEqual(list(STRUCTURAL_SUPPORTED_LAYERS), after_projection["active_layers"])
        self.assertEqual(["XIAOYUN", "DAILY", "HOURLY"], after_projection["excluded_layers"])

    def test_occurrence_identity_and_interpretive_firewalls_remain_explicit(self) -> None:
        _, structural = self.resolve("repeated_occurrence")
        projection = structural_projection(structural.candidates[0])
        self.assertEqual("1.1.0", projection["profile_version"])
        self.assertEqual("1.1.0", STRUCTURAL_PROJECTION_ALGORITHM_VERSION)
        self.assertEqual(STRUCTURAL_SEMANTIC_SCOPE, projection["semantic_scope"])
        ids = [
            row["instance_id"]
            for row in projection["active_temporal_stems"]
            + projection["active_temporal_branches"]
        ]
        self.assertEqual(len(ids), len(set(ids)))
        forbidden = {
            "effect",
            "severity",
            "strength",
            "root_strength",
            "seasonal_strength",
            "winner",
            "transformation_succeeded",
            "relation_priority",
            "pattern",
            "useful_god",
            "prediction",
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


if __name__ == "__main__":
    unittest.main()
