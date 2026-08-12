from __future__ import annotations

import unittest
from dataclasses import replace

from fortune_training.bazi_classical_effect_constraint_graph.models import (
    EffectConstraintMultiplicityReference,
)
from fortune_training.bazi_classical_effect_semantic_candidate import (
    project_fragment_semantic_candidates,
)
from fortune_training.bazi_classical_non_selecting_participant_allocation import (
    BaziClassicalNonSelectingParticipantAllocationEngine,
    allocation_hash_bundle,
    bazi_classical_non_selecting_participant_allocation_r1_profile,
    project_proposal_allocation_elaboration,
    replay_allocation_domain_observation,
)
from fortune_training.bazi_classical_non_selecting_participant_allocation.models import (
    FragmentAllocationElaborationProjection,
)
from fortune_training.bazi_classical_semantic_closure_governance import (
    project_fragment_governance,
)
from test_bazi_classical_non_selecting_participant_allocation_r1 import (
    BaziClassicalNonSelectingParticipantAllocationR1Tests as Unit6Stack,
)


class BaziClassicalNonSelectingParticipantAllocationIntegrityR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Unit6Stack.setUpClass()
        cls.effect, cls.admission, cls.semantic, cls.mechanism, cls.request, cls.result = (
            Unit6Stack.cross
        )
        cls.profile = bazi_classical_non_selecting_participant_allocation_r1_profile()

    def test_stale_unit5_payload_with_old_hashes_fails_closed(self):
        outer = self.mechanism.candidates[0]
        fragment = outer.fragment_governance_projections[0]
        changed_fragment = replace(
            fragment,
            source_unresolved_graph_requirements_provenance=(
                *fragment.source_unresolved_graph_requirements_provenance,
                "STALE_UNIT5_PAYLOAD_TAMPER",
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
            self.mechanism,
            candidates=(changed_outer, *self.mechanism.candidates[1:]),
        )
        result = BaziClassicalNonSelectingParticipantAllocationEngine().resolve_typed(
            replace(
                self.request,
                source_mechanism_closure_resolution=changed_mechanism,
            )
        )
        self.assertEqual("FAILED", result.status)
        self.assertTrue(any(
            "UPSTREAM_UNIT5_MECHANISM_CLOSURE_REPLAY_MISMATCH" in diagnostic
            for diagnostic in result.diagnostics
        ))

    def test_duplicate_unit5_outer_lineage_fails_closed(self):
        duplicate = replace(
            self.mechanism,
            status="MULTI_CANDIDATE",
            candidates=(self.mechanism.candidates[0], self.mechanism.candidates[0]),
        )
        result = BaziClassicalNonSelectingParticipantAllocationEngine().resolve_typed(
            replace(
                self.request,
                source_mechanism_closure_resolution=duplicate,
            )
        )
        self.assertEqual("FAILED", result.status)
        self.assertTrue(any(
            "UPSTREAM_UNIT5_OUTER_LINEAGE_PROJECTED_MORE_THAN_ONCE" in diagnostic
            for diagnostic in result.diagnostics
        ))

    def _controlled_allocation(self):
        effect, admission, semantic, _, _, _ = Unit6Stack.multiplicity
        for effect_outer, admission_outer, semantic_outer in zip(
            effect.candidates,
            admission.candidates,
            semantic.candidates,
            strict=True,
        ):
            for fragment in effect_outer.fragments:
                if fragment.source_occurrence_id != "ZPZQ-CL-09-005-002":
                    continue
                allocation_node = next(
                    (
                        node
                        for node in fragment.effect_constraint_nodes
                        if node.constraint.source_claim_edge_class
                        == "SOURCE_ASSERTED_PARTICIPANT_ALLOCATION"
                    ),
                    None,
                )
                if allocation_node is None:
                    continue
                admission_row = next(
                    row
                    for row in admission_outer.fragment_admissions
                    if row.source_fragment_id == fragment.fragment_id
                )
                admitted = replace(
                    admission_row,
                    admission_status="ADMITTED",
                    admission_blocker_ids=(),
                )
                local_fragment = replace(
                    fragment,
                    effect_constraint_nodes=(allocation_node,),
                )
                semantic_fragment = project_fragment_semantic_candidates(
                    admission_outer,
                    admitted,
                    local_fragment,
                    Unit6Stack.semantic_profile,
                )
                unit5_fragment = project_fragment_governance(
                    semantic_outer,
                    semantic_fragment,
                    Unit6Stack.unit5_profile,
                )
                candidate = semantic_fragment.semantic_candidates[0]
                proposal = unit5_fragment.mechanism_proposals[0]
                reference = EffectConstraintMultiplicityReference(
                    multiplicity_constraint_id="CONTROLLED-MATCH",
                    exchangeable_symbolic_slot_node_ids=("SLOT-A", "SLOT-B"),
                    exact_runtime_instance_ids=("R1", "R2"),
                    required_symbolic_cardinality=2,
                    slot_equivalence="EXCHANGEABLE_SOURCE_EQUIVALENT",
                    alternative_path_requirement="PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS",
                )
                controlled_candidate = replace(
                    candidate,
                    multiplicity_references=(reference,),
                )
                elaboration = project_proposal_allocation_elaboration(
                    unit5_fragment,
                    controlled_candidate,
                    proposal,
                    self.profile,
                )
                return semantic_outer, unit5_fragment, controlled_candidate, proposal, elaboration, reference
        raise AssertionError("controlled 005-002 allocation fixture not found")

    def test_recomputed_hash_does_not_hide_synthetic_extra_path(self):
        _, unit5_fragment, candidate, proposal, elaboration, reference = (
            self._controlled_allocation()
        )
        observation = elaboration.allocation_domain_observations[0]
        legal_path = observation.path_candidates[0]
        synthetic_path = replace(
            legal_path,
            path_candidate_id=f"{legal_path.path_candidate_id}:SYNTHETIC",
        )
        tampered_observation = replace(
            observation,
            path_candidates=(legal_path, synthetic_path),
        )
        tampered_elaboration = replace(
            elaboration,
            allocation_domain_observations=(tampered_observation,),
        )
        tampered_fragment = FragmentAllocationElaborationProjection(
            fragment_allocation_projection_id="CONTROLLED-TAMPERED-FRAGMENT",
            source_fragment_governance_projection_id=(
                unit5_fragment.fragment_governance_projection_id
            ),
            source_fragment_semantic_projection_id=(
                unit5_fragment.source_fragment_semantic_projection_id
            ),
            source_fragment_id=unit5_fragment.source_fragment_id,
            source_occurrence_id=unit5_fragment.source_occurrence_id,
            binding_candidate_id=unit5_fragment.binding_candidate_id,
            source_governance_status=unit5_fragment.governance_status,
            allocation_status="ALLOCATION_DOMAIN_ELABORATION_PROJECTED",
            source_mechanism_proposal_ids=(proposal.mechanism_proposal_id,),
            proposal_elaborations=(tampered_elaboration,),
            allocation_domain_observation_ids=(
                tampered_observation.allocation_domain_observation_id,
            ),
        )
        source_mechanism = self.mechanism.candidates[0]
        hashes = allocation_hash_bundle(
            source_mechanism,
            (tampered_fragment,),
            (),
            (),
            (tampered_observation.allocation_domain_observation_id,),
            (legal_path.path_candidate_id, synthetic_path.path_candidate_id),
            ("CONTROLLED-TAMPERED-LINEAGE",),
            self.profile,
        )
        self.assertTrue(hashes.fact_hash)
        self.assertFalse(
            replay_allocation_domain_observation(
                tampered_observation,
                candidate,
                proposal,
                reference,
                self.profile,
            )
        )

    def test_recomputed_hash_does_not_hide_changed_unit5_closure_status(self):
        _, unit5_fragment, candidate, proposal, elaboration, reference = (
            self._controlled_allocation()
        )
        observation = elaboration.allocation_domain_observations[0]
        first_row = observation.unit5_allocation_closure_rows[0]
        tampered_row = replace(
            first_row,
            runtime_dependency_status="AVAILABLE_EXACTLY",
        )
        tampered_observation = replace(
            observation,
            unit5_allocation_closure_rows=(
                tampered_row,
                *observation.unit5_allocation_closure_rows[1:],
            ),
        )
        tampered_elaboration = replace(
            elaboration,
            allocation_domain_observations=(tampered_observation,),
        )
        tampered_fragment = FragmentAllocationElaborationProjection(
            fragment_allocation_projection_id="CONTROLLED-CLOSURE-TAMPER",
            source_fragment_governance_projection_id=(
                unit5_fragment.fragment_governance_projection_id
            ),
            source_fragment_semantic_projection_id=(
                unit5_fragment.source_fragment_semantic_projection_id
            ),
            source_fragment_id=unit5_fragment.source_fragment_id,
            source_occurrence_id=unit5_fragment.source_occurrence_id,
            binding_candidate_id=unit5_fragment.binding_candidate_id,
            source_governance_status=unit5_fragment.governance_status,
            allocation_status="ALLOCATION_DOMAIN_ELABORATION_PROJECTED",
            source_mechanism_proposal_ids=(proposal.mechanism_proposal_id,),
            proposal_elaborations=(tampered_elaboration,),
            allocation_domain_observation_ids=(
                tampered_observation.allocation_domain_observation_id,
            ),
        )
        hashes = allocation_hash_bundle(
            self.mechanism.candidates[0],
            (tampered_fragment,),
            (),
            (),
            (tampered_observation.allocation_domain_observation_id,),
            tuple(
                path.path_candidate_id for path in tampered_observation.path_candidates
            ),
            ("CONTROLLED-CLOSURE-TAMPER-LINEAGE",),
            self.profile,
        )
        self.assertTrue(hashes.computation_hash)
        self.assertFalse(
            replay_allocation_domain_observation(
                tampered_observation,
                candidate,
                proposal,
                reference,
                self.profile,
            )
        )


if __name__ == "__main__":
    unittest.main()
