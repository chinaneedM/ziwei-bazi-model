#!/usr/bin/env python3
"""12VC: a scoped received transcription nonhit does not disprove a 1959 scholarly quotation."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12VC-JINGZHIJU-QUOTE-LOCATOR-BOUNDARY-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
PREV="docs/research/MING-DATONG-YEHUOBIAN-12VA-1959-2019-MING-PRINT-HISTORIOGRAPHY-R1.json"
GUARDS=(
"quotation_absent_in_one_displayed_received_entry_not_absent_in_all_editions",
"1959_author_misattribution_not_proven",
"zhu_yizun_historical_physical_leaf_not_obtained",
"1819_fulishanfang_jingzhiju_is_not_1827_yehuobian",
"current_reproduced_text_is_not_original_glyph_vote",
"ocr_nonhit_does_not_prove_missing_passage",
"an_earlier_comment_on_publication_does_not_establish_ming_print_existence",
"exact_1827_1869_gaizao_original_pages_not_obtained",
"no_historical_rule_selected_or_algorithm_reopened",
"no_external_contact_or_order")
def validate(r,st,prev):
 if r.get("schema")!="TIANWEN-12VC-PANG1959-JINGZHIJU-ATTRIBUTION-LOCATOR-BOUNDARY-R1" or r.get("status")!="QUOTATION_CHAPTER_LOCATOR_UNRESOLVED_NOT_DISPROVED":
  raise ValueError("schema/status")
 prior=r.get("prior_registered_secondary",{})
 if prior.get("source_id")!=prev["source_delta"]["new_source_id"] or prior.get("published_abstract_quote")!="惜其书未刊行于世":
  raise ValueError("scholar citation linkage")
 if any(prior.get(k) is not None for k in ("exact_chapter_in_published_abstract","original_leaf_id","physical_edition")):
  raise ValueError("unearned quotation locator")
 if prior.get("full_1959_article_inspected") is not False:
  raise ValueError("whole journal article unreviewed")
 loci=r.get("locator_probe",[])
 if len(loci)!=2 or loci[0].get("target")!="靜志居詩話 卷十七 沈德符" or loci[0].get("url")!="https://ccddb.net/靜志居詩話/卷十七/沈德符":
  raise ValueError("specific Shen Defu received transcription locator")
 if loci[0].get("wording_quoted_in_1959_present_in_this_displayed_entry") is not False or loci[0].get("physically_edition_bound") is not False or loci[0].get("complete_all_editions_verified") is not False:
  raise ValueError("received quote nonhit promoted to comprehensive absence")
 if loci[1].get("ocr_status")!="UNPROOFREAD_AUTOMATIC_OCR" or loci[1].get("negative_quote_vote_authorized") is not False:
  raise ValueError("OCR treated as physical negative")
 if any(r.get("firewalls",{}).get(k) is not True for k in GUARDS):
  raise ValueError("scope/firewall overreach")
 a=r.get("adjudication",{})
 if a.get("quote_target")!="PANG1959_ASCRIBED_ZHU_JINGZHIJU_UNVERIFIED_EXACT_LOCUS" or a.get("conclusion")!="NEEDS_EDITION_SCOPED_PHYSICAL_PAGE_COMPARISON_NO_ATTRIBUTION_ERROR_VERDICT":
  raise ValueError("overclaim of citation defect")
 if any(a.get(k)!=0 for k in ("new_registered_sources","new_original_images","new_ancient_glyph_votes","transmission_nodes_added","transmission_edges_added","algorithm_reopens")):
  raise ValueError("unsupported provenance increment")
 account=r.get("accounting",{})
 if (account.get("root_sources"),account.get("extension_sources"),account.get("total_sources"),account.get("graph_nodes"),account.get("graph_edges"))!=(647,43,690,252,238):
  raise ValueError("source-at-checkpoint immutable accounting")
 live=st["historical_audit"]
 if live["external_source_registry_total_unique_count"]<690 or live["row_count"]!=222:
  raise ValueError("live source regressed")
 if tuple(map(int,st["schema_version"].split(".")))<(1,559,0) or not any(x.startswith("12VC ") for x in live["current_focus"]):
  raise ValueError("continuity state missing")
 return {"status":"PASS","citation_error_disproved":False,"historical_glyph_votes":0,"new_sources":0}
def verify(root=ROOT):
 def j(p):return json.loads((root/p).read_text(encoding="utf-8"))
 return validate(j(REC),j(STATE),j(PREV))
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False,sort_keys=True))
