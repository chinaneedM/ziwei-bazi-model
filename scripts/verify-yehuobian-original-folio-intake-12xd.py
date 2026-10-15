#!/usr/bin/env python3
"""12XD. Checks source metadata completeness and image digest; never authenticates an ancient leaf."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12XD-IOC-COPY-FORM-AND-ORIGINAL-FOLIO-INTAKE-R1.json"
XC="docs/research/MING-DATONG-YEHUOBIAN-12XC-TOKYO-ITEM-SPECIFIC-REPRODUCTION-DOSSIER-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
MANIFEST="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
def read(name):
 return json.loads((ROOT/name).read_text(encoding="utf-8"))
def need(ok,msg):
 if not ok:raise ValueError(msg)
def check_ledger(r,xc,state,man):
 need(r["schema"]=="TIANWEN-12XD-IOC-ORIGINAL-FOLIO-COPY-FORM-AND-SAFE-INTAKE-R1","ledger schema")
 need(r["predecessor"]==XC,"parent link")
 need(r["official_copy_form"]["url"]=="https://www.ioc.u-tokyo.ac.jp/~library/form/form_kicho_copy.pdf","provider PDF")
 need(r["official_example_pdf"]["url"]=="https://www.ioc.u-tokyo.ac.jp/~library/form/form_kicho_copy_sample.pdf","provider example")
 need(r["official_copy_form"]["pages"]==r["official_example_pdf"]["pages"]==1,"PDF pagination")
 need(r["official_copy_form"]["filled"] is False and r["official_copy_form"]["submitted"] is False and r["official_example_pdf"]["is_original_target"] is False,"not an application or historical witness")
 fields=r["official_copy_form"]["fields"]
 need(set(fields)=={"申請日","氏名","住所","電話/Fax","E-mail","所属","所在地","所属電話/Fax","請求記号","資料名","複写箇所（頁）","複写目的"},"PDF form field map")
 reserve=r["reservation"]
 need(reserve["advance_open_days_start"]==5 and reserve["advance_open_days_end"]==2 and reserve["maximum_books_per_booking"]==10 and reserve["maximum_stitched_cases_per_booking"]==5 and reserve["booking_confirmed"] is False,"reservation constraints")
 candidates=r["primary_catalogs"]
 need([x["catalog_detail"] for x in candidates]==["9927","90972"],"item lineage")
 p=xc["target_items"]
 for i,item in enumerate(candidates):
  need(item["ciNii"]==p[i]["cinii"] and item["barcode"]==p[i]["item"] and item["date_catalog"]==p[i]["year"],"catalog/item binding")
  need(item["original_leaf_number"] is None and item["original_page_image"] is None and item["formal_request_ready"] is False,"folio and formal request not ready")
 need(candidates[0]["request_shelfmark"]=="大木;子部:雜家類:16-20" and candidates[1]["request_shelfmark"]=="倉石文庫:20128:11","distinct physical volume notation")
 need(r["supplementary_catalog"]["reported_missing_juan"]==[21,22] and r["supplementary_catalog"]["juan20_present_verified"] is False,"Imabori cannot be assumed complete")
 loc=r["literary_locator"]
 need(loc["juan"]==20 and loc["chapter"]=="改造漏刻" and loc["original_folio_number"] is None and loc["received_text_not_original_print_page"] is True,"received text not original print")
 need([q["key"] for q in r["four_loci"]]==["palace_domain","palace_clock","beijing_winter","beijing_summer"] and all(q["source_print_reading"] is None for q in r["four_loci"]),"glyphs remain unknown")
 g=r["invariants"];h=state["historical_audit"]
 need(all(g[k]==0 for k in ("source_registry_added","ancient_print_page_images","historical_glyph_votes","historical_print_independence_votes","letters_sent","reservations_booked","copy_orders_submitted","algorithm_reopens")),"no false progress")
 need((g["source_root"],g["source_extensions"],g["source_union"])==(647,59,706)==(h["external_source_registry_root_count"],h["external_source_registry_extension_count"],h["external_source_registry_total_unique_count"]),"registry state")
 need(man["combined_source_count"]==706,"registry manifest")
 need((g["matrix_rows"],g["matrix_audited"],g["provenance_repairs"])==(h["row_count"],h["audited_row_count"],h["repaired_provenance_metadata_defect_count"])==(222,222,45),"audit matrix")
 need(g["formal_batches"]==len(h["completed_batches"])==487 and (g["graph_nodes"],g["graph_edges"])==(252,238),"formal and genealogy state")
 need(g["product"]==state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"product freeze")
 need(r["intake_contract"]["initial_receipts"]==0 and r["intake_contract"]["never_auto_infer_print_or_historical_glyph"] is True and r["intake_contract"]["never_auto_link_distinct_copies"] is True,"intake cannot create original")
 need(all(r["transmission_impact"][x]==[] for x in ("nodes_added_or_strengthened","edges_supported","edges_revised","edges_rejected_or_unproved")),"genealogy unchanged")
 return {"status":"PASS","catalog_items":2,"documented_provider_pdf_forms":2,"new_original_source_images":0,"historical_glyph_votes":0}
def check_receipt(receipt,image_bytes,record=None):
 """No claim of historical authenticity: ensures digest and required manual evidence pointers ONLY."""
 record=record or read(REC)
 need(isinstance(receipt,dict),"receipt object")
 target={x["barcode"]:x for x in record["primary_catalogs"]}
 barcode=receipt.get("physical_item_barcode")
 need(barcode in target,"item is not verified target")
 item=target[barcode]
 for k,expected in (("catalog_detail",item["catalog_detail"]),("ncid",item["ciNii"]),("source_shelfmark",item["request_shelfmark"]),("juan",20),("chapter","改造漏刻")):
  need(receipt.get(k)==expected,"catalog item scope: "+k)
 need(receipt.get("provider")=="TOKYO_IOC" and receipt.get("capture_channel") in ("INSTITUTION_FULFILLED_COPY","INSTITUTION_PUBLIC_LINK_WITH_ITEM_BINDING","AUTHORIZED_ONSITE_IMAGE"),"institutional provenance required")
 need(isinstance(receipt.get("custody_document"),str) and len(receipt["custody_document"].strip())>=10,"item-specific custody receipt missing")
 need(isinstance(receipt.get("original_leaf_ref"),str) and len(receipt["original_leaf_ref"].strip())>=2,"folio coordinate missing")
 url=receipt.get("source_image_url")
 need(isinstance(url,str) and url.startswith("https://"),"official source URL required")
 need(record["intake_contract"]["disallowed_modern_1959_image_path_substring"] not in url,"modern 1959 surrogate cannot stand for antique folio")
 need(receipt.get("capture_date") and receipt.get("research_use_authorization_ref"),"date and written scope of reuse required")
 need(receipt.get("personal_identifying_data_included") is False,"no personal details in public research receipt")
 need(receipt.get("claims_ancient_glyph_votes")==0 and receipt.get("claims_independent_print_witnesses")==0,"no automatic original or independent print vote")
 need(isinstance(image_bytes,bytes) and len(image_bytes)>=32,"image binary required")
 form=receipt.get("format")
 magic={"PNG":b"\x89PNG\r\n\x1a\n","JPEG":b"\xff\xd8\xff","PDF":b"%PDF-","TIFF_LE":b"II*\x00","TIFF_BE":b"MM\x00*"}
 need(form in magic and image_bytes.startswith(magic[form]),"file signature only, not decoded")
 need(receipt.get("image_bytes")==len(image_bytes) and receipt.get("image_sha256")==hashlib.sha256(image_bytes).hexdigest(),"original binary digest mismatch")
 need(receipt.get("human_glyph_review_completed") is False and receipt.get("print_plate_identity_adjudicated") is False,"human review pending")
 return {"status":"METADATA_COMPLETE_PENDING_HUMAN_PAGE_AND_PLATE_REVIEW","image_sha256":receipt["image_sha256"],"physical_item_barcode":barcode,"historical_glyph_votes_awarded":0,"plate_independence_votes_awarded":0}
def verify():
 return check_ledger(read(REC),read(XC),read(STATE),read(MANIFEST))
if __name__=="__main__":
 parser=argparse.ArgumentParser();parser.add_argument("--receipt-json");parser.add_argument("--image-file")
 opt=parser.parse_args()
 need(bool(opt.receipt_json)==bool(opt.image_file),"receipt and image both required")
 out=verify()
 if opt.receipt_json:
  import importlib.util
  strict_path=ROOT/"scripts/verify-yehuobian-original-folio-intake-12xg.py"
  strict_spec=importlib.util.spec_from_file_location("original_folio_strict_12xg",strict_path)
  strict_mod=importlib.util.module_from_spec(strict_spec)
  strict_spec.loader.exec_module(strict_mod)
  out["intake"]=strict_mod.validate(json.loads(Path(opt.receipt_json).read_text(encoding="utf-8")),Path(opt.image_file).read_bytes())
 print(json.dumps(out,ensure_ascii=False))
