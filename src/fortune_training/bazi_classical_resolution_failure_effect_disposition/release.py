from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from fortune_training.bazi_classical_final_effect_candidate_envelope.release import (
    CONTRACT_PATH as UNIT7_CONTRACT_PATH,
    validate_release_contract as validate_unit7_release_contract,
)
from fortune_training.bazi_classical_resolution_effect_disposition.release import (
    CONTRACT_PATH as UNIT8_CONTRACT_PATH,
    validate_release_contract as validate_unit8_release_contract,
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
    CANDIDATE_PROJECTION_STATUSES,
    FRAGMENT_PROJECTION_STATUSES,
    INDEX_SEMANTICS,
    bazi_classical_resolution_failure_effect_disposition_r1_profile,
)


AUDIT_ID = "BAZI-CLASSICAL-CANDIDATE-PRESERVING-RESOLUTION-FAILURE-EFFECT-DISPOSITION-R1"
AUDIT_ROOT = Path("audits/bazi-classical-resolution-failure-effect-disposition-r1")
CONTRACT_PATH = AUDIT_ROOT / "contract.json"
REPORT_PATH = AUDIT_ROOT / "coverage-report.md"
SCHEMA_PATH = Path(
    "schemas/bazi-classical-resolution-failure-effect-disposition-r1.schema.json"
)
RUNTIME_SCHEMA_PATH = Path(
    "schemas/bazi-classical-resolution-failure-effect-disposition-runtime-r1.schema.json"
)

EXPECTED_UNIT7_CONTRACT_SEMANTICS_SHA256 = (
    "41cd0acc91e6fa16ee4bca8ac46e96a7eb42cfe453edde5cab75b0c35b766354"
)
EXPECTED_UNIT8_CONTRACT_SEMANTICS_SHA256 = (
    "3b9e8b124ee00679bc14bfeab4c34fd626f85df20cb029a4670c02c3fc8425f6"
)


def build_release_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    unit7 = validate_unit7_release_contract(root)
    unit8 = validate_unit8_release_contract(root)
    if unit7["contract_semantics_sha256"] != EXPECTED_UNIT7_CONTRACT_SEMANTICS_SHA256:
        raise TrainingError("released Unit 7 contract semantic identity changed")
    if unit8["contract_semantics_sha256"] != EXPECTED_UNIT8_CONTRACT_SEMANTICS_SHA256:
        raise TrainingError("released Unit 8 contract semantic identity changed")

    profile = bazi_classical_resolution_failure_effect_disposition_r1_profile()
    contract = {
        "schema": "BAZI-CLASSICAL-RESOLUTION-FAILURE-EFFECT-DISPOSITION-CONTRACT-R1",
        "audit_id": AUDIT_ID,
        "authority": {
            "unit7_contract_path": UNIT7_CONTRACT_PATH.as_posix(),
            "unit7_contract_semantics_sha256": unit7["contract_semantics_sha256"],
            "unit8_contract_path": UNIT8_CONTRACT_PATH.as_posix(),
            "unit8_contract_semantics_sha256": unit8["contract_semantics_sha256"],
            "unit8_runtime_output_dependency": "NONE_SIBLING_RELEASE_IDENTITY_ONLY",
        },
        "resolution_failure_effect_profile": json_value(profile),
        "closed_vocabularies": {
            "candidate_projection_statuses": list(CANDIDATE_PROJECTION_STATUSES),
            "fragment_projection_statuses": list(FRAGMENT_PROJECTION_STATUSES),
            "index_semantics": INDEX_SEMANTICS,
            "handled_mapping": {
                "semantic_candidate_kind": profile.handled_semantic_candidate_kind,
                "mechanism_proposal_kind": profile.handled_mechanism_proposal_kind,
                "source_claim_edge_class": profile.handled_source_claim_edge_class,
                "effect_facet": profile.handled_effect_facet,
                "disposition_kind": profile.disposition_kind,
                "resolution_mechanism_disposition": (
                    profile.resolution_mechanism_disposition
                ),
            },
        },
        "local_resolution_failure_closure_contract": {
            "closure_requirement_id": profile.failure_closure_requirement_id,
            "expected_upstream_status": profile.expected_upstream_closure_status,
            "unit9_local_closure_result": profile.local_closure_result,
            "semantic_scope": profile.disposition_semantic_scope,
            "mutates_unit5_unit7_or_unit8": False,
            "reversal_reappearance_released": False,
            "interaction_chain_execution_released": False,
            "general_resolver_readiness": "NOT_RELEASED",
        },
        "candidate_projection_contract": {
            "unit7_candidate_to_unit9_projection": "EXACTLY_ONE_TO_ONE",
            "handled_resolution_failure_candidate_to_disposition": "EXACTLY_ONE_TO_ONE",
            "non_resolution_failure_candidate_disposition_count": 0,
            "raw_relation_action": profile.raw_relation_action,
            "raw_relation_presence_semantics": profile.raw_relation_presence_semantics,
            "source_final_candidate": "EXACT_PASS_THROUGH_UNCHANGED",
            "target_relation_restored_state_semantics": (
                profile.target_relation_restored_state_semantics
            ),
        },
        "preservation_contract": {
            "unit7_outer_to_unit9_outer": "EXACTLY_ONE_TO_ONE",
            "unit7_fragment_to_unit9_fragment": "EXACTLY_ONE_TO_ONE",
            "unit7_zero_candidate_fragment": "PRESERVE_ZERO_CANDIDATES",
            "same_effect_channel_candidates": "PRESERVE_SEPARATE_UNRANKED",
            "source_record_factorization": "PRESERVE_EXACT_LINEAGE",
            "source_narrative_order": "PROVENANCE_ONLY_NOT_EXECUTED",
            "source_unresolved_graph_requirements": "PROVENANCE_ONLY",
            "unit8_resolution_candidate_runtime_precondition": "FORBIDDEN",
            "future_reversal_candidate_derived_consequence": "FORBIDDEN",
            "cross_outer_composition": "NOT_RELEASED",
            "cross_source_composition": "NOT_RELEASED",
            "cartesian_expansion": "NOT_RELEASED",
        },
        "unreleased_neighbor_primitives": {
            "CLASSICAL_REVERSAL_OR_REAPPEARANCE_SEMANTICS": "NOT_RELEASED",
            "CLASSICAL_INTERACTION_CHAIN_RESOLUTION": "NOT_RELEASED",
            "CLASSICAL_ATTENUATION_GRADE": "NOT_RELEASED",
            "CLASSICAL_PARTICIPANT_ALLOCATION": "NOT_RELEASED",
            "COMPATIBLE_EXACT_INSTANCE_PATH_ENUMERATION": "NOT_UPGRADED_BY_UNIT9",
        },
        "hard_exclusions": [
            "GENERAL_CLASSICAL_RESOLVER",
            "EXECUTE_UNIT8_RESOLUTION_BEFORE_UNIT9_FAILURE",
            "REVERSAL_OR_REAPPEARANCE_SEMANTICS",
            "SOURCE_NARRATIVE_CHAIN_EXECUTION",
            "TARGET_RELATION_RESTORED_ACTIVE_OR_IN_FORCE_STATE",
            "CANDIDATE_GLOBAL_TRUTH_SELECTION",
            "SOURCE_ARBITRATION_OR_TRUTH_SELECTION",
            "CLASSICAL_OPERABILITY_APPLICABILITY_OR_READINESS",
            "ATTENUATION_GRADE",
            "PARTICIPANT_ALLOCATION_OR_PATH_SELECTION",
            "INFERRED_SLOT_INSTANCE_COMPATIBILITY",
            "COEXISTENCE_OR_EXCLUSIVITY_INFERENCE",
            "CONTRADICTION_OR_CONFLICT_RESOLUTION",
            "PRECEDENCE_OR_PRIORITY",
            "WINNER_OR_LOSER",
            "GLOBAL_SUPPRESSION_ACTIVATION_RELEASE_CANCELLATION_OVERRIDE_NEGATION",
            "RAW_RELATION_DELETION_OR_MUTATION",
            "GRAPH_MUTATION_OR_FIXPOINT",
            "MONOTONICITY_LATTICE_TERMINATION_SOLVER",
            "CROSS_SOURCE_COMPOSITION",
            "CARTESIAN_CANDIDATE_WORLDS",
            "RESOLVED_GLOBAL_CLASSICAL_EFFECT_STATE",
            "FINAL_CLASSICAL_VERDICT",
            "PREDICTION_SEMANTICS",
        ],
    }
    contract["determinism"] = {
        "contract_semantics_sha256": object_sha256(contract)
    }
    return contract


def build_coverage_report(contract: dict[str, Any]) -> str:
    digest = contract["determinism"]["contract_semantics_sha256"]
    return "\n".join((
        "# Bazi Classical Candidate-Preserving Resolution-Failure Effect Disposition R1",
        "",
        "- Unit 9 closes only `CLASSICAL_RESOLUTION_FAILURE_SEMANTICS` as a candidate-local source-asserted failed-resolution effect disposition.",
        "- Failure means the exact source-grounded resolution mechanism is asserted not to hold as resolution; it does not restore or reactivate the target relation.",
        "- Every Unit 7 candidate is preserved exactly once; only resolution-failure candidates emit one Unit 9 disposition.",
        "- Unit 8 remains an independently released sibling; Unit 9 never executes Unit 8 runtime output as a precondition.",
        "- Reversal/reappearance, interaction-chain execution, attenuation, participant allocation, arbitration, readiness, global state and final verdict remain unreleased.",
        f"- Deterministic Unit 9 contract semantics: `{digest}`.",
        "",
    ))


def validate_release_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    actual = load_json(root / CONTRACT_PATH)
    expected = build_release_contract(root)
    if actual != expected:
        raise TrainingError(
            "Unit 9 resolution-failure effect disposition release contract is stale or tampered"
        )
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
            f"Unit 9 release contract schema validation failed: {errors[0].message}"
        )
    report_path = root / REPORT_PATH
    expected_report = build_coverage_report(actual)
    if (
        not report_path.is_file()
        or report_path.read_text(encoding="utf-8") != expected_report
    ):
        raise TrainingError("Unit 9 coverage report is stale or missing")
    return {
        "status": "PASS",
        "audit_id": AUDIT_ID,
        "handled_semantic_candidate_kind": profile_value(
            actual, "handled_semantic_candidate_kind"
        ),
        "contract_semantics_sha256": actual["determinism"][
            "contract_semantics_sha256"
        ],
        "schema_sha256": sha256_file(root / SCHEMA_PATH),
        "runtime_schema_sha256": sha256_file(root / RUNTIME_SCHEMA_PATH),
        "report_sha256": sha256_file(report_path),
    }


def profile_value(contract: dict[str, Any], key: str) -> Any:
    return contract["resolution_failure_effect_profile"][key]


def write_release_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    contract = build_release_contract(root)
    atomic_write_json(root / CONTRACT_PATH, contract)
    atomic_write_bytes(
        root / REPORT_PATH,
        build_coverage_report(contract).encode("utf-8"),
    )
    return validate_release_contract(root)
