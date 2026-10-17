#!/usr/bin/env python3
"""12YU source-internal Siku paratext proof, without imprint authentication."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YU-MEI-CADAL06054965-VOLUME-PARATEXT-EDITION-SELF-LABEL-R1.json"
def read():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json"))
def must(c,m):
 if not c:raise ValueError(m)
def verify(d,l,s):
 src=d["source"]
 must(d["schema"]=="TIANWEN-12YU-MEI-CADAL06054965-NATIVE-PARATEXT-FIELD-EDITION-BOUNDARY-R1" and d["grade"].startswith("HASH_BOUND_NATIVE_DIGITIZED_SOURCE_PARATEXT"),"grade")
 must(src["catalog_item"]=="CADAL06054965" and src["source_file_bytes"]==4259929 and src["source_image_pages"]==126 and src["source_book_item_sha256"]=="195c3ff35ae297b43fad6bb597d46dd046b109bee4c8eae8732fba336adab800" and src["original_archive_was_reverified"] is True and src["ocr_used"] is False,"source origin")
 a=d["source_internal_printed_page_reviews"]
 expected={1:("四庫全書 子部","3095e2684816b0f1eca20836ec97032dfa622e75e9acf43107f2422b03e0de15"),2:("欽定四庫全書；子部；大統歷志卷三四；校官名銜","bd29e380b97136616db086a9cd09af2c69786d50a67dc7f3a7e5f0e2789ce874"),3:("欽定四庫全書；大統歷志卷三；宣城梅文鼎撰","46c39cb1267047de838f7babf04235bb00ec73c2331b54684ef3448fee0ce99d"),126:("大統歷志卷四","7f1bb9afda7d5fe3d11875fda0ded5e0e94c5eaf7cd01082e083f28147f6f0a9")}
 must(len(a)==4 and {x["digital_page"] for x in a}==set(expected),"bounded 4 folios")
 for x in a:
  glyph,sha=expected[x["digital_page"]]
  must(x["direct_visible"]==glyph and x["original_png_sha256"]==sha and len(x["rgb_sha256"])==64,"printed glyph page or pixel hash")
 scope=d["scan_scope"]
 must(scope["native_pages_exported"]==28 and scope["original_page_count"]==126 and scope["bounded_paratext_pages_directly_read"]==[1,2,3,126] and scope["entire_book_line_by_line_collated"] is False and scope["colophon_and_specific_copy_print_date_from_this_scope"]=="UNVERIFIED","no complete colophon proof")
 dates=d["chronology_firewall"]
 must(dates["physical_origination_year"]=="UNVERIFIED" and dates["physical_repository_identifier_specific_copy"]=="UNVERIFIED" and dates["name_qinding_siku"]=="SELF_DESIGNATION_NOT_PROOF_OF_WENYUANGE_OR_WENJINGE_COPY" and dates["relation_to_12yt"]=="SAME_ONE_DIGITIZED_SOURCE_NO_ADDITIONAL_PHYSICAL_VOTE","chronology conflation")
 impact=d["evidence_impact"]
 must(all(impact[q]==0 for q in ("new_digitized_sources","new_original_print_numeric_loci","new_independent_ancient_physical_copy_votes","new_source_registry_entries","new_genealogy_nodes","new_genealogy_edges","new_algorithm_reopens")),"false independent proof")
 must(impact["open_research_issues"]==11 and impact["g893_original_principal"]=="5/6" and impact["g893_cross_witness_final"]=="0/6" and impact["deterministic_product"]=="CLOSED","product freeze")
 item=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 must(item["status"]=="OPEN" and DOC in item["source_refs"] and DOC.replace(".json",".md") in item["source_refs"] and item["mei_12yu_original_paratext_edition_reviews"][0]["physical_copy_votes_added"]==0,"issue5 crossbinding")
 must(s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,s["schema_version"].split(".")))>=(1,633,0),"state")
 must(l["checkpoint_log"][-1]["state_version"]==s["schema_version"] and len(l["checkpoint_log"][-1]["reviewed_issue_ids"])==len(l["issues"]),"checkpoint")
 must(any(x.startswith("12YU ") for x in s["historical_audit"]["current_focus"]) and s["invariants"]["algorithm_reopen_count"]==0 and s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","focus")
 return {"status":"PASS","source_pages":126,"exported_paratext_pages":28,"original_read_paratext_pages":4,"source_copy_printing_date":"UNVERIFIED","new_physical_witnesses":0,"open_issues":11}
if __name__=="__main__":print(json.dumps(verify(*read()),ensure_ascii=False))
