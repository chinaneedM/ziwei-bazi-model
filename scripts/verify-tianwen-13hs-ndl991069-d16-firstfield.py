#!/usr/bin/env python3
"""13HS: source-bound 1909 late received-print arithmetic anomaly; no correction of original."""
import argparse, hashlib, io, json, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13HS-NDL991069-1909-D12-D17-FIRSTFIELD-ANOMALY-R1.json"
def check(e, with_state=True):
 assert e["schema"]=="TIANWEN-13HS-NDL991069-1909-D12-D17-FIRSTFIELD-ANOMALY-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["source"]["pid"]=="991069"
 assert e["source"]["edition_year"]==1909 and e["source"]["canvas"]==73
 assert e["source"]["source_jpeg_sha256"]=="c5fc1b3aeff9aedb84bc36fff02fad2a865e7c86c9fd1e624f7f18a548f945bb"
 assert e["source"]["image_dimensions"]==[3773,2943]
 assert e["source"]["artifact_zip_sha256"]=="5fa5a8d197238794d16ed5c3e37e33fe5d74b4838d4d51da27195548c42935e9"
 assert e["local_original_context"]=="太陽冬至前後二氣盈初縮末限"
 assert e["printed_first_field_prefix"]=="五分"
 rows=e["rows"]
 assert [r["day"] for r in rows]==["十二日","十三日","十四日","十五日","十六日","十七日"]
 assert [r["printed_literal"] for r in rows]==["五分一六一八","五分一八〇四","五分一九九〇","五分二一七六","五分一三六二","五分二五四八"]
 vals=[r["encoded_numeral"] for r in rows]
 assert vals==[1618,1804,1990,2176,1362,2548]
 delta=[vals[i+1]-vals[i] for i in range(5)]
 a=e["arithmetic_control"]
 assert delta==a["adjacent_differences"]==[186,186,186,-814,1186]
 assert a["day16_literal"]==vals[4]==1362
 assert a["day16_if_regular_neighbour_step"]==vals[3]+186==vals[5]-186==2362
 assert a["anomalous_offset"]==vals[4]-a["day16_if_regular_neighbour_step"]==-1000
 assert a["candidate_2362_not_original_glyph"] is True
 assert a["decision"]=="LITERAL_RETAINED_POSSIBLE_RECEIVED_PRINT_OR_TRANSCRIPTION_VARIANT_NOT_PROVEN_HISTORICAL_CORRECTION"
 assert [r["rgb_sha256"] for r in rows]==["766a8599f0519cd62393ff5eb5e3294506ec1fa8bef67667cf6b4e57318c98cf","307055a3d80351c61e22d29592ad1a185ef90b09c7bfa4697f34855a3515a8c6","82cc2fa89e9e810404762e9d1cb6b9c0eed2a9ba0c31b76c6c6819890d1b137d","8861c06874ea4c62ca726ed9ec250ca3abf42acd9a9a026596213686d2e1eb3e","2a3a6a0a7827b92f6e27143ba69d8bc52d323e4e64f70b0af28e93decce96be2","5430ca780fd18bfb9bdce331cc8e9dbbfea637bd7efeca6ce14c2ee1cb45b8b2"]
 assert e["full_context_region"]["rgb_sha256"]=="53e29ef7d515929b9c242ce40b25336e44a5754da370054ffcb9b4984fb1831a"
 for reg in rows+[e["full_context_region"]]:
  x1,y1,x2,y2=reg["original_image_bbox_xyxy"] if "original_image_bbox_xyxy" in reg else reg["bbox_xyxy"]
  assert 0<=x1<x2<=3773 and 0<=y1<y2<=2943
 f=e["firewall"]
 assert f["not_nikh_summer_table"] and f["not_ncl03130_original"]
 assert f["ncl03130_original_d14"] is f["ncl03130_original_d16"] is f["ancient_technical_unit"] is f["early_archetype_decision"] is None
 assert f["g893_six_original"]==f["d5_zero_or_five"]=="OPEN" and f["prior_13ei"]=="RETRACTED"
 assert all(f[k]==0 for k in ("new_independent_physical_witnesses","new_registry_sources","new_graph_nodes","new_graph_edges","algorithm_reopens","candidate_collapses"))
 assert e["counts"]=={"matrix":[222,222],"source_registry":761,"genealogy":[252,238],"open_issues":11,"product":"CLOSED"}
 assert e["transmission_impact"]=="NONE"
 if with_state:
  s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
  l=json.loads((ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf8"))
  assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]and tuple(map(int,s["schema_version"].split("."))) >= (1,872,0)
  assert any(x.startswith("13HS ") for x in s["historical_audit"]["current_focus"])
  assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
  assert any(x.startswith("13HS ") for x in s["historical_audit"]["current_focus"])
  i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  assert i["priority"]=="P0" and i["status"]=="OPEN"
  assert i["next_action"].startswith("13HS CURRENT ACTION:") or "ARCHIVED 13HS PRIOR ACTION:" in i["next_action"]
  assert "ARCHIVED 13HQ PRIOR ACTION:" in i["next_action"]
  assert any(h.get("revision_id","").startswith("TW-OPEN-0005-13HS-") for h in i["history"])
  assert str(E.relative_to(ROOT)) in i["source_refs"]
  assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
def replay_original_jpeg(e,b):
 from PIL import Image
 assert hashlib.sha256(b).hexdigest()==e["source"]["source_jpeg_sha256"]
 with Image.open(io.BytesIO(b)) as im:
  rgb=im.convert("RGB")
  assert list(rgb.size)==e["source"]["image_dimensions"]
  for r in e["rows"]+[e["full_context_region"]]:
   box=r.get("original_image_bbox_xyxy",r.get("bbox_xyxy"))
   assert hashlib.sha256(rgb.crop(tuple(box)).tobytes()).hexdigest()==r["rgb_sha256"]
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--zip");p.add_argument("--jpeg");args=p.parse_args()
 e=json.loads(E.read_text(encoding="utf8"));check(e)
 if args.jpeg: assert replay_original_jpeg(e,Path(args.jpeg).read_bytes())
 if args.zip:
  b=Path(args.zip).read_bytes()
  assert hashlib.sha256(b).hexdigest()==e["source"]["artifact_zip_sha256"]
  with zipfile.ZipFile(io.BytesIO(b)) as z: assert replay_original_jpeg(e,z.read("canvas-073-full-provider.jpg"))
 print("TIANWEN_13HS_NDL1909_D16_LITERAL_ANOMALY_SCOPE_PASS")
