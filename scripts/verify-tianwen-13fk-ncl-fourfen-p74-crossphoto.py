#!/usr/bin/env python3
"""13FK NLC original page74 three bounded Fourfen glyph agrees + day9 withheld."""
import hashlib,json,argparse
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13FK-NCL-P74-D7D8D10-CROSS-PHOTO-FOURFEN-BOUNDED-COLLATION-R1.json"
F="docs/research/TIANWEN-13FJ-NIKH-JUAN52-FOURFEN-D4D10-SIX-REPEATED-STRING-STEPS-R1.json"
EN="docs/research/TIANWEN-13EN-NCL03130-P74-FOURFEN-D4-D6-BOUNDED-PREFIX-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(x):return json.loads((R/x).read_text(encoding="utf8"))
def check(e,f,en,s,l):
 assert e["schema"]=="TIANWEN-13FK-NCL-P74-D7D8D10-CROSS-PHOTO-FOURFEN-BOUNDED-COLLATION-R1" and e["issue_id"]=="TW-OPEN-0005"
 a=e["NLC_original"];ni=e["NIKH_comparator"];q=e["fresh_native_photo_ROIs"];c=e["comparison"];i=e["impact"]
 assert a["source_pdf"]=="NCL-03130_09_高麗史.pdf" and a["original_pdf_sha256"]==en["source"]["pdf_sha256"]
 assert a["original_page_number"]==en["source"]["pdf_page"]==74
 assert a["png_sha256"]==en["source"]["png_sha256"]=="a3f597f96f494a5ee9a6d582850f0642035d858bcbc587abc6fac11853018a14"
 assert a["native_RGB_sha256"]==en["source"]["rgb_sha256"]=="c0bf6332279b6ff77e155a5204710ca82d868454a039f8b6660109080b1c1160"
 assert a["native_image_dimensions"]==[1305,873] and a["archive_run_id"]==39938606876 and a["archive_artifact_id"]==12494518841
 assert a["book_physical_copy_identity"] is a["physical_print_or_repair_date"] is None and a["qing_vs_1905_layer"]=="UNBOUND"
 assert a["same_original_NCL_source_as_13EN"] and a["no_OCR_used"] and a["not_four_separate_ancient_books"]
 assert ni["publisher_gallery_original_glyphs_D7_D8_D9_D10"]==[z["glyphs"] for z in f["new_source_pixel_direct_collations"]]
 assert [r["day"] for r in q]==[7,8,9,10]
 assert [r["day_heading"] for r in q]==["七日","八日","九日","十日"]
 assert [r["read_original_fourfen"] for r in q]==["四分五四九六","四分五六五八",None,"四分五九八二"]
 assert [r["matches_NIKH_same_day_literal"] for r in q]==[True,True,None,True]
 assert q[2]["reason_for_null"]=="P74_SPINE_OR_PAGE_GUTTER_INTERSECTS_TARGET_COLUMN_AND_NEIGHBOR_LANES_AMBIGUOUS"
 assert [r["original_native_lane_bbox"] for r in q]==[[650,399,679,665],[561,399,591,665],[510,399,539,665],[431,399,460,665]]
 assert [r["original_lane_RGB_SHA256"] for r in q]==["49253b2f5b2f42819dda34a00ee1639b5e0562a4210b7d1c1e3e8d1c9516d560","45c9c2c81eec9c8aaded3e92fc25ff60715a28e06c7abf6e16a875bbbb6e228d","052b6391701f0b8b8ef1af0471ea88aab02640fabddc9cb9006b3217fa0b80dc","fa2cf4b6d6ed306ceb9e548d57c7021281469a021e84a97be08db05bc181809b"]
 assert [r["original_native_heading_bbox"] for r in q]==[[590,145,685,295],[505,145,600,295],[460,145,538,295],[360,145,465,295]]
 assert [r["original_heading_RGB_SHA256"] for r in q]==["e626905439b6cd178f62a7c51a52124b884f52bcdfad90119b1275936ffafc94","e836f897f203202fe7191fade4d9051257a19317375c95191e0896b4a4a63991","8760df61f1071b9e5b470a9997f1ed649ebd194eba2427b9f115629b5252ddca","89f0bd5a1898415eca7b49f432e9c922bfee5d90bac460449f61e65af4896756"]
 assert all(r["comparison_NIKH_day"+str(r["day"])]==("四分"+f["new_source_pixel_direct_collations"][r["day"]-7]["glyphs"]) for r in q)
 assert all(r["read_original_fourfen"]==r["comparison_NIKH_day"+str(r["day"])] for r in q if r["day"]!=9)
 assert all(0<=b[0]<b[2]<=1305 and 0<=b[1]<b[3]<=873 for r in q for b in [r["original_native_lane_bbox"],r["original_native_heading_bbox"]])
 assert e["immutable_NCL_13EN_days4_5_6"]["day5_exact_visible"]==en["findings"]["fourfen_d5_clear_prefix"]=="四分〇一七二"
 assert c["NLC_replayed_day7_day8_day10_matching_NIKH"]==3 and c["NLC_day9_gutter_limited_unknown"]
 assert c["NLC_day5_vs_NIKH_day5_opposed_source_photo_glyphs"]==["四分〇一七二","四分五一七二"] and c["historic_D5_numeric_winner"] is None
 assert c["same_ancient_physical_book_authenticated"] is False and c["independent_physical_print_states_verified"] is False and c["NLC_day5_print_typo_proven"] is False
 assert c["no_full_day4_to_day10_NLC_replay_claim"] and e["independent_unresolved"]["older_13EI_false_claim"]=="RETRACTED"
 assert e["independent_unresolved"]["G893_six_original_numeric_controls"]=="OPEN"
 assert i["new_BOUNDED_NLC_day_photo_positive_rows"]==3 and i["new_NLC_indeterminate_day_photo_positions"]==1
 assert i["external_source_registry_total"]==761 and i["matrix_audited"]==i["matrix_row_total"]==222 and i["genealogy_nodes"]==252 and i["genealogy_edges"]==238
 assert i["remaining_OPEN_or_BLOCKED_risks"]==11 and i["product"]=="CLOSED"
 assert all(i[x]==0 for x in ("new_ancient_physical_editions_authenticated","source_registry_delta","matrix_row_delta","genealogy_node_delta","genealogy_edge_delta","risk_closures","algorithm_reopens","chart_candidate_collapses"))
 assert e["transmission_impact"]["new_supported_edges"]==[]
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert any(z.startswith("13FK ") for z in s["historical_audit"]["current_focus"]) and l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0" and issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert all(any(h.get("revision_id", "").startswith("TW-OPEN-0005-" + t + "-") and "next_action" in h.get("changed_fields", []) for h in issue["history"]) for t in ['13FK'])
 assert {P,P.replace(".json",".md")}.issubset(set(issue["source_refs"]))
 assert any(t.get("revision_id")=="TW-OPEN-0005-13FK-NLC-P74-D7D8D10-THREE-POSITIVE-D9-UNKNOWN-20261024" for t in issue["history"])
 assert len(l["issues"])==11 and l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
def pixel_replay(e,p):
 from PIL import Image
 raw=Path(p).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==e["NLC_original"]["png_sha256"]
 with Image.open(p) as photo: im=photo.convert("RGB")
 assert list(im.size)==e["NLC_original"]["native_image_dimensions"]
 assert hashlib.sha256(im.tobytes()).hexdigest()==e["NLC_original"]["native_RGB_sha256"]
 for row in e["fresh_native_photo_ROIs"]:
  for box,key in (("original_native_lane_bbox","original_lane_RGB_SHA256"),("original_native_heading_bbox","original_heading_RGB_SHA256")):
   assert hashlib.sha256(im.crop(tuple(row[box])).tobytes()).hexdigest()==row[key]
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--original-png");args=ap.parse_args()
 a=load(P);assert check(a,load(F),load(EN),load(S),load(L))
 if args.original_png:assert pixel_replay(a,args.original_png)
 print("13FK_PASS_NLC_DAY7_DAY8_DAY10_MATCH_D9_UNDECIDED_SOURCE_ORIGINAL_PHOTO_NO_EDITION_WINNER")
