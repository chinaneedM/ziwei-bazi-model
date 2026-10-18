#!/usr/bin/env python3
"""12XX L124 original-folio/field evidence integrity; CI is NOT a source-image reader."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-12XX-G893-L124-DIRECT-ORIGINAL-JI-XINGDU-GLYPH-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
OLDER="docs/research/TIANWEN-12XW-G893-CROSS-EDITION-LIVE-STAGE-OVERLAY-R1.json"

def require(test,msg):
    if not test:raise ValueError(msg)

def load():
    return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (P,LEDGER,STATE,OLDER))

def validate(d,lg,st,old):
    require(d["schema"]=="TIANWEN-12XX-G893-L124-DIRECT-ORIGINAL-JI-XINGDU-GLYPH-R1","12XX source schema")
    require(d["physical_source"]["catalog_book_code"]=="GK00893_00" and d["physical_source"]["physical_copy_count"]==1 and d["physical_source"]["independent_new_witnesses"]==0,"wrong physical source or duplicate witness")
    require(d["archived_original"]["archive_sha256"]=="ee9ecf1de3bb6abe5678e0f8ec8383ef985051e77d091ee40840756e57081107" and d["archived_original"]["verified_source_jpegs"]==204,"source archive unbound")
    require(d["source_page"]["page_id"]=="035b" and d["source_page"]["source_original_sha256"]=="06b5a0ba80c5604576f84b59fc1017b5b0822920e737ef5c96a66b2d82d9e02c","target original page changed")
    require(d["structural_header"]["page_id"]=="018b" and d["structural_header"]["source_original_sha256"]=="4decd1801d832ba5b471b047dd84cca487245038622a589b48552a0fb43ab83a","original title header changed")
    require(d["structural_header"]["observed_column_label"]=="疾曆限行度" and d["target"]["field_identity"]=="疾曆限行度","slow/fast header confusion")
    require(d["target"]["control_id"]=="VAR-NUM-LUNAR-L124-JI-XINGDU" and d["target"]["original_day_heading"]=="一百二十四" and d["target"]["original_literal_full_field"]=="一度〇二八一","source original target glyph changed")
    require(d["target"]["source_scoped_compact_reading"]=="1度0281" and d["target"]["normalized_numeric_value"] is None and d["target"]["historical_cross_witness_mechanical_final_decision"] is None,"original literal inflated to numeric adjudication")
    require(d["target"]["arithmetic_derivation_and_unit_standardization"]=="PENDING" and d["target"]["cross_witness_variant_cause"]=="PENDING","unreplayed mechanics marked complete")
    require(d["guards"]["ocr_used"] is False and all(d["guards"][k] for k in ("older_12xs_roi_snapshot_not_rewritten","older_12xw_overlay_not_rewritten","historical_12xq_not_rewritten")),"source snapshot or manual reading guard lost")
    require(all(d["guards"][k]==0 for k in ("all_six_cross_edition_arithmetic_variant_decisions_completed","new_source_registry_records","new_lineage_edges","algorithm_changes")),"unsupported research/model delta")
    rois=d["original_rgb_pixel_regions"]
    require(rois["original_image_dimensions_px"]==[1150,2000] and len(rois["regions"])==3,"original RGB region count")
    require({x["role"] for x in rois["regions"]}=={"L124_COLUMN_AND_FIELD","L124_DAY_HEADING","ORIGINAL_TABLE_FIELD_HEADER"},"missing original pixel support")
    for row in rois["regions"]:
        x1,y1,x2,y2=row["rect_px"]
        require(0<=x1<x2<=1150 and 0<=y1<y2<=2000 and len(row["rgb_pixel_sha256"])==64,"pixel ROI invalid")
        require(row["page_id"]==("018b" if row["role"]=="ORIGINAL_TABLE_FIELD_HEADER" else "035b"),"ROI page swap")
    issue=next(x for x in lg["issues"] if x["id"]=="TW-OPEN-0005")
    require(issue["status"]=="OPEN" and P in issue["source_refs"],"G893 unresolved source row missing")
    present=[x for x in issue["g893_target_field_reviews"] if x["control_id"]==d["target"]["control_id"]]
    require(len(present)==1 and present[0]["evidence_doc"]==P and present[0]["original_literal_full_field"]==d["target"]["original_literal_full_field"],"live original L124 field missing/mismatch")
    require(len(issue["g893_target_field_reviews"])>=2 and len(issue["g893_loss_gain_complete_field_reviews"])==2,"source full field count not four")
    require(len(issue["g893_target_page_locators"])==6 and len(issue["g893_field_identity_roi_reviews"])==3,"historical day/ROI evidence dropped")
    require(any(x.get("event")=="G893_SOURCE_FULL_FIELD_COLLATION_APPEND" and P in x.get("evidence_refs",[]) for x in issue["history"]),"append-only direct source review absent")
    require(st["schema_version"]==lg["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,st["schema_version"].split(".")))>= (1,611,0),"state guard version")
    require(any(x.startswith("12XX ") for x in st["historical_audit"]["current_focus"]), "new source focus missing")
    require(old["current_state_version"]=="1.610.0" and old["complete_source_literal_field_count"]==3,"12XW historical snapshot overwritten")
    require(st["historical_audit"]["row_count"]==st["historical_audit"]["audited_row_count"]==222 and st["historical_audit"]["external_source_registry_total_unique_count"]>=706,"provenance counts changed")
    require(st["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and st["invariants"]["algorithm_reopen_count"]==0,"no new algorithm authorized")
    require(sum(x["status"]!="RESOLVED_WITH_EVIDENCE" for x in lg["issues"])==11,"unclosed issue erased")
    return {"status":"PASS","target":"G893-L124","original_complete_fields":4,"remaining_original_fields":2,"cross_witness_numeric_decisions":0}

if __name__=="__main__":
    print(json.dumps(validate(*load()),ensure_ascii=False))
