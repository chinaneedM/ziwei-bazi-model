#!/usr/bin/env python3
"""13JS late-source editorial basis citation does not bind 1972 original folio."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13JS-TAKEDA2005-1972-ASIA-CITATION-AND-ORIGINAL-COPY-SCOPE-R1.json"
def load():
 return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in (P,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def verify(e,s,l):
 assert e["schema"]=="TIANWEN-13JS-TAKEDA2005-1972-ASIA-EDITORIAL-CITATION-SCOPE-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 p=e["primary_later_publication"]
 assert (p["title"],p["editor"],p["publisher"],p["publication_year"],p["japanese_cinii_ncid"],p["volumes"])==("高麗史日本伝","武田幸男","岩波書店",2005,"BA71855261",2)
 assert p["editorial_note_recorded_in_cinii_and_teikyo"]
 assert [x["ndl_bib_id"] for x in p["ndls"]]==["000007771747","000007856539"]
 assert all(p[k] is False for k in ("facsimile_1972_original_title_page_directly_examined","later_2005_printed_preface_directly_examined","original_gk5553_or_gk5554_physical_folio_directly_examined"))
 assert [x["ncid"] for x in e["target_1972_catalog_records"]]==["BA63617326","BB04922175"]
 a=e["adjudication"]
 for k in ("editorial_basis_mentions_asia_1972_three_volumes","later_japanese_publication_bibliography_is_separate_later_work","does_not_identify_exact_1972_cinii_ncid","does_not_prove_1972_composition_of_original_gk5554_vs_woodblock_supplements","does_not_supply_1972_copy_title_colophon_or_juan52_photograph","no_independent_ancient_physical_witness","previous_1972_yonsei_four_volume_is_not_automatically_same_source"):
  assert a[k] is True,k
 assert a["khs_8_12_26_vs_snu_8_26_29"]=="OPEN" and a["old_13io_physical_book29"]=="RETRACTED_UNBOUND"
 assert a["deterministic_product"]=="CLOSED"
 for k in ("g893_original_numeric_target_decisions_this_batch","new_original_1972_pages","new_ancient_physical_copy_votes","source_registry_growth","genealogy_nodes_added","genealogy_edges_added","algorithm_reopens"):
  assert a[k]==0,k
 assert e["transmission_impact"].startswith("NO_GRAPH_CHANGE_")
 focus=s["historical_audit"]["current_focus"]
 assert any(x.startswith("13JR ") for x in focus) and any(x.startswith("13JS ") for x in focus)
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(focus)
 assert l["binding"]["latest_research_focus_prefix"]==focus[-1].split(" ",1)[0]
 issue=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert P in issue["source_refs"] and P.replace(".json",".md") in issue["source_refs"]
 matches=[(idx,v) for idx,v in enumerate(issue["history"]) if v.get("revision_id")=="TW-OPEN-0005-13JS-2005-TAKEDA1972-CITATION-SCOPE-20261028"]
 assert len(matches)==1
 ix,revision=matches[0]
 assert revision["event"]=="ISSUE_REVISION" and revision["evidence_refs"]==[P,P.replace(".json",".md")]
 old=[i for i,r in enumerate(issue["history"]) if r.get("revision_id","").startswith("TW-OPEN-0005-13JR-")]
 assert old and old[-1]<ix
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 assert set(l["checkpoint_log"][-1]["reviewed_issue_ids"])=={i["id"] for i in l["issues"]}
 return {"status":"PASS","modern_editorial_basis_note":1,"ancient_copies_added":0,"source_registry_growth":0}
if __name__=="__main__":
 print(json.dumps(verify(*load()),ensure_ascii=False))
