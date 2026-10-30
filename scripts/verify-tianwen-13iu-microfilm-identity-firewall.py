#!/usr/bin/env python3
"""13IU: fail closed when an M/F label is promoted across independent shelfmarks."""
import hashlib,json
from pathlib import Path
# Verify historical action text through append-only revisions, not the current instruction.
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-13IU-GK5553-GK5554-MICROFILM-IDENTITY-FIREWALL-R1.json"
def load(path=DOC):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(e,*,state=None,ledger=None):
 assert e["schema"]=="TIANWEN-13IU-GK5553-GK5554-MICROFILM-IDENTITY-FIREWALL-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 prior=e["predecessor"]
 raw=(ROOT/prior["path"]).read_bytes()
 assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==prior["immutable_blob_sha"]
 a,b=e["firstparty_records"]["GK05553_00"],e["firstparty_records"]["GK05554_00"]
 assert a["catalog_shelfmark"]=="奎貴5553-v.1-46" and a["catalog_volume_total"]==46
 assert a["supplemental_manuscript_books"]==a["designation_excluded_book_numbers"]==[8,26,29]
 assert b["catalog_shelfmark"]=="奎貴5554" and b["catalog_volume_count"]==32
 assert b["catalog_description"]=="零本32冊"
 assert b["independently_labeled_gk5554_microfilm_entry_present"] is False
 assert not a["book29_original_leaf_obtained"] and not b["physical_juan81_82_original_leaf_obtained"]
 expected=[(1,9),(10,16),(17,24),(25,31),(32,38),(39,43),(44,46)]
 for record in [a,b]:
  items=record["microfilm_list"]
  assert len(items)==7
  for i,item in enumerate(items):
   assert item["code"]==f"M/F74-102-17-{i+1}"
   assert item["displayed_subject"]=="GK05553"
   assert tuple(item["listed_volume_range"])==expected[i]
 assert a["microfilm_list"]==b["microfilm_list"]
 her=e["official_heritage_index"]
 assert (her["described_juan"],her["described_books"])==(98,32)
 assert not her["direct_korean_detailed_description_obtained"] and not her["physical_impression_exact_year_proven"]
 c=e["comparison"]
 assert c["both_detail_pages_list_same_seven_mf_labels"] is True
 assert c["listed_microfilm_all_identify_other_holding_in_gk5554_detail"] is True
 assert c["gk5554_microfilm_independent_identity"]=="UNBOUND_BY_LISTED_LABELS"
 assert c["copy_or_link_template_cause"]=="UNKNOWN_DO_NOT_INFER_SITE_BUG_OR_FALSE_PHYSICAL_OBJECT"
 assert c["source_5553_volume29_to_juan81_83"]=="RETRACTED_UNBOUND"
 assert c["no_claim_that_gk5554_original_is_absent"] and c["no_claim_that_every_shown_image_is_gk5553"]
 assert c["separate_crosswalks_required"]==["CATALOG_RECORD_ID","MICROFILM_DISPLAY_SUBJECT","SERVED_IMAGE_COPY_ID","BOOK_NUMBER","JUAN","TARGET_PHYSICAL_LEAF","DATE_LAYER"]
 assert e["active_unresolved_targets"]=={"GK3467_WINTER_TITLE_D1_D7":None,"G893_SIX_NUMERIC_CONTROLS":None,"NLC03130_SOLAR_D30":None,"NLC03130_SUMMER_D14":None,"GK5553_5554_JUAN81_82_COPY_COMPARISON":None,"D5_ZERO_FIVE_GLYPH":None,"HISTORICAL_13EI_STATUS":"RETRACTED"}
 assert e["counts"]=={"matrix":[222,222],"external_sources":761,"genealogy":[252,238],"open_risks":11,"chart":"CLOSED","algorithm_reopens":0,"candidate_collapses":0,"new_ancient_pages":0,"new_source_entries":0,"new_genealogy_edges":0}
 assert e["transmission_impact"]["edges_supported"]==[]
 s=state if state is not None else load("docs/PROJECT-CURRENT-STATE-R1.json")
 l=ledger if ledger is not None else load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert tuple(map(int,s["schema_version"].split("."))) >= (1,900,0)
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 focus=s["historical_audit"]["current_focus"]
 assert any(x.startswith("13IU ") for x in focus)
 assert l["binding"]["source_focus_count"]==len(focus)
 assert l["binding"]["latest_research_focus_prefix"]==focus[-1].split(" ",1)[0]
 issue=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert DOC in issue["source_refs"]
 assert "13IO" in historical_action_view(issue) and "RETRACTED" in historical_action_view(issue)
 assert all(z in historical_action_view(issue) for z in ("四分","初度","NLC03130 solar D30","NLC03130 summer D14","13EI","NULL","D1-D6","GK03539_00"))
 assert any(h.get("revision_id","").startswith("TW-OPEN-0005-13IU-") and DOC in h.get("evidence_refs",[]) for h in issue["history"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
if __name__=="__main__":
 assert check(load())
 print("TIANWEN_13IU_CROSS_HOLDING_MICROFILM_FIREWALL_PASS")
