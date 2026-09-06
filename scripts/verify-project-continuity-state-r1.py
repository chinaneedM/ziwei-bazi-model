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
LATEST_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-11-BAZI-G893-1912-1920-PRECIOUS-CATALOG-T.md"
LATEST_MACHINE_EVIDENCE = ROOT / "docs" / "research" / "KYUJANGGAK-G893-1912-1920-PRECIOUS-CATALOG-R1.json"

EXPECTED_BRANCH = "agent/fusion-chart-core-r1-20260822"
EXPECTED_S00_S19_STATUS = "PROJECT_RESEARCH_CORPUS_NOT_INERRANT_AUTHORITY"
LATEST_BATCH_ID = "BATCH-11-BAZI-G893-1912-1920-PRECIOUS-CATALOG-T"
LATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-11-BAZI-G893-1912-1920-PRECIOUS-CATALOG-T.md"


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> int:
    for path in (STATE, PROTOCOL, AUTHORITY, MATRIX, SOURCE_REGISTRY, LATEST_BATCH, LATEST_MACHINE_EVIDENCE):
        if not path.is_file():
            fail(f"continuity artifact missing: {path.relative_to(ROOT)}")

    state = json.loads(STATE.read_text(encoding="utf-8"))
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    registry = json.loads(SOURCE_REGISTRY.read_text(encoding="utf-8"))
    evidence = json.loads(LATEST_MACHINE_EVIDENCE.read_text(encoding="utf-8"))

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
    required_authority = {
        "s00_s19_status": EXPECTED_S00_S19_STATUS,
        "canonical_path_semantics": "LEGACY_STORAGE_AND_FREEZE_IDENTITY_NOT_EPISTEMIC_TRUTH",
        "modern_software_status": "COMPATIBILITY_WITNESS_ONLY",
        "philology_required": True,
        "terminology_normalization_policy": "CONTEXTUAL_PHILOLOGY_BEFORE_MECHANICAL_RULE_IDENTITY",
        "homonym_policy": "SAME_NAME_DOES_NOT_IMPLY_SAME_RULE_OR_SYSTEM",
        "research_scope_policy": "OPEN_ENDED_CROSS_EDITION_CROSS_REGION_CROSS_LANGUAGE_CROSS_DISCIPLINE",
        "first_source_stop_policy": "FORBIDDEN_WHEN_MATERIAL_ADDITIONAL_WITNESSES_ARE_SEARCHABLE",
    }
    for key, expected in required_authority.items():
        if authority.get(key) != expected:
            fail(f"research authority policy regressed for {key}")
    if "EVIDENCE_WEIGHTED_NOT_SOURCE_COUNT" not in authority.get("conflict_adjudication_policy", ""):
        fail("evidence-weighted conflict adjudication policy regressed")
    if "DO_NOT_FALSELY_EQUALIZE_DEMONSTRATED_TRANSMISSION_ERRORS" not in authority.get("candidate_preservation_policy", ""):
        fail("false-equivalence prohibition regressed")

    if "PROJECT_RESEARCH_CORPUS_NOT_INERRANT_AUTHORITY" not in matrix.get("canonical_source_policy", ""):
        fail("historical matrix still treats S00-S19 as unquestioned authority")
    if matrix.get("research_authority_policy_doc") != "docs/FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md":
        fail("historical matrix is not bound to research authority policy")
    if "not infallible historical authority" not in registry.get("authority_policy", ""):
        fail("external source registry authority policy regressed")
    if registry.get("research_authority_policy_doc") != "docs/FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md":
        fail("external source registry is not bound to research authority policy")

    source_ids = {item.get("source_id") for item in registry.get("sources", ())}
    required_sources = (
        "EXT-NDL-OGAWA-SHOUSHI-LICHENG-1673",
        "EXT-KYUSHU-OGAWA-SHOUSHI-LICHENG-1673",
        "EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893",
        "EXT-LI-LIANG-SUNRISE-TABLES-2022",
        "EXT-KYUJANGGAK-CHILJEONGSAN-NAEPYEON-G894-1444",
        "EXT-NIKH-SEJONG-SILLOK-V156-CHILJEONGSAN-TABLES",
        "EXT-NIKH-CHILJEONGSAN-HISTORY-1444",
    )
    for source_id in required_sources:
        if source_id not in source_ids:
            fail(f"required continuity source witness missing: {source_id}")

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

    # Provenance-only catalog batches can advance without changing any Matrix row.
    # The Matrix batch ledger must remain an exact prefix; state may append explicitly
    # documented, zero-row-effect provenance batches after that prefix.
    matrix_batches = matrix.get("historical_research_batches", [])
    state_batches = audit_state.get("completed_batches", [])
    if state_batches[: len(matrix_batches)] != matrix_batches:
        fail("current-state completed batch prefix differs from Historical Audit Matrix")
    if state_batches[len(matrix_batches) :] != [LATEST_BATCH_ID]:
        fail("unexpected supplemental provenance-only batch list after Historical Audit Matrix prefix")
    if audit_state.get("latest_batch_doc") != LATEST_BATCH_DOC:
        fail(f"current-state latest batch drift: {audit_state.get('latest_batch_doc')!r}")

    if evidence.get("status") != "COMPLETE_DIRECT_NO_OCR_FULL_RENDERER_OBJECT_TITLE_PRESENCE_REVIEW_NEGATIVE_CATALOG_WITNESS_ONLY":
        fail("Batch 11T machine evidence status mismatch")
    coverage = evidence.get("direct_digital_object_access", {}).get("page_coverage_validation", {})
    if coverage.get("valid_image_count") != 75 or coverage.get("missing_page_count") != 0:
        fail("Batch 11T full renderer page coverage regressed")
    if coverage.get("all_pages_valid_image") is not True or coverage.get("all_pages_ocr_false") is not True:
        fail("Batch 11T no-OCR full-image coverage regressed")
    review = evidence.get("direct_visual_review", {})
    if review.get("exact_title_visible") is not False or review.get("short_title_visible") is not False:
        fail("Batch 11T negative title-presence result regressed")
    if evidence.get("target_status") != "ALL_SIX_PENDING_DIRECT_TARGET_PAGE":
        fail("Batch 11T G893 target-page fail-closed status regressed")

    focus_text = "\n".join(audit_state.get("current_focus", ()))
    for fragment in (
        "Batch 11T",
        "GK26787_00",
        "[1912-1920]",
        "NOT SEEN",
        "1936 Rufus",
        "UNRESOLVED",
        "PENDING_DIRECT_TARGET_PAGE",
        "奎26775-v.1-7",
    ):
        if fragment not in focus_text:
            fail(f"current-state lost Batch 11T continuity boundary: {fragment}")

    if invariants.get("confirmed_chart_algorithm_defect_count") != audit_summary.get("confirmed_chart_algorithm_defect_count"):
        fail("chart algorithm defect count drift")
    if invariants.get("algorithm_reopen_count") != audit_summary.get("algorithm_reopen_count"):
        fail("algorithm reopen count drift")
    if invariants.get("candidate_collapse_count") != audit_summary.get("candidate_collapse_count"):
        fail("candidate collapse count drift")

    bootstrap = "\n".join(state.get("new_chat_bootstrap_order", ()))
    for fragment in (
        "live GitHub branch HEAD",
        "recent commit history",
        "GitHub Actions",
        "PROJECT-CONTINUITY-PROTOCOL-R1.md",
        "PROJECT-CURRENT-STATE-R1.json",
        "FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md",
    ):
        if fragment not in bootstrap:
            fail(f"new-chat bootstrap order missing required step: {fragment}")

    authority_text = AUTHORITY.read_text(encoding="utf-8")
    protocol_text = PROTOCOL.read_text(encoding="utf-8")
    if "Philology / 训诂" not in authority_text or "PHILOLOGICALLY_AMBIGUOUS_PRESERVE_CANDIDATES" not in authority_text:
        fail("research authority policy lost philology/训诂 method")
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
        "completed_batch_count": len(state_batches),
        "latest_batch": LATEST_BATCH_ID,
        "provenance_defect_count": audit_state.get("confirmed_provenance_metadata_defect_count"),
        "chart_algorithm_defect_count": invariants.get("confirmed_chart_algorithm_defect_count"),
        "s00_s19_status": authority.get("s00_s19_status"),
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
