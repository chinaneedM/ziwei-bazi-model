#!/usr/bin/env python3
"""12XY G893 native geometric context guard: ROI metadata is never an ancient numerical vote."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12XY-G893-L101-D16-ADJACENT-ORIGINAL-COLUMN-SCOPE-R1.json"
OLDER="docs/research/TIANWEN-12XS-G893-THREE-TARGET-PIXEL-ROI-GATES-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"

def need(t,message):
    if not t: raise ValueError(message)

def load():
    return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,OLDER,STATE,LEDGER))

EXPECTED={
"001a":"8b07513ca8aad42ae167a93f22c39f14850c8cd1c345db9ce98c1e0e769226a5",
"002b":"f9812e8c6a357eb6cd1117bb2af58d816e01030d5b93f34e7094bddb766b2b55",
"018b":"4decd1801d832ba5b471b047dd84cca487245038622a589b48552a0fb43ab83a",
"032a":"dcaaa1e0e70090c5c4c9b06e3d519f890552acea93f2f18136cf49d9e5e3b098",
"032b":"65457d858a2b2a6c5d04603d4e03430e25e671cbb7f66f6563f9d36798bc300c",
}
EXPECTED_ROLES={
"001a":{"SOLAR_ORIGINAL_HEADER"},
"002b":{"D15_D16_D17_ORIGINAL_NEIGHBORS","D16_DAY_AND_ADJACENT_FIELDS"},
"018b":{"LUNAR_ORIGINAL_MULTI_COLUMN_HEADER"},
"032a":{"L100_ADJACENT_SOURCE_PAGE"},
"032b":{"L101_L102_SOURCE_LAYOUT","L101_MULTI_COLUMN_CONTEXT","L101_DAY_HEADER"},
}

def verify(d,older,state,lg):
    need(d["schema"]=="TIANWEN-12XY-G893-L101-D16-ADJACENT-ORIGINAL-COLUMN-SCOPE-R1","schema")
    need(d["source_id"]=="EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893" and d["catalog_book_code"]=="GK00893_00","physical witness")
    require_archive=d["source_archive"]
    need(require_archive["bytes"]==33525981 and require_archive["sha256"]=="ee9ecf1de3bb6abe5678e0f8ec8383ef985051e77d091ee40840756e57081107","recovered source ZIP")
    need(require_archive["original_jpg_sha256_rechecked"]==require_archive["total_original_jpg"]==204,"204 original pages not replayed")
    originals={x["page_id"]:x for x in d["source_pages"]}
    need(len(d["source_pages"])==len(originals)==5 and {k:x["jpeg_sha256"] for k,x in originals.items()}==EXPECTED,"original JPEG page/hash mismatch")
    for pid, row in originals.items():
        need(row["native_dimensions"]==[1150,2000] and row["one_physical_holding"] is True,"source image copy count/dimensions")
        need(row["source_issued_url"].startswith("https://kyudb.snu.ac.kr/ImageServlet.do?") and ("GK00893_00IH_0001_"+pid+".jpg") in row["source_issued_url"],"original page source URL")
    regions=d["replayed_original_rgb_regions"]
    need(len(regions)==8 and len({(x["page_id"],x["role"]) for x in regions})==8,"original 8 ROI scope")
    roles={}
    for x in regions:
        roles.setdefault(x["page_id"],set()).add(x["role"])
        l,t,r,b=x["rect_px"]
        need(type(l) is type(t) is type(r) is type(b) is int and 0<=l<r<=1150 and 0<=t<b<=2000,"original ROI pixel coordinate")
        need(re.fullmatch("[0-9a-f]{64}",x["rgb_pixel_sha256"]) is not None,"original RGB sha malformed")
    need(roles==EXPECTED_ROLES,"expected original page/header/neighbor ROI not recorded")
    manual=d["original_manual_visual"]
    need(manual["lunar"]["original_heading_seen"]=="一百〇一" and manual["lunar"]["same_copy_next_limit_seen"]=="一百〇二" and manual["lunar"]["preceding_day_header_seen"]=="一百","L101 neighbor identification")
    need(manual["lunar"]["original_complete_target_accumulated_degree_literal"] is None and manual["lunar"]["target_accumulated_degree_column_exact_identity"]=="UNRESOLVED","unearned L101 numerical column vote")
    need(manual["solar"]["original_heading_seen"]=="十六日" and manual["solar"]["same_copy_adjacent_day_headings_seen"]==["十五日","十七日"],"solar neighbor scope")
    need(manual["solar"]["original_second_difference_numeric_literal"] is None and manual["solar"]["original_second_difference_column_exact_identity"]=="UNRESOLVED_NO_ONE_TO_ONE_MAPPING_PROVED","D16 false field mapping")
    need(manual["solar"]["observed_header_terms"]==["積日","日差加一秒八十六少","盈縮加分","盈縮積度"],"solar original header family")
    need(manual["lunar"]["do_not_assign_ming_5_20481125_to_this_source"] is True and manual["solar"]["do_not_assign_ming_5_2362_or_goryeosa_5_1362_to_this_source"] is True,"external digital value substituted for G893")
    need(d["source_specific_comparison"]["all_are_external_witnesses_not_g893_readings"] is True,"witness mixing")
    grade=d["research_grade"]
    need(grade["complete_source_literal_fields_prior_and_now"]==4 and grade["original_target_day_pages_located"]==6 and grade["final_cross_witness_numeric_or_mechanical_decisions"]==0,"unsupported numeric grade promotion")
    need(len(grade["remaining_two_source_fields"])==2 and set(grade["remaining_two_source_fields"])=={"NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING","VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE"},"missing original targets concealed")
    need(all(grade[k]==0 for k in ("new_primary_source_records","new_independent_print_votes","new_genealogy_edges","new_algorithm_reopens")),"unsupported source/stemma/algorithm changes")
    need(grade["old_12xs_12xw_12xx_snapshots_mutated"] is False and older["reviews"][0]["field_literal"] is None and older["reviews"][1]["field_literal"] is None,"old non-numeric source snapshots overwritten")
    issue=next(x for x in lg["issues"] if x["id"]=="TW-OPEN-0005")
    need(issue["status"]=="OPEN" and DOC in issue["source_refs"],"omission source/case link")
    scopes=issue.get("g893_contextual_column_geometry_reviews",[])
    need(len(scopes)==1 and scopes[0]["evidence_doc"]==DOC and set(scopes[0]["source_page_ids"])==set(EXPECTED),"missing append-only source geometry")
    need(scopes[0]["fully_adjudicated_original_target_fields_added"]==0 and scopes[0]["numeric_values_adjudicated"]==0,"overclaimed contextual grade")
    need(any(x.get("event")=="G893_CONTEXTUAL_ORIGINAL_COLUMN_GEOMETRY_APPEND" and DOC in x.get("evidence_refs",[]) for x in issue["history"]),"no append-only research evidence event")
    need(state["schema_version"]==lg["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,state["schema_version"].split(".")))>= (1,612,0),"state/omission synchronization")
    need(any(x.startswith("12XY ") for x in state["historical_audit"]["current_focus"]) and state["historical_audit"]["row_count"]==222,"research focus not advanced")
    need(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"chart CLOSED violated")
    need(sum(x["status"]!="RESOLVED_WITH_EVIDENCE" for x in lg["issues"])==11,"open research issues lost")
    return {"status":"PASS","original_page_sha_refs":5,"source_native_rgb_regions":8,"complete_original_target_fields":4,"unresolved_original_target_fields":2,"cross_witness_numeric_decisions":0}

if __name__=="__main__":
    print(json.dumps(verify(*load()),ensure_ascii=False))
