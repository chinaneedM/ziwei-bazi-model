#!/usr/bin/env python3
"""13IX: bound gov Korean book/juan modern interpretation, never ancient folio."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
J="docs/research/TIANWEN-13IX-KHS-2114-2-DIRECT-KOREAN-JUAN81-82-BOUNDARY-R1.json"
def get(p=J):return json.loads((R/p).read_text(encoding="utf-8"))
def check(x,s=None,l=None):
 assert x["schema"]=="TIANWEN-13IX-KHS-2114-2-DIRECT-KOREAN-JUAN81-82-BOUNDARY-R1"
 assert x["issue_id"]=="TW-OPEN-0005" and x["predecessor"]["retained_13IO"]=="RETRACTED_UNBOUND"
 a=x["firstparty_khs_2114_2"]
 assert a["retrieval_run_13iv"]==40604470633 and a["collation_run_13iw"]==40605206380 and a["collation_artifact_id"]==12780925924
 assert a["raw_sha256"]=="c8a7de9c9f0ff5a64674153e7dd2048b3e6bb7e6193e0f9f9d18d7fc9106a5b9"
 assert a["body_text_sha256_utf8"]=="7f962af9ec2693a558e3a84acd013615850c847b897f827afa2c15d3a976ffc9"
 assert a["raw_bytes"]==5414 and a["description_length"]==1759 and a["collation_run_success"]
 assert x["predecessor"]["path"]=="docs/research/TIANWEN-13IW-KHS-2114-2-XML-BYTE-IDENTITY-AND-BOOK-JUAN-COLLATION-R1.json"
 assert x["predecessor"]["git_blob_sha"]=="0d258482ee423a0712fea119c3b40ecd8020b58d"
 assert a["institution"]=="국가유산청 / Korea Heritage Service"
 assert a["source_url"]=="https://www.khs.go.kr/cha/SearchKindOpenapiDt.do?ccbaKdcd=12&ccbaAsno=0021140000200&ccbaCtcd=11"
 assert a["authentication"]=="DIRECT_OFFICIAL_XML_2114_2_FIRSTPARTY_MODERN_HERITAGE_DESIGNATION_DESCRIPTION"
 b=a["gk5554_bounded_book_range"]
 assert b["physical_book_ordinals"]==[17,18] and b["juan_span"]==[79,80,81,82]
 assert b["official_korean_excerpt"]=="권79∼권82(17책∼18책)"
 assert b["exact_book_to_individual_juan"] is None and b["original_photographed_folio"] is None
 assert b["source_offset_13iw"]==1276
 c=a["gk5554_supplement_to_gk5553_bounded_claim"]
 assert c["gk5554_shelfmark"]=="奎貴5554" and c["gk5553_shelfmark"]=="奎貴5553"
 assert c["missing_in_stated_gk5553_comparison"]==[81,82]
 assert "5553" in c["official_korean_excerpt"] and "권81, 권82" in c["official_korean_excerpt"]
 assert c["official_korean_excerpt"]=="‘奎貴5553’에 없는 권81, 권82를 보완할"
 assert c["source_offset_13iw"]==1631
 assert c["scope"]=="2021_OFFICIAL_DESIGNATED_COPY_COMPARISON_NOT_1553_EVERY_BOOK_PHYSICAL_LEAF"
 assert not c["original_printed_books_collated"]
 assert a["gk5553_comparison_extent"]["juan"]==131 and a["gk5553_comparison_extent"]["books"]==43
 assert a["gk5553_comparison_extent"]["source_offset_13iw"]==1418
 assert a["gk5553_comparison_extent"]["source_label"]=="奎貴5553"
 assert a["gk5553_comparison_extent"]["designation_2114_1_comparator"] is True
 z=x["separate_firstparty_snu_scope"]
 assert z["snu_url"]=="https://kyudb.snu.ac.kr/book/view.do?book_cd=GK05553_00"
 assert z["full_catalog_books"]==46 and z["manuscript_replacement_books"]==z["designated_copy_excluded_books"]==[8,26,29]
 assert z["designated_print_book_count"]==43 and z["government_131_43_does_not_prove_missing_from_all_46"]
 assert z["book29_to_juan81_83"]=="RETRACTED_UNBOUND" and z["book29_original_source_juan"] is None
 assert z["gk5554_direct_image_leaf_unavailable"]
 assert x["lower_authority_record"]["prior_2021_reprinted_text"]=="SECONDARY_DERIVATIVE"
 assert x["lower_authority_record"]["prior_13IT_and_13IU_remain_immutable"] is True
 assert x["lower_authority_record"]["its_5554_supplement_juan81_82_is_now_independently_supported_as_GOVERNMENT_2021_DESCRIPTION"]
 assert x["lower_authority_record"]["its_5553_manuscript_books_8_12_26_is_still_not_verified_by_THIS_2114_2_DESCRIPTION"]
 i=x["interpretive_limits"]
 assert i["can_claim_modern_official_supplement81_82"]
 assert all(i[k] is False for k in i if k!="can_claim_modern_official_supplement81_82")
 assert x["pending_ancient"]["historical_13EI"]=="RETRACTED"
 assert all(x["pending_ancient"][k] is None for k in ("g893_six_original_numeric","gk3467_winter_d1_d7","nlc03130_solar_d30","nlc03130_summer_d14","d5_zero_five","fourfen_to_chudu_original_bridge"))
 assert x["impact"]=={"source_registry_total":761,"matrix":[222,222],"genealogy":[252,238],"issue_count":11,"chart":"CLOSED","algorithm_reopens":0,"new_original_physical_pages":0,"new_ancient_numeric_winners":0,"new_genealogy_edges":0,"one_modern_government_description_source_recovered":True}
 assert x["transmission_impact"]["edges_supported"]==[]
 s=get("docs/PROJECT-CURRENT-STATE-R1.json") if s is None else s
 l=get("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json") if l is None else l
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,903,0)
 focus=s["historical_audit"]["current_focus"]
 assert any(t.startswith("13IX ") for t in focus) and len(focus)==l["binding"]["source_focus_count"] and focus[-1].split(" ",1)[0]==l["binding"]["latest_research_focus_prefix"]
 issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN" and J in issue["source_refs"]
 assert all(v in issue["next_action"] for v in ("GK03539_00","GK03579_00","GK03269_00","D1-D6","四分","初度","G893","NLC03130 solar D30","NLC03130 summer D14","NULL","13EI","RETRACTED"))
 assert any(h.get("revision_id","").startswith("TW-OPEN-0005-13IX-") and J in h.get("evidence_refs",[]) for h in issue["history"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
if __name__=="__main__":
 assert check(get())
 print("TIANWEN_13IX_FIRSTPARTY_GOV_SCOPE_NO_ANCIENT_FOLIO_PASS")
