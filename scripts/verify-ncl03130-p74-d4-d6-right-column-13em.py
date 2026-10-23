#!/usr/bin/env python3
"""13EM source-original right-neighbor glyph-only positive: no numeric assignment."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13EM-NCL03130-P74-D4-D6-RIGHT-NEIGHBOR-LONG-STRIPS-R1.json"
EL="docs/research/TIANWEN-13EL-NCL03130-P74-D6-CHUDU-LONG-AND-D4-D6-CONTROLS-R1.json"
EK="docs/research/TIANWEN-13EK-NCL03130-P74-D4-D5-CHUDU-LONG-STRIPS-R1.json"
EI="docs/research/TIANWEN-13EI-NCL03130-D4-MISATTRIBUTED-CHUDU-ROI-ERRATUM-R1.json"
ED="docs/research/TIANWEN-13ED-NCL03130-SOLAR-D30-EXTENDED-ORIGINAL-STRIP-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
EXPECTED=json.loads(r'''[["D4_RIGHT_FULL",[974,405,1002,815],"41232f81b4144b32ae41fb0ea92bd09cb281dfa74b7ab4b866ebbc10601c0ef4","一千四百四十一二二七一"],["D5_RIGHT_FULL",[879,405,909,815],"f0074f8777cf218a6c480af88f2ea59275707288e0e0c869f82b1bc180f11ca3","一千九百一十二七〇七二"],["D6_RIGHT_FULL",[785,405,819,815],"ace3950cfc60b0624009a49c18be48423976d1ec22b9ef3f3d685272e481213b","一千三百七十九七一二五"],["D4_RIGHT_NARROW",[977,415,996,803],"1bfe8c6fce65fd1cec4ef75269200c759db32bb46180f4e28b6b11433819e409",null],["D5_RIGHT_NARROW",[882,415,903,803],"dd21f90009c57d24517140e1066e24bf7d4d6ea3b8d3906b826e9df5a5949c69",null],["D6_RIGHT_NARROW",[789,415,814,803],"b54a935d7b2502cef333cb06f7fa056d785df004e25a422bcf372007ba89891f",null],["D4_RIGHT_TAIL",[977,763,996,830],"f288044c42c9e7dde640b1d6627cb22710658f557974dab35c8c11564c3c7b21",null],["D5_RIGHT_TAIL",[882,763,903,830],"be470b6ff450a1e6eea5d5f136e808e5160a7d0f44c6aadfb628074bd738c59f",null],["D6_RIGHT_TAIL",[789,763,814,830],"820be14fda21992e1146e489c173a3db4fd5b5d0caf25ce948624772a479d9de",null],["D4_THREE_LANE_CONTEXT",[915,397,1006,815],"3b643e6e613e6ee36d387dcf914ec7aa5d60b2f5bef1af8b13aebc1b56c8e12e",null],["D5_THREE_LANE_CONTEXT",[823,397,911,815],"0bf4b930e96ccbe67efaad282a231829ee90961c9251b1745a0506468b7fc39e",null],["D6_THREE_LANE_CONTEXT",[731,397,819,815],"9f12a3e713639f773653953ac4ab4dbafad787d6b5e17fb726b88805cace65fd",null],["D4_CHUDU_SOURCE_CONTROL",[943,411,970,771],"a82d6f37825b16f1c1250604f8021cbf165b2ce26d0913928a19be720eb0375c","初度九十五二八五一"],["D5_CHUDU_SOURCE_CONTROL",[849,411,876,771],"3005a769650dbb37c5213ab977a1f196b88c9a2bca6f02e0d7e75b1747e2dc79","初度九十五三三〇〇"],["D6_CHUDU_SOURCE_CONTROL",[759,411,785,771],"0867d3c79f288e3b83c6d3cf682628b0be4f3ddac6d0d4102cfddae6e9dd66f9","初度九十五三七五〇"],["D6_PRINTED_DAY_TITLE",[704,150,792,300],"149d70bd1d383d5396258a3af68f2c9c1758f5c6a45579abeee3e5cd4c5b6b4b","六日"]]''')
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(e,el,ek,ei,ed,state,ledger):
 assert e["schema"]=="TIANWEN-13EM-NCL03130-P74-D4-D6-RIGHT-NEIGHBOR-LONG-STRIPS-R1" and e["issue_id"]=="TW-OPEN-0005"
 s=e["source"]
 assert s["pdf_sha256"]==el["source"]["pdf_sha256"]==ek["source"]["pdf_sha256"]==ei["source"]["pdf_sha256"]==ed["source"]["pdf_sha256"]
 assert s["original_pdf_page"]==el["source"]["pdf_page"]==74 and s["png_sha256"]==el["source"]["png_sha256"] and s["rgb_sha256"]==el["source"]["rgb_sha256"] and s["size"]==el["source"]["image_size"]==[1305,873]
 assert s["archived_run"]==el["source"]["archive_run_id"] and s["artifact_id"]==el["source"]["artifact_id"]
 assert s["physical_copy"]==s["qing_vs_1905_layer"]=="UNBOUND" and s["ocr_used"] is False and s["independent_witnesses_added"]==0
 assert len(e["rois"])==len(EXPECTED)==16
 assert [[z["name"],z["bbox"],z["rgb_sha256"],z["visible_literal"]] for z in e["rois"]]==EXPECTED
 assert all(z["grade"]=="ORIGINAL_IMAGE_SOURCE_LOCAL_RGB_SHA_AND_BOUNDED_HUMAN_GLYPH_READ" for z in e["rois"])
 assert all(0<=z["bbox"][0]<z["bbox"][2]<=1305 and 0<=z["bbox"][1]<z["bbox"][3]<=873 for z in e["rois"])
 f=e["findings"]
 assert f["source_day_labels"]==["四日","五日","六日"]
 assert f["right_neighbor_visible_strings"]==[z["visible_literal"] for z in e["rois"][:3]]==["一千四百四十一二二七一","一千九百一十二七〇七二","一千三百七十九七一二五"]
 assert f["right_neighbor_visible_lengths"]==list(map(len,f["right_neighbor_visible_strings"]))==[11,11,11]
 assert f["source_original_chudu_control_strings"]==[z["visible_literal"] for z in e["rois"][12:15]]==[ek["findings"]["D4_visible_string"],ek["findings"]["D5_visible_string"],el["findings"]["d6_visible"]]
 assert [z["rgb_sha256"] for z in e["rois"][12:15]]==[ek["rois"][0]["rgb_sha256"],ek["rois"][1]["rgb_sha256"],el["rois"][1]["rgb_sha256"]]
 assert e["rois"][15]["rgb_sha256"]==el["rois"][0]["rgb_sha256"] and e["rois"][15]["visible_literal"]=="六日"
 assert f["prior_13el_d6_right_unread_record_preserved"] and el["findings"]["d6_right_full_text"]=="UNREAD"
 assert f["prior_13ei_false_13eh_chudu_binding_retracted"] and ei["replacement"]["normalized_pair_geometry"]=="RETRACTED_NOT_ADMISSIBLE"
 assert f["p73_technical_header_to_right_neighbor_field"]==f["right_neighbor_arithmetic_field_or_units"]=="UNPROVEN"
 assert all(f[z] is None for z in ("right_neighbor_exact_numeric_d4","right_neighbor_exact_numeric_d5","right_neighbor_exact_numeric_d6","day30_historical_decimal"))
 assert f["day30_source_literal"]==ed["finding"]["d30_visible_glyph_group"]=="初度九十六二〇三" and f["day30_missing_digit_inference"]=="FORBIDDEN"
 assert f["same_page_right_neighbor_and_chudu_concatenation"] is False and f["source_image_witnesses_added"]==0 and f["d4_d5_d6_same_digital_page"] is True
 assert f["transmission_independence"]=="UNBOUND" and f["source_original_right_neighbor_full_strip_bounded_negative_outside"]=="NOT_ASSERTED"
 impact=e["impact"];assert impact["issues_open_or_blocked"]==11 and impact["product"]=="CLOSED"
 assert all(impact[k]==0 for k in ("matrix_rows_changed","source_registry_entries_added","genealogy_nodes_added","genealogy_edges_added","algorithm_reopens","issues_closed"))
 assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
 assert any(z.startswith("13EM DIRECT SOURCE-ORIGINAL") for z in state["historical_audit"]["current_focus"])
 assert ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 q=next(z for z in ledger["issues"] if z["id"]=="TW-OPEN-0005")
 assert q["priority"]=="P0" and q["status"]=="OPEN" and q["next_action"].startswith(ledger["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION")
 assert {E,E.replace(".json",".md")}.issubset(set(q["source_refs"]))
 h=next(z for z in q["history"] if z.get("revision_id")=="TW-OPEN-0005-13EM-P74-THREE-RIGHT-STRIPS-20261024")
 assert h["previous_next_action"].startswith("13EL CURRENT ACTION") and set(h["changed_fields"])=={"source_refs","next_action"}
 assert len(ledger["issues"])==11 and ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
 return True
def replay(e,source_dir):
 from PIL import Image
 p=Path(source_dir)/"original-p074.png"
 assert hashlib.sha256(p.read_bytes()).hexdigest()==e["source"]["png_sha256"]
 with Image.open(p) as im:rgb=im.convert("RGB")
 assert list(rgb.size)==e["source"]["size"] and hashlib.sha256(rgb.tobytes()).hexdigest()==e["source"]["rgb_sha256"]
 for z in e["rois"]:
  assert hashlib.sha256(rgb.crop(tuple(z["bbox"])).tobytes()).hexdigest()==z["rgb_sha256"],z["name"]
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--source-dir");a=p.parse_args()
 e=read(E);assert check(e,read(EL),read(EK),read(EI),read(ED),read(S),read(L))
 if a.source_dir:assert replay(e,a.source_dir)
 print("13EM_PASS SOURCE_ORIGINAL_P74_D4_D6_RIGHT_GLYPHS_NUMERIC_UNBOUND")
