#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"
SOURCE_REGISTRY = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
ZIWEI_QUANSHU_NANYANGTANG = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-NANYANGTANG-LATE-ZI-DIRECT-COLLATION-R1.json"
ZIWEI_LATE_ZI_TIMEKEEPING = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-LATE-ZI-TIMEKEEPING-COLLATION-R1.json"
ZIWEI_LATE_ZI_TIME_COORDINATE_AI = ROOT / "docs" / "research" / "ZIWEI-LATE-ZI-HISTORICAL-TIME-COORDINATE-NARROWING-R1.json"
ZIWEI_FULLBOOK_LUOJING_AJ = ROOT / "docs" / "research" / "ZIWEI-FULLBOOK-LUOJING-TIMEKEEPING-SEMANTICS-R1.json"
ZIWEI_INDEPENDENT_EDITION_ROUTES = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-INDEPENDENT-EDITION-ROUTES-R1.json"
ZIWEI_WENGUANG_GOOGLE_INDEX = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-WENGUANG-GOOGLE-INDEX-PREVIEW-R1.json"
ZIWEI_JINGLUNTANG_PHYSICAL_ROUTE = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-JINGLUNTANG-PHYSICAL-ROUTE-R1.json"
BAZI_RELATION_CANDIDATES = ROOT / "src" / "fortune_training" / "bazi_chart" / "historical_relation_candidates.py"
BAZI_RELATION_CANDIDATE_TEST = ROOT / "tests" / "test_bazi_historical_relation_candidates_r1.py"
BAZI_TEMPORAL_ANNOTATIONS = ROOT / "src" / "fortune_training" / "bazi_application" / "temporal_annotations.py"
BAZI_TEMPORAL_HIDDEN_ORDER_TEST = ROOT / "tests" / "test_bazi_temporal_hidden_stem_order_lineage_r1.py"
HISTORICAL_CALENDAR_CONTRACT = ROOT / "src" / "fortune_training" / "historical_calendar" / "contract.py"
HISTORICAL_CALENDAR_CONTRACT_TEST = ROOT / "tests" / "test_historical_calendar_adapter_contract_r1.py"
MING_DATONG_1578_ORACLE = ROOT / "tests" / "fixtures" / "ming-datong-1578-month-start-oracle-r1.json"
MING_DATONG_1578_ORACLE_TEST = ROOT / "tests" / "test_ming_datong_1578_month_start_oracle_r1.py"
MING_DATONG_1569_QISHUO_RESEARCH = ROOT / "docs" / "research" / "MING-DATONG-1569-QISHUO-METHOD-RESEARCH-R1.json"
MING_DATONG_1569_QISHUO_RESEARCH_TEST = ROOT / "tests" / "test_ming_datong_1569_qishuo_method_research_r1.py"
MING_DATONG_1569_TIME_COORDINATE = ROOT / "docs" / "research" / "MING-DATONG-1569-TIME-COORDINATE-R1.json"
MING_DATONG_1569_TIME_COORDINATE_TEST = ROOT / "tests" / "test_ming_datong_1569_time_coordinate_r1.py"
MING_DATONG_1578_D1_REPLAY = ROOT / "docs" / "research" / "MING-DATONG-1578-D1-SOURCE-REPLAY-R1.json"
MING_DATONG_1578_D1_REPLAY_TEST = ROOT / "tests" / "test_ming_datong_1578_d1_source_replay_r1.py"
MING_DATONG_1578_PHYSICAL_COLLATION = ROOT / "docs" / "research" / "MING-DATONG-1578-NCL-06313-PHYSICAL-ALMANAC-COLLATION-R1.json"
MING_DATONG_1578_PHYSICAL_COLLATION_TEST = ROOT / "tests" / "test_ming_datong_1578_ncl_06313_physical_almanac_collation_r1.py"
MING_DATONG_1569_FIXED_POINT_PRECISION = ROOT / "docs" / "research" / "MING-DATONG-1569-FIXED-POINT-PRECISION-AUDIT-R1.json"
MING_DATONG_1569_FIXED_POINT_PRECISION_TEST = ROOT / "tests" / "test_ming_datong_1569_fixed_point_precision_audit_r1.py"
KYUSHU_OGAWA_1673_COLLATION = ROOT / "docs" / "research" / "KYUSHU-OGAWA-1673-SHOUSHI-LICHENG-DIRECT-COLLATION-R1.json"
KYUSHU_OGAWA_1673_COLLATION_TEST = ROOT / "tests" / "test_kyushu_ogawa_1673_shoushi_licheng_direct_collation_r1.py"
KYUJANGGAK_G893_PROVENANCE = ROOT / "docs" / "research" / "KYUJANGGAK-G893-PROVENANCE-AND-PUBLIC-FIGURE-CONTROL-R1.json"
KYUJANGGAK_G893_PROVENANCE_TEST = ROOT / "tests" / "test_kyujanggak_g893_provenance_public_figure_r1.py"
JOSEON_1444_WITNESS_ROUTES = ROOT / "docs" / "research" / "JOSEON-1444-CHILJEONGSAN-EARLY-TABLE-WITNESS-ROUTES-R1.json"
JOSEON_1444_WITNESS_ROUTES_TEST = ROOT / "tests" / "test_joseon_1444_chiljeongsan_witness_routes_r1.py"
SILLOK_NATIVE_DIRECT_COLLATION = ROOT / "docs" / "research" / "SILLOK-CHILJEONGSAN-NATIVE-DIRECT-COLLATION-R1.json"
SILLOK_NATIVE_DIRECT_COLLATION_TEST = ROOT / "tests" / "test_sillok_chiljeongsan_native_direct_collation_r1.py"
KYUJANGGAK_G894_DIRECT_COLLATION = ROOT / "docs" / "research" / "KYUJANGGAK-G894-DIRECT-TARGET-PAGE-BINDING-R1.json"
KYUJANGGAK_G894_DIRECT_COLLATION_TEST = ROOT / "tests" / "test_kyujanggak_g894_direct_target_page_binding_r1.py"
KYUJANGGAK_G894_FIELD_BRIDGE = ROOT / "docs" / "research" / "KYUJANGGAK-G894-LUNAR-FIELD-SEMANTIC-BRIDGE-R1.json"
KYUJANGGAK_G894_FIELD_BRIDGE_TEST = ROOT / "tests" / "test_kyujanggak_g894_lunar_field_semantic_bridge_r1.py"

ALLOWED = {
    "HISTORICALLY_SUPPORTED",
    "SUPPORTED_BUT_SCHOOL_SPECIFIC",
    "DISPUTED_MULTIPLE_CANDIDATES",
    "MODERN_COMPATIBILITY_ONLY",
    "SOURCE_INSUFFICIENT",
    "IMPLEMENTATION_REVIEW_REQUIRED",
    "MISSING_FROM_PRODUCT",
    "NOT_YET_FORMALIZED",
}
REQUIRED_MODULES = {
    "Time / Calendar","四柱本命","八字派生字段","大运","小运","神煞","八字动态时限",
    "紫微本命","十二宫","主星","辅星","杂曜","四化","庙旺落陷","大限","小限","流年","流月",
    "流日","流时","动态辅助星","Structural R1–R8","Combined Fusion",
    "candidate/profile rules","provenance / hashes / lineage",
}
REQUIRED_FIELDS = {
    "rule_id","system","module","rule_or_field","current_implementation","current_profile",
    "primary_source","source_quote","source_quote_location","historical_period","later_witnesses",
    "school_attribution","competing_methods","current_implementation_match","confidence",
    "audit_status","proposed_action","algorithm_reopen_authorized",
}

def main() -> int:
    data=json.loads(MATRIX.read_text(encoding="utf-8"))
    source_registry=json.loads(SOURCE_REGISTRY.read_text(encoding="utf-8"))
    if source_registry.get("schema")!="FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1":
        raise SystemExit("external historical source registry schema mismatch")
    source_ids=[item.get("source_id") for item in source_registry.get("sources",())]
    if len(source_ids)!=len(set(source_ids)) or not source_ids:
        raise SystemExit("external historical source registry has invalid/duplicate IDs")
    by_source_id={item.get("source_id"): item for item in source_registry["sources"]}
    jielan=by_source_id.get("EXT-ZIWEI-JIELAN-1581")
    shlib=by_source_id.get("EXT-SHANGHAI-LIB-JIELAN-1581")
    if jielan is None or shlib is None:
        raise SystemExit("Jielan 1581 historical/bibliographic source pair is missing")
    if "EXT-SHANGHAI-LIB-JIELAN-1581" not in jielan.get("bibliographic_witnesses",()):
        raise SystemExit("Jielan 1581 source is not bound to its library bibliographic witness")
    if shlib.get("source_role")!="LIBRARY_CATALOG_BIBLIOGRAPHIC_WITNESS_FOR_JIELAN_1581_EDITION":
        raise SystemExit("Jielan 1581 library witness role mismatch")
    if shlib.get("catalog_identifier")!="子4051":
        raise SystemExit("Jielan 1581 library catalog identifier mismatch")
    if shlib.get("edition")!="明万历九年金陵书坊王洛川刻本":
        raise SystemExit("Jielan 1581 library edition identity mismatch")
    wang=by_source_id.get("EXT-WANGTINGZHI-ANXING-2013")
    uibe=by_source_id.get("EXT-UIBE-WANGTINGZHI-ANXING-2013")
    if wang is None or uibe is None:
        raise SystemExit("Wang Tingzhi Zhongzhou dynamic-auxiliary source pair is missing")
    if "EXT-UIBE-WANGTINGZHI-ANXING-2013" not in wang.get("bibliographic_witnesses",()):
        raise SystemExit("Wang Tingzhi rule-text witness is not bound to its library bibliographic witness")
    if uibe.get("source_role")!="LIBRARY_CATALOG_BIBLIOGRAPHIC_WITNESS_FOR_WANGTINGZHI_ANXING_2013":
        raise SystemExit("Wang Tingzhi library witness role mismatch")
    if wang.get("isbn")!="978-7-309-09665-1" or uibe.get("isbn")!="978-7-309-09665-1":
        raise SystemExit("Wang Tingzhi edition ISBN mismatch")
    if by_source_id.get("EXT-CTEXT-WUXING-JINGJI-V28") is None:
        raise SystemExit("Batch 08B Five-Tigers witness is missing")
    if by_source_id.get("EXT-WANGTINGZHI-ZHONGZHOU-CHUJI") is None:
        raise SystemExit("Batch 08B Zhongzhou temporal witness is missing")
    if by_source_id.get("EXT-XINGQIAO-WANGTINGZHI-ZHONGZHOU-CHUJI") is None:
        raise SystemExit("Batch 08B Zhongzhou bibliographic witness is missing")
    if by_source_id.get("EXT-USNO-EQUATION-OF-TIME") is None:
        raise SystemExit("Batch 08C USNO solar-time witness is missing")
    time12ai=by_source_id.get("EXT-CTEXT-MINGSHI-ASTRONOMY-DINGSHI-SOLAR-STELLAR")
    if time12ai is None:
        raise SystemExit("Batch 12AI Ming solar-stellar time witness is missing")
    if time12ai.get("source_role") != "RECEIVED_INSTITUTIONAL_WITNESS_FOR_MING_SOLAR_STELLAR_TIME_DETERMINATION_NOT_ZIWEI_DOCTRINE":
        raise SystemExit("Batch 12AI Ming time witness authority scope regressed")
    if time12ai.get("machine_probe", {}).get("response_sha256") != "157eac2885f6bd3e6c72899f90539e4dd817cf63099c6e17508a8fc419293c16":
        raise SystemExit("Batch 12AI Ming time witness response binding regressed")
    if not ZIWEI_LATE_ZI_TIME_COORDINATE_AI.is_file():
        raise SystemExit("Batch 12AI time-coordinate evidence artifact is missing")
    time12ai_evidence=json.loads(ZIWEI_LATE_ZI_TIME_COORDINATE_AI.read_text(encoding="utf-8"))
    if time12ai_evidence.get("batch_id") != "BATCH-12-ZIWEI-LATE-ZI-HISTORICAL-TIME-COORDINATE-NARROWING-AI":
        raise SystemExit("Batch 12AI evidence identity mismatch")
    if time12ai_evidence.get("controlling_probe", {}).get("artifact_zip_sha256") != "9e3151f558b6425586fc2e2c593f5a01f82529f42f6cbd7e8f3e3973fc6df98f":
        raise SystemExit("Batch 12AI evidence archive binding regressed")
    for source_id in (
        "EXT-CTEXT-HUANGMING-JINGSHI-WENBIAN-V493-DINGSHI-LUOJING",
        "EXT-SHIDIAN-XU-ZHIMO-LUOJING-DINGMENZHEN-MING",
        "EXT-SHIDIAN-SIKU-LUOJING-DINGMENZHEN-CATALOG",
    ):
        src12aj=by_source_id.get(source_id)
        if src12aj is None:
            raise SystemExit(f"Batch 12AJ Luojing semantic source missing: {source_id}")
        if src12aj.get("machine_probe", {}).get("workflow_run_id") != 34324767233:
            raise SystemExit(f"Batch 12AJ source probe binding regressed: {source_id}")
        if src12aj.get("machine_probe", {}).get("artifact_zip_sha256") != "5e86d5837910be780e8f69ec0ad2f8ad2666f125ae8d9b0548d51b7d2a7f54f2":
            raise SystemExit(f"Batch 12AJ source artifact digest regressed: {source_id}")
    if not ZIWEI_FULLBOOK_LUOJING_AJ.is_file():
        raise SystemExit("Batch 12AJ Luojing evidence artifact is missing")
    luojing12aj=json.loads(ZIWEI_FULLBOOK_LUOJING_AJ.read_text(encoding="utf-8"))
    if luojing12aj.get("batch_id") != "BATCH-12-ZIWEI-FULLBOOK-LUOJING-TIMEKEEPING-SEMANTICS-AJ":
        raise SystemExit("Batch 12AJ evidence identity mismatch")
    probe12aj=luojing12aj.get("controlling_probe", {})
    if probe12aj.get("workflow_run_id") != 34324767233 or probe12aj.get("artifact_id") != 10093334440:
        raise SystemExit("Batch 12AJ controlling probe binding regressed")
    if probe12aj.get("artifact_zip_sha256") != "5e86d5837910be780e8f69ec0ad2f8ad2666f125ae8d9b0548d51b7d2a7f54f2" or probe12aj.get("all_control_terms_hit") is not True:
        raise SystemExit("Batch 12AJ stabilized term gate regressed")
    if by_source_id.get("EXT-ZIWEI-QVXIAN-TRUE-SOLAR-2022") is None:
        raise SystemExit("Batch 08C modern Ziwei true-solar witness is missing")
    if by_source_id.get("EXT-CTEXT-ZIWEI-DATAWIKI-LATE-ZI") is None:
        raise SystemExit("Batch 08D late-Zi dispute witness is missing")
    if by_source_id.get("EXT-XUANMEN-LINGDONGLAI-LATE-ZI") is None:
        raise SystemExit("Batch 08D late-Zi practice witness is missing")
    nanyangtang=by_source_id.get("EXT-ZIWEI-QUANSHU-NANYANGTANG-SCAN")
    if nanyangtang is None:
        raise SystemExit("Batch 12A Nanyangtang Fullbook facsimile witness is missing")
    if nanyangtang.get("pdf_sha256") != "32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7" or nanyangtang.get("direct_target_page_1_based") != 320:
        raise SystemExit("Batch 12A Nanyangtang source binding mismatch")
    if not ZIWEI_QUANSHU_NANYANGTANG.is_file():
        raise SystemExit("Batch 12A Nanyangtang direct-collation artifact is missing")
    nanyang_evidence=json.loads(ZIWEI_QUANSHU_NANYANGTANG.read_text(encoding="utf-8"))
    if nanyang_evidence.get("status") != "DIRECT_NO_OCR_TARGET_SECTION_COLLATION_COMPLETE_NEW_HISTORICAL_CANDIDATE_IDENTIFIED":
        raise SystemExit("Batch 12A Nanyangtang evidence status mismatch")
    direct=nanyang_evidence.get("direct_collation", {})
    if direct.get("pdf_page_1_based") != 320 or direct.get("heading") != "論人生時要審的確":
        raise SystemExit("Batch 12A direct target-page binding mismatch")
    if direct.get("s01_claimed_sentence_status") != "NOT_OBSERVED_ON_DIRECT_TARGET_SECTION_PAGE" or direct.get("whole_volume_negative_claim_authorized") is not False:
        raise SystemExit("Batch 12A S01 quotation quarantine boundary regressed")
    for source_id in ("EXT-NAOJ-KOYOMI-TEIJI-SHICHEN","EXT-CTEXT-RIZHILU-BAIKE","EXT-WIKISOURCE-ZWDSQS-V3-LATE-ZI","EXT-SHIDIAN-ZWDSQS-LATE-ZI"):
        if by_source_id.get(source_id) is None:
            raise SystemExit(f"Batch 12B timekeeping/transcription source is missing: {source_id}")
    if not ZIWEI_LATE_ZI_TIMEKEEPING.is_file():
        raise SystemExit("Batch 12B timekeeping collation artifact is missing")
    timekeeping=json.loads(ZIWEI_LATE_ZI_TIMEKEEPING.read_text(encoding="utf-8"))
    if timekeeping.get("status") != "GENERIC_ZI_UPPER_LOWER_HALF_TIMEKEEPING_ORIENTATION_CLOSED_RUNTIME_BINDING_STILL_OPEN":
        raise SystemExit("Batch 12B timekeeping adjudication status mismatch")
    mapping=timekeeping.get("adjudication", {})
    if mapping.get("upper_half_orientation") != "BEFORE_MIDNIGHT_PREVIOUS_DAY" or mapping.get("lower_half_orientation") != "AFTER_MIDNIGHT_CURRENT_DAY":
        raise SystemExit("Batch 12B upper/lower-half orientation regressed")
    if mapping.get("ten_ke_equal_duration_interpretation") != "REJECTED":
        raise SystemExit("Batch 12B ten-ke equal-duration firewall regressed")
    if mapping.get("runtime_time_standard_binding") != "UNRESOLVED":
        raise SystemExit("Batch 12B runtime time-standard was prematurely selected")
    for source_id in (
        "EXT-XINYITANG-ZWDSQS-WENGUANG-FACSIMILE-2017",
        "EXT-XINYITANG-ZWDSQS-WENCHENGTANG-COLLATION",
        "EXT-SKYLIGHT-ZWDSQS-WENSHENG-JISHU-COMPARISON-2017",
    ):
        if by_source_id.get(source_id) is None:
            raise SystemExit(f"Batch 12C independent Fullbook edition source is missing: {source_id}")
    if not ZIWEI_INDEPENDENT_EDITION_ROUTES.is_file():
        raise SystemExit("Batch 12C independent-edition route artifact is missing")
    edition_routes=json.loads(ZIWEI_INDEPENDENT_EDITION_ROUTES.read_text(encoding="utf-8"))
    if edition_routes.get("status") != "INDEPENDENT_FULLBOOK_EDITION_ROUTES_BOUND_NO_INDEPENDENT_TARGET_PAGE_OBSERVED":
        raise SystemExit("Batch 12C independent-edition route status mismatch")
    workflow=edition_routes.get("research_workflow", {})
    if workflow.get("workflow_run_id") != 34120317222 or workflow.get("artifact_id") != 10017909080:
        raise SystemExit("Batch 12C workflow/artifact provenance mismatch")
    preview=edition_routes.get("public_preview_controls", {}).get("books_preview_image_urls", {})
    if preview.get("attempted_count") != 13 or preview.get("http_403_count") != 13 or preview.get("saved_image_count") != 0:
        raise SystemExit("Batch 12C preview access boundary regressed")
    edition_adjudication=edition_routes.get("adjudication", {})
    if edition_adjudication.get("independent_physical_target_page_status") != "NO_INDEPENDENT_TARGET_PAGE_OBSERVED":
        raise SystemExit("Batch 12C incorrectly claims an independent target page")
    if edition_adjudication.get("hai_glyph_stability_across_physical_editions") != "UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES":
        raise SystemExit("Batch 12C HAI glyph stability boundary regressed")
    for source_id in (
        "EXT-GOOGLE-PLAY-ZWDSQS-WENGUANG-2017",
        "EXT-XINYI-ZWDSQS-WENGUANG-PUBLIC-SAMPLES-2021",
    ):
        if by_source_id.get(source_id) is None:
            raise SystemExit(f"Batch 12D Google/Heart-One source is missing: {source_id}")
    if not ZIWEI_WENGUANG_GOOGLE_INDEX.is_file():
        raise SystemExit("Batch 12D Wenguang Google index evidence is missing")
    wenguang_index=json.loads(ZIWEI_WENGUANG_GOOGLE_INDEX.read_text(encoding="utf-8"))
    if wenguang_index.get("status") != "COMBINED_WENGUANG_FACSIMILE_PUBLIC_INDEX_SUPPORTS_HAI_READING_TARGET_GLYPH_NOT_PUBLICLY_DISPLAYED":
        raise SystemExit("Batch 12D evidence status mismatch")
    volume=wenguang_index.get("distribution_volume", {})
    if volume.get("volume_id") != "aIRbDgAAQBAJ" or volume.get("isbn") != "9789888266944" or volume.get("declared_page_count") != 266:
        raise SystemExit("Batch 12D Google distribution identity mismatch")
    index=wenguang_index.get("public_search_index", {})
    if index.get("workflow_run_id") != 34121750009 or index.get("artifact_id") != 10018452113:
        raise SystemExit("Batch 12D search-index provenance mismatch")
    if index.get("target_heading_query", {}).get("target_page_id") != "PT165":
        raise SystemExit("Batch 12D target PT165 binding mismatch")
    reading=index.get("target_index_reading", "")
    if "上五刻" not in reading or "下五刻" not in reading or "亥時" not in reading:
        raise SystemExit("Batch 12D target index reading regressed")
    if index.get("target_index_reading_authority") != "SEARCH_INDEX_TEXT_ONLY_NOT_PHYSICAL_GLYPH_AUTHORITY":
        raise SystemExit("Batch 12D index/glyph authority firewall regressed")
    if index.get("negative_textual_claim_authorized") is not False:
        raise SystemExit("Batch 12D zero-result negative-proof firewall regressed")
    viewer=wenguang_index.get("embedded_viewer_control", {})
    if viewer.get("workflow_run_id") != 34123161798 or viewer.get("artifact_id") != 10019011766:
        raise SystemExit("Batch 12D viewer provenance mismatch")
    if viewer.get("go_to_pt165_returned") is not True or viewer.get("after_page_id") != "PT166" or viewer.get("target_page_directly_observed") is not False:
        raise SystemExit("Batch 12D viewer fail-closed state regressed")
    adjudication12d=wenguang_index.get("adjudication", {})
    if adjudication12d.get("pt165_base_copy_identity") != "UNRESOLVED_DUNHUATANG_VS_JISHUTANG":
        raise SystemExit("Batch 12D PT165 base-copy boundary regressed")
    if adjudication12d.get("hai_glyph_stability_across_physical_editions") != "UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES":
        raise SystemExit("Batch 12D HAI glyph stability boundary regressed")
    if adjudication12d.get("hpa_zdate_006_status") != "MISSING_FROM_PRODUCT" or adjudication12d.get("algorithm_reopen_authorized") is not False:
        raise SystemExit("Batch 12D candidate/product boundary regressed")
    for source_id in (
        "EXT-SHLIB-ZWDSQS-JINGLUNTANG-QING",
        "EXT-KUMYO-ZWDSQS-JINGLUNTANG-19C-PHYSICAL",
    ):
        if by_source_id.get(source_id) is None:
            raise SystemExit(f"Batch 12E Jingluntang source is missing: {source_id}")
    if not ZIWEI_JINGLUNTANG_PHYSICAL_ROUTE.is_file():
        raise SystemExit("Batch 12E Jingluntang physical-route evidence is missing")
    jingluntang=json.loads(ZIWEI_JINGLUNTANG_PHYSICAL_ROUTE.read_text(encoding="utf-8"))
    if jingluntang.get("status") != "INDEPENDENT_QING_JINGLUNTANG_EDITION_IDENTITY_AND_PHYSICAL_COPY_BOUND_TARGET_PAGE_NOT_OBSERVED":
        raise SystemExit("Batch 12E evidence status mismatch")
    shlib=jingluntang.get("shanghai_library", {})
    if shlib.get("instance_id") != "1pjr6vy1ffsq3l1y" or shlib.get("identifier") != "子30814110" or shlib.get("edition_label") != "清經綸堂刻本":
        raise SystemExit("Batch 12E SHLIB Jingluntang identity mismatch")
    if shlib.get("public_content_negotiation", {}).get("jsonld", {}).get("http_status") != 200:
        raise SystemExit("Batch 12E SHLIB JSON-LD route regressed")
    if shlib.get("anonymous_route_controls", {}).get("dhapi_pdfview_root", {}).get("http_status") != 412:
        raise SystemExit("Batch 12E SHLIB anonymous page-route boundary regressed")
    tokens=shlib.get("public_metadata_token_scan", {})
    if any(tokens.get(key) for key in ("iiif","manifest","itemid","itemId","dhapi","pdfview")):
        raise SystemExit("Batch 12E SHLIB metadata unexpectedly exposes a page object route")
    kumyo=jingluntang.get("kumyo_physical_copy", {})
    if kumyo.get("auction_no") != "BBAA18036" or kumyo.get("unique_embedded_physical_image_count") != 8:
        raise SystemExit("Batch 12E Kumyo physical-copy binding mismatch")
    if len(kumyo.get("unique_image_sha256", ())) != 8 or len(set(kumyo.get("unique_image_sha256", ()))) != 8:
        raise SystemExit("Batch 12E Kumyo unique-image digest set regressed")
    if kumyo.get("jingluntang_label_visibly_observed") is not True:
        raise SystemExit("Batch 12E Kumyo Jingluntang label review regressed")
    if kumyo.get("target_heading_observed") is not False or kumyo.get("target_hai_glyph_observed") is not False:
        raise SystemExit("Batch 12E incorrectly claims a target page/glyph")
    adjudication12e=jingluntang.get("adjudication", {})
    if adjudication12e.get("jingluntang_edition_family_identity") != "CLOSED_AT_LIBRARY_AND_PUBLIC_PHYSICAL_COPY_LEVEL":
        raise SystemExit("Batch 12E Jingluntang identity closure regressed")
    if adjudication12e.get("hai_glyph_stability_across_physical_editions") != "UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES":
        raise SystemExit("Batch 12E HAI glyph stability boundary regressed")
    if adjudication12e.get("hpa_zdate_006_status") != "MISSING_FROM_PRODUCT" or adjudication12e.get("algorithm_reopen_authorized") is not False:
        raise SystemExit("Batch 12E candidate/product boundary regressed")
    for source_id in ("EXT-HKO-24-SOLAR-TERMS","EXT-HKO-SOLAR-TERM-TIMES","EXT-CTEXT-SANMING-V2-SEASONS","EXT-CTEXT-MINGLI-TANYUAN-YEAR-MONTH","EXT-CTEXT-QIANLI-MINGGAO-YEAR"):
        if by_source_id.get(source_id) is None:
            raise SystemExit(f"Batch 09A source witness missing: {source_id}")
    for source_id in ("EXT-CTEXT-QIANLI-MINGGAO-DAYUN","EXT-CTEXT-MINGLI-TANYUAN-DAYUN","EXT-CTEXT-SANMING-V2-DAYUN"):
        if by_source_id.get(source_id) is None:
            raise SystemExit(f"Batch 09B Dayun source witness missing: {source_id}")
    for source_id in ("EXT-CTEXT-SANMING-V2-RELATIONS","EXT-CTEXT-XINGLI-KAOYUAN-RELATIONS","EXT-CTEXT-SANMING-V1-FOUR-EARTH-BUREAU"):
        if by_source_id.get(source_id) is None:
            raise SystemExit(f"Batch 10A relation source witness missing: {source_id}")
    for source_id in ("EXT-CTEXT-SANMING-V6-DIRECTIONAL-TRIADS","EXT-CTEXT-WUXING-JINGJI-V23-BREAK","EXT-CTEXT-SANMING-V2-ZUOXIA-ZIHUA","EXT-MODERN-OPENFATE-HALF-TRINE-2026"):
        if by_source_id.get(source_id) is None:
            raise SystemExit(f"Batch 10B relation source witness missing: {source_id}")
    if by_source_id.get("EXT-CTEXT-ZIPING-ZHENQUAN-PINGZHU-ZAQI") is None:
        raise SystemExit("Batch 11A later hidden-stem hierarchy witness is missing")
    for source_id in ("EXT-KOTENMON-DAMING-DATONG-1569","EXT-NCL-DATONG-1578-ALMANAC","EXT-IHNS-MING-DATONG-COMPILATION-2019","EXT-MINGSHILU-WANLI-1578-MONTH-STARTS","EXT-WANLI-QIJUZHU-1578-MONTH-CORROBORATION","EXT-WIKISOURCE-GUJIN-LULIKAO-V49-DATONG","EXT-SHAO-LIYONG-DATONG-1527-2011","EXT-YTLIU-MING-DATONG-CONJUNCTION-D1-D2","EXT-SHAO-LI-ZHANG-REAL-NEW-MOON-1996","EXT-AA-LI-ZHANG-SYZYGY-1998","EXT-WIKISOURCE-MINGSHI-V35-DATONG-TIME","EXT-CTEXT-MINGSHI-ASTRONOMY-BEIJING-NANJING-CLOCK","EXT-WIKISOURCE-WANLI-YEHUO-DATONG-DAYLENGTH","EXT-RAA-MIHN-SHOUSHI-AFFILIATED-2014","EXT-WILEY-CHOI-DATONGLI-SUNRISE-2018","EXT-LOC-DATONG-1524-ALMANAC","EXT-WIKISOURCE-GUJIN-LULIKAO-V50-SHOUSHI-PRECISION"):
        if by_source_id.get(source_id) is None:
            raise SystemExit(f"Batch 11D/11E Ming Datong source witness missing: {source_id}")
    for source_id in ("EXT-NDL-OGAWA-SHOUSHI-LICHENG-1673","EXT-KYUSHU-OGAWA-SHOUSHI-LICHENG-1673"):
        if by_source_id.get(source_id) is None:
            raise SystemExit(f"Batch 11K/11L Ogawa source witness missing: {source_id}")
    for source_id in ("EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893","EXT-LI-LIANG-SUNRISE-TABLES-2022"):
        if by_source_id.get(source_id) is None:
            raise SystemExit(f"Batch 11M G893 provenance source witness missing: {source_id}")
    g893_source=by_source_id["EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893"]
    if "CONFLICTING_1434_AND_1444" not in g893_source.get("exact_print_year_status",""):
        raise SystemExit("Batch 11M G893 exact-copy-year conflict boundary is missing")
    if "EXT-LI-LIANG-SUNRISE-TABLES-2022" not in g893_source.get("bibliographic_witnesses",()):
        raise SystemExit("Batch 11M G893 1444 secondary date witness is not bound")
    for source_id in ("EXT-KYUJANGGAK-CHILJEONGSAN-NAEPYEON-G894-1444","EXT-NIKH-SEJONG-SILLOK-V156-CHILJEONGSAN-TABLES","EXT-NIKH-CHILJEONGSAN-HISTORY-1444"):
        if by_source_id.get(source_id) is None:
            raise SystemExit(f"Batch 11N Joseon witness source missing: {source_id}")
    kyushu_source=by_source_id["EXT-KYUSHU-OGAWA-SHOUSHI-LICHENG-1673"]
    if kyushu_source.get("reading_artifact") != "docs/research/KYUSHU-OGAWA-1673-SHOUSHI-LICHENG-DIRECT-COLLATION-R1.json":
        raise SystemExit("Batch 11L Kyushu source reading-artifact binding mismatch")
    if kyushu_source.get("workflow_run_id") != 34010515542 or kyushu_source.get("artifact_id") != 9982311056:
        raise SystemExit("Batch 11L Kyushu exact evidence package binding mismatch")
    for item in source_registry["sources"]:
        if not item.get("url","").startswith("https://"):
            raise SystemExit(f"external source lacks https URL: {item.get('source_id')}")
    if data.get("schema")!="FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1":
        raise SystemExit("historical provenance matrix schema mismatch")
    if data.get("deterministic_product_state")!="CLOSED":
        raise SystemExit("deterministic product closure was reopened")
    if data.get("self_inward_transformation_state")!="NOT_YET_FORMALIZED":
        raise SystemExit("self/inward transformation direction was formalized without audit")
    if set(data.get("allowed_audit_statuses",()))!=ALLOWED:
        raise SystemExit("allowed audit status set mismatch")
    rows=data.get("rows",())
    if not rows:
        raise SystemExit("historical provenance inventory is empty")
    ids=[]
    modules=set()
    for row in rows:
        missing=REQUIRED_FIELDS-set(row)
        if missing:
            raise SystemExit(f"{row.get('rule_id','<missing>')} missing fields: {sorted(missing)}")
        if row["audit_status"] not in ALLOWED:
            raise SystemExit(f"invalid audit status: {row['rule_id']}")
        if row["algorithm_reopen_authorized"] is not False:
            raise SystemExit(f"inventory row unexpectedly authorizes reopen: {row['rule_id']}")
        if not row["current_implementation"] or not row["current_profile"]:
            raise SystemExit(f"missing implementation/profile identity: {row['rule_id']}")
        ids.append(row["rule_id"])
        modules.add(row["module"])
    if len(ids)!=len(set(ids)):
        raise SystemExit("duplicate historical provenance rule_id")
    missing_modules=REQUIRED_MODULES-modules
    if missing_modules:
        raise SystemExit("matrix missing modules: "+", ".join(sorted(missing_modules)))
    if len(rows) < 80:
        raise SystemExit(f"inventory unexpectedly small: {len(rows)}")
    special=[r for r in rows if r["rule_id"]=="HPA-ZT-016"]
    if len(special)!=1 or special[0]["audit_status"]!="NOT_YET_FORMALIZED":
        raise SystemExit("ZIWEI self/inward transformation audit state mismatch")
    audit_summary=data.get("audit_summary",{})
    if audit_summary.get("confirmed_chart_algorithm_defect_count") != 0:
        raise SystemExit("historical audit unexpectedly reports a chart algorithm defect")
    if audit_summary.get("algorithm_reopen_count") != 0:
        raise SystemExit("historical audit unexpectedly reopened an algorithm")
    if audit_summary.get("confirmed_provenance_metadata_defect_count", 0) < 10:
        raise SystemExit("known provenance metadata defects are missing")
    if audit_summary.get("repaired_provenance_metadata_defect_count", 0) < 10:
        raise SystemExit("known provenance metadata repairs are missing")
    if audit_summary.get("historical_candidate_runtime_resolver_count", 0) < 3:
        raise SystemExit("source-scoped historical candidate runtime resolver accounting regressed")
    if audit_summary.get("historical_candidate_registry_count", 0) < 3:
        raise SystemExit("historical candidate registry accounting regressed")
    if audit_summary.get("historical_candidate_extension_count", 0) < 6:
        raise SystemExit("historical candidate extension accounting regressed")
    if audit_summary.get("identified_missing_candidate_family_count", 0) < 14:
        raise SystemExit("cumulative historical candidate discovery accounting regressed")
    current_missing = sum(row.get("audit_status") == "MISSING_FROM_PRODUCT" for row in rows)
    if current_missing != 10 or audit_summary.get("current_missing_from_product_row_count") != 10:
        raise SystemExit("current MISSING_FROM_PRODUCT row accounting mismatch after Batch 12A Ziwei Fullbook facsimile discovery")
    row_nanyang=next((row for row in rows if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if row_nanyang is None or row_nanyang.get("audit_status") != "MISSING_FROM_PRODUCT":
        raise SystemExit("Batch 12A HPA-ZDATE-006 missing-product row is absent")
    if row_nanyang.get("algorithm_reopen_authorized") is not False:
        raise SystemExit("Batch 12A historical candidate improperly authorized an algorithm reopen")
    if row_nanyang.get("candidate_method_id") != "NANYANGTANG-FULLBOOK-ZI-TEN-KE-HAI-SPLIT-R1":
        raise SystemExit("Batch 12A candidate method identity mismatch")
    if row_nanyang.get("timekeeping_orientation_status") != "CLOSED_AT_GENERIC_FIXED_SHICHEN_LEVEL":
        raise SystemExit("Batch 12B HPA-ZDATE-006 timekeeping status regressed")
    if row_nanyang.get("runtime_time_standard_binding") != "UNRESOLVED_DO_NOT_CHOOSE_CIVIL_MEAN_OR_APPARENT_SOLAR_TIME_FROM_TIMEKEEPING_TRANSLATION":
        raise SystemExit("Batch 12B runtime time-standard firewall regressed")
    if row_nanyang.get("independent_physical_target_page_status") != "NANYANGTANG_FULLBOOK_AND_GUANGYI_FULLBOOK_DIRECT_TARGET_PAGES_OBSERVED; KOREA_SPRINGGANG_MANUSCRIPT_DIRECT_TARGET_PASSAGE_ALSO_OBSERVED":
        raise SystemExit("Batch 12AF HPA-ZDATE-006 physical target-page status regressed")
    if row_nanyang.get("hai_glyph_cross_edition_status") != "EXPLICIT_HAI_IS_NOT_UNIVERSAL_ACROSS_BROADER_RECEIVED_ZIWEI_TRANSMISSION: KOREA_SPRINGGANG_MANUSCRIPT_HAS_NON_HAI_VARIANT; NANYANGTANG_AND_GUANGYI_DIRECT_PHYSICAL_FULLBOOK_EDITIONS_BOTH_HAVE 昨夜亥時/今日子時; GLOBAL_ALL_FULLBOOK_EDITION_STABILITY_NOT_CLAIMED":
        raise SystemExit("Batch 12AF HPA-ZDATE-006 HAI glyph boundary regressed")
    if row_nanyang.get("batch_12z_korea_cnts_direct_collation_artifact") != "docs/research/ZIWEI-KOREA-CNTS-ZIWEIDOUSHUFANGSHU-DIRECT-LATE-ZI-COLLATION-R1.json":
        raise SystemExit("Batch 12Z HPA-ZDATE-006 Korea CNTS artifact binding regressed")
    if row_nanyang.get("korea_cnts_explicit_hai_glyph_in_exact_target_span") is not False:
        raise SystemExit("Batch 12Z HPA-ZDATE-006 Korea exact-span non-Hai boundary regressed")
    if row_nanyang.get("independent_hai_glyph_witness_count_added_batch_12z") != 0:
        raise SystemExit("Batch 12Z HPA-ZDATE-006 Hai witness accounting regressed")
    if row_nanyang.get("batch_12af_guangyi_yulgok_direct_collation_artifact") != "docs/research/ZIWEI-GUANGYI-YULGOK-DIRECT-LATE-ZI-COLLATION-R1.json":
        raise SystemExit("Batch 12AF HPA-ZDATE-006 Guangyi/Yulgok artifact binding regressed")
    if row_nanyang.get("yulgok_guangyi_direct_imprint") != "上海廣益書局印行":
        raise SystemExit("Batch 12AF HPA-ZDATE-006 Guangyi imprint binding regressed")
    if row_nanyang.get("yulgok_guangyi_target_heading") != "論人生時要審的確" or row_nanyang.get("yulgok_guangyi_target_juan") != 3:
        raise SystemExit("Batch 12AF HPA-ZDATE-006 target location binding regressed")
    if row_nanyang.get("yulgok_guangyi_target_decisive_direct_reading") != "如子時有十刻上五刻屬昨夜亥時下五刻屬今日子時":
        raise SystemExit("Batch 12AF HPA-ZDATE-006 direct target reading regressed")
    if row_nanyang.get("direct_fullbook_physical_target_text_witness_count_added_batch_12af") != 1 or row_nanyang.get("independent_hai_glyph_witness_count_added_batch_12af") != 1:
        raise SystemExit("Batch 12AF HPA-ZDATE-006 witness accounting regressed")
    yulgok_guangyi=by_source_id.get("EXT-YULGOK-B005-B00320-GUANGYI-ZWDSQS")
    if yulgok_guangyi is None:
        raise SystemExit("Batch 12AF Yulgok Guangyi registry source is missing")
    if yulgok_guangyi.get("target_image_sha256") != "2d1fc5ce8459d3696166b0471b2075fee247ede94b73eb833d435fe54ee847e0":
        raise SystemExit("Batch 12AF Yulgok Guangyi target image binding regressed")
    if yulgok_guangyi.get("independent_hai_glyph_witness_increment") != 1 or yulgok_guangyi.get("stemmatic_independence_claimed") is not False:
        raise SystemExit("Batch 12AF Yulgok Guangyi witness/stemma firewall regressed")

    jiaojing=by_source_id.get("EXT-HANAUCTION-JIAOJINGSHANFANG-ZWDSQS-PHYSICAL")
    if jiaojing is None:
        raise SystemExit("Batch 12AG Jiaojingshanfang registry source is missing")
    if jiaojing.get("direct_target_page_observed") is not False or jiaojing.get("direct_visual_review_of_2012_detail_photos_completed") is not True:
        raise SystemExit("Batch 12AH target-page/image-review state regressed")
    if jiaojing.get("media_scope_classification") != "AUCTION_ROUND_EVENT_SCENERY_VIDEO_THUMBNAILS_NOT_TARGET_OBJECT_PHOTOS":
        raise SystemExit("Batch 12AH Jiaojingshanfang media-scope repair regressed")
    if jiaojing.get("provenance_defect_id") != "PROV-DEFECT-010" or jiaojing.get("provenance_defect_repair_status") != "REPAIRED_FORWARD_ONLY_DURING_BATCH_12AH":
        raise SystemExit("Batch 12AH Jiaojingshanfang provenance defect repair regressed")
    if jiaojing.get("independent_target_text_witness_increment") != 0 or jiaojing.get("independent_hai_glyph_witness_increment") != 0:
        raise SystemExit("Batch 12AG Jiaojingshanfang witness accounting regressed")
    if jiaojing.get("stemmatic_independence_claimed") is not False:
        raise SystemExit("Batch 12AG Jiaojingshanfang stemmatic-independence firewall regressed")
    if row_nanyang.get("batch_12ag_jiaojingshanfang_hanauction_physical_edition_artifact") != "docs/research/ZIWEI-JIAOJINGSHANFANG-HANAUCTION-PHYSICAL-EDITION-PROVENANCE-R1.json":
        raise SystemExit("Batch 12AG HPA-ZDATE-006 artifact binding regressed")
    if row_nanyang.get("jiaojingshanfang_target_page_status") != "PENDING_DIRECT_VISUAL_TARGET_PAGE":
        raise SystemExit("Batch 12AG HPA-ZDATE-006 target-page status regressed")
    if row_nanyang.get("independent_textual_witness_count_added_batch_12ag") != 0 or row_nanyang.get("independent_hai_glyph_witness_count_added_batch_12ag") != 0:
        raise SystemExit("Batch 12AG HPA-ZDATE-006 witness firewall regressed")
    if row_nanyang.get("batch_12ah_jiaojingshanfang_detail_photo_visual_adjudication_artifact") != "docs/research/ZIWEI-JIAOJINGSHANFANG-HANAUCTION-DETAIL-PHOTO-VISUAL-ADJUDICATION-R1.json":
        raise SystemExit("Batch 12AH HPA-ZDATE-006 artifact binding regressed")
    if row_nanyang.get("defect_id") != "PROV-DEFECT-010" or row_nanyang.get("repair_status") != "REPAIRED_FORWARD_ONLY_DURING_BATCH_12AH":
        raise SystemExit("Batch 12AH HPA-ZDATE-006 provenance repair regressed")
    if row_nanyang.get("jiaojingshanfang_2012_detail_photo_visual_review_status") != "DIRECTLY_REVIEWED_AND_RECLASSIFIED_AS_AUCTION_EVENT_MEDIA_NOT_TARGET_OBJECT":
        raise SystemExit("Batch 12AH HPA-ZDATE-006 visual adjudication regressed")
    if row_nanyang.get("independent_textual_witness_count_added_batch_12ah") != 0 or row_nanyang.get("independent_hai_glyph_witness_count_added_batch_12ah") != 0:
        raise SystemExit("Batch 12AH HPA-ZDATE-006 witness firewall regressed")
    if row_nanyang.get("batch_12ai_ziwei_late_zi_time_coordinate_artifact") != "docs/research/ZIWEI-LATE-ZI-HISTORICAL-TIME-COORDINATE-NARROWING-R1.json":
        raise SystemExit("Batch 12AI HPA-ZDATE-006 artifact binding regressed")
    if row_nanyang.get("historical_time_coordinate_family") != "LOCAL_OBSERVATIONAL_ASTRONOMICAL_TIME_COORDINATE":
        raise SystemExit("Batch 12AI HPA-ZDATE-006 coordinate-family binding regressed")
    if row_nanyang.get("historical_daytime_time_basis") != "SUNDIAL_TRUE_SUN" or row_nanyang.get("historical_nighttime_time_basis") != "STELLAR_TIME_READING_WITH_CLEPSYDRA_AS_SUPPLEMENT":
        raise SystemExit("Batch 12AI HPA-ZDATE-006 day/night time basis regressed")
    if row_nanyang.get("runtime_time_standard_binding_status_batch_12ai") != "PARTIALLY_NARROWED_NOT_CLOSED":
        raise SystemExit("Batch 12AI HPA-ZDATE-006 batch-scoped runtime binding regressed")
    if row_nanyang.get("local_apparent_solar_time_historical_binding") != "STRONGEST_MODERN_DAYTIME_TRANSLATION_NOT_NATAL_RUNTIME_WINNER":
        raise SystemExit("Batch 12AI apparent-solar translation was promoted beyond evidence")
    if row_nanyang.get("historical_nighttime_to_runtime_apparent_solar_equivalence") != "UNRESOLVED" or row_nanyang.get("natal_birthplace_time_coordinate_binding") != "UNRESOLVED":
        raise SystemExit("Batch 12AI unresolved source bridges were silently closed")
    if row_nanyang.get("candidate_selected_batch_12ai") is not False or row_nanyang.get("candidate_collapsed_batch_12ai") is not False:
        raise SystemExit("Batch 12AI candidate state regressed")
    if row_nanyang.get("independent_textual_witness_count_added_batch_12ai") != 0 or row_nanyang.get("independent_hai_glyph_witness_count_added_batch_12ai") != 0:
        raise SystemExit("Batch 12AI HPA-ZDATE-006 witness firewall regressed")
    if row_nanyang.get("batch_12aj_fullbook_luojing_timekeeping_semantics_artifact") != "docs/research/ZIWEI-FULLBOOK-LUOJING-TIMEKEEPING-SEMANTICS-R1.json":
        raise SystemExit("Batch 12AJ HPA-ZDATE-006 artifact binding regressed")
    if row_nanyang.get("fullbook_luojing_phrase_direct_physical_edition_agreement") != "CONFIRMED_NANYANGTANG_AND_GUANGYI":
        raise SystemExit("Batch 12AJ Fullbook physical phrase agreement regressed")
    if row_nanyang.get("fullbook_luojing_term_mechanical_concept") != "MAGNETIC_COMPASS_DIRECTION_AND_MERIDIAN_ORIENTATION_INSTRUMENT_FAMILY":
        raise SystemExit("Batch 12AJ Luojing mechanical concept regressed")
    if row_nanyang.get("fullbook_luojing_standalone_timekeeper_equivalence") != "REJECTED_BY_CONTEMPORANEOUS_TECHNICAL_CONTROL":
        raise SystemExit("Batch 12AJ standalone-clock equivalence regressed")
    if row_nanyang.get("fullbook_luojing_direct_true_solar_time_equivalence") != "NOT_ESTABLISHED":
        raise SystemExit("Batch 12AJ true-solar inference firewall regressed")
    if row_nanyang.get("runtime_time_standard_binding_status") != "PARTIALLY_NARROWED_WITH_FULLBOOK_INSTRUMENT_SEMANTIC_TENSION_NOT_CLOSED":
        raise SystemExit("Batch 12AJ runtime time-standard state regressed")
    if row_nanyang.get("local_apparent_solar_time_runtime_winner_selected") is not False or row_nanyang.get("luojing_means_true_solar_time") is not False:
        raise SystemExit("Batch 12AJ solar-time winner firewall regressed")
    if row_nanyang.get("independent_textual_witness_count_added_batch_12aj") != 0 or row_nanyang.get("independent_hai_glyph_witness_count_added_batch_12aj") != 0:
        raise SystemExit("Batch 12AJ witness double-counting firewall regressed")

    korea_cnts=by_source_id.get("EXT-KOREA-NLK-CNTS-00047996572-ZIWEIDOUSHUFANGSHU")
    if korea_cnts is None:
        raise SystemExit("Batch 12Z Korea CNTS physical manuscript registry source is missing")
    if korea_cnts.get("pdf_sha256") != "b21bbf3e2c7cdada4153f847ff9f359dbb29e71998e1f931417d108b571b23c3":
        raise SystemExit("Batch 12Z Korea CNTS source PDF identity regressed")
    if korea_cnts.get("explicit_hai_glyph_in_exact_target_span") is not False or korea_cnts.get("direct_ocr_used") is not False:
        raise SystemExit("Batch 12Z Korea CNTS direct-glyph/no-OCR boundary regressed")
    if row_nanyang.get("combined_facsimile_volume_id") != "aIRbDgAAQBAJ" or row_nanyang.get("combined_facsimile_target_index_page_id") != "PT165":
        raise SystemExit("Batch 12D HPA-ZDATE-006 index-text binding regressed")
    if row_nanyang.get("combined_facsimile_index_text_status") != "TARGET_PASSAGE_CORROBORATED_AT_PUBLIC_SEARCH_INDEX_LEVEL_NOT_GLYPH_AUTHORITY":
        raise SystemExit("Batch 12D HPA-ZDATE-006 index authority boundary regressed")
    if row_nanyang.get("combined_facsimile_target_image_status") != "PUBLIC_EMBEDDED_VIEWER_DID_NOT_DISPLAY_TARGET_GLYPHS":
        raise SystemExit("Batch 12D HPA-ZDATE-006 viewer boundary regressed")
    if row_nanyang.get("combined_facsimile_base_copy_identity_for_pt165") != "UNRESOLVED_DUNHUATANG_VS_JISHUTANG":
        raise SystemExit("Batch 12D HPA-ZDATE-006 base-copy identity was prematurely closed")
    if "子30814110" not in row_nanyang.get("jingluntang_library_instance", ""):
        raise SystemExit("Batch 12E HPA-ZDATE-006 Jingluntang binding regressed")
    if row_nanyang.get("jingluntang_public_image_review_status") != "EIGHT_UNIQUE_PHYSICAL_IMAGES_DIRECTLY_REVIEWED_NO_TARGET_SECTION":
        raise SystemExit("Batch 12E HPA-ZDATE-006 physical-image review boundary regressed")
    if row_nanyang.get("jingluntang_target_page_status") != "NOT_OBSERVED_IN_PUBLIC_SHLIB_METADATA_OR_KUMYO_PHYSICAL_IMAGES":
        raise SystemExit("Batch 12E HPA-ZDATE-006 target-page boundary regressed")
    if "GLOBAL_ALL_FULLBOOK_EDITION_STABILITY_NOT_CLAIMED" not in row_nanyang.get("hai_glyph_cross_edition_status", ""):
        raise SystemExit("Batch 12AF HPA-ZDATE-006 global Fullbook stability firewall regressed")
    defect_ids=[row.get("defect_id") for row in rows if row.get("defect_id")]
    if len(defect_ids)!=len(set(defect_ids)):
        raise SystemExit("duplicate historical provenance defect_id")
    summary=data.get("inventory_summary",{})
    if summary.get("row_count")!=len(rows):
        raise SystemExit("inventory row_count mismatch")
    audited_ids=data.get("audited_row_ids",())
    if summary.get("audited_row_count")!=len(audited_ids) or len(audited_ids) < 165:
        raise SystemExit("historical audited-row accounting mismatch or regressed below Batch 07A")
    batches=data.get("historical_research_batches",())
    if "BATCH-06-ZIWEI-NATAL-FOUNDATIONS" not in batches:
        raise SystemExit("Batch 06 Ziwei natal foundations audit is missing")
    if "BATCH-07-ZIWEI-MINOR-STARS-A" not in batches:
        raise SystemExit("Batch 07A Ziwei minor-star decomposition is missing")
    if "BATCH-07-ZIWEI-MINOR-STARS-B" not in batches:
        raise SystemExit("Batch 07B Ziwei minor-star early-print closure is missing")
    if "BATCH-07-ZIWEI-MINOR-STARS-C" not in batches:
        raise SystemExit("Batch 07C Ziwei minor-star source-gap closure is missing")
    if "BATCH-08-ZIWEI-DYNAMIC-AUXILIARIES-A" not in batches:
        raise SystemExit("Batch 08A Ziwei dynamic auxiliary audit is missing")
    if "BATCH-08-ZIWEI-TEMPORAL-FRAMES-B" not in batches:
        raise SystemExit("Batch 08B Ziwei temporal-frame audit is missing")
    if "BATCH-08-ZIWEI-TIME-STANDARDS-C" not in batches:
        raise SystemExit("Batch 08C Ziwei time-standard audit is missing")
    if "BATCH-08-ZIWEI-CALENDAR-DATE-BOUNDARY-D" not in batches:
        raise SystemExit("Batch 08D Ziwei calendar-date/day-boundary audit is missing")
    if "BATCH-09-TIME-SOLAR-TERMS-BAZI-YEAR-MONTH-A" not in batches:
        raise SystemExit("Batch 09A solar-term/Bazi year-month audit is missing")
    if "BATCH-09-BAZI-DAYUN-SEQUENCE-B" not in batches:
        raise SystemExit("Batch 09B Bazi Dayun sequence audit is missing")
    if "BATCH-10-BAZI-RAW-RELATIONS-AFFINITY-A" not in batches:
        raise SystemExit("Batch 10A Bazi raw-relation/affinity audit is missing")
    if "BATCH-10-BAZI-EXCLUDED-RELATION-FAMILIES-B" not in batches:
        raise SystemExit("Batch 10B excluded Bazi relation-family audit is missing")
    if "BATCH-10-BAZI-HISTORICAL-RELATION-CANDIDATES-C" not in batches:
        raise SystemExit("Batch 10C Bazi historical relation candidate runtime is missing")
    if "BATCH-11-BAZI-HIDDEN-STEM-ORDER-A" not in batches:
        raise SystemExit("Batch 11A Bazi hidden-stem order audit is missing")
    if "BATCH-11-BAZI-DAYUN-CALENDAR-REALIZATION-B" not in batches:
        raise SystemExit("Batch 11B Bazi Dayun calendar-realization audit is missing")
    if "BATCH-11-BAZI-HISTORICAL-CALENDAR-ADAPTER-C" not in batches:
        raise SystemExit("Batch 11C historical-calendar adapter contract is missing")
    if "BATCH-11-BAZI-MING-DATONG-SOURCE-CLOSURE-D" not in batches:
        raise SystemExit("Batch 11D Ming Datong source closure is missing")
    if "BATCH-11-BAZI-MING-DATONG-1578-MONTH-ORACLE-E" not in batches:
        raise SystemExit("Batch 11E Ming Datong 1578 oracle is missing")
    if "BATCH-11-BAZI-MING-DATONG-CONJUNCTION-METHOD-F" not in batches:
        raise SystemExit("Batch 11F Ming Datong conjunction-method adjudication is missing")
    if "BATCH-11-BAZI-MING-DATONG-TIME-COORDINATE-G" not in batches:
        raise SystemExit("Batch 11G Ming Datong time-coordinate audit is missing")
    if "BATCH-11-BAZI-MING-DATONG-1578-D1-SOURCE-REPLAY-H" not in batches:
        raise SystemExit("Batch 11H Ming Datong 1578 D1 source replay is missing")
    if "BATCH-11-BAZI-MING-DATONG-1578-PHYSICAL-ALMANAC-CLOSURE-I" not in batches:
        raise SystemExit("Batch 11I Ming Datong 1578 physical almanac closure is missing")
    if "BATCH-11-BAZI-MING-DATONG-FIXED-POINT-PRECISION-J" not in batches:
        raise SystemExit("Batch 11J Ming Datong fixed-point precision audit is missing")
    if "BATCH-11-BAZI-OGAWA-1673-NATIVE-EVIDENCE-K" not in batches:
        raise SystemExit("Batch 11K NDL Ogawa native evidence audit is missing")
    if "BATCH-11-BAZI-OGAWA-1673-KYUSHU-COLLATION-L" not in batches:
        raise SystemExit("Batch 11L Kyushu Ogawa direct collation audit is missing")
    if "BATCH-11-BAZI-G893-PROVENANCE-PUBLIC-FIGURE-M" not in batches:
        raise SystemExit("Batch 11M G893 provenance/public-figure audit is missing")
    if "BATCH-11-BAZI-JOSEON-1444-CHILJEONGSAN-WITNESS-ROUTES-N" not in batches:
        raise SystemExit("Batch 11N Joseon 1444 witness-route audit is missing")
    minor_child_ids={f"HPA-ZMINOR-{index:03d}" for index in range(1,27)}
    if not minor_child_ids.issubset(set(ids)):
        raise SystemExit("Batch 07A/07B/07C minor-star child rows are incomplete")
    minor_parent=next((row for row in rows if row["rule_id"]=="HPA-ZIWEI-008"), None)
    if minor_parent is None or minor_parent["audit_status"]!="SOURCE_INSUFFICIENT" or "FULLY_DECOMPOSED" not in minor_parent["current_implementation_match"]:
        raise SystemExit("operational minor-star parent was not fully decomposed after Batch 07C")
    dynamic_child_ids={f"HPA-ZAUX-{index:03d}" for index in range(1,9)}
    if not dynamic_child_ids.issubset(set(ids)):
        raise SystemExit("Batch 08A dynamic auxiliary child rows are incomplete")
    kui_yue_parent=next((row for row in rows if row["rule_id"]=="HPA-ZT-011"), None)
    if kui_yue_parent is None or kui_yue_parent.get("defect_id")!="PROV-DEFECT-007":
        raise SystemExit("Batch 08A Kui/Yue provenance-label repair is missing")
    temporal_child_ids={f"HPA-ZTEMP-{index:03d}" for index in range(1,7)}
    if not temporal_child_ids.issubset(set(ids)):
        raise SystemExit("Batch 08B temporal-frame child rows are incomplete")
    temporal_by_id={row["rule_id"]: row for row in rows if row["rule_id"].startswith("HPA-ZTEMP-")}
    ztemp004=temporal_by_id["HPA-ZTEMP-004"]
    ztemp006=temporal_by_id["HPA-ZTEMP-006"]
    if ztemp004["audit_status"]!="HISTORICALLY_SUPPORTED":
        raise SystemExit("1581 day-anchored flow-hour candidate productization status regressed")
    if ztemp006["audit_status"]!="SUPPORTED_BUT_SCHOOL_SPECIFIC":
        raise SystemExit("Zhongzhou leap-month candidate school scope regressed")
    for row,method_id in (
        (ztemp004,"JIELAN-1581-DAY-ANCHORED-FLOW-HOUR-R1"),
        (ztemp006,"ZHONGZHOU-LEAP-MONTH-HALF-SPLIT-R1"),
    ):
        if row.get("selection_status")!="PRESERVED_NOT_SELECTED":
            raise SystemExit(f"Ziwei temporal candidate was silently selected: {row['rule_id']}")
        if row.get("candidate_method_id")!=method_id:
            raise SystemExit(f"Ziwei temporal candidate method identity regressed: {row['rule_id']}")
        if row.get("runtime_resolver_id")!="ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-RUNTIME-R1":
            raise SystemExit(f"Ziwei temporal candidate runtime identity regressed: {row['rule_id']}")
        if row.get("algorithm_reopen_authorized") is not False:
            raise SystemExit(f"Ziwei temporal candidate incorrectly reopened production: {row['rule_id']}")
    if "TIME_STANDARD_SPECIFIC_PARENT_DAILY_FRAME_REQUIRED" not in ztemp004.get("current_implementation_match",""):
        raise SystemExit("1581 historical hour candidate lost parent-day/time-standard binding")
    if "DAILY_ACTIVE_ADDRESS_NOT_EMITTED" not in ztemp006.get("current_implementation_match",""):
        raise SystemExit("Zhongzhou leap-month candidate invented unresolved daily geometry")

    temporal_candidate_paths=(
        ROOT/"src"/"fortune_training"/"ziwei_chart"/"temporal_historical_candidates.py",
        ROOT/"tests"/"test_ziwei_temporal_historical_candidate_api_r1.py",
        ROOT/"tests"/"test_shared_ziwei_historical_temporal_candidates_r1.py",
        ROOT/"schemas"/"shared-ziwei-selector-projection-r1.schema.json",
        ROOT/"docs"/"ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-PRODUCTIZATION-R1.md",
    )
    for path in temporal_candidate_paths:
        if not path.is_file():
            raise SystemExit(f"Ziwei temporal candidate productization artifact missing: {path.relative_to(ROOT)}")
    temporal_candidate_source=temporal_candidate_paths[0].read_text(encoding="utf-8")
    for token in (
        "ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-REGISTRY-R1",
        "ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-RUNTIME-R1",
        "JIELAN-1581-DAY-ANCHORED-FLOW-HOUR-R1",
        "ZHONGZHOU-LEAP-MONTH-HALF-SPLIT-R1",
        "PRESERVED_NOT_SELECTED",
        "NOT_CLOSED_BY_THIS_MONTH_POLICY_API",
    ):
        if token not in temporal_candidate_source:
            raise SystemExit(f"Ziwei temporal candidate source contract missing: {token}")
    time_standard_child_ids={"HPA-ZTIME-001","HPA-ZTIME-002"}
    if not time_standard_child_ids.issubset(set(ids)):
        raise SystemExit("Batch 08C Ziwei time-standard child rows are incomplete")
    time_by_id={row["rule_id"]: row for row in rows if row["rule_id"].startswith("HPA-ZTIME-")}
    if time_by_id["HPA-ZTIME-001"]["audit_status"]!="SUPPORTED_BUT_SCHOOL_SPECIFIC":
        raise SystemExit("Luoyang time standard lost school-specific scope")
    if time_by_id["HPA-ZTIME-002"]["audit_status"]!="MODERN_COMPATIBILITY_ONLY":
        raise SystemExit("local apparent solar time was incorrectly upgraded to historical authority")
    date_child_ids={f"HPA-ZDATE-{index:03d}" for index in range(1,6)}
    if not date_child_ids.issubset(set(ids)):
        raise SystemExit("Batch 08D Ziwei date-boundary child rows are incomplete")
    date_by_id={row["rule_id"]: row for row in rows if row["rule_id"].startswith("HPA-ZDATE-")}
    if date_by_id["HPA-ZDATE-003"]["audit_status"]!="DISPUTED_MULTIPLE_CANDIDATES":
        raise SystemExit("Ziwei 23:00 rollover was incorrectly upgraded to historical winner")
    if next(row for row in rows if row["rule_id"]=="HPA-TIME-009")["audit_status"]!="DISPUTED_MULTIPLE_CANDIDATES":
        raise SystemExit("Ziwei effective calendar-date parent lost candidate dispute")
    btime_child_ids={f"HPA-BTIME-{index:03d}" for index in range(1,5)}
    if not btime_child_ids.issubset(set(ids)):
        raise SystemExit("Batch 09A Bazi time child rows are incomplete")
    btime_by_id={row["rule_id"]: row for row in rows if row["rule_id"].startswith("HPA-BTIME-")}
    if btime_by_id["HPA-BTIME-001"]["audit_status"]!="MODERN_COMPATIBILITY_ONLY":
        raise SystemExit("solar-term numerical realization was incorrectly upgraded to classical doctrine")
    for rule_id in ("HPA-BTIME-002","HPA-BTIME-003","HPA-BTIME-004"):
        if btime_by_id[rule_id]["audit_status"]!="HISTORICALLY_SUPPORTED":
            raise SystemExit(f"historically supported Bazi time rule regressed: {rule_id}")
    dayun_sequence_child_ids={"HPA-DAYUN-SEQ-001","HPA-DAYUN-SEQ-002"}
    if not dayun_sequence_child_ids.issubset(set(ids)):
        raise SystemExit("Batch 09B Dayun sequence child rows are incomplete")
    dayun_sequence_by_id={row["rule_id"]: row for row in rows if row["rule_id"].startswith("HPA-DAYUN-SEQ-")}
    for rule_id in dayun_sequence_child_ids:
        if dayun_sequence_by_id[rule_id]["audit_status"]!="HISTORICALLY_SUPPORTED":
            raise SystemExit(f"historically supported Dayun sequence rule regressed: {rule_id}")
    dayun_parent=next(row for row in rows if row["rule_id"]=="HPA-DAYUN-004")
    if dayun_parent["audit_status"]!="HISTORICALLY_SUPPORTED":
        raise SystemExit("Dayun sequence parent did not close historically")
    batch10_child_ids={"HPA-BAFF-001","HPA-BAFF-002"} | {f"HPA-BREL-{index:03d}" for index in range(1,8)}
    if not batch10_child_ids.issubset(set(ids)):
        raise SystemExit("Batch 10A affinity/raw-relation child rows are incomplete")
    by_rule_id={row["rule_id"]: row for row in rows}
    for rule_id in ("HPA-BAZI-004","HPA-BAZI-013","HPA-BAFF-001","HPA-BAFF-002","HPA-BREL-001","HPA-BREL-002","HPA-BREL-003","HPA-BREL-004","HPA-BREL-005","HPA-BREL-006"):
        if by_rule_id[rule_id]["audit_status"]!="HISTORICALLY_SUPPORTED":
            raise SystemExit(f"Batch 10A supported relation/affinity rule regressed: {rule_id}")
    if "arity-4" not in by_rule_id["HPA-BREL-007"]["current_implementation"]:
        raise SystemExit("four-earth bureau lost separate arity-4 typing requirement")
    if "LIUHAI_ALIAS_RECORDED_IN_PROVENANCE_ONLY" not in by_rule_id["HPA-BREL-004"]["current_implementation_match"]:
        raise SystemExit("穿/害 terminology bridge regressed into duplicate mechanics")
    batch10b_ids={f"HPA-BREL-{index:03d}" for index in range(8,13)}
    if not batch10b_ids.issubset(set(ids)):
        raise SystemExit("Batch 10B excluded relation rows are incomplete")
    if by_rule_id["HPA-BREL-010"]["audit_status"]!="DISPUTED_MULTIPLE_CANDIDATES":
        raise SystemExit("later six-break table lost disputed status")
    if by_rule_id["HPA-BREL-011"]["audit_status"]!="MODERN_COMPATIBILITY_ONLY":
        raise SystemExit("modern half-trine/arched-trine family was incorrectly upgraded")
    if "DIFFERENT_WORDING_SAME_MECHANICAL_RULE" not in by_rule_id["HPA-BREL-008"]["school_attribution"]:
        raise SystemExit("属象/方/三会 philological bridge regressed")
    candidate_source=BAZI_RELATION_CANDIDATES.read_text(encoding="utf-8")
    candidate_test=BAZI_RELATION_CANDIDATE_TEST.read_text(encoding="utf-8")
    for token in ("BAZI-HISTORICAL-RELATION-CANDIDATES-R1","PRESERVED_NOT_SELECTED","FOUR_EARTH_BUREAU","DIRECTIONAL_TRIAD","BRANCH_BREAK_EARLY_FOUR","STEM_HIDDEN_COMBINATION"):
        if token not in candidate_source:
            raise SystemExit(f"Batch 10C candidate runtime token missing: {token}")
    if "test_four_earth_bureau_is_arity_four_and_not_raw_trine" not in candidate_test:
        raise SystemExit("Batch 10C historical relation candidate tests are missing")
    for rule_id in ("HPA-BREL-007","HPA-BREL-008","HPA-BREL-009","HPA-BREL-012"):
        if by_rule_id[rule_id]["audit_status"]!="HISTORICALLY_SUPPORTED":
            raise SystemExit(f"productized historical relation candidate did not close: {rule_id}")
        if "PRESERVED_NOT_SELECTED" not in by_rule_id[rule_id]["current_profile"]:
            raise SystemExit(f"productized relation candidate lost unselected profile: {rule_id}")
    if by_rule_id["HPA-BAZI-005"]["audit_status"]!="DISPUTED_MULTIPLE_CANDIDATES":
        raise SystemExit("raw relation parent did not close to candidate-preserving state")
    if by_rule_id["HPA-BCAND-001"]["audit_status"]!="DISPUTED_MULTIPLE_CANDIDATES":
        raise SystemExit("Bazi historical candidate registry row missing/disposition mismatch")
    defect8=by_rule_id["HPA-BREL-012"]
    if defect8.get("defect_id")!="PROV-DEFECT-008" or defect8.get("repair_status")!="REPAIRED_FORWARD_ONLY_DURING_BATCH_10C":
        raise SystemExit("PROV-DEFECT-008 source-scope repair is incomplete")
    hidden_order_ids={"HPA-BHIDDEN-001","HPA-BHIDDEN-002","HPA-BHIDDEN-003"}
    if not hidden_order_ids.issubset(set(ids)):
        raise SystemExit("Batch 11A hidden-stem decomposition is incomplete")
    if by_rule_id["HPA-BHIDDEN-001"]["audit_status"]!="HISTORICALLY_SUPPORTED":
        raise SystemExit("YHZP hidden-stem textual sequence lost historical support")
    if by_rule_id["HPA-BHIDDEN-002"]["audit_status"]!="SOURCE_INSUFFICIENT":
        raise SystemExit("normalized registry order was incorrectly upgraded to historical authority")
    if by_rule_id["HPA-BHIDDEN-003"]["audit_status"]!="SUPPORTED_BUT_SCHOOL_SPECIFIC":
        raise SystemExit("later main-qi hierarchy lost scoped status")
    if by_rule_id["HPA-BAZI-015"]["audit_status"]!="SOURCE_INSUFFICIENT" or "FULLY_DECOMPOSED" not in by_rule_id["HPA-BAZI-015"]["current_implementation_match"]:
        raise SystemExit("hidden-stem order parent was not fully decomposed")
    flow_hidden=by_rule_id["HPA-BAZI-FLOW-003"]
    if flow_hidden["audit_status"]!="HISTORICALLY_SUPPORTED":
        raise SystemExit("temporal hidden-stem registry reuse did not close")
    if flow_hidden.get("defect_id")!="PROV-DEFECT-009" or flow_hidden.get("repair_status")!="REPAIRED_FORWARD_ONLY_DURING_BATCH_11A":
        raise SystemExit("PROV-DEFECT-009 temporal hidden-stem hash repair is incomplete")
    temporal_source=BAZI_TEMPORAL_ANNOTATIONS.read_text(encoding="utf-8")
    temporal_test=BAZI_TEMPORAL_HIDDEN_ORDER_TEST.read_text(encoding="utf-8")
    for token in ('TEMPORAL_CLASSICAL_ANNOTATION_PROFILE_VERSION = "1.0.2"', 'TEMPORAL_CLASSICAL_ANNOTATION_HASH_VERSION = "1.0.1"', '"hidden_stem_registry_order"'):
        if token not in temporal_source:
            raise SystemExit(f"Batch 11A temporal hash-lineage token missing: {token}")
    if "test_order_is_lineage_not_fact_identity" not in temporal_test or "test_membership_change_still_changes_fact_identity" not in temporal_test:
        raise SystemExit("Batch 11A temporal hidden-stem order tests are missing")
    historical_calendar_source=HISTORICAL_CALENDAR_CONTRACT.read_text(encoding="utf-8")
    historical_calendar_test=HISTORICAL_CALENDAR_CONTRACT_TEST.read_text(encoding="utf-8")
    for token in ("HISTORICAL-CHINESE-CALENDAR-ADAPTER-CONTRACT-R1","MING-DATONG-CALENDAR-CONTEXT-R1","QING-SHIXIAN-1645-CALENDAR-CONTEXT-R1","MODERN_CHINESE_CALENDAR_FALLBACK_FORBIDDEN","PRESERVED_NOT_SELECTED"):
        if token not in historical_calendar_source:
            raise SystemExit(f"Batch 11C historical-calendar contract token missing: {token}")
    if "test_fail_closed_adapter_never_falls_back_to_modern_calendar" not in historical_calendar_test:
        raise SystemExit("Batch 11C historical-calendar contract tests are missing")
    for source_id in ("EXT-CTEXT-MINGSHI-DATONG-CALENDAR","EXT-LOC-XINLI-XIAOHUO-SHIXIAN-1645"):
        if source_id not in by_source_id:
            raise SystemExit(f"Batch 11C calendar-regime source missing: {source_id}")
    for rule_id in ("HPA-DAYUN-CAL-002","HPA-DAYUN-CAL-003","HPA-DAYUN-CAL-004"):
        row=by_rule_id[rule_id]
        if row["audit_status"]!="MISSING_FROM_PRODUCT":
            raise SystemExit(f"historical Dayun calendar candidate was prematurely productized: {rule_id}")
        if row.get("adapter_contract_id")!="HISTORICAL-CHINESE-CALENDAR-ADAPTER-CONTRACT-R1":
            raise SystemExit(f"historical Dayun calendar row lost adapter contract binding: {rule_id}")
    if "MING_DATONG" not in by_rule_id["HPA-DAYUN-CAL-002"].get("calendar_regime_context",""):
        raise SystemExit("Ming Dayun calendarization lost Datong context research binding")
    if "MODERN_CHINESE_CALENDAR_FALLBACK_FORBIDDEN" not in by_rule_id["HPA-DAYUN-CAL-002"]["current_implementation_match"]:
        raise SystemExit("historical Dayun calendarization no longer forbids modern calendar fallback")
    if "COMPLETE_1578_OFFICIAL_RECORD_MONTH_START_CHAIN_MACHINE_FIXTURED" not in by_rule_id["HPA-DAYUN-CAL-002"]["current_implementation_match"]:
        raise SystemExit("Batch 11E target-year oracle binding is missing")
    if by_rule_id["HPA-DAYUN-CAL-002"].get("oracle_fixture") != "tests/fixtures/ming-datong-1578-month-start-oracle-r1.json":
        raise SystemExit("Batch 11E oracle fixture binding mismatch")
    if not MING_DATONG_1578_ORACLE.is_file() or not MING_DATONG_1578_ORACLE_TEST.is_file():
        raise SystemExit("Batch 11E oracle fixture/test is missing")
    oracle=json.loads(MING_DATONG_1578_ORACLE.read_text(encoding="utf-8"))
    if oracle.get("schema")!="MING-DATONG-1578-MONTH-START-ORACLE-R1":
        raise SystemExit("Batch 11E oracle schema mismatch")
    if oracle.get("runtime_selection_authorized") is not False or oracle.get("general_calendar_arithmetic_certified") is not False:
        raise SystemExit("Batch 11E evidence oracle was incorrectly promoted to runtime arithmetic")
    months=oracle.get("months",())
    if [item.get("month") for item in months] != list(range(1,13)):
        raise SystemExit("Batch 11E oracle month sequence mismatch")
    starts=[item.get("start_index") for item in months]+[oracle.get("next_anchor",{}).get("start_index")]
    derived=[(starts[i+1]-starts[i])%60 for i in range(12)]
    if derived != [29,30,30,29,30,29,30,29,29,30,29,30] or sum(derived)!=354:
        raise SystemExit("Batch 11E oracle month-length replay mismatch")
    row_dayun_cal=by_rule_id["HPA-DAYUN-CAL-002"]
    if row_dayun_cal.get("conjunction_method_historical_adjudication") != "D1_SHOUSHI_STYLE_CHIJIXINGDU_IS_MING_OFFICIAL_PRODUCTION_METHOD":
        raise SystemExit("Batch 11F D1 historical adjudication missing")
    if row_dayun_cal.get("conjunction_method_runtime_authorized") is not False:
        raise SystemExit("Batch 11F historical subrule was prematurely authorized for runtime")
    if row_dayun_cal.get("d2_received_variant_disposition") != "PRESERVE_FOR_TEXTUAL_TRANSMISSION_HISTORY_NOT_EQUAL_PRODUCTION_CANDIDATE":
        raise SystemExit("Batch 11F D2 received-variant disposition mismatch")
    if row_dayun_cal.get("method_research_artifact") != "docs/research/MING-DATONG-1569-QISHUO-METHOD-RESEARCH-R1.json":
        raise SystemExit("Batch 11F research artifact binding mismatch")
    if not MING_DATONG_1569_QISHUO_RESEARCH.is_file() or not MING_DATONG_1569_QISHUO_RESEARCH_TEST.is_file():
        raise SystemExit("Batch 11F research artifact/test missing")
    qishuo=json.loads(MING_DATONG_1569_QISHUO_RESEARCH.read_text(encoding="utf-8"))
    adjudication=qishuo.get("historical_subrule_adjudication",{})
    if adjudication.get("winner_id") != "MING_DATONG_D1_SHOUSHI_STYLE_CHIJIXINGDU":
        raise SystemExit("Batch 11F research winner identity mismatch")
    if adjudication.get("status") != "HISTORICALLY_ADJUDICATED_FOR_MING_OFFICIAL_PRODUCTION":
        raise SystemExit("Batch 11F research adjudication status mismatch")
    if qishuo.get("runtime_selection_authorized") is not False or qishuo.get("general_calendar_arithmetic_certified") is not False:
        raise SystemExit("Batch 11F research was incorrectly promoted to executable calendar arithmetic")
    if row_dayun_cal.get("historical_time_coordinate_status") != "INTERNAL_DAY_AND_CLOCK_COORDINATE_CLOSED_GEOGRAPHIC_QISHUO_REFERENCE_UNRESOLVED":
        raise SystemExit("Batch 11G time-coordinate disposition mismatch")
    if row_dayun_cal.get("historical_computational_day_boundary") != "ZI_ZHENG":
        raise SystemExit("Batch 11G computational day boundary mismatch")
    if row_dayun_cal.get("astrological_day_boundary_inference_forbidden") is not True:
        raise SystemExit("Batch 11G astrological day-boundary firewall missing")
    if row_dayun_cal.get("historical_time_coordinate_artifact") != "docs/research/MING-DATONG-1569-TIME-COORDINATE-R1.json":
        raise SystemExit("Batch 11G time-coordinate artifact binding mismatch")
    if not MING_DATONG_1569_TIME_COORDINATE.is_file() or not MING_DATONG_1569_TIME_COORDINATE_TEST.is_file():
        raise SystemExit("Batch 11G time-coordinate artifact/test missing")
    time_coord=json.loads(MING_DATONG_1569_TIME_COORDINATE.read_text(encoding="utf-8"))
    if time_coord.get("schema") != "MING-DATONG-1569-TIME-COORDINATE-R1":
        raise SystemExit("Batch 11G time-coordinate schema mismatch")
    internal=time_coord.get("internal_coordinate",{})
    if internal.get("computational_day_boundary") != "ZI_ZHENG" or internal.get("day_cycle_source_units") != 10000 or internal.get("ke_per_day") != 100:
        raise SystemExit("Batch 11G internal time coordinate regressed")
    scope=time_coord.get("scope_firewalls",{})
    if scope.get("astrological_day_boundary_inference_forbidden") is not True:
        raise SystemExit("Batch 11G astrological inference firewall regressed")
    geography=time_coord.get("geographic_realization",{})
    if geography.get("qishuo_meridian_reference_status") != "UNRESOLVED":
        raise SystemExit("Batch 11G qishuo geographic reference was silently selected")
    if row_dayun_cal.get("d1_source_replay_batch") != "BATCH-11-BAZI-MING-DATONG-1578-D1-SOURCE-REPLAY-H":
        raise SystemExit("Batch 11H D1 replay batch binding mismatch")
    if row_dayun_cal.get("d1_source_replay_artifact") != "docs/research/MING-DATONG-1578-D1-SOURCE-REPLAY-R1.json":
        raise SystemExit("Batch 11H D1 replay artifact binding mismatch")
    if row_dayun_cal.get("d1_source_replay_result") != "1578_MONTHS_1_TO_12_PLUS_1579_MONTH_1_ANCHOR_13_OF_13_DAY_LEVEL_MATCH_ZERO_MISMATCH":
        raise SystemExit("Batch 11H D1 replay result mismatch")
    if row_dayun_cal.get("physical_almanac_collation_artifact") != "docs/research/MING-DATONG-1578-NCL-06313-PHYSICAL-ALMANAC-COLLATION-R1.json":
        raise SystemExit("Batch 11H/11I physical almanac artifact binding mismatch")
    snapshot=row_dayun_cal.get("batch_11h_physical_snapshot",{})
    if snapshot.get("batch_id") != "BATCH-11-BAZI-MING-DATONG-1578-D1-SOURCE-REPLAY-H":
        raise SystemExit("Batch 11H physical snapshot binding mismatch")
    if snapshot.get("direct_month_page_match_count") != 11 or snapshot.get("direct_month_page_mismatch_count") != 0:
        raise SystemExit("Batch 11H historical physical snapshot counts regressed")
    if snapshot.get("unresolved_direct_months") != [6] or snapshot.get("complete_12_month_page_collation") is not False:
        raise SystemExit("Batch 11H historical June-gap snapshot regressed")
    if row_dayun_cal.get("physical_almanac_closure_batch") != "BATCH-11-BAZI-MING-DATONG-1578-PHYSICAL-ALMANAC-CLOSURE-I":
        raise SystemExit("Batch 11I physical almanac closure binding mismatch")
    if row_dayun_cal.get("physical_almanac_direct_month_page_match_count") != 12 or row_dayun_cal.get("physical_almanac_direct_month_page_mismatch_count") != 0:
        raise SystemExit("Batch 11I current physical almanac direct-page counts mismatch")
    if row_dayun_cal.get("physical_almanac_unresolved_direct_months") != [] or row_dayun_cal.get("physical_almanac_complete_12_month_page_collation") is not True:
        raise SystemExit("Batch 11I current 12-month physical collation did not close")
    if row_dayun_cal.get("general_historical_calendar_runtime_authorized") is not False or row_dayun_cal.get("audit_status") != "MISSING_FROM_PRODUCT":
        raise SystemExit("Batch 11I prematurely authorized historical calendar runtime")
    pku=by_source_id.get("EXT-PKU-DATONG-1578-ALMANAC")
    if pku is None or pku.get("catalog_identifier") != "北京大学图书馆善本索书号 528.7/1578":
        raise SystemExit("Batch 11H Peking University second-copy bibliography is missing")
    ncl=by_source_id.get("EXT-NCL-DATONG-1578-ALMANAC")
    if ncl is None or ncl.get("physical_collation_artifact") != "docs/research/MING-DATONG-1578-NCL-06313-PHYSICAL-ALMANAC-COLLATION-R1.json":
        raise SystemExit("Batch 11H NCL physical-collation source binding mismatch")
    for path in (MING_DATONG_1578_D1_REPLAY,MING_DATONG_1578_D1_REPLAY_TEST,MING_DATONG_1578_PHYSICAL_COLLATION,MING_DATONG_1578_PHYSICAL_COLLATION_TEST):
        if not path.is_file():
            raise SystemExit(f"Batch 11H artifact/test missing: {path.relative_to(ROOT)}")
    replay1578=json.loads(MING_DATONG_1578_D1_REPLAY.read_text(encoding="utf-8"))
    if replay1578.get("schema") != "MING-DATONG-1578-D1-SOURCE-REPLAY-R1":
        raise SystemExit("Batch 11H D1 replay schema mismatch")
    replay_result=replay1578.get("oracle_result",{})
    if replay_result.get("total_compared_month_starts") != 13 or replay_result.get("mismatch_count") != 0:
        raise SystemExit("Batch 11H D1 13/13 day-level replay regressed")
    if replay1578.get("runtime_selection_authorized") is not False or replay1578.get("general_calendar_arithmetic_certified") is not False:
        raise SystemExit("Batch 11H D1 replay was promoted to general runtime")
    physical1578=json.loads(MING_DATONG_1578_PHYSICAL_COLLATION.read_text(encoding="utf-8"))
    if physical1578.get("schema") != "MING-DATONG-1578-NCL-06313-PHYSICAL-ALMANAC-COLLATION-R1":
        raise SystemExit("Batch 11H physical collation schema mismatch")
    direct=physical1578.get("direct_collation_summary",{})
    if direct.get("directly_rendered_month_pages") != 12 or direct.get("direct_month_identity_matches") != 12 or direct.get("direct_month_size_matches") != 12 or direct.get("direct_month_size_mismatches") != 0:
        raise SystemExit("Batch 11I physical collation 12/12 direct-count regression")
    if direct.get("unresolved_direct_page_months") != [] or direct.get("complete_physical_month_page_collation") is not True:
        raise SystemExit("Batch 11I physical June-page closure regressed")
    month6=next((m for m in physical1578.get("months",()) if m.get("month")==6),None)
    if month6 is None or month6.get("direct_physical_page_status") != "DIRECT_SCREENSHOT_COLLATION":
        raise SystemExit("Batch 11I month-6 direct-render status mismatch")
    if month6.get("physical_month_identity_match") is not True or month6.get("physical_size_label_match") is not True:
        raise SystemExit("Batch 11I month-6 identity/size certification mismatch")
    recovery=physical1578.get("public_scan",{}).get("direct_render_recovery",{})
    if recovery.get("recovered_direct_render") is not True or recovery.get("directly_visible_heading") != "六月小":
        raise SystemExit("Batch 11I June direct-render evidence binding mismatch")
    if physical1578.get("epistemic_firewalls",{}).get("month_title_and_size_as_fine_first_day_ganzhi_glyph_transcription") != "FORBIDDEN":
        raise SystemExit("Batch 11I fine-glyph inference firewall missing")
    if physical1578.get("runtime_selection_authorized") is not False or physical1578.get("general_calendar_arithmetic_certified") is not False:
        raise SystemExit("Batch 11I physical evidence was promoted to runtime arithmetic")
    if row_dayun_cal.get("fixed_point_precision_audit_artifact") != "docs/research/MING-DATONG-1569-FIXED-POINT-PRECISION-AUDIT-R1.json":
        raise SystemExit("Batch 11J precision artifact binding mismatch")
    if row_dayun_cal.get("fixed_point_precision_audit_batch") != "BATCH-11-BAZI-MING-DATONG-FIXED-POINT-PRECISION-J":
        raise SystemExit("Batch 11J precision batch binding mismatch")
    if row_dayun_cal.get("table_generation_precision_map_status") != "CLOSED_FOR_1569_PRIMARY_TABLES_STAGE_SCOPED":
        raise SystemExit("Batch 11J table precision map status mismatch")
    if row_dayun_cal.get("single_global_rounding_rule_status") != "REJECTED_BY_PRIMARY_TABLE_EVIDENCE":
        raise SystemExit("Batch 11J single-global-rounding adjudication regressed")
    if row_dayun_cal.get("dynamic_interpolation_precision_status") != "OPEN_BEYOND_1596_DATONG_WORKED_EXAMPLE":
        raise SystemExit("Batch 11J dynamic precision gate was silently closed")
    for path in (MING_DATONG_1569_FIXED_POINT_PRECISION,MING_DATONG_1569_FIXED_POINT_PRECISION_TEST):
        if not path.is_file():
            raise SystemExit(f"Batch 11J precision artifact/test missing: {path.relative_to(ROOT)}")
    precision=json.loads(MING_DATONG_1569_FIXED_POINT_PRECISION.read_text(encoding="utf-8"))
    if precision.get("schema") != "MING-DATONG-1569-FIXED-POINT-PRECISION-AUDIT-R1":
        raise SystemExit("Batch 11J precision schema mismatch")
    if precision.get("adjudication",{}).get("single_global_rounding_rule") != "REJECTED_BY_PRIMARY_TABLE_EVIDENCE":
        raise SystemExit("Batch 11J precision global-rounding adjudication mismatch")
    if precision.get("adjudication",{}).get("table_generation_precision_map") != "CLOSED_FOR_1569_PRIMARY_TABLES":
        raise SystemExit("Batch 11J table precision map was not closed")
    if precision.get("adjudication",{}).get("dynamic_interpolation_and_d1_conjunction_precision") != "OPEN_BEYOND_THE_1596_DATONG_WORKED_EXAMPLE":
        raise SystemExit("Batch 11J dynamic precision was overclaimed")
    precision_rules={item.get("rule_id"):item for item in precision.get("table_generation_precision_rules",())}
    expected_precision_counts={
        "PREC-DAY-RATE-FLOOR":(168,168),
        "PREC-LOSS-GAIN-SHORTCUT-TRUNCATE":(168,168),
        "PREC-LINE-SPEED-CEILING":(334,334),
        "PREC-XINGDU-SHORTCUT-TRUNCATE":(336,336),
    }
    for rule_id,(evaluated,matched) in expected_precision_counts.items():
        item=precision_rules.get(rule_id)
        if item is None:
            raise SystemExit(f"Batch 11J precision rule missing: {rule_id}")
        actual_eval=item.get("generic_evaluated_cells",item.get("evaluated_cells",item.get("evaluated_rows")))
        actual_match=item.get("generic_ceiling_match_count",item.get("primary_match_count"))
        if (actual_eval,actual_match)!=(evaluated,matched):
            raise SystemExit(f"Batch 11J precision count mismatch: {rule_id}")
    if precision.get("runtime_selection_authorized") is not False or precision.get("general_calendar_arithmetic_certified") is not False:
        raise SystemExit("Batch 11J precision audit was promoted to runtime arithmetic")
    for path in (KYUSHU_OGAWA_1673_COLLATION,KYUSHU_OGAWA_1673_COLLATION_TEST):
        if not path.is_file():
            raise SystemExit(f"Batch 11L Kyushu artifact/test missing: {path.relative_to(ROOT)}")
    kyushu=json.loads(KYUSHU_OGAWA_1673_COLLATION.read_text(encoding="utf-8"))
    if kyushu.get("schema") != "KYUSHU-OGAWA-1673-SHOUSHI-LICHENG-DIRECT-COLLATION-R1":
        raise SystemExit("Batch 11L Kyushu direct-collation schema mismatch")
    if kyushu.get("runtime_effect") != "NONE":
        raise SystemExit("Batch 11L Kyushu evidence was promoted to runtime")
    findings=kyushu.get("findings",{})
    if findings.get("solar_d16",{}).get("result") != "FIELD_STRUCTURALLY_NOT_DIRECTLY_COMPARABLE":
        raise SystemExit("Batch 11L D16 structural non-comparability regressed")
    if findings.get("l114",{}).get("normalized_value") != "9日3489":
        raise SystemExit("Batch 11L L114 direct reading regressed")
    l124=being_l124=findings.get("l124",{})
    if l124.get("raw_ji_xingdu_directly_printed") is not False or l124.get("direct_raw_ji_xingdu_value") is not None:
        raise SystemExit("Batch 11L L124 derived control was mislabeled as a direct raw glyph")
    if l124.get("direct_derived_values",{}).get("疾曆限行度") != "0.0797587":
        raise SystemExit("Batch 11L L124 derived Ji control mismatch")
    if l124.get("goryeosa_received_variant_counterfactual",{}).get("derived_truncate_7dp") != "0.0757785":
        raise SystemExit("Batch 11L L124 Goryeosa counterfactual mismatch")
    if l124.get("classification") != "MECHANICALLY_LINKED_DERIVED_CONTROL_SUPPORTS_MING_1_0281_LINEAGE_NOT_DIRECT_RAW_GLYPH":
        raise SystemExit("Batch 11L L124 evidence classification regressed")
    for path in (KYUJANGGAK_G893_PROVENANCE,KYUJANGGAK_G893_PROVENANCE_TEST):
        if not path.is_file():
            raise SystemExit(f"Batch 11M G893 artifact/test missing: {path.relative_to(ROOT)}")
    g893=json.loads(KYUJANGGAK_G893_PROVENANCE.read_text(encoding="utf-8"))
    if g893.get("schema") != "KYUJANGGAK-G893-PROVENANCE-AND-PUBLIC-FIGURE-CONTROL-R1":
        raise SystemExit("Batch 11M G893 provenance schema mismatch")
    provider=g893.get("provider_catalog",{})
    if provider.get("date") != "15世紀前半（世宗年間 1418-1450）" or provider.get("exact_print_year_stated") is not False:
        raise SystemExit("Batch 11M G893 provider date-range boundary regressed")
    date_adj=g893.get("exact_print_year_adjudication",{})
    if date_adj.get("project_copy_level_value") != "UNRESOLVED_WITHIN_1418_1450_PROVIDER_RANGE":
        raise SystemExit("Batch 11M G893 exact copy year was silently selected")
    claims="\n".join(item.get("claim","") for item in date_adj.get("evidence",()))
    if "1434" not in claims or "1444" not in claims:
        raise SystemExit("Batch 11M G893 1434/1444 conflict evidence is incomplete")
    fig=g893.get("public_object_figure",{})
    if fig.get("direct_target_control_visible") is not False or fig.get("target_value_authorized") is not False:
        raise SystemExit("Batch 11M public opening figure was overpromoted to target-value evidence")
    visible="\n".join(fig.get("directly_visible",()))
    for token in ("授時曆立成卷上","嘉儀大夫太史令臣王恂奉敕撰","太陽冬至前後二象盈初縮末限","初日","八日"):
        if token not in visible:
            raise SystemExit(f"Batch 11M public opening figure binding missing visible token: {token}")
    targets=g893.get("six_target_status",())
    if len(targets) != 6 or not all(item.get("status","").startswith("PENDING_DIRECT_TARGET_PAGE") for item in targets):
        raise SystemExit("Batch 11M G893 target-page fail-closed state regressed")
    if g893.get("epistemic_boundaries",{}).get("algorithm_or_runtime_selection_effect") != "NONE":
        raise SystemExit("Batch 11M G893 provenance evidence was promoted to runtime")
    for path in (JOSEON_1444_WITNESS_ROUTES,JOSEON_1444_WITNESS_ROUTES_TEST):
        if not path.is_file():
            raise SystemExit(f"Batch 11N Joseon witness artifact/test missing: {path.relative_to(ROOT)}")
    joseon=json.loads(JOSEON_1444_WITNESS_ROUTES.read_text(encoding="utf-8"))
    if joseon.get("schema") != "JOSEON-1444-CHILJEONGSAN-EARLY-TABLE-WITNESS-ROUTES-R1":
        raise SystemExit("Batch 11N Joseon witness-route schema mismatch")
    g894=joseon.get("witnesses",{}).get("kyujanggak_g894",{})
    if g894.get("catalog_identifier") != "奎貴894-v.1-3" or g894.get("publication_year") != 1444 or g894.get("edition") != "甲寅字":
        raise SystemExit("Batch 11N G894 provider identity/date boundary regressed")
    if "SEPARATE_WORK_AND_SEPARATE_CATALOG_OBJECT" not in g894.get("relationship_to_g893",""):
        raise SystemExit("Batch 11N G894 was conflated with G893")
    sillok=joseon.get("witnesses",{}).get("sejong_sillok_v156",{})
    if sillok.get("solar",{}).get("article_id") != "wda_50016011" or sillok.get("solar",{}).get("taebaeksan_location") != "60冊 156卷 6張 A面":
        raise SystemExit("Batch 11N Sillok solar table binding regressed")
    if sillok.get("lunar",{}).get("article_id") != "wda_50016016" or sillok.get("lunar",{}).get("taebaeksan_location") != "60冊 156卷 13張 A面":
        raise SystemExit("Batch 11N Sillok lunar table binding regressed")
    targets=joseon.get("target_controls",())
    if len(targets) != 6 or not all("PENDING" in item.get("g894_status","") and "PENDING" in item.get("sillok_status","") and item.get("g893_effect") == "NONE" for item in targets):
        raise SystemExit("Batch 11N witness target fail-closed state regressed")
    boundaries=joseon.get("epistemic_boundaries",{})
    for key in ("g894_as_g893","adjacent_call_number_as_shared_copy_genealogy","sejong_sillok_table_as_1444_g894_same_glyph_surface","article_embedded_image_as_read_numeric_value","value_prepopulation_from_ming_goryeosa_ogawa","source_count_as_variant_adjudication"):
        if boundaries.get(key) != "FORBIDDEN":
            raise SystemExit(f"Batch 11N Joseon evidence boundary regressed: {key}")
    if boundaries.get("algorithm_or_runtime_selection_effect") != "NONE":
        raise SystemExit("Batch 11N Joseon witness evidence was promoted to runtime")
    for path in (SILLOK_NATIVE_DIRECT_COLLATION,SILLOK_NATIVE_DIRECT_COLLATION_TEST):
        if not path.is_file():
            raise SystemExit(f"Batch 11O Sillok native-collation artifact/test missing: {path.relative_to(ROOT)}")
    sillok_native=json.loads(SILLOK_NATIVE_DIRECT_COLLATION.read_text(encoding="utf-8"))
    if sillok_native.get("schema") != "SILLOK-CHILJEONGSAN-NATIVE-DIRECT-COLLATION-R1":
        raise SystemExit("Batch 11O Sillok native-collation schema mismatch")
    if sillok_native.get("audit_batch") != "BATCH-11-BAZI-JOSEON-SILLOK-NATIVE-COLLATION-O":
        raise SystemExit("Batch 11O Sillok native-collation batch binding mismatch")
    if sillok_native.get("runtime_effect") != "NONE" or sillok_native.get("algorithm_reopen_authorized") is not False:
        raise SystemExit("Batch 11O Sillok evidence was promoted to runtime/algorithm authority")
    by_control={item.get("control_id"):item for item in sillok_native.get("lunar_controls",())}
    expected_sillok={
        "VAR-NUM-LUNAR-L8-LOSSGAIN":("益一十〇分五六〇一七七五","10.5601775"),
        "NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING":("五度二十〇四八一一二五","5.20481125"),
        "VAR-NUM-LUNAR-L114-DAYRATE":("九日三四八九","9日3489"),
        "VAR-NUM-LUNAR-L124-JI-XINGDU":("疾一度〇二八一","1.0281"),
        "VAR-NUM-LUNAR-L132-LOSSGAIN":("損七分八八六〇七五","7.886075"),
    }
    if set(by_control) != set(expected_sillok):
        raise SystemExit("Batch 11O Sillok lunar control set mismatch")
    for control_id,(surface,normalized) in expected_sillok.items():
        item=by_control[control_id]
        if item.get("direct_surface") != surface or item.get("normalized_value") != normalized or item.get("reading_confidence") != "HIGH":
            raise SystemExit(f"Batch 11O Sillok direct reading mismatch: {control_id}")
    if sillok_native.get("solar_control",{}).get("status") != "PENDING_DIRECT_SOLAR_TABLE_CONTINUATION_IMAGE":
        raise SystemExit("Batch 11O solar D16 was silently closed")
    nav=sillok_native.get("solar_navigation_evidence",{})
    if nav.get("official_image_tree_walk",{}).get("outcome") != "START_API_UNAVAILABLE":
        raise SystemExit("Batch 11O official image-tree transport snapshot mismatch")
    if nav.get("adjudication") != "SOLAR_D16_REMAINS_PENDING_DIRECT_OFFICIAL_CONTINUATION_IMAGE; NO_FILENAME_OR_NEXT_NODE_VALUE_INFERRED":
        raise SystemExit("Batch 11O D16 fail-closed adjudication mismatch")
    if "BATCH-11-BAZI-JOSEON-SILLOK-NATIVE-COLLATION-O" not in data.get("historical_research_batches",()):
        raise SystemExit("Batch 11O missing from Historical Audit Matrix batch ledger")
    if row_dayun_cal.get("joseon_sillok_native_collation_artifact") != "docs/research/SILLOK-CHILJEONGSAN-NATIVE-DIRECT-COLLATION-R1.json":
        raise SystemExit("Batch 11O Matrix artifact binding mismatch")
    if row_dayun_cal.get("joseon_sillok_direct_lunar_control_count") != 5:
        raise SystemExit("Batch 11O Matrix direct-control count mismatch")
    if row_dayun_cal.get("joseon_sillok_direct_readings",{}).get("l124_ji_xingdu") != "1.0281":
        raise SystemExit("Batch 11O Matrix L124 direct reading mismatch")
    if row_dayun_cal.get("joseon_sillok_solar_d16_status") != "PENDING_DIRECT_OFFICIAL_CONTINUATION_IMAGE":
        raise SystemExit("Batch 11O Matrix solar D16 status mismatch")
    nikh_sillok=by_source_id.get("EXT-NIKH-SEJONG-SILLOK-V156-CHILJEONGSAN-TABLES")
    if nikh_sillok is None or nikh_sillok.get("native_direct_collation_artifact") != "docs/research/SILLOK-CHILJEONGSAN-NATIVE-DIRECT-COLLATION-R1.json":
        raise SystemExit("Batch 11O source-registry artifact binding mismatch")
    if nikh_sillok.get("native_direct_readings",{}).get("VAR-NUM-LUNAR-L124-JI-XINGDU",{}).get("normalized") != "1.0281":
        raise SystemExit("Batch 11O source-registry L124 reading mismatch")
    if nikh_sillok.get("solar_d16_status") != "6A_DIRECT_NATIVE_PAGE_BOUND_BUT_D16_CONTINUATION_NOT_YET_DIRECTLY_BOUND":
        raise SystemExit("Batch 11O source-registry solar status mismatch")
    for path in (KYUJANGGAK_G894_DIRECT_COLLATION,KYUJANGGAK_G894_DIRECT_COLLATION_TEST,KYUJANGGAK_G894_FIELD_BRIDGE,KYUJANGGAK_G894_FIELD_BRIDGE_TEST):
        if not path.is_file():
            raise SystemExit(f"Batch 11P G894 artifact/test missing: {path.relative_to(ROOT)}")
    g894_direct=json.loads(KYUJANGGAK_G894_DIRECT_COLLATION.read_text(encoding="utf-8"))
    if g894_direct.get("schema") != "KYUJANGGAK-G894-DIRECT-TARGET-PAGE-BINDING-R1":
        raise SystemExit("Batch 11P G894 direct-collation schema mismatch")
    if g894_direct.get("catalog_identifier") != "奎貴894-v.1-3" or g894_direct.get("book_cd") != "GK00894_00" or g894_direct.get("item_cd") != "GJB":
        raise SystemExit("Batch 11P G894 provider object identity mismatch")
    if g894_direct.get("runtime_effect") != "NONE" or g894_direct.get("algorithm_reopen_authorized") is not False:
        raise SystemExit("Batch 11P G894 evidence was promoted to runtime")
    g894_by_control={item.get("control_id"):item for item in g894_direct.get("target_pages",())}
    expected_g894={
        "VAR-NUM-LUNAR-L8-LOSSGAIN":("益一十〇分五六〇一七七五","10.5601775"),
        "NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING":("五度二十〇四八一一二五","5.20481125"),
        "VAR-NUM-LUNAR-L114-DAYRATE":("九日三四八九","9日3489"),
        "VAR-NUM-LUNAR-L124-JI-XINGDU":("疾一度〇二八一","1.0281"),
        "VAR-NUM-LUNAR-L132-LOSSGAIN":("損七分八八六〇七五","7.886075"),
    }
    for control_id,(surface,normalized) in expected_g894.items():
        item=g894_by_control.get(control_id,{})
        if item.get("direct_surface") != surface or item.get("normalized_value") != normalized or item.get("reading_confidence") != "HIGH":
            raise SystemExit(f"Batch 11P G894 direct reading mismatch: {control_id}")
    d16=g894_by_control.get("VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE",{})
    if d16.get("target_value_status") != "STRUCTURALLY_NONCOMPARABLE_NO_G894_VALUE" or d16.get("target_value") is not None:
        raise SystemExit("Batch 11P G894 solar D16 structural status mismatch")
    bridge=json.loads(KYUJANGGAK_G894_FIELD_BRIDGE.read_text(encoding="utf-8"))
    if bridge.get("direct_header",{}).get("columns") != ["限數","遲疾曆日率","損益分","遲疾度","疾曆限行度","遲曆限行度"]:
        raise SystemExit("Batch 11P G894 six-column header mismatch")
    method_text="\n".join(item.get("stable_surface","") for item in bridge.get("direct_method_fragments",()))
    for fragment in ("損益分乘之如八百二十而一","以八百二十乘之","遲疾限下行度除之"):
        if fragment not in method_text:
            raise SystemExit(f"Batch 11P G894 method bridge missing: {fragment}")
    if "BATCH-11-BAZI-JOSEON-G894-NATIVE-COLLATION-P" not in data.get("historical_research_batches",()):
        raise SystemExit("Batch 11P missing from Historical Audit Matrix batch ledger")
    if row_dayun_cal.get("joseon_g894_native_collation_artifact") != "docs/research/KYUJANGGAK-G894-DIRECT-TARGET-PAGE-BINDING-R1.json":
        raise SystemExit("Batch 11P Matrix G894 artifact binding mismatch")
    if row_dayun_cal.get("joseon_g894_field_semantic_bridge_artifact") != "docs/research/KYUJANGGAK-G894-LUNAR-FIELD-SEMANTIC-BRIDGE-R1.json":
        raise SystemExit("Batch 11P Matrix G894 field-bridge binding mismatch")
    if row_dayun_cal.get("joseon_g894_direct_lunar_control_count") != 5:
        raise SystemExit("Batch 11P Matrix G894 direct-control count mismatch")
    if row_dayun_cal.get("joseon_g894_direct_readings",{}).get("l124_ji_xingdu") != "1.0281":
        raise SystemExit("Batch 11P Matrix G894 L124 reading mismatch")
    if row_dayun_cal.get("joseon_g894_solar_d16_status") != "STRUCTURALLY_NONCOMPARABLE_TARGET_FIELD_ABSENT":
        raise SystemExit("Batch 11P Matrix G894 D16 status mismatch")
    g894_registry=by_source_id.get("EXT-KYUJANGGAK-CHILJEONGSAN-NAEPYEON-G894-1444")
    if g894_registry is None or g894_registry.get("direct_reading_artifact") != "docs/research/KYUJANGGAK-G894-DIRECT-TARGET-PAGE-BINDING-R1.json":
        raise SystemExit("Batch 11P source-registry G894 artifact binding mismatch")
    if g894_registry.get("direct_readings",{}).get("VAR-NUM-LUNAR-L124-JI-XINGDU",{}).get("normalized") != "1.0281":
        raise SystemExit("Batch 11P source-registry G894 L124 reading mismatch")
    if g894_registry.get("direct_readings",{}).get("VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE",{}).get("status") != "STRUCTURALLY_NONCOMPARABLE_TARGET_FIELD_ABSENT":
        raise SystemExit("Batch 11P source-registry G894 D16 status mismatch")
    actual_status_counts={}
    actual_module_counts={}
    for row in rows:
        actual_status_counts[row["audit_status"]]=actual_status_counts.get(row["audit_status"],0)+1
        actual_module_counts[row["module"]]=actual_module_counts.get(row["module"],0)+1
    if summary.get("status_counts")!=actual_status_counts:
        raise SystemExit("inventory status_counts mismatch")
    if summary.get("module_counts")!=actual_module_counts:
        raise SystemExit("inventory module_counts mismatch")
    print(json.dumps({
        "schema":"FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-R1-MACHINE-GATE",
        "status":"PASS",
        "row_count":len(rows),
        "deterministic_product":"CLOSED",
        "self_inward_transformation":"NOT_YET_FORMALIZED",
        "algorithm_reopen_authorized_count":sum(bool(r["algorithm_reopen_authorized"]) for r in rows),
        "historical_research_batch_count":len(data.get("historical_research_batches",())),
        "audited_row_count":len(data.get("audited_row_ids",())),
        "confirmed_chart_algorithm_defect_count":audit_summary.get("confirmed_chart_algorithm_defect_count"),
        "confirmed_provenance_metadata_defect_count":audit_summary.get("confirmed_provenance_metadata_defect_count"),
        "repaired_provenance_metadata_defect_count":audit_summary.get("repaired_provenance_metadata_defect_count"),
        "historical_candidate_registry_count":audit_summary.get("historical_candidate_registry_count"),
        "historical_candidate_runtime_resolver_count":audit_summary.get("historical_candidate_runtime_resolver_count"),
        "identified_missing_candidate_family_count":audit_summary.get("identified_missing_candidate_family_count"),
    }, ensure_ascii=False, sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
