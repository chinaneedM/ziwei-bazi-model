#!/usr/bin/env python3
"""13HU: verify three previously registered direct-image solar winter titles without phantom sources."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"docs/research/TIANWEN-13HU-THREE-SOURCE-WINTER-HEADING-PROVENANCE-RECONCILIATION-R1.json"
CG=ROOT/"docs/research/TIANWEN-13CG-GORYEOSA-TWO-HOLDING-ORIGINAL-INITIAL-TABLE-HEADINGS-AND-OBSCURED-DAY0-R1.json"
HT=ROOT/"docs/research/TIANWEN-13HT-NDL991069-CANVAS72-TABLE-HEADING-GLYPH-ERRATUM-R1.json"
def check(e,with_state=True):
 assert e["schema"]=="TIANWEN-13HU-THREE-SOURCE-WINTER-HEADING-PROVENANCE-RECONCILIATION-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 title="大陽冬至前後二象盈初縮末限"
 assert e["observed_heading"]==title
 cg=json.loads(CG.read_text(encoding="utf8"));ht=json.loads(HT.read_text(encoding="utf8"))
 w=e["source_scoped_image_objects"]
 assert len(w)==3 and [x["source"] for x in w]==["NAJ","WASEDA","NDL1909"]
 for row in w[:2]:
  s=cg["sources"][row["source"]];q=next(x for x in cg["original_rgb_rois"] if x["source"]==row["source"] and x["key"]=="SOLAR_TITLE")
  assert row["holding"]==s["holding"] and row["source_url"]==s["provider_item"]
  assert row["original_image_sha256"]==s["original_jpeg_sha256"]
  assert row["pixel_bbox_xyxy"]==q["bbox"] and row["rgb_sha256"]==q["rgb_sha256"]
  assert row["observed_heading"]==q["observed"]==title and row["preexisting_evidence"] is True
 n=w[2]
 assert n["original_image_sha256"]==ht["source"]["source_jpeg_sha256"]
 assert n["pixel_bbox_xyxy"]==ht["source_roi"]["bbox_xyxy"]
 assert n["rgb_sha256"]==ht["source_roi"]["rgb_sha256"]
 assert n["observed_heading"]==ht["corrected_direct_source_reading"]==title
 assert e["physical_holdings"]["matched_title_count"]==3
 assert e["physical_holdings"]["independent_edition_recension_relationship_proven"] is False
 assert e["physical_holdings"]["independent_print_block_relationship_proven"] is False
 assert e["physical_holdings"]["new_independent_historical_votes"]==0
 assert e["family_scope"]["title_same_wording_does_not_prove_direct_copying"] and e["family_scope"]["title_same_wording_does_not_transfer_numeric_fields"]
 assert e["family_scope"]["cross_copy_number_D16"]=="UNREVIEWED_IN_THIS_BATCH"
 assert e["family_scope"]["ndl_1909_printed_D16"]=="五分一三六二"
 assert e["family_scope"]["ndl_1909_arithmetic_counterfactual"]=="五分二三六二"
 assert e["family_scope"]["taiwan_NCL03130_original_summer_D14"] is None
 assert e["residual_priority"]["G893_six"]==e["residual_priority"]["D5_zero_five"]=="OPEN"
 assert e["residual_priority"]["legacy_13ei"]=="RETRACTED"
 assert all(v==0 for v in e["effect"].values())
 assert e["counts"]=={"matrix":[222,222],"sources":761,"graph":[252,238],"open_issues":11,"product":"CLOSED"}
 assert e["transmission_impact"]=="NONE"
 if with_state:
  s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
  l=json.loads((ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf8"))
  assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,s["schema_version"].split("."))) >= (1,874,0)
  assert any(x.startswith("13HU ") for x in s["historical_audit"]["current_focus"])
  assert any(x.startswith("13HU ") for x in s["historical_audit"]["current_focus"])
  assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
  i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  assert i["priority"]=="P0" and i["status"]=="OPEN"
  assert i["next_action"].startswith("13HU CURRENT ACTION:") or "ARCHIVED 13HU PRIOR ACTION:" in i["next_action"]
  assert "ARCHIVED 13HT PRIOR ACTION:" in i["next_action"]
  assert any(h.get("revision_id","").startswith("TW-OPEN-0005-13HU-") for h in i["history"])
  assert str(P.relative_to(ROOT)) in i["source_refs"]
  assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
if __name__=="__main__":
 e=json.loads(P.read_text(encoding="utf8"));check(e)
 print("TIANWEN_13HU_THREE_SOURCE_TITLE_CROSSWALK_PASS")
