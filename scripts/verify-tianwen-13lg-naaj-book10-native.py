#!/usr/bin/env python3
"""13LG: direct NAAJ book10 original image checks, never invent copy stemma."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13LG-NAJDA-2810037-BOOK10-J35-P6-ORIGINAL-23897709-R1.json"
def load():return tuple(json.loads((ROOT/f).read_text(encoding="utf-8")) for f in (E,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13LG-NAJDA-2810037-BOOK10-J35-P6-ORIGINAL-23897709-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 a=e["archive"];f=e["original_pdf"];p,q=e["page_collation"];c=e["comparison"]
 assert a["reference_code"]=="281-0037" and a["source_book_number"]==10 and a["original_title_page_verifies_historical_juan35"]
 assert not a["exact_1739_physical_impression_proved"] and not a["shared_printing_blocks_with_2810038_harvard_proved"]
 assert f["bytes"]==9931786 and f["pages"]==51 and f["sha1"]=="8d846026d8be21e3407a395421417a1323dfb421"
 assert f["sha256"]=="8892b16c3b8e17f12211195cf7b58acfd5b7dc0d0aefca6623f653a04d4da93e"
 assert f["github_actions_source_run_id"]==41008895126 and f["github_actions_artifact_id"]==12956527752 and f["hash_verified_against_mediawiki_original_metadata"] and f["independently_read_original_pdf_from_artifact"]
 assert p["pdf_page"]==2 and p["chapter_title"]=="明史卷三十五" and p["roi_xyxy"]==[470,60,590,400] and p["roi_rgb_sha256"]=="1b3be2524398737a8d4561bb241915c28b0eaaf22bad55251a29d15aef26aed0"
 assert q["pdf_page"]==6 and q["original_printed_text"]=="有閏加二十三萬八九七七○九" and q["normalized_numeric_basic_units"]=="238977.09" and q["roi_xyxy"]==[590,85,642,712] and q["roi_rgb_sha256"]=="e3099ff2b939cc3df01112b10978f32710ddc95243c386259e3fe81edff4b90f"
 assert p["full_page_rgb_sha256"]=="738bed76d0fc1599dee67f5854041e0ffc4a9e2ac942df5f3697a9539ed4dba7" and q["full_page_rgb_sha256"]=="a90105202278a2cd0a4c6fb06e7840a673a3d342882f1c6c6ed02e30d49a1913"
 assert c["historical_independent_textual_recensions_added"]==0 and not c["edition_stemma_judged"] and not c["causal_copying_direction_judged"] and c["g893_six_historically_adjudicated_winners"]==0 and c["algorithm_reopens"]==0
 assert e["unchanged_scope"]==dict(source_registry_root=647,source_registry_extension=118,source_registry_total=765,historical_matrix_rows=222,historical_matrix_audited=222,genealogy_nodes=252,genealogy_edges=238,p0_p1_issues_open=11,product="CLOSED")
 assert not e["transmission_impact"]["edges_supported"] and not e["transmission_impact"]["edges_revised"]
 focus=s["historical_audit"]["current_focus"];b=l["binding"]
 assert any(x.startswith("13LG ") for x in focus) and b["source_focus_count"]==len(focus) and b["latest_research_focus_prefix"]==focus[-1].split(" ",1)[0]
 assert s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]==b["reviewed_state_version"]==l["checkpoint_log"][-1]["state_version"]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0" and issue["next_action"].startswith(b["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert E in issue["source_refs"] and E[:-5]+".md" in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13LG-NAJDA2810037-ORIGINAL-20261030" for x in issue["history"])
 assert "13LG CURRENT ACTION:" in issue["next_action"] and "13LF CURRENT ACTION:" in issue["next_action"] and "13JM CURRENT ACTION:" in issue["next_action"] and "RETRACTED" in issue["next_action"]
 assert len(l["issues"])==11 and s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
 return {"status":"PASS","confirmed_original_book10_juan35":True,"confirmed_numeric_original":"238977.09","historical_winners":0,"new_independent_recensions":0}
if __name__=="__main__":print(json.dumps(check(*load()),ensure_ascii=False))
