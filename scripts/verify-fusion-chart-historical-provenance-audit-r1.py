#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"

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
    "紫微本命","十二宫","主星","辅星","杂曜","四化","庙旺落陷","流年","流月",
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
    summary=data.get("inventory_summary",{})
    if summary.get("row_count")!=len(rows):
        raise SystemExit("inventory row_count mismatch")
    print(json.dumps({
        "schema":"FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-R1-MACHINE-GATE",
        "status":"PASS",
        "row_count":len(rows),
        "deterministic_product":"CLOSED",
        "self_inward_transformation":"NOT_YET_FORMALIZED",
        "algorithm_reopen_authorized_count":sum(bool(r["algorithm_reopen_authorized"]) for r in rows),
    }, ensure_ascii=False, sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
