#!/usr/bin/env python3
"""13LE direct NAAJ original page numeric and term collation; preserve copy/impression evidence firewall."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13LE-NAJDA-2810038-J35-P6-ORIGINAL-23897709-P14-CHIJILI-R1.json"
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (E,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def guard(ok,why):
 if not ok:raise ValueError(why)
def check(e,s,l):
 guard(e["schema"]=="TIANWEN-13LE-NAJDA-2810038-J35-P6-ORIGINAL-23897709-P14-CHIJILI-R1" and e["issue_id"]=="TW-OPEN-0005","record identity")
 x=e["original_file"];h=e["archive_holding"];p,q=e["page_collation"];c=e["comparison"];scope=e["scope"]
 guard(x["sha1"]=="984fbeb6db2e5dd16ffe40133747732d87b0fd40" and x["sha256"]=="73322281149551c76f96008c1b9f3933e817543f7cb8710c92268ade9ca031eb" and x["bytes"]==15476093 and x["pdf_pages"]==73,"binary hashes")
 guard(x["github_actions_original_artifact_id"]==12954898597 and x["post_download_local_sha256_matches"] and x["non_ocr_human_visual_review_completed"] and x["pdf_creation_metadata_not_copy_impression_date"],"native acquisition")
 guard(h["item_reference_code"]=="281-0038" and h["target_book_number"]=="0011" and h["historic_chapter"]=="明史卷三十五 / 志第十一" and not h["physical_1739_impression_directly_verified"] and not h["same_printing_blocks_as_harvard_proven"],"specific holding")
 guard(p["pdf_page_1_based"]==6 and p["roi_xyxy"]==[609,90,673,728] and p["image_size"]==[1117,811] and p["full_page_rgb_sha256"]=="f5963e5ce75039038ce4aee42655e1ecef6224b36ed9411cc6072c0fba793cb4" and p["roi_rgb_sha256"]=="77152d36d6317ada3e767c7da631b0de10823e1142a757adfa3ffbc55f6c241d" and p["original_native_printed_reading"]=="有閏加二十三萬八九七七○九" and p["normalized_number_basic_units"]=="238977.09","native numerical page")
 guard(q["pdf_page_1_based"]==14 and q["roi_xyxy"]==[137,89,256,720] and q["full_page_rgb_sha256"]=="3231e1ba936a2fe1cba168150b3a12cec2d18add8e78c0209297eee172ac79fa" and q["roi_rgb_sha256"]=="148151c47ffeb3f2a56e203a6b95bfafdc71cee093852e7657734b6b9e0bb397" and q["original_native_printed_reading"]=="推平交入轉遲疾歷","native distinct term")
 guard(c["harvard_p7_normalized_basic_units"]=="238977.09" and c["cadal_siku_p11_normalized_basic_units"]=="288977.09" and c["numerical_delta_basic_units"]=="50000" and not c["ancient_copying_direction_historically_established"] and not c["publisher_same_impression_harvard_naaj_established"] and c["independent_textual_recension_votes_new"]==0 and c["new_g893_historically_adjudicated_numeric_winners"]==0,"evidence scope")
 guard(scope==dict(source_registry_total=765,matrix_rows_audited=222,graph_nodes=252,graph_edges=238,open_risks=11,registered_sources_added=0,original_historical_numeric_winners_added=0,transmission_nodes_added=0,transmission_edges_added=0,chart_algorithm_reopens=0,product="CLOSED"),"unchanged invariants")
 guard(s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]==l["binding"]["reviewed_state_version"]==l["checkpoint_log"][-1]["state_version"],"state version")
 focus=s["historical_audit"]["current_focus"]
 guard(any(z.startswith("13LE ") for z in focus) and l["binding"]["source_focus_count"]==len(focus) and focus[-1].split(" ",1)[0]==l["binding"]["latest_research_focus_prefix"],"forward-compatible focus")
 issue=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
 guard(issue["status"]=="OPEN" and issue["priority"]=="P0" and issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:") and E in issue["source_refs"] and "docs/research/TIANWEN-13LE-NAJDA-2810038-J35-P6-ORIGINAL-23897709-P14-CHIJILI-R1.md" in issue["source_refs"],"risk record")
 guard(any(z.get("revision_id")=="TW-OPEN-0005-13LE-NAJDA-P6-P14-20261030" for z in issue["history"]),"append only")
 guard(len(l["issues"])==11 and s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0,"product")
 return {"status":"PASS","original_naaj_2810038_pdf_page6":"238977.09","same_glyph_as_harvard":True,"siku_cadal_original":"288977.09","numeric_historical_winners":0,"independent_recension_votes_new":0}
if __name__=="__main__":print(json.dumps(check(*load()),ensure_ascii=False))
