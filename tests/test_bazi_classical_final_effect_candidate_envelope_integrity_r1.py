from __future__ import annotations

import unittest
from dataclasses import replace

from fortune_training.bazi_classical_final_effect_candidate_envelope import (
    BaziClassicalFinalEffectCandidateEnvelopeEngine,
    build_expected_indexes,
    final_effect_hash_bundle,
    validate_final_effect_envelope,
)
from test_bazi_classical_final_effect_candidate_envelope_r1 import (
    BaziClassicalFinalEffectCandidateEnvelopeR1Tests as Unit7Stack,
)


class BaziClassicalFinalEffectCandidateEnvelopeIntegrityR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Unit7Stack.setUpClass()
        cls.profile = Unit7Stack.profile
        cls.stack = Unit7Stack.cross

    @staticmethod
    def _first_candidate(result):
        for outer in result.candidates:
            for index, fragment in enumerate(outer.fragment_envelopes):
                if fragment.final_candidates:
                    return outer, index, fragment
        raise AssertionError("no Unit 7 candidate fixture")

    def _validate_changed_fragments(self, outer, fragments):
        effect, admission, semantic, mechanism, allocation, _, _ = self.stack
        source_allocation = next(row for row in allocation.candidates if row.allocation_envelope_id == outer.source_allocation_envelope_id)
        source_mechanism = next(row for row in mechanism.candidates if row.mechanism_closure_envelope_id == outer.source_mechanism_closure_envelope_id)
        source_semantic = next(row for row in semantic.candidates if row.semantic_projection_envelope_id == outer.source_semantic_projection_envelope_id)
        source_admission = next(row for row in admission.candidates if row.admission_envelope_id == outer.source_admission_envelope_id)
        source_effect = next(row for row in effect.candidates if row.effect_envelope_id == outer.source_effect_envelope_id)
        candidates = tuple(candidate for fragment in fragments for candidate in fragment.final_candidates)
        indexes = build_expected_indexes(candidates)
        candidate_ids = tuple(row.final_candidate_id for row in candidates)
        hashes = final_effect_hash_bundle(
            source_allocation,
            fragments,
            outer.source_record_candidate_sets,
            *indexes,
            candidate_ids,
            outer.lineage_binding_keys,
            self.profile,
        )
        return validate_final_effect_envelope(
            source_allocation,
            source_mechanism,
            source_semantic,
            source_admission,
            source_effect,
            fragments,
            outer.source_record_candidate_sets,
            *indexes,
            candidate_ids,
            outer.lineage_binding_keys,
            self.profile,
            hashes,
        )

    def test_stale_unit6_payload_fails_closed(self):
        *_, allocation, request, _ = self.stack
        outer = allocation.candidates[0]
        fragment = outer.fragment_allocation_projections[0]
        changed = replace(fragment, source_occurrence_id=f"{fragment.source_occurrence_id}:TAMPER")
        changed_outer = replace(outer, fragment_allocation_projections=(changed, *outer.fragment_allocation_projections[1:]))
        changed_resolution = replace(allocation, candidates=(changed_outer, *allocation.candidates[1:]))
        result = BaziClassicalFinalEffectCandidateEnvelopeEngine().resolve_typed(
            replace(request, source_allocation_resolution=changed_resolution)
        )
        self.assertEqual("FAILED", result.status)
        self.assertTrue(any("UPSTREAM_UNIT6_ALLOCATION_REPLAY_MISMATCH" in row for row in result.diagnostics))

    def test_duplicate_unit6_outer_lineage_fails_closed(self):
        *_, allocation, request, _ = self.stack
        duplicate = replace(allocation, status="MULTI_CANDIDATE", candidates=(allocation.candidates[0], allocation.candidates[0]))
        result = BaziClassicalFinalEffectCandidateEnvelopeEngine().resolve_typed(
            replace(request, source_allocation_resolution=duplicate)
        )
        self.assertEqual("FAILED", result.status)
        self.assertTrue(any("UPSTREAM_UNIT6_OUTER_LINEAGE_PROJECTED_MORE_THAN_ONCE" in row for row in result.diagnostics))

    def test_recomputed_hashes_do_not_hide_changed_closure_status(self):
        outer, index, fragment = self._first_candidate(self.stack[-1])
        candidate = fragment.final_candidates[0]
        row = candidate.closure_governance_rows[0]
        changed_row = replace(row, runtime_dependency_status="AVAILABLE_EXACTLY")
        changed_candidate = replace(candidate, closure_governance_rows=(changed_row, *candidate.closure_governance_rows[1:]))
        changed_fragment = replace(fragment, final_candidates=(changed_candidate, *fragment.final_candidates[1:]))
        fragments = list(outer.fragment_envelopes)
        fragments[index] = changed_fragment
        report = self._validate_changed_fragments(outer, tuple(fragments))
        self.assertEqual("FAIL", report.status)
        self.assertTrue(any(row.code == "FINAL_CANDIDATE_SEMANTIC_REPLAY_MISMATCH" for row in report.diagnostics))

    def test_recomputed_hashes_do_not_hide_candidate_deletion(self):
        outer, index, fragment = self._first_candidate(self.stack[-1])
        changed_fragment = replace(
            fragment,
            final_candidates=fragment.final_candidates[1:],
            final_candidate_ids=fragment.final_candidate_ids[1:],
        )
        fragments = list(outer.fragment_envelopes)
        fragments[index] = changed_fragment
        report = self._validate_changed_fragments(outer, tuple(fragments))
        self.assertEqual("FAIL", report.status)
        self.assertTrue(any(row.code == "FINAL_FRAGMENT_SOURCE_CHAIN_REPLAY_MISMATCH" for row in report.diagnostics))


if __name__ == "__main__":
    unittest.main()
