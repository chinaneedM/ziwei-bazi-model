#!/usr/bin/env python3
"""12YE source-original full eight-digit printed solar lane guard; no OCR."""
import json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YE-G893-SOLAR-EIGHT-PLACE-PRECISION-R1.json"
NUMS=["5.21768249","5.23626073","5.25483711"]
GLYPHS=["五分二一七六八二四九","五分二三六二六〇七三","五分二五四八三七一一"]
HASHES=["7774923553373bd6fa0fdcc7f7cda005842451859219fa0179c997693c832a47","e0c8b48ba433ec87687d76250e47eb73a2db51ea153cf69411bb8eb6f9e8250f","431440e240c24e7a875d729e586d7b1cbdb67562caa80f2f195ac31dfb7866f5","daffb805e7730de9186396c4a0bb3d198c201bebf9de68c9666669d1f3d00cd7"]
def need(value,msg):
 if not value:raise ValueError(msg)
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json"))
def verify(d,ledger,state):
 need(d["schema"]=="TIANWEN-12YE-G893-SOLAR-EIGHT-PLACE-SOURCE-PRECISION-R1","schema")
 a=d["archive"];need(a["sha256"]=="ee9ecf1de3bb6abe5678e0f8ec8383ef985051e77d091ee40840756e57081107" and a["size"]==33525981 and a["crc"]=="PASS" and a["original_jpegs_verified"]==204 and a["physical_copies"]==1 and a["original_images_committed"]==0,"archive")
 need([x["sha256"] for x in d["pages"]]==["8b07513ca8aad42ae167a93f22c39f14850c8cd1c345db9ce98c1e0e769226a5","f9812e8c6a357eb6cd1117bb2af58d816e01030d5b93f34e7094bddb766b2b55"],"pages")
 need(len(d["rois"])==4 and [x["sha256"] for x in d["rois"]]==HASHES,"original native crops")
 need(all(x["page"]=="002b" and 0<=x["rect"][0]<x["rect"][2]<=1150 and 0<=x["rect"][1]<x["rect"][3]<=2000 for x in d["rois"]),"crop geometry")
 old=json.loads((ROOT/d["prior_evidence"]).read_text(encoding="utf-8"))
 oldrows=old["original_reading_scope"]["source_bounded_candidate_vertical_lane"]
 rows=d["readings"];need(len(rows)==3 and len(oldrows)==3,"day number")
 for i,x in enumerate(rows):
  need((x["day"],x["original_glyphs"],x["lexical_decimal"],x["prior_four_places"])==(i+15,GLYPHS[i],NUMS[i],oldrows[i]["derived_candidate_decimal_string"]),"original glyph/eight-place/prefix")
  need(x["original_glyphs"]=="五分"+"".join("〇一二三四五六七八九"[int(ch)] for ch in NUMS[i].split(".")[1]),"old numeral mapping")
  need(x["lexical_decimal"][:6]==x["prior_four_places"],"four-place prefix")
 u,v,w=map(Decimal,NUMS); q=d["arithmetic"]
 need(str(v-u)==q["delta_15_16"]=="0.01857824" and str(w-v)==q["delta_16_17"]=="0.01857638" and str(w-2*v+u)==q["second_difference"]=="-0.00000186" and q["exact_precision"]=="DECIMAL_8","exact decimal")
 need(q["prior_four_place_deltas"]==["0.0186","0.0186"],"historic short step")
 g=d["boundaries"]
 need(all(g[k]=="UNPROVEN" for k in ("source_header_unit_to_lane","original_d16_formal_target","ming_1569_identical_mechanical_field","copying_causality")),"false field unit bridge")
 need(g["adjacent_large_lane_arithmetic"]=="PENDING" and g["source_original_complete_targets"]=="5/6" and g["final_cross_witness_decisions"]=="0/6" and g["open_research_issues"]==11 and g["new_physical_copies"]==g["new_graph_edges"]==g["algorithm_reopens"]==0,"false award")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 need(issue["status"]=="OPEN" and DOC in issue["source_refs"] and "docs/research/TIANWEN-12YE-G893-SOLAR-EIGHT-PLACE-PRECISION-R1.md" in issue["source_refs"],"source risk missing")
 need(issue["g893_d16_eight_place_original_reviews"][-1]["source_second_difference"]=="-0.00000186" and any(h["event"]=="G893_EIGHT_PLACE_SOURCE_PRECISION_APPEND" for h in issue["history"]),"historical 12YE archive not retained")
 need(issue["g893_12ye_dual_column_errata"][-1]["retracted_false_second_difference"]=="-0.00000186" and issue["g893_12ye_dual_column_errata"][-1]["correction"]=="RETRACTED_AS_CROSS_COLUMN_CONCATENATION" and issue["g893_12yf_long_direction_errata"][-1]["retracted_relation"]=="LONG_INCREASE_EQUALS_10_MINUS_SHORT","dangerous uncorrected 12YE eight place reading")
 need(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,state["schema_version"].split(".")))>=(1,620,0) and any(f.startswith("12YE ") for f in state["historical_audit"]["current_focus"]) and any(f.startswith("12YF ") for f in state["historical_audit"]["current_focus"]) and any(f.startswith("12YG ") for f in state["historical_audit"]["current_focus"]),"state mismatch")
 need(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"product reopen")
 return {"status":"PASS","historical_12ye_raw_record":"PRESERVED_BUT_RETRACTED_BY_12YF","alleged_eight_decimal_field":"INVALID_CROSS_COLUMN_JOIN","old_derived_minus_0_00000186":"NOT_SOURCE_EVIDENCE","original_d16_mechanical_field":"UNPROVEN"}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
