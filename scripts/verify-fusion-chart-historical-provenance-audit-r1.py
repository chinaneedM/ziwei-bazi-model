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
    for source_id in ("EXT-KOTENMON-DAMING-DATONG-1569","EXT-NCL-DATONG-1578-ALMANAC","EXT-IHNS-MING-DATONG-COMPILATION-2019","EXT-MINGSHILU-WANLI-1578-MONTH-STARTS","EXT-WANLI-QIJUZHU-1578-MONTH-CORROBORATION","EXT-WIKISOURCE-GUJIN-LULIKAO-V49-DATONG","EXT-SHAO-LIYONG-DATONG-1527-2011","EXT-YTLIU-MING-DATONG-CONJUNCTION-D1-D2","EXT-SHAO-LI-ZHANG-REAL-NEW-MOON-1996","EXT-AA-LI-ZHANG-SYZYGY-1998","EXT-WIKISOURCE-MINGSHI-V35-DATONG-TIME","EXT-CTEXT-MINGSHI-ASTRONOMY-BEIJING-NANJING-CLOCK","EXT-WIKISOURCE-WANLI-YEHUO-DATONG-DAYLENGTH","EXT-RAA-MIHN-SHOUSHI-AFFILIATED-2014","EXT-WILEY-CHOI-DATONGLI-SUNRISE-2018","EXT-LOC-DATONG-1524-ALMANAC"):
        if by_source_id.get(source_id) is None:
            raise SystemExit(f"Batch 11D/11E Ming Datong source witness missing: {source_id}")
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
    if audit_summary.get("identified_missing_candidate_family_count", 0) < 13:
        raise SystemExit("known historical candidate gaps are missing")
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
        raise SystemExit("Batch 11H physical almanac artifact binding mismatch")
    if row_dayun_cal.get("physical_almanac_direct_month_page_match_count") != 11 or row_dayun_cal.get("physical_almanac_direct_month_page_mismatch_count") != 0:
        raise SystemExit("Batch 11H physical almanac direct-page counts mismatch")
    if row_dayun_cal.get("physical_almanac_unresolved_direct_months") != [6] or row_dayun_cal.get("physical_almanac_complete_12_month_page_collation") is not False:
        raise SystemExit("Batch 11H unresolved June-page firewall regressed")
    if row_dayun_cal.get("general_historical_calendar_runtime_authorized") is not False or row_dayun_cal.get("audit_status") != "MISSING_FROM_PRODUCT":
        raise SystemExit("Batch 11H prematurely authorized historical calendar runtime")
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
    if direct.get("directly_rendered_month_pages") != 11 or direct.get("direct_month_size_mismatches") != 0:
        raise SystemExit("Batch 11H physical collation direct-count regression")
    if direct.get("unresolved_direct_page_months") != [6] or direct.get("complete_physical_month_page_collation") is not False:
        raise SystemExit("Batch 11H physical June-page uncertainty was silently collapsed")
    month6=next((m for m in physical1578.get("months",()) if m.get("month")==6),None)
    if month6 is None or month6.get("direct_physical_page_status") != "PDF_PAGE_SCREENSHOT_TOOL_ERROR_NOT_DIRECTLY_CERTIFIED":
        raise SystemExit("Batch 11H month-6 technical-access status mismatch")
    if physical1578.get("epistemic_firewalls",{}).get("infer_month6_direct_physical_reading_from_neighbors") != "FORBIDDEN":
        raise SystemExit("Batch 11H month-6 inference firewall missing")
    if physical1578.get("runtime_selection_authorized") is not False or physical1578.get("general_calendar_arithmetic_certified") is not False:
        raise SystemExit("Batch 11H physical evidence was promoted to runtime arithmetic")
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
