#!/usr/bin/env python3
"""13EF source P73 original heading and three technical terms: strict original ROI SHA."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13EF-NCL03130-SOLAR-P73-TECHNICAL-HEADINGS-R1.json";STATE="docs/PROJECT-CURRENT-STATE-R1.json";LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
DZ="docs/research/TIANWEN-13DZ-NCL03130-CORRECT-SOLAR-D28-ORIGINAL-P76-LOCATOR-R1.json"
EE="docs/research/TIANWEN-13EE-NCL03130-SOLAR-SAME-COLUMN-THREE-FOLIO-R1.json"
NAMES=["solar_table_title","technical_labels_panel","xingdu_header","ying_suo_ji_header","ri_cha_header","first_day_heading","ji_ri_heading","opening_xingdu_footprint","opening_multi_column_panel"]
BOXES=[[456,159,511,632],[325,392,459,622],[329,402,374,495],[371,398,416,569],[416,396,457,500],[327,161,373,253],[410,156,456,256],[331,388,373,800],[327,388,455,800]]
HASHES=["6893b7712b46a28460167908c88094428be819f287affb6a4c576d1705966617","2cc22963cef125259bb01bd99eeb05e1848bec1f27c7a62cb34d1f801f3b7d19","d8d2c619042e556b5cfabfc9f7e943c19e65d8f3a4d8e254d3556bde18a5a6b1","02d347c0a3cd1ebd1fe849a9946784585c4f6183b247ac062a584587da031d07","3591c4790b73e375c2b0d3e9a50f84990df7a2ceff474d059316dcce6f65733e","17242e4963652a445f6605599771ff7ed37ca6f28547c3d8bb4745b385fb8d02","6826b6faaae84e25325290bc074ee3a77b5f0d421579b26b33d030e1d6d27dc9","b2cc051e044c181b0ba307a2c5f14d048594cfd69b1c1331090d096f9758bf93","3ae4d9cf4c619c5cd1aa62ca36843a9ac1f36e43fa92eac9fba86c2f7424e579"]
GLYPHS=["大陽夏至前後二象縮初盈末限",None,"行度","盈縮積","日差","初日","積日",None,None]
GRADES=["DIRECT_ORIGINAL_HEADING","ORIGINAL_GROUPED_LABEL_GEOMETRY","DIRECT_ORIGINAL_TECHNICAL_TERM","DIRECT_ORIGINAL_TECHNICAL_TERM","DIRECT_ORIGINAL_TECHNICAL_TERM","DIRECT_ORIGINAL_DAY_HEADING","DIRECT_ORIGINAL_COLUMN_TOP_LABEL","SOURCE_IMAGE_FIELD_GEOMETRY_ONLY","SOURCE_IMAGE_MULTICOLUMN_GEOMETRY_ONLY"]
def read(p):return json.loads((ROOT/p).read_text(encoding="utf8"))
def check(e,s,l,dz,ee):
 assert e["schema"]=="TIANWEN-13EF-NCL03130-SOLAR-P73-TECHNICAL-HEADINGS-R1" and e["issue_id"]=="TW-OPEN-0005"
 assert e["evidence_type"]=="DIRECT_ARCHIVED_SOURCE_ORIGINAL_P73_HEADER_GLYPH_AND_ROI_REPLAY_NOT_MECHANICAL_RULE_ADJUDICATION"
 a=e["source"];p=a["original_page"];reg={v["page"]:v for v in dz["original_page_register"]}[73]
 assert a["pdf_sha256"]==dz["source"]["source_sha256"]==ee["source"]["pdf_sha256"]
 assert a["original_archive_run"]==ee["source"]["archive_run"] and a["original_archive_artifact_id"]==ee["source"]["archive_artifact_id"]
 assert (p["page"],p["size"],p["png_sha256"],p["rgb_sha256"])==(73,reg["size"],reg["png_sha256"],reg["rgb_sha256"])
 assert a["physical_copy"]==a["qing_vs_1905_stratum"]=="UNBOUND" and a["ocr_used"] is False
 arr=e["original_rois"];assert len(arr)==len(NAMES)==9
 assert [(r["name"],r["bbox"],r["rgb_sha256"],r["original_literal"],r["grade"]) for r in arr]==list(zip(NAMES,BOXES,HASHES,GLYPHS,GRADES))
 pos=e["positive_source_facts"]
 assert pos["full_table_title"]=="大陽夏至前後二象縮初盈末限" and pos["table_class"]=="SOLAR_XIAZHI"
 assert pos["visible_original_technical_names"]==["行度","盈縮積","日差"]
 assert pos["opening_day_title"]=="初日" and pos["additional_top_label"]=="積日"
 lim=e["limits"]
 assert lim["direct_long_short_cumulative_identity_on_later_pages"]=="NOT_ESTABLISHED_BY_HEADER_ALONE"
 assert lim["source_p73_day0_to_p75_p77_numeric_rule"]=="UNPROVEN" and lim["original_d30_exact_numeric"] is None
 assert lim["earlier_d30_original_visible_literal"]==ee["observation"]["d30_existing_literal"]
 assert lim["global_day_offset_law"]=="UNPROVEN" and lim["same_witness_pages_not_independent"] is True
 assert not lim["all_visible_rois_complete_numeric_lines"] and lim["independent_physical_copy_added"]==0
 imp=e["impact"];assert (imp["new_source_original_p73_heading_review"],imp["new_original_technical_terms_registered"],imp["remaining_risks_open_or_blocked"],imp["product"])==(1,3,11,"CLOSED")
 assert all(imp[k]==0 for k in ("new_physical_witnesses","new_stemmatic_independent_votes","new_numerical_field_adjudications","new_registry_sources","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens","issues_closed"))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"]) and l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13EF DIRECT NCL03130 TRUE SOLAR P73") for x in s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 current_prefix=issue["next_action"].split(" ",1)[0]
 assert issue["next_action"].startswith(current_prefix+" CURRENT ACTION")
 future=[h for h in issue["history"] if h.get("event")=="ISSUE_REVISION" and "next_action" in h.get("changed_fields",[])]
 assert future and future[-1]["revision_id"].startswith("TW-OPEN-0005-"+current_prefix+"-")
 assert future[-1].get("evidence_refs") and any(z.startswith(current_prefix+" ") for z in s["historical_audit"]["current_focus"])
 assert "D30" in issue["next_action"] and pos["visible_original_technical_names"]==["行度","盈縮積","日差"]
 assert E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"]
 h=next(h for h in issue["history"] if h.get("revision_id")=="TW-OPEN-0005-13EF-P73-ORIGINAL-TECHNICAL-HEADINGS-20261023")
 assert h["previous_next_action"].startswith("13EE CURRENT ACTION") and set(h["changed_fields"])=={"source_refs","next_action"}
 assert set([E,E.replace(".json",".md"),EE]).issubset(set(h["evidence_refs"]))
 assert len(l["issues"])==11 and l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
def replay(e,path):
 from PIL import Image
 src=Path(path);b=src.read_bytes();p=e["source"]["original_page"]
 assert hashlib.sha256(b).hexdigest()==p["png_sha256"]
 with Image.open(src) as im:rgb=im.convert("RGB")
 assert list(rgb.size)==p["size"] and hashlib.sha256(rgb.tobytes()).hexdigest()==p["rgb_sha256"]
 for r in e["original_rois"]:
  x0,y0,x1,y1=r["bbox"];assert 0<=x0<x1<=rgb.width and 0<=y0<y1<=rgb.height
  assert hashlib.sha256(rgb.crop(r["bbox"]).tobytes()).hexdigest()==r["rgb_sha256"],r["name"]
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--source-image");args=p.parse_args()
 e=read(E);assert check(e,read(STATE),read(LEDGER),read(DZ),read(EE))
 if args.source_image:assert replay(e,args.source_image)
 print("13EF_PASS ORIGINAL_P73_XINGDU_YING_SUO_JI_RI_CHA D30_NUMERIC_OPEN")
