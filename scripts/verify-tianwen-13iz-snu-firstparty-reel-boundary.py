#!/usr/bin/env python3
"""13IZ firstparty SNU 32-volume PDF service: no ancient physical-folio inference."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13IZ-SNU-GK5553-GK5554-FIRSTPARTY-VOLLIST-ACCESS-BOUNDARY-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
def get(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(e=None,state=None,ledger=None,manifest=None):
 e=get(E) if e is None else e
 state=get(S) if state is None else state
 ledger=get(L) if ledger is None else ledger
 manifest=get(M) if manifest is None else manifest
 assert e["schema"]=="TIANWEN-13IZ-SNU-GK5553-GK5554-FIRSTPARTY-VOLLIST-ACCESS-BOUNDARY-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 src=e["evidence_source"];a=e["official_5553"];b=e["official_5554"];lim=e["evidence_boundary"];old=e["prior_13iy"]
 assert src["run_id"]==40633848115 and src["job_id"]==122636165639 and src["artifact_id"]==12792772609
 assert src["artifact_zip_sha256"]=="017ba403723c25f3113463a2196c4715e9bab04df7f78ea48609a54ffafaa83e"
 assert src["public_post_url"]=="https://kyudb.snu.ac.kr/ajax/book/mfPdfList.do"
 assert src["catalog_gk5553"]=="https://kyudb.snu.ac.kr/book/view.do?book_cd=GK05553_00"
 assert src["catalog_gk5554"]=="https://kyudb.snu.ac.kr/book/view.do?book_cd=GK05554_00"
 assert src["test_count"]==10
 assert a["catalog_request_status"]=="TRANSPORT_ERROR" and a["public_catalog_html_acquired"] is False
 assert a["provider_volumes_response"] is a["physical_book12_folio"] is a["physical_book29_folio"] is None
 assert a["negative_original_absence_proven"] is False
 assert b["catalog_request_status"]=="CAPTURED" and b["source_emitted_exact_book_identity"] is True
 assert b["source_emitted_mfPdfList_endpoint"] is True and b["source_emitted_exact_onclick_for_5554"] is False
 assert b["public_ajax_http"]==200 and b["raw_json_bytes"]==6263
 assert b["raw_json_sha256"]=="af2c8082894765fa9752121b2ff29894f1c0d8848637f4d99817186226d97410"
 assert b["result_literal"]=="SUCCESS" and b["volList_count"]==32 and b["provider_books"]==["GK05554_00"]
 assert b["volume_no_lower"]=="0001" and b["volume_no_upper"]=="0032"
 assert b["all_item_cd"]=="GJB" and b["all_is_pdf"]=="N"
 assert len(b["source_emitted_microfilm_labels"])==7
 assert all("5553" in v and "M/F74-102-17-" in v for v in b["source_emitted_microfilm_labels"])
 assert all(b[k] is False for k in ("item_volumes_are_exact_original_folio_proof","all_32_volumes_printed_original_images_acquired","other_image_service_absence_proven"))
 assert b["gk5554_books17_18_juan81_82_physical_titles"] is None
 assert all(v is True for k,v in lim.items() if k!="previous_13IO_book29_to_juan81_83")
 assert lim["previous_13IO_book29_to_juan81_83"]=="RETRACTED_UNBOUND"
 assert old["firstparty_khs_manuscript_books"]==[8,12,26] and old["firstparty_snu_catalog_manuscript_books"]==[8,26,29] and old["book12_29_winner"] is None
 assert all(v is None for k,v in e["pending_ancient"].items() if k!="erroneous_13ei")
 assert e["pending_ancient"]["erroneous_13ei"]=="RETRACTED"
 assert e["impact"]=={"historical_matrix":[222,222],"root_sources":647,"extension_sources":116,"total_sources":763,"genealogy_nodes":252,"genealogy_edges":238,"open_issues":11,"chart":"CLOSED","algorithms_reopened":0,"new_original_ancient_pages":0,"new_ancient_numeric_winners":0,"new_transmission_edges":0,"source_registry_entries_added":0}
 assert e["transmission_impact"]["edges_supported"]==[]
 assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,state["schema_version"].split(".")))>=(1,905,0)
 assert manifest["combined_source_count"]==state["historical_audit"]["external_source_registry_total_unique_count"]>=763
 assert manifest["root_source_count"]==647 and manifest["combined_source_count"]==manifest["root_source_count"]+manifest["extension_source_count"]
 assert any(x.startswith("13IZ ") for x in state["historical_audit"]["current_focus"])
 assert ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert len(state["historical_audit"]["current_focus"])==ledger["binding"]["source_focus_count"]
 issue=next(i for i in ledger["issues"] if i["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN" and {E,E.replace(".json",".md")}.issubset(set(issue["source_refs"]))
 assert issue["next_action"].startswith(ledger["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert any(h.get("revision_id","").startswith("TW-OPEN-0005-13IZ-") and h.get("previous_next_action","").startswith("13IY CURRENT ACTION:") for h in issue["history"])
 assert all(k in issue["next_action"] for k in ("GK05553_00","GK05554_00","G893","GK03539_00","GK03579_00","GK03269_00","D1-D6","四分","初度","NLC03130 solar D30","NLC03130 summer D14","NULL","13EI","RETRACTED"))
 assert any(x.get("revision_id","").startswith("TW-OPEN-0005-13IZ-") and E in x.get("evidence_refs",[]) for x in issue["history"])
 assert ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
 return True
if __name__=="__main__":
 assert check()
 print("TIANWEN_13IZ_FIRSTPARTY_32_N_PDF_VOLUMES_NO_ANCIENT_FOLIO_PASS")
