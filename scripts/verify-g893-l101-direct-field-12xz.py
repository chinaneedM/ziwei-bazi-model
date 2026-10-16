#!/usr/bin/env python3
"""12XZ G893 direct original L101 glyph/source evidence, forward-only CI guard."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12XZ-G893-L101-DIRECT-FULL-GLYPH-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
XY="docs/research/TIANWEN-12XY-G893-L101-D16-ADJACENT-ORIGINAL-COLUMN-SCOPE-R1.json"
XS="docs/research/TIANWEN-12XS-G893-THREE-TARGET-PIXEL-ROI-GATES-R1.json"
VARIANT="docs/research/MING-DATONG-1569-CROSS-EDITION-VARIANT-LEDGER-R1.json"
def require(q,msg):
    if not q: raise ValueError(msg)
def load():
    return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,STATE,LEDGER,XY,XS,VARIANT))
def verify(d,state,ledger,xy,xs,variant):
    require(d["schema"]=="TIANWEN-12XZ-G893-L101-SOURCE-ORIGINAL-FULL-LITERAL-FIELD-R1","source evidence schema")
    require(d["source_id"]=="EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893" and d["catalog_book_code"]=="GK00893_00","wrong physical original")
    archive=d["archive"]
    require(archive["bytes"]==33525981 and archive["sha256"]=="ee9ecf1de3bb6abe5678e0f8ec8383ef985051e77d091ee40840756e57081107" and archive["original_jpg_sha256_verified"]==archive["original_total_jpg"]==204,"source archive integrity grade")
    src=d["source_page"];hdr=d["structural_header"];n=d["neighbor"];target=d["target"]
    require(src["page_id"]=="032b" and src["source_original_sha256"]=="65457d858a2b2a6c5d04603d4e03430e25e671cbb7f66f6563f9d36798bc300c" and src["source_original_jpeg_reviewed"] is True,"source target page SHA")
    require(hdr["page_id"]=="018b" and hdr["source_original_sha256"]=="4decd1801d832ba5b471b047dd84cca487245038622a589b48552a0fb43ab83a" and hdr["observed_column_label"]=="遲疾度" and hdr["independent_page_sha256_checked_against_report"] is True,"source original table column")
    require(n["previous_same_source_page_id"]=="032a" and n["previous_original_jpeg_sha256"]=="dcaaa1e0e70090c5c4c9b06e3d519f890552acea93f2f18136cf49d9e5e3b098" and n["next_limit_day"]=="一百〇二","same-copy neighbor integrity")
    require(target["control_id"]=="NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING" and target["original_day_heading"]=="一百〇一" and target["field_identity"]=="遲疾度","wrong ancient row/column")
    require(target["original_literal_full_field"]=="五度二十〇分四八一一二五" and target["source_scoped_compact_reading"]=="五度二十〇分四八一一二五" and target["explicit_zero_glyph_count"]==1,"exact original glyph collation changed")
    require(target["original_section_to_normalized_source_value"] is None and target["arithmetic_derivation_and_unit_standardization"]=="PENDING" and target["cross_witness_variant_cause"]=="PENDING" and target["cross_witness_numeric_variant_final_decision"] is None,"original glyph improperly becomes final numeric mechanics")
    px=d["original_rgb_pixel_regions"]
    require(px["source_original_image_size_px"]==[1150,2000] and len(px["regions"])==5 and len({(x["page_id"],x["role"]) for x in px["regions"]})==5,"native original ROI suite")
    roles={x["role"]:x["page_id"] for x in px["regions"]}
    require(roles=={"L101_FULL_SOURCE_GLYPH_COLUMN":"032b","L101_ORIGINAL_DAY_HEADING":"032b","LUNAR_CHIJI_ORIGINAL_FIELD_HEADER":"018b","L102_SAME_COPY_COLUMN_LAYOUT":"032b","L100_SAME_COPY_PRECEDING_LAYOUT":"032a"},"ROI pages and semantics switched")
    expected_rgb={
      "L101_FULL_SOURCE_GLYPH_COLUMN":"adde837c9095558ed7e835dda9a54cc075f7e319ea969ccd396a03177e7dbc22",
      "L101_ORIGINAL_DAY_HEADING":"871dbdfa0851570813681b02b038e3de52747cb68c85d1644f472b994faebc96",
      "LUNAR_CHIJI_ORIGINAL_FIELD_HEADER":"3d59749f6c5d324170144395cc78f29bdf8ddbfc7d1d28f00c2fc9c0856595cc",
      "L102_SAME_COPY_COLUMN_LAYOUT":"bb20854d2524bc3324a0b86b4923ce8249cd616069761964ab5b9e4704cf8d87",
      "L100_SAME_COPY_PRECEDING_LAYOUT":"c69dc73c2a5092204d3fd3c8aeade1ad77b1f024bf61e354ea612f1d79dee8cc"
    }
    for x in px["regions"]:
        b=x["rect_px"]
        require(x["rgb_pixel_sha256"]==expected_rgb[x["role"]],"original RGB ROI integrity changed")
        require(len(b)==4 and all(type(t) is int for t in b) and 0<=b[0]<b[2]<=1150 and 0<=b[1]<b[3]<=2000 and re.fullmatch("[0-9a-f]{64}",x["rgb_pixel_sha256"]) is not None,"invalid original crop")
    require(d["safeguards"]["ocr_used"] is False and d["ocr_used"] is False,"OCR cannot establish original surface")
    require(all(d["safeguards"][k]==0 for k in ("all_six_cross_edition_arithmetic_variant_decisions_completed","new_source_registry_records","new_lineage_edges","algorithm_changes")),"unearned historical or algorithm vote")
    require(xy["original_manual_visual"]["lunar"]["original_complete_target_accumulated_degree_literal"] is None and xy["research_grade"]["complete_source_literal_fields_prior_and_now"]==4,"frozen 12XY historical stage rewritten")
    require(xs["reviews"][1]["field_literal"] is None and xs["reviews"][1]["field_identity_positive"] is False,"frozen ROI candidate rewritten")
    require(variant["philological_normalization_controls"][0]["ming_1569_primary_normalized"]=="5.20481125" and variant["philological_normalization_controls"][0]["krdb_o_surface"]=="五度二十四八一一二五","later comparator not kept separate")
    issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
    require(issue["status"]=="OPEN" and DOC in issue["source_refs"],"unresolved issue/source link lost")
    fields=[x for x in issue["g893_target_field_reviews"] if x["control_id"]==target["control_id"]]
    require(len(fields)==1 and fields[0]["evidence_doc"]==DOC and fields[0]["original_literal_full_field"]==target["original_literal_full_field"] and fields[0]["header_page_id"]=="018b","issue original source field not bound")
    require(len(issue["g893_target_field_reviews"])==3 and len(issue["g893_loss_gain_complete_field_reviews"])==2 and len(issue["g893_target_page_locators"])==6,"wrong full field counts")
    require(any(x.get("event")=="G893_SOURCE_FULL_FIELD_COLLATION_APPEND" and DOC in x.get("evidence_refs",[]) for x in issue["history"]),"append-only source reading event missing")
    require(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,state["schema_version"].split(".")))>=(1,613,0),"handoff state mismatch")
    require(any(x.startswith("12XZ ") for x in state["historical_audit"]["current_focus"]),"current source family not saved")
    require(state["historical_audit"]["row_count"]==222 and state["historical_audit"]["audited_row_count"]==222 and state["historical_audit"]["external_source_registry_total_unique_count"]==706,"historical matrix/source counts")
    require(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"product improperly reopened")
    require(sum(x["status"]!="RESOLVED_WITH_EVIDENCE" for x in ledger["issues"])==11,"research omission silently closed")
    return {"result":"PASS","original_day_pages":6,"complete_original_literal_fields":5,"source_fields_still_unresolved":1,"cross_witness_numeric_decisions":0}
if __name__=="__main__":
    print(json.dumps(verify(*load()),ensure_ascii=False))
