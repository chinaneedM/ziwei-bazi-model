#!/usr/bin/env python3
"""13LN exact first-party six-color region acquisition versus historical adjudication firewall."""
import json,re
from pathlib import Path
# Historical source text is validated through immutable issue revisions.
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
ROOT=Path(__file__).resolve().parents[1]
D="docs/research/"
E=D+"TIANWEN-13LN-NAAJ-P7-NATIVE-COLOR-ACQUISITION-AND-SOURCE-SCOPE-R1.json"
M=D+"TIANWEN-13LM-NAAJ-P7-COLOR-OVERVIEW-DISCRIMINATOR-TRIAGE-R1.json"
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in [E,M,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"])
def check(e,m,s,l):
 assert e["schema"]=="TIANWEN-13LN-NAAJ-P7-NATIVE-COLOR-ACQUISITION-AND-SOURCE-SCOPE-R1" and e["no_ocr"] is True
 assert e["prior_batch"]==M
 a=e["acquisition"]
 assert a["head_sha"]=="ee75491951fd8ab7ce484a12a3b6d41805cc92c6"
 assert a["workflow_run_id"]==41049137487 and a["artifact_id"]==12974296262 and a["conclusion"]=="success"
 assert a["artifact_zip_sha256"]=="369e9b6c9bbb54f40210d589c515a20c0a0d2b41dc36ea25a11fff82d71bfd5b"
 assert a["artifact_zip_bytes"]==672871 and a["zip_file_count"]==7
 assert a["library_archive"]["sha256"]==a["artifact_zip_sha256"]
 assert a["library_archive"]["library_file_id"]=="libfile_c16bed342e108191a4b48a70931e3c50"
 assert e["independent_local_replay"]["six_of_six_jpeg_sha_and_rgb_match"] is True
 assert e["independent_local_replay"]["six_of_six_pixels_match"] is True
 assert len(e["controls"])==6 and len(m["targets"])==3
 src={r["holding"]:r for r in m["sources"]}
 seen=set()
 for c in e["controls"]:
  key=(c["holding"],c["target_id"]);assert key not in seen
  seen.add(key)
  t=next(t for t in m["targets"] if t["target_id"]==c["target_id"])
  p=next(p for p in t["positions"] if p["holding"]==c["holding"])
  x,y,xx,yy=p["planned_native_canvas_xyxy"]
  assert c["source_content_id"]==src[c["holding"]]["source_content_id"]
  assert c["native_region_xyxy"]==[x,y,xx,yy]
  assert c["pixels"]==[xx-x,yy-y]
  assert c["url"]==src[c["holding"]]["firstparty_service"]+f"/{x},{y},{xx-x},{yy-y}/{xx-x},/0/native.jpg"
  assert bool(re.fullmatch("[0-9a-f]{64}",c["jpeg_sha256"])) and bool(re.fullmatch("[0-9a-f]{64}",c["rgb_sha256"]))
  assert c["bytes"]>10000 and c["human_reading"]=="PENDING" and c["same_woodblock_proven"] is False
 assert len(seen)==6
 assert len(e["visual_screen_results"])==3
 assert all(x["accidental_unique_woodblock_damage_identified"] is False for x in e["visual_screen_results"])
 adj=e["adjudication"]
 assert adj["new_direct_firstparty_p7_color_regions_acquired"]==6
 for key in ("original_jp2_acquired","unprocessed_raw_photography_acquired","identical_physical_woodblock_proven","specific_ancient_impression_year_proven","unique_accidental_engraving_defect_confirmed","verified_same_historical_edition"):
  assert adj[key] is False,key
 assert adj["independent_historical_recensions_added"]==adj["g893_six_numeric_winners"]==adj["algorithm_reopens"]==0
 assert adj["naaj_harvard_print_literal_retained"]=="238977.09" and adj["cadal_siku_print_literal_retained"]=="288977.09"
 assert adj["chart_product"]=="CLOSED"
 assert e["transmission_impact"]["edges_supported"]==e["transmission_impact"]["edges_revised"]==[]
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 assert tuple(int(x) for x in s["schema_version"].split("."))>=(1,958,0)
 assert any(f.startswith("13LN ") for f in s["historical_audit"]["current_focus"])
 assert l["binding"]["reviewed_state_version"]==s["schema_version"]==l["checkpoint_log"][-1]["state_version"]
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and "13LN CURRENT ACTION:" in historical_action_view(issue)
 assert "13LM CURRENT ACTION:" in historical_action_view(issue) and E in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13LN-NATIVE-COLOR-20261030" for x in issue["history"])
 assert sum(x["status"]=="RESOLVED_WITH_EVIDENCE" for x in l["issues"])==0
 return {"status":"PASS","source_native_jpeg_regions":6,"historical_winners":0,"same_plate_proven":False,"product":"CLOSED"}
if __name__=="__main__":print(json.dumps(check(*load()),ensure_ascii=False))
