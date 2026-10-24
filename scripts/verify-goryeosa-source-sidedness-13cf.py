#!/usr/bin/env python3
"""13CF: immutable source-ROI positions; never infer a historical C field from proximity."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CF-GORYEOSA-SOURCE-D17-SIDEDNESS-AND-FOLIO-FIELD-FIREWALL-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
SOURCES={"CE":{"path":"docs/research/TIANWEN-13CE-GORYEOSA-ORIGINAL-FOLIO-SEAM-TOPOLOGY-R1.json","sha":"340416f4c479a44f76169e379d79f5773527eade"},"CB":{"path":"docs/research/TIANWEN-13CB-WASEDA-D16-D17-ORIGINAL-FOLIO-SEAM-ARITHMETIC-BOUNDARY-R1.json","sha":"b7a5270cb7a3d91bc49adef6a4c7612f1dea700e"},"CC":{"path":"docs/research/TIANWEN-13CC-NAJ-GORYEOSA-D17-D18-CANVAS-SEAM-AND-CUMULATIVE-FIELD-BOUNDARY-R1.json","sha":"4d6e732a5d2c7286ba36b174d4ef45c42ec12113"},"BO":{"path":"docs/research/TIANWEN-13BO-GORYEOSA-WASEDA-P23-D17-D18-ORIGINAL-HEADER-CUMULATIVE-LONG-R1.json","sha":"e4115ce8d121c976bd9866b2307bb7662e09fc4d"}}

def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def bind_sources(e):
    assert e["immutable_prior_git_blobs"]==SOURCES
    out={}
    for k,v in SOURCES.items():
        b=(ROOT/v["path"]).read_bytes()
        sha=hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+bytes([0])+b).hexdigest()
        assert sha==v["sha"], (k,"prior original research SHA mismatch",sha)
        out[k]=json.loads(b)
    return out

def expected_source_boxes(src):
    ce=src["CE"];cb=src["CB"];cc=src["CC"];bo=src["BO"]
    def header(holder,day):
        return next(x for x in ce["original_headings"] if x["source"]==holder and x["day"]==day)
    def roi(o,key):
        return next(x for x in o if x["key"]==key)
    w_c=roi(bo["original_numeric_rois"],"P23_D17_C")
    w_n=roi(cb["new_original_rgb_rois"],"P23_LEFT_FOLIO_RIGHT_EDGE_NUMERAL")
    n_n=roi(cc["original_rois"],"NAJ_C17_NUMERAL_7570_TIGHT")
    assert ce["sources"]["WASEDA"]["source_sha256"]==cb["source"]["jpeg_sha256"]==bo["source"]["jpeg_sha256"]
    assert ce["sources"]["NAJ"]["source_sha256"]==cc["source"]["canvas17"]["original_jpeg_sha256"]
    assert cc["source"]["two_canvases_same_holding"] is True
    assert w_c["field"]=="CUMULATIVE" and w_c["day"]==17 and w_c["value"]=="8000.2697"
    assert w_n["decimal"]==n_n["decimal"]=="7570.6624"
    assert w_n["role"]=="OUTER_RIGHT_NUMERIC_LANE_OF_LEFT_FOLIO_NO_INDEPENDENT_SAME_DAY_FIELD_ASSIGNMENT"
    assert n_n["grade"]=="SINGLE_NATIVE_NUMERIC_LANE_ADJACENT_TO_D17_LAYOUT_NOT_GLOBAL_C_FIELD_WITNESS"
    return [
      ("W_D17_HEADING",header("WASEDA",17)["bbox"],header("WASEDA",17)["literal"]),
      ("W_D17_PRINTED_C8000",w_c["bbox"],w_c["literal"]),
      ("W_7570_OUTER_RIGHT_MARGIN",w_n["bbox"],w_n["literal"]),
      ("W_D16_HEADING_ACROSS_GUTTER",header("WASEDA",16)["bbox"],header("WASEDA",16)["literal"]),
      ("NAJ_D17_HEADING",header("NAJ",17)["bbox"],header("NAJ",17)["literal"]),
      ("NAJ_7570_ADJACENT",n_n["bbox"],n_n["reading"]),
    ]

def check(e,src,state,ledger):
    assert e["schema"]=="TIANWEN-13CF-SOURCE-NATIVE-D17-HEADING-NUMERIC-SIDEDNESS-FIREWALL-R1"
    assert e["issue_id"]=="TW-OPEN-0005"
    assert e["grade"]=="DERIVED_SHA_BOUND_NATIVE_RGB_BOX_GEOMETRY_NO_NEW_ORIGINAL_PIXEL"
    assert set(src)==set(SOURCES)
    bound=expected_source_boxes(src)
    rows=e["bounded_positions"]
    assert len(rows)==6
    assert [(x["key"],x["bbox"],x["literal"]) for x in rows]==bound
    assert [x["leaf"] for x in rows]==["LEFT","LEFT","LEFT","RIGHT","LEFT","LEFT"]
    assert all(x["holder"] in ("WASEDA","NAJ") for x in rows)
    p={x["key"]:x for x in rows}
    s=e["source_original_identity"]
    assert s["WASEDA"]["original_image_sha256"]==src["CE"]["sources"]["WASEDA"]["source_sha256"]
    assert s["NAJ"]["original_image_sha256"]==src["CE"]["sources"]["NAJ"]["source_sha256"]
    assert s["WASEDA"]["gutter_x_approx"]==src["CE"]["sources"]["WASEDA"]["photo_gutter_x_approx"]==1300
    assert s["NAJ"]["gutter_x_approx"]==src["CE"]["sources"]["NAJ"]["photo_gutter_x_approx"]==1500
    wh, wc, wn, w16 = (p[k] for k in ("W_D17_HEADING","W_D17_PRINTED_C8000","W_7570_OUTER_RIGHT_MARGIN","W_D16_HEADING_ACROSS_GUTTER"))
    nh,nn=(p[k] for k in ("NAJ_D17_HEADING","NAJ_7570_ADJACENT"))
    assert wc["bbox"][2] < wh["bbox"][0] < wh["bbox"][2] < wn["bbox"][0] < s["WASEDA"]["gutter_x_approx"] < w16["bbox"][0]
    assert nh["bbox"][2] < nn["bbox"][0] < s["NAJ"]["gutter_x_approx"]
    c=e["side_of_heading_controls"]
    assert [(x["holder"],x["heading"],x["numeric"],x["relationship"],x["horizontal_gap_px"]) for x in c]==[
       ("WASEDA","W_D17_HEADING","W_D17_PRINTED_C8000","NUMERIC_TO_LEFT",2),
       ("WASEDA","W_D17_HEADING","W_7570_OUTER_RIGHT_MARGIN","NUMERIC_TO_RIGHT",10),
       ("NAJ","NAJ_D17_HEADING","NAJ_7570_ADJACENT","NUMERIC_TO_RIGHT",30)]
    assert wh["bbox"][0]-wc["bbox"][2]==c[0]["horizontal_gap_px"]
    assert wn["bbox"][0]-wh["bbox"][2]==c[1]["horizontal_gap_px"]
    assert nn["bbox"][0]-nh["bbox"][2]==c[2]["horizontal_gap_px"]
    assert all(x["eligible_for_historical_mechanical_claim"] is False for x in c)
    assert all(e["folio_control"].values())
    assert e["interpretation_boundary"]=={
      "source_image_numeric_same_side_is_not_proof_of_field_identity":True,
      "left_vs_right_side_of_heading_is_source_specific_not_universal":True,
      "NAJ_D17_7570_same_day_yingsuoji":"UNBOUND",
      "WASEDA_D16_7570_same_day_yingsuoji":"UNBOUND",
      "cross_holding_exact_column_equivalence":"UNRESOLVED",
      "uniform_historical_day_shift":"UNPROVEN",
      "G893_Ming1569_shao_wei_units":"UNPROVEN",
      "transmission_lineage_winner":"UNRESOLVED",
      "original_D16_short_5_1362_vs_5_2362":"UNRESOLVED",
      "historical_early_archetype":"UNRESOLVED"}
    assert set(e["scope_firewall"].values())=={0,11,"CLOSED"}
    assert all(v==0 for k,v in e["scope_firewall"].items() if k.startswith("new_") or k=="algorithm_reopens")
    assert e["scope_firewall"]["open_research_issues"]==11
    assert e["scope_firewall"]["deterministic_product"]=="CLOSED"
    a=state["historical_audit"]
    assert state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
    assert state["invariants"]["algorithm_reopen_count"]==0
    assert a["row_count"]==a["audited_row_count"]==222
    assert a["external_source_registry_total_unique_count"]==a["external_source_registry_root_count"]+a["external_source_registry_extension_count"]
    assert any(x.startswith("13CF ") for x in a["current_focus"])
    assert ledger["binding"]["reviewed_state_version"]==state["schema_version"]
    assert ledger["binding"]["source_focus_count"]==len(a["current_focus"])
    q=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
    assert q["status"]=="OPEN"
    assert E in q["source_refs"]
    assert any(x.get("revision_id")=="TW-OPEN-0005-SIDEDNESS-13CF" for x in q["history"])
    assert any(x["id"]=="OMISSIONS-13CF-SIDEDNESS-20261021" for x in ledger["checkpoint_log"])
    assert len([x for x in ledger["issues"] if x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS")])==11
    return True

if __name__=="__main__":
    data=load(E)
    assert check(data,bind_sources(data),load(STATE),load(LEDGER))
    print("TIANWEN_13CF_SOURCE_SIDEDNESS=PASS")
