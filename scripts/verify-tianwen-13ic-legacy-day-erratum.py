#!/usr/bin/env python3
"""13IC: forward-only day/field attribution erratum; old archive retained."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=R/"docs/research/TIANWEN-13IC-WASEDA-13BO-13CD-13CF-DAY-LABEL-DESCENDANT-ERRATUM-R1.json"
def read(p):return json.loads((R/p).read_text(encoding="utf8"))
def overlap(a,b):return max(0,min(a[2],b[2])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[1],b[1]))
def area(a):return (a[2]-a[0])*(a[3]-a[1])
def check(e,with_state=True):
 assert e["schema"]=="TIANWEN-13IC-WASEDA-LEGACY-DAY-ATTRIBUTION-DESCENDANT-FORWARD-ERRATUM-R1" and e["issue_id"]=="TW-OPEN-0005"
 s={}
 for x in e["frozen_dependencies"]:
  b=(R/x["path"]).read_bytes()
  assert hashlib.sha1(b"blob "+str(len(b)).encode()+bytes([0])+b).hexdigest()==x["sha"]
  s[x["key"]]=json.loads(b)
 bo,bj,cd,cf,ia,ib=[s[x] for x in ("13BO","13BJ","13CD","13CF","13IA","13IB")]
 assert bo["source"]["jpeg_sha256"]==bj["source"]["original_jpeg_sha256"]==e["original_shared_waseda_image"]
 assert ia["correction"]=="NAJ_AND_WASEDA_ORIGINAL_PRINTED_D18_D19_SAME_C_VALUES_NOT_CROSS_HOLDING_D17_D18_SHIFT"
 older={x["key"]:x for x in bo["original_numeric_rois"]}
 newer={x["id"]:x for x in bj["source_native_rgb_regions"]}
 for i,(a,b,od,nd) in enumerate((("P23_D17_C","D18_CUMULATIVE",17,18),("P23_D18_C","D19_CUMULATIVE",18,19))):
  x=e["corrections"][i];old=older[a];new=newer[b]
  assert (x["legacy"],x["rebind"],x["old_day"],x["new_day"])==(a,b,od,nd)
  assert old["day"]==od and new["layout_day"]==nd
  assert old["literal"]==new["original_literal"]==x["literal"]
  assert old["value"]==new["decimal_value"]==x["decimal"]
  assert old["bbox"]==x["old_bbox"] and new["original_rgb_roi_bbox"]==x["new_bbox"]
  assert x["overlap_pixels"]==overlap(x["old_bbox"],x["new_bbox"])>0
  assert x["old_area_pixels"]==area(x["old_bbox"])
  assert newer["D"+str(nd)+"_HEADING"]["original_literal"]==("十八日" if nd==18 else "十九日")
 assert cd["positive_literal_position_matches"][1]["observed_naj_minus_waseda_heading_offset"]==1
 assert cd["positive_literal_position_matches"][1]["waseda_printed_day"]==17
 assert cf["bounded_positions"][1]["key"]=="W_D17_PRINTED_C8000" and cf["bounded_positions"][1]["literal"]==e["corrections"][0]["literal"]
 assert cf["bounded_positions"][1]["bbox"]==e["corrections"][0]["old_bbox"]
 assert e["prior_claims_retracted"]["13BO"]=="PRINTED_D17_C8000_AND_D18_C8424_DAY_LABELS_ONLY"
 assert e["prior_claims_retracted"]["13CD"]=="CROSS_HOLDING_WASEDA_D17_C8000_NAJ_D18_C8000_OFFSET_PLUS_ONE"
 assert e["prior_claims_retracted"]["13CF"]=="W_D17_PRINTED_C8000_SAME_DAY_CUMULATIVE_IDENTITY_ONLY"
 assert e["new_cross_holding_local_d17_long_offset"]==e["new_cross_holding_local_d18_c_offset"]==0
 assert e["uniform_all_fields_global_rule"]=="UNPROVEN"
 t=e["separate_cross_layer_orig_modern"]
 assert t["WASEDA_ORIG_D18_B_equals_NIKH_MODERN_D18_B"] and t["WASEDA_ORIG_D18_C_equals_NIKH_MODERN_D17_C"]
 assert t["uniform_both_column_day_offset"]==ib["finding"]["uniform_cross_field_day_shift"]=="FALSIFIED_IN_SCOPED_ROW_ONLY"
 f=e["strict"];assert f["no_source_document_overwrite"]
 assert f["NIKH_modern_D18_raw"]=="八千四百二十四六四〇八三"
 assert f["D16_original"]=="五分一三六二" and f["D16_math_only"]=="五分二三六二"
 assert f["G893_six"]==f["D5_zero_five"]=="OPEN" and f["NCL03130_summer_D14"] is None
 assert all(f[k]==0 for k in ("new_photos","new_glyphs","new_sources","new_graph_nodes","new_graph_edges","algorithm_reopens","candidates_collapsed"))
 assert e["transmission_impact"]=="NONE" and e["counts"]=={"matrix":[222,222],"registry":761,"graph":[252,238],"open_issues":11,"product":"CLOSED"}
 if with_state:
  s=read("docs/PROJECT-CURRENT-STATE-R1.json");ld=read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
  assert s["schema_version"]==ld["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,s["schema_version"].split(".")))>=(1,882,0)
  assert any(x.startswith("13IC ") for x in s["historical_audit"]["current_focus"]) and ld["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split()[0]
  assert ld["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
  q=next(x for x in ld["issues"] if x["id"]=="TW-OPEN-0005")
  assert all(any(h.get("revision_id", "").startswith("TW-OPEN-0005-" + t + "-") and "next_action" in h.get("changed_fields", []) for h in q["history"]) for t in ['13IC','13IB'])
  assert any(x.get("revision_id","").startswith("TW-OPEN-0005-13IC-") for x in q["history"])
  assert "docs/research/TIANWEN-13IC-WASEDA-13BO-13CD-13CF-DAY-LABEL-DESCENDANT-ERRATUM-R1.json" in q["source_refs"] and ld["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
if __name__=="__main__":
 assert check(read("docs/research/TIANWEN-13IC-WASEDA-13BO-13CD-13CF-DAY-LABEL-DESCENDANT-ERRATUM-R1.json"))
 print("ARCHIVED_13IC_DAY_ATTRIBUTION_SUPERSEDED_BY_SOURCE_ORIGINAL_13ID")
 print("TIANWEN_13IC_DESCENDANT_SOURCE_DAY_FORWARD_ERRATUM_PASS")
