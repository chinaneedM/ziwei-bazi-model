from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from fortune_training.classical_relation_evidence import (
    AUDIT_ID,
    COVERAGE_PATH,
    CURRENT_RELATION_FAMILIES,
    EXPECTED_SOURCE_BYTES,
    EXPECTED_SOURCE_PATH,
    EXPECTED_SOURCE_SHA256,
    MATRIX_PATH,
    REPORT_PATH,
    _bind_conflict_groups,
    _build_records,
    _dependency_tags,
    _is_candidate,
    _relation_families,
    _runtime_dependency_map,
    _statement_classes,
    validate_classical_relation_evidence,
)
from fortune_training.cli import build_parser
from fortune_training.util import sha256_file


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _dependency_status(rows: list[dict[str, str]], primitive: str) -> str:
    return next(row["status"] for row in rows if row["primitive"] == primitive)


class ClassicalRelationEvidenceClassificationTests(unittest.TestCase):
    def test_real_two_pass_discovers_control_term_and_replays_target_locator(self):
        control = json.dumps(
            {
                "SOURCE_TERM_OCCURRENCE_ID": "FIXTURE-TERM-001",
                "RAW_TERM": "牵合",
                "RESULT_OCCURRENCE_ROLE": "TECHNICAL_TERM",
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ) + "\n"
        target = "此局受牵合暂缓。\n"
        payload = (control + target).encode("utf-8")
        target_bytes = target.encode("utf-8")
        self.assertFalse(_is_candidate(target.strip(), "", [], [], []))

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            segment_path = root / "fixture-segment.txt"
            segment_path.write_bytes(payload)
            index = {
                "source": {
                    "canonical_path": "fixture-canonical.txt",
                    "canonical_sha256": hashlib.sha256(payload).hexdigest(),
                },
                "segments": [
                    {
                        "segment_id": "S14-0001",
                        "path": "fixture-segment.txt",
                        "sha256": hashlib.sha256(payload).hexdigest(),
                        "sequence": 1,
                        "line_start": 1,
                        "line_end_inclusive": 2,
                        "byte_start": 0,
                    }
                ],
            }
            first = _build_records(root, index)
            second = _build_records(root, index)

        self.assertEqual(first, second)
        records, coverage, discovery = first
        self.assertEqual(discovery["pass1_discovered_terms"], ["牵合"])
        self.assertEqual(discovery["pass2_vocabulary_only_record_count"], 2)
        self.assertEqual(
            discovery["vocabulary_closure_sha256"],
            hashlib.sha256('["牵合"]'.encode("utf-8")).hexdigest(),
        )
        target_record = next(
            record for record in records if record["exact_excerpt"] == target.strip()
        )
        self.assertEqual(target_record["canonical_line_start"], 2)
        self.assertEqual(target_record["canonical_byte_start"], len(control.encode("utf-8")))
        self.assertEqual(target_record["canonical_byte_end_exclusive"], len(payload))
        self.assertEqual(
            target_record["passage_sha256"], hashlib.sha256(target_bytes).hexdigest()
        )
        self.assertEqual(coverage[0]["new_vocabulary_discovered"], ["牵合"])

    def test_conflict_linkage_requires_explicit_id_and_distinct_source_roles(self):
        def record(
            evidence_id: str,
            source_conflict_id: str | None,
            source_pairing_role: str | None,
        ) -> dict[str, object]:
            return {
                "evidence_id": evidence_id,
                "relation_families": ["BRANCH_CHONG"],
                "review_status": "CONFLICT_REQUIRES_REVIEW",
                "source_conflict_id": source_conflict_id,
                "source_pairing_role": source_pairing_role,
                "conflict_group_ids": [],
            }

        paired_a = record("S14-EV-L00001-000000000001", "SOURCE-CONFLICT-1", "SOURCE_A")
        paired_b = record("S14-EV-L00002-000000000002", "SOURCE-CONFLICT-1", "SOURCE_B")
        unrelated = record("S14-EV-L00003-000000000003", None, None)
        one_sided = record("S14-EV-L00004-000000000004", "SOURCE-CONFLICT-2", "SOURCE_A")
        records = [paired_a, paired_b, unrelated, one_sided]

        groups = _bind_conflict_groups(records)

        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]["source_conflict_id"], "SOURCE-CONFLICT-1")
        self.assertEqual(
            set(groups[0]["evidence_ids"]),
            {paired_a["evidence_id"], paired_b["evidence_id"]},
        )
        self.assertEqual(unrelated["conflict_group_ids"], [])
        self.assertEqual(one_sided["conflict_group_ids"], [])

    def test_direct_rule_and_example_remain_distinct(self):
        families, gaps = _relation_families("甲己相合。", "论十干合而不合")
        tags = _dependency_tags("甲己相合。", families, gaps)
        direct = _statement_classes(
            "甲己相合。", {}, families, gaps, tags, "JSON:RAW_CLAUSE_TEXT"
        )
        example = _statement_classes(
            "甲子己丑丙寅辛卯，甲己相合。",
            {},
            families,
            gaps,
            tags,
            "JSON:RAW_CLAUSE_TEXT",
        )
        self.assertEqual(direct[0], "DEFINITION_OR_NOMINAL_RELATION")
        self.assertEqual(example[0], "EXAMPLE_ONLY")

    def test_conflict_is_profile_candidate_and_unresolved(self):
        families, gaps = _relation_families("不同版本有异说。", "论十干合而不合")
        tags = _dependency_tags("不同版本有异说。", families, gaps)
        primary, _, review, labels = _statement_classes(
            "不同版本有异说。",
            {"CONFLICT_ID": "TEST-CONFLICT"},
            families,
            gaps,
            tags,
            "JSON:OTHER_SOURCE_POSITION",
        )
        self.assertEqual(primary, "CONTRADICTORY_OR_ALTERNATIVE_STATEMENT")
        self.assertEqual(review, "CONFLICT_REQUIRES_REVIEW")
        self.assertIn("PROFILE_CANDIDATE", labels)

    def test_natal_and_flow_month_roles_never_substitute(self):
        natal_rows, _ = _runtime_dependency_map(
            ["STEM_FIVE_COMBINATION"],
            [],
            ["MONTH_COMMAND_OR_SEASON"],
            "月令为审计条件",
        )
        flow_rows, _ = _runtime_dependency_map(
            ["STEM_FIVE_COMBINATION"],
            [],
            ["MONTH_COMMAND_OR_SEASON", "TEMPORAL_CONTEXT"],
            "当前流月季节为审计条件",
        )
        self.assertEqual(
            _dependency_status(natal_rows, "NATAL_MONTH_COMMAND"),
            "AVAILABLE_EXACTLY",
        )
        self.assertFalse(any(row["primitive"] == "ACTIVE_FLOW_SOLAR_MONTH" for row in natal_rows))
        self.assertEqual(
            _dependency_status(flow_rows, "ACTIVE_FLOW_SOLAR_MONTH"),
            "AVAILABLE_EXACTLY",
        )
        self.assertFalse(any(row["primitive"] == "NATAL_MONTH_COMMAND" for row in flow_rows))

    def test_incidence_is_neutral_topology_not_competition(self):
        rows, missing = _runtime_dependency_map(
            ["STEM_FIVE_COMBINATION"],
            [],
            ["MULTIPLICITY_OR_COMPETITION"],
            "两干争合一干",
        )
        self.assertEqual(
            _dependency_status(rows, "RELATION_INCIDENCE_EXACT_TOPOLOGY"),
            "AVAILABLE_AS_NEUTRAL_EVIDENCE_ONLY",
        )
        self.assertIn("CLASSICAL_COMPETITION_SEMANTICS", missing)

    def test_transition_is_neutral_set_change_not_release(self):
        rows, missing = _runtime_dependency_map(
            ["BRANCH_CHONG"], [], ["CLASH_OR_RELEASE"], "冲开合局"
        )
        self.assertEqual(
            _dependency_status(rows, "RELATION_TRANSITION_BEFORE_AFTER"),
            "AVAILABLE_AS_NEUTRAL_EVIDENCE_ONLY",
        )
        self.assertIn("CLASH_RELEASE_OR_CANCELLATION_SEMANTICS", missing)

    def test_unavailable_strength_is_not_inferred_from_hidden_stem_order(self):
        rows, missing = _runtime_dependency_map(
            ["STEM_FIVE_COMBINATION"],
            [],
            ["ROOT_OR_SUPPORT", "STRENGTH_GRADE"],
            "有根而旺",
        )
        self.assertEqual(
            _dependency_status(rows, "STRENGTH_OR_WANGSHUAI_GRADE"),
            "MISSING_PRIMITIVE",
        )
        self.assertIn("ROOT_OR_SUPPORT_GRADE", missing)

    def test_unreleased_family_remains_outside_registry(self):
        rows, missing = _runtime_dependency_map([], ["BRANCH_HARM"], [], "六害")
        self.assertEqual(
            _dependency_status(rows, "RELATION_REGISTRY:BRANCH_HARM"),
            "OUTSIDE_CURRENT_RELATION_REGISTRY",
        )
        self.assertEqual(missing, [])


class ClassicalRelationEvidenceReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads((PROJECT_ROOT / MATRIX_PATH).read_text(encoding="utf-8"))
        cls.coverage = json.loads((PROJECT_ROOT / COVERAGE_PATH).read_text(encoding="utf-8"))

    def test_release_artifacts_validate_and_cover_all_52_segments(self):
        report = validate_classical_relation_evidence(PROJECT_ROOT)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["segment_count"], 52)
        self.assertTrue(report["all_segments_terminal"])
        self.assertEqual(len(self.coverage["segments"]), 52)
        self.assertEqual(
            [row["sequence"] for row in self.coverage["segments"]], list(range(1, 53))
        )
        self.assertEqual(
            sum(row["scanned_line_count"] for row in self.coverage["segments"]), 15442
        )
        self.assertEqual(
            sum(row["scanned_byte_count"] for row in self.coverage["segments"]),
            EXPECTED_SOURCE_BYTES,
        )

    def test_every_released_relation_family_has_source_evidence(self):
        counts = self.matrix["summary"]["relation_family_counts"]
        for family in CURRENT_RELATION_FAMILIES:
            with self.subTest(family=family):
                self.assertGreater(counts.get(family, 0), 0)

    def test_examples_rules_conflicts_and_gaps_are_not_flattened(self):
        classes = self.matrix["summary"]["statement_class_counts"]
        self.assertGreater(classes["DEFINITION_OR_NOMINAL_RELATION"], 0)
        self.assertGreater(classes["EXAMPLE_ONLY"], 0)
        self.assertGreater(classes["CONTRADICTORY_OR_ALTERNATIVE_STATEMENT"], 0)
        self.assertGreater(classes["RUNTIME_RELATION_GAP"], 0)
        self.assertTrue(self.matrix["conflict_groups"])

    def test_two_pass_closure_and_source_conflict_links_are_published(self):
        discovery = self.matrix["method"]["vocabulary_expansion"]
        self.assertGreater(discovery["pass2_vocabulary_only_record_count"], 0)
        self.assertEqual(
            discovery["pass1_discovered_terms"],
            sorted(
                {
                    term
                    for segment in self.coverage["segments"]
                    for term in segment["new_vocabulary_discovered"]
                }
            ),
        )
        records = {record["evidence_id"]: record for record in self.matrix["records"]}
        for group in self.matrix["conflict_groups"]:
            linked = [records[evidence_id] for evidence_id in group["evidence_ids"]]
            self.assertEqual(
                {record["source_conflict_id"] for record in linked},
                {group["source_conflict_id"]},
            )
            self.assertGreaterEqual(
                len({record["source_pairing_role"] for record in linked}), 2
            )
        one_sided = [
            record
            for record in records.values()
            if record["review_status"] == "CONFLICT_REQUIRES_REVIEW"
            and not record["conflict_group_ids"]
        ]
        self.assertEqual(len(one_sided), 1)

    def test_exact_source_identity_and_prediction_boundary(self):
        authority = self.matrix["authority"]
        self.assertEqual(authority["canonical_source_path"], EXPECTED_SOURCE_PATH)
        self.assertEqual(authority["canonical_source_sha256"], EXPECTED_SOURCE_SHA256)
        self.assertFalse(authority["prediction_source_selection_allowed"])
        self.assertEqual(
            sha256_file(PROJECT_ROOT / EXPECTED_SOURCE_PATH), EXPECTED_SOURCE_SHA256
        )
        runtime_policy = (PROJECT_ROOT / "config/model-runtime.json").read_text(encoding="utf-8")
        self.assertNotIn("audits/bazi-classical-relation-lifecycle-evidence-r1", runtime_policy)

    def test_report_declares_no_semantic_evaluator(self):
        report = (PROJECT_ROOT / REPORT_PATH).read_text(encoding="utf-8")
        self.assertIn("no Classical lifecycle semantic evaluator is released", report)
        self.assertIn("`ENTERED` is not activation", report)
        self.assertIn("active Flow month never replaces Natal month command", report)

    def test_cli_exposes_build_and_validation_paths(self):
        parser = build_parser()
        action = next(item for item in parser._actions if item.dest == "command")
        self.assertIn("classical-relation-evidence-build", action.choices)
        self.assertIn("classical-relation-evidence-validate", action.choices)
        self.assertEqual(self.matrix["schema"], AUDIT_ID)


if __name__ == "__main__":
    unittest.main()
