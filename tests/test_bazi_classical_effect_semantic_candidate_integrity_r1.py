from __future__ import annotations

import unittest
from dataclasses import replace

from fortune_training.bazi_classical_effect_semantic_candidate import (
    BaziClassicalEffectSemanticCandidateProjectionEngine,
    BaziClassicalEffectSemanticCandidateProjectionError,
    BaziClassicalEffectSemanticCandidateProjectionRequest,
    bazi_classical_effect_semantic_candidate_projection_r1_profile,
    project_fragment_semantic_candidates,
)
from fortune_training.bazi_classical_effect_semantic_candidate.integrity import (
    replay_effect_envelope_self_contained,
)
from fortune_training.bazi_classical_resolver_admission import (
    BaziClassicalResolverAdmissionEngine,
    BaziClassicalResolverAdmissionRequest,
    bazi_classical_resolver_admission_strict_r1_profile,
    shen_zpzq_ch09_classical_interaction_r1_profile,
)
from test_bazi_classical_effect_constraint_graph_factorized_composition_r1 import (
    BaziClassicalEffectConstraintGraphFactorizedCompositionR1Tests as Unit2Stack,
)


class BaziClassicalEffectSemanticCandidateIntegrityR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Unit2Stack.setUpClass()
        cls.binding, cls.projection, _, cls.effect = Unit2Stack.cross_layer
        cls.admission = BaziClassicalResolverAdmissionEngine().resolve_typed(
            BaziClassicalResolverAdmissionRequest(
                cls.binding,
                cls.projection,
                cls.effect,
                shen_zpzq_ch09_classical_interaction_r1_profile(),
                bazi_classical_resolver_admission_strict_r1_profile(),
            )
        )
        if cls.admission.status == "FAILED":
            raise AssertionError(cls.admission.diagnostics)
        cls.profile = bazi_classical_effect_semantic_candidate_projection_r1_profile()
        cls.request = BaziClassicalEffectSemanticCandidateProjectionRequest(
            cls.effect, cls.admission, cls.profile
        )

    def test_stale_unit2_payload_fails_self_replay_and_unit4(self):
        outer = self.effect.candidates[0]
        fragment = outer.fragments[0]
        changed_fragment = replace(
            fragment,
            source_unresolved_graph_requirements=(
                *fragment.source_unresolved_graph_requirements,
                "TAMPERED_STALE_PAYLOAD",
            ),
        )
        changed_outer = replace(outer, fragments=(changed_fragment, *outer.fragments[1:]))
        self.assertFalse(replay_effect_envelope_self_contained(changed_outer))
        changed_effect = replace(
            self.effect,
            candidates=(changed_outer, *self.effect.candidates[1:]),
        )
        result = BaziClassicalEffectSemanticCandidateProjectionEngine().resolve_typed(
            replace(self.request, source_effect_constraint_resolution=changed_effect)
        )
        self.assertEqual("FAILED", result.status)
        self.assertTrue(any(
            "UPSTREAM_ADMISSION_ENVELOPE_REPLAY_MISMATCH" in diagnostic
            for diagnostic in result.diagnostics
        ))

    def test_stale_unit3_admission_payload_fails_hash_replay(self):
        outer = self.admission.candidates[0]
        row = outer.fragment_admissions[0]
        changed_row = replace(
            row,
            admission_status=(
                "PRESERVED_NOT_ADMITTED" if row.admission_status == "ADMITTED" else "ADMITTED"
            ),
        )
        changed_outer = replace(
            outer,
            fragment_admissions=(changed_row, *outer.fragment_admissions[1:]),
        )
        changed_admission = replace(
            self.admission,
            candidates=(changed_outer, *self.admission.candidates[1:]),
        )
        result = BaziClassicalEffectSemanticCandidateProjectionEngine().resolve_typed(
            replace(self.request, source_resolver_admission_resolution=changed_admission)
        )
        self.assertEqual("FAILED", result.status)
        self.assertTrue(any(
            "UPSTREAM_ADMISSION_ENVELOPE_REPLAY_MISMATCH" in diagnostic
            for diagnostic in result.diagnostics
        ))

    def test_duplicate_unit3_outer_lineage_fails_closed(self):
        duplicate = replace(
            self.admission,
            status="MULTI_CANDIDATE",
            candidates=(self.admission.candidates[0], self.admission.candidates[0]),
        )
        result = BaziClassicalEffectSemanticCandidateProjectionEngine().resolve_typed(
            replace(self.request, source_resolver_admission_resolution=duplicate)
        )
        self.assertEqual("FAILED", result.status)
        self.assertTrue(any(
            "UPSTREAM_ADMISSION_OUTER_LINEAGE_PROJECTED_MORE_THAN_ONCE" in diagnostic
            for diagnostic in result.diagnostics
        ))

    def test_claim_facet_mapping_drift_exposes_machine_code(self):
        effect_outer = self.effect.candidates[0]
        admission_outer = self.admission.candidates[0]
        fragment = effect_outer.fragments[0]
        admission_row = next(
            row for row in admission_outer.fragment_admissions
            if row.source_fragment_id == fragment.fragment_id
        )
        admitted = replace(admission_row, admission_status="ADMITTED", admission_blocker_ids=())
        node = fragment.effect_constraint_nodes[0]
        bad_constraint = replace(
            node.constraint,
            source_claim_edge_class="SOURCE_ASSERTED_ATTENUATION",
            source_assertion_class="ATTENUATION_ASSERTION",
            effect_facet="RELATION_EFFECT_DISPOSITION",
            multiplicity_references=(),
        )
        bad_fragment = replace(
            fragment,
            effect_constraint_nodes=(replace(node, constraint=bad_constraint),),
        )
        with self.assertRaises(BaziClassicalEffectSemanticCandidateProjectionError) as caught:
            project_fragment_semantic_candidates(
                admission_outer,
                admitted,
                bad_fragment,
                self.profile,
            )
        self.assertEqual(
            "UNIT2_CLAIM_FACET_MAPPING_MISMATCH",
            caught.exception.diagnostic_code,
        )

    def test_profile_releases_no_solver_semantics(self):
        for value in (
            self.profile.candidate_truth_semantics,
            self.profile.candidate_coexistence_semantics,
            self.profile.candidate_exclusivity_semantics,
            self.profile.candidate_priority_semantics,
            self.profile.candidate_conflict_semantics,
            self.profile.candidate_rewrite_semantics,
            self.profile.candidate_state_transition_semantics,
            self.profile.candidate_winner_loser_semantics,
            self.profile.cross_outer_composition,
            self.profile.cartesian_expansion,
        ):
            self.assertEqual("NOT_RELEASED", value)


if __name__ == "__main__":
    unittest.main()
