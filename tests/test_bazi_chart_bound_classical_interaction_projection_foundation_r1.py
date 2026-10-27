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
from fortune_training.bazi_chart_bound_classical_interaction_projection import (
    BaziChartBoundClassicalInteractionProjectionEngine,
    BaziChartBoundClassicalInteractionProjectionRequest,
    bazi_chart_bound_classical_interaction_projection_foundation_r1_profile,
    derive_source_scope_specifications,
    validate_source_scope_artifact,
)
from fortune_training.bazi_chart_bound_classical_interaction_projection.scope import (
    CROSS_LAYER_EXTENSION_UNRESOLVED,
    DIRECT_SOURCE_RECORD_NATAL_CONTEXT,
    EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED,
    NO_R1_RUNTIME_SOURCE_SCOPE_SPECIFICATION,
    SOURCE_CONTEXT_INHERITED_NATAL_CONTEXT,
)
from fortune_training.bazi_chart_source_pattern_binding import (
    BaziChartSourcePatternBindingEngine,
    BaziChartSourcePatternBindingRequest,
    bazi_chart_specific_exact_source_pattern_binding_candidates_r1_profile,
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


class BaziChartBoundClassicalInteractionProjectionFoundationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph = json.loads((ROOT / "audits/bazi-structured-source-interaction-pattern-graph-r1/graph.json").read_text(encoding="utf-8"))
        cls.matrix = json.loads((ROOT / "audits/bazi-classical-relation-interaction-assertion-matrix-r1/matrix.json").read_text(encoding="utf-8"))
        cls.fixture = json.loads((ROOT / "tests/fixtures/bazi-chart-specific-exact-source-pattern-binding-candidates-r1.json").read_text(encoding="utf-8"))
        cls.projection_profile = bazi_chart_bound_classical_interaction_projection_foundation_r1_profile()
        cls.binding_profile = bazi_chart_specific_exact_source_pattern_binding_candidates_r1_profile()
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
        binding_request = BaziChartSourcePatternBindingRequest(
            natal, incidence.candidates, branch.candidates, stem.candidates, cls.graph, cls.binding_profile
        )
        binding = BaziChartSourcePatternBindingEngine().resolve_typed(binding_request)
        if binding.status == "FAILED":
            raise AssertionError(binding.diagnostics)
        projection_request = BaziChartBoundClassicalInteractionProjectionRequest(
            binding, incidence.candidates, cls.graph, cls.matrix, cls.projection_profile
        )
        projection = BaziChartBoundClassicalInteractionProjectionEngine().resolve_typed(projection_request)
        if projection.status == "FAILED":
            raise AssertionError(projection.diagnostics)
        return incidence.candidates, binding, projection_request, projection

    def test_release_scope_artifact_is_closed_and_deterministic(self):
        report = validate_source_scope_artifact(ROOT)
        self.assertEqual("PASS", report["status"])
        self.assertEqual(24, report["source_record_count"])
        self.assertEqual(19, report["projected_claim_template_count"])
        self.assertEqual(
            {"EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED": 13, "NO_R1_RUNTIME_SOURCE_SCOPE_SPECIFICATION": 11},
            report["scope_class_counts"],
        )

    def test_scope_matrix_is_exactly_13_natal_specs_and_11_no_r1_specs(self):
        rows = derive_source_scope_specifications(self.graph)
        self.assertEqual(24, len(rows))
        counts = Counter(row.scope_specification_status for row in rows)
        self.assertEqual(13, counts[EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED])
        self.assertEqual(11, counts[NO_R1_RUNTIME_SOURCE_SCOPE_SPECIFICATION])
        exact = [row for row in rows if row.scope_specification_status == EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED]
        self.assertTrue(all(row.source_chart_domain == "NATAL_FOUR_PILLAR" for row in exact))
        self.assertTrue(all(row.runtime_scope_subject == "ALL_BOUND_SOURCE_PARTICIPANTS" for row in exact))
        self.assertTrue(all(row.required_runtime_participant_layer == "NATAL" for row in exact))
        self.assertEqual(7, sum(row.source_scope_evidence_mode == DIRECT_SOURCE_RECORD_NATAL_CONTEXT for row in exact))
        self.assertEqual(6, sum(row.source_scope_evidence_mode == SOURCE_CONTEXT_INHERITED_NATAL_CONTEXT for row in exact))
        for row in exact:
            if row.source_scope_evidence_mode == SOURCE_CONTEXT_INHERITED_NATAL_CONTEXT:
                self.assertEqual((f"BSSIPG-R1-CTX-{row.source_occurrence_id}-01",), row.context_inheritance_edge_ids)

    def test_cross_layer_exact_binding_is_preserved_and_marked_unresolved_extension(self):
        _, binding, _, projection = self.cross_layer
        binding_outer = binding.candidates[0]
        source_inventory = next(
            row for row in binding_outer.graph_binding_inventory
            if row.source_occurrence_id == "ZPZQ-CL-09-003-002"
        )
        projected = [
            row for row in projection.candidates[0].bundles
            if row.source_occurrence_id == "ZPZQ-CL-09-003-002"
        ]
        self.assertEqual(len(source_inventory.binding_candidates), len(projected))
        self.assertEqual(
            {row.binding_candidate_id for row in source_inventory.binding_candidates},
            {row.binding_candidate_id for row in projected},
        )
        self.assertTrue(projected)
        self.assertTrue(all(
            row.source_scope_compatibility.source_scope_compatibility == CROSS_LAYER_EXTENSION_UNRESOLVED
            for row in projected
        ))
        self.assertTrue(all(row.source_scope_compatibility.cross_layer_participant_instance_ids for row in projected))

    def test_one_binding_candidate_projects_exactly_one_observation_bundle_and_one_to_one_claims(self):
        _, binding, _, projection = self.cross_layer
        source_candidates = [
            candidate
            for inventory in binding.candidates[0].graph_binding_inventory
            for candidate in inventory.binding_candidates
        ]
        bundles = projection.candidates[0].bundles
        self.assertEqual(len(source_candidates), len(bundles))
        self.assertEqual(
            [row.binding_candidate_id for row in source_candidates],
            [row.binding_candidate_id for row in bundles],
        )
        by_id = {row.binding_candidate_id: row for row in source_candidates}
        for bundle in bundles:
            source = by_id[bundle.binding_candidate_id]
            self.assertEqual(bundle.binding_candidate_id, bundle.neutral_observation_bundle.binding_candidate_id)
            self.assertEqual(
                source.source_interaction_claim_edge_ids,
                tuple(row.source_claim_edge_id for row in bundle.chart_bound_claims),
            )

    def test_topology_observations_are_only_claim_scoped_actor_target_pairs(self):
        _, _, _, projection = self.cross_layer
        graph_claim_by_id = {row["interaction_claim_edge_id"]: row for row in self.graph["interaction_claim_edges"]}
        for bundle in projection.candidates[0].bundles:
            claim_by_id = {row.source_claim_edge_id: row for row in bundle.chart_bound_claims}
            for topology in bundle.neutral_observation_bundle.relation_pair_topology_observations:
                self.assertTrue(topology.referencing_claim_edge_ids)
                observed_pair = set(topology.exact_relation_ids)
                for edge_id in topology.referencing_claim_edge_ids:
                    claim = claim_by_id[edge_id]
                    self.assertEqual(
                        observed_pair,
                        set(claim.actor_exact_relation_ids) | set(claim.target_exact_relation_ids),
                    )
                    self.assertTrue(graph_claim_by_id[edge_id]["actor_relation_pattern_node_ids"])
                    self.assertTrue(graph_claim_by_id[edge_id]["target_relation_pattern_node_ids"])

    def test_no_relation_transition_observation_or_semantic_state_is_emitted(self):
        transition_users = [
            row["source_occurrence_id"]
            for row in self.matrix["records"]
            if any(dep["primitive"] == "RELATION_TRANSITION_SET_CHANGE" for dep in row["neutral_runtime_dependency_map"])
        ]
        self.assertEqual([], transition_users)
        payload = BaziChartBoundClassicalInteractionProjectionEngine().resolve(self.cross_layer[2])
        encoded = json.dumps(payload, ensure_ascii=False)
        for forbidden in (
            "transition_observation", "winner", "suppression", "activation", "release_verdict",
            "resolver_admission", "effect_constraint", "rewrite_rule", "semantic_atom",
        ):
            self.assertNotIn(forbidden, encoded.lower())

    def test_incidence_degree_remains_raw_count_without_multiplicity_or_competition_inference(self):
        _, _, _, projection = self.multiplicity
        bundles = [row for row in projection.candidates[0].bundles if row.source_occurrence_id == "ZPZQ-CL-09-005-002"]
        self.assertTrue(bundles)
        saw_incidence = False
        for bundle in bundles:
            observations = bundle.neutral_observation_bundle
            if "RELATION_INCIDENCE_DEGREE" in observations.required_neutral_primitives:
                saw_incidence = True
                for fact in observations.participant_incidence_observations:
                    self.assertEqual(fact.relation_count, len(fact.relation_ids))
            encoded = json.dumps(BaziChartBoundClassicalInteractionProjectionEngine().resolve(self.multiplicity[2]), ensure_ascii=False)
            self.assertNotIn("competition", encoded.lower())
            self.assertNotIn("dominance", encoded.lower())
        self.assertTrue(saw_incidence)

    def test_005_002_exchangeability_and_three_source_claims_are_preserved_without_selection(self):
        _, binding, _, projection = self.multiplicity
        inventory = next(
            row for row in binding.candidates[0].graph_binding_inventory
            if row.source_occurrence_id == "ZPZQ-CL-09-005-002"
        )
        bundles = [row for row in projection.candidates[0].bundles if row.source_occurrence_id == "ZPZQ-CL-09-005-002"]
        self.assertEqual(len(inventory.binding_candidates), len(bundles))
        self.assertGreaterEqual(len(bundles), 2)
        for source_candidate, bundle in zip(inventory.binding_candidates, bundles, strict=True):
            self.assertEqual(source_candidate.binding_candidate_id, bundle.binding_candidate_id)
            self.assertEqual(3, len(bundle.chart_bound_claims))
            self.assertEqual(
                [
                    "SOURCE_ASSERTED_RESOLUTION",
                    "SOURCE_ASSERTED_PARTICIPANT_ALLOCATION",
                    "SOURCE_ASSERTED_REVERSAL_OR_REAPPEARANCE",
                ],
                [row.source_claim_edge_class for row in bundle.chart_bound_claims],
            )
            self.assertEqual(1, len(source_candidate.multiplicity_bindings))
            multiplicity = source_candidate.multiplicity_bindings[0]
            self.assertEqual(2, len(set(multiplicity.exact_runtime_instance_ids)))
            self.assertEqual("PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS", multiplicity.alternative_path_requirement)
            encoded = json.dumps([row.__dict__ for row in bundle.chart_bound_claims], ensure_ascii=False)
            self.assertNotIn("selected", encoded.lower())
            self.assertNotIn("winner", encoded.lower())
            self.assertNotIn("loser", encoded.lower())

    def test_source_unresolved_graph_requirements_are_provenance_not_projection_blockers(self):
        _, binding, _, projection = self.cross_layer
        inventory_by_source = {row.source_occurrence_id: row for row in binding.candidates[0].graph_binding_inventory}
        projected = [row for row in projection.candidates[0].bundles if row.source_occurrence_id == "ZPZQ-CL-09-003-002"]
        self.assertTrue(projected)
        upstream = inventory_by_source["ZPZQ-CL-09-003-002"].source_unresolved_graph_requirements
        self.assertIn("CLASSICAL_RESOLUTION_SEMANTICS", upstream)
        for bundle in projected:
            self.assertEqual(upstream, bundle.source_unresolved_graph_requirements)
            self.assertTrue(bundle.chart_bound_claims)
            self.assertTrue(all(row.source_unresolved_graph_requirements == upstream for row in bundle.chart_bound_claims))

    def test_upstream_binding_tamper_fails_closed(self):
        incidence, binding, request, _ = self.cross_layer
        outer = binding.candidates[0]
        inventories = list(outer.graph_binding_inventory)
        target_index = next(i for i, row in enumerate(inventories) if row.binding_candidates)
        inventories[target_index] = replace(
            inventories[target_index],
            source_unresolved_graph_requirements=(*inventories[target_index].source_unresolved_graph_requirements, "TAMPERED"),
        )
        tampered_outer = replace(outer, graph_binding_inventory=tuple(inventories))
        tampered_binding = replace(binding, candidates=(tampered_outer, *binding.candidates[1:]))
        tampered_request = replace(request, source_binding_resolution=tampered_binding, incidence_candidates=incidence)
        result = BaziChartBoundClassicalInteractionProjectionEngine().resolve_typed(tampered_request)
        self.assertEqual("FAILED", result.status)
        self.assertTrue(any("UPSTREAM_BINDING_HASH_REPLAY_MISMATCH" in row for row in result.diagnostics))

    def test_source_graph_and_matrix_tamper_fail_closed_before_projection(self):
        graph = copy.deepcopy(self.graph)
        graph["interaction_claim_edges"][0]["edge_class"] = "SOURCE_ASSERTED_ATTENUATION"
        graph_request = replace(self.cross_layer[2], source_graph=graph)
        graph_result = BaziChartBoundClassicalInteractionProjectionEngine().resolve_typed(graph_request)
        self.assertEqual("FAILED", graph_result.status)

        matrix = copy.deepcopy(self.matrix)
        matrix["records"][1]["neutral_runtime_dependency_map"] = []
        matrix_request = replace(self.cross_layer[2], assertion_matrix=matrix)
        matrix_result = BaziChartBoundClassicalInteractionProjectionEngine().resolve_typed(matrix_request)
        self.assertEqual("FAILED", matrix_result.status)

    def test_public_runtime_schema_is_closed_against_forbidden_semantics(self):
        schema = json.loads((ROOT / "schemas/bazi-chart-bound-classical-interaction-projection-runtime-r1.schema.json").read_text(encoding="utf-8"))
        payload = BaziChartBoundClassicalInteractionProjectionEngine().resolve(self.cross_layer[2])
        Draft202012Validator(schema).validate(payload)
        tampered = copy.deepcopy(payload)
        tampered["candidates"][0]["bundles"][0]["winner"] = "invented"
        self.assertTrue(list(Draft202012Validator(schema).iter_errors(tampered)))
        tampered_transition = copy.deepcopy(payload)
        tampered_transition["candidates"][0]["bundles"][0]["neutral_observation_bundle"]["relation_transition_observations"] = []
        self.assertTrue(list(Draft202012Validator(schema).iter_errors(tampered_transition)))


if __name__ == "__main__":
    unittest.main()
