#!/usr/bin/env python3
"""13EK exact-NCL original glyph strip positive with SHA and decimal firewall."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13EK-NCL03130-P74-D4-D5-CHUDU-LONG-STRIPS-R1.json";S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json";EJ="docs/research/TIANWEN-13EJ-NCL03130-P74-D4-D5-TRIPLE-LANE-R1.json";EI="docs/research/TIANWEN-13EI-NCL03130-D4-MISATTRIBUTED-CHUDU-ROI-ERRATUM-R1.json";ED="docs/research/TIANWEN-13ED-NCL03130-SOLAR-D30-EXTENDED-ORIGINAL-STRIP-R1.json"
EXPECTED=json.loads(r'''[["D4_CHUDU_LONG",[943,411,970,771],"a82d6f37825b16f1c1250604f8021cbf165b2ce26d0913928a19be720eb0375c","初度九十五二八五一"],["D5_CHUDU_LONG",[849,411,876,771],"3005a769650dbb37c5213ab977a1f196b88c9a2bca6f02e0d7e75b1747e2dc79","初度九十五三三〇〇"],["D4_LOWER_TAIL",[943,771,970,830],"c702230aac436f44407d3c37b1f41646b26f8bd51960501e3bf692b4d3524487",null],["D5_LOWER_TAIL",[849,771,876,830],"8d04634715f04bbc86d67570a4102835cda24bb83bfc042bd217949a973f2c09",null],["D4_EXTENDED",[943,405,970,830],"99e47841e2fd50bc11b389e14b49246c0ce732fd7b55f2a347084bdeda86093f",null],["D5_EXTENDED",[849,405,876,830],"caf2dea7a743478275aa3a291056963040201efeefac1165a695260bf321043c",null],["D4_FOURFEN_NEIGHBOR",[918,411,945,771],"41022bfb57573dfb9579c6f2a075f107833d7367725137a583c5c7bd6a2faa9f",null],["D5_FOURFEN_NEIGHBOR",[826,411,855,771],"6785ec77f463723ac44552069104b244a364861deaf89c0913f7d5d3c23bbce0",null],["D4_D5_PANEL",[804,397,1003,790],"cd7ed52849863f08406ede7848cc57d113c8120647fd0aa9ad2a5ce917135755",null]]''')
def read(p):return json.loads((ROOT/p).read_text(encoding="utf8"))
def check(e,s,l,ej,ei,ed):
 assert e["schema"]=="TIANWEN-13EK-NCL03130-P74-D4-D5-CHUDU-LONG-STRIPS-R1" and e["issue_id"]=="TW-OPEN-0005"
 assert e["predecessors"]==[EJ,EI] and e["source"]["ocr_used"] is False
 src=e["source"]
 assert src["pdf_sha256"]==ej["source"]["pdf_sha256"]==ei["source"]["pdf_sha256"]==ed["source"]["pdf_sha256"]
 assert src["pdf_page"]==ej["source"]["pdf_page"]==74
 assert src["png_sha256"]==ej["source"]["png_sha256"] and src["rgb_sha256"]==ej["source"]["rgb_sha256"] and src["size"]==ej["source"]["image_size"]
 assert src["artifact_id"]==ej["source"]["artifact_id"] and src["original_archive_run"]==ei["source"]["archive_run_id"]
 assert src["physical_copy"]==src["qing_vs_1905_stratum"]=="UNBOUND" and src["independent_original_witnesses_added"]==0
 assert [[z["name"],z["bbox"],z["rgb_sha256"],z["visible_literal"]] for z in e["rois"]]==EXPECTED
 assert len(e["rois"])==9 and all(z["grade"]=="ORIGINAL_RGB_SHA_AND_HUMAN_SOURCE_GLYPH_OBSERVATION" for z in e["rois"])
 assert all(0<=r["bbox"][0]<r["bbox"][2]<=1305 and 0<=r["bbox"][1]<r["bbox"][3]<=873 for r in e["rois"])
 f=e["findings"]
 assert f["printed_days"]==["四日","五日"] and ej["observations"]["d4_heading"]=="四日" and ej["observations"]["d5_heading"]=="五日"
 assert f["D4_visible_string"]==e["rois"][0]["visible_literal"]=="初度九十五二八五一"
 assert f["D5_visible_string"]==e["rois"][1]["visible_literal"]=="初度九十五三三〇〇"
 assert f["D4_visible_characters"]==len(f["D4_visible_string"])==9
 assert f["D5_visible_characters"]==len(f["D5_visible_string"])==9
 assert f["existing_D30_source_string"]==ed["finding"]["d30_visible_glyph_group"]=="初度九十六二〇三"
 assert f["existing_D30_visible_characters"]==len(f["existing_D30_source_string"])==8
 assert f["visible_one_character_length_difference_only"] is True and f["source_literal_count_not_historical_decimal_precision"] is True
 assert f["D4_exact_numeric_decimal"] is f["D5_exact_numeric_decimal"] is f["D30_exact_numeric_decimal"] is None
 assert f["full_semantic_field_complete"]=="UNPROVEN" and f["technical_heading_map_to_p73"]=="UNPROVEN"
 assert f["negative_tail_scope"].startswith("HUMAN_OBSERVED_NO_ADDITIONAL_SAME_NARROW_STRIP_GLYPH")
 assert f["same_page_adjacent_column_splicing"] is False and f["entire_row_all_lanes_transcribed"] is False
 assert f["legacy_13eh_misread_reinstated"] is False and ei["replacement"]["normalized_pair_geometry"]=="RETRACTED_NOT_ADMISSIBLE"
 i=e["impact"]; assert i["risks_open_or_blocked"]==11 and i["chart"]=="CLOSED"
 assert all(i[k]==0 for k in ("new_independent_sources","algorithm_reopens","matrix_rows_changed","genealogy_nodes_added","genealogy_edges_added","risks_closed"))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13EK SHA-BOUND ORIGINAL P74 D4/D5 CHUDU LONG STRIPS") for x in s["historical_audit"]["current_focus"])
 q=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert q["priority"]=="P0" and q["status"]=="OPEN" and q["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION")
 assert all(x in q["next_action"] for x in ("D4","D5","D30","初度","NULL"))
 assert {E,E.replace(".json",".md")}.issubset(set(q["source_refs"]))
 h=next(x for x in q["history"] if x.get("revision_id")=="TW-OPEN-0005-13EK-ORIGINAL-P74-D4-D5-LONG-LITERALS-20261023")
 assert h["revision_id"]=="TW-OPEN-0005-13EK-ORIGINAL-P74-D4-D5-LONG-LITERALS-20261023"
 assert h["previous_next_action"].startswith("13EJ CURRENT ACTION") and set(h["changed_fields"])=={"source_refs","next_action"}
 assert {E,E.replace(".json",".md"),EJ,EI,ED}.issubset(set(h["evidence_refs"]))
 assert len(l["issues"])==11 and l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
def replay(e,source_dir):
 from PIL import Image
 f=Path(source_dir)/"original-p074.png"
 assert hashlib.sha256(f.read_bytes()).hexdigest()==e["source"]["png_sha256"]
 with Image.open(f) as im:rgb=im.convert("RGB")
 assert list(rgb.size)==e["source"]["size"] and hashlib.sha256(rgb.tobytes()).hexdigest()==e["source"]["rgb_sha256"]
 for r in e["rois"]:
  assert hashlib.sha256(rgb.crop(tuple(r["bbox"])).tobytes()).hexdigest()==r["rgb_sha256"],r["name"]
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--source-dir");a=p.parse_args()
 e=read(E);assert check(e,read(S),read(L),read(EJ),read(EI),read(ED))
 if a.source_dir:assert replay(e,a.source_dir)
 print("13EK_PASS ORIGINAL_P74_D4_D5_FULL_VISIBLE_CHUDU_CHARS_D30_NUMERIC_NULL")
