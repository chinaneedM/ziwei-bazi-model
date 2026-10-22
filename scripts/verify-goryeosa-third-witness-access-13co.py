#!/usr/bin/env python3
"""13CO third-witness route research: reject unsupported original-glyph promotion."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CO-GORYEOSA-NCL03130-NDL1909-THIRD-WITNESS-ACCESS-FIREWALL-R1.json";S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13CO-GORYEOSA-NDL1909-NCL03130-CANDIDATE-ACCESS-FIREWALL-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 a,b=e["new_candidate_routes"];assert [a["route_id"],b["route_id"]]==["NDL-JPNO50001638-PID991069","TAIWAN-NCL-208-03130-COMMONS"]
 assert a["bibliography"]["publication_year"]==1909 and a["bibliography"]["work_volume_range"]==[47,87]
 assert a["bibliography"]["contains_work_volume_52_at_range_level"] is True
 assert a["bibliography"]["edition_scope"]=="MODERN_1909_PRINTED_RECEIVED_EDITION"
 assert a["institutional_first_party_catalog_url"]=="https://ndlsearch.ndl.go.jp/books/R100000039-I991069"
 assert a["bibliography"]["ndljp_pid"]=="991069"
 assert a["access"]["actual_target_page_image_downloaded"] is False
 assert a["access"]["original_printed_D16_glyph_read"]=="NOT_REVIEWED" and a["access"]["image_sha256"] is None
 assert a["does_not_resolve_independent_early_exemplar"] is True
 assert b["metadata"]["claimed_call_number"]=="208 03130" and b["metadata"]["stated_total_physical_fascicles"]==40
 assert b["metadata"]["digitized_files_listed_in_commons"]==24
 assert b["metadata"]["catalog_or_mirror_edition_date_is_not_folio_52_copy_date"] is True
 assert b["surrogate_conflict"]["commons_filename_prefix"]=="NCL-03130"
 assert b["surrogate_conflict"]["observed_upload_history_original_localnames"]==["03117_8.pdf","03117_21.pdf"]
 assert b["surrogate_conflict"]["record_grading"]=="METADATA_LEAD_QUARANTINED_UNTIL_SOURCE_NATIVE_IDENTITY"
 assert b["surrogate_conflict"]["source_03117_not_conclusively_proved_wrong_copy"] is True
 assert b["surrogate_conflict"]["original_source_pdf_contents_checked"] is False
 assert b["access"]["d16_glyph_read"]=="NOT_REVIEWED" and b["access"]["verified_original_target_page_sha256"] is None
 q=e["evidence_limits"]
 assert q["third_qualified_direct_original_D16_witnesses_added"]==q["source_original_D16_pixels_collected"]==0
 assert q["historic_goryeosa_work_composition_year"]==1451 and q["modern_NDL_reprint_year"]==1909
 assert q["can_identify_NDL_1909_as_1451_edition"] is False
 assert q["original_D16_short_attested_by_two_previous_copies"]=="5.1362" and q["arithmetic_candidate_not_attested"]=="5.2362"
 assert all(e["scope"][k]==0 for k in ["research_registry_rows_added","historical_matrix_rows_added","genealogy_nodes_added","genealogy_edges_added","algorithm_reopens","original_historic_copy_votes_added"])
 assert e["scope"]["chart"]=="CLOSED" and e["scope"]["open_or_blocked_issues"]==11
 assert s["schema_version"]=="1.751.0" or s["schema_version"].startswith("1.")
 assert any(x.startswith("13CO ") for x in s["historical_audit"]["current_focus"])
 assert s["historical_audit"]["row_count"]==s["historical_audit"]["audited_row_count"]==222
 assert s["historical_audit"]["external_source_registry_total_unique_count"]==754
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
 assert l["binding"]["reviewed_state_version"]==s["schema_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13CO-THIRD-ROUTE-FIREWALL" for x in issue["history"])
 assert any(x["id"]=="OMISSIONS-13CO-THIRD-ROUTE-20261022" for x in l["checkpoint_log"])
 assert len([x for x in l["issues"] if x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS")])==11
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L))
 print("TIANWEN_13CO_THIRD_WITNESS_ACCESS_FIREWALL=PASS; ORIGINAL_D16_IMAGE=NOT_ACQUIRED")
