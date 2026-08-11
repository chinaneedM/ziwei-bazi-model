from __future__ import annotations

import copy
import json
import unittest
from collections import Counter
from pathlib import Path

from fortune_training.bazi_classical_relation_interaction_assertion import (
    MANDATORY_SOURCE_OCCURRENCE_IDS,
    MATRIX_PATH,
)
from fortune_training.bazi_structured_source_interaction_pattern_graph import (
    AUDIT_ID,
    GRAPH_PATH,
    INHERITANCE_REGISTRY,
    REPORT_PATH,
    SCHEMA_PATH,
    UPSTREAM_CONTRACT_HASHES,
    build_structured_source_interaction_pattern_graph,
    validate_structured_source_interaction_pattern_graph,
    validate_structured_source_interaction_pattern_graph_value,
)
from fortune_training.cli import build_parser
from fortune_training.util import TrainingError, object_sha256, sha256_file
from fortune_training.verify import verify_repository


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class StructuredSourceInteractionPatternGraphR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph = json.loads((PROJECT_ROOT / GRAPH_PATH).read_text(encoding="utf-8"))
        cls.matrix = json.loads((PROJECT_ROOT / MATRIX_PATH).read_text(encoding="utf-8"))
        cls.records = {row["source_occurrence_id"]: row for row in cls.graph["graph_records"]}

    def rows(self, key: str, source_occurrence_id: str) -> list[dict]:
        return [row for row in self.graph[key] if row.get("source_occurrence_id", row.get("inheriting_source_occurrence_id")) == source_occurrence_id]

    def test_release_artifacts_validate_and_repository_verify_includes_graph(self):
        report = validate_structured_source_interaction_pattern_graph(PROJECT_ROOT)
        self.assertEqual(report["status"], "PASS")
        self.assertTrue(report["matrix_exact_replay"])
        self.assertTrue(report["upstream_hash_regression"])
        repository_report = verify_repository(PROJECT_ROOT)
        self.assertEqual(repository_report["structured_source_interaction_pattern_graph"]["audit_id"], AUDIT_ID)
        self.assertTrue((PROJECT_ROOT / SCHEMA_PATH).is_file())
        self.assertTrue((PROJECT_ROOT / REPORT_PATH).is_file())

    def test_matrix_universe_is_covered_exactly_once_in_authoritative_order(self):
        occurrence_ids = [row["source_occurrence_id"] for row in self.graph["graph_records"]]
        self.assertEqual(occurrence_ids, list(MANDATORY_SOURCE_OCCURRENCE_IDS))
        self.assertEqual(len(occurrence_ids), 24)
        self.assertEqual(Counter(occurrence_ids), Counter({value: 1 for value in occurrence_ids}))
        self.assertEqual(self.graph["summary"]["matrix_record_count"], 24)
        self.assertEqual(self.graph["summary"]["graph_record_count"], 24)

    def test_every_graph_record_exactly_replays_matrix_identity_and_source_hashes(self):
        matrix = {row["source_occurrence_id"]: row for row in self.matrix["records"]}
        for row in self.graph["graph_records"]:
            upstream = matrix[row["source_occurrence_id"]]
            self.assertEqual(row["interaction_assertion_id"], upstream["interaction_assertion_id"])
            self.assertEqual(row["matrix_record_sha256"], upstream["record_sha256"])
            self.assertEqual(row["source_text_sha256"], upstream["source_text_sha256"])
            self.assertEqual(row["source_record_sha256"], upstream["source_record_sha256"])
            self.assertEqual(row["exact_source_text"], upstream["exact_source_text"])
            self.assertEqual(row["exact_source_fragments"], upstream["source_assertion_fragments"])

    def test_contextual_general_and_summary_records_remain_covered(self):
        expected_roles = Counter(row["source_assertion_role"] for row in self.matrix["records"])
        actual_roles = Counter(row["source_assertion_role"] for row in self.graph["graph_records"])
        self.assertEqual(actual_roles, expected_roles)
        for oid in ("ZPZQ-CL-09-005-001", "ZPZQ-CL-09-007-001", "ZPZQ-CL-09-009-001"):
            self.assertEqual(self.records[oid]["graph_status"], "CONTEXTUAL_UNRESOLVED_GRAPH")
            self.assertTrue(self.records[oid]["interaction_claim_edge_ids"])
        self.assertFalse(self.records["ZPZQ-CL-09-005-001"]["relation_pattern_node_ids"])

    def test_every_claim_edge_replays_upstream_reference_kinds_and_unresolved_bindings(self):
        matrix = {row["source_occurrence_id"]: row for row in self.matrix["records"]}
        for edge in self.graph["interaction_claim_edges"]:
            with self.subTest(edge=edge["interaction_claim_edge_id"]):
                upstream = matrix[edge["source_occurrence_id"]]
                self.assertEqual(edge["actor_reference_kind"], upstream["actor_reference_kind"])
                self.assertEqual(edge["target_reference_kind"], upstream["target_reference_kind"])
                if upstream["actor_reference_kind"] == "UNRESOLVED_ACTOR":
                    self.assertFalse(edge["actor_relation_pattern_node_ids"])
                    self.assertFalse(edge["actor_participant_pattern_node_ids"])
                if upstream["target_reference_kind"] == "UNRESOLVED_TARGET":
                    self.assertFalse(edge["target_relation_pattern_node_ids"])
                    self.assertFalse(edge["target_participant_pattern_node_ids"])

        unresolved = self.rows("interaction_claim_edges", "ZPZQ-CL-09-005-001")[0]
        self.assertEqual(unresolved["actor_reference_kind"], "UNRESOLVED_ACTOR")
        self.assertEqual(unresolved["target_reference_kind"], "UNRESOLVED_TARGET")
        self.assertFalse(unresolved["context_participant_pattern_node_ids"])

    def test_003_002_preserves_month_clash_harmony_and_source_claim(self):
        positions = self.rows("position_pattern_constraints", "ZPZQ-CL-09-003-002")
        self.assertIn(("MONTH", "酉月"), {(row["natal_pillar"], row["source_fragment"]) for row in positions})
        relations = self.rows("relation_pattern_nodes", "ZPZQ-CL-09-003-002")
        self.assertEqual({row["released_neutral_semantic_relation_id"] for row in relations}, {"BRANCH.CLASH.MAO_YOU", "BRANCH.HARMONY.SIX.MAO_XU"})
        claims = self.rows("interaction_claim_edges", "ZPZQ-CL-09-003-002")
        self.assertEqual(claims[0]["edge_class"], "SOURCE_ASSERTED_RESOLUTION")
        self.assertFalse(claims[0]["raw_relation_mutation_emitted"])

    def test_003_003_target_is_inherited_with_explicit_same_block_provenance(self):
        oid = "ZPZQ-CL-09-003-003"
        inheritance = self.rows("context_inheritance_edges", oid)
        self.assertEqual(len(inheritance), 1)
        self.assertEqual(inheritance[0]["antecedent_source_occurrence_id"], "ZPZQ-CL-09-003-002")
        self.assertFalse(inheritance[0]["direct_source_lexeme_claimed"])
        inherited_relations = [row for row in self.rows("relation_pattern_nodes", oid) if row["source_evidence_mode"] == "SOURCE_CONTEXT_INHERITED"]
        self.assertEqual(len(inherited_relations), 1)
        self.assertEqual(inherited_relations[0]["released_neutral_semantic_relation_id"], "BRANCH.CLASH.MAO_YOU")
        direct_actor = [row for row in self.rows("relation_pattern_nodes", oid) if row["source_evidence_mode"] == "DIRECT_SOURCE_TEXT"]
        self.assertEqual(direct_actor[0]["released_neutral_semantic_relation_id"], "BRANCH.HARMONY.SIX.CHEN_YOU")

    def test_context_inheritance_is_closed_to_regression_locked_same_block_chains(self):
        actual = {row["inheriting_source_occurrence_id"]: row["antecedent_source_occurrence_id"] for row in self.graph["context_inheritance_edges"]}
        self.assertEqual(actual, INHERITANCE_REGISTRY)
        for edge in self.graph["context_inheritance_edges"]:
            self.assertEqual(edge["inheritance_scope"], "REGRESSION_LOCKED_SAME_SOURCE_BLOCK_EXAMPLE_CHAIN")
            self.assertEqual(edge["provenance"]["source_evidence_mode"], "SOURCE_CONTEXT_INHERITED")

    def test_complete_sanhe_patterns_always_keep_three_symbolic_participants(self):
        sanhe = [row for row in self.graph["relation_pattern_nodes"] if row["released_neutral_relation_family"] == "BRANCH_TRINE"]
        self.assertGreaterEqual(len(sanhe), 6)
        for row in sanhe:
            self.assertEqual(row["source_arity"], 3)
            self.assertEqual(row["source_orientation"], "GROUP")
            self.assertEqual(len(row["symbolic_ordered_participant_node_ids"]), 3)

    def test_005_002_preserves_two_exchangeable_mao_slots_and_all_paths(self):
        oid = "ZPZQ-CL-09-005-002"
        nodes = [row for row in self.rows("participant_pattern_nodes", oid) if row["literal_value"] == "卯"]
        self.assertEqual(len(nodes), 2)
        self.assertEqual({row["symbolic_slot_index"] for row in nodes}, {1, 2})
        self.assertEqual({row["exchangeability_status"] for row in nodes}, {"EXCHANGEABLE_SOURCE_EQUIVALENT"})
        multiplicity = self.rows("multiplicity_constraints", oid)[0]
        self.assertEqual(multiplicity["required_symbolic_cardinality"], 2)
        self.assertEqual(multiplicity["exact_slot_selection"], "NOT_SELECTED")
        self.assertEqual(multiplicity["alternative_path_requirement"], "PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS")
        self.assertFalse(multiplicity["winner_emitted"])
        for relation in self.rows("relation_pattern_nodes", oid):
            self.assertEqual(len(relation["compatible_symbolic_participant_paths"]), 2)

    def test_007_002_positions_shared_chou_sanhe_and_narrative_chain_are_static(self):
        oid = "ZPZQ-CL-09-007-002"
        nodes = {row["literal_value"]: row["participant_pattern_node_id"] for row in self.rows("participant_pattern_nodes", oid)}
        positions = self.rows("position_pattern_constraints", oid)
        exact = {(row["natal_pillar"], row["source_fragment"]) for row in positions if row["constraint_status"] == "EXACT_SYMBOLIC_PARTICIPANT_PILLAR_CONSTRAINT"}
        self.assertEqual(exact, {("YEAR", "子年"), ("MONTH", "午月"), ("DAY", "日坐丑位")})
        unresolved_hour = [row for row in positions if row["constraint_status"] == "UNRESOLVED_SOURCE_TIME_CONTEXT"]
        self.assertEqual(len(unresolved_hour), 1)
        self.assertIsNone(unresolved_hour[0]["natal_pillar"])
        self.assertEqual(set(unresolved_hour[0]["participant_pattern_node_ids"]), {nodes["巳"], nodes["酉"]})
        relations = self.rows("relation_pattern_nodes", oid)
        harmony = next(row for row in relations if row["released_neutral_relation_family"] == "BRANCH_SIX_HARMONY")
        sanhe = next(row for row in relations if row["released_neutral_relation_family"] == "BRANCH_TRINE")
        self.assertIn(nodes["丑"], harmony["symbolic_ordered_participant_node_ids"])
        self.assertIn(nodes["丑"], sanhe["symbolic_ordered_participant_node_ids"])
        chain = self.rows("interaction_chain_patterns", oid)[0]
        self.assertEqual(chain["sequence_semantics"], "SOURCE_NARRATIVE_ORDER_ONLY")
        self.assertFalse(chain["runtime_state_transition_emitted"])
        self.assertFalse(chain["suppression_or_activation_emitted"])

    def test_007_003_preserves_exact_chain_without_suppression_semantics(self):
        oid = "ZPZQ-CL-09-007-003"
        semantic_ids = {row["released_neutral_semantic_relation_id"] for row in self.rows("relation_pattern_nodes", oid)}
        self.assertEqual(semantic_ids, {"BRANCH.PUNISHMENT.ZI_MAO", "BRANCH.HARMONY.SIX.MAO_XU", "BRANCH.TRINE.FIRE"})
        edge_classes = [row["edge_class"] for row in self.rows("interaction_claim_edges", oid)]
        self.assertEqual(edge_classes, ["SOURCE_ASSERTED_RESOLUTION", "SOURCE_ASSERTED_RESOLUTION_FAILURE", "SOURCE_ASSERTED_REVERSAL_OR_REAPPEARANCE"])
        chain = self.rows("interaction_chain_patterns", oid)[0]
        self.assertFalse(chain["suppression_or_activation_emitted"])
        self.assertFalse(chain["runtime_state_transition_emitted"])

    def test_009_relation_on_relation_and_attenuation_are_preserved(self):
        resolution = self.rows("interaction_claim_edges", "ZPZQ-CL-09-009-003")[0]
        self.assertEqual(resolution["edge_class"], "SOURCE_ASSERTED_RESOLUTION")
        self.assertTrue(resolution["actor_relation_pattern_node_ids"])
        self.assertTrue(resolution["target_relation_pattern_node_ids"])
        attenuation = self.rows("interaction_claim_edges", "ZPZQ-CL-09-009-004")[0]
        self.assertEqual(attenuation["edge_class"], "SOURCE_ASSERTED_ATTENUATION")
        self.assertIn("冲之无力", attenuation["exact_source_fragments"])
        self.assertFalse(attenuation["raw_relation_mutation_emitted"])

    def test_qtbj_keeps_participant_context_actor_and_unresolved_jiehe_target(self):
        for oid in ("QTBJ-CL-05347", "QTBJ-CL-05370"):
            record = self.records[oid]
            self.assertEqual(record["graph_status"], "PARTICIPANT_MEDIATED_SOURCE_GRAPH")
            nodes = self.rows("participant_pattern_nodes", oid)
            gui = next(row for row in nodes if row["literal_value"] == "癸")
            bing = next(row for row in nodes if row["literal_value"] == "丙")
            self.assertEqual(gui["source_role"], "PARTICIPANT_OR_CONTEXT_ACTOR")
            relation = self.rows("relation_pattern_nodes", oid)[0]
            self.assertEqual(relation["source_fragment"], "解合")
            self.assertEqual(relation["pattern_resolution_status"], "UNRESOLVED_RELATION_PATTERN")
            self.assertIsNone(relation["released_neutral_relation_family"])
            self.assertIsNone(relation["released_neutral_semantic_relation_id"])
            edge = self.rows("interaction_claim_edges", oid)[0]
            self.assertIn(gui["participant_pattern_node_id"], edge["actor_participant_pattern_node_ids"])
            self.assertIn(bing["participant_pattern_node_id"], edge["target_participant_pattern_node_ids"])
            self.assertIn("QTBJ_SOURCE_CONTEXT_FORCE_OR_ROOT_SEMANTICS_UNRESOLVED", edge["unresolved_requirements"])
            self.assertTrue({"癸水通源", "癸水有力"} & set(edge["exact_source_fragments"]))
            self.assertNotIn("CONTROL", json.dumps(self.rows("relation_pattern_nodes", oid)).upper())

    def test_generic_relation_lexemes_never_broad_infer_runtime_relation(self):
        generic_oids = {"ZPZQ-CL-09-003-001", "ZPZQ-CL-09-003-006", "ZPZQ-CL-09-003-011", "ZPZQ-CL-09-007-004", "ZPZQ-CL-09-009-005"}
        for row in self.graph["relation_pattern_nodes"]:
            if row["source_occurrence_id"] in generic_oids:
                self.assertNotEqual(row["pattern_resolution_status"], "EXACT_RELEASED_RELATION_PATTERN")
                self.assertIsNone(row["released_neutral_relation_family"])
                self.assertIsNone(row["released_neutral_semantic_relation_id"])

    def test_graph_emits_no_chart_instance_binding_or_downstream_runtime_fields(self):
        payload = json.dumps(self.graph, ensure_ascii=False)
        for forbidden_key in ("instance_id", "candidate_index", "binding_verdict", '"operability"', '"precedence"', '"winner"', '"loser"', '"activation"', '"suppression"', '"release_verdict"', '"final_outcome"'):
            self.assertNotIn(forbidden_key, payload)
        self.assertTrue(all(value is False for value in self.graph["scope"].values()))

    def test_shared_symbolic_participant_is_not_competition_and_exited_is_not_resolution(self):
        payload = json.dumps(self.graph, ensure_ascii=False)
        self.assertNotIn("COMPET", payload.upper())
        self.assertNotIn('"EXITED"', payload)
        self.assertIn("SHARED_PARTICIPANT", (PROJECT_ROOT / REPORT_PATH).read_text(encoding="utf-8"))

    def test_independent_hash_chain_and_deterministic_rebuild(self):
        first, first_report = build_structured_source_interaction_pattern_graph(PROJECT_ROOT)
        second, second_report = build_structured_source_interaction_pattern_graph(PROJECT_ROOT)
        self.assertEqual(first, second)
        self.assertEqual(first_report, second_report)
        self.assertEqual(first, self.graph)
        for row in first["graph_records"]:
            self.assertEqual(row["graph_record_sha256"], object_sha256({key: value for key, value in row.items() if key != "graph_record_sha256"}))
        without_determinism = {key: value for key, value in first.items() if key != "determinism"}
        self.assertEqual(first["determinism"]["artifact_semantics_sha256"], object_sha256(without_determinism))

    def test_released_upstream_contract_hashes_are_regression_locked(self):
        for path, expected in UPSTREAM_CONTRACT_HASHES.items():
            self.assertEqual(sha256_file(PROJECT_ROOT / path), expected)
        self.assertEqual(self.graph["authority"]["upstream_contract_file_sha256"], UPSTREAM_CONTRACT_HASHES)

    def test_schema_is_closed_and_tampering_unknown_property_fails(self):
        tampered = copy.deepcopy(self.graph)
        tampered["participant_pattern_nodes"][0]["chart_instance_id"] = "invented"
        with self.assertRaises(TrainingError):
            validate_structured_source_interaction_pattern_graph_value(PROJECT_ROOT, tampered)

    def test_tampering_node_edge_context_multiplicity_locator_or_hash_fails(self):
        mutations = []
        node = copy.deepcopy(self.graph); node["participant_pattern_nodes"][0]["source_lexeme"] = "午"; mutations.append(node)
        edge = copy.deepcopy(self.graph); edge["interaction_claim_edges"][0]["edge_class"] = "SOURCE_ASSERTED_ATTENUATION"; mutations.append(edge)
        context = copy.deepcopy(self.graph); context["context_inheritance_edges"][0]["antecedent_source_occurrence_id"] = "ZPZQ-CL-09-009-003"; mutations.append(context)
        multiplicity = copy.deepcopy(self.graph); multiplicity["multiplicity_constraints"][0]["exact_slot_selection"] = "SLOT_1"; mutations.append(multiplicity)
        locator = copy.deepcopy(self.graph); locator["graph_records"][0]["source_occurrence_id"] = "INVENTED"; mutations.append(locator)
        digest = copy.deepcopy(self.graph); digest["graph_records"][0]["graph_record_sha256"] = "0" * 64; mutations.append(digest)
        for value in mutations:
            with self.subTest(index=mutations.index(value)):
                with self.assertRaises(TrainingError):
                    validate_structured_source_interaction_pattern_graph_value(PROJECT_ROOT, value)

    def test_validator_rejects_unresolved_actor_or_target_binding_upgrade(self):
        tampered = copy.deepcopy(self.graph)
        edge = next(row for row in tampered["interaction_claim_edges"] if row["source_occurrence_id"] == "ZPZQ-CL-09-005-001")
        edge["actor_participant_pattern_node_ids"] = ["BSSIPG-R1-P-INVENTED-01"]
        with self.assertRaises(TrainingError):
            validate_structured_source_interaction_pattern_graph_value(PROJECT_ROOT, tampered)

    def test_cli_exposes_deterministic_build_and_validate_tooling(self):
        parser = build_parser()
        self.assertEqual(parser.parse_args(["structured-source-interaction-pattern-graph-build"]).command, "structured-source-interaction-pattern-graph-build")
        self.assertEqual(parser.parse_args(["structured-source-interaction-pattern-graph-validate"]).command, "structured-source-interaction-pattern-graph-validate")


if __name__ == "__main__":
    unittest.main()
