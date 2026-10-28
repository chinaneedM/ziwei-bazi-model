#!/usr/bin/env python3
"""13JB firstparty SNU vol18 TOC: authenticated HTML, not ancient original."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13JB-GK5554-BOOK18-JUAN80-82-SOURCE-EMITTED-TOC-R1.json";S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def get(p):return json.loads((R/p).read_text(encoding="utf-8"))
def check(e=None,s=None,l=None):
 e=get(E) if e is None else e;s=get(S) if s is None else s;l=get(L) if l is None else l
 assert e["schema"]=="TIANWEN-13JB-GK5554-BOOK18-JUAN80-82-SOURCE-EMITTED-TOC-R1" and e["issue_id"]=="TW-OPEN-0005"
 a=e["source"];p=e["page_metadata"];c=e["corroboration_scope"];im=e["impact"]
 assert a["url"]=="https://kyudb.snu.ac.kr/book/text.do?item_cd=GJB&book_cd=GK05554_00&vol_no=0018"
 assert a["original_observation_run"]==40634324150 and a["original_observation_job"]==122637665741 and a["artifact_id"]==12792862189
 assert a["raw_bytes"]==174564 and a["raw_html_sha256"]=="31c9afa4e92d68b6ec728758c20ca4cd0787c91a5690cbcd222bf8febdd13374"
 assert a["artifact_zip_sha256"]=="69af32187eb18899facbbfe27b471a72bd7f3356a0e7254b0f0fb75817e58ee5"
 assert a["retrieval_13ja"]=="HTTP_200_FIRSTPARTY_HTML" and a["followup_13jb"]=="TRANSPORT_ERROR_NO_NEW_BYTE_PROOF"
 assert a["manual_bounded_index_extraction_with_no_ocr"] is True
 assert p["digital_vol_no"]=="0018" and p["shelfmark"]=="奎貴5554" and p["first_named_page"]=="001a"
 assert p["bookinfo_html"]=='<div class="bookinfo" data-vol_no="0018" data-page_no="001a" data-ori_title="高麗史" data-kor_title="고려사" data-call_no="奎貴5554">'
 assert p["ancient_physical_book_no_inferred"] is False and p["impression_year_from_html"] is None
 t=e["source_emitted_toc"]
 assert [(x["work_juan"],x["page_no"]) for x in t]==[(80,"001a"),(81,"048a"),(82,"085a")]
 assert [x["rubric"] for x in t]==["志 卷第34 食貨3","志 卷第35 兵1","志 卷第36 兵2"]
 assert [x["literal_heading"] for x in t]==["▶卷80 志 卷第34 食貨3","▶卷81 志 卷第35 兵1","▶卷82 志 卷第36 兵2"]
 assert [x["onclick"] for x in t]==[f"fn_originalImg('GJB','GK05554_00' ,'0018','{page}');" for page in ("001a","048a","085a")]
 assert all(x["photo_bytes"] is None and x["original_folio_glyph_verified"] is False for x in t)
 assert c["khs_2114_2_book_span"]==[17,18] and c["khs_2114_2_juan_span"]==[79,80,81,82]
 assert c["snu_digital_vol18_juan_list"]==[80,81,82] and c["snu_digital_vol17_original_heading"] is None
 assert c["can_infer_vol17_exact_juan79_from_complement"] is False and c["can_assign_antique_physical_folio_page"] is False
 assert c["gk5553_book29_to_81_83"]=="RETRACTED_UNBOUND"
 assert all(v is None for v in e["still_missing"].values())
 assert all(v is True for v in e["safeguards"].values())
 assert e["prior_13iy_firstparty_conflict"]=={"official_gov_manuscript_books":[8,12,26],"snu_catalog_manuscript_books":[8,26,29],"preferred_candidate":None}
 assert im=={"matrix":[222,222],"sources":763,"graph_nodes":252,"graph_edges":238,"issues":11,"chart":"CLOSED","ancient_page_images_added":0,"historical_numeric_winners":0,"algorithm_reopens":0,"original_physical_copy_votes":0}
 assert e["transmission_impact"]["edges_supported"]==[]
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,906,0)
 assert s["historical_audit"]["external_source_registry_total_unique_count"]>=im["sources"]
 assert any(x.startswith("13JB ") for x in s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0" and {E,E.replace(".json",".md")}.issubset(set(issue["source_refs"]))
 assert issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert all(k in issue["next_action"] for k in ("GK05554_00","0018","048a","085a","GK05553_00","G893","NLC03130 solar D30","NLC03130 summer D14","D1-D6","四分","初度","13EI","RETRACTED"))
 assert any(x.get("revision_id","").startswith("TW-OPEN-0005-13JB-") and E in x.get("evidence_refs",[]) for x in issue["history"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
if __name__=="__main__":
 assert check()
 print("13JB_PASS_GK5554_DIGITAL_VOL0018_JUAN80_81_82_TOC_NO_ANCIENT_FOLIO")
