from __future__ import annotations

import copy
import json
import unittest
from collections import Counter
from pathlib import Path

from fortune_training.bazi_classical_relation_interaction_assertion import (
    ACTOR_REFERENCE_KINDS,
    ASSERTION_CLASSES,
    AUDIT_ID,
    MANDATORY_SHEN_BLOCK_COUNTS,
    MANDATORY_SHEN_SOURCE_OCCURRENCE_IDS,
    MANDATORY_SOURCE_OCCURRENCE_IDS,
    MATRIX_PATH,
    NEUTRAL_RUNTIME_PRIMITIVES,
    QTBJ_EXPLICIT_RELEASE_SOURCE_OCCURRENCE_IDS,
    REPORT_PATH,
    build_classical_relation_interaction_assertion_matrix,
    validate_classical_relation_interaction_assertion_matrix,
    validate_classical_relation_interaction_assertion_matrix_value,
)
from fortune_training.cli import build_parser
from fortune_training.util import TrainingError, object_sha256, sha256_file
from fortune_training.verify import verify_repository


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ClassicalRelationInteractionAssertionReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads((PROJECT_ROOT / MATRIX_PATH).read_text(encoding="utf-8"))
        cls.records = {
            record["source_occurrence_id"]: record for record in cls.matrix["records"]
        }

    def test_release_artifact_validates_and_is_in_repository_verify(self):
        report = validate_classical_relation_interaction_assertion_matrix(PROJECT_ROOT)
        self.assertEqual(report["status"], "PASS")
        self.assertTrue(report["mandatory_source_exactly_once"])
        self.assertTrue(report["source_locator_replay"])
        self.assertTrue(report["neutral_contract_refs_resolved"])
        repository_report = verify_repository(PROJECT_ROOT)
        self.assertEqual(
            repository_report["classical_relation_interaction_assertion"]["audit_id"],
            AUDIT_ID,
        )

    def test_four_shen_blocks_preserve_exact_22_occurrences_exactly_once(self):
        occurrence_ids = [record["source_occurrence_id"] for record in self.matrix["records"]]
        self.assertEqual(occurrence_ids[:22], list(MANDATORY_SHEN_SOURCE_OCCURRENCE_IDS))
        self.assertEqual(len(occurrence_ids[:22]), len(set(occurrence_ids[:22])))
        self.assertEqual(
            Counter(
                record["parent_source_block_id"]
                for record in self.matrix["records"][:22]
            ),
            Counter(MANDATORY_SHEN_BLOCK_COUNTS),
        )
        self.assertEqual(self.matrix["summary"]["shen_record_count"], 22)

    def test_complete_source_universe_is_closed_and_ordered(self):
        self.assertEqual(
            [record["source_occurrence_id"] for record in self.matrix["records"]],
            list(MANDATORY_SOURCE_OCCURRENCE_IDS),
        )
        self.assertEqual(len(self.records), 24)
        self.assertEqual(
            self.matrix["mandatory_source_universe"]["qtbj_explicit_release_source_occurrence_ids"],
            list(QTBJ_EXPLICIT_RELEASE_SOURCE_OCCURRENCE_IDS),
        )

    def test_success_reversal_failure_attenuation_and_allocation_are_distinct(self):
        self.assertEqual(
            self.records["ZPZQ-CL-09-003-006"]["primary_assertion_class"],
            "RESOLUTION_ASSERTION",
        )
        reversal = self.records["ZPZQ-CL-09-005-002"]
        self.assertEqual(
            reversal["primary_assertion_class"],
            "REVERSAL_OR_REAPPEARANCE_ASSERTION",
        )
        self.assertIn(
            "PARTICIPANT_ALLOCATION_ASSERTION",
            reversal["secondary_assertion_classes"],
        )
        self.assertEqual(
            self.records["ZPZQ-CL-09-007-004"]["primary_assertion_class"],
            "RESOLUTION_FAILURE_ASSERTION",
        )
        self.assertEqual(
            self.records["ZPZQ-CL-09-009-004"]["primary_assertion_class"],
            "ATTENUATION_ASSERTION",
        )
        observed = {
            record["primary_assertion_class"] for record in self.matrix["records"]
        } | {
            secondary
            for record in self.matrix["records"]
            for secondary in record["secondary_assertion_classes"]
        }
        self.assertEqual(observed, set(ASSERTION_CLASSES))

    def test_context_questions_and_summaries_are_preserved_not_dropped(self):
        for source_occurrence_id in (
            "ZPZQ-CL-09-005-001",
            "ZPZQ-CL-09-007-001",
            "ZPZQ-CL-09-009-001",
        ):
            self.assertEqual(
                self.records[source_occurrence_id]["source_assertion_role"],
                "CONTEXTUAL_QUESTION",
            )
        for source_occurrence_id in (
            "ZPZQ-CL-09-003-006",
            "ZPZQ-CL-09-003-011",
            "ZPZQ-CL-09-007-004",
            "ZPZQ-CL-09-009-005",
        ):
            self.assertEqual(
                self.records[source_occurrence_id]["source_assertion_role"],
                "SUMMARY_SOURCE_ASSERTION",
            )

    def test_qtbj_release_is_participant_mediated_and_never_invents_relation_actor(self):
        expected_layers = {
            "QTBJ-CL-05347": "QTBJ_CORE_SOURCE",
            "QTBJ-CL-05370": "XU_COMMENTARY_SOURCE",
        }
        for source_occurrence_id, source_layer in expected_layers.items():
            record = self.records[source_occurrence_id]
            self.assertEqual(record["source_layer"], source_layer)
            self.assertEqual(
                record["primary_assertion_class"],
                "PARTICIPANT_MEDIATED_RELEASE_ASSERTION",
            )
            self.assertEqual(
                record["actor_reference_kind"], "PARTICIPANT_OR_CONTEXT_ACTOR"
            )
            self.assertNotEqual(record["actor_reference_kind"], "RELATION_PATTERN_ACTOR")
            self.assertIn("解合", record["exact_source_text"])

    def test_hequqiyi_preserves_multiplicity_without_exact_winner(self):
        multiplicity = self.records["ZPZQ-CL-09-005-002"][
            "multiplicity_and_alternative_path"
        ]
        self.assertEqual(
            multiplicity["source_named_multiplicity"],
            [{"participant_lexeme": "卯", "count": 2}],
        )
        self.assertEqual(multiplicity["exact_instance_selection"], "NOT_SELECTED")
        self.assertEqual(
            multiplicity["alternative_path_signal"],
            "PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS",
        )
        self.assertIn("合去其一", multiplicity["allocation_lexemes"])
        self.assertIn(
            "COMPATIBLE_EXACT_INSTANCE_PATH_ENUMERATION",
            self.records["ZPZQ-CL-09-005-002"]["unresolved_semantic_requirements"],
        )

    def test_chongzhiwuli_is_attenuation_not_relation_absence(self):
        record = self.records["ZPZQ-CL-09-009-004"]
        self.assertIn("冲之无力", record["source_assertion_fragments"])
        self.assertEqual(record["primary_assertion_class"], "ATTENUATION_ASSERTION")
        self.assertEqual(
            record["runtime_semantic_boundary"]["relation_presence_verdict"],
            "NOT_EMITTED",
        )
        self.assertIn(
            "CLASSICAL_ATTENUATION_GRADE", record["unresolved_semantic_requirements"]
        )

    def test_buchong_buxing_never_delete_or_mutate_raw_relations(self):
        negative_effect_records = [
            record
            for record in self.matrix["records"]
            if "不冲" in record["exact_source_text"] or "不刑" in record["exact_source_text"]
        ]
        self.assertGreater(len(negative_effect_records), 0)
        for record in negative_effect_records:
            self.assertFalse(
                record["runtime_semantic_boundary"]["raw_relation_mutation_allowed"]
            )
            self.assertEqual(
                record["runtime_semantic_boundary"]["relation_presence_verdict"],
                "NOT_EMITTED",
            )

    def test_only_released_neutral_facts_are_dependencies(self):
        for record in self.matrix["records"]:
            for dependency in record["neutral_runtime_dependency_map"]:
                self.assertIn(dependency["primitive"], NEUTRAL_RUNTIME_PRIMITIVES)
                self.assertEqual(
                    dependency["binding_status"],
                    "AVAILABLE_AS_NEUTRAL_EVIDENCE_ONLY",
                )
        allocation_primitives = {
            row["primitive"]
            for row in self.records["ZPZQ-CL-09-005-002"][
                "neutral_runtime_dependency_map"
            ]
        }
        self.assertIn("RELATION_INCIDENCE_DEGREE", allocation_primitives)
        self.assertIn("RELATION_PAIR_TOPOLOGY", allocation_primitives)

    def test_artifact_emits_no_precedence_operability_resolver_or_runtime_mutation(self):
        scope = self.matrix["scope"]
        self.assertFalse(scope["global_relation_precedence_released"])
        self.assertFalse(scope["classical_operability_evaluator_released"])
        self.assertFalse(scope["graph_or_fixpoint_resolver_released"])
        self.assertFalse(scope["winner_selection_released"])
        self.assertFalse(scope["participant_auto_allocation_released"])
        self.assertFalse(scope["raw_relation_mutation_released"])
        self.assertFalse(scope["activation_suppression_or_cancellation_runtime_released"])
        self.assertNotIn("precedence_rules", self.matrix)
        self.assertNotIn("winner", self.matrix)

    def test_deterministic_rebuild_record_hashes_and_artifact_hash(self):
        first, first_report = build_classical_relation_interaction_assertion_matrix(
            PROJECT_ROOT
        )
        second, second_report = build_classical_relation_interaction_assertion_matrix(
            PROJECT_ROOT
        )
        self.assertEqual(first, second)
        self.assertEqual(first_report, second_report)
        self.assertEqual(first, self.matrix)
        for record in first["records"]:
            self.assertEqual(
                record["record_sha256"],
                object_sha256(
                    {key: value for key, value in record.items() if key != "record_sha256"}
                ),
            )
        without_determinism = {
            key: value for key, value in first.items() if key != "determinism"
        }
        self.assertEqual(
            first["determinism"]["artifact_semantics_sha256"],
            object_sha256(without_determinism),
        )

    def test_source_and_provenance_integrity_is_exact(self):
        authority = self.matrix["authority"]
        self.assertEqual(
            sha256_file(PROJECT_ROOT / authority["canonical_source_path"]),
            authority["canonical_source_sha256"],
        )
        self.assertEqual(
            sha256_file(PROJECT_ROOT / authority["source_access_index_path"]),
            authority["source_access_index_sha256"],
        )
        for record in self.matrix["records"]:
            self.assertEqual(record["canonical_source_sha256"], authority["canonical_source_sha256"])
            self.assertTrue(record["source_assertion_fragments"])
            for fragment in record["source_assertion_fragments"]:
                self.assertIn(fragment, record["exact_source_text"])

    def test_tampering_fails_closed(self):
        value = copy.deepcopy(self.matrix)
        value["records"][0]["runtime_semantic_boundary"][
            "raw_relation_mutation_allowed"
        ] = True
        with self.assertRaises(TrainingError):
            validate_classical_relation_interaction_assertion_matrix_value(
                PROJECT_ROOT, value
            )

    def test_report_and_cli_publish_boundary(self):
        report = (PROJECT_ROOT / REPORT_PATH).read_text(encoding="utf-8")
        self.assertIn("`冲之无力` is preserved as attenuation language", report)
        self.assertIn("`合去其一` preserves all compatible future exact-instance", report)
        self.assertIn("create no generic stem-control relation", report)
        parser = build_parser()
        action = next(item for item in parser._actions if item.dest == "command")
        self.assertIn("classical-relation-interaction-assertion-build", action.choices)
        self.assertIn("classical-relation-interaction-assertion-validate", action.choices)
        self.assertEqual(self.matrix["schema"], AUDIT_ID)

    def test_closed_actor_vocabulary_is_complete(self):
        self.assertEqual(
            set(self.matrix["closed_vocabularies"]["actor_reference_kinds"]),
            set(ACTOR_REFERENCE_KINDS),
        )
        observed = {record["actor_reference_kind"] for record in self.matrix["records"]}
        self.assertEqual(observed, set(ACTOR_REFERENCE_KINDS))


if __name__ == "__main__":
    unittest.main()
