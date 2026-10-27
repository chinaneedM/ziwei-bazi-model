#!/usr/bin/env python3
"""13BY original Waseda winter D88 to same-page summer title/day0 regression."""
import json,hashlib,argparse
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BY-GORYEOSA-WASEDA-P31-WINTER-D88-SUMMER-NEW-TITLE-R1.json"
MD="docs/research/TIANWEN-13BY-GORYEOSA-WASEDA-P31-WINTER-D88-SUMMER-NEW-TITLE-R1.md"
BV="docs/research/TIANWEN-13BV-GORYEOSA-WASEDA-P21-P23-ORIGINAL-SOLAR-TABLE-TITLE-AND-FIRST-DAY-INDEX-R1.json"
BX="docs/research/TIANWEN-13BX-GORYEOSA-WASEDA-P26-P27-ORIGINAL-D39-D56-AND-EXTENDED-FOLIO-ATLAS-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
ROI=[["WINTER_D83",30,"WINTER_DAY","八十三日",[465,350,615,680],"241982ba72e68efa386cb37989963dae5bce05c3c9ff09cce35ad741f4ee265b"],["WINTER_D84",31,"WINTER_DAY","八十四日",[2035,355,2190,680],"27524ab024aecaf621ef62c9ae4f150a9cc3105c41d6f2c8b55d34ceee0db0e4"],["WINTER_D88",31,"WINTER_LAST_DAY","八十八日",[995,355,1125,675],"4dda581e6e01333d6b863510cc420e651ab61e14b6ac4944632b5b65e1bb1045"],["SUMMER_TITLE",31,"NEW_SUMMER_TITLE","大陽夏至前後二象縮初盈末限",[825,355,948,1300],"ad333e27e80e6f9fc07b9065ba14968e1ca88a236c030cdfef7ed2342eb4bec9"],["SUMMER_JIRI",31,"DAY_INDEX_LABEL","積日",[735,355,820,640],"3594b026e1359ad6c8b3de4bc544902b05452e404aa1bcd78943a1ce8ddef5e8"],["SUMMER_D0",31,"SUMMER_DAY","初日",[615,350,700,660],"9654c0cd2abe78e97290e2e3c343dcf65a6afaf5bf9f336ea123580f955d8a83"],["SUMMER_D1",31,"SUMMER_DAY","一日",[435,350,550,660],"4d2b405ab42d44529d1e84747eef20d4aafe809ef597fba62063cfef133a9fbe"],["SUMMER_D2",32,"SUMMER_DAY","二日",[2050,350,2185,675],"2a4ae2c46ae09ff15c381ce3105141d8805f357cea14e5e9336d3fd8d1704aea"],["SUMMER_D10",32,"SUMMER_DAY","十日",[380,345,555,680],"dad21ed2f6b8f53199652d9b8701c4faf02ab33a35fe058afe1cc88103eba66d"]]
SOURCES=[[30,91,"93bd7198f3e56c8738d481b0281e064cab2ef32684997f494c8d91582b1b9f60",[2592,1728]],[31,94,"c499de6f3030154720f1dd422a26820c4fca233e81b5c56caf5e57906e4283ea",[2592,1728]],[32,97,"e2fc1d5d5d2621c4d78186d6d6ce6343a07b2fb07e7bd99e7e3391fc3338cd25",[2592,1728]]]
def load(p):return json.loads((R/p).read_text(encoding="utf-8"))
def replay(e,paths):
 from PIL import Image
 assert len(paths)==3
 for source,path in zip(e["source"]["source_images"],paths):
  raw=Path(path).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==source["sha256"]
  with Image.open(path) as im:
   rgb=im.convert("RGB")
   assert list(rgb.size)==source["dimensions"]
   for z in e["original_rgb_lanes"]:
    if z["page"]==source["page"]:
     assert hashlib.sha256(rgb.crop(tuple(z["bbox"])).tobytes()).hexdigest()==z["rgb_sha256"]
 return True
def check(e,s,l,prior):
 assert e["schema"]=="TIANWEN-13BY-WASEDA-ORIGINAL-WINTER-D88-AND-SUMMER-START-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["date"]=="2026-10-21"
 assert e["grade"]=="ORIGINAL_JPEG_SHA256_MANUAL_NATIVE_RGB_PRINTED_SECTION_AND_DAY_NO_OCR"
 src=e["source"]
 assert src["physical_holding"]=="WASEDA-RI06-02809-BOOK33"
 assert src["pdf_sha256"]==prior["BX"]["source"]["pdf_sha256"]==prior["BV"]["source"]["pdf_sha256"]
 assert src["run"]==39601924438 and src["artifact_id"]==12346735638
 assert src["artifact_zip_sha256"]=="0ce306c099a1ed62dd24a3256ba043062490409bd5d531b543c16f1b00017710"
 assert [(x["page"],x["xref"],x["sha256"],x["dimensions"]) for x in src["source_images"]]==[tuple(x) for x in SOURCES]
 assert [(z["key"],z["page"],z["role"],z["literal"],z["bbox"],z["rgb_sha256"]) for z in e["original_rgb_lanes"]]==[tuple(x) for x in ROI]
 assert len(e["original_rgb_lanes"])==9
 f=e["findings"]
 assert f["last_winter_printed_day"]=="八十八日" and f["winter_last_page"]==31
 assert f["winter_copy_specific_table_end"] is True
 assert f["next_title_original_literal"]=="大陽夏至前後二象縮初盈末限"
 assert f["next_summer_title_page"]==31
 assert f["summer_day_index_label"]=="積日" and f["summer_initial_days"]==["初日","一日"]
 assert f["next_original_page_first_last"]==["二日","十日"]
 assert f["source_title_first_glyph"]=="大_GRAPH; NORMALIZED_太_NOT_ADJUDICATED"
 assert f["previous_13BV_title_literal"]==prior["BV"]["finding"]["solar_table_original_title"]
 assert f["historical_original_title_normalization_winner"]=="UNRESOLVED"
 assert f["Waseda_D16_independent_cumulative"]=="UNBOUND"
 assert f["whole_table_calendar_formula_proven"] is False
 assert f["cross_copy_universal_day_shift_proven"] is False
 assert f["printed_積日_equivalent_numeric_cumulative"]=="UNPROVEN"
 assert f["G893_SHAO_WEI_MING1569_same_units"]=="UNPROVEN"
 assert f["D16_ancestral_one_two"]=="UNRESOLVED"
 assert e["provenance"]=={"prior_table_first_days":BV,"prior_bulk_atlas_request":BX,"source_atlas_already_archived":True,"original_page30_32_manual_rois_count":9,"all_original_day_numbers_independently_roi_verified":False}
 scope=e["scope"]
 assert all(scope[k]==0 for k in ("new_physical_witnesses","new_independent_stemmatic_votes","new_registry_sources","matrix_rows_added","genealogy_nodes_added","genealogy_edges_added","algorithm_reopens"))
 assert scope["research_issues_open"]==len(l["issues"])==11 and scope["product"]=="CLOSED"
 assert e["transmission_impact"]["nodes_added"]==e["transmission_impact"]["edges_supported"]==e["transmission_impact"]["edges_revised"]==[]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert issue["source_refs"].count(MD)==issue["source_refs"].count(P)==1
 assert issue["source_refs"].index(P)==issue["source_refs"].index(MD)+1
 rev=next(x for x in issue["history"] if x.get("revision_id")=="TW-OPEN-0005-ORIGINAL-WINTER-SUMMER-13BY")
 assert rev["previous_next_action"].startswith("13BX CURRENT ACTION")
 assert {MD,P,BX,BV}.issubset(set(rev["evidence_refs"]))
 later=any("next_action" in z.get("changed_fields",[]) for z in issue["history"][issue["history"].index(rev)+1:])
 prefix=l["binding"]["latest_research_focus_prefix"]
 assert issue["next_action"].startswith("13BY CURRENT ACTION") or (later and prefix!="13BY" and (issue["next_action"].startswith(prefix+" CURRENT ACTION") or issue["next_action"].startswith(next((z["revision_id"].split("-")[3]+" CURRENT ACTION" for z in reversed(issue["history"]) if "next_action" in z.get("changed_fields",[]) and len(z.get("revision_id","").split("-"))>3 and z["revision_id"].split("-")[3].startswith("13")),"__NO_RECORDED_ACTION__"))))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert any(z.startswith("13BY ") for z in s["historical_audit"]["current_focus"])
 assert prefix==s["historical_audit"]["current_focus"][-1].split(" ")[0]
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 assert set(l["checkpoint_log"][-1]["reviewed_issue_ids"])=={z["id"] for z in l["issues"]}
 assert (R/MD).is_file()
 return True
if __name__=="__main__":
 parser=argparse.ArgumentParser();parser.add_argument("--p30");parser.add_argument("--p31");parser.add_argument("--p32")
 args=parser.parse_args()
 e=load(P)
 assert check(e,load(S),load(L),{"BX":load(BX),"BV":load(BV)})
 if any((args.p30,args.p31,args.p32)):
  assert all((args.p30,args.p31,args.p32))
  assert replay(e,(args.p30,args.p31,args.p32))
 print("13BY Waseda source winter D88 to summer table title and day0 source original SHA PASS")
