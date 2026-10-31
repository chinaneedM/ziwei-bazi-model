#!/usr/bin/env python3
"""13MN direct original G893 three-day lane; never infer complete cross-source identity."""
from pathlib import Path
from decimal import Decimal
import json,re
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13MN-G893-D15-D17-DIRECT-ORIGINAL-NUMERIC-LANE-R1.json"
S=R/"docs/PROJECT-CURRENT-STATE-R1.json"
L=R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def check(e,s,l):
    assert e["schema"]=="TIANWEN-13MN-G893-D15-D17-DIRECT-ORIGINAL-NUMERIC-LANE-R1"
    assert e["issue_id"]=="TW-OPEN-0005"
    a=e["acquisition"]
    assert a["previously_archived_artifact_run"]==41144025711 and a["artifact_id"]==13019278183
    assert a["zip_sha256"]=="1d8f10da7c27411bf38ad635494a1b9f4e700fb76cb37b2a7541c075a0ca9835"
    assert a["artifact_is_existing_same_copy_not_new_physical_witness"] is True and a["ocr_used"] is False
    g=e["g893_direct_original"]
    assert g["image_page"]=="002b" and g["native_pixels"]==[1150,2000]
    assert g["original_jpeg_sha256"]=="f9812e8c6a357eb6cd1117bb2af58d816e01030d5b93f34e7094bddb766b2b55"
    assert g["original_rgb_sha256"]=="e3eca1b8f979c1de7ccc5e924d2d493288e7764f92e0a77ad96cf26e80c987f7"
    assert g["day_headings_original_print_right_to_left"]==[19,18,17,16,15,14]
    assert g["header_001a_jpeg_sha256"]=="8b07513ca8aad42ae167a93f22c39f14850c8cd1c345db9ce98c1e0e769226a5"
    assert g["header_001a_rgb_review_crop"]==[710,240,960,1330]
    assert g["header_001a_rgb_review_crop_sha256"]=="30e811c62fff6e063a67a5918a3ad67fe24f04f0f92146747eff3dbfddaec518"
    assert g["header_observed_fields"]==["積日","日差","盈縮加分","盈縮積度"]
    assert g["header_observed_increment_glyph"]=="加一秒八十六少"
    expected=[
      (15,"五分二一七六","5.2176",[782,215,1010,1385],"46684c363d8939a8ee00baff0189501c8709b1d2758eaca94f05e2e530c24fc1"),
      (16,"五分二三六二","5.2362",[610,215,810,1385],"8346fd8854bee5d2a40e1f952dc3bf5ac54ebd15247966a18b65f176967d9add"),
      (17,"五分二五四八","5.2548",[400,215,620,1385],"0b01f531a4416d63a527cb352998230bb0f40c0819083466722fc52cbb430571")]
    rows=g["observations"]
    assert len(rows)==3
    for x,(day,glyph,number,box,hash_) in zip(rows,expected):
        assert x["day"]==day and x["original_print"]==glyph and x["normalized"]==number
        assert x["native_rgb_crop_box"]==box and x["native_rgb_crop_sha256"]==hash_
        assert re.fullmatch(r"[0-9a-f]{64}",hash_)
    vals=[Decimal(x["normalized"]) for x in rows]
    assert vals==[Decimal("5.2176"),Decimal("5.2362"),Decimal("5.2548")]
    assert vals[1]-vals[0]==vals[2]-vals[1]==Decimal("0.0186")
    z=e["independent_1569_print"]
    assert z["pdf_sha256"]=="4c006b7ce131902fe33012d42f62cd2bbc2140affa3d5886e0da02966352cb7c"
    assert z["p14_original_250pct_rgb_sha256"]=="b8c55c92798098afa761b35f00b664584a96399873560cfb0cf939d065b438b1"
    assert z["p15_original_250pct_rgb_sha256"]=="7b35af0e1e802c9346c927a02c67d1681e01b5120c3cf891160126f2018478d5"
    assert z["p15_day_index"]==[15,16,17] and z["p15_printed_decimals"]==[str(x) for x in vals]
    assert z["exact_three_numeric_strings_agree_with_G893_original"] is True
    assert z["same_field_unit_radix_calendar_epoch_confirmed"] is False
    assert z["physical_edition_impression_independence_adjudicated"] is False
    c=e["received_conflict"]
    assert c["official_received_day16"]=="5.1362" and c["G893_original_day16"]=="5.2362"
    assert Decimal(c["official_received_day16"])-vals[1]==Decimal(c["numerical_difference_received_minus_direct_original"])==Decimal("-0.1000")
    assert c["inferred_historical_emendation_not_proven"] is True
    p=e["scope_guard"]
    assert p["G893_D15_D17_source_original_numeric_readings_positive"] is True
    assert p["G893_D16_source_original_numeric_value_positive"] is True
    for k in ("G893_header_to_both_D16_numeric_lanes_complete","same_unit_and_field_across_1569_and_G893_proven","transmission_edge_or_same_physical_copy_inferred"):
        assert p[k] is False
    for k in ("historical_G893_six_cross_original_winners","new_registry_sources","new_physical_copies","matrix_rows_changed","graph_nodes_changed","graph_edges_changed","algorithm_reopens"):
        assert type(p[k]) is int and p[k]==0
    assert p["product"]=="CLOSED" and p["transmission_impact"].startswith("NONE;")
    assert tuple(map(int,s["schema_version"].split(".")))>=(1,976,0)
    assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    focus=s["historical_audit"]["current_focus"]
    assert any(x.startswith("13MN ") for x in focus)
    assert len(focus)==l["binding"]["source_focus_count"]
    assert focus[-1].split(" ",1)[0]==l["binding"]["latest_research_focus_prefix"]
    issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
    assert issue["priority"]=="P0" and issue["status"]=="OPEN"
    assert "docs/research/TIANWEN-13MN-G893-D15-D17-DIRECT-ORIGINAL-NUMERIC-LANE-R1.json" in issue["source_refs"]
    assert "docs/research/TIANWEN-13MN-G893-D15-D17-DIRECT-ORIGINAL-NUMERIC-LANE-R1.md" in issue["source_refs"]
    assert any(x.get("revision_id")=="TW-OPEN-0005-13MN-DIRECT-ORIGINAL-D15-D17-20261031" for x in issue["history"])
    assert any(x.get("id")=="OMISSIONS-13MN-G893-DIRECT-ORIGINAL-D15-D17-20261031" for x in l["checkpoint_log"])
    assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
    assert s["historical_audit"]["external_source_registry_total_unique_count"]==765
    return {"status":"PASS","direct_original_days":[15,16,17],"direct_g893_d16":"5.2362","cross_original_winners":0}
if __name__=="__main__":
    print(json.dumps(check(json.loads(E.read_text(encoding="utf-8")),json.loads(S.read_text(encoding="utf-8")),json.loads(L.read_text(encoding="utf-8"))),ensure_ascii=False))
