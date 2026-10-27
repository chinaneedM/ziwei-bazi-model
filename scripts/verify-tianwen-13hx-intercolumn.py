#!/usr/bin/env python3
"""13HX historical source replay: D18 unsupported normalization is retracted in 13HY."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13HX-NIKH-GORYEOSA-WINTER-D14-D18-INTERCOLUMN-RECURRENCE-R1.json"
def check(e,with_state=True):
 assert e["schema"]=="TIANWEN-13HX-NIKH-GORYEOSA-WINTER-D14-D18-INTERCOLUMN-RECURRENCE-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["transmission_impact"]=="NONE"
 z=e["source"];assert z["item_id"]=="kr_052_0010_0010_0020_0010"
 assert z["existing_source_id"]=="EXT-KRDB-GORYEOSA-V52-SHOUSHI-LICHENG"
 assert z["grade"]=="MODERN_INSTITUTIONAL_EDITORIAL_TRANSCRIPTION_NOT_NEW_PHYSICAL_WITNESS"
 assert z["columns"]==["積日","日差加一秒八十六少","盈縮加分","盈縮積","行度"]
 d=e["daily_rows"]
 assert [x["day"] for x in d]==[14,15,16,17,18]
 assert [x["differential_literal"] for x in d]==["五分一九九〇","五分二一七六","五分一三六二","五分二五四八","五分二七三四"]
 assert [x["differential_encoded"] for x in d]==[51990,52176,51362,52548,52734]
 assert [x["additive_encoded"] for x in d]==[4400239,4348249,4296073,4243711,4191163]
 assert [x["cumulative_encoded"] for x in d]==[66958136,71358375,75706624,80002697,84246408]
 assert [x["additive_literal"] for x in d]==["四百四十〇〇二三九","四百三十四八二四九","四百二十九六〇七三","四百二十四三七一一","四百一十九一一六三"]
 assert [x["cumulative_literal"] for x in d]==["六千六百九十五八一三六","七千一百三十五八三七五","七千五百七十〇六六二四","八千〇〇〇二六九七","八千四百二十四六四〇八三"]
 t=e["transitions"];assert len(t)==4
 for n,x in enumerate(d[:-1]):
  z=t[n];y=d[n+1]
  assert z["from_day"]==x["day"] and z["to_day"]==y["day"]
  assert z["observed_differential"]==x["differential_encoded"]
  assert z["inferred_from_additive"]==x["additive_encoded"]-y["additive_encoded"]
  assert z["differential_residual"]==z["observed_differential"]-z["inferred_from_additive"]
  assert z["observed_additive"]==x["additive_encoded"]
  assert z["inferred_from_cumulative"]==y["cumulative_encoded"]-x["cumulative_encoded"]
  assert z["additive_residual"]==z["observed_additive"]-z["inferred_from_cumulative"]==0
 assert [x["differential_residual"] for x in t]==[0,0,-1000,0]
 a=e["result"];assert a["checked_differential_transitions"]==a["checked_accumulation_transitions"]==4
 assert a["nonzero_differential_residual_days"]==[16] and a["nonzero_accumulation_residual_days"]==[]
 assert a["day16_printed_literal"]==d[2]["differential_literal"]=="五分一三六二"
 assert a["day16_printed_integer"]==d[2]["differential_encoded"]==51362
 assert a["day16_crosscolumn_implied_integer"]==t[2]["inferred_from_additive"]==52362
 assert a["day16_crosscolumn_implied_literal"]=="五分二三六二" and a["day16_residual"]==-1000
 assert a["physical_day16_glyph_must_not_be_replaced"] and not a["all_0_to_88_rows_exhaustively_reviewed"]
 p=json.loads((ROOT/e["prior_original"]["source_evidence"]).read_text(encoding="utf8"))
 assert [x["source"] for x in p["holdings"]]==e["prior_original"]["holdings"]==["NAJ","WASEDA","NDL1909"]
 assert all(x["rows"][1]["literal"]=="五分一三六二" for x in p["holdings"])
 assert e["prior_original"]["direct_photo_d16"]=="五分一三六二"
 assert not e["prior_original"]["crosscolumn_values_direct_original_read_in_this_batch"]
 assert not e["prior_original"]["same_print_block_independence_proven"]
 f=e["firewall"]
 assert f["received_edited_columns_not_independent_original_witnesses"] and f["no_corrected_2362_physical_glyph_claim"]
 assert f["no_ancient_mechanical_unit_or_copy_stemma_determined"]
 assert f["G893_six"]==f["D5_zero_five"]=="OPEN" and f["legacy_13EI"]=="RETRACTED" and f["NCL03130_summer_D14_original"] is None
 assert all(f[k]==0 for k in ["added_registered_sources","added_independent_physical_witnesses","added_graph_nodes","added_graph_edges","algorithm_reopens","candidate_collapses"])
 assert e["counts"]=={"matrix":[222,222],"sources":761,"graph":[252,238],"omission_issues":11,"product":"CLOSED"}
 if with_state:
  s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
  l=json.loads((ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf8"))
  assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
  assert tuple(map(int,s["schema_version"].split("."))) >= (1,877,0)
  assert any(x.startswith("13HX ") for x in s["historical_audit"]["current_focus"])
  assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ")[0]
  assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
  issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  assert (issue["next_action"].startswith("13HX CURRENT ACTION:") or "ARCHIVED 13HX PRIOR ACTION:" in issue["next_action"]) and "ARCHIVED 13HW PRIOR ACTION:" in issue["next_action"]
  assert any(z.get("revision_id","").startswith("TW-OPEN-0005-13HX-") for z in issue["history"])
  assert str(E.relative_to(ROOT)) in issue["source_refs"] and l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
if __name__=="__main__":
 assert check(json.loads(E.read_text(encoding="utf8")))
 print("TIANWEN_13HX_NIKH_WINTER_INTERCOLUMN_LITERAL_PRESERVED_PASS")
