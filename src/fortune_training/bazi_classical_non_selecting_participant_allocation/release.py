from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from fortune_training.bazi_classical_effect_semantic_candidate.release import (
    CONTRACT_PATH as UNIT4_CONTRACT_PATH,
    validate_release_contract as validate_unit4_release_contract,
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
    ALLOCATION_DOMAIN_CLASSIFICATIONS,
    ALTERNATIVE_PATH_REQUIREMENT,
    DOMAIN_BLOCKER_IDS,
    EXPECTED_ALLOCATION_CLOSURE_ROWS,
    FRAGMENT_ALLOCATION_STATUSES,
    PATH_CANDIDATE_KIND,
    SLOT_EQUIVALENCE_VALUES,
    bazi_classical_non_selecting_participant_allocation_r1_profile,
)


AUDIT_ID = "BAZI-CLASSICAL-NON-SELECTING-PARTICIPANT-ALLOCATION-R1"
AUDIT_ROOT = Path("audits/bazi-classical-non-selecting-participant-allocation-r1")
CONTRACT_PATH = AUDIT_ROOT / "contract.json"
REPORT_PATH = AUDIT_ROOT / "coverage-report.md"
SCHEMA_PATH = Path("schemas/bazi-classical-non-selecting-participant-allocation-r1.schema.json")
RUNTIME_SCHEMA_PATH = Path("schemas/bazi-classical-non-selecting-participant-allocation-runtime-r1.schema.json")

EXPECTED_UNIT4_CONTRACT_SEMANTICS_SHA256 = "d96ea5a66bea6ff5b71b280723c460954d80ed8da6d05008f909cef30a13a3c8"
EXPECTED_UNIT5_CONTRACT_SEMANTICS_SHA256 = "358fcf00ef1c09321639c0df80e837fc2fd3dba0332cb82aea573b0a13ced998"


def build_release_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    unit4 = validate_unit4_release_contract(root)
    unit5 = validate_unit5_release_contract(root)
    if unit4["contract_semantics_sha256"] != EXPECTED_UNIT4_CONTRACT_SEMANTICS_SHA256:
        raise TrainingError("released Unit 4 contract semantic identity changed")
    if unit5["contract_semantics_sha256"] != EXPECTED_UNIT5_CONTRACT_SEMANTICS_SHA256:
        raise TrainingError("released Unit 5 contract semantic identity changed")

    profile = bazi_classical_non_selecting_participant_allocation_r1_profile()
    contract = {
        "schema": "BAZI-CLASSICAL-NON-SELECTING-PARTICIPANT-ALLOCATION-CONTRACT-R1",
        "audit_id": AUDIT_ID,
        "authority": {
            "unit4_contract_path": UNIT4_CONTRACT_PATH.as_posix(),
            "unit4_contract_semantics_sha256": unit4["contract_semantics_sha256"],
            "unit5_contract_path": UNIT5_CONTRACT_PATH.as_posix(),
            "unit5_contract_semantics_sha256": unit5["contract_semantics_sha256"],
        },
        "allocation_profile": json_value(profile),
        "closed_vocabularies": {
            "allocation_domain_classifications": list(ALLOCATION_DOMAIN_CLASSIFICATIONS),
            "domain_blocker_ids": list(DOMAIN_BLOCKER_IDS),
            "path_candidate_kind": PATH_CANDIDATE_KIND,
            "slot_equivalence_values": list(SLOT_EQUIVALENCE_VALUES),
            "alternative_path_requirement": ALTERNATIVE_PATH_REQUIREMENT,
            "fragment_allocation_statuses": list(FRAGMENT_ALLOCATION_STATUSES),
            "expected_allocation_closure_rows": EXPECTED_ALLOCATION_CLOSURE_ROWS,
        },
        "classification_contract": {
            "EXACT_INSTANCE_SET_CARDINALITY_MATCH": {
                "predicate": "UNIQUE_EXACT_RUNTIME_INSTANCE_COUNT_EQUALS_REQUIRED_SYMBOLIC_CARDINALITY",
                "path_candidate_cardinality": 1,
                "path_candidate_kind": PATH_CANDIDATE_KIND,
                "blocker_ids": [],
                "slot_assignment": "NOT_RELEASED",
                "path_ordering": "NOT_RELEASED",
            },
            "EXACT_INSTANCE_POOL_REQUIRES_COMPATIBILITY_RELATION": {
                "predicate": "UNIQUE_EXACT_RUNTIME_INSTANCE_COUNT_GREATER_THAN_REQUIRED_SYMBOLIC_CARDINALITY",
                "path_candidate_cardinality": 0,
                "blocker_ids": [
                    "SLOT_INSTANCE_COMPATIBILITY_RELATION_NOT_RELEASED",
                    "SYNTHETIC_COMBINATORIAL_ENUMERATION_FORBIDDEN",
                ],
            },
            "INSUFFICIENT_EXACT_INSTANCE_CARDINALITY": {
                "predicate": "UNIQUE_EXACT_RUNTIME_INSTANCE_COUNT_LESS_THAN_REQUIRED_SYMBOLIC_CARDINALITY",
                "path_candidate_cardinality": 0,
                "blocker_ids": ["INSUFFICIENT_EXACT_RUNTIME_INSTANCE_CARDINALITY"],
            },
        },
        "multiplicity_contract": {
            "symbolic_slot_ids": "NON_EMPTY_DISTINCT",
            "required_symbolic_cardinality": "POSITIVE_AND_EQUALS_SYMBOLIC_SLOT_COUNT",
            "exact_runtime_instance_ids": "DISTINCT_EXACT_IDENTITIES",
            "slot_equivalence": "EXCHANGEABLE_SOURCE_EQUIVALENT_ONLY",
            "alternative_path_requirement": ALTERNATIVE_PATH_REQUIREMENT,
            "deduplication_repair": "FORBIDDEN",
            "inferred_default_repair": "FORBIDDEN",
        },
        "preservation_contract": {
            "unit5_outer_to_unit6_outer": "EXACTLY_ONE_TO_ONE",
            "unit5_fragment_to_unit6_fragment": "EXACTLY_ONE_TO_ONE",
            "unit5_proposal_to_unit6_proposal_sidecar": "EXACTLY_ONE_TO_ONE",
            "allocation_multiplicity_reference_to_domain_observation": "EXACTLY_ONE_TO_ONE",
            "non_allocation_proposal_domain_count": 0,
            "zero_proposal_fragment_domain_count": 0,
            "synthetic_permutation_generation": "FORBIDDEN",
            "synthetic_combination_generation": "FORBIDDEN",
            "inferred_slot_instance_compatibility": "FORBIDDEN",
            "participant_path_selection": "NOT_RELEASED",
            "coexistence_exclusivity": "NOT_RELEASED",
            "precedence_priority_winner": "NOT_RELEASED",
            "relation_effect_state": "NOT_RELEASED",
            "rewrite_application": "NOT_RELEASED",
            "cross_outer_composition": "NOT_RELEASED",
            "cartesian_expansion": "NOT_RELEASED",
        },
        "record_specific_locks": {
            "ZPZQ-CL-09-005-002": {
                "slot_equivalence": "EXCHANGEABLE_SOURCE_EQUIVALENT",
                "required_symbolic_cardinality": 2,
                "allocation_closure_status": "MISSING_PRIMITIVE",
                "compatible_path_enumeration_status": "PARTIALLY_AVAILABLE",
                "participant_path_selection": "NOT_RELEASED",
                "synthetic_path_generation": "FORBIDDEN",
            }
        },
        "hard_exclusions": [
            "SYNTHETIC_PERMUTATION_OR_COMBINATION_GENERATION",
            "INFERRED_SLOT_INSTANCE_COMPATIBILITY_RELATION",
            "SLOT_ASSIGNMENT",
            "PATH_ORDERING",
            "PARTICIPANT_OR_PATH_SELECTION",
            "COEXISTENCE_OR_EXCLUSIVITY_INFERENCE",
            "ALLOCATION_TRUTH_OR_OPERABILITY",
            "LIFECYCLE_TRUTH",
            "SOURCE_ARBITRATION",
            "CONFLICT_RESOLUTION",
            "PRECEDENCE",
            "PRIORITY",
            "WINNER_OR_LOSER",
            "SUPPRESSION",
            "ACTIVATION",
            "RELEASE",
            "CANCELLATION",
            "OVERRIDE",
            "RELATION_OR_EFFECT_STATE",
            "APPLIED_REWRITE",
            "GRAPH_MUTATION_OR_FIXPOINT",
            "UNIT7_FINAL_EFFECT_ENVELOPE",
            "CROSS_SOURCE_COMPOSITION",
            "CARTESIAN_CANDIDATE_WORLDS",
            "FINAL_CLASSICAL_VERDICT",
            "PREDICTION_SEMANTICS",
        ],
    }
    contract["determinism"] = {"contract_semantics_sha256": object_sha256(contract)}
    return contract


def build_coverage_report(contract: dict[str, Any]) -> str:
    digest = contract["determinism"]["contract_semantics_sha256"]
    return "\n".join((
        "# Bazi Classical Non-Selecting Participant Allocation Elaboration R1",
        "",
        "- Unit 6 elaborates only multiplicity structure already present in Unit 4 allocation candidates and preserved by Unit 5 governance.",
        "- `PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS` is a preservation requirement, not a compatibility predicate.",
        "- Cardinality match emits exactly one unordered exact-instance-set candidate; a larger instance pool emits zero synthetic paths plus compatibility/synthesis blockers; insufficient cardinality emits zero paths plus a cardinality blocker.",
        "- Exchangeable symbolic slots never authorize permutations, slot assignment, or path ordering.",
        "- Unit 5 allocation closure statuses remain unchanged: allocation semantics `MISSING_PRIMITIVE`, compatible path enumeration `PARTIALLY_AVAILABLE`.",
        "- Non-allocation proposals and zero-proposal fragments remain preserved with zero allocation domains.",
        "- No participant/path selection, truth/operability, precedence/winner, relation/effect state, rewrite, graph mutation, cross-source composition, Cartesian worlds, or final verdict is released.",
        f"- Deterministic Unit 6 contract semantics: `{digest}`.",
        "",
    ))


def validate_release_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    actual = load_json(root / CONTRACT_PATH)
    expected = build_release_contract(root)
    if actual != expected:
        raise TrainingError("Unit 6 allocation release contract is stale or tampered")
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
            f"Unit 6 release contract schema validation failed: {errors[0].message}"
        )
    report_path = root / REPORT_PATH
    expected_report = build_coverage_report(actual)
    if not report_path.is_file() or report_path.read_text(encoding="utf-8") != expected_report:
        raise TrainingError("Unit 6 coverage report is stale or missing")
    return {
        "status": "PASS",
        "audit_id": AUDIT_ID,
        "allocation_domain_classification_count": len(
            actual["closed_vocabularies"]["allocation_domain_classifications"]
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
