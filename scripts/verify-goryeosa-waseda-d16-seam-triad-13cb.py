#!/usr/bin/env python3
"""13CB: same-copy Waseda p23 folio-seam numeral triad; no global day/field claim."""
import argparse,hashlib,io,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CB-WASEDA-D16-D17-ORIGINAL-FOLIO-SEAM-ARITHMETIC-BOUNDARY-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
EXPECTED=[
 ("P23_LEFT_FOLIO_RIGHT_EDGE_NUMERAL",[1135,680,1175,1410],"39915c512c38efb29fa64b9b97be6528e3144284dd2ce1af74466514dd661fa2"),
 ("P23_INTERFOLIO_SPACING",[1230,320,1395,1500],"eb328b627cb674d64d2aeeb49ec7de39ad1715b8fdefd09d7027c8358a12c7fc"),
 ("P23_D16_LEFT_BOUNDARY",[1360,680,1420,1420],"b199877388bf7fb904ea74312556e19f6970285998080daa9d5c722252b8564a")
]
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13CB-WASEDA-P23-ORIGINAL-FOLIO-SEAM-SOURCE-NUMERALS-AND-BOUNDED-ARITHMETIC-R1"
 assert e["source_grade"]=="ORIGINAL_FIRSTPARTY_JPEG_REPLAY_MANUAL_NATIVE_RGB_TIGHT_LANE_NO_OCR"
 assert e["issue_id"]=="TW-OPEN-0005"
 assert e["source"]["jpeg_sha256"]=="388f3d5dd9e9861f8ce90c304b154edaeaee98614bb12cd3468f957dcde6fc66"
 assert [(x["key"],x["bbox"],x["rgb_sha256"]) for x in e["new_original_rgb_rois"]]==EXPECTED
 assert e["new_original_rgb_rois"][0]["literal"]=="七千五百七十〇六六二四"
 assert e["new_original_rgb_rois"][0]["decimal"]=="7570.6624"
 a=e["local_numeric_identity"]
 assert (a["outer_folio_numeral"],a["printed_day16_long"],a["tightly_bound_day17_cumulative"])==("7570.6624","429.6073","8000.2697")
 assert a["int_units_1e4"]=={"outer":75706624,"long":4296073,"result":80002697}
 assert a["int_units_1e4"]["outer"]+a["int_units_1e4"]["long"]==a["int_units_1e4"]["result"]
 assert a["arithmetic_true"] is True and a["source_specific_only"] is True
 assert a["globally_proven_day_index_or_unit_formula"] is False
 b=e["field_day_binding_boundary"]
 assert b["outer_folio_numeric_is_on_opposite_leaf_from_D16_heading"] is True
 assert b["original_D16_same_day_isolated_yingsuoji"]=="UNBOUND"
 assert b["printed_D16_source_field_winner"]=="UNRESOLVED"
 assert b["signed_historical_D16_C_field_value"]=="NOT_ADJUDICATED"
 assert b["deterministic_product_algorithm_change_authorized"] is False
 assert all(v==0 for k,v in e["scope_firewall"].items() if k.startswith("new_") or k=="algorithm_reopens")
 assert e["scope_firewall"]["open_issues"]==11 and e["scope_firewall"]["product"]=="CLOSED"
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 assert s["historical_audit"]["row_count"]==222 and s["historical_audit"]["external_source_registry_total_unique_count"]==s["historical_audit"]["external_source_registry_root_count"]+s["historical_audit"]["external_source_registry_extension_count"]
 assert any(x.startswith("13CB WASEDA") for x in s["historical_audit"]["current_focus"])
 assert l["binding"]["reviewed_state_version"]==s["schema_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"] in ("13CB", "13CC","13CD","13CE","13CF","13CG") or l["binding"]["latest_research_focus_prefix"]>"13CB"
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN"
 assert any(x.get("revision_id")=="TW-OPEN-0005-WASEDA-FOLIO-SEAM-13CB" for x in issue["history"])
 assert any(x.get("id")=="OMISSIONS-13CB-WASEDA-D16-D17-SEAM-20261021" for x in l["checkpoint_log"])
 return True
def replay(e,path):
 from PIL import Image
 raw=Path(path).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==e["source"]["artifact_zip_sha256"]
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  assert z.testzip() is None
  dat=z.read(e["source"]["artifact_filename"])
  assert hashlib.sha256(dat).hexdigest()==e["source"]["jpeg_sha256"]
  im=Image.open(io.BytesIO(dat)).convert("RGB")
  assert list(im.size)==e["source"]["image_dimensions"]
  for row in e["new_original_rgb_rois"]:
   assert hashlib.sha256(im.crop(tuple(row["bbox"])).tobytes()).hexdigest()==row["rgb_sha256"]
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--artifact");args=p.parse_args()
 e,s,l=load(E),load(S),load(L);check(e,s,l)
 if args.artifact:replay(e,args.artifact)
 print("TIANWEN_13CB_SOURCE_ORIGINAL_FOLIO_SEAM=PASS")
