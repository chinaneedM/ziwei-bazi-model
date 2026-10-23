#!/usr/bin/env python3
"""13EJ source original bounded local D4/D5 glyph triads; no inferred numeric values."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13EJ-NCL03130-P74-D4-D5-TRIPLE-LANE-R1.json";S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json";EI="docs/research/TIANWEN-13EI-NCL03130-D4-MISATTRIBUTED-CHUDU-ROI-ERRATUM-R1.json";EG="docs/research/TIANWEN-13EG-NCL03130-SOLAR-FOLIO-DAY-BOUNDARIES-R1.json";ED="docs/research/TIANWEN-13ED-NCL03130-SOLAR-D30-EXTENDED-ORIGINAL-STRIP-R1.json"
EXPECTED=json.loads(r'''[["d4_heading",[885,150,951,300],"dac2d4865d428da1a875428c6542a24b5192ac05b0bcb49799d6ed625b23bb38","四日"],["d5_heading",[796,150,880,300],"fbe99140e3d22c09ae796069a60ebd31d76c832be6db3736b923b068694455ea","五日"],["d4_fourfen",[920,406,944,526],"a2025bbeaeee02f463802dbb5f2bcef70699cc6c7e728e1ea84d6ff33594d219","四分"],["d4_chudu",[948,406,970,526],"fe1d3dafd52e4207206e071d4ef3230a01265d81fda4782a65274dddb8b2163f","初度"],["d4_right",[972,406,994,526],"486736959e933a609384f4f841434c4361314eb1c965a543d7cdcc203f9f6388","一千"],["d5_fourfen",[831,405,855,525],"2d744d926a6f0901bf48f2c3ad4928aafd640c5f4de1d48364f6cb793484cf71","四分"],["d5_chudu",[851,404,874,524],"c52e5e3743ddcfbfce0116dfc78233d4cdbe9bf11821cf7ceed81eaf37ebb8e5","初度"],["d5_right",[880,404,904,524],"3733103270a18a445da080cbf5caedff8bffedd70035e0e8b89665f36514b06a","一千"],["d4_d5_context",[813,402,998,805],"9c87ced0df45309d09704d1f278c737a7df26dba21976e9fd66446da05d87bc0",null]]''')
def read(p):return json.loads((ROOT/p).read_text(encoding="utf8"))
def check(e,s,l,ei,eg,ed):
 assert e["schema"]=="TIANWEN-13EJ-NCL03130-P74-D4-D5-TRIPLE-LANE-R1" and e["issue_id"]=="TW-OPEN-0005"
 assert e["predecessors"]==[EI,EG]
 p=e["source"];target=next(x for x in eg["pages"] if x["pdf_page"]==74)
 assert p["pdf_sha256"]==ei["source"]["pdf_sha256"]==eg["source"]["pdf_sha256"]==ed["source"]["pdf_sha256"]
 assert p["pdf_page"]==74 and p["png_sha256"]==target["png_sha256"] and p["rgb_sha256"]==target["rgb_sha256"] and p["image_size"]==target["png_size"]
 assert p["artifact_id"]==ei["source"]["archive_artifact_id"] and p["workflow_run"]==ei["source"]["archive_run_id"]
 assert p["ocr_used"] is False and p["physical_copy"]==p["qing_vs_1905_stratum"]=="UNBOUND"
 assert [[x["name"],x["bbox"],x["rgb_sha256"],x["visible"]] for x in e["rois"]]==EXPECTED
 assert e["rois"][0]["rgb_sha256"]==target["boundaries"][0]["roi_rgb_sha256"]
 assert all(0<=b["bbox"][0]<b["bbox"][2]<=1305 and 0<=b["bbox"][1]<b["bbox"][3]<=873 for b in e["rois"])
 assert ei["error"]["actual_visible_opening"]=="四分" and ei["replacement"]["normalized_pair_geometry"]=="RETRACTED_NOT_ADMISSIBLE"
 o=e["observations"]
 assert o["d4_heading"]=="四日" and o["d5_heading"]=="五日"
 assert o["d4_visible_columns"]==o["d5_visible_columns"]==["四分","初度","一千"]
 assert o["reading_status"]=="PREFIX_ONLY_NOT_COMPLETE_NUMERIC_FIELD"
 assert o["previous_13eh_false_equal_offset_retracted"] is True and o["prior_13ei_erratum_preserved"] is True
 assert o["d30_original_literal"]==ed["finding"]["d30_visible_glyph_group"]=="初度九十六二〇三" and o["d30_exact_numeric"] is None
 assert o["technical_semantic_relation_p73"]==o["global_day_offset"]=="UNPROVEN" and o["independent_original_witness_count"]==0
 i=e["impact"]
 assert i["open_or_blocked"]==11 and i["product"]=="CLOSED"
 assert all(i[k]==0 for k in ("new_sources","new_ancient_witnesses","matrix_rows","genealogy_nodes","genealogy_edges","algorithm_reopens","issues_closed"))
 assert s["schema_version"]=="1.785.0"==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]=="13EJ"==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert s["historical_audit"]["current_focus"][-1].startswith("13EJ NCL03130 P74 D4 D5 ORIGINAL GLYPH TRIADS")
 q=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert q["status"]=="OPEN" and q["priority"]=="P0" and q["next_action"].startswith("13EJ CURRENT ACTION")
 assert all(k in q["next_action"] for k in ("D4","D5","D30","四分","初度","NULL"))
 assert set([E,E.replace(".json",".md")]).issubset(set(q["source_refs"]))
 h=q["history"][-1]
 assert h["revision_id"]=="TW-OPEN-0005-13EJ-SAME-PAGE-D4-D5-PREFIX-20261023" and h["previous_next_action"].startswith("13EI CURRENT ACTION")
 assert set(h["changed_fields"])=={"source_refs","next_action"}
 assert len(l["issues"])==11 and l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
def replay(e,directory):
 from PIL import Image
 f=Path(directory)/"original-p074.png"
 assert hashlib.sha256(f.read_bytes()).hexdigest()==e["source"]["png_sha256"]
 with Image.open(f) as im:rgb=im.convert("RGB")
 assert hashlib.sha256(rgb.tobytes()).hexdigest()==e["source"]["rgb_sha256"]
 for z in e["rois"]:
  assert hashlib.sha256(rgb.crop(tuple(z["bbox"])).tobytes()).hexdigest()==z["rgb_sha256"],z["name"]
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--source-dir");args=p.parse_args()
 e=read(E);assert check(e,read(S),read(L),read(EI),read(EG),read(ED))
 if args.source_dir:assert replay(e,args.source_dir)
 print("13EJ_PASS ORIGINAL_P74_D4_D5_BOUNDED_GLYPHS_D30_NULL")
