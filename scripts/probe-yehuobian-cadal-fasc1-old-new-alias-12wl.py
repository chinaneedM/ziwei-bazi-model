#!/usr/bin/env python3
"""12WL bounded original Commons fascicle-1 alias replay, no OCR/no paper-print vote."""
import argparse, importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/"scripts/probe-yehuobian-cadal-duplicate-alias-12wc.py"
OLD="File:野獲編(一).djvu"
NEW="File:CADAL02096900 野獲編（一）.djvu"
KNOWN_NEW_SHA="711dc16b17d139612fbe852dc99869bb709b85c161440dfc7618ee1dbd6f38fa"
SOURCE_BOUND=8000000
PAGES=(5,7,10)
ITEMS=(
 {"title":OLD,"label":"old","expected_bytes":2791559},
 {"title":NEW,"label":"new","expected_bytes":2833699,"expected_sha256":KNOWN_NEW_SHA},
)
def load_capture_module():
 spec=importlib.util.spec_from_file_location("tianwen_cadal_12wc",PARENT)
 mod=importlib.util.module_from_spec(spec)
 spec.loader.exec_module(mod)
 return mod
def validate_config(items=ITEMS,pages=PAGES):
 if len(items)!=2 or [x["title"] for x in items]!=[OLD,NEW]:
  raise ValueError("only publicly listed old/new first fascicle Commons aliases allowed")
 if [x["expected_bytes"] for x in items]!=[2791559,2833699]:
  raise ValueError("Commons publicly declared source-byte boundary")
 if items[1].get("expected_sha256")!=KNOWN_NEW_SHA:
  raise ValueError("replay prior exact 12WJ original sha256")
 if pages!=(5,7,10):raise ValueError("fixed selected source paratext pages")
 return True
def execute(output_dir):
 validate_config()
 m=load_capture_module()
 # Keep original bounded HTTPS Wikimedia imageinfo, source SHA1 and actual-byte
 # verification, DJVU signature, no-OCR rendering and image pixel comparisons.
 m.ITEMS=ITEMS
 m.PAGES=PAGES
 m.MAX_SOURCE_BYTES=SOURCE_BOUND
 out=m.execute(output_dir)
 if out["ancient_1827_1869_print_votes"]!=0 or out["physical_copy_identity_bound"] is not False:
  raise ValueError("digital alias is not an independent historical paper witness")
 if out["sources"][1]["sha256"]!=KNOWN_NEW_SHA:
  raise ValueError("old 12WJ source image hash altered")
 out["schema"]="TIANWEN-12WL-CADAL02096900-DUAL-ORIGINAL-SOURCE-IMAGE-REPLAY-R1"
 out["historical_print_impression_bound"]=False
 out["cross_fascicle_cadal02096915_same_paper_copy_proven"]=False
 out["human_paratext_glyph_recollation"]=False
 out["original_1827_1869_juan20_target_leaves_obtained"]=False
 out["registered_source_additions"]=0
 Path(output_dir,"atlas.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 return out
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--output-dir",default="cadal-fasc1-dual-alias-12wl-output")
 a=ap.parse_args()
 try:
  r=execute(a.output_dir)
  print(json.dumps({"status":"ORIGINALS_REPLAYED_DIGITAL_SCOPE_ONLY","sources":[{"label":x["label"],"bytes":x["bytes"],"sha256":x["sha256"],"page_count":x["pages_count"]} for x in r["sources"]],"page_diff":r["selected_pages"],"historical_print_votes":0},ensure_ascii=False))
 except Exception as e:
  d=Path(a.output_dir);d.mkdir(parents=True,exist_ok=True)
  (d/"capture-error.json").write_text(json.dumps({"status":"CAPTURE_FAILED_NO_PRINT_VOTE","error":str(e),"historical_print_votes":0}))
  raise
if __name__=="__main__":main()
