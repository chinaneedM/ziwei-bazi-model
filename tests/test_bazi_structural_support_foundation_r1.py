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
)
from fortune_training.bazi_structural_support import (
    ACTIVE_FLOW_SOLAR_MONTH,
    EXACT_HIDDEN_STEM_MATCH,
    NATAL_MONTH_COMMAND,
    SAME_ELEMENT_HIDDEN_SUPPORT,
    BaziStructuralSupportEngine,
    BaziStructuralSupportRequest,
    bazi_structural_support_foundation_r1_profile,
    structural_support_hash_bundle,
    validate_structural_support_context,
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
    (
        ROOT
        / "tests"
        / "fixtures"
        / "bazi-structural-support-foundation-r1.json"
    ).read_text(encoding="utf-8")
)


class BaziStructuralSupportFoundationR1Tests(unittest.TestCase):
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
        result = cls.chart_engine.resolve_typed(BaziChartRequest(
            BirthInput(
                reported_local_datetime=local,
                birth_place="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone_id="Asia/Shanghai",
                **kwargs,
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
            bazi_temporal_v1_continuous_profile(),
            dayun_count=4,
        ))
        if not result.candidates:
            raise RuntimeError(f"fixture requires Temporal candidates: {result.status}")
        return result

    @classmethod
    def _flow(cls, target, natal=None, temporal=None):
        natal = natal or cls.natal
        temporal = temporal or cls.temporal
        return cls.flow_engine.resolve_typed(BaziFlowRequest(
            natal,
            temporal.candidates,
            target,
            cls.chart_profile,
        ))

    @classmethod
    def _stack(cls, target, natal=None, temporal=None):
        natal = natal or cls.natal
        flow = cls._flow(target, natal, temporal)
        structural = cls.structural_engine.resolve_typed(BaziStructuralRequest(
            natal,
            flow.candidates,
            cls.structural_profile,
        ))
        support = cls.support_engine.resolve_typed(BaziStructuralSupportRequest(
            natal,
            flow.candidates,
            structural.candidates,
            cls.support_profile,
        ))
        return flow, structural, support

    @classmethod
    def _fixture_target(cls, key):
        row = FIXTURE["targets"][key]
        target = cls.chart_engine.time_calendar.solar_terms.term(
            row["solar_term_year"], row["solar_longitude_degrees"]
        ).utc_instant
        return target + timedelta(microseconds=row.get("offset_microseconds", 0))

    def test_natal_month_command_is_fixed_typed_role_across_target_months(self):
        first = self._stack(
            self._fixture_target("pre_dayun")
        )[2].candidates[0].context
        second = self._stack(
            self._fixture_target("flow_month_exact")
        )[2].candidates[0].context
        expected = FIXTURE["natal"]["expected_month_command"]
        self.assertEqual(NATAL_MONTH_COMMAND, first.natal_month_command.role_id)
        self.assertEqual(expected["source_branch_instance_id"], first.natal_month_command.source_branch_instance_id)
        self.assertEqual(expected["ganzhi"], first.natal_month_command.natal_month_ganzhi)
        self.assertEqual(expected["branch"], first.natal_month_command.branch)
        self.assertEqual(first.natal_month_command, second.natal_month_command)
        self.assertNotEqual(
            first.active_flow_solar_month.reference_id,
            second.active_flow_solar_month.reference_id,
        )
        self.assertEqual(ACTIVE_FLOW_SOLAR_MONTH, second.active_flow_solar_month.role_id)
        self.assertNotEqual(
            second.natal_month_command.role_id,
            second.active_flow_solar_month.role_id,
        )
        same_flow_month = self._stack(
            self._fixture_target("flow_month_exact") + timedelta(days=1)
        )[2].candidates[0].context
        self.assertEqual(
            second.active_flow_solar_month.reference_id,
            same_flow_month.active_flow_solar_month.reference_id,
        )
        self.assertNotEqual(
            second.active_flow_solar_month.upstream_flow_fact_hash,
            same_flow_month.active_flow_solar_month.upstream_flow_fact_hash,
        )

    def test_exact_jie_selects_new_flow_month_and_only_month_bound_evidence_turns_over(self):
        before = self._stack(
            self._fixture_target("flow_month_before")
        )[2].candidates[0].context
        exact = self._stack(
            self._fixture_target("flow_month_exact")
        )[2].candidates[0].context
        self.assertEqual(before.natal_month_command, exact.natal_month_command)
        self.assertNotEqual(before.active_flow_solar_month, exact.active_flow_solar_month)
        self.assertEqual(
            self._fixture_target("flow_month_exact"),
            exact.active_flow_solar_month.start_utc,
        )
        before_month_id = before.active_flow_solar_month.source_temporal_branch_instance_id
        exact_month_id = exact.active_flow_solar_month.source_temporal_branch_instance_id
        before_month_stem_id = before_month_id.removesuffix(".BRANCH") + ".STEM"
        exact_month_stem_id = exact_month_id.removesuffix(".BRANCH") + ".STEM"

        def stable_rows(context, month_ids):
            return {
                row for row in context.support_evidence_candidates
                if row.visible_stem_instance_id not in month_ids
                and row.supporting_branch_instance_id not in month_ids
            }

        self.assertEqual(
            stable_rows(before, {before_month_id, before_month_stem_id}),
            stable_rows(exact, {exact_month_id, exact_month_stem_id}),
        )

    def test_exact_and_same_element_different_stem_remain_distinct_candidates(self):
        context = self._stack(
            self._fixture_target("pre_dayun")
        )[2].candidates[0].context
        expected = FIXTURE["evidence_discrimination"]
        exact = next(
            row for row in context.support_evidence_candidates
            if row.visible_stem_instance_id == expected["visible_stem_instance_id"]
            and row.supporting_branch_instance_id == expected["exact_supporting_branch_instance_id"]
            and row.evidence_class == EXACT_HIDDEN_STEM_MATCH
        )
        same = next(
            row for row in context.support_evidence_candidates
            if row.visible_stem_instance_id == expected["visible_stem_instance_id"]
            and row.supporting_branch_instance_id == expected["same_element_supporting_branch_instance_id"]
            and row.evidence_class == SAME_ELEMENT_HIDDEN_SUPPORT
        )
        self.assertNotEqual(exact.candidate_id, same.candidate_id)
        self.assertTrue(exact.source_exposure_link_ids)
        self.assertFalse(same.source_exposure_link_ids)
        self.assertIn(NATAL_MONTH_COMMAND, same.supporting_branch_role_ids)
        self.assertFalse(hasattr(exact, "root"))
        self.assertFalse(hasattr(exact, "strength"))
        self.assertFalse(hasattr(exact, "weight"))

    def test_cross_layer_repeated_characters_preserve_occurrence_identity(self):
        context = self._stack(
            self._fixture_target("repeated_occurrence")
        )[2].candidates[0].context
        yi_visible_ids = {
            row.visible_stem_instance_id
            for row in context.support_evidence_candidates
            if row.visible_stem_instance_id in {
                stem.instance_id
                for stem in self.natal.chart.stems
                if stem.stem == "乙"
            } or "ANNUAL" in row.visible_stem_instance_id
        }
        si_branch_ids = {
            row.supporting_branch_instance_id
            for row in context.support_evidence_candidates
            if row.supporting_branch_instance_id in {
                branch.instance_id
                for branch in self.natal.chart.branches
                if branch.branch == "巳"
            } or "MONTHLY" in row.supporting_branch_instance_id
        }
        self.assertGreaterEqual(len(yi_visible_ids), 3)
        self.assertGreaterEqual(len(si_branch_ids), 3)
        self.assertEqual(
            len(context.support_evidence_candidates),
            len({row.candidate_id for row in context.support_evidence_candidates}),
        )

    def test_pre_dayun_has_natal_annual_monthly_support_without_fake_dayun(self):
        flow, structural, support = self._stack(self._fixture_target("pre_dayun"))
        self.assertEqual("PRE_DAYUN", flow.candidates[0].context.active_dayun_kind)
        self.assertFalse(any(
            "DAYUN" in row.participant_layers
            for row in support.candidates[0].context.support_evidence_candidates
        ))
        self.assertTrue(any(
            "ANNUAL" in row.participant_layers
            for row in support.candidates[0].context.support_evidence_candidates
        ))
        self.assertTrue(any(
            "MONTHLY" in row.participant_layers
            for row in support.candidates[0].context.support_evidence_candidates
        ))
        self.assertEqual("PASS", structural.candidates[0].integrity.status)

    def test_multi_structural_candidates_are_preserved(self):
        natal = self._natal(
            datetime(2025, 2, 7, 10, 10), uncertainty_seconds=120
        )
        temporal = self._temporal(natal)
        flow, structural, support = self._stack(
            datetime(2026, 1, 1, tzinfo=timezone.utc), natal, temporal
        )
        self.assertEqual("MULTI_CANDIDATE", structural.status)
        self.assertEqual("MULTI_CANDIDATE", support.status)
        self.assertEqual(len(structural.candidates), len(support.candidates))
        self.assertEqual(
            len(support.candidates),
            len({row.context.upstream_structural_fact_hash for row in support.candidates}),
        )
        self.assertEqual(len(flow.candidates), len(support.candidates))

    def test_only_identical_complete_support_payload_deduplicates(self):
        target = self._fixture_target("flow_month_exact")
        flow, structural, _ = self._stack(target)
        candidate = structural.candidates[0]
        result = self.support_engine.resolve_typed(BaziStructuralSupportRequest(
            self.natal,
            flow.candidates,
            (candidate, candidate),
            self.support_profile,
        ))
        self.assertEqual("RESOLVED", result.status)
        self.assertEqual(1, len(result.candidates))
        self.assertEqual((0, 1), result.candidates[0].source_structural_candidate_indices)

    def test_upstream_hashes_and_facts_remain_byte_stable(self):
        expected = FIXTURE["natal"]
        original_natal_hashes = self.natal.hashes
        original_natal_state = self.natal.chart
        flow, structural, support = self._stack(
            self._fixture_target("flow_month_exact")
        )
        original_flow_hashes = flow.candidates[0].hashes
        original_structural_hashes = structural.candidates[0].hashes
        self.assertEqual(expected["expected_fact_hash"], self.natal.hashes.fact_hash)
        self.assertEqual(expected["expected_pillars"], [
            row.ganzhi for row in self.natal.chart.pillars
        ])
        self.assertEqual(original_natal_hashes, self.natal.hashes)
        self.assertEqual(original_natal_state, self.natal.chart)
        self.assertEqual(original_flow_hashes, flow.candidates[0].hashes)
        self.assertEqual(original_structural_hashes, structural.candidates[0].hashes)
        self.assertNotEqual(
            support.candidates[0].hashes.fact_hash,
            structural.candidates[0].hashes.fact_hash,
        )

    def test_integrity_and_hash_replay_detect_tampering(self):
        flow, structural, support = self._stack(
            self._fixture_target("flow_month_exact")
        )
        row = support.candidates[0]
        tampered_role = replace(
            row.context.natal_month_command,
            source_branch_instance_id="DAY.BRANCH",
        )
        tampered = replace(row.context, natal_month_command=tampered_role)
        report = validate_structural_support_context(
            tampered,
            self.natal,
            flow.candidates[0],
            structural.candidates[0],
            self.support_profile,
            row.hashes,
        )
        codes = {item.code for item in report.diagnostics}
        self.assertEqual("FAIL", report.status)
        self.assertIn("NATAL_MONTH_COMMAND_REPLAY_MISMATCH", codes)
        self.assertIn("NATAL_MONTH_COMMAND_BINDING_INVALID", codes)
        self.assertIn("SUPPORT_HASH_REPLAY_MISMATCH", codes)
        self.assertNotEqual(
            row.hashes.fact_hash,
            structural_support_hash_bundle(
                tampered,
                self.natal,
                flow.candidates[0],
                structural.candidates[0],
                self.support_profile,
            ).fact_hash,
        )


if __name__ == "__main__":
    unittest.main()
