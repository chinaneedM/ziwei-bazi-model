#!/usr/bin/env python3
"""13CQ: prevent premature promotion of NCL composite manuscript stratum and missing-juan claim."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CQ-GORYEOSA-NCL03130-MISSING-JUAN-1905-STRATA-R1.json";S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13CQ-NCL03130-MISSING-JUAN-1904-1905-STRATA-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 assert e["previous_checkpoint"]=="docs/research/TIANWEN-13CP-GORYEOSA-NCL03117-03130-SURROGATE-ID-CROSSWALK-R1.json"
 a,b,c=e["sources"]
 assert a["type"]=="MIRROR_TRANSCRIBED_PARATEXT" and "缺卷朱記于首" in a["text_fragments"] and "乙巳夏" in a["text_fragments"]
 assert b["type"]=="INDEPENDENT_YEAR_EQUIVALENCE" and b["pairs"]==[{"era":"光緒三十年甲辰","ce":1904},{"era":"光緒三十一年乙巳","ce":1905}]
 assert c["url"]=="https://rbook.ncl.edu.tw/NCLSearch/FAQ"
 p=e["provenance"]
 assert p["red_register_original_image_obtained"] is False and p["red_register_actual_juan_membership"]==[]
 assert p["work_juan_52_register_membership"]=="UNRESOLVED"
 assert p["old_copy_acquisition"]=="GUANGXU_JIACHEN_1904_REPORTED"
 assert p["ding_hefu_supplement_completion"]=="GUANGXU_YISI_SUMMER_1905_REPORTED"
 assert p["juan52_original_stratum"]=="UNBOUND"
 assert p["date_layer_rule"]=="1905_COMPLETION_NOT_EQUAL_TO_EACH_EXISTING_FOLIO_DATE"
 assert [x["id"] for x in e["acquisition_gate"]]==["FRONT","JUAN52","STRATA","GLYPHS","LINEAGE"]
 v=e["limits"]
 assert v["first_party_ncl03130_exact_item"]=="UNBOUND" and v["provider_original_pdf_downloaded"] is False and v["provider_original_pdf_sha256"] is None
 assert v["missing_register_read_directly"] is False and v["juan52_original_folio_read"] is False
 assert v["juan52_in_missing_list"]==v["juan52_1905_replacement_status"]=="UNRESOLVED"
 assert v["third_independent_d16_original_witnesses"]==0
 assert v["original_d16_short_waseda_naj"]=="5.1362" and v["derived_candidate_d16_short_not_original"]=="5.2362"
 for key in ["no_adjudication_of_printed_digit","no_source_image_or_ocr_this_batch","avoid_1904_date_as_folio_copy_age","avoid_commons_pdf_counts_as_independent_copies"]:assert v[key] is True
 w=e["scope"]
 assert (w["matrix_rows"],w["registered_sources"],w["graph_nodes"],w["graph_edges"],w["open_risks"])==(222,754,252,238,11)
 for key in ["new_registry_rows","new_graph_nodes","new_graph_edges","new_original_historical_witnesses","algorithm_reopens"]:assert w[key]==0
 assert w["product"]=="CLOSED" and s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 assert s["invariants"]["algorithm_reopen_count"]==0
 assert s["historical_audit"]["row_count"]==s["historical_audit"]["audited_row_count"]==222
 assert s["historical_audit"]["external_source_registry_total_unique_count"]==s["historical_audit"]["external_source_registry_root_count"]+s["historical_audit"]["external_source_registry_extension_count"]
 assert any(x.startswith("13CQ ") for x in s["historical_audit"]["current_focus"])
 assert l["binding"]["reviewed_state_version"]==s["schema_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13CQ-1905-MANUSCRIPT-STRATA" for x in issue["history"])
 assert any(x["id"]=="OMISSIONS-13CQ-MISSING-JUAN-20261022" for x in l["checkpoint_log"])
 assert sum(x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS") for x in l["issues"])==11
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L))
 print("TIANWEN_13CQ_NCL_MISSING_JUAN_STRATA=PASS; RED_LIST_ORIGINAL_NOT_READ")
