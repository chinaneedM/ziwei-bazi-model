from __future__ import annotations

import unittest
from dataclasses import replace

from fortune_training.bazi_classical_semantic_closure_governance import (
    bazi_classical_semantic_mechanism_closure_governance_r1_profile,
)
from fortune_training.bazi_classical_semantic_closure_governance.integrity import (
    mechanism_closure_hash_bundle,
    validate_mechanism_closure_envelope,
)
from test_bazi_classical_semantic_mechanism_closure_governance_r1 import (
    BaziClassicalSemanticMechanismClosureGovernanceR1Tests as Unit5Stack,
)


class BaziClassicalSemanticMechanismClosureAcceptanceR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Unit5Stack.setUpClass()
        cls.effect, cls.admission, cls.semantic, _, cls.result = Unit5Stack.cross
        cls.profile = bazi_classical_semantic_mechanism_closure_governance_r1_profile()

    def test_recomputed_envelope_hash_cannot_hide_proposal_semantic_tamper(self):
        source_semantic = self.semantic.candidates[0]
        admission = self.admission.candidates[0]
        effect = self.effect.candidates[0]
        envelope = self.result.candidates[0]

        fragment_index = next(
            index
            for index, fragment in enumerate(envelope.fragment_governance_projections)
            if fragment.mechanism_proposals
        )
        fragment = envelope.fragment_governance_projections[fragment_index]
        proposal = fragment.mechanism_proposals[0]
        tampered_proposal = replace(
            proposal,
            rewrite_application_semantics="RELEASED",
        )
        tampered_fragment = replace(
            fragment,
            mechanism_proposals=(
                tampered_proposal,
                *fragment.mechanism_proposals[1:],
            ),
        )
        fragments = list(envelope.fragment_governance_projections)
        fragments[fragment_index] = tampered_fragment
        tampered_fragments = tuple(fragments)

        tampered_hashes = mechanism_closure_hash_bundle(
            source_semantic,
            tampered_fragments,
            envelope.source_record_candidate_sets,
            envelope.closure_requirement_index,
            envelope.mechanism_proposal_index,
            envelope.projected_mechanism_proposal_ids,
            envelope.lineage_binding_keys,
            self.profile,
        )
        self.assertNotEqual(envelope.hashes, tampered_hashes)

        validation = validate_mechanism_closure_envelope(
            source_semantic,
            admission,
            effect,
            tampered_fragments,
            envelope.source_record_candidate_sets,
            envelope.closure_requirement_index,
            envelope.mechanism_proposal_index,
            envelope.projected_mechanism_proposal_ids,
            envelope.lineage_binding_keys,
            self.profile,
            tampered_hashes,
        )
        self.assertEqual("FAIL", validation.status)
        self.assertTrue(any(
            row.code == "MECHANISM_PROPOSAL_REPLAY_MISMATCH"
            for row in validation.diagnostics
        ))


if __name__ == "__main__":
    unittest.main()
