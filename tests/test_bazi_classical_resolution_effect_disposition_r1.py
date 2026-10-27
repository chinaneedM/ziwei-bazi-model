from __future__ import annotations

import copy
import json
import unittest
from dataclasses import replace
from pathlib import Path

from jsonschema import Draft202012Validator

from fortune_training.bazi_classical_resolution_effect_disposition import (
    BaziClassicalResolutionEffectDispositionEngine,
    BaziClassicalResolutionEffectDispositionRequest,
    build_expected_indexes,
    expected_candidate_projection,
    expected_fragment_projection,
    bazi_classical_resolution_effect_disposition_r1_profile,
)
from fortune_training.bazi_classical_resolution_effect_disposition.release import (
    validate_release_contract,
)
from fortune_training.bazi_classical_semantic_closure_governance.models import (
    ClassicalSemanticClosureGovernanceRow,
)
from fortune_training.calendar_foundation.models import json_value
import test_bazi_classical_final_effect_candidate_envelope_r1 as unit7_tests


ROOT = Path(__file__).resolve().parents[1]


class BaziClassicalResolutionEffectDispositionR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        unit7_tests.BaziClassicalFinalEffectCandidateEnvelopeR1Tests.setUpClass()
        source = unit7_tests.BaziClassicalFinalEffectCandidateEnvelopeR1Tests
        cls.profile = bazi_classical_resolution_effect_disposition_r1_profile()
        cls.cross = cls._unit8(source.cross)
        cls.multiplicity = cls._unit8(source.multiplicity)
        cls.base_allocation_candidate = source.controlled_fragment.final_candidates[0]
        cls.resolution_candidate = cls._resolution_candidate(cls.base_allocation_candidate)

    @classmethod
    def _unit8(cls, stack):
        effect, admission, semantic, mechanism, allocation, _, final = stack
        request = BaziClassicalResolutionEffectDispositionRequest(
            effect,
            admission,
            semantic,
            mechanism,
            allocation,
            final,
            cls.profile,
        )
        result = BaziClassicalResolutionEffectDispositionEngine().resolve_typed(request)
        if result.status == "FAILED":
            raise AssertionError(result.diagnostics)
        return request, result

    @staticmethod
    def _resolution_candidate(candidate):
        closure = ClassicalSemanticClosureGovernanceRow(
            closure_requirement_id="CLASSICAL_RESOLUTION_SEMANTICS",
            runtime_dependency_status="MISSING_PRIMITIVE",
            governance_class="SEMANTIC_EFFECT_DISPOSITION_CLOSURE",
            future_owner="FUTURE_EXECUTION_CAPABLE_SEMANTIC_REWRITE_OR_RESOLVER",
            upstream_support_class=(
                "EXACT_SOURCE_GROUNDED_RELATION_IDENTITY_WITHOUT_CLASSICAL_SEMANTIC_CLOSURE"
            ),
            upstream_support_reference_ids=(candidate.target_exact_relation_id,),
        )
        return replace(
            candidate,
            final_candidate_id="CONTROLLED-UNIT8-RESOLUTION-FINAL-CANDIDATE",
            source_claim_edge_class="SOURCE_ASSERTED_RESOLUTION",
            source_assertion_class="RESOLUTION_ASSERTION",
            effect_facet="RELATION_EFFECT_DISPOSITION",
            semantic_candidate_kind="SOURCE_GROUNDED_RESOLUTION_CANDIDATE",
            mechanism_proposal_kind="RESOLUTION_MECHANISM_PROPOSAL",
            unresolved_classical_semantic_requirements=(
                "CLASSICAL_RESOLUTION_SEMANTICS",
            ),
            closure_governance_rows=(closure,),
            multiplicity_references=(),
            allocation_domain_observations=(),
        )

    def test_release_contract_is_exact_and_closed(self):
        report = validate_release_contract(ROOT)
        self.assertEqual("PASS", report["status"])
        self.assertEqual(
            "SOURCE_GROUNDED_RESOLUTION_CANDIDATE",
            report["handled_semantic_candidate_kind"],
        )
        self.assertEqual(
            "3b9e8b124ee00679bc14bfeab4c34fd626f85df20cb029a4670c02c3fc8425f6",
            report["contract_semantics_sha256"],
        )
        contract = json.loads((ROOT / "audits/bazi-classical-resolution-effect-disposition-r1/contract.json").read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas/bazi-classical-resolution-effect-disposition-r1.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        validator.validate(contract)
        changed = copy.deepcopy(contract)
        changed["local_resolution_closure_contract"]["general_resolver_readiness"] = "RELEASED"
        self.assertTrue(list(validator.iter_errors(changed)))
        changed = copy.deepcopy(contract)
        changed["hard_exclusions"].remove("PRECEDENCE_OR_PRIORITY")
        self.assertTrue(list(validator.iter_errors(changed)))

    def test_resolution_candidate_projects_one_candidate_local_disposition(self):
        projection = expected_candidate_projection(self.resolution_candidate, self.profile)
        self.assertEqual("RESOLUTION_EFFECT_DISPOSITION_PROJECTED", projection.projection_status)
        self.assertEqual(self.resolution_candidate, projection.source_final_candidate)
        self.assertEqual(1, len(projection.resolution_closure_rows))
        local = projection.resolution_closure_rows[0]
        self.assertEqual("CLASSICAL_RESOLUTION_SEMANTICS", local.closure_requirement_id)
        self.assertEqual("MISSING_PRIMITIVE", local.upstream_runtime_dependency_status)
        self.assertEqual(
            "AVAILABLE_EXACTLY_AS_CANDIDATE_LOCAL_SOURCE_ASSERTED_EFFECT_DISPOSITION",
            local.unit8_local_closure_result,
        )
        self.assertEqual(1, len(projection.resolution_effect_dispositions))
        disposition = projection.resolution_effect_dispositions[0]
        self.assertEqual("SOURCE_ASSERTED_RESOLVED_EFFECT_DISPOSITION", disposition.disposition_kind)
        self.assertEqual("CANDIDATE_LOCAL_SOURCE_ASSERTED_EFFECT_BRANCH_ONLY", disposition.semantic_scope)
        self.assertEqual("NO_MUTATION", disposition.raw_relation_action)
        self.assertEqual("UNCHANGED", disposition.raw_relation_presence_semantics)
        self.assertEqual(self.resolution_candidate.target_exact_relation_id, disposition.target_exact_relation_id)
        self.assertEqual(self.resolution_candidate.target_effect_channel_id, disposition.target_effect_channel_id)
        self.assertEqual(self.resolution_candidate.closure_governance_rows[0].runtime_dependency_status, "MISSING_PRIMITIVE")

    def test_non_resolution_candidates_emit_zero_resolution_dispositions(self):
        variants = (
            ("SOURCE_GROUNDED_RESOLUTION_FAILURE_CANDIDATE", "RESOLUTION_FAILURE_MECHANISM_PROPOSAL", "SOURCE_ASSERTED_RESOLUTION_FAILURE", "RELATION_EFFECT_DISPOSITION"),
            ("SOURCE_GROUNDED_REVERSAL_OR_REAPPEARANCE_CANDIDATE", "REVERSAL_OR_REAPPEARANCE_MECHANISM_PROPOSAL", "SOURCE_ASSERTED_REVERSAL_OR_REAPPEARANCE", "RELATION_EFFECT_DISPOSITION"),
            ("SOURCE_GROUNDED_ATTENUATION_CANDIDATE", "ATTENUATION_MECHANISM_PROPOSAL", "SOURCE_ASSERTED_ATTENUATION", "RELATION_EFFECT_GRADE"),
            ("SOURCE_GROUNDED_PARTICIPANT_ALLOCATION_CANDIDATE", "PARTICIPANT_ALLOCATION_MECHANISM_PROPOSAL", "SOURCE_ASSERTED_PARTICIPANT_ALLOCATION", "RELATION_PARTICIPANT_ALLOCATION"),
        )
        for semantic_kind, mechanism_kind, claim_class, facet in variants:
            candidate = replace(
                self.resolution_candidate,
                final_candidate_id=f"CONTROLLED:{semantic_kind}",
                semantic_candidate_kind=semantic_kind,
                mechanism_proposal_kind=mechanism_kind,
                source_claim_edge_class=claim_class,
                effect_facet=facet,
            )
            projection = expected_candidate_projection(candidate, self.profile)
            self.assertEqual("PRESERVED_NON_RESOLUTION_CANDIDATE", projection.projection_status)
            self.assertEqual((), projection.resolution_closure_rows)
            self.assertEqual((), projection.resolution_effect_dispositions)
            self.assertEqual((), projection.resolution_effect_disposition_ids)

    def test_same_channel_resolution_candidates_remain_separate_and_unranked(self):
        first = expected_candidate_projection(self.resolution_candidate, self.profile)
        second_candidate = replace(
            self.resolution_candidate,
            final_candidate_id="CONTROLLED-UNIT8-RESOLUTION-FINAL-CANDIDATE-SECOND",
            source_claim_edge_id=f"{self.resolution_candidate.source_claim_edge_id}:SECOND",
        )
        second = expected_candidate_projection(second_candidate, self.profile)
        effect_index, _, closure_index = build_expected_indexes((first, second))
        self.assertEqual(1, len(effect_index))
        row = effect_index[0]
        self.assertEqual((first.candidate_projection_id, second.candidate_projection_id), row.candidate_projection_ids)
        self.assertEqual("IDENTITY_ONLY_NO_MERGE_RANK_ARBITRATION_SELECTION_OR_GLOBAL_STATE", row.index_semantics)
        self.assertEqual(2, len(row.resolution_effect_disposition_ids))
        self.assertEqual(2, len(closure_index[0].candidate_projection_ids))

    def test_zero_candidate_fragment_remains_zero_candidate(self):
        source = unit7_tests.BaziClassicalFinalEffectCandidateEnvelopeR1Tests.controlled_fragment
        zero = replace(
            source,
            final_fragment_status="PRESERVED_ZERO_FINAL_EFFECT_CANDIDATES",
            source_semantic_candidate_ids=(),
            source_mechanism_proposal_ids=(),
            source_allocation_elaboration_ids=(),
            final_candidates=(),
            final_candidate_ids=(),
        )
        projected = expected_fragment_projection(zero, self.profile)
        self.assertEqual("PRESERVED_ZERO_CANDIDATES", projected.projection_status)
        self.assertEqual((), projected.candidate_projections)
        self.assertEqual((), projected.resolution_effect_disposition_ids)

    def test_real_stack_replays_unit7_and_preserves_every_outer_and_fragment(self):
        for request, result in (self.cross, self.multiplicity):
            self.assertEqual(len(request.source_final_effect_resolution.candidates), len(result.candidates))
            for source_outer, projected_outer in zip(
                request.source_final_effect_resolution.candidates,
                result.candidates,
                strict=True,
            ):
                self.assertEqual(source_outer.final_effect_envelope_id, projected_outer.source_final_effect_envelope_id)
                self.assertEqual(len(source_outer.fragment_envelopes), len(projected_outer.fragment_projections))
                for source_fragment, projected_fragment in zip(
                    source_outer.fragment_envelopes,
                    projected_outer.fragment_projections,
                    strict=True,
                ):
                    self.assertEqual(source_fragment.final_fragment_id, projected_fragment.source_final_fragment_id)
                    self.assertEqual(source_fragment.final_candidate_ids, projected_fragment.source_final_candidate_ids)
                self.assertEqual("NOT_RELEASED", projected_outer.candidate_global_truth_semantics)
                self.assertEqual("NOT_RELEASED", projected_outer.global_operability_semantics)
                self.assertEqual("NOT_RELEASED", projected_outer.execution_readiness_semantics)
                self.assertEqual("NOT_RELEASED", projected_outer.precedence_semantics)
                self.assertEqual("NOT_RELEASED", projected_outer.winner_loser_semantics)
                self.assertEqual("NOT_RELEASED", projected_outer.global_relation_effect_state_semantics)
                self.assertEqual("NOT_RELEASED", projected_outer.final_classical_verdict_semantics)

    def test_runtime_schema_rejects_resolver_surface_at_outer_and_nested_candidate(self):
        payload = BaziClassicalResolutionEffectDispositionEngine().resolve(self.cross[0])
        schema = json.loads((ROOT / "schemas/bazi-classical-resolution-effect-disposition-runtime-r1.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        validator.validate(payload)
        forbidden = [
            "truth", "operative", "applicable", "ready_for_execution",
            "selected_candidate", "selected_participant_id", "selected_path",
            "winner", "loser", "priority", "precedence", "conflict_result",
            "relation_state", "global_effect_state", "rewrite_result", "activated",
            "suppressed", "released", "cancelled", "overridden", "fixpoint",
            "final_verdict", "final_classical_verdict",
        ]
        for field in forbidden:
            changed = copy.deepcopy(payload)
            changed["candidates"][0][field] = True
            self.assertTrue(list(validator.iter_errors(changed)), field)

        projection = expected_candidate_projection(self.resolution_candidate, self.profile)
        projection_payload = json_value(projection)
        projection_validator = validator.evolve(schema=schema["$defs"]["candidateProjection"])
        projection_validator.validate(projection_payload)
        for field in forbidden:
            changed = copy.deepcopy(projection_payload)
            changed["source_final_candidate"][field] = True
            self.assertTrue(list(projection_validator.iter_errors(changed)), field)


if __name__ == "__main__":
    unittest.main()
