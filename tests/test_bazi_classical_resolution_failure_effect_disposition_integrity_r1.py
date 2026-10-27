from __future__ import annotations

import unittest
from dataclasses import replace

from fortune_training.bazi_classical_resolution_failure_effect_disposition import (
    BaziClassicalResolutionFailureEffectDispositionEngine,
    bazi_classical_resolution_failure_effect_disposition_r1_profile,
    resolution_failure_effect_hash_bundle,
    validate_resolution_failure_effect_envelope,
)
from fortune_training.bazi_classical_resolution_failure_effect_disposition.engine import (
    _project_envelope,
)
import test_bazi_classical_final_effect_candidate_envelope_r1 as unit7_tests
import test_bazi_classical_resolution_failure_effect_disposition_r1 as unit9_tests


class BaziClassicalResolutionFailureEffectDispositionIntegrityR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        unit9_tests.BaziClassicalResolutionFailureEffectDispositionR1Tests.setUpClass()
        cls.profile = bazi_classical_resolution_failure_effect_disposition_r1_profile()
        cls.real_request = (
            unit9_tests.BaziClassicalResolutionFailureEffectDispositionR1Tests.cross[0]
        )
        cls.synthetic_source = cls._synthetic_source_outer()
        cls.synthetic_envelope = _project_envelope(cls.synthetic_source, cls.profile)

    @classmethod
    def _synthetic_source_outer(cls):
        source = unit7_tests.BaziClassicalFinalEffectCandidateEnvelopeR1Tests
        real_outer = source.cross[-1].candidates[0]
        failure = (
            unit9_tests.BaziClassicalResolutionFailureEffectDispositionR1Tests.failure_candidate
        )
        base_fragment = real_outer.fragment_envelopes[0]
        controlled_fragment = replace(
            base_fragment,
            final_fragment_status="FINAL_EFFECT_CANDIDATES_ASSEMBLED",
            source_semantic_candidate_ids=(failure.source_semantic_candidate_id,),
            source_mechanism_proposal_ids=(failure.source_mechanism_proposal_id,),
            source_allocation_elaboration_ids=(failure.source_allocation_elaboration_id,),
            final_candidates=(failure,),
            final_candidate_ids=(failure.final_candidate_id,),
        )
        fragments = (controlled_fragment, *real_outer.fragment_envelopes[1:])
        return replace(real_outer, fragment_envelopes=fragments)

    def _recomputed_hashes(self, *, fragments=None, source_sets=None, lineage=None):
        envelope = self.synthetic_envelope
        return resolution_failure_effect_hash_bundle(
            self.synthetic_source,
            envelope.fragment_projections if fragments is None else fragments,
            envelope.source_record_candidate_sets if source_sets is None else source_sets,
            envelope.effect_channel_index,
            envelope.source_occurrence_index,
            envelope.local_closure_index,
            envelope.projected_candidate_projection_ids,
            envelope.projected_resolution_failure_effect_disposition_ids,
            envelope.lineage_binding_keys if lineage is None else lineage,
            self.profile,
        )

    def _validate(
        self,
        *,
        fragments=None,
        source_sets=None,
        lineage=None,
        hashes=None,
    ):
        envelope = self.synthetic_envelope
        fragments = envelope.fragment_projections if fragments is None else fragments
        source_sets = (
            envelope.source_record_candidate_sets
            if source_sets is None
            else source_sets
        )
        lineage = envelope.lineage_binding_keys if lineage is None else lineage
        hashes = envelope.hashes if hashes is None else hashes
        return validate_resolution_failure_effect_envelope(
            self.synthetic_source,
            fragments,
            source_sets,
            envelope.effect_channel_index,
            envelope.source_occurrence_index,
            envelope.local_closure_index,
            envelope.projected_candidate_projection_ids,
            envelope.projected_resolution_failure_effect_disposition_ids,
            lineage,
            self.profile,
            hashes,
        )

    def test_recomputed_unit9_hash_cannot_hide_restoration_semantic_tamper(self):
        envelope = self.synthetic_envelope
        fragment = envelope.fragment_projections[0]
        projection = fragment.candidate_projections[0]
        disposition = projection.resolution_failure_effect_dispositions[0]
        changed_disposition = replace(
            disposition,
            resolution_mechanism_disposition="RESTORED",
        )
        changed_projection = replace(
            projection,
            resolution_failure_effect_dispositions=(changed_disposition,),
        )
        changed_fragment = replace(
            fragment,
            candidate_projections=(
                changed_projection,
                *fragment.candidate_projections[1:],
            ),
        )
        changed_fragments = (
            changed_fragment,
            *envelope.fragment_projections[1:],
        )
        hashes = self._recomputed_hashes(fragments=changed_fragments)
        report = self._validate(fragments=changed_fragments, hashes=hashes)
        self.assertEqual("FAIL", report.status)
        self.assertIn(
            "UNIT9_FRAGMENT_SEMANTIC_REPLAY_MISMATCH",
            {row.code for row in report.diagnostics},
        )

    def test_recomputed_unit9_hash_cannot_hide_source_record_factorization_tamper(self):
        envelope = self.synthetic_envelope
        changed = replace(
            envelope.source_record_candidate_sets[0],
            source_occurrence_id="TAMPERED-SOURCE-OCCURRENCE",
        )
        changed_sets = (changed, *envelope.source_record_candidate_sets[1:])
        hashes = self._recomputed_hashes(source_sets=changed_sets)
        report = self._validate(source_sets=changed_sets, hashes=hashes)
        self.assertEqual("FAIL", report.status)
        self.assertIn(
            "UNIT9_SOURCE_RECORD_FACTORIZATION_REPLAY_MISMATCH",
            {row.code for row in report.diagnostics},
        )

    def test_tampered_unit7_envelope_fails_full_replay_before_unit9_projection(self):
        request = self.real_request
        source = request.source_final_effect_resolution
        changed_outer = replace(
            source.candidates[0],
            candidate_truth_semantics="RELEASED",
        )
        changed_source = replace(
            source,
            candidates=(changed_outer, *source.candidates[1:]),
        )
        changed_request = replace(
            request,
            source_final_effect_resolution=changed_source,
        )
        result = BaziClassicalResolutionFailureEffectDispositionEngine().resolve_typed(
            changed_request
        )
        self.assertEqual("FAILED", result.status)
        self.assertTrue(any(
            value.startswith("UPSTREAM_UNIT7_FULL_RESOLUTION_REPLAY_MISMATCH:")
            for value in result.diagnostics
        ))

    def test_changed_failure_mapping_and_closure_status_fail_closed(self):
        candidate = (
            unit9_tests.BaziClassicalResolutionFailureEffectDispositionR1Tests.failure_candidate
        )
        bad_mechanism = replace(
            candidate,
            mechanism_proposal_kind="REVERSAL_OR_REAPPEARANCE_MECHANISM_PROPOSAL",
        )
        with self.assertRaises(ValueError):
            unit9_tests.expected_candidate_projection(bad_mechanism, self.profile)

        bad_row = replace(
            candidate.closure_governance_rows[0],
            runtime_dependency_status="AVAILABLE_EXACTLY",
        )
        bad_closure = replace(candidate, closure_governance_rows=(bad_row,))
        with self.assertRaises(ValueError):
            unit9_tests.expected_candidate_projection(bad_closure, self.profile)

    def test_recomputed_unit9_hash_cannot_hide_lineage_binding_tamper(self):
        envelope = self.synthetic_envelope
        changed_lineage = (
            *envelope.lineage_binding_keys[:-1],
            "RESOLUTION_FAILURE_EFFECT_DISPOSITION_PROFILE:TAMPERED:9.9.9",
        )
        hashes = self._recomputed_hashes(lineage=changed_lineage)
        report = self._validate(lineage=changed_lineage, hashes=hashes)
        self.assertEqual("FAIL", report.status)
        self.assertIn(
            "UNIT9_LINEAGE_BINDING_REPLAY_MISMATCH",
            {row.code for row in report.diagnostics},
        )

    def test_duplicate_unit7_outer_lineage_fails_closed(self):
        request = self.real_request
        source = request.source_final_effect_resolution
        duplicate = replace(
            source,
            status="MULTI_CANDIDATE",
            candidates=(source.candidates[0], source.candidates[0]),
        )
        result = BaziClassicalResolutionFailureEffectDispositionEngine().resolve_typed(
            replace(request, source_final_effect_resolution=duplicate)
        )
        self.assertEqual("FAILED", result.status)


if __name__ == "__main__":
    unittest.main()
