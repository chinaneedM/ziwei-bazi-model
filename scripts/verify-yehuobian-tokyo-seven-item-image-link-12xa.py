#!/usr/bin/env python3
"""12XA: exact source HTML binary checks + no cross-item image attribution."""
import argparse,hashlib,json,zipfile
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12XA-TOKYO-SEVEN-ITEM-IMAGE-LINK-BOUNDARY-R1.json"
WZ="docs/research/MING-DATONG-YEHUOBIAN-12WZ-TOKYO-SEVEN-FIRSTPARTY-RECORDS-AND-IMABORI-LEAF-GATE-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
MANIFEST="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
def require(ok,msg):
 if not ok:raise ValueError(msg)
def jread(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def validate(r,wz,s,manifest):
 require(r["schema"]=="TIANWEN-12XA-TOKYO-IOC-SEVEN-SOURCE-ITEM-IMAGE-AFFORDANCE-BINARY-SCOPE-R1","schema")
 a=r["source"]
 require(a["source_id"]=="EXT-TOKYO-IOC-KANSEKI-YEHUOBIAN-SEVEN-EXACT-ITEM-DETAILS-12WZ","registered bibliographic parent")
 require(a["parent_record"]==WZ and a["original_title_result_sha256"]==wz["source"]["one_title12WX"]["query_html_sha256"],"original search source")
 require((a["github_actions_run"],a["github_artifact_id"],a["original_zip_size_bytes"])==(38744524548,11977836428,13826),"actual artifact receipt")
 require(a["original_zip_sha256_github_reported"]==a["original_zip_sha256_locally_independently_recomputed"]=="33f31f23f768e70edaa2b2a067aa4731f259898201201a86857281b3f6ca0c5f","independent archive SHA")
 require(a["seven_original_provider_pages_sha256_locally_recomputed"] is True and a["source_original_page_count"]==7 and a["ocr_used"] is False,"scope no OCR")
 records=r["item_controls"]
 require(len(records)==len(wz["items"])==7,"seven provider item receipts")
 for a,b in zip(records,wz["items"]):
  require((a["id"],a["rank"],a["raw_original_html_bytes"],a["raw_original_html_sha256"])==(b["id"],b["rank"],b["bytes"],b["sha"]),"source original HTML identities")
  require(a["provider_catalog_shelfmark"]==b["shelfmark"] and a["edition_role"]==b["role"],"physical catalog shelfmark")
  require(a["contains_literal_img_element"] is (a["id"]=="9928") and a["has_explicit_pdflink_image_control"] is (a["id"]=="9928"),"image affordance restricted to 1959")
  require(a["has_target_juan20_original_image_control"] is False,"none of seven has verified original juan20 image")
 m=r["modern_image_control"]
 require(m["only_catalog_item_with_visible_image_icon"]=="9928" and "1959" in m["catalog_edition"],"modern separate edition")
 require(m["provider_source_emitted_href"]=="javascript:pdflink('/ttsweb/hb_new/B/B17/B1765700-1,2_photo.html')" and m["provider_source_emitted_icon_src"]=="images/image-icon.gif","original link exact control")
 require(m["image_link_was_followed"] is False and m["contents_of_image_or_pdf_examined"] is False and m["modern_item_has_no_historical_original_print_authority"] is True,"no modern image promotion")
 targets=r["physical_target_controls"]
 require(set(targets)=={"9927","90972","103841","104379"},"four ancient print candidates")
 require(targets["9927"]["catalog_edition_year"]==1827 and targets["9927"]["cinii_item"]=="6403767830","1827 exact barcoded book")
 require(targets["90972"]["catalog_edition_year"]==1869 and targets["90972"]["cinii_item"]=="6403148395","1869 exact barcoded book")
 require(targets["103841"]["recorded_missing_juan"]==[21,22] and targets["103841"]["juan20_complete_or_available_proven"] is False,"Imabori volume20 unknown")
 require("虫損" in targets["104379"]["source_catalog_use_note"],"damaged access limit")
 require(all(z["no_direct_digitized_folio_button_in_original_detail_html"] is True and z["source_original_juan20_folio_obtained"] is False for z in targets.values()),"original source folios still missing")
 q=r["scope"]
 require(all(q[k] is True for k in ("digital_button_on_modern_item_not_transferable_to_old_physical_copy","lack_of_button_in_seven_pages_not_proof_no_digitization_elsewhere","online_access_unknown_not_source_absence","source_metadata_print_date_not_original_folio_print_date_proof")),"negative proof scope")
 require(all(q[k]==0 for k in ("independent_1827_and_1869_juan20_printed_page_images_acquired","new_juan20_gaizao_louke_glyph_votes","new_ancient_print_impression_votes","new_registry_source_entries","new_transmission_edges","algorithm_reopens")),"no original page or source promotion")
 require(q["product"]==s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","algorithm closed")
 historic=r["accounting_at_this_research_snapshot"];h=s["historical_audit"]
 require(historic["root_registry"]==647 and historic["extension_sources"]==59 and historic["union_sources"]==706,"frozen metadata research checkpoint")
 require(manifest["combined_source_count"]==h["external_source_registry_total_unique_count"]>=706,"current registry union state sync")
 require(historic["matrix_rows"]==historic["matrix_audited"]==h["row_count"]==222 and historic["provenance_repairs"]==45,"matrix")
 require(historic["genealogy_nodes"]==252 and historic["genealogy_edges"]==238 and historic["formal_batches"]==len(h["completed_batches"])==487,"genealogy and batch")
 require(r["transmission_impact"]["edges_supported"]==[] and r["transmission_impact"]["nodes_added_or_strengthened"]==[],"no genealogy promotion")
 return {"status":"PASS","item_details":7,"modern_image_button_only":1,"historical_print_glyph_votes":0}
class Tags(HTMLParser):
 def __init__(self):
  super().__init__();self.href=[];self.img=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=="a" and a.get("href"):self.href.append(a["href"])
  if t=="img":self.img.append(a.get("src"))
def validate_artifact(path,r):
 p=Path(path)
 raw=p.read_bytes()
 require(len(raw)==r["source"]["original_zip_size_bytes"] and hashlib.sha256(raw).hexdigest()==r["source"]["original_zip_sha256_github_reported"],"actual archived ZIP SHA")
 expected={("detail-"+x["id"]+".html"):x for x in r["item_controls"]}
 with zipfile.ZipFile(p) as z:
  require(set(z.namelist())==set(expected)|{"receipt.json"} and len(z.namelist())==8,"no extra archive files")
  for name,e in expected.items():
   b=z.read(name)
   require(len(b)==e["raw_original_html_bytes"] and hashlib.sha256(b).hexdigest()==e["raw_original_html_sha256"],"actual provider original bytes "+name)
   tags=Tags();tags.feed(b.decode("utf-8",errors="replace"))
   links=[x for x in tags.href if "pdflink(" in x]
   if e["id"]=="9928":
    require(links==[r["modern_image_control"]["provider_source_emitted_href"]],"modern source emitted PDF control exact")
    require(tags.img==[r["modern_image_control"]["provider_source_emitted_icon_src"]],"modern image icon exact")
   else:
    require(links==[] and tags.img==[],"original catalog page lacks image control "+name)
 return {"status":"PASS","original_zip_and_html_objects_rehashed":8,"source_details":7,"source_original_1827_1869_leaf_images":0}
def verify(artifact=None):
 r=jread(REC);out=validate(r,jread(WZ),jread(STATE),jread(MANIFEST))
 if artifact:out["artifact"]=validate_artifact(artifact,r)
 return out
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--artifact-zip",default=None)
 z=a.parse_args();print(json.dumps(verify(z.artifact_zip),ensure_ascii=False))
