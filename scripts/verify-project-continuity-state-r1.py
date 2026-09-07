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
IDENTITY_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-11-BAZI-G893-1940-PRECIOUS-CATALOG-U.md"
IDENTITY_MACHINE_EVIDENCE = ROOT / "docs" / "research" / "KYUJANGGAK-G893-1940-PRECIOUS-CATALOG-IDENTIFIER-BINDING-R1.json"
MF_PDF_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-11-BAZI-G893-MF-PDF-ROUTE-V.md"
MF_PDF_MACHINE_EVIDENCE = ROOT / "docs" / "research" / "KYUJANGGAK-G893-MF-PDF-ROUTE-R1.json"
ARTICLE_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-11-BAZI-G893-LEE-JING-1998-OFFICIAL-ARCHIVE-W.md"
ARTICLE_MACHINE_EVIDENCE = ROOT / "docs" / "research" / "G893-LEE-JING-1998-OFFICIAL-JOURNAL-ARCHIVE-R1.json"
LATEST_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-11-BAZI-G893-OFFICIAL-REPRODUCTION-ROUTE-X.md"
LATEST_MACHINE_EVIDENCE = ROOT / "docs" / "research" / "KYUJANGGAK-G893-OFFICIAL-REPRODUCTION-ROUTE-R1.json"
ZIWEI_LATE_ZI_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-QUANSHU-LATE-ZI-FACSIMILE-A.md"
ZIWEI_LATE_ZI_EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-NANYANGTANG-LATE-ZI-DIRECT-COLLATION-R1.json"
ZIWEI_TIMEKEEPING_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-LATE-ZI-TIMEKEEPING-B.md"
ZIWEI_TIMEKEEPING_EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-LATE-ZI-TIMEKEEPING-COLLATION-R1.json"
ZIWEI_EDITION_ROUTES_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-QUANSHU-INDEPENDENT-EDITION-ROUTES-C.md"
ZIWEI_EDITION_ROUTES_EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-INDEPENDENT-EDITION-ROUTES-R1.json"
ZIWEI_WENGUANG_INDEX_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-QUANSHU-WENGUANG-INDEX-PREVIEW-D.md"
ZIWEI_WENGUANG_INDEX_EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-WENGUANG-GOOGLE-INDEX-PREVIEW-R1.json"
ZIWEI_JINGLUNTANG_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-QUANSHU-JINGLUNTANG-PHYSICAL-ROUTE-E.md"
ZIWEI_JINGLUNTANG_EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-JINGLUNTANG-PHYSICAL-ROUTE-R1.json"
ZIWEI_POST_E_ROUTES_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-QUANSHU-WENCHENGTANG-DALIAN-COLLATION-ROUTES-F.md"
ZIWEI_POST_E_ROUTES_EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-WENCHENGTANG-DALIAN-COLLATION-ROUTES-R1.json"
ZIWEI_QUANJI_LATE_ZI_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-QUANJI-LIANYUANGE-LATE-ZI-COLLATION-G.md"
ZIWEI_QUANJI_LATE_ZI_EVIDENCE = ROOT / "docs/research/ZIWEI-QUANJI-LIANYUANGE-LATE-ZI-COLLATION-R1.json"

EXPECTED_BRANCH = "agent/fusion-chart-core-r1-20260822"
EXPECTED_S00_S19_STATUS = "PROJECT_RESEARCH_CORPUS_NOT_INERRANT_AUTHORITY"
SUPPLEMENTAL_BATCH_IDS = [
    "BATCH-11-BAZI-G893-1912-1920-PRECIOUS-CATALOG-T",
    "BATCH-11-BAZI-G893-1940-PRECIOUS-CATALOG-U",
    "BATCH-11-BAZI-G893-MF-PDF-ROUTE-V",
    "BATCH-11-BAZI-G893-LEE-JING-1998-OFFICIAL-ARCHIVE-W",
    "BATCH-11-BAZI-G893-OFFICIAL-REPRODUCTION-ROUTE-X",
    "BATCH-12-ZIWEI-QUANSHU-LATE-ZI-FACSIMILE-A",
    "BATCH-12-ZIWEI-LATE-ZI-TIMEKEEPING-B",
    "BATCH-12-ZIWEI-QUANSHU-INDEPENDENT-EDITION-ROUTES-C",
    "BATCH-12-ZIWEI-QUANSHU-WENGUANG-INDEX-PREVIEW-D",
    "BATCH-12-ZIWEI-QUANSHU-JINGLUNTANG-PHYSICAL-ROUTE-E",
    "BATCH-12-ZIWEI-QUANSHU-WENCHENGTANG-DALIAN-COLLATION-ROUTES-F",
    "BATCH-12-ZIWEI-QUANJI-LIANYUANGE-LATE-ZI-COLLATION-G",
]
LATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]
LATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-QUANJI-LIANYUANGE-LATE-ZI-COLLATION-G.md"


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> int:
    for path in (STATE, PROTOCOL, AUTHORITY, MATRIX, SOURCE_REGISTRY, IDENTITY_BATCH, IDENTITY_MACHINE_EVIDENCE, MF_PDF_BATCH, MF_PDF_MACHINE_EVIDENCE, ARTICLE_BATCH, ARTICLE_MACHINE_EVIDENCE, LATEST_BATCH, LATEST_MACHINE_EVIDENCE, ZIWEI_LATE_ZI_BATCH, ZIWEI_LATE_ZI_EVIDENCE, ZIWEI_TIMEKEEPING_BATCH, ZIWEI_TIMEKEEPING_EVIDENCE, ZIWEI_EDITION_ROUTES_BATCH, ZIWEI_EDITION_ROUTES_EVIDENCE, ZIWEI_WENGUANG_INDEX_BATCH, ZIWEI_WENGUANG_INDEX_EVIDENCE, ZIWEI_JINGLUNTANG_BATCH, ZIWEI_JINGLUNTANG_EVIDENCE, ZIWEI_POST_E_ROUTES_BATCH, ZIWEI_POST_E_ROUTES_EVIDENCE, ZIWEI_QUANJI_LATE_ZI_BATCH, ZIWEI_QUANJI_LATE_ZI_EVIDENCE):
        if not path.is_file():
            fail(f"continuity artifact missing: {path.relative_to(ROOT)}")

    state = json.loads(STATE.read_text(encoding="utf-8"))
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    registry = json.loads(SOURCE_REGISTRY.read_text(encoding="utf-8"))
    identity_evidence = json.loads(IDENTITY_MACHINE_EVIDENCE.read_text(encoding="utf-8"))
    mf_pdf_evidence = json.loads(MF_PDF_MACHINE_EVIDENCE.read_text(encoding="utf-8"))
    article_evidence = json.loads(ARTICLE_MACHINE_EVIDENCE.read_text(encoding="utf-8"))
    evidence = json.loads(LATEST_MACHINE_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_late_zi_evidence = json.loads(ZIWEI_LATE_ZI_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_timekeeping_evidence = json.loads(ZIWEI_TIMEKEEPING_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_edition_routes_evidence = json.loads(ZIWEI_EDITION_ROUTES_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_wenguang_index_evidence = json.loads(ZIWEI_WENGUANG_INDEX_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_jingluntang_evidence = json.loads(ZIWEI_JINGLUNTANG_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_post_e_routes_evidence = json.loads(ZIWEI_POST_E_ROUTES_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_quanji_late_zi_evidence = json.loads(ZIWEI_QUANJI_LATE_ZI_EVIDENCE.read_text(encoding="utf-8"))

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
        "EXT-GOOGLE-BOOKS-JIELAN-WENCHENGTANG-COLLATION-INDEX",
        "EXT-DESTINYNET-ZWDSQJ-LATE-ZI-RECEIVED-TRANSCRIPTION",
        "EXT-GOOGLE-BOOKS-JIELAN-LIANYUANGE-QUANJI-INDEX",
        "EXT-XINYITANG-JIELAN-LIANYUANGE-QUANJI-COLLATION",
        "EXT-DALIAN-LIB-ZWDSQS-GUANGYI-MINGUO",
        "EXT-GUOXUEDASHI-ZWDSQS-WENCHENGTANG-LIAONING-LOCATOR",
        "EXT-NANKAI-LNLIB-GUJI-LEGACY-ROUTE",
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

    # Batch 11U remains the controlling catalog-item identity gate.
    if identity_evidence.get("status") != "DIRECT_NO_OCR_1940_PRECIOUS_BOOK_NUMBER_893_BINDING_CLOSES_CATALOG_ITEM_CONTINUITY":
        fail("Batch 11U machine evidence status mismatch")
    source_object = identity_evidence.get("source_object", {})
    if source_object.get("book_cd") != "GK26786_00" or source_object.get("item_cd") != "BBG":
        fail("Batch 11U 1940 provider-object binding regressed")
    if source_object.get("renderer_page_count") != 148 or source_object.get("ocr_used") is not False:
        fail("Batch 11U 1940 renderer/no-OCR controls regressed")
    header = identity_evidence.get("internal_catalog_header", {})
    if header.get("page_id") != "0125" or header.get("visible_title") != "奎章閣貴重圖書目錄":
        fail("Batch 11U internal precious-catalog header binding regressed")
    for field in ("書名", "圖書番號", "冊數", "備考"):
        if field not in header.get("visible_field_headers", ()):
            fail(f"Batch 11U lost direct table-field header: {field}")
    entry = identity_evidence.get("direct_entry_binding", {})
    target_entry = entry.get("target_entry", {})
    adjacent = entry.get("adjacent_control_entry", {})
    if entry.get("page_id") != "0129":
        fail("Batch 11U target-entry page binding regressed")
    if target_entry.get("title") != "授時曆立成" or target_entry.get("book_number") != 893 or target_entry.get("volume_count") != 1:
        fail("Batch 11U 授時曆立成 / 圖書番號 893 direct reading regressed")
    if adjacent.get("title") != "授時曆捷法立成" or adjacent.get("book_number") != 892:
        fail("Batch 11U adjacent Kang-Bo control regressed")
    current_binding = identity_evidence.get("current_object_binding", {})
    if current_binding.get("current_catalog_identifier") != "奎貴893" or current_binding.get("current_book_cd") != "GK00893_00":
        fail("Batch 11U current G893 binding regressed")
    if current_binding.get("exact_item_continuity_to_current_gk00893_00") != "RESOLVED_AT_CATALOG_IDENTIFIER_LEVEL":
        fail("Batch 11U catalog-item continuity closure regressed")
    control_1930 = identity_evidence.get("1930_control", {})
    if control_1930.get("generic_numeric_order_893_as_current_precious_893") != "DISPROVEN_BY_DIRECT_1930_PAGE_READING":
        fail("Batch 11U 1930 generic-number disproof regressed")
    if identity_evidence.get("target_status") != "ALL_SIX_PENDING_DIRECT_TARGET_PAGE":
        fail("Batch 11U G893 target-page fail-closed status regressed")

    if mf_pdf_evidence.get("status") != "DIRECT_MF_PDF_ROUTE_CLOSED_NO_DOWNLOADABLE_PDF_OBJECT_OBSERVED":
        fail("Batch 11V machine mf_pdf_evidence status mismatch")
    if mf_pdf_evidence.get("book_cd") != "GK00893_00" or mf_pdf_evidence.get("item_cd") != "SIC" or mf_pdf_evidence.get("volume_id") != "0001":
        fail("Batch 11V G893 object/volume binding regressed")
    if mf_pdf_evidence.get("catalog_identifier") != "奎貴893" or mf_pdf_evidence.get("title") != "授時曆立成":
        fail("Batch 11V G893 title/catalog binding regressed")
    if mf_pdf_evidence.get("microfilm_number") != "M/F73-102-37-A":
        fail("Batch 11V microfilm catalog number regressed")
    if mf_pdf_evidence.get("ocr_used") is not False:
        fail("Batch 11V no-OCR boundary regressed")

    probe = mf_pdf_evidence.get("direct_provider_probe", {})
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

    adjudication = mf_pdf_evidence.get("adjudication", {})
    if adjudication.get("mf_pdf_route_status") != "CLOSED_NO_DOWNLOADABLE_PDF_OBJECT_OBSERVED":
        fail("Batch 11V route closure state regressed")
    if adjudication.get("renderer_route_retried") is not False:
        fail("Batch 11V must remain a distinct M/F route, not a renderer retry")
    if mf_pdf_evidence.get("target_status") != "ALL_SIX_PENDING_DIRECT_TARGET_PAGE":
        fail("Batch 11V G893 target-page fail-closed status regressed")

    boundaries = mf_pdf_evidence.get("epistemic_boundaries", {})
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

    # Batch 11W upgrades the 1998 specialist paper to a direct official record/abstract witness.
    if article_evidence.get("status") != "DIRECT_OFFICIAL_JOURNAL_RECORD_AND_ABSTRACT_BOUND_FULLTEXT_REMAINS_CNKI_ROUTED_NO_TARGET_PAGE_EXPOSED":
        fail("Batch 11W machine article_evidence status mismatch")
    archive = article_evidence.get("official_archive", {})
    if archive.get("paper_uuid") != "5c4276d953bd47ca2679c70209d179cf":
        fail("Batch 11W official paper UUID regressed")
    if archive.get("title") != "朝鲜奎章阁本的《授时历立成》" or archive.get("authors") != ["李银姬", "景冰"]:
        fail("Batch 11W title/author identity regressed")
    if archive.get("year_id") != "adaf0591-da7f-47b1-a26b-f97893bc2011" or archive.get("issue_id") != "081bfc10-b643-4702-9389-346193d8815e":
        fail("Batch 11W official 1998-02 issue binding regressed")
    if archive.get("cnki_node_id") != "ZGKS802.008":
        fail("Batch 11W CNKI node binding regressed")
    if archive.get("paper_html_sha256") != "e36670c425afd627551d25acec219eb1b4c7cb4285edef6aceff83adaf454825":
        fail("Batch 11W official paper HTML digest regressed")
    access = article_evidence.get("access_boundary", {})
    if access.get("official_portal_abstract_visible") is not True or access.get("official_portal_references_visible") is not True:
        fail("Batch 11W direct official abstract/reference surface regressed")
    if access.get("official_portal_fulltext_visible") is not False or access.get("full_article_directly_retrieved") is not False:
        fail("Batch 11W must not claim direct full-article retrieval")
    if access.get("public_target_figure_exposed_on_official_portal") is not False:
        fail("Batch 11W must not claim a public target figure")
    if article_evidence.get("paywall_or_auth_bypass_attempted") is not False:
        fail("Batch 11W access-boundary control regressed")
    if article_evidence.get("target_status") != "ALL_SIX_PENDING_DIRECT_TARGET_PAGE":
        fail("Batch 11W G893 target-page fail-closed status regressed")

    lee_source = next(
        (item for item in registry.get("sources", ()) if item.get("source_id") == "EXT-LEE-JING-KYUJANGGAK-SHOUSHI-LICHENG-1998"),
        None,
    )
    if not lee_source:
        fail("Batch 11W Lee/Jing source registry entry missing")
    official_binding = lee_source.get("official_archive_binding", {})
    if official_binding.get("paper_uuid") != "5c4276d953bd47ca2679c70209d179cf" or official_binding.get("cnki_node_id") != "ZGKS802.008":
        fail("Batch 11W source-registry official archive binding regressed")
    if lee_source.get("target_effect") != "NONE_ALL_SIX_PENDING_DIRECT_TARGET_PAGE":
        fail("Batch 11W source-registry target-effect boundary regressed")

    # Batch 11X binds the official institutional reproduction route without claiming fulfillment.
    if evidence.get("status") != "OFFICIAL_REPRODUCTION_APPLICATION_ROUTE_DIRECTLY_CONFIRMED_REQUEST_NOT_SUBMITTED":
        fail("Batch 11X machine evidence status mismatch")
    obj = evidence.get("g893_object", {})
    if obj.get("catalog_identifier") != "奎貴893" or obj.get("book_cd") != "GK00893_00":
        fail("Batch 11X G893 object identity regressed")
    if obj.get("microfilm_number") != "M/F73-102-37-A" or obj.get("reproduction_request_ui_visible") is not True:
        fail("Batch 11X object-specific reproduction route regressed")
    service = evidence.get("official_service_notice", {}).get("direct_observations", {})
    if service.get("microfilm_method") != "MICROFILM_SCAN_PDF_UPLOADED_TO_HOMEPAGE":
        fail("Batch 11X official microfilm PDF publication method regressed")
    if service.get("procedure") != ["HOMEPAGE", "SEARCH_MATERIAL", "REPRODUCTION_REQUEST", "CHECK_APPROVAL_EMAIL"]:
        fail("Batch 11X official application procedure regressed")
    if service.get("normal_processing_period") != "WITHIN_2_WEEKS_OF_APPLICATION_UNLESS_DELAY_SEPARATELY_NOTIFIED":
        fail("Batch 11X processing-period statement regressed")
    nonmember = evidence.get("nonmember_cart_surface", {})
    if nonmember.get("observed_service_change_effective_date") != "2024-02-01":
        fail("Batch 11X 2024 service-change date regressed")
    if "MICROFILM_SCAN_PDF" not in nonmember.get("observed_change", ""):
        fail("Batch 11X non-member PDF-publication transition regressed")
    if evidence.get("external_application_submitted") is not False or evidence.get("approval_received") is not False:
        fail("Batch 11X must not claim a submitted or approved request")
    route = evidence.get("route_adjudication", {})
    if route.get("g893_request_acceptance") != "UNTESTED" or route.get("whole_volume_vs_selected_pages") != "UNRESOLVED_UNTIL_REQUEST_FORM_OR_APPROVAL":
        fail("Batch 11X fulfillment uncertainty regressed")
    if route.get("fee_or_charge") != "NOT_STATED_IN_REVIEWED_OFFICIAL_NOTICE_DO_NOT_INFER_FREE":
        fail("Batch 11X fee boundary regressed")
    if evidence.get("target_status") != "ALL_SIX_PENDING_DIRECT_TARGET_PAGE":
        fail("Batch 11X target-page fail-closed status regressed")
    g893_source = next(
        (item for item in registry.get("sources", ()) if item.get("source_id") == "EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893"),
        None,
    )
    if not g893_source:
        fail("Batch 11X G893 registry source missing")
    reproduction = g893_source.get("official_reproduction_route", {})
    if reproduction.get("status") != "DIRECTLY_CONFIRMED_REQUEST_NOT_SUBMITTED" or reproduction.get("request_submitted") is not False:
        fail("Batch 11X registry reproduction route regressed")
    if reproduction.get("target_effect") != "NONE_ALL_SIX_PENDING_DIRECT_TARGET_PAGE":
        fail("Batch 11X registry target boundary regressed")

    if ziwei_late_zi_evidence.get("batch_id") != "BATCH-12-ZIWEI-QUANSHU-LATE-ZI-FACSIMILE-A":
        fail("Batch 12A Ziwei late-Zi evidence batch identity mismatch")
    source_obj = ziwei_late_zi_evidence.get("source_object", {})
    if source_obj.get("pdf_sha256") != "32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7" or source_obj.get("pdf_page_count") != 527:
        fail("Batch 12A Ziwei Fullbook PDF identity regressed")
    direct = ziwei_late_zi_evidence.get("direct_collation", {})
    if direct.get("pdf_page_1_based") != 320 or direct.get("heading") != "論人生時要審的確":
        fail("Batch 12A target-section binding regressed")
    if direct.get("s01_claimed_sentence_status") != "NOT_OBSERVED_ON_DIRECT_TARGET_SECTION_PAGE" or direct.get("whole_volume_negative_claim_authorized") is not False:
        fail("Batch 12A S01 exact-quotation scope firewall regressed")
    philology = ziwei_late_zi_evidence.get("philological_adjudication", {})
    if philology.get("candidate_method_id") != "NANYANGTANG-FULLBOOK-ZI-TEN-KE-HAI-SPLIT-R1":
        fail("Batch 12A candidate identity regressed")
    if philology.get("runtime_capability_status") != "MISSING_FROM_PRODUCT" or philology.get("runtime_selection_authorized") is not False:
        fail("Batch 12A missing-product / no-selection boundary regressed")
    nanyang_source = next((item for item in registry.get("sources", ()) if item.get("source_id") == "EXT-ZIWEI-QUANSHU-NANYANGTANG-SCAN"), None)
    if not nanyang_source or nanyang_source.get("pdf_sha256") != "32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7":
        fail("Batch 12A external-source registry binding regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("audit_status") != "MISSING_FROM_PRODUCT" or nanyang_row.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12A HPA-ZDATE-006 continuity boundary regressed")

    if ziwei_timekeeping_evidence.get("batch_id") != "BATCH-12-ZIWEI-LATE-ZI-TIMEKEEPING-B":
        fail("Batch 12B Ziwei timekeeping evidence batch identity mismatch")
    adjudication = ziwei_timekeeping_evidence.get("adjudication", {})
    if adjudication.get("upper_half_orientation") != "BEFORE_MIDNIGHT_PREVIOUS_DAY" or adjudication.get("lower_half_orientation") != "AFTER_MIDNIGHT_CURRENT_DAY":
        fail("Batch 12B generic upper/lower-half orientation regressed")
    if adjudication.get("ten_ke_equal_duration_interpretation") != "REJECTED":
        fail("Batch 12B ten-ke equal-duration interpretation firewall regressed")
    if adjudication.get("runtime_time_standard_binding") != "UNRESOLVED":
        fail("Batch 12B runtime time-standard was prematurely selected")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("timekeeping_orientation_status") != "CLOSED_AT_GENERIC_FIXED_SHICHEN_LEVEL":
        fail("Batch 12B matrix timekeeping status regressed")
    if nanyang_row.get("audit_status") != "MISSING_FROM_PRODUCT" or nanyang_row.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12B candidate/product boundary regressed")

    if ziwei_edition_routes_evidence.get("batch_id") != "BATCH-12-ZIWEI-QUANSHU-INDEPENDENT-EDITION-ROUTES-C":
        fail("Batch 12C Ziwei edition-route evidence batch identity mismatch")
    route_workflow = ziwei_edition_routes_evidence.get("research_workflow", {})
    if route_workflow.get("workflow_run_id") != 34120317222 or route_workflow.get("artifact_id") != 10017909080:
        fail("Batch 12C exact workflow/artifact provenance regressed")
    wenguang = ziwei_edition_routes_evidence.get("heart_one_wenguangtang_facsimile", {})
    if wenguang.get("isbn") != "9789888266944" or wenguang.get("official_probe", {}).get("http_status") != 200:
        fail("Batch 12C Wenguangtang facsimile identity regressed")
    if {row.get("name") for row in wenguang.get("publisher_described_base_copies", ())} != {"敦化堂刊本", "繼述堂刊本"}:
        fail("Batch 12C Dunhuatang/Jishutang base-copy identity regressed")
    wencheng = ziwei_edition_routes_evidence.get("wenchengtang_route", {})
    if wencheng.get("relation_to_wenguangtang_family") != "SEPARATE_QING_FULLBOOK_EDITION_ROUTE":
        fail("Batch 12C Wenchengtang independence boundary regressed")
    preview = ziwei_edition_routes_evidence.get("public_preview_controls", {}).get("books_preview_image_urls", {})
    if preview.get("attempted_count") != 13 or preview.get("http_403_count") != 13 or preview.get("saved_image_count") != 0:
        fail("Batch 12C public-preview access controls regressed")
    route_adjudication = ziwei_edition_routes_evidence.get("adjudication", {})
    if route_adjudication.get("independent_physical_target_page_status") != "NO_INDEPENDENT_TARGET_PAGE_OBSERVED":
        fail("Batch 12C incorrectly claims a physical target page")
    if route_adjudication.get("hai_glyph_stability_across_physical_editions") != "UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES":
        fail("Batch 12C HAI glyph stability boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("hai_glyph_cross_edition_status") != "UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES":
        fail("Batch 12C matrix HAI glyph boundary regressed")
    if nanyang_row.get("audit_status") != "MISSING_FROM_PRODUCT" or nanyang_row.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12C candidate/product boundary regressed")

    if ziwei_wenguang_index_evidence.get("batch_id") != "BATCH-12-ZIWEI-QUANSHU-WENGUANG-INDEX-PREVIEW-D":
        fail("Batch 12D Ziwei Wenguang index evidence batch identity mismatch")
    distribution = ziwei_wenguang_index_evidence.get("distribution_volume", {})
    if distribution.get("volume_id") != "aIRbDgAAQBAJ" or distribution.get("isbn") != "9789888266944" or distribution.get("declared_page_count") != 266:
        fail("Batch 12D Google distribution identity regressed")
    search_index = ziwei_wenguang_index_evidence.get("public_search_index", {})
    if search_index.get("workflow_run_id") != 34121750009 or search_index.get("artifact_id") != 10018452113:
        fail("Batch 12D search-index provenance regressed")
    if search_index.get("target_heading_query", {}).get("target_page_id") != "PT165":
        fail("Batch 12D target PT165 binding regressed")
    reading = search_index.get("target_index_reading", "")
    if "上五刻" not in reading or "下五刻" not in reading or "亥時" not in reading:
        fail("Batch 12D target index text regressed")
    if search_index.get("target_index_reading_authority") != "SEARCH_INDEX_TEXT_ONLY_NOT_PHYSICAL_GLYPH_AUTHORITY":
        fail("Batch 12D index/glyph authority boundary regressed")
    if search_index.get("negative_textual_claim_authorized") is not False:
        fail("Batch 12D zero-result negative-proof firewall regressed")
    viewer = ziwei_wenguang_index_evidence.get("embedded_viewer_control", {})
    if viewer.get("workflow_run_id") != 34123161798 or viewer.get("artifact_id") != 10019011766:
        fail("Batch 12D Embedded Viewer provenance regressed")
    if viewer.get("go_to_pt165_returned") is not True or viewer.get("after_page_id") != "PT166" or viewer.get("target_page_directly_observed") is not False:
        fail("Batch 12D viewer fail-closed state regressed")
    adjudication12d = ziwei_wenguang_index_evidence.get("adjudication", {})
    if adjudication12d.get("pt165_base_copy_identity") != "UNRESOLVED_DUNHUATANG_VS_JISHUTANG":
        fail("Batch 12D PT165 base-copy identity was prematurely closed")
    if adjudication12d.get("hai_glyph_stability_across_physical_editions") != "UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES":
        fail("Batch 12D HAI glyph stability boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("combined_facsimile_volume_id") != "aIRbDgAAQBAJ" or nanyang_row.get("combined_facsimile_target_index_page_id") != "PT165":
        fail("Batch 12D matrix Google index binding regressed")
    if nanyang_row.get("combined_facsimile_target_image_status") != "PUBLIC_EMBEDDED_VIEWER_DID_NOT_DISPLAY_TARGET_GLYPHS":
        fail("Batch 12D matrix viewer boundary regressed")
    if nanyang_row.get("audit_status") != "MISSING_FROM_PRODUCT" or nanyang_row.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12D candidate/product boundary regressed")

    if ziwei_jingluntang_evidence.get("batch_id") != "BATCH-12-ZIWEI-QUANSHU-JINGLUNTANG-PHYSICAL-ROUTE-E":
        fail("Batch 12E Ziwei Jingluntang evidence batch identity mismatch")
    shlib = ziwei_jingluntang_evidence.get("shanghai_library", {})
    if shlib.get("instance_id") != "1pjr6vy1ffsq3l1y" or shlib.get("identifier") != "子30814110" or shlib.get("edition_label") != "清經綸堂刻本":
        fail("Batch 12E SHLIB Jingluntang identity regressed")
    if shlib.get("public_content_negotiation", {}).get("jsonld", {}).get("http_status") != 200:
        fail("Batch 12E SHLIB JSON-LD route regressed")
    if shlib.get("anonymous_route_controls", {}).get("dhapi_pdfview_root", {}).get("http_status") != 412:
        fail("Batch 12E SHLIB anonymous digital-object boundary regressed")
    token_scan = shlib.get("public_metadata_token_scan", {})
    if any(token_scan.get(key) for key in ("iiif", "manifest", "itemid", "itemId", "dhapi", "pdfview")):
        fail("Batch 12E SHLIB metadata unexpectedly exposes a page object")
    kumyo = ziwei_jingluntang_evidence.get("kumyo_physical_copy", {})
    if kumyo.get("auction_no") != "BBAA18036" or kumyo.get("unique_embedded_physical_image_count") != 8:
        fail("Batch 12E Kumyo physical-copy identity regressed")
    if len(kumyo.get("unique_image_sha256", ())) != 8 or len(set(kumyo.get("unique_image_sha256", ()))) != 8:
        fail("Batch 12E Kumyo unique image digest set regressed")
    if kumyo.get("jingluntang_label_visibly_observed") is not True:
        fail("Batch 12E Kumyo Jingluntang label visual-review boundary regressed")
    if kumyo.get("target_heading_observed") is not False or kumyo.get("target_hai_glyph_observed") is not False:
        fail("Batch 12E incorrectly claims the late-Zi target page")
    adjudication12e = ziwei_jingluntang_evidence.get("adjudication", {})
    if adjudication12e.get("jingluntang_edition_family_identity") != "CLOSED_AT_LIBRARY_AND_PUBLIC_PHYSICAL_COPY_LEVEL":
        fail("Batch 12E Jingluntang identity closure regressed")
    if adjudication12e.get("hai_glyph_stability_across_physical_editions") != "UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES":
        fail("Batch 12E HAI glyph stability boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or "子30814110" not in nanyang_row.get("jingluntang_library_instance", ""):
        fail("Batch 12E matrix Jingluntang binding regressed")
    if nanyang_row.get("jingluntang_public_image_review_status") != "EIGHT_UNIQUE_PHYSICAL_IMAGES_DIRECTLY_REVIEWED_NO_TARGET_SECTION":
        fail("Batch 12E matrix physical-image review boundary regressed")
    if nanyang_row.get("audit_status") != "MISSING_FROM_PRODUCT" or nanyang_row.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12E candidate/product boundary regressed")


    if ziwei_post_e_routes_evidence.get("batch_id") != "BATCH-12-ZIWEI-QUANSHU-WENCHENGTANG-DALIAN-COLLATION-ROUTES-F":
        fail("Batch 12F post-12E route evidence batch identity mismatch")
    liaoning12f = ziwei_post_e_routes_evidence.get("liaoning_wenchengtang_route", {})
    institutional12f = liaoning12f.get("institutional_route_witness", {})
    locator12f = liaoning12f.get("secondary_locator", {})
    if institutional12f.get("http_status") != 200 or institutional12f.get("legacy_catalog_route_bound") is not True:
        fail("Batch 12F Liaoning institutional route binding regressed")
    if locator12f.get("authority") != "SECONDARY_CATALOG_LOCATOR_ONLY_NOT_LIBRARY_PRIMARY_RECORD":
        fail("Batch 12F Liaoning secondary-locator authority ceiling regressed")
    if liaoning12f.get("target_page_observed") is not False or "OFFICIAL_LIAONING_TARGET_RECORD_NOT_RETRIEVED" not in liaoning12f.get("adjudication", ""):
        fail("Batch 12F Liaoning target-record boundary regressed")
    dalian12f = ziwei_post_e_routes_evidence.get("dalian_guangyi_route", {})
    direct12f = dalian12f.get("direct_catalog_identity", {})
    if dalian12f.get("direct_item_http_status") != 200 or direct12f.get("edition") != "石印本" or direct12f.get("publication_statement") != "廣益書局 民國":
        fail("Batch 12F Dalian official Guangyi identity regressed")
    if direct12f.get("juan") != "四卷" or direct12f.get("physical_form") != "四冊一函":
        fail("Batch 12F Dalian physical-form identity regressed")
    image12f = dalian12f.get("public_image_candidate_review", {})
    if image12f.get("successfully_saved_image_count") != 6 or image12f.get("direct_visual_review_completed") is not True:
        fail("Batch 12F Dalian image visual-review count regressed")
    if image12f.get("classification") != "ALL_SIX_SAVED_IMAGES_ARE_SITE_UI_ASSETS_NOT_BOOK_PAGES" or image12f.get("target_page_observed") is not False:
        fail("Batch 12F Dalian UI-asset/book-page firewall regressed")
    search12f = dalian12f.get("published_get_form_search_control", {})
    if search12f.get("query_count") != 14 or search12f.get("negative_catalog_conclusion_authorized") is not False:
        fail("Batch 12F Dalian search-control boundary regressed")
    if search12f.get("every_query_term_present_in_returned_text") is not False or search12f.get("every_query_ziwei_present_in_returned_text") is not False:
        fail("Batch 12F Dalian returned-page query-reflection control regressed")
    jielan12f = ziwei_post_e_routes_evidence.get("jielan_wenchengtang_collation_index", {})
    if jielan12f.get("volume_id") != "rZRcCwAAQBAJ" or jielan12f.get("authority_ceiling") != "EDITORIAL_COLLATION_AND_SEARCH_INDEX_ONLY_NOT_DIRECT_WENCHENGTANG_GLYPH":
        fail("Batch 12F Jielan/Wenchengtang authority ceiling regressed")
    controls12f = jielan12f.get("controls", {})
    if controls12f.get("wenchengtang_result_counts") != [1, 1, 1] or controls12f.get("wenchengtang_page_ids") != ["PT176"]:
        fail("Batch 12F Jielan Wenchengtang PT176 index binding regressed")
    if controls12f.get("exact_target_heading_result_counts") != [0, 0, 0] or jielan12f.get("zero_results_as_negative_proof_authorized") is not False:
        fail("Batch 12F zero-result negative-proof firewall regressed")
    adjudication12f = ziwei_post_e_routes_evidence.get("adjudication", {})
    if adjudication12f.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or adjudication12f.get("hai_glyph_stability_across_physical_editions") != "UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES":
        fail("Batch 12F HPA-ZDATE-006 fail-closed state regressed")
    if adjudication12f.get("algorithm_reopen_authorized") is not False or adjudication12f.get("confirmed_chart_algorithm_defect_count") != 0:
        fail("Batch 12F algorithm boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("batch_12f_route_artifact") != "docs/research/ZIWEI-QUANSHU-WENCHENGTANG-DALIAN-COLLATION-ROUTES-R1.json":
        fail("Batch 12F matrix route-artifact binding regressed")
    if nanyang_row.get("wenchengtang_target_late_zi_glyph_status") != "NOT_DIRECTLY_OBSERVED":
        fail("Batch 12F matrix Wenchengtang glyph boundary regressed")
    if nanyang_row.get("audit_status") != "MISSING_FROM_PRODUCT" or nanyang_row.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12F candidate/product boundary regressed")


    if ziwei_quanji_late_zi_evidence.get("batch_id") != "BATCH-12-ZIWEI-QUANJI-LIANYUANGE-LATE-ZI-COLLATION-G":
        fail("Batch 12G Quanji evidence batch identity mismatch")
    pub12g = ziwei_quanji_late_zi_evidence.get("publisher_lianyuange_route", {})
    if pub12g.get("http_status") != 200 or pub12g.get("lianyuange_present") is not True or pub12g.get("quanji_present") is not True:
        fail("Batch 12G Lianyuange publisher-route binding regressed")
    idx12g = ziwei_quanji_late_zi_evidence.get("google_books_jielan_index", {})
    if idx12g.get("volume_id") != "rZRcCwAAQBAJ" or idx12g.get("workflow_run_id") != 34133129317 or idx12g.get("artifact_id") != 10022892119:
        fail("Batch 12G Google Books provenance regressed")
    if idx12g.get("lianyuange_query", {}).get("page_ids") != ["PT176", "PT177"]:
        fail("Batch 12G Lianyuange PT176/PT177 index binding regressed")
    anomaly12g = idx12g.get("ten_ke_query_anomaly", {})
    if anomaly12g.get("page_id") != "PT88" or anomaly12g.get("snippet_contains_query_term") is not False or anomaly12g.get("positive_target_evidence_authorized") is not False:
        fail("Batch 12G ten-ke index-mismatch firewall regressed")
    if idx12g.get("zero_result_as_negative_textual_proof") != "FORBIDDEN" or idx12g.get("physical_lianyuange_target_page_observed") is not False:
        fail("Batch 12G index/physical target fail-closed boundary regressed")
    rec12g = ziwei_quanji_late_zi_evidence.get("received_quanji_transcription_control", {})
    if rec12g.get("authority") != "SECONDARY_RECEIVED_TRANSCRIPTION_ONLY_NOT_PHYSICAL_GLYPH_AUTHORITY":
        fail("Batch 12G received-transcription authority ceiling regressed")
    controls12g = rec12g.get("controls", {})
    for key in ("ten_ke_present", "upper_five_previous_night_present", "lower_five_current_night_zi_present"):
        if controls12g.get(key) is not True:
            fail(f"Batch 12G received Quanji control missing: {key}")
    phil12g = ziwei_quanji_late_zi_evidence.get("philological_adjudication", {})
    if phil12g.get("relation_to_nanyangtang_fullbook") != "PARALLEL_BUT_NOT_MECHANICALLY_IDENTICAL":
        fail("Batch 12G philological relation regressed")
    if phil12g.get("new_candidate_row_authorized") is not False or phil12g.get("hpa_zdate_006_reclassification_authorized") is not False:
        fail("Batch 12G candidate/reclassification firewall regressed")
    adj12g = ziwei_quanji_late_zi_evidence.get("adjudication", {})
    if adj12g.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or adj12g.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12G product/algorithm boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("quanji_lianyuange_collation_artifact") != "docs/research/ZIWEI-QUANJI-LIANYUANGE-LATE-ZI-COLLATION-R1.json":
        fail("Batch 12G Matrix Quanji artifact binding regressed")
    if nanyang_row.get("quanji_candidate_formalization_status") != "NOT_AUTHORIZED_PENDING_DIRECT_PHYSICAL_TARGET_PAGE":
        fail("Batch 12G Matrix candidate-formalization boundary regressed")

    focus_text = "\n".join(audit_state.get("current_focus", ()))
    for fragment in (
        "Batch 11U",
        "RESOLVED_AT_CATALOG_IDENTIFIER_LEVEL",
        "1930 generic main sequence number 893",
        "Batch 11V",
        "ERROR - DIR NOT EXIST",
        "CLOSED_NO_DOWNLOADABLE_PDF_OBJECT_OBSERVED",
        "Batch 11W",
        "5c4276d953bd47ca2679c70209d179cf",
        "ZGKS802.008",
        "Batch 11X",
        "M/F73-102-37-A",
        "2024-02-01",
        "No G893 reproduction request has been submitted",
        "PENDING_DIRECT_TARGET_PAGE",
        "Batch 12A",
        "32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7",
        "HPA-ZDATE-006",
        "MISSING_FROM_PRODUCT",
        "Batch 12B",
        "8-large+2-small-ke structure",
        "23:00–24:00",
        "runtime time",
        "Batch 12C",
        "9789888266944",
        "敦化堂",
        "繼述堂",
        "文誠堂",
        "34120317222",
        "10017909080",
        "UNRESOLVED",
        "Batch 12D",
        "aIRbDgAAQBAJ",
        "PT165",
        "34123161798",
        "10019011766",
        "34121401508",
        "10018315848",
        "Batch 12E",
        "1pjr6vy1ffsq3l1y",
        "子30814110",
        "清經綸堂刻本",
        "BBAA18036",
        "34124948029",
        "10019806060",
        "Batch 12F",
        "rZRcCwAAQBAJ",
        "34128596022",
        "10021127358",
        "34128847746",
        "10021385955",
        "34129199244",
        "10021353934",
        "UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES",
        "Batch 12G",
        "34133129317",
        "10022892119",
        "連元閣",
        "PARALLEL_BUT_NOT_MECHANICALLY_IDENTICAL",
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
