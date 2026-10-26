#!/usr/bin/env python3
"""13HW source-scoped received-text full endpoint arithmetic; never edit printed D16."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13HW-NIKH-GORYEOSA-WINTER-87-DAY-ENDPOINT-ARITHMETIC-R1.json"
def check(e,with_state=True):
 assert e["schema"]=="TIANWEN-13HW-NIKH-GORYEOSA-WINTER-87-DAY-ENDPOINT-ARITHMETIC-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 z=e["transcription_source"]
 assert z["item_id"]=="kr_052_0010_0010_0020_0010"
 assert z["grade"]=="MODERN_INSTITUTIONAL_EDITORIAL_TRANSCRIPTION_NOT_NEW_PHYSICAL_WITNESS"
 assert z["existing_source_id"]=="EXT-KRDB-GORYEOSA-V52-SHOUSHI-LICHENG"
 assert z["printed_title"]=="大陽冬至前後二象盈初縮末限"
 assert z["heading"]=="日差加一秒八十六少"
 rows=e["anchor_rows"]
 assert [x["day_index"] for x in rows]==[0,15,16,17,87,88]
 assert [x["literal"] for x in rows]==["四分九三八六","五分二一七六","五分一三六二","五分二五四八","六分五五六八","六分五七五四"]
 assert [x["encoded"] for x in rows]==[49386,52176,51362,52548,65568,65754]
 k=e["encoding_policy"];a=e["arithmetic"]
 assert k["initial_integer"]==rows[0]["encoded"] and k["terminal_integer"]==rows[4]["encoded"]
 assert k["numerical_scale_is_not_an_independent_ancient_unit"] is True
 assert k["do_not_identify_shaowith_wei"] is True
 assert a["increment_count"]==87 and a["observed_total_difference"]==65568-49386==16182
 assert a["slope_from_endpoints"]==a["observed_total_difference"]//a["increment_count"]==186
 assert a["observed_total_difference"]%a["increment_count"]==0
 for r in rows:
  pred=49386+186*r["day_index"]
  assert r["model_expected"]==pred and r["residual"]==r["encoded"]-pred
 assert [r["residual"] for r in rows]==[0,0,-1000,0,0,0]
 assert a["day88_out_of_sample_check"]==65754
 assert a["day16_counterfactual_integer"]==52362
 assert a["day16_counterfactual_literal"]=="五分二三六二"
 assert a["day16_printed_integer"]==51362 and a["day16_printed_literal"]=="五分一三六二"
 assert a["day16_residual"]==-1000 and a["nonzero_residual_at_checked_anchors"]==[16]
 assert a["strict_original_glyph_replacement_forbidden"] is True
 assert a["full_0_to_88_table_exhaustively_verified"] is False
 for p in e["method_parallels"]:
  assert "ORIGINAL_PHOTO_NOT_REVIEWED" in p["source_kind"]
  assert "TRANSCRIPTION" in p["source_status"]
 assert e["crosswork_title_control"]["edited_title"]=="太陽冬至前後二象盈初縮末限"
 assert e["crosswork_title_control"]["goryeosa_title"]=="大陽冬至前後二象盈初縮末限"
 prior=json.loads((ROOT/e["direct_prior_evidence"]["photo_record"]).read_text(encoding="utf8"))
 assert [x["source"] for x in prior["holdings"]]==e["direct_prior_evidence"]["photographed_sources"]
 assert all(x["rows"][1]["literal"]=="五分一三六二" for x in prior["holdings"])
 assert prior["arithmetic"]["candidate_attested_in_reviewed_images"] is False
 f=e["firewall"]
 assert f["received_editorial_text_not_physical_witness"] and f["d16_two_not_attested_in_three_photos"] and f["mei_not_direct_yuan_print"]
 assert f["unit_shao_vs_wei_identity"] is f["early_original_numerical_winner"] is f["taiwan_NCL03130_summer_D14_original"] is f["taiwan_NCL03130_old_supplement_layer"] is None
 assert f["G893_six"]==f["D5_zero_five"]=="OPEN" and f["legacy_13EI"]=="RETRACTED"
 assert all(f[x]==0 for x in ("added_registered_sources","added_independent_physical_witnesses","added_graph_nodes","added_graph_edges","algorithm_reopens","candidate_collapses"))
 assert e["counts"]=={"matrix":[222,222],"external_sources":761,"genealogy":[252,238],"risk_issues":11,"product":"CLOSED"}
 assert e["transmission_impact"]=="NONE"
 if with_state:
  s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
  l=json.loads((ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf8"))
  assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]=="1.876.0"
  assert s["historical_audit"]["current_focus"][-1].startswith("13HW ") and l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
  assert l["binding"]["latest_research_focus_prefix"]=="13HW"
  issue=next(v for v in l["issues"] if v["id"]=="TW-OPEN-0005")
  assert issue["priority"]=="P0" and issue["status"]=="OPEN"
  assert issue["next_action"].startswith("13HW CURRENT ACTION:")
  assert "ARCHIVED 13HV PRIOR ACTION:" in issue["next_action"]
  assert issue["history"][-1]["revision_id"].startswith("TW-OPEN-0005-13HW-")
  assert str(E.relative_to(ROOT)) in issue["source_refs"]
  assert l["checkpoint_log"][-1]["state_version"]=="1.876.0"
 return True
if __name__=="__main__":
 e=json.loads(E.read_text(encoding="utf8"));assert check(e)
 print("TIANWEN_13HW_NIKH_WINTER_ENDPOINT_LITERAL_VS_FORMULA_PASS")
