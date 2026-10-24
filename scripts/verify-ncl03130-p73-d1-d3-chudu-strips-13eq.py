#!/usr/bin/env python3
"""13EQ: source-original NCL03130 p73 D1-D3 narrow vertical glyph strings; no numbers inferred."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13EQ-NCL03130-P73-D1-D3-ORIGINAL-CHUDU-STRIPS-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json";EO="docs/research/TIANWEN-13EO-NCL03130-P73-HEADINGS-P74-DAY-SEQUENCE-R1.json";EP="docs/research/TIANWEN-13EP-NCL03130-P73-SUMMER-RICHA-ORIGINAL-R1.json";EN="docs/research/TIANWEN-13EN-NCL03130-P74-FOURFEN-D4-D6-BOUNDED-PREFIX-R1.json";EI="docs/research/TIANWEN-13EI-NCL03130-D4-MISATTRIBUTED-CHUDU-ROI-ERRATUM-R1.json";ED="docs/research/TIANWEN-13ED-NCL03130-SOLAR-D30-EXTENDED-ORIGINAL-STRIP-R1.json"
EXPECTED=json.loads(r'''[["P73_D1_CHUDU",[274,405,305,745],"f60196b5cc91f86b97fa58025353367ef295c6befe9edbbeff2ffda23a72fd70","初度九十五分一五一六"],["P73_D2_CHUDU",[194,405,224,710],"2c9308d28470e7896bca3d0ade9131df49dd64efa54dfbfd603a8becfcfc51c0","初度九十五一九五九"],["P73_D3_CHUDU",[112,405,144,709],"e6bbfee7dd6e8c3dfbae313e1ff65aea49b90375417c0e373cd4504b3d64d78e","初度九十五二四〇五"],["P73_D1_HEADER_AND_GLYPH_CONTEXT",[239,146,315,768],"2acf88b95f77b6c5bd7994f97eefff6645141a4b536fc42b033a8086335dee7d",null],["P73_D2_HEADER_AND_GLYPH_CONTEXT",[155,146,235,765],"8b70d920ac11eacc4f540a98d3241a84089b30dee0db1cc8089e2f5ebf0c40da",null],["P73_D3_HEADER_AND_GLYPH_CONTEXT",[68,146,151,760],"1a0e86aa08804829cb4d9e2b66e4cea68b2a2a40d30ae8705e875a032579dad1",null],["P73_D1_D3_DATA_CONTEXT",[105,392,310,776],"76dc2c3156e3808f67b9d8183da894531206684649c55e1bbca06a288b52b111",null],["P73_D1_ADJACENT_LANES",[253,405,329,746],"76e95fdb257cc3c56b64465fc3b2823969115fb20afcf8e60dbc877891079d65",null],["P73_D2_ADJACENT_LANES",[173,405,248,737],"021d044a4b39ab80890b5b0f222702a3fd93de868bf8e2d4ac86dfcb4324cde0",null],["P73_D3_ADJACENT_LANES",[92,405,169,736],"50c0dfef19870fc5b3945f8053995a4c62afd155a9fb4d05067c5031d8d307f1",null]]''')
def read(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(e,eo,ep,en,ei,ed,s,l):
 assert e["schema"]=="TIANWEN-13EQ-NCL03130-P73-D1-D3-SOURCE-ORIGINAL-CHUDU-STRIPS-R1" and e["issue_id"]=="TW-OPEN-0005"
 src=e["source"];orig=eo["source"];prior=ep["source"]
 assert src["pdf_sha256"]==orig["original_pdf_sha256"]==prior["original_pdf_sha256"]==en["source"]["pdf_sha256"]
 assert src["png_sha256"]==orig["original_page_73"]["png_sha256"]==prior["png_sha256"]
 assert src["rgb_sha256"]==orig["original_page_73"]["rgb_sha256"]==prior["rgb_sha256"]
 assert src["image_size"]==orig["original_page_73"]["image_size"]==[1305,874]
 assert src["pdf_page"]==73 and src["run"]==orig["original_archive_run"] and src["artifact_id"]==orig["artifact_id"]
 assert src["ocr_used"] is False and src["independent_physical_witnesses_added"]==0
 assert src["physical_copy_identity"]==src["qing_vs_1905_copy_layer"]=="UNBOUND"
 assert len(e["rois"])==10
 assert [[x["name"],x["bbox"],x["rgb_sha256"],x["visible_original"]] for x in e["rois"]]==EXPECTED
 assert [x["day"] for x in e["rois"][:3]]==[1,2,3]
 assert all(r["grade"]==("ORIGINAL_DIRECT_VISIBLE_VERTICAL_GLYPH_STRIP" if i<3 else "SOURCE_RGB_PIXEL_BOUND_CONTEXT_NO_DIGIT_IMPUTATION") for i,r in enumerate(e["rois"]))
 assert all(0<=r["bbox"][0]<r["bbox"][2]<=1305 and 0<=r["bbox"][1]<r["bbox"][3]<=874 for r in e["rois"])
 labels=e["day_label_rois_reused_from_13eo"]
 assert [(x["name"],x["literal"],x["bbox"],x["rgb_sha256"]) for x in labels]==[("D"+str(i),str(["","一日","二日","三日"][i]),eo["rois"][6+i]["bbox"],eo["rois"][6+i]["rgb_sha256"]) for i in (1,2,3)]
 o=e["observations"]
 assert o["source_printed_day_indexes"]==[1,2,3]
 assert o["source_local_chudu_literals"]==[r[3] for r in EXPECTED[:3]]
 assert o["d1_explicit_fen_character_between_wushi_and_suffix"] is True
 assert o["d2_d3_do_not_show_same_explicit_fen_character_in_these_bounded_strips"] is True
 assert o["interpretation_of_d1_fen_as_decimal_position"]=="UNPROVEN"
 assert o["per_day_decimal_values"]==[None,None,None] and o["historical_units"]=="UNBOUND"
 assert o["technical_heading_to_daily_lane_identity"]=="UNPROVEN"
 assert o["same_digitized_original_not_three_independent_witnesses"] is True
 assert o["p74_d4_preexisting_original_literal"]==en["findings"]["chudu_originals"][0]=="初度九十五二八五一"
 assert o["p73_d1_to_p74_d4_numerical_progression"]=="NOT_ADJUDICATED"
 assert o["d4_d5_d6_fourfen_complete_numerics"]==en["findings"]["d4_d5_d6_fourfen_exact_decimals"]==[None,None,None]
 assert o["p76_solar_d30_original"]==ed["finding"]["d30_visible_glyph_group"]=="初度九十六二〇三" and o["p76_solar_d30_numeric"] is None
 assert o["prior_13ei_source_glyph_erratum_still_retracted"] is True and ei["replacement"]["normalized_pair_geometry"]=="RETRACTED_NOT_ADMISSIBLE"
 assert ep["findings"]["p73_richa_vertical_original"]=="日差加一秒六十二少"
 i=e["impact"];assert i["chart_product"]=="CLOSED" and i["open_or_blocked_risks"]==11
 assert all(i[z]==0 for z in ("matrix_rows_changed","registry_sources_added","genealogy_nodes_added","genealogy_edges_added","risks_closed","algorithm_reopens"))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13EQ ") for x in s["historical_audit"]["current_focus"])
 q=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert q["priority"]=="P0" and q["status"]=="OPEN" and q["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert all(x in q["next_action"] for x in ("D1","D2","D3","D4","D5","D6","D30","初度","四分","NULL"))
 assert E in q["source_refs"] and E.replace(".json",".md") in q["source_refs"]
 h=next(x for x in q["history"] if x.get("revision_id")=="TW-OPEN-0005-13EQ-P73-D1-D3-ORIGINAL-STRIPS-20261024")
 assert h["previous_next_action"].startswith("13EP CURRENT ACTION:") and set(h["changed_fields"])=={"source_refs","next_action"} and bool(h["evidence_refs"])
 assert len(l["issues"])==11 and l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
def replay(e,original_png_dir):
 from PIL import Image
 p=Path(original_png_dir)/e["source"]["png_name"]
 assert hashlib.sha256(p.read_bytes()).hexdigest()==e["source"]["png_sha256"],str(p)
 with Image.open(p) as im:rgb=im.convert("RGB")
 assert list(rgb.size)==e["source"]["image_size"] and hashlib.sha256(rgb.tobytes()).hexdigest()==e["source"]["rgb_sha256"]
 for r in e["rois"]:
  assert hashlib.sha256(rgb.crop(tuple(r["bbox"])).tobytes()).hexdigest()==r["rgb_sha256"],r["name"]
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--source-dir");args=p.parse_args()
 e=read(E);assert check(e,read(EO),read(EP),read(EN),read(EI),read(ED),read(S),read(L))
 if args.source_dir:assert replay(e,args.source_dir)
 print("13EQ_PASS ORIGINAL_P73_D1_D3_GLYPHS_SHA_BOUND_NO_NUMERICAL_IMPUTATION")
