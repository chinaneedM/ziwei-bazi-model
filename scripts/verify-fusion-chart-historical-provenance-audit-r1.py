#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"
SOURCE_REGISTRY = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
BAZI_RELATION_CANDIDATES = ROOT / "src" / "fortune_training" / "bazi_chart" / "historical_relation_candidates.py"
BAZI_RELATION_CANDIDATE_TEST = ROOT / "tests" / "test_bazi_historical_relation_candidates_r1.py"
BAZI_TEMPORAL_ANNOTATIONS = ROOT / "src" / "fortune_training" / "bazi_application" / "temporal_annotations.py"
BAZI_TEMPORAL_HIDDEN_ORDER_TEST = ROOT / "tests" / "test_bazi_temporal_hidden_stem_order_lineage_r1.py"

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
    if by_source_id.get("EXT-ZIWEI-QVXIAN-TRUE-SOLAR-2022") is None:
        raise SystemExit("Batch 08C modern Ziwei true-solar witness is missing")
    if by_source_id.get("EXT-CTEXT-ZIWEI-DATAWIKI-LATE-ZI") is None:
        raise SystemExit("Batch 08D late-Zi dispute witness is missing")
    if by_source_id.get("EXT-XUANMEN-LINGDONGLAI-LATE-ZI") is None:
        raise SystemExit("Batch 08D late-Zi practice witness is missing")
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
    if audit_summary.get("confirmed_provenance_metadata_defect_count", 0) < 9:
        raise SystemExit("known provenance metadata defects are missing")
    if audit_summary.get("repaired_provenance_metadata_defect_count", 0) < 9:
        raise SystemExit("known provenance metadata repairs are missing")
    if audit_summary.get("historical_candidate_runtime_resolver_count", 0) < 2:
        raise SystemExit("source-scoped historical candidate runtime resolver is missing")
    if audit_summary.get("historical_candidate_registry_count", 0) < 2:
        raise SystemExit("historical candidate registry is missing")
    if audit_summary.get("historical_candidate_extension_count", 0) < 4:
        raise SystemExit("historical candidate extension accounting regressed")
    if audit_summary.get("identified_missing_candidate_family_count", 0) < 12:
        raise SystemExit("known historical candidate gaps are missing")
    defect_ids=[row.get("defect_id") for row in rows if row.get("defect_id")]
    if len(defect_ids)!=len(set(defect_ids)):
        raise SystemExit("duplicate historical provenance defect_id")
    summary=data.get("inventory_summary",{})
    if summary.get("row_count")!=len(rows):
        raise SystemExit("inventory row_count mismatch")
    audited_ids=data.get("audited_row_ids",())
    if summary.get("audited_row_count")!=len(audited_ids) or len(audited_ids) < 158:
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
    if temporal_by_id["HPA-ZTEMP-004"]["audit_status"]!="MISSING_FROM_PRODUCT":
        raise SystemExit("1581 day-anchored flow-hour product gap was not preserved")
    if temporal_by_id["HPA-ZTEMP-006"]["audit_status"]!="MISSING_FROM_PRODUCT":
        raise SystemExit("Zhongzhou leap-month product gap was not preserved")
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
