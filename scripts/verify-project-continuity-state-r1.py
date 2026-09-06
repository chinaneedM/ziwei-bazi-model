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
LATEST_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-11-BAZI-G893-MF-PDF-ROUTE-V.md"
LATEST_MACHINE_EVIDENCE = ROOT / "docs" / "research" / "KYUJANGGAK-G893-MF-PDF-ROUTE-R1.json"

EXPECTED_BRANCH = "agent/fusion-chart-core-r1-20260822"
EXPECTED_S00_S19_STATUS = "PROJECT_RESEARCH_CORPUS_NOT_INERRANT_AUTHORITY"
SUPPLEMENTAL_BATCH_IDS = [
    "BATCH-11-BAZI-G893-1912-1920-PRECIOUS-CATALOG-T",
    "BATCH-11-BAZI-G893-1940-PRECIOUS-CATALOG-U",
    "BATCH-11-BAZI-G893-MF-PDF-ROUTE-V",
]
LATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]
LATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-11-BAZI-G893-MF-PDF-ROUTE-V.md"


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
        "EXT-KYUJANGGAK-PRECIOUS-BOOK-RELATIONS-1940",
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

    # Provenance/access-only batches can advance without changing any Matrix row.
    # The Matrix batch ledger remains an exact prefix; state may append explicitly
    # documented zero-row-effect batches after that prefix.
    matrix_batches = matrix.get("historical_research_batches", [])
    state_batches = audit_state.get("completed_batches", [])
    if state_batches[: len(matrix_batches)] != matrix_batches:
        fail("current-state completed batch prefix differs from Historical Audit Matrix")
    if state_batches[len(matrix_batches) :] != SUPPLEMENTAL_BATCH_IDS:
        fail("unexpected supplemental provenance/access batch list after Historical Audit Matrix prefix")
    if audit_state.get("latest_batch_doc") != LATEST_BATCH_DOC:
        fail(f"current-state latest batch drift: {audit_state.get('latest_batch_doc')!r}")

    if evidence.get("status") != "DIRECT_MF_PDF_ROUTE_CLOSED_NO_DOWNLOADABLE_PDF_OBJECT_OBSERVED":
        fail("Batch 11V machine evidence status mismatch")
    if evidence.get("book_cd") != "GK00893_00" or evidence.get("item_cd") != "SIC" or evidence.get("volume_id") != "0001":
        fail("Batch 11V G893 object/volume binding regressed")
    if evidence.get("catalog_identifier") != "奎貴893" or evidence.get("title") != "授時曆立成":
        fail("Batch 11V G893 title/catalog binding regressed")
    if evidence.get("microfilm_number") != "M/F73-102-37-A":
        fail("Batch 11V microfilm catalog number regressed")
    if evidence.get("ocr_used") is not False:
        fail("Batch 11V no-OCR boundary regressed")

    probe = evidence.get("direct_provider_probe", {})
    initial = probe.get("initial_list_probe", {})
    returned = initial.get("returned_volume", {})
    if initial.get("workflow_run_id") != 34044864073 or initial.get("artifact_id") != 9992787144:
        fail("Batch 11V initial M/F list probe provenance regressed")
    if initial.get("list_transport_http_200") is not True or initial.get("list_result") != "ERROR - DIR NOT EXIST":
        fail("Batch 11V M/F list route result regressed")
    expected_returned = {
        "CALL_NUM": "奎貴893",
        "ORI_TIT": "授時曆立成",
        "BOOK_CD": "GK00893_00",
        "ITEM_CD": "SIC",
        "VOL_NO": "0001",
    }
    for key, expected in expected_returned.items():
        if returned.get(key) != expected:
            fail(f"Batch 11V returned G893 volume metadata regressed for {key}")
    if returned.get("IS_PDF") is not None:
        fail("Batch 11V unexpectedly claims an IS_PDF value")

    direct = probe.get("direct_pdf_control", {})
    if direct.get("workflow_run_id") != 34044991699 or direct.get("artifact_id") != 9992817769:
        fail("Batch 11V direct-PDF control provenance regressed")
    if direct.get("list_result") != "ERROR - DIR NOT EXIST" or direct.get("is_pdf_values") != [None]:
        fail("Batch 11V direct-PDF list-state regressed")
    if direct.get("direct_transport_http_200") is not True:
        fail("Batch 11V direct mfPdf transport no longer records HTTP 200")
    if direct.get("direct_pdf_magic") is not False or direct.get("direct_pdf_returned") is not False:
        fail("Batch 11V must remain closed unless a real PDF object is directly observed")

    adjudication = evidence.get("adjudication", {})
    if adjudication.get("mf_pdf_route_status") != "CLOSED_NO_DOWNLOADABLE_PDF_OBJECT_OBSERVED":
        fail("Batch 11V route closure state regressed")
    if adjudication.get("renderer_route_retried") is not False:
        fail("Batch 11V must remain a distinct M/F route, not a renderer retry")
    if evidence.get("target_status") != "ALL_SIX_PENDING_DIRECT_TARGET_PAGE":
        fail("Batch 11V G893 target-page fail-closed status regressed")

    boundaries = evidence.get("epistemic_boundaries", {})
    required_boundaries = {
        "mf_pdf_ui_marker_as_downloadable_pdf_proof": "FORBIDDEN",
        "microfilm_catalog_number_as_online_pdf_presence": "FORBIDDEN",
        "error_dir_not_exist_as_physical_microfilm_absence": "FORBIDDEN",
        "returned_thumbnail_filename_as_target_folio_binding": "FORBIDDEN",
        "technical_endpoint_success_as_target_glyph_authority": "FORBIDDEN",
    }
    for key, expected in required_boundaries.items():
        if boundaries.get(key) != expected:
            fail(f"Batch 11V epistemic boundary regressed: {key}")

    focus_text = "\n".join(audit_state.get("current_focus", ()))
    for fragment in (
        "Batch 11U",
        "RESOLVED_AT_CATALOG_IDENTIFIER_LEVEL",
        "Batch 11V",
        "ERROR - DIR NOT EXIST",
        "IS_PDF was null",
        "CLOSED_NO_DOWNLOADABLE_PDF_OBJECT_OBSERVED",
        "M/F73-102-37-A",
        "PENDING_DIRECT_TARGET_PAGE",
    ):
        if fragment not in focus_text:
            fail(f"current-state lost Batch 11V continuity boundary: {fragment}")

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
