#!/usr/bin/env python3
"""13CP bibliographic object vs uploader filename firewall; no source pixel claims."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CP-GORYEOSA-NCL03117-03130-SURROGATE-ID-CROSSWALK-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13CP-NCL03117-NCL03130-COMMONS-UPLOAD-NAME-OBJECT-FIREWALL-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["previous_check"]=="docs/research/TIANWEN-13CO-GORYEOSA-NCL03130-NDL1909-THIRD-WITNESS-ACCESS-FIREWALL-R1.json"
 a=e["authority"]["03117"];b=e["authority"]["03130"]
 assert a["book_number"]=="03117" and a["call_number"]=="207 03117"
 assert a["title"]=="史臠二十五卷" and a["creator"]=="余文龍" and a["books"]==32
 assert "1618" in a["edition"] and a["first_party_item_url"].startswith("https://rbook.ncl.edu.tw/NCLSearch/Search/SearchDetail?")
 assert a["source_scope"]=="DIRECT_FIRST_PARTY_CATALOG_IDENTITY_ONLY_NOT_GORYEOSA_TEXT"
 assert b["metadata_call_number"]=="208 03130" and b["metadata_title"]=="高麗史"
 assert b["metadata_total_books"]==40 and "補鈔本" in b["metadata_edition"]
 assert b["source_scope"]=="SECONDARY_HOSTED_CATALOG_CAPTION_CANNOT_BIND_THIS_PDF_TO_PHYSICAL_COPY"
 docs=e["digital_surrogate_metadata"]
 assert len(docs)==5
 assert [(x["display"],x["upload_comment"],x["pages"]) for x in docs]==[
 ("NCL-03130 02 高麗史.pdf","03117_2.pdf",201),
 ("NCL-03130 07 高麗史.pdf","03117_7.pdf",187),
 ("NCL-03130 08 高麗史.pdf","03117_8.pdf",189),
 ("NCL-03130 20 高麗史.pdf","03117_20.pdf",166),
 ("NCL-03130 21 高麗史.pdf","03117_21.pdf",171)]
 assert all(x["source_url"].startswith("https://commons.wikimedia.org/wiki/File:NCL-03130_") for x in docs)
 c=e["other_item_03117_commons_file_history_crosscheck"]
 assert [(x["display"],x["upload_comment"]) for x in c]==[
 ("NCL-03117 1 史臠.pdf","10277_1.pdf"),("NCL-03117 2 史臠.pdf","10277_2.pdf")]
 k=e["interpretation"]
 assert k["five_observations_not_one_typo"] is True
 assert k["namespaces_are_distinct_as_bibliographic_identity"] is True
 assert k["upload_comment_source_filename_is_not_catalog_number"]=="PROVEN_UNSAFE_IDENTITY_SHORTCUT"
 for q in ["five_alias_occurrences_do_not_prove_five_independent_historical_copies","reciprocal_local_upload_names_10277_for_03117_demonstrate_upload_comment_is_not_catalog_number","cannot_claim_03130_display_is_false_from_03117_comments_only","cannot_claim_scanned_pdf_is_03130_original_without_original_image_or_provider_item"]:
  assert k[q] is True
 assert k["pdf_original_bytes_acquired_this_batch"] is False
 assert k["pdf_image_pages_reviewed_this_batch"]==k["third_original_D16_glyphs_added"]==k["physical_copy_new_votes"]==0
 assert k["NCL03130_ju52_page"]==k["old_qing_vs_guangxu_replacement_segment"]=="UNBOUND"
 sc=e["scope"]
 for q in ["new_source_registry_entries","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","new_historical_physical_copies","algorithm_reopens"]:
  assert sc[q]==0
 assert sc["deterministic_product"]=="CLOSED" and sc["open_or_blocked_risks"]==11
 assert (sc["matrix_audited"],sc["registered_sources"],sc["graph_nodes"],sc["graph_edges"])==(222,754,252,238)
 assert s["historical_audit"]["row_count"]==s["historical_audit"]["audited_row_count"]==222
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 assert s["invariants"]["algorithm_reopen_count"]==0
 assert any(t.startswith("13CP ") for t in s["historical_audit"]["current_focus"])
 assert s["historical_audit"]["latest_batch_doc"].endswith("YEHUOBIAN-SHLIB-FIRSTPARTY-AND-OLD20-ATLAS-QD.md")
 assert l["binding"]["reviewed_state_version"]==s["schema_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13CP-UPLOAD-ALIAS-FIREWALL" for x in issue["history"])
 assert any(x["id"]=="OMISSIONS-13CP-ID-FIREWALL-20261022" for x in l["checkpoint_log"])
 assert len([i for i in l["issues"] if i["status"] in ["OPEN","BLOCKED_SOURCE_ACCESS"]])==11
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L))
 print("TIANWEN_13CP_NCL_IDENTITY_UPLOAD_ALIAS_FIREWALL=PASS; ORIGINAL_VOLUME52_FOLIO=UNBOUND")
