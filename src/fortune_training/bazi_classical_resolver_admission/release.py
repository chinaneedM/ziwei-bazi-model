from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from fortune_training.bazi_chart_bound_classical_interaction_projection.release import (
    SCOPE_ARTIFACT_PATH,
    validate_source_scope_artifact,
)
from fortune_training.bazi_classical_effect_constraint_graph.release import (
    CONTRACT_PATH as EFFECT_CONTRACT_PATH,
    validate_release_contract as validate_effect_release_contract,
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

from .dependency import PRIMITIVE_OBSERVATION_ATTRIBUTE
from .profile import (
    ADMISSION_BLOCKER_CLASSES,
    ADMISSION_STATUSES,
    SOURCE_MEMBER_OCCURRENCE_IDS,
    bazi_classical_resolver_admission_strict_r1_profile,
    shen_zpzq_ch09_classical_interaction_r1_profile,
)


AUDIT_ID = "BAZI-CLASSICAL-SOURCE-SEMANTIC-PROFILE-RESOLVER-ADMISSION-R1"
AUDIT_ROOT = Path("audits/bazi-classical-source-semantic-profile-resolver-admission-r1")
CONTRACT_PATH = AUDIT_ROOT / "contract.json"
REPORT_PATH = AUDIT_ROOT / "coverage-report.md"
SCHEMA_PATH = Path("schemas/bazi-classical-source-semantic-profile-resolver-admission-r1.schema.json")
RUNTIME_SCHEMA_PATH = Path("schemas/bazi-classical-resolver-admission-runtime-r1.schema.json")

EXPECTED_EFFECT_CONTRACT_SEMANTICS_SHA256 = "0c6dfccb89710c57f96a762406df32a70395b8fef2bb15ab6654445a22108950"
EXPECTED_SCOPE_SEMANTICS_SHA256 = "949009f0521f3d8710e9f11c1341d0961324f1d6b4f197eeeeb8c25279f2daec"


def build_release_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    effect_release = validate_effect_release_contract(root)
    if effect_release["contract_semantics_sha256"] != EXPECTED_EFFECT_CONTRACT_SEMANTICS_SHA256:
        raise TrainingError("released Unit 2 contract semantic identity changed")
    scope_release = validate_source_scope_artifact(root)
    if scope_release["source_scope_specifications_semantics_sha256"] != EXPECTED_SCOPE_SEMANTICS_SHA256:
        raise TrainingError("released #249 source-scope semantic identity changed")
    scope_artifact = load_json(root / SCOPE_ARTIFACT_PATH)
    exact_ids = tuple(scope_artifact["summary"]["scope_class_source_occurrence_ids"]["EXACT_RUNTIME_SOURCE_SCOPE_SPECIFIED"])
    if exact_ids != SOURCE_MEMBER_OCCURRENCE_IDS:
        raise TrainingError("Unit 3 source semantic partition member universe changed")

    source_profile = shen_zpzq_ch09_classical_interaction_r1_profile()
    admission_profile = bazi_classical_resolver_admission_strict_r1_profile()
    contract = {
        "schema": "BAZI-CLASSICAL-SOURCE-SEMANTIC-PROFILE-RESOLVER-ADMISSION-CONTRACT-R1",
        "audit_id": AUDIT_ID,
        "authority": {
            "unit2_effect_contract_path": EFFECT_CONTRACT_PATH.as_posix(),
            "unit2_effect_contract_semantics_sha256": effect_release["contract_semantics_sha256"],
            "source_scope_artifact_path": SCOPE_ARTIFACT_PATH.as_posix(),
            "source_scope_specifications_semantics_sha256": scope_release["source_scope_specifications_semantics_sha256"],
        },
        "source_semantic_profile": json_value(source_profile),
        "resolver_admission_profile": json_value(admission_profile),
        "closed_vocabularies": {
            "admission_statuses": list(ADMISSION_STATUSES),
            "admission_blocker_classes": list(ADMISSION_BLOCKER_CLASSES),
            "neutral_dependency_observation_map": dict(PRIMITIVE_OBSERVATION_ATTRIBUTE),
        },
        "strict_admission_contract": {
            "partition_match_required": True,
            "structural_binding_class_required": "FULL_EXACT_BINDING_ENUMERATION",
            "residual_unresolved_structural_constraint_ids_required": "EMPTY",
            "source_scope_compatibility_required": "DIRECT_SOURCE_SCOPE_MATCH",
            "declared_neutral_dependencies_required": "EXACTLY_MATERIALIZED",
            "source_unresolved_graph_requirements": "PROVENANCE_ONLY_NEVER_DIRECT_PREDICATE",
            "unresolved_classical_semantic_requirements": "PASS_THROUGH_NOT_SOLVED",
            "lifecycle_global_truth_gate": "NOT_RELEASED",
        },
        "preservation_contract": {
            "one_unit2_envelope_to_one_admission_envelope": True,
            "one_unit2_fragment_to_one_admission_projection": True,
            "fragment_deletion": "FORBIDDEN",
            "fragment_merge": "FORBIDDEN",
            "fragment_selection": "NOT_RELEASED",
            "member_selection_semantics": "NOT_RELEASED",
            "member_coexistence_semantics": "NOT_RELEASED",
            "member_exclusivity_semantics": "NOT_RELEASED",
            "cross_outer_composition": "NOT_RELEASED",
            "cartesian_expansion": "NOT_RELEASED",
        },
        "regression_matrix": [
            {
                "structural_binding_class": "FULL_EXACT_BINDING_ENUMERATION",
                "source_scope_compatibility": "DIRECT_SOURCE_SCOPE_MATCH",
                "expected_status": "ADMITTED_IF_DECLARED_DEPENDENCIES_EXACTLY_MATERIALIZED",
                "required_blockers": [],
            },
            {
                "structural_binding_class": "FULL_EXACT_BINDING_ENUMERATION",
                "source_scope_compatibility": "CROSS_LAYER_EXTENSION_UNRESOLVED",
                "expected_status": "PRESERVED_NOT_ADMITTED",
                "required_blockers": ["CROSS_LAYER_EXTENSION_UNRESOLVED"],
            },
            {
                "structural_binding_class": "PARTIAL_EXACT_BINDING_ENUMERATION",
                "source_scope_compatibility": "DIRECT_SOURCE_SCOPE_MATCH",
                "expected_status": "PRESERVED_NOT_ADMITTED",
                "required_blockers": ["STRUCTURAL_BINDING_PARTIAL"],
            },
            {
                "structural_binding_class": "PARTIAL_EXACT_BINDING_ENUMERATION",
                "source_scope_compatibility": "CROSS_LAYER_EXTENSION_UNRESOLVED",
                "expected_status": "PRESERVED_NOT_ADMITTED",
                "required_blockers": ["STRUCTURAL_BINDING_PARTIAL", "CROSS_LAYER_EXTENSION_UNRESOLVED"],
            },
        ],
        "hard_exclusions": [
            "CANDIDATE_PRESERVING_RESOLVER",
            "SEMANTIC_ATOM",
            "REWRITE_RULE",
            "MECHANISM_CANDIDATE_MATRIX",
            "CLOSURE_GAP_MATRIX",
            "G6_ALLOCATION_ELABORATION",
            "LIFECYCLE_ELIGIBILITY_SOLVING",
            "SOURCE_CLAIM_ARBITRATION",
            "SOURCE_TRUTH_OR_APPLICABILITY_SELECTION",
            "RELATION_OPERABILITY_TRUTH",
            "PRECEDENCE",
            "WINNER_OR_LOSER",
            "CONFLICT_RESOLUTION",
            "SUPPRESSION",
            "ACTIVATION",
            "DEACTIVATION",
            "RELEASE",
            "CANCELLATION",
            "OVERRIDE",
            "NEGATION",
            "RELATION_OR_EFFECT_STATE",
            "GRAPH_REWRITE",
            "FIXPOINT",
            "CYCLE_HANDLING",
            "MONOTONICITY_LATTICE_TERMINATION_SOLVING",
            "FINAL_CLASSICAL_VERDICT",
            "CROSS_SOURCE_COMPOSITION",
            "CARTESIAN_CANDIDATE_WORLD_GENERATION",
        ],
    }
    contract["determinism"] = {"contract_semantics_sha256": object_sha256(contract)}
    return contract


def build_coverage_report(contract: dict[str, Any]) -> str:
    digest = contract["determinism"]["contract_semantics_sha256"]
    return "\n".join((
        "# Bazi Classical Source Semantic Profile & Resolver Admission R1",
        "",
        "- Source semantic profile is partition identity only: Shen `ZPZQ-CH-09`, 13 exact-runtime-scope source records.",
        "- Admission is a sidecar projection over every Unit 2 fragment; no fragment is deleted, merged, ranked, or selected.",
        "- Strict admission requires partition match, FULL exact binding, no residual structural blocker, DIRECT source scope, and exact materialization of every declared neutral primitive.",
        "- PARTIAL and cross-layer-extension cases remain preserved with independent blockers; PARTIAL is never collapsed into a generic unusable state.",
        "- Upstream `source_unresolved_graph_requirements` remains provenance only and is never a direct admission predicate.",
        "- Unresolved Classical semantic requirements pass through admission unchanged and remain unsolved.",
        "- Neutral dependency materialization reuses #249 exact observation bundles; transition-set change and lifecycle truth are not introduced.",
        "- Unit 2 factorized source-record candidate sets preserve selection/coexistence/exclusivity as `NOT_RELEASED`.",
        "- Raw relations remain immutable exact references; no relation/effect truth, precedence, winner, state, rewrite, fixpoint, or final verdict is emitted.",
        f"- Deterministic Unit 3 contract semantics: `{digest}`.",
        "",
    ))


def validate_release_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    actual = load_json(root / CONTRACT_PATH)
    expected = build_release_contract(root)
    if actual != expected:
        raise TrainingError("Classical resolver admission contract is stale or tampered")
    schema = load_json(root / SCHEMA_PATH)
    runtime_schema = load_json(root / RUNTIME_SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator.check_schema(runtime_schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(actual), key=lambda row: list(row.path))
    if errors:
        raise TrainingError(f"Unit 3 release contract schema validation failed: {errors[0].message}")
    report_path = root / REPORT_PATH
    expected_report = build_coverage_report(actual)
    if not report_path.is_file() or report_path.read_text(encoding="utf-8") != expected_report:
        raise TrainingError("Unit 3 coverage report is stale or missing")
    return {
        "status": "PASS",
        "audit_id": AUDIT_ID,
        "source_profile_member_count": len(actual["source_semantic_profile"]["member_source_occurrence_ids"]),
        "admission_status_count": len(actual["closed_vocabularies"]["admission_statuses"]),
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
