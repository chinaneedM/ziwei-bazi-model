#!/usr/bin/env python3
"""13GV: bind visually readable p74 十四日 date label to persistent exact source pixels;
all ancient numerical readings remain absent."""
import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"docs/research/TIANWEN-13GV-NLC-P74-D14-DAYHEADING-VISUAL-SCOPE-R1.json"
def sha(data):return hashlib.sha256(data).hexdigest()
def verify(e):
 assert e["schema"]=="TIANWEN-13GV-NLC-P74-D14-DAYHEADING-VISUAL-SCOPE-R1"
 assert e["evidence_grade"]=="SOURCE_DIGITAL_SURROGATE_BOUND_DAY_HEADING_VISUAL_READING_ONLY"
 assert e["issue_id"]=="TW-OPEN-0005"
 s=e["original_source"]
 gs=json.loads((ROOT/s["last_source_geometry"]).read_text(encoding="utf8"))
 gr=json.loads((ROOT/s["prior_source_roi"]).read_text(encoding="utf8"))
 assert s["pdf_sha256"]==gs["source"]["original_pdf_sha256"]==gr["source"]["pdf_sha256"]
 assert s["permanent_context_path"]==gs["source"]["origin"]==gr["source"]["origin_image"]
 assert s["permanent_context_rgb_sha256"]==gs["source"]["origin_rgb_sha256"]==gr["source"]["origin_image_rgb_sha256"]
 assert s["context_original_embedded_box"]==gr["source"]["origin_image_box"]==[60,185,230,1080]
 assert s["page"]==74 and s["xref"]==291 and s["source_native_pixel_grid"]==[1754,1173]
 im=Image.open(ROOT/s["permanent_context_path"]).convert("RGB")
 assert sha(im.tobytes())==s["permanent_context_rgb_sha256"]
 z=e["bounded_visual_review"]
 prior=next(x for x in gr["d14_nested_existing_source_rois"] if x["role"]=="D14_PRINTED_DAY_HEADING")
 assert z["source_native_xyxy"]==prior["source_xyxy"]==[80,213,171,408]
 assert z["original_rgb_sha256"]==prior["rgb_sha256"]
 box=z["source_native_xyxy"];base=s["context_original_embedded_box"]
 crop=im.crop((box[0]-base[0],box[1]-base[1],box[2]-base[0],box[3]-base[1]))
 assert sha(crop.tobytes())==z["original_rgb_sha256"]
 assert z["visible_label"]=="十四日" and z["field"]=="PRINTED_DAY_HEADER_ONLY"
 assert z["reading_kind"]=="SOURCE_IMAGE_VISUAL_PROVISIONAL_NOT_INDEPENDENT_EDITION_CERTIFICATION"
 assert z["original_printed_day_only"] is True and z["certified_complete_fourfen_numeric_field"] is False
 assert gs["evaluation"]["original_date_heading_literal"] is None and gs["evaluation"]["complete_day14_fourfen"] is None
 for k in ("same_day_fourfen_row","same_day_fourfen_technical_lane","same_day_chudu_technical_lane","same_day_terminal_glyph","historical_fourfen_chudu_unit","old_nlc_day9_fourfen","old_nlc_day30_fourfen","original_printed_physical_folio","copying_layer"):
  assert e["still_unresolved"][k] is None,k
 assert e["still_unresolved"]["old_day5"]=="〇/五_UNRESOLVED" and e["still_unresolved"]["G893_six"]=="OPEN" and e["still_unresolved"]["old_13EI"]=="RETRACTED"
 assert e["prior_13gs_null_preserved"] is True
 assert e["quantitative_guards"]=={"new_independent_original_images":0,"new_physical_copies":0,"source_registry_growth":0,"matrix":[222,222],"source_registry":761,"transmission_graph":[252,238],"omission_issues":11,"algorithm_reopens":0,"candidate_collapses":0,"product":"CLOSED"}
 assert e["transmission_impact"]["edges_supported"]==[] and e["transmission_impact"]["edges_revised"]==[]
 return True
if __name__=="__main__":
 print("13GV_PASS_BOUND_VISUAL_DAY14_HEADER_ONLY_FOURFEN_NULL" if verify(json.loads(P.read_text(encoding="utf8"))) else "FAIL")
