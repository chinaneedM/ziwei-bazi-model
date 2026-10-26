#!/usr/bin/env python3
"""13IA: forward-only source-physical day-label correction, with frozen Git blob proofs."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13IA-PHYSICAL-WASEDA-DAY-LABEL-FORWARD-ERRATUM-R1.json"
def load(p):return json.loads((R/p).read_text(encoding="utf8"))
def check(e,with_state=True):
 assert e["schema"]=="TIANWEN-13IA-WASEDA-ORIGINAL-PRINTED-DAY-LABEL-FORWARD-ERRATUM-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 docs=[]
 for x in e["frozen_sources"]:
  b=(R/x["path"]).read_bytes()
  h=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
  assert h==x["sha"],x["path"]
  docs.append(json.loads(b))
 bt,bj,hz=docs
 assert bt["comparison"]["local_field_label_difference"]==e["retracted_13BT_old_waseda_label"]=="NAJ_CUMULATIVE_PRINTED_D18_D19_MATCHES_WASEDA_CUMULATIVE_PRINTED_D17_D18"
 assert e["correction"]=="NAJ_AND_WASEDA_ORIGINAL_PRINTED_D18_D19_SAME_C_VALUES_NOT_CROSS_HOLDING_D17_D18_SHIFT"
 n,w=e["original_printed"]
 assert (n["holding"],w["holding"])==("NAJ","WASEDA")
 assert n["jpeg"]==bt["firstparty_source"]["jpeg_sha256"]
 assert w["jpeg"]==bj["source"]["original_jpeg_sha256"]
 assert [r["day"] for r in n["rows"]]==[18,19]
 assert [r["day"] for r in w["rows"]]==[18,19,20]
 for i,row in enumerate(n["rows"]):
  z=bt["paired_original_field_columns"][i]
  assert (row["day"],row["literal"],row["decimal"],row["rgb"])==(z["day"],z["cumulative_literal"],z["cumulative_value"],z["cumulative_sha256"])
 for row in w["rows"]:
  d=row["day"]; byid={x["id"]:x for x in bj["source_native_rgb_regions"]}
  num=byid[f"D{d}_CUMULATIVE"]; label=byid[f"D{d}_HEADING"]
  assert label["original_literal"]=={18:"十八日",19:"十九日",20:"二十日"}[d]
  assert (row["literal"],row["decimal"],row["rgb"])==(num["original_literal"],num["decimal_value"],num["original_rgb_pixel_sha256"])
 assert [x["decimal"] for x in n["rows"]]==["8000.2697","8424.6408"]
 assert [x["decimal"] for x in w["rows"]]==["8000.2697","8424.6408","8843.7571"]
 modern=e["official_modern"]
 assert [x["day"] for x in modern]==[17,18,19]
 assert [x["raw"] for x in modern]==[hz["D17"]["C"],hz["D18"]["C"],hz["D19"]["C"]]
 assert modern[0]["raw"]==n["rows"][0]["literal"] and modern[2]["raw"]==w["rows"][2]["literal"]
 assert e["original_printed_D19_has_no_trailing_three"] is True
 assert e["actual_original_printed_D18_C"]==n["rows"][0]["literal"]==w["rows"][0]["literal"]
 assert e["actual_original_printed_D19_C"]==n["rows"][1]["literal"]==w["rows"][1]["literal"]
 assert e["modern_D18_raw_C"]==modern[1]["raw"]=="八千四百二十四六四〇八三"
 assert e["modern_D18_arithmetical_eight_digit_counterfactual"]=="84246408"==str(hz["arithmetic"]["left_C18"])
 assert e["local_c_field_printed_day_minus_modern_edit_day"]==1
 assert e["whole_table_day_index_law"]=="UNPROVEN"
 assert e["ancient_D18_same_numbered_day_modern_C"]=="NOT_EQUIVALENT"
 assert e["cannot_count_two_holding_as_independent_printing_lineages"] is True
 for k in ["source_original_new_photos","new_glyphs","new_physical_holdings","added_registry_sources","added_graph_nodes","added_graph_edges","algorithms_reopened","candidates_collapsed"]:assert e[k]==0
 assert e["D16_attested"]=="五分一三六二" and e["D16_counterfactual_only"]=="五分二三六二"
 assert e["counts"]=={"matrix":[222,222],"sources":761,"graph":[252,238],"issues":11,"product":"CLOSED"}
 assert e["transmission_impact"]=="NONE"
 if with_state:
  s=load("docs/PROJECT-CURRENT-STATE-R1.json");l=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
  assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,s["schema_version"].split("."))) >= (1,880,0)
  assert any(x.startswith("13IA ") for x in s["historical_audit"]["current_focus"])
  assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ")[0]
  assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
  i=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
  assert i["priority"]=="P0" and i["status"]=="OPEN"
  assert (i["next_action"].startswith("13IA CURRENT ACTION:") or "ARCHIVED 13IA PRIOR ACTION:" in i["next_action"]) and "ARCHIVED 13HZ PRIOR ACTION:" in i["next_action"]
  assert any(x.get("revision_id","").startswith("TW-OPEN-0005-13IA-") for x in i["history"])
  assert str(E.relative_to(R)) in i["source_refs"] and l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
if __name__=="__main__":
 assert check(load(str(E.relative_to(R))))
 print("TIANWEN_13IA_WASEDA_PRINTED_DAY_FORWARD_ERRATUM_PASS")
