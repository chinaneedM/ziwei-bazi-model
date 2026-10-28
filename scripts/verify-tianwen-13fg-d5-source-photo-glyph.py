#!/usr/bin/env python3
"""Fail-closed 13FG NIKH source-pixel D5 五 / NLC 〇 evidence status validator."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13FG-NIKH-JUAN52-PHOTO-D5-FIVE-VS-NCL-CIRCLE-BOUNDED-COLLATION-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def read(path):return json.loads((R/path).read_text(encoding="utf8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13FG-NIKH-JUAN52-PHOTO-D5-FIVE-VS-NCL-CIRCLE-BOUNDED-COLLATION-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 a=e["source_image_recovery"]; d=e["D5_direct_visual_image_evidence"];o=e["opposing_prior_source"];im=e["impact"]
 assert a["source_emitted_total_images"]==23 and a["first_pass_13FE_requested"]==23 and a["first_pass_13FE_valid_jpegs"]==17
 assert a["targeted_second_pass_13FF_success_indices"]==[3,4]
 assert a["first_pass_13FE_transport_error_indices"]==[3,4,9,13,17,22]
 assert a["outstanding_transport_error_indices"]==[9,13,17,22]
 assert a["total_captured_unique_modern_viewer_images"]==19
 assert a["physical_witness_count_from_19_images"]==1 and a["physical_copy_independence_proven"] is False
 assert a["failed_transport_is_not_absent_folio"] and a["no_unauthorized_endpoint_enumeration"]
 hashes=a["captured_modern_index_to_exact_sha256"]
 assert len(hashes)==19 and set(hashes)=={str(x) for x in range(1,24)}-{"9","13","17","22"}
 assert all(isinstance(x,str) and len(x)==64 and all(c in "0123456789abcdef" for c in x) for x in hashes.values())
 assert d["modern_viewer_index"]==2 and d["modern_filename"]=="kr_052_1056.jpg"
 assert d["source_JPEG_bytes"]==261092
 assert d["source_JPEG_SHA256"]==hashes["2"]=="0b8e8a2a280d52068e79c8fdb04b1c7caae994205dd5502403c35672c51b21a7"
 assert d["directly_visible_day_heading"]=="五日"
 assert d["directly_visible_column_heading"]=="四分" and d["directly_visible_four_glyphs"]=="五一七二"
 assert d["directly_read_literal"]=="四分五一七二" and d["direct_visual_method"]=="HUMAN_STYLE_VISUAL_REVIEW_NO_OCR"
 assert d["original_RGB_day_heading_bbox_xyxy"]==[110,263,210,432]
 assert d["original_RGB_day_heading_sha256"]=="427d4b129cadc2e7fccb018f7e2a0a3322ee0a111e79c10c109bc5e140e9f41b"
 assert d["original_RGB_fourfen_lane_bbox_xyxy"]==[167,606,250,1450]
 assert d["original_RGB_fourfen_lane_sha256"]=="e3bcf659d342b6fe46349eb0dbb91433992d59b0cccb3befbb17d5c401a4c833"
 assert d["physical_original_book_number"] is d["physical_original_leaf_number"] is d["historical_numeric_D5_interpreted_as_decimal"] is None
 assert d["original_physical_edition_identity_verified"] is False and d["independent_authenticated_physical_copy_vote_added"]==0
 assert o["prior_visual_D5"]=="四分〇一七二"
 assert o["KRDB_modern_editorial_D5"]==o["NIKH_saved_photo_D5"]=="四分五一七二"
 assert o["contradictory_photographic_glyphs_observed"] and o["historic_true_winner"]=="UNADJUDICATED"
 assert o["NCL_O_original_reading_withdrawn"] is False and o["KRDB_modern_digital_editorial_FIVE_error_claim_proven"] is False
 assert e["independent_unresolved_controls"]["prior_13EI_false_claim"]=="RETRACTED"
 assert e["independent_unresolved_controls"]["G893_six_source_original_controls"]=="OPEN"
 assert im["source_registry_total_unique_count"]==761 and im["matrix_audited_count"]==im["matrix_row_count"]==222
 assert im["historical_photo_literal_observation_delta"]==1 and im["separately_authenticated_independent_ancient_editions_added"]==0
 assert all(im[k]==0 for k in ("source_registry_delta","matrix_rows_delta","genealogy_node_delta","genealogy_edge_delta","cross_edition_historical_numeric_adjudications_added","chart_algorithm_reopens","chart_candidate_collapses","risk_closure_count"))
 assert im["risk_issue_status"]=="OPEN" and im["risk_issue_priority"]=="P0" and im["product_status"]=="CLOSED"
 assert e["transmission_impact"]["new_supported_edges"]==[] and e["transmission_impact"]["not_established_as_recension_variant_edge"]
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert isinstance(l["binding"]["latest_research_focus_prefix"],str) and l["binding"]["latest_research_focus_prefix"] and l["binding"]["latest_research_focus_prefix"].startswith("13")
 assert any(x.startswith("13FG ") for x in s["historical_audit"]["current_focus"])
 # Preserve the immutable 13FG 761-source historical snapshot, but compare
 # the live handoff against it monotonically after later valid shard growth.
 assert s["historical_audit"]["external_source_registry_total_unique_count"]>=im["source_registry_total_unique_count"]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert {P,P.replace(".json",".md")}.issubset(set(issue["source_refs"]))
 assert issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert any(x.get("revision_id")=="TW-OPEN-0005-13FG-TWO-ORIGINAL-PHOTO-D5-FIVE-VS-CIRCLE-20261024" for x in issue["history"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"] and len(l["issues"])==11
 return True
if __name__=="__main__":
 assert check(read(P),read(S),read(L))
 print("13FG_PASS_NIKH_SOURCE_PIXEL_D5_FIVE_NCL_SOURCE_PIXEL_CIRCLE_PHYSICAL_EDITION_UNBOUND")
