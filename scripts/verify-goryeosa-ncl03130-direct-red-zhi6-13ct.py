#!/usr/bin/env python3
"""13CT: source-SHA bounded red genre shortage list versus local 志第六, fail-closed."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CT-NCL03130-RED-REGISTER-CATEGORY-ZHI6-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13CT-NCL03130-DIRECT-RED-REGISTER-GENRE-ZHI6-CROSSWALK-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 assert e["previous_checkpoint"]=="docs/research/TIANWEN-13CS-NCL03130-SHA-FRONT-IMAGE-R1.json"
 p=e["primary_image"]
 assert (p["workflow_run_id"],p["artifact_id"],p["pdf_pages"],p["pdf_page_1based"])==(39773078687,12423406394,204,7)
 assert p["pdf_sha256"]=="24fb9612634ba085d2546ba6c1f02305aa2a02b9ddfd02f0b645ba0409b5e01e"
 assert p["png_file"]=="front-page-007.png" and p["png_sha256"]=="baa5ab0199a41af85ee6a5290601d15390a7faf7ea2c247b0cdd8e7867dee456"
 assert p["png_dimensions_px"]==[1474,974] and p["manual_visual_review"] and not p["ocr_used"]
 assert "NOT_YET_NCL_FIRSTPARTY" in p["origin"]
 red=e["red_marginalia_observation"]
 assert red["visible_red_text_genre_tokens"]==["世家","志","傳"]
 assert red["visible_shortage_marker"]=="少"
 assert red["readable_bounded_fragments"]==["世家少…","志少…","傳少…"]
 assert red["specific_juan_numbers_full_list_transcribed"] is False
 assert red["autograph_attribution_to_wu_directly_verified"] is False
 assert red["copy_number_mapping_validated"] is False
 w=e["first_party_text_structure_crosswalk"]
 assert (w["whole_work_juan"],w["genre"],w["genre_juan"])==(52,"志",6)
 assert w["source_url"].startswith("https://db.history.go.kr/goryeo/")
 assert w["type"]=="FIRSTPARTY_RECEIVED_TEXT_STRUCTURAL_MAP_NOT_EVIDENCE_OF_NCL_P7_PHYSICAL_FOLIO"
 gate=e["scope_gates"]
 assert gate["original_missing_list_complete_numbers"]=="UNREAD"
 assert gate["is_genre_zhi_six_missing"]=="UNRESOLVED"
 assert gate["whether_juan52_qing_old_hand"]==gate["whether_juan52_1905_supplement"]=="UNBOUND"
 assert gate["direct_firstparty_ncl20803130_object"]=="UNBOUND" and gate["native_juan52_target_folio_obtained"] is False
 assert gate["treat_pdf_part01_as_40_physical_book_identity"] is False
 assert gate["third_independent_d16_historical_votes_added"]==gate["r1_algorithm_reopen"]==0
 assert gate["printed_original_d16_short_existing_two_copies"]=="5.1362"
 assert gate["numerical_repair_only"]=="5.2362"
 assert not e["transmission_impact"]["edges_supported"]
 z=e["snapshot"];assert (z["matrix_audited"],z["external_source_total"],z["genealogy_nodes"],z["genealogy_edges"],z["open_or_blocked_issues"],z["algorithm_reopens"],z["product"])==(222,754,252,238,11,0,"CLOSED")
 assert s["historical_audit"]["row_count"]==s["historical_audit"]["audited_row_count"]==222
 assert s["historical_audit"]["external_source_registry_total_unique_count"]==s["historical_audit"]["external_source_registry_root_count"]+s["historical_audit"]["external_source_registry_extension_count"]
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
 assert any(x.startswith("13CT ") for x in s["historical_audit"]["current_focus"])
 assert s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]==s["schema_version"]
 assert l["binding"]["reviewed_state_version"]==s["schema_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"]
 assert any(x.get("event")=="ISSUE_REVISION" and x.get("revision_id")=="TW-OPEN-0005-13CT-RED-ZHI6" and "next_action" in x.get("changed_fields",[]) for x in issue["history"])
 assert "CURRENT ACTION" in issue["next_action"]
 assert any(x["id"]=="OMISSIONS-13CT-DIRECT-RED-ZHI6-20261022" for x in l["checkpoint_log"])
 assert sum(x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS") for x in l["issues"])==11
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L))
 print("TIANWEN_13CT_DIRECT_RED_GENRE_MARKERS_ZHI6_UNRESOLVED=PASS")
