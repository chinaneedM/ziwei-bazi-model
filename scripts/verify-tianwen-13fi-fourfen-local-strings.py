#!/usr/bin/env python3
"""13FI source-native NIKH D4-D6 Fourfen string-step, not historic decimal units."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13FI-GORYEOSA-NIKH-D4D5D6-FOURFEN-PHOTO-STRING-STEPS-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def get(p):return json.loads((ROOT/p).read_text(encoding="utf8"))
def check(x,s,l):
 assert x["schema"]=="TIANWEN-13FI-GORYEOSA-NIKH-D4D5D6-FOURFEN-PHOTO-STRING-STEPS-R1" and x["issue_id"]=="TW-OPEN-0005"
 a=x["source_photo_literal_rows"]; r=x["literal_digit_replay"];o=x["opposing_NLC_day5_scope"];b=x["limitations"];i=x["impact"]
 assert [q["day"] for q in a]==[4,5,6] and [q["heading"] for q in a]==["四日","五日","六日"]
 assert [q["printed_heading"] for q in a]==["四分"]*3
 assert [q["direct_photo_glyphs"] for q in a]==["五〇一〇","五一七二","五三三四"]
 assert [q["source_index"] for q in a]==[2,2,3]
 assert [q["image_sha256"] for q in a]==["0b8e8a2a280d52068e79c8fdb04b1c7caae994205dd5502403c35672c51b21a7"]*2+["61eb6a9dab9bbde1c91ab7d372ed0007f72fc2fb1aac436265ff882982465961"]
 assert [q["crop_bbox_xyxy"] for q in a]==[[320,600,480,1600],[167,606,250,1450],[820,600,1026,1580]]
 assert [q["sha256_native_RGB_crop"] for q in a]==["2257f0e6bbec036bbf10ce6d81b21cdee250c2572eedb504be9c1dc6c2eba5ec","e3bcf659d342b6fe46349eb0dbb91433992d59b0cccb3befbb17d5c401a4c833","00de0362d3e6b48afbdcc491aed88b0d09dd7c9b9ba3900b3c0d7afe887fc12d"]
 assert a[0]["file_bytes"]==a[1]["file_bytes"]==261092 and a[2]["file_bytes"]==249769
 assert r["four_digit_values_for_STRING_ARITHMETIC_ONLY"]==[5010,5172,5334]
 assert r["D4_to_D5_step"]==r["D5_to_D6_step"]==162 and r["second_difference"]==0
 assert [r["four_digit_values_for_STRING_ARITHMETIC_ONLY"][i+1]-r["four_digit_values_for_STRING_ARITHMETIC_ONLY"][i] for i in (0,1)]==[162,162]
 assert r["intrinsic_equal_step_observed"] and r["establishes_historic_D5_numeric_value"] is False and r["unit_time_calendar_mapping"] is None
 assert o["prior_original_literal"]=="四分〇一七二" and o["conditional_digit_string_if_circle_is_zero"]==172
 assert (o["counterfactual_left_step"],o["counterfactual_right_step"],o["counterfactual_second_difference"])==(-4838,5162,10000)
 assert o["winner"]=="UNADJUDICATED" and o["NLC_original_glyph_revision_authorized"] is False
 assert b["source_photos_read_without_OCR"] and b["NIKH_D4_D5_D6_one_hosted_copy_group"] and b["old_13EI"]=="RETRACTED"
 assert b["original_fourfen_column_to_technical_mechanism_mapping"]=="UNPROVEN" and b["G893_six_controls"]=="OPEN"
 assert b["D4_D6_complete_source_numeric_tails_as_HISTORIC_MECHANICAL_RULE"] is b["winter_D16_source_numeric"] is b["summer_D30_source_numeric"] is None
 assert i["external_registry_total"]==761 and i["matrix_rows"]==i["matrix_audited"]==222
 assert i["risk_remaining_open_or_blocked"]==11 and i["product_status"]=="CLOSED"
 assert all(i[k]==0 for k in ("additional_source_original_glyph_decisions","source_registry_added","matrix_changed","genealogy_new_nodes","genealogy_new_edges","risk_closures","algorithm_reopen_count","candidate_collapse_count"))
 assert i["transmission_impact"]["new_supported_edges"]==[]
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(z.startswith("13FI ") for z in s["historical_audit"]["current_focus"])
 issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert {P,P.replace(".json",".md")}.issubset(set(issue["source_refs"]))
 assert issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert any(z.get("revision_id")=="TW-OPEN-0005-13FI-NIKH-D4D5D6-SAME-GALLERY-STRING-REPLAY-20261024" for z in issue["history"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"] and len(l["issues"])==11
 return True
if __name__=="__main__":
 assert check(get(P),get(S),get(L))
 print("13FI_PASS_SOURCE_NATIVE_FOURFEN_D4D5D6_TWO_EQUAL_STRING_STEPS_NO_HISTORICAL_WINNER")
