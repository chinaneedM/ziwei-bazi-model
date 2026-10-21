#!/usr/bin/env python3
"""13CC NAJ two original source canvases, tight RGB glyphs, source bounded arithmetic."""
import argparse, hashlib, io, json, zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CC-NAJ-GORYEOSA-D17-D18-CANVAS-SEAM-AND-CUMULATIVE-FIELD-BOUNDARY-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
ROIS=[
 (17,"NAJ_C17_D17_ORIGINAL_HEADER",[410,500,515,825],"4c6bad9be3e636e3e1a2ea53b387b6d1fd03dc8d1beb31ea15d4742107083d33"),
 (17,"NAJ_C17_NUMERAL_7570_TIGHT",[565,920,609,1790],"c116eeca76b57ce002bde5761ae4cc77380bf1b472a056a9ea4a58a163571e2a"),
 (17,"NAJ_C17_LAYOUT_CONTEXT",[390,460,720,1820],"ec5cc6759c1093f300da59574577e113c6b04a58a4749c6918f8a4f71ad7aa49"),
 (18,"NAJ_C18_D18_ORIGINAL_HEADER",[2350,520,2465,815],"09a8f78fe2446bad31a689db2e339cc1a508de357c125bd39c92dd9e249cc257"),
 (18,"NAJ_C18_C8000_TIGHT",[2490,827,2552,1760],"433e8d3aab7170282c8bb94dd6e42acc7e1aa6cdb1d09738bd485e7a107ca20b"),
]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13CC-NAJ-ORIGINAL-D17-D18-CANVAS-SEAM-AND-LOCAL-NUMERIC-COUNTEREXAMPLE-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 assert e["evidence_grade"]=="DIRECT_MANUAL_SOURCE_NATIVE_RGB_TIGHT_ROI_SHA_NO_OCR_EXISTING_FIRSTPARTY_SOURCE_OBJECTS"
 assert e["source"]["holding"]=="NAJ-282-0006-PHYSICAL51"
 assert e["source"]["physical_witness_count"]==1 and e["source"]["digital_image_count"]==2
 assert [ (x["canvas"],x["key"],x["bbox"],x["rgb_sha256"]) for x in e["original_rois"]]==ROIS
 assert [x["reading"] for x in e["original_rois"] if "reading" in x]==["十七日","七千五百七十〇六六二四","十八日","八千〇〇〇二六九七"]
 v=e["firstparty_comparison"];a=v["ten_thousandths_int"]
 assert (a["num_17_candidate"],a["num_18_bound"],a["delta"],a["long_D16"],a["long_D17"])==(75706624,80002697,4296073,4296073,4243711)
 assert a["num_18_bound"]-a["num_17_candidate"]==a["delta"]
 assert a["delta"]==a["long_D16"] and a["delta"]!=a["long_D17"]
 assert v["naive_day17_long_difference_mismatch"]=="5.2362"
 assert v["original_D17_same_day_cumulative_field_fully_adjudicated"] is False
 assert v["independent_original_printed_D16_cumulative_value"]=="UNBOUND"
 assert v["proves_whole_table_day_shift"] is False and v["proves_cross_holding_direct_copying"] is False
 assert v["G893_Ming1569_shared_units"]=="UNPROVEN"
 assert e["source_boundary"]["new_original_copy_witnesses"]==0
 assert all(e["scope_firewall"][k]==0 for k in ("new_physical_witnesses","new_registry_entries","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","new_independent_stemmatic_votes","algorithm_reopens"))
 assert e["scope_firewall"]["open_or_blocked_issues"]==11 and e["scope_firewall"]["product"]=="CLOSED"
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["historical_audit"]["row_count"]==222
 assert s["historical_audit"]["external_source_registry_total_unique_count"]==754
 assert any(x.startswith("13CC NAJ") for x in s["historical_audit"]["current_focus"])
 assert l["binding"]["reviewed_state_version"]==s["schema_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and any(x.get("revision_id")=="TW-OPEN-0005-NAJ-CANVAS-SEAM-13CC" for x in issue["history"])
 assert any(x["id"]=="OMISSIONS-13CC-NAJ-D17-D18-20261021" for x in l["checkpoint_log"])
 return True
def replay(e,p17,p18):
 from PIL import Image
 for idx,path in [(17,p17),(18,p18)]:
  spec=e["source"]["canvas"+str(idx)]
  raw=Path(path).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==spec["archive_zip_sha256"]
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   assert z.testzip() is None
   orig=z.read(spec["filename"])
   assert hashlib.sha256(orig).hexdigest()==spec["original_jpeg_sha256"]
   im=Image.open(io.BytesIO(orig)).convert("RGB")
   assert list(im.size)==e["source"]["native_image_dimensions"]
   for r in e["original_rois"]:
    if r["canvas"]==idx:
     assert hashlib.sha256(im.crop(tuple(r["bbox"])).tobytes()).hexdigest()==r["rgb_sha256"]
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--canvas17");p.add_argument("--canvas18");a=p.parse_args()
 e,s,l=load(E),load(S),load(L);check(e,s,l)
 if bool(a.canvas17)!=bool(a.canvas18):p.error("both firstparty artifact ZIPs required")
 if a.canvas17:replay(e,a.canvas17,a.canvas18)
 print("TIANWEN_13CC_NAJ_CANVAS17_18_BOUNDARY=PASS")
