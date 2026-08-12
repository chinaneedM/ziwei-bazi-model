from __future__ import annotations

import unittest

from fortune_training.bazi_classical_resolution_effect_disposition import (
    resolution_effect_hash_bundle,
    validate_resolution_effect_envelope,
)
import test_bazi_classical_resolution_effect_disposition_integrity_r1 as unit8_integrity_tests


class BaziClassicalResolutionEffectDispositionLineageIntegrityR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        source = unit8_integrity_tests.BaziClassicalResolutionEffectDispositionIntegrityR1Tests
        source.setUpClass()
        cls.source = source

    def test_recomputed_unit8_hash_cannot_hide_lineage_binding_tamper(self):
        source = self.source
        envelope = source.synthetic_envelope
        changed_lineage = (
            *envelope.lineage_binding_keys[:-1],
            "RESOLUTION_EFFECT_DISPOSITION_PROFILE:TAMPERED:9.9.9",
        )
        recomputed = resolution_effect_hash_bundle(
            source.synthetic_source,
            envelope.fragment_projections,
            envelope.source_record_candidate_sets,
            envelope.effect_channel_index,
            envelope.source_occurrence_index,
            envelope.local_closure_index,
            envelope.projected_candidate_projection_ids,
            envelope.projected_resolution_effect_disposition_ids,
            changed_lineage,
            source.profile,
        )
        report = validate_resolution_effect_envelope(
            source.synthetic_source,
            envelope.fragment_projections,
            envelope.source_record_candidate_sets,
            envelope.effect_channel_index,
            envelope.source_occurrence_index,
            envelope.local_closure_index,
            envelope.projected_candidate_projection_ids,
            envelope.projected_resolution_effect_disposition_ids,
            changed_lineage,
            source.profile,
            recomputed,
        )
        self.assertEqual("FAIL", report.status)
        self.assertIn(
            "UNIT8_LINEAGE_BINDING_REPLAY_MISMATCH",
            {row.code for row in report.diagnostics},
        )


if __name__ == "__main__":
    unittest.main()
