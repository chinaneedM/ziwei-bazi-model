from __future__ import annotations

import unittest
from dataclasses import replace

from fortune_training.bazi_classical_resolver_admission import (
    BaziClassicalResolverAdmissionEngine,
    BaziClassicalResolverAdmissionRequest,
    bazi_classical_resolver_admission_strict_r1_profile,
    project_fragment_admission,
    shen_zpzq_ch09_classical_interaction_r1_profile,
)
from test_bazi_classical_effect_constraint_graph_factorized_composition_r1 import (
    BaziClassicalEffectConstraintGraphFactorizedCompositionR1Tests as Unit2Stack,
)


class BaziClassicalResolverAdmissionIntegrityR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Unit2Stack.setUpClass()
        cls.binding, cls.projection, _, cls.effect = Unit2Stack.cross_layer
        cls.source_profile = shen_zpzq_ch09_classical_interaction_r1_profile()
        cls.admission_profile = bazi_classical_resolver_admission_strict_r1_profile()
        cls.request = BaziClassicalResolverAdmissionRequest(
            cls.binding, cls.projection, cls.effect, cls.source_profile, cls.admission_profile
        )

    def _003_pair(self):
        effect_envelope = self.effect.candidates[0]
        projection_outer = self.projection.candidates[0]
        fragment = next(row for row in effect_envelope.fragments if row.source_occurrence_id == "ZPZQ-CL-09-003-002")
        bundle = next(row for row in projection_outer.bundles if row.binding_candidate_id == fragment.binding_candidate_id)
        return effect_envelope, fragment, bundle

    def test_missing_declared_dependency_preserves_fragment_but_blocks_admission(self):
        effect_envelope, fragment, bundle = self._003_pair()
        neutral = bundle.neutral_observation_bundle
        primitive_to_attribute = {
            "EXACT_RAW_RELATION_OCCURRENCE_IDENTITY": "relation_identity_observations",
            "EXACT_PARTICIPANT_INSTANCE_IDENTITY": "participant_identity_observations",
            "RELATION_INCIDENCE_DEGREE": "participant_incidence_observations",
            "RELATION_PAIR_TOPOLOGY": "relation_pair_topology_observations",
            "EXACT_TEMPORAL_LAYER_FRAME": "temporal_layer_frame_observations",
        }
        empty = next(
            primitive for primitive, attribute in primitive_to_attribute.items()
            if primitive not in neutral.required_neutral_primitives and not getattr(neutral, attribute)
        )
        local_bundle = replace(
            bundle,
            neutral_observation_bundle=replace(neutral, required_neutral_primitives=(*neutral.required_neutral_primitives, empty)),
            structural_binding_class="FULL_EXACT_BINDING_ENUMERATION",
            source_scope_compatibility=replace(bundle.source_scope_compatibility, source_scope_compatibility="DIRECT_SOURCE_SCOPE_MATCH"),
            residual_unresolved_structural_constraint_ids=(),
        )
        local_fragment = replace(
            fragment,
            structural_binding_class="FULL_EXACT_BINDING_ENUMERATION",
            source_scope_compatibility="DIRECT_SOURCE_SCOPE_MATCH",
            residual_unresolved_structural_constraint_ids=(),
        )
        row = project_fragment_admission(effect_envelope, local_fragment, local_bundle, self.source_profile, self.admission_profile)
        self.assertEqual("PRESERVED_NOT_ADMITTED", row.admission_status)
        self.assertIn(f"MATERIALIZED_DEPENDENCY_MISSING:{empty}", row.admission_blocker_ids)
        self.assertEqual(fragment.fragment_id, row.source_fragment_id)

    def test_partition_mismatch_is_preserved_outside_profile(self):
        effect_envelope, fragment, bundle = self._003_pair()
        row = project_fragment_admission(
            effect_envelope,
            replace(fragment, source_occurrence_id="QTBJ-CL-05347"),
            replace(bundle, source_occurrence_id="QTBJ-CL-05347"),
            self.source_profile,
            self.admission_profile,
        )
        self.assertEqual("PRESERVED_OUTSIDE_PROFILE", row.admission_status)
        self.assertFalse(row.partition_match)
        self.assertEqual(("SOURCE_SEMANTIC_PARTITION_MISMATCH",), row.admission_blocker_ids)

    def test_projection_dependency_payload_change_with_stale_hash_fails_closed(self):
        outer = self.projection.candidates[0]
        bundle = outer.bundles[0]
        changed = replace(bundle, neutral_observation_bundle=replace(bundle.neutral_observation_bundle, required_neutral_primitives=()))
        changed_outer = replace(outer, bundles=(changed, *outer.bundles[1:]))
        request = replace(
            self.request,
            source_projection_resolution=replace(self.projection, candidates=(changed_outer, *self.projection.candidates[1:])),
        )
        result = BaziClassicalResolverAdmissionEngine().resolve_typed(request)
        self.assertEqual("FAILED", result.status)
        self.assertTrue(any("UPSTREAM_EFFECT_ENVELOPE_REPLAY_MISMATCH" in row for row in result.diagnostics))

    def test_duplicate_effect_outer_lineage_fails_closed(self):
        duplicate = replace(
            self.effect,
            status="MULTI_CANDIDATE",
            candidates=(self.effect.candidates[0], self.effect.candidates[0]),
        )
        result = BaziClassicalResolverAdmissionEngine().resolve_typed(
            replace(self.request, source_effect_constraint_resolution=duplicate)
        )
        self.assertEqual("FAILED", result.status)
        self.assertTrue(any("UPSTREAM_EFFECT_OUTER_LINEAGE_PROJECTED_MORE_THAN_ONCE" in row for row in result.diagnostics))

    def test_admission_profile_does_not_release_lifecycle_or_cartesian_solving(self):
        self.assertEqual("PARALLEL_NOT_GLOBAL_ADMISSION_GATE", self.admission_profile.lifecycle_dependency_policy)
        self.assertEqual("NOT_RELEASED", self.admission_profile.cartesian_expansion_policy)
        self.assertEqual("NOT_RELEASED", self.admission_profile.cross_source_composition_policy)
        self.assertEqual("PROVENANCE_ONLY_NEVER_DIRECT_PREDICATE", self.admission_profile.source_unresolved_graph_requirement_policy)


if __name__ == "__main__":
    unittest.main()
