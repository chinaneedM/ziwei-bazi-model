#!/usr/bin/env python3
"""12WN: bounded first-party Google Books volume ID metadata; ZERO original-image votes."""
import argparse
import hashlib
import json
import urllib.request
import urllib.error
from pathlib import Path
from urllib.parse import urlparse

ID="VAWHNTyDZC8C"
API="https://www.googleapis.com/books/v1/volumes/"+ID+"?projection=FULL"
MAX_BYTES=550_000
UA="Tianwen-historical-evidence/12WN (public book metadata only; no page enumeration)"
def check_url(url):
    u=urlparse(url)
    if u.scheme!="https" or u.hostname!="www.googleapis.com" or not u.path=="/books/v1/volumes/"+ID:
        raise ValueError("unapproved source URL or redirect")
def read_public_metadata(opener=urllib.request.urlopen):
    req=urllib.request.Request(API,headers={"User-Agent":UA,"Accept":"application/json"})
    check_url(req.full_url)
    with opener(req,timeout=40) as r:
        check_url(r.geturl())
        b=r.read(MAX_BYTES+1)
    if len(b)>MAX_BYTES:
        raise ValueError("Google Books source document too large")
    try: obj=json.loads(b.decode("utf-8"))
    except Exception as exc:raise ValueError("invalid Google Books JSON") from exc
    if not isinstance(obj,dict) or obj.get("id")!=ID or obj.get("kind")!="books#volume":
        raise ValueError("provider returned nonmatching or non-volume JSON")
    return obj,b
def classify(obj):
    info=obj.get("volumeInfo") or {}
    access=obj.get("accessInfo") or {}
    title=info.get("title")
    if not isinstance(title,str) or not any(s in title for s in ("野獲","野获")):
        raise ValueError("volume title does not bind proposed Yehuobian work")
    date=info.get("publishedDate")
    return {
       "provider":"Google Books official Volume resource",
       "google_volume_id":ID,
       "metadata_title":title,
       "metadata_authors":info.get("authors"),
       "metadata_publisher":info.get("publisher"),
       "provider_catalog_published_date":date,
       "source_attribution_from_api":info.get("description"),
       "volume_page_count_reported":info.get("pageCount"),
       "volume_print_type":info.get("printType"),
       "volume_preview_link":info.get("previewLink"),
       "canonical_volume_link":info.get("canonicalVolumeLink"),
       "public_api_access_country":access.get("country"),
       "api_viewability":access.get("viewability"),
       "api_public_domain_flag":access.get("publicDomain"),
       "api_pdf_available":(access.get("pdf") or {}).get("isAvailable"),
       "api_epub_available":(access.get("epub") or {}).get("isAvailable"),
       "api_pdf_download_link_reported":(access.get("pdf") or {}).get("downloadLink"),
       "source_ocr_glyphs_examined":False,
       "source_printed_page_images_examined":False,
       "source_juan20_folio_identified":False,
       "specific_keio_physical_copy_catalog_number_verified":False,
       "original_1827_unrepaired_print_proven":False,
       "1869_print_comparator_proven":False,
       "new_independent_ancient_original_folio_votes":0,
       "algorithm_reopens":0,
       "scope_warning":"Google Books metadata publication year and original-from statement cannot independently date the scanned PAPER copy, specify fascicle 20 or certify unchanged 1827 printing. API viewability depends on access country; no page image is acquired.",
    }
def write_receipt(output):
    d=Path(output);d.mkdir(parents=True,exist_ok=True)
    try:
        obj,blob=read_public_metadata()
        summary=classify(obj)
        summary["provider_metadata_exact_response_sha256"]=hashlib.sha256(blob).hexdigest()
        summary["provider_metadata_response_bytes"]=len(blob)
        summary["metadata_endpoint"]=API
        summary["schema"]="TIANWEN-12WN-KEIO-GOOGLEBOOKS-OFFICIAL-VOLUME-METADATA-RECEIPT-R1"
        summary["status"]="FIRST_PARTY_GOOGLE_VOLUME_METADATA_ONLY_NO_AUTHENTICATED_ORIGINAL_FOLIO"
        (d/"provider-original-volume.json").write_bytes(blob)
        (d/"metadata-receipt.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        return summary
    except Exception as e:
        (d/"capture-error.json").write_text(json.dumps({"status":"ACCESS_BOUNDARY_NO_NEW_SOURCE_AUTHORITY","error_class":type(e).__name__,"details":str(e),"original_leaf_votes":0},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        raise
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output-dir",default="keio-googlebooks-12wn-output")
    args=ap.parse_args()
    r=write_receipt(args.output_dir)
    print(json.dumps({"status":r["status"],"volume_id":r["google_volume_id"],"title":r["metadata_title"],"published_date":r["provider_catalog_published_date"],"viewability":r["api_viewability"],"original_leaf_votes":0},ensure_ascii=False))
if __name__=="__main__":main()
