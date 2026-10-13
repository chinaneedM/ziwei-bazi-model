#!/usr/bin/env python3
"""12VF: scope an additional 及 glyph variant and quarantine noninstitutional catalog leads."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12VF-SHENZHEN-XI-WEI-JI-ZI-RECEIVED-VARIANT-R1.json"
LEADS="docs/research/MING-DATONG-YEHUOBIAN-12VF-THREE-SECONDARY-HOLDINGS-QUARANTINE-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
PZ="docs/research/MING-DATONG-YEHUOBIAN-12PZ-RECEIVED-PREFACE-JUAN-COUNT-TEXTUAL-VARIANTS-R1.json"
VE="docs/research/MING-DATONG-YEHUOBIAN-12VE-THREE-PREDICATES-OF-SHENZHEN-PARATEXT-R1.json"
def validate(r,leads,st,pz,ve):
 if r.get("schema")!="TIANWEN-12VF-SHENZHEN-XI-WEI-JI-ZI-RECEIVED-VARIANT-R1" or r.get("status")!="TWO_RECEIVED_VARIANTS_NO_PHYSICAL_WINNER": raise ValueError("received variant schema")
 if ve["predicates"][0]["wording"]!="惜未梓" or r["forward_correction"]["earlier_12ve_printing_wording"]!="惜未梓": raise ValueError("forward correction does not match prior")
 ws=r.get("witnesses",[])
 if len(ws)!=2 or [w.get("id") for w in ws]!=["WIKISOURCE_RECEIVED","CTEXT_RECEIVED"]: raise ValueError("two witnessed groups")
 if ws[0]["url"]!=pz["received_text_groups"][0]["url"].replace("/wiki/%E8%90%AC%E6%9B%86%E9%87%8E%E7%8D%B2%E7%B7%A8","/zh-hans/萬曆野獲編") or "ctext.org/wiki.pl?chapter=938703" not in ws[1]["url"]: raise ValueError("known reading routes")
 for w in ws:
  if w["direct_original_folio_seen"] is not False or w["edition_physical_copy_identified"] is not False: raise ValueError("false original source")
 if [w["readings"]["PRINTING_CLAUSE"] for w in ws]!=["惜未梓","惜未及梓"]: raise ValueError("variant not preserved")
 if [w["readings"]["CONTINUATION_JUAN_COUNT"] for w in ws]!=["十二卷","十卷"]: raise ValueError("existing volume variants")
 loc=r["loci"]
 if len(loc)!=2 or loc[0]["id"]!="BU_YI_XU_PRINTING_WORDING" or loc[1]["id"]!="BU_YI_XU_CONTINUATION_NUMBER": raise ValueError("loci")
 if loc[0]["readings"]!={"WIKISOURCE_RECEIVED":"惜未梓","CTEXT_RECEIVED":"惜未及梓"}: raise ValueError("locus wording")
 if loc[1]["readings"]!={"WIKISOURCE_RECEIVED":"十二卷","CTEXT_RECEIVED":"十卷"}: raise ValueError("locus numerals")
 if any(l["physical_print_glyph_authority"] is not False or l["independent_voting_allowed"] is not False for l in loc): raise ValueError("unearned glyph")
 gate=r.get("forward_correction",{})
 if len(gate)!=9 or any(gate.get(k) is not True for k in ("earlier_record_unchanged","no_alternative_winner_selected","no_recension_pairing_proved_from_two_websites","ctext_direct_source_html_not_claimed","quote_origin_or_1713_physical_copy_unverified","text_variation_does_not_change_12ve_three_predicates","no_1827_1869_target_glyph_inference")): raise ValueError("source scope")
 if leads.get("schema")!="TIANWEN-12VF-SECONDARY-1827-HOLDING-LEADS-QUARANTINE-R1" or leads.get("status")!="SECONDARY_CATALOG_LEADS_ONLY_NO_INSTITUTIONAL_ITEM_CONFIRMATION": raise ValueError("leads schema")
 q=leads.get("leads",[])
 if len(q)!=3 or [x.get("key") for x in q]!=["HENAN_UNIVERSITY","TSINGHUA_UNIVERSITY","SHANDONG_UNIVERSITY"]: raise ValueError("lead groups")
 for x in q:
  if x["provider_verified"] is not False or x["provider_catalog_item_id"] is not None or x["image_url"] is not None or x["page_sha256"] is not None or x["target_glyph_votes"]!=0 or x["original_juan20_target_available"] is not False: raise ValueError("secondary promoted to physical")
 if any(leads[k] is not False for k in ("eight_candidate_source_issue_queue_modified","tertiary_leads_added_as_verified_physical_copies")): raise ValueError("prior eight candidate source queue changed")
 if leads["no_inference_from_7_copies_about_juan20_missing"] is not True or leads["no_inference_from_34_copies_about_complete_1827_setting"] is not True: raise ValueError("extent overclaim")
 for a in (r["accounting"],leads["accounting"]):
  for k,v in a.items():
   if k.startswith("new_") and v!=0: raise ValueError("unearned increment")
 if (r["accounting"]["root_sources"],r["accounting"]["extension_sources"],r["accounting"]["total_sources"],r["accounting"]["matrix_rows"],r["accounting"]["audited_rows"],r["accounting"]["genealogy_nodes"],r["accounting"]["genealogy_edges"],r["accounting"]["formal_batches"],r["accounting"]["latest_formal"])!=(647,43,690,222,222,252,238,487,"12QD"): raise ValueError("immutable batch snapshot")
 h=st["historical_audit"]
 if tuple(map(int,st["schema_version"].split(".")))<(1,562,0) or not any(x.startswith("12VF ") for x in h["current_focus"]): raise ValueError("handoff")
 if h["external_source_registry_total_unique_count"]<690 or h["row_count"]!=222 or h["audited_row_count"]!=222 or st["invariants"]["algorithm_reopen_count"]!=0: raise ValueError("live state regression")
 return {"status":"PASS","new_reading_loci":1,"independent_original_glyph_votes":0,"secondary_unverified_leads":3}
def verify(root=ROOT):
 def j(p):return json.loads((root/p).read_text(encoding="utf-8"))
 return validate(j(REC),j(LEADS),j(STATE),j(PZ),j(VE))
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False,sort_keys=True))
