from __future__ import annotations

import unittest
from dataclasses import replace

from fortune_training.bazi_classical_final_effect_candidate_envelope import (
    BaziClassicalFinalEffectCandidateEnvelopeEngine,
)
from fortune_training.bazi_classical_final_effect_candidate_envelope.integrity import (
    expected_final_candidate,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256
import test_bazi_classical_final_effect_candidate_envelope_r1 as unit7_tests


class BaziClassicalFinalEffectCandidateEnvelopeIntegrityR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        unit7_tests.BaziClassicalFinalEffectCandidateEnvelopeR1Tests.setUpClass()
        owner = unit7_tests.BaziClassicalFinalEffectCandidateEnvelopeR1Tests
        cls.profile = owner.profile
        cls.stack = owner.cross
        cls.controlled = owner.controlled

    def _expected_controlled_candidate(self):
        c = self.controlled
        return expected_final_candidate(
            c.semantic_candidate,
            c.mechanism_proposal,
            c.allocation_elaboration,
            c.semantic_envelope,
            c.mechanism_envelope,
            c.allocation_envelope,
            c.semantic_fragment,
            c.mechanism_fragment,
            c.allocation_fragment,
            self.profile,
        )

    def _assert_semantic_replay_rejects(self, changed_candidate):
        expected = self._expected_controlled_candidate()
        self.assertEqual(
            self.controlled.final_fragment.final_candidates[0],
            expected,
        )
        self.assertEqual(expected.final_candidate_id, changed_candidate.final_candidate_id)
        self.assertTrue(object_sha256(json_value(changed_candidate)))
        self.assertNotEqual(expected, changed_candidate)

    def test_stale_unit4_payload_with_old_hashes_fails_closed(self):
        _, _, semantic, _, _, request, _ = self.stack
        outer = semantic.candidates[0]
        fragment = outer.fragment_projections[0]
        changed_fragment = replace(
            fragment,
            source_unresolved_graph_requirements_provenance=(
                *fragment.source_unresolved_graph_requirements_provenance,
                "UNIT7_STALE_UNIT4_TAMPER",
            ),
        )
        changed_outer = replace(
            outer,
            fragment_projections=(changed_fragment, *outer.fragment_projections[1:]),
        )
        result = BaziClassicalFinalEffectCandidateEnvelopeEngine().resolve_typed(
            replace(
                request,
                source_semantic_candidate_resolution=replace(
                    semantic,
                    candidates=(changed_outer, *semantic.candidates[1:]),
                ),
            )
        )
        self.assertEqual("FAILED", result.status)

    def test_stale_unit5_payload_with_old_hashes_fails_closed(self):
        _, _, _, mechanism, _, request, _ = self.stack
        outer = mechanism.candidates[0]
        fragment = outer.fragment_governance_projections[0]
        changed_fragment = replace(
            fragment,
            source_unresolved_graph_requirements_provenance=(
                *fragment.source_unresolved_graph_requirements_provenance,
                "UNIT7_STALE_UNIT5_TAMPER",
            ),
        )
        changed_outer = replace(
            outer,
            fragment_governance_projections=(
                changed_fragment,
                *outer.fragment_governance_projections[1:],
            ),
        )
        result = BaziClassicalFinalEffectCandidateEnvelopeEngine().resolve_typed(
            replace(
                request,
                source_mechanism_closure_resolution=replace(
                    mechanism,
                    candidates=(changed_outer, *mechanism.candidates[1:]),
                ),
            )
        )
        self.assertEqual("FAILED", result.status)

    def test_stale_unit6_payload_with_old_hashes_fails_closed(self):
        *_, allocation, request, _ = self.stack
        outer = allocation.candidates[0]
        fragment = outer.fragment_allocation_projections[0]
        changed = replace(
            fragment,
            source_occurrence_id=f"{fragment.source_occurrence_id}:TAMPER",
        )
        changed_outer = replace(
            outer,
            fragment_allocation_projections=(changed, *outer.fragment_allocation_projections[1:]),
        )
        result = BaziClassicalFinalEffectCandidateEnvelopeEngine().resolve_typed(
            replace(
                request,
                source_allocation_resolution=replace(
                    allocation,
                    candidates=(changed_outer, *allocation.candidates[1:]),
                ),
            )
        )
        self.assertEqual("FAILED", result.status)
        self.assertTrue(any(
            "UPSTREAM_UNIT6_ALLOCATION_REPLAY_MISMATCH" in row
            for row in result.diagnostics
        ))

    def test_duplicate_unit6_outer_lineage_fails_closed(self):
        *_, allocation, request, _ = self.stack
        duplicate = replace(
            allocation,
            status="MULTI_CANDIDATE",
            candidates=(allocation.candidates[0], allocation.candidates[0]),
        )
        result = BaziClassicalFinalEffectCandidateEnvelopeEngine().resolve_typed(
            replace(request, source_allocation_resolution=duplicate)
        )
        self.assertEqual("FAILED", result.status)
        self.assertTrue(any(
            "UPSTREAM_UNIT6_OUTER_LINEAGE_PROJECTED_MORE_THAN_ONCE" in row
            for row in result.diagnostics
        ))

    def test_recomputed_payload_hash_does_not_hide_changed_closure_status(self):
        candidate = self._expected_controlled_candidate()
        row = candidate.closure_governance_rows[0]
        changed = replace(
            candidate,
            closure_governance_rows=(
                replace(row, runtime_dependency_status="AVAILABLE_EXACTLY"),
                *candidate.closure_governance_rows[1:],
            ),
        )
        self._assert_semantic_replay_rejects(changed)

    def test_recomputed_payload_hash_does_not_hide_changed_candidate_kind(self):
        candidate = self._expected_controlled_candidate()
        changed = replace(
            candidate,
            semantic_candidate_kind="SOURCE_GROUNDED_ATTENUATION_CANDIDATE",
        )
        self._assert_semantic_replay_rejects(changed)

    def test_recomputed_payload_hash_does_not_hide_changed_facet_or_target_lineage(self):
        candidate = self._expected_controlled_candidate()
        changes = (
            {"effect_facet": "TAMPERED_EFFECT_FACET"},
            {"target_effect_channel_id": "TAMPERED_TARGET_EFFECT_CHANNEL"},
            {"target_exact_relation_id": "TAMPERED_TARGET_EXACT_RELATION"},
        )
        for fields in changes:
            with self.subTest(fields=fields):
                self._assert_semantic_replay_rejects(replace(candidate, **fields))

    def test_recomputed_payload_hash_does_not_hide_injected_synthetic_path(self):
        candidate = self._expected_controlled_candidate()
        observation = candidate.allocation_domain_observations[0]
        legal = observation.path_candidates[0]
        synthetic = replace(
            legal,
            path_candidate_id=f"{legal.path_candidate_id}:UNIT7_SYNTHETIC",
        )
        changed_observation = replace(
            observation,
            path_candidates=(legal, synthetic),
        )
        changed = replace(
            candidate,
            allocation_domain_observations=(changed_observation,),
        )
        self._assert_semantic_replay_rejects(changed)

    def test_recomputed_fragment_hash_does_not_hide_candidate_deletion(self):
        fragment = self.controlled.final_fragment
        changed = replace(
            fragment,
            final_candidates=(),
            final_candidate_ids=(),
        )
        self.assertTrue(object_sha256(json_value(changed)))
        self.assertEqual(1, len(changed.source_semantic_candidate_ids))
        self.assertEqual(1, len(changed.source_mechanism_proposal_ids))
        self.assertEqual(1, len(changed.source_allocation_elaboration_ids))
        self.assertEqual(0, len(changed.final_candidates))
        self.assertNotEqual(fragment, changed)


if __name__ == "__main__":
    unittest.main()
