#!/usr/bin/env python3
"""13CU: safeguard ambiguous NCL03130 Zhi red numeral against premature range promotion."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CU-NCL03130-ZHI-MISSING-RANGE-GLYPH-ROI-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p):return json.loads((R/p).read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13CU-NCL03130-ZHI-SHORTAGE-GLYPH-ALTERNATIVES-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["previous_checkpoint"]=="docs/research/TIANWEN-13CT-NCL03130-RED-REGISTER-CATEGORY-ZHI6-R1.json"
 p=e["physical_source_boundary"]
 assert p["github_workflow_run"]==39773078687 and p["github_artifact_id"]==12423406394
 assert p["original_pdf_sha256"]=="24fb9612634ba085d2546ba6c1f02305aa2a02b9ddfd02f0b645ba0409b5e01e"
 assert p["pdf_page_1based"]==7 and p["source_png_sha256"]=="baa5ab0199a41af85ee6a5290601d15390a7faf7ea2c247b0cdd8e7867dee456"
 assert p["source_png_dimensions"]==[1474,974]
 assert p["roi_digest_method"]=="SHA256_OF_PIL_RGB_CROP_TOBYTES_AFTER_DECODE_SOURCE_PNG"
 assert p["ocr_used"] is False and p["image_filters_and_resize_create_no_new_original_pixels"] is True
 assert "NO_FIRSTPARTY_NCL_ITEM_LINK" in p["hosting"]
 expected=[["genre_zhi",[991,115,1053,187],"0461691a33439846bbc34d477067d8f4d61560a778097601900f3af279259bd4"],["marker_shao",[986,188,1046,247],"8c87afe21be264aef006a75484631130bb560f3f21f1811860151f890f0ea7ef"],["first_numeral",[986,246,1049,285],"cc5bb903565ed35ac5c2ad0ae39fadeaa4017aae056fc8af66c46dfba619c77e"],["range_connector_ambiguous",[989,282,1045,332],"d30c0d7c4dbb2eb1a82f3509dd87e7fa07c0e7dcc24aed3243813e8fcc8d1c33"],["end_numeral_candidate",[990,328,1046,377],"62550812556e549df8690d9504d3979ed7eb0c6c4c85343a943d322da2377bcd"],["further_numbers",[986,400,1056,502],"4e3717e58fda1dbab550ac9ba3718ff03d8b6e87f6013c3e94d51d26ddd01d86"],["entire_zhi_column",[970,105,1061,705],"37d4cec8bb9882e7c632b66a0e80b0b6fa91788614e67924c2033dbe794550a6"]]
 observed=[[x["id"],x["bbox"],x["rgb_sha256"]] for x in e["manual_red_ink_crops"]]
 assert observed==expected
 for x in e["manual_red_ink_crops"]:
  a,b,c,d=x["bbox"]
  assert 0<=a<c<=1474 and 0<=b<d<=974
 readings=e["bounded_reading"]
 assert readings["stable_genre_and_marker"]=="志少"
 assert readings["fourth_linking_glyph_verdict"].startswith("AMBIGUOUS")
 assert readings["is_zhi_six_mentioned_or_included"]=="UNRESOLVED"
 assert readings["is_fully_transcribed"] is False and readings["cannot_use_probable_to_select_A"] is True
 assert readings["current_option"]=="C"
 options=readings["options"]
 assert [x["id"] for x in options]==["A","B","C"]
 assert options[0]["status"]=="CONDITIONAL_ONLY_NOT_ATTESTED" and options[0]["implied_six_in_missing_range"] is True
 assert options[1]["status"]=="CONDITIONAL_ONLY_NOT_ATTESTED" and options[1]["implied_six_in_missing_range"] is None
 assert options[2]["status"]=="CURRENT_FAIL_CLOSED"
 t=e["text_structure"]
 assert t["whole_book_juan"]==52 and t["genre_juan"]==6
 assert t["kind"]=="FIRSTPARTY_RECEIVED_TEXT_INDEX_ONLY"
 n=e["next_gate"]
 assert n["z6_current_status"]=="UNRESOLVED" and n["third_historical_copy_votes"]==0
 assert n["existing_waseda_naj_printed_D16_SHORT"]=="5.1362" and n["derived_only_D16_short_candidate"]=="5.2362"
 assert len(e["transmission_impact"]["edges_supported"])==0 and len(e["transmission_impact"]["nodes_added_or_strengthened"])==0
 c=e["counts"]
 assert (c["matrix_rows"],c["audited_rows"],c["source_total"],c["genealogy_nodes"],c["genealogy_edges"],c["open_research_risks"],c["algorithm_reopens"],c["product"])==(222,222,754,252,238,11,0,"CLOSED")
 assert (s["historical_audit"]["row_count"],s["historical_audit"]["audited_row_count"],s["historical_audit"]["external_source_registry_total_unique_count"])==(222,222,s["historical_audit"]["external_source_registry_root_count"]+s["historical_audit"]["external_source_registry_extension_count"])
 assert s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]==l["binding"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert any(x.startswith("13CU ") for x in s["historical_audit"]["current_focus"])
 i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert i["status"]=="OPEN" and E in i["source_refs"]
 assert any(x.get("event")=="ISSUE_REVISION" and x.get("revision_id")=="TW-OPEN-0005-13CU-ZHI-RANGE-CONNECTOR" and "next_action" in x.get("changed_fields",[]) for x in i["history"])
 assert "CURRENT ACTION:" in i["next_action"]
 assert any(x.get("id")=="OMISSIONS-13CU-ZHI-AMBIGUOUS-CONNECTOR-20261022" for x in l["checkpoint_log"])
 assert sum(x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS") for x in l["issues"])==11
 assert s["invariants"]["algorithm_reopen_count"]==0 and s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L))
 print("TIANWEN_13CU_AMBIGUOUS_ZHI_RANGE_GLYPH_FAIL_CLOSED=PASS")
