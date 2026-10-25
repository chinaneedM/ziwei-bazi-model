#!/usr/bin/env python3
"""13GP: hash-bound same-PDF embedded JPEG crop acceptance, no historical glyph upgrade."""
import hashlib,io,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'docs/research/TIANWEN-13GP-NCL03130-EMBEDDED-XOBJECT-ROI-REPLAY-R1.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def covers(a,b):return a[0]<=b[0] and a[1]<=b[1] and a[2]>=b[2] and a[3]>=b[3]
def check(d):
 assert d["grade"]=="EXACT_SOURCE_SHA_AND_PDF_IMAGE_XOBJECT_AFFINE_BOUNDED_NATIVE_RGB_CROPS_NO_FULL_GLYPH"
 g=json.loads((ROOT/d["source"]["prior_13gn"]).read_text(encoding="utf8"))
 o=json.loads((ROOT/d["source"]["prior_13go"]).read_text(encoding="utf8"))
 assert d["source"]["pdf_sha256"]==g["source"]["sha256"]==o["source"]["pdf_sha256"]
 assert d["source"]["pdf_bytes"]==g["source"]["bytes"]==50735589
 assert d["source"]["action_run"]==40187378679 and d["source"]["action_conclusion"]=="success"
 assert d["geometry_evidence"]=="PDF_XOBJECT_AFFINE_GEOMETRY_ONLY_NO_INDEPENDENT_SCRIBAL_LANDMARK_REGISTRATION"
 assert d["source"]["source_independence"]=="SAME_DIGITAL_SURROGATE_NO_NEW_PHYSICAL_WITNESS"
 assert [x["target"] for x in d["images"]]==["D14","D30"]
 for item in d["images"]:
  target=item["target"]
  page=item["page"]
  original=next(x for x in g["pages"] if x["page"]==page)
  prior=next(x for x in o["cases"] if x["target"]==target)
  assert item["xref"]==original["embedded"]["xref"]
  assert item["old_render_box"]==prior["prior_render_union_xyxy"]
  assert item["old_ratio_projection"]==prior["ratio_projected_xyxy"]
  a=item["actual_affine_projection"]
  assert all(abs(a[i]-item["old_ratio_projection"][i])<=2 for i in range(4))
  crop=item["source_box"]
  assert covers(crop,a) and covers(crop,prior["proposed_followup_embedded_probe_xyxy"])
  assert 0<=crop[0]<crop[2]<=original["embedded"]["size"][0]
  assert 0<=crop[1]<crop[3]<=original["embedded"]["size"][1]
  assert item["placement_matrix"][0]>0 and item["placement_matrix"][3]>0
  assert item["placement_rect"][0]==0 and item["placement_rect"][1]==0
  f=ROOT/item["image_file"];b=f.read_bytes()
  im=Image.open(io.BytesIO(b))
  assert im.mode=="RGB" and list(im.size)==item["image_wh"]==[crop[2]-crop[0],crop[3]-crop[1]]
  assert len(b)==item["png_bytes"] and sha(b)==item["png_sha256"]
  assert sha(im.tobytes())==item["rgb_sha256"]
 assert all(v is None for v in d["target_status"].values())
 assert d["no_promotion_guards"]=={"new_physical_witnesses":0,"new_historical_glyph_certifications":0,"registration_is_glyph_independent":False,"old_D5":"〇/五_UNRESOLVED","G893_six":"OPEN","prior_13EI":"RETRACTED","algorithm_reopens":0,"candidate_collapses":0,"source_registry_added":0,"genealogy_edges_added":0}
 assert d["transmission_impact"]["edges_supported"]==d["transmission_impact"]["edges_revised"]==[]
 assert d["counts"]=={"matrix":[222,222],"sources":761,"genealogy":[252,238],"open_or_blocked":11,"product":"CLOSED"}
 return True
if __name__=="__main__":
 check(json.loads(E.read_text(encoding="utf8")));print("13GP_PASS_NATIVE_IMAGE_SHA_XOBJECT_GEOMETRY_NO_GLYPH_PROMOTION")
