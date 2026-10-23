#!/usr/bin/env python3
"""13BZ original Waseda source-image D90..D93 repeated heading and textual terminal."""
import argparse,hashlib,io,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BZ-GORYEOSA-WASEDA-SUMMER-D91-D93-AND-EXPLANATORY-TERMINUS-R1.json"
MD="docs/research/TIANWEN-13BZ-GORYEOSA-WASEDA-SUMMER-D91-D93-AND-EXPLANATORY-TERMINUS-R1.md"
BY="docs/research/TIANWEN-13BY-GORYEOSA-WASEDA-P31-WINTER-D88-SUMMER-NEW-TITLE-R1.json"
BX="docs/research/TIANWEN-13BX-GORYEOSA-WASEDA-P26-P27-ORIGINAL-D39-D56-AND-EXTENDED-FOLIO-ATLAS-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
EXPECTED_SOURCES=[{"page":42,"xref":127,"sha":"abdfaf2af286568ce6fd7966b5bbe51ef1b7476fd8dcf6999801ca3a7eb8def5"},{"page":43,"xref":130,"sha":"7fce99dc3d9bbacada8744773d656b105d254206769301457e7c1105c136eb5a"},{"page":44,"xref":133,"sha":"09dcf033326803c6b59bd174a9220a6bfa0a680e349e1cdd842b659caa12b0c7"}]
EXPECTED_ROIS=[[42,"P42_D90",[570,375,715,650],"23002c4edc69a4c7f5fa4a8bd966c966b4be151d6f817bd8f8caf58ae7afa345","DAY","九十日"],[42,"P42_D91",[420,375,550,650],"0dcb28dac5d8001f33243f403a509efd65cf94463f9e9018934dd7396bbed80b","DAY","九十一日"],[43,"P43_D92",[1970,367,2140,650],"8f392f3bbb3a7ceced76d4279b54988134593f8bc0e5081cf4e2126dca4b2d26","DAY","九十二日"],[43,"P43_D93_RIGHT",[1790,366,1970,650],"f09a183f728ea162cb45e51656f19c66e3714236f6fae80ee9943a478bd0fcbe","DAY","九十三日"],[43,"P43_D93_LEFT",[1590,365,1790,655],"8df235541c0588d2da06faaa5d1f38f165c0664288a645fb041d302d005d1989","DAY","九十三日"],[43,"P43_YING_CHU_LIMIT_PROSE",[1340,377,1650,1410],"9a7558bcd03f6c29586d894f467e274ca0116d9b1e160a79f8760b18042e3069","POST_TABLE_PROSE","盈初縮末限以初日行分至八十八日計得"],[43,"P43_SUO_CHU_LIMIT_PROSE",[785,375,1130,1400],"fa63f37b04cc830c87337c9fdf500838be824d4c560a67c6b8f7f69d9a3fade1","POST_TABLE_PROSE","縮初盈末限以初日行分至九十三日計得"],[44,"P44_REPEATED_D92",[1970,367,2140,650],"3ca945b1c3d1f8cc5b6400ec1165b11cc210cfb042ff80ea73c24a48c6d5dc6b","DUPLICATE_CAPTURE","九十二日"],[44,"P44_REPEATED_YING_CHU_PROSE",[1340,377,1650,1410],"42a4f95742770cc504b15cb9ac05dd38dbf9c43c72df6deb37bd849d59e59f6b","DUPLICATE_CAPTURE","盈初縮末限以初日行分至八十八日計得"],[44,"P44_ATTACHED_NOTE",[398,410,670,1010],"62321d3acdf8c0cb18569d871fc3a2e5328e07973d28550e217b6dde9e464260","PHYSICAL_NOTE_STATE","紙條遮蓋區"]]
ARCHIVE_SHA="0ce306c099a1ed62dd24a3256ba043062490409bd5d531b543c16f1b00017710"
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def replay(e,zip_path):
 from PIL import Image
 raw=Path(zip_path).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==ARCHIVE_SHA
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  assert z.testzip() is None
  receipt=json.loads(z.read("receipt.json"))
  for src in e["source"]["image_sources"]:
   row=next(x for x in receipt["original_image_rows"] if x["page_1based"]==src["page"])
   assert row["embedded_xref"]==src["xref"] and row["original_sha256"]==src["sha"]
   img=z.read(row["original_file"])
   assert hashlib.sha256(img).hexdigest()==src["sha"]
   with Image.open(io.BytesIO(img)) as im:
    rgb=im.convert("RGB")
    assert list(rgb.size)==[2592,1728]
    for b in e["original_native_rgb_rois"]:
     if b["page"]==src["page"]:
      assert hashlib.sha256(rgb.crop(tuple(b["bbox"])).tobytes()).hexdigest()==b["rgb_sha256"]
 return True
def check(e,st,ld,old):
 assert e["schema"]=="TIANWEN-13BZ-WASEDA-SUMMER-D90-D93-ORIGINAL-TERMINAL-EXPLANATION-AND-ATTACHED-NOTE-R1"
 assert e["date"]=="2026-10-21" and e["issue_id"]=="TW-OPEN-0005"
 assert e["grade"]=="DIRECT_MANUAL_ORIGINAL_JPEG_TIGHT_RGB_ROI_NO_OCR"
 a=e["source"];assert a["holding"]=="WASEDA-RI06-02809-BOOK33"
 assert a["pdf_sha256"]==old["BY"]["source"]["pdf_sha256"]
 assert a["run"]==39601924438 and a["artifact_id"]==12346735638 and a["archive_zip_sha256"]==ARCHIVE_SHA
 assert a["image_dimensions"]==[2592,1728] and a["image_sources"]==EXPECTED_SOURCES
 assert [(x["page"],x["key"],x["bbox"],x["rgb_sha256"],x["role"],x["literal"]) for x in e["original_native_rgb_rois"]]==[tuple(x) for x in EXPECTED_ROIS]
 for b in e["original_native_rgb_rois"]:
  x1,y1,x2,y2=b["bbox"];assert 0<=x1<x2<=2592 and 0<=y1<y2<=1728
 assert e["original_segment_context"]["previous_segment"]==BY
 assert e["original_segment_context"]["summer_title"]==old["BY"]["findings"]["next_title_original_literal"]
 assert e["original_segment_context"]["printed_day_restart"]=="初日"
 assert e["original_segment_context"]["summer_printed_D90"]=="九十日" and e["original_segment_context"]["summer_printed_D91"]=="九十一日"
 assert e["original_segment_context"]["summer_printed_D92"]=="九十二日"
 assert e["original_segment_context"]["summer_printed_D93_occurrences_in_p43"]==2
 assert e["original_segment_context"]["day_93_repeated_in_same_original_print"] is True
 assert e["original_segment_context"]["after_D93_source_kind"]=="NON_DAY_COLUMN_EXPLANATORY_LIMIT_PROSE"
 assert e["original_segment_context"]["claimed_day94_original"] is False
 assert e["original_segment_context"]["all_intermediate_printed_summer_day_glyphs_individually_hashed"] is False
 assert [r["literal"] for r in e["original_native_rgb_rois"] if r["page"]==43 and r["role"]=="DAY"]==["九十二日","九十三日","九十三日"]
 assert e["firstparty_prose_scope"]["p43_right"]=="盈初縮末限以初日行分至八十八日計得"
 assert e["firstparty_prose_scope"]["p43_left"]=="縮初盈末限以初日行分至九十三日計得"
 assert e["firstparty_prose_scope"]["prose_88_and_93_are_not_additional_independent_day_header_votes"] is True
 assert e["firstparty_prose_scope"]["first_summer_table_printed_terminal_day"]==93
 assert e["firstparty_prose_scope"]["complete_printed_table_next_section_mechanical_law"]=="NOT_YET_PROVEN"
 b=e["double_page_source_scope"]
 assert all(b[k] is True for k in ("p43_p44_same_layout_opening_observed","provider_image_sha_distinct","attached_note_paper_position_or_cover_differs"))
 assert b["reason_for_repeat_source_capture"]=="UNKNOWN"
 assert b["physical_source_vote_count_for_both_images"]==1 and b["independent_stemmatic_votes_added"]==0
 assert e["previous_evidence"]=={"summer_restart_source":BY,"atlas_acquisition_source":BX}
 assert old["BX"]["requested_atlas"]["pages_first"]==28 and old["BX"]["requested_atlas"]["pages_last"]==44
 assert old["BY"]["findings"]["summer_initial_days"]==["初日","一日"]
 u=e["future_unresolved"]
 assert u["winter_D16_same_original_cumulative"]=="UNBOUND"
 assert u["winter_summer_field_units_and_timing"]=="UNPROVEN"
 assert u["NAJ_versus_Waseda_label_alignment_global"]=="UNPROVEN"
 assert u["G893_shao_wei_and_Ming1569_same_field"]=="UNPROVEN"
 assert u["waseda_naj_stemma"]==u["day16_earliest_archetype"]=="UNRESOLVED"
 fw=e["scope_firewall"];assert fw["existing_original_jpeg_sources_reused"]==3
 assert all(fw[k]==0 for k in ("new_physical_historical_witnesses","new_source_registry_rows","new_stemmatic_votes","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens"))
 assert fw["open_issues"]==len(ld["issues"])==11 and fw["product"]=="CLOSED"
 assert e["transmission_impact"]["nodes_added"]==e["transmission_impact"]["edges_supported"]==e["transmission_impact"]["edges_revised"]==[]
 issue=next(z for z in ld["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert issue["source_refs"].count(MD)==issue["source_refs"].count(P)==1
 assert issue["source_refs"].index(P)==issue["source_refs"].index(MD)+1
 rev=next(z for z in issue["history"] if z.get("revision_id")=="TW-OPEN-0005-SUMMER-TABLE-TERMINUS-13BZ")
 assert rev["previous_next_action"].startswith("13BY CURRENT ACTION")
 assert {MD,P,BY,BX}.issubset(set(rev["evidence_refs"]))
 later=any("next_action" in x.get("changed_fields",[]) for x in issue["history"][issue["history"].index(rev)+1:])
 prefix=ld["binding"]["latest_research_focus_prefix"]
 assert issue["next_action"].startswith("13BZ CURRENT ACTION") or (later and prefix!="13BZ" and (issue["next_action"].startswith(prefix+" CURRENT ACTION") or issue["next_action"].startswith(next((z["revision_id"].split("-")[3]+" CURRENT ACTION" for z in reversed(issue["history"]) if "next_action" in z.get("changed_fields",[]) and len(z.get("revision_id","").split("-"))>3 and z["revision_id"].split("-")[3].startswith("13")),"__NO_RECORDED_ACTION__"))))
 assert st["schema_version"]==ld["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert ld["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
 assert any(x.startswith("13BZ ") for x in st["historical_audit"]["current_focus"])
 assert prefix==st["historical_audit"]["current_focus"][-1].split(" ")[0]
 assert ld["checkpoint_log"][-1]["state_version"]==st["schema_version"]
 assert set(ld["checkpoint_log"][-1]["reviewed_issue_ids"])=={x["id"] for x in ld["issues"]}
 assert (ROOT/MD).is_file()
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--atlas-zip");a=p.parse_args()
 e=load(P);assert check(e,load(STATE),load(LEDGER),{"BY":load(BY),"BX":load(BX)})
 if a.atlas_zip: assert replay(e,a.atlas_zip)
 print("13BZ original Waseda summer D91-D93 terminal and repeated digital capture boundary PASS")
