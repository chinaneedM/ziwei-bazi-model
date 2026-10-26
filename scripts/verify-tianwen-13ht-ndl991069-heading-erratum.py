#!/usr/bin/env python3
"""13HT forward-only correction of NDL1909 table heading glyphs."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13HT-NDL991069-CANVAS72-TABLE-HEADING-GLYPH-ERRATUM-R1.json"
OLD="太陽冬至前後二氣盈初縮末限"
NEW="大陽冬至前後二象盈初縮末限"
def check(e,with_state=True):
 assert e["schema"]=="TIANWEN-13HT-NDL991069-CANVAS72-TABLE-HEADING-GLYPH-ERRATUM-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["source"]["pid"]=="991069"
 assert e["source"]["later_print_year"]==1909 and e["source"]["canvas"]==72
 assert e["source"]["source_jpeg_sha256"]=="83f76e06aad3ab3d8f1c757c69a8d2d8450086acce6baf71d900b1c0d3ade9cd"
 assert e["source_roi"]["bbox_xyxy"]==[660,515,865,1370]
 assert e["source_roi"]["rgb_sha256"]=="b7996e868f289ffff294f05e1196d2515c29ed1ec9b501715bf2d06a9211e311"
 assert e["source_roi"]["method"]=="NO_OCR_NATIVE_RESOLUTION_HUMAN_VISUAL_GLYPH_COLLATION"
 assert e["corrected_direct_source_reading"]==NEW
 assert [x["old"] for x in e["corrected_pairwise_atoms"]]==["太陽","二氣"]
 assert [x["direct"] for x in e["corrected_pairwise_atoms"]]==["大陽","二象"]
 assert len(e["preserved_prior_erroneous_claims"])==3
 for x in e["preserved_prior_erroneous_claims"]:
  assert x["old_literal"]==OLD
  original=json.loads((ROOT/x["record"]).read_text(encoding="utf8"))
  v=original
  for part in x["field"].split("."):v=v[part]
  assert v==OLD, "old immutable research record was silently rewritten"
 n=e["institutional_text_crosscheck"]
 assert n["literal"]==NEW
 assert n["grade"]=="MODERN_INSTITUTIONAL_EDITED_TRANSCRIPTION_NOT_INDEPENDENT_PHYSICAL_PRINT"
 assert n["winter_day16_literal_in_official_text"]=="五分一三六二"
 assert n["winter_day16_arithmetic_candidate"]=="五分二三六二"
 assert n["candidate_not_printed_glyph"] is True
 f=e["firewall"]
 assert f["original_prior_records_immutable"] and f["source_specific_not_global_title_winner"]
 assert f["does_not_disprove_other_recensions"] and f["does_not_set_ancient_technical_unit"]
 assert f["ncl03130_summer_d14_original"] is f["ncl03130_copy_layer"] is None
 assert f["g893_six"]==f["d5_zero_five"]=="OPEN" and f["previous_13ei"]=="RETRACTED"
 assert all(f[k]==0 for k in ("new_physical_witnesses","new_source_registry_entries","new_graph_nodes","new_graph_edges","algorithm_reopens","candidate_collapses"))
 assert e["transmission_impact"]=="NONE"
 assert e["counts"]=={"matrix":[222,222],"sources":761,"graph":[252,238],"issues":11,"product":"CLOSED"}
 if with_state:
  s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
  l=json.loads((ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf8"))
  assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]=="1.873.0"
  assert l["binding"]["latest_research_focus_prefix"]=="13HT"
  assert s["historical_audit"]["current_focus"][-1].startswith("13HT ")
  assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
  issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  assert issue["priority"]=="P0" and issue["status"]=="OPEN"
  assert issue["next_action"].startswith("13HT CURRENT ACTION:")
  assert "ARCHIVED 13HS PRIOR ACTION:" in issue["next_action"]
  assert issue["history"][-1]["revision_id"].startswith("TW-OPEN-0005-13HT-")
  assert str(E.relative_to(ROOT)) in issue["source_refs"]
  assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
def replay(e,fp):
 from PIL import Image
 assert hashlib.sha256(Path(fp).read_bytes()).hexdigest()==e["source"]["source_jpeg_sha256"]
 with Image.open(fp) as image:
  rgb=image.convert("RGB")
  assert list(rgb.size)==e["source"]["source_dimensions"]
  assert hashlib.sha256(rgb.crop(tuple(e["source_roi"]["bbox_xyxy"])).tobytes()).hexdigest()==e["source_roi"]["rgb_sha256"]
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--jpeg");a=p.parse_args()
 e=json.loads(E.read_text(encoding="utf8"));assert check(e)
 if a.jpeg:assert replay(e,a.jpeg)
 print("TIANWEN_13HT_NDL1909_TABLE_HEADING_FORWARD_ERRATUM_PASS")
