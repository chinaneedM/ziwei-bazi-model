#!/usr/bin/env python3
"""13MS original source atlas / provenance layers and cross-batch pixel hash conflict."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13MS-ZHOU1569-ORIGINAL-SOURCE-ATLAS-AND-NAAJ-HOLDING-R1.json"
S=ROOT/"docs/PROJECT-CURRENT-STATE-R1.json"
L=ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
P=ROOT/"docs/research/TIANWEN-13MQ-G893-ZHOU1569-D15-SECOND-LANE-ORIGINAL-PRINT-SCOPE-R1.json"
def check(e,s,l,p):
 assert e["schema"]=="TIANWEN-13MS-ZHOU1569-ORIGINAL-SOURCE-ATLAS-AND-NAAJ-HOLDING-R1"
 a=e["original_acquisition"]
 assert a["workflow_run_id"]==41196638003 and a["artifact_id"]==13041277087
 assert a["source_sha256"]==p["provenance"]["zhou1569_pdf_sha256"]
 assert a["source_bytes"]==4936040 and a["total_pdf_pages"]==45
 assert a["rendered_1based_pages"]==[14,15,16] and a["scale"]==2.5
 assert a["render_env_evidenced_by_action_logs"]["pymupdf"]=="1.28.2"
 assert a["ocr"] is False and a["new_physical_copy_count"]==a["new_registered_source_count"]==0
 assert len(a["original_roi_samples"])==6
 assert a["original_roi_samples"][3]["box"]==p["original_roi_controls"][1]["box"]
 v=e["pixel_replay_conflict"]
 assert v["target_box"]==p["original_roi_controls"][1]["box"]
 assert v["previous_13mq_rgb_sha256"]==p["original_roi_controls"][1]["rgb_sha256"]
 assert v["new_13ms_rgb_sha256"]==a["original_roi_samples"][3]["rgb_sha256"]
 assert v["previous_13mq_rgb_sha256"]!=v["new_13ms_rgb_sha256"]
 assert v["hashes_equal"] is False and v["same_source_pdf_sha256"] is True
 assert v["status"]=="UNRECONCILED_DERIVED_PIXEL_RGB_SHA_NOT_HISTORICAL_TEXT_VARIANT"
 assert e["calendrical_dates_separated"]["specific_surviving_copy_impression_date"]=="NOT_ORIGINAL_COPY_ATTESTED_FROM_DIRECT_COLophon"
 assert len(e["historical_source_provenance_leads"])==3
 assert any("子151-0003" in x["identification"] for x in e["historical_source_provenance_leads"])
 g=e["no_promotion"]
 for k in ("cross_source_field_identity","source_units_radix_epoch_bound","solar_second_column_mechanical_win","source_print_digit_historical_error","physical_copy_independence_proven","prediction_scope_activation"):
  assert g[k] is False
 for k in ("registered_source_count_delta","registered_genealogy_node_delta","registered_genealogy_edge_delta","g893_six_historical_winners","algorithm_reopen"):
  assert g[k]==0
 assert g["deterministic_product"]==s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,981,0)
 assert any(f.startswith("13MS ") for f in s["historical_audit"]["current_focus"])
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
 issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert "docs/research/TIANWEN-13MS-ZHOU1569-ORIGINAL-SOURCE-ATLAS-AND-NAAJ-HOLDING-R1.json" in issue["source_refs"] and "docs/research/TIANWEN-13MS-ZHOU1569-ORIGINAL-SOURCE-ATLAS-AND-NAAJ-HOLDING-R1.md" in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13MS-ORIGINAL-ATLAS-NAJK-COPY-SCOPE-20261031" for x in issue["history"])
 assert any(x["id"]=="OMISSIONS-13MS-ORIGINAL-ATLAS-BIBLIO-SCOPE-20261031" for x in l["checkpoint_log"])
 assert s["historical_audit"]["external_source_registry_total_unique_count"]==765
 return {"status":"PASS","source_pdf_byte_verified":True,"new_rgb_crops":6,"legacy_13mq_rgb_status":"UNRECONCILED","six_historical_winners":0}
if __name__=="__main__":
 e,s,l,p=(json.loads(q.read_text(encoding="utf-8")) for q in (E,S,L,P))
 print(json.dumps(check(e,s,l,p),ensure_ascii=False))
