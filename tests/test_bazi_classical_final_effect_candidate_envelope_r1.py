from __future__ import annotations

import copy
import json
import unittest
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

from jsonschema import Draft202012Validator

from fortune_training.bazi_classical_effect_semantic_candidate.models import (
    ClassicalFragmentSemanticCandidateProjection,
)
from fortune_training.bazi_classical_final_effect_candidate_envelope import (
    BaziClassicalFinalEffectCandidateEnvelopeEngine,
    BaziClassicalFinalEffectCandidateEnvelopeRequest,
    build_expected_indexes,
    bazi_classical_final_effect_candidate_envelope_r1_profile,
    validate_release_contract,
)
from fortune_training.bazi_classical_final_effect_candidate_envelope.engine import (
    _project_fragment,
)
from fortune_training.bazi_classical_non_selecting_participant_allocation.models import (
    FragmentAllocationElaborationProjection,
)
from fortune_training.calendar_foundation.models import json_value
import test_bazi_classical_non_selecting_participant_allocation_integrity_r1 as unit6_integrity_tests
import test_bazi_classical_non_selecting_participant_allocation_r1 as unit6_tests

ROOT = Path(__file__).resolve().parents[1]


class BaziClassicalFinalEffectCandidateEnvelopeR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        unit6_tests.BaziClassicalNonSelectingParticipantAllocationR1Tests.setUpClass()
        cls.profile = bazi_classical_final_effect_candidate_envelope_r1_profile()
        cls.cross = cls._unit7(
            unit6_tests.BaziClassicalNonSelectingParticipantAllocationR1Tests.cross
        )
        cls.multiplicity = cls._unit7(
            unit6_tests.BaziClassicalNonSelectingParticipantAllocationR1Tests.multiplicity
        )
        cls.controlled = cls._controlled_candidate_fixture()
        cls.controlled_fragment = cls.controlled.final_fragment

    @classmethod
    def _unit7(cls, stack):
        effect, admission, semantic, mechanism, _, allocation = stack
        request = BaziClassicalFinalEffectCandidateEnvelopeRequest(
            effect, admission, semantic, mechanism, allocation, cls.profile
        )
        result = BaziClassicalFinalEffectCandidateEnvelopeEngine().resolve_typed(request)
        if result.status == "FAILED":
            raise AssertionError(result.diagnostics)
        return effect, admission, semantic, mechanism, allocation, request, result

    @classmethod
    def _controlled_candidate_fixture(cls):
        helper_cls = unit6_integrity_tests.BaziClassicalNonSelectingParticipantAllocationIntegrityR1Tests
        helper_cls.setUpClass()
        helper = helper_cls(methodName="test_recomputed_hash_does_not_hide_synthetic_extra_path")
        _, unit5_fragment, candidate, proposal, elaboration, _ = helper._controlled_allocation()
        semantic_fragment = ClassicalFragmentSemanticCandidateProjection(
            fragment_semantic_projection_id=unit5_fragment.source_fragment_semantic_projection_id,
            source_admission_projection_id=candidate.source_admission_projection_id,
            source_fragment_id=candidate.source_fragment_id,
            source_fragment_fact_hash=candidate.source_fragment_fact_hash,
            source_fragment_computation_hash=candidate.source_fragment_computation_hash,
            source_occurrence_id=candidate.source_occurrence_id,
            binding_candidate_id=candidate.binding_candidate_id,
            admission_status="ADMITTED",
            admission_blocker_ids=(),
            source_semantic_profile_id=candidate.source_semantic_profile_id,
            source_semantic_partition_id=candidate.source_semantic_partition_id,
            projection_status="SEMANTIC_CANDIDATES_PROJECTED",
            semantic_candidates=(candidate,),
            source_unresolved_graph_requirements_provenance=(
                candidate.source_unresolved_graph_requirements_provenance
            ),
            unresolved_classical_semantic_requirements=(
                candidate.unresolved_classical_semantic_requirements
            ),
        )
        allocation_fragment = FragmentAllocationElaborationProjection(
            fragment_allocation_projection_id="CONTROLLED-UNIT7-ALLOCATION-FRAGMENT",
            source_fragment_governance_projection_id=unit5_fragment.fragment_governance_projection_id,
            source_fragment_semantic_projection_id=unit5_fragment.source_fragment_semantic_projection_id,
            source_fragment_id=unit5_fragment.source_fragment_id,
            source_occurrence_id=unit5_fragment.source_occurrence_id,
            binding_candidate_id=unit5_fragment.binding_candidate_id,
            source_governance_status=unit5_fragment.governance_status,
            allocation_status="ALLOCATION_DOMAIN_ELABORATION_PROJECTED",
            source_mechanism_proposal_ids=(proposal.mechanism_proposal_id,),
            proposal_elaborations=(elaboration,),
            allocation_domain_observation_ids=tuple(
                row.allocation_domain_observation_id
                for row in elaboration.allocation_domain_observations
            ),
        )
        semantic_envelope = SimpleNamespace(
            semantic_projection_envelope_id="CONTROLLED-UNIT4-ENVELOPE",
            source_admission_envelope_id="CONTROLLED-UNIT3-ADMISSION-ENVELOPE",
            source_effect_envelope_id="CONTROLLED-UNIT2-EFFECT-ENVELOPE",
            hashes=SimpleNamespace(fact_hash="0" * 64, computation_hash="1" * 64),
        )
        mechanism_envelope = SimpleNamespace(
            mechanism_closure_envelope_id="CONTROLLED-UNIT5-ENVELOPE",
            hashes=SimpleNamespace(fact_hash="2" * 64, computation_hash="3" * 64),
        )
        allocation_envelope = SimpleNamespace(
            allocation_envelope_id="CONTROLLED-UNIT6-ENVELOPE",
            hashes=SimpleNamespace(fact_hash="4" * 64, computation_hash="5" * 64),
        )
        final_fragment = _project_fragment(
            allocation_fragment,
            unit5_fragment,
            semantic_fragment,
            semantic_envelope,
            mechanism_envelope,
            allocation_envelope,
            cls.profile,
        )
        return SimpleNamespace(
            final_fragment=final_fragment,
            semantic_candidate=candidate,
            mechanism_proposal=proposal,
            allocation_elaboration=elaboration,
            semantic_envelope=semantic_envelope,
            mechanism_envelope=mechanism_envelope,
            allocation_envelope=allocation_envelope,
            semantic_fragment=semantic_fragment,
            mechanism_fragment=unit5_fragment,
            allocation_fragment=allocation_fragment,
        )

    def test_release_contract_is_exact_and_closed(self):
        report = validate_release_contract(ROOT)
        self.assertEqual("PASS", report["status"])
        self.assertEqual(5, report["semantic_candidate_kind_count"])
        self.assertEqual(
            "41cd0acc91e6fa16ee4bca8ac46e96a7eb42cfe453edde5cab75b0c35b766354",
            report["contract_semantics_sha256"],
        )
        contract = json.loads((ROOT / "audits/bazi-classical-final-effect-candidate-envelope-r1/contract.json").read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas/bazi-classical-final-effect-candidate-envelope-r1.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        validator.validate(contract)
        for path, value in (
            (("candidate_assembly_contract", "execution_readiness_inference"), "RELEASED"),
            (("preservation_contract", "participant_path_selection"), "RELEASED"),
            (("preservation_contract", "same_effect_channel_candidates"), "MERGED"),
        ):
            changed = copy.deepcopy(contract)
            changed[path[0]][path[1]] = value
            self.assertTrue(list(validator.iter_errors(changed)), path)

    def test_real_upstream_outer_and_fragment_lineage_is_preserved(self):
        for _, _, semantic, mechanism, allocation, _, result in (self.cross, self.multiplicity):
            self.assertEqual(len(allocation.candidates), len(result.candidates))
            semantic_by_id = {row.semantic_projection_envelope_id: row for row in semantic.candidates}
            mechanism_by_id = {row.mechanism_closure_envelope_id: row for row in mechanism.candidates}
            for allocation_outer, final_outer in zip(allocation.candidates, result.candidates, strict=True):
                self.assertEqual(allocation_outer.allocation_envelope_id, final_outer.source_allocation_envelope_id)
                self.assertEqual(len(allocation_outer.fragment_allocation_projections), len(final_outer.fragment_envelopes))
                semantic_outer = semantic_by_id[final_outer.source_semantic_projection_envelope_id]
                mechanism_outer = mechanism_by_id[final_outer.source_mechanism_closure_envelope_id]
                semantic_fragments = {row.fragment_semantic_projection_id: row for row in semantic_outer.fragment_projections}
                mechanism_fragments = {row.fragment_governance_projection_id: row for row in mechanism_outer.fragment_governance_projections}
                for allocation_fragment, final_fragment in zip(allocation_outer.fragment_allocation_projections, final_outer.fragment_envelopes, strict=True):
                    semantic_fragment = semantic_fragments[final_fragment.source_fragment_semantic_projection_id]
                    mechanism_fragment = mechanism_fragments[final_fragment.source_fragment_governance_projection_id]
                    self.assertEqual(tuple(row.semantic_candidate_id for row in semantic_fragment.semantic_candidates), final_fragment.source_semantic_candidate_ids)
                    self.assertEqual(tuple(row.mechanism_proposal_id for row in mechanism_fragment.mechanism_proposals), final_fragment.source_mechanism_proposal_ids)
                    self.assertEqual(tuple(row.proposal_allocation_elaboration_id for row in allocation_fragment.proposal_elaborations), final_fragment.source_allocation_elaboration_ids)

    def test_controlled_candidate_chain_is_exact_one_to_one_pass_through(self):
        fragment = self.controlled_fragment
        self.assertEqual("FINAL_EFFECT_CANDIDATES_ASSEMBLED", fragment.final_fragment_status)
        self.assertEqual(1, len(fragment.final_candidates))
        candidate = fragment.final_candidates[0]
        self.assertEqual(fragment.source_semantic_candidate_ids, (candidate.source_semantic_candidate_id,))
        self.assertEqual(fragment.source_mechanism_proposal_ids, (candidate.source_mechanism_proposal_id,))
        self.assertEqual(fragment.source_allocation_elaboration_ids, (candidate.source_allocation_elaboration_id,))
        self.assertEqual("SOURCE_GROUNDED_PARTICIPANT_ALLOCATION_CANDIDATE", candidate.semantic_candidate_kind)
        self.assertEqual("PARTICIPANT_ALLOCATION_MECHANISM_PROPOSAL", candidate.mechanism_proposal_kind)
        self.assertEqual(1, len(candidate.multiplicity_references))
        self.assertEqual(1, len(candidate.allocation_domain_observations))
        observation = candidate.allocation_domain_observations[0]
        self.assertEqual("EXACT_INSTANCE_SET_CARDINALITY_MATCH", observation.allocation_domain_classification)
        self.assertEqual(1, len(observation.path_candidates))
        self.assertEqual("NOT_RELEASED", observation.path_candidates[0].selection_semantics)

    def test_zero_candidate_fragments_remain_zero_candidate_fragments(self):
        found = False
        for stack in (self.cross, self.multiplicity):
            for outer in stack[-1].candidates:
                for fragment in outer.fragment_envelopes:
                    if fragment.source_semantic_candidate_ids:
                        continue
                    found = True
                    self.assertEqual("PRESERVED_ZERO_FINAL_EFFECT_CANDIDATES", fragment.final_fragment_status)
                    self.assertEqual((), fragment.final_candidates)
                    self.assertEqual((), fragment.final_candidate_ids)
                    self.assertEqual((), fragment.source_mechanism_proposal_ids)
                    self.assertEqual((), fragment.source_allocation_elaboration_ids)
        self.assertTrue(found)

    def test_outer_semantics_remain_pre_resolver_only(self):
        for stack in (self.cross, self.multiplicity):
            for outer in stack[-1].candidates:
                self.assertEqual("SOURCE_GROUNDED_PRE_RESOLVER_ENVELOPE_ASSEMBLY_ONLY", outer.final_candidate_semantics)
                self.assertEqual("NOT_RELEASED", outer.candidate_truth_semantics)
                self.assertEqual("NOT_RELEASED", outer.candidate_operability_semantics)
                self.assertEqual("NOT_RELEASED_BEYOND_UNIT3_ADMISSION", outer.candidate_applicability_semantics)
                self.assertEqual("NOT_RELEASED", outer.mechanism_execution_semantics)
                self.assertEqual("NOT_RELEASED", outer.execution_readiness_semantics)
                self.assertEqual("NOT_RELEASED", outer.participant_path_selection_semantics)
                self.assertEqual("NOT_RELEASED", outer.precedence_semantics)
                self.assertEqual("NOT_RELEASED", outer.priority_semantics)
                self.assertEqual("NOT_RELEASED", outer.winner_loser_semantics)
                self.assertEqual("NOT_RELEASED", outer.relation_effect_state_semantics)
                self.assertEqual("NOT_RELEASED", outer.rewrite_application_semantics)
                self.assertEqual("FORBIDDEN", outer.synthetic_permutation_generation)
                self.assertEqual("FORBIDDEN", outer.synthetic_combination_generation)
                self.assertEqual("FORBIDDEN", outer.inferred_slot_instance_compatibility)
                for field in ("truth", "operative", "ready_for_execution", "selected_candidate", "selected_participant_id", "selected_path", "winner", "loser", "priority", "precedence", "relation_state", "effect_state", "rewrite_result", "final_classical_verdict"):
                    self.assertFalse(hasattr(outer, field), field)

    def test_same_effect_channel_index_preserves_separate_unranked_candidates(self):
        candidate = self.controlled_fragment.final_candidates[0]
        other = replace(candidate, final_candidate_id=f"{candidate.final_candidate_id}:SECOND")
        effect_index, semantic_index, mechanism_index, _, _ = build_expected_indexes((candidate, other))
        row = effect_index[0]
        self.assertEqual((candidate.final_candidate_id, other.final_candidate_id), row.final_candidate_ids)
        self.assertEqual("IDENTITY_ONLY_NO_MERGE_RANK_ARBITRATION_OR_SELECTION", row.index_semantics)
        self.assertTrue(any(len(row.final_candidate_ids) == 2 for row in semantic_index))
        self.assertTrue(any(len(row.final_candidate_ids) == 2 for row in mechanism_index))

    def test_record_specific_005_002_lock_remains_non_selecting(self):
        contract = json.loads((ROOT / "audits/bazi-classical-final-effect-candidate-envelope-r1/contract.json").read_text(encoding="utf-8"))
        lock = contract["record_specific_locks"]["ZPZQ-CL-09-005-002"]
        self.assertEqual(["SOURCE_GROUNDED_REVERSAL_OR_REAPPEARANCE_CANDIDATE", "SOURCE_GROUNDED_RESOLUTION_CANDIDATE", "SOURCE_GROUNDED_PARTICIPANT_ALLOCATION_CANDIDATE"], lock["semantic_candidates"])
        self.assertEqual("MISSING_PRIMITIVE", lock["allocation_closure_status"])
        self.assertEqual("PARTIALLY_AVAILABLE", lock["compatible_path_enumeration_status"])
        self.assertEqual("NOT_RELEASED", lock["participant_path_selection"])
        self.assertEqual("FORBIDDEN", lock["synthetic_path_generation"])

    def test_runtime_schema_is_closed_against_resolver_surface(self):
        payload = BaziClassicalFinalEffectCandidateEnvelopeEngine().resolve(self.cross[-2])
        schema = json.loads((ROOT / "schemas/bazi-classical-final-effect-candidate-envelope-runtime-r1.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        validator.validate(payload)
        forbidden = ["truth", "operative", "applicable", "ready_for_execution", "selected_candidate", "selected_participant_id", "selected_path", "slot_assignment", "path_order", "winner", "loser", "priority", "precedence", "conflict_result", "relation_state", "effect_state", "rewrite_result", "activated", "suppressed", "released", "cancelled", "overridden", "fixpoint", "final_verdict", "final_classical_verdict"]
        for field in forbidden:
            changed = copy.deepcopy(payload)
            changed["candidates"][0][field] = True
            self.assertTrue(list(validator.iter_errors(changed)), field)
        candidate_validator = validator.evolve(schema=schema["$defs"]["finalCandidate"])
        candidate_payload = json_value(self.controlled_fragment.final_candidates[0])
        candidate_validator.validate(candidate_payload)
        for field in forbidden:
            changed = copy.deepcopy(candidate_payload)
            changed[field] = True
            self.assertTrue(list(candidate_validator.iter_errors(changed)), field)


if __name__ == "__main__":
    unittest.main()
