#!/usr/bin/env python3
"""13IW byte identity / foreign modern commentary not classical folio and live state check."""
import json
from pathlib import Path
# Verify historical action text through append-only revisions, not the current instruction.
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
ROOT=Path(__file__).resolve().parents[1]
PATH="docs/research/TIANWEN-13IW-KHS-2114-2-XML-BYTE-IDENTITY-AND-BOOK-JUAN-COLLATION-R1.json"
def load(p=PATH):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(e,state=None,ledger=None):
 assert e["schema"]=="TIANWEN-13IW-KHS-2114-2-XML-BYTE-IDENTITY-AND-BOOK-JUAN-COLLATION-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 assert e["predecessor"]["retained_at_write_status"]=="OFFICIAL_XML_NOT_YET_RETURNED_IN_13IV_RECORD"
 a=e["source"];n=e["negative_control"]
 assert a["run_id"]==40604470633 and a["run_conclusion"]=="success" and a["run_status"]=="completed"
 assert a["artifact_id"]==12780626673
 assert a["official_book_code"]=="0021140000200" and a["https_status"]==200 and a["body_size_bytes"]==5414
 assert a["body_sha256"]=="c8a7de9c9f0ff5a64674153e7dd2048b3e6bb7e6193e0f9f9d18d7fc9106a5b9"
 assert a["xml_description_char_count"]==1759 and a["official_full_description_recovered"]
 assert a["matched_book_title"] and a["matched_2114_2_identity"]
 assert not e["source_authentication"]["physical_original_leaf_verified"]
 assert n["code"]=="21140200" and n["https_status"]==200 and n["body_size_bytes"]==1049
 assert n["body_sha256"]=="2ad17e5106a236287c618d998a840bf89ced6c0d7438ca28c37f3ff81171f6d7"
 assert not n["matched_target_title"] and n["description_char_count"]==0 and n["no_automatic_short_code_to_long_code_equivalence"]
 assert e["source_authentication"]["book29_juan81_83_status"]=="RETRACTED_UNBOUND"
 assert e["firstparty_korean_juan_and_book_scope"]["physical_juan81_82_photo"] is None
 assert e["firstparty_korean_juan_and_book_scope"]["original_gk5553_book29_leaf"] is None
 assert e["firstparty_korean_juan_and_book_scope"]["gk5554_juan81_82"].endswith("NOT_YET_ADJUDICATED_IN_THIS_RECORD")
 assert e["original_ancient_controls"]["older_13EI"]=="RETRACTED"
 assert all(e["original_ancient_controls"][k] is None for k in ("g893_six_original_numeric","gk3467_winter_d1_d7","nlc03130_solar_d30","nlc03130_summer_d14","d5_zero_five_glyph","distinct_fourfen_chudu_bridge"))
 assert e["counts"]=={"matrix":[222,222],"sources":761,"genealogy":[252,238],"open_issues":11,"chart":"CLOSED","algorithm_reopens":0,"ancient_pages_added":0,"ancient_glyph_votes":0,"numerical_winners":0,"lineage_edges_added":0}
 assert not e["transmission_impact"]["edges_supported"]
 s=load("docs/PROJECT-CURRENT-STATE-R1.json") if state is None else state
 l=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json") if ledger is None else ledger
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,902,0)
 focus=s["historical_audit"]["current_focus"]
 assert any(x.startswith("13IW ") for x in focus) and len(focus)==l["binding"]["source_focus_count"]
 assert focus[-1].split(" ",1)[0]==l["binding"]["latest_research_focus_prefix"]
 issue=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and PATH in issue["source_refs"]
 assert all(x in historical_action_view(issue) for x in ("GK03539_00","GK03579_00","GK03269_00","D1-D6","四分","初度","G893","NLC03130 solar D30","NLC03130 summer D14","NULL","13EI","RETRACTED"))
 assert any(h.get("revision_id","").startswith("TW-OPEN-0005-13IW-") and PATH in h.get("evidence_refs",[]) for h in issue["history"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
if __name__=="__main__":
 assert check(load())
 print("TIANWEN_13IW_KHS_OFFICIAL_XML_BYTE_IDENTITY_PASS")
