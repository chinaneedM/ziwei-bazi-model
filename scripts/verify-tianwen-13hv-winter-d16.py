#!/usr/bin/env python3
"""Verify source-bound preexisting original winter D15-D17 numerals, no genealogical inflation."""
import argparse,hashlib,json,zipfile,io
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; E=ROOT/"docs/research/TIANWEN-13HV-NAJ-WASEDA-NDL-WINTER-D15-D17-SAME-LITERAL-R1.json"
def check(e, with_state=True):
 assert e["schema"]=="TIANWEN-13HV-THREE-SOURCE-WINTER-D15-D17-R1" and e["issue_id"]=="TW-OPEN-0005"
 assert e["source_title"]=="大陽冬至前後二象盈初縮末限"
 assert e["source_field"]=="日差加一秒八十六少"
 assert [x["source"] for x in e["holdings"]]==["NAJ","WASEDA","NDL1909"]
 old=json.loads((ROOT/e["source_docs"][1]).read_text(encoding="utf8"))
 hs=json.loads((ROOT/e["source_docs"][2]).read_text(encoding="utf8"))
 assert e["holdings"][0]["source_jpeg_sha256"]==old["photos"]["N17"]["original_jpeg_sha256"]
 assert e["holdings"][1]["source_jpeg_sha256"]==old["photos"]["W23"]["original_jpeg_sha256"]
 assert e["holdings"][2]["source_jpeg_sha256"]==hs["source"]["source_jpeg_sha256"]
 for h in e["holdings"]:
  assert [r["day"] for r in h["rows"]]==["十五日","十六日","十七日"]
  assert [r["literal"] for r in h["rows"]]==["五分二一七六","五分一三六二","五分二五四八"]
  assert all(len(r["rgb_sha256"])==64 and 0<=r["bbox_xyxy"][0]<r["bbox_xyxy"][2]<=h["dimensions"][0] and 0<=r["bbox_xyxy"][1]<r["bbox_xyxy"][3]<=h["dimensions"][1] for r in h["rows"])
 assert e["arithmetic"]=={"day15":2176,"day16_printed":1362,"day17":2548,"observed_deltas":[-814,1186],"uniform_186_d16_candidate":2362,"candidate_attested_in_reviewed_images":False}
 f=e["firewall"]
 assert f["no_new_physical_witnesses"] and f["no_new_registered_sources"] and f["no_new_genealogy_edges"] and f["not_unique_to_1909"]
 assert f["copy_printing_independence_proven"] is False and f["ancestor_of_discrepancy_proven"] is False
 assert f["ncl03130_summer_d14"] is f["ncl03130_old_or_supplement"] is None
 assert f["g893_six"]==f["d5_zero_five"]=="OPEN" and f["thirteen_ei"]=="RETRACTED"
 assert f["algorithm_reopens"]==f["candidate_collapses"]==0
 assert e["counts"]=={"matrix":[222,222],"sources":761,"graph":[252,238],"issues":11,"product":"CLOSED"}
 assert e["transmission_impact"]=="NONE"
 if with_state:
  s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
  l=json.loads((ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf8"))
  assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]=="1.875.0"
  assert l["binding"]["latest_research_focus_prefix"]=="13HV"
  assert s["historical_audit"]["current_focus"][-1].startswith("13HV ") and l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
  i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  assert i["status"]=="OPEN" and i["priority"]=="P0"
  assert i["next_action"].startswith("13HV CURRENT ACTION:") and "ARCHIVED 13HU PRIOR ACTION:" in i["next_action"]
  assert i["history"][-1]["revision_id"].startswith("TW-OPEN-0005-13HV-")
  assert str(E.relative_to(ROOT)) in i["source_refs"] and l["checkpoint_log"][-1]["state_version"]=="1.875.0"
 return True
def replay(source,p):
 from PIL import Image
 b=Path(p).read_bytes()
 assert hashlib.sha256(b).hexdigest()==source["archive_zip_sha256"]
 with zipfile.ZipFile(io.BytesIO(b)) as z:raw=z.read(source["member"])
 assert hashlib.sha256(raw).hexdigest()==source["source_jpeg_sha256"]
 with Image.open(io.BytesIO(raw)) as im:
  rgb=im.convert("RGB"); assert list(rgb.size)==source["dimensions"]
  for r in source["rows"]: assert hashlib.sha256(rgb.crop(tuple(r["bbox_xyxy"])).tobytes()).hexdigest()==r["rgb_sha256"]
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser()
 for k in ["najzip","wasedazip","ndlzip"]:p.add_argument("--"+k)
 a=p.parse_args();x=json.loads(E.read_text(encoding="utf8"));check(x)
 for path,source in zip([a.najzip,a.wasedazip,a.ndlzip],x["holdings"]):
  if path:replay(source,path)
 print("TIANWEN_13HV_PREEXISTING_THREE_ORIGINAL_WINTER_D16_PASS")
