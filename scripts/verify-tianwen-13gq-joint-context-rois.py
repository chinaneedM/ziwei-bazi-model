#!/usr/bin/env python3
"""13GQ same-source contextual images: reject unearned full-field attribution."""
import hashlib,io,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];E=ROOT/"docs/research/TIANWEN-13GQ-NCL03130-ORIGINAL-JOINT-HEADING-FIELD-CONTEXT-R1.json"
def sha(v):return hashlib.sha256(v).hexdigest()
def covers(a,b):return a[0]<=b[0] and a[1]<=b[1] and a[2]>=b[2] and a[3]>=b[3]
def check(d):
 assert d["grade"]=="EXACT_SAME_SOURCE_NATIVE_CONTEXT_IMAGES_AND_BOUNDED_VISUAL_GEOMETRY_WITHOUT_ORIGINAL_FIELD_CERTIFICATION"
 gn=json.loads((ROOT/d["source"]["prior_13gn"]).read_text(encoding="utf8"))
 go=json.loads((ROOT/d["source"]["prior_13go"]).read_text(encoding="utf8"))
 gp=json.loads((ROOT/d["source"]["prior_13gp"]).read_text(encoding="utf8"))
 assert d["source"]["original_pdf_sha256"]==gn["source"]["sha256"]==go["source"]["pdf_sha256"]==gp["source"]["pdf_sha256"]
 assert d["source"]["bytes"]==50735589 and d["source"]["action_status"]=="success"
 assert d["source"]["live_access_run_id"]==40187983221 and d["source"]["artifact_id"]==12597286279
 assert [x["tag"] for x in d["context_panels"]]==["D9","D14","D30"]
 for row in d["context_panels"]:
  p=next(x for x in gn["pages"] if x["page"]==row["page"])
  rect=row["box"]
  assert row["xref"]==p["embedded"]["xref"]
  assert 0<=rect[0]<rect[2]<=p["embedded"]["size"][0]
  assert 0<=rect[1]<rect[3]<=p["embedded"]["size"][1]
  assert row["image_wh"]==[rect[2]-rect[0],rect[3]-rect[1]]
  if row["tag"]=="D9":
   old=next(x for x in go["cases"] if x["target"]=="D9")
   assert covers(rect,old["ratio_projected_xyxy"])
  else:
   old=next(x for x in gp["images"] if x["target"]==row["tag"])
   assert covers(rect,old["source_box"])
  raw=(ROOT/row["image_file"]).read_bytes()
  im=Image.open(io.BytesIO(raw))
  assert im.mode=="RGB" and list(im.size)==row["image_wh"]
  assert len(raw)==row["png_bytes"] and sha(raw)==row["png_sha256"] and sha(im.tobytes())==row["rgb_sha256"]
  assert row["field_identity_certified"] is False and row["exact_ancient_literal"] is None
 assert all(v is None for v in d["unresolved"].values())
 assert d["inspection"]["source_specific_total_numeric_fields_certified"]==0
 assert d["inspection"]["no_ocr"] and d["inspection"]["no_resizing"] and d["inspection"]["no_digit_interpolation"]
 assert d["firewall"]=={"old_D5":"〇/五_UNRESOLVED","G893_six":"OPEN","retracted_13EI":"RETRACTED","new_physical_witnesses":0,"new_independent_sources":0,"algorithm_reopens":0,"candidate_collapses":0,"transmission_edges_added":0}
 assert d["transmission_impact"]["edges_supported"]==d["transmission_impact"]["edges_revised"]==[]
 assert d["counts"]=={"matrix":[222,222],"sources":761,"graph":[252,238],"risks":11,"product":"CLOSED"}
 return True
if __name__=="__main__":
 check(json.loads(E.read_text(encoding="utf8")))
 print("13GQ_PASS_SOURCE_NATIVE_CONTEXT_NO_FIELD_PROMOTION")
