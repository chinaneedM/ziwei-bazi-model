#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "docs" / "PROJECT-CURRENT-STATE-R1.json"
PROTOCOL = ROOT / "docs" / "PROJECT-CONTINUITY-PROTOCOL-R1.md"
AUTHORITY = ROOT / "docs" / "FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md"
MATRIX = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"
SOURCE_REGISTRY = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"

EXPECTED_BRANCH = "agent/fusion-chart-core-r1-20260822"
EXPECTED_S00_S19_STATUS = "PROJECT_RESEARCH_CORPUS_NOT_INERRANT_AUTHORITY"


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> int:
    for path in (STATE, PROTOCOL, AUTHORITY, MATRIX, SOURCE_REGISTRY):
        if not path.is_file():
            fail(f"continuity artifact missing: {path.relative_to(ROOT)}")

    state = json.loads(STATE.read_text(encoding="utf-8"))
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    registry = json.loads(SOURCE_REGISTRY.read_text(encoding="utf-8"))

    if state.get("schema") != "ZIWEI-BAZI-PROJECT-CURRENT-STATE-R1":
        fail("project current-state schema mismatch")
    if state.get("development_branch") != EXPECTED_BRANCH:
        fail("project current-state branch mismatch")
    if state.get("github_remote_is_only_live_state_source") is not True:
        fail("GitHub live remote is not declared as the only live state source")
    if state.get("embedded_commit_sha_is_authoritative") is not False:
        fail("current-state file must not treat an embedded SHA as authoritative")
    if state.get("startup_requires_live_remote_refresh") is not True:
        fail("new-chat startup must require live remote refresh")

    authority = state.get("source_authority_policy", {})
    if authority.get("s00_s19_status") != EXPECTED_S00_S19_STATUS:
        fail("S00-S19 epistemic status regressed")
    if authority.get("canonical_path_semantics") != "LEGACY_STORAGE_AND_FREEZE_IDENTITY_NOT_EPISTEMIC_TRUTH":
        fail("canonical path is being conflated with epistemic truth")
    if authority.get("modern_software_status") != "COMPATIBILITY_WITNESS_ONLY":
        fail("modern software authority classification regressed")
    if authority.get("philology_required") is not True:
        fail("philological interpretation requirement regressed")
    if authority.get("terminology_normalization_policy") != "CONTEXTUAL_PHILOLOGY_BEFORE_MECHANICAL_RULE_IDENTITY":
        fail("terminology normalization policy regressed")
    if authority.get("homonym_policy") != "SAME_NAME_DOES_NOT_IMPLY_SAME_RULE_OR_SYSTEM":
        fail("historical homonym separation policy regressed")
    if authority.get("research_scope_policy") != "OPEN_ENDED_CROSS_EDITION_CROSS_REGION_CROSS_LANGUAGE_CROSS_DISCIPLINE":
        fail("open-ended cross-source research scope policy regressed")
    if authority.get("first_source_stop_policy") != "FORBIDDEN_WHEN_MATERIAL_ADDITIONAL_WITNESSES_ARE_SEARCHABLE":
        fail("first-source stopping prohibition regressed")
    if "EVIDENCE_WEIGHTED_NOT_SOURCE_COUNT" not in authority.get("conflict_adjudication_policy", ""):
        fail("evidence-weighted conflict adjudication policy regressed")
    if "DO_NOT_FALSELY_EQUALIZE_DEMONSTRATED_TRANSMISSION_ERRORS" not in authority.get("candidate_preservation_policy", ""):
        fail("false-equivalence prohibition for adjudicated transmission errors regressed")

    matrix_policy = matrix.get("canonical_source_policy", "")
    if "PROJECT_RESEARCH_CORPUS_NOT_INERRANT_AUTHORITY" not in matrix_policy:
        fail("historical matrix still treats S00-S19 as unquestioned authority")
    if matrix.get("research_authority_policy_doc") != "docs/FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md":
        fail("historical matrix is not bound to research authority policy")

    registry_policy = registry.get("authority_policy", "")
    if "not infallible historical authority" not in registry_policy:
        fail("external source registry authority policy regressed")
    if registry.get("research_authority_policy_doc") != "docs/FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md":
        fail("external source registry is not bound to research authority policy")
    source_ids = {item.get("source_id") for item in registry.get("sources", ())}
    for source_id in ("EXT-NDL-OGAWA-SHOUSHI-LICHENG-1673", "EXT-KYUSHU-OGAWA-SHOUSHI-LICHENG-1673"):
        if source_id not in source_ids:
            fail(f"Ogawa continuity source witness missing: {source_id}")

    invariants = state.get("invariants", {})
    if invariants.get("deterministic_fusion_chart_product_r1") != matrix.get("deterministic_product_state"):
        fail("deterministic product state drift between current-state and matrix")
    if invariants.get("ziwei_self_inward_transformation_direction") != matrix.get("self_inward_transformation_state"):
        fail("self/inward transformation state drift between current-state and matrix")

    matrix_summary = matrix.get("inventory_summary", {})
    audit_summary = matrix.get("audit_summary", {})
    audit_state = state.get("historical_audit", {})

    parity = {
        "row_count": matrix_summary.get("row_count"),
        "audited_row_count": matrix_summary.get("audited_row_count"),
        "confirmed_provenance_metadata_defect_count": audit_summary.get("confirmed_provenance_metadata_defect_count"),
        "repaired_provenance_metadata_defect_count": audit_summary.get("repaired_provenance_metadata_defect_count"),
        "historical_candidate_registry_count": audit_summary.get("historical_candidate_registry_count"),
        "historical_candidate_runtime_resolver_count": audit_summary.get("historical_candidate_runtime_resolver_count"),
        "identified_missing_candidate_family_count": audit_summary.get("identified_missing_candidate_family_count"),
    }
    for key, expected in parity.items():
        if audit_state.get(key) != expected:
            fail(f"current-state historical audit parity mismatch for {key}: state={audit_state.get(key)!r} matrix={expected!r}")

    if audit_state.get("completed_batches") != matrix.get("historical_research_batches"):
        fail("current-state completed batch list differs from Historical Audit Matrix")
    required_recent_batches = (
        "BATCH-11-BAZI-OGAWA-1673-NATIVE-EVIDENCE-K",
        "BATCH-11-BAZI-OGAWA-1673-KYUSHU-COLLATION-L",
    )
    for batch_id in required_recent_batches:
        if batch_id not in audit_state.get("completed_batches", ()):
            fail(f"current-state lost recent Ogawa research batch: {batch_id}")
    if not audit_state.get("latest_batch_doc"):
        fail("current-state latest batch document is missing")
    latest_batch_doc = ROOT / audit_state["latest_batch_doc"]
    if not latest_batch_doc.is_file():
        fail(f"current-state latest batch document does not exist: {audit_state['latest_batch_doc']}")
    expected_latest = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-11-BAZI-OGAWA-1673-KYUSHU-COLLATION-L.md"
    if audit_state.get("latest_batch_doc") != expected_latest:
        fail(f"current-state latest batch drift: {audit_state.get('latest_batch_doc')!r}")

    if invariants.get("confirmed_chart_algorithm_defect_count") != audit_summary.get("confirmed_chart_algorithm_defect_count"):
        fail("chart algorithm defect count drift")
    if invariants.get("algorithm_reopen_count") != audit_summary.get("algorithm_reopen_count"):
        fail("algorithm reopen count drift")
    if invariants.get("candidate_collapse_count") != audit_summary.get("candidate_collapse_count"):
        fail("candidate collapse count drift")

    bootstrap = state.get("new_chat_bootstrap_order", ())
    required_bootstrap_fragments = (
        "live GitHub branch HEAD",
        "recent commit history",
        "GitHub Actions",
        "PROJECT-CONTINUITY-PROTOCOL-R1.md",
        "PROJECT-CURRENT-STATE-R1.json",
        "FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md",
    )
    joined = "\n".join(bootstrap)
    for fragment in required_bootstrap_fragments:
        if fragment not in joined:
            fail(f"new-chat bootstrap order missing required step: {fragment}")

    authority_text = AUTHORITY.read_text(encoding="utf-8")
    protocol_text = PROTOCOL.read_text(encoding="utf-8")
    if "Philology / 训诂" not in authority_text or "PHILOLOGICALLY_AMBIGUOUS_PRESERVE_CANDIDATES" not in authority_text:
        fail("research authority policy lost its philology/训诂 method")
    if "Exhaustive research horizon and conflict adjudication" not in authority_text:
        fail("research authority policy lost exhaustive-horizon/conflict-adjudication method")
    if "FIRST_SOURCE_STOP=FORBIDDEN_WHEN_MATERIAL_ADDITIONAL_WITNESSES_ARE_SEARCHABLE" not in authority_text:
        fail("research authority policy lost first-source stopping prohibition")
    if "FALSE_EQUIVALENCE_OF_DEMONSTRATED_TRANSMISSION_ERROR=FORBIDDEN" not in authority_text:
        fail("research authority policy lost false-equivalence prohibition")
    if "Philological continuity rule" not in protocol_text:
        fail("continuity protocol lost philological continuity rule")

    contract = state.get("continuity_contract", {})
    if contract.get("ci_gate_required") is not True:
        fail("continuity CI gate was disabled")
    if contract.get("verifier") != "scripts/verify-project-continuity-state-r1.py":
        fail("continuity verifier identity mismatch")

    print(json.dumps({
        "schema": "ZIWEI-BAZI-PROJECT-CONTINUITY-STATE-R1-GATE",
        "status": "PASS",
        "branch": EXPECTED_BRANCH,
        "stage": state.get("current_stage"),
        "row_count": audit_state.get("row_count"),
        "audited_row_count": audit_state.get("audited_row_count"),
        "completed_batch_count": len(audit_state.get("completed_batches", ())),
        "provenance_defect_count": audit_state.get("confirmed_provenance_metadata_defect_count"),
        "chart_algorithm_defect_count": invariants.get("confirmed_chart_algorithm_defect_count"),
        "s00_s19_status": authority.get("s00_s19_status"),
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
