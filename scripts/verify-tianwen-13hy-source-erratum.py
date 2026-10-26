#!/usr/bin/env python3
"""13HY forward-only NIKH D18 terminal 三 erratum, source scoped D13-D17 crosscolumns."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13HY-NIKH-WINTER-D18-EDITORIAL-TRAILING-THREE-ERRATUM-AND-D13-D17-REPLAY-R1.json"
def check(e,with_state=True):
 assert e["schema"]=="TIANWEN-13HY-NIKH-WINTER-D18-FORWARD-ERRATUM-D13-D17-R1" and e["issue_id"]=="TW-OPEN-0005"
 assert e["correction_type"]=="FORWARD_ONLY_SOURCE_LITERAL_AND_NUMERIC_NORMALIZATION_ERRATUM"
 a=e["earlier_assertion"];raw=(ROOT/a["research_file"]).read_bytes()
 assert hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\0"+raw).hexdigest()==a["research_file_git_blob_sha"]=="6fe9b5ebe1855535e0c6e9b13e8fb7ef9a08c1e4"
 old=json.loads(raw)
 assert old["daily_rows"][-1]["cumulative_literal"]==a["d18_official_literal"]=="八千四百二十四六四〇八三"
 assert old["daily_rows"][-1]["cumulative_encoded"]==a["d18_wrongly_assigned_integer"]==84246408
 assert a["previous_D17_D18_cumulative_equality_claim"]=="RETRACTED_IN_13HY"
 v=e["modern_editorial_variant"]
 assert v["nikh_d18_C"]=="八千四百二十四六四〇八三" and v["wikisource_d18_C"]=="八千四百二十四六四〇八"
 assert v["grade"]=="TWO_MODERN_RECEIVED_TEXT_LAYERS_NOT_TWO_ORIGINAL_PHYSICAL_WITNESSES"
 assert v["d18_original_glyph"] is None and v["terminal_three_adjudication"]=="OPEN_PENDING_DIRECT_ORIGINAL_PAGE"
 z=e["source"];assert z["item_id"]=="kr_052_0010_0010_0020_0010"
 assert z["registered_source_id"]=="EXT-KRDB-GORYEOSA-V52-SHOUSHI-LICHENG" and z["scope"]=="D13_D18_WINTER_TABLE_OFFICIAL_MODERN_EDITED_TEXT_NOT_PHYSICAL_ORIGINAL"
 w=e["clean_window"];d=w["days"];t=w["transitions"]
 assert w["start"]==13 and w["end"]==17 and len(d)==5 and len(t)==4
 assert [x["day"] for x in d]==[13,14,15,16,17]
 assert [x["A_literal"] for x in d]==["五分一八〇四","五分一九九〇","五分二一七六","五分一三六二","五分二五四八"]
 assert [x["A"] for x in d]==[51804,51990,52176,51362,52548]
 assert [x["B_literal"] for x in d]==["四百四十五二〇四三","四百四十〇〇二三九","四百三十四八二四九","四百二十九六〇七三","四百二十四三七一一"]
 assert [x["B"] for x in d]==[4452043,4400239,4348249,4296073,4243711]
 assert [x["C_literal"] for x in d]==["六千二百五十〇六〇九三","六千六百九十五八一三六","七千一百三十五八三七五","七千五百七十〇六六二四","八千〇〇〇二六九七"]
 assert [x["C"] for x in d]==[62506093,66958136,71358375,75706624,80002697]
 for n,x in enumerate(d[:-1]):
  y=d[n+1];q=t[n]
  assert q["from"]==x["day"] and q["to"]==y["day"]
  assert q["observed_A"]==x["A"] and q["derived_A"]==x["B"]-y["B"]
  assert q["A_residual"]==x["A"]-q["derived_A"]
  assert q["observed_B"]==x["B"] and q["derived_B"]==y["C"]-x["C"]
  assert q["B_residual"]==x["B"]-q["derived_B"]==0
 assert [x["A_residual"] for x in t]==w["observed_A_residuals"]==[0,0,0,-1000]
 assert [x["B_residual"] for x in t]==w["observed_B_residuals"]==[0,0,0,0]
 assert w["day16_original_photos_literal"]=="五分一三六二" and w["day16_calculation_only"]=="五分二三六二"
 assert w["B_C_columns_original_photos_reviewed_this_batch"] is False
 prior=json.loads((ROOT/e["prior_photographs"]["evidence"]).read_text(encoding="utf8"))
 assert [x["source"] for x in prior["holdings"]]==e["prior_photographs"]["sources"]==["NAJ","WASEDA","NDL1909"]
 assert all(x["rows"][1]["literal"]=="五分一三六二" for x in prior["holdings"])
 assert e["prior_photographs"]["shared_printing_block_or_ancestor_proven"] is False
 f=e["firewall"]
 assert all(f[k] is True for k in ["legacy_13HX_file_immutable","legacy_13HX_unsupported_C18_inference_retracted","no_new_registered_sources","no_new_physical_witnesses","no_new_graph_nodes","no_new_graph_edges","no_chart_algorithm_reopen","no_candidate_collapse"])
 assert f["G893_six"]==f["D5_zero_five"]=="OPEN" and f["NCL03130_summer_D14"] is None and f["legacy_13EI"]=="RETRACTED" and f["ancient_unit_identity"] is None
 assert e["counts"]=={"matrix":[222,222],"sources":761,"graph":[252,238],"risks":11,"product":"CLOSED"} and e["transmission_impact"]=="NONE"
 if with_state:
  s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
  l=json.loads((ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf8"))
  assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
  assert tuple(map(int,s["schema_version"].split("."))) >= (1,878,0)
  assert any(x.startswith("13HY ") for x in s["historical_audit"]["current_focus"])
  assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ")[0]
  assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
  i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  assert (i["next_action"].startswith("13HY CURRENT ACTION:") or "ARCHIVED 13HY PRIOR ACTION:" in i["next_action"]) and "ARCHIVED 13HX PRIOR ACTION:" in i["next_action"]
  assert any(z.get("revision_id","").startswith("TW-OPEN-0005-13HY-") for z in i["history"])
  assert str(E.relative_to(ROOT)) in i["source_refs"] and l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
if __name__=="__main__":
 assert check(json.loads(E.read_text(encoding="utf8")))
 print("TIANWEN_13HY_D18_ORIGINAL_UNRESOLVED_CLEAN_D13_D17_PASS")
