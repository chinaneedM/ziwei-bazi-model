#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
THIS="docs/research/TIANWEN-12ZK-GORYEOSA-GK05553-GK05554-SHARED-TOC-NONHOLDINGS-FIREWALL-R1.json"
OLD="docs/research/TIANWEN-12ZJ-GORYEOSA-5554-13941-NUMBERING-CENSUS-FIREWALL-R1.json"
def load():
 return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in (THIS,OLD,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def chk(c, m):
 if not c: raise ValueError(m)
def verify(d,old,state,ledger):
 chk(d["schema"]=="TIANWEN-12ZK-GORYEOSA-SHARED-TOC-NONHOLDINGS-FIREWALL-R1" and d["prior"]==OLD,"batch identity")
 a,b=d["items"];x=d["shared_fields"];q=d["boundaries"]
 chk(a["item"]=="GK05553_00" and a["description"]=="139卷, 卷首, 合46冊" and a["supplementary_manuscript_books"]==[8,26,29],"5553")
 chk(b["item"]=="GK05554_00" and b["description"]=="零本32冊" and b["heritage"]=="2114-2","5554")
 chk(a["impression"]==b["impression"]=="[刊年未詳]","impression period")
 chk(x["work_toc_5553"]==x["work_toc_5554"] and "卷50-52:曆志" in x["work_toc_5553"],"duplicated work TOC")
 chk(x["item_note_5553"]==x["item_note_5554"] and "32冊外缺" in x["item_note_5553"],"shared catalog note")
 chk(x["microfilm_5553"]==x["microfilm_5554"] and "奎 5553/" in x["microfilm_5554"] and x["microfilm_all_seven_lines_identify_5553"],"M/F still 5553")
 chk(not q["work_level_toc_is_copy_specific_fascicle_census"] and q["work52_belongs_to_complete_work_toc"],"no generic toc as holdings")
 for k in ("gk05554_work52_physical_book","gk05554_work52_d16_native_glyph","gk05554_work52_d18_native_glyph","gk05554_original_page_sha256"):
  chk(q[k] is None,"no original " + k)
 for k in ("gk05553_microfilm_licenses_gk05554_original_read","same_edition_catalog_proves_identical_physical_copy","same_edition_catalog_proves_same_impression"):
  chk(q[k] is False,"no cross-object inference "+k)
 chk(q["physical_survivor_98_vs_received_body_95_gap"]=="OPEN","count gap still open")
 for k in ("new_original_targets","new_physical_witnesses","new_registry_sources","new_transmission_edges","algorithm_reopens"):
  chk(q[k]==0,"no fabricated witness "+k)
 chk((q["g893_original_control"],q["g893_cross_independent_copy"],q["open_issues"],q["product"])==("5/6","0/6",11,"CLOSED") and d["transmission_impact"]=="NONE","research firewall")
 chk(old["source"]["kyudb"]["item"]=="GK05554_00" and old["boundaries"]["glyph_5554_d16"] is None,"prior proof boundary")
 issue=next(z for z in ledger["issues"] if z["id"]=="TW-OPEN-0005")
 chk(issue["status"]=="OPEN" and THIS in issue["source_refs"] and THIS.replace(".json",".md") in issue["source_refs"],"issue source crosswalk")
 f=state["historical_audit"]["current_focus"]
 chk(any(z.startswith("12ZK ") for z in f) and len(f)==ledger["binding"]["source_focus_count"] and ledger["binding"]["latest_research_focus_prefix"]==f[-1].split(" ",1)[0],"focus")
 chk(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"version synchronization")
 chk(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={z["id"] for z in ledger["issues"]},"whole ledger reviewed")
 return {"status":"PASS","new_originals":0,"open_issues":11}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
