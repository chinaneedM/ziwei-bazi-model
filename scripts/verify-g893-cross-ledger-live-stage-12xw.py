#!/usr/bin/env python3
"""Validate the 12XW G893 archival-stage versus current evidence reconciliation."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P="docs/research/"
OVERLAY=P+"TIANWEN-12XW-G893-CROSS-EDITION-LIVE-STAGE-OVERLAY-R1.json"
VARIANT=P+"MING-DATONG-1569-CROSS-EDITION-VARIANT-LEDGER-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
XR=P+"TIANWEN-12XR-G893-L114-DAYRATE-FULL-FIELD-SEPARATION-R1.json"
XU=P+"TIANWEN-12XU-G893-L8-L132-SOURCE-GLYPH-AND-SYMMETRIC-LOCATORS-R1.json"
XS=P+"TIANWEN-12XS-G893-THREE-TARGET-PIXEL-ROI-GATES-R1.json"

def need(test, reason):
    if not test:
        raise ValueError(reason)

def get(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def blobsha(path):
    b=(ROOT/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+bytes([0])+b).hexdigest()

def read_inputs():
    return tuple(get(x) for x in (OVERLAY,VARIANT,LEDGER,STATE,XR,XU,XS))

def verify(o,v,lg,s,xr,xu,xs):
    need(o["schema"]=="TIANWEN-12XW-G893-CROSS-EDITION-LIVE-STAGE-OVERLAY-R1","12XW evidence schema")
    need(o["historic_variant_ledger"]==VARIANT and o["historic_variant_ledger_git_blob_sha"]==blobsha(VARIANT),"archival variant ledger changed without re-evaluation")
    w=[x for x in v["comparison_witnesses"] if x["source_id"]==o["source_id"]]
    need(len(w)==1 and w[0]["direct_target_image_status"]==o["historic_g893_witness_stage"],"old G893 acquisition-stage evidence erased")
    need(o["archival_statement_policy"]=="PRESERVE_EARLIER_SNAPSHOT_NO_SILENT_REWRITE_AND_NEVER_USE_OLD_STAGE_AS_LIVE_TASK","old stage incorrectly made live")
    issue=next(x for x in lg["issues"] if x["id"]==o["issue_id"])
    need(issue["id"]=="TW-OPEN-0005" and issue["status"]=="OPEN","unresolved original targets prematurely closed")
    loc=issue["g893_target_page_locators"]
    expect=[{k:x[k] for k in ("control_id","page_id","page_sha256","evidence_doc")} for x in loc]
    need(len(expect)==6 and o["original_day_page_locators"]==expect,"six source page ID/SHA mismatches")
    need(all(x["numeric_value"] is None and x["status"]=="LOCATED_NUMERIC_UNADJUDICATED" for x in loc),"locator promoted to number")
    fields=[{k:x[k] for k in ("control_id","page_id","header_page_id","field_identity","complete_original_literal")} for x in xu["original_fields"]]
    fields.append({"control_id":xr["target"]["control_id"],"page_id":xr["source_page"]["page_id"],"header_page_id":xr["structural_header"]["page_id"],"field_identity":xr["structural_header"]["observed_column_label"],"complete_original_literal":xr["target"]["original_literal_full_field"]})
    fields.sort(key=lambda x:x["control_id"])
    need(len(fields)==3 and o["complete_source_literal_fields"]==fields,"three full source glyph columns do not match original evidence")
    completed={x["control_id"] for x in fields}
    reviewed={x["control_id"] for x in issue["g893_target_field_reviews"]+issue["g893_loss_gain_complete_field_reviews"]}
    need(reviewed==completed,"original field review and live omission issue out of sync")
    remaining=[x["control_id"] for x in loc if x["control_id"] not in completed]
    need(len(remaining)==3 and remaining==o["unresolved_source_full_field_controls"],"unresolved three source fields hidden")
    need({x["control_id"] for x in xs["reviews"]}==set(remaining),"ROI source regions confused with complete original field")
    need(all(x["field_identity_positive"] is False and x["field_literal"] is None and x["numeric_value"] is None for x in xs["reviews"]),"unresolved ROI incorrectly given a glyph/numeric decision")
    need(o["same_copy_symmetric_locator_only"]==[{"limit":x["limit"],"page_id":x["page_id"]} for x in issue["g893_same_copy_symmetric_control_locators"]],"same-copy symmetry locator mismatch")
    need(xr["target"]["arithmetic_derivation_and_unit_standardization"]=="PENDING" and all(x["normalized_numeric_value"] is None for x in xu["original_fields"]),"literal mechanically over-normalized")
    need(o["final_cross_edition_mechanical_variant_decisions"]==xu["scope"]["full_numeric_mechanical_variant_decisions"]==0,"unearned cross-witness numeric decision")
    need((o["current_g893_original_jpeg_sha_verified_count"],o["current_g893_original_rgb_roi_verified_count"],o["total_target_controls"],o["complete_source_literal_field_count"])==(204,9,6,3),"G893 source-stage counters changed")
    need(all(o[k] is True for k in ("no_new_source_votes","no_new_lineage_edges","no_algorithm_reopen")),"unsupported positive source/lineage/algorithm delta")
    need(o["all_open_research_issues"]==sum(x["status"]!="RESOLVED_WITH_EVIDENCE" for x in lg["issues"])==11,"open research omissions miscounted")
    need(OVERLAY in issue["source_refs"] and issue["history"][-1]["event"]=="CROSS_LEDGER_STAGE_RECONCILIATION","append-only evidence event absent")
    need(all((ROOT/p).is_file() for p in o["evidence_refs"]),"referenced source evidence missing")
    need(s["schema_version"]==o["current_state_version"]==lg["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"research state/ledger desync")
    need(s["historical_audit"]["current_focus"][-1].startswith("12XW "),"latest G893 focus stale")
    need((s["historical_audit"]["row_count"],s["historical_audit"]["audited_row_count"],s["historical_audit"]["external_source_registry_total_unique_count"])==(222,222,706),"Matrix/source registry scope changed")
    need(s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0,"chart algorithm reopened")
    return {"status":"PASS","original_day_pages":6,"fully_collated_original_fields":3,"missing_full_original_fields":3,"cross_edition_numeric_decisions":0}

def main():
    print(json.dumps(verify(*read_inputs()),ensure_ascii=False))
if __name__=="__main__":
    main()
