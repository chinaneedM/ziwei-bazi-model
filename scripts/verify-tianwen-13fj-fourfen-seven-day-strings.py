#!/usr/bin/env python3
"""13FJ bounded NIKH Fourfen glyph-string steps D4-D10; never historic number adjudication."""
import argparse,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13FJ-NIKH-JUAN52-FOURFEN-D4D10-SIX-REPEATED-STRING-STEPS-R1.json"
FI="docs/research/TIANWEN-13FI-GORYEOSA-NIKH-D4D5D6-FOURFEN-PHOTO-STRING-STEPS-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
MAP={"〇":"0","一":"1","二":"2","三":"3","四":"4","五":"5","六":"6","七":"7","八":"8","九":"9"}
def read(p):return json.loads((R/p).read_text(encoding="utf8"))
def strnum(s):
 assert len(s)==4 and all(k in MAP for k in s)
 return int("".join(MAP[z] for z in s))
def check(x,fi,s,l):
 assert x["schema"]=="TIANWEN-13FJ-NIKH-JUAN52-FOURFEN-D4D10-SIX-REPEATED-STRING-STEPS-R1"
 assert x["issue_id"]=="TW-OPEN-0005"
 src=x["source_gallery_scope"];z=src["image3"]
 assert z=={"name":"kr_052_1057.jpg","source_viewer_index":3,"bytes":249769,"width":1027,"height":2000,"sha256":"61eb6a9dab9bbde1c91ab7d372ed0007f72fc2fb1aac436265ff882982465961"}
 assert src["valid_JPEG_download_prior_run"]==40057001564 and src["valid_JPEG_download_prior_artifact_id"]==12545602956
 assert src["source_work_juan"]==52 and src["physical_catalog_menu_label"]=="奎貴5553[乙亥字]"
 assert src["source_physical_book_ordinal"] is src["source_original_leaf_or_page"] is src["source_physical_edition_date"] is src["source_original_paper_state"] is None
 assert src["original_juan52_to_physical_book_mapping_authenticated"] is False and src["one_modern_gallery_not_four_independent_physical_copies"]
 a=x["new_source_pixel_direct_collations"]
 assert [p["day"] for p in a]==[7,8,9,10]
 assert [p["header"] for p in a]==["七日","八日","九日","十日"]
 assert [p["glyphs"] for p in a]==["五四九六","五六五八","五八二〇","五九八二"]
 assert [p["source_stated_fourfen_heading"] for p in a]==["四分"]*4
 assert all(p["direct_visual_method"]=="SOURCE_NATIVE_PIXEL_HUMAN_VISUAL_NO_OCR" for p in a)
 assert all(p["photo_image3_sha256"]==z["sha256"] for p in a)
 assert [p["native_bbox_xyxy"] for p in a]==[[716,606,790,1190],[476,606,555,1190],[275,606,360,1190],[79,606,171,1190]]
 assert [p["native_RGB_SHA256"] for p in a]==["f57d6a718070d0e2054265372c902d355de5e2e7eb46bfe674feee15773b485c","ad7ab657938b3dc34c88ab5f13a12d9df03e2a33d7a8cbb68ffc6a1400e85f20","d753ceeefe38ce963959c5f147cf150a75f55a2787bc85c84779ad37966e32f1","b280cc0ceda59794b3b8865bb99beb4ac065cc4913794c7d06f56ced2c262dc3"]
 assert [p["heading_bbox_xyxy"] for p in a]==[[576,238,667,407],[400,238,494,407],[204,238,307,407],[18,238,142,407]]
 assert [p["heading_native_RGB_SHA256"] for p in a]==["5d5aede949f2f6152df6dc1d564bd799e6899c02f1853fb439afe0fed0a8294f","c45649d4ed943a517e57592ccbbb0cb7828623ccb126a8eeabf9f79a1e2f5d5f","658e490249ceb032183c07b3a2c92b31ec588aebfb2016a21a4261f789f32e4a","fbae6387efa960e52fadc4c8d321818f663fc3e33d08ea1a0131546d2ac2d979"]
 # All source-native boxes must be in the actual photograph, not inferred physical folio coordinates.
 for r in a:
  for key in ("native_bbox_xyxy","heading_bbox_xyxy"):
   lft,top,right,bottom=r[key]
   assert 0<=lft<right<=z["width"] and 0<=top<bottom<=z["height"]
 old=x["prior_13fi_immutable_dependency"]
 assert old["prior_evidence_file"]==FI
 assert [old["day"+str(d)]["glyphs"] for d in (4,5,6)]==[r["direct_photo_glyphs"] for r in fi["source_photo_literal_rows"]]
 assert [old["day"+str(d)]["source_photo_sha256"] for d in (4,5,6)]==[r["image_sha256"] for r in fi["source_photo_literal_rows"]]
 assert [old["day"+str(d)]["RGB_lane_SHA256"] for d in (4,5,6)]==[r["sha256_native_RGB_crop"] for r in fi["source_photo_literal_rows"]]
 assert old["day6"]["source_photo_sha256"]==z["sha256"]
 q=x["literal_string_replay"]
 assert q["temporary_character_digit_map"]==MAP
 glyphs=[old["day"+str(d)]["glyphs"] for d in (4,5,6)]+[r["glyphs"] for r in a]
 assert glyphs==q["literal_glyphs_D4_to_D10"]
 assert glyphs==["五〇一〇","五一七二","五三三四","五四九六","五六五八","五八二〇","五九八二"]
 values=[strnum(y) for y in glyphs]
 assert values==[5010,5172,5334,5496,5658,5820,5982]==q["string_ordinal_temporary_values"]
 intervals=[b-a for a,b in zip(values,values[1:])]
 assert intervals==q["successive_literal_string_differences"]==[162]*6
 assert q["all_six_adjacent_steps_equal"] and q["source_day5_FIVE_internal_continuity_strengthened"]
 assert q["historic_decimal_unit_or_arithmetic_not_inferred"] and q["daily_printed_fourfen_header_not_equated_to_ecliptic_or_chudu_units"]
 assert q["NLC_prior_day5_original_photo"]=="四分〇一七二" and q["NLC_prior_source_GLYPH_O_erased"] is False
 assert q["NLC_prior_source_corruption_or_erratum_proven"] is False
 assert q["different_authenticated_physical_editions_with_verified_equivalent_row_count"]==0
 assert q["cross_copy_historical_winner"]=="UNADJUDICATED" and q["historical_source_number_D5"] is None
 t=x["remaining_research_boundaries"]
 assert t["G893_original_six_numeric_controls"]=="OPEN" and t["previous_13EI_source_claim"]=="RETRACTED"
 assert t["D30_summer_original_historic_number"] is t["D16_winter_original_historic_number"] is None
 assert t["NIKH_physical_book_or_leaf_source_photo_identity"]=="UNBOUND"
 assert t["uncollected_four_viewer_photos_due_transport_only"]==[9,13,17,22]
 tr=x["transmission_impact"];ch=x["changes"]
 assert tr["new_supported_edges"]==tr["revised_edges"]==tr["rejected_edges"]==[] and tr["distinct_original_physical_witnesses_authenticated"]==tr["physical_independent_editions_newly_voted"]==0
 assert ch["new_original_photo_glyph_bounded_daily_rows"]==4 and ch["external_source_registry_combined_unique_total"]==761
 assert ch["matrix_row_count"]==ch["matrix_audited_row_count"]==222 and ch["genealogy_node_total"]==252 and ch["genealogy_edge_total"]==238
 assert ch["open_or_blocked_risks"]==11 and ch["product"]=="CLOSED"
 assert all(ch[k]==0 for k in ("new_independent_publisher_gallery_groups","new_independent_physical_copies","new_ancient_historical_numeric_winners","external_source_registry_delta","matrix_row_delta","genealogy_node_delta","genealogy_edge_delta","closed_risks","algorithm_reopen_count","chart_candidate_collapse_count"))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(h.startswith("13FJ ") for h in s["historical_audit"]["current_focus"])
 issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert all(any(h.get("revision_id", "").startswith("TW-OPEN-0005-" + t + "-") and "next_action" in h.get("changed_fields", []) for h in issue["history"]) for t in ['13FJ'])
 assert {P,P.replace(".json",".md")}.issubset(set(issue["source_refs"]))
 assert any(h.get("revision_id")=="TW-OPEN-0005-13FJ-D4D10-NIKH-SEVEN-DAYS-SIX-STRING-STEPS-20261024" for h in issue["history"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"] and len(l["issues"])==11
 return True
def replay_source_JPEG(x,jpeg_path):
 # Optional pixel replay from the byte-identical saved official source, not a fetched guess.
 z=x["source_gallery_scope"]["image3"]
 p=Path(jpeg_path);raw=p.read_bytes()
 assert len(raw)==z["bytes"] and hashlib.sha256(raw).hexdigest()==z["sha256"]
 from PIL import Image
 with Image.open(p) as photo: rgb=photo.convert("RGB")
 assert rgb.size==(z["width"],z["height"])
 for lane in x["new_source_pixel_direct_collations"]:
  for key,sha_key in (("native_bbox_xyxy","native_RGB_SHA256"),("heading_bbox_xyxy","heading_native_RGB_SHA256")):
   assert hashlib.sha256(rgb.crop(tuple(lane[key])).tobytes()).hexdigest()==lane[sha_key]
 return True
if __name__=="__main__":
 arg=argparse.ArgumentParser()
 arg.add_argument("--source-jpeg",help="SHA-identical NIKH first-party saved kr_052_1057.jpg (optional)")
 options=arg.parse_args()
 e=read(P);assert check(e,read(FI),read(S),read(L))
 if options.source_jpeg: assert replay_source_JPEG(e,options.source_jpeg)
 print("13FJ_PASS_SEVEN_DAILY_SOURCE_GLYPH_STRINGS_SIX_162_STEPS_NO_HISTORICAL_WINNER")
