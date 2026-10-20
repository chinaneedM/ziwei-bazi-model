#!/usr/bin/env python3
"""13BF: bounded original cumulative/long source arithmetic, not header-law adjudication."""
import json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PC="docs/research/TIANWEN-13BF-GORYEOSA-D14-D17-ORIGINAL-ACCUMULATIVE-LOCAL-INDEX-OFFSET-R1.json"
PBE="docs/research/TIANWEN-13BE-GORYEOSA-D16-ORIGINAL-LONG-LANE-DUAL-COPY-COLLATION-R1.json"
PBD="docs/research/TIANWEN-13BD-GORYEOSA-D16-D17-ORIGINAL-MULTICOLUMN-IMAGE-PROBE-R1.json"
PYZ="docs/research/TIANWEN-12YZ-GORYEOSA-D14-D20-INTRATABLE-THREE-COLUMN-RECEIVED-ARITHMETIC-R1.json"
MD=PC.replace(".json",".md")
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
SOURCE={
 "NAJ-282-0006-PHYSICAL51":[
 ([930,870,965,1775],"d03684c941c0221c36eb2921c88bc27503742a88bfd3e0eea84db57aedba457a"),
 ([775,870,815,1775],"7e31157abde08accdd6c4382a184c40f506750ad29ad818b874d48d20bc07be4"),
 ([885,870,940,1775],"1105124fd5110196c64d0b53b1303b4e6693ac161250eb338a58182afea734a7")],
 "WASEDA-RI06-02809-BOOK33":[
 ([1760,700,1810,1470],"e374e74999f707ce6999f8a544d87fa1fb26e3f316156cc462c7c284505293e9"),
 ([1600,700,1650,1470],"f7eb6a5c5318151e8cf5bd8ee08cd8c938b614d14be2b522c42b4bb5bc2cf503"),
 ([1715,700,1777,1470],"d11b0dfaf56a5e75399dfbfa9299bbd6366366fa4494d92b24d2b7ce681b89a8")]}
def check(e,be,bd,yz,ledger,state):
 assert e["schema"]=="TIANWEN-13BF-HISTORICAL-ORIGINAL-D14-D17-CUMULATIVE-LOCAL-PREDECESSOR-LONG-DIFFERENCE-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 p=e["prior_evidence"]
 assert (p["source_capture"],p["day16_17_source_original"],p["received_comparator"])==(PBD,PBE,PYZ)
 assert p["action_run_id"]==be["source_capture"]["action_run_id"]==39421117170
 assert p["source_artifact_id"]==be["source_capture"]["artifact_id"]==12263559032
 assert e["new_original_image_objects"]==0 and "NO_OCR" in e["source_scope"]
 s=e["manuscript_originals"]
 assert len(s)==2 and [x["holding"] for x in s]==list(SOURCE)
 assert [x["holding"] for x in be["source_original_image_reviews"]]==list(SOURCE)
 roles=["DAY14_LONG","DAY15_LONG","DAY15_CUMULATIVE_APPARENT_LAYOUT"]
 glyphs=["四百四十〇〇二三九","四百三十四八二四九","六千六百九十五八一三六"]
 digits=["440.0239","434.8249","6695.8136"]
 for r,old,original in zip(s,be["source_original_image_reviews"],bd["sources"]):
    assert r["source_JPEG_sha256"]==old["original_image_sha256"]
    assert r["source_JPEG_sha256"]==(original["existing_JPEG_sha256"] if "existing_JPEG_sha256" in original else original["embedded_JPEG_sha256"])
    assert len(r["new_original_roi"])==3
    for i,z in enumerate(r["new_original_roi"]):
        assert z["role"]==roles[i] and z["literal"]==glyphs[i] and z["decimal"]==digits[i]
        assert (z["bbox"],z["rgb_pixel_sha256"])==SOURCE[r["holding"]][i]
 c=e["previous_day_original_cumulative_slots_from_13be"]
 assert [(z["day"],z["layout_decimal"],z["literal"]) for z in c]==[
    (16,"7135.8375","七千一百三十五八三七五"),
    (17,"7570.6624","七千五百七十〇六六二四")]
 original=be["source_original_image_reviews"]
 for row in original:
    assert row["day_rois"][0]["adjacent_cumulative_original"]==c[0]["literal"]
    assert row["day_rois"][1]["adjacent_cumulative_original"]==c[1]["literal"]
    assert row["day_rois"][0]["long_original"]=="四百二十九六〇七三"
 numbers={15:Decimal(digits[2]),16:Decimal(c[0]["layout_decimal"]),17:Decimal(c[1]["layout_decimal"])}
 longs={14:Decimal(digits[0]),15:Decimal(digits[1]),16:Decimal(be["roman_decimal_bridge"]["day16_long"])}
 edges=e["bounded_original_local_numeric_equations"]
 assert len(edges)==2
 for z,d in zip(edges,(15,16)):
    assert z["original_layout_day_from"]==d and z["original_layout_day_to"]==d+1
    assert z["matches_original_long_day"]==d-1
    assert Decimal(z["cum_delta"])==numbers[d+1]-numbers[d]==longs[d-1]==Decimal(z["long_value"])
    assert Decimal(z["does_not_match_original_long_at_from_day"])==longs[d]
    assert longs[d-1]!=longs[d]
 bridge=e["received_digital_text_index_bridge"]
 assert bridge["grade"]=="MODERN_INSTITUTIONAL_TEXT_COMPARATOR_NOT_NEW_ORIGINAL"
 for rec in bridge["observed_matches"]:
    day=rec["original_layout_day"];recv=rec["received_row_day"]
    assert day in (15,16,17) and recv==day-1
    assert Decimal(rec["cum"])==numbers[day]
    assert yz["modern_received_rows"][recv-14]["cumulative"]==rec["cum"]
 assert [z["original_layout_day"] for z in bridge["observed_matches"]]==[15,16,17]
 assert bridge["can_promote_received_row_shift_to_historical_header_definition"] is False
 assert bridge["do_not_claim_modern_editorial_error_or_original_page_error"] is True
 assert e["local_source_arithmetic_status"]=="TWO_ORIGINAL_PHYSICAL_IMAGE_LANES_SHOW_TWO_PREDECESSOR_LONG_DIFFERENCES"
 assert e["original_heading_and_all_day_scope"].startswith("UNRESOLVED")
 assert e["physical_copy_date_or_print_lineage_independence"]=="UNRESOLVED"
 assert e["ancient_archetype_one_or_two"]=="UNRESOLVED" and e["cross_work_G893_same_unit"]=="UNPROVEN"
 for key in ("independent_stemmatic_votes_added","original_physical_witnesses_added","registry_source_entries_added","transmission_graph_nodes_added","transmission_graph_edges_added","matrix_rows_added","algorithm_reopens"):
    assert e[key]==0
 assert e["open_research_issues"]==11 and e["product_R1"]=="CLOSED"
 issue=next(z for z in ledger["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert issue["source_refs"].count(MD)==issue["source_refs"].count(PC)==1
 assert issue["source_refs"].index(PC)==issue["source_refs"].index(MD)+1
 assert any(x.get("event")=="GORYEOSA_13BF_TWO_ORIGINAL_CUMULATIVE_LOCAL_LEADLAG_ARITHMETIC" for x in issue["history"])
 assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert any(x.startswith("13BF ") for x in state["historical_audit"]["current_focus"])
 assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
 assert ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ")[0]
 assert ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
 assert len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==11
 return True
if __name__=="__main__":
 assert check(load(PC),load(PBE),load(PBD),load(PYZ),load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"),load("docs/PROJECT-CURRENT-STATE-R1.json"))
 print("13BF source original 2-edge cumulative predecessor long arithmetic PASS")
