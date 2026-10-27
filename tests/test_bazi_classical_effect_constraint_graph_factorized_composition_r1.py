from __future__ import annotations

import copy
import json
import unittest
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
from fortune_training.bazi_chart_bound_classical_interaction_projection import (
    BaziChartBoundClassicalInteractionProjectionEngine,
    BaziChartBoundClassicalInteractionProjectionRequest,
    bazi_chart_bound_classical_interaction_projection_foundation_r1_profile,
)
from fortune_training.bazi_chart_source_pattern_binding import (
    BaziChartSourcePatternBindingEngine,
    BaziChartSourcePatternBindingRequest,
    bazi_chart_specific_exact_source_pattern_binding_candidates_r1_profile,
)
from fortune_training.bazi_classical_effect_constraint_graph import (
    BaziClassicalEffectConstraintGraphEngine,
    BaziClassicalEffectConstraintGraphRequest,
    bazi_classical_effect_constraint_graph_factorized_composition_r1_profile,
    validate_release_contract,
)
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


ROOT = Path(__file__).resolve().parents[1]


class BaziClassicalEffectConstraintGraphFactorizedCompositionR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph = json.loads((ROOT / "audits/bazi-structured-source-interaction-pattern-graph-r1/graph.json").read_text(encoding="utf-8"))
        cls.matrix = json.loads((ROOT / "audits/bazi-classical-relation-interaction-assertion-matrix-r1/matrix.json").read_text(encoding="utf-8"))
        cls.fixture = json.loads((ROOT / "tests/fixtures/bazi-chart-specific-exact-source-pattern-binding-candidates-r1.json").read_text(encoding="utf-8"))
        cls.binding_profile = bazi_chart_specific_exact_source_pattern_binding_candidates_r1_profile()
        cls.projection_profile = bazi_chart_bound_classical_interaction_projection_foundation_r1_profile()
        cls.effect_profile = bazi_classical_effect_constraint_graph_factorized_composition_r1_profile()
        cls.chart_engine = BaziChartFoundation.from_repository(ROOT)
        cls.chart_profile = bazi_foundation_v1_profile(cls.chart_engine.time_calendar.policy_registry)
        scenarios = cls.fixture["scenarios"]
        cls.cross_layer = cls._stack(
            datetime.fromisoformat(scenarios["cross_layer_mao_you_mao_xu"]["reported_local_datetime"]),
            datetime.fromisoformat(scenarios["cross_layer_mao_you_mao_xu"]["target_utc"]),
        )
        cls.multiplicity = cls._stack(
            datetime.fromisoformat(scenarios["two_mao_exchangeability"]["reported_local_datetime"]),
            datetime.fromisoformat(scenarios["two_mao_exchangeability"]["target_utc"]),
        )

    @classmethod
    def _stack(cls, reported: datetime, target: datetime):
        natal = cls.chart_engine.resolve_typed(BaziChartRequest(
            BirthInput(
                reported_local_datetime=reported,
                birth_place="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone_id="Asia/Shanghai",
                uncertainty_seconds=0,
            ),
            cls.chart_profile,
        )).candidates[0]
        temporal = BaziTemporalEngine().resolve_typed(BaziTemporalRequest(
            natal, BaziSex.MALE, bazi_temporal_v1_continuous_profile(), dayun_count=10
        ))
        flow = BaziFlowEngine(cls.chart_engine.time_calendar.bazi).resolve_typed(BaziFlowRequest(
            natal, temporal.candidates, target, cls.chart_profile
        ))
        structural = BaziStructuralEngine().resolve_typed(BaziStructuralRequest(
            natal, flow.candidates, bazi_structural_context_r1_profile()
        ))
        support = BaziStructuralSupportEngine().resolve_typed(BaziStructuralSupportRequest(
            natal, flow.candidates, structural.candidates, bazi_structural_support_foundation_r1_profile()
        ))
        incidence = BaziRelationIncidenceEngine().resolve_typed(BaziRelationIncidenceRequest(
            natal, target, flow.candidates, structural.candidates, support.candidates,
            bazi_relation_incidence_foundation_r1_profile(),
        ))
        branch = BaziBranchRelationPositionalEngine().resolve_typed(BaziBranchRelationPositionalRequest(
            natal, structural.candidates, incidence.candidates,
            bazi_branch_relation_positional_context_foundation_r1_profile(),
        ))
        stem = BaziStemRelationPositionalEngine().resolve_typed(BaziStemRelationPositionalRequest(
            natal, structural.candidates, incidence.candidates,
            bazi_stem_relation_positional_context_foundation_r1_profile(),
        ))
        binding = BaziChartSourcePatternBindingEngine().resolve_typed(BaziChartSourcePatternBindingRequest(
            natal, incidence.candidates, branch.candidates, stem.candidates, cls.graph, cls.binding_profile
        ))
        if binding.status == "FAILED":
            raise AssertionError(binding.diagnostics)
        projection = BaziChartBoundClassicalInteractionProjectionEngine().resolve_typed(
            BaziChartBoundClassicalInteractionProjectionRequest(
                binding, incidence.candidates, cls.graph, cls.matrix, cls.projection_profile
            )
        )
        if projection.status == "FAILED":
            raise AssertionError(projection.diagnostics)
        effect_request = BaziClassicalEffectConstraintGraphRequest(
            projection, binding, cls.graph, cls.effect_profile
        )
        effect = BaziClassicalEffectConstraintGraphEngine().resolve_typed(effect_request)
        if effect.status == "FAILED":
            raise AssertionError(effect.diagnostics)
        return binding, projection, effect_request, effect

    def test_release_contract_is_closed_and_deterministic(self):
        report = validate_release_contract(ROOT)
        self.assertEqual("PASS", report["status"])
        self.assertEqual(13, report["exact_source_record_count"])
        self.assertEqual(19, report["projected_claim_template_count"])
        self.assertEqual(3, report["source_narrative_chain_count"])
        self.assertEqual("0c6dfccb89710c57f96a762406df32a70395b8fef2bb15ab6654445a22108950", report["contract_semantics_sha256"])

    def test_one_projection_bundle_maps_to_one_fragment_and_one_claim_to_one_constraint(self):
        _, projection, _, effect = self.cross_layer
        for projection_outer, envelope in zip(projection.candidates, effect.candidates, strict=True):
            self.assertEqual(len(projection_outer.bundles), len(envelope.fragments))
            self.assertEqual(
                [row.binding_candidate_id for row in projection_outer.bundles],
                [row.binding_candidate_id for row in envelope.fragments],
            )
            for bundle, fragment in zip(projection_outer.bundles, envelope.fragments, strict=True):
                self.assertEqual(
                    [row.source_claim_edge_id for row in bundle.chart_bound_claims],
                    [row.constraint.source_claim_edge_id for row in fragment.effect_constraint_nodes],
                )
                self.assertEqual(len(bundle.chart_bound_claims), len(fragment.effect_constraint_nodes))

    def test_cross_layer_scope_is_preserved_without_pruning_or_resolution(self):
        _, projection, _, effect = self.cross_layer
        projection_bundles = [
            row for row in projection.candidates[0].bundles
            if row.source_occurrence_id == "ZPZQ-CL-09-003-002"
        ]
        fragments = [
            row for row in effect.candidates[0].fragments
            if row.source_occurrence_id == "ZPZQ-CL-09-003-002"
        ]
        self.assertTrue(fragments)
        self.assertEqual(len(projection_bundles), len(fragments))
        self.assertTrue(all(row.source_scope_compatibility == "CROSS_LAYER_EXTENSION_UNRESOLVED" for row in fragments))
        self.assertTrue(all(row.structural_binding_class in {"FULL_EXACT_BINDING_ENUMERATION", "PARTIAL_EXACT_BINDING_ENUMERATION"} for row in fragments))

    def test_005_002_multiplicity_and_narrative_adjacency_are_preserved_without_selection(self):
        binding, projection, _, effect = self.multiplicity
        source_inventory = next(
            row for row in binding.candidates[0].graph_binding_inventory
            if row.source_occurrence_id == "ZPZQ-CL-09-005-002"
        )
        fragments = [
            row for row in effect.candidates[0].fragments
            if row.source_occurrence_id == "ZPZQ-CL-09-005-002"
        ]
        projection_bundles = [
            row for row in projection.candidates[0].bundles
            if row.source_occurrence_id == "ZPZQ-CL-09-005-002"
        ]
        self.assertEqual(len(source_inventory.binding_candidates), len(projection_bundles))
        self.assertEqual(len(projection_bundles), len(fragments))
        self.assertGreaterEqual(len(fragments), 2)
        for fragment in fragments:
            constraints = [row.constraint for row in fragment.effect_constraint_nodes]
            self.assertEqual(
                ["SOURCE_ASSERTED_RESOLUTION", "SOURCE_ASSERTED_PARTICIPANT_ALLOCATION", "SOURCE_ASSERTED_REVERSAL_OR_REAPPEARANCE"],
                [row.source_claim_edge_class for row in constraints],
            )
            self.assertEqual(
                ["RELATION_EFFECT_DISPOSITION", "RELATION_PARTICIPANT_ALLOCATION", "RELATION_EFFECT_DISPOSITION"],
                [row.effect_facet for row in constraints],
            )
            allocation = constraints[1]
            self.assertEqual(1, len(allocation.multiplicity_references))
            multiplicity = allocation.multiplicity_references[0]
            self.assertEqual(2, multiplicity.required_symbolic_cardinality)
            self.assertEqual(2, len(set(multiplicity.exact_runtime_instance_ids)))
            self.assertEqual("PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS", multiplicity.alternative_path_requirement)
            self.assertEqual((), constraints[0].multiplicity_references)
            self.assertEqual((), constraints[2].multiplicity_references)
            narrative = [row for row in fragment.graph_edges if row.edge_kind == "SOURCE_NARRATIVE_PRECEDES"]
            self.assertEqual(2, len(narrative))
            node_by_claim = {row.constraint.source_claim_edge_id: row.constraint_node_id for row in fragment.effect_constraint_nodes}
            claim_ids = [row.source_claim_edge_id for row in constraints]
            self.assertEqual(node_by_claim[claim_ids[0]], narrative[0].source_node_id)
            self.assertEqual(node_by_claim[claim_ids[1]], narrative[0].target_node_id)
            self.assertEqual(node_by_claim[claim_ids[1]], narrative[1].source_node_id)
            self.assertEqual(node_by_claim[claim_ids[2]], narrative[1].target_node_id)
            self.assertFalse(any(
                row.source_node_id == node_by_claim[claim_ids[0]] and row.target_node_id == node_by_claim[claim_ids[2]]
                for row in narrative
            ))

    def test_007_chains_are_source_narrative_only_and_009_004_is_grade_only(self):
        chains = {
            row["source_occurrence_id"]: row
            for row in self.graph["interaction_chain_patterns"]
            if row["source_occurrence_id"] in {"ZPZQ-CL-09-007-002", "ZPZQ-CL-09-007-003"}
        }
        self.assertEqual({"ZPZQ-CL-09-007-002", "ZPZQ-CL-09-007-003"}, set(chains))
        for chain in chains.values():
            self.assertEqual("SOURCE_NARRATIVE_ORDER_ONLY", chain["sequence_semantics"])
            self.assertFalse(chain["runtime_state_transition_emitted"])
            self.assertFalse(chain["suppression_or_activation_emitted"])
            self.assertEqual(3, len(chain["ordered_interaction_claim_edge_ids"]))
        attenuation_claims = [
            row for row in self.graph["interaction_claim_edges"]
            if row["source_occurrence_id"] == "ZPZQ-CL-09-009-004"
        ]
        self.assertEqual(1, len(attenuation_claims))
        self.assertEqual("SOURCE_ASSERTED_ATTENUATION", attenuation_claims[0]["edge_class"])
        contract = json.loads((ROOT / "audits/bazi-classical-effect-constraint-graph-factorized-composition-r1/contract.json").read_text(encoding="utf-8"))
        self.assertEqual(
            "RELATION_EFFECT_GRADE",
            contract["closed_vocabularies"]["source_claim_to_effect_facet"]["SOURCE_ASSERTED_ATTENUATION"],
        )

    def test_composition_is_factorized_not_cartesian_and_indexes_are_identity_only(self):
        _, projection, _, effect = self.multiplicity
        for projection_outer, envelope in zip(projection.candidates, effect.candidates, strict=True):
            self.assertEqual("NOT_RELEASED", envelope.cartesian_expansion)
            self.assertEqual("NOT_RELEASED", envelope.cross_source_layer_composition)
            self.assertEqual("IMMUTABLE_EXACT_REFERENCE_ONLY", envelope.raw_relation_immutability_contract)
            self.assertEqual({"SHEN_CLASSICAL_SOURCE"}, {row.source_layer for row in envelope.source_layer_partitions})
            flattened = [
                fragment_id
                for partition in envelope.source_layer_partitions
                for record_set in partition.source_record_candidate_sets
                for fragment_id in record_set.fragment_ids
            ]
            self.assertEqual([row.fragment_id for row in envelope.fragments], flattened)
            for partition in envelope.source_layer_partitions:
                for record_set in partition.source_record_candidate_sets:
                    self.assertEqual("NOT_RELEASED", record_set.member_selection_semantics)
                    self.assertEqual("NOT_RELEASED", record_set.member_coexistence_semantics)
                    self.assertEqual("NOT_RELEASED", record_set.member_exclusivity_semantics)
            for entry in envelope.effect_channel_coordinate_index:
                self.assertEqual(len(entry.referencing_fragment_ids), len(entry.fragment_local_effect_channel_ids))
                self.assertGreaterEqual(len(entry.fragment_local_effect_channel_ids), 1)
            self.assertEqual(len(projection_outer.bundles), len(envelope.fragments))

    def test_upstream_projection_tamper_fails_closed_even_if_pass_flag_is_retained(self):
        binding, projection, request, _ = self.cross_layer
        outer = projection.candidates[0]
        bundle = outer.bundles[0]
        claim = bundle.chart_bound_claims[0]
        tampered_claim = replace(claim, exact_source_fragments=(*claim.exact_source_fragments, "TAMPERED"))
        tampered_bundle = replace(bundle, chart_bound_claims=(tampered_claim, *bundle.chart_bound_claims[1:]))
        tampered_outer = replace(outer, bundles=(tampered_bundle, *outer.bundles[1:]))
        tampered_projection = replace(projection, candidates=(tampered_outer, *projection.candidates[1:]))
        tampered_request = replace(request, source_projection_resolution=tampered_projection, source_binding_resolution=binding)
        result = BaziClassicalEffectConstraintGraphEngine().resolve_typed(tampered_request)
        self.assertEqual("FAILED", result.status)
        self.assertTrue(any("UPSTREAM_PROJECTION_HASH_REPLAY_MISMATCH" in row for row in result.diagnostics))

    def test_same_upstream_outer_cannot_be_composed_twice_or_cross_mixed(self):
        binding, projection, request, _ = self.cross_layer
        duplicate_projection = replace(
            projection,
            status="MULTI_CANDIDATE",
            candidates=(projection.candidates[0], projection.candidates[0]),
        )
        duplicate_request = replace(request, source_projection_resolution=duplicate_projection, source_binding_resolution=binding)
        result = BaziClassicalEffectConstraintGraphEngine().resolve_typed(duplicate_request)
        self.assertEqual("FAILED", result.status)
        self.assertTrue(any("UPSTREAM_OUTER_LINEAGE_COMPOSED_MORE_THAN_ONCE" in row for row in result.diagnostics))

    def test_runtime_schema_rejects_solver_state_winner_and_unreleased_edges(self):
        _, _, request, _ = self.multiplicity
        payload = BaziClassicalEffectConstraintGraphEngine().resolve(request)
        schema = json.loads((ROOT / "schemas/bazi-classical-effect-constraint-graph-factorized-composition-runtime-r1.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(payload)
        tampered = copy.deepcopy(payload)
        tampered["candidates"][0]["winner"] = "invented"
        self.assertTrue(list(Draft202012Validator(schema).iter_errors(tampered)))
        tampered_state = copy.deepcopy(payload)
        tampered_state["candidates"][0]["fragments"][0]["effect_constraint_nodes"][0]["constraint"]["relation_state"] = "RESOLVED"
        self.assertTrue(list(Draft202012Validator(schema).iter_errors(tampered_state)))
        tampered_edge = copy.deepcopy(payload)
        tampered_edge["candidates"][0]["fragments"][0]["graph_edges"][0]["edge_kind"] = "NEGATES"
        self.assertTrue(list(Draft202012Validator(schema).iter_errors(tampered_edge)))

    def test_runtime_output_contains_no_resolver_or_final_verdict_surface(self):
        _, _, request, _ = self.cross_layer
        payload = BaziClassicalEffectConstraintGraphEngine().resolve(request)
        encoded = json.dumps(payload, ensure_ascii=False).lower()
        for forbidden in (
            '"winner"', '"loser"', '"relation_state"', '"resolver_admission"',
            '"semantic_atom"', '"rewrite_rule"', '"fixpoint"', '"final_classical_verdict"',
            '"suppresses"', '"activates"', '"negates"', '"overrides"',
        ):
            self.assertNotIn(forbidden, encoded)


if __name__ == "__main__":
    unittest.main()
