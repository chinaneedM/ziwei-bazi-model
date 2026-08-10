from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from fortune_training.bazi_five_combination_evidence_binding import (
    AUDIT_ID,
    BINDINGS_PATH,
    BINDING_ASSERTION_STRENGTHS,
    BINDING_DISPOSITIONS,
    EXPECTED_EVIDENCE_COUNT,
    NEUTRAL_PREDICATE_KINDS,
    PREDICATE_SPECS,
    PRIMITIVE_BINDINGS,
    REPORT_PATH,
    REQUIRED_UNRESOLVED_PRIMITIVES,
    _validate_runtime_field_path,
    build_five_combination_evidence_bindings,
    validate_five_combination_evidence_binding_value,
    validate_five_combination_evidence_bindings,
)
from fortune_training.classical_relation_evidence import MATRIX_PATH
from fortune_training.cli import build_parser
from fortune_training.util import TrainingError, object_sha256, sha256_file


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class FiveCombinationEvidenceBindingReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = json.loads((PROJECT_ROOT / BINDINGS_PATH).read_text(encoding="utf-8"))
        cls.matrix = json.loads((PROJECT_ROOT / MATRIX_PATH).read_text(encoding="utf-8"))
        cls.source_records = {
            record["evidence_id"]: record
            for record in cls.matrix["records"]
            if "STEM_FIVE_COMBINATION" in record["relation_families"]
        }

    def test_release_artifacts_validate(self):
        report = validate_five_combination_evidence_bindings(PROJECT_ROOT)
        self.assertEqual(report["status"], "PASS")
        self.assertTrue(report["source_locator_replay"])
        self.assertTrue(report["runtime_field_path_resolution"])
        self.assertTrue(report["deterministic_rebuild"])

    def test_all_current_five_combination_evidence_is_covered_exactly_once(self):
        evidence_ids = [
            record["source_evidence_id"] for record in self.catalog["records"]
        ]
        self.assertEqual(len(self.source_records), EXPECTED_EVIDENCE_COUNT)
        self.assertEqual(len(evidence_ids), EXPECTED_EVIDENCE_COUNT)
        self.assertEqual(len(set(evidence_ids)), EXPECTED_EVIDENCE_COUNT)
        self.assertEqual(set(evidence_ids), set(self.source_records))

    def test_source_locator_segment_and_passage_metadata_is_preserved(self):
        fields = (
            "source_id",
            "canonical_source_path",
            "canonical_source_sha256",
            "access_segment_id",
            "access_segment_path",
            "access_segment_sha256",
            "canonical_line_start",
            "canonical_line_end",
            "segment_local_line_start",
            "segment_local_line_end",
            "canonical_byte_start",
            "canonical_byte_end_exclusive",
            "passage_sha256",
        )
        for binding in self.catalog["records"]:
            source = self.source_records[binding["source_evidence_id"]]
            for field in fields:
                self.assertEqual(binding[field], source[field])
            self.assertEqual(
                sha256_file(PROJECT_ROOT / binding["access_segment_path"]),
                binding["access_segment_sha256"],
            )

    def test_closed_registries_and_current_runtime_paths(self):
        self.assertEqual(
            tuple(self.catalog["closed_vocabularies"]["binding_dispositions"]),
            BINDING_DISPOSITIONS,
        )
        self.assertEqual(
            tuple(self.catalog["closed_vocabularies"]["binding_assertion_strengths"]),
            BINDING_ASSERTION_STRENGTHS,
        )
        self.assertEqual(
            tuple(self.catalog["closed_vocabularies"]["neutral_predicate_kinds"]),
            NEUTRAL_PREDICATE_KINDS,
        )
        self.assertEqual(set(self.catalog["runtime_predicate_registry"]), set(PREDICATE_SPECS))
        for spec in PREDICATE_SPECS.values():
            for path in spec["runtime_fact_or_field_paths"]:
                _validate_runtime_field_path(path)

    def test_positional_coordinates_remain_related_neutral_evidence(self):
        positional = {
            "NATAL_POSITION_DOMAIN",
            "NATAL_PILLAR_ORDINALS",
            "NATAL_ORDINAL_DISTANCE",
            "NATAL_INTERVENING_VISIBLE_STEM_IDS",
            "INTERVENER_STEM_IDENTITY",
            "NATAL_DAY_MASTER_PARTICIPATION",
        }
        rows = [
            predicate
            for record in self.catalog["records"]
            for predicate in record["neutral_predicate_bindings"]
            if predicate["predicate_kind"] in positional
        ]
        self.assertTrue(rows)
        self.assertEqual(
            {row["binding_assertion_strength"] for row in rows},
            {"RELATED_NEUTRAL_EVIDENCE"},
        )
        self.assertTrue(
            all(
                "CLASSICAL_ORDER_OR_PROXIMITY"
                in record["unresolved_runtime_primitives"]
                for record in self.catalog["records"]
                if any(
                    predicate["predicate_kind"] in positional
                    for predicate in record["neutral_predicate_bindings"]
                )
            )
        )

    def test_shared_participant_and_support_remain_neutral(self):
        shared = [
            predicate
            for record in self.catalog["records"]
            for predicate in record["neutral_predicate_bindings"]
            if predicate["predicate_kind"]
            == "RELATION_PAIR_SHARED_PARTICIPANT_TOPOLOGY"
        ]
        self.assertTrue(shared)
        self.assertEqual(
            {row["binding_assertion_strength"] for row in shared},
            {"RELATED_NEUTRAL_EVIDENCE"},
        )
        for record in self.catalog["records"]:
            if "ROOT_OR_SUPPORT" not in record["source_condition_dependency_tags"]:
                continue
            support = {
                predicate["predicate_kind"]: predicate["binding_assertion_strength"]
                for predicate in record["neutral_predicate_bindings"]
            }
            self.assertEqual(
                support.get("EXACT_HIDDEN_STEM_MATCH_REFERENCE"),
                "RELATED_NEUTRAL_EVIDENCE",
            )
            self.assertEqual(
                support.get("SAME_ELEMENT_HIDDEN_SUPPORT_REFERENCE"),
                "RELATED_NEUTRAL_EVIDENCE",
            )
            self.assertIn("ROOT_OR_SUPPORT_GRADE", record["unresolved_runtime_primitives"])

    def test_natal_month_command_and_flow_month_are_distinct(self):
        natal = PREDICATE_SPECS["NATAL_MONTH_COMMAND_REFERENCE"]
        flow = PREDICATE_SPECS["ACTIVE_FLOW_SOLAR_MONTH_REFERENCE"]
        self.assertNotEqual(natal["runtime_contract"], "")
        self.assertNotEqual(natal["runtime_fact_or_field_paths"], flow["runtime_fact_or_field_paths"])
        self.assertTrue(
            all("NatalMonthCommandReference" in path or "natal_month_command" in path for path in natal["runtime_fact_or_field_paths"])
        )
        self.assertTrue(
            all("ActiveFlowSolarMonthReference" in path or "active_flow_solar_month" in path for path in flow["runtime_fact_or_field_paths"])
        )

    def test_profile_conflict_and_one_sided_metadata_is_exactly_preserved(self):
        for binding in self.catalog["records"]:
            source = self.source_records[binding["source_evidence_id"]]
            self.assertEqual(binding["source_conflict_group_ids"], source["conflict_group_ids"])
            self.assertEqual(
                binding["source_alternative_profile_labels"],
                source["alternative_profile_labels"],
            )
            if source["review_status"] == "CONFLICT_REQUIRES_REVIEW":
                self.assertEqual(
                    binding["binding_disposition"],
                    "PROFILE_ALTERNATIVE_UNRESOLVED",
                )
                self.assertTrue(binding["profile_selection_required"])
        self.assertEqual(self.catalog["summary"]["relevant_conflict_group_count"], 0)
        self.assertEqual(self.catalog["summary"]["relevant_profile_label_count"], 0)

    def test_required_missing_primitives_are_not_pretended_solved(self):
        required = set(REQUIRED_UNRESOLVED_PRIMITIVES)
        for primitive in required:
            source_ids = {
                record["evidence_id"]
                for record in self.source_records.values()
                if primitive in record["runtime_gap_tags"]
            }
            if not source_ids:
                continue
            bound_ids = {
                record["source_evidence_id"]
                for record in self.catalog["records"]
                if primitive in record["unresolved_runtime_primitives"]
            }
            self.assertTrue(source_ids.issubset(bound_ids), primitive)

    def test_transformation_tag_does_not_infer_nominal_element_identity(self):
        evidence_id = "S14-EV-L07720-be1e2719740f"
        source = self.source_records[evidence_id]
        self.assertIn("TRANSFORMATION", source["condition_dependency_tags"])
        self.assertEqual(source["statement_class"], "TRANSFORMATION_CONDITION")
        self.assertIn("方为真化", source["exact_excerpt"])
        self.assertEqual(
            {dependency["primitive"] for dependency in source["runtime_dependency_map"]},
            {
                "EXACT_RAW_RELATION_OCCURRENCES",
                "EXACT_STEM_BRANCH_OCCURRENCE_IDS",
                "TRANSFORMATION_SUCCESS",
            },
        )
        binding = next(
            record
            for record in self.catalog["records"]
            if record["source_evidence_id"] == evidence_id
        )
        self.assertNotIn(
            "NOMINAL_TRANSFORMATION_ELEMENT_IDENTITY",
            {
                predicate["predicate_kind"]
                for predicate in binding["neutral_predicate_bindings"]
            },
        )
        self.assertIn(
            "TRANSFORMATION_SUCCESS", binding["unresolved_runtime_primitives"]
        )

    def test_nominal_element_identity_has_no_unreviewed_exact_binding(self):
        source_primitives = {
            dependency["primitive"]
            for source in self.source_records.values()
            for dependency in source["runtime_dependency_map"]
        }
        self.assertFalse(
            any(
                predicate_kind == "NOMINAL_TRANSFORMATION_ELEMENT_IDENTITY"
                for bindings in (
                    PRIMITIVE_BINDINGS.get(primitive, ())
                    for primitive in source_primitives
                )
                for predicate_kind, _strength in bindings
            )
        )
        self.assertFalse(
            any(
                predicate["predicate_kind"]
                == "NOMINAL_TRANSFORMATION_ELEMENT_IDENTITY"
                for record in self.catalog["records"]
                for predicate in record["neutral_predicate_bindings"]
            )
        )

    def test_non_conditions_are_retained_without_predicate_compilation(self):
        non_conditions = [
            record
            for record in self.catalog["records"]
            if record["binding_disposition"] == "NON_CONDITION_RECORD"
        ]
        self.assertTrue(non_conditions)
        self.assertTrue(all(not record["neutral_predicate_bindings"] for record in non_conditions))
        self.assertEqual(
            {record["source_statement_class"] for record in non_conditions},
            {"COMMENTARY_OR_EXPLANATION", "EXAMPLE_ONLY", "RESULT_OR_EFFECT_STATEMENT"},
        )

    def test_no_new_machine_outcome_vocabulary_is_published(self):
        forbidden_exact = {
            "ELIGIBLE",
            "INELIGIBLE",
            "SATISFIED",
            "UNSATISFIED",
            "NEAR",
            "FAR",
            "TOO_NEAR",
            "TOO_FAR",
            "BLOCKED",
            "UNBLOCKED",
            "ENGAGED",
            "NOT_ENGAGED",
            "FIRST_CLAIM",
            "PRIORITY",
            "COMPETITION",
            "WINNER",
            "LOSER",
            "TRANSFORMED",
            "NOT_TRANSFORMED",
        }
        machine_values = set()
        for record in self.catalog["records"]:
            machine_values.add(record["binding_disposition"])
            for predicate in record["neutral_predicate_bindings"]:
                machine_values.add(predicate["predicate_kind"])
                machine_values.add(predicate["binding_assertion_strength"])
        self.assertFalse(machine_values & forbidden_exact)
        self.assertFalse(self.catalog["scope"]["per_chart_runtime_evaluator_released"])
        self.assertFalse(self.catalog["scope"]["classical_outcome_semantics_released"])
        self.assertFalse(self.catalog["scope"]["free_text_semantic_compiler_used"])

    def test_deterministic_rebuild_and_hashes(self):
        first, first_report = build_five_combination_evidence_bindings(PROJECT_ROOT)
        second, second_report = build_five_combination_evidence_bindings(PROJECT_ROOT)
        self.assertEqual(first, second)
        self.assertEqual(first_report, second_report)
        self.assertEqual(first, self.catalog)
        self.assertEqual(
            first["determinism"]["records_semantics_sha256"],
            object_sha256(first["records"]),
        )
        self.assertEqual(
            (PROJECT_ROOT / REPORT_PATH).read_text(encoding="utf-8"),
            first_report,
        )

    def test_cli_exposes_build_and_validate(self):
        parser = build_parser()
        action = next(item for item in parser._actions if item.dest == "command")
        self.assertIn("five-combination-evidence-binding-build", action.choices)
        self.assertIn("five-combination-evidence-binding-validate", action.choices)
        self.assertEqual(self.catalog["schema"], AUDIT_ID)


class FiveCombinationEvidenceBindingTamperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = json.loads((PROJECT_ROOT / BINDINGS_PATH).read_text(encoding="utf-8"))

    def _assert_tamper_fails(self, mutation) -> None:
        value = copy.deepcopy(self.catalog)
        mutation(value)
        with self.assertRaises(TrainingError):
            validate_five_combination_evidence_binding_value(PROJECT_ROOT, value)

    def test_source_and_binding_tampering_fails_closed(self):
        bound_index = next(
            index
            for index, record in enumerate(self.catalog["records"])
            if record["neutral_predicate_bindings"]
            and record["unresolved_runtime_primitives"]
        )
        mutations = (
            lambda value: value["records"][0].__setitem__("source_evidence_id", "S14-EV-L00001-000000000000"),
            lambda value: value["records"][0].__setitem__("canonical_byte_start", value["records"][0]["canonical_byte_start"] + 1),
            lambda value: value["records"][bound_index].__setitem__("binding_disposition", "EXACT_NEUTRAL_BINDING"),
            lambda value: value["records"][bound_index]["neutral_predicate_bindings"][0].__setitem__("predicate_kind", "PARTICIPANT_ELEMENT_IDENTITY"),
            lambda value: value["records"][bound_index]["neutral_predicate_bindings"][0].__setitem__("binding_assertion_strength", "RELATED_NEUTRAL_EVIDENCE"),
            lambda value: value["records"][bound_index]["neutral_predicate_bindings"][0]["runtime_fact_or_field_paths"].__setitem__(0, "fortune_training.bazi_chart.models:StemInstance.absent_field"),
            lambda value: value["records"][0]["source_conflict_group_ids"].append("INVENTED-CONFLICT"),
            lambda value: value["records"][0]["source_alternative_profile_labels"].append("INVENTED-PROFILE"),
            lambda value: value["records"][bound_index]["unresolved_runtime_primitives"].pop(),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self._assert_tamper_fails(mutation)


if __name__ == "__main__":
    unittest.main()
