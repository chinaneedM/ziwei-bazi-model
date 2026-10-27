from __future__ import annotations

import copy
import json
import unittest
from dataclasses import replace
from pathlib import Path

from jsonschema import Draft202012Validator

from fortune_training.bazi_classical_resolver_admission import (
    BaziClassicalResolverAdmissionEngine,
    BaziClassicalResolverAdmissionRequest,
    bazi_classical_resolver_admission_strict_r1_profile,
    project_fragment_admission,
    shen_zpzq_ch09_classical_interaction_r1_profile,
    validate_release_contract,
)
from test_bazi_classical_effect_constraint_graph_factorized_composition_r1 import (
    BaziClassicalEffectConstraintGraphFactorizedCompositionR1Tests as Unit2Stack,
)

ROOT = Path(__file__).resolve().parents[1]


class BaziClassicalSourceProfileResolverAdmissionR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Unit2Stack.setUpClass()
        cls.binding, cls.projection, _, cls.effect = Unit2Stack.cross_layer
        cls.source_profile = shen_zpzq_ch09_classical_interaction_r1_profile()
        cls.admission_profile = bazi_classical_resolver_admission_strict_r1_profile()
        cls.request = BaziClassicalResolverAdmissionRequest(
            cls.binding, cls.projection, cls.effect, cls.source_profile, cls.admission_profile
        )
        cls.result = BaziClassicalResolverAdmissionEngine().resolve_typed(cls.request)
        if cls.result.status == "FAILED":
            raise AssertionError(cls.result.diagnostics)

    def test_release_contract_and_source_partition_are_closed(self):
        report = validate_release_contract(ROOT)
        self.assertEqual("PASS", report["status"])
        self.assertEqual(13, report["source_profile_member_count"])
        self.assertEqual("869916b557dcc889831b4775679cf1bd0db9e786f280ec42493cafd188e9bec6", report["contract_semantics_sha256"])
        self.assertEqual("PARTITION_IDENTITY_ONLY", self.source_profile.semantic_role)
        self.assertIn("ZPZQ-CL-09-007-002", self.source_profile.member_source_occurrence_ids)
        self.assertNotIn("QTBJ-CL-05347", self.source_profile.member_source_occurrence_ids)

    def test_release_schema_rejects_nested_policy_and_regression_drift(self):
        contract = json.loads((ROOT / "audits/bazi-classical-source-semantic-profile-resolver-admission-r1/contract.json").read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas/bazi-classical-source-semantic-profile-resolver-admission-r1.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        validator.validate(contract)
        mutations = []
        changed = copy.deepcopy(contract)
        changed["strict_admission_contract"]["lifecycle_global_truth_gate"] = "RELEASED"
        mutations.append(changed)
        changed = copy.deepcopy(contract)
        changed["preservation_contract"]["fragment_selection"] = "FIRST"
        mutations.append(changed)
        changed = copy.deepcopy(contract)
        changed["regression_matrix"][0]["expected_status"] = "ADMITTED"
        mutations.append(changed)
        changed = copy.deepcopy(contract)
        changed["hard_exclusions"].remove("PRECEDENCE")
        mutations.append(changed)
        for changed in mutations:
            self.assertTrue(list(validator.iter_errors(changed)))

    def test_007_002_is_upstream_partial(self):
        plan = json.loads((ROOT / "audits/bazi-chart-specific-exact-source-pattern-binding-candidates-r1/bindability-plan.json").read_text(encoding="utf-8"))
        row = next(row for row in plan["bindability_plan"] if row["source_occurrence_id"] == "ZPZQ-CL-09-007-002")
        self.assertEqual("PARTIAL_EXACT_BINDING_ENUMERATION", row["bindability_class"])
        self.assertIn("SOURCE_POSITION_CONTEXT_REMAINS_UNRESOLVED", row["structural_reason_ids"])

    def test_real_runtime_preserves_every_unit2_fragment_exactly_once(self):
        self.assertEqual(len(self.effect.candidates), len(self.result.candidates))
        for source, projected in zip(self.effect.candidates, self.result.candidates, strict=True):
            self.assertEqual([row.fragment_id for row in source.fragments], [row.source_fragment_id for row in projected.fragment_admissions])
            self.assertEqual("NOT_RELEASED", projected.fragment_selection_semantics)
            self.assertEqual("NOT_RELEASED", projected.cross_outer_composition)
            self.assertEqual("NOT_RELEASED", projected.cartesian_expansion)

    def test_cross_layer_003_002_is_preserved_not_admitted(self):
        rows = [row for envelope in self.result.candidates for row in envelope.fragment_admissions if row.source_occurrence_id == "ZPZQ-CL-09-003-002"]
        self.assertTrue(rows)
        self.assertTrue(all(row.admission_status == "PRESERVED_NOT_ADMITTED" for row in rows))
        self.assertTrue(all("CROSS_LAYER_EXTENSION_UNRESOLVED" in row.admission_blocker_ids for row in rows))

    def test_four_structural_scope_combinations_are_independent(self):
        source = self.effect.candidates[0]
        projection = self.projection.candidates[0]
        fragment = next(row for row in source.fragments if row.source_occurrence_id == "ZPZQ-CL-09-003-002")
        bundle = next(row for row in projection.bundles if row.binding_candidate_id == fragment.binding_candidate_id)

        def classify(structural: str, scope: str):
            local_bundle = replace(
                bundle,
                structural_binding_class=structural,
                source_scope_compatibility=replace(bundle.source_scope_compatibility, source_scope_compatibility=scope),
                residual_unresolved_structural_constraint_ids=(),
            )
            local_fragment = replace(
                fragment,
                structural_binding_class=structural,
                source_scope_compatibility=scope,
                residual_unresolved_structural_constraint_ids=(),
            )
            return project_fragment_admission(source, local_fragment, local_bundle, self.source_profile, self.admission_profile)

        self.assertEqual(("ADMITTED", ()), (classify("FULL_EXACT_BINDING_ENUMERATION", "DIRECT_SOURCE_SCOPE_MATCH").admission_status, classify("FULL_EXACT_BINDING_ENUMERATION", "DIRECT_SOURCE_SCOPE_MATCH").admission_blocker_ids))
        self.assertEqual(("CROSS_LAYER_EXTENSION_UNRESOLVED",), classify("FULL_EXACT_BINDING_ENUMERATION", "CROSS_LAYER_EXTENSION_UNRESOLVED").admission_blocker_ids)
        self.assertEqual(("STRUCTURAL_BINDING_PARTIAL",), classify("PARTIAL_EXACT_BINDING_ENUMERATION", "DIRECT_SOURCE_SCOPE_MATCH").admission_blocker_ids)
        self.assertEqual(("STRUCTURAL_BINDING_PARTIAL", "CROSS_LAYER_EXTENSION_UNRESOLVED"), classify("PARTIAL_EXACT_BINDING_ENUMERATION", "CROSS_LAYER_EXTENSION_UNRESOLVED").admission_blocker_ids)

    def test_source_graph_requirements_are_provenance_not_admission_predicate(self):
        source = self.effect.candidates[0]
        projection = self.projection.candidates[0]
        fragment = next(row for row in source.fragments if row.source_occurrence_id == "ZPZQ-CL-09-003-002")
        bundle = next(row for row in projection.bundles if row.binding_candidate_id == fragment.binding_candidate_id)
        provenance = ("CLASSICAL_RESOLUTION_SEMANTICS", "SOURCE_PATTERN_TO_EXACT_INSTANCE_BINDING")
        local_bundle = replace(bundle, source_scope_compatibility=replace(bundle.source_scope_compatibility, source_scope_compatibility="DIRECT_SOURCE_SCOPE_MATCH"), residual_unresolved_structural_constraint_ids=(), source_unresolved_graph_requirements=provenance)
        local_fragment = replace(fragment, structural_binding_class="FULL_EXACT_BINDING_ENUMERATION", source_scope_compatibility="DIRECT_SOURCE_SCOPE_MATCH", residual_unresolved_structural_constraint_ids=(), source_unresolved_graph_requirements=provenance)
        row = project_fragment_admission(source, local_fragment, local_bundle, self.source_profile, self.admission_profile)
        self.assertEqual("ADMITTED", row.admission_status)
        self.assertEqual(provenance, row.source_unresolved_graph_requirements_provenance)
        self.assertTrue(row.unresolved_classical_semantic_requirements)

    def test_public_runtime_schema_is_closed(self):
        payload = BaziClassicalResolverAdmissionEngine().resolve(self.request)
        schema = json.loads((ROOT / "schemas/bazi-classical-resolver-admission-runtime-r1.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(payload)
        payload["candidates"][0]["fragment_admissions"][0]["winner"] = "invented"
        self.assertTrue(list(Draft202012Validator(schema).iter_errors(payload)))


if __name__ == "__main__":
    unittest.main()
