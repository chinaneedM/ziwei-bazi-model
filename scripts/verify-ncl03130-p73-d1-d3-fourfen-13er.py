#!/usr/bin/env python3
"""13ER NCL source-local D1-D3 四分 visible glyph strips, no numerical filling."""
import argparse,hashlib,json
from pathlib import Path
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13ER-NCL03130-P73-D1-D3-FOURFEN-BOUNDED-ORIGINAL-R1.json";EQ="docs/research/TIANWEN-13EQ-NCL03130-P73-D1-D3-ORIGINAL-CHUDU-STRIPS-R1.json";EN="docs/research/TIANWEN-13EN-NCL03130-P74-FOURFEN-D4-D6-BOUNDED-PREFIX-R1.json";EI="docs/research/TIANWEN-13EI-NCL03130-D4-MISATTRIBUTED-CHUDU-ROI-ERRATUM-R1.json";ED="docs/research/TIANWEN-13ED-NCL03130-SOLAR-D30-EXTENDED-ORIGINAL-STRIP-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
EXPECTED=json.loads(r'''[["P73_D1_FOURFEN",[260,397,287,751],"b4fdeaf077058f3df3f569d24094341e56e9bd19b9cbf0a4ae4827f64d8b8fa0","四分四五二四"],["P73_D2_FOURFEN",[176,397,204,749],"0a4706467ded140d6ca6556a3c31a58cd0e3a0c102e6ab0cb07d611449639ce2","四分四六八六"],["P73_D3_FOURFEN",[91,397,118,750],"497e577fb35abd11aa33b9fb9a0c9d49459861d2e0bc8a4b58383edbf64101a9","四分四八四八"],["P73_D1_CONTEXT",[220,385,312,789],"a585842c97ba86d2d63502c3df5ced99beba366971b68a043460dbbfca38dee4",null],["P73_D2_CONTEXT",[137,385,235,789],"a340f599ca8a18d89f5d51e57e732c5f89e956f80e4f543eea6a34524edc19e4",null],["P73_D3_CONTEXT",[52,385,155,789],"038ce11f328df442b8cbd9aceca7edc73f86817cabb72ea9540c94c80a2e6123",null],["P73_D1_LEFT_NEIGHBORS",[215,397,260,750],"8ca7e1d3fd074ff4cc95132c32d65c6797980abe57a5bc3e5c950ad32123b48f",null],["P73_D2_LEFT_NEIGHBORS",[129,397,177,750],"a23099fe34a5063d102727acce0bc6674b06b3ae1c9c16d558c1d11f73f70258",null],["P73_D3_LEFT_NEIGHBORS",[45,397,91,750],"fa1975ccaa67a68831287d0b93b6bf75ce6f9d55fb47ef7c684c9bf0c0c4b304",null]]''')
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(e,eq,en,ei,ed,s,l):
 assert e["schema"]=="TIANWEN-13ER-NCL03130-P73-D1-D3-FOURFEN-BOUNDED-ORIGINAL-R1" and e["issue_id"]=="TW-OPEN-0005"
 src=e["source"];orig=eq["source"]
 assert src["pdf_sha256"]==orig["pdf_sha256"]==en["source"]["pdf_sha256"]
 assert src["png_sha256"]==orig["png_sha256"] and src["rgb_sha256"]==orig["rgb_sha256"]
 assert src["pdf_page"]==73 and src["image_size"]==[1305,874]==orig["image_size"]
 assert src["run"]==orig["run"] and src["artifact_id"]==orig["artifact_id"]
 assert src["ocr_used"] is False and src["new_independent_physical_witnesses"]==0
 assert src["source_physical_copy_identity"]==src["qing_vs_1905_copy_layer"]=="UNBOUND"
 assert len(e["rois"])==len(EXPECTED)==9
 assert [[r["name"],r["bbox"],r["rgb_sha256"],r["visible_original"]] for r in e["rois"]]==EXPECTED
 assert [r["day"] for r in e["rois"][:3]]==[1,2,3]
 assert all(r["grade"]==("DIRECT_ORIGINAL_VISIBLE_LOCAL_VERTICAL_STRIP_BOUNDED" if i<3 else "ORIGINAL_PIXEL_CONTEXT_NO_LITERAL_INFERENCE") for i,r in enumerate(e["rois"]))
 assert all(0<=r["bbox"][0]<r["bbox"][2]<=1305 and 0<=r["bbox"][1]<r["bbox"][3]<=874 for r in e["rois"])
 f=e["findings"]
 assert f["days"]==[1,2,3] and f["source_original_fourfen_bounded_visible_strips"]==[r[3] for r in EXPECTED[:3]]
 assert f["complete_original_fourfen_field_proven"]==[False]*3
 assert f["numeric_fourfen_values"]==[None]*3 and f["possible_lower_tail_or_row_length"]=="NOT_ADJUDICATED"
 assert f["p73_chudu_originals"]==eq["observations"]["source_local_chudu_literals"]
 assert f["p74_fourfen_prefixes_preexisting"]==[en["findings"][k] for k in ("fourfen_d4_clear_prefix","fourfen_d5_clear_prefix","fourfen_d6_clear_prefix")]
 assert f["p73_field_title_to_numeric_lane"]=="UNPROVEN" and f["explicit_original_d1_fen_unit_role"]=="UNBOUND"
 assert f["p76_solar_day30_visible"]==ed["finding"]["d30_visible_glyph_group"]=="初度九十六二〇三"
 assert f["p76_solar_day30_decimal"] is None
 assert f["prior_13ei_chudu_roi_misreading_retracted"] is True and ei["replacement"]["normalized_pair_geometry"]=="RETRACTED_NOT_ADMISSIBLE"
 assert f["independent_source_witnesses_added"]==0
 i=e["impact"];assert i["chart_product"]=="CLOSED" and i["open_or_blocked_risks"]==11
 assert all(i[z]==0 for z in ("matrix_rows_changed","registry_sources_added","genealogy_nodes_added","genealogy_edges_added","risks_closed","algorithm_reopens"))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(z.startswith("13ER ") for z in s["historical_audit"]["current_focus"])
 q=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert q["priority"]=="P0" and q["status"]=="OPEN" and historical_action_view(q).startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert all(z in historical_action_view(q) for z in ("D1","D2","D3","D4","D5","D6","D30","四分","初度","NULL"))
 assert {E,E.replace(".json",".md")}.issubset(set(q["source_refs"]))
 h=next(z for z in q["history"] if z.get("revision_id")=="TW-OPEN-0005-13ER-P73-D1-D3-FOURFEN-SOURCE-20261024")
 assert h["previous_next_action"].startswith("13EQ CURRENT ACTION:") and set(h["changed_fields"])=={"source_refs","next_action"}
 assert len(l["issues"])==11 and l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
def replay(e,source_dir):
 from PIL import Image
 f=Path(source_dir)/e["source"]["png_name"]
 assert hashlib.sha256(f.read_bytes()).hexdigest()==e["source"]["png_sha256"]
 with Image.open(f) as im:rgb=im.convert("RGB")
 assert list(rgb.size)==e["source"]["image_size"] and hashlib.sha256(rgb.tobytes()).hexdigest()==e["source"]["rgb_sha256"]
 for r in e["rois"]:
  assert hashlib.sha256(rgb.crop(tuple(r["bbox"])).tobytes()).hexdigest()==r["rgb_sha256"],r["name"]
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--source-dir");a=p.parse_args()
 e=read(E);assert check(e,read(EQ),read(EN),read(EI),read(ED),read(S),read(L))
 if a.source_dir:assert replay(e,a.source_dir)
 print("13ER_PASS ORIGINAL_D1_D3_FOURFEN_BOUNDED_NO_DECIMAL_OR_WITNESS_INFLATION")
