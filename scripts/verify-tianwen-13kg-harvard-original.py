#!/usr/bin/env python3
"""13KG: Harvard Ming Shi printed original scoped to PDF pages 11/12 only.

Check source/leaf digests and non-award boundaries. --pdf replays source pixels;
no OCR and no historical page-number guessing.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13KG-HARVARD-1739-MINGSHI-J33-DIRECT-PRINTED-POLARITY-R1.json"
SHARD="docs/research/TIANWEN-13KG-HARVARD-MINGSHI-V10-DIRECT-IMAGE-SOURCE-SHARD-R1.json"
SOURCE_SHA="dde1bfd5d3cf15954ddc6dbf1c020971806038bbc7f737b9053d5643e5c7c264"
EXPECTED={
 11:("共得五秒八十一微為初限平立合差","1729d74605f74ac1ff15a7e0b057d56398424b9472602d04eec9ac34fc2061c0",
     "55afb1634fb5558e4db1a7de7c1b6b180e6b35094fddc39ea3c1cd615820de7e","c87713d304e4ef4380a3703b32ed659509a7c281e9b728670e175b24fd977821"),
 12:("置損益分以其限平立合差益減損加之即為次限損益分","d84b365e58b07ee8ccaa1fe4b2cbf243e9cd6ca61660946d171eb211b68b2ac6",
     "9e2efc909ef20b1d8682a30474e33d438bcaa6c91914c5116791e2394c9967ef","1a8f84fb8d05cb9c08c89b06cea686fa10502f4b113a3276d6b0555aa8bff690")}
ROI={11:[245,150,620,1630],12:[1110,145,1750,1660]}

def check(ok,msg):
 if not ok: raise ValueError(msg)

def sha(raw):
 return hashlib.sha256(raw).hexdigest()

def verify(e,shard,pdf=None):
 check(e["schema"]=="TIANWEN-13KG-HARVARD-1739-MINGSHI-J33-DIRECT-PRINTED-POLARITY-R1","schema")
 check(e["issue_id"]=="TW-OPEN-0005" and e["physical_source_count_delta"]==0,"original source count")
 w=e["witness"]
 check(w["source_sha256"]==SOURCE_SHA and w["source_sha1"]=="5aa766a7985b92c84f81626529d57ca96fd865ab","source digest")
 check(w["size_bytes"]==46883051 and w["page_count"]==52 and w["digital_volume_index"]==10 and w["literary_juan"]==33,"volume identity")
 check(w["edition_impression_date_bound"] is False and w["physical_copy_catalog_identity_bound"] is False,"unproven impression")
 check(w["source_pdf_api_sha1_and_bytes_matched"] is True and w["acquisition_artifact_id"]==12873689749,"source acquisition")
 check("Harvard_drs_428231183" in w["source_url"] and w["source_url"].startswith("https://upload.wikimedia.org/"),"source address")
 pages=w["manually_collated_pages"]
 check(len(pages)==2 and {p["page"] for p in pages}==set(EXPECTED),"two original print loci")
 s=shard["sources"]
 check(len(s)==1 and s[0]["physical_glyph_authority"] is True and s[0]["verification_status"]=="DIRECT_SOURCE_IMAGE_GLYPH_COLLATED_EDITION_UNBOUND","source authority")
 a=s[0]["direct_image_attestation"]
 check(a["source_url"]==w["source_url"] and a["source_sha256"]==SOURCE_SHA and
       a["page_sha256"]=={str(p["page"]):p["sha256"] for p in pages},"registry image identity")
 for p in pages:
  n=p["page"]; lit,ph,rgb,rhash=EXPECTED[n]
  check(p["literal"]==lit and (p["sha256"],p["rgb_sha256"],p["rect_rgb_sha256"])==(ph,rgb,rhash),"original glyph or hash")
  check(p["rect_px"]==ROI[n],"scoped ROI")
  check(all(isinstance(v,int) for v in p["size_px"]) and p["size_px"][0]==2070,"source raster dimensions")
  x0,y0,x1,y1=p["rect_px"]
  check(0<=x0<x1<=p["size_px"][0] and 0<=y0<y1<=p["size_px"][1],"ROI bounded")
 check(e["observed_original_readings"]["after_81_wei_50_xian_explicit"] is False,"do not insert 50纖 into printed source")
 b=e["remaining_boundaries"]
 check(b["new_physical_impression_votes"]==0 and b["source_registry_new_digital_entry"]==1 and b["G893_cross_witness_numeric_winners"]==0,"no false historical winner")
 check(all(b[k] is False for k in ["huang_printed_original_observed","huang_ocr_error_proven","ancient_impression_year_proven","transmission_direct_copy_edge_added","TW_OPEN_0005_closed"]),"uncertainty retained")
 check(b["graph_edges_added"]==0 and b["algorithm_reopens"]==0 and b["product"]=="CLOSED","product/graph")
 if pdf is not None:
  import io
  import fitz
  from PIL import Image
  data=Path(pdf).read_bytes()
  check(sha(data)==SOURCE_SHA and len(data)==46883051,"original PDF bytes")
  doc=fitz.open(stream=data,filetype="pdf")
  check(len(doc)==52,"PDF page count")
  for p in pages:
   n=p["page"]
   pix=doc[n-1].get_pixmap(matrix=fitz.Matrix(1.15,1.15),colorspace=fitz.csRGB,alpha=False)
   png=pix.tobytes("png")
   img=Image.open(io.BytesIO(png)).convert("RGB")
   check(sha(png)==p["sha256"],"rendered PDF source page SHA")
   check(list(img.size)==p["size_px"] and sha(img.tobytes())==p["rgb_sha256"],"original raster pixels")
   check(sha(img.crop(p["rect_px"]).tobytes())==p["rect_rgb_sha256"],"ROI pixels")
  doc.close()
 return {"status":"PASS","source":w["source_file_title"],"source_PDF_pages":52,
         "visually_attested_printed_loci":2,"pdf_pixels_replayed":bool(pdf),
         "new_registered_digital_source":1,"historical_numeric_winners":0}

def check_handoff():
 state=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text())
 ledger=json.loads((ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text())
 h=state["historical_audit"]
 check(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==h["research_omission_guard"]["reviewed_state_version"],"handoff version")
 check(ledger["binding"]["source_focus_count"]==len(h["current_focus"]) and h["current_focus"][-1].startswith(ledger["binding"]["latest_research_focus_prefix"]+" "),"latest source focus")
 i=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 check(i["next_action"].startswith(ledger["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:"),"next action")
 check({E,E.replace(".json",".md"),SHARD}.issubset(i["source_refs"]),"bound source refs")
 check(any(x.get("revision_id")=="TW-OPEN-0005-13KG-HARVARD-PRINTED-20261029" for x in i["history"]),"append-only issue")
 check(h["external_source_registry_total_unique_count"]>=764 and h["external_source_registry_total_unique_count"]==h["external_source_registry_root_count"]+h["external_source_registry_extension_count"] and state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","source/algorithm invariant")

if __name__=="__main__":
 parser=argparse.ArgumentParser();parser.add_argument("--pdf",type=Path)
 args=parser.parse_args()
 check_handoff()
 print(json.dumps(verify(json.loads((ROOT/E).read_text()),json.loads((ROOT/SHARD).read_text()),args.pdf),ensure_ascii=False))
