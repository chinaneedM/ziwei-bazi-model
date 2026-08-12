from __future__ import annotations

import unittest
from dataclasses import replace

from fortune_training.bazi_classical_final_effect_candidate_envelope import (
    BaziClassicalFinalEffectCandidateEnvelopeEngine,
)
from test_bazi_classical_final_effect_candidate_envelope_integrity_r1 import (
    BaziClassicalFinalEffectCandidateEnvelopeIntegrityR1Tests as Unit7Integrity,
)
from test_bazi_classical_final_effect_candidate_envelope_r1 import (
    BaziClassicalFinalEffectCandidateEnvelopeR1Tests as Unit7Stack,
)
from test_bazi_classical_non_selecting_participant_allocation_integrity_r1 import (
    BaziClassicalNonSelectingParticipantAllocationIntegrityR1Tests as Unit6Integrity,
)


class BaziClassicalFinalEffectCandidateEnvelopeTamperR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Unit7Stack.setUpClass()
        Unit7Integrity.setUpClass()
        Unit6Integrity.setUpClass()
        cls.stack = Unit7Stack.cross
        cls.integrity = Unit7Integrity(
            methodName="test_recomputed_hashes_do_not_hide_changed_closure_status"
        )

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
        changed_semantic = replace(
            semantic,
            candidates=(changed_outer, *semantic.candidates[1:]),
        )
        result = BaziClassicalFinalEffectCandidateEnvelopeEngine().resolve_typed(
            replace(request, source_semantic_candidate_resolution=changed_semantic)
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
        changed_mechanism = replace(
            mechanism,
            candidates=(changed_outer, *mechanism.candidates[1:]),
        )
        result = BaziClassicalFinalEffectCandidateEnvelopeEngine().resolve_typed(
            replace(request, source_mechanism_closure_resolution=changed_mechanism)
        )
        self.assertEqual("FAILED", result.status)

    def test_recomputed_unit7_hashes_do_not_hide_changed_candidate_kind(self):
        outer, index, fragment = self.integrity._first_candidate(self.stack[-1])
        candidate = fragment.final_candidates[0]
        changed_kind = (
            "SOURCE_GROUNDED_ATTENUATION_CANDIDATE"
            if candidate.semantic_candidate_kind
            != "SOURCE_GROUNDED_ATTENUATION_CANDIDATE"
            else "SOURCE_GROUNDED_RESOLUTION_CANDIDATE"
        )
        changed_candidate = replace(candidate, semantic_candidate_kind=changed_kind)
        changed_fragment = replace(
            fragment,
            final_candidates=(changed_candidate, *fragment.final_candidates[1:]),
        )
        fragments = list(outer.fragment_envelopes)
        fragments[index] = changed_fragment
        report = self.integrity._validate_changed_fragments(outer, tuple(fragments))
        self.assertEqual("FAIL", report.status)
        self.assertTrue(
            any(
                row.code == "FINAL_CANDIDATE_SEMANTIC_REPLAY_MISMATCH"
                for row in report.diagnostics
            )
        )

    def test_recomputed_unit7_hashes_do_not_hide_injected_synthetic_path(self):
        helper = Unit6Integrity(
            methodName="test_recomputed_hash_does_not_hide_synthetic_extra_path"
        )
        _, _, _, _, elaboration, _ = helper._controlled_allocation()
        observation = elaboration.allocation_domain_observations[0]
        legal_path = observation.path_candidates[0]
        synthetic_path = replace(
            legal_path,
            path_candidate_id=f"{legal_path.path_candidate_id}:UNIT7_SYNTHETIC",
        )
        tampered_observation = replace(
            observation,
            path_candidates=(legal_path, synthetic_path),
        )

        outer, index, fragment = self.integrity._first_candidate(self.stack[-1])
        candidate = fragment.final_candidates[0]
        changed_candidate = replace(
            candidate,
            allocation_domain_observations=(tampered_observation,),
        )
        changed_fragment = replace(
            fragment,
            final_candidates=(changed_candidate, *fragment.final_candidates[1:]),
        )
        fragments = list(outer.fragment_envelopes)
        fragments[index] = changed_fragment
        report = self.integrity._validate_changed_fragments(outer, tuple(fragments))
        self.assertEqual("FAIL", report.status)
        self.assertTrue(
            any(
                row.code == "FINAL_CANDIDATE_SEMANTIC_REPLAY_MISMATCH"
                for row in report.diagnostics
            )
        )


if __name__ == "__main__":
    unittest.main()
