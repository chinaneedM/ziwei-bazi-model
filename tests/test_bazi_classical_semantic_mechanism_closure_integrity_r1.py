from __future__ import annotations

import unittest
from dataclasses import replace

from fortune_training.bazi_classical_effect_semantic_candidate import (
    bazi_classical_effect_semantic_candidate_projection_r1_profile,
    project_fragment_semantic_candidates,
)
from fortune_training.bazi_classical_semantic_closure_governance import (
    BaziClassicalSemanticMechanismClosureGovernanceEngine,
    BaziClassicalSemanticMechanismClosureGovernanceError,
    bazi_classical_semantic_mechanism_closure_governance_r1_profile,
    project_fragment_governance,
    project_mechanism_proposal,
)
from test_bazi_classical_semantic_mechanism_closure_governance_r1 import (
    BaziClassicalSemanticMechanismClosureGovernanceR1Tests as Unit5Stack,
)


class BaziClassicalSemanticMechanismClosureIntegrityR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Unit5Stack.setUpClass()
        cls.effect, cls.admission, cls.semantic, cls.request, cls.result = Unit5Stack.cross
        cls.semantic_profile = bazi_classical_effect_semantic_candidate_projection_r1_profile()
        cls.closure_profile = bazi_classical_semantic_mechanism_closure_governance_r1_profile()

    def _controlled_candidate(
        self,
        *,
        claim_class: str,
        assertion_class: str,
        facet: str,
        requirements: tuple[str, ...],
        narrative_ids: tuple[str, ...] = (),
    ):
        effect_outer = self.effect.candidates[0]
        admission_outer = self.admission.candidates[0]
        semantic_outer = self.semantic.candidates[0]
        fragment = effect_outer.fragments[0]
        admission_row = next(
            row for row in admission_outer.fragment_admissions
            if row.source_fragment_id == fragment.fragment_id
        )
        admitted = replace(
            admission_row,
            admission_status="ADMITTED",
            admission_blocker_ids=(),
        )
        node = fragment.effect_constraint_nodes[0]
        constraint = replace(
            node.constraint,
            source_claim_edge_class=claim_class,
            source_assertion_class=assertion_class,
            effect_facet=facet,
            unresolved_classical_semantic_requirements=requirements,
            source_narrative_chain_ids=narrative_ids,
            multiplicity_references=(),
        )
        local_fragment = replace(
            fragment,
            effect_constraint_nodes=(replace(node, constraint=constraint),),
        )
        fragment_projection = project_fragment_semantic_candidates(
            admission_outer,
            admitted,
            local_fragment,
            self.semantic_profile,
        )
        return semantic_outer, fragment_projection, fragment_projection.semantic_candidates[0]

    def test_stale_unit4_payload_with_old_hashes_fails_closed(self):
        outer = self.semantic.candidates[0]
        fragment = outer.fragment_projections[0]
        changed_fragment = replace(
            fragment,
            source_unresolved_graph_requirements_provenance=(
                *fragment.source_unresolved_graph_requirements_provenance,
                "STALE_UNIT4_PAYLOAD_TAMPER",
            ),
        )
        changed_outer = replace(
            outer,
            fragment_projections=(changed_fragment, *outer.fragment_projections[1:]),
        )
        changed_semantic = replace(
            self.semantic,
            candidates=(changed_outer, *self.semantic.candidates[1:]),
        )
        result = BaziClassicalSemanticMechanismClosureGovernanceEngine().resolve_typed(
            replace(
                self.request,
                source_semantic_candidate_resolution=changed_semantic,
            )
        )
        self.assertEqual("FAILED", result.status)
        self.assertTrue(any(
            "UPSTREAM_UNIT4_SEMANTIC_ENVELOPE_REPLAY_MISMATCH" in diagnostic
            for diagnostic in result.diagnostics
        ))

    def test_duplicate_unit4_outer_lineage_fails_closed(self):
        duplicate = replace(
            self.semantic,
            status="MULTI_CANDIDATE",
            candidates=(self.semantic.candidates[0], self.semantic.candidates[0]),
        )
        result = BaziClassicalSemanticMechanismClosureGovernanceEngine().resolve_typed(
            replace(
                self.request,
                source_semantic_candidate_resolution=duplicate,
            )
        )
        self.assertEqual("FAILED", result.status)
        self.assertTrue(any(
            "UPSTREAM_UNIT4_OUTER_LINEAGE_PROJECTED_MORE_THAN_ONCE" in diagnostic
            for diagnostic in result.diagnostics
        ))

    def test_unknown_closure_requirement_fails_closed(self):
        semantic_outer, fragment_projection, candidate = self._controlled_candidate(
            claim_class="SOURCE_ASSERTED_RESOLUTION",
            assertion_class="RESOLUTION_ASSERTION",
            facet="RELATION_EFFECT_DISPOSITION",
            requirements=("UNKNOWN_UNIT5_REQUIREMENT",),
        )
        with self.assertRaises(BaziClassicalSemanticMechanismClosureGovernanceError) as caught:
            project_mechanism_proposal(
                semantic_outer,
                fragment_projection,
                candidate,
                self.closure_profile,
            )
        self.assertEqual(
            "UNKNOWN_UNIT5_CLOSURE_REQUIREMENT",
            caught.exception.diagnostic_code,
        )

    def test_empty_closure_requirement_set_fails_closed(self):
        semantic_outer, fragment_projection, candidate = self._controlled_candidate(
            claim_class="SOURCE_ASSERTED_RESOLUTION",
            assertion_class="RESOLUTION_ASSERTION",
            facet="RELATION_EFFECT_DISPOSITION",
            requirements=(),
        )
        with self.assertRaises(BaziClassicalSemanticMechanismClosureGovernanceError) as caught:
            project_mechanism_proposal(
                semantic_outer,
                fragment_projection,
                candidate,
                self.closure_profile,
            )
        self.assertEqual(
            "SEMANTIC_CANDIDATE_WITHOUT_DECLARED_CLOSURE_REQUIREMENT",
            caught.exception.diagnostic_code,
        )

    def test_narrative_chain_is_provenance_only_not_transition(self):
        semantic_outer, fragment_projection, candidate = self._controlled_candidate(
            claim_class="SOURCE_ASSERTED_RESOLUTION_FAILURE",
            assertion_class="RESOLUTION_FAILURE_ASSERTION",
            facet="RELATION_EFFECT_DISPOSITION",
            requirements=(
                "CLASSICAL_RESOLUTION_FAILURE_SEMANTICS",
                "CLASSICAL_INTERACTION_CHAIN_RESOLUTION",
            ),
            narrative_ids=("CONTROLLED_NARRATIVE_CHAIN",),
        )
        proposal = project_mechanism_proposal(
            semantic_outer,
            fragment_projection,
            candidate,
            self.closure_profile,
        )
        chain_row = next(
            row for row in proposal.closure_governance_rows
            if row.closure_requirement_id == "CLASSICAL_INTERACTION_CHAIN_RESOLUTION"
        )
        self.assertEqual("MISSING_PRIMITIVE", chain_row.runtime_dependency_status)
        self.assertEqual(
            "SOURCE_NARRATIVE_CHAIN_IDENTITY_PROVENANCE_ONLY",
            chain_row.upstream_support_class,
        )
        self.assertEqual(
            ("CONTROLLED_NARRATIVE_CHAIN",),
            chain_row.upstream_support_reference_ids,
        )
        self.assertFalse(hasattr(proposal, "transition_edge"))
        self.assertFalse(hasattr(proposal, "rewrite_edge"))
        self.assertFalse(hasattr(proposal, "rewrite_result"))
        self.assertFalse(hasattr(proposal, "relation_state"))

    def test_real_zero_candidate_fragment_remains_zero_proposals(self):
        source_outer = self.semantic.candidates[0]
        source_fragment = next(
            row for row in source_outer.fragment_projections
            if not row.semantic_candidates
        )
        projected = project_fragment_governance(
            source_outer,
            source_fragment,
            self.closure_profile,
        )
        self.assertEqual((), projected.mechanism_proposals)
        self.assertEqual((), projected.source_semantic_candidate_ids)
        if source_fragment.projection_status == "PRESERVED_NO_SEMANTIC_CANDIDATES":
            self.assertEqual(
                "PRESERVED_ZERO_MECHANISM_PROPOSALS",
                projected.governance_status,
            )
        else:
            self.assertEqual(
                "PRESERVED_OUTSIDE_PROFILE_ZERO_MECHANISM_PROPOSALS",
                projected.governance_status,
            )


if __name__ == "__main__":
    unittest.main()
