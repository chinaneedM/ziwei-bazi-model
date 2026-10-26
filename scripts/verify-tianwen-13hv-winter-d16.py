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
 assert [r["rgb_sha256"] for h in e["holdings"] for r in h["rows"]]==["32862909c8433fe743c9bd7da61a4ed54b46c4496490d30f934cc70b5d08a52d","581d2b22b8b55be17028aaa314432eee0b690ced4e86f22517d05c0e49676719","295a7f1e2ff955c593e6c8e75ed11b592f678fcefb2a3fcd1fc014b6054809e1","f2db39c2900c410303dbb03493420817307001af5b61d2b39e04d6ded2c9d323","9b98af3da4e38d8d96dbf4be956373a7169a883ee87c5abb182cae0bb35f4e73","3faf76423fca12040aaf802792b386a0718c258f0e6856f0bd68862186258f88","8861c06874ea4c62ca726ed9ec250ca3abf42acd9a9a026596213686d2e1eb3e","2a3a6a0a7827b92f6e27143ba69d8bc52d323e4e64f70b0af28e93decce96be2","5430ca780fd18bfb9bdce331cc8e9dbbfea637bd7efeca6ce14c2ee1cb45b8b2"]
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
  assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]and tuple(map(int,s["schema_version"].split("."))) >= (1,875,0)
  assert any(x.startswith("13HV ") for x in s["historical_audit"]["current_focus"])
  assert any(x.startswith("13HV ") for x in s["historical_audit"]["current_focus"]) and l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
  i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  assert i["status"]=="OPEN" and i["priority"]=="P0"
  assert (i["next_action"].startswith("13HV CURRENT ACTION:") or "ARCHIVED 13HV PRIOR ACTION:" in i["next_action"]) and "ARCHIVED 13HU PRIOR ACTION:" in i["next_action"]
  assert any(z.get("revision_id","").startswith("TW-OPEN-0005-13HV-") for z in i["history"])
  assert str(E.relative_to(ROOT)) in i["source_refs"] and l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
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
