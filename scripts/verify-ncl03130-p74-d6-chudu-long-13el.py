#!/usr/bin/env python3
"""13EL NCL03130 original p74 D6 positive glyph and D4-D6 source scope gate."""
import argparse, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13EL-NCL03130-P74-D6-CHUDU-LONG-AND-D4-D6-CONTROLS-R1.json"; EK="docs/research/TIANWEN-13EK-NCL03130-P74-D4-D5-CHUDU-LONG-STRIPS-R1.json"; EI="docs/research/TIANWEN-13EI-NCL03130-D4-MISATTRIBUTED-CHUDU-ROI-ERRATUM-R1.json"; ED="docs/research/TIANWEN-13ED-NCL03130-SOLAR-D30-EXTENDED-ORIGINAL-STRIP-R1.json"; S="docs/PROJECT-CURRENT-STATE-R1.json"; L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
EXPECTED=json.loads(r'''[["D6_HEADING",[704,150,792,300],"149d70bd1d383d5396258a3af68f2c9c1758f5c6a45579abeee3e5cd4c5b6b4b","六日"],["D6_CHUDU_LONG",[759,411,785,771],"0867d3c79f288e3b83c6d3cf682628b0be4f3ddac6d0d4102cfddae6e9dd66f9","初度九十五三七五〇"],["D6_LOWER_TAIL",[759,771,785,830],"6211c50c19b6fb5ef4c9a5609735a4d00cc330506290703ee6acd03aa3772e04",null],["D6_EXTENDED",[759,405,785,830],"bb1fda39684a4aa04fc0ad84c5608d6d0518b75646488c131768ac5e66092fd3",null],["D6_FOURFEN_NEIGHBOR",[734,411,763,771],"577bee294bee7e1e0454e0f234f79cd65ad230edaed1932c8e606d8acdfceaf4",null],["D6_RIGHT_NEIGHBOR",[785,411,815,771],"750b9f720fc27f707ea1007d9a1e13baafb92cae6c941aedbee0516d940d7a78",null],["D6_CONTEXT_PANEL",[705,395,824,830],"a1d8cdd1e7e2edaa0a2f7d610a50ef47a93b28db9c737f92b227d572072e8baa",null],["D4_CHUDU_CONTROL",[943,411,970,771],"a82d6f37825b16f1c1250604f8021cbf165b2ce26d0913928a19be720eb0375c","初度九十五二八五一"],["D5_CHUDU_CONTROL",[849,411,876,771],"3005a769650dbb37c5213ab977a1f196b88c9a2bca6f02e0d7e75b1747e2dc79","初度九十五三三〇〇"]]''')
def read(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(e,ek,ei,ed,s,l):
 assert e["schema"]=="TIANWEN-13EL-NCL03130-P74-D6-CHUDU-LONG-AND-D4-D6-CONTROLS-R1" and e["issue_id"]=="TW-OPEN-0005"
 src=e["source"]; src0=ek["source"]
 assert src["pdf_sha256"]==src0["pdf_sha256"]==ed["source"]["pdf_sha256"]==ei["source"]["pdf_sha256"]
 assert src["pdf_page"]==src0["pdf_page"]==74 and src["png_sha256"]==src0["png_sha256"] and src["rgb_sha256"]==src0["rgb_sha256"] and src["image_size"]==src0["size"]==[1305,873]
 assert src["archive_run_id"]==src0["original_archive_run"] and src["artifact_id"]==src0["artifact_id"]
 assert src["ocr_used"] is False and src["physical_copy"]==src["qing_vs_1905_stratum"]=="UNBOUND" and src["independent_witnesses_added"]==0
 assert [[r["name"],r["bbox"],r["rgb_sha256"],r["visible_literal"]] for r in e["rois"]]==EXPECTED
 assert len(e["rois"])==9 and all(x["grade"]=="SOURCE_ORIGINAL_RGBA_FREE_RGB_SHA_AND_DIRECT_HUMAN_BOUNDED_GLYPH" for x in e["rois"])
 assert all(0<=b["bbox"][0]<b["bbox"][2]<=1305 and 0<=b["bbox"][1]<b["bbox"][3]<=873 for b in e["rois"])
 assert e["rois"][-2]["rgb_sha256"]==ek["rois"][0]["rgb_sha256"] and e["rois"][-1]["rgb_sha256"]==ek["rois"][1]["rgb_sha256"]
 f=e["findings"]; assert f["source_printed_day_6"]=="六日" and e["rois"][0]["visible_literal"]=="六日"
 assert f["d4_visible"]==ek["findings"]["D4_visible_string"]==e["rois"][7]["visible_literal"]
 assert f["d5_visible"]==ek["findings"]["D5_visible_string"]==e["rois"][8]["visible_literal"]
 assert f["d6_visible"]==e["rois"][1]["visible_literal"]=="初度九十五三七五〇"
 assert f["d4_d5_d6_visible_lengths"]==list(map(len,(f["d4_visible"],f["d5_visible"],f["d6_visible"])))==[9,9,9]
 assert f["d30_preserved"]==ed["finding"]["d30_visible_glyph_group"]=="初度九十六二〇三" and f["d30_visible_length"]==8
 assert all(f[k] is None for k in ("original_full_decimal_d4","original_full_decimal_d5","original_full_decimal_d6","original_full_decimal_d30"))
 assert f["d6_fourfen_full_text"]==f["d6_right_full_text"]=="UNREAD" and f["p73_heading_to_daily_lanes"]=="UNPROVEN" and f["same_copy_d30_missing_digit"]=="UNPROVEN"
 assert f["prior_13eh_erratum_preserved"] is True and f["one_source_three_day_readings_not_three_witnesses"] is True and f["number_of_new_independent_early_copies"]==0
 assert ei["replacement"]["normalized_pair_geometry"]=="RETRACTED_NOT_ADMISSIBLE"
 i=e["impact"];assert i["product"]=="CLOSED" and i["risks_open_or_blocked"]==11
 assert all(i[k]==0 for k in ("matrix_rows_changed","source_registry_entries_added","genealogy_nodes_added","genealogy_edges_added","algorithm_reopens","risks_closed"))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert s["historical_audit"]["current_focus"][-1].startswith("13EL ")
 assert l["binding"]["latest_research_focus_prefix"]=="13EL"
 q=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert q["priority"]=="P0" and q["status"]=="OPEN" and q["next_action"].startswith("13EL CURRENT ACTION")
 assert all(z in q["next_action"] for z in ("D4","D5","D6","D30","初度","NULL"))
 assert {E,E.replace(".json",".md")}.issubset(set(q["source_refs"]))
 assert q["history"][-1]["revision_id"]=="TW-OPEN-0005-13EL-P74-D6-SOURCE-ORIGINAL-20261024"
 assert q["history"][-1]["previous_next_action"].startswith("13EK CURRENT ACTION")
 assert len(l["issues"])==11 and l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
def replay(e,source_dir):
 from PIL import Image
 f=Path(source_dir)/"original-p074.png"
 assert hashlib.sha256(f.read_bytes()).hexdigest()==e["source"]["png_sha256"]
 with Image.open(f) as im: rgb=im.convert("RGB")
 assert list(rgb.size)==e["source"]["image_size"] and hashlib.sha256(rgb.tobytes()).hexdigest()==e["source"]["rgb_sha256"]
 for r in e["rois"]:
  assert hashlib.sha256(rgb.crop(tuple(r["bbox"])).tobytes()).hexdigest()==r["rgb_sha256"],r["name"]
 return True
if __name__=="__main__":
 parser=argparse.ArgumentParser();parser.add_argument("--source-dir");args=parser.parse_args()
 e=read(E);assert check(e,read(EK),read(EI),read(ED),read(S),read(L))
 if args.source_dir:assert replay(e,args.source_dir)
 print("13EL_PASS D6_ORIGINAL_GLYPHS_REPLAY_SCOPE_NO_DECIMAL_IMPUTATION")
