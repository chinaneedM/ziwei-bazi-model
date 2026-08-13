from __future__ import annotations

import copy
import json
import unittest
from dataclasses import replace
from pathlib import Path

from jsonschema import Draft202012Validator

from fortune_training.bazi_classical_reversal_reappearance_effect_disposition import (
    BaziClassicalReversalReappearanceEffectDispositionEngine,
    BaziClassicalReversalReappearanceEffectDispositionRequest,
    build_expected_indexes,
    expected_candidate_projection,
    expected_fragment_projection,
    bazi_classical_reversal_reappearance_effect_disposition_r1_profile,
)
from fortune_training.bazi_classical_reversal_reappearance_effect_disposition.release import (
    validate_release_contract,
)
from fortune_training.bazi_classical_semantic_closure_governance.models import (
    ClassicalSemanticClosureGovernanceRow,
)
from fortune_training.calendar_foundation.models import json_value
import test_bazi_classical_final_effect_candidate_envelope_r1 as unit7_tests


ROOT = Path(__file__).resolve().parents[1]


class BaziClassicalReversalReappearanceEffectDispositionR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        unit7_tests.BaziClassicalFinalEffectCandidateEnvelopeR1Tests.setUpClass()
        source = unit7_tests.BaziClassicalFinalEffectCandidateEnvelopeR1Tests
        cls.profile = bazi_classical_reversal_reappearance_effect_disposition_r1_profile()
        cls.cross = cls._unit10(source.cross)
        cls.multiplicity = cls._unit10(source.multiplicity)
        cls.base_allocation_candidate = source.controlled_fragment.final_candidates[0]
        cls.reversal_candidate = cls._reversal_candidate(cls.base_allocation_candidate)

    @classmethod
    def _unit10(cls, stack):
        effect, admission, semantic, mechanism, allocation, _, final = stack
        request = BaziClassicalReversalReappearanceEffectDispositionRequest(
            effect,
            admission,
            semantic,
            mechanism,
            allocation,
            final,
            cls.profile,
        )
        result = BaziClassicalReversalReappearanceEffectDispositionEngine().resolve_typed(
            request
        )
        if result.status == "FAILED":
            raise AssertionError(result.diagnostics)
        return request, result

    @staticmethod
    def _reversal_candidate(candidate):
        closure = ClassicalSemanticClosureGovernanceRow(
            closure_requirement_id="CLASSICAL_REVERSAL_OR_REAPPEARANCE_SEMANTICS",
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
            final_candidate_id="CONTROLLED-UNIT10-REVERSAL-REAPPEARANCE-FINAL-CANDIDATE",
            source_claim_edge_class="SOURCE_ASSERTED_REVERSAL_OR_REAPPEARANCE",
            source_assertion_class="REVERSAL_OR_REAPPEARANCE_ASSERTION",
            effect_facet="RELATION_EFFECT_DISPOSITION",
            semantic_candidate_kind="SOURCE_GROUNDED_REVERSAL_OR_REAPPEARANCE_CANDIDATE",
            mechanism_proposal_kind="REVERSAL_OR_REAPPEARANCE_MECHANISM_PROPOSAL",
            unresolved_classical_semantic_requirements=(
                "CLASSICAL_REVERSAL_OR_REAPPEARANCE_SEMANTICS",
            ),
            closure_governance_rows=(closure,),
            multiplicity_references=(),
            allocation_domain_observations=(),
        )

    def test_release_contract_is_exact_and_closed(self):
        report = validate_release_contract(ROOT)
        self.assertEqual("PASS", report["status"])
        self.assertEqual(
            "SOURCE_GROUNDED_REVERSAL_OR_REAPPEARANCE_CANDIDATE",
            report["handled_semantic_candidate_kind"],
        )
        self.assertEqual(
            "536d41bb4251bec0f9dec10d80b39985eed72f2745dad31862399855f9c0a6fe",
            report["contract_semantics_sha256"],
        )
        contract = json.loads(
            (
                ROOT
                / "audits/bazi-classical-reversal-reappearance-effect-disposition-r1/contract.json"
            ).read_text(encoding="utf-8")
        )
        schema = json.loads(
            (
                ROOT
                / "schemas/bazi-classical-reversal-reappearance-effect-disposition-r1.schema.json"
            ).read_text(encoding="utf-8")
        )
        validator = Draft202012Validator(schema)
        validator.validate(contract)
        changed = copy.deepcopy(contract)
        changed["local_reversal_reappearance_closure_contract"][
            "interaction_chain_execution_released"
        ] = True
        self.assertTrue(list(validator.iter_errors(changed)))
        changed = copy.deepcopy(contract)
        changed["hard_exclusions"].remove(
            "SOURCE_ASSERTION_REVERSAL_VS_REAPPEARANCE_SUBTYPE_INFERENCE"
        )
        self.assertTrue(list(validator.iter_errors(changed)))

    def test_reversal_candidate_projects_one_combined_candidate_local_disposition(self):
        projection = expected_candidate_projection(self.reversal_candidate, self.profile)
        self.assertEqual(
            "REVERSAL_REAPPEARANCE_EFFECT_DISPOSITION_PROJECTED",
            projection.projection_status,
        )
        self.assertEqual(self.reversal_candidate, projection.source_final_candidate)
        self.assertEqual(1, len(projection.reversal_reappearance_closure_rows))
        local = projection.reversal_reappearance_closure_rows[0]
        self.assertEqual(
            "CLASSICAL_REVERSAL_OR_REAPPEARANCE_SEMANTICS",
            local.closure_requirement_id,
        )
        self.assertEqual("MISSING_PRIMITIVE", local.upstream_runtime_dependency_status)
        self.assertEqual(
            "AVAILABLE_EXACTLY_AS_CANDIDATE_LOCAL_SOURCE_ASSERTED_REVERSAL_OR_REAPPEARANCE_EFFECT_DISPOSITION",
            local.unit10_local_closure_result,
        )
        self.assertEqual(1, len(projection.reversal_reappearance_effect_dispositions))
        disposition = projection.reversal_reappearance_effect_dispositions[0]
        self.assertEqual(
            "SOURCE_ASSERTED_REVERSAL_OR_REAPPEARANCE_EFFECT_DISPOSITION",
            disposition.disposition_kind,
        )
        self.assertEqual(
            "SOURCE_ASSERTED_REVERSAL_OR_REAPPEARANCE_OF_TARGET_EFFECT_CHANNEL",
            disposition.source_asserted_disposition,
        )
        self.assertEqual(
            "NOT_RELEASED_SOURCE_CLASS_REMAINS_COMBINED",
            disposition.source_assertion_subtype_split,
        )
        self.assertEqual("NO_MUTATION", disposition.raw_relation_action)
        self.assertEqual("UNCHANGED", disposition.raw_relation_presence_semantics)

    def test_non_reversal_candidates_emit_zero_unit10_dispositions(self):
        variants = (
            ("SOURCE_GROUNDED_RESOLUTION_CANDIDATE", "RESOLUTION_MECHANISM_PROPOSAL", "SOURCE_ASSERTED_RESOLUTION", "RELATION_EFFECT_DISPOSITION"),
            ("SOURCE_GROUNDED_RESOLUTION_FAILURE_CANDIDATE", "RESOLUTION_FAILURE_MECHANISM_PROPOSAL", "SOURCE_ASSERTED_RESOLUTION_FAILURE", "RELATION_EFFECT_DISPOSITION"),
            ("SOURCE_GROUNDED_ATTENUATION_CANDIDATE", "ATTENUATION_MECHANISM_PROPOSAL", "SOURCE_ASSERTED_ATTENUATION", "RELATION_EFFECT_GRADE"),
            ("SOURCE_GROUNDED_PARTICIPANT_ALLOCATION_CANDIDATE", "PARTICIPANT_ALLOCATION_MECHANISM_PROPOSAL", "SOURCE_ASSERTED_PARTICIPANT_ALLOCATION", "RELATION_PARTICIPANT_ALLOCATION"),
        )
        for semantic_kind, mechanism_kind, claim_class, facet in variants:
            candidate = replace(
                self.reversal_candidate,
                final_candidate_id=f"CONTROLLED:{semantic_kind}",
                semantic_candidate_kind=semantic_kind,
                mechanism_proposal_kind=mechanism_kind,
                source_claim_edge_class=claim_class,
                effect_facet=facet,
            )
            projection = expected_candidate_projection(candidate, self.profile)
            self.assertEqual(
                "PRESERVED_NON_REVERSAL_REAPPEARANCE_CANDIDATE",
                projection.projection_status,
            )
            self.assertEqual((), projection.reversal_reappearance_closure_rows)
            self.assertEqual((), projection.reversal_reappearance_effect_dispositions)

    def test_same_channel_candidates_remain_separate_and_unranked(self):
        first = expected_candidate_projection(self.reversal_candidate, self.profile)
        second_candidate = replace(
            self.reversal_candidate,
            final_candidate_id="CONTROLLED-UNIT10-REVERSAL-REAPPEARANCE-SECOND",
            source_claim_edge_id=f"{self.reversal_candidate.source_claim_edge_id}:SECOND",
        )
        second = expected_candidate_projection(second_candidate, self.profile)
        effect_index, _, closure_index = build_expected_indexes((first, second))
        self.assertEqual(1, len(effect_index))
        self.assertEqual(
            (first.candidate_projection_id, second.candidate_projection_id),
            effect_index[0].candidate_projection_ids,
        )
        self.assertEqual(
            "IDENTITY_ONLY_NO_MERGE_RANK_ARBITRATION_SELECTION_OR_GLOBAL_STATE",
            effect_index[0].index_semantics,
        )
        self.assertEqual(2, len(effect_index[0].reversal_reappearance_effect_disposition_ids))
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
        self.assertEqual((), projected.reversal_reappearance_effect_disposition_ids)

    def test_real_stack_replays_unit7_without_executing_sibling_or_chain_state(self):
        for request, result in (self.cross, self.multiplicity):
            self.assertEqual(
                len(request.source_final_effect_resolution.candidates),
                len(result.candidates),
            )
            for source_outer, projected_outer in zip(
                request.source_final_effect_resolution.candidates,
                result.candidates,
                strict=True,
            ):
                self.assertEqual(
                    source_outer.final_effect_envelope_id,
                    projected_outer.source_final_effect_envelope_id,
                )
                self.assertEqual(
                    len(source_outer.fragment_envelopes),
                    len(projected_outer.fragment_projections),
                )
                self.assertEqual(
                    "NOT_RELEASED_SOURCE_CLASS_REMAINS_COMBINED",
                    projected_outer.source_assertion_subtype_split,
                )
                self.assertEqual("NOT_RELEASED", projected_outer.global_target_relation_restored_state_semantics)
                self.assertEqual("NOT_RELEASED", projected_outer.global_target_relation_active_in_force_state_semantics)
                self.assertEqual("NOT_RELEASED", projected_outer.prior_resolution_execution_semantics)
                self.assertEqual("NOT_RELEASED", projected_outer.prior_resolution_failure_execution_semantics)
                self.assertEqual("NOT_RELEASED", projected_outer.interaction_chain_execution_semantics)
                self.assertEqual("NOT_RELEASED", projected_outer.candidate_global_truth_semantics)
                self.assertEqual("NOT_RELEASED", projected_outer.execution_readiness_semantics)
                self.assertEqual("NOT_RELEASED", projected_outer.final_classical_verdict_semantics)

    def test_runtime_schema_rejects_global_state_and_subtype_injection(self):
        payload = BaziClassicalReversalReappearanceEffectDispositionEngine().resolve(
            self.cross[0]
        )
        schema = json.loads(
            (
                ROOT
                / "schemas/bazi-classical-reversal-reappearance-effect-disposition-runtime-r1.schema.json"
            ).read_text(encoding="utf-8")
        )
        validator = Draft202012Validator(schema)
        validator.validate(payload)
        forbidden = [
            "restored", "reactivated", "active", "in_force", "global_reappeared",
            "reversal_subtype", "reappearance_subtype", "truth", "operative",
            "applicable", "ready_for_execution", "selected_candidate",
            "selected_participant_id", "selected_path", "winner", "loser",
            "priority", "precedence", "conflict_result", "relation_state",
            "global_effect_state", "rewrite_result", "activated", "suppressed",
            "released", "cancelled", "overridden", "fixpoint", "final_verdict",
            "final_classical_verdict",
        ]
        for field in forbidden:
            changed = copy.deepcopy(payload)
            changed["candidates"][0][field] = True
            self.assertTrue(list(validator.iter_errors(changed)), field)

        projection = expected_candidate_projection(self.reversal_candidate, self.profile)
        projection_payload = json_value(projection)
        projection_validator = validator.evolve(
            schema=schema["$defs"]["candidateProjection"]
        )
        projection_validator.validate(projection_payload)
        for field in forbidden:
            changed = copy.deepcopy(projection_payload)
            changed["source_final_candidate"][field] = True
            self.assertTrue(list(projection_validator.iter_errors(changed)), field)


if __name__ == "__main__":
    unittest.main()
