#!/usr/bin/env python3
"""13GR: validate day14 nested pixels against durable 13GQ original photo."""
import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];E=ROOT/"docs/research/TIANWEN-13GR-NLC-P74-D12-D14-ORIGINAL-PIXEL-CONTROL-R1.json"
def sha(x):return hashlib.sha256(x).hexdigest()
def check(e):
 assert e["grade"]=="SAME_PDF_DAY12_DAY13_SOURCE_CONTROLS_AND_DAY14_NESTED_ORIGINAL_RGB_NO_NEW_GLYPH"
 s=e["source"]
 gn=json.loads((ROOT/s["prior_13gn"]).read_text(encoding="utf8"))
 gd=json.loads((ROOT/s["prior_13gd"]).read_text(encoding="utf8"))
 gq=json.loads((ROOT/s["prior_13gq"]).read_text(encoding="utf8"))
 assert s["pdf_sha256"]==gn["source"]["sha256"]==gd["source"]["pdf_sha256"]
 assert s["page"]==74 and s["xref"]==291 and s["original_embedded_size"]==[1754,1173]
 assert s["run_id"]==40188885048 and s["action_result"]=="success"
 assert s["artifacts_are_temporary_and_must_not_be_conflated_with_repository_pixels"] is True
 src=next(x for x in gq["context_panels"] if x["tag"]=="D14")
 assert src["box"]==s["origin_image_box"] and src["rgb_sha256"]==s["origin_image_rgb_sha256"]
 im=Image.open(ROOT/s["origin_image"]).convert("RGB")
 assert sha(im.tobytes())==s["origin_image_rgb_sha256"]
 outer=s["origin_image_box"]
 for row in e["d14_nested_existing_source_rois"]:
  b=row["source_xyxy"]
  assert outer[0]<=b[0]<b[2]<=outer[2] and outer[1]<=b[1]<b[3]<=outer[3]
  crop=im.crop((b[0]-outer[0],b[1]-outer[1],b[2]-outer[0],b[3]-outer[1]))
  assert sha(crop.tobytes())==row["rgb_sha256"]
  assert row["original_literal"] is None
 assert [x["day"] for x in e["same_original_positive_controls"]]==[12,13]
 for x in e["same_original_positive_controls"]:
  prior=next(x0 for x0 in gd["positive_source_rows"] if x0["day"]==x["day"])
  assert x["prior_literal"]=="四分"+prior["remainder"]
  assert x["numeric_rgb_sha256"]!=e["d14_nested_existing_source_rois"][0]["rgb_sha256"]
 assert e["full_three_day_source_context"]["repository_blob_archived"] is False
 assert all(e["status"][k] is None for k in ["D14_terminal_original_glyph","D14_complete_source_specific_fourfen","D9_complete_source_specific_fourfen","D30_complete_source_specific_fourfen","historical_unit"])
 assert e["status"]["new_independent_witnesses"]==e["status"]["algorithms_reopened"]==e["status"]["candidates_collapsed"]==0
 assert e["status"]["prior_13EI"]=="RETRACTED" and e["status"]["G893_six"]=="OPEN"
 assert e["counts"]=={"matrix":[222,222],"sources":761,"graph":[252,238],"issues":11,"product":"CLOSED"}
 return True
if __name__=="__main__":
 check(json.loads(E.read_text(encoding="utf8")))
 print("13GR_PASS_NATIVE_D14_GQ_PIXEL_NESTING_AND_D12_D13_CONTROLS_OPEN")
