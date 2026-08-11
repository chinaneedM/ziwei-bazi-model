from __future__ import annotations

import copy
import json
import unittest
from collections import Counter
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator

from fortune_training.bazi_branch_relation_positional import (
    BaziBranchRelationPositionalEngine,
    BaziBranchRelationPositionalRequest,
    bazi_branch_relation_positional_context_foundation_r1_profile,
)
from fortune_training.bazi_chart import BaziChartFoundation, BaziChartRequest, bazi_foundation_v1_profile
from fortune_training.bazi_chart_source_pattern_binding import (
    BaziChartSourcePatternBindingEngine,
    BaziChartSourcePatternBindingRequest,
    FULL_EXACT_BINDING_ENUMERATION,
    NOT_R1_EXACT_BINDABLE,
    PARTIAL_EXACT_BINDING_ENUMERATION,
    bazi_chart_specific_exact_source_pattern_binding_candidates_r1_profile,
    derive_bindability_plan,
    validate_bindability_plan_artifact,
    validate_binding_resolution_replay,
)
from fortune_training.bazi_chart_source_pattern_binding.bindability import BindingPlanError
from fortune_training.bazi_chart_source_pattern_binding.enumeration import (
    _RelationOption,
    _apply_exact_positions,
    _merge_assignments,
    _relation_options,
    _runtime_participants,
    enumerate_graph_inventory,
)
from fortune_training.bazi_chart_source_pattern_binding.models import SourceRelationExactBinding
from fortune_training.bazi_flow import BaziFlowEngine, BaziFlowRequest
from fortune_training.bazi_relation_incidence import (
    BaziRelationIncidenceEngine,
    BaziRelationIncidenceRequest,
    bazi_relation_incidence_foundation_r1_profile,
)
from fortune_training.bazi_stem_relation_positional import (
    BaziStemRelationPositionalEngine,
    BaziStemRelationPositionalRequest,
    bazi_stem_relation_positional_context_foundation_r1_profile,
)
from fortune_training.bazi_structural import BaziStructuralEngine, BaziStructuralRequest, bazi_structural_context_r1_profile
from fortune_training.bazi_structural_support import (
    BaziStructuralSupportEngine,
    BaziStructuralSupportRequest,
    bazi_structural_support_foundation_r1_profile,
)
from fortune_training.bazi_temporal import BaziSex, BaziTemporalEngine, BaziTemporalRequest, bazi_temporal_v1_continuous_profile
from fortune_training.calendar_foundation import BirthInput
from fortune_training.calendar_foundation.models import json_value


ROOT = Path(__file__).resolve().parents[1]


class BaziChartSpecificExactSourcePatternBindingCandidatesR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph = json.loads((ROOT / "audits/bazi-structured-source-interaction-pattern-graph-r1/graph.json").read_text(encoding="utf-8"))
        cls.fixture = json.loads((ROOT / "tests/fixtures/bazi-chart-specific-exact-source-pattern-binding-candidates-r1.json").read_text(encoding="utf-8"))
        cls.profile = bazi_chart_specific_exact_source_pattern_binding_candidates_r1_profile()
        cls.chart_engine = BaziChartFoundation.from_repository(ROOT)
        cls.chart_profile = bazi_foundation_v1_profile(cls.chart_engine.time_calendar.policy_registry)
        scenarios = cls.fixture["scenarios"]
        cls.exact = cls._stack(datetime.fromisoformat(scenarios["cross_layer_mao_you_mao_xu"]["reported_local_datetime"]), datetime.fromisoformat(scenarios["cross_layer_mao_you_mao_xu"]["target_utc"]))
        cls.multiplicity = cls._stack(datetime.fromisoformat(scenarios["two_mao_exchangeability"]["reported_local_datetime"]), datetime.fromisoformat(scenarios["two_mao_exchangeability"]["target_utc"]))
        cls.sanhe = cls._stack(datetime.fromisoformat(scenarios["complete_sanhe"]["reported_local_datetime"]), datetime.fromisoformat(scenarios["complete_sanhe"]["target_utc"]))

    @classmethod
    def _stack(cls, reported: datetime, target: datetime, duplicate_incidence: bool = False):
        natal = cls.chart_engine.resolve_typed(BaziChartRequest(
            BirthInput(reported_local_datetime=reported, birth_place="Beijing", latitude=39.9042, longitude=116.4074, timezone_id="Asia/Shanghai", uncertainty_seconds=0),
            cls.chart_profile,
        )).candidates[0]
        temporal = BaziTemporalEngine().resolve_typed(BaziTemporalRequest(natal, BaziSex.MALE, bazi_temporal_v1_continuous_profile(), dayun_count=10))
        flow = BaziFlowEngine(cls.chart_engine.time_calendar.bazi).resolve_typed(BaziFlowRequest(natal, temporal.candidates, target, cls.chart_profile))
        structural = BaziStructuralEngine().resolve_typed(BaziStructuralRequest(natal, flow.candidates, bazi_structural_context_r1_profile()))
        support = BaziStructuralSupportEngine().resolve_typed(BaziStructuralSupportRequest(natal, flow.candidates, structural.candidates, bazi_structural_support_foundation_r1_profile()))
        incidence = BaziRelationIncidenceEngine().resolve_typed(BaziRelationIncidenceRequest(natal, target, flow.candidates, structural.candidates, support.candidates, bazi_relation_incidence_foundation_r1_profile()))
        incidence_candidates = incidence.candidates * (2 if duplicate_incidence else 1)
        branch = BaziBranchRelationPositionalEngine().resolve_typed(BaziBranchRelationPositionalRequest(natal, structural.candidates, incidence_candidates, bazi_branch_relation_positional_context_foundation_r1_profile()))
        stem = BaziStemRelationPositionalEngine().resolve_typed(BaziStemRelationPositionalRequest(natal, structural.candidates, incidence_candidates, bazi_stem_relation_positional_context_foundation_r1_profile()))
        request = BaziChartSourcePatternBindingRequest(natal, incidence_candidates, branch.candidates, stem.candidates, cls.graph, cls.profile)
        result = BaziChartSourcePatternBindingEngine().resolve_typed(request)
        if result.status == "FAILED":
            raise AssertionError(result.diagnostics)
        return natal, incidence_candidates, branch.candidates, stem.candidates, request, result

    def test_bindability_plan_is_mechanical_and_regression_locked_11_2_11(self):
        plan = derive_bindability_plan(self.graph, self.profile)
        self.assertEqual(24, len(plan))
        self.assertEqual({FULL_EXACT_BINDING_ENUMERATION: 11, PARTIAL_EXACT_BINDING_ENUMERATION: 2, NOT_R1_EXACT_BINDABLE: 11}, Counter(row.bindability_class for row in plan))
        partial = [row.source_occurrence_id for row in plan if row.bindability_class == PARTIAL_EXACT_BINDING_ENUMERATION]
        self.assertEqual(["ZPZQ-CL-09-007-002", "ZPZQ-CL-09-007-003"], partial)
        not_bindable = {row.source_occurrence_id for row in plan if row.bindability_class == NOT_R1_EXACT_BINDABLE}
        self.assertTrue({"ZPZQ-CL-09-005-001", "QTBJ-CL-05347", "QTBJ-CL-05370"} <= not_bindable)

    def test_release_plan_schema_and_deterministic_replay_pass(self):
        report = validate_bindability_plan_artifact(ROOT)
        self.assertEqual("PASS", report["status"])
        self.assertEqual(24, report["graph_record_count"])

    def test_public_runtime_result_validates_against_closed_schema(self):
        schema = json.loads((ROOT / "schemas/bazi-chart-specific-exact-source-pattern-binding-runtime-r1.schema.json").read_text(encoding="utf-8"))
        result = BaziChartSourcePatternBindingEngine().resolve(self.exact[-2])
        Draft202012Validator(schema).validate(result)
        tampered = copy.deepcopy(result)
        tampered["candidates"][0]["graph_binding_inventory"][0]["winner"] = "invented"
        self.assertTrue(list(Draft202012Validator(schema).iter_errors(tampered)))

    def test_claim_identity_tamper_fails_graph_identity_but_claims_are_not_filters(self):
        tampered = copy.deepcopy(self.graph)
        tampered["interaction_claim_edges"][0]["edge_class"] = "SOURCE_ASSERTED_ATTENUATION"
        with self.assertRaises(BindingPlanError):
            derive_bindability_plan(tampered, self.profile)
        original_plan = derive_bindability_plan(self.graph, self.profile)
        natal, incidence, branch, stem, _, _ = self.exact
        original = enumerate_graph_inventory(self.graph, original_plan, natal, incidence[0], branch[0], stem[0])
        # Enumeration itself reads only graph record IDs and structural objects.
        changed = copy.deepcopy(self.graph)
        changed["interaction_claim_edges"][0]["edge_class"] = "SOURCE_ASSERTED_ATTENUATION"
        self.assertEqual(original, enumerate_graph_inventory(changed, original_plan, natal, incidence[0], branch[0], stem[0]))

    def test_exact_cross_layer_bindings_preserve_every_physical_path(self):
        candidate = self.exact[-1].candidates[0]
        inventory = next(row for row in candidate.graph_binding_inventory if row.source_occurrence_id == "ZPZQ-CL-09-003-002")
        self.assertEqual("EXACT_BINDING_CANDIDATES_PRESENT", inventory.inventory_status)
        self.assertEqual(self.fixture["scenarios"]["cross_layer_mao_you_mao_xu"]["expected_binding_candidate_count"], len(inventory.binding_candidates))
        harmony_fact_ids = {binding.positional_fact_id for item in inventory.binding_candidates for binding in item.relation_bindings if binding.source_relation_family == "BRANCH_SIX_HARMONY"}
        self.assertEqual(2, len(harmony_fact_ids))
        for item in inventory.binding_candidates:
            month_you = next(row for row in item.participant_bindings if row.literal_value == "酉")
            self.assertEqual(("NATAL",), month_you.participant_layers)
            self.assertEqual(("MONTH",), month_you.raw_position_tokens)
            mao = next(row for row in item.participant_bindings if row.literal_value == "卯")
            self.assertIn(mao.participant_layers[0], {"ANNUAL"})

    def test_participant_literals_alone_never_manufacture_missing_relation(self):
        natal, incidence, branches, stems, _, _ = self.exact
        branch = branches[0]
        context = replace(branch.context, branch_relation_positional_facts=tuple(row for row in branch.context.branch_relation_positional_facts if row.source_semantic_relation_id != "BRANCH.CLASH.MAO_YOU"))
        inventories = enumerate_graph_inventory(self.graph, derive_bindability_plan(self.graph, self.profile), natal, incidence[0], replace(branch, context=context), stems[0])
        target = next(row for row in inventories if row.source_occurrence_id == "ZPZQ-CL-09-003-002")
        self.assertEqual("NO_COMPATIBLE_EXACT_BINDING_ASSIGNMENT", target.inventory_status)

    def test_same_symbolic_node_must_unify_to_one_exact_instance(self):
        binding = SourceRelationExactBinding("r", "ref", "rel", "sem", "fact", "type", "family", "SYMMETRIC", 2, ("shared", "x"), ("A", "X"), ("pA", "pX"), "DIRECT_SOURCE_TEXT")
        left = _RelationOption(binding, (("shared", "A"), ("x", "X")))
        right = _RelationOption(replace(binding, relation_pattern_node_id="r2"), (("shared", "B"), ("y", "Y")))
        self.assertIsNone(_merge_assignments((left, right)))
        self.assertEqual("A", _merge_assignments((left, replace(right, assignments=(("shared", "A"), ("y", "Y")))))["shared"])

    def test_complete_sanhe_options_remain_one_arity_three_relation(self):
        natal, incidence, branches, stems, _, _ = self.sanhe
        node = next(row for row in self.graph["relation_pattern_nodes"] if row["released_neutral_semantic_relation_id"] == "BRANCH.TRINE.METAL")
        participants = {row["participant_pattern_node_id"]: row for row in self.graph["participant_pattern_nodes"]}
        options = _relation_options(node, participants, incidence[0], branches[0], stems[0], _runtime_participants(natal, branches[0], stems[0]))
        self.assertTrue(options)
        self.assertTrue(all(row.binding.source_arity == 3 and len(row.binding.runtime_participant_instance_ids) == 3 for row in options))

    def test_unresolved_source_time_is_preserved_without_hour_and_or_compilation(self):
        graph_record = next(row for row in self.graph["graph_records"] if row["source_occurrence_id"] == "ZPZQ-CL-09-007-002")
        position_map = {row["position_constraint_id"]: row for row in self.graph["position_pattern_constraints"]}
        unresolved = next(position_map[value] for value in graph_record["position_constraint_ids"] if position_map[value]["constraint_status"] == "UNRESOLVED_SOURCE_TIME_CONTEXT")
        natal, _, branches, stems, _, _ = self.exact
        runtime = _runtime_participants(natal, branches[0], stems[0])
        applied = _apply_exact_positions({}, (unresolved,), {row["participant_pattern_node_id"]: row for row in self.graph["participant_pattern_nodes"]}, natal, runtime)
        self.assertIsNotNone(applied)
        self.assertEqual("SOURCE_POSITION_CONTEXT_UNRESOLVED", applied[1][0].replay_status)
        self.assertEqual((), applied[1][0].runtime_instance_ids)

    def test_two_mao_exchangeability_keeps_distinct_instances_and_physical_paths(self):
        candidate = self.multiplicity[-1].candidates[0]
        inventory = next(row for row in candidate.graph_binding_inventory if row.source_occurrence_id == "ZPZQ-CL-09-005-002")
        self.assertEqual("EXACT_BINDING_CANDIDATES_PRESENT", inventory.inventory_status)
        self.assertGreaterEqual(len(inventory.binding_candidates), self.fixture["scenarios"]["two_mao_exchangeability"]["minimum_binding_candidate_count"])
        self.assertEqual(len(inventory.binding_candidates), len({row.normalized_assignment_signature for row in inventory.binding_candidates}))
        for item in inventory.binding_candidates:
            multiplicity = item.multiplicity_bindings[0]
            self.assertEqual(2, multiplicity.required_symbolic_cardinality)
            self.assertEqual(2, len(set(multiplicity.exact_runtime_instance_ids)))
            self.assertEqual("PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS", multiplicity.alternative_path_requirement)

    def test_complete_upstream_lineage_multiplicity_is_preserved_without_cartesian_join(self):
        duplicated = self._stack(datetime(2024, 9, 17, 12), datetime.fromisoformat("2035-10-15T00:00:00+00:00"), duplicate_incidence=True)
        candidate = duplicated[-1].candidates[0]
        self.assertEqual((0, 1), candidate.source_incidence_candidate_indices)
        broken_request = replace(duplicated[-2], branch_positional_candidates=duplicated[2] * 2)
        broken = BaziChartSourcePatternBindingEngine().resolve_typed(broken_request)
        self.assertEqual("FAILED", broken.status)
        self.assertIn("BRANCH_POSITIONAL_EXACT_JOIN_CARDINALITY_MISMATCH", broken.diagnostics[0])

    def test_fact_computation_hashes_and_complete_enumeration_replay_are_independent(self):
        request, result = self.exact[-2], self.exact[-1]
        candidate = result.candidates[0]
        self.assertNotEqual(candidate.hashes.fact_hash, candidate.hashes.computation_hash)
        self.assertTrue(validate_binding_resolution_replay(request, result))
        tampered_candidate = replace(candidate, hashes=replace(candidate.hashes, fact_hash="0" * 64))
        tampered = replace(result, candidates=(tampered_candidate,))
        self.assertFalse(validate_binding_resolution_replay(request, tampered))

    def test_public_payload_has_no_operability_resolver_or_transition_leakage(self):
        payload = json.dumps(json_value(self.exact[-1]), ensure_ascii=False)
        lowered = payload.lower()
        for forbidden in ("operable", "inoperable", "precedence", "winner", "loser", "activation", "suppression", "release_verdict", "final_outcome", "prediction", "吉凶"):
            self.assertNotIn(forbidden, lowered)
        package = ROOT / "src/fortune_training/bazi_chart_source_pattern_binding"
        source = "\n".join(path.read_text(encoding="utf-8") for path in package.glob("*.py"))
        self.assertNotIn("generate_raw_relations", source)
        self.assertNotIn("bazi_relation_transition", source)
        self.assertNotIn("bazi_five_combination_evidence_binding", source)


if __name__ == "__main__":
    unittest.main()
