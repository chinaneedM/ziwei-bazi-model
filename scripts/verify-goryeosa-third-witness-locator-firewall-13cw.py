#!/usr/bin/env python3
"""13CW: exact third-copy locator scope, categorical no-ID-guess, no physical source inflation."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CW-NCL-NEIGHBOR-AND-CNTS-CATALOG-GAP-FIREWALL-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p): return json.loads((R/p).read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13CW-GORYEOSA-THIRD-WITNESS-LOCATOR-FIREWALL-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 n=e["first_party_ncl_neighbor_control"]
 assert n["observed_title"]=="東國史略" and n["observed_call_number"]=="208 03128"
 assert n["expected_target_call_number"]=="208 03130"
 assert n["is_target_item"] is False and n["exact_target_03130_verified"] is False
 assert n["no_firstparty_absence_inference"] is True
 assert "SearchDetail" in n["entry"] and n["source_class"].startswith("FIRSTPARTY_NEIGHBOR")
 k=e["commons_korean_category_bounded_listing"]
 assert k["listing_snapshot_first_page_files"]==200 and k["listing_total_claimed_files"]==372
 assert [x["label"] for x in k["entries_observed"]]==["CNTS-00129837049","CNTS-00129837050","CNTS-00129837052"]
 assert k["proposed_missing_intermediate_identifier"]=="CNTS-00129837051"
 assert k["proposed_identifier_verified"] is False and k["v52_physical_copy_presence"]=="UNDETERMINED"
 assert k["category_first_page_nonappearance_not_absence_proof"] is True
 assert k["a_numeric_gap_is_not_an_item_or_copy_identity"] is True
 m=e["commons_taiwan_mirror_separation"]
 assert m["visible_named_mirror_parts"]==24 and m["source_described_physical_fascicles"]==40
 assert m["mirror_named_file_numbers_are_not_juan_numbers"] is True
 assert m["mirror_part_count_cannot_establish_missing_fascicles"] is True
 assert m["uploader_local_filename_03117_is_not_ncl_03117_physical_identity"] is True
 assert m["p7_ambiguous_red_zhi_range"]=="UNRESOLVED" and m["genre_zhi6_1905_hand"]=="UNBOUND"
 assert m["direct_target_physical_folio"]=="NOT_OBTAINED"
 assert len(e["priority_resolution_route"])==4
 z=e["scope"]
 assert z["third_new_independent_historical_originals"]==0 and z["ncl_physical_vol52_recovered"] is False
 assert z["original_d16_two_holding_literal"]=="5.1362" and z["derived_d16_arithmetic_only"]=="5.2362"
 assert (z["matrix_rows"],z["matrix_audited"],z["registry_total"],z["genealogy_nodes"],z["genealogy_edges"],z["open_risks"])==(222,222,754,252,238,11)
 assert z["confirmed_chart_algorithm_defects"]==z["algorithm_reopens"]==z["historical_sources_registered_added"]==z["graph_nodes_added"]==z["graph_edges_added"]==0
 assert z["product"]=="CLOSED"
 t=e["transmission_impact"]
 assert not t["nodes_added_or_strengthened"] and not t["edges_supported"] and not t["edges_revised"]
 assert len(t["edges_rejected_or_unproved"])==3
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13CW ") for x in s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"] and "docs/research/TIANWEN-13CW-NCL-NEIGHBOR-AND-CNTS-CATALOG-GAP-FIREWALL-R1.md" in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13CW-THIRD-WITNESS-LOCATOR-FIREWALL" for x in issue["history"])
 assert "CURRENT ACTION:" in issue["next_action"]
 assert any(x.get("id")=="OMISSIONS-13CW-THIRD-WITNESS-LOCATOR-FIREWALL-20261022" for x in l["checkpoint_log"])
 assert sum(i["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS") for i in l["issues"])==11
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L))
 print("TIANWEN_13CW_THIRD_WITNESS_LOCATOR_NO_ID_GUESS=PASS")
