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
    SOURCE_CLAIM_TO_SEMANTIC_CANDIDATE,
    bazi_classical_effect_semantic_candidate_projection_r1_profile,
    project_fragment_semantic_candidates,
    validate_release_contract,
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

ROOT = Path(__file__).resolve().parents[1]


class BaziClassicalEffectSemanticCandidateProjectionR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Unit2Stack.setUpClass()
        cls.source_profile = shen_zpzq_ch09_classical_interaction_r1_profile()
        cls.admission_profile = bazi_classical_resolver_admission_strict_r1_profile()
        cls.semantic_profile = bazi_classical_effect_semantic_candidate_projection_r1_profile()
        cls.cross = cls._unit4(Unit2Stack.cross_layer)
        cls.multiplicity = cls._unit4(Unit2Stack.multiplicity)

    @classmethod
    def _unit4(cls, stack):
        binding, projection, _, effect = stack
        admission_request = BaziClassicalResolverAdmissionRequest(
            binding, projection, effect, cls.source_profile, cls.admission_profile
        )
        admission = BaziClassicalResolverAdmissionEngine().resolve_typed(admission_request)
        if admission.status == "FAILED":
            raise AssertionError(admission.diagnostics)
        request = BaziClassicalEffectSemanticCandidateProjectionRequest(
            effect, admission, cls.semantic_profile
        )
        result = BaziClassicalEffectSemanticCandidateProjectionEngine().resolve_typed(request)
        if result.status == "FAILED":
            raise AssertionError(result.diagnostics)
        return effect, admission, request, result

    def test_release_contract_is_exact_and_closed(self):
        report = validate_release_contract(ROOT)
        self.assertEqual("PASS", report["status"])
        self.assertEqual(5, report["semantic_candidate_kind_count"])
        self.assertEqual(
            "d96ea5a66bea6ff5b71b280723c460954d80ed8da6d05008f909cef30a13a3c8",
            report["contract_semantics_sha256"],
        )
        contract = json.loads((ROOT / "audits/bazi-classical-effect-semantic-candidate-projection-r1/contract.json").read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas/bazi-classical-effect-semantic-candidate-projection-r1.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(contract)
        changed = copy.deepcopy(contract)
        changed["candidate_preservation_contract"]["candidate_priority"] = "RELEASED"
        self.assertTrue(list(Draft202012Validator(schema).iter_errors(changed)))
        changed = copy.deepcopy(contract)
        changed["hard_exclusions"].remove("PRECEDENCE")
        self.assertTrue(list(Draft202012Validator(schema).iter_errors(changed)))

    def test_real_stack_preserves_one_outer_and_every_fragment(self):
        for effect, admission, _, result in (self.cross, self.multiplicity):
            self.assertEqual(len(admission.candidates), len(result.candidates))
            for effect_outer, admission_outer, semantic_outer in zip(
                effect.candidates, admission.candidates, result.candidates, strict=True
            ):
                self.assertEqual(admission_outer.admission_envelope_id, semantic_outer.source_admission_envelope_id)
                self.assertEqual(effect_outer.envelope_id, semantic_outer.source_effect_envelope_id)
                self.assertEqual(
                    [row.fragment_id for row in effect_outer.fragments],
                    [row.source_fragment_id for row in semantic_outer.fragment_projections],
                )
                self.assertEqual("NOT_RELEASED", semantic_outer.cross_outer_composition)
                self.assertEqual("NOT_RELEASED", semantic_outer.cartesian_expansion)
                self.assertEqual("NOT_RELEASED", semantic_outer.candidate_priority_semantics)
                self.assertEqual("NOT_RELEASED", semantic_outer.candidate_conflict_semantics)
                self.assertEqual("NOT_RELEASED", semantic_outer.candidate_winner_loser_semantics)

    def test_non_admitted_and_outside_profile_emit_zero_candidates(self):
        effect, admission, _, result = self.cross
        admission_rows = {
            row.source_fragment_id: row
            for outer in admission.candidates
            for row in outer.fragment_admissions
        }
        semantic_rows = {
            row.source_fragment_id: row
            for outer in result.candidates
            for row in outer.fragment_projections
        }
        self.assertEqual(set(admission_rows), set(semantic_rows))
        for fragment_id, upstream in admission_rows.items():
            row = semantic_rows[fragment_id]
            if upstream.admission_status == "PRESERVED_NOT_ADMITTED":
                self.assertEqual("PRESERVED_NO_SEMANTIC_CANDIDATES", row.projection_status)
                self.assertEqual((), row.semantic_candidates)
            elif upstream.admission_status == "PRESERVED_OUTSIDE_PROFILE":
                self.assertEqual("PRESERVED_OUTSIDE_PROFILE_NO_SEMANTIC_CANDIDATES", row.projection_status)
                self.assertEqual((), row.semantic_candidates)

    def test_five_claim_classes_map_one_to_one_without_solver_state(self):
        effect, admission, _, _ = self.cross
        effect_outer = effect.candidates[0]
        admission_outer = admission.candidates[0]
        base_fragment = effect_outer.fragments[0]
        base_admission = next(
            row for row in admission_outer.fragment_admissions
            if row.source_fragment_id == base_fragment.fragment_id
        )
        base_constraint_node = base_fragment.effect_constraint_nodes[0]
        mapping = {
            "SOURCE_ASSERTED_RESOLUTION": ("RESOLUTION_ASSERTION", "RELATION_EFFECT_DISPOSITION"),
            "SOURCE_ASSERTED_RESOLUTION_FAILURE": ("RESOLUTION_FAILURE_ASSERTION", "RELATION_EFFECT_DISPOSITION"),
            "SOURCE_ASSERTED_REVERSAL_OR_REAPPEARANCE": ("REVERSAL_OR_REAPPEARANCE_ASSERTION", "RELATION_EFFECT_DISPOSITION"),
            "SOURCE_ASSERTED_ATTENUATION": ("ATTENUATION_ASSERTION", "RELATION_EFFECT_GRADE"),
        }
        admitted = replace(base_admission, admission_status="ADMITTED", admission_blocker_ids=())
        for claim_class, (assertion_class, facet) in mapping.items():
            constraint = replace(
                base_constraint_node.constraint,
                source_claim_edge_class=claim_class,
                source_assertion_class=assertion_class,
                effect_facet=facet,
                multiplicity_references=(),
            )
            fragment = replace(
                base_fragment,
                effect_constraint_nodes=(replace(base_constraint_node, constraint=constraint),),
            )
            row = project_fragment_semantic_candidates(
                admission_outer, admitted, fragment, self.semantic_profile
            )
            self.assertEqual(1, len(row.semantic_candidates))
            candidate = row.semantic_candidates[0]
            self.assertEqual(SOURCE_CLAIM_TO_SEMANTIC_CANDIDATE[claim_class][1], candidate.semantic_candidate_kind)
            self.assertEqual(facet, candidate.effect_facet)
            self.assertEqual("NOT_RELEASED", candidate.candidate_truth_semantics)
            self.assertFalse(hasattr(candidate, "winner"))
            self.assertFalse(hasattr(candidate, "relation_state"))

    def test_005_002_allocation_candidate_preserves_multiplicity_without_selection(self):
        effect, admission, _, _ = self.multiplicity
        found = False
        for effect_outer, admission_outer in zip(effect.candidates, admission.candidates, strict=True):
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
                row = project_fragment_semantic_candidates(
                    admission_outer, admitted, local_fragment, self.semantic_profile
                )
                candidate = row.semantic_candidates[0]
                self.assertEqual("SOURCE_GROUNDED_PARTICIPANT_ALLOCATION_CANDIDATE", candidate.semantic_candidate_kind)
                self.assertTrue(candidate.multiplicity_references)
                self.assertTrue(all(
                    ref.alternative_path_requirement == "PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS"
                    for ref in candidate.multiplicity_references
                ))
                self.assertFalse(hasattr(candidate, "selected_participant_id"))
                self.assertFalse(hasattr(candidate, "selected_path"))
        self.assertTrue(found, "005-002 allocation constraint not present in multiplicity fixture")

    def test_007_partial_admission_is_not_upgraded(self):
        _, admission, _, result = self.cross
        upstream_rows = [
            row for outer in admission.candidates for row in outer.fragment_admissions
            if row.source_occurrence_id in {"ZPZQ-CL-09-007-002", "ZPZQ-CL-09-007-003"}
        ]
        semantic_rows = [
            row for outer in result.candidates for row in outer.fragment_projections
            if row.source_occurrence_id in {"ZPZQ-CL-09-007-002", "ZPZQ-CL-09-007-003"}
        ]
        self.assertEqual(len(upstream_rows), len(semantic_rows))
        for upstream, projected in zip(upstream_rows, semantic_rows, strict=True):
            self.assertNotEqual("ADMITTED", upstream.admission_status)
            self.assertEqual((), projected.semantic_candidates)

    def test_runtime_schema_rejects_solver_and_rewrite_fields(self):
        _, _, request, _ = self.cross
        payload = BaziClassicalEffectSemanticCandidateProjectionEngine().resolve(request)
        schema = json.loads((ROOT / "schemas/bazi-classical-effect-semantic-candidate-runtime-r1.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        validator.validate(payload)
        outer = payload["candidates"][0]
        forbidden = ["winner", "precedence", "priority", "relation_state", "effect_state", "rewrite_result", "fixpoint"]
        for field in forbidden:
            changed = copy.deepcopy(payload)
            changed["candidates"][0][field] = "invented"
            self.assertTrue(list(validator.iter_errors(changed)), field)


if __name__ == "__main__":
    unittest.main()
