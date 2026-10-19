#!/usr/bin/env python3
import json,hashlib,re,argparse
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13X-WASEDA-GORYEOSA-WORK52-D16-D18-ORIGINAL-IMAGE-R1.json"
def read(p=E):return json.loads((R/p).read_text(encoding="utf8"))
def check(d):
 assert d["schema"]=="TIANWEN-13X-WASEDA-GORYEOSA-ORIGINAL-WORK52-SOLAR-D16-D18-R1"
 s=d["source"]
 assert s["shelfmark"]=="リ06 02809" and s["digital_group"]==33 and s["pdf_pages"]==85 and s["pdf_bytes"]==58769815
 assert s["pdf_sha256"]=="28ebfeb34191f45715bc449d27da61fe04fb05eb45e84dd00cf569699f46225f"
 assert s["source_workflow_run_id"]==39233784146 and s["source_artifact_id"]==12177878468 and s["physical_book_impression_date"] is None
 pages=d["native_pages"]
 assert [p["pdf_page_1_based"] for p in pages]==[2,21,23]
 assert [p["source_embedded_jpeg_xref"] for p in pages]==[7,64,70]
 assert [p["source_jpeg_sha256"] for p in pages]==[
 "f11097ba0f4a2064d617107f78fd974616e31143b6b343fa086b0e7d0dfd3623",
 "acf08f57fcd82d35f6b2b3359449dd72def4b7124f9a25412bbec3812bc96bb7",
 "388f3d5dd9e9861f8ce90c304b154edaeaee98614bb12cd3468f957dcde6fc66"]
 assert "高麗史五十二" in d["original_title"] and "志卷第六" in d["original_title"]
 assert all(x["source_native_dimensions"]==[2592,1728] for x in pages)
 assert [r["rgb_pixels_sha256"] for r in d["source_roi"]]==[
 "79f11ce60e23b61b117481b52f870c6a79f71b5c7a0b982092d28ad187a200d7",
 "f35fba87f6f730135f4ae9429d6d6333c2f302ae3c66f15361dfb8c0b20893a3",
 "da7679fe16b4ccaeaf5254eaaabd2bd2c1a3c8fb3a685c30d3b7895b5289005b",
 "3f3ade6cf43436bdb353d0d94305ff65f987a127efd03f5b9f28647627873efa"]
 assert [r["page"] for r in d["source_roi"]]==[2,21,23,23]
 assert all(re.fullmatch("[0-9a-f]{64}",r["rgb_pixels_sha256"]) for r in d["source_roi"])
 assert d["direct_readings"]["day16"]["short"]=="五分一三六二" and d["direct_readings"]["day16"]["long"]=="四百二十九六〇七三"
 assert d["direct_readings"]["day18"]["short"]=="五分二七三四" and d["direct_readings"]["day18"]["long"]=="四百一十九一一六三"
 assert d["direct_readings"]["day18"]["cumulative_original"] is None
 assert d["comparison"]["g893_other_original_day16_candidate"]=="五分二三六二"
 assert d["comparison"]["waseda_day18_cumulative_folio"] is None
 assert d["comparison"]["ming1569_same_column_proven"] is False
 assert all(d["adjudication"][x]==0 for x in ("independent_final_numeric_votes_added","external_registry_sources_added","transmission_edges_added","algorithm_reopens"))
 assert d["adjudication"]["unresolved_research_issues"]==11 and d["adjudication"]["product_r1"]=="CLOSED"
 prior=read(d["prior_unverified_route"])
 assert prior["candidate_book_0033"]["internal_work52_verified"] is False
 state=read("docs/PROJECT-CURRENT-STATE-R1.json");ledger=read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert tuple(map(int,state["schema_version"].split(".")))>=(1,683,0)
 assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert len(state["historical_audit"]["current_focus"])==ledger["binding"]["source_focus_count"]
 assert ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"] and E[:-5]+".md" in issue["source_refs"]
 assert len(ledger["issues"])==11 and ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
 assert set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={x["id"] for x in ledger["issues"]}
 return True
def verify_pdf(filepath,d):
 import fitz
 from PIL import Image
 from io import BytesIO
 p=Path(filepath)
 assert p.stat().st_size==d["source"]["pdf_bytes"]
 assert hashlib.sha256(p.read_bytes()).hexdigest()==d["source"]["pdf_sha256"]
 pdf=fitz.open(str(p))
 try:
  assert len(pdf)==d["source"]["pdf_pages"]
  for rec in d["native_pages"]:
   n=rec["pdf_page_1_based"];xref=rec["source_embedded_jpeg_xref"]
   assert any(item[0]==xref for item in pdf[n-1].get_images(full=True))
   orig=pdf.extract_image(xref)
   assert orig["ext"]=="jpeg" and hashlib.sha256(orig["image"]).hexdigest()==rec["source_jpeg_sha256"]
   rgb=Image.open(BytesIO(orig["image"])).convert("RGB")
   for roi in [x for x in d["source_roi"] if x["page"]==n]:
    raw=rgb.crop(tuple(roi["xyxy"])).tobytes()
    assert hashlib.sha256(raw).hexdigest()==roi["rgb_pixels_sha256"]
  return True
 finally:pdf.close()
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--source-pdf");args=ap.parse_args()
 d=read();check(d)
 if args.source_pdf:verify_pdf(args.source_pdf,d)
 print(json.dumps({"status":"PASS_SOURCE_PIXELS" if args.source_pdf else "PASS_STATIC","native_pages":3,"independent_physical_votes":0}))
