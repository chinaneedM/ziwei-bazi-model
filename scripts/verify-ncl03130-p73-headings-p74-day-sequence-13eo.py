#!/usr/bin/env python3
"""13EO: p73 four original heading glyphs, day labels, and bounded p74 day sequence."""
import argparse,hashlib,json
from pathlib import Path
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13EO-NCL03130-P73-HEADINGS-P74-DAY-SEQUENCE-R1.json"
EN="docs/research/TIANWEN-13EN-NCL03130-P74-FOURFEN-D4-D6-BOUNDED-PREFIX-R1.json"
EI="docs/research/TIANWEN-13EI-NCL03130-D4-MISATTRIBUTED-CHUDU-ROI-ERRATUM-R1.json"
ED="docs/research/TIANWEN-13ED-NCL03130-SOLAR-D30-EXTENDED-ORIGINAL-STRIP-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
EXPECTED=json.loads(r'''[["P73_XING_DU",[370,415,393,480],"21eaec3997e354203fe0918fc119632d594671beb17eaf7923123a48f3f404ed","行度"],["P73_YING_SUO_JI",[392,413,414,509],"487ca3a0f226ad2dd8671e90280b1f076565e4ab2e0979e450a45663379319de","盈縮積"],["P73_YING_SUO_JIA_FEN",[414,413,435,529],"d6f74b544203b176b9048b5430fcd0a8a910a3e1b1d89bf40fab1c6ddd2bc882","盈縮加分"],["P73_RI_CHA",[434,410,456,485],"21f7dcb1c2b50a69986a839f3c5d401eae59d7dc569962bbfaac99dce5b049d2","日差"],["P73_HEADER_PANEL",[363,406,461,540],"c51ab3766b87c57239fa86047ef4b79c8f8b5810fcfaa7008341b7492a8171c6",null],["P73_HEADER_CONTEXT",[330,399,504,590],"d58c5bd1e955937d0bcb321e1e728cb8f42cc72822bb6fdb96a3a7f69d66873b",null],["P73_INIT_DAY",[333,159,364,241],"36b710ba956d74c4cb830a3722080d1e6e8b0013b0ab42f2508f9df242924adf","初日"],["P73_DAY1",[235,159,285,245],"3cb6dabd803543286a118761d433e3e424b242352b7e5b7c59f14b0611646d66","一日"],["P73_DAY2",[153,159,200,245],"e6da3d2050b99c3ec9c8caabdd920526d95399fb909964aff1403c793f7911e7","二日"],["P73_DAY3",[69,159,120,245],"c7f2c48435584a607800abb23e551d9c9abb0cfa55d500d2e840dbb2ff0c33a5","三日"],["P73_DAY_HEADER_GROUP",[61,151,368,249],"45c1b109be7020740162cc241e16f578833e87ae4ccb66f9a0754e9b9f2c85f7",null],["P73_TITLE_REGION",[460,160,502,430],"49338de643ffa831cf9e221783f3b3877e2a7baee999bf6e84e504424d7071b8",null],["P73_FULL_PAGE",[0,0,1305,874],"9bda3eb23094c0f7ad5c4637329c0bccaa73d55d08e84a69c968ce7e0cf094c3",null],["P73_INITIAL_DATA_CONTEXT",[300,390,504,758],"b14e841c9552a34094288dde30e37b9d1526ea8f14457293922802236d9d5a3c",null]]''')
def read(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(e,en,ei,ed,s,l):
 assert e["schema"]=="TIANWEN-13EO-NCL03130-P73-HEADINGS-P74-DAY-SEQUENCE-R1" and e["issue_id"]=="TW-OPEN-0005"
 src=e["source"];p73=src["original_page_73"];p74=src["original_page_74"]
 assert src["original_pdf_sha256"]==en["source"]["pdf_sha256"]==ed["source"]["pdf_sha256"]
 assert src["original_archive_run"]==en["source"]["original_archive_run"] and src["artifact_id"]==en["source"]["artifact_id"]
 assert p73["pdf_page"]==73 and p73["png_sha256"]=="e4597c62fa1cd49eebc3372fcc30e8be273485736a2f7d2a903061f22ca47f52"
 assert p73["rgb_sha256"]=="9bda3eb23094c0f7ad5c4637329c0bccaa73d55d08e84a69c968ce7e0cf094c3" and p73["image_size"]==[1305,874]
 assert p74["pdf_page"]==74 and p74["png_sha256"]==en["source"]["png_sha256"] and p74["rgb_sha256"]==en["source"]["rgb_sha256"] and p74["image_size"]==en["source"]["image_size"]==[1305,873]
 assert src["ocr_used"] is False and src["physical_copy_identity"]==src["qing_vs_1905_copy_layer"]=="UNBOUND" and src["independent_witnesses_added"]==0
 assert [[r["name"],r["bbox"],r["rgb_sha256"],r["visible_literal"]] for r in e["rois"]]==EXPECTED and len(e["rois"])==14
 assert all(r["grade"]==("SOURCE_NATIVE_DIRECT_GLYPH_BOUNDED" if r["visible_literal"] else "SOURCE_NATIVE_PIXEL_CONTEXT_NO_TEXT_IMPUTATION") for r in e["rois"])
 assert all(0<=r["bbox"][0]<r["bbox"][2]<=1305 and 0<=r["bbox"][1]<r["bbox"][3]<=874 for r in e["rois"])
 assert e["rois"][12]["rgb_sha256"]==p73["rgb_sha256"] and e["rois"][12]["bbox"]==[0,0,1305,874]
 f=e["findings"]
 assert f["p73_original_vertical_technical_headers"]==[r["visible_literal"] for r in e["rois"][:4]]==["行度","盈縮積","盈縮加分","日差"]
 assert f["p73_original_printed_day_labels"]==[r["visible_literal"] for r in e["rois"][6:10]]==["初日","一日","二日","三日"]
 assert f["p74_original_printed_day_labels"]==[r["visible_prefix"] for r in en["rois"][15:18]]==["四日","五日","六日"]
 assert f["p73_to_p74_digital_page_day_index_continuity"] is True and f["one_original_digital_scan_not_independent_witnesses"] is True and f["number_of_independent_new_early_copies"]==0
 assert all(f[z]=="UNPROVEN" for z in ("p73_header_to_p74_d4_d5_d6_chudu","p73_header_to_p74_d4_d5_d6_fourfen","p73_header_to_p74_d4_d5_d6_right_neighbor","historical_arithmetic_mapping"))
 assert f["p73_technical_header_value_units"]=="UNBOUND" and f["title_entire_vertical_text"]=="UNREAD_NO_TITLE_CONJECTURE"
 assert f["source_original_d4_d5_d6_fourfen_complete_lanes"]==[False,False,False]
 assert f["source_original_d4_d5_d6_fourfen_prefixes"]==[en["findings"][z] for z in ("fourfen_d4_clear_prefix","fourfen_d5_clear_prefix","fourfen_d6_clear_prefix")]
 assert f["d30_original_visible"]==ed["finding"]["d30_visible_glyph_group"]=="初度九十六二〇三" and f["d30_decimal"] is None
 assert f["prior_13ei_false_13eh_chudu_attribution_still_retracted"] is True and ei["replacement"]["normalized_pair_geometry"]=="RETRACTED_NOT_ADMISSIBLE"
 i=e["impact"];assert i["chart_product"]=="CLOSED" and i["open_or_blocked_risks"]==11
 assert all(i[z]==0 for z in ("matrix_rows_changed","registry_sources_added","genealogy_nodes_added","genealogy_edges_added","algorithm_reopens","risks_closed"))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert any(z.startswith("13EO P73 SOURCE ORIGINAL") for z in s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 q=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert q["priority"]=="P0" and q["status"]=="OPEN" and historical_action_view(q).startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION")
 assert {E,E.replace(".json",".md")}.issubset(set(q["source_refs"]))
 h=next(z for z in q["history"] if z.get("revision_id")=="TW-OPEN-0005-13EO-P73-HEADINGS-DAY-CONTINUITY-20261024")
 assert h["previous_next_action"].startswith("13EN CURRENT ACTION") and set(h["changed_fields"])=={"source_refs","next_action"}
 assert len(l["issues"])==11 and l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
def replay(e,source_dir):
 from PIL import Image
 p=Path(source_dir)
 for src in (e["source"]["original_page_73"],e["source"]["original_page_74"]):
  f=p/src["png_name"]
  assert hashlib.sha256(f.read_bytes()).hexdigest()==src["png_sha256"],str(f)
  with Image.open(f) as im:rgb=im.convert("RGB")
  assert list(rgb.size)==src["image_size"] and hashlib.sha256(rgb.tobytes()).hexdigest()==src["rgb_sha256"]
  if src["pdf_page"]==73:
   for r in e["rois"]:
    assert hashlib.sha256(rgb.crop(tuple(r["bbox"])).tobytes()).hexdigest()==r["rgb_sha256"],r["name"]
 return True
if __name__=="__main__":
 parser=argparse.ArgumentParser();parser.add_argument("--source-dir");args=parser.parse_args()
 e=read(E);assert check(e,read(EN),read(EI),read(ED),read(S),read(L))
 if args.source_dir:assert replay(e,args.source_dir)
 print("13EO_PASS P73_HEADER_GLYPHS_P74_DAY_SEQUENTIAL_NO_FIELD_IMPUTATION")
