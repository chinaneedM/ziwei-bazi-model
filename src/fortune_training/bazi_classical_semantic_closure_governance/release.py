from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from fortune_training.bazi_classical_effect_semantic_candidate.release import (
    CONTRACT_PATH as UNIT4_CONTRACT_PATH,
    validate_release_contract as validate_unit4_release_contract,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.classical_relation_evidence import (
    AUDIT_ID as LIFECYCLE_AUDIT_ID,
    EXPECTED_SOURCE_SHA256 as LIFECYCLE_SOURCE_SHA256,
    MATRIX_PATH as LIFECYCLE_MATRIX_PATH,
    RUNTIME_STATUSES as LIFECYCLE_RUNTIME_STATUSES,
    validate_classical_relation_evidence,
)
from fortune_training.util import (
    TrainingError,
    atomic_write_bytes,
    atomic_write_json,
    load_json,
    object_sha256,
    sha256_file,
)

from .profile import (
    CLOSURE_REQUIREMENT_REGISTRY,
    FRAGMENT_GOVERNANCE_STATUSES,
    MECHANISM_PROPOSAL_KINDS,
    RUNTIME_DEPENDENCY_STATUSES,
    SEMANTIC_CANDIDATE_TO_MECHANISM_PROPOSAL,
    bazi_classical_semantic_mechanism_closure_governance_r1_profile,
)


AUDIT_ID = "BAZI-CLASSICAL-SEMANTIC-MECHANISM-CLOSURE-GOVERNANCE-R1"
AUDIT_ROOT = Path("audits/bazi-classical-semantic-mechanism-closure-governance-r1")
CONTRACT_PATH = AUDIT_ROOT / "contract.json"
REPORT_PATH = AUDIT_ROOT / "coverage-report.md"
SCHEMA_PATH = Path("schemas/bazi-classical-semantic-mechanism-closure-governance-r1.schema.json")
RUNTIME_SCHEMA_PATH = Path("schemas/bazi-classical-semantic-mechanism-closure-runtime-r1.schema.json")

EXPECTED_UNIT4_CONTRACT_SEMANTICS_SHA256 = "d96ea5a66bea6ff5b71b280723c460954d80ed8da6d05008f909cef30a13a3c8"
EXPECTED_LIFECYCLE_MATRIX_GIT_BLOB_SHA1 = "f4adc67e97581cb0fc64118b87e4c146818522c7"


def _git_blob_sha1(path: Path) -> str:
    payload = path.read_bytes()
    header = f"blob {len(payload)}\0".encode("utf-8")
    return hashlib.sha1(header + payload).hexdigest()


def build_release_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    unit4 = validate_unit4_release_contract(root)
    if unit4["contract_semantics_sha256"] != EXPECTED_UNIT4_CONTRACT_SEMANTICS_SHA256:
        raise TrainingError("released Unit 4 contract semantic identity changed")
    lifecycle = validate_classical_relation_evidence(root)
    if tuple(LIFECYCLE_RUNTIME_STATUSES) != RUNTIME_DEPENDENCY_STATUSES:
        raise TrainingError("#229 runtime dependency status vocabulary drifted")
    matrix_blob_sha1 = _git_blob_sha1(root / LIFECYCLE_MATRIX_PATH)
    if matrix_blob_sha1 != EXPECTED_LIFECYCLE_MATRIX_GIT_BLOB_SHA1:
        raise TrainingError("#229 lifecycle evidence matrix identity changed")

    profile = bazi_classical_semantic_mechanism_closure_governance_r1_profile()
    contract = {
        "schema": "BAZI-CLASSICAL-SEMANTIC-MECHANISM-CLOSURE-GOVERNANCE-CONTRACT-R1",
        "audit_id": AUDIT_ID,
        "authority": {
            "unit4_contract_path": UNIT4_CONTRACT_PATH.as_posix(),
            "unit4_contract_semantics_sha256": unit4["contract_semantics_sha256"],
            "lifecycle_audit_id": LIFECYCLE_AUDIT_ID,
            "lifecycle_source_sha256": LIFECYCLE_SOURCE_SHA256,
            "lifecycle_matrix_path": LIFECYCLE_MATRIX_PATH.as_posix(),
            "lifecycle_matrix_git_blob_sha1": matrix_blob_sha1,
            "lifecycle_runtime_dependency_statuses": list(LIFECYCLE_RUNTIME_STATUSES),
            "lifecycle_evidence_record_count": lifecycle["evidence_record_count"],
            "candidate_specific_lifecycle_evidence_binding": "NOT_RELEASED",
        },
        "mechanism_closure_profile": json_value(profile),
        "closed_vocabularies": {
            "mechanism_proposal_kinds": list(MECHANISM_PROPOSAL_KINDS),
            "fragment_governance_statuses": list(FRAGMENT_GOVERNANCE_STATUSES),
            "runtime_dependency_statuses": list(RUNTIME_DEPENDENCY_STATUSES),
            "semantic_candidate_to_mechanism_proposal": dict(
                SEMANTIC_CANDIDATE_TO_MECHANISM_PROPOSAL
            ),
            "closure_requirement_registry": CLOSURE_REQUIREMENT_REGISTRY,
        },
        "closure_input_contract": {
            "claim_level_input": "UNIT4_UNRESOLVED_CLASSICAL_SEMANTIC_REQUIREMENTS_ONLY",
            "source_unresolved_graph_requirements": "PROVENANCE_ONLY_NEVER_CLOSURE_PREDICATE",
            "source_narrative_chain_ids": "PROVENANCE_ORDER_ONLY_NEVER_STATE_TRANSITION",
            "unknown_requirement": "FAIL_CLOSED",
            "empty_requirement_set": "FAIL_CLOSED_FOR_MECHANISM_PROPOSAL",
        },
        "proposal_preservation_contract": {
            "candidate_to_proposal_cardinality": "EXACTLY_ONE_TO_ONE",
            "candidate_drop": "FORBIDDEN",
            "candidate_merge": "FORBIDDEN",
            "candidate_split": "FORBIDDEN",
            "proposal_execution": "NOT_RELEASED",
            "rewrite_application": "NOT_RELEASED",
            "proposal_selection": "NOT_RELEASED",
            "proposal_truth": "NOT_RELEASED",
            "proposal_applicability": "NOT_RELEASED_BEYOND_UNIT3_ADMISSION",
            "proposal_conflict_resolution": "NOT_RELEASED",
            "precedence": "NOT_RELEASED",
            "priority": "NOT_RELEASED",
            "winner_loser": "NOT_RELEASED",
            "state_transition": "NOT_RELEASED",
            "lifecycle_truth_gate": "NOT_RELEASED",
            "cross_outer_composition": "NOT_RELEASED",
            "cartesian_expansion": "NOT_RELEASED",
        },
        "record_specific_locks": {
            "ZPZQ-CL-09-005-002": {
                "allocation_semantics_status": "MISSING_PRIMITIVE",
                "compatible_path_enumeration_status": "PARTIALLY_AVAILABLE",
                "participant_path_selection": "NOT_RELEASED",
                "future_owner": "UNIT6_NON_SELECTING_ALLOCATION_ELABORATION",
            },
            "ZPZQ-CL-09-007-002_003": {
                "interaction_chain_resolution_status": "MISSING_PRIMITIVE",
                "source_narrative_order": "PROVENANCE_ONLY",
                "arbitration": "NOT_RELEASED",
            },
            "ZPZQ-CL-09-009-004": {
                "attenuation_grade_status": "MISSING_PRIMITIVE",
                "numeric_grade": "NOT_RELEASED",
                "disposition_synthesis": "FORBIDDEN",
            },
        },
        "hard_exclusions": [
            "APPLIED_SEMANTIC_REWRITE",
            "GRAPH_MUTATION",
            "RELATION_OR_EFFECT_STATE_TRANSITION",
            "SOURCE_CLAIM_ARBITRATION",
            "CONTRADICTION_RESOLUTION",
            "SOURCE_TRUTH_SELECTION",
            "CANDIDATE_TRUTH_OR_APPLICABILITY_SELECTION",
            "CLASSICAL_OPERABILITY_TRUTH",
            "LIFECYCLE_TRUTH_GATE",
            "PRECEDENCE",
            "PRIORITY",
            "WINNER_OR_LOSER",
            "COMPETITION_OR_DOMINANCE_VERDICT",
            "SUPPRESSION",
            "ACTIVATION",
            "DEACTIVATION",
            "RELEASE",
            "CANCELLATION",
            "OVERRIDE",
            "NEGATION",
            "RESCUE_SEMANTICS",
            "NUMERIC_ATTENUATION_STRENGTH_OR_WANGSHUAI_GRADE",
            "PARTICIPANT_OR_PATH_SELECTION",
            "UNIT6_ALLOCATION_ELABORATION",
            "UNIT7_FINAL_EFFECT_CANDIDATE_ENVELOPE",
            "EXECUTABLE_REWRITE_RULES",
            "GRAPH_FIXPOINT_OR_CYCLE_HANDLING",
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
        "# Bazi Classical Semantic Mechanism Proposal & Closure-Gap Governance R1",
        "",
        "- Unit 5 is governance-only: every Unit 4 semantic candidate maps one-to-one to a non-executing mechanism proposal plus explicit closure rows.",
        "- The seven claim-level closure requirements are closed and reuse the #229 six-status runtime dependency vocabulary.",
        "- #229 remains a dependency-status/gap authority only; no candidate-specific lifecycle evidence IDs are inferred or bound in R1.",
        "- `source_unresolved_graph_requirements_provenance` is never a closure predicate; source narrative chain IDs remain provenance order only.",
        "- Unknown or empty candidate closure requirements fail closed rather than implying readiness.",
        "- `005-002` keeps allocation semantics missing and compatible-path enumeration partial; no path is selected.",
        "- `007-002/003` chain resolution remains missing; narrative order does not become state transition or arbitration.",
        "- `009-004` attenuation grade remains missing with no numeric grade or disposition synthesis.",
        "- Proposal execution, rewrite application, truth/applicability, conflict, precedence, winner/loser, state transition, lifecycle truth, cross-outer composition, and Cartesian worlds remain `NOT_RELEASED`.",
        f"- Deterministic Unit 5 contract semantics: `{digest}`.",
        "",
    ))


def validate_release_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    actual = load_json(root / CONTRACT_PATH)
    expected = build_release_contract(root)
    if actual != expected:
        raise TrainingError("Unit 5 mechanism/closure release contract is stale or tampered")
    schema = load_json(root / SCHEMA_PATH)
    runtime_schema = load_json(root / RUNTIME_SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator.check_schema(runtime_schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(actual),
        key=lambda row: list(row.path),
    )
    if errors:
        raise TrainingError(
            f"Unit 5 release contract schema validation failed: {errors[0].message}"
        )
    report_path = root / REPORT_PATH
    expected_report = build_coverage_report(actual)
    if not report_path.is_file() or report_path.read_text(encoding="utf-8") != expected_report:
        raise TrainingError("Unit 5 coverage report is stale or missing")
    return {
        "status": "PASS",
        "audit_id": AUDIT_ID,
        "mechanism_proposal_kind_count": len(
            actual["closed_vocabularies"]["mechanism_proposal_kinds"]
        ),
        "closure_requirement_count": len(
            actual["closed_vocabularies"]["closure_requirement_registry"]
        ),
        "contract_semantics_sha256": actual["determinism"][
            "contract_semantics_sha256"
        ],
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
