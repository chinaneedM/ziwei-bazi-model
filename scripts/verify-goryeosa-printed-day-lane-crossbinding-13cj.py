#!/usr/bin/env python3
"""13CJ: immutable source-day heading-to-long/short column cross-batch geometry."""
import hashlib
import json
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CJ-GORYEOSA-D16-D18-HEADING-TO-LONG-SHORT-LANES-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
P={
"13CI":"docs/research/TIANWEN-13CI-GORYEOSA-D16-D18-TWO-ORIGINAL-LONG-SHORT-ASYMMETRY-R1.json",
"13CH":"docs/research/TIANWEN-13CH-GORYEOSA-TWO-HOLDING-D01-D20-ORIGINAL-HEADING-ATLAS-R1.json",
"13BS":"docs/research/TIANWEN-13BS-GORYEOSA-WASEDA-D16-NAJ-D18-D19-SOURCE-NATIVE-GLYPH-COLLATION-R1.json",
"13BO":"docs/research/TIANWEN-13BO-GORYEOSA-WASEDA-P23-D17-D18-ORIGINAL-HEADER-CUMULATIVE-LONG-R1.json"
}
MAPPING={"NAJ17":"N17","NAJ18":"N18","W23":"W23"}
DAYS={16:"十六日",17:"十七日",18:"十八日"}
OLD=[("W23",16,"LONG","13BS","W_D16_LONG"),("W23",16,"SHORT","13BS","W_D16_SHORT"),("W23",17,"LONG","13BO","P23_D17_LONG"),("W23",18,"LONG","13BO","P23_D18_LONG")]
def load(p):
 return json.loads((ROOT/p).read_text(encoding="utf-8"))
def frozen(e):
 assert set(e["frozen_prior_sources"])==set(P)
 out={}
 for k,p in P.items():
  row=e["frozen_prior_sources"][k]
  assert row["path"]==p
  raw=(ROOT/p).read_bytes()
  gitblob=b"blob "+str(len(raw)).encode()+b"\0"+raw
  assert hashlib.sha1(gitblob).hexdigest()==row["git_blob_sha"],k
  out[k]=json.loads(raw)
 return out
def check(e,s,l,prior=None):
 assert e["schema"]=="TIANWEN-13CJ-SOURCE-PRINTED-DAY-TO-LONG-SHORT-COLUMN-GEOMETRY-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["evidence_grade"].startswith("DERIVED_ONLY_")
 old=prior if prior is not None else frozen(e)
 assert set(old)==set(P)
 base,atlas,bs,bo=(old[k] for k in ("13CI","13CH","13BS","13BO"))
 assert e["two_existing_historical_holdings"]==["NAJ-282-0006-PHYSICAL51","WASEDA-RI06-02809-BOOK33"]
 arr=e["atlas_to_numerical_original_bindings"]
 assert len(arr)==len(base["rois"])==10
 gaps=[]
 for out,r in zip(arr,base["rois"]):
  key=MAPPING[r["source"]]
  photo=atlas["photos"][key]
  head=next(x for x in photo["day_header_rois"] if x["day"]==r["printed_day"])
  assert r["printed_day"] in DAYS and head["literal"]==DAYS[r["printed_day"]]
  assert photo["original_jpeg_sha256"]==base["sources"][r["source"]]["image_sha256"]
  assert photo["source_dimensions"]==base["sources"][r["source"]]["dimensions"]
  assert out["source"]==r["source"] and out["atlas_photo"]==key
  assert out["printed_day"]==r["printed_day"] and out["technical_lane"]==r["field"]
  assert out["day_heading_original"]==head["literal"]
  assert out["day_heading_bbox"]==head["bbox"] and out["day_heading_rgb_sha256"]==head["rgb_sha256"]
  assert out["day_heading_leaf"]==head["leaf"] and out["source_jpeg_sha256"]==photo["original_jpeg_sha256"]
  assert out["numeric_bbox"]==r["bbox"] and out["numeric_rgb_sha256"]==r["rgb_sha256"]
  assert out["numeric_original"]==r["original"] and out["numeric_decimal"]==r["decimal"]
  hl,ht,hr,hb=head["bbox"];nl,nt,nr,nb=r["bbox"]
  assert hl<=nl<nr<=hr and nt>=hb and 0<nt-hb<=50
  assert out["heading_to_numeric_y_gap_pixels"]==nt-hb
  assert out["full_numeric_x_inside_printed_heading_x"] is True
  gaps.append(nt-hb)
 assert sorted(set(gaps))==[10,15,50]
 assert [(x["source"],x["printed_day"],x["technical_lane"]) for x in arr]==[(x["source"],x["printed_day"],x["field"]) for x in base["rois"]]
 assert [(r["source"],r["day"],r["field"],r["batch"],r["key"]) for r in e["prior_exact_roi_reuse_targets"]]==OLD
 for src,day,field,batch,key in OLD:
  now=next(x for x in base["rois"] if (x["source"],x["printed_day"],x["field"])==(src,day,field))
  prev=next(x for x in (bs["original_rgb_rois"] if batch=="13BS" else bo["original_numeric_rois"]) if x["key"]==key)
  assert prev["bbox"]==now["bbox"]
  assert (prev.get("rgb_sha256") or prev.get("pixel_sha256"))==now["rgb_sha256"]
  assert (prev.get("numeric") or prev.get("value"))==now["decimal"]
  assert prev["literal"]==now["original"]
 a=e["arithmetic_boundary"]
 assert Decimal(a["D16_long_minus_D17_long"])==Decimal("5.2362")
 assert Decimal(a["source_printed_D16_short_in_both"])==Decimal("5.1362")
 assert Decimal(a["discrepancy"])==Decimal("0.1000")
 assert Decimal(a["D17_long_minus_D18_long"])==Decimal(a["D17_short_in_both"])==Decimal("5.2548")
 assert a["source_printed_short16_must_not_be_corrected_by_arithmetic"] is True
 z=e["geometry_conclusion"]
 assert z["exact_day_header_to_numeric_lane_pairs"]==10
 assert z["source_original_holdings"]==2 and z["source_original_jpegs"]==3
 assert z["all_x_numeric_rois_wholly_within_same_printed_day_heading_roi"] is True
 assert (z["observed_min_heading_bottom_to_numeral_top_pixels"],z["observed_max_heading_bottom_to_numeral_top_pixels"])==(min(gaps),max(gaps))
 assert z["proves_only"]=="SOURCE_LOCAL_PRINTED_DAY_COLUMN_GEOMETRY_FOR_ISOLATED_LONG_SHORT_FIELDS"
 assert set(z["does_not_prove"])=={"SAME_DAY_YINGSUOJI_C_FIELD","WHOLE_TABLE_GLOBAL_RECURRENCE","G893_MING1569_UNIT_IDENTITY","D16_HISTORICAL_CORRECTION","INDEPENDENT_COPY_GENEALOGY"}
 assert e["source_boundaries"]["W_D16_same_day_yingsuoji"]==e["source_boundaries"]["NAJ_D17_same_day_yingsuoji"]=="UNBOUND"
 assert e["source_boundaries"]["G893_Ming1569_unit_equivalence"]=="UNPROVEN"
 scope=e["new_evidence_scope"]
 for k in ("new_provider_jpeg_objects","new_original_pixel_crops","new_independent_physical_witnesses","new_source_registry_entries","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","new_stemmatic_votes","algorithm_reopens"):
  assert scope[k]==0
 assert scope["open_research_issues"]==11 and scope["product"]=="CLOSED"
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
 audit=s["historical_audit"]
 assert audit["row_count"]==audit["audited_row_count"]==222 and audit["external_source_registry_total_unique_count"]==audit["external_source_registry_root_count"]+audit["external_source_registry_extension_count"]
 assert any(x.startswith("13CJ ") for x in audit["current_focus"])
 assert l["binding"]["reviewed_state_version"]==s["schema_version"]
 assert l["binding"]["source_focus_count"]==len(audit["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-SOURCEDAY-LANES-13CJ" for x in issue["history"])
 assert any(x["id"]=="OMISSIONS-13CJ-HEADED-LANES-20261022" for x in l["checkpoint_log"])
 assert len([x for x in l["issues"] if x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS")])==11
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L))
 print("TIANWEN_13CJ_CROSS_BATCH_PRINTED_DAY_LANES=PASS")
