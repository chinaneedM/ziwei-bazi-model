#!/usr/bin/env python3
"""13EP original-image summer 日差 phrase scope, exact source and forward-only handoff gate."""
import argparse, hashlib, json
from pathlib import Path
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13EP-NCL03130-P73-SUMMER-RICHA-ORIGINAL-R1.json"
EO="docs/research/TIANWEN-13EO-NCL03130-P73-HEADINGS-P74-DAY-SEQUENCE-R1.json"
EN="docs/research/TIANWEN-13EN-NCL03130-P74-FOURFEN-D4-D6-BOUNDED-PREFIX-R1.json"
EI="docs/research/TIANWEN-13EI-NCL03130-D4-MISATTRIBUTED-CHUDU-ROI-ERRATUM-R1.json"
ED="docs/research/TIANWEN-13ED-NCL03130-SOLAR-D30-EXTENDED-ORIGINAL-STRIP-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
SHA=["61e32898b52c70af94d9eef1bbb7059f7d36490c3d229e5f70a3291cb222084c",
"67d38e905ce96e520dec358b7d887930fc27a0cfc3adc254ceae24f36fa6e8c2",
"7c54ed977cc8e2a369609dc36ca42e15d0f4d96055e868add321161d384e69c0",
"12fca90661948736e35031bfc2a6b4a8ffb38351a1cae526407a1cd777b8737c",
"2b0ca713947825ad6f663e2d267f04bdee39087d9593dd9a46d1b5873981dc0d",
"d5a9af24a4619be568dd09b2b31ab93cbcec938fa4ac5b204800a92b9ac4d5f4"]
BBOX=[[433,408,457,737],[435,413,456,731],[435,480,457,737],
[431,402,462,754],[363,401,503,790],[333,405,459,744]]
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(e,eo,en,ei,ed,s,l):
 assert e["schema"]=="TIANWEN-13EP-NCL03130-P73-SUMMER-RICHA-DIRECT-ORIGINAL-R1" and e["issue_id"]=="TW-OPEN-0005"
 a=e["source"];b=eo["source"]
 assert a["original_pdf_sha256"]==b["original_pdf_sha256"]==en["source"]["pdf_sha256"]
 assert a["artifact_id"]==b["artifact_id"] and a["original_archive_run"]==b["original_archive_run"]
 assert a["page"]==73 and a["png_sha256"]==b["original_page_73"]["png_sha256"]
 assert a["rgb_sha256"]==b["original_page_73"]["rgb_sha256"]
 assert a["image_size"]==[1305,874] and a["ocr_used"] is False
 assert a["physical_copy_identity"]==a["qing_vs_1905_source_leaf"]=="UNBOUND"
 assert a["new_independent_physical_witnesses"]==0
 rois=e["rois"]
 assert len(rois)==6 and [r["bbox"] for r in rois]==BBOX
 assert [r["rgb_sha256"] for r in rois]==SHA
 assert [r["visible_literal"] for r in rois]==["日差加一秒六十二少","日差加一秒六十二少","加一秒六十二少",None,None,None]
 assert all(0<=x0<x1<=1305 and 0<=y0<y1<=874 for x0,y0,x1,y1 in [(*r["bbox"][:1],r["bbox"][1],r["bbox"][2],r["bbox"][3]) for r in rois])
 f=e["findings"]
 assert f["p73_richa_vertical_original"]=="日差加一秒六十二少" and f["p73_richa_suffix_original"]=="加一秒六十二少"
 assert f["independent_source_original_p73_header"]==eo["findings"]["p73_original_vertical_technical_headers"][-1]=="日差"
 assert f["comparison_from_existing_13CV_winter_received_record"]=="日差加一秒八十六少"
 assert f["numeric_value"] is f["historical_decimal"] is None
 assert f["technical_subheader_does_not_equal_day_specific_printed_row"] is True
 assert f["unit_scale_or_fen_miao_shao_equivalence"]=="UNBOUND" and f["p73_to_p74_day4_6_field_assignment"]=="UNPROVEN"
 assert f["p74_fourfen_exact_decimals"]==en["findings"]["d4_d5_d6_fourfen_exact_decimals"]==[None]*3
 assert f["p76_solar_d30_original"]==ed["finding"]["d30_visible_glyph_group"]=="初度九十六二〇三"
 assert f["p76_solar_d30_decimal"] is None and f["g893_six_targets_closed"]==0
 assert f["earlier_13ei_false_chudu_attribution_stays_retracted"] is True and ei["replacement"]["normalized_pair_geometry"]=="RETRACTED_NOT_ADMISSIBLE"
 assert all(v==0 for k,v in e["impact"].items() if k in ("matrix_rows_changed","registry_sources_added","genealogy_nodes_added","genealogy_edges_added","risks_closed","algorithm_reopens"))
 assert e["impact"]["chart_product"]=="CLOSED" and e["impact"]["risks_open_or_blocked"]==11
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert any(x.startswith("13EP ") for x in s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 q=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert q["priority"]=="P0" and q["status"]=="OPEN" and historical_action_view(q).startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert P in q["source_refs"] and P.replace(".json",".md") in q["source_refs"]
 h=next(x for x in q["history"] if x.get("revision_id")=="TW-OPEN-0005-13EP-P73-SUMMER-RICHA-20261024")
 assert h["previous_next_action"].startswith("13EO CURRENT ACTION:") and set(h["changed_fields"])=={"source_refs","next_action"}
 assert all(x in historical_action_view(q) for x in ("D4","D5","D6","D30","四分","初度","NULL"))
 assert any(x.get("revision_id")=="TW-OPEN-0005-13EP-LEGACY-GATE-EXPLICIT-DAYLABELS-20261024" and x.get("previous_next_action","").startswith("13EP CURRENT ACTION:") for x in q["history"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"] and len(l["issues"])==11
 return True
def replay(e,source_dir):
 from PIL import Image
 p=Path(source_dir)/e["source"]["png_filename"]
 assert hashlib.sha256(p.read_bytes()).hexdigest()==e["source"]["png_sha256"]
 with Image.open(p) as im:rgb=im.convert("RGB")
 assert list(rgb.size)==e["source"]["image_size"] and hashlib.sha256(rgb.tobytes()).hexdigest()==e["source"]["rgb_sha256"]
 for r in e["rois"]:
  assert hashlib.sha256(rgb.crop(tuple(r["bbox"])).tobytes()).hexdigest()==r["rgb_sha256"],r["name"]
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--source-dir");args=p.parse_args()
 e=read(P);assert check(e,read(EO),read(EN),read(EI),read(ED),read(S),read(L))
 if args.source_dir:assert replay(e,args.source_dir)
 print("13EP_PASS SUMMER_RICHA_LITERAL_ORIGINAL_SHA_NO_NUMERIC_CONVERSION")
