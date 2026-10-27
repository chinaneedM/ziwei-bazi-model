from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from fortune_training.bazi_classical_effect_constraint_graph.release import (
    CONTRACT_PATH as UNIT2_CONTRACT_PATH,
    validate_release_contract as validate_unit2_release_contract,
)
from fortune_training.bazi_classical_resolver_admission.release import (
    CONTRACT_PATH as UNIT3_CONTRACT_PATH,
    validate_release_contract as validate_unit3_release_contract,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import (
    TrainingError,
    atomic_write_bytes,
    atomic_write_json,
    load_json,
    object_sha256,
    sha256_file,
)

from .profile import (
    FRAGMENT_PROJECTION_STATUSES,
    SEMANTIC_CANDIDATE_KINDS,
    SOURCE_CLAIM_TO_SEMANTIC_CANDIDATE,
    bazi_classical_effect_semantic_candidate_projection_r1_profile,
)


AUDIT_ID = "BAZI-CLASSICAL-EFFECT-SEMANTIC-CANDIDATE-PROJECTION-R1"
AUDIT_ROOT = Path("audits/bazi-classical-effect-semantic-candidate-projection-r1")
CONTRACT_PATH = AUDIT_ROOT / "contract.json"
REPORT_PATH = AUDIT_ROOT / "coverage-report.md"
SCHEMA_PATH = Path("schemas/bazi-classical-effect-semantic-candidate-projection-r1.schema.json")
RUNTIME_SCHEMA_PATH = Path("schemas/bazi-classical-effect-semantic-candidate-runtime-r1.schema.json")

EXPECTED_UNIT2_CONTRACT_SEMANTICS_SHA256 = "0c6dfccb89710c57f96a762406df32a70395b8fef2bb15ab6654445a22108950"
EXPECTED_UNIT3_CONTRACT_SEMANTICS_SHA256 = "869916b557dcc889831b4775679cf1bd0db9e786f280ec42493cafd188e9bec6"


def build_release_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    unit2 = validate_unit2_release_contract(root)
    if unit2["contract_semantics_sha256"] != EXPECTED_UNIT2_CONTRACT_SEMANTICS_SHA256:
        raise TrainingError("released Unit 2 contract semantic identity changed")
    unit3 = validate_unit3_release_contract(root)
    if unit3["contract_semantics_sha256"] != EXPECTED_UNIT3_CONTRACT_SEMANTICS_SHA256:
        raise TrainingError("released Unit 3 contract semantic identity changed")

    profile = bazi_classical_effect_semantic_candidate_projection_r1_profile()
    contract = {
        "schema": "BAZI-CLASSICAL-EFFECT-SEMANTIC-CANDIDATE-PROJECTION-CONTRACT-R1",
        "audit_id": AUDIT_ID,
        "authority": {
            "unit2_contract_path": UNIT2_CONTRACT_PATH.as_posix(),
            "unit2_contract_semantics_sha256": unit2["contract_semantics_sha256"],
            "unit3_contract_path": UNIT3_CONTRACT_PATH.as_posix(),
            "unit3_contract_semantics_sha256": unit3["contract_semantics_sha256"],
        },
        "semantic_candidate_profile": json_value(profile),
        "closed_vocabularies": {
            "semantic_candidate_kinds": list(SEMANTIC_CANDIDATE_KINDS),
            "fragment_projection_statuses": list(FRAGMENT_PROJECTION_STATUSES),
            "source_claim_to_semantic_candidate": {
                key: {"effect_facet": value[0], "semantic_candidate_kind": value[1]}
                for key, value in SOURCE_CLAIM_TO_SEMANTIC_CANDIDATE.items()
            },
        },
        "admission_projection_contract": {
            "ADMITTED": "ONE_SEMANTIC_CANDIDATE_PER_UNIT2_EFFECT_CONSTRAINT",
            "PRESERVED_NOT_ADMITTED": "PRESERVE_FRAGMENT_ZERO_SEMANTIC_CANDIDATES",
            "PRESERVED_OUTSIDE_PROFILE": "PRESERVE_FRAGMENT_ZERO_SEMANTIC_CANDIDATES",
            "unit3_admission_re_evaluation": "FORBIDDEN",
        },
        "candidate_preservation_contract": {
            "constraint_drop": "FORBIDDEN",
            "constraint_merge": "FORBIDDEN",
            "constraint_split": "FORBIDDEN",
            "candidate_selection": "NOT_RELEASED",
            "candidate_truth": "NOT_RELEASED",
            "candidate_coexistence": "NOT_RELEASED",
            "candidate_exclusivity": "NOT_RELEASED",
            "candidate_priority": "NOT_RELEASED",
            "candidate_conflict": "NOT_RELEASED",
            "candidate_rewrite": "NOT_RELEASED",
            "candidate_state_transition": "NOT_RELEASED",
            "candidate_winner_loser": "NOT_RELEASED",
            "cross_outer_composition": "NOT_RELEASED",
            "cartesian_expansion": "NOT_RELEASED",
        },
        "record_specific_locks": {
            "ZPZQ-CL-09-005-002": {
                "released_candidate_kinds": [
                    "SOURCE_GROUNDED_REVERSAL_OR_REAPPEARANCE_CANDIDATE",
                    "SOURCE_GROUNDED_RESOLUTION_CANDIDATE",
                    "SOURCE_GROUNDED_PARTICIPANT_ALLOCATION_CANDIDATE",
                ],
                "allocation_policy": "PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS_NO_SELECTION",
            },
            "ZPZQ-CL-09-007-002_003": {
                "candidate_preservation_when_admitted": [
                    "SOURCE_GROUNDED_RESOLUTION_FAILURE_CANDIDATE",
                    "SOURCE_GROUNDED_RESOLUTION_CANDIDATE",
                    "SOURCE_GROUNDED_REVERSAL_OR_REAPPEARANCE_CANDIDATE",
                ],
                "current_unit3_partial_admission_authoritative": True,
                "arbitration": "NOT_RELEASED",
            },
            "ZPZQ-CL-09-009-004": {
                "effect_facet": "RELATION_EFFECT_GRADE",
                "semantic_candidate_kind": "SOURCE_GROUNDED_ATTENUATION_CANDIDATE",
                "numeric_grade": "NOT_RELEASED",
                "disposition_synthesis": "FORBIDDEN",
            },
        },
        "hard_exclusions": [
            "UNIT5_REWRITE_OR_ARBITRATION",
            "MECHANISM_CANDIDATE_MATRIX",
            "CLOSURE_GAP_MATRIX",
            "SOURCE_CLAIM_ARBITRATION",
            "CONTRADICTION_RESOLUTION",
            "SOURCE_TRUTH_SELECTION",
            "CANDIDATE_APPLICABILITY_SELECTION_BEYOND_UNIT3_ADMISSION",
            "CLASSICAL_OPERABILITY_TRUTH",
            "PRECEDENCE",
            "PRIORITY",
            "WINNER_OR_LOSER",
            "SUPPRESSION",
            "ACTIVATION",
            "DEACTIVATION",
            "RELEASE",
            "CANCELLATION",
            "OVERRIDE",
            "NEGATION",
            "RELATION_OR_EFFECT_STATE",
            "NUMERIC_ATTENUATION_GRADE",
            "PARTICIPANT_OR_PATH_SELECTION",
            "UNIT6_ALLOCATION_ELABORATION",
            "UNIT7_EFFECT_CANDIDATE_ENVELOPE",
            "GRAPH_REWRITE",
            "FIXPOINT",
            "CYCLE_HANDLING",
            "MONOTONICITY_LATTICE_TERMINATION_SOLVING",
            "CROSS_SOURCE_COMPOSITION",
            "CARTESIAN_CANDIDATE_WORLD_GENERATION",
            "FINAL_CLASSICAL_VERDICT",
            "PREDICTION_SEMANTICS",
        ],
    }
    contract["determinism"] = {"contract_semantics_sha256": object_sha256(contract)}
    return contract


def build_coverage_report(contract: dict[str, Any]) -> str:
    digest = contract["determinism"]["contract_semantics_sha256"]
    return "\n".join((
        "# Bazi Classical Effect Semantic Candidate Projection R1",
        "",
        "- Unit 4 consumes released Unit 2 effect constraints and Unit 3 admission sidecars only.",
        "- Exactly five source-grounded semantic candidate kinds are released; each maps one-to-one from an already released Unit 2 source claim class and effect facet.",
        "- `ADMITTED` fragments project one candidate per Unit 2 effect constraint; non-admitted/outside-profile fragments remain present with zero candidates.",
        "- Candidate existence is source-grounded possibility only: truth, operability, coexistence, exclusivity, priority, conflict, rewrite, state transition, and winner/loser semantics remain `NOT_RELEASED`.",
        "- `005-002` allocation preserves multiplicity/path provenance and selects no participant/path.",
        "- `007-002/003` candidate tensions remain unarbitrated and current Unit 3 PARTIAL admission remains authoritative.",
        "- `009-004` remains grade-only attenuation with no numeric grade or disposition synthesis.",
        "- Source narrative order and source-unresolved graph requirements remain provenance only.",
        "- No Unit 5 rewrite governance, Unit 6 allocation elaboration, Unit 7 envelope, precedence, winner, fixpoint, relation/effect state, or final verdict is released.",
        f"- Deterministic Unit 4 contract semantics: `{digest}`.",
        "",
    ))


def validate_release_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    actual = load_json(root / CONTRACT_PATH)
    expected = build_release_contract(root)
    if actual != expected:
        raise TrainingError("Unit 4 semantic candidate release contract is stale or tampered")
    schema = load_json(root / SCHEMA_PATH)
    runtime_schema = load_json(root / RUNTIME_SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator.check_schema(runtime_schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(actual), key=lambda row: list(row.path))
    if errors:
        raise TrainingError(f"Unit 4 release contract schema validation failed: {errors[0].message}")
    expected_report = build_coverage_report(actual)
    report_path = root / REPORT_PATH
    if not report_path.is_file() or report_path.read_text(encoding="utf-8") != expected_report:
        raise TrainingError("Unit 4 coverage report is stale or missing")
    return {
        "status": "PASS",
        "audit_id": AUDIT_ID,
        "semantic_candidate_kind_count": len(actual["closed_vocabularies"]["semantic_candidate_kinds"]),
        "contract_semantics_sha256": actual["determinism"]["contract_semantics_sha256"],
        "schema_sha256": sha256_file(root / SCHEMA_PATH),
        "runtime_schema_sha256": sha256_file(root / RUNTIME_SCHEMA_PATH),
        "report_sha256": sha256_file(report_path),
    }


def write_release_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    contract = build_release_contract(root)
    atomic_write_json(root / CONTRACT_PATH, contract)
    atomic_write_bytes(root / REPORT_PATH, build_coverage_report(contract).encode("utf-8"))
    return validate_release_contract(root)
