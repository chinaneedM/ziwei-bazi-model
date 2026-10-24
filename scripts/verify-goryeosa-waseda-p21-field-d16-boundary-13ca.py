#!/usr/bin/env python3
"""13CA original Waseda field-heading contrast, SHA-bound P21/P23, not a D16 winner."""
import argparse, hashlib, io, json, zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = "docs/research/TIANWEN-13CA-WASEDA-SOLAR-D16-HEADER-FIELD-IDENTITY-BOUNDARY-R1.json"
S = "docs/PROJECT-CURRENT-STATE-R1.json"
L = "docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
EXPECTED = {
 "P21_JIRI_HEAD": ([990,350,1105,670], "d6b2f36509a9e9db04cda0f949b38133ad2b3567da1f366b9048e5b5abdb8271"),
 "P21_FOUR_FIELD_HEADS_AND_RICHA_UNIT": ([895,690,1100,1370], "2a6270912ac3e095a8a9902429d1c27c4d66c2eb3fecf20d5bffb3068fec309c"),
 "P23_D16_DAY_HEADING": ([1395,335,1495,650], "702716e580b9274fe735a425e874ccecdf7f961e8e048866eb89327989afcac5"),
 "P23_D16_NUMERIC_OPEN_SPREAD": ([1360,685,1550,1460], "32856f3bd0728b4b79440263537cd76be8f06aa32abda3e7714a2ac264f1edaf"),
}
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13CA-WASEDA-ORIGINAL-P21-FIELD-HEADER-AND-P23-D16-SCOPE-R1"
 assert e["grade"]=="MANUAL_DIRECT_ORIGINAL_PROVIDER_JPEG_SHA_AND_NATIVE_RGB_ROI_NO_OCR"
 assert e["issue_id"]=="TW-OPEN-0005" and len(e["source_native_rgb_rois"])==4
 assert [r["key"] for r in e["source_native_rgb_rois"]]==list(EXPECTED)
 for r in e["source_native_rgb_rois"]:
  box,sha=EXPECTED[r["key"]]
  assert r["bbox"]==box and r["rgb_sha256"]==sha and r["page"]==(21 if r["key"].startswith("P21") else 23)
 assert e["direct_reading"]["day_index_literal"]=="積日"
 assert e["direct_reading"]["distinct_field_headers"]==["行度","盈縮積","盈縮加分","日差"]
 assert e["direct_reading"]["rical_unit_literal"]=="日差加一秒八十六少"
 assert e["direct_reading"]["jiri_equals_yingsuoji"] is False
 for key in ["jiri_means_cumulative_numeric_C","yingsuoji_global_mechanical_field_identity","G893_shao_wei_equivalent_to_Waseda_richa_unit","G893_vs_Ming1569_original_field_unit_equivalence","winter_summer_field_equivalence"]:
  assert e["direct_reading"][key]=="NOT_PROVEN"
 assert e["direct_reading"]["original_D16_same_day_isolated_yingsuoji"]=="UNBOUND"
 assert e["direct_reading"]["printed_original_D16_C_numeric_value"]=="NOT_ADJUDICATED"
 assert e["same_original_not_new_witness"] is True and e["full_same_day_column_mapping_completed"] is False
 assert all(e["scope"][k]==0 for k in ("new_physical_witnesses","new_independent_stemmatic_votes","new_source_registry_rows","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens"))
 assert e["scope"]["open_research_risks"]==11 and e["scope"]["product"]=="CLOSED"
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 assert s["historical_audit"]["row_count"]==222 and s["historical_audit"]["external_source_registry_total_unique_count"]==s["historical_audit"]["external_source_registry_root_count"]+s["historical_audit"]["external_source_registry_extension_count"]
 assert any(x.startswith("13CA WASEDA") for x in s["historical_audit"]["current_focus"])
 assert l["binding"]["reviewed_state_version"]==s["schema_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN"
 assert any(x.get("revision_id")=="TW-OPEN-0005-SOLAR-HEADER-BOUNDARY-13CA" for x in issue["history"])
 assert any(x.get("id")=="OMISSIONS-13CA-WASEDA-SOLAR-HEADER-20261021" for x in l["checkpoint_log"])
 return True
def replay(e,artifact21,artifact23):
 from PIL import Image
 for page,artifact in [(21,artifact21),(23,artifact23)]:
  spec=e["source"]["p"+str(page)]
  raw=Path(artifact).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==spec["source_zip_sha256"]
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   assert z.testzip() is None
   src=z.read(spec["image_filename"])
   assert hashlib.sha256(src).hexdigest()==spec["original_jpeg_sha256"]
   rgb=Image.open(io.BytesIO(src)).convert("RGB")
   assert list(rgb.size)==e["source"]["image_dimensions"]
   for r in e["source_native_rgb_rois"]:
    if r["page"]==page:
     assert hashlib.sha256(rgb.crop(tuple(r["bbox"])).tobytes()).hexdigest()==r["rgb_sha256"]
 return True
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--artifact21");a.add_argument("--artifact23");args=a.parse_args()
 e,s,l=load(E),load(S),load(L);check(e,s,l)
 if bool(args.artifact21)!=bool(args.artifact23):a.error("both artifacts required")
 if args.artifact21: replay(e,args.artifact21,args.artifact23)
 print("TIANWEN_13CA_ORIGINAL_FIELD_BOUNDARY=PASS")
