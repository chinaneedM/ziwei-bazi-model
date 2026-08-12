from __future__ import annotations

import copy
import json
import unittest
from dataclasses import replace
from pathlib import Path

from jsonschema import Draft202012Validator

from fortune_training.bazi_classical_effect_constraint_graph.models import (
    EffectConstraintMultiplicityReference,
)
from fortune_training.bazi_classical_effect_semantic_candidate import (
    bazi_classical_effect_semantic_candidate_projection_r1_profile,
    project_fragment_semantic_candidates,
)
from fortune_training.bazi_classical_non_selecting_participant_allocation import (
    AllocationMultiplicityContractError,
    BaziClassicalNonSelectingParticipantAllocationEngine,
    BaziClassicalNonSelectingParticipantAllocationRequest,
    bazi_classical_non_selecting_participant_allocation_r1_profile,
    build_unordered_path_candidate,
    classify_allocation_domain,
    project_proposal_allocation_elaboration,
    validate_multiplicity_reference,
    validate_release_contract,
)
from fortune_training.bazi_classical_semantic_closure_governance import (
    bazi_classical_semantic_mechanism_closure_governance_r1_profile,
    project_fragment_governance,
)
from fortune_training.calendar_foundation.models import json_value
from test_bazi_classical_semantic_mechanism_closure_governance_r1 import (
    BaziClassicalSemanticMechanismClosureGovernanceR1Tests as Unit5Stack,
)

ROOT = Path(__file__).resolve().parents[1]


class BaziClassicalNonSelectingParticipantAllocationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Unit5Stack.setUpClass()
        cls.profile = bazi_classical_non_selecting_participant_allocation_r1_profile()
        cls.semantic_profile = bazi_classical_effect_semantic_candidate_projection_r1_profile()
        cls.unit5_profile = bazi_classical_semantic_mechanism_closure_governance_r1_profile()
        cls.cross = cls._unit6(Unit5Stack.cross)
        cls.multiplicity = cls._unit6(Unit5Stack.multiplicity)

    @classmethod
    def _unit6(cls, stack):
        effect, admission, semantic, _, mechanism = stack
        request = BaziClassicalNonSelectingParticipantAllocationRequest(
            effect,
            admission,
            semantic,
            mechanism,
            cls.profile,
        )
        result = BaziClassicalNonSelectingParticipantAllocationEngine().resolve_typed(
            request
        )
        if result.status == "FAILED":
            raise AssertionError(result.diagnostics)
        return effect, admission, semantic, mechanism, request, result

    @staticmethod
    def _reference(runtime_ids: tuple[str, ...]) -> EffectConstraintMultiplicityReference:
        return EffectConstraintMultiplicityReference(
            multiplicity_constraint_id="CONTROLLED-MULTIPLICITY",
            exchangeable_symbolic_slot_node_ids=("SLOT-A", "SLOT-B"),
            exact_runtime_instance_ids=runtime_ids,
            required_symbolic_cardinality=2,
            slot_equivalence="EXCHANGEABLE_SOURCE_EQUIVALENT",
            alternative_path_requirement="PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS",
        )

    def test_release_contract_is_exact_and_closed(self):
        report = validate_release_contract(ROOT)
        self.assertEqual("PASS", report["status"])
        self.assertEqual(3, report["allocation_domain_classification_count"])
        self.assertEqual(
            "dd85bf571a5cf106321bfb0366ffeee5023563dfe099664fdecaefc3cbe15fea",
            report["contract_semantics_sha256"],
        )
        contract = json.loads((ROOT / "audits/bazi-classical-non-selecting-participant-allocation-r1/contract.json").read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas/bazi-classical-non-selecting-participant-allocation-r1.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        validator.validate(contract)
        changed = copy.deepcopy(contract)
        changed["classification_contract"]["EXACT_INSTANCE_POOL_REQUIRES_COMPATIBILITY_RELATION"]["path_candidate_cardinality"] = 3
        self.assertTrue(list(validator.iter_errors(changed)))
        changed = copy.deepcopy(contract)
        changed["preservation_contract"]["participant_path_selection"] = "RELEASED"
        self.assertTrue(list(validator.iter_errors(changed)))

    def test_cardinality_match_emits_only_one_unordered_identity_candidate(self):
        reference = self._reference(("R1", "R2"))
        classification, blockers = classify_allocation_domain(reference)
        self.assertEqual("EXACT_INSTANCE_SET_CARDINALITY_MATCH", classification)
        self.assertEqual((), blockers)
        candidate = build_unordered_path_candidate(
            "SEMANTIC-CANDIDATE",
            "MECHANISM-PROPOSAL",
            reference,
            self.profile,
        )
        self.assertEqual(
            "UNORDERED_EXACT_INSTANCE_SET_PATH_CANDIDATE",
            candidate.path_candidate_kind,
        )
        self.assertEqual(("R1", "R2"), candidate.exact_runtime_instance_ids)
        self.assertEqual("NOT_RELEASED", candidate.slot_assignment_semantics)
        self.assertEqual("NOT_RELEASED", candidate.path_ordering_semantics)
        self.assertEqual("NOT_RELEASED", candidate.selection_semantics)
        self.assertFalse(hasattr(candidate, "slot_assignment"))
        self.assertFalse(hasattr(candidate, "selected_path"))

    def test_larger_instance_pool_emits_compatibility_and_synthesis_blockers(self):
        reference = self._reference(("R1", "R2", "R3"))
        classification, blockers = classify_allocation_domain(reference)
        self.assertEqual(
            "EXACT_INSTANCE_POOL_REQUIRES_COMPATIBILITY_RELATION",
            classification,
        )
        self.assertEqual(
            (
                "SLOT_INSTANCE_COMPATIBILITY_RELATION_NOT_RELEASED",
                "SYNTHETIC_COMBINATORIAL_ENUMERATION_FORBIDDEN",
            ),
            blockers,
        )
        with self.assertRaises(AllocationMultiplicityContractError):
            build_unordered_path_candidate(
                "SEMANTIC-CANDIDATE",
                "MECHANISM-PROPOSAL",
                reference,
                self.profile,
            )

    def test_insufficient_instance_count_emits_only_cardinality_blocker(self):
        reference = self._reference(("R1",))
        classification, blockers = classify_allocation_domain(reference)
        self.assertEqual("INSUFFICIENT_EXACT_INSTANCE_CARDINALITY", classification)
        self.assertEqual(
            ("INSUFFICIENT_EXACT_RUNTIME_INSTANCE_CARDINALITY",),
            blockers,
        )

    def test_multiplicity_contract_rejects_duplicates_and_drift(self):
        invalid = [
            replace(
                self._reference(("R1", "R2")),
                exchangeable_symbolic_slot_node_ids=("SLOT-A", "SLOT-A"),
            ),
            replace(
                self._reference(("R1", "R2")),
                exact_runtime_instance_ids=("R1", "R1"),
            ),
            replace(
                self._reference(("R1", "R2")),
                required_symbolic_cardinality=3,
            ),
            replace(
                self._reference(("R1", "R2")),
                slot_equivalence="INVENTED_EQUIVALENCE",
            ),
            replace(
                self._reference(("R1", "R2")),
                alternative_path_requirement="GENERATE_ALL_PERMUTATIONS",
            ),
        ]
        for reference in invalid:
            with self.assertRaises(AllocationMultiplicityContractError):
                validate_multiplicity_reference(reference)

    def test_real_stack_preserves_one_outer_and_every_fragment(self):
        for _, _, _, mechanism, _, result in (self.cross, self.multiplicity):
            self.assertEqual(len(mechanism.candidates), len(result.candidates))
            for source, projected in zip(
                mechanism.candidates,
                result.candidates,
                strict=True,
            ):
                self.assertEqual(
                    source.mechanism_closure_envelope_id,
                    projected.source_mechanism_closure_envelope_id,
                )
                self.assertEqual(
                    [row.fragment_governance_projection_id for row in source.fragment_governance_projections],
                    [row.source_fragment_governance_projection_id for row in projected.fragment_allocation_projections],
                )
                self.assertEqual("FORBIDDEN", projected.synthetic_permutation_generation)
                self.assertEqual("FORBIDDEN", projected.synthetic_combination_generation)
                self.assertEqual("FORBIDDEN", projected.inferred_slot_instance_compatibility)
                self.assertEqual("NOT_RELEASED", projected.participant_path_selection_semantics)
                self.assertEqual("NOT_RELEASED", projected.precedence_semantics)
                self.assertEqual("NOT_RELEASED", projected.winner_loser_semantics)

    def test_controlled_005_allocation_preserves_unit5_closure_rows(self):
        effect, admission, semantic, _, _, _ = self.multiplicity
        found = False
        for effect_outer, admission_outer, semantic_outer in zip(
            effect.candidates,
            admission.candidates,
            semantic.candidates,
            strict=True,
        ):
            for fragment in effect_outer.fragments:
                if fragment.source_occurrence_id != "ZPZQ-CL-09-005-002":
                    continue
                allocation_nodes = [
                    node
                    for node in fragment.effect_constraint_nodes
                    if node.constraint.source_claim_edge_class
                    == "SOURCE_ASSERTED_PARTICIPANT_ALLOCATION"
                ]
                if not allocation_nodes:
                    continue
                found = True
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
                    effect_constraint_nodes=(allocation_nodes[0],),
                )
                semantic_fragment = project_fragment_semantic_candidates(
                    admission_outer,
                    admitted,
                    local_fragment,
                    self.semantic_profile,
                )
                unit5_fragment = project_fragment_governance(
                    semantic_outer,
                    semantic_fragment,
                    self.unit5_profile,
                )
                candidate = semantic_fragment.semantic_candidates[0]
                proposal = unit5_fragment.mechanism_proposals[0]
                elaboration = project_proposal_allocation_elaboration(
                    unit5_fragment,
                    candidate,
                    proposal,
                    self.profile,
                )
                self.assertEqual(
                    len(candidate.multiplicity_references),
                    len(elaboration.allocation_domain_observations),
                )
                for observation in elaboration.allocation_domain_observations:
                    self.assertEqual(
                        proposal.closure_governance_rows,
                        observation.unit5_allocation_closure_rows,
                    )
                    statuses = {
                        row.closure_requirement_id: row.runtime_dependency_status
                        for row in observation.unit5_allocation_closure_rows
                    }
                    self.assertEqual(
                        "MISSING_PRIMITIVE",
                        statuses["CLASSICAL_PARTICIPANT_ALLOCATION"],
                    )
                    self.assertEqual(
                        "PARTIALLY_AVAILABLE",
                        statuses["COMPATIBLE_EXACT_INSTANCE_PATH_ENUMERATION"],
                    )
                    self.assertLessEqual(len(observation.path_candidates), 1)
                    self.assertFalse(hasattr(observation, "selected_path"))
                    self.assertFalse(hasattr(observation, "slot_assignment"))
        self.assertTrue(found)

    def test_runtime_schema_rejects_selection_and_solver_surface(self):
        _, _, _, _, request, _ = self.cross
        payload = BaziClassicalNonSelectingParticipantAllocationEngine().resolve(request)
        schema = json.loads((ROOT / "schemas/bazi-classical-non-selecting-participant-allocation-runtime-r1.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        validator.validate(payload)
        forbidden = [
            "selected_participant_id", "selected_path", "slot_assignment", "path_order",
            "compatible", "truth", "operative", "winner", "priority", "precedence",
            "relation_state", "effect_state", "rewrite_result", "final_classical_verdict",
        ]
        for field in forbidden:
            changed = copy.deepcopy(payload)
            changed["candidates"][0][field] = True
            self.assertTrue(list(validator.iter_errors(changed)), field)

        legal_path = json_value(
            build_unordered_path_candidate(
                "SEMANTIC-CANDIDATE",
                "MECHANISM-PROPOSAL",
                self._reference(("R1", "R2")),
                self.profile,
            )
        )
        path_validator = Draft202012Validator(schema["$defs"]["pathCandidate"])
        path_validator.validate(legal_path)
        for field in ("slot_assignment", "path_order", "selected_path", "compatible"):
            changed = copy.deepcopy(legal_path)
            changed[field] = True
            self.assertTrue(list(path_validator.iter_errors(changed)), field)


if __name__ == "__main__":
    unittest.main()
