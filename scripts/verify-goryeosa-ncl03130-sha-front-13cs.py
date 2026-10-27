#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CS-NCL03130-SHA-FRONT-IMAGE-R1.json"
def read(p):return json.loads((R/p).read_text(encoding="utf8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13CS-NCL03130-SOURCE-MIRROR-FRONT-IMAGE-R1"
 c=e["verified_capture"]
 assert c["workflow_run"]==39771104334 and c["artifact_id"]==12421898945
 assert c["pdf_sha256"]=="24fb9612634ba085d2546ba6c1f02305aa2a02b9ddfd02f0b645ba0409b5e01e"
 assert c["pdf_pages"]==204 and c["bytes"]==50586812 and c["no_ocr"]
 a=e["original_front_preview_observation"]
 assert a["manually_visually_reviewed_pdf_pages"]==[3,4,7,8,9,10]
 assert a["red_handwritten_marks_visible_on_page_7"] and not a["red_marks_identified_as_missing_juan_register"]
 assert a["missing_juan_register_transcribed"] is False and a["volume52_missing_status"]=="UNRESOLVED"
 assert a["qing_old_vs_1905_supplement"]=="UNBOUND"
 p=e["new_review_acquisition"]
 assert p["matrix_scale"]==3.5 and p["expected_pdf_sha256"]==c["pdf_sha256"]
 assert p["next_run_success_at_commit"]=="NOT_YET_OBSERVED"
 assert e["source_firewall"]["third_original_copy_d16_count"]==0
 assert e["source_firewall"]["original_waseda_naj_short_d16"]=="5.1362"
 assert e["source_firewall"]["historical_glyph_adjudicated"] is False
 assert e["source_firewall"]["first_party_ncl_208_03130_binding"]=="UNBOUND"
 assert s["historical_audit"]["row_count"]==s["historical_audit"]["audited_row_count"]==222
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 assert s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]==l["binding"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert any(x.startswith("13CS ") for x in s["historical_audit"]["current_focus"])
 assert any(x["id"]=="OMISSIONS-13CS-SHA-FRONT-20261022" for x in l["checkpoint_log"])
 assert E in next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["source_refs"]
 assert sum(x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS") for x in l["issues"])==11
 return True
if __name__=="__main__":
 assert check(read(E),read("docs/PROJECT-CURRENT-STATE-R1.json"),read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
 print("TIANWEN_13CS_NCL03130_SOURCE_SHA_FRONT_IMAGES=PASS")
