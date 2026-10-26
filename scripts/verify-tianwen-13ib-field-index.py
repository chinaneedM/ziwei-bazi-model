#!/usr/bin/env python3
"""13IB: frozen photo-vs-edit text local B/C shift firewall."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13IB-WINTER-CUMULATIVE-VS-ADDITION-FIELD-INDEX-CONTROL-R1.json"
def read(p):return json.loads((R/p).read_text(encoding="utf8"))
def check(e,with_state=True):
 assert e["schema"]=="TIANWEN-13IB-WINTER-B-C-FIELD-SPECIFIC-INDEX-CONTROL-R1" and e["issue_id"]=="TW-OPEN-0005"
 docs=[]
 for x in e["frozen"]:
  b=(R/x["path"]).read_bytes()
  assert hashlib.sha1(b"blob "+str(len(b)).encode()+bytes([0])+b).hexdigest()==x["sha"]
  docs.append(json.loads(b))
 bj,hz,ia=docs
 assert ia["correction"]=="NAJ_AND_WASEDA_ORIGINAL_PRINTED_D18_D19_SAME_C_VALUES_NOT_CROSS_HOLDING_D17_D18_SHIFT"
 roi={z["id"]:z for z in bj["source_native_rgb_regions"]}
 p=e["printed"];m=e["edited"];f=e["finding"];s=e["strict"]
 for day in (18,19,20):
  z=p["D"+str(day)]
  assert roi[f"D{day}_HEADING"]["original_literal"]==z["heading"]
  assert roi[f"D{day}_CUMULATIVE"]["original_literal"]==z["C_original"]
  assert int(roi[f"D{day}_CUMULATIVE"]["decimal_value"].replace(".",""))==z["C"]
 assert roi["D18_LONG"]["original_literal"]==p["D18"]["B_original"]
 assert int(roi["D18_LONG"]["decimal_value"].replace(".",""))==p["D18"]["B"]
 for day in (17,18):
  y=m["D"+str(day)];q=hz["D"+str(day)]
  assert (y["B_original"],y["B"],y["C_original"])==(q["B"],q["B_int"],q["C"])
 assert m["D17"]["C"]==hz["D17"]["C_int"]==p["D18"]["C"]==80002697
 assert m["D18"]["B"]==hz["D18"]["B_int"]==p["D18"]["B"]==4191163
 assert m["D17"]["B"]==4243711!=p["D18"]["B"]
 assert m["D18"]["C"] is None and m["D18"]["raw_digits"]==hz["D18"]["C_digit_stream"]=="842464083"
 assert f["B_print_D18_maps_edited_day"]==18 and f["C_print_D18_maps_edited_day"]==17
 assert f["uniform_cross_field_day_shift"]=="FALSIFIED_IN_SCOPED_ROW_ONLY"
 assert p["D19"]["C"]-p["D18"]["C"]==f["original_C_delta_D18_D19"]==m["D17"]["B"]==4243711
 assert p["D20"]["C"]-p["D19"]["C"]==f["original_C_delta_D19_D20"]==p["D18"]["B"]==4191163
 assert f["whole_table_index_rule"]=="UNPROVEN" and f["ancient_unit_identity"]=="UNRESOLVED"
 assert s["modern_d18_terminal_three_must_stay"] and s["original_d16_literal"]=="五分一三六二" and s["computed_only_d16"]=="五分二三六二"
 assert s["G893_six"]==s["D5_zero_five"]=="OPEN" and s["NCL03130_summer_d14"] is None
 for name in ("new_physical_pages","new_glyphs","new_source_registry","new_graph_nodes","new_graph_edges","algorithm_reopen","candidate_collapse"):
  assert s[name]==0
 assert e["transmission_impact"]=="NONE" and e["counts"]=={"matrix":[222,222],"sources":761,"graph":[252,238],"open_issues":11,"product":"CLOSED"}
 if with_state:
  st=read("docs/PROJECT-CURRENT-STATE-R1.json");ld=read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
  assert st["schema_version"]==ld["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,st["schema_version"].split("."))) >= (1,881,0)
  assert any(x.startswith("13IB ") for x in st["historical_audit"]["current_focus"]) and ld["binding"]["latest_research_focus_prefix"]==st["historical_audit"]["current_focus"][-1].split(" ")[0]
  assert ld["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
  i=next(x for x in ld["issues"] if x["id"]=="TW-OPEN-0005")
  assert i["priority"]=="P0" and i["status"]=="OPEN"
  assert (i["next_action"].startswith("13IB CURRENT ACTION:") or "ARCHIVED 13IB PRIOR ACTION:" in i["next_action"]) and "ARCHIVED 13IA PRIOR ACTION:" in i["next_action"]
  assert any(x.get("revision_id","").startswith("TW-OPEN-0005-13IB-") for x in i["history"])
  assert "docs/research/TIANWEN-13IB-WINTER-CUMULATIVE-VS-ADDITION-FIELD-INDEX-CONTROL-R1.json" in i["source_refs"] and ld["checkpoint_log"][-1]["state_version"]==st["schema_version"]
 return True
if __name__=="__main__":
 assert check(read("docs/research/TIANWEN-13IB-WINTER-CUMULATIVE-VS-ADDITION-FIELD-INDEX-CONTROL-R1.json"))
 print("ARCHIVED_13IB_DAY_ATTRIBUTION_SUPERSEDED_BY_SOURCE_ORIGINAL_13ID")
 print("TIANWEN_13IB_FIELD_SPECIFIC_DAY_SHIFT_GATE_PASS")
