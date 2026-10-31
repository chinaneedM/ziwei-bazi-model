#!/usr/bin/env python3
"""13MR source-local Zhou operator scope and forward-only P0 continuity gate."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13MR-ZHOU1569-ORIGINAL-OPERATOR-PRINTED-FIELD-SCOPE-R1.json"
S=R/"docs/PROJECT-CURRENT-STATE-R1.json"
L=R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
P=R/"docs/research/TIANWEN-13MQ-G893-ZHOU1569-D15-SECOND-LANE-ORIGINAL-PRINT-SCOPE-R1.json"
def check(e,s,l,p):
 assert e["schema"]=="TIANWEN-13MR-ZHOU1569-ORIGINAL-OPERATOR-PRINTED-FIELD-SCOPE-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["source"]["ocr_used"] is False
 assert e["source"]["new_pdf_bytes_retrieved_this_batch"] is False
 assert e["source"]["new_source_pixel_sha_computed_this_batch"] is False
 assert e["source"]["physical_copy_count_increment"]==0
 assert e["source"]["prior_archived_source_sha256"]==p["provenance"]["zhou1569_pdf_sha256"]
 assert e["visible_original_page14"]["section_heading"]=="推盈縮差度分法"
 assert e["visible_original_page14"]["operator_phrases"]==["其積日下盈縮加分乘之得數","復加其下盈縮積度全分"]
 assert e["visible_original_page14"]["table_heading"]=="太陽冬至前後立成卷第二"
 assert e["page15"]["day_headings"]==[15,16,17]
 assert e["page15"]["prior_source_scoped_short_prints"]==["5.2176","5.2362","5.2548"]
 assert e["page15"]["prior_original_d15_another_numeric_string"]==p["reading_adjudication"]["zhou_other_column_print"]
 assert e["page15"]["new_numeral_readings_this_batch"]==0
 c=e["comparison"]
 assert c["g893_d15_other_print"]==p["reading_adjudication"]["g893_other_column_print"]
 assert c["zhou_d15_other_print"]==p["reading_adjudication"]["zhou_other_column_print"]
 assert c["same_printed_strings"] is False and c["shared_short_strings_are_not_same_fields"] is True
 assert c["source_1569_operator_to_D15_second_numeric_lane"]=="NOT_YET_GLYPH_AND_COLUMN_BOUND"
 assert c["g893_header_to_d15_original_numeric_lane"]=="NOT_YET_FULLY_BOUND"
 assert c["cross_source_field_unit_radix_epoch_identity"]=="UNPROVEN"
 assert c["surviving_1569_physical_impression"]=="UNBOUND" and c["direct_copying"]=="UNPROVEN"
 assert e["guard"]["g893_final_historical_winners"]==e["guard"]["algorithm_reopens"]==0
 assert e["guard"]["product"]==s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 assert e["guard"]["external_unique_sources"]==s["historical_audit"]["external_source_registry_total_unique_count"]==765
 assert e["guard"]["matrix_rows"]==s["historical_audit"]["row_count"]==222
 assert e["guard"]["matrix_audited"]==s["historical_audit"]["audited_row_count"]==222
 assert e["guard"]["unresolved_issues"]==len(l["issues"])==11
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,980,0)
 assert any(f.startswith("13MR ") for f in s["historical_audit"]["current_focus"])
 i=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
 assert i["priority"]=="P0" and i["status"]=="OPEN"
 assert "docs/research/TIANWEN-13MR-ZHOU1569-ORIGINAL-OPERATOR-PRINTED-FIELD-SCOPE-R1.json" in i["source_refs"]
 assert "docs/research/TIANWEN-13MR-ZHOU1569-ORIGINAL-OPERATOR-PRINTED-FIELD-SCOPE-R1.md" in i["source_refs"]
 assert any(x["revision_id"]=="TW-OPEN-0005-13MR-OPERATOR-SCOPE-20261031" for x in i["history"] if "revision_id" in x)
 assert any(x["id"]=="OMISSIONS-13MR-OPERATOR-SCOPE-20261031" for x in l["checkpoint_log"])
 return {"status":"PASS","pixel_replay":"NOT_EXECUTED_WITHOUT_SOURCE_BYTES","same_field_equivalence":"NOT_PROVEN","historic_winners":0}
if __name__=="__main__":
 e,s,l,p=(json.loads(x.read_text(encoding="utf-8")) for x in (E,S,L,P))
 print(json.dumps(check(e,s,l,p),ensure_ascii=False))
