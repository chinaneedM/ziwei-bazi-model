#!/usr/bin/env python3
"""13LT bounded original source title leaf; NOT Ming shi juan35 or physical date proof."""
import json,re
from pathlib import Path
# Verify historical action text through append-only revisions, not the current instruction.
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
ROOT=Path(__file__).resolve().parents[1]
PATH="docs/research/TIANWEN-13LT-BSB1739-MINGSHI-V2-36-SOURCE-FOLIOS-J51-J46-TITLE-COLLATION-R1.json"
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13LT-BSB1739-MINGSHI-V2-36-SOURCE-FOLIOS-J51-J46-TITLE-COLLATION-R1" and e["issue_id"]=="TW-OPEN-0005"
 a=e["acquisition"];t=e["textual_scope"];c=e["counts"]
 assert a["artifact_id"]==12977811076 and a["workflow_run_id"]==41056970542
 assert a["artifact_zip_sha256"]=="3dd97d5bc9d994f708d8a7982585c98d2bb2b4582333e9aab6f30cf8b3b3edb6"
 assert a["artifact_zip_bytes"]==9229171
 assert a["durable_archive"]["library_file_id"]=="libfile_6bbef08da644819185575c89108c90a5"
 assert a["attempted"]==a["acquired"]==len(a["requested_indices"])==36 and a["no_ocr"] is True
 assert a["all_1880_pages_exhaustively_collated"] is False
 assert [x["canvas_1_based"] for x in a["source_page_title_loci"]]==[1570,1810]
 assert [x["manual_read"] for x in a["source_page_title_loci"]]==["明史卷五十一","明史卷四十六"]
 for x in a["source_page_title_loci"]:
  assert x["status"]=="DIRECT_PROVIDER_IMAGE_GLYPH_POSITIVE"
  for k in ["jpeg_bytes_sha256","decoded_rgb_sha256","title_crop_rgb_sha256"]:
   assert re.fullmatch(r"[0-9a-f]{64}",x[k]),k
  p=x["title_crop_xyxy"];w,h=x["image_px"]
  assert len(p)==4 and 0<=p[0]<p[2]<=w and 0<=p[1]<p[3]<=h
  assert x["source_url"].startswith("https://api.digitale-sammlungen.de/iiif/image/v2/bsb11166692_")
 assert t["target_juan35"]=="NOT_YET_LOCATED" and t["target_juan35_not_present_proven"] is False
 assert t["this_does_not_prove_global_inverse_order"] is True
 assert t["original_238977_09_or_288977_09_new_glyph"]=="NOT_EXAMINED"
 assert t["copy_impression_1739_not_proven"] is True
 assert c==dict(sources=765,matrix_rows=222,matrix_audited=222,graph_nodes=252,graph_edges=238,risks_open=11,g893_historic_six_numeric_winners=0,algorithm_reopens=0,product="CLOSED")
 assert e["transmission_impact"]["edges_supported"]==e["transmission_impact"]["edges_revised"]==[]
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,962,0)
 assert any(x.startswith("13LT ") for x in s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and "13LT CURRENT ACTION:" in historical_action_view(issue)
 assert PATH in issue["source_refs"] and "13LQ CURRENT ACTION:" in historical_action_view(issue)
 assert any(x.get("revision_id")=="TW-OPEN-0005-13LT-BSB-TWO-JUAN-TITLE-20261030" for x in issue["history"])
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 return {"status":"PASS","original_heading_positives":2,"source_images":36,"juan35_location":"OPEN","numeric_winners":0}
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf8")) for p in [PATH,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"])
if __name__=="__main__":print(json.dumps(check(*load()),ensure_ascii=False))
