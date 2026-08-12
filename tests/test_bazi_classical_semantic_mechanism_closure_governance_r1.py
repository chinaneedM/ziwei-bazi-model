from __future__ import annotations

import copy
import json
import unittest
from dataclasses import replace
from pathlib import Path

from jsonschema import Draft202012Validator

from fortune_training.bazi_classical_effect_semantic_candidate import (
    BaziClassicalEffectSemanticCandidateProjectionEngine,
    BaziClassicalEffectSemanticCandidateProjectionRequest,
    bazi_classical_effect_semantic_candidate_projection_r1_profile,
    project_fragment_semantic_candidates,
)
from fortune_training.bazi_classical_resolver_admission import (
    BaziClassicalResolverAdmissionEngine,
    BaziClassicalResolverAdmissionRequest,
    bazi_classical_resolver_admission_strict_r1_profile,
    shen_zpzq_ch09_classical_interaction_r1_profile,
)
from fortune_training.bazi_classical_semantic_closure_governance import (
    BaziClassicalSemanticMechanismClosureGovernanceEngine,
    BaziClassicalSemanticMechanismClosureGovernanceRequest,
    RUNTIME_DEPENDENCY_STATUSES,
    bazi_classical_semantic_mechanism_closure_governance_r1_profile,
    project_mechanism_proposal,
    validate_release_contract,
)
from fortune_training.classical_relation_evidence import RUNTIME_STATUSES
from test_bazi_classical_effect_constraint_graph_factorized_composition_r1 import (
    BaziClassicalEffectConstraintGraphFactorizedCompositionR1Tests as Unit2Stack,
)

ROOT = Path(__file__).resolve().parents[1]


class BaziClassicalSemanticMechanismClosureGovernanceR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Unit2Stack.setUpClass()
        cls.source_profile = shen_zpzq_ch09_classical_interaction_r1_profile()
        cls.admission_profile = bazi_classical_resolver_admission_strict_r1_profile()
        cls.semantic_profile = bazi_classical_effect_semantic_candidate_projection_r1_profile()
        cls.closure_profile = bazi_classical_semantic_mechanism_closure_governance_r1_profile()
        cls.cross = cls._stack(Unit2Stack.cross_layer)
        cls.multiplicity = cls._stack(Unit2Stack.multiplicity)

    @classmethod
    def _stack(cls, stack):
        binding, projection, _, effect = stack
        admission = BaziClassicalResolverAdmissionEngine().resolve_typed(
            BaziClassicalResolverAdmissionRequest(
                binding, projection, effect, cls.source_profile, cls.admission_profile
            )
        )
        if admission.status == "FAILED":
            raise AssertionError(admission.diagnostics)
        semantic = BaziClassicalEffectSemanticCandidateProjectionEngine().resolve_typed(
            BaziClassicalEffectSemanticCandidateProjectionRequest(
                effect, admission, cls.semantic_profile
            )
        )
        if semantic.status == "FAILED":
            raise AssertionError(semantic.diagnostics)
        request = BaziClassicalSemanticMechanismClosureGovernanceRequest(
            effect, admission, semantic, cls.closure_profile
        )
        result = BaziClassicalSemanticMechanismClosureGovernanceEngine().resolve_typed(request)
        if result.status == "FAILED":
            raise AssertionError(result.diagnostics)
        return effect, admission, semantic, request, result

    def test_release_contract_binds_unit4_and_229_status_vocabulary(self):
        report = validate_release_contract(ROOT)
        self.assertEqual("PASS", report["status"])
        self.assertEqual(5, report["mechanism_proposal_kind_count"])
        self.assertEqual(7, report["closure_requirement_count"])
        self.assertEqual(
            "358fcf00ef1c09321639c0df80e837fc2fd3dba0332cb82aea573b0a13ced998",
            report["contract_semantics_sha256"],
        )
        self.assertEqual(tuple(RUNTIME_STATUSES), RUNTIME_DEPENDENCY_STATUSES)
        contract = json.loads((ROOT / "audits/bazi-classical-semantic-mechanism-closure-governance-r1/contract.json").read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas/bazi-classical-semantic-mechanism-closure-governance-r1.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        validator.validate(contract)
        changed = copy.deepcopy(contract)
        changed["proposal_preservation_contract"]["precedence"] = "RELEASED"
        self.assertTrue(list(validator.iter_errors(changed)))
        changed = copy.deepcopy(contract)
        changed["closed_vocabularies"]["closure_requirement_registry"]["CLASSICAL_ATTENUATION_GRADE"]["runtime_dependency_status"] = "AVAILABLE_EXACTLY"
        self.assertTrue(list(validator.iter_errors(changed)))

    def test_real_stack_preserves_one_outer_and_every_fragment(self):
        for _, _, semantic, _, result in (self.cross, self.multiplicity):
            self.assertEqual(len(semantic.candidates), len(result.candidates))
            for source, projected in zip(semantic.candidates, result.candidates, strict=True):
                self.assertEqual(source.semantic_projection_envelope_id, projected.source_semantic_projection_envelope_id)
                self.assertEqual(
                    [row.fragment_semantic_projection_id for row in source.fragment_projections],
                    [row.source_fragment_semantic_projection_id for row in projected.fragment_governance_projections],
                )
                self.assertEqual("NOT_RELEASED", projected.mechanism_execution_semantics)
                self.assertEqual("NOT_RELEASED", projected.rewrite_application_semantics)
                self.assertEqual("NOT_RELEASED", projected.precedence_semantics)
                self.assertEqual("NOT_RELEASED", projected.winner_loser_semantics)
                self.assertEqual("NOT_RELEASED", projected.state_transition_semantics)
                self.assertEqual("NOT_RELEASED", projected.lifecycle_truth_gate)

    def _controlled_candidate(self, claim_class, assertion_class, facet, requirements):
        effect, admission, semantic, _, _ = self.cross
        effect_outer = effect.candidates[0]
        admission_outer = admission.candidates[0]
        semantic_outer = semantic.candidates[0]
        fragment = effect_outer.fragments[0]
        admission_row = next(
            row for row in admission_outer.fragment_admissions
            if row.source_fragment_id == fragment.fragment_id
        )
        admitted = replace(admission_row, admission_status="ADMITTED", admission_blocker_ids=())
        node = fragment.effect_constraint_nodes[0]
        constraint = replace(
            node.constraint,
            source_claim_edge_class=claim_class,
            source_assertion_class=assertion_class,
            effect_facet=facet,
            unresolved_classical_semantic_requirements=tuple(requirements),
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
        candidate = fragment_projection.semantic_candidates[0]
        proposal = project_mechanism_proposal(
            semantic_outer,
            fragment_projection,
            candidate,
            self.closure_profile,
        )
        return candidate, proposal

    def test_resolution_failure_reversal_and_attenuation_closure_rows(self):
        cases = [
            (
                "SOURCE_ASSERTED_RESOLUTION",
                "RESOLUTION_ASSERTION",
                "RELATION_EFFECT_DISPOSITION",
                ("CLASSICAL_RESOLUTION_SEMANTICS",),
                "RESOLUTION_MECHANISM_PROPOSAL",
                ("MISSING_PRIMITIVE",),
            ),
            (
                "SOURCE_ASSERTED_RESOLUTION_FAILURE",
                "RESOLUTION_FAILURE_ASSERTION",
                "RELATION_EFFECT_DISPOSITION",
                ("CLASSICAL_RESOLUTION_FAILURE_SEMANTICS", "CLASSICAL_INTERACTION_CHAIN_RESOLUTION"),
                "RESOLUTION_FAILURE_MECHANISM_PROPOSAL",
                ("MISSING_PRIMITIVE", "MISSING_PRIMITIVE"),
            ),
            (
                "SOURCE_ASSERTED_REVERSAL_OR_REAPPEARANCE",
                "REVERSAL_OR_REAPPEARANCE_ASSERTION",
                "RELATION_EFFECT_DISPOSITION",
                ("CLASSICAL_REVERSAL_OR_REAPPEARANCE_SEMANTICS",),
                "REVERSAL_OR_REAPPEARANCE_MECHANISM_PROPOSAL",
                ("MISSING_PRIMITIVE",),
            ),
            (
                "SOURCE_ASSERTED_ATTENUATION",
                "ATTENUATION_ASSERTION",
                "RELATION_EFFECT_GRADE",
                ("CLASSICAL_ATTENUATION_GRADE",),
                "ATTENUATION_MECHANISM_PROPOSAL",
                ("MISSING_PRIMITIVE",),
            ),
        ]
        for claim, assertion, facet, requirements, proposal_kind, statuses in cases:
            candidate, proposal = self._controlled_candidate(
                claim, assertion, facet, requirements
            )
            self.assertEqual(proposal_kind, proposal.mechanism_proposal_kind)
            self.assertEqual(requirements, proposal.unresolved_classical_semantic_requirements)
            self.assertEqual(
                statuses,
                tuple(row.runtime_dependency_status for row in proposal.closure_governance_rows),
            )
            self.assertEqual("NOT_RELEASED", proposal.mechanism_execution_semantics)
            self.assertEqual("NOT_RELEASED", proposal.rewrite_application_semantics)
            self.assertFalse(hasattr(proposal, "winner"))
            self.assertFalse(hasattr(proposal, "relation_state"))
            if candidate.semantic_candidate_kind == "SOURCE_GROUNDED_ATTENUATION_CANDIDATE":
                self.assertFalse(hasattr(proposal, "numeric_grade"))

    def test_005_allocation_has_missing_semantics_and_partial_path_support(self):
        effect, admission, semantic, _, _ = self.multiplicity
        found = False
        for effect_outer, admission_outer, semantic_outer in zip(
            effect.candidates, admission.candidates, semantic.candidates, strict=True
        ):
            for fragment in effect_outer.fragments:
                if fragment.source_occurrence_id != "ZPZQ-CL-09-005-002":
                    continue
                allocation_nodes = [
                    node for node in fragment.effect_constraint_nodes
                    if node.constraint.source_claim_edge_class == "SOURCE_ASSERTED_PARTICIPANT_ALLOCATION"
                ]
                if not allocation_nodes:
                    continue
                found = True
                upstream = next(
                    row for row in admission_outer.fragment_admissions
                    if row.source_fragment_id == fragment.fragment_id
                )
                admitted = replace(upstream, admission_status="ADMITTED", admission_blocker_ids=())
                local_fragment = replace(fragment, effect_constraint_nodes=(allocation_nodes[0],))
                fragment_projection = project_fragment_semantic_candidates(
                    admission_outer, admitted, local_fragment, self.semantic_profile
                )
                candidate = fragment_projection.semantic_candidates[0]
                proposal = project_mechanism_proposal(
                    semantic_outer, fragment_projection, candidate, self.closure_profile
                )
                status_by_requirement = {
                    row.closure_requirement_id: row.runtime_dependency_status
                    for row in proposal.closure_governance_rows
                }
                self.assertEqual("MISSING_PRIMITIVE", status_by_requirement["CLASSICAL_PARTICIPANT_ALLOCATION"])
                self.assertEqual("PARTIALLY_AVAILABLE", status_by_requirement["COMPATIBLE_EXACT_INSTANCE_PATH_ENUMERATION"])
                path_row = next(
                    row for row in proposal.closure_governance_rows
                    if row.closure_requirement_id == "COMPATIBLE_EXACT_INSTANCE_PATH_ENUMERATION"
                )
                self.assertEqual(
                    "EXACT_MULTIPLICITY_RUNTIME_INSTANCE_PROVENANCE_PARTIAL_PATH_SUPPORT",
                    path_row.upstream_support_class,
                )
                self.assertTrue(path_row.upstream_support_reference_ids)
                self.assertFalse(hasattr(proposal, "selected_path"))
                self.assertFalse(hasattr(proposal, "selected_participant_id"))
        self.assertTrue(found)

    def test_source_graph_provenance_does_not_change_closure_rows(self):
        _, proposal = self._controlled_candidate(
            "SOURCE_ASSERTED_RESOLUTION",
            "RESOLUTION_ASSERTION",
            "RELATION_EFFECT_DISPOSITION",
            ("CLASSICAL_RESOLUTION_SEMANTICS",),
        )
        effect, admission, semantic, _, _ = self.cross
        semantic_outer = semantic.candidates[0]
        fragment_projection = semantic_outer.fragment_projections[0]
        source_candidate = replace(
            fragment_projection.semantic_candidates[0],
            semantic_candidate_kind="SOURCE_GROUNDED_RESOLUTION_CANDIDATE",
            unresolved_classical_semantic_requirements=("CLASSICAL_RESOLUTION_SEMANTICS",),
            source_unresolved_graph_requirements_provenance=("TOTALLY_DIFFERENT_PROVENANCE",),
        )
        changed = project_mechanism_proposal(
            semantic_outer,
            fragment_projection,
            source_candidate,
            self.closure_profile,
        )
        self.assertEqual(
            tuple((row.closure_requirement_id, row.runtime_dependency_status, row.governance_class, row.future_owner) for row in proposal.closure_governance_rows),
            tuple((row.closure_requirement_id, row.runtime_dependency_status, row.governance_class, row.future_owner) for row in changed.closure_governance_rows),
        )

    def test_runtime_schema_is_closed_against_resolver_surface(self):
        _, _, _, request, _ = self.cross
        payload = BaziClassicalSemanticMechanismClosureGovernanceEngine().resolve(request)
        schema = json.loads((ROOT / "schemas/bazi-classical-semantic-mechanism-closure-runtime-r1.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        validator.validate(payload)
        forbidden = [
            "truth", "operative", "applicable", "winner", "loser", "priority",
            "precedence", "conflict_result", "rewrite_result", "relation_state",
            "effect_state", "activated", "suppressed", "released", "cancelled",
            "overridden", "fixpoint", "final_classical_verdict",
        ]
        for field in forbidden:
            changed = copy.deepcopy(payload)
            changed["candidates"][0][field] = "invented"
            self.assertTrue(list(validator.iter_errors(changed)), field)


if __name__ == "__main__":
    unittest.main()
