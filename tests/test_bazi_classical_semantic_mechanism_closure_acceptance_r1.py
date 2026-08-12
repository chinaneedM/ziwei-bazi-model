from __future__ import annotations

import unittest
from dataclasses import replace

from fortune_training.bazi_classical_semantic_closure_governance import (
    bazi_classical_semantic_mechanism_closure_governance_r1_profile,
    project_fragment_governance,
)
from fortune_training.bazi_classical_semantic_closure_governance.integrity import (
    mechanism_closure_hash_bundle,
    replay_mechanism_proposal,
)
from test_bazi_classical_semantic_mechanism_closure_governance_r1 import (
    BaziClassicalSemanticMechanismClosureGovernanceR1Tests as Unit5Stack,
)


class BaziClassicalSemanticMechanismClosureAcceptanceR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Unit5Stack.setUpClass()
        cls.profile = bazi_classical_semantic_mechanism_closure_governance_r1_profile()

    def test_recomputed_hash_does_not_replace_independent_proposal_semantic_replay(self):
        helper = Unit5Stack(
            methodName="test_real_stack_preserves_one_outer_and_every_fragment"
        )
        semantic_outer, fragment_projection, candidate, proposal = helper._controlled_candidate(
            "SOURCE_ASSERTED_RESOLUTION",
            "RESOLUTION_ASSERTION",
            "RELATION_EFFECT_DISPOSITION",
            ("CLASSICAL_RESOLUTION_SEMANTICS",),
        )
        self.assertTrue(
            replay_mechanism_proposal(
                semantic_outer,
                fragment_projection,
                candidate,
                proposal,
                self.profile,
            )
        )

        governance_fragment = project_fragment_governance(
            semantic_outer,
            fragment_projection,
            self.profile,
        )
        self.assertEqual(
            proposal.mechanism_proposal_id,
            governance_fragment.mechanism_proposals[0].mechanism_proposal_id,
        )
        original_hashes = mechanism_closure_hash_bundle(
            semantic_outer,
            (governance_fragment,),
            (),
            (),
            (),
            (proposal.mechanism_proposal_id,),
            ("CONTROLLED_ACCEPTANCE_LINEAGE",),
            self.profile,
        )

        tampered_proposal = replace(
            proposal,
            rewrite_application_semantics="RELEASED",
        )
        tampered_fragment = replace(
            governance_fragment,
            mechanism_proposals=(tampered_proposal,),
        )
        tampered_hashes = mechanism_closure_hash_bundle(
            semantic_outer,
            (tampered_fragment,),
            (),
            (),
            (),
            (tampered_proposal.mechanism_proposal_id,),
            ("CONTROLLED_ACCEPTANCE_LINEAGE",),
            self.profile,
        )
        self.assertNotEqual(original_hashes, tampered_hashes)
        self.assertFalse(
            replay_mechanism_proposal(
                semantic_outer,
                fragment_projection,
                candidate,
                tampered_proposal,
                self.profile,
            )
        )


if __name__ == "__main__":
    unittest.main()
