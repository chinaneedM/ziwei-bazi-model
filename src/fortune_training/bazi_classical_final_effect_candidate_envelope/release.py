from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from fortune_training.bazi_classical_effect_semantic_candidate.release import (
    CONTRACT_PATH as UNIT4_CONTRACT_PATH,
    validate_release_contract as validate_unit4_release_contract,
)
from fortune_training.bazi_classical_non_selecting_participant_allocation.release import (
    CONTRACT_PATH as UNIT6_CONTRACT_PATH,
    validate_release_contract as validate_unit6_release_contract,
)
from fortune_training.bazi_classical_semantic_closure_governance.release import (
    CONTRACT_PATH as UNIT5_CONTRACT_PATH,
    validate_release_contract as validate_unit5_release_contract,
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
    FRAGMENT_FINAL_STATUSES,
    INDEX_SEMANTICS,
    SEMANTIC_TO_MECHANISM,
    bazi_classical_final_effect_candidate_envelope_r1_profile,
)


AUDIT_ID = "BAZI-CLASSICAL-FINAL-EFFECT-CANDIDATE-ENVELOPE-ASSEMBLY-R1"
AUDIT_ROOT = Path("audits/bazi-classical-final-effect-candidate-envelope-r1")
CONTRACT_PATH = AUDIT_ROOT / "contract.json"
REPORT_PATH = AUDIT_ROOT / "coverage-report.md"
SCHEMA_PATH = Path("schemas/bazi-classical-final-effect-candidate-envelope-r1.schema.json")
RUNTIME_SCHEMA_PATH = Path("schemas/bazi-classical-final-effect-candidate-envelope-runtime-r1.schema.json")

EXPECTED_UNIT4_CONTRACT_SEMANTICS_SHA256 = "d96ea5a66bea6ff5b71b280723c460954d80ed8da6d05008f909cef30a13a3c8"
EXPECTED_UNIT5_CONTRACT_SEMANTICS_SHA256 = "358fcf00ef1c09321639c0df80e837fc2fd3dba0332cb82aea573b0a13ced998"
EXPECTED_UNIT6_CONTRACT_SEMANTICS_SHA256 = "dd85bf571a5cf106321bfb0366ffeee5023563dfe099664fdecaefc3cbe15fea"


def build_release_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    unit4 = validate_unit4_release_contract(root)
    unit5 = validate_unit5_release_contract(root)
    unit6 = validate_unit6_release_contract(root)
    for label, actual, expected in (
        ("Unit 4", unit4["contract_semantics_sha256"], EXPECTED_UNIT4_CONTRACT_SEMANTICS_SHA256),
        ("Unit 5", unit5["contract_semantics_sha256"], EXPECTED_UNIT5_CONTRACT_SEMANTICS_SHA256),
        ("Unit 6", unit6["contract_semantics_sha256"], EXPECTED_UNIT6_CONTRACT_SEMANTICS_SHA256),
    ):
        if actual != expected:
            raise TrainingError(f"released {label} contract semantic identity changed")

    profile = bazi_classical_final_effect_candidate_envelope_r1_profile()
    contract = {
        "schema": "BAZI-CLASSICAL-FINAL-EFFECT-CANDIDATE-ENVELOPE-CONTRACT-R1",
        "audit_id": AUDIT_ID,
        "authority": {
            "unit4_contract_path": UNIT4_CONTRACT_PATH.as_posix(),
            "unit4_contract_semantics_sha256": unit4["contract_semantics_sha256"],
            "unit5_contract_path": UNIT5_CONTRACT_PATH.as_posix(),
            "unit5_contract_semantics_sha256": unit5["contract_semantics_sha256"],
            "unit6_contract_path": UNIT6_CONTRACT_PATH.as_posix(),
            "unit6_contract_semantics_sha256": unit6["contract_semantics_sha256"],
        },
        "final_effect_profile": json_value(profile),
        "closed_vocabularies": {
            "semantic_to_mechanism": SEMANTIC_TO_MECHANISM,
            "fragment_final_statuses": list(FRAGMENT_FINAL_STATUSES),
            "index_semantics": INDEX_SEMANTICS,
        },
        "candidate_assembly_contract": {
            "unit4_candidate_to_unit5_proposal": "EXACTLY_ONE_TO_ONE",
            "unit5_proposal_to_unit6_proposal_sidecar": "EXACTLY_ONE_TO_ONE",
            "unit4_candidate_chain_to_unit7_candidate": "EXACTLY_ONE_TO_ONE",
            "unit5_closure_rows": "EXACT_PASS_THROUGH_UNCHANGED",
            "unit4_multiplicity_references": "EXACT_PASS_THROUGH_UNCHANGED",
            "unit6_allocation_domains": "EXACT_PASS_THROUGH_UNCHANGED",
            "unit6_path_candidates": "EXACT_PASS_THROUGH_NO_SYNTHESIS",
            "non_allocation_unit6_domain_count": 0,
            "execution_readiness_inference": "NOT_RELEASED",
        },
        "preservation_contract": {
            "unit6_outer_to_unit7_outer": "EXACTLY_ONE_TO_ONE",
            "unit6_fragment_to_unit7_fragment": "EXACTLY_ONE_TO_ONE",
            "zero_candidate_fragment": "PRESERVE_ZERO_FINAL_EFFECT_CANDIDATES",
            "same_effect_channel_candidates": "PRESERVE_SEPARATE_UNRANKED",
            "source_record_factorization": "PRESERVE_UNCHANGED",
            "source_narrative_order": "PROVENANCE_ONLY",
            "source_unresolved_graph_requirements": "PROVENANCE_ONLY",
            "synthetic_permutation_generation": "FORBIDDEN",
            "synthetic_combination_generation": "FORBIDDEN",
            "inferred_slot_instance_compatibility": "FORBIDDEN",
            "participant_path_selection": "NOT_RELEASED",
            "coexistence_exclusivity": "NOT_RELEASED",
            "precedence_priority_winner": "NOT_RELEASED",
            "relation_effect_state": "NOT_RELEASED",
            "rewrite_application": "NOT_RELEASED",
            "cross_outer_composition": "NOT_RELEASED",
            "cross_source_composition": "NOT_RELEASED",
            "cartesian_expansion": "NOT_RELEASED",
        },
        "record_specific_locks": {
            "ZPZQ-CL-09-005-002": {
                "semantic_candidates": [
                    "SOURCE_GROUNDED_REVERSAL_OR_REAPPEARANCE_CANDIDATE",
                    "SOURCE_GROUNDED_RESOLUTION_CANDIDATE",
                    "SOURCE_GROUNDED_PARTICIPANT_ALLOCATION_CANDIDATE",
                ],
                "allocation_closure_status": "MISSING_PRIMITIVE",
                "compatible_path_enumeration_status": "PARTIALLY_AVAILABLE",
                "participant_path_selection": "NOT_RELEASED",
                "synthetic_path_generation": "FORBIDDEN",
            }
        },
        "hard_exclusions": [
            "CANDIDATE_TRUTH_SELECTION",
            "EXECUTION_READINESS_INFERENCE",
            "APPLIED_SEMANTIC_REWRITE",
            "EXECUTABLE_REWRITE_RULES",
            "GRAPH_MUTATION_OR_FIXPOINT",
            "MONOTONICITY_LATTICE_TERMINATION_SOLVER",
            "LIFECYCLE_TRUTH",
            "CLASSICAL_OPERABILITY_TRUTH",
            "SOURCE_ARBITRATION_OR_TRUTH_SELECTION",
            "CONTRADICTION_OR_CONFLICT_RESOLUTION",
            "COEXISTENCE_OR_EXCLUSIVITY_INFERENCE",
            "PRECEDENCE",
            "PRIORITY",
            "WINNER_OR_LOSER",
            "SUPPRESSION_OR_ACTIVATION_OR_RELEASE",
            "CANCELLATION_OR_OVERRIDE_OR_NEGATION",
            "PARTICIPANT_OR_PATH_SELECTION",
            "INFERRED_SLOT_INSTANCE_COMPATIBILITY",
            "SYNTHETIC_PERMUTATION_OR_COMBINATION_GENERATION",
            "NUMERIC_ATTENUATION_STRENGTH_OR_WANGSHUAI_GRADE",
            "RELATION_OR_EFFECT_STATE",
            "CROSS_SOURCE_COMPOSITION",
            "CARTESIAN_CANDIDATE_WORLDS",
            "RESOLVED_CLASSICAL_EFFECT_DISPOSITION",
            "FINAL_CLASSICAL_VERDICT",
            "PREDICTION_SEMANTICS",
        ],
    }
    contract["determinism"] = {"contract_semantics_sha256": object_sha256(contract)}
    return contract


def build_coverage_report(contract: dict[str, Any]) -> str:
    digest = contract["determinism"]["contract_semantics_sha256"]
    return "\n".join((
        "# Bazi Classical Final Effect Candidate Envelope Assembly R1",
        "",
        "- Unit 7 is the final pre-resolver assembly layer; `final` describes envelope shape, not Classical truth or verdict.",
        "- Every Unit 4 semantic candidate joins exactly one Unit 5 mechanism proposal and exactly one Unit 6 proposal allocation sidecar.",
        "- Unit 5 closure rows and statuses pass through unchanged; Unit 6 allocation domains/path candidates pass through exactly without synthesis.",
        "- Zero-candidate fragments remain zero-candidate fragments and same-channel candidates remain separate and unranked.",
        "- No execution-readiness inference, truth/operability, precedence/winner, relation/effect state, rewrite, fixpoint, cross-source composition, Cartesian worlds, or final verdict is released.",
        f"- Deterministic Unit 7 contract semantics: `{digest}`.",
        "",
    ))


def validate_release_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    actual = load_json(root / CONTRACT_PATH)
    expected = build_release_contract(root)
    if actual != expected:
        raise TrainingError("Unit 7 final effect envelope release contract is stale or tampered")
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
            f"Unit 7 release contract schema validation failed: {errors[0].message}"
        )
    report_path = root / REPORT_PATH
    expected_report = build_coverage_report(actual)
    if not report_path.is_file() or report_path.read_text(encoding="utf-8") != expected_report:
        raise TrainingError("Unit 7 coverage report is stale or missing")
    return {
        "status": "PASS",
        "audit_id": AUDIT_ID,
        "semantic_candidate_kind_count": len(SEMANTIC_TO_MECHANISM),
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
