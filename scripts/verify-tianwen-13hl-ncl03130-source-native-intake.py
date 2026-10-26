#!/usr/bin/env python3
"""13HL bounded NCL03130 first-party interface and UNSENT source-request readiness."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13HL-NCL03130-NATIVE-DETAIL-AND-TARGET-RESEARCH-REQUEST-SPEC-R1.json"
def blob(p):
 b=(ROOT/p).read_bytes()
 return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def check(e):
 assert e["issue_id"]=="TW-OPEN-0005" and e["schema"]=="TIANWEN-13HL-NCL03130-NATIVE-DETAIL-AND-TARGET-RESEARCH-REQUEST-SPEC-R1"
 c=e["provider_controls"];nb=c["indexed_neighbor_example"]
 assert c["catalog_shelfmark"]=="03130" and c["catalog_item_id"]=="549927"
 assert c["source_native_search_entry"].endswith("/Search/Index/1")
 assert c["aggregate_original_source_link_final"]==c["source_native_search_entry"]
 assert nb["book_number"]=="03128" and nb["title"]=="東國史略" and not nb["is_03130_target"]
 assert "/Search/SearchDetail?" in nb["url"] and "SourceID=1" in nb["url"]
 assert c["indexed_neighbor_does_not_infer_target_opaque_item_token"]
 assert not c["exact_03130_native_item_url_obtained"] and not c["exact_03130_native_folio_url_obtained"]
 assert len(e["evidence_requirements"])==5 and not any(x["verified"] for x in e["evidence_requirements"])
 a=e["authorization_firewall"]
 assert not a["contact_or_application_submitted"] and not a["license_granted"]
 assert a["requires_applicant_identity_and_purpose_to_submit"] and not a["user_identifying_information_collected"]
 assert a["research_copy_policy"].endswith("/Index/8") and a["license_reuse_policy"].endswith("/Index/9")
 assert e["source_scope"]["stable_predecessor_blob"]==blob(e["source_scope"]["stable_predecessor_json"])
 assert e["source_scope"]["research_policy_predecessor_blob"]==blob(e["source_scope"]["institutional_research_policy_predecessor"])
 t=e["source_scope"]
 assert t["local_original_d14_full_numeral"] is None and t["local_original_d14_terminal"] is None
 assert t["volume52_old_or_supplement_layer"] is None and t["historical_ancient_unit"] is None
 assert t["四分_初度_equivalence"] is None and t["old_day5_〇_五"]==t["g893_six"]=="OPEN"
 assert t["nikh_photo4_scoped_reading"]=="四分六六三〇" and t["inherited_13ei"]=="RETRACTED"
 assert e["evidence_effect"]=={"new_registry_entries":0,"new_physical_witnesses":0,"new_target_original_glyphs":0,"new_genealogy_nodes":0,"new_genealogy_edges":0,"algorithm_reopens":0,"candidate_collapses":0,"research_request_sent":False}
 assert e["invariants"]=={"matrix":[222,222],"sources":761,"graph":[252,238],"open_issues":11,"chart":"CLOSED"} and e["transmission_impact"]=="NONE"
 s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
 l=json.loads((ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf8"))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]=="1.866.0"
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]=="13HL" and s["historical_audit"]["current_focus"][-1].startswith("13HL ")
 i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert i["priority"]=="P0" and i["status"]=="OPEN" and i["next_action"].startswith("13HL CURRENT ACTION:")
 assert "ARCHIVED 13HK PRIOR ACTION:" in i["next_action"]
 assert "docs/research/TIANWEN-13HL-NCL03130-NATIVE-DETAIL-AND-TARGET-RESEARCH-REQUEST-SPEC-R1.json" in i["source_refs"] and "docs/research/TIANWEN-13HL-NCL03130-NATIVE-DETAIL-AND-TARGET-RESEARCH-REQUEST-SPEC-R1.md" in i["source_refs"]
 assert i["history"][-1]["revision_id"].startswith("TW-OPEN-0005-13HL-") and "next_action" in i["history"][-1]["changed_fields"]
 return True
if __name__=="__main__":
 print("TIANWEN_13HL_NCL03130_REQUEST_SPEC_PASS" if check(json.loads(E.read_text(encoding="utf8"))) else "FAIL")
